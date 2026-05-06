---
description: List all Claude Code components tracked by sync (skills, commands, agents, rules, settings)
allowed-tools: [Bash]
---

Run immediately:

```bash
python3 "$(find ~/.claude/plugins -name "cli.py" -path "*/sync*" 2>/dev/null | head -1)" --list
```
