---
description: Sync and backup Claude Code configuration when user asks to "sync my claude settings", "backup my claude config", "export claude settings", "sync to git", "push claude config", "pull claude config", or discusses backing up or version controlling claude settings.
argument-hint: [--export|--import] [--target <path>|--source <path>] [--push] [--pull] [--dry-run] [--list] [--diff] [--status]
allowed-tools: [Bash, Read]
---

# Claude Sync

Sync and backup Claude Code settings, skills, commands, hooks, and agents.

## Arguments

User invoked with: $ARGUMENTS

## Available Commands

### Export (Backup)
```
/claude-sync --export --target ~/dotfiles/claude
/claude-sync --export --target ~/dotfiles/claude --push    # Export + git push
/claude-sync --export --target ~/dotfiles/claude --dry-run
```

### Import (Restore)
```
/claude-sync --import --source ~/dotfiles/claude
/claude-sync --import --source ~/dotfiles/claude --pull     # Git pull + import
/claude-sync --import --source ~/dotfiles/claude --dry-run
```

### Git Workflow
- `--push` adds, commits, and pushes to remote after export
- `--pull` pulls from remote before import (stashes local changes first)

### Status & Preview
```
/claude-sync --status           # Show sync status
/claude-sync --list             # List synced components
/claude-sync --diff             # Show differences
```

## Workflow

**Initial setup:**
```bash
# Create and initialize git repo
mkdir -p ~/dotfiles/claude
cd ~/dotfiles/claude
git init
git remote add origin git@github.com:username/dotfiles.git
git commit -m "Initial commit" --allow-empty
git push -u origin HEAD
```

**Daily sync:**
```
/claude-sync --export --target ~/dotfiles/claude --push
```

**On another machine:**
```
/claude-sync --import --source ~/dotfiles/claude --pull
```

## What Gets Synced

**Exported (safe to version control):**
- `skills/` — All skills
- `commands/` — All commands
- `agents/` — All agents
- `rules/` — All rules
- `settings.json` — (filtered to remove secrets)
- `keybindings.json` — Keyboard shortcuts

**Never Exported:**
- `credentials.json` — API keys and tokens
- `settings.local.json` — Local overrides
- `history.jsonl` — Session history
- `cache/` — Cache files
- `sessions/` — Session data
- `telemetry/` — Telemetry data
- `backups/` — Backup files

## Security Filtering

Before export, these are automatically filtered/removed:
- API keys (sk-, ANTHROPIC_, MINIMAX_, OPENAI_, etc.)
- Bearer tokens and auth tokens
- File paths containing secrets
- Session IDs
- Credentials files

## Dry Run

Use `--dry-run` to preview what would be synced without making changes:

```
/claude-sync --export --target ~/dotfiles/claude --dry-run
```

This shows:
- Which files would be copied
- Which files would be filtered/ignored
- Any warnings about sensitive data

## Error Handling

If sync fails:
1. Check that target directory exists and is writable
2. Verify source `.claude/` is accessible
3. Ensure sufficient disk space
4. Check file permissions

Report any errors to the user with actionable hints.