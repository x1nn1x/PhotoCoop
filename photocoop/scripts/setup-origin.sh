#!/usr/bin/env bash
# One-time: point this clone at a GitHub repo named PhotoCoOp (or pass a full git URL).
#
# Usage:
#   ./photocoop/scripts/setup-origin.sh
#   ./photocoop/scripts/setup-origin.sh git@github.com:YOU/PhotoCoOp.git
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
cd "$ROOT"

if git remote get-url origin >/dev/null 2>&1; then
	echo "origin already set to: $(git remote get-url origin)"
	exit 0
fi

URL="${1:-}"
if [[ -z "$URL" ]]; then
	if command -v gh >/dev/null 2>&1; then
		echo "==> Creating GitHub repo with gh (private by default; pass --public to gh if you want)"
		gh repo create PhotoCoOp --source=. --remote=origin --private --push=false
		git remote set-url origin "$(gh repo view --json sshUrl -q .sshUrl 2>/dev/null || gh repo view --json url -q .url)"
		# Prefer SSH when available
		SSH_URL="$(gh repo view --json sshUrl -q .sshUrl)"
		git remote set-url origin "$SSH_URL"
		echo "origin → $(git remote get-url origin)"
		echo
		echo "Push when ready:"
		echo "  git push -u origin photocoop"
		exit 0
	fi
	echo "usage: $0 <git-url>" >&2
	echo "example: $0 git@github.com:YOU/PhotoCoOp.git" >&2
	echo
	echo "Or install GitHub CLI: brew install gh && gh auth login" >&2
	echo "then re-run: $0" >&2
	exit 1
fi

git remote add origin "$URL"
echo "origin → $(git remote get-url origin)"
echo
echo "Push when ready:"
echo "  git push -u origin photocoop"
