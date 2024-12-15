import pytest
from playwright.sync_api import sync_playwright
import random
import time
import re

@pytest.fixture(scope="function")
def browser_setup():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)  # Use visible browser
        context = browser.new_context(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36")
        yield context
        browser.close()

def test_search(browser_setup):
    search_term = "Quality Engineering"
    page = browser_setup.new_page()

    try:
        # Open the webpage
        page.goto("https://onlinelibrary.wiley.com/action/doSearch?AllField=Quality+Engineering")
        page.set_viewport_size({"width": 1920, "height": 1080})

        # Wait for search results to load
        page.wait_for_selector(".search-result", timeout=15000)
        results = page.locator("li.search__item")  # Locating each search item

        result_count = results.count()
        assert result_count > 0, f"No results found for '{search_term}'."
        print(f"Search successful. Found {result_count} results for '{search_term}'.")

        # Extract all the publication titles (inside <a> tags with class 'publication_title visitable')
        titles = results.locator('a.publication_title.visitable').all_text_contents()

        # Verify that each title contains 'Quality' and 'Engineering' (case-insensitive)
        for title in titles:
            assert re.search(r'quality', title, re.IGNORECASE), f"Title '{title}' does not contain 'Quality'"
            assert re.search(r'engineering', title, re.IGNORECASE), f"Title '{title}' does not contain 'Engineering'"

        print("All titles contain 'Quality' and 'Engineering'.")

    except Exception as e:
        pytest.fail(f"Test failed due to an error: {e}")
