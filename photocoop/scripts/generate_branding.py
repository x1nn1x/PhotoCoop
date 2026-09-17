#!/usr/bin/env python3
"""Generate original PhotoCoop branding that uses Graphite's expected filenames.

Run from the repo root:
    python3 photocoop/scripts/generate_branding.py
"""

from __future__ import annotations

import math
import struct
import zlib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "photocoop" / "branding"

INK = "#e8e6e1"
ACCENT = "#2ec4b6"
CORAL = "#ff6b4a"
TEAL_DARK = (14, 42, 50, 255)
TEAL = (46, 196, 182, 255)
CORAL_RGBA = (255, 107, 74, 255)
PAPER = (244, 239, 230, 255)

SVG_FILES = [
	"assets/graphics/graphite-logotype-solid.svg",
	"assets/icon-12px-solid/add.svg",
	"assets/icon-12px-solid/checkmark.svg",
	"assets/icon-12px-solid/clipped.svg",
	"assets/icon-12px-solid/close-x.svg",
	"assets/icon-12px-solid/delay.svg",
	"assets/icon-12px-solid/dot-thick.svg",
	"assets/icon-12px-solid/dot.svg",
	"assets/icon-12px-solid/dropdown-arrow.svg",
	"assets/icon-12px-solid/edit-12px.svg",
	"assets/icon-12px-solid/empty-12px.svg",
	"assets/icon-12px-solid/failure.svg",
	"assets/icon-12px-solid/fullscreen-enter.svg",
	"assets/icon-12px-solid/fullscreen-exit.svg",
	"assets/icon-12px-solid/gradient-spread-clear.svg",
	"assets/icon-12px-solid/gradient-spread-pad.svg",
	"assets/icon-12px-solid/gradient-spread-reflect.svg",
	"assets/icon-12px-solid/gradient-spread-repeat.svg",
	"assets/icon-12px-solid/grid-dotted.svg",
	"assets/icon-12px-solid/grid.svg",
	"assets/icon-12px-solid/info.svg",
	"assets/icon-12px-solid/keyboard-arrow-down.svg",
	"assets/icon-12px-solid/keyboard-arrow-left.svg",
	"assets/icon-12px-solid/keyboard-arrow-right.svg",
	"assets/icon-12px-solid/keyboard-arrow-up.svg",
	"assets/icon-12px-solid/keyboard-backspace.svg",
	"assets/icon-12px-solid/keyboard-command.svg",
	"assets/icon-12px-solid/keyboard-control.svg",
	"assets/icon-12px-solid/keyboard-enter.svg",
	"assets/icon-12px-solid/keyboard-option.svg",
	"assets/icon-12px-solid/keyboard-shift.svg",
	"assets/icon-12px-solid/keyboard-space.svg",
	"assets/icon-12px-solid/keyboard-tab.svg",
	"assets/icon-12px-solid/license-12px.svg",
	"assets/icon-12px-solid/link.svg",
	"assets/icon-12px-solid/overlays.svg",
	"assets/icon-12px-solid/remove.svg",
	"assets/icon-12px-solid/render-mode-normal.svg",
	"assets/icon-12px-solid/render-mode-outline.svg",
	"assets/icon-12px-solid/render-mode-pixels.svg",
	"assets/icon-12px-solid/render-mode-svg.svg",
	"assets/icon-12px-solid/snapping.svg",
	"assets/icon-12px-solid/swap-horizontal.svg",
	"assets/icon-12px-solid/swap-vertical.svg",
	"assets/icon-12px-solid/vertical-ellipsis.svg",
	"assets/icon-12px-solid/warning.svg",
	"assets/icon-12px-solid/window-button-win-close.svg",
	"assets/icon-12px-solid/window-button-win-maximize.svg",
	"assets/icon-12px-solid/window-button-win-minimize.svg",
	"assets/icon-12px-solid/window-button-win-restore-down.svg",
	"assets/icon-12px-solid/working-colors.svg",
	"assets/icon-16px-solid/align-bottom.svg",
	"assets/icon-16px-solid/align-horizontal-center.svg",
	"assets/icon-16px-solid/align-left.svg",
	"assets/icon-16px-solid/align-right.svg",
	"assets/icon-16px-solid/align-top.svg",
	"assets/icon-16px-solid/align-vertical-center.svg",
	"assets/icon-16px-solid/artboard.svg",
	"assets/icon-16px-solid/boolean-difference.svg",
	"assets/icon-16px-solid/boolean-divide.svg",
	"assets/icon-16px-solid/boolean-intersect.svg",
	"assets/icon-16px-solid/boolean-subtract-back.svg",
	"assets/icon-16px-solid/boolean-subtract-front.svg",
	"assets/icon-16px-solid/boolean-union.svg",
	"assets/icon-16px-solid/bug.svg",
	"assets/icon-16px-solid/checkbox-checked.svg",
	"assets/icon-16px-solid/checkbox-unchecked.svg",
	"assets/icon-16px-solid/close-all.svg",
	"assets/icon-16px-solid/close.svg",
	"assets/icon-16px-solid/code.svg",
	"assets/icon-16px-solid/copy.svg",
	"assets/icon-16px-solid/credits.svg",
	"assets/icon-16px-solid/custom-color.svg",
	"assets/icon-16px-solid/cut.svg",
	"assets/icon-16px-solid/data-source-graph.svg",
	"assets/icon-16px-solid/data-source-timeline.svg",
	"assets/icon-16px-solid/data-source-value.svg",
	"assets/icon-16px-solid/deselect-all.svg",
	"assets/icon-16px-solid/edit.svg",
	"assets/icon-16px-solid/empty.svg",
	"assets/icon-16px-solid/expand-fill-stroke.svg",
	"assets/icon-16px-solid/eye-hidden.svg",
	"assets/icon-16px-solid/eye-hide.svg",
	"assets/icon-16px-solid/eye-show.svg",
	"assets/icon-16px-solid/eye-visible.svg",
	"assets/icon-16px-solid/eyedropper.svg",
	"assets/icon-16px-solid/file-export.svg",
	"assets/icon-16px-solid/file-import.svg",
	"assets/icon-16px-solid/file.svg",
	"assets/icon-16px-solid/flip-horizontal.svg",
	"assets/icon-16px-solid/flip-vertical.svg",
	"assets/icon-16px-solid/folder-open.svg",
	"assets/icon-16px-solid/folder.svg",
	"assets/icon-16px-solid/frame-all.svg",
	"assets/icon-16px-solid/frame-selected.svg",
	"assets/icon-16px-solid/graph-view-closed.svg",
	"assets/icon-16px-solid/graph-view-open.svg",
	"assets/icon-16px-solid/graphite-logo.svg",
	"assets/icon-16px-solid/handle-visibility-all.svg",
	"assets/icon-16px-solid/handle-visibility-frontier.svg",
	"assets/icon-16px-solid/handle-visibility-selected.svg",
	"assets/icon-16px-solid/heart.svg",
	"assets/icon-16px-solid/history-redo.svg",
	"assets/icon-16px-solid/history-undo.svg",
	"assets/icon-16px-solid/icons-grid.svg",
	"assets/icon-16px-solid/image.svg",
	"assets/icon-16px-solid/interpolation-blend.svg",
	"assets/icon-16px-solid/interpolation-morph.svg",
	"assets/icon-16px-solid/layer.svg",
	"assets/icon-16px-solid/license.svg",
	"assets/icon-16px-solid/new-layer.svg",
	"assets/icon-16px-solid/node-blur.svg",
	"assets/icon-16px-solid/node-brushwork.svg",
	"assets/icon-16px-solid/node-color-correction.svg",
	"assets/icon-16px-solid/node-gradient.svg",
	"assets/icon-16px-solid/node-imaginate.svg",
	"assets/icon-16px-solid/node-magic-wand.svg",
	"assets/icon-16px-solid/node-mask.svg",
	"assets/icon-16px-solid/node-motion-blur.svg",
	"assets/icon-16px-solid/node-nodes.svg",
	"assets/icon-16px-solid/node-output.svg",
	"assets/icon-16px-solid/node-shape.svg",
	"assets/icon-16px-solid/node-text.svg",
	"assets/icon-16px-solid/node-transform.svg",
	"assets/icon-16px-solid/node.svg",
	"assets/icon-16px-solid/padlock-locked.svg",
	"assets/icon-16px-solid/padlock-unlocked.svg",
	"assets/icon-16px-solid/paste.svg",
	"assets/icon-16px-solid/pin-active.svg",
	"assets/icon-16px-solid/pin-inactive.svg",
	"assets/icon-16px-solid/playback-pause.svg",
	"assets/icon-16px-solid/playback-play.svg",
	"assets/icon-16px-solid/playback-to-end.svg",
	"assets/icon-16px-solid/playback-to-start.svg",
	"assets/icon-16px-solid/random.svg",
	"assets/icon-16px-solid/reload.svg",
	"assets/icon-16px-solid/reset.svg",
	"assets/icon-16px-solid/resync.svg",
	"assets/icon-16px-solid/reverse-radial-gradient-to-left.svg",
	"assets/icon-16px-solid/reverse-radial-gradient-to-right.svg",
	"assets/icon-16px-solid/reverse.svg",
	"assets/icon-16px-solid/save.svg",
	"assets/icon-16px-solid/select-all.svg",
	"assets/icon-16px-solid/select-parent.svg",
	"assets/icon-16px-solid/settings.svg",
	"assets/icon-16px-solid/small-dot.svg",
	"assets/icon-16px-solid/stack-bottom.svg",
	"assets/icon-16px-solid/stack-hollow.svg",
	"assets/icon-16px-solid/stack-lower.svg",
	"assets/icon-16px-solid/stack-raise.svg",
	"assets/icon-16px-solid/stack-reverse.svg",
	"assets/icon-16px-solid/stack.svg",
	"assets/icon-16px-solid/stroke-align-center.svg",
	"assets/icon-16px-solid/stroke-align-inside.svg",
	"assets/icon-16px-solid/stroke-align-outside.svg",
	"assets/icon-16px-solid/stroke-cap-butt.svg",
	"assets/icon-16px-solid/stroke-cap-round.svg",
	"assets/icon-16px-solid/stroke-cap-square.svg",
	"assets/icon-16px-solid/stroke-join-bevel.svg",
	"assets/icon-16px-solid/stroke-join-miter.svg",
	"assets/icon-16px-solid/stroke-join-round.svg",
	"assets/icon-16px-solid/stroke-order-above.svg",
	"assets/icon-16px-solid/stroke-order-below.svg",
	"assets/icon-16px-solid/text-align-center.svg",
	"assets/icon-16px-solid/text-align-left.svg",
	"assets/icon-16px-solid/text-align-right.svg",
	"assets/icon-16px-solid/text-align-spine-away.svg",
	"assets/icon-16px-solid/text-align-spine-towards.svg",
	"assets/icon-16px-solid/text-justify-all.svg",
	"assets/icon-16px-solid/text-justify-center.svg",
	"assets/icon-16px-solid/text-justify-left.svg",
	"assets/icon-16px-solid/text-justify-right.svg",
	"assets/icon-16px-solid/tilt-reset.svg",
	"assets/icon-16px-solid/tilt.svg",
	"assets/icon-16px-solid/transformation-grab.svg",
	"assets/icon-16px-solid/transformation-rotate.svg",
	"assets/icon-16px-solid/transformation-scale.svg",
	"assets/icon-16px-solid/trash.svg",
	"assets/icon-16px-solid/turn-negative-90.svg",
	"assets/icon-16px-solid/turn-positive-90.svg",
	"assets/icon-16px-solid/user-manual.svg",
	"assets/icon-16px-solid/viewport-design-mode.svg",
	"assets/icon-16px-solid/viewport-guide-mode.svg",
	"assets/icon-16px-solid/viewport-select-mode.svg",
	"assets/icon-16px-solid/volunteer.svg",
	"assets/icon-16px-solid/website.svg",
	"assets/icon-16px-solid/working-colors-primary.svg",
	"assets/icon-16px-solid/working-colors-secondary.svg",
	"assets/icon-16px-solid/zoom-1x.svg",
	"assets/icon-16px-solid/zoom-2x.svg",
	"assets/icon-16px-solid/zoom-in.svg",
	"assets/icon-16px-solid/zoom-out.svg",
	"assets/icon-16px-solid/zoom-reset.svg",
	"assets/icon-16px-two-tone/mouse-hint-drag.svg",
	"assets/icon-16px-two-tone/mouse-hint-lmb-double.svg",
	"assets/icon-16px-two-tone/mouse-hint-lmb-drag.svg",
	"assets/icon-16px-two-tone/mouse-hint-lmb.svg",
	"assets/icon-16px-two-tone/mouse-hint-mmb-drag.svg",
	"assets/icon-16px-two-tone/mouse-hint-mmb.svg",
	"assets/icon-16px-two-tone/mouse-hint-none.svg",
	"assets/icon-16px-two-tone/mouse-hint-rmb-double.svg",
	"assets/icon-16px-two-tone/mouse-hint-rmb-drag.svg",
	"assets/icon-16px-two-tone/mouse-hint-rmb.svg",
	"assets/icon-16px-two-tone/mouse-hint-scroll-down.svg",
	"assets/icon-16px-two-tone/mouse-hint-scroll-up.svg",
	"assets/icon-24px-two-tone/general-artboard-tool.svg",
	"assets/icon-24px-two-tone/general-eyedropper-tool.svg",
	"assets/icon-24px-two-tone/general-fill-tool.svg",
	"assets/icon-24px-two-tone/general-gradient-tool.svg",
	"assets/icon-24px-two-tone/general-marquee-tool.svg",
	"assets/icon-24px-two-tone/general-navigate-tool.svg",
	"assets/icon-24px-two-tone/general-select-tool.svg",
	"assets/icon-24px-two-tone/raster-brush-tool.svg",
	"assets/icon-24px-two-tone/raster-clone-tool.svg",
	"assets/icon-24px-two-tone/raster-detail-tool.svg",
	"assets/icon-24px-two-tone/raster-heal-tool.svg",
	"assets/icon-24px-two-tone/raster-imaginate-tool.svg",
	"assets/icon-24px-two-tone/raster-patch-tool.svg",
	"assets/icon-24px-two-tone/raster-relight-tool.svg",
	"assets/icon-24px-two-tone/vector-ellipse-tool.svg",
	"assets/icon-24px-two-tone/vector-freehand-tool.svg",
	"assets/icon-24px-two-tone/vector-line-tool.svg",
	"assets/icon-24px-two-tone/vector-path-tool.svg",
	"assets/icon-24px-two-tone/vector-pen-tool.svg",
	"assets/icon-24px-two-tone/vector-polygon-tool.svg",
	"assets/icon-24px-two-tone/vector-rectangle-tool.svg",
	"assets/icon-24px-two-tone/vector-spline-tool.svg",
	"assets/icon-24px-two-tone/vector-text-tool.svg",
	"app-icons/graphite.svg",
	"favicons/safari-pinned-tab.svg",
]


def svg_doc(size: int | None, inner: str, view: str | None = None) -> str:
	if size is None:
		vb = view or "0 0 24 24"
		return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{vb}" fill="currentColor">{inner}</svg>\n'
	return f'<svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" viewBox="0 0 {size} {size}" fill="currentColor">{inner}</svg>\n'


def glyph(stem: str, size: int) -> str:
	"""Original geometric glyphs. Named after Graphite files so Vite resolution works; artwork is PhotoCoop."""
	s = size
	m = max(1.0, s / 16)
	cx, cy = s / 2, s / 2

	def circle(r, sw=None):
		if sw:
			return f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="currentColor" stroke-width="{sw}"/>'
		return f'<circle cx="{cx}" cy="{cy}" r="{r}"/>'

	def rect(x, y, w, h, r=0):
		return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}"/>'

	def line(x1, y1, x2, y2, sw=1.5):
		return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="currentColor" stroke-width="{sw * m}" stroke-linecap="round"/>'

	def poly(points):
		return f'<polygon points="{points}"/>'

	# Shared primitives
	plus = line(cx, 3 * m, cx, s - 3 * m) + line(3 * m, cy, s - 3 * m, cy)
	minus = line(3 * m, cy, s - 3 * m, cy)
	x_mark = line(4 * m, 4 * m, s - 4 * m, s - 4 * m) + line(s - 4 * m, 4 * m, 4 * m, s - 4 * m)
	check = f'<polyline points="{3.5 * m},{s * 0.52} {s * 0.42},{s * 0.74} {s - 3 * m},{s * 0.28}" fill="none" stroke="currentColor" stroke-width="{1.8 * m}" stroke-linecap="round" stroke-linejoin="round"/>'
	dot = circle(max(1.2, 1.6 * m))
	arrow_down = poly(f"{cx},{s - 3 * m} {4 * m},{6 * m} {s - 4 * m},{6 * m}")
	arrow_up = poly(f"{cx},{3 * m} {4 * m},{s - 6 * m} {s - 4 * m},{s - 6 * m}")
	arrow_left = poly(f"{3 * m},{cy} {s - 6 * m},{4 * m} {s - 6 * m},{s - 4 * m}")
	arrow_right = poly(f"{s - 3 * m},{cy} {6 * m},{4 * m} {6 * m},{s - 4 * m}")
	frame = rect(3 * m, 3 * m, s - 6 * m, s - 6 * m, 1.2 * m)
	frame_stroke = f'<rect x="{3 * m}" y="{3 * m}" width="{s - 6 * m}" height="{s - 6 * m}" rx="{1.2 * m}" fill="none" stroke="currentColor" stroke-width="{1.4 * m}"/>'
	eye = f'<ellipse cx="{cx}" cy="{cy}" rx="{s * 0.38}" ry="{s * 0.22}" fill="none" stroke="currentColor" stroke-width="{1.4 * m}"/>' + circle(s * 0.12)
	grid = "".join(rect(3 * m + col * 4 * m, 3 * m + row * 4 * m, 3 * m, 3 * m, 0.4 * m) for row in range(3) for col in range(3))
	play = poly(f"{5 * m},{3 * m} {s - 3 * m},{cy} {5 * m},{s - 3 * m}")
	pause = rect(4 * m, 3 * m, 3 * m, s - 6 * m, 0.5 * m) + rect(s - 7 * m, 3 * m, 3 * m, s - 6 * m, 0.5 * m)
	mark = (
		f'<rect x="{2.5 * m}" y="{4 * m}" width="{s * 0.52}" height="{s * 0.52}" rx="{2 * m}" fill="none" stroke="currentColor" stroke-width="{1.5 * m}"/>'
		f'<rect x="{s * 0.36}" y="{s * 0.28}" width="{s * 0.52}" height="{s * 0.52}" rx="{2 * m}"/>'
	)

	table = {
		"add": plus,
		"remove": minus,
		"checkmark": check,
		"close-x": x_mark,
		"close": x_mark,
		"close-all": x_mark + f'<rect x="{2 * m}" y="{2 * m}" width="{s - 4 * m}" height="{s - 4 * m}" fill="none" stroke="currentColor" stroke-width="{1.2 * m}"/>',
		"dot": circle(max(1.1, 1.3 * m)),
		"dot-thick": circle(max(1.8, 2.2 * m)),
		"small-dot": circle(max(1.0, 1.1 * m)),
		"dropdown-arrow": arrow_down,
		"keyboard-arrow-down": arrow_down,
		"keyboard-arrow-up": arrow_up,
		"keyboard-arrow-left": arrow_left,
		"keyboard-arrow-right": arrow_right,
		"empty-12px": "",
		"empty": "",
		"info": circle(s * 0.38, 1.4 * m) + rect(cx - 0.7 * m, 5 * m, 1.4 * m, 1.4 * m) + rect(cx - 0.7 * m, 7.5 * m, 1.4 * m, 5 * m),
		"warning": poly(f"{cx},{2.5 * m} {s - 2.5 * m},{s - 2.5 * m} {2.5 * m},{s - 2.5 * m}") + rect(cx - 0.7 * m, 6 * m, 1.4 * m, 4 * m) + rect(cx - 0.7 * m, s - 4.5 * m, 1.4 * m, 1.4 * m),
		"failure": x_mark,
		"grid": grid,
		"grid-dotted": "".join(f'<circle cx="{3.5 * m + c * 4.5 * m}" cy="{3.5 * m + r * 4.5 * m}" r="{0.9 * m}"/>' for r in range(3) for c in range(3)),
		"icons-grid": grid,
		"link": f'<path d="M{5 * m} {s - 5 * m}h{4 * m}v{-4 * m}h{2 * m}L{s - 3 * m} {3 * m}h{-5 * m}v{2 * m}h{2 * m}L{7 * m} {11 * m}H{5 * m}z"/>',
		"overlays": rect(3 * m, 3 * m, s * 0.55, s * 0.55, 1 * m) + f'<rect x="{s * 0.32}" y="{s * 0.32}" width="{s * 0.55}" height="{s * 0.55}" rx="{1 * m}" fill="none" stroke="currentColor" stroke-width="{1.3 * m}"/>',
		"snapping": frame_stroke + circle(1.6 * m),
		"swap-horizontal": line(3 * m, 5 * m, s - 3 * m, 5 * m) + arrow_right.replace(str(cy), str(5 * m))[:0] + line(s - 3 * m, s - 5 * m, 3 * m, s - 5 * m) + poly(f"{s - 3 * m},{5 * m} {s - 7 * m},{3 * m} {s - 7 * m},{7 * m}") + poly(f"{3 * m},{s - 5 * m} {7 * m},{s - 7 * m} {7 * m},{s - 3 * m}"),
		"swap-vertical": poly(f"{cx},{3 * m} {cx - 3 * m},{7 * m} {cx + 3 * m},{7 * m}") + poly(f"{cx},{s - 3 * m} {cx - 3 * m},{s - 7 * m} {cx + 3 * m},{s - 7 * m}") + line(cx, 6 * m, cx, s - 6 * m),
		"vertical-ellipsis": "".join(f'<circle cx="{cx}" cy="{4 * m + i * 4 * m}" r="{1.15 * m}"/>' for i in range(3)),
		"fullscreen-enter": frame_stroke,
		"fullscreen-exit": rect(5 * m, 5 * m, s - 10 * m, s - 10 * m, 1 * m),
		"window-button-win-close": x_mark,
		"window-button-win-maximize": frame_stroke,
		"window-button-win-minimize": minus,
		"window-button-win-restore-down": frame_stroke + f'<rect x="{5 * m}" y="{5 * m}" width="{s - 10 * m}" height="{s - 10 * m}" fill="none" stroke="currentColor" stroke-width="{1.2 * m}"/>',
		"working-colors": f'<circle cx="{cx - 2 * m}" cy="{cy}" r="{s * 0.28}"/>' + f'<circle cx="{cx + 2.5 * m}" cy="{cy}" r="{s * 0.22}" fill="none" stroke="currentColor" stroke-width="{1.3 * m}"/>',
		"working-colors-primary": circle(s * 0.32),
		"working-colors-secondary": circle(s * 0.32, 1.4 * m),
		"align-left": rect(3 * m, 3 * m, 2 * m, s - 6 * m) + rect(6.5 * m, 5 * m, s - 10 * m, 2.2 * m) + rect(6.5 * m, s - 7.2 * m, s * 0.45, 2.2 * m),
		"align-right": rect(s - 5 * m, 3 * m, 2 * m, s - 6 * m) + rect(3 * m, 5 * m, s - 10 * m, 2.2 * m) + rect(s * 0.35, s - 7.2 * m, s * 0.45, 2.2 * m),
		"align-top": rect(3 * m, 3 * m, s - 6 * m, 2 * m) + rect(5 * m, 6.5 * m, 2.2 * m, s - 10 * m) + rect(s - 7.2 * m, 6.5 * m, 2.2 * m, s * 0.45),
		"align-bottom": rect(3 * m, s - 5 * m, s - 6 * m, 2 * m) + rect(5 * m, 3 * m, 2.2 * m, s - 10 * m) + rect(s - 7.2 * m, 3 * m, 2.2 * m, s * 0.45),
		"align-horizontal-center": rect(cx - m, 3 * m, 2 * m, s - 6 * m) + rect(4 * m, 5 * m, s - 8 * m, 2 * m) + rect(6 * m, s - 7 * m, s - 12 * m, 2 * m),
		"align-vertical-center": rect(3 * m, cy - m, s - 6 * m, 2 * m) + rect(5 * m, 4 * m, 2 * m, s - 8 * m) + rect(s - 7 * m, 6 * m, 2 * m, s - 12 * m),
		"text-align-left": "".join(rect(3 * m, 4 * m + i * 3 * m, (s - 6 * m) * (1 if i % 2 == 0 else 0.7), 1.6 * m) for i in range(4)),
		"text-align-right": "".join(rect(3 * m + (0 if i % 2 == 0 else (s - 6 * m) * 0.3), 4 * m + i * 3 * m, (s - 6 * m) * (1 if i % 2 == 0 else 0.7), 1.6 * m) for i in range(4)),
		"text-align-center": "".join(rect(4 * m + (0 if i % 2 == 0 else m), 4 * m + i * 3 * m, s - 8 * m - (0 if i % 2 == 0 else 2 * m), 1.6 * m) for i in range(4)),
		"text-justify-all": "".join(rect(3 * m, 4 * m + i * 3 * m, s - 6 * m, 1.6 * m) for i in range(4)),
		"text-justify-left": "".join(rect(3 * m, 4 * m + i * 3 * m, s - 6 * m if i < 3 else s * 0.5, 1.6 * m) for i in range(4)),
		"text-justify-right": "".join(rect(3 * m if i < 3 else s * 0.4, 4 * m + i * 3 * m, s - 6 * m if i < 3 else s * 0.5, 1.6 * m) for i in range(4)),
		"text-justify-center": "".join(rect(3 * m if i < 3 else 5 * m, 4 * m + i * 3 * m, s - 6 * m if i < 3 else s - 10 * m, 1.6 * m) for i in range(4)),
		"checkbox-checked": frame_stroke + check,
		"checkbox-unchecked": frame_stroke,
		"eye-visible": eye,
		"eye-show": eye,
		"eye-hidden": eye + line(3 * m, s - 4 * m, s - 3 * m, 4 * m),
		"eye-hide": eye + line(3 * m, s - 4 * m, s - 3 * m, 4 * m),
		"file": frame_stroke + line(cx, 6 * m, cx, 10 * m),
		"file-import": frame_stroke + arrow_down,
		"file-export": frame_stroke + arrow_up,
		"folder": f'<path d="M{3 * m} {6 * m}h{4 * m}l{2 * m} {-2 * m}h{s - 12 * m}v{s - 7 * m}H{3 * m}z"/>',
		"folder-open": f'<path d="M{3 * m} {7 * m}h{10 * m}l{2 * m} {s - 10 * m}H{3 * m}z"/>' + f'<path d="M{3 * m} {5 * m}h{4 * m}l{1.5 * m} {-1.5 * m}h{4 * m}" fill="none" stroke="currentColor" stroke-width="{1.2 * m}"/>',
		"save": frame + rect(6 * m, 3 * m, s - 12 * m, 5 * m, 0.6 * m),
		"copy": rect(5 * m, 5 * m, s - 8 * m, s - 8 * m, 1 * m) + f'<rect x="{3 * m}" y="{3 * m}" width="{s - 8 * m}" height="{s - 8 * m}" rx="{1 * m}" fill="none" stroke="currentColor" stroke-width="{1.2 * m}"/>',
		"cut": line(4 * m, 4 * m, s - 4 * m, s - 4 * m) + circle(1.6 * m).replace(f'cx="{cx}"', f'cx="{4.5 * m}"').replace(f'cy="{cy}"', f'cy="{s - 4.5 * m}"') + circle(1.6 * m).replace(f'cx="{cx}"', f'cx="{s - 4.5 * m}"').replace(f'cy="{cy}"', f'cy="{4.5 * m}"'),
		"paste": frame_stroke + rect(6 * m, 3 * m, s - 12 * m, 3 * m, 0.8 * m),
		"trash": f'<path d="M{4 * m} {5 * m}h{s - 8 * m}l{-1.2 * m} {s - 8 * m}H{5.2 * m}z"/>' + rect(6 * m, 3 * m, s - 12 * m, 2 * m, 0.4 * m),
		"settings": circle(s * 0.16) + f'<g fill="none" stroke="currentColor" stroke-width="{1.5 * m}">' + circle(s * 0.34, 1.5 * m) + "</g>",
		"zoom-in": circle(s * 0.28, 1.4 * m) + plus + line(cx + s * 0.22, cy + s * 0.22, s - 3 * m, s - 3 * m),
		"zoom-out": circle(s * 0.28, 1.4 * m) + minus + line(cx + s * 0.22, cy + s * 0.22, s - 3 * m, s - 3 * m),
		"zoom-reset": circle(s * 0.3, 1.4 * m),
		"zoom-1x": circle(s * 0.3, 1.4 * m) + f'<text x="{cx}" y="{cy + 1.2 * m}" text-anchor="middle" font-size="{6 * m}" font-family="Arial" fill="currentColor">1</text>',
		"zoom-2x": circle(s * 0.3, 1.4 * m) + f'<text x="{cx}" y="{cy + 1.2 * m}" text-anchor="middle" font-size="{6 * m}" font-family="Arial" fill="currentColor">2</text>',
		"history-undo": f'<path d="M{s - 4 * m} {11 * m}a{5 * m} {5 * m} 0 1 0 {-0.1 * m} 0" fill="none" stroke="currentColor" stroke-width="{1.5 * m}"/>' + poly(f"{4 * m},{4 * m} {8 * m},{4 * m} {4 * m},{8 * m}"),
		"history-redo": f'<path d="M{4 * m} {11 * m}a{5 * m} {5 * m} 0 1 1 {0.1 * m} 0" fill="none" stroke="currentColor" stroke-width="{1.5 * m}"/>' + poly(f"{s - 4 * m},{4 * m} {s - 8 * m},{4 * m} {s - 4 * m},{8 * m}"),
		"playback-play": play,
		"playback-pause": pause,
		"playback-to-start": rect(3 * m, 4 * m, 2 * m, s - 8 * m) + poly(f"{s - 3 * m},{4 * m} {7 * m},{cy} {s - 3 * m},{s - 4 * m}"),
		"playback-to-end": rect(s - 5 * m, 4 * m, 2 * m, s - 8 * m) + poly(f"{3 * m},{4 * m} {s - 7 * m},{cy} {3 * m},{s - 4 * m}"),
		"padlock-locked": rect(5 * m, 8 * m, s - 10 * m, 6 * m, 1 * m) + f'<path d="M{6 * m} {8 * m}v{-2.5 * m}a{2.5 * m} {2.5 * m} 0 0 1 {s - 12 * m} 0V{8 * m}" fill="none" stroke="currentColor" stroke-width="{1.4 * m}"/>',
		"padlock-unlocked": rect(5 * m, 8 * m, s - 10 * m, 6 * m, 1 * m) + f'<path d="M{6 * m} {8 * m}v{-2.5 * m}a{2.5 * m} {2.5 * m} 0 0 1 {s - 12 * m} 0" fill="none" stroke="currentColor" stroke-width="{1.4 * m}"/>',
		"pin-active": poly(f"{cx},{s - 3 * m} {4 * m},{8 * m} {s - 4 * m},{8 * m}") + circle(1.5 * m).replace(f'cy="{cy}"', f'cy="{5.5 * m}"'),
		"pin-inactive": f'<g fill="none" stroke="currentColor" stroke-width="{1.4 * m}">' + poly(f"{cx},{s - 3 * m} {4 * m},{8 * m} {s - 4 * m},{8 * m}") + "</g>",
		"heart": f'<path d="M{cx} {s - 3.5 * m} C{3 * m} {s * 0.55}, {3 * m} {4 * m}, {cx} {6 * m} C{s - 3 * m} {4 * m}, {s - 3 * m} {s * 0.55}, {cx} {s - 3.5 * m}z"/>',
		"bug": circle(s * 0.22).replace(f'cy="{cy}"', f'cy="{cy - m}"') + rect(cx - 2 * m, cy, 4 * m, 5 * m, 1 * m) + line(3 * m, 5 * m, 6 * m, 7 * m) + line(s - 3 * m, 5 * m, s - 6 * m, 7 * m),
		"code": f'<polyline points="{7 * m},{4 * m} {3 * m},{cy} {7 * m},{s - 4 * m}" fill="none" stroke="currentColor" stroke-width="{1.5 * m}" stroke-linejoin="round"/>' + f'<polyline points="{s - 7 * m},{4 * m} {s - 3 * m},{cy} {s - 7 * m},{s - 4 * m}" fill="none" stroke="currentColor" stroke-width="{1.5 * m}" stroke-linejoin="round"/>',
		"license": frame_stroke + line(5 * m, 7 * m, s - 5 * m, 7 * m) + line(5 * m, 10 * m, s - 6 * m, 10 * m),
		"license-12px": frame_stroke + line(4 * m, 6 * m, s - 4 * m, 6 * m),
		"user-manual": frame_stroke + line(5 * m, 6 * m, s - 5 * m, 6 * m) + line(5 * m, 9 * m, s - 5 * m, 9 * m) + line(5 * m, 12 * m, s - 8 * m, 12 * m),
		"website": circle(s * 0.36, 1.3 * m) + line(cx, 3 * m, cx, s - 3 * m) + f'<ellipse cx="{cx}" cy="{cy}" rx="{s * 0.18}" ry="{s * 0.36}" fill="none" stroke="currentColor" stroke-width="{1.2 * m}"/>',
		"volunteer": f'<circle cx="{cx}" cy="{6 * m}" r="{2.4 * m}"/>' + f'<path d="M{4 * m} {s - 3 * m}v{-4 * m}a{4 * m} {3 * m} 0 0 1 {s - 8 * m} 0v{4 * m}"/>',
		"credits": f'<circle cx="{cx}" cy="{6 * m}" r="{2.2 * m}"/>' + f'<circle cx="{5 * m}" cy="{s - 4 * m}" r="{1.6 * m}"/>' + f'<circle cx="{s - 5 * m}" cy="{s - 4 * m}" r="{1.6 * m}"/>',
		"image": frame_stroke + poly(f"{4 * m},{s - 4 * m} {7 * m},{9 * m} {10 * m},{12 * m} {s - 4 * m},{6 * m} {s - 4 * m},{s - 4 * m}"),
		"layer": rect(4 * m, 8 * m, s - 8 * m, 5 * m, 0.8 * m) + f'<rect x="{5 * m}" y="{5 * m}" width="{s - 10 * m}" height="{5 * m}" rx="{0.8 * m}" fill="none" stroke="currentColor" stroke-width="{1.2 * m}"/>',
		"new-layer": rect(4 * m, 8 * m, s - 8 * m, 5 * m, 0.8 * m) + plus,
		"stack": "".join(rect(4 * m, 4 * m + i * 3.2 * m, s - 8 * m, 2.4 * m, 0.5 * m) for i in range(3)),
		"stack-hollow": "".join(f'<rect x="{4 * m}" y="{4 * m + i * 3.2 * m}" width="{s - 8 * m}" height="{2.4 * m}" rx="{0.5 * m}" fill="none" stroke="currentColor" stroke-width="{1.2 * m}"/>' for i in range(3)),
		"stack-raise": "".join(rect(4 * m, 6 * m + i * 3 * m, s - 8 * m, 2.2 * m, 0.4 * m) for i in range(2)) + arrow_up,
		"stack-lower": "".join(rect(4 * m, 4 * m + i * 3 * m, s - 8 * m, 2.2 * m, 0.4 * m) for i in range(2)) + arrow_down,
		"stack-bottom": rect(4 * m, s - 6 * m, s - 8 * m, 2.4 * m, 0.4 * m) + arrow_down,
		"stack-reverse": line(4 * m, 5 * m, s - 4 * m, s - 5 * m) + line(s - 4 * m, 5 * m, 4 * m, s - 5 * m),
		"node": circle(s * 0.28),
		"node-nodes": circle(s * 0.16).replace(f'cx="{cx}"', f'cx="{5 * m}"') + circle(s * 0.16).replace(f'cx="{cx}"', f'cx="{s - 5 * m}"') + line(6.5 * m, cy, s - 6.5 * m, cy),
		"node-output": circle(s * 0.2) + arrow_right,
		"node-shape": rect(4 * m, 4 * m, s - 8 * m, s - 8 * m, 1.2 * m),
		"node-text": f'<text x="{cx}" y="{cy + 3 * m}" text-anchor="middle" font-size="{10 * m}" font-family="Arial" font-weight="700" fill="currentColor">T</text>',
		"node-blur": circle(s * 0.3, 1.2 * m) + circle(s * 0.16),
		"node-gradient": f'<defs><linearGradient id="g{s}" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="currentColor" stop-opacity="0.2"/><stop offset="1" stop-color="currentColor"/></linearGradient></defs>' + f'<rect x="{3 * m}" y="{3 * m}" width="{s - 6 * m}" height="{s - 6 * m}" rx="{1 * m}" fill="url(#g{s})"/>',
		"node-mask": frame_stroke + circle(s * 0.2),
		"node-transform": frame_stroke + plus,
		"node-color-correction": circle(s * 0.32) + circle(s * 0.14),
		"node-brushwork": f'<path d="M{4 * m} {s - 4 * m} Q{cx} {3 * m} {s - 4 * m} {s - 5 * m}" fill="none" stroke="currentColor" stroke-width="{2 * m}" stroke-linecap="round"/>',
		"node-motion-blur": line(3 * m, cy, s - 3 * m, cy, 2) + line(3 * m, cy - 3 * m, s - 6 * m, cy - 3 * m) + line(5 * m, cy + 3 * m, s - 3 * m, cy + 3 * m),
		"node-magic-wand": line(cx, 3 * m, cx, s - 4 * m) + poly(f"{cx},{3 * m} {cx - 2.5 * m},{7 * m} {cx + 2.5 * m},{7 * m}"),
		"node-imaginate": circle(s * 0.34, 1.3 * m) + f'<circle cx="{cx - 1.5 * m}" cy="{cy - m}" r="{1.2 * m}"/>' + f'<circle cx="{cx + 2 * m}" cy="{cy + 1.5 * m}" r="{0.9 * m}"/>',
		"artboard": frame_stroke,
		"frame-all": frame_stroke + rect(6 * m, 6 * m, s - 12 * m, s - 12 * m, 0.6 * m),
		"frame-selected": frame_stroke + circle(1.4 * m),
		"graph-view-open": circle(s * 0.12).replace(f'cx="{cx}"', f'cx="{5 * m}"').replace(f'cy="{cy}"', f'cy="{5 * m}"') + circle(s * 0.12).replace(f'cx="{cx}"', f'cx="{s - 5 * m}"').replace(f'cy="{cy}"', f'cy="{s - 5 * m}"') + line(6 * m, 6 * m, s - 6 * m, s - 6 * m),
		"graph-view-closed": circle(s * 0.12) + frame_stroke,
		"graphite-logo": mark,
		"select-all": frame_stroke + rect(6 * m, 6 * m, s - 12 * m, s - 12 * m, 0.5 * m),
		"deselect-all": frame_stroke,
		"select-parent": frame_stroke + arrow_up,
		"reset": f'<path d="M{s - 4 * m} {7 * m}a{5 * m} {5 * m} 0 1 0 {0} {2 * m}" fill="none" stroke="currentColor" stroke-width="{1.5 * m}" stroke-linecap="round"/>' + poly(f"{s - 4 * m},{4 * m} {s - 4 * m},{8 * m} {s - 8 * m},{6.5 * m}"),
		"reload": f'<path d="M{s - 4 * m} {7 * m}a{5 * m} {5 * m} 0 1 0 {0} {2 * m}" fill="none" stroke="currentColor" stroke-width="{1.5 * m}" stroke-linecap="round"/>',
		"resync": plus + circle(s * 0.34, 1.3 * m),
		"random": "".join(f'<circle cx="{4.5 * m + (i % 3) * 4 * m}" cy="{4.5 * m + (i // 3) * 4 * m}" r="{1.1 * m}"/>' for i in [0, 2, 4, 6, 8]),
		"reverse": arrow_left + arrow_right,
		"edit": f'<path d="M{4 * m} {s - 4 * m}l{1.5 * m} {-6 * m} {6 * m} {-3 * m} {2 * m} {2 * m} {-6 * m} {3 * m}z"/>',
		"edit-12px": f'<path d="M{3 * m} {s - 3 * m}l{1 * m} {-4 * m} {5 * m} {-2.5 * m} {1.5 * m} {1.5 * m} {-5 * m} {2.5 * m}z"/>',
		"eyedropper": line(5 * m, s - 5 * m, s - 5 * m, 5 * m, 1.8) + circle(1.5 * m).replace(f'cx="{cx}"', f'cx="{s - 5 * m}"').replace(f'cy="{cy}"', f'cy="{5 * m}"'),
		"custom-color": circle(s * 0.34),
		"boolean-union": f'<circle cx="{cx - 2 * m}" cy="{cy}" r="{s * 0.28}"/>' + f'<circle cx="{cx + 2 * m}" cy="{cy}" r="{s * 0.28}"/>',
		"boolean-intersect": f'<circle cx="{cx - 2 * m}" cy="{cy}" r="{s * 0.28}" fill="none" stroke="currentColor" stroke-width="{1.3 * m}"/>' + f'<circle cx="{cx + 2 * m}" cy="{cy}" r="{s * 0.28}"/>',
		"boolean-difference": f'<circle cx="{cx - 2 * m}" cy="{cy}" r="{s * 0.28}"/>' + f'<circle cx="{cx + 2 * m}" cy="{cy}" r="{s * 0.28}" fill="none" stroke="currentColor" stroke-width="{1.3 * m}"/>',
		"boolean-divide": line(3 * m, 3 * m, s - 3 * m, s - 3 * m) + circle(s * 0.28),
		"boolean-subtract-front": f'<rect x="{4 * m}" y="{4 * m}" width="{s * 0.45}" height="{s * 0.45}" rx="{1 * m}"/>' + f'<rect x="{s * 0.38}" y="{s * 0.38}" width="{s * 0.45}" height="{s * 0.45}" rx="{1 * m}" fill="none" stroke="currentColor" stroke-width="{1.3 * m}"/>',
		"boolean-subtract-back": f'<rect x="{4 * m}" y="{4 * m}" width="{s * 0.45}" height="{s * 0.45}" rx="{1 * m}" fill="none" stroke="currentColor" stroke-width="{1.3 * m}"/>' + f'<rect x="{s * 0.38}" y="{s * 0.38}" width="{s * 0.45}" height="{s * 0.45}" rx="{1 * m}"/>',
		"flip-horizontal": rect(3 * m, 4 * m, 4 * m, s - 8 * m) + f'<rect x="{s - 7 * m}" y="{4 * m}" width="{4 * m}" height="{s - 8 * m}" fill="none" stroke="currentColor" stroke-width="{1.3 * m}"/>',
		"flip-vertical": rect(4 * m, 3 * m, s - 8 * m, 4 * m) + f'<rect x="{4 * m}" y="{s - 7 * m}" width="{s - 8 * m}" height="{4 * m}" fill="none" stroke="currentColor" stroke-width="{1.3 * m}"/>',
		"turn-positive-90": f'<path d="M{4 * m} {s - 5 * m}v{-6 * m}h{8 * m}" fill="none" stroke="currentColor" stroke-width="{1.5 * m}"/>' + arrow_right,
		"turn-negative-90": f'<path d="M{s - 4 * m} {s - 5 * m}v{-6 * m}h{-8 * m}" fill="none" stroke="currentColor" stroke-width="{1.5 * m}"/>' + arrow_left,
		"transformation-grab": circle(s * 0.16) + frame_stroke,
		"transformation-rotate": f'<path d="M{s - 4 * m} {8 * m}a{5 * m} {5 * m} 0 1 0 -1 {0}" fill="none" stroke="currentColor" stroke-width="{1.5 * m}"/>',
		"transformation-scale": frame_stroke + rect(s - 6 * m, s - 6 * m, 3 * m, 3 * m),
		"tilt": line(3 * m, s - 5 * m, s - 3 * m, 5 * m),
		"tilt-reset": line(3 * m, cy, s - 3 * m, cy),
		"stroke-align-center": line(3 * m, cy, s - 3 * m, cy, 2.4),
		"stroke-align-inside": rect(4 * m, 4 * m, s - 8 * m, s - 8 * m) + f'<rect x="{6 * m}" y="{6 * m}" width="{s - 12 * m}" height="{s - 12 * m}" fill="none" stroke="currentColor" stroke-width="{1.4 * m}"/>',
		"stroke-align-outside": frame_stroke + rect(6 * m, 6 * m, s - 12 * m, s - 12 * m),
		"stroke-cap-butt": line(4 * m, cy, s - 4 * m, cy, 3),
		"stroke-cap-round": line(4 * m, cy, s - 4 * m, cy, 3) + circle(2 * m).replace(f'cx="{cx}"', f'cx="{s - 4 * m}"'),
		"stroke-cap-square": line(4 * m, cy, s - 4 * m, cy, 3) + rect(s - 6 * m, cy - 2 * m, 4 * m, 4 * m),
		"stroke-join-miter": f'<polyline points="{4 * m},{s - 4 * m} {cx},{4 * m} {s - 4 * m},{s - 4 * m}" fill="none" stroke="currentColor" stroke-width="{1.8 * m}" stroke-linejoin="miter"/>',
		"stroke-join-round": f'<polyline points="{4 * m},{s - 4 * m} {cx},{4 * m} {s - 4 * m},{s - 4 * m}" fill="none" stroke="currentColor" stroke-width="{1.8 * m}" stroke-linejoin="round"/>',
		"stroke-join-bevel": f'<polyline points="{4 * m},{s - 4 * m} {cx},{4 * m} {s - 4 * m},{s - 4 * m}" fill="none" stroke="currentColor" stroke-width="{1.8 * m}" stroke-linejoin="bevel"/>',
		"stroke-order-above": rect(4 * m, 8 * m, s - 8 * m, 5 * m) + line(4 * m, 6 * m, s - 4 * m, 6 * m, 2),
		"stroke-order-below": rect(4 * m, 4 * m, s - 8 * m, 5 * m) + line(4 * m, s - 5 * m, s - 4 * m, s - 5 * m, 2),
		"expand-fill-stroke": frame + f'<rect x="{5 * m}" y="{5 * m}" width="{s - 10 * m}" height="{s - 10 * m}" fill="none" stroke="currentColor" stroke-width="{1.3 * m}"/>',
		"handle-visibility-all": circle(1.4 * m) + circle(1.4 * m).replace(f'cx="{cx}"', f'cx="{5 * m}"') + circle(1.4 * m).replace(f'cx="{cx}"', f'cx="{s - 5 * m}"'),
		"handle-visibility-selected": circle(1.6 * m),
		"handle-visibility-frontier": circle(1.4 * m) + circle(1.4 * m, 1.1 * m).replace(f'cx="{cx}"', f'cx="{s - 5 * m}"'),
		"interpolation-blend": f'<circle cx="{5 * m}" cy="{cy}" r="{2.3 * m}"/>' + f'<circle cx="{s - 5 * m}" cy="{cy}" r="{2.3 * m}" fill="none" stroke="currentColor" stroke-width="{1.3 * m}"/>',
		"interpolation-morph": f'<rect x="{3 * m}" y="{5 * m}" width="{4 * m}" height="{6 * m}"/>' + f'<circle cx="{s - 5 * m}" cy="{cy}" r="{3 * m}" fill="none" stroke="currentColor" stroke-width="{1.3 * m}"/>',
		"keyboard-enter": f'<path d="M{4 * m} {11 * m}h{8 * m}V{5 * m}" fill="none" stroke="currentColor" stroke-width="{1.5 * m}"/>' + arrow_left,
		"keyboard-backspace": arrow_left + rect(s - 5 * m, 5 * m, 2 * m, s - 10 * m),
		"keyboard-tab": arrow_right + line(3 * m, 4 * m, 3 * m, s - 4 * m),
		"keyboard-space": rect(3 * m, cy, s - 6 * m, 3 * m, 0.8 * m),
		"keyboard-shift": arrow_up,
		"keyboard-command": rect(4 * m, 4 * m, 3 * m, 3 * m, 0.8 * m) + rect(s - 7 * m, 4 * m, 3 * m, 3 * m, 0.8 * m) + rect(4 * m, s - 7 * m, 3 * m, 3 * m, 0.8 * m) + rect(s - 7 * m, s - 7 * m, 3 * m, 3 * m, 0.8 * m),
		"keyboard-control": f'<text x="{cx}" y="{cy + 3 * m}" text-anchor="middle" font-size="{7 * m}" font-family="Arial" fill="currentColor">^</text>',
		"keyboard-option": f'<polyline points="{3 * m},{s - 4 * m} {7 * m},{s - 4 * m} {11 * m},{4 * m} {s - 3 * m},{4 * m}" fill="none" stroke="currentColor" stroke-width="{1.4 * m}"/>',
		"delay": circle(s * 0.36, 1.3 * m) + line(cx, cy, cx, 5 * m) + line(cx, cy, s - 5 * m, cy),
		"clipped": frame_stroke + line(3 * m, 3 * m, s - 3 * m, s - 3 * m),
		"render-mode-normal": frame,
		"render-mode-outline": frame_stroke,
		"render-mode-pixels": grid,
		"render-mode-svg": f'<text x="{cx}" y="{cy + 3 * m}" text-anchor="middle" font-size="{6 * m}" font-family="Arial" fill="currentColor">SVG</text>',
		"gradient-spread-pad": rect(3 * m, 5 * m, s - 6 * m, 6 * m, 0.8 * m),
		"gradient-spread-repeat": rect(3 * m, 4 * m, 3.5 * m, 8 * m) + rect(7 * m, 4 * m, 3.5 * m, 8 * m) + rect(11 * m, 4 * m, 2 * m, 8 * m),
		"gradient-spread-reflect": rect(3 * m, 4 * m, 4 * m, 8 * m) + f'<rect x="{8 * m}" y="{4 * m}" width="{5 * m}" height="{8 * m}" fill="none" stroke="currentColor" stroke-width="{1.2 * m}"/>',
		"gradient-spread-clear": frame_stroke,
		"reverse-radial-gradient-to-left": circle(s * 0.3, 1.3 * m) + arrow_left,
		"reverse-radial-gradient-to-right": circle(s * 0.3, 1.3 * m) + arrow_right,
		"data-source-graph": line(3 * m, s - 4 * m, 6 * m, 8 * m) + line(6 * m, 8 * m, 10 * m, 11 * m) + line(10 * m, 11 * m, s - 3 * m, 4 * m),
		"data-source-timeline": line(3 * m, cy, s - 3 * m, cy) + circle(1.3 * m).replace(f'cx="{cx}"', f'cx="{5 * m}"') + circle(1.3 * m) + circle(1.3 * m).replace(f'cx="{cx}"', f'cx="{s - 5 * m}"'),
		"data-source-value": f'<text x="{cx}" y="{cy + 3 * m}" text-anchor="middle" font-size="{9 * m}" font-family="Arial" fill="currentColor">42</text>',
		"viewport-design-mode": frame,
		"viewport-guide-mode": frame_stroke + line(cx, 3 * m, cx, s - 3 * m),
		"viewport-select-mode": frame_stroke + rect(6 * m, 6 * m, s - 12 * m, s - 12 * m, 0.4 * m),
		"text-align-spine-away": line(cx, 3 * m, cx, s - 3 * m) + arrow_left + arrow_right,
		"text-align-spine-towards": line(cx, 3 * m, cx, s - 3 * m) + poly(f"{5 * m},{cy} {8 * m},{cy - 2 * m} {8 * m},{cy + 2 * m}") + poly(f"{s - 5 * m},{cy} {s - 8 * m},{cy - 2 * m} {s - 8 * m},{cy + 2 * m}"),
	}

	if stem in table:
		return table[stem]

	# Mouse hints and tools: two-tone body + accent
	if stem.startswith("mouse-hint"):
		body = f'<rect x="{4 * m}" y="{3 * m}" width="{s - 8 * m}" height="{s - 6 * m}" rx="{3 * m}" fill="currentColor" opacity="0.35"/>'
		if "lmb" in stem:
			body += f'<rect x="{4 * m}" y="{3 * m}" width="{(s - 8 * m) / 2}" height="{6 * m}" rx="{2 * m}"/>'
		elif "rmb" in stem:
			body += f'<rect x="{cx}" y="{3 * m}" width="{(s - 8 * m) / 2}" height="{6 * m}" rx="{2 * m}"/>'
		elif "mmb" in stem:
			body += f'<rect x="{cx - 1.5 * m}" y="{3 * m}" width="{3 * m}" height="{6 * m}" rx="{1 * m}"/>'
		if "drag" in stem:
			body += arrow_right
		if "scroll-up" in stem:
			body += arrow_up
		if "scroll-down" in stem:
			body += arrow_down
		if "double" in stem:
			body += circle(1.1 * m)
		return body

	if stem.endswith("-tool") or "tool" in stem:
		accent = f'<rect x="{3 * m}" y="{3 * m}" width="{s - 6 * m}" height="{s - 6 * m}" rx="{3 * m}" fill="currentColor" opacity="0.28"/>'
		if "marquee" in stem:
			return accent + f'<rect x="{4 * m}" y="{5 * m}" width="{s - 8 * m}" height="{s - 10 * m}" rx="{1 * m}" fill="none" stroke="currentColor" stroke-width="{1.6 * m}" stroke-dasharray="{2.2 * m} {1.6 * m}"/>'
		if "select" in stem:
			return accent + frame_stroke
		if "artboard" in stem:
			return accent + frame_stroke
		if "eyedropper" in stem:
			return accent + line(5 * m, s - 5 * m, s - 5 * m, 5 * m, 1.8)
		if "fill" in stem:
			return accent + circle(s * 0.22)
		if "gradient" in stem:
			return accent + line(4 * m, s - 4 * m, s - 4 * m, 4 * m, 2)
		if "navigate" in stem:
			return accent + arrow_right
		if "brush" in stem:
			return accent + f'<path d="M{5 * m} {s - 4 * m}l{2 * m} {-8 * m} {3 * m} {1 * m} {-2 * m} {8 * m}z"/>'
		if "clone" in stem:
			return accent + copy if False else accent + rect(5 * m, 5 * m, 6 * m, 6 * m) + f'<rect x="{7 * m}" y="{7 * m}" width="{6 * m}" height="{6 * m}" fill="none" stroke="currentColor" stroke-width="{1.2 * m}"/>'
		if "ellipse" in stem:
			return accent + f'<ellipse cx="{cx}" cy="{cy}" rx="{s * 0.28}" ry="{s * 0.2}" fill="none" stroke="currentColor" stroke-width="{1.5 * m}"/>'
		if "rectangle" in stem:
			return accent + frame_stroke
		if "polygon" in stem:
			return accent + poly(f"{cx},{4 * m} {s - 4 * m},{s * 0.38} {s - 6 * m},{s - 4 * m} {6 * m},{s - 4 * m} {4 * m},{s * 0.38}")
		if "line" in stem:
			return accent + line(4 * m, s - 5 * m, s - 4 * m, 5 * m, 2)
		if "pen" in stem:
			return accent + f'<path d="M{5 * m} {s - 4 * m}l{2 * m} {-7 * m} {4 * m} {1.5 * m} {-2 * m} {7 * m}z"/>'
		if "path" in stem:
			return accent + f'<path d="M{4 * m} {s - 5 * m}C{6 * m} {4 * m},{s - 6 * m} {s - 4 * m},{s - 4 * m} {5 * m}" fill="none" stroke="currentColor" stroke-width="{1.6 * m}"/>'
		if "spline" in stem:
			return accent + f'<path d="M{3 * m} {s - 4 * m}C{6 * m} {3 * m},{s - 6 * m} {s - 3 * m},{s - 3 * m} {4 * m}" fill="none" stroke="currentColor" stroke-width="{1.6 * m}"/>'
		if "freehand" in stem:
			return accent + f'<path d="M{4 * m} {12 * m}q{3 * m} {-6 * m} {6 * m} {0} q{3 * m} {5 * m} {6 * m} {-2}" fill="none" stroke="currentColor" stroke-width="{1.6 * m}" stroke-linecap="round"/>'
		if "text" in stem:
			return accent + f'<text x="{cx}" y="{cy + 4 * m}" text-anchor="middle" font-size="{11 * m}" font-family="Arial" font-weight="700" fill="currentColor">A</text>'
		if "heal" in stem or "patch" in stem or "detail" in stem or "relight" in stem or "imaginate" in stem:
			return accent + circle(s * 0.22)
		return accent + mark

	# Fallback: unique but simple monogram from the stem
	letters = "".join(ch for ch in stem.upper().replace("-", "") if ch.isalpha())[:2] or "P"
	h = abs(hash(stem))
	r = 2 + (h % 3)
	return (
		f'<rect x="{2.5 * m}" y="{2.5 * m}" width="{s - 5 * m}" height="{s - 5 * m}" rx="{r * m}" fill="none" stroke="currentColor" stroke-width="{1.4 * m}"/>'
		f'<text x="{cx}" y="{cy + 2.4 * m}" text-anchor="middle" font-size="{7 * m}" font-family="Arial" font-weight="700" fill="currentColor">{letters}</text>'
	)


def logotype_svg() -> str:
	return """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 640 120" fill="currentColor">
  <rect x="8" y="28" width="64" height="64" rx="16" fill="none" stroke="currentColor" stroke-width="6"/>
  <rect x="36" y="44" width="64" height="64" rx="16"/>
  <circle cx="68" cy="76" r="10" fill="none" stroke="currentColor" stroke-width="5"/>
  <text x="124" y="82" font-family="Arial, Helvetica, sans-serif" font-size="64" font-weight="700" letter-spacing="-1.5">PhotoCoop</text>
</svg>
"""


def app_icon_svg() -> str:
	return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512">
  <rect width="512" height="512" rx="112" fill="#0e2a32"/>
  <rect x="86" y="118" width="250" height="250" rx="56" fill="none" stroke="{ACCENT}" stroke-width="28"/>
  <rect x="176" y="176" width="250" height="250" rx="56" fill="{CORAL}"/>
  <circle cx="301" cy="301" r="42" fill="#0e2a32"/>
</svg>
"""


def safari_pin_svg() -> str:
	return """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 16 16">
  <rect x="2" y="3" width="8" height="8" rx="2"/>
  <rect x="6" y="5" width="8" height="8" rx="2"/>
</svg>
"""


def write_png(path: Path, width: int, height: int, pixels: bytes) -> None:
	def chunk(tag: bytes, data: bytes) -> bytes:
		return struct.pack(">I", len(data)) + tag + data + struct.pack(">I", zlib.crc32(tag + data) & 0xFFFFFFFF)

	raw = b"".join(b"\x00" + pixels[y * width * 4 : (y + 1) * width * 4] for y in range(height))
	png = b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", struct.pack(">IIBBBBB", width, height, 8, 6, 0, 0, 0)) + chunk(b"IDAT", zlib.compress(raw, 9)) + chunk(b"IEND", b"")
	path.write_bytes(png)


def blend(dst, src):
	sr, sg, sb, sa = src
	if sa == 0:
		return dst
	dr, dg, db, da = dst
	a = sa / 255
	return (
		int(sr * a + dr * (1 - a)),
		int(sg * a + dg * (1 - a)),
		int(sb * a + db * (1 - a)),
		min(255, int(sa + da * (1 - a))),
	)


def fill_round_rect(buf, w, h, x, y, rw, rh, radius, color):
	for py in range(max(0, int(y)), min(h, int(y + rh) + 1)):
		for px in range(max(0, int(x)), min(w, int(x + rw) + 1)):
			dx = min(px - x, x + rw - px)
			dy = min(py - y, y + rh - py)
			inside = True
			if dx < radius and dy < radius:
				inside = (radius - dx) ** 2 + (radius - dy) ** 2 <= radius * radius
			if inside:
				i = (py * w + px) * 4
				cur = (buf[i], buf[i + 1], buf[i + 2], buf[i + 3])
				r, g, b, a = blend(cur, color)
				buf[i : i + 4] = bytes((r, g, b, a))


def fill_circle(buf, w, h, cx, cy, radius, color):
	r2 = radius * radius
	for py in range(max(0, int(cy - radius)), min(h, int(cy + radius) + 1)):
		for px in range(max(0, int(cx - radius)), min(w, int(cx + radius) + 1)):
			if (px - cx) ** 2 + (py - cy) ** 2 <= r2:
				i = (py * w + px) * 4
				cur = (buf[i], buf[i + 1], buf[i + 2], buf[i + 3])
				r, g, b, a = blend(cur, color)
				buf[i : i + 4] = bytes((r, g, b, a))


def stroke_round_rect(buf, w, h, x, y, rw, rh, radius, color, thickness):
	fill_round_rect(buf, w, h, x, y, rw, rh, radius, color)
	inner = (
		x + thickness,
		y + thickness,
		rw - thickness * 2,
		rh - thickness * 2,
		max(0, radius - thickness),
	)
	fill_round_rect(buf, w, h, *inner, (0, 0, 0, 0) if False else TEAL_DARK)


def render_mark(size: int) -> bytes:
	buf = bytearray(size * size * 4)
	# background
	fill_round_rect(buf, size, size, 0, 0, size, size, size * 0.22, TEAL_DARK)
	unit = size / 512
	stroke_round_rect(buf, size, size, 86 * unit, 118 * unit, 250 * unit, 250 * unit, 56 * unit, TEAL, 28 * unit)
	fill_round_rect(buf, size, size, 176 * unit, 176 * unit, 250 * unit, 250 * unit, 56 * unit, CORAL_RGBA)
	fill_circle(buf, size, size, 301 * unit, 301 * unit, 42 * unit, TEAL_DARK)
	return bytes(buf)


def write_ico(path: Path, png32: bytes) -> None:
	# ICO with a single PNG-compressed 32x32 image
	count = 1
	header = struct.pack("<HHH", 0, 1, count)
	entry = struct.pack("<BBBBHHII", 32, 32, 0, 0, 1, 32, len(png32), 6 + 16)
	path.write_bytes(header + entry + png32)


def write_icns(path: Path, images: dict[int, bytes]) -> None:
	"""Minimal ICNS with PNG icons."""
	chunks = []
	mapping = {16: b"icp4", 32: b"icp5", 64: b"icp6", 128: b"ic07", 256: b"ic08", 512: b"ic09", 1024: b"ic10"}
	for size, png in images.items():
		tag = mapping.get(size)
		if not tag:
			continue
		chunks.append(tag + struct.pack(">I", len(png) + 8) + png)
	body = b"".join(chunks)
	path.write_bytes(b"icns" + struct.pack(">I", len(body) + 8) + body)


def size_from_path(rel: str) -> int | None:
	if "icon-12px" in rel:
		return 12
	if "icon-16px" in rel:
		return 16
	if "icon-24px" in rel:
		return 24
	return None


def main() -> None:
	if OUT.exists():
		for child in OUT.rglob("*"):
			if child.is_file():
				child.unlink()

	for rel in SVG_FILES:
		path = OUT / rel
		path.parent.mkdir(parents=True, exist_ok=True)
		stem = Path(rel).stem
		if rel.endswith("graphite-logotype-solid.svg"):
			path.write_text(logotype_svg())
		elif rel.endswith("graphite.svg") and "app-icons" in rel:
			path.write_text(app_icon_svg())
		elif rel.endswith("safari-pinned-tab.svg"):
			path.write_text(safari_pin_svg())
		else:
			size = size_from_path(rel) or 16
			path.write_text(svg_doc(size, glyph(stem, size)))

	# Raster app icons and favicons
	sizes = [16, 32, 70, 128, 144, 150, 180, 192, 256, 310, 512, 1024]
	rasters = {s: render_mark(s) for s in sizes}

	def png(size: int) -> bytes:
		from io import BytesIO

		bio_path = OUT / f".tmp-{size}.png"
		bio_path.parent.mkdir(parents=True, exist_ok=True)
		write_png(bio_path, size, size, rasters[size])
		data = bio_path.read_bytes()
		bio_path.unlink()
		return data

	png_cache = {s: png(s) for s in sizes}

	app = OUT / "app-icons"
	app.mkdir(parents=True, exist_ok=True)
	write_png(app / "graphite.png", 512, 512, rasters[512])
	write_png(app / "graphite-128.png", 128, 128, rasters[128])
	write_png(app / "graphite-256.png", 256, 256, rasters[256])
	write_png(app / "graphite-512.png", 512, 512, rasters[512])
	write_ico(app / "graphite.ico", png_cache[32])
	write_icns(
		app / "graphite.icns",
		{16: png_cache[16], 32: png_cache[32], 128: png_cache[128], 256: png_cache[256], 512: png_cache[512], 1024: png_cache[1024]},
	)

	fav = OUT / "favicons"
	fav.mkdir(parents=True, exist_ok=True)
	write_png(fav / "favicon-16x16.png", 16, 16, rasters[16])
	write_png(fav / "favicon-32x32.png", 32, 32, rasters[32])
	write_png(fav / "apple-touch-icon.png", 180, 180, rasters[180])
	write_png(fav / "android-chrome-192x192.png", 192, 192, rasters[192])
	write_png(fav / "android-chrome-512x512.png", 512, 512, rasters[512])
	write_png(fav / "mstile-70x70.png", 70, 70, rasters[70])
	write_png(fav / "mstile-144x144.png", 144, 144, rasters[144])
	write_png(fav / "mstile-150x150.png", 150, 150, rasters[150])
	write_png(fav / "mstile-310x310.png", 310, 310, rasters[310])
	# Wide tile: letterboxed mark
	wide = bytearray(310 * 150 * 4)
	fill_round_rect(wide, 310, 150, 0, 0, 310, 150, 0, TEAL_DARK)
	# blit 128 mark centered
	mark128 = rasters[128]
	ox, oy = (310 - 128) // 2, (150 - 128) // 2
	for y in range(128):
		for x in range(128):
			si = (y * 128 + x) * 4
			di = ((oy + y) * 310 + (ox + x)) * 4
			wide[di : di + 4] = mark128[si : si + 4]
	write_png(fav / "mstile-310x150.png", 310, 150, bytes(wide))
	write_ico(fav / "favicon.ico", png_cache[32])

	(fav / "site.webmanifest").write_text(
		"""{
  "name": "PhotoCoop",
  "short_name": "PhotoCoop",
  "icons": [
    {"src": "/android-chrome-192x192.png", "sizes": "192x192", "type": "image/png"},
    {"src": "/android-chrome-512x512.png", "sizes": "512x512", "type": "image/png"}
  ],
  "theme_color": "#0e2a32",
  "background_color": "#0e2a32",
  "display": "standalone"
}
"""
	)
	(fav / "browserconfig.xml").write_text(
		"""<?xml version="1.0" encoding="utf-8"?>
<browserconfig>
  <msapplication>
    <tile>
      <square70x70logo src="/mstile-70x70.png"/>
      <square150x150logo src="/mstile-150x150.png"/>
      <square310x310logo src="/mstile-310x310.png"/>
      <wide310x150logo src="/mstile-310x150.png"/>
      <TileColor>#0e2a32</TileColor>
    </tile>
  </msapplication>
</browserconfig>
"""
	)

	(OUT / "LICENSE.txt").write_text(
		"""PhotoCoop branding assets
Copyright (c) PhotoCoop contributors

These logos, icons, and raster app icons are original PhotoCoop artwork.
They are not Graphite brand assets and are not licensed under the Graphite
Branding License. You may use them as part of PhotoCoop.

Graphite source code remains MIT OR Apache-2.0 as provided by Graphite contributors.
"""
	)
	(OUT / ".photocoop-branding").write_text("photocoop-branding-v1\n")
	print(f"Wrote {sum(1 for _ in OUT.rglob('*') if _.is_file())} files to {OUT}")


if __name__ == "__main__":
	main()
