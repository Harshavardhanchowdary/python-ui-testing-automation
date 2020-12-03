# Name   : Scroll.py
# Author : Harshavardhan (HK)
# Time    : 03/12/2020 12:45 pm
# Desc: Scroll class holds all the methods to scroll the web page.

import time

from selenium.webdriver.common.by import By


class Scroll:
    def __init__(self, context):
        self.context = context

    def execute_javascript(self, script, *args):
        """
        Synchronously executes JavaScript in the current window or frame.

        :Args:
         - script: The JavaScript to execute.
         - *args: Any applicable arguments for your JavaScript.
        """
        try:
            value = self.context.driver.execute_script(script, *args)

            self.context.logger.info(f'Successfully executed javascript {script} on the '
                                     f'argument(s) {args if len(args) > 0 else "No args"}')
            if value is not None:
                self.context.logger.info(f'Result : {value}')
            return value
        except Exception as ex:
            self.context.logger.error(f'Unable to execute javascript {script} on the '
                                      f'argument(s) {args if len(args) > 0 else "No args"}.')
            self.context.logger.exception(ex)
            raise Exception('Unable to execute javascript {script} on the '
                            f'argument(s) {args if len(args) > 0 else "No args"}. Error: {ex}')

    def scroll_to_page_end(self):
        """
        Simulates the scroll to the bottom of the page
        """
        wait_time = 1
        initial_height = self.execute_javascript("return document.body.scrollHeight")
        while True:
            self.execute_javascript(f"window.scrollBy(0, {initial_height});")
            # Wait time before next scroll
            time.sleep(wait_time)
            new_height = self.execute_javascript("return document.body.scrollHeight")
            if new_height == initial_height:
                break
            initial_height = new_height

    def scroll_to_page_start(self):
        """
        Simulates the scroll to the start of the page
        """
        self.execute_javascript(
            "window.scrollBy(0, -document.body.scrollHeight);")

    def scroll_element_into_view(self, locator, js=True, timeout=None):
        """
        Find element and scroll the element into view
        :param locator:  String to find the element on webpage
        :param js: True if to perform action using execute_javascript(default), for native methods set it as False
        :param timeout: The timeout to find the element.
            If None, timeout defaults to 30 seconds.
        :return:
        """
        element = self.context.driver.find_element(By.ID, locator)
        if js:
            self.execute_javascript('arguments[0].scrollIntoView(true)', element)
        else:

            try:
                location = element.location_once_scrolled_into_view
                self.context.logger.info(
                    f'Successfully scrolled element into view. Location:{location}')

            except Exception as ex:
                self.context.logger.error(
                    f'Unable to scroll element into view.')
                self.context.logger.exception(ex)
                raise Exception(
                    f'Unable to scroll element into view. Error: {ex}')
