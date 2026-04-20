import re

with open('skills.py', 'r', encoding='utf-8') as f:
    code = f.read()

def inject_recovery(func_name, no_new_limit, old_break_code, replace_with):
    # Ensure the function initializes recovery_attempted = False
    return code.replace(old_break_code, replace_with)

# 1. scrape_feed
code = code.replace(
    '''        DOM_SEL = "article"''',
    '''        DOM_SEL = "article"\n        recovery_attempted = False'''
)
code = code.replace(
    '''            if no_new >= 8 and curr_dom_final == prev_dom:\n                break''',
    '''            if no_new >= 8 and curr_dom_final == prev_dom:\n                if not recovery_attempted:\n                    log.warning("[scrape_feed] Stalled for 60s+. Attempting recovery (dismiss, refresh)...")\n                    await dismiss_instagram_modals(page)\n                    await page.evaluate("window.scrollTo(0, 0)")\n                    await asyncio.sleep(2)\n                    await page.reload(timeout=30000)\n                    await browser.human_delay(3, 5)\n                    recovery_attempted = True\n                    no_new = 0\n                    continue\n                else:\n                    break'''
)

# 2. scrape_explore
code = code.replace(
    '''        DOM_SEL = "a[href*='/p/'], a[href*='/reel/']"''',
    '''        DOM_SEL = "a[href*='/p/'], a[href*='/reel/']"\n        recovery_attempted = False'''
)
code = code.replace(
    '''            if no_new >= 8 and curr_dom_final == prev_dom:\n                break''',
    '''            if no_new >= 8 and curr_dom_final == prev_dom:\n                if not recovery_attempted:\n                    log.warning("[scrape_explore] Stalled for 60s+. Attempting recovery (dismiss, refresh)...")\n                    await dismiss_instagram_modals(page)\n                    await page.evaluate("window.scrollTo(0, 0)")\n                    await asyncio.sleep(2)\n                    await page.reload(timeout=30000)\n                    await browser.human_delay(3, 5)\n                    recovery_attempted = True\n                    no_new = 0\n                    continue\n                else:\n                    break'''
)

# 3. scrape_search
code = code.replace(
    '''            if no_new >= 6 and curr_dom_final == prev_dom:\n                break''',
    '''            if no_new >= 6 and curr_dom_final == prev_dom:\n                if not recovery_attempted:\n                    log.warning("[scrape_search] Stalled for 60s+. Attempting recovery (dismiss, refresh)...")\n                    await dismiss_instagram_modals(page)\n                    await page.evaluate("window.scrollTo(0, 0)")\n                    await asyncio.sleep(2)\n                    await page.reload(timeout=30000)\n                    await browser.human_delay(3, 5)\n                    recovery_attempted = True\n                    no_new = 0\n                    continue\n                else:\n                    break'''
)

# 4. scrape_search_tab
code = code.replace(
    '''            if no_new >= 4 and curr_dom_final == prev_dom:\n                break''',
    '''            if no_new >= 4 and curr_dom_final == prev_dom:\n                if not recovery_attempted:\n                    log.warning("[scrape_search_tab] Stalled for 60s+. Attempting recovery (dismiss, refresh)...")\n                    await dismiss_instagram_modals(page)\n                    await page.evaluate("window.scrollTo(0, 0)")\n                    await asyncio.sleep(2)\n                    try:\n                        await page.reload(timeout=30000)\n                    except:\n                        pass\n                    await browser.human_delay(3, 5)\n                    recovery_attempted = True\n                    no_new = 0\n                    continue\n                else:\n                    break'''
)

# Adjust remaining logic safely. Let's just write.
with open('skills.py', 'w', encoding='utf-8') as f:
    f.write(code)
