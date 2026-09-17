#!/usr/bin/env bash
# Push the photocoop branch and create a GitHub Release people can download.
#
# Usage:
#   ./photocoop/scripts/publish-release.sh 0.1.0
#   ./photocoop/scripts/publish-release.sh 0.1.0 --skip-build   # reuse existing zip
#
# Prerequisites:
#   - origin remote pointing at your PhotoCoOp GitHub repo
#   - clean working tree on branch photocoop
#   - gh CLI authenticated (brew install gh && gh auth login), OR upload the zip manually
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
cd "$ROOT"

VERSION="${1:-}"
SKIP_BUILD=0
if [[ "${2:-}" == "--skip-build" ]]; then
	SKIP_BUILD=1
fi

if [[ -z "$VERSION" ]]; then
	echo "usage: $0 <version> [--skip-build]" >&2
	echo "example: $0 0.1.0" >&2
	exit 1
fi

VERSION="${VERSION#v}"
TAG="v${VERSION}"
BRANCH="$(git branch --show-current)"
ZIP="$ROOT/photocoop/dist/PhotoCoop-macOS.zip"

if [[ "$BRANCH" != "photocoop" && "${PHOTOCOOP_ALLOW_OTHER_BRANCH:-}" != "1" ]]; then
	echo "error: publish from the photocoop branch (currently on '$BRANCH')" >&2
	exit 1
fi

if ! git remote get-url origin >/dev/null 2>&1; then
	echo "error: no 'origin' remote. Create a GitHub repo, then:" >&2
	echo "  git remote add origin git@github.com:YOU/PhotoCoOp.git" >&2
	echo "  See photocoop/UPDATING.md" >&2
	exit 1
fi

if [[ -n "$(git status --porcelain)" ]]; then
	echo "error: working tree is dirty. Commit PhotoCoOp changes before publishing." >&2
	git status -sb
	exit 1
fi

if [[ "$SKIP_BUILD" -eq 0 ]]; then
	"$ROOT/photocoop/scripts/build-app.sh"
fi

if [[ ! -f "$ZIP" ]]; then
	echo "error: missing $ZIP — run ./photocoop/scripts/build-app.sh first" >&2
	exit 1
fi

GRAPHITE_BASE="$(git rev-parse --short upstream/master 2>/dev/null || git rev-parse --short HEAD)"
NOTES="$(mktemp)"
trap 'rm -f "$NOTES"' EXIT

cat >"$NOTES" <<EOF
## PhotoCoOp ${TAG}

macOS build with PhotoCoOp features on top of Graphite.

- Graphite base: \`${GRAPHITE_BASE}\`
- Branch: \`${BRANCH}\` @ \`$(git rev-parse --short HEAD)\`

### macOS

1. Download **PhotoCoop-macOS.zip**
2. Unzip and open **PhotoCoop.app** (right-click → Open the first time if Gatekeeper blocks it)

### Source

Clone this repo and check out tag \`${TAG}\` to build from source.
EOF

echo "==> Pushing $BRANCH to origin"
git push -u origin "HEAD:photocoop"

if git rev-parse "$TAG" >/dev/null 2>&1; then
	echo "error: tag $TAG already exists locally" >&2
	exit 1
fi

echo "==> Tagging $TAG"
git tag -a "$TAG" -m "PhotoCoOp $TAG (Graphite ${GRAPHITE_BASE})"
git push origin "$TAG"

if command -v gh >/dev/null 2>&1; then
	echo "==> Creating GitHub Release $TAG"
	gh release create "$TAG" "$ZIP" \
		--title "PhotoCoOp $TAG" \
		--notes-file "$NOTES" \
		--target photocoop
	echo
	gh release view "$TAG" --web 2>/dev/null || gh release view "$TAG"
else
	echo
	echo "gh CLI not installed — pushed tag $TAG, but you still need to upload the zip:"
	echo "  1. brew install gh && gh auth login"
	echo "  2. gh release create $TAG \"$ZIP\" --title \"PhotoCoOp $TAG\" --notes-file /dev/stdin --target photocoop <<'EOF'"
	cat "$NOTES"
	echo "EOF"
	echo
	echo "Or upload $ZIP manually on GitHub → Releases → Draft from tag $TAG"
fi
