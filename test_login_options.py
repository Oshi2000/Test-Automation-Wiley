import pytest
from playwright.sync_api import sync_playwright
import time

@pytest.fixture(scope="function")
def browser_setup():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)  # Use visible browser
        context = browser.new_context(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36")
        yield context
        browser.close()

def test_login_options(browser_setup):
    page = browser_setup.new_page()

    try:
        # Open the webpage
        page.goto("https://onlinelibrary.wiley.com/")
        page.set_viewport_size({"width": 1920, "height": 1080})

        # Wait for and locate the "Login / Register" link
        page.wait_for_selector("span.sign-in-label")
        login_register_link = page.locator("span.sign-in-label")
        
        # Click the "Login / Register" link
        login_register_link.click()
        print("Clicked 'Login / Register' link.")

        # Wait for the dropdown with the login options to appear
        page.wait_for_selector("div.navigation-login-dropdown-container", timeout=5000)
        print("Login dropdown menu appeared.")

        # Wait for 1 second
        time.sleep(1)

        # Verify the 'Individual login' option is visible
        individual_login_locator = page.locator("li:has(a[href='/action/showLogin?acdl-redirect=true&uri=%2F']) a")
        assert individual_login_locator.is_visible(), "'Individual login' option is not visible."

        # Verify the 'Institutional login' option is visible
        institutional_login_locator = page.locator("li:has(a[href='/action/ssostart?redirectUri=%2F']) a")
        assert institutional_login_locator.is_visible(), "'Institutional login' option is not visible."

        # Verify the 'Register' option is visible
        register_locator = page.locator("li:has(a[href='/action/registration?redirectUri=%2F&acdl-redirect=true']) a")
        assert register_locator.is_visible(), "'Register' option is not visible."

        print("All three options are visible.")

    except Exception as e:
        pytest.fail(f"Test failed due to an error: {e}")
