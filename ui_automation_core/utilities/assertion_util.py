from hamcrest import *


class Assert:
    """
    Assert class holds the Wrapper functions on top of hamcrest assertions.
    require logger object to logg

    USAGE: Assert(context).assert_true(1==1)
    """

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

    def assert_ends_with(self, actual, exp_end_string, message=None):
        """
    This matcher first checks whether the evaluated object is a string.
    If so, it checks if string matches the ending characters of the evaluated object.


        :param actual: String to be inspected.
        :param exp_end_string: The string expected to be the end of actual string
        :param message: Error message to be displayed on failure.
        :return: None
        """
        self.context.logger.info(f'Trying to check if string '
                                 f'matches the ending characters of the evaluated string object .')
        try:
            assert_that(actual, ends_with(exp_end_string), message)
            self.context.logger.info(f'Assertion Successful.')
        except AssertionError as ex:
            self.context.logger.error(f'Assertion failure!!')
            self.context.logger.exception(ex)
            raise ex

    def assert_starts_with(self, actual, exp_start_string, message=None):
        """
    This matcher first checks whether the evaluated object is a string.
    If so, it checks if string matches the strting characters of the evaluated object.


        :param actual: String to be inspected.
        :param exp_start_string: The string expected to be the start of actual string
        :param message: Error message to be displayed on failure.
        :return: None
        """
        self.context.logger.info(f'Trying to check if string '
                                 f'matches the starting characters of the evaluated string object .')
        try:
            assert_that(actual, starts_with(exp_start_string), message)
            self.context.logger.info(f'Assertion Successful.')
        except AssertionError as ex:
            self.context.logger.error(f'Assertion failure!!')
            self.context.logger.exception(ex)
            raise ex

    def assert_greater_than(self, item, value, message="Object is NOT greater than a given value."):
        """
        Matches if object is greater than a given value.

        :param item: The object to be matched
        :param value: The numeric value to be compared against.
        :param message: Error message to be displayed on failure.
        :return: None
        """
        self.context.logger.info(
            f'Trying to assert if the given object `{item}` is greater than a given value `{value}`.')
        try:
            assert_that(item, greater_than(value), message)
            self.context.logger.info(f'Assertion Successful.')
        except AssertionError as ex:
            self.context.logger.error(f'Assertion failure!!')
            self.context.logger.exception(ex)
            raise ex

    def assert_greater_than_or_equal_to(self, item, value, message="Object is NOT greater than or equal to"
                                                                   " a given value."):
        """
        Matches if object is greater than or equal to a given value.

        :param item: The object to be matched
        :param value: The numeric value to be compared against.
        :param message: Error message to be displayed on failure.
        :return: None
        """
        self.context.logger.info(
            f'Trying to assert if `{item}` is greater than or equal to `{value}`.')
        try:
            assert_that(item, greater_than_or_equal_to(value), message)
            self.context.logger.info(f'Assertion Successful.')
        except AssertionError as ex:
            self.context.logger.error(f'Assertion failure!!')
            self.context.logger.exception(ex)
            raise ex

    def assert_less_than(self, item, value, message="Object is NOT less than a given value."):
        """
        Matches if object is less than a given value.

        :param item: The object to be matched
        :param value: The numeric value to be compared against.
        :param message: Error message to be displayed on failure.
        :return: None
        """
        self.context.logger.info(f'Trying to assert if `{item}` is less than `{value}`.')
        try:
            assert_that(item, less_than(value), message)
            self.context.logger.info(f'Assertion Successful.')
        except AssertionError as ex:
            self.context.logger.error(f'Assertion failure!!')
            self.context.logger.exception(ex)
            raise ex

    def assert_less_than_or_equal_to(self, item, value, message="Object is NOT less than or equal to"
                                                                " a given value ."):
        """
        Matches if object is less than or equal to a given value.

        :param item: The object to be matched
        :param value: The numeric value to be compared against.
        :param message: Error message to be displayed on failure.
        :return: None
        """
        self.context.logger.info(
            f'Trying to assert if `{item}` is less than or equal to `{value}`.')
        try:
            assert_that(item, less_than_or_equal_to(value), message)
            self.context.logger.info(f'Assertion Successful.')
        except AssertionError as ex:
            self.context.logger.error(f'Assertion failure!!')
            self.context.logger.exception(ex)
            raise ex

    def assert_close_to(self, item, value, delta, message="Object is NOT close to"
                                                          " a given value, within a given delta."):
        """
        Matches if object is a number close to a given value, within a given delta.

        :param item: The object to be matched
        :param value: The numeric value to be compared against.
        :param delta: The maximum delta between the values for which the numbers are considered close.
        :param message: Error message to be displayed on failure.
        :return: None
        """
        self.context.logger.info(f'Trying to assert `{item}` is close to '
                                 f'`{value}`, within a given delta `{delta}`.')
        try:
            assert_that(item, close_to(value, delta), message)
            self.context.logger.info(f'Assertion Successful.')
        except AssertionError as ex:
            self.context.logger.error(f'Assertion failure!!')
            self.context.logger.exception(ex)
            raise ex

    def assert_matches_regexp(self, actual, pattern, message="String does NOT match the given regular expression"):
        """
        Verifies string matches a regular expression.

        :param actual: The string to be inspected.
        :param pattern: The regular expression to search for.
        :param message: Error message to be displayed on failure.
        :return: None
        """
        self.context.logger.info(f'Trying to assert `{actual}` string matches `{pattern}` regex pattern.')
        try:
            assert_that(actual, matches_regexp(pattern), message)
            self.context.logger.info(f'Assertion Successful.')
        except AssertionError as ex:
            self.context.logger.error(f'Assertion failure!!')
            self.context.logger.exception(ex)
            raise ex

    def assert_is_empty(self, item, message="The collection is NOT empty."):
        """
         Verifies that a collection is empty.
        This matcher matches any collection-like object that responds to the __len__ method, and has a length of 0.

        :param item: The collection to be inspected.
        :param message: Error message to be displayed on failure.
        :return: None
        """
        self.context.logger.info(f'Trying to assert that a collection is empty.')

        try:
            assert_that(item, empty(), message)
            self.context.logger.info(f'Assertion Successful.')
        except AssertionError as ex:
            self.context.logger.error(f'Assertion failure!!')
            self.context.logger.exception(ex)
            raise ex

    def assert_contains_inanyorder_sequence(self, actual_sequence, items,
                                            message="The list of objects does NOT match the "
                                                    "entire sequence in any order"):
        """
        Verify that the list of objects  match the entire sequence in any order.

        :param actual_sequence: The sequence to be inspected.
        :param items: The list of objects to compare against.
        :param message: Error message to be displayed on failure.
        :return: None

        USAGE: my_list=[1, 2, 3, 4]
               assert_contains_inanyorder_sequence(my_list, [4, 2, 1, 3])
        """
        self.context.logger.info(
            f'Trying to assert if the list of objects exactly match the entire sequence in any order.')
        try:
            assert_that(actual_sequence, contains_inanyorder(*items), message)
            self.context.logger.info(f'Assertion Successful.')
        except AssertionError as ex:
            self.context.logger.error(f'Assertion failure!!')
            self.context.logger.exception(ex)
            raise ex

    def assert_has_item(self, actual_sequence, item, message="The given item is NOT displayed in the sequence"):
        """
        Verify if the given item is displayed in the sequence.

        :param actual_sequence:  The sequence to be checked
        :param item:  The value to be checked in the sequence.
        :param message: Error message to be displayed on failure.
        :return: None

        USAGE: my_list=[1, 2, 3, 4]
               assert_has_item(my_list, 4)
        """
        self.context.logger.info(
            f'Trying to assert if the given item `{item}` present in the sequence `{actual_sequence}`.')
        try:
            assert_that(actual_sequence, has_item(item), message)
            self.context.logger.info(f'Assertion Successful.')
        except AssertionError as ex:
            self.context.logger.error(f'Assertion failure!!')
            self.context.logger.exception(ex)
            raise ex

    def assert_has_items(self, actual_sequence, items, message="The given items is NOT displayed in the sequence."):
        """
        Verify if the given items is displayed in the sequence.

        :param actual_sequence:  The sequence to be checked
        :param items:  The values to be checked in the sequence.
        :param message: Error message to be displayed on failure.
        :return: None

        USAGE: my_list=[1, 2, 3, 4]
               assert_has_items(my_list, [4, 1])
        """
        self.context.logger.info(
            f'Trying to assert if the given items `{items}` present in the sequence `{actual_sequence}`.')
        try:
            assert_that(actual_sequence, has_items(*items), message)
            self.context.logger.info(f'Assertion Successful.')
        except AssertionError as ex:
            self.context.logger.error(f'Assertion failure!!')
            self.context.logger.exception(ex)
            raise ex

    def assert_has_entry(self, dict_collection, key_match, value_match,
                         message="Dictionary collection does NOT contains a given key-value pair."):
        """
        Verify that a dictionary collection contains a given key-value pair.

        :param dict_collection: The dictionary collection to be inspected.
        :param key_match: The dictionary key.
        :param value_match: The dictionary value.
        :param message: Error message to be displayed on failure.
        :return: None

        Usage: my_dic= {'foo':1, 'bar':2}
            assert_has_entry(my_dic, 'foo', 1)
        """
        self.context.logger.info(
            f'Trying to assert if dictionary collection `{dict_collection}` '
            f'contains a given key-value pair `{key_match + ":" + str(value_match)}`.')
        try:
            assert_that(dict_collection, has_entry(key_match, value_match), message)
            self.context.logger.info(f'Assertion Successful.')
        except AssertionError as ex:
            self.context.logger.error(f'Assertion failure!!')
            self.context.logger.exception(ex)
            raise ex

    def assert_has_entries(self, dict_collection, dict_expected):
        """
        Verify that a dictionary collection contains a list of given key-value pairs.

        :param dict_collection:
        :param dict_expected: A dictionary mapping to associated value matchers.
        :return: None

        USAGE: my_dic= {'foo':1, 'bar':2}
                assert_has_entries(my_dic, {'foo':1, 'bar':2})
        """
        self.context.logger.info(
            f'Trying to assert if dictionary collection `{dict_collection}` '
            f'contains a given key-value pair `{dict_expected}`.')
        try:
            assert_that(dict_collection, has_entries(dict_expected))
            self.context.logger.info(f'Assertion Successful.')
        except AssertionError as ex:
            self.context.logger.error(f'Assertion failure!!')
            self.context.logger.exception(ex)
            raise ex

    def assert_has_key(self, dict_collection, key_match, message="The dictionary collection does NOT "
                                                                 "contains the given key entry."):
        """
        Verify that a dictionary collection contains the given key entry.

        :param dict_collection: The dictionary to be inspected.
        :param key_match: The dictionary key.
        :param message: Error message to be displayed on failure.
        :return: None

        USAGE: my_dic= {'foo':1, 'bar':2}
            assert_has_key(my_dic, 'foo')
        """
        self.context.logger.info(
            f'Trying to assert if dictionary collection `{dict_collection}` '
            f'contains a given key `{key_match}`.')
        try:
            assert_that(dict_collection, has_key(key_match), message)
            self.context.logger.info(f'Assertion Successful.')
        except AssertionError as ex:
            self.context.logger.error(f'Assertion failure!!')
            self.context.logger.exception(ex)
            raise ex

    def assert_has_value(self, dict_collection, value_match, message=None):
        """
        Verify that a dictionary collection contains the given value entry.

        :param dict_collection: The dictionary to be inspected.
        :param value_match: The dictionary value.
        :param message: Error message to be displayed on failure.
        :return: None

        USAGE: my_dic= {'foo':1, 'bar':2}
            assert_has_key(my_dic, 'foo')
        """
        self.context.logger.info(
            f'Trying to assert if dictionary collection `{dict_collection}` '
            f'contains a given value `{str(value_match)}`.')
        try:
            assert_that(dict_collection, has_value(value_match), message)
            self.context.logger.info(f'Assertion Successful.')
        except AssertionError as ex:
            self.context.logger.error(f'Assertion failure!!')
            self.context.logger.exception(ex)
            raise ex