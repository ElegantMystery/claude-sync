---
description: Git pull from ~/dotfiles/claude and import Claude Code config. Pulls from main by default; use --branch <name> to pull from a specific branch.
argument-hint: [--source <path>] [--branch <name>] [--dry-run]
allowed-tools: [Bash]
---

Run immediately with the user's arguments (default source is ~/dotfiles/claude):

```bash
python3 "$(find ~/.claude/plugins -name "cli.py" -path "*/sync*" 2>/dev/null | head -1)" --import --source ~/dotfiles/claude --pull $ARGUMENTS
```

**Branch:** Pulls from the current branch (default: `main`). Pass `--branch <name>` to switch to and pull a specific remote branch.
