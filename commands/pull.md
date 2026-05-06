---
description: Git pull from ~/dotfiles/claude and import Claude Code config
argument-hint: [--source <path>] [--dry-run]
allowed-tools: [Bash]
---

Run immediately with the user's arguments (default source is ~/dotfiles/claude):

```bash
python3 "$(find ~/.claude/plugins -name "cli.py" -path "*/sync*" 2>/dev/null | head -1)" --import --source ~/dotfiles/claude --pull $ARGUMENTS
```
