---
description: Set up Claude Code config sync — creates a private GitHub repo and initializes ~/dotfiles/claude automatically.
argument-hint: [--repo-name <name>]
allowed-tools: [Bash]
---

# Setup Claude Sync

Guide the user through first-time setup by creating a private GitHub repo and initializing the local dotfiles directory.

## Steps

1. If the user did not provide a repo name in $ARGUMENTS, ask them:
   > What would you like to name your dotfiles repo? (e.g. `dotfiles` or `claude-config`)

2. Create a private GitHub repo with that name:

```bash
gh repo create <REPO_NAME> --private --description "Claude Code configuration backup"
```

3. Get the SSH remote URL:

```bash
gh repo view <REPO_NAME> --json sshUrl --jq '.sshUrl'
```

4. Initialize the local repo and push using the URL from step 3:

```bash
python3 "$(find ~/.claude/plugins -name "cli.py" -path "*/sync*" 2>/dev/null | head -1)" --init --remote <SSH_URL> --target ~/dotfiles/claude
```

5. Export current Claude config and push:

```bash
python3 "$(find ~/.claude/plugins -name "cli.py" -path "*/sync*" 2>/dev/null | head -1)" --export --target ~/dotfiles/claude --push
```

6. Tell the user setup is complete. Show them the repo URL and that they can now use `/sync:push` to save settings anytime.
