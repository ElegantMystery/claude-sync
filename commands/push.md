---
description: Export Claude Code config to ~/dotfiles/claude and git push
argument-hint: [--target <path>] [--dry-run]
allowed-tools: [Bash]
---

Run immediately with the user's arguments (default target is ~/dotfiles/claude):

```bash
python3 "$(find ~/.claude/plugins -name "cli.py" -path "*/sync*" 2>/dev/null | head -1)" --export --target ~/dotfiles/claude --push $ARGUMENTS
```

If this fails with "not a git repository", tell the user to run `/sync:setup` first — it will create a private GitHub repo and set everything up automatically.
