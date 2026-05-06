---
description: Set up a git repo for syncing Claude Code config. Asks for a remote URL and initializes ~/dotfiles/claude.
argument-hint: [--remote <git-url>] [--target <path>]
allowed-tools: [Bash]
---

# Setup Claude Sync

Help the user set up a git repository to sync their Claude Code config.

## Steps

1. If the user did not provide a `--remote` URL in $ARGUMENTS, ask them:
   > What is your git remote URL? (e.g. `git@github.com:username/dotfiles.git`)

2. Once you have the remote URL, run:

```bash
python3 "$(find ~/.claude/plugins -name "cli.py" -path "*/sync*" 2>/dev/null | head -1)" --init --remote <REMOTE_URL> --target ~/dotfiles/claude
```

3. Then export their current config and push:

```bash
python3 "$(find ~/.claude/plugins -name "cli.py" -path "*/sync*" 2>/dev/null | head -1)" --export --target ~/dotfiles/claude --push
```

4. Tell the user setup is complete and they can now use `/sync:push` daily.
