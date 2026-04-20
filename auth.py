"""
auth.py — Instagram login flow with Playwright.

Opens a headed Chromium browser for manual Instagram login.
Saves session cookies to storage_state.json for headless reuse.
Includes a safety warning about using a secondary account.
"""
import asyncio
import json
import os
import sys
from pathlib import Path

if sys.stdout.encoding.lower() != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

PROJECT_ROOT = Path(__file__).parent.resolve()
STORAGE_STATE = PROJECT_ROOT / "storage_state.json"

# ── Terminal color helpers ──
def _c(code: str, text: str) -> str:
    return f"\033[{code}m{text}\033[0m"

RED    = lambda t: _c("91", t)
YELLOW = lambda t: _c("93", t)
GREEN  = lambda t: _c("92", t)
CYAN   = lambda t: _c("96", t)
BOLD   = lambda t: _c("1", t)
DIM    = lambda t: _c("2", t)


CUSTOM_CSS = """
/* ═══════════════════════════════════════════════
   FilPars — Dark Blue Glass Theme for Instagram
   ═══════════════════════════════════════════════ */

@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600&display=swap');

/* ── Base ── */
*, *::before, *::after {
    box-sizing: border-box !important;
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
}
html, body {
    background: #08080a !important;
    min-height: 100vh !important;
}
body {
    background:
        radial-gradient(ellipse 60% 40% at 20% 20%, rgba(0,89,255,0.12) 0%, transparent 70%),
        radial-gradient(ellipse 50% 35% at 80% 80%, rgba(0,40,120,0.1) 0%, transparent 70%),
        #08080a !important;
}

/* ── Hide Instagram header/footer noise ── */
nav, footer, section > section > div:not(:first-child) {
    display: none !important;
}

/* ── Center the login form like a floating card ── */
main, [role="main"] {
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    min-height: 100vh !important;
    background: transparent !important;
}

/* ── The login box itself ── */
form, div[class*="x1hc1fzr"], div[class*="x1cy8zhl"],
article > div, section > main > div > article {
    background: rgba(255,255,255,0.04) !important;
    border: 1px solid rgba(0,89,255,0.25) !important;
    border-radius: 20px !important;
    backdrop-filter: blur(24px) !important;
    -webkit-backdrop-filter: blur(24px) !important;
    box-shadow:
        0 0 0 1px rgba(0,89,255,0.1),
        0 8px 32px rgba(0,0,0,0.6),
        0 0 60px rgba(0,89,255,0.12),
        inset 0 1px 0 rgba(255,255,255,0.06) !important;
    padding: 32px !important;
}

/* ── All backgrounds transparent ── */
div, section, article, aside {
    background-color: transparent !important;
}

/* ── Instagram logo ── */
i[data-visualcompletion="css-img"] {
    filter: brightness(0) invert(1) !important;
    opacity: 0.9 !important;
}

/* ── Inputs ── */
input[type="text"],
input[type="password"],
input[name="username"],
input[name="password"] {
    background: rgba(0,0,0,0.5) !important;
    border: 1.5px solid rgba(255,255,255,0.1) !important;
    border-radius: 12px !important;
    color: #fff !important;
    padding: 13px 16px !important;
    font-size: 14px !important;
    font-weight: 400 !important;
    transition: border-color 0.2s, box-shadow 0.2s !important;
    caret-color: #0059FF !important;
}
input[type="text"]:focus,
input[type="password"]:focus {
    border-color: rgba(0,89,255,0.8) !important;
    box-shadow: 0 0 0 3px rgba(0,89,255,0.15) !important;
    outline: none !important;
}
input::placeholder {
    color: rgba(255,255,255,0.35) !important;
}

/* ── Password eye toggle ── */
button[type="button"]._aao5 span,
div[role="button"] span {
    color: rgba(255,255,255,0.5) !important;
}

/* ── Primary submit button ── */
button[type="submit"] {
    background: linear-gradient(135deg, #0059FF 0%, #0038CC 100%) !important;
    border: none !important;
    border-radius: 12px !important;
    color: #fff !important;
    font-weight: 600 !important;
    font-size: 14px !important;
    padding: 13px !important;
    width: 100% !important;
    cursor: pointer !important;
    letter-spacing: 0.02em !important;
    box-shadow: 0 4px 14px rgba(0,89,255,0.4) !important;
    transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1) !important;
    opacity: 1 !important;
}
button[type="submit"]:hover {
    background: linear-gradient(135deg, #0070FF 0%, #004FD4 100%) !important;
    box-shadow: 0 6px 20px rgba(0,89,255,0.55) !important;
    transform: translateY(-1px) !important;
}
button[type="submit"]:active {
    transform: translateY(0) !important;
}
button[type="submit"]:disabled {
    background: rgba(0,89,255,0.3) !important;
    box-shadow: none !important;
    transform: none !important;
}

/* ── OR divider ── */
div._ak18,
div[style*="border-top"] {
    border-color: rgba(255,255,255,0.1) !important;
}

/* ── Links ── */
a {
    color: rgba(0,140,255,0.9) !important;
    text-decoration: none !important;
}
a:hover { color: #fff !important; }

/* ── Text ── */
span, p, label {
    color: rgba(255,255,255,0.75) !important;
}
h1, h2, h3 { color: #fff !important; font-weight: 600 !important; }

/* ── Facebook login button ── */
button[type="button"]._acan {
    background: rgba(24,119,242,0.15) !important;
    border: 1px solid rgba(24,119,242,0.3) !important;
    border-radius: 12px !important;
    color: #4a9eff !important;
}
button[type="button"]._acan svg path { fill: #4a9eff !important; }

/* ── Helper text / error ── */
p[role="alert"], span[style*="color"] {
    color: #ff6b6b !important;
}

/* ── FilPars watermark overlay ── */
body::after {
    content: 'FilPars';
    position: fixed;
    bottom: 20px;
    right: 24px;
    font-size: 11px;
    font-weight: 600;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: rgba(0,89,255,0.4);
    pointer-events: none;
    z-index: 99999;
    font-family: 'Inter', sans-serif !important;
}
"""


def print_banner():
    print()
    print(_c("95", "  ╔══════════════════════════════════════════════════════════════╗"))
    print(_c("95", "  ║") + BOLD("🟦  FilPars — Instagram Stealth Scraper              ") + _c("95", "║"))
    print(_c("95", "  ║") + "                                                              " + _c("95", "║"))
    print(_c("95", "  ║") + "  " + CYAN("Авторизация Instagram") + "                                       " + _c("95", "║"))
    print(_c("95", "  ╚══════════════════════════════════════════════════════════════╝"))
    print()


def print_warning():
    print(_c("41;97", "  ⚠️  ВНИМАНИЕ — ПРОЧИТАЙТЕ ПЕРЕД ВХОДОМ  ⚠️                     "))
    print()
    print(YELLOW("  ┌──────────────────────────────────────────────────────────┐"))
    print(YELLOW("  │") + RED("  🚫 НЕ используйте свой ОСНОВНОЙ аккаунт Instagram!     ") + YELLOW("│"))
    print(YELLOW("  │                                                          │"))
    print(YELLOW("  │") + "  Instagram может временно ограничить аккаунт, который    " + YELLOW("│"))
    print(YELLOW("  │") + "  используется для автоматического сбора данных.           " + YELLOW("│"))
    print(YELLOW("  │                                                          │"))
    print(YELLOW("  │") + GREEN("  ✅ Создайте ОТДЕЛЬНЫЙ аккаунт для парсинга              ") + YELLOW("│"))
    print(YELLOW("  │") + GREEN("  ✅ Подождите 2-3 дня после создания перед парсингом     ") + YELLOW("│"))
    print(YELLOW("  │") + GREEN("  ✅ Подпишитесь на 10-20 аккаунтов для правдоподобности  ") + YELLOW("│"))
    print(YELLOW("  │") + GREEN("  ✅ Не запускайте парсинг чаще 2 раз в сутки             ") + YELLOW("│"))
    print(YELLOW("  │                                                          │"))
    print(YELLOW("  │") + DIM("  Мы заботимся о вашей безопасности 🔒                    ") + YELLOW("│"))
    print(YELLOW("  └──────────────────────────────────────────────────────────┘"))
    print()


def print_instructions():
    print(CYAN("  📋 Инструкция:"))
    print()
    print("  1️⃣  Откроется браузер с Instagram")
    print("  2️⃣  Войдите в " + BOLD("ЗАПАСНОЙ") + " аккаунт вручную")
    print("  3️⃣  Если появится двухфакторная аутентификация — пройдите её")
    print("  4️⃣  Дождитесь загрузки ленты (домашняя страница)")
    print("  5️⃣  " + GREEN("Нажмите Enter в этом окне") + " чтобы сохранить сессию")
    print()


async def run_auth():
    """Launch a headed browser for manual Instagram login."""
    print_banner()
    print_warning()

    # Ask for confirmation
    print(f"  Текущая папка: {DIM(str(PROJECT_ROOT))}")
    if STORAGE_STATE.exists():
        print(f"  ⚡ Найдена существующая сессия: {DIM(str(STORAGE_STATE))}")
        print(YELLOW("     Она будет перезаписана при новом входе."))
    print()

    # Пропускаем ручное подтверждение (Claude сам предупредит в чате)
    print(GREEN("  ⚡ Окно авторизации открывается, пожалуйста подождите..."))

    print()
    print_instructions()

    # Import Playwright
    try:
        from playwright.async_api import async_playwright
    except ImportError:
        print(RED("  ❌ Playwright не установлен!"))
        print("  Запустите: pip install playwright && playwright install chromium")
        return False

    print(CYAN("  🚀 Запускаю браузер..."))
    print()

    async with async_playwright() as pw:
        browser = await pw.chromium.launch(
            headless=False,
            args=[
                "--disable-blink-features=AutomationControlled",
                "--no-first-run",
                "--no-default-browser-check",
                "--window-size=420,780",
            ],
        )
        context = await browser.new_context(
            viewport={"width": 420, "height": 780},
            user_agent=(
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/121.0.0.0 Safari/537.36"
            ),
            locale="ru-RU",
            timezone_id="Europe/Moscow",
        )

        page = await context.new_page()

        # Navigate to instagram.com root (avoids 429 on /accounts/login/ direct)
        print(CYAN("  🌐 Подключаюсь к Instagram..."))
        try:
            await page.goto("https://www.instagram.com/", wait_until="commit", timeout=30000)
            # Wait for login form OR already logged-in feed
            await page.wait_for_selector(
                'input[name="username"], a[href="/"][role="link"], button:has-text("Log in"), button:has-text("Войти")',
                timeout=60000
            )
            print(GREEN("  ✅ Instagram загружен."))
        except Exception as e:
            print(YELLOW(f"  ⚠️  Медленная загрузка (но продолжаем): {e}"))
        # Dismiss cookie banner if present
        try:
            cookie_btn = await page.wait_for_selector(
                'button:has-text("Allow"), button:has-text("Разрешить"), '
                'button:has-text("Accept"), button:has-text("Принять")',
                timeout=5000,
            )
            if cookie_btn:
                await cookie_btn.click()
        except Exception:
            pass

        # --- INJECT CUSTOM CSS THEME ---
        try:
            print(CYAN("  💅 Применяю фирменный дизайн FilPars..."))
            await page.add_style_tag(content=CUSTOM_CSS)
        except Exception as e:
            pass


        print(_c("43;30", "  ⏳ Войдите в Instagram в открытом браузере...                  "))
        print()
        print(DIM("  Сессия сохранится автоматически когда вы войдёте."))
        print(DIM("  (Или нажмите Enter для ручного сохранения)"))
        print()

        # Auto-detect login: poll URL until it leaves /login/
        logged_in = False
        max_wait = 300  # 5 minutes max
        for _ in range(max_wait * 2):  # check every 0.5s
            try:
                current_url = page.url
                # Logged in = no longer on login/challenge page
                if ("instagram.com" in current_url
                    and "/login" not in current_url
                    and "/challenge" not in current_url
                    and "/accounts/" not in current_url):
                    logged_in = True
                    print()
                    print(GREEN("  🎉 Вход обнаружен! Сохраняю сессию..."))
                    # Wait a bit for cookies to settle
                    await asyncio.sleep(3)
                    break
            except Exception:
                pass

            # Check if user pressed Enter (non-blocking on Windows is tricky,
            # so we just poll URL)
            await asyncio.sleep(0.5)

        if not logged_in:
            print()
            print(YELLOW("  ⏱ Тайм-аут 5 минут. Проверяю текущий статус..."))
            current_url = page.url
            if "login" in current_url or "challenge" in current_url:
                print(YELLOW(f"  ⚠️  URL: {current_url}"))
                retry = input(BOLD("  Всё равно сохранить сессию? (да/нет): ")).strip().lower()
                if retry not in ("да", "yes", "y", "д"):
                    await browser.close()
                    print(RED("  ❌ Отменено."))
                    return False

        # Save session state
        storage = await context.storage_state()
        with open(STORAGE_STATE, "w", encoding="utf-8") as f:
            json.dump(storage, f, ensure_ascii=False, indent=2)

        await browser.close()

    # Verify saved data
    cookies_count = len(storage.get("cookies", []))
    origins_count = len(storage.get("origins", []))

    print()
    print(_c("42;97", "  ✅ Сессия сохранена!                                           "))
    print()
    print(f"  📁 Файл:    {GREEN(str(STORAGE_STATE))}")
    print(f"  🍪 Cookies: {BOLD(str(cookies_count))}")
    print(f"  🌐 Origins: {BOLD(str(origins_count))}")
    print()
    print(CYAN("  🎯 Теперь можно запускать парсинг:"))
    print(f"     {DIM('python run_scraper.py')}")
    print()
    print(_c("95", "  ──────────────────────────────────────────────────────────────"))
    print(f"  🟦 FilPars — t.me/banana_marketing")
    print(_c("95", "  ──────────────────────────────────────────────────────────────"))
    print()

    return True


if __name__ == "__main__":
    os.chdir(PROJECT_ROOT)
    try:
        result = asyncio.run(run_auth())
        sys.exit(0 if result else 1)
    except KeyboardInterrupt:
        print()
        print(RED("  ❌ Прервано пользователем."))
        sys.exit(1)
