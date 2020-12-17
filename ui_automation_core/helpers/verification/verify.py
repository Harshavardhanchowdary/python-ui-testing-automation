import requests
from selenium.common.exceptions import NoAlertPresentException, TimeoutException
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from ui_automation_core.helpers.actions.action import Actions
from ui_automation_core.helpers.select.select import SelectAction
from ui_automation_core.helpers.web_element.locator import Locator
from ui_automation_core.helpers.web_element.wait_states import ElementWaitState


class Verify:
    def __init__(self, context):
        self.context = context

    default_timeout = 3

    # Verify Alert Not Present
    def is_alert_not_present(self, timeout=None):
        """
        Verify if alert does not present

        :param timeout: wait time before throwing any exception.
                    If None, timeout is set to default timeout.
        :return: True if alert does not present else False.
        """
        is_alert_not_present = True
        timeout = self.default_timeout if timeout is None else timeout
        try:
            WebDriverWait(self.context.driver, timeout).until(EC.alert_is_present())
            alert = self.context.driver.switch_to.alert
            if isinstance(alert, Alert):
                self.context.logger.error(
                    f'Alert is present on webpage.')
                is_alert_not_present = False
        except (NoAlertPresentException or TimeoutException) as ex:
            self.context.logger.info(f'Alert is NOT present on webpage.')

        return is_alert_not_present

    # Verify Alert Present
    def is_alert_present(self, timeout=None):
        """
        Verify if alert does present

        :param timeout: wait time before throwing any exception.
                    If None, timeout is set to default timeout.
        :return: True if alert does present else False.
        """
        is_alert_present = False
        timeout = self.default_timeout if timeout is None else timeout
        try:
            WebDriverWait(self.context.driver, timeout).until(EC.alert_is_present())
            alert = self.context.driver.switch_to.alert
            if isinstance(alert, Alert):
                self.context.logger.info(
                    f'Alert is present on webpage.')
                is_alert_present = True
        except (NoAlertPresentException or TimeoutException) as ex:
            self.context.logger.error(f'Alert is NOT present on webpage.')

        return is_alert_present

    # Verify Element Attribute Value
    def is_attribute_value(self, locator, attribute, value):
        """
        Verify if the web element has an attribute with the specified name and value.

        :param locator: web element or a locator string on which the action need to be performed.
        :param attribute: attribute with the specified name
        :param value: expected attribute value
        :return: True if the web element has an attribute with the specified name and value, else False
        """
        is_vale_equal = False
        try:
            if (locator, attribute, value) is None:
                raise ValueError('Please provide the valid parameters '
                                 '(locator, attribute, value) to perform an action.')
            actual_attribute_value = Actions(self.context).get_attribute(locator, attribute)
            if value.lower().strip() == actual_attribute_value.lower().strip():
                is_vale_equal = True
                self.context.logger.info(f'The attribute `{attribute}` the supplied value {value}.')
            else:
                self.context.logger.error(f'The attribute `{attribute}` has does not have the supplied value {value}.')
                self.context.logger.error(f'Expected value: `{value}`, but found `{actual_attribute_value}`.')
            return is_vale_equal
        except ValueError as ve_err:
            self.context.logger.error('An ValueError occurred.')
            self.context.logger.exception(ve_err)

    # Verify Element Checked
    def is_element_selected(self, locator, timeout=None):
        """
        Verify if the given web element is selected.

        :param locator: The string pattern to find the element.
        :param timeout: wait time before throwing any exception.
                    If None, timeout is set to default timeout.
        :return:True if the given web element is selected otherwise returns False.
        """

        is_selected = False
        is_web_element = isinstance(locator, WebElement)
        _ele_to_log = None
        if timeout is None:
            timeout = self.default_timeout
        try:
            _ele_to_log = locator.get_attribute('outerHTML') if is_web_element else locator

            if is_web_element:
                is_selected = locator.is_selected()
                self.context.logger.info(f'Successfully checked if the given element `{_ele_to_log}` is selected.')
            else:
                try:
                    element = Locator(self.context).get_element(locator,
                                                                ElementWaitState.SELECTED,
                                                                False,
                                                                timeout)
                    if isinstance(element, WebElement):
                        self.context.logger.info(f'The element {_ele_to_log} is already selected.')
                        is_selected = True
                except TimeoutException as t_ex:
                    self.context.logger.error(f'The element {_ele_to_log} is not selected.')
            return is_selected
        except Exception as ex:
            self.context.logger.Error(f'Unable to verify if the given element {_ele_to_log} is selected.')
            self.context.logger.exception(ex)
            raise Exception(f'Unable to verify if the given element {_ele_to_log} is selected. Error:{ex}')

    # Verify Element Clickable
    def is_element_clickable(self, locator, timeout=None):
        """
        Verify if the given element is clickable.
        :param locator: The string pattern or web element to find the element.
        :param timeout: wait time before throwing any exception.
                    If None, timeout is set to default timeout.
        :return: True if the given element is clickable otherwise False.
        """
        is_enabled = False
        is_web_element = isinstance(locator, WebElement)
        _ele_to_log = None
        try:
            _ele_to_log = locator.get_attribute('outerHTML') if is_web_element else locator

            if is_web_element:
                is_enabled = locator.is_enabled() and locator.is_displayed()
                self.context.logger.info(f'Successfully checked if the given element `{_ele_to_log}` is clickable.')
            else:
                element = Locator(self.context).get_element(locator,
                                                            ElementWaitState.CLICKABLE,
                                                            False,
                                                            timeout)
                if isinstance(element, WebElement):
                    self.context.logger.info(f'The element {_ele_to_log} is clickable.')
                    is_enabled = True
                else:
                    self.context.logger.info(f'The element {_ele_to_log} is not clickable.')
            return is_enabled
        except Exception as ex:
            self.context.logger.Error(f'Unable to verify if the given element {_ele_to_log} is clickable.')
            self.context.logger.exception(ex)
            raise Exception(f'Unable to verify if the given element {_ele_to_log} is clickable. Error:{ex}')

    def is_attribute_present(self, locator, attribute, timeout=None):
        """
        Verify if the web element has an attribute with the specified name.
        :param locator: The string pattern or web element to find the element.
        :param attribute: attribute name
        :param timeout: wait time before throwing any exception.
                    If None, timeout is set to default timeout.
        :return: True if the web element has an attribute with the specified name otherwise False
        """
        is_attr_present = False
        web_element = locator if isinstance(locator, WebElement) \
            else Locator(self.context).get_element(locator, ElementWaitState.PRESENT, False, timeout)
        element_to_log = locator if not isinstance(locator, WebElement) else locator.get_attribute('outerHTML')

        try:
            attribute_value = web_element.get_attribute(attribute)
            self.context.logger.info(
                f'Successfully retrieved the attribute with the specified name `{attribute}`'
                f' on the element `{element_to_log}`.')
            if attribute_value is not None:
                is_attr_present = True
                self.context.logger.info(
                    f'The web element `{element_to_log}` has an attribute with the specified name `{attribute}`.')
            else:
                self.context.logger.info(
                    f'The web element `{element_to_log}` NOT have an attribute with the specified name `{attribute}`.')
            return is_attr_present

        except Exception as ex:
            self.context.logger.Error(
                f'Unable to verify if the given element {element_to_log} has an attribute with the specified '
                f'name `{attribute}`.')
            self.context.logger.exception(ex)
            raise Exception(
                f'Unable to verify if the given element {element_to_log} has an attribute with the specified '
                f'name `{attribute}`. Error:{ex}')

    # Verify Element Not Visible
    def is_element_not_visible(self, locator, timeout=None):
        """
        Verify if given web element is NOT visible.
        :param locator: The string pattern to find the element.
        :param timeout: wait time before throwing any exception.
                    If None, timeout is set to default timeout.
        :return: True if given web element is NOT visible else False.
        """
        is_ele_not_invisible = True
        element = Locator(self.context).get_element(locator, ElementWaitState.INVISIBLE, False, timeout)
        if isinstance(element, WebElement) or None:
            self.context.logger.error(
                f'The given web element `{locator}` is visible on the web page.')
            is_ele_not_invisible = False
        else:
            self.context.logger.info(
                f'The given web element `{locator}` is NOT visible on the web page')

        return is_ele_not_invisible

    # Verify Element Not Present
    def is_element_not_present(self, locator, timeout=None):
        """
        Verify if the given web element does NOT present on the DOM.
        :param locator: The string pattern to find the element.
        :param timeout: wait time before throwing any exception.
                    If None, timeout is set to default timeout.
        :return: True if the given web element does NOT present on the DOM else False.
        """

        is_ele_not_present = True
        element = Locator(self.context).get_element(locator, ElementWaitState.PRESENT, False, timeout)
        if isinstance(element, WebElement):
            self.context.logger.error(f'The given element {locator} does present on DOM.')
            is_ele_not_present = False
        else:
            self.context.logger.info(
                f'The given element `{locator}` does not present on DOM.')
        return is_ele_not_present

    # Verify Element Present
    def is_element_present(self, locator, timeout=None):
        """
        Verify if the given web element does present on DOM.
        :param locator: The string pattern to find the element.
        :param timeout: wait time before throwing any exception.
                    If None, timeout is set to default timeout.
        :return: True if the element is present on DOM else False.
        """

        is_ele_present = False
        element = Locator(self.context).get_element(locator, ElementWaitState.PRESENT, False, timeout)
        if isinstance(element, WebElement):
            self.context.logger.info(f'The given element {locator} does present on DOM.')
            is_ele_present = True
        else:
            self.context.logger.error(
                f'The given element `{locator}` does not present on DOM.')
        return is_ele_present

    # Verify Element Text
    def element_text(self, locator, text, timeout=None):
        """
        Verify text of an element.

        :param locator: web element or a locator string on which the action need to be performed.
        :param text: expected text to match with element text
        :param timeout: wait time before throwing any exception.
                    If None, timeout is set to default timeout.
        :return: True if text of an element matches else False
        """
        does_match = False
        try:
            self.context.logger.info('Trying to get element text.')
            actual_text = Actions(self.context).get_web_element_inner_text(locator=locator, timeout=timeout)
            if actual_text.strip() == text.strip():
                self.context.logger.info(f'Successfully verified text of an element and the actual text `{text}` '
                                         f'matches with the expected text `{actual_text.strip()}`.')
                does_match = True
            else:
                self.context.logger.error(f'Successfully verified text of an element and the actual text `{text}` '
                                          f'does NOT matches with the expected text `{actual_text.strip()}`.')
            return does_match
        except Exception as ex:
            self.context.logger.Error(
                f'Unable to verify if all links (URLs) on the current page are accessible.')
            self.context.logger.exception(ex)
            raise Exception(
                f'Unable to verify if all links (URLs) on the current page are accessible.')

    # Verify Element Visible
    def is_element_visible(self, locator, timeout=None):
        """
        Verify if the given web element is visible.

        Criteria for visibility of an element:
            1. The element has an opacity greater than  0.
            2. There are no other elements hiding it.
            3. The element has the visibility property set to visible.
            4. The element has the display property not set none.

        :param locator: The string pattern to find the element or a web element to perform an action.
        :param timeout: wait time before throwing any exception.
                    If None, timeout is set to default timeout.
        :return: True if the given web element is visible else False.
        """
        # Set initial visibility to false
        is_ele_visible = False
        is_web_element = isinstance(locator, WebElement)
        _ele_to_log = None
        try:
            _ele_to_log = locator.get_attribute('outerHTML') if is_web_element else locator

            if is_web_element:
                # if the locator is web element
                is_ele_visible = locator.is_displayed()
                self.context.logger.info(f'Successfully checked for the visibility of the element `{_ele_to_log}`.')
            else:
                # if locator is a pattern string
                element = Locator(self.context).get_element(locator, ElementWaitState.VISIBLE, False, timeout)
                # if we find the web element
                if isinstance(element, WebElement):
                    self.context.logger.info(f'The element `{_ele_to_log}` is visible on the web page.')
                    is_ele_visible = True
                else:
                    self.context.logger.error(f'The element `{_ele_to_log}` is not visible on the web page.')
            return is_ele_visible
        except Exception as ex:
            self.context.logger.error(f'Unable to perform the visibility check on the element `{_ele_to_log}`.')
            self.context.logger.exception(ex)
            raise Exception(f'Unable to perform the visibility check on the element `{_ele_to_log}`. Error:{ex}.')

    # Verify All Links On Current Page Accessible
    def are_all_links_accessible(self):
        """
        Verify if all links (URLs) on the current page are accessible.
        :return: True if all links (URLs) on the current page are accessible else False
        """
        all_links_accessible = True
        broken_links = 0
        self.context.logger.info('Trying to obtain all the links on the web page.')
        try:
            links = Locator(self.context).get_elements('<a>')
            self.context.logger.info(f'Successfully obtained {len(links)} links on the current web page.')
            for link in links:
                link_text = link.get_attribute('href').strip()
                if link_text is not (None or ""):
                    r = requests.get(link_text)
                    self.context.logger.info(f'URL:{link_text}, Status Code: {r.status_code}.')
                    if r.status_code != 200:
                        broken_links += 1
                        all_links_accessible = False
            if all_links_accessible:
                self.context.logger.info(
                    'Successfully verified if all links (URLs) on the current page are accessible '
                    'and all the links found to be accessible.')
            else:
                self.context.logger.error(
                    f'Successfully verified if all links (URLs) on the current page are accessible'
                    f' and found {broken_links} broken links.')
            return all_links_accessible
        except Exception as ex:
            self.context.logger.error(
                f'Unable to verify if all links (URLs) on the current page are accessible.')
            self.context.logger.exception(ex)
            raise Exception(
                f'Unable to verify if all links (URLs) on the current page are accessible.')

    # Verify Options Present
    def options_present(self, locator, options, timeout=None):
        """
        Verify if all expected options are present within the given select object.
        :param locator: web element or a locator string on which the action need to be performed.
        :param options: List of expected dropdown options
        :param timeout: wait time before throwing any exception.
                    If None, timeout is set to default timeout.
        :return: True if all the options match else False
        """
        self.context.logger.info('Trying to retrieve all dropdown options.')
        is_match = False
        try:
            option_items = SelectAction(self.context).get_all_dropdown_options(locator=locator, timeout=timeout)
            actual_options = []
            for op_it in option_items:
                actual_options.append(op_it.text)
            if set(actual_options) == set(options):
                self.context.logger.info(f'Successfully matched all options. '
                                         f'Actual options: {actual_options} and Expected options:{options}.')
                is_match = True
            else:
                self.context.logger.error(f'Unable to matched all options. '
                                          f'Actual options: {actual_options} and Expected options:{options}.')
            return is_match
        except Exception as ex:
            self.context.logger.error(
                f'Unable to verify if all expected options are present within the given select object.')
            self.context.logger.exception(ex)
            raise Exception(
                f'Unable to verify if all expected options are present within the given select object.')
