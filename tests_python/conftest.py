import pytest
from playwright.sync_api import Page

@pytest.fixture(autouse=True)
def screenshot_on_failure(request, page: Page):
    yield
    if request.node.rep_call.failed:
        if not page.is_closed():
            page.screenshot(path=f"screenshots/{request.node.name}-error.png")