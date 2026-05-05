---
name: claude-sync
description: This skill should be used when the user asks to "sync claude settings", "backup claude config", "export claude settings", or discusses version controlling or backing up their claude code configuration.
version: 1.0.0
---

# Claude Sync Plugin

This plugin provides backup and sync functionality for Claude Code's `.claude/` directory.

## Overview

The `claude-sync` plugin enables users to:
- Export their Claude Code configuration to a version-controlled repository
- Import/restore configuration from a backup
- Preview changes with dry-run mode
- Automatically filter sensitive data before export

## When This Skill Applies

This skill activates when the user:
- Asks to sync, backup, or export their Claude Code settings
- Wants to version control their `.claude/` directory
- Asks about moving their config to a new machine
- Wants to share their config with teammates (via shared repo)
- Asks about "sync plugin" or "claude backup"

## Core Concepts

### What Gets Synced

**Exported (safe to version control):**
```
skills/         # All installed skills
commands/       # All custom commands
agents/         # All custom agents
rules/          # All rules
keybindings.json
settings.json   # (with secrets filtered)
```

**Never Exported (excluded):**
```
credentials.json
settings.local.json
history.jsonl
cache/
sessions/
telemetry/
backups/
*.log
```

### Secret Filtering

The export process automatically filters:
- API keys: `sk-`, `ANTHROPIC_`, `MINIMAX_`, `OPENAI_`, etc.
- Bearer tokens: `Bearer `, `token=`, `auth=`
- Credentials: entire `credentials.json` files
- File paths with sensitive identifiers

### Sync Modes

**Export Mode:**
```bash
# Full export to target directory
/claude-sync --export --target ~/dotfiles/claude

# Dry run - preview only
/claude-sync --export --target ~/dotfiles/claude --dry-run
```

**Import Mode:**
```bash
# Full import from source directory
/claude-sync --import --source ~/dotfiles/claude

# Dry run - preview only
/claude-sync --import --source ~/dotfiles/claude --dry-run
```

### Git Integration

For users who want automatic git commits:

1. Initialize git in target directory:
   ```bash
   cd ~/dotfiles/claude
   git init
   git add -a
   git commit -m "Initial claude config"
   ```

2. After each export, optionally auto-commit:
   ```bash
   cd ~/dotfiles/claude
   git add -a
   git commit -m "Update claude config: $(date)"
   ```

## Usage Examples

### Example 1: First-time Setup

1. Create a dotfiles repo:
   ```bash
   mkdir -p ~/dotfiles/claude
   cd ~/dotfiles/claude
   git init
   ```

2. Export current config:
   ```
   /claude-sync --export --target ~/dotfiles/claude
   ```

3. Push to remote:
   ```bash
   cd ~/dotfiles/claude
   git remote add origin git@github.com:username/dotfiles.git
   git push -u main
   ```

### Example 2: Syncing After Changes

```
/claude-sync --export --target ~/dotfiles/claude
```

### Example 3: Restoring on New Machine

1. Clone dotfiles repo:
   ```bash
   git clone git@github.com:username/dotfiles.git ~/dotfiles
   ```

2. Install plugin (if not auto-installed)

3. Import config:
   ```
   /claude-sync --import --source ~/dotfiles/claude
   ```

### Example 4: Checking Differences

```
/claude-sync --diff
```

Shows what changed between current config and last sync.

## Implementation Details

### Architecture

```
claude-sync/
├── .claude-plugin/
│   └── plugin.json          # Plugin manifest
├── commands/
│   └── claude-sync.md       # Main command
├── skills/
│   └── claude-sync/
│       └── SKILL.md         # This file
├── scripts/
│   ├── sync.py              # Main sync logic
│   ├── filter.py            # Secret filtering
│   └── cli.py               # CLI entry point
└── hooks/
    └── (future: auto-sync hooks)
```

### Filter Rules

The secret filter removes:
1. **Environment variables**: ANTHROPIC_AUTH_TOKEN, MINIMAX_API_KEY, OPENAI_API_KEY, etc.
2. **Bearer tokens**: Any string matching `Bearer [a-zA-Z0-9_-]+`
3. **API keys**: Strings starting with `sk-`, `sk-api-`, or matching key patterns
4. **Credentials files**: Entire files named `credentials.json`, `.credentials`
5. **Session IDs**: Strings matching UUID patterns
6. **File paths**: References to `/home/*/.claude/cache/`, `/session-env/`, etc.

### Permissions Required

The sync command needs:
- Read access to `~/.claude/`
- Write access to target directory (for export) or `~/.claude/` (for import)

## Troubleshooting

### Export Fails
- Check target directory exists: `ls -la ~/dotfiles/claude`
- Verify write permissions: `touch ~/dotfiles/claude/test`
- Ensure enough disk space

### Import Fails
- Check source directory exists: `ls -la ~/dotfiles/claude`
- Verify `~/.claude/` is writable
- Backup current config first: `cp -r ~/.claude ~/.claude.bak`

### Secrets Still Visible
- Check filter rules in `scripts/filter.py`
- Run with `--dry-run` to see what would be exported
- Report false positives/negatives for filter improvement

## Future Enhancements

Planned features:
- Auto-sync on session end (hook-based)
- Git integration (auto-commit after export)
- Selective sync (choose specific components)
- Encryption for sensitive values
- Sync status dashboard