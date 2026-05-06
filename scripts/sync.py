#!/usr/bin/env python3
"""Main sync logic for claude-sync plugin."""

import argparse
import shutil
import subprocess
import sys
from datetime import datetime
from pathlib import Path

from filter import (
    should_exclude_file,
    filter_file_content,
    get_syncable_components,
    get_excluded_components,
)

# Default claude config directory
DEFAULT_CLAUDE_DIR = Path.home() / '.claude'


def run_git(cmd: list[str], cwd: Path, capture: bool = True) -> tuple[int, str, str]:
    """Run a git command and return (returncode, stdout, stderr)."""
    try:
        result = subprocess.run(
            cmd,
            cwd=cwd,
            capture_output=True,
            text=True,
        )
        return result.returncode, result.stdout, result.stderr
    except FileNotFoundError:
        return 1, "", "git not found"
    except Exception as e:
        return 1, "", str(e)


def export_claude_config(source: Path, target: Path, dry_run: bool = False, verbose: bool = True):
    """Export claude config from source to target."""
    if not source.exists():
        print(f"Error: Source directory {source} does not exist", file=sys.stderr)
        return False

    if not dry_run and not target.exists():
        target.mkdir(parents=True, exist_ok=True)

    syncable = get_syncable_components()
    excluded = get_excluded_components()
    files_synced = []
    files_excluded = []
    files_filtered = []

    for component in syncable:
        src_path = source / component
        dst_path = target / component

        if not src_path.exists():
            continue

        if src_path.is_dir():
            # Sync directory
            for item in src_path.rglob('*'):
                if item.is_file():
                    rel_path = item.relative_to(src_path)
                    dst_item = dst_path / rel_path

                    if should_exclude_file(item):
                        files_excluded.append(str(rel_path))
                        continue

                    if not dry_run:
                        dst_item.parent.mkdir(parents=True, exist_ok=True)
                        content = filter_file_content(item)
                        dst_item.write_text(content, encoding='utf-8')
                    files_synced.append(str(rel_path))
                    files_filtered.append(str(rel_path))
        else:
            # Sync single file
            if should_exclude_file(src_path):
                files_excluded.append(component)
                continue

            if not dry_run:
                content = filter_file_content(src_path)
                dst_path.write_text(content, encoding='utf-8')
            files_synced.append(component)

    if verbose:
        print(f"\n{'[DRY RUN] ' if dry_run else ''}Export Summary:")
        print(f"  Files synced: {len(files_synced)}")
        print(f"  Files excluded: {len(files_excluded)}")

        if files_excluded:
            print(f"\n  Excluded files:")
            for f in files_excluded[:10]:
                print(f"    - {f}")
            if len(files_excluded) > 10:
                print(f"    ... and {len(files_excluded) - 10} more")

    return True


def git_init(target: Path, remote: str | None = None, verbose: bool = True) -> bool:
    """Initialize a git repo at target, optionally add a remote and push."""
    target.mkdir(parents=True, exist_ok=True)

    rc, _, _ = run_git(['git', 'rev-parse', '--git-dir'], target)
    if rc == 0:
        print(f"{target} is already a git repository")
        return True

    rc, _, stderr = run_git(['git', 'init', '-b', 'main'], target)
    if rc != 0:
        print(f"Error during git init: {stderr}", file=sys.stderr)
        return False

    if verbose:
        print(f"Initialized git repository at {target}")

    if remote:
        rc, _, stderr = run_git(['git', 'remote', 'add', 'origin', remote], target)
        if rc != 0:
            print(f"Error adding remote: {stderr}", file=sys.stderr)
            return False
        if verbose:
            print(f"Remote set to {remote}")

    # Initial empty commit so the branch exists
    rc, _, stderr = run_git(['git', 'commit', '--allow-empty', '-m', 'Initial commit'], target)
    if rc != 0:
        print(f"Error during initial commit: {stderr}", file=sys.stderr)
        return False

    if remote:
        rc, _, stderr = run_git(['git', 'push', '-u', 'origin', 'main'], target)
        if rc != 0:
            print(f"Error during initial push: {stderr}", file=sys.stderr)
            return False
        if verbose:
            print("Pushed to remote — ready to use /sync:push")

    return True


def git_push(target: Path, message: str | None = None, verbose: bool = True) -> bool:
    """Git add, commit, and push to remote."""
    if not target.exists():
        print(f"Error: Target directory {target} does not exist", file=sys.stderr)
        return False

    # Check if it's a git repo
    rc, _, _ = run_git(['git', 'rev-parse', '--git-dir'], target)
    if rc != 0:
        print(f"Error: {target} is not a git repository", file=sys.stderr)
        print("Run: cd TARGET && git init && git remote add origin URL", file=sys.stderr)
        return False

    # Git add
    rc, _, stderr = run_git(['git', 'add', '-A'], target)
    if rc != 0:
        print(f"Error during git add: {stderr}", file=sys.stderr)
        return False

    # Check if there are changes to commit
    rc, stdout, _ = run_git(['git', 'status', '--porcelain'], target)
    if not stdout.strip():
        if verbose:
            print("Nothing to commit - working tree clean")
        return True

    # Git commit
    msg = message or f"Claude config sync {datetime.now().isoformat()}"
    rc, _, stderr = run_git(['git', 'commit', '-m', msg], target)
    if rc != 0:
        print(f"Error during git commit: {stderr}", file=sys.stderr)
        return False

    if verbose:
        print(f"Committed: {msg}")

    # Git push
    rc, _, stderr = run_git(['git', 'push', '-u', 'origin', 'HEAD'], target)
    if rc != 0:
        print(f"Error during git push: {stderr}", file=sys.stderr)
        return False

    if verbose:
        print("Pushed to remote")

    return True


def git_pull(source: Path, verbose: bool = True) -> bool:
    """Git pull from remote to source directory."""
    if not source.exists():
        print(f"Error: Source directory {source} does not exist", file=sys.stderr)
        return False

    # Check if it's a git repo
    rc, _, _ = run_git(['git', 'rev-parse', '--git-dir'], source)
    if rc != 0:
        print(f"Error: {source} is not a git repository", file=sys.stderr)
        return False

    # Git stash local changes first (to protect uncommitted local work)
    rc, stdout, _ = run_git(['git', 'status', '--porcelain'], source)
    if stdout.strip():
        if verbose:
            print("Stashing local changes...")
        rc, _, stderr = run_git(['git', 'stash'], source)
        if rc != 0:
            print(f"Error during git stash: {stderr}", file=sys.stderr)
            return False

    # Git pull
    rc, _, stderr = run_git(['git', 'pull', '--rebase', 'origin', 'HEAD'], source)
    if rc != 0:
        print(f"Error during git pull: {stderr}", file=sys.stderr)
        return False

    if verbose:
        print("Pulled from remote")

    return True


def import_claude_config(source: Path, target: Path, dry_run: bool = False, verbose: bool = True):
    """Import claude config from source to target (~/.claude)."""
    if not source.exists():
        print(f"Error: Source directory {source} does not exist", file=sys.stderr)
        return False

    if not dry_run:
        # Backup existing config first
        backup_dir = target.parent / '.claude.bak'
        if target.exists() and not backup_dir.exists():
            print(f"Creating backup at {backup_dir}...")
            shutil.copytree(target, backup_dir, dirs_exist_ok=True)

    syncable = get_syncable_components()
    files_imported = []

    for component in syncable:
        src_path = source / component
        dst_path = target / component

        if not src_path.exists():
            continue

        if not dry_run:
            if dst_path.exists():
                if dst_path.is_dir():
                    shutil.rmtree(dst_path)
                else:
                    dst_path.unlink()
            shutil.copytree(src_path, dst_path)
        files_imported.append(component)

    if verbose:
        print(f"\n{'[DRY RUN] ' if dry_run else ''}Import Summary:")
        print(f"  Components imported: {len(files_imported)}")

    return True


def list_components(claude_dir: Path = DEFAULT_CLAUDE_DIR, verbose: bool = True):
    """List all syncable components and their status."""
    if not claude_dir.exists():
        print(f"Error: {claude_dir} does not exist", file=sys.stderr)
        return False

    syncable = get_syncable_components()
    excluded = get_excluded_components()

    print("\nClaude Config Components:")
    print("\n  Syncable:")
    for component in syncable:
        path = claude_dir / component
        status = "✓" if path.exists() else "✗"
        print(f"    {status} {component}")

    print("\n  Excluded (never synced):")
    for component in sorted(excluded):
        print(f"    - {component}")

    return True


def diff_config(source: Path, target: Path, verbose: bool = True):
    """Show differences between source and target."""
    if not source.exists():
        print(f"Error: Source directory {source} does not exist", file=sys.stderr)
        return False

    print(f"\nDiff: {source} -> {target}")
    print("(This feature is a placeholder - full diff coming soon)")

    return True


def status(claude_dir: Path = DEFAULT_CLAUDE_DIR, verbose: bool = True):
    """Show sync status."""
    if not claude_dir.exists():
        print(f"Error: {claude_dir} does not exist", file=sys.stderr)
        return False

    syncable = get_syncable_components()
    total = 0
    existing = 0

    for component in syncable:
        path = claude_dir / component
        if path.exists():
            if path.is_dir():
                total += len(list(path.rglob('*')))
            else:
                total += 1
            existing += 1

    print(f"\nStatus:")
    print(f"  Config directory: {claude_dir}")
    print(f"  Components: {existing}/{len(syncable)}")
    print(f"  Total files: ~{total}")

    return True


def main():
    parser = argparse.ArgumentParser(description='Claude Sync - Backup and sync Claude Code config')
    parser.add_argument('--export', action='store_true', help='Export config to target directory')
    parser.add_argument('--import', dest='import_config', action='store_true', help='Import config from source directory')
    parser.add_argument('--push', action='store_true', help='Git push after export')
    parser.add_argument('--pull', action='store_true', help='Git pull before import')
    parser.add_argument('--target', type=Path, help='Target directory for export')
    parser.add_argument('--source', type=Path, help='Source directory for import')
    parser.add_argument('--claude-dir', type=Path, default=DEFAULT_CLAUDE_DIR, help=f'Claude dir (default: {DEFAULT_CLAUDE_DIR})')
    parser.add_argument('--dry-run', action='store_true', help='Preview without making changes')
    parser.add_argument('--list', action='store_true', help='List all components')
    parser.add_argument('--diff', action='store_true', help='Show differences')
    parser.add_argument('--status', action='store_true', help='Show sync status')
    parser.add_argument('--init', action='store_true', help='Initialize git repo at target directory')
    parser.add_argument('--remote', type=str, help='Remote URL for --init')
    parser.add_argument('--quiet', action='store_true', help='Suppress output')

    args = parser.parse_args()

    verbose = not args.quiet

    if args.init:
        target = args.target or Path.home() / 'dotfiles' / 'claude'
        return git_init(target, args.remote, verbose)

    if args.list:
        return list_components(args.claude_dir, verbose)

    if args.status:
        return status(args.claude_dir, verbose)

    if args.diff:
        if not args.target:
            print("Error: --diff requires --target", file=sys.stderr)
            return False
        return diff_config(args.claude_dir, args.target, verbose)

    if args.export:
        if not args.target:
            print("Error: --export requires --target", file=sys.stderr)
            return False
        success = export_claude_config(args.claude_dir, args.target, args.dry_run, verbose)
        if success and args.push and not args.dry_run:
            return git_push(args.target, verbose=verbose)
        return success

    if args.import_config:
        if not args.source:
            print("Error: --import requires --source", file=sys.stderr)
            return False
        if args.pull and not args.dry_run:
            if not git_pull(args.source, verbose=verbose):
                return False
        return import_claude_config(args.source, args.claude_dir, args.dry_run, verbose)

    # Default: show status
    return status(args.claude_dir, verbose)


if __name__ == '__main__':
    sys.exit(0 if main() else 1)