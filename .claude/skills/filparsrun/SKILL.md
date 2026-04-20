---
description: Запуск FilPars (парсер + дашборд)
---
Запусти главное окно FilPars:

1. Проверь что зависимости установлены: `python -c "import webview, playwright; print('OK')"` (Mac: `python3 -c ...`)
2. Если нет — сначала запусти `/filpars-install`
3. ЗАПУСК ИНТЕРФЕЙСА: Получи жёсткий путь, который был сохранён при установке:
   - Mac/Linux: `cat ~/.filpars_path`
   - Windows: `type $env:USERPROFILE\.filpars_path`
   Это и есть АБСОЛЮТНЫЙ ПУТЬ к папке парсера. Если файла нет — запусти `/filpars-install`.
4. Запусти парсер в ОТДЕЛЬНОМ окне:
   - **macOS**: `osascript -e 'tell app "Terminal" to do script "cd <ПУТЬ> && python3 run_scraper.py"'`
   - **Windows**: `cmd /c start python <АБСОЛЮТНЫЙ_ПУТЬ>\run_scraper.py`
   ОБЯЗАТЕЛЬНО сделай это сам!
5. Сообщи пользователю что окно открыто и готово к работе.
