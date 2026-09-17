# PhotoCoop Graphite hooks

These are the only Graphite files PhotoCoop should edit. After merging `upstream/master`, re-check this list.

| File | Why |
|---|---|
| `.gitignore` | Ignore only root `/branding/`, not `photocoop/branding/` |
| `tools/cargo-run/src/branding.rs` | Download Graphite icons, then add PhotoCoop-only files (marquee) |
| `frontend/vite.config.ts` | Allow Vite to read files outside `frontend/` |
| `frontend/index.html` | App title (keep Graphite splash/theme colors until PhotoCoop restyles) |
| `editor/Cargo.toml` | Depend on `photocoop-identity` |
| `editor/src/messages/menu_bar/menu_bar_message_handler.rs` | PhotoCoop menu labels |
| `editor/src/messages/dialog/simple_dialogs/about_graphite_dialog.rs` | About PhotoCoop copy |
| `editor/src/messages/dialog/simple_dialogs/licenses_dialog.rs` | Fork licensing copy |
| `desktop/src/consts.rs` | Display name, app id, data directory |
| `desktop/bundle/src/common.rs` | Display name |
| `desktop/bundle/src/mac.rs` | Bundle id (keep Graphite document types) |
| `desktop/ui/src/dirs.rs` | Data directory |
| `desktop/ui/src/consts.rs` | IPC prefix |
| `desktop/ui/src/remote/spawn.rs` | CEF frame service name |
| `desktop/platform/win/build.rs` | Windows product strings |
| `Cargo.toml` | Workspace member `photocoop/identity` |
| `editor/src/messages/tool/tool_messages/mod.rs` | `#[path]` include for `photocoop/tools/marquee_tool.rs` |
| `editor/src/messages/prelude.rs` | Re-export `MarqueeToolMessage` |
| `editor/src/messages/tool/tool_message.rs` | `ToolMessage::Marquee` child + `ActivateToolMarquee` |
| `editor/src/messages/tool/utility_types.rs` | `ToolType::Marquee`, toolbar group, message conversions |
| `editor/src/messages/tool/tool_message_handler.rs` | Activate + advertise marquee |
| `editor/src/messages/input_mapper/input_mappings.rs` | Marquee pointer events, Delete/Backspace; `M` activates marquee |
| `editor/src/messages/portfolio/document/graph_operation/graph_operation_message.rs` | `MarqueeRegionEdit` (punch/lift inside the region) |
| `editor/src/messages/portfolio/document/graph_operation/graph_operation_message_handler.rs` | Dispatch `MarqueeRegionEdit` |
| `frontend/src/icons.ts` | Import **new** PhotoCoop icons (do not swap Graphite filenames) |

Search for `PHOTOCOOP-HOOK` to find every patch.

PhotoCoop currently uses Graphite's downloaded icons. New tool icons still need an `icons.ts` import plus a file under `photocoop/branding/` that `branding.rs` copies after the Graphite archive.
