# claude-sync

Sync and backup Claude Code configuration to a version-controlled repository with automatic secret filtering.

## Installation

**Step 1:** Add this repo as a marketplace source:

```
/marketplace add ElegantMystery/claude-sync
```

**Step 2:** Install the plugin:

```
/plugin install sync
```

**Step 3:** Reload plugins:

```
/reload-plugins
```

## Commands

| Command | Description |
|---------|-------------|
| `/sync:push` | Export `~/.claude` to `~/dotfiles/claude` and git push |
| `/sync:pull` | Git pull latest dotfiles (no import) |
| `/sync:apply` | Import from `~/dotfiles/claude` into `~/.claude` |
| `/sync:status` | Show sync status and file count |
| `/sync:list` | List all tracked components |

## Typical Workflow

**First-time setup** (create a dotfiles repo):

```bash
mkdir -p ~/dotfiles/claude
cd ~/dotfiles/claude
git init
git remote add origin git@github.com:username/dotfiles.git
git commit -m "Initial commit" --allow-empty
git push -u origin HEAD
```

**Daily — save your settings:**

```
/sync:push
```

**On a new machine — restore your settings:**

```
/sync:pull
/sync:apply
```

**Preview before applying:**

```
/sync:apply --dry-run
```

## What Gets Synced

| Component | Notes |
|-----------|-------|
| `skills/` | All skills |
| `commands/` | All commands |
| `agents/` | All agents |
| `rules/` | All rules |
| `settings.json` | Filtered — secrets removed |
| `keybindings.json` | Keyboard shortcuts |

**Never synced:**
- `credentials.json` — API keys and tokens
- `settings.local.json` — Local overrides
- `history.jsonl` — Session history
- `cache/`, `sessions/`, `telemetry/`, `backups/`

## Security

Secret values are automatically filtered before export:
- API keys (`sk-`, `ANTHROPIC_`, `MINIMAX_`, `OPENAI_`, etc.)
- Bearer tokens and auth tokens
- Credentials files
- Session IDs

## License

MIT
