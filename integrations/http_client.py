"""
HTML fetching utilities backed by Playwright.
If need, can be moved to microservice or even use some external API (e.g. Firecrawl)

HeadlessBrowser - A headless browser utility using Playwright.
HyperlinkParser - An HTML parser to extract hyperlinks from HTML content.

"""

from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from html.parser import HTMLParser
import re
from concurrent.futures import ThreadPoolExecutor

class HeadlessBrowser:
    """Headless browser utility using Playwright.
    Provides a synchronous ``fetch_html`` method to get page content and metadata.
    Uses a dedicated thread for browser operations, to have predictible ram/cpu usage
    and allow scalling on celery workers pool.
    Parses hyperlinks within the same domain.
    Browser runs in a dedicated thread to avoid async context issues.
    """

    def __init__(self, headless: bool = True, timeout_ms: int = 15000):
        self.headless = headless
        self.timeout_ms = timeout_ms
        self._executor = ThreadPoolExecutor(max_workers=1)
        self._playwright = None
        self._browser = None

    def _init_browser(self):
        """Initialize browser in thread. Called once."""
        if not self._playwright:
            playwright_ctx = sync_playwright()
            self._playwright = playwright_ctx.__enter__()
            self._browser = self._playwright.chromium.launch(headless=self.headless)

    def _fetch_in_thread(self, url: str) -> tuple[str, str, str, list[str], int]:
        """Fetch HTML in dedicated thread."""
        self._init_browser()

        page = self._browser.new_page()
        try:
            response = page.goto(url, wait_until="domcontentloaded", timeout=self.timeout_ms)
            try:
                page.wait_for_load_state("networkidle", timeout=self.timeout_ms)
            except PlaywrightTimeoutError:
                pass

            html_content = page.content()
            soup = BeautifulSoup(html_content, "html.parser")
            for tag in soup(["script", "style"]):
                tag.decompose()
            plain_text = soup.get_text(separator=" ", strip=True)
            title = soup.title.string.strip() if soup.title and soup.title.string else page.title()
            status_code = response.status
            child_links = self.get_domain_hyperlinks(url, html_content)

            return html_content, plain_text, title, child_links, status_code
        finally:
            page.close()

    def fetch_html(self, url: str) -> tuple[str, str, str, list[str], int]:
        """Synchronously fetch HTML and derived metadata for the given URL."""
        return self._executor.submit(self._fetch_in_thread, url).result()

    def get_domain_hyperlinks(self, url: str, html_content: str) -> list[str]:
        """Extract hyperlinks from HTML that are within the same domain."""
        local_domain = urlparse(url).netloc
        parser = HyperlinkParser()
        parser.feed(html_content)

        HTTP_URL_PATTERN = r'^http[s]*://.+'
        clean_links = []

        for link in set(parser.hyperlinks):
            clean_link = None

            if re.search(HTTP_URL_PATTERN, link):
                url_obj = urlparse(link)
                if url_obj.netloc == local_domain:
                    clean_link = link
            else:
                if link.startswith("/"):
                    link = link[1:]
                elif link.startswith("#") or link.startswith("mailto:"):
                    continue
                clean_link = "https://" + local_domain + "/" + link

            if clean_link is not None:
                if clean_link.endswith("/"):
                    clean_link = clean_link[:-1]
                clean_links.append(clean_link)

        return list(set(clean_links))

    def close(self):
        """Close browser and cleanup resources."""
        if self._executor:
            self._executor.shutdown(wait=True)
            self._executor = None

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()


class HyperlinkParser(HTMLParser):
    """HTML parser to extract hyperlinks."""

    def __init__(self):
        super().__init__()
        self.hyperlinks = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "a" and "href" in attrs:
            self.hyperlinks.append(attrs["href"])

    def error(self, message):
        pass



