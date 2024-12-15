import pytest
from playwright.sync_api import sync_playwright
import random
import time
import re

# Fixture for browser setup, providing a new browser context for each test
@pytest.fixture(scope="function")
def browser_setup():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)  # Launch a visible browser for debugging
        context = browser.new_context(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36")
        yield context
        browser.close()



# Test 01: Verify the "Login / Register" dropdown functionality
def test_login_options(browser_setup):
    page = browser_setup.new_page()

    try:
        # Step 1: Open the Wiley Online Library homepage
        page.goto("https://onlinelibrary.wiley.com/")
        page.set_viewport_size({"width": 1920, "height": 1080})

        # Step 2: Locate and click the "Login / Register" link
        page.wait_for_selector("span.sign-in-label")
        login_register_link = page.locator("span.sign-in-label")
        login_register_link.click()
        print("Clicked 'Login / Register' link.")

        # Step 3: Verify that the login dropdown menu appears
        page.wait_for_selector("div.navigation-login-dropdown-container", timeout=5000)
        print("Login dropdown menu appeared.")

        # Step 4: Verify the presence of individual login, institutional login, and register options
        individual_login_locator = page.locator("li:has(a[href='/action/showLogin?acdl-redirect=true&uri=%2F']) a")
        assert individual_login_locator.is_visible(), "'Individual login' option is not visible."

        institutional_login_locator = page.locator("li:has(a[href='/action/ssostart?redirectUri=%2F']) a")
        assert institutional_login_locator.is_visible(), "'Institutional login' option is not visible."

        register_locator = page.locator("li:has(a[href='/action/registration?redirectUri=%2F&acdl-redirect=true']) a")
        assert register_locator.is_visible(), "'Register' option is not visible."

        print("All three options are visible.")

        # Added for clarity before going to the next test case
        time.sleep(1)

    except Exception as e:
        pytest.fail(f"Test failed due to an error: {e}")



# Test 02: Verify search functionality for a specific term
def test_search(browser_setup):
    search_term = "Quality Engineering"
    page = browser_setup.new_page()

    try:
        # Step 1: Open the search results page for the given term
        page.goto("https://onlinelibrary.wiley.com/action/doSearch?AllField=Quality+Engineering")
        page.set_viewport_size({"width": 1920, "height": 1080})

        # Step 2: Wait for the search results to load
        page.wait_for_selector(".search-result", timeout=15000)
        results = page.locator("li.search__item")  # Locate individual search items

        # Step 3: Validate that search results are found
        result_count = results.count()
        assert result_count > 0, f"No results found for '{search_term}'."
        print(f"Search successful. Found {result_count} results for '{search_term}'.")

        # Step 4: Validate that each result contains the search terms
        titles = results.locator('a.publication_title.visitable').all_text_contents()
        for title in titles:
            assert re.search(r'quality', title, re.IGNORECASE), f"Title '{title}' does not contain 'Quality'"
            assert re.search(r'engineering', title, re.IGNORECASE), f"Title '{title}' does not contain 'Engineering'"

        print("All titles contain 'Quality' and 'Engineering'.")

        # Added for clarity before going to the next test case
        time.sleep(1)

    except Exception as e:
        pytest.fail(f"Test failed due to an error: {e}")



# Test 03: Verify the "Agriculture, Aquaculture & Food Science" dropdown functionality
def test_agriculture(browser_setup):
    page = browser_setup.new_page()

    try:
        # Step 1: Open the Wiley Online Library homepage
        page.goto("https://onlinelibrary.wiley.com/")
        page.set_viewport_size({"width": 1920, "height": 1080})

        # Step 2: Locate and click the "Agriculture, Aquaculture & Food Science" dropdown link
        page.wait_for_selector("li.accordion-tabbed__tab")
        dropdown_link = page.locator("a#accordionHeader-1")
        dropdown_link.click()
        print("Clicked 'Agriculture, Aquaculture & Food Science' link.")

        # Step 3: Verify that the dropdown menu appears
        page.wait_for_selector("div.accordion-tabbed__content[aria-labelledby='accordionHeader-1']", timeout=5000)
        expanded_content = page.locator("div.accordion-tabbed__content[aria-labelledby='accordionHeader-1']")
        assert expanded_content.is_visible(), "'Agriculture, Aquaculture & Food Science' dropdown content is not visible."

        # Step 4: Verify and click on the "Agriculture" option
        agriculture_option = page.locator("a[href='/topic/browse/000018']")
        assert agriculture_option.is_visible(), "'Agriculture' option is not visible."
        agriculture_option.click()
        print("Clicked on the 'Agriculture' option.")

        # Step 5: Validate navigation to the "Agriculture" page
        page.wait_for_load_state("load", timeout=5000)
        current_url = page.url
        assert "/topic/browse/000018" in current_url, f"Failed to navigate to the 'Agriculture' page. Current URL: {current_url}"

        print("Navigated to the 'Agriculture' page successfully.")

        # Added for clarity before ending
        time.sleep(1)

    except Exception as e:
        pytest.fail(f"Test failed due to an error: {e}")
