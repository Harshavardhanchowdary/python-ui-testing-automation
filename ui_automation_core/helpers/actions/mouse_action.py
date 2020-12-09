from enum import Enum, auto

from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.remote.webelement import WebElement

from ui_automation_core.helpers import js_executor
from ui_automation_core.helpers.web_element.locator import Locator
from ui_automation_core.helpers.web_element.wait_states import ElementWaitState


class ClickMethod(Enum):
    API_CLICK = auto()
    ACTION_CHAIN_CLICK = auto()
    JAVA_SCRIPT_CLICK = auto()


class MouseAction:
    """
    MouseAction class is a collection of Mouse Actions that you want to perform on an web element.

    """

    def __init__(self, context):
        self.context = context

    def click_web_element(self, locator=None, click_method=ClickMethod.API_CLICK,
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
        element_to_log = None
        try:
            if not isinstance(click_method, ClickMethod):
                raise TypeError(f'`{click_method}` must be an instance of ClickMethod.')

            if locator is None:
                raise ValueError('Please provide the string pattern or a web element to perform a click')

            if isinstance(locator, WebElement):
                element, element_to_log = locator, locator.get_attribute('outerHTML')
            else:
                element, element_to_log = Locator(self.context).get_element(locator, wait_state, True, timeout), locator
            if click_method is ClickMethod.API_CLICK:
                element.click()
                self.context.logger.info(
                    f'Successfully clicked on the element {element_to_log}')
            if click_method is ClickMethod.JAVA_SCRIPT_CLICK:
                js_executor.execute_javascript('arguments[0].click();', element)
                self.context.logger.info(
                    f'Successfully clicked on the element {element_to_log}')
            if click_method is ClickMethod.ACTION_CHAIN_CLICK:
                ActionChains(self.context.driver).click(element).perform()
                self.context.logger.info(
                    f'Successfully clicked on the element {element_to_log}')
            return self
        except TypeError:
            self.context.logger.error(f'`{click_method}` must be an instance of ClickMethod')
            raise TypeError
        except ValueError:
            self.context.logger.error('String pattern is None. Please provide a valid pattern to locate the element.')
            raise ValueError
        except Exception as ex:
            self.context.logger.error(
                f'Unable to click on the element `{element_to_log}`.')
            self.context.logger.exception(ex)
            raise Exception(
                f'Unable to click on the element `{element_to_log}`. Error: {ex}')

    def double_click(self, locator=None, wait_state=ElementWaitState.PRESENT, timeout=None):
        """
        Double-clicks an element.

        :param locator: Web element or a locator string on which the click action need to be performed
        :param wait_state: he wait state for retrial. Choose state from ElementWaitState class.
        :param timeout: wait time before throwing any exception.
                    If None, timeout defaults to 20 seconds.
        :return: self
        """
        element_to_log = None
        try:

            if locator is None:
                raise ValueError('Please provide the string pattern or a web element to perform a double click.')

            if isinstance(locator, WebElement):
                element, element_to_log = locator, locator.get_attribute('outerHTML')

            else:
                element, element_to_log = Locator(self.context).get_element(locator, wait_state, True, timeout) \
                                              if locator is not None else None, locator
            ActionChains(self.context.driver).double_click(element).perform()
            self.context.logger.info(
                f'Successfully double clicked on element {element_to_log}')
            return self
        except ValueError:
            self.context.logger.error(
                'String pattern is None. Please provide a valid pattern to locate the element and perform a '
                'click action.')
            raise ValueError

        except Exception as ex:
            self.context.logger.error(f'Unable to double click on element {element_to_log}.')
            self.context.logger.exception(ex)
            raise Exception(
                f'Unable to double click on element {element_to_log}. Error: {ex}')

    def context_click(self, locator=None, wait_state=ElementWaitState.PRESENT, timeout=None):
        """
        Right-click on the given element.

        :param locator: Web element or a locator string on which the click action need to be performed
        :param wait_state: he wait state for retrial. Choose state from ElementWaitState class.
        :param timeout: wait time before throwing any exception.
                    If None, timeout defaults to 20 seconds.
        :return: self
        """
        element_to_log = None
        try:
            if locator is None:
                raise ValueError('Please provide the string pattern or a web element to perform a right click.')

            if isinstance(locator, WebElement):
                element, element_to_log = locator, locator.get_attribute('outerHTML')
            else:
                element, element_to_log = Locator(self.context).get_element(locator, wait_state, True, timeout) \
                                              if locator is not None else None, locator
            ActionChains(self.context.driver).context_click(element).perform()
            self.context.logger.info(
                f'Successfully right clicked on element {element_to_log}')
            return self
        except ValueError:
            self.context.logger.error(
                'String pattern is None. Please provide a valid pattern to locate the element and perform a '
                'right click action.')
            raise ValueError

        except Exception as ex:
            self.context.logger.error(f'Unable to right click on element {element_to_log}.')
            self.context.logger.exception(ex)
            raise Exception(
                f'Unable to right click on element {element_to_log}. Error: {ex}')

    def move_cursor_to_element(self, locator, wait_state=ElementWaitState.PRESENT, timeout=None):
        """
        Simulate users hovering a mouse over the given element.

        :param locator: Web element or a locator string on which the click action need to be performed
        :param wait_state: he wait state for retrial. Choose state from ElementWaitState class.
        :param timeout: wait time before throwing any exception.
                    If None, timeout defaults to 20 seconds.
        :return: self
        """
        element_to_log = None
        try:

            if locator is None:
                raise ValueError('Please provide the string pattern or a web element to perform an action.')

            if isinstance(locator, WebElement):
                element, element_to_log = locator, locator.get_attribute('outerHTML')
            else:
                element, element_to_log = Locator(self.context).get_element(locator, wait_state, True, timeout) \
                                              if locator is not None else None, locator
            ActionChains(self.context.driver).move_to_element(element).perform()

            self.context.logger.info(
                f'Successfully moved the cursor on to the element {element_to_log}')
            return self
        except ValueError:
            self.context.logger.error(
                'String pattern is None. Please provide a valid pattern to locate the element and perform an '
                'action.')
            raise ValueError

        except Exception as ex:
            self.context.logger.error(f'Unable to move the cursor to the element {element_to_log}.')
            self.context.logger.exception(ex)
            raise Exception(
                f'Unable to move to the element {element_to_log}. Error: {ex}')

    def move_cursor_by_offset(self, x_offset, y_offset):
        """
        Moving the mouse to an offset from current mouse position.

        :param x_offset: X offset to move to, as a positive or negative integer.
        :param y_offset: Y offset to move to, as a positive or negative integer.
        :return: self
        """
        try:
            ActionChains(self.context.driver).move_by_offset(
                x_offset, y_offset).perform()
            self.context.logger.info(
                f'Successfully moved by offset {x_offset, y_offset}')
            return self
        except Exception as ex:
            self.context.logger.error(f'Unable to move by offset {x_offset, y_offset}.')
            self.context.logger.exception(ex)
            raise Exception(
                f'Unable to move by offset {x_offset, y_offset}. Error: {ex}')

    def move_cursor_to_element_by_offset(self, locator, x_offset, y_offset,
                                         wait_state=ElementWaitState.PRESENT, timeout=None):
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
        element_to_log = None
        try:

            element, element_to_log = (locator, locator.get_attribute('outerHTML')) \
                if isinstance(locator, WebElement) \
                else (Locator(self.context).get_element(locator, wait_state, True, timeout), locator)

            (ActionChains(self.context.driver).move_to_element_with_offset(element, x_offset, y_offset).perform())

            self.context.logger.info(f'Successfully moved mouse pointer by an offset {x_offset, y_offset} '
                                     f'on the element {element_to_log}')
            return self
        except Exception as ex:
            self.context.logger.error(f'Unable to move by an offset {x_offset, y_offset} '
                                      f'on the element {element_to_log}')
            self.context.logger.exception(ex)
            raise Exception(f'Unable to move by an offset {x_offset, y_offset} to the '
                            f'element {element_to_log}. Error: {ex}')

    def drag_and_drop_to_object(self, source, target, wait_state=ElementWaitState.PRESENT, timeout=None):
        """
        Drag an object and drop it onto another object. Holds down the left mouse button on the source element,
        then moves to the target element and releases the mouse button.

        :param source: The element to mouse down. (element to be moved). Can be a locator string or an web element.
        :param target: The element to mouse up. (destination location). Can be locator string or an web element
        :param wait_state: he wait state for retrial. Choose state from ElementWaitState class.
        :param timeout: wait time before throwing any exception.
                    If None, timeout defaults to 20 seconds.
        :return: self
        """
        trg_element = None
        trg_element_to_log = None
        src_element_to_log = None
        try:
            if source is None:
                raise ValueError(
                    'Please provide the `source` string pattern or a web element to perform drag and drop.')
            if target is None:
                raise ValueError(
                    'Please provide the `target` string pattern or a web element to perform a drag and drop.')
            if isinstance(source, WebElement):
                src_element, src_element_to_log = source, source.get_attribute('outerHTML')
            else:
                src_element, src_element_to_log = Locator(self.context).get_element(source, wait_state, True,
                                                                                    timeout), source
            if isinstance(target, WebElement):
                src_element, trg_element_to_log = target, target.get_attribute('outerHTML')
            else:
                trg_element, trg_element_to_log = Locator(self.context).get_element(target, wait_state, True,
                                                                                    timeout), target

            (ActionChains(self.context.driver).drag_and_drop(src_element, trg_element).perform())
            self.context.logger.info(f'Successfully dragged from the source element '
                                     f'{src_element_to_log} and dropped onto target element {trg_element_to_log}')
            return self
        except ValueError:
            self.context.logger.error(
                f'Locator pattern is None. Please provide a valid {"`source`" if source is None else "`target`"}'
                f' pattern to locate the element and perform a drag and drop operation.')

            raise ValueError

        except Exception as ex:
            self.context.logger.error(f'Unable to drag and drop on elements {src_element_to_log} '
                                      f'and {trg_element_to_log}.')
            self.context.logger.exception(ex)
            raise Exception(f'Unable to drag and drop on elements {src_element_to_log} '
                            f'and {trg_element_to_log}. Error: {ex}')

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

        element_to_log = None
        try:

            if src_locator is None:
                raise ValueError(
                    'Please provide the `source` string pattern or a web element to perform drag and drop.')

            if isinstance(src_locator, WebElement):
                element, element_to_log = src_locator, src_locator.get_attribute('outerHTML')
            else:
                element, element_to_log = Locator(self.context).get_element(src_locator, wait_state, True, timeout), \
                                          src_locator
            (ActionChains(self.context.driver)
             .drag_and_drop_by_offset(element, x_offset, y_offset).perform())
            self.context.logger.info(
                f'Successfully moved the source element {element_to_log} by an offset {x_offset, y_offset}')
            return self
        except ValueError:
            self.context.logger.error(
                f'Locator pattern is None. Please provide a valid `source`'
                f' pattern to locate the element and perform a drag and drop operation.')

            raise ValueError
        except Exception as ex:
            self.context.logger.error(
                f'Unable to move the source element {element_to_log} by an offset {x_offset, y_offset}.')
            self.context.logger.exception(ex)
            raise Exception(
                f'Unable to move the source element {element_to_log} by an offset {x_offset, y_offset}. Error: {ex}')
