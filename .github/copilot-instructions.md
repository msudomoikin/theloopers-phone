# Copilot Instructions for theloopers-phone

## Project Overview
- This repo contains two main implementations: a TypeScript/Vite web app (`js/`) and a Python CLI (`py/`).
- The web app simulates a phone keypad, tone generation, and phonebook features. The Python codebase mirrors similar logic for CLI purposes.

## Architecture & Key Components
- **js/src/**: Main TypeScript source. Key files:
  - `Phone.ts`: Central class for phone logic. Now HAS-A `Numpad` (see `Numpad.ts`).
  - `Numpad.ts`: Encapsulates keypad logic, extracted from `main.ts`.
  - `TonePlayer.ts`, `TonePlayerVanilla.ts`: DTMF tone generation.
  - `phonebook.ts`: Phonebook management.
  - `main.ts`: App entry point; wires up UI and main classes.
- **py/**: Python analogs for phone, numpad, tone player, etc. Used for CLI.

## Developer Workflows
- **Web App (js/):**
  - Build: `npm run build` (uses Vite)
  - Dev: `npm run dev`
  - Test: No standard JS tests found; add to `js/` if needed.
- **Python (py/):**
  - Run: `python main.py` (entry point)
  - Dependencies: See `requirements.txt`

## Patterns & Conventions
- **TypeScript:**
  - Use classes for main entities (Phone, Numpad, TonePlayer).
  - UI logic is separated from business logic (see `main.ts` vs. `Phone.ts`).
  - Prefer composition (Phone HAS-A Numpad) over inheritance.
- **Python:**
  - Mirrors JS structure for parity; keep logic consistent across languages.

## Integration Points
- **Audio:**
  - Web: Uses `TonePlayer` for DTMF; assets in `js/src/assets/`.
  - Python: `tone-player.py` for CLI audio.
- **Phonebook:**
  - Shared logic in both JS and Python.

## External Dependencies
- JS: Vite, TypeScript, browser APIs for audio.
- Python: Standard library, see `requirements.txt` for extras.

## Examples
- To add a new keypad feature, update `Numpad.ts` and wire it in `Phone.ts`.
- For new phonebook logic, update both `js/src/phonebook.ts` and `py/phonebook.py`.

## Key Files
- `js/src/Phone.ts`, `js/src/Numpad.ts`, `js/src/main.ts`, `py/phone.py`, `py/numpad.py`

---
