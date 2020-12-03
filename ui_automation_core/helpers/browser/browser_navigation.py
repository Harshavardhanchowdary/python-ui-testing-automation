class BrowserINavigation:

    def __init__(self, context):
        self.context = context

    def launch_browser_with_url(self, url):
        """
                Launches the selected webdriver with the application URL
                :param
                url: application url under test
                :return:
                None
                """

        try:
            self.context.driver.get(url)
            self.context.logger.info(f'Successfully launched the browser with URL:`{url}`.')
        except Exception as ex:
            self.context.logger.error('Unable to launched the browser.')
            self.context.logger.exception(ex)
            raise Exception(f'Unable to launched the browser. Error: {str(ex)}')

    def close_browser_active_window(self):
        """
                Close the current browser window having focus.
        """
        try:
            self.context.driver.close()
            self.context.logger.info('Successfully closed the current window.')
        except Exception as ex:
            self.context.logger.error('Unable to close the current window.')
            self.context.logger.exception(ex)
            raise Exception(f'Unable to close the current window. Error: {str(ex)}')

    def close_browser_all_windows(self):
        """
        Quits all the browser sessions along with all the associated browser windows, tabs and pop-ups.
        """
        try:
            self.context.driver.quit()
            self.context.logger.info('Successfully quit the browser and all its associated windows')
        except Exception as ex:
            self.context.logger.error('Unable to quit the browser and all associated windows.')
            self.context.logger.exception(ex)
            raise Exception(f'Unable to quit the browser and its associated windows. Error: {str(ex)}')

    def get_url(self) -> str:
        """
        Returns the URL of the current page.
        :return url: current active window URL
         """
        try:
            url = self.context.driver.current_url
            self.context.logger.info(f'Successfully retrieved current active window url. URL: `{url}`.')
            return url
        except Exception as ex:
            self.context.logger.error(f'Unable to get the URL of the current page.')
            self.context.logger.exception(ex)
            raise Exception(f'Unable to get the URL of the current page. Error: {str(ex)}')

    def maximize_current_window(self):
        """
        Resize the current window to take up the entire screen.
        """
        try:
            self.context.driver.maximize_window()
            self.context.logger.info('Successfully maximized the current window.')
            return self
        except Exception as ex:
            self.context.logger.error('Unable to maximize the current window.')
            self.context.logger.exception(ex)
            raise Exception(f'Unable to maximize the current window. Error: {str(ex)}')

    def minimize_current_window(self):
        """
        Minimizes the window of current browsing context.
        The exact behavior of this command is specific to individual window managers.
        Minimize Window typically hides the window in the system tray.
        """
        try:
            self.context.driver.minimize_window()
            self.context.logger.info('Successfully minimized the current window')
            return self
        except Exception as ex:
            self.context.logger.error('Unable to minimize the current window.')
            self.context.logger.exception(ex)
            raise Exception(f'Unable to minimize the current window. Error: {str(ex)}')

    def fullscreen_current_window(self):
        """
        Fills the entire screen, similar to pressing F11 in most browsers.
        """
        try:
            self.context.driver.fullscreen_window()
            self.context.logger.info('Successfully performed full screen action on the current ' \
                                     'window')
            return self
        except Exception as ex:
            self.context.logger.error('Unable to perform full screen action on the current ' \
                                      'window.')
            self.context.logger.exception(ex)
            raise Exception('Unable to perform full screen action on the current window. ' \
                            f'Error: {str(ex)}')

    def get_current_window_rect(self):
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
        try:
            rect = self.context.driver.get_window_rect()
            self.context.logger.info('Successfully performed get current window rect.')
            self.context.logger.info(f'The value is {rect}')
            return rect
        except Exception as ex:
            self.context.logger.error('Unable to get current window rect.')
            self.context.logger.exception(ex)
            raise Exception(f'Unable to get current window rect. Error: {str(ex)}')

    def page_refresh(self):
        """
        Simulate users clicking "refresh" button on their browser
        """
        try:
            self.context.driver.refresh()
            self.context.logger.info('Successfully refreshed the current page.')
            return self
        except Exception as ex:
            self.context.logger.error(
                'Unable to refresh the current page.')
            self.context.logger.exception(ex)
            raise Exception(
                f'Unable to refresh the current page. Error: {str(ex)}')

    def back(self):
        """
        Simulate users clicking "back" button on their browser.
        """
        try:
            self.context.driver.back()
            self.context.logger.info(
                'Navigated one step backward on the browser')
            return self
        except Exception as ex:
            self.context.logger.error('Unable to navigate one step backward on the browser. '
                                      'Error: %s' % ex)
            raise Exception(
                f'Unable to navigate one step backward on the browser. Error: {str(ex)}')

    def forward(self):
        """
       Simulate users clicking "forward" button on their browser.
        """
        try:
            self.context.driver.forward()
            self.context.logger.info(
                'Navigated one step forward on the browser')
            return self
        except Exception as ex:
            self.context.logger.error('Unable to navigate one step forward on the browser. '
                                      'Error: %s' % ex)
            raise Exception(
                f'Unable to navigate one step forward on the browser. Error: {str(ex)}')

