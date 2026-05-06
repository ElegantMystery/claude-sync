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

<!-- AUTO-GENERATED from commands/*.md -->
| Command | Description |
|---------|-------------|
| `/sync:setup` | Set up sync — choose to create a new private GitHub repo or link an existing one |
| `/sync:push` | Export `~/.claude` to `~/dotfiles/claude` and git push |
| `/sync:pull` | Git pull latest dotfiles from remote (no import) |
| `/sync:apply` | Apply synced config from `~/dotfiles/claude` into `~/.claude` |
| `/sync:status` | Show sync status — components tracked, file count, and dotfiles repo state |
| `/sync:list` | List all tracked components and their sync status |
<!-- END AUTO-GENERATED -->

## Typical Workflow

**First time — create your dotfiles repo:**

```
/sync:setup
```

Claude will ask whether to create a new private GitHub repo or link an existing one. Run `/sync:push` after to save your config.

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

<!-- AUTO-GENERATED from scripts/filter.py -->
| Component | Notes |
|-----------|-------|
| `skills/` | All skills |
| `commands/` | All commands |
| `agents/` | All agents |
| `rules/` | All rules |
| `settings.json` | Filtered — secrets removed |
| `keybindings.json` | Keyboard shortcuts |
<!-- END AUTO-GENERATED -->

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

## Requirements

- [GitHub CLI (`gh`)](https://cli.github.com/) — required for `/sync:setup` and `/sync:push`/`/sync:pull`
- Python 3.10+
- Git

## License

MIT
