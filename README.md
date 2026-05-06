# claude-sync

Sync and backup Claude Code configuration to a version-controlled repository with automatic secret filtering.

## Installation

**Step 1:** Add this repo as a marketplace source:

```
/marketplace add ElegantMystery/claude-sync
```

**Step 2:** Install the plugin:

```
/plugin install claude-sync
```

**Step 3:** Reload plugins:

```
/reload-plugins
```

## Features

- **Export**: Sync `.claude/` directory to a target backup folder
- **Import**: Restore `.claude/` from a backup folder  
- **Secret Filtering**: Automatically strips API keys, tokens, and credentials
- **Selective Sync**: Choose which components to sync (settings, skills, commands, agents, rules, hooks)
- **Dry Run**: Preview changes before applying
- **Git Integration**: Optional git commit after sync

## Usage

```
/claude-sync --export --target ~/dotfiles/claude
/claude-sync --import --source ~/dotfiles/claude
/claude-sync --status
/claude-sync --list
/claude-sync --diff
```

## Components

The plugin syncs these components:
- `settings.json` (filtered - secrets removed)
- `skills/` directory
- `commands/` directory
- `agents/` directory
- `rules/` directory
- `hooks/` configuration (from settings)

## Components Excluded (Not Synced)

These contain sensitive data and are never synced:
- API keys and tokens
- Credentials files
- Session history
- Cache files
- Telemetry data

## Security

All secret values are filtered before export:
- API keys (sk-, ANTHROPIC_, MINIMAX_, etc.)
- Bearer tokens
- Credentials files
- File paths and session IDs

## License

MIT