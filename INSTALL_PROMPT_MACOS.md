# FilPars — macOS Setup Prompt for Claude Code

Copy the text below and paste it into Claude Code to have it install FilPars automatically.

---

## 🚀 Установочный промпт (вставить в Claude Code)

```
Установи FilPars Instagram парсер у меня на Mac. Вот инструкции шаг за шагом:

1. Проверь что есть Python 3.10+: `python3 --version`. Если нет — скажи мне установить через brew: `brew install python@3.12`

2. Найди папку с проектом — ищи ТОЛЬКО в этих директориях (не делай глобальный find!):
   - `./filpars`
   - `../filpars`  
   - `~/filpars`
   - `~/Documents/filpars`
   - `./virealresearcher`
   - `~/virealresearcher`
   
   Если НЕ нашёл — клонируй: `git clone https://github.com/fsbtactic-code/virealresearcher.git ~/filpars`
   
   Если нашёл — обнови: `cd <путь> && git pull`
   
   Запомни АБСОЛЮТНЫЙ ПУТЬ к папке проекта.

3. Перейди в папку проекта и запусти установщик:
   ```
   cd <АБСОЛЮТНЫЙ_ПУТЬ>
   python3 install_all.py
   ```
   
   Если увидишь ошибки:
   - `xcode-select --install` нужен → дай мне нажать Install в диалоге, потом перезапусти
   - pip ошибка → `python3 -m ensurepip --upgrade && python3 install_all.py`
   - playwright ошибка → `python3 -m playwright install chromium`
   - WebView ошибка → `pip3 install pyobjc-framework-WebKit pyobjc-core`

4. Скопируй скиллы в текущий проект (если нужно):
   ```
   cp -r <ПУТЬ_К_FILPARS>/.claude/skills/* ./.claude/skills/
   ```
   
5. Добавь MCP сервер в `~/.claude.json`. Найди или создай файл и добавь в секцию `mcpServers`:
   ```json
   "filpars": {
     "command": "python3",
     "args": ["<АБСОЛЮТНЫЙ_ПУТЬ>/mcp_server.py"],
     "cwd": "<АБСОЛЮТНЫЙ_ПУТЬ>"
   }
   ```
   Используй реальный путь из шага 2.

6. Проверь что всё работает:
   ```
   python3 -c "import webview, playwright, playwright_stealth, pydantic, mcp; print('✅ Все пакеты OK')"
   python3 -c "from interceptor import PostFilter; print('✅ Interceptor OK')"
   ```

7. Запусти авторизацию Instagram (нужен запасной аккаунт!):
   Открой новый терминал и запусти:
   ```
   cd <АБСОЛЮТНЫЙ_ПУТЬ> && python3 auth.py
   ```
   
   Залогинься в браузере. После закрытия окна — напиши мне.

8. После авторизации запусти главное окно:
   ```
   cd <АБСОЛЮТНЫЙ_ПУТЬ> && python3 run_scraper.py
   ```

Если что-то пошло не так на любом шаге — прочитай `.ai-context.md` в папке проекта и исправь ошибку самостоятельно. Потом сообщи мне что именно исправил.
```

---

## Quick Commands (macOS Terminal)

```bash
# Install
git clone https://github.com/fsbtactic-code/virealresearcher.git ~/filpars
cd ~/filpars
python3 install_all.py

# Auth
python3 auth.py

# Run
python3 run_scraper.py
```

## Troubleshooting macOS

| Problem | Solution |
|---------|----------|
| `xcode-select: error` | `xcode-select --install` (click Install) |
| `No module named 'webview'` | `pip3 install pywebview` |
| `objc error` on WebView start | `pip3 install pyobjc-framework-WebKit pyobjc-core` |
| `playwright not found` | `pip3 install playwright && python3 -m playwright install chromium` |
| Window doesn't open | Check `scraper.log` in project dir |
| MCP not found in Claude | Edit `~/.claude.json`, add `"filpars"` block (see above) |

## Required Python Packages

```
playwright>=1.40.0
playwright-stealth>=1.0.6
pywebview>=5.0
pydantic>=2.0.0
mcp
pyobjc-framework-WebKit   # macOS only
pyobjc-core               # macOS only
```
