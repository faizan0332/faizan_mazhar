from selenium.common.exceptions import StaleElementReferenceException

from scrapper import logger
from scrapper.tasks.callbacks import handle_terms_popup_callback, load_next_page_callback, extract_news_callback

from scrapper.utils.browserwrapper import BrowserClient
from scrapper.utils.constants import (
    WEB_SITE_URL,
    archive_images, search_phrase, sections, number_of_month
)
from scrapper.utils.helper import generate_action, generate_date_range


class Scrapper:

    def __init__(self):
        logger.info("Opening a browser client.")
        self.news = []
        self.browser_client = BrowserClient()
        self.browser_client.set_obscure_elements = {
            "target": "id:complianceOverlay",
            "handle": handle_terms_popup_callback,
            "target_button": "css:#complianceOverlay button",
        }

    def load_news(self):
        logger.info("Loading website")
        self.browser_client.open_site(WEB_SITE_URL)
        self.browser_client.execute_operation(
            [
		generate_action("wait", 'css:button[aria-controls="search-input"]'),
                generate_action("click", 'css:button[aria-controls="search-input"]'),
                generate_action("wait", 'css:input[name="query"]'),
                generate_action(
                    "insert_text", 'css:input[name="query"]', search_phrase),
                generate_action("click", 'css:button[data-test-id="search-submit"]'),
                generate_action("wait", 'css:div[data-testid="section"] button'),
                generate_action("click", 'css:div[data-testid="section"] button'),
            ],
            handle_obscure_elements=True
        )
        logger.info("Applying latest news filter.")
        self.browser_client.execute_operation([
            generate_action("click", 'css:select[data-testid="SearchForm-sortBy"]'),
            generate_action("wait", 'css:option[value="newest"]'),
            generate_action("click", 'css:option[value="newest"]')]
        )
        logger.info("Applying section filter for news")
        section_filter = []
        for section in sections:
            section_filter.append(
                generate_action("check_box", f'css:input[value^="{section}"]')
            )
        self.browser_client.execute_operation(section_filter)
        start_date, end_date = generate_date_range(number_of_month)
        logger.info("Applying date filter for news")
        self.browser_client.execute_operation(
            [
                generate_action("click", 'css:div[aria-label="Date Range"] button'),
                generate_action("wait", 'css:button[value="Specific Dates"]'),
                generate_action("click", 'css:button[value="Specific Dates"]'),
                generate_action("insert_text", "id:startDate", start_date),
                generate_action("insert_text", "id:endDate", end_date),
                generate_action("click", 'css:div[aria-label="Date Range"] button'),
            ]
        )

    def read_news(self):
        try:
            logger.info("Extracting news from filtered page.")
            self.browser_client.extract_content(
                'css:ol[data-testid="search-results"]', extract_news_callback, load_next_page_callback
            )
        except StaleElementReferenceException:
            logger.warning("[WARNING]: Stale Element Detect.")
            self.browser_client.extract_content(
                'css:ol[data-testid="search-results"]', extract_news_callback, load_next_page_callback
            )

    def generate_output(self):
        archive_images()
        self.browser_client.close_browser()
