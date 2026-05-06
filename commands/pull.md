---
description: Git pull from ~/dotfiles/claude and import Claude Code config. Pulls from the current branch (default: main). To pull from a different branch, check it out in ~/dotfiles/claude first.
argument-hint: [--source <path>] [--dry-run]
allowed-tools: [Bash]
---

Run immediately with the user's arguments (default source is ~/dotfiles/claude):

```bash
python3 "$(find ~/.claude/plugins -name "cli.py" -path "*/sync*" 2>/dev/null | head -1)" --import --source ~/dotfiles/claude --pull $ARGUMENTS
```

**Branch:** Pulls from whichever branch is currently checked out in `~/dotfiles/claude` (default: `main`). To pull from a different branch, run `git -C ~/dotfiles/claude checkout <branch>` first.
