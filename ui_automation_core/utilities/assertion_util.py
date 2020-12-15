from hamcrest import *


class Assert:

    def __init__(self, context):
        self.context = context

    def assert_true(self, condition, message='Condition does not evaluate to True.'):
        """
        Verify that the condition is True.

        :param condition: Condition to be evaluated
        :param message: Error message to be displayed on failure.
        """
        self.context.logger.info(f'Trying to assert if the given condition is TRUE.')
        try:
            assert_that(condition, equal_to(True), message)
            self.context.logger.info(f'Assertion Successful.')
        except AssertionError as ex:
            self.context.logger.error(f'Assertion failure!!')
            self.context.logger.exception(ex)
            raise ex

    def assert_false(self, condition, message='Condition does not evaluate to False.'):
        """
        Verify that the condition is False.

        :param condition: Condition to be evaluated
        :param message: Error message to be displayed on failure.
        """
        self.context.logger.info(f'Trying to assert if the given condition is FALSE.')
        try:
            assert_that(condition, equal_to(False), message)
            self.context.logger.info(f'Assertion Successful.')
        except AssertionError as ex:
            self.context.logger.error(f'Assertion failure!!')
            self.context.logger.exception(ex)
            raise ex

    def assert_equals(self, actual, expected, ignore_case=False, ignore_whitespace=False,
                      message='The expected object is NOT equal to the given object.'):
        """
        Matches if object is equal to a given object.

        :param actual: The value to be compared against.
        :param expected: the value to be compared with
        :param ignore_case: Set to False by default, If wants to ignore case Set it to True
        :param ignore_whitespace: Set to False by default, If wants to ignore whitespace Set it to True
        :param message: Error message to be displayed on failure.
        """
        self.context.logger.info(f'Trying to assert if the given values are equal.  Actual Value: `{actual}`,'
                                 f' Expected Value: `{expected}`.')
        try:
            if ignore_case:
                assert_that(actual, equal_to_ignoring_case(expected), message)
                self.context.logger.info(f'Assertion Successful, Object matched by ignoring case.')
            elif ignore_whitespace:
                assert_that(actual, equal_to_ignoring_whitespace(expected), message)
                self.context.logger.info(f'Assertion Successful, Object matched by ignoring whitespace.')
            else:
                assert_that(actual, equal_to(expected), message)
                self.context.logger.info(f'Assertion Successful.')
        except AssertionError as ex:
            self.context.logger.error(f'Assertion failure!!')
            self.context.logger.exception(ex)
            raise ex

    def assert_not_equals(self, actual, expected, message="The expected object is equal to the given object."):
        """
        Matches if object is NOT equal to a given object.

        :param actual: The value to be compared against.
        :param expected: the value to be compared with
        :param message: Error message to be displayed on failure.
        """
        self.context.logger.info(f'Trying to assert if the given values are NOT equal. Actual Value: `{actual}`,'
                                 f' Expected Value: `{expected}`.')
        try:
            assert_that(actual, is_not(equal_to(expected)), message)
            self.context.logger.info(f'Assertion Successful.')
        except AssertionError as ex:
            self.context.logger.error(f'Assertion failure!!')
            self.context.logger.exception(ex)
            raise ex

    def assert_contains_string(self, actual_string, substring, message="The main string does not contain substring."):
        """
        Matches if object is a string containing a given string.

        :param actual_string: The string to be inspected.
        :param substring: The string to search for
        :param message: Error message to be displayed on failure.
        :return:
        """
        self.context.logger.info(f'Trying to assert if the given substring `{substring}` present in `{actual_string}`.')
        try:
            assert_that(actual_string, contains_string(substring), message)
            self.context.logger.info(f'Assertion Successful.')
        except AssertionError as ex:
            self.context.logger.error(f'Assertion failure!!')
            self.context.logger.exception(ex)
            raise ex

    def assert_none(self, item, message='Provided object is NOT None.'):
        """
        Matches if object is None

        :param item: Object to be inspected.
        :param message: Error message to be displayed on failure.
        :return: None
        """
        self.context.logger.info(f'Trying to assert if the given object is None.')
        try:
            assert_that(item, none(), message)
            self.context.logger.info(f'Assertion Successful.')
        except AssertionError as ex:
            self.context.logger.error(f'Assertion failure!!')
            self.context.logger.exception(ex)
            raise ex

    def assert_not_none(self, item, message='Provided object is None.'):
        """
        Matches if object is None

        :param item: Object to be inspected.
        :param message: Error message to be displayed on failure.
        :return: None
        """
        self.context.logger.info(f'Trying to assert if the given object is NOT None.')
        try:
            assert_that(item, not_none(), message)
            self.context.logger.info(f'Assertion Successful.')
        except AssertionError as ex:
            self.context.logger.error(f'Assertion failure!!')
            self.context.logger.exception(ex)
            raise ex
