# Name   : BrowserWindow.py
# Author : Harshavardhan (HK)
# Time    : 03/12/2020 12:45 pm
# Desc: BrowserWindow class holds all the methods to manipulate browser windows.
from selenium.webdriver.common.alert import Alert

from ui_automation_core.helpers.browser.alert_action_type import AlertActionType


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

    def switch_to_alert(self):
        """
        Switches focus to an alert displayed on current page
        :return: Alert object
        """
        try:

            self.context.logger.info(
                'Successfully switched the focus to the alert on the web page.')
            return self.context.driver.switch_to.alert
        except Exception as ex:
            self.context.logger.error('Unable to switch the focus to the alert.')
            self.context.logger.exception(f'Error: {ex}')
            raise Exception(
                f'Unable to switch the focus to the alert. Error: {ex}')

    def switch_to_active_element(self):
        """
        Returns the element with focus, or BODY if nothing has focus.
        """
        try:
            active_ele = self.context.driver.switch_to.active_element
            self.context.logger.info(
                'Successfully switched focus to the current active element')
            return active_ele

        except Exception as ex:
            self.context.logger.error('Unable to switch focus to the  current active element. ')
            self.context.logger.exception(ex)
            raise Exception(
                'Unable to switch  focus to the current element. Error: %s' % ex)

    def switch_to_frame(self, frame_reference):
        """
        Switch the current context into an iframe using frame name or frame Id.

        :param frame_reference:Frame name or Id
        :return: None
        """

        try:
            self.context.driver.switch_to.frame(frame_reference)
            self.context.logger.info(f'Successfully switched to the frame with reference '
                                     f'{frame_reference}')
        except Exception as ex:
            self.context.logger.error('Unable to switch to the frame with reference '
                                      f'{frame_reference}.')
            self.context.logger.exception(ex)
            raise Exception(f'Unable to switch to the frame with reference {frame_reference}. '
                            f'Error: {ex}')

    def switch_to_default_content(self):
        """
        Switch back to default window, after dealing with some framed elements
        """
        try:
            self.context.driver.switch_to.default_content()
            self.context.logger.info(
                'Successfully Switch back to default/parent window')
        except Exception as ex:
            self.context.logger.error('Unable to switch back to default/parent window')
            raise Exception(
                'Unable to switch back to default/parent window. Error: %s' % ex)

    def switch_to_parent_frame(self):
        """
        Switches focus to the parent frame.
        If the current context is not a child frame context, the context remains unchanged.
        """
        try:
            self.context.driver.switch_to.parent_frame()
            self.context.logger.info(
                'Successfully switched to the parent frame.')
        except Exception as ex:
            self.context.logger.error(
                'Unable to switch to the parent frame.')
            self.context.logger.exception(ex)
            raise Exception(
                'Unable to switch to the parent frame. Error: %s' % ex)

    def alert_get_text(self):
        """
        Get displayed text of an alert popup (alert, confirmation popup, prompt popup)
        :return: Text of an alert
        """
        self.context.logger.info(
            'Trying to retrieve alert text.')
        try:
            alert_text = Alert(self.context.driver).text
            self.context.logger.info(
                f'Successfully retrieved the of an alert popup. The text retrieved is `{alert_text}`')
            return alert_text
        except Exception as ex:
            self.context.logger.error(
                f'Unable to retrieve text of an alert popup.')
            self.context.logger.exception(ex)
            raise Exception(
                f'Unable to retrieve text of an alert popup. Error: {ex}')

    def alert_action(self, action):
        """
        Simulate users clicking on "OK"/"Cancel" button of an alert popup (alert, confirmation popup, prompt popup).

        :param action: Action to perform on popup. Should be an instance of AlertActionType
            Available values are
            AlertActionType.ACCEPT, AlertActionType.DISMISS
        :return: self
        """
        try:
            if not isinstance(action, AlertActionType):
                raise TypeError(f'{action} must be an instance of AlertActionType')
            if action is AlertActionType.ACCEPT:
                Alert(self.context.driver).accept()
            elif action is AlertActionType.DISMISS:
                Alert(self.context.driver).dismiss()
            self.context.logger.info(
                f'Successfully performed the action {action} on the popup.')
            return self
        except TypeError:
            self.context.logger.error(f'{action} must be an instance of AlertActionType')
            raise TypeError
        except Exception as ex:
            self.context.logger.error(f'Unable to perform action {action} on the popup.')
            self.context.logger.exception(ex)
            raise Exception(
                f'Unable to perform action {action} on the popup. Error: {ex}')

    def alert_send_keys(self, text):
        """
        Simulate users typing text into a prompt popup.

        :param text: Text be entered into the prompt popup.
        :return: self
        """
        try:
            Alert(self.context.driver).send_keys(text)
            self.context.logger.info(
                f'Successfully sent keys {text} to the popup.')
            return self
        except Exception as ex:
            self.context.logger.error(f'Unable to send the keys {text} to the alert.')
            self.context.logger.exception(ex)
            raise Exception(
                f'Unable to send the keys {text} to the alert. Error: {ex}')
