from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options

# Util Links
# https://linuxhint.com/selenium-web-automation-python/
# https://pythonspot.com/selenium-get-source/
# https://realpython.com/modern-web-automation-with-python-and-selenium/
# https://www.techbeamers.com/selenium-webdriver-python-tutorial/

class Simulator():
    """
    Create headless browser to simulate actions on page
        
    Parameters:
        debag (bool)   : if true return window browser
    """

    def __init__(self, debag=False):
        self.opts = Options()
        
        if debag is False:
            self.opts.set_headless()

        self.browser = Firefox(options=self.opts)
        self.browser.maximize_window()

    def get_html(self, link):
        """
        Get browser rendered page
        
        Parameters:
            url (string)   : Target Link

        Returns:
            code (string)  : Page HTML code
        """

        self.browser.get(link)
        return self.browser.page_source

    def __del__(self):
        print("Browser close.")
        self.browser.close()