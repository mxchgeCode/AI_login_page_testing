from playwright.sync_api import sync_playwright

def test_login():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        try:
            page = browser.new_page()

            page.goto("https://practicetestautomation.com/practice-test-login/", wait_until="domcontentloaded")

            print(page.content())  # отладка HTML

            page.wait_for_selector('#submit', timeout=15000, state='visible')

            # page.fill('input[name="username"]', 'student')
            page.fill('input[name="password"]', 'Password123')

            page.click('#submit')

            page.wait_for_load_state('networkidle')

            print("Current URL after login:", page.url)

            assert "logged-in-successfully" in page.url or "logged-in" in page.url

        finally:
            browser.close()



