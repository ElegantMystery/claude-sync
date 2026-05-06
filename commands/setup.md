---
description: Set up Claude Code config sync — creates a private GitHub repo and initializes ~/dotfiles/claude automatically.
argument-hint: []
allowed-tools: [Bash]
---

# Setup Claude Sync

## Step 1: Check current state

```bash
python3 "$(find ~/.claude/plugins -name "cli.py" -path "*/sync*" 2>/dev/null | head -1)" --status
```

- If output shows `Git repo: ✓` — tell the user they are already set up and stop here.
- If output shows `Git repo: ✗` — continue to Step 2.

## Step 2: Ask how to set up

Present exactly this choice to the user:

```
How would you like to set up sync?

  1) Create a new private GitHub repo
  2) Use an existing GitHub repo

Enter 1 or 2:
```

Wait for the user's response before proceeding.

## Step 3a: If user chose 1 — Create new repo

Ask in a single message:
> What would you like to name the new repo? (e.g. `dotfiles` or `claude-config`)

Wait for the user's response, then:

```bash
gh repo create <REPO_NAME> --private --description "Claude Code configuration backup"
```

Get SSH URL:

```bash
gh repo view <REPO_NAME> --json sshUrl --jq '.sshUrl'
```

Use the SSH URL as `<REMOTE_URL>` in Step 4.

## Step 3b: If user chose 2 — Use existing repo

Ask in a single message:
> Paste the SSH or HTTPS URL of your existing GitHub repo:

Wait for the user's response. Use the pasted URL as `<REMOTE_URL>` in Step 4.

## Step 4: Initialize local repo and push

```bash
python3 "$(find ~/.claude/plugins -name "cli.py" -path "*/sync*" 2>/dev/null | head -1)" --init --remote <REMOTE_URL> --target ~/dotfiles/claude
```

## Step 5: Export config and push

```bash
python3 "$(find ~/.claude/plugins -name "cli.py" -path "*/sync*" 2>/dev/null | head -1)" --export --target ~/dotfiles/claude --push
```

## Step 6: Confirm

Tell the user setup is complete, show the repo URL, and remind them to use `/sync:push` to save settings anytime.
