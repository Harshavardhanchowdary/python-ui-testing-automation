# Name   : BrowserWindow.py
# Author : Harshavardhan (HK)
# Time    : 03/12/2020 12:45 pm
# Desc: BrowserWindow class holds all the methods to manipulate browser windows.

class BrowserWindow:
    def __init__(self, context):
        self.context = context

    def get_current_window_handle(self):
        """
        Usage:	driver.current_window_handle
        :return: handle -> handle of the current window
        """

        try:
            handle = self.context.driver.current_window_handle
            self.context.logger.info(
                f'Successfully retrieved current window handle. Handle:{handle}')
            return handle
        except Exception as ex:
            self.context.logger.error(
                f'Unable to retrieve current window handle.')
            self.context.logger.exception(ex)
            raise Exception(
                f'Unable to retrieve current window handle. Error: {ex}')
