import pytest
from selene.support.shared import browser
from utils import attach

BASE_URL = "https://demowebshop.tricentis.com"


@pytest.fixture(scope="function", autouse=True)
def setup_browser(request):
    browser.config.window_width = 1920
    browser.config.window_height = 1080
    yield
    attach.add_html(browser)
    attach.add_screenshot(browser)
    attach.add_logs(browser)
    browser.quit()