"""Secret filtering for claude-sync plugin."""

import re
import json
from pathlib import Path

# Patterns that indicate secrets
SECRET_PATTERNS = [
    # API keys
    (r'sk-[a-zA-Z0-9]{32,}', '[API_KEY]'),
    (r'sk-api-[a-zA-Z0-9]{32,}', '[API_KEY]'),
    # Environment variables with secrets
    (r'(ANTHROPIC_AUTH_TOKEN|MINIMAX_API_KEY|OPENAI_API_KEY|GITHUB_PERSONAL_ACCESS_TOKEN)["\']?\s*[:=]\s*["\'][^"\']{10,}["\']', '[REDACTED]'),
    # Bearer tokens
    (r'Bearer\s+[a-zA-Z0-9_-]{20,}', '[BEARER_TOKEN]'),
    # Token patterns in JSON values
    (r'"(token|api_key|apiKey|secret|Secret)["\']\s*:\s*["\'][a-zA-Z0-9_-]{20,}["\']', '"[REDACTED]"'),
    # ghp_ tokens (GitHub Personal Access Tokens)
    (r'ghp_[a-zA-Z0-9]{36,}', '[GITHUB_TOKEN]'),
    # UUIDs that look like session IDs
    (r'[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12}', '[SESSION_ID]'),
]

# Files that are never exported
EXCLUDED_FILES = {
    'credentials.json',
    '.credentials',
    'settings.local.json',
    'history.jsonl',
    '.DS_Store',
    'desktop.ini',
}

# Directories that are never exported
EXCLUDED_DIRS = {
    'cache',
    'sessions',
    'telemetry',
    'backups',
    'tasks',
    'plans',
    'session-env',
    'file-history',
    'debug',
    'downloads',
    'ide',
    'paste-cache',
    'shell-snapshots',
    'statsig',
    'todos',
    '.git',
    '.svn',
    '.hg',
}

# Extensions that are never exported
EXCLUDED_EXTENSIONS = {'.log', '.swp', '.swo', '.bak', '.tmp'}


def should_exclude_file(path: Path) -> bool:
    """Check if a file should be excluded from sync."""
    if path.name in EXCLUDED_FILES:
        return True
    if path.suffix in EXCLUDED_EXTENSIONS:
        return True
    for parent in path.parts:
        if parent in EXCLUDED_DIRS:
            return True
    return False


def filter_secrets_in_text(text: str) -> str:
    """Apply secret filtering to text content."""
    result = text
    for pattern, replacement in SECRET_PATTERNS:
        result = re.sub(pattern, replacement, result, flags=re.IGNORECASE)
    return result


def filter_json_content(content: str) -> str:
    """Filter secrets from JSON content."""
    try:
        data = json.loads(content)
        filtered_data = _filter_dict_recursive(data)
        return json.dumps(filtered_data, indent=2)
    except json.JSONDecodeError:
        return filter_secrets_in_text(content)


def _filter_dict_recursive(obj):
    """Recursively filter secrets in dict values."""
    if isinstance(obj, dict):
        return {k: _filter_dict_recursive(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [_filter_dict_recursive(item) for item in obj]
    elif isinstance(obj, str):
        return filter_secrets_in_text(obj)
    else:
        return obj


def filter_file_content(path: Path) -> str:
    """Read and filter file content based on file type."""
    if not path.exists():
        return ""

    content = path.read_text(encoding='utf-8')

    if path.suffix == '.json':
        return filter_json_content(content)
    else:
        return filter_secrets_in_text(content)


# Components that are synced
SYNC_COMPONENTS = [
    'skills',
    'commands',
    'agents',
    'rules',
    'keybindings.json',
    'settings.json',
]

# Components that are always excluded
ALWAYS_EXCLUDED = {
    'credentials.json',
    '.credentials.json',
    'settings.local.json',
}


def get_syncable_components():
    """Return list of components that can be synced."""
    return SYNC_COMPONENTS.copy()


def get_excluded_components():
    """Return list of components that are never synced."""
    return list(EXCLUDED_FILES | ALWAYS_EXCLUDED | EXCLUDED_DIRS)