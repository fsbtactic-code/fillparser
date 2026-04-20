# FilPars — Claude Code Instructions

## Slash Commands

- `/filpars-install` — Установить всё: зависимости, Playwright, проверить готовность
- `/filparsauth`    — Открыть защищённое окно для входа в Instagram
- `/filparsrun`     — Запустить главное окно парсера (в отдельном процессе)
- `/filpars-debug`  — Диагностика и автоматический самодебаг при проблемах

## What is this?

FilPars — Instagram stealth scraper. Десктопное приложение (pywebview + Playwright) для поиска вирусного контента конкурентов. Поддерживает macOS, Windows, Linux.

## Quick Setup

```bash
python install_all.py    # установка всего
python auth.py           # авторизация Instagram (один раз)
python run_scraper.py    # запуск GUI
```

## If something breaks

1. Run `/filpars-debug` — Claude Code сам диагностирует и чинит
2. Read `.ai-context.md` for architecture and known issues
3. Common fixes:
   - `storage_state.json not found` → run `python auth.py`
   - `playwright` errors → run `python -m playwright install chromium`
   - Import errors → run `pip install -r requirements.txt`
   - macOS WebView → `pip install pyobjc-framework-WebKit`
   - Window doesn't resize → already fixed, uses native OS title bar

## File Map

| File | Purpose |
|------|---------| 
| `run_scraper.py` | Entry point — GUI + background worker thread |
| `skills.py` | Scraping logic: feed, explore, search, virality scoring |
| `interceptor.py` | Passive network interception, PostData, PostFilter |
| `browser_core.py` | Stealth Playwright browser with media blocking |
| `auth.py` | Instagram login flow (headed browser) |
| `web_launcher.py` | pywebview window creation |
| `mcp_server.py` | MCP server for Claude Code (tools incl. launch_gui) |
| `ui_templates/launcher.html` | Full UI: settings panel + results dashboard |
| `install_all.py` | Universal cross-platform installer (Win/Mac/Linux) |
| `assets/logo.svg` | FilPars brand logo |

## Rules

- NEVER commit `storage_state.json` (user's Instagram session)
- Browser runs `headless=False` (Instagram blocks headless)
- PostFilter always uses `max_age_hours` to filter old posts
- Search scrolls limited to 12 per keyword by default (7 in bulk AI mode)
- All scraping happens in a daemon thread, GUI stays responsive
