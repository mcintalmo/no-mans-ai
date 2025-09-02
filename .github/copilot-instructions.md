# Copilot Instructions – NMS Co‑Pilot Project

## Project Overview

This repository implements a **modular, voice‑controlled AI companion** for *No Man’s Sky*.  
The system listens to microphone input, parses spoken commands into structured intents, and dispatches them to one or more backends (e.g., Voice Attack, AutoHotkey, Lua mod API).  
It is designed to be **configurable, extendable, and backend‑agnostic**.

## Core Architecture

```
[Mic Input] → [STT Engine] → [Intent Parser] → [Action Dispatcher] → [Game Backend]
```

### Modules

- **`stt/`** – Speech‑to‑Text engines (Vosk, Whisper, etc.), all implementing a common interface.
- **`intents/`** – Intent parsing logic. Start with regex; later support LLM‑based parsing (Ollama, GPT).
- **`dispatchers/`** – Action execution backends (Voice Attack, AutoHotkey, Lua socket/HTTP, mock).
- **`llm/`** – Local or remote LLM clients for advanced parsing and personality.
- **`utils/`** – Shared helpers (config loading, logging, schema validation).
- **`tests/`** – Unit and integration tests for each layer.

## Design Principles

- **Layer isolation** – STT, parsing, and dispatching are independent and swappable.
- **Schema‑driven config** – Commands, patterns, and mappings live in YAML/JSON, not hardcoded.
- **Backend‑agnostic** – No direct coupling to Voice Attack or any single control method.
- **Extensibility** – Easy to add new STT engines, parsers, or dispatchers without breaking existing code.
- **Testability** – Include mocks and logging for safe iteration.

## Coding Guidelines

- Use **Python 3.10+**.
- Follow **PEP 8** style and type‑hint all public functions.
- Keep functions small and single‑purpose.
- Use dependency injection for STT, parser, and dispatcher instances.
- Log all recognized text, parsed intents, and dispatched actions.
- Avoid hardcoding paths; load from `config.yaml`.
