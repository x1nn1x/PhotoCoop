# GitHub setup for PhotoCoop

One-time steps so you can push the `photocoop` branch and publish Releases.

## 1. Git author

GitHub attributes commits by email. Use your own:

```sh
git config --global user.name "Your Name"
git config --global user.email "you@example.com"
```

Prefer the address on your GitHub account, or Settings → Emails → noreply address.

```sh
git config --global --get user.name
git config --global --get user.email
```

## 2. GitHub CLI

```sh
brew install gh
gh auth login
gh auth status
```

## 3. Link `origin`

```sh
cd /path/to/PhotoCoop
./photocoop/scripts/setup-origin.sh
# or: ./photocoop/scripts/setup-origin.sh git@github.com:YOURUSER/PhotoCoop.git
git remote -v   # origin must be YOUR PhotoCoop repo, not GraphiteEditor/Graphite
```

## 4. Commit and push

```sh
git status
git add -A
git status   # confirm no PhotoCoop.app, dist/, or editor junk
git commit -m "Add PhotoCoop overlay, marquee tool, and publish scripts."
git push -u origin photocoop
```

Optional macOS Release zip:

```sh
./photocoop/scripts/publish-release.sh 0.1.0
```

## Do not commit

- Built apps: `photocoop/PhotoCoop.app`, `photocoop/dist/`
- Local IDE / editor config folders (see `.gitignore`)
- Secrets, tokens, `.env`, private keys

Those paths are listed in `.gitignore`. Always skim `git status` before the first public push.
