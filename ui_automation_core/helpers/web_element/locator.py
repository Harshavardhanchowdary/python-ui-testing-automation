import re
from enum import Enum

from selenium.common.exceptions import TimeoutException, StaleElementReferenceException, WebDriverException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from ui_automation_core.helpers.web_element.wait_states import ElementWaitState


class _ElementType(Enum):
    SINGLE = 1
    MULTIPLE = 2


class Locator:
    default_wait = 20
    # any string starting with # followed by at least one character
    _id_regex = re.compile(r'^([#])(.+)')
    # any text starting with / or // or ( followed by at least one character
    _xpath_regex = re.compile(r'^[\\/].+|^[(].+')
    # any string starting with . followed by at least one character
    _class_regex = re.compile(r'^([.])(.+)')
    # any string starting with @ followed by at least one character
    _link_text_regex = re.compile(r'^([@])(.+)')
    # any string starting with @ followed by at least one character and ends with @
    _partial_link_text_regex = re.compile(r'^([@])(.+)([@])$')
    # any string starting with < followed by at least one character and ends with >
    _tag_regex = re.compile(r'^([<])(.+)([>])$')
    # any string starting with css (by ignoring case) followed by at least one character
    _css_regex = re.compile(r'^(?i)([c][s][s][=])(.+)')
    # any string starting with [ followed by at least one character and ends with ]
    _name_regex = re.compile(r'^([\[])(.+)[]]$')

    def __init__(self, context):
        self.context = context

    def _get_locator(self, locator_pattern):
        """
        Used to return By class based on the locator string provided\n
        :param locator_pattern:
        :return: locator method type and locator string as a tuple
        """
        locator_string = None
        if self._id_regex.search(locator_pattern) is not None:
            return By.ID, self._id_regex.search(locator_pattern).group(2)
        elif self._xpath_regex.search(locator_pattern) is not None:
            return By.XPATH, self._xpath_regex.search(locator_pattern).group()
        elif self._class_regex.search(locator_pattern) is not None:
            return By.CLASS_NAME, self._class_regex.search(locator_pattern).group(2)
        elif self._partial_link_text_regex.search(locator_pattern) is not None:
            return By.PARTIAL_LINK_TEXT, self._partial_link_text_regex.search(locator_pattern).group(2)
        elif self._link_text_regex.search(locator_pattern) is not None:
            return By.LINK_TEXT, self._link_text_regex.search(locator_pattern).group(2)
        elif self._tag_regex.search(locator_pattern) is not None:
            return By.TAG_NAME, self._tag_regex.search(locator_pattern).group(2)
        elif self._css_regex.search(locator_pattern) is not None:
            return By.CSS_SELECTOR, self._css_regex.search(locator_pattern).group(2)
        elif self._name_regex.search(locator_pattern) is not None:
            return By.NAME, self._name_regex.search(locator_pattern).group(2)

        if locator_string is None:
            self.context.logger.error(f'Unsupported pattern \'{locator_pattern}\'. '
                                      'Supported locator patterns are: '
                                      'ID - Begins with `#`, '
                                      'XPATH - Begins with `// or / or (`, '
                                      'CLASS - Begins with `.`, '
                                      'LINK_TEXT - Begins with `@`, '
                                      'PARTIAL_LINK_TEXT - Begins with `@` and ends with `@`, '
                                      'TAG - Begins with `<` and ends with `>`, '
                                      'CSS - Begins with `css=`, '
                                      'NAME - Begins with `[` and ends with `]`')

            raise Exception(f'Unsupported pattern \'{locator_pattern}\'. '
                            'Supported locator strategies are: '
                            'ID - Begins with `#`, '
                            'XPATH - Begins with `// or / or (`, '
                            'CLASS - Begins with `.`, '
                            'LINK_TEXT - Begins with `@`, '
                            'PARTIAL_LINK_TEXT - Begins with `@` and ends with `@`, '
                            'TAG - Begins with `<` and ends with `>`, '
                            'CSS - Begins with `css=`, '
                            'NAME - Begins with `[` and ends with `]`')
        return locator_string

    def _get_web_element(self, element_type, locator_string, wait_state, throw_exception, timeout):
        """
        Returns web element or web elements based on the element type
        :param element_type: can be ElementType.SINGLE or ElementType.MULTIPLE
        :param locator_string: unique string to identify web element in DOM
        :param wait_state: ElementWaitState
        :param throw_exception: by default it is set to true, can be set to false
        :param timeout: wait time before throwing any exception
        :return: web element or web elements based on elementType
        """
        by_locator = None
        web_element = None
        if timeout is None:
            timeout = self.default_wait
        try:
            # retrieve the element locator in the form of tuple ex:(id, test)
            by_locator = self._get_locator(locator_string)

            # Check if the element_type has a valid value
            if not isinstance(element_type, _ElementType):
                self.context.logger.error(f'{repr(element_type)} must be an instance of _ElementType enum class')
                raise TypeError(f'{repr(element_type)} must be an instance of _ElementType enum class')

            # Retrieves single web element
            if element_type is _ElementType.SINGLE:
                web_element = self._get_single_web_element(
                    wait_state, by_locator, timeout)

            # Retrieves multiple web element
            if element_type is _ElementType.MULTIPLE:
                web_element = self._get_multiple_web_elements(
                    wait_state, by_locator, timeout)

        except StaleElementReferenceException as stale_ex:
            if throw_exception:
                self.context.logger.error(
                    f'The element {str(by_locator)} is no longer attached to the DOM '
                    f'i.e. it has been removed from the document or the document has changed')

                self.context.logger.exception(stale_ex)
                raise StaleElementReferenceException(
                    f'The element {str(by_locator)} is no longer attached to the DOM '
                    f'i.e. it has been removed from the document or the document has changed.'
                    f' Error {stale_ex}')

        except TimeoutException as timeout_ex:
            if throw_exception:
                self.context.logger.error(f'Timed out after {str(timeout)} seconds waiting for the '
                                          f'element {str(by_locator)} state {str(wait_state)}.')

                self.context.logger.exception(timeout_ex)
                raise TimeoutException(f'Timed out after {str(timeout)} seconds waiting for the '
                                       f'element {str(by_locator)} state {str(wait_state)}. Error {timeout_ex}')
        except WebDriverException as ex:
            if throw_exception:
                self.context.logger.error(f'An error occurred while identifying the element '
                                          f'{str(by_locator)} on the web page.')

                self.context.logger.exception(ex)
                raise WebDriverException(f'An error occurred while identifying the element '
                                         f'{str(by_locator)} on the web page. Error {ex}')
        return web_element

    def _get_single_web_element(self, wait_state, by_locator, timeout):
        """
        Retrieves the web element based on the locator string and the wait condition provided\n
        :param wait_state: is a instance of ElementWaitState
        :param by_locator: locator of the element to be located
        :param timeout: by default it is set to 20sec or can be supplied
        :return: a web_element
        """
        if wait_state is ElementWaitState.PRESENT:
            # An expectation for checking that an element is present on the DOM of a page.
            # This does not necessarily mean that the element is visible
            self.context.logger.info(f'Waiting for the presence of element '
                                     f'{str(by_locator)} on the web page')
            web_element = (WebDriverWait(self.context.driver, timeout)
                           .until(EC.presence_of_element_located(by_locator)))
            self.context.logger.info(f'Successfully waited for the presence of element '
                                     f'{str(by_locator)} on the web page')

        elif wait_state is ElementWaitState.VISIBLE:
            # An Expectation for checking that an element is either invisible or not present on the DOM.

            web_element = (WebDriverWait(self.context.driver, timeout)
                           .until(EC.visibility_of_element_located(by_locator)))
            self.context.logger.info(f'Successfully waited for the visibility of element '
                                     f'{str(by_locator)} on the web page. Please evaluate its return type')

        elif wait_state is ElementWaitState.INVISIBLE:
            # An Expectation for checking that an element is either invisible or not present on the DOM.

            web_element = (WebDriverWait(self.context.driver, timeout)
                           .until(EC.invisibility_of_element_located(by_locator)))
            self.context.logger.info(f'Successfully waited for the invisibility of element '
                                     f'{str(by_locator)} on the web page. Please evaluate its return type')

        elif wait_state is ElementWaitState.CLICKABLE:
            # An Expectation for checking an element is visible and enabled such that you can click it.

            web_element = (WebDriverWait(self.context.driver, timeout)
                           .until(EC.element_to_be_clickable(by_locator)))
            self.context.logger.info(f'Successfully waited for the element {str(by_locator)} '
                                     'to be clickable on the web page. Please evaluate its return type')

        elif wait_state is ElementWaitState.SELECTED:
            # An expectation for the element to be located is selected. locator is a tuple of (by, path)

            web_element = (WebDriverWait(self.context.driver, timeout)
                           .until(EC.element_located_to_be_selected(by_locator)))
            self.context.logger.info(f'Successfully waited for the element {str(by_locator)} '
                                     'to be in selected state on the web page. Please evaluate its return type')

        elif wait_state is ElementWaitState.FRAME_AVAILABLE_AND_SWITCH_TO:
            # An expectation for checking whether the given frame is available to switch to.
            # If the frame is available it switches the given driver to the specified frame.

            web_element = (WebDriverWait(self.context.driver, timeout)
                           .until(EC.frame_to_be_available_and_switch_to_it(by_locator)))
            self.context.logger.info(f'Successfully waited for the frame {str(by_locator)} '
                                     'to be available on the web page. Please evaluate its return type')
        else:
            try:
                raise ValueError(f'Invalid wait state {wait_state} to get single web element. '
                                 'Please choose an appropriate option!')
            except ValueError:
                self.context.logger.error(f'Invalid wait state {wait_state} to get '
                                          'single web element. Please choose an appropriate option!')
                raise ValueError
        return web_element

    def _get_multiple_web_elements(self, wait_state, by_locator, timeout):
        """
        Retrieves the web elements based on the locator string and the wait condition provided\n
        :param wait_state: is a instance of ElementWaitState,
        :param by_locator: locator of the elements to be located
        :param timeout: by default it is set to 20sec or can be supplied
        :return: web_elements
        """
        if wait_state is ElementWaitState.PRESENT_OF_ALL:
            # An expectation for checking that there is at least one element present on a web page.
            # locator is used to find the element returns the list of WebElements once they are located
            self.context.logger.info(f'Waiting for the presence of all elements with locator `'
                                     f'{str(by_locator)}` on the web page.')
            web_elements = (WebDriverWait(self.context.driver, timeout)
                            .until(EC.presence_of_all_elements_located(by_locator)))
            self.context.logger.info(f'Successfully waited for the presence of all elements with locator `'
                                     f'{str(by_locator)}` on the web page. Evaluate the list of returned web elements')

        elif wait_state is ElementWaitState.VISIBLE_OF_ANY:
            # An expectation for checking that there is at least one element visible on a web page.
            # locator is used to find the element returns the list of WebElements once they are located
            self.context.logger.info(f'Waiting for the visibility of any element  with locator `'
                                     f'{str(by_locator)}` on the web page.')
            web_elements = (WebDriverWait(self.context.driver, timeout)
                            .until(EC.visibility_of_any_elements_located(by_locator)))
            self.context.logger.info(f'Successfully waited for the visibility of any element  with locator `'
                                     f'{str(by_locator)}` on the web page.')

        elif wait_state is ElementWaitState.VISIBLE_OF_ALL:
            # An expectation for checking that all elements are present on the DOM of a page and visible.
            # Visibility means that the elements are not only displayed
            # but also has a height and width that is greater than 0.
            # locator - used to find the elements returns the list of WebElements once they are located and visible
            self.context.logger.info(f'Waiting for the visibility of all elements with locator `'
                                     f'{str(by_locator)}` on the web page. Evaluate the list of returned web elements')
            web_elements = (WebDriverWait(self.context.driver, timeout)
                            .until(EC.visibility_of_all_elements_located(by_locator)))
            self.context.logger.info(f'Successfully waited for the visibility of all elements '
                                     f'{str(by_locator)} on the web page. Evaluate the list of returned web elements')
        else:
            try:
                raise Exception(f'Invalid wait state {wait_state} to get multiple elements. '
                                'Please choose an appropriate option!')
            except ValueError:
                self.context.logger.error(f'Invalid wait state {wait_state} to get '
                                          'multiple elements. Please choose an appropriate option!')
                raise ValueError
        return web_elements

    def get_element(self,
                    locator, wait_state=ElementWaitState.PRESENT,
                    throw_exception=True, timeout=None):
        """
        Returns the web element based the specified locator pattern or 'None' if no element is found.

        :param locator: The string pattern used to find the element on a web page.
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
        return self._get_web_element(_ElementType.SINGLE,
                                     locator, wait_state,
                                     throw_exception, timeout)

    def get_elements(self,
                     locator, wait_state=ElementWaitState.PRESENT_OF_ALL,
                     throw_exception=True, timeout=None):
        """
        Returns the web elements based the specified locator pattern or 'None' if no elements are found.

        :param locator: The string pattern used to find the element on a web page.
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
        return self._get_web_element(_ElementType.MULTIPLE,
                                     locator, wait_state,
                                     throw_exception, timeout)

        # TODO: get_elements_from_parent_element,
        #  TODO: get_element_from_parent_element
