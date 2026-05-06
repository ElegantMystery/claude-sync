---
description: Show Claude Code sync status — which components are tracked and how many files
allowed-tools: [Bash]
---

Run immediately:

```bash
python3 "$(find ~/.claude/plugins -name "cli.py" -path "*/sync*" 2>/dev/null | head -1)" --status
```
