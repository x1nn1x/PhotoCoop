use crate::messages::layout::utility_types::widget_prelude::*;
use crate::messages::prelude::*;

pub struct LicensesDialog {
	pub localized_commit_year: String,
}

impl DialogLayoutHolder for LicensesDialog {
	const ICON: &'static str = "License12px";
	const TITLE: &'static str = "Licenses";

	fn layout_buttons(&self) -> Layout {
		let widgets = vec![TextButton::new("OK").emphasized(true).on_update(|_| FrontendMessage::DialogClose.into()).widget_instance()];

		Layout(vec![LayoutGroup::row(widgets)])
	}

	fn layout_column_2(&self) -> Layout {
		#[allow(clippy::type_complexity)]
		let button_definitions: &[(&str, &str, fn() -> Message)] = &[
			("Code", "Source Code License", || {
				FrontendMessage::TriggerVisitLink {
					url: photocoop_identity::GRAPHITE_LICENSE_URL.into(),
				}
				.into()
			}),
			("GraphiteLogo", "Branding License", || {
				FrontendMessage::TriggerVisitLink {
					url: "https://graphite.art/license#branding".into(),
				}
				.into()
			}),
			("IconsGrid", "Dependency Licenses", || FrontendMessage::TriggerDisplayThirdPartyLicensesDialog.into()),
		];
		let widgets = button_definitions
			.iter()
			.map(|&(icon, label, message_factory)| TextButton::new(label).icon(icon).flush(true).on_update(move |_| message_factory()).widget_instance())
			.collect();

		Layout(vec![LayoutGroup::column(widgets)])
	}
}

impl LayoutHolder for LicensesDialog {
	fn layout(&self) -> Layout {
		// PHOTOCOOP-HOOK: fork licensing copy; Graphite source license is unchanged.
		let year = &self.localized_commit_year;
		let description = format!(
			"
			PhotoCoop is a fork of Graphite. Graphite source code is\n\
			copyright © {year} Graphite contributors and is available under\n\
			both the MIT and Apache 2.0 licenses.\n\
			\n\
			PhotoCoop logos and icons are original PhotoCoop artwork and\n\
			replace Graphite's proprietary branding.\n\
			\n\
			PhotoCoop is distributed with third-party open source code\n\
			dependencies. See \"Dependency Licenses\" for details.
			"
		);
		let description = description.trim();

		Layout(vec![
			LayoutGroup::row(vec![TextLabel::new(photocoop_identity::licenses_intro()).bold(true).widget_instance()]),
			LayoutGroup::row(vec![TextLabel::new(description).multiline(true).widget_instance()]),
		])
	}
}
