"""
HTTP Client for fetching HTML content from URLs using headless browser.
"""

from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup


class HeadlessBrowser:
    """Headless browser-based HTTP client for fetching web content."""

    def __init__(self):
        self.playwright = sync_playwright().start()
        self.browser = self.playwright.chromium.launch(headless=True)

    def fetch_html(self, url: str) -> tuple[str, str, str, int]:
        """
        Fetch HTML content from a URL.

        Args:
            url: The URL to fetch

        Returns:
            tuple[str, str, str, int]: A tuple of (html_content, plain_text, title, status_code)
        """
        page = self.browser.new_page()
        try:
            response = page.goto(url)
            html_content = page.content()

            # Extract plain text from HTML
            soup = BeautifulSoup(html_content, 'html.parser')
            # Remove script and style elements
            for script in soup(['script', 'style']):
                script.decompose()
            plain_text = soup.get_text(separator=' ', strip=True)

            # Extract title
            title = soup.title.string if soup.title else page.title()

            status_code = response.status if response else 200
            return html_content, plain_text, title, status_code
        finally:
            page.close()

    def close(self):
        """Close the browser session."""
        if self.browser:
            self.browser.close()
            self.browser = None
        if self.playwright:
            self.playwright.stop()
            self.playwright = None

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
