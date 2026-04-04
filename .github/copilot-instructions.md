# Copilot Instructions

## Project Overview

Docker Deck is a lightweight web dashboard for real-time monitoring and management of Docker containers. It renders a card-based UI auto-refreshing every 5 seconds, showing each container's state, ports, and image. It runs as a Python app (locally or in Docker) and is accessible at `http://localhost:80`.

## Tech Stack

- **Python 3.13+** (uses match-case, modern generic type hints like `list[T]`)
- **NiceGUI** — UI framework built on Quasar/Vue.js; all UI is Python-first
- **Pydantic v2** — data validation via `BaseModel`
- **uv** — package manager and runner

## Architecture

```
main.py                   # Entry point: NiceGUI layout, styling, auto-refresh timer
docker_deck/
  models.py               # Service (Pydantic BaseModel) + ServiceState (Enum)
  data_gather.py          # Docker CLI interaction and JSON parsing → list[Service]
background_images/        # Static assets served by NiceGUI
```

**Data flow:** `main_ui()` (decorated `@ui.refreshable`) calls `get_running_containers()`, which runs `docker ps -a --format json`, parses the output, and returns `list[Service]`. The UI re-renders by calling `main_ui.refresh()`.

## Commands

```bash
uv sync           # Install all dependencies (including dev)
uv run main.py    # Run the app locally (serves on http://localhost:80)
flake8 .          # Lint
mypy .            # Type check
pylint .          # Code analysis
```

No test suite currently exists.

## Key Conventions

- **Pydantic models** for all domain data — don't use plain dicts or dataclasses for `Service`-like objects.
- **`@ui.refreshable`** for any UI function that needs reactive updates; trigger re-render with `fn.refresh()`.
- **NiceGUI context managers** for layout composition:
  ```python
  with ui.card():
      with ui.grid(columns=2):
          ...
  ```
- **match-case** for type-safe branching (e.g., regex match results in `parse_ports()`).
- **Inline error handling** in data gathering — return empty list `[]` on Docker CLI failure rather than raising.
- **Subprocess over Docker SDK** — Docker is accessed via `subprocess.run(["docker", ...])`, not the Python Docker SDK.
- Type hints use modern syntax (`list[Service]`, `dict`, not `List`, `Dict` from `typing`).
- Enum values are UPPERCASE; classes are PascalCase; functions are snake_case.
- UI styling uses Quasar CSS classes plus custom glass-morphism CSS injected via `ui.add_head_html()`.
