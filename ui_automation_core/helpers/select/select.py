from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import Select

from ui_automation_core.helpers.select.select_method import SelectMethod
from ui_automation_core.helpers.web_element.locator import Locator
from ui_automation_core.helpers.web_element.wait_states import ElementWaitState


class SelectAction:

    def __init__(self, context):
        self.context = context

    @staticmethod
    def _select_by_visible_text(select, is_select, *values):
        for value in values:
            if is_select:
                # Select all options that display text matching the argument.
                select.select_by_visible_text(value)
            else:
                # Deselect all options that display text matching the argument.
                select.deselect_by_visible_text(value)

    @staticmethod
    def _select_by_value(select, is_select, *values):
        for value in values:
            if is_select:
                # Select all options that have a value matching the argument.
                select.select_by_value(value)
            else:
                # Deselect all options that have a value matching the argument.
                select.deselect_by_value(value)

    @staticmethod
    def _select_by_index(select, is_select, *values):
        for value in values:
            if is_select:
                # Select the option at the given index. This is done by examing the “index” attribute of an element,
                # and not merely by counting.
                select.select_by_index(int(value))
            else:
                # Deselect the option at the given index. This is done by examing the “index” attribute of an element,
                # and not merely by counting.
                select.deselect_by_index(int(value))

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
        if locator is None:
            raise ValueError('Please provide the string pattern or a web element to perform an action')

        element, log_element = (locator, locator.get_attribute('outerHTML')) \
            if isinstance(locator, WebElement) \
            else (Locator(self.context).get_element(locator, wait_state, True, timeout), locator)
        try:

            if not element.is_selected() and is_select:
                # if checkbox is not selected and is_select is true
                element.click()
                self.context.logger.info(
                    f'Successfully selected the element {log_element}')
            elif element.is_selected() and not is_select:
                # if checkbox is selected and is_select is false
                element.click()
                self.context.logger.info(
                    f'Successfully unselected the element {log_element}')
            elif not element.is_selected() and not is_select:
                # if checkbox is not selected and is_select is false
                # element.click()
                self.context.logger.info(f'The element {log_element} is already in unselected state.')
            elif element.is_selected() and is_select:
                # if checkbox is selected and is_select is true
                # element.click()
                self.context.logger.info(
                    f'The element {log_element} is already in selected state')
            return self
        except ValueError:
            self.context.logger.error(
                'String pattern is None.'
                ' Please provide a valid pattern to locate the element and to perform an action.')
            raise ValueError

        except Exception as ex:
            self.context.logger.error(f'Unable to select/unselect the element {log_element}.')
            self.context.logger.exception(ex)
            raise Exception(
                f'Unable to select/unselect the element {log_element}. Error: {ex}')

    def select_dropdown(self, locator, select_by, is_select, values=None,
                        wait_state=ElementWaitState.PRESENT, timeout=None):
        """
        Select an option or list of options at the given index, value or visible text.

        :param locator: Web element or a locator string on which the action need to be performed.
        :param select_by: Method to select a dropdown value. Should be a instance of SelectMethod enum class
        :param is_select: is a boolean value True: To select , False: to deselect
        in case of multiselect dropdown.
        :param values: A list of single or multiple indices, values or visible texts
        :param wait_state: he wait state for retrial. Choose state from ElementWaitState class.
        :param timeout: wait time before throwing any exception. If None, timeout defaults to 20 seconds.
        :return: self

        USAGE:  select_dropdown('#dropdown', SelectMethod.VALUE, True, ['Option One'])\n
                select_dropdown('#dropdown', SelectMethod.VALUE, True, ['Option One', 'Option Two'])\n
                select_dropdown('#dropdown', SelectMethod.INDEX, True, [1, 2])
        """
        if values is None:
            values = []
        element_to_log = None
        try:
            if len(values) <= 0:
                raise ValueError('Please provide one or more dropdown values or indices to perform the action.')
            if locator is None:
                raise ValueError('Please provide the `Locator`string pattern or a web element to perform an action.')
            if not isinstance(select_by, SelectMethod):
                self.context.logger.error('{strategy} must be an instance of SelectStrategy'
                                          .format(strategy=repr(select_by)))
                raise TypeError('{strategy} must be an instance of SelectStrategy'
                                .format(strategy=repr(select_by)))

            element, element_to_log = (locator, locator.get_attribute('outerHTML')) \
                if isinstance(locator, WebElement) \
                else (Locator(self.context).get_element(locator, wait_state, True, timeout), locator)
            select = Select(element)
            if select_by is SelectMethod.VISIBLE_TEXT:
                self._select_by_visible_text(select, is_select, *values)
            if select_by is SelectMethod.VALUE:
                self._select_by_value(select, is_select, *values)
            if select_by is SelectMethod.INDEX:
                self._select_by_index(select, is_select, *values)
            self.context.logger.info(f'Successfully selected/deselected the item {values} on '
                                     f'the dropdown element {element_to_log}')
            return self
        # Exception Handling
        except ValueError as val_ex:
            self.context.logger.error(f'ValueError  occurred.')
            self.context.logger.exception(val_ex)
        except TypeError as tpe_ex:
            self.context.logger.error(f'TypeError occurred.')
            self.context.logger.exception(tpe_ex)
            raise TypeError
        except Exception as ex:
            self.context.logger.error(f'Unable to select/deselect the item {values} on the '
                                      f'dropdown element {element_to_log}. Error: {ex}')
            raise Exception(f'Unable to select the item {values} on the '
                            f'dropdown element {element_to_log}. Error: {ex}')

    def get_all_dropdown_options(self, locator, wait_state=ElementWaitState.PRESENT, timeout=None):
        """
        Get a list of all options belonging to this select tag.

        :param locator:  Web element or a locator string on which the action need to be performed.
        :param wait_state: he wait state for retrial. Choose state from ElementWaitState class.
        :param timeout: wait time before throwing any exception. If None, timeout defaults to 20 seconds.
        :return: Returns a list of all options belonging to this select tag
        """
        element_to_log = None
        try:
            if locator is None:
                raise ValueError('Please provide the string pattern or a web element to perform an action')

            element, element_to_log = (locator, locator.get_attribute('outerHTML')) \
                if isinstance(locator, WebElement) \
                else (Locator(self.context).get_element(locator, wait_state, True, timeout), locator)
            options = Select(element).options
            self.context.logger.info(f'Successfully retrieved {len(options)} options from the '
                                     f'dropdown element {element_to_log}')
            log_options = []
            for opt in options:
                log_options.append(opt.text)
            self.context.logger.info(f'The dropdown options are: { log_options}')
            return options
        except ValueError:
            self.context.logger.error(
                'String pattern is None.'
                ' Please provide a valid pattern to locate the element and to perform an action.')
            raise ValueError

        except Exception as ex:
            self.context.logger.error(f'Unable to get all the options from the '
                                      f'dropdown element {element_to_log}, Error: {ex}')
            self.context.logger.exception(ex)
            raise Exception(f'Unable to get all the options from the '
                            f'dropdown element {element_to_log}, Error: {ex}')

    def get_dropdown_first_option(self, locator, wait_state=ElementWaitState.PRESENT,
                            timeout=None):
        """
        Get the first dropdown option selected

        :param locator:  Web element or a locator string on which the action need to be performed.
        :param wait_state: he wait state for retrial. Choose state from ElementWaitState class.
        :param timeout: wait time before throwing any exception. If None, timeout defaults to 20 seconds.
        :return: Returns the first selected option in this select tag
         (or the currently selected option in a normal select)
        """

        element_to_log = None
        try:
            if locator is None:
                raise ValueError('Please provide the string pattern or a web element to perform an action')

            element, element_to_log = (locator, locator.get_attribute('outerHTML')) \
                if isinstance(locator, WebElement) \
                else (Locator(self.context).get_element(locator, wait_state, True, timeout), locator)
            option_text = Select(element).first_selected_option.text
            self.context.logger.info(f'Successfully performed get first selected option call on the '
                                     f'dropdown element {element_to_log}. The selected option is `{option_text}`')
            return option_text
        except ValueError:
            self.context.logger.error(
                'String pattern is None.'
                ' Please provide a valid pattern to locate the element and to perform an action.')
            raise ValueError

        except Exception as ex:
            self.context.logger.error(f'Unable to get the first selected option from the '
                                      f'dropdown element {element_to_log}.')
            self.context.logger.exception(ex)
            raise Exception(f'Unable to get the first selected option from the '
                            f'dropdown element {element_to_log}, Error: {ex}')

    def deselect_all_options_dropdown(self, locator, wait_state=ElementWaitState.PRESENT,
                                      timeout=None):
        """
        Deselect all options from multiselect.

        :param locator:  Web element or a locator string on which the action need to be performed.
        :param wait_state: he wait state for retrial. Choose state from ElementWaitState class.
        :param timeout: wait time before throwing any exception. If None, timeout defaults to 20 seconds.
        :return: self
        """
        element_to_log = None
        try:
            if locator is None:
                raise ValueError('Please provide the string pattern or a web element to perform an action')

            element, element_to_log = (locator, locator.get_attribute('outerHTML')) \
                if isinstance(locator, WebElement) \
                else (Locator(self.context).get_element(locator, wait_state, True, timeout), locator)
            Select(element).deselect_all()
            self.context.logger.info(f'Successfully deselected all the options from the'
                                     f'multiselect dropdown element {element_to_log}')
            return self
        except ValueError:
            self.context.logger.error(
                'String pattern is None.'
                ' Please provide a valid pattern to locate the element and to perform an action.')
            raise ValueError

        except Exception as ex:
            self.context.logger.error(f'Unable to deselect all options from the '
                                      f'multiselect dropdown element {element_to_log}.')
            self.context.logger.exception(ex)
            raise Exception(f'Unable to deselect all options from the '
                            f'multiselect dropdown element {element_to_log}, Error: {ex}')