"""
HTML fetching utilities backed by Playwright.
If need, can be moved to microservice or even use some external API (e.g. Firecrawl)

HeadlessBrowser - A headless browser utility using Playwright.
HyperlinkParser - An HTML parser to extract hyperlinks from HTML content.

"""

from playwright.async_api import async_playwright, TimeoutError as AsyncPlaywrightTimeoutError
from asgiref.sync import async_to_sync
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from html.parser import HTMLParser
import re

class HeadlessBrowser:
    """Headless browser utilityby Playwright.
    Provides a synchronous ``fetch_html`` method to get page content and metadata.
    Parses hyperlinks within the same domain.
    started and reused across calls until ``close`` is invoked.
    """

    def __init__(self, headless: bool = True, timeout_ms: int = 15000):
        self._playwright = None
        self._browser = None
        self.headless = headless
        self.timeout_ms = timeout_ms

    async def _start(self):
        if not self._playwright:
            self._playwright = await async_playwright().start()
            self._browser = await self._playwright.chromium.launch(headless=self.headless)

    async def _fetch_html_async(self, url: str) -> tuple[str, str, str, str, int]:
        await self._start()
        page = await self._browser.new_page()
        try:


            response = await page.goto(url, wait_until="domcontentloaded", timeout=self.timeout_ms)
            try:
                await page.wait_for_load_state("networkidle", timeout=self.timeout_ms)
            except AsyncPlaywrightTimeoutError:
                pass
            html_content = await page.content()
            soup = BeautifulSoup(html_content, "html.parser")
            for tag in soup(["script", "style"]):
                tag.decompose()
            plain_text = soup.get_text(separator=" ", strip=True)
            title = soup.title.string.strip() if soup.title and soup.title.string else await page.title()
            status_code = response.status



            # Get the hyperlinks from the URL and add them to the queue
            child_links = self.get_domain_hyperlinks(url, html_content)


            return html_content, plain_text, title, child_links, status_code
        finally:
            await page.close()

    def fetch_html(self, url: str) -> tuple[str, str, str, str, int]:
        """Synchronously fetch HTML and derived metadata for the given URL."""
        return async_to_sync(self._fetch_html_async)(url)


    # Function to get the hyperlinks from a URL that are within the same domain
    def get_domain_hyperlinks(self, url: str, html_content: str) -> list[str]:

        # Parse the URL and get the domain
        local_domain = urlparse(url).netloc

        # Create the HTML Parser and then Parse the HTML to get hyperlinks
        parser = HyperlinkParser()
        parser.feed(html_content)
        links = parser.hyperlinks

        # Regex pattern to match a URL
        HTTP_URL_PATTERN = r'^http[s]*://.+'
        clean_links = []
        for link in set(links):
            clean_link = None

            # If the link is a URL, check if it is within the same domain
            if re.search(HTTP_URL_PATTERN, link):
                # Parse the URL and check if the domain is the same
                url_obj = urlparse(link)
                if url_obj.netloc == local_domain:
                    clean_link = link

            # If the link is not a URL, check if it is a relative link
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

        # Return the list of hyperlinks that are within the same domain
        return list(set(clean_links))


    async def _close_async(self):
        if self._browser:
            try:
                await self._browser.close()
            finally:
                self._browser = None
        if self._playwright:
            try:
                await self._playwright.stop()
            finally:
                self._playwright = None

    def close(self):
        async_to_sync(self._close_async)()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()


# HTML Parser class to extract hyperlinks
class HyperlinkParser(HTMLParser):
    def __init__(self):
        super().__init__()
        # Create a list to store the hyperlinks
        self.hyperlinks = []

    # Override the HTMLParser's handle_starttag method to get the hyperlinks
    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)

        # If the tag is an anchor tag and it has an href attribute, add the href attribute to the list of hyperlinks
        if tag == "a" and "href" in attrs:
            self.hyperlinks.append(attrs["href"])

    def error(self, message):
        pass



