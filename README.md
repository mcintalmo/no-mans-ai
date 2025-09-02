# No Man's AI — voice companion for No Man's Sky

Lightweight, modular voice-controlled AI companion for No Man's Sky. The project listens to
microphone input, converts speech to text, parses intents, and dispatches actions to backends such
as Voice Attack, AutoHotkey, or an in-game Lua mod.

## Features

- Pluggable STT engines (Vosk by default)
- Regex-based intent parsing with easy-to-add commands
- Backend-agnostic action dispatching
- Designed for local-first, testable development

## Quick start (Windows)

1. Create and activate a Python virtual environment (recommended):

```powershell
uv venv
.\.venv\Scripts\Activate.ps1
```

2. Install dependencies (project uses `pyproject.toml` — use your preferred tool). Example with pip:

```powershell
uv sync
```

3. Download a Vosk model and install it as `./models` in the repo root (or set `VOSK_MODEL_PATH`):

PowerShell example:

```powershell
# Download small English model
Invoke-WebRequest -Uri 'https://alphacephei.com/vosk/models/vosk-model-small-en-us-0.15.zip' -OutFile 'vosk-model-small-en-us-0.15.zip'
Expand-Archive -Path 'vosk-model-small-en-us-0.15.zip' -DestinationPath '.\models'
Rename-Item -Path '.\models\vosk-model-small-en-us-0.15'
```

Alternatively, set the environment variable before running:

```powershell
$env:VOSK_MODEL_PATH = 'C:\path\to\vosk-model-small-en-us-0.15'
```

4. Run the app:

```powershell
uv run src/main.py
```

## Where to look in the code

- `src/main.py` — simple end-to-end example: STT setup, intent parsing, and action triggering.
- `src/stt/`, `src/intent/`, `src/dispatch/` — modular components (expand these folders with new engines or backends).

## Tests

- Unit tests live in `tests/`. Run them with your test runner (e.g., `pytest`).
