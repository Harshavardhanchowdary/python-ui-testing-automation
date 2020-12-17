import os
from datetime import datetime
from pathlib import Path

from selenium.webdriver import ActionChains
from selenium.webdriver.remote.webelement import WebElement

from ui_automation_core.helpers.web_element.locator import Locator
from ui_automation_core.helpers.web_element.wait_states import ElementWaitState


class Actions:
    """

    """

    def __init__(self, context):
        self.context = context

    def get_web_element_inner_text(self, locator, wait_state=ElementWaitState.PRESENT, timeout=None):
        """
        Get the visible (i.e. not hidden by CSS) inner text of the web element without any leading
                or trailing whitespace.

        :param locator: The string pattern to find the element or the web element itself.
        :param wait_state: The wait state for retrial. Choose state from ElementWaitState class.
        :param timeout: wait time before throwing any exception.
                    If None, timeout is set to default timeout.
        :return: inner html
        """

        outer_html = None
        try:

            if isinstance(locator, WebElement):
                outer_html = locator.get_attribute('outerHTML')
                element_text = locator.text

            else:
                element = Locator(self.context).get_element(locator, wait_state, True, timeout)
                outer_html = element.get_attribute('outerHTML')
                element_text = element.text

            self.context.logger.info(f'Successfully performed get text on `{outer_html}` html.'
                                     f'Text obtained `{element_text}` ')
            return element_text
        except Exception as ex:
            self.context.logger.error(f'Unable to get the text on the element `{outer_html}`. '
                                      'Error: {ex}')
            self.context.logger.exception(ex)
            raise Exception(
                f'Unable to get the text on the element `{outer_html}`. Error:{ex}')

    def set_text(self, locator, text, clear_text=True, wait_state=ElementWaitState.PRESENT, timeout=None):
        """
        Set the value of an input field, as though you type it in.
        It also clears the previous value of the input field if clear_text is set to true.
        :param locator:
        :param text:
        :param clear_text: boolean value to clear the previous value of the input field
            Defaults to True
        :param wait_state: he wait state for element retrial. Choose state from ElementWaitState class.
            Defaults to ElementWaitState.PRESENT.
        :param timeout: wait time before throwing any exception.
                    If None, timeout is set to default timeout.
        :return: self
        """
        field_name = None
        try:
            if isinstance(locator, WebElement):
                field_name = locator.get_attribute('name')
                if clear_text:
                    locator.clear()
                    self.context.logger.info(
                        f'Successfully cleared the text from input field `Input Field Name: {field_name}`.')
                locator.send_keys(text)
            else:
                element = Locator(self.context).get_element(locator, wait_state, True, timeout)
                field_name = element.get_attribute('name')
                if clear_text:
                    element.clear()
                    self.context.logger.info(
                        f'Successfully cleared the text from input field `Input Field Name: {field_name}`.')
                element.send_keys(text)
            self.context.logger.info(
                f'Successfully entered the text \'{text}\' in the input field `Input Field Name:{field_name}`')
            return self
        except Exception as ex:
            self.context.logger.error(f'Unable to set the text \'{text}\' n the input field '
                                      f'`Input Field Name:{field_name}`.')
            self.context.logger.exception(ex)
            raise Exception('Unable to set the text \'{text}\' n the input field '
                            f'`Input Field Name:{field_name}`. Error: {ex}')

    def submit_form(self, locator, wait_state=ElementWaitState.PRESENT, timeout=None):
        """
        Submits a form.
        If the current element is a form or an element within a form, then this will be submitted.
        :param locator:  Web element or a locator string on which the action need to be performed.
        :param wait_state: he wait state for retrial. Choose state from ElementWaitState class.
        :param timeout: wait time before throwing any exception. If None, timeout is set to default timeout.
        :return: self
        """

        element_to_log = None
        try:
            if locator is None:
                raise ValueError('Please provide the string pattern or a web element to perform an action.')

            element, element_to_log = (locator, locator.get_attribute('outerHTML')) \
                if isinstance(locator, WebElement) \
                else (Locator(self.context).get_element(locator, wait_state, True, timeout), locator)
            element.submit()
            self.context.logger.info('Successfully performed a submit action on the element '
                                     f'{element_to_log}')
            return self
        except Exception as ex:
            self.context.logger.error(
                f'Unable to submit the form from. Submit action performed on the element `{element_to_log}`.')
            self.context.logger.exception(ex)
            raise Exception(
                f'Unable to submit the form from. Submit action performed on the element `{element_to_log}`. '
                f'Error: {ex}')

    def clear_text(self, locator, wait_state=ElementWaitState.PRESENT, timeout=None):
        """
        Clears the text if it’s a text entry element.

        :param locator:  Web element or a locator string on which the action need to be performed.
        :param wait_state: he wait state for retrial. Choose state from ElementWaitState class.
        :param timeout: wait time before throwing any exception. If None, timeout is set to default timeout.
        :return: self
        """
        element_to_log = None
        try:
            if locator is None:
                raise ValueError('Please provide the string pattern or a web element to perform an action.')

            element, element_to_log = (locator, locator.get_attribute('outerHTML')) \
                if isinstance(locator, WebElement) \
                else (Locator(self.context).get_element(locator, wait_state, True, timeout), locator)
            element.clear()
            self.context.logger.info('Successfully cleared the text from the input field '
                                     f'`{element_to_log}`')
            return self
        except ValueError:
            self.context.logger.error(
                'String pattern is None.'
                ' Please provide a valid pattern to locate the element and to perform an action.')
            raise ValueError
        except Exception as ex:
            self.context.logger.error(f'Unable to clear the text from input field `{element_to_log}`.')
            self.context.logger.exception(ex)
            raise Exception(
                f'Unable to clear the text from input field `{element_to_log}`. Error: {ex}')

    def get_attribute(self, locator, attribute, wait_state=ElementWaitState.PRESENT, timeout=None):
        """
        Gets the given attribute or property of the element.

        :param locator:  Web element or a locator string on which the action need to be performed.
        :param attribute: attribute/ property
        :param wait_state: he wait state for retrial. Choose state from ElementWaitState class.
        :param timeout: wait time before throwing any exception. If None, timeout is set to default timeout.
        :return: This method will first try to return the value of a property with the given name.
         If a property with that name doesn't exist, it returns the value of the attribute with the same name.
         If there’s no attribute with that name, None is returned.
        """
        element_to_log = None
        try:
            if locator is None:
                raise ValueError('Please provide the string pattern or a web element to perform an action.')
            if attribute is None:
                raise ValueError('Please provide the valid attribute  to perform an action.')
            element, element_to_log = (locator, locator.get_attribute('outerHTML')) \
                if isinstance(locator, WebElement) \
                else (Locator(self.context).get_element(locator, wait_state, True, timeout), locator)
            value = element.get_attribute(attribute)
            self.context.logger.info(f'Successfully performed get attribute call for \'{attribute}\' '
                                     f'on the element {element_to_log}. The value obtained is: `{value}`')
            return value
        except ValueError as val_ex:
            self.context.logger.error(
                f'ValueError occurred.')
            self.context.logger.exception(val_ex)
            raise ValueError
        except Exception as ex:
            self.context.logger.error(f'Unable to get attribute value for \'{attribute}\' on the'
                                      f' element {element_to_log}.')
            self.context.logger.error(ex)
            raise Exception(f'Unable to get attribute value for \'{attribute}\' on the element '
                            f'{element_to_log}. Error: {ex}')

    def get_property(self, locator, name, wait_state=ElementWaitState.PRESENT, timeout=None):
        """
        Gets the given property of the element.

        :param locator:  Web element or a locator string on which the action need to be performed.
        :param name: Name of the property
        :param wait_state: he wait state for retrial. Choose state from ElementWaitState class.
        :param timeout: wait time before throwing any exception. If None, timeout is set to default timeout.
        :return: the given property of the element.
        """
        element_to_log = None
        try:
            if locator is None:
                raise ValueError('Please provide the string pattern or a web element to perform an action.')
            if name is None:
                raise ValueError('Please provide the valid property name to perform an action.')
            element, element_to_log = (locator, locator.get_attribute('outerHTML')) \
                if isinstance(locator, WebElement) \
                else (Locator(self.context).get_element(locator, wait_state, True, timeout), locator)
            value = element.get_property(name)
            self.context.logger.info(f'Successfully performed get property call for \'{name}\' '
                                     f'on the element {element_to_log}. The retrieved value is `{value}.')
            return value
        except ValueError as val_ex:
            self.context.logger.error(
                f'ValueError occurred.')
            self.context.logger.exception(val_ex)
            raise ValueError
        except Exception as ex:
            self.context.logger.error(f'Unable to get property value for \'{name}\' on'
                                      f' the element {element_to_log}.')
            self.context.logger.exception(ex)

            raise Exception(f'Unable to get property value for \'{name}\' on the element '
                            f'{element_to_log}. Error: {ex}')

    def get_element_size(self, locator, wait_state=ElementWaitState.PRESENT, timeout=None):
        """
        The size of the element.
        :param locator:  Web element or a locator string on which the action need to be performed.
        :param wait_state: he wait state for retrial. Choose state from ElementWaitState class.
        :param timeout: wait time before throwing any exception. If None, timeout is set to default timeout.
        :return: The size of the element.
        """

        element_to_log = None
        try:
            if locator is None:
                raise ValueError('Please provide the string pattern or a web element to perform an action.')
            element, element_to_log = (locator, locator.get_attribute('outerHTML')) \
                if isinstance(locator, WebElement) \
                else (Locator(self.context).get_element(locator, wait_state, True, timeout), locator)
            size = element.size
            self.context.logger.info(f'Successfully performed get size call on the '
                                     f'element {element_to_log} and the value is {size}')
            return size
        except ValueError as val_ex:
            self.context.logger.error(
                f'ValueError occurred.')
            self.context.logger.exception(val_ex)
            raise ValueError
        except Exception as ex:
            self.context.logger.error(f'Unable to get size on the element {element_to_log}.')
            self.context.logger.exception(ex)
            raise Exception(
                f'Unable to get get size on the element {element_to_log}. Error: {ex}')

    def get_location(self, locator, wait_state=ElementWaitState.PRESENT, timeout=None):
        """
        Gets the location of the element in the renderable canvas.
        The size of the element.
        :param locator:  Web element or a locator string on which the action need to be performed.
        :param wait_state: he wait state for retrial. Choose state from ElementWaitState class.
        :param timeout: wait time before throwing any exception. If None, timeout is set to default timeout.
        :return: The location of the element.
        """

        element_to_log = None
        try:
            if locator is None:
                raise ValueError('Please provide the string pattern or a web element to perform an action.')
            element, element_to_log = (locator, locator.get_attribute('outerHTML')) \
                if isinstance(locator, WebElement) \
                else (Locator(self.context).get_element(locator, wait_state, True, timeout), locator)
            loc = element.location
            self.context.logger.info(f'Successfully performed get location call on the '
                                     f'element {element_to_log}. The value is `{loc}`')

            return loc
        except ValueError as val_ex:
            self.context.logger.error(
                f'ValueError occurred.')
            self.context.logger.exception(val_ex)
            raise ValueError

        except Exception as ex:
            self.context.logger.error(f'Unable to get location of the element {element_to_log}.')
            self.context.logger.exception(ex)
            raise Exception(
                f'Unable to get get location of the element {element_to_log}. Error: {ex}')

    def get_rectangle(self, locator, wait_state=ElementWaitState.PRESENT, timeout=None):
        """
        A dictionary with the size and location of the element.
        :param locator:  Web element or a locator string on which the action need to be performed.
        :param wait_state: he wait state for retrial. Choose state from ElementWaitState class.
        :param timeout: wait time before throwing any exception. If None, timeout is set to default timeout.
        :return:  A dictionary with the size and location of the element.
        """

        element_to_log = None
        try:
            if locator is None:
                raise ValueError('Please provide the string pattern or a web element to perform an action.')
            element, element_to_log = (locator, locator.get_attribute('outerHTML')) \
                if isinstance(locator, WebElement) \
                else (Locator(self.context).get_element(locator, wait_state, True, timeout), locator)
            size = element.rect
            self.context.logger.info(f'Successfully performed get rect call on the '
                                     f'element {element_to_log}. The value is `{size}`.')
            return size
        except ValueError as val_ex:
            self.context.logger.error(
                f'ValueError occurred.')
            self.context.logger.exception(val_ex)
            raise ValueError

        except Exception as ex:
            self.context.logger.error(f'Unable to perform get rect on the element {element_to_log}.')
            self.context.logger.exception(ex)
            raise Exception(
                f'Unable to perform get rect on the element {element_to_log}. Error: {ex}')

    def take_screenshot(self, file_path=None, locator=None, wait_state=ElementWaitState.PRESENT,
                        timeout=None):

        """
        Takes the screenshot of entire page or a given element.

        :param file_path: Path+filename.png,  where the screenshot should be saved.
                Default: None - To save screenshot to screenshots folder.

        :param locator:  Web element or a locator string whose screenshot need to be taken.
                Default: None - To take entire screenshot.

        :param wait_state: he wait state for retrial. Choose state from ElementWaitState class.
        :param timeout: wait time before throwing any exception. If None, timeout is set to default timeout.
        :return: Boolean True if successful. False if there is any IOError.
        """

        element_to_log = None
        if file_path is None:
            if not os.path.exists('../../screenshots/'):
                self.context.logger.info(f"Trying to create a Screenshots directory.")
                os.makedirs('../../screenshots/')
                self.context.logger.info(f"Screenshots directory created.")

            file_path = f'{os.path.abspath("screenshots")}/{datetime.now().strftime("%Y_%m_%d_%H_%M_%S_%f")}' \
                        f'_{"ele " if locator is not None else "full_screen"}.png'

        try:
            parent_dir = Path(file_path).parent
            if not parent_dir.exists():
                self.context.logger.error(f'The parent directory `{parent_dir}` does not exist, '
                                          'Please provide a valid path !!')
                raise FileNotFoundError(f'The parent directory `{parent_dir}` does not exist, '
                                        'Please provide a valid path !!')
            if isinstance(locator, WebElement):
                element, element_to_log = locator, locator.get_attribute('outerHTML')
            else:
                element, element_to_log = Locator(self.context).get_element(locator, wait_state, True, timeout) \
                                              if locator is not None else None, locator
            if element is None:
                status = self.context.driver.save_screenshot(file_path)
            else:
                status = element.screenshot(file_path)
            self.context.logger.info(f'Successfully captured the screenshot of the '
                                     f'{"element " + element_to_log if element_to_log is not None else "entire page"} '
                                     f'to the file {file_path}')
            return status

        except Exception as ex:
            self.context.logger.error(f'Unable to take screenshot of the element {element_to_log}.')
            self.context.logger.exception(ex)
            raise Exception(
                f'Unable to take screenshot of the element {element_to_log}. Error: {ex}')

    def key_press_and_release(self, modifier_value, key, locator=None,
                              wait_state=ElementWaitState.PRESENT, timeout=None):
        """
        Sends a key press and releasing it.
            Should only be used with modifier keys (Control, Alt and Shift).
        :param modifier_value: Should be modifier keys (Control, Alt and Shift).
        :param key: The key to send.
         :param locator: The element to send keys. If None, sends a key to current focused element..
        :param wait_state: he wait state for retrial. Choose state from ElementWaitState class.
        :param timeout: wait time before throwing any exception. If None, timeout is set to default timeout.
        :return: self

        USAGE: key_press_and_release(KeyCode.CONTROL,'c')
        """
        element_to_log = None
        try:

            element, element_to_log = (locator, locator.get_attribute('outerHTML')) \
                if isinstance(locator, WebElement) \
                else (Locator(self.context).get_element(locator, wait_state, True, timeout)
                      if locator is not None else None, locator)

            ActionChains(self.context.driver)\
                .key_down(modifier_value, element)\
                .send_keys(key)\
                .key_up(modifier_value, element)\
                .perform()

            self.context.logger.info(f'Successfully performed key press and release '
                                     f'{(modifier_value, key)} on element {element_to_log}')
            return self
        except Exception as ex:
            self.context.logger.error(f'Unable to perform key press and release '
                                      f'{(modifier_value, key)} on element {element_to_log}.')
            self.context.logger.exception(ex)
            raise Exception(f'Unable to perform key press and release {(modifier_value, key)} '
                            f'on element{element_to_log}. Error: {ex}')


