# Updating & publishing PhotoCoOp

Lightweight loop: pull Graphite → keep PhotoCoOp features → push source → publish a downloadable macOS build.

## One-time setup

1. Commit all PhotoCoOp work on the `photocoop` branch (features must be in git, not only on disk).
2. Log into GitHub as yourself and wire `origin` — see **[GITHUB_AUTH.md](GITHUB_AUTH.md)**.
3. Push:

```sh
git push -u origin photocoop
```

Remotes:

| Remote | Points at |
|---|---|
| `upstream` | https://github.com/GraphiteEditor/Graphite.git |
| `origin` | your PhotoCoOp GitHub repo |

## Every time Graphite moves

```sh
# 1. Merge latest Graphite (fails cleanly if you have uncommitted edits)
./photocoop/scripts/sync-upstream.sh

# 2. If there were conflicts: fix PHOTOCOOP-HOOK sites (see hooks.md), commit, continue

# 3. Build the .app + zip
./photocoop/scripts/build-app.sh

# 4. Push source + GitHub Release (people download the zip)
./photocoop/scripts/publish-release.sh 0.1.1
```

`publish-release.sh` already builds unless you pass `--skip-build`.

What end users do: open your repo → **Releases** → download **PhotoCoop-macOS.zip**.

What you keep: PhotoCoOp code under `photocoop/` plus thin `PHOTOCOOP-HOOK` patches. Graphite arrives via `git merge upstream/master`, not by rewriting the fork by hand.

## What each script does

| Script | Role |
|---|---|
| `setup-origin.sh` | Add `origin` (optionally create the GitHub repo) |
| `sync-upstream.sh` | `git fetch upstream` + `merge upstream/master` |
| `build-app.sh` | Release `.app` → `photocoop/PhotoCoop.app` + `photocoop/dist/PhotoCoop-macOS.zip` |
| `publish-release.sh` | Push `photocoop`, tag `v*`, upload zip as a GitHub Release |

The `.app` is gitignored on purpose. Source stays in git; binaries ship on Releases.

## Conflict tips

Conflicts should almost always be in files listed in [`hooks.md`](hooks.md). Search `PHOTOCOOP-HOOK`. Prefer re-applying a small hook over accepting upstream wholesale on those lines. Feature bodies live in `photocoop/tools/` and usually merge without touching Graphite.
