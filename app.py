from playwright.sync_api import sync_playwright


def test_login():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        try:
            page = browser.new_page()

            page.goto(
                "https://practicetestautomation.com/practice-test-login/",
                wait_until="domcontentloaded",
            )

            print(page.content())  # отладка HTML

            page.wait_for_selector("#submit", timeout=15000, state="visible")

            page.fill('input[name="username"]', "student")
            page.fill('input[name="password"]', "Password123")

            page.click("#submit")

            page.wait_for_load_state("networkidle")

            print("Current URL after login:", page.url)

            assert "logged-in-successfully" in page.url or "logged-in" in page.url

        finally:
            browser.close()


def test_negative_username():
    """Test case 2: Negative username test"""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        try:
            page = browser.new_page()

            # Открыть страницу
            page.goto(
                "https://practicetestautomation.com/practice-test-login/",
                wait_until="domcontentloaded",
            )

            print(page.content())  # отладка HTML

            # Дождаться загрузки кнопки Submit
            page.wait_for_selector("#submit", timeout=15000, state="visible")

            # Ввести некорректное имя пользователя "incorrectUser" в поле Username
            page.fill('input[name="username"]', "incorrectUser")

            # Ввести пароль "Password123" в поле Password
            page.fill('input[name="password"]', "Password123")

            # Нажать кнопку Submit
            page.click("#submit")

            # Дождаться появления сообщения об ошибке
            page.wait_for_load_state("networkidle")

            print("Current URL after failed login:", page.url)

            # Проверить, что отображается сообщение об ошибке
            error_selector = ".error, .alert, [class*='error'], #error"
            error_element = page.locator(error_selector).first

            # Проверить, что текст сообщения об ошибке "Your username is invalid!"
            error_text = error_element.text_content()
            print(f"Error message: {error_text}")

            assert "Your username is invalid!" in error_text, f"Expected error message not found. Actual: {error_text}"

        finally:
            browser.close()


def test_negative_password():
    """Test case 3: Negative password test"""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        try:
            page = browser.new_page()

            # Открыть страницу
            page.goto(
                "https://practicetestautomation.com/practice-test-login/",
                wait_until="domcontentloaded",
            )

            print(page.content())  # отладка HTML

            # Дождаться загрузки кнопки Submit
            page.wait_for_selector("#submit", timeout=15000, state="visible")

            # Ввести корректное имя пользователя "student" в поле Username
            page.fill('input[name="username"]', "student")

            # Ввести некорректный пароль "incorrectPassword" в поле Password
            page.fill('input[name="password"]', "incorrectPassword")

            # Нажать кнопку Submit
            page.click("#submit")

            # Дождаться появления сообщения об ошибке
            page.wait_for_load_state("networkidle")

            print("Current URL after failed login:", page.url)

            # Проверить, что отображается сообщение об ошибке
            error_selector = ".error, .alert, [class*='error'], #error"
            error_element = page.locator(error_selector).first

            # Проверить, что текст сообщения об ошибке "Your password is invalid!"
            error_text = error_element.text_content()
            print(f"Error message: {error_text}")

            assert "Your password is invalid!" in error_text, f"Expected error message not found. Actual: {error_text}"

        finally:
            browser.close()
