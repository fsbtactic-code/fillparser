# Banana Parser — Claude Code Instructions

## What is this?

Banana Parser — Instagram stealth scraper that finds viral competitor content. It runs as a desktop GUI (pywebview + Playwright).

## Quick Setup (run these commands)

```bash
python install_all.py
python auth.py        # one-time Instagram login
python run_scraper.py # launch the app
```

## If something breaks

1. Read `.ai-context.md` for architecture and known issues
2. Common fixes:
   - `storage_state.json not found` → run `python auth.py`
   - `playwright` errors → run `python -m playwright install chromium`
   - Import errors → run `pip install -r requirements.txt`

## File Map

- `run_scraper.py` — entry point, GUI + background worker
- `skills.py` — scraping logic (feed, explore, search, virality scoring)
- `interceptor.py` — passive network interception, PostFilter
- `browser_core.py` — stealth Playwright browser
- `auth.py` — Instagram login flow
- `web_launcher.py` — pywebview window
- `ui_templates/launcher.html` — full UI (settings + dashboard)
- `install_all.py` — universal installer

## Rules

- NEVER commit `storage_state.json` (contains user's Instagram session)
- Browser must run in `headless=False` mode (Instagram blocks headless)
- Always use `PostFilter` with `max_age_hours` to filter old posts
- Search scrolls are limited to 12 per keyword
