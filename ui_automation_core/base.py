# Name   : base.py
# Author : Harshavardhan (HK)
# Time   : 02/12/2020 10:25 pm
# Desc   : Base class holds all the methods to interact with web applications
from ui_automation_core.helpers.actions.action import Actions
from ui_automation_core.helpers.actions.mouse_action import ClickMethod, MouseAction
from ui_automation_core.helpers.browser.browser_cookie import BrowserCookie
from ui_automation_core.helpers.browser.browser_navigation import BrowserINavigation
from ui_automation_core.helpers.browser.browser_window import BrowserWindow
from ui_automation_core.helpers.scroll.scroll import Scroll
from ui_automation_core.helpers.select.select import SelectAction
from ui_automation_core.helpers.select.select_method import SelectMethod
from ui_automation_core.helpers.web_element.locator import Locator, ElementWaitState


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

    def get_element(self, pattern, wait_state=ElementWaitState.PRESENT,
                    throw_exception=True, timeout=None):
        """
                Returns the web element based the specified locator pattern or 'None' if the element is not found.

                :param pattern: The string pattern used to find the element on a web page.
                :param wait_state: Choose state from ElementWaitState class. Defaults to ElementWaitState.PRESENT.
                 Allowed states are
                    ElementWaitState.PRESENT,
                    ElementWaitState.VISIBLE,
                    ElementWaitState.INVISIBLE,
                    ElementWaitState.CLICKABLE,
                    ElementWaitState.SELECTED,
                    ElementWaitState.FRAME_AVAILABLE_AND_SWITCH_TO
                :param throw_exception: The boolean to throw exception or not.
                        Defaulted to true.
                :param timeout: wait time before throwing expectation.
                :return:  Web element
        """
        return Locator(self.context).get_element(pattern, wait_state,
                                                 throw_exception, timeout)

    def get_elements(self, pattern, wait_state=ElementWaitState.PRESENT_OF_ALL,
                     throw_exception=True, timeout=None):
        """
                Returns the web elements based the specified locator pattern or 'None' no elements are found.

                :param pattern: The string pattern used to find the element on a web page.
                :param wait_state: Choose state from ElementWaitState class.
                Defaults to ElementWaitState.PRESENT.

                 Allowed states are
                 ElementWaitState.PRESENT_OF_ALL,
                 ElementWaitState.VISIBLE_OF_ALL,
                 ElementWaitState.VISIBLE_OF_ANY

                :param throw_exception: The boolean to throw exception or not.
                        Defaulted to true.
                :param timeout: wait time before throwing expectation.
                :return:  Web elements
        """
        return Locator(self.context).get_elements(pattern, wait_state,
                                                  throw_exception, timeout)

    def get_text(self, locator, wait_state=ElementWaitState.PRESENT, timeout=None):
        """
        Get the visible (i.e. not hidden by CSS) inner text of the web element without any leading
                or trailing whitespace.

        :param locator: The string pattern to find the element or the web element itself.
        :param wait_state: The wait state for retrial. Choose state from ElementWaitState class.
        :param timeout: wait time before throwing any exception.
                    If None, timeout defaults to 20 seconds.
        :return: inner html
        """
        return Actions(self.context).get_web_element_inner_text(locator, wait_state, timeout)

    def set_text(self, locator, text, clear_text=True, wait_state=ElementWaitState.PRESENT, timeout=None):
        """
        Set the value of an input field, as though you type it in.
        It also clears the previous value of the input field if clear_text is set to true.

        :param locator: locator pattern to identify element on the web page
        :param text: Text to enter in input field
        :param clear_text: boolean value to clear the previous value of the input field
                   Defaults to True
        :param wait_state: he wait state for element retrial. Choose state from ElementWaitState class.
                   Defaults to ElementWaitState.PRESENT.
        :param timeout: wait time before throwing any exception.
                           If None, timeout defaults to 20 seconds.
        :return: self
               """
        return Actions(self.context).set_text(locator, text, clear_text, wait_state, timeout)

    def submit(self, locator, wait_state=ElementWaitState.PRESENT, timeout=None):
        """
        Submits a form.
        If the current element is a form or an element within a form, then this will be submitted.

               :param locator:  Web element or a locator string on which the action need to be performed.
               :param wait_state: he wait state for retrial. Choose state from ElementWaitState class.
               :param timeout: wait time before throwing any exception. If None, timeout defaults to 20 seconds.
               :return: self
               """
        return Actions(self.context).submit_form(locator, wait_state, timeout)

    def clear(self, locator, wait_state=ElementWaitState.PRESENT, timeout=None):
        """
        Clears the text if it’s a text entry element.

        :param locator:  Web element or a locator string on which the action need to be performed.
        :param wait_state: he wait state for retrial. Choose state from ElementWaitState class.
        :param timeout: wait time before throwing any exception. If None, timeout defaults to 20 seconds.
        :return: self
        """
        return Actions(self.context).clear_text(locator, wait_state, timeout)

    def get_attribute(self, locator, attribute, wait_state=ElementWaitState.PRESENT, timeout=None, ):
        """
                Gets the given attribute or property of the element.

                :param locator:  Web element or a locator string on which the action need to be performed.
                :param attribute: attribute/ property
                :param wait_state: he wait state for retrial. Choose state from ElementWaitState class.
                :param timeout: wait time before throwing any exception. If None, timeout defaults to 20 seconds.
                :return: This method will first try to return the value of a property with the given name.
                 If a property with that name doesn't exist, it returns the value of the attribute with the same name.
                 If there’s no attribute with that name, None is returned.
                """
        return Actions(self.context).get_attribute(locator, attribute, wait_state, timeout)

    def get_property(self, locator, name, wait_state=ElementWaitState.PRESENT, timeout=None, ):
        """
                Gets the given property of the element.

                :param locator:  Web element or a locator string on which the action need to be performed.
                :param name: Name of the property
                :param wait_state: he wait state for retrial. Choose state from ElementWaitState class.
                :param timeout: wait time before throwing any exception. If None, timeout defaults to 20 seconds.
                :return: the given property of the element.
                """
        return Actions(self.context).get_property(locator, name, wait_state, timeout)

    def click(self, locator=None, click_method=ClickMethod.API_CLICK,
              wait_state=ElementWaitState.PRESENT, timeout=None):
        """
        Simulates user clicking on an element with different click methods available.

            :param locator: Web element or a locator string on which the click action need to be performed
            :param click_method: Method to perform click and  by default  click_method=ClickMethod.API_CLICK
            Available methods are:
                API_CLICK
                JAVA_SCRIPT_CLICK
                ACTION_CHAIN_CLICK
            :param wait_state: he wait state for retrial. Choose state from ElementWaitState class.
            :param timeout: wait time before throwing any exception.
                            If None, timeout defaults to 20 seconds.
            :return: self
        """
        return MouseAction(self.context).click_web_element(locator, click_method, wait_state, timeout)

    def double_click(self, locator=None, wait_state=ElementWaitState.PRESENT, timeout=None):
        """
                Double-clicks an element.

                :param locator: Web element or a locator string on which the click action need to be performed
                :param wait_state: he wait state for retrial. Choose state from ElementWaitState class.
                :param timeout: wait time before throwing any exception.
                            If None, timeout defaults to 20 seconds.
                :return: self
                """
        return MouseAction(self.context).double_click(locator, wait_state, timeout)

    def right_click(self, locator=None, wait_state=ElementWaitState.PRESENT, timeout=None):
        """
                Right-clicks an element.

                :param locator: Web element or a locator string on which the click action need to be performed
                :param wait_state: he wait state for retrial. Choose state from ElementWaitState class.
                :param timeout: wait time before throwing any exception.
                            If None, timeout defaults to 20 seconds.
                :return: self
                """
        return MouseAction(self.context).context_click(locator, wait_state, timeout)

    def mouse_over(self, locator=None, wait_state=ElementWaitState.PRESENT, timeout=None):
        """
        Simulate users hovering a mouse over the given element.

        :param locator: Web element or a locator string on which the click action need to be performed
        :param wait_state: he wait state for retrial. Choose state from ElementWaitState class.
        :param timeout: wait time before throwing any exception.
                    If None, timeout defaults to 20 seconds.
        :return: self
        """
        return MouseAction(self.context).move_cursor_to_element(locator, wait_state, timeout)

    def mouse_move_offset(self, x_offset, y_offset):
        """
        Moving the mouse to an offset from current mouse position.

        :param x_offset: X offset to move to, as a positive or negative integer.
        :param y_offset: Y offset to move to, as a positive or negative integer.
        :return: self
        """
        return MouseAction(self.context).move_cursor_by_offset(x_offset, y_offset)

    def mouse_over_offset(self, locator, x_offset, y_offset, wait_state=ElementWaitState.PRESENT, timeout=None):
        """
               Simulate users hovering a mouse over the given element with the relative position (x, y)
               from the top-left corner of that element.

               :param locator: locator: Web element or a locator string on which the click action need to be performed
               :param x_offset: X offset to move to, as a positive or negative integer.
               :param y_offset: Y offset to move to, as a positive or negative integer.
               :param wait_state: he wait state for retrial. Choose state from ElementWaitState class.
               :param timeout: wait time before throwing any exception.
                           If None, timeout defaults to 20 seconds.
               :return: self
               """
        return MouseAction(self.context).move_cursor_to_element_by_offset(locator, x_offset, y_offset, wait_state,
                                                                          timeout)

    def drag_and_drop(self, source, target, wait_state=ElementWaitState.PRESENT, timeout=None):
        """
                Drag an object and drop it onto another object. Holds down the left mouse button on the source element,
                then moves to the target element and releases the mouse button.

                :param source: The element to mouse down. (element to be moved). Can be a locator string or an web element
                :param target: The element to mouse up. (destination location). Can be locator string or an web element
                :param wait_state: he wait state for retrial. Choose state from ElementWaitState class.
                :param timeout: wait time before throwing any exception.
                            If None, timeout defaults to 20 seconds.
                :return: self
                """
        return MouseAction(self.context).drag_and_drop_to_object(source, target, wait_state, timeout)

    def drag_and_drop_by_offset(self, src_locator, x_offset, y_offset,
                                wait_state=ElementWaitState.PRESENT, timeout=None):
        """
               Drag an object and drop it to an offset location. Holds down the left mouse button on the source element,
               then moves to the target offset and releases the mouse button.

               :param src_locator: The element to mouse down. (element to be moved). Can be a locator string or an web element
               :param x_offset: X offset to move to
               :param y_offset: Y offset to move to.
               :param wait_state: he wait state for retrial. Choose state from ElementWaitState class.
               :param timeout: wait time before throwing any exception.
                           If None, timeout defaults to 20 seconds.
               :return: self
               """
        return MouseAction(self.context).drag_and_drop_by_offset(src_locator, x_offset, y_offset, wait_state, timeout)

    def select_checkbox(self, locator, is_select, wait_state=ElementWaitState.PRESENT,
                        timeout=None):
        """
               Select or unselect the checkbox.

               :param locator: Web element or a locator string on which the click action need to be performed.
               :param is_select: The boolean to perform select/unselect
               :param wait_state: he wait state for retrial. Choose state from ElementWaitState class.
               :param timeout: wait time before throwing any exception.
                           If None, timeout defaults to 20 seconds.
               :return: self

               """
        return SelectAction(self.context).select_checkbox(locator, is_select, wait_state, timeout)

    def select_option(self, locator, select_by, is_select, values=None,
                      wait_state=ElementWaitState.PRESENT, timeout=None):
        """
                Select an option or list of options at the given index, value or visible text.

                :param locator: Web element or a locator string on which the action need to be performed.
                :param select_by: Method to select a dropdown value. Should be a instance of SelectMethod enum class.
                :param is_select: is a boolean value True: To select , False: to deselect
                in case of multiselect dropdown.
                :param values: A list of single or multiple indices, values or visible texts.
                :param wait_state: he wait state for retrial. Choose state from ElementWaitState class.
                :param timeout: wait time before throwing any exception. If None, timeout defaults to 20 seconds.
                :return: self

                USAGE:  select_dropdown('#dropdown', SelectMethod.VALUE, True, ['Option One'])\n
                        select_dropdown('#dropdown', SelectMethod.VALUE, True, ['Option One', 'Option Two'])\n
                        select_dropdown('#dropdown', SelectMethod.INDEX, True, [1, 2])
                """
        return SelectAction(self.context).select_dropdown(locator, select_by, is_select, values,
                                                          wait_state, timeout)

    def select_option_by_index(self, locator, is_select, values=None, select_by=SelectMethod.INDEX,
                               wait_state=ElementWaitState.PRESENT, timeout=None):
        """
                Select an option or list of options at the given index.

                :param locator:Web element or a locator string on which the action need to be performed.
                :param select_by: Method is by default set to SelectMethod.INDEX.
                :param is_select: is a boolean value True: To select , False: to deselect
                in case of multiselect dropdown.
                :param values: A list of single or multiple indices, values or visible texts.
                :param wait_state: he wait state for retrial. Choose state from ElementWaitState class.
                :param timeout: wait time before throwing any exception. If None, timeout defaults to 20 seconds.
                :return: self

                USAGE: select_dropdown('#dropdown', True, [1, 2])
                """
        return SelectAction(self.context).select_dropdown(locator, select_by, is_select, values,
                                                          wait_state, timeout)

    def select_option_by_value(self, locator, is_select, values=None, select_by=SelectMethod.VALUE,
                               wait_state=ElementWaitState.PRESENT, timeout=None):
        """
                Select an option or list of options at the given value.

                :param locator: Web element or a locator string on which the action need to be performed.
                :param select_by: Method is by default set to SelectMethod.VALUE.
                :param is_select: is a boolean value True: To select , False: to deselect
                in case of multiselect dropdown.
                :param values: A list of single or multiple indices, values or visible texts.
                :param wait_state: he wait state for retrial. Choose state from ElementWaitState class.
                :param timeout: wait time before throwing any exception. If None, timeout defaults to 20 seconds.
                :return: self

                USAGE: select_dropdown('#dropdown', True, [1, 2])
                """
        return SelectAction(self.context).select_dropdown(locator, select_by, is_select, values,
                                                          wait_state, timeout)

    def select_option_by_visible_text(self, locator, is_select, values=None, select_by=SelectMethod.VISIBLE_TEXT,
                                      wait_state=ElementWaitState.PRESENT, timeout=None):
        """
                Select an option or list of options at the given index.

                :param locator: Web element or a locator string on which the action need to be performed.
                :param select_by: Method is by default set to SelectMethod.VISIBLE_TEXT.
                :param is_select: is a boolean value True: To select , False: to deselect.
                in case of multiselect dropdown.
                :param values: A list of single or multiple indices, values or visible texts.
                :param wait_state: he wait state for retrial. Choose state from ElementWaitState class.
                :param timeout: wait time before throwing any exception. If None, timeout defaults to 20 seconds.
                :return: self

                USAGE: select_dropdown('#dropdown', True, [1, 2])
                """
        return SelectAction(self.context).select_dropdown(locator, select_by, is_select, values,
                                                          wait_state, timeout)

    def get_all_dropdown_options(self, locator, wait_state=ElementWaitState.PRESENT, timeout=None):
        """
                Get a list of all options belonging to this select tag.

                :param locator:  Web element or a locator string on which the action need to be performed.
                :param wait_state: he wait state for retrial. Choose state from ElementWaitState class.
                :param timeout: wait time before throwing any exception. If None, timeout defaults to 20 seconds.
                :return: Returns a list of all options belonging to this select tag
                """
        return SelectAction(self.context).get_all_dropdown_options(locator, wait_state, timeout)

    def get_dropdown_first_option_selected(self, locator, wait_state=ElementWaitState.PRESENT, timeout=None):
        """
                Get the first dropdown option selected

                :param locator:  Web element or a locator string on which the action need to be performed.
                :param wait_state: he wait state for retrial. Choose state from ElementWaitState class.
                :param timeout: wait time before throwing any exception. If None, timeout defaults to 20 seconds.
                :return: Returns the first selected option in this select tag
                 (or the currently selected option in a normal select)
                    """
        return SelectAction(self.context).get_dropdown_first_option(locator, wait_state, timeout)

    def deselect_all_options(self, locator, wait_state=ElementWaitState.PRESENT, timeout=None):
        """
                Deselect all options from multiselect.

                :param locator:  Web element or a locator string on which the action need to be performed.
                :param wait_state: he wait state for retrial. Choose state from ElementWaitState class.
                :param timeout: wait time before throwing any exception. If None, timeout defaults to 20 seconds.
                :return: self
                """
        return SelectAction(self.context).deselect_all_options_dropdown(locator, wait_state, timeout)
