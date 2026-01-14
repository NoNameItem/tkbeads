# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

tkbeads is a TUI application for the [Beads](https://github.com/steveyegge/beads) task tracker, built with Textual. It provides a Kanban board interface for viewing and managing tasks stored in `.beads/issues.jsonl`.

**Requirements:** Python 3.14+

## Development Commands

```bash
# Activate virtual environment
source .venv/bin/activate

# Install dependencies (including dev tools)
uv sync --all-groups

# Run the application
python -m tkbeads

# Linting and formatting
ruff check .           # Check for lint errors
ruff check --fix .     # Auto-fix lint errors
ruff format .          # Format code

# Type checking
ty check src/
```

## Architecture

The design follows a three-layer architecture:

```
UI Layer (Textual)     → KanbanScreen, TaskDetailModal
State Layer            → TaskStore (reactive state)
Data Layer             → BeadsLoader + FileWatcher
```

**Data flow:**
- Read: FileWatcher → BeadsLoader → TaskStore → UI updates
- Write: UI action → TaskStore.update_status() → BeadsLoader.save() → file updated

## Planned Project Structure

```
src/tkbeads/
├── __main__.py          # Entry point
├── app.py               # TkbeadsApp
├── data/
│   ├── models.py        # Task, Status dataclasses
│   ├── loader.py        # BeadsLoader (reads/writes issues.jsonl)
│   └── watcher.py       # FileWatcher
├── store/
│   └── task_store.py    # TaskStore (reactive state)
├── ui/
│   ├── screens/kanban.py
│   ├── widgets/board.py, card.py
│   └── modals/detail.py
└── styles/app.tcss
```

## Key Domain Concepts

**Task statuses and column mapping:**
- BLOCKED column: `status == open` AND has open blockers
- READY column: `status == open` AND no open blockers
- IN_PROGRESS column: `status == in_progress`
- CLOSED column: `status == closed`

**Task hierarchy:** Tasks can have parent-child relationships via `parent_id`. Children display with ancestor chains when in different columns than parents.
