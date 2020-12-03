# Name   : base.py
# Author : Harshavardhan (HK)
# Time   : 02/12/2020 10:25 pm
# Desc   : Base class holds all the methods to interact with web applications
from ui_automation_core.helpers.browser.browser_cookie import BrowserCookie
from ui_automation_core.helpers.browser.browser_navigation import BrowserINavigation
from ui_automation_core.helpers.browser.browser_window import BrowserWindow
from ui_automation_core.helpers.scroll.scroll import Scroll


class BasePage:

    def __init__(self, context):
        """
        Context holds all the values from the class which instantiate the base class
        :param context:
        """
        self.context = context
        self.browser_navigation = BrowserINavigation(self.context)

    def open_browser(self, url: str) -> None:
        """
        Launches the selected webdriver with the application URL
                :param
                -> url: application url under test
                :return:
                -> None
        """
        self.browser_navigation.launch_browser_with_url(url)

    def close_browser(self, all_windows: bool = False) -> None:
        """
        Closes the current driver instance.
        :param all_windows:
                if `True`: Quits all the browser sessions along with all the associated browser windows, tabs and pop-ups.
                `False':  Close the current browser window having focus.
        :return:
        """
        if not all_windows:
            self.browser_navigation.close_browser_active_window()
        else:
            self.browser_navigation.close_browser_all_windows()

    def get_window_title(self) -> str:
        """
            Returns the URL of the current page.
            :return url: current active window URL
        """
        return self.browser_navigation.get_url()

    def maximize_window(self):
        """
        Resize the current window to take up the entire screen.
        """
        self.browser_navigation.maximize_current_window()

    def minimize_window(self):
        """
        Minimizes the window of current browsing context.
        The exact behavior of this command is specific to individual window managers.
        Minimize Window typically hides the window in the system tray.
        """
        self.browser_navigation.minimize_current_window()

    def fullscreen_window(self):
        """
        Fills the entire screen, similar to pressing F11 in most browsers.
        """
        self.browser_navigation.fullscreen_current_window()

    def get_window_rect(self):
        """
               Gets the x, y coordinates of the window as well as height and width of
               the current window.
               :return rect
               x - Horizontal position of the operating system window associated with window, equivalent to Window.screenX.
               y- Vertical position of the operating system window associated with window, equivalent to Window.screenY.
               width - Width of outer bounds of the operating system window associated with window, equivalent to Window.
               outerWidth.
               height - Height of the outer bounds of the operating system window associated with window, equivalent to Window.
               outerHeight.

               """
        return self.browser_navigation.get_current_window_rect()

    def refresh(self):
        """
        Simulate users clicking "refresh" button on their browser
        """
        return self.browser_navigation.page_refresh()

    def navigate_back(self):
        """
               Simulate users clicking "back" button on their browser.
               """
        return self.browser_navigation.back()

    def navigate_forward(self):
        """
               Simulate users clicking "forward" button on their browser.
               """
        return self.browser_navigation.forward()

    def delete_all_cookies(self):
        """
        Delete all cookies in the scope of the session.
        """
        BrowserCookie(self.context).delete_all_cookies()

    def delete_a_cookie(self, cookie_name):
        """
        Deletes a single cookie with the given name.
        :param cookie_name: name of the cookie to be deleted
        :return: none
        Usage
        driver.delete_a_cookie(‘my_cookie’)
        """
        BrowserCookie(self.context).delete_a_cookie(cookie_name)

    def add_cookie(self, cookie_dict: dict) -> None:
        """
        Adds a cookie to your current session.
        :param cookie_dict: A dictionary object, with required keys - “name” and “value”;
                            optional keys - “path”, “domain”, “secure”, “expiry”
        :return: none

        Usage:
            driver.add_cookie({‘name’ : ‘foo’, ‘value’ : ‘bar’})
            driver.add_cookie({‘name’ : ‘foo’, ‘value’ : ‘bar’, ‘path’ : ‘/’})
            driver.add_cookie({‘name’ : ‘foo’, ‘value’ : ‘bar’, ‘path’ : ‘/’, ‘secure’:True})
        """
        BrowserCookie(self.context).add_a_cookie(cookie_dict)

    def get_cookie(self, cookie_name: str):
        """
         Get a single cookie by name. Returns the cookie if found, None if not.
         :param cookie_name:
         :return:  cookie if found, None if not
         Usage:	driver.get_cookie(‘my_cookie’)
         """
        return BrowserCookie(self.context).get_a_cookie(cookie_name)

    def get_cookies(self) -> dict:
        """
        Returns a set of dictionaries, corresponding to cookies visible in the current session.
        :return:  set of dictionaries
        Usage:	driver.get_all_cookie()
        """

        return BrowserCookie(self.context).get_all_cookies()

    def get_current_window_handle(self):
        """
                Usage:	driver.current_window_handle
                :return: handle -> handle of the current window
                """
        return BrowserWindow(self.context).get_current_window_handle()

    def scroll_to_bottom(self):
        """
                Simulates the scroll to the bottom of the page
        """
        Scroll(self.context).scroll_to_page_end()

    def scroll_to_start(self):
        """
                Simulates the scroll to the start of the page
        """
        Scroll(self.context).scroll_to_page_start()

    def scroll_element_into_view(self, locator, js=True, timeout=None):
        """
         Find element and scroll the element into view
            :param locator:  String to find the element on webpage
            :param js: True if to perform action using execute_javascript(default), for native methods set it as False
            :param timeout: The timeout to find the element.
                    If None, timeout defaults to 30 seconds.
            :return: None
                """
        Scroll(self.context).scroll_element_into_view(locator, js, timeout)
