---
description: Set up Claude Code config sync — creates a private GitHub repo and initializes ~/dotfiles/claude automatically.
argument-hint: [--repo-name <name>]
allowed-tools: [Bash]
---

# Setup Claude Sync

## Step 1: Check current state

First, check if the dotfiles repo is already initialized:

```bash
python3 "$(find ~/.claude/plugins -name "cli.py" -path "*/sync*" 2>/dev/null | head -1)" --status
```

- If the output shows `Git repo: ✓` — tell the user they are already set up and stop here.
- If the output shows `Git repo: ✗` — continue to Step 2.

## Step 2: Ask for repo name

Ask the user:
> Your dotfiles repo is not set up yet. What would you like to name it? (e.g. `dotfiles` or `claude-config`)

## Step 3: Create private GitHub repo

```bash
gh repo create <REPO_NAME> --private --description "Claude Code configuration backup"
```

## Step 4: Get SSH remote URL

```bash
gh repo view <REPO_NAME> --json sshUrl --jq '.sshUrl'
```

## Step 5: Initialize local repo and push

```bash
python3 "$(find ~/.claude/plugins -name "cli.py" -path "*/sync*" 2>/dev/null | head -1)" --init --remote <SSH_URL> --target ~/dotfiles/claude
```

## Step 6: Export config and push

```bash
python3 "$(find ~/.claude/plugins -name "cli.py" -path "*/sync*" 2>/dev/null | head -1)" --export --target ~/dotfiles/claude --push
```

## Step 7: Confirm

Tell the user setup is complete, show the repo URL, and remind them to use `/sync:push` to save settings anytime.
