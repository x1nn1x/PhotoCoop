# PhotoCoop

PhotoCoop is a fork of [Graphite](https://github.com/GraphiteEditor/Graphite). Graphite remains the engine; this overlay adds PhotoCoop branding, theme, and features while staying mergeable with upstream.

Graphite source is MIT OR Apache-2.0. Graphite logos and icons are **not** open source. For now PhotoCoop uses Graphite's UI and downloaded icons so the editor matches upstream; replace them before a public PhotoCoop release.

## Layout

```
photocoop/
  branding/     Original icons, logotype, favicons (Graphite filenames)
  theme/        CSS variable overrides
  identity/     Product-name constants used by thin Graphite hooks
  tools/        PhotoCoop editor tools compiled into graphite-editor
  scripts/      Sync Graphite, build .app, publish GitHub Releases
  hooks.md      Graphite files we patch
  UPDATING.md   How to pull Graphite + publish PhotoCoop updates
```

The rest of the tree is Graphite. Keep PhotoCoop work in this folder when you can.

## Update Graphite & publish PhotoCoop

A daily **Upstream Sync Check** Action opens an `upstream-sync` issue when Graphite has commits you have not merged yet. See **[UPDATING.md](UPDATING.md)**. Short version:

```sh
./photocoop/scripts/sync-upstream.sh      # merge latest Graphite
./photocoop/scripts/build-app.sh          # PhotoCoop.app + zip
./photocoop/scripts/publish-release.sh 0.1.0   # push source + GitHub Release
```

People download **PhotoCoop-macOS.zip** from your repo’s Releases page. They get Graphite’s updates plus PhotoCoop features without rebuilding.

## Git remotes

```
upstream  https://github.com/GraphiteEditor/Graphite.git
origin    your PhotoCoop GitHub repo
```

```sh
./photocoop/scripts/setup-origin.sh   # one-time
```

Work on the `photocoop` branch. Use merge, not rebase, for this long-lived fork.

## Adding features

Put new code in `photocoop/` and register it with one `PHOTOCOOP-HOOK` in Graphite. Prefer adding files over editing Graphite files. Keep [`hooks.md`](hooks.md) current.

## Run

```sh
cargo run
```

Opens the web app at http://localhost:8080. First run downloads Graphite branding; PhotoCoop-only icons are copied afterward.

Desktop:

```sh
./photocoop/scripts/build-app.sh
open photocoop/PhotoCoop.app
```
