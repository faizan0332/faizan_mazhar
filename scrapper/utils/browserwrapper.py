from datetime import timedelta
from RPA.Browser.Selenium import Selenium


class BrowserClient:
    browser_driver = None
    offset = 0
    _obscure_elements = []

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(BrowserClient, cls).__new__(cls)
        return cls.instance
    
    @property
    def obscure_elements(self):
        return self._obscure_elements

    @obscure_elements.setter
    def set_obscure_elements(self, new_element):
        self.obscure_elements.append(new_element)

    def __init__(self):
        self.browser_driver = Selenium()
    
    def open_site(self, site_url):
        self.browser_driver.open_available_browser(site_url, maximized=True)
    
    def close_browser(self):
        self.browser_driver.close_all_browsers()
    
    def extract_content(self, target_element, call_back, next_page=None):
        """
        Extracts content from current loaded page. This method only performs obscure element check.
        
        target_element: Element to find in the page. 
        call_back: Function which will only take one parameter WebElement found against target_element.
        next_page: Function which will be called to load next page
        Exception: This method will raise exception if target element is not found in the page. Calling 
        method needs to handle that exception accordingly.
        """
        while True:
            web_element = self.browser_driver.find_element(target_element)
            self.offset = call_back(web_element, self.offset)
            if next_page and not next_page(self.browser_driver, self.offset):
                break

    def execute_operation(self, operations, handle_obscure_elements=False):
        """
        operations: Defines action to be performed by the bot
        """
        if handle_obscure_elements:
            self.__check_for_obscure_element()
        for operation in operations:
            if operation.get("action") and operation.get("action").lower() != "custom":
                target = operation.get("target", None)   
                action_name = operation.get("action", None)

                # sanity check to ensure target is given. This is performed here to ensure that all 
                # execute gets executed.
                assert target is not None
                assert action_name is not None  # sanity check to ensure action is given

                # Get the function mentioned by action and pass operation as kwargs.
                getattr(self, f"_BrowserClient__{action_name.lower()}")(**operation)

    def __click(self, **kwargs):
        self.browser_driver.click_element(kwargs.get("target"))
    
    def __wait(self, **kwargs):
        self.browser_driver.wait_until_page_contains_element(kwargs.get("target"), timeout=timedelta(seconds=60))

    def __insert_text(self, **kwargs):
        self.browser_driver.input_text(kwargs.get("target"), kwargs.get("input_text"))
    
    def __check_box(self, **kwargs):
        self.browser_driver.select_checkbox(kwargs.get("target"))
    
    def __check_for_obscure_element(self):
        """
        This function has only one purpose. Check for any overlaying pop up and close it.
        likes cookies, terms and condition.
        """

        try:
            for _obscure_element in self._obscure_elements:
                target = _obscure_element.get("target")
                self.browser_driver.find_elements(target)
                _obscure_element.get("handle")(self.browser_driver, **_obscure_element)
        except Exception:
            pass
