import datetime
import traceback

from dateutil import parser

from RPA.HTTP import HTTP
from RPA.Browser.Selenium import By
from RPA.Browser.Selenium import WebDriverWait
from dateutil.relativedelta import relativedelta
from selenium.common.exceptions import NoSuchElementException

from scrapper import logger
from scrapper.utils.constants import store_in_excel, search_phrase, IMAGE_BASE_PATH, contains_currency, number_of_month, \
    datetime_threshold


def __extract_element(web_element, locator, element_locator):
    try:
        return web_element.find_element(locator, element_locator)
    except NoSuchElementException:
        pass


def handle_terms_popup_callback(browser_driver, target, **kwargs):
    logger.info("Closing popup dialogs")
    try:
        browser_driver.wait_until_element_is_visible('//button[contains(text(), "Accept all")]')
        browser_driver.click_button('//button[contains(text(), "Accept all")]')
    except:
        logger.warning("[WARNING]: Popup element not found")


def load_next_page_callback(browser_driver, offset):
    if offset == None:
        return False
    logger.info("Loading next batch of news.")
    try:
        browser_driver.click_button('css:button[data-testid="search-show-more-button"]')
        wait = WebDriverWait(browser_driver, 60)
        wait.until(
            lambda driver: len(
                browser_driver.find_element("css:ol[data-testid=\"search-results\"]").find_elements(By.TAG_NAME,
                                                                                                    "li")) > offset
        )
        return True
    except Exception as e:
        return False


def extract_news_callback(parent_element, offset):
    logger.info("Extracting news element from page")
    http_client = HTTP()
    news_count = 1
    news_elements = parent_element.find_elements(By.TAG_NAME, "li")
    data_to_store = []
    for news_element in news_elements:
        if news_count < offset:
            news_count += 1
            continue
        try:
            # Check if current li element is for advertisement or not
            news_element.find_element(By.CSS_SELECTOR, "div[data-testid=\"StandardAd\"]")
            logger.info("Skip advertisement element")
            news_count += 1
            continue
        except NoSuchElementException:
            pass  # Current element does is not an advertisement 
        news_image = __extract_element(news_element, By.TAG_NAME, "img")
        news_title = news_element.find_element(By.TAG_NAME, "h4").text
        news_description = __extract_element(
            __extract_element(news_element, By.TAG_NAME, "a"), By.TAG_NAME, "p"
        )
        news_description_text = ""
        if news_description:
            news_description_text = news_description.text

        news_date = news_element.find_element(By.TAG_NAME, "div").find_element(By.TAG_NAME, "span").text
        news_datetime_obj = parser.parse(news_date).date()
        if news_datetime_obj <= datetime_threshold:
            if data_to_store:
                store_in_excel(data_to_store)
            return None
        image_file_name = ""
        has_currency_mention = contains_currency(news_title) or contains_currency(
            news_description
        )

        # save file
        if news_image:
            logger.info("Downloading news feature image")
            img_src = news_image.get_attribute("src")
            image_file_name = img_src.split("/")[-1].split("?")[0]
            image_file_path = f"{IMAGE_BASE_PATH}{image_file_name}"
            http_client.download(img_src, image_file_path)
            logger.info("News feature image download complete")

        data_to_store.append(
            {
                "Title": news_title,
                "Date": news_date,
                "Description": news_description_text,
                "Picture filename": image_file_name,
                "Search phrases count": news_title.lower().count(search_phrase),
                "Currency in title or description": has_currency_mention,
            }
        )
        news_count += 1
    if data_to_store:
        store_in_excel(data_to_store)
    return news_count
