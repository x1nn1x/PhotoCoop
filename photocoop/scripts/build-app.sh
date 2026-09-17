#!/usr/bin/env bash
# Build PhotoCoop.app into photocoop/ for local use or packaging into a GitHub Release.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
cd "$ROOT"

STUB="$ROOT/photocoop/.raster-shader-stub.wgsl"
APP_SRC="$ROOT/target/release/PhotoCoop.app"
APP_DST="$ROOT/photocoop/PhotoCoop.app"
DIST="$ROOT/photocoop/dist"
ZIP="$DIST/PhotoCoop-macOS.zip"

if [[ ! -f "$STUB" ]]; then
	echo "error: missing shader stub at $STUB" >&2
	exit 1
fi

echo "==> Building desktop release (this can take several minutes)"
env -u CARGO_TARGET_DIR RASTER_NODES_SHADER_PATH="$STUB" cargo run -p cargo-run -- build desktop

if [[ ! -d "$APP_SRC" ]]; then
	echo "error: expected $APP_SRC after build" >&2
	exit 1
fi

echo "==> Installing into photocoop/PhotoCoop.app"
rm -rf "$APP_DST"
cp -R "$APP_SRC" "$APP_DST"
codesign --force --deep --sign - "$APP_DST"
xattr -cr "$APP_DST"

mkdir -p "$DIST"
rm -f "$ZIP"
echo "==> Zipping for GitHub Releases → $ZIP"
ditto -c -k --sequesterRsrc --keepParent "$APP_DST" "$ZIP"

echo
echo "Ready:"
echo "  app: $APP_DST"
echo "  zip: $ZIP ($(du -h "$ZIP" | awk '{print $1}'))"
echo
echo "Publish with: ./photocoop/scripts/publish-release.sh <version>"
