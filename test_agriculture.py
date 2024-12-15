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

def test_agriculture(browser_setup):
    page = browser_setup.new_page()

    try:
        # Open the webpage
        page.goto("https://onlinelibrary.wiley.com/")
        page.set_viewport_size({"width": 1920, "height": 1080})

        # Wait for and locate the "Agriculture, Aquaculture & Food Science" dropdown
        page.wait_for_selector("li.accordion-tabbed__tab")
        dropdown_link = page.locator("a#accordionHeader-1")

        # Click the "Agriculture, Aquaculture & Food Science" link to open the dropdown
        dropdown_link.click()
        print("Clicked 'Agriculture, Aquaculture & Food Science' link.")

        # Wait for the specific dropdown content to become visible using its aria-labelledby
        page.wait_for_selector("div.accordion-tabbed__content[aria-labelledby='accordionHeader-1']", timeout=5000)
        print("Dropdown menu appeared.")

        # Verify that the dropdown menu has expanded
        expanded_content = page.locator("div.accordion-tabbed__content[aria-labelledby='accordionHeader-1']")
        assert expanded_content.is_visible(), "'Agriculture, Aquaculture & Food Science' dropdown content is not visible."

        # Verify the options inside the dropdown
        agriculture_option = page.locator("a[href='/topic/browse/000018']")
        assert agriculture_option.is_visible(), "'Agriculture' option is not visible."
        
        # After clicking on the "Agriculture" option, use wait_for_load_state
        agriculture_option.click()
        print("Clicked on the 'Agriculture' option.")

        # Wait for the page to load (you can specify 'load' as the state)
        page.wait_for_load_state("load", timeout=5000)
        # Wait for 1 second
        time.sleep(1)
        current_url = page.url
        assert "/topic/browse/000018" in current_url, f"Failed to navigate to the 'Agriculture' page. Current URL: {current_url}"

        print("Navigated to the 'Agriculture' page successfully.")


    except Exception as e:
        pytest.fail(f"Test failed due to an error: {e}")
