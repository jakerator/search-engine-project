"""HTML fetching utilities backed by Playwright.


"""

from playwright.async_api import async_playwright, TimeoutError as AsyncPlaywrightTimeoutError
from asgiref.sync import async_to_sync
from bs4 import BeautifulSoup


class HeadlessBrowser:
    """Headless browser utilities backed by Playwright.

    Provides a synchronous ``fetch_html`` method which internally executes an
    async workflow via ``async_to_sync``. The browser instance is lazily
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

    async def _fetch_html_async(self, url: str) -> tuple[str, str, str, int]:
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
            status_code = response.status if response else 200
            return html_content, plain_text, title, status_code
        finally:
            await page.close()

    def fetch_html(self, url: str) -> tuple[str, str, str, int]:
        """Synchronously fetch HTML and derived metadata for the given URL."""
        return async_to_sync(self._fetch_html_async)(url)

    async def _close_async(self):
        if self._browser:
            await self._browser.close()
            self._browser = None
        if self._playwright:
            await self._playwright.stop()
            self._playwright = None

    def close(self):
        async_to_sync(self._close_async)()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

