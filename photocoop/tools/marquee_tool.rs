//! PhotoCoop marquee (region selection) tool.
//!
//! Lives in `photocoop/tools/` so Graphite only needs a `#[path]` include plus
//! registration hooks. Behavior follows Photoshop / Photopea / Krita: the
//! rectangle or ellipse is a spatial selection on the current layer. Delete
//! clears content inside it; dragging inside moves that content.

use super::tool_prelude::*;
use crate::consts::{COLOR_OVERLAY_BLACK, COLOR_OVERLAY_BLUE_05, COLOR_OVERLAY_WHITE};
use crate::messages::portfolio::document::graph_operation::transform_utils;
use crate::messages::portfolio::document::graph_operation::utility_types::{ModifyInputsContext, TransformIn};
use crate::messages::portfolio::document::node_graph::document_node_definitions::resolve_proto_node_type;
use crate::messages::portfolio::document::overlays::utility_types::OverlayContext;
use crate::messages::portfolio::document::utility_types::document_metadata::LayerNodeIdentifier;
use crate::messages::portfolio::document::utility_types::network_interface::{FlowType, InputConnector, NodeNetworkInterface};
use crate::messages::portfolio::document::utility_types::nodes::SelectedNodes;
use crate::messages::tool::common_functionality::graph_modification_utils::NodeGraphLayer;
use crate::messages::tool::common_functionality::resize::Resize;
use graph_craft::application_io::resource::ResourceId;
use graph_craft::document::value::TaggedValue;
use graph_craft::document::{NodeId, NodeInput};
use graphene_std::Color;
use graphene_std::raster_types::{BitmapMut, Image};
use graphene_std::renderer::Quad;
use graphene_std::vector::algorithms::shapes::{ellipse_bezpath, rectangle_bezpath};
use graphene_std::vector::misc::BooleanOperation;
use std::collections::HashMap;

const DRAG_THRESHOLD: f64 = 3.;
const STENCIL_MAX: u32 = 4096;

#[derive(Default, ExtractField)]
pub struct MarqueeTool {
	fsm_state: MarqueeToolFsmState,
	data: MarqueeToolData,
	options: MarqueeOptions,
}

#[derive(Clone, Copy, Debug, Default, PartialEq, Eq, serde::Serialize, serde::Deserialize)]
#[cfg_attr(feature = "wasm", derive(tsify::Tsify))]
pub enum MarqueeShape {
	#[default]
	Rectangle,
	Ellipse,
}

#[derive(Clone, Debug, Default)]
struct MarqueeOptions {
	shape: MarqueeShape,
}

#[impl_message(Message, ToolMessage, Marquee)]
#[cfg_attr(feature = "wasm", derive(tsify::Tsify))]
#[derive(PartialEq, Clone, Debug, serde::Serialize, serde::Deserialize)]
pub enum MarqueeToolMessage {
	Abort,
	Overlays { context: OverlayContext },
	PointerDown,
	PointerMove { constrain: Key, center: Key },
	PointerUp { constrain: Key, center: Key },
	Delete,
	CycleShape,
	SetShape { shape: MarqueeShape },
}

impl ToolMetadata for MarqueeTool {
	fn icon_name(&self) -> String {
		"GeneralMarqueeTool".into()
	}
	fn tooltip_label(&self) -> String {
		"Marquee Tool".into()
	}
	fn tooltip_description(&self) -> String {
		"Select a rectangular or elliptical region on the current layer. Delete clears inside it. Drag inside to move that content. Shift constrains to a square or circle. Alt draws from the center."
			.into()
	}
	fn tool_type(&self) -> crate::messages::tool::utility_types::ToolType {
		ToolType::Marquee
	}
}

#[message_handler_data]
impl<'a> MessageHandler<ToolMessage, &mut ToolActionMessageContext<'a>> for MarqueeTool {
	fn process_message(&mut self, message: ToolMessage, responses: &mut VecDeque<Message>, context: &mut ToolActionMessageContext<'a>) {
		match &message {
			ToolMessage::Marquee(MarqueeToolMessage::SetShape { shape }) => {
				self.options.shape = *shape;
				self.send_layout(responses, LayoutTarget::ToolOptions);
				responses.add(OverlaysMessage::Draw);
				return;
			}
			ToolMessage::Marquee(MarqueeToolMessage::CycleShape) if self.fsm_state != MarqueeToolFsmState::Drawing && self.fsm_state != MarqueeToolFsmState::Moving => {
				self.options.shape = match self.options.shape {
					MarqueeShape::Rectangle => MarqueeShape::Ellipse,
					MarqueeShape::Ellipse => MarqueeShape::Rectangle,
				};
				self.send_layout(responses, LayoutTarget::ToolOptions);
				responses.add(OverlaysMessage::Draw);
				return;
			}
			_ => {}
		}

		self.fsm_state.process_event(message, &mut self.data, context, &self.options, responses, false);
	}

	fn actions(&self) -> ActionList {
		let mut common = actions!(MarqueeToolMessageDiscriminant; PointerMove, CycleShape);
		let extra = match self.fsm_state {
			MarqueeToolFsmState::Ready => {
				let mut ready = actions!(MarqueeToolMessageDiscriminant; PointerDown, Abort);
				if self.data.committed.is_some() {
					ready.extend(actions!(MarqueeToolMessageDiscriminant; Delete));
				}
				ready
			}
			MarqueeToolFsmState::Drawing | MarqueeToolFsmState::Moving => actions!(MarqueeToolMessageDiscriminant; PointerUp, Abort),
		};
		common.extend(extra);
		common
	}
}

impl LayoutHolder for MarqueeTool {
	fn layout(&self) -> Layout {
		let shape = RadioInput::new(vec![
			RadioEntryData::new("rectangle")
				.icon("VectorRectangleTool")
				.tooltip_label("Rectangular Marquee")
				.tooltip_description("Drag a rectangle. Shift for a square.")
				.on_update(|_| MarqueeToolMessage::SetShape { shape: MarqueeShape::Rectangle }.into()),
			RadioEntryData::new("ellipse")
				.icon("VectorEllipseTool")
				.tooltip_label("Elliptical Marquee")
				.tooltip_description("Drag an ellipse. Shift for a circle.")
				.on_update(|_| MarqueeToolMessage::SetShape { shape: MarqueeShape::Ellipse }.into()),
		])
		.selected_index(Some(self.options.shape as u32))
		.widget_instance();

		Layout(vec![LayoutGroup::row(vec![shape])])
	}
}

impl ToolTransition for MarqueeTool {
	fn event_to_message_map(&self) -> EventToMessageMap {
		EventToMessageMap {
			tool_abort: Some(MarqueeToolMessage::Abort.into()),
			overlay_provider: Some(|context| MarqueeToolMessage::Overlays { context }.into()),
			..Default::default()
		}
	}
}

#[derive(Clone, Copy, Debug, Default, PartialEq, Eq)]
enum MarqueeToolFsmState {
	#[default]
	Ready,
	Drawing,
	Moving,
}

#[derive(Clone, Copy, Debug)]
struct MarqueeRegion {
	start: DVec2,
	end: DVec2,
	shape: MarqueeShape,
}

impl MarqueeRegion {
	fn min_max(self) -> (DVec2, DVec2) {
		(self.start.min(self.end), self.start.max(self.end))
	}

	fn contains_document_point(self, point: DVec2) -> bool {
		let (min, max) = self.min_max();
		match self.shape {
			MarqueeShape::Rectangle => point.x >= min.x && point.x <= max.x && point.y >= min.y && point.y <= max.y,
			MarqueeShape::Ellipse => {
				let radius = (max - min) / 2.;
				if radius.x.abs() < f64::EPSILON || radius.y.abs() < f64::EPSILON {
					return false;
				}
				let normalized = (point - (min + max) / 2.) / radius;
				normalized.length_squared() <= 1.
			}
		}
	}

	fn translate(&mut self, delta: DVec2) {
		self.start += delta;
		self.end += delta;
	}
}

#[derive(Clone, Debug, Default)]
struct MarqueeToolData {
	draw: Resize,
	committed: Option<MarqueeRegion>,
	previous: Option<MarqueeRegion>,
	last_mouse_viewport: DVec2,
}

impl Fsm for MarqueeToolFsmState {
	type ToolData = MarqueeToolData;
	type ToolOptions = MarqueeOptions;

	fn transition(self, event: ToolMessage, tool_data: &mut Self::ToolData, context: &mut ToolActionMessageContext, options: &Self::ToolOptions, responses: &mut VecDeque<Message>) -> Self {
		let ToolActionMessageContext { document, input, viewport, .. } = context;
		let ToolMessage::Marquee(event) = event else { return self };

		match (self, event) {
			(_, MarqueeToolMessage::Overlays { context: mut overlay_context }) => {
				if let Some((region, start, end)) = live_or_committed_viewport(tool_data, document, input, viewport, options, self) {
					draw_marquee(&mut overlay_context, start, end, region.shape);
				}
				self
			}
			(MarqueeToolFsmState::Ready, MarqueeToolMessage::PointerMove { .. }) => {
				update_marquee_cursor(tool_data, document, input, responses);
				self
			}
			(MarqueeToolFsmState::Ready, MarqueeToolMessage::Delete) => {
				if let Some(region) = tool_data.committed {
					let layers = target_layers(&document.network_interface);
					if !layers.is_empty() {
						responses.add(DocumentMessage::StartTransaction);
						responses.add(GraphOperationMessage::MarqueeRegionEdit {
							layers,
							start: region.start,
							end: region.end,
							ellipse: matches!(region.shape, MarqueeShape::Ellipse),
							lift: false,
							keep_inside: false,
						});
						responses.add(DocumentMessage::EndTransaction);
					}
					responses.add(OverlaysMessage::Draw);
				}
				self
			}
			(MarqueeToolFsmState::Ready, MarqueeToolMessage::PointerDown) => {
				let doc_mouse = document.metadata().document_to_viewport.inverse().transform_point2(input.mouse.position);
				if let Some(region) = tool_data.committed
					&& region.contains_document_point(doc_mouse)
				{
					let layers = target_layers(&document.network_interface);
					if layers.is_empty() {
						return self;
					}
					responses.add(DocumentMessage::StartTransaction);
					responses.add(GraphOperationMessage::MarqueeRegionEdit {
						layers,
						start: region.start,
						end: region.end,
						ellipse: matches!(region.shape, MarqueeShape::Ellipse),
						lift: true,
						keep_inside: false,
					});
					tool_data.last_mouse_viewport = input.mouse.position;
					return MarqueeToolFsmState::Moving;
				}

				tool_data.previous = tool_data.committed;
				tool_data.committed = None;
				tool_data.draw.start(document, input, viewport);
				MarqueeToolFsmState::Drawing
			}
			(MarqueeToolFsmState::Drawing, MarqueeToolMessage::PointerMove { constrain, center }) => {
				let _ = tool_data.draw.calculate_points_ignore_layer(document, input, viewport, center, constrain, false);
				responses.add(OverlaysMessage::Draw);
				self
			}
			(MarqueeToolFsmState::Drawing, MarqueeToolMessage::PointerUp { constrain, center }) => {
				let points = tool_data.draw.calculate_points_ignore_layer(document, input, viewport, center, constrain, false);
				tool_data.draw.cleanup(responses);
				if points[0].distance(points[1]) < DRAG_THRESHOLD {
					tool_data.committed = None;
				} else {
					let to_document = document.metadata().document_to_viewport.inverse();
					tool_data.committed = Some(MarqueeRegion {
						start: to_document.transform_point2(points[0]),
						end: to_document.transform_point2(points[1]),
						shape: options.shape,
					});
				}
				responses.add(OverlaysMessage::Draw);
				MarqueeToolFsmState::Ready
			}
			(MarqueeToolFsmState::Moving, MarqueeToolMessage::PointerMove { .. }) => {
				let delta_viewport = input.mouse.position - tool_data.last_mouse_viewport;
				tool_data.last_mouse_viewport = input.mouse.position;
				if delta_viewport.length_squared() > 0. {
					let delta_document = document.metadata().document_to_viewport.inverse().transform_vector2(delta_viewport);
					if let Some(region) = tool_data.committed.as_mut() {
						region.translate(delta_document);
					}
					let transform = DAffine2::from_translation(delta_viewport);
					let layers = target_layers(&document.network_interface);
					for layer in layers {
						responses.add(GraphOperationMessage::TransformChange {
							layer,
							transform,
							transform_in: TransformIn::Viewport,
							skip_rerender: true,
						});
					}
					responses.add(OverlaysMessage::Draw);
				}
				self
			}
			(MarqueeToolFsmState::Moving, MarqueeToolMessage::PointerUp { .. }) => {
				responses.add(NodeGraphMessage::RunDocumentGraph);
				responses.add(DocumentMessage::EndTransaction);
				responses.add(OverlaysMessage::Draw);
				MarqueeToolFsmState::Ready
			}
			(MarqueeToolFsmState::Drawing, MarqueeToolMessage::Abort) => {
				tool_data.draw.cleanup(responses);
				tool_data.committed = tool_data.previous;
				responses.add(OverlaysMessage::Draw);
				MarqueeToolFsmState::Ready
			}
			(MarqueeToolFsmState::Moving, MarqueeToolMessage::Abort) => {
				responses.add(DocumentMessage::AbortTransaction);
				tool_data.committed = tool_data.previous.or(tool_data.committed);
				responses.add(OverlaysMessage::Draw);
				MarqueeToolFsmState::Ready
			}
			(MarqueeToolFsmState::Ready, MarqueeToolMessage::Abort) => {
				if tool_data.committed.is_some() {
					tool_data.committed = None;
					responses.add(OverlaysMessage::Draw);
				}
				self
			}
			_ => self,
		}
	}

	fn update_hints(&self, responses: &mut VecDeque<Message>) {
		let hint_data = match self {
			MarqueeToolFsmState::Ready => HintData(vec![
				HintGroup(vec![HintInfo::mouse(MouseMotion::LmbDrag, "Draw Marquee")]),
				HintGroup(vec![HintInfo::mouse(MouseMotion::LmbDrag, "Move Selected Content")]),
				HintGroup(vec![HintInfo::keys([Key::Delete], "Clear Inside")]),
				HintGroup(vec![HintInfo::keys([Key::Shift], "Constrain 1:1"), HintInfo::keys([Key::Alt], "From Center")]),
				HintGroup(vec![HintInfo::keys([Key::KeyM], "Cycle Shape"), HintInfo::keys([Key::Escape], "Clear Marquee")]),
			]),
			MarqueeToolFsmState::Drawing => HintData(vec![HintGroup(vec![
				HintInfo::keys([Key::Shift], "Constrain 1:1"),
				HintInfo::keys([Key::Alt], "From Center"),
				HintInfo::keys([Key::Escape], "Cancel").prepend_slash(),
			])]),
			MarqueeToolFsmState::Moving => HintData(vec![HintGroup(vec![HintInfo::keys([Key::Escape], "Cancel").prepend_slash()])]),
		};
		hint_data.send_layout(responses);
	}

	fn update_cursor(&self, responses: &mut VecDeque<Message>) {
		let cursor = match self {
			MarqueeToolFsmState::Moving => MouseCursorIcon::Move,
			_ => MouseCursorIcon::Crosshair,
		};
		responses.add(FrontendMessage::UpdateMouseCursor { cursor });
	}
}

fn update_marquee_cursor(tool_data: &MarqueeToolData, document: &DocumentMessageHandler, input: &InputPreprocessorMessageHandler, responses: &mut VecDeque<Message>) {
	let cursor = if let Some(region) = tool_data.committed {
		let doc_mouse = document.metadata().document_to_viewport.inverse().transform_point2(input.mouse.position);
		if region.contains_document_point(doc_mouse) {
			MouseCursorIcon::Move
		} else {
			MouseCursorIcon::Crosshair
		}
	} else {
		MouseCursorIcon::Crosshair
	};
	responses.add(FrontendMessage::UpdateMouseCursor { cursor });
}

fn live_or_committed_viewport(
	tool_data: &mut MarqueeToolData,
	document: &DocumentMessageHandler,
	input: &InputPreprocessorMessageHandler,
	viewport: &ViewportMessageHandler,
	options: &MarqueeOptions,
	state: MarqueeToolFsmState,
) -> Option<(MarqueeRegion, DVec2, DVec2)> {
	if state == MarqueeToolFsmState::Drawing {
		let points = tool_data.draw.calculate_points_ignore_layer(document, input, viewport, Key::Alt, Key::Shift, false);
		return Some((
			MarqueeRegion {
				start: points[0],
				end: points[1],
				shape: options.shape,
			},
			points[0],
			points[1],
		));
	}

	let region = tool_data.committed?;
	let to_viewport = document.metadata().document_to_viewport;
	Some((region, to_viewport.transform_point2(region.start), to_viewport.transform_point2(region.end)))
}

fn draw_marquee(overlay: &mut OverlayContext, start: DVec2, end: DVec2, shape: MarqueeShape) {
	let min = start.min(end);
	let max = start.max(end);
	if (max - min).length_squared() < 0.5 {
		return;
	}

	match shape {
		MarqueeShape::Rectangle => {
			let quad = Quad::from_box([min, max]);
			overlay.quad(quad, Some(COLOR_OVERLAY_BLUE_05), Some(COLOR_OVERLAY_BLUE_05));
			overlay.dashed_quad(quad, Some(COLOR_OVERLAY_BLACK), None, Some(4.), Some(4.), Some(0.));
			overlay.dashed_quad(quad, Some(COLOR_OVERLAY_WHITE), None, Some(4.), Some(4.), Some(4.));
		}
		MarqueeShape::Ellipse => {
			let center = (min + max) / 2.;
			let radius = (max - min) / 2.;
			overlay.dashed_ellipse(
				center,
				radius.x.abs(),
				radius.y.abs(),
				None,
				None,
				None,
				None,
				Some(COLOR_OVERLAY_BLUE_05),
				Some(COLOR_OVERLAY_BLACK),
				Some(4.),
				Some(4.),
				Some(0.),
			);
			overlay.dashed_ellipse(
				center,
				radius.x.abs(),
				radius.y.abs(),
				None,
				None,
				None,
				None,
				None,
				Some(COLOR_OVERLAY_WHITE),
				Some(4.),
				Some(4.),
				Some(4.),
			);
		}
	}
}

#[derive(Clone, Copy)]
enum MarqueeOp {
	ClearInside,
	KeepInside,
}

fn target_layers(network_interface: &NodeNetworkInterface) -> Vec<LayerNodeIdentifier> {
	// Prefer the shallowest selected layers so a boolean/group from a previous punch stays editable.
	// Do not skip folders: the first delete wraps vector content in a boolean group, and that group
	// must remain a valid marquee target for further punches and moves.
	network_interface
		.shallowest_unique_layers(&[])
		.filter(|&layer| layer != LayerNodeIdentifier::ROOT_PARENT)
		.filter(|&layer| !network_interface.is_artboard(&layer.to_node(), &[]))
		.filter(|&layer| {
			let selected = network_interface.selected_nodes();
			selected.layer_visible(layer, network_interface) && !selected.layer_locked(layer, network_interface)
		})
		.collect()
}

pub(crate) fn apply_marquee_region_edit(
	network_interface: &mut NodeNetworkInterface,
	layers: Vec<LayerNodeIdentifier>,
	start: DVec2,
	end: DVec2,
	ellipse: bool,
	lift: bool,
	keep_inside: bool,
	responses: &mut VecDeque<Message>,
) {
	let region = MarqueeRegion {
		start,
		end,
		shape: if ellipse { MarqueeShape::Ellipse } else { MarqueeShape::Rectangle },
	};
	if lift {
		let mut floating = Vec::new();
		for layer in layers {
			let Some(copy) = duplicate_layer_now(network_interface, layer) else { continue };
			apply_marquee_to_layer(network_interface, layer, region, MarqueeOp::ClearInside, responses);
			apply_marquee_to_layer(network_interface, copy, region, MarqueeOp::KeepInside, responses);
			floating.push(copy);
		}
		if !floating.is_empty() {
			let nodes = floating.iter().map(|layer| layer.to_node()).collect();
			responses.add(NodeGraphMessage::SelectedNodesSet { nodes });
		}
	} else {
		let op = if keep_inside { MarqueeOp::KeepInside } else { MarqueeOp::ClearInside };
		for layer in layers {
			apply_marquee_to_layer(network_interface, layer, region, op, responses);
		}
	}
	responses.add(NodeGraphMessage::RunDocumentGraph);
}

fn apply_marquee_to_layer(network_interface: &mut NodeNetworkInterface, layer: LayerNodeIdentifier, region: MarqueeRegion, op: MarqueeOp, responses: &mut VecDeque<Message>) {
	if NodeGraphLayer::is_raster_layer(layer, network_interface) {
		insert_region_mask(network_interface, layer, region, op, responses);
	} else {
		boolean_region(network_interface, layer, region, op, responses);
	}
}

fn insert_region_mask(network_interface: &mut NodeNetworkInterface, layer: LayerNodeIdentifier, region: MarqueeRegion, op: MarqueeOp, responses: &mut VecDeque<Message>) {
	let Some((min, max)) = stencil_bounds(network_interface, layer, region) else { return };
	let size = max - min;
	if size.x.abs() < 1e-6 || size.y.abs() < 1e-6 {
		return;
	}

	let width = (size.x.abs().ceil() as u32).clamp(1, STENCIL_MAX);
	let height = (size.y.abs().ceil() as u32).clamp(1, STENCIL_MAX);
	let keep_inside = matches!(op, MarqueeOp::KeepInside);
	let mut stencil = Image::new(width, height, if keep_inside { Color::BLACK } else { Color::WHITE });
	for y in 0..height {
		for x in 0..width {
			let document_point = min + DVec2::new((x as f64 + 0.5) / width as f64, (y as f64 + 0.5) / height as f64) * size;
			let inside = region.contains_document_point(document_point);
			let keep = if keep_inside { inside } else { !inside };
			if let Some(pixel) = stencil.get_pixel_mut(x, y) {
				*pixel = if keep { Color::WHITE } else { Color::BLACK };
			}
		}
	}

	let Some(mask_definition) = resolve_proto_node_type(graphene_std::raster_nodes::std_nodes::mask::IDENTIFIER) else {
		return;
	};
	let Some(image_definition) = resolve_proto_node_type(graphene_std::raster_nodes::std_nodes::image::IDENTIFIER) else {
		return;
	};
	let Some(transform_definition) = resolve_proto_node_type(graphene_std::transform_nodes::transform::IDENTIFIER) else {
		return;
	};

	let resource_id = ResourceId::new();
	responses.add(ResourceMessage::StoreEmbedded {
		resource_id,
		data: stencil.to_png().into(),
	});

	let mask_id = NodeId::new();
	network_interface.insert_node(mask_id, mask_definition.default_node_template(), &[]);
	network_interface.insert_node_before_input(&mask_id, &InputConnector::layer_secondary_input(layer.to_node()), &[]);

	let image_node = image_definition.node_template_input_override([Some(NodeInput::value(TaggedValue::Resource(resource_id), false))]);
	let image_id = NodeId::new();
	network_interface.insert_node(image_id, image_node, &[]);

	let transform_id = NodeId::new();
	network_interface.insert_node(transform_id, transform_definition.default_node_template(), &[]);
	network_interface.set_input(&InputConnector::primary_input(transform_id), NodeInput::node(image_id, 0), &[]);
	transform_utils::update_transform(network_interface, &transform_id, DAffine2::from_scale_angle_translation(size, 0., min));
	network_interface.set_input(
		&InputConnector::node(mask_id, graphene_std::raster_nodes::std_nodes::mask::StencilInput),
		NodeInput::node(transform_id, 0),
		&[],
	);
}

fn stencil_bounds(network_interface: &NodeNetworkInterface, layer: LayerNodeIdentifier, region: MarqueeRegion) -> Option<(DVec2, DVec2)> {
	let (region_min, region_max) = region.min_max();
	let [layer_min, layer_max] = network_interface.document_metadata().bounding_box_document(layer).unwrap_or([region_min, region_max]);
	let min = layer_min.min(region_min);
	let max = layer_max.max(region_max);
	Some((min, max))
}

fn boolean_region(network_interface: &mut NodeNetworkInterface, layer: LayerNodeIdentifier, region: MarqueeRegion, op: MarqueeOp, responses: &mut VecDeque<Message>) {
	let Some(parent) = layer.parent(network_interface.document_metadata()) else { return };
	let insert_index = DocumentMessageHandler::get_calculated_insert_index(network_interface.document_metadata(), &SelectedNodes(vec![layer.to_node()]), parent);
	let (min, max) = region.min_max();
	let parent_to_document = if parent == LayerNodeIdentifier::ROOT_PARENT {
		DAffine2::IDENTITY
	} else {
		network_interface.document_metadata().transform_to_document(parent)
	};
	let to_parent = parent_to_document.inverse();
	let local_min = to_parent.transform_point2(min);
	let local_max = to_parent.transform_point2(max);
	let bezpath = match region.shape {
		MarqueeShape::Rectangle => rectangle_bezpath(local_min, local_max),
		MarqueeShape::Ellipse => ellipse_bezpath(local_min, local_max),
	};
	let operation = match op {
		MarqueeOp::ClearInside => BooleanOperation::SubtractFront,
		MarqueeOp::KeepInside => BooleanOperation::Intersect,
	};

	let folder_id = NodeId::new();
	let shape_id = NodeId::new();
	{
		let mut modify_inputs = ModifyInputsContext::new(network_interface, responses);
		let folder = modify_inputs.create_layer(folder_id);
		modify_inputs.insert_boolean_data(operation, folder);
		let shape = modify_inputs.create_layer(shape_id);
		modify_inputs.insert_vector(bezpath, shape, true, true, false);
	}

	let folder = LayerNodeIdentifier::new_unchecked(folder_id);
	let shape = LayerNodeIdentifier::new_unchecked(shape_id);
	network_interface.move_layer_to_stack(folder, parent, insert_index, &[]);
	network_interface.move_layer_to_stack(layer, folder, 1, &[]);
	network_interface.move_layer_to_stack(shape, folder, 0, &[]);
	responses.add(NodeGraphMessage::SelectedNodesSet { nodes: vec![folder_id] });
}

fn duplicate_layer_now(network_interface: &mut NodeNetworkInterface, layer: LayerNodeIdentifier) -> Option<LayerNodeIdentifier> {
	let Some(parent) = layer.parent(network_interface.document_metadata()) else { return None };
	let insert_index = DocumentMessageHandler::get_calculated_insert_index(network_interface.document_metadata(), &SelectedNodes(vec![layer.to_node()]), parent);

	let mut copy_ids = HashMap::new();
	copy_ids.insert(layer.to_node(), NodeId(0));
	network_interface
		.upstream_flow_back_from_nodes(vec![layer.to_node()], &[], FlowType::LayerChildrenUpstreamFlow)
		.enumerate()
		.for_each(|(index, node_id)| {
			copy_ids.insert(node_id, NodeId((index + 1) as u64));
		});

	let nodes = network_interface.copy_nodes(&copy_ids, &[]).collect::<Vec<_>>();
	let new_ids: HashMap<_, _> = nodes.iter().map(|(id, _)| (*id, NodeId::new())).collect();
	let &new_layer_id = new_ids.get(&NodeId(0))?;
	network_interface.insert_node_group(nodes, new_ids, &[]);
	let new_layer = LayerNodeIdentifier::new_unchecked(new_layer_id);
	network_interface.move_layer_to_stack(new_layer, parent, insert_index, &[]);
	Some(new_layer)
}
