---
description: Apply synced Claude Code config from ~/dotfiles/claude to ~/.claude
argument-hint: [--source <path>] [--dry-run]
allowed-tools: [Bash]
---

Run immediately (default source is ~/dotfiles/claude):

```bash
python3 "$(find ~/.claude/plugins -name "cli.py" -path "*/sync*" 2>/dev/null | head -1)" --import --source ~/dotfiles/claude $ARGUMENTS
```
