#!/usr/bin/env bash
# Merge the latest Graphite (upstream/master) into the current PhotoCoop branch.
# PhotoCoop features stay in photocoop/ + PHOTOCOOP-HOOK sites listed in hooks.md.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
cd "$ROOT"

BRANCH="$(git branch --show-current)"
if [[ "$BRANCH" != "photocoop" && "${PHOTOCOOP_ALLOW_OTHER_BRANCH:-}" != "1" ]]; then
	echo "error: checkout the photocoop branch first (currently on '$BRANCH')" >&2
	echo "       or set PHOTOCOOP_ALLOW_OTHER_BRANCH=1 to override" >&2
	exit 1
fi

if ! git remote get-url upstream >/dev/null 2>&1; then
	echo "error: missing 'upstream' remote (expected GraphiteEditor/Graphite)" >&2
	exit 1
fi

if [[ -n "$(git status --porcelain)" ]]; then
	echo "error: working tree is dirty. Commit or stash PhotoCoop work before syncing." >&2
	git status -sb
	exit 1
fi

echo "==> Fetching upstream (Graphite)"
git fetch upstream

BEFORE="$(git rev-parse HEAD)"
if git merge-base --is-ancestor upstream/master HEAD; then
	echo "Already up to date with upstream/master ($(git rev-parse --short upstream/master))."
	exit 0
fi

echo "==> Merging upstream/master into $BRANCH"
echo "    Graphite tip: $(git rev-parse --short upstream/master)"
if ! git merge upstream/master --no-edit; then
	echo
	echo "Merge conflicts. Resolve files listed in photocoop/hooks.md (search PHOTOCOOP-HOOK),"
	echo "then:  git add -A && git commit"
	echo "Then rebuild:  ./photocoop/scripts/build-app.sh"
	exit 1
fi

echo
echo "Merged Graphite into PhotoCoop."
echo "  before: $(git rev-parse --short "$BEFORE")"
echo "  after:  $(git rev-parse --short HEAD)"
echo "  graphite base: $(git rev-parse --short upstream/master)"
echo
echo "Next:"
echo "  1. Smoke-test: cargo check -p graphite-editor"
echo "  2. Rebuild app: ./photocoop/scripts/build-app.sh"
echo "  3. Publish:     ./photocoop/scripts/publish-release.sh <version>"
