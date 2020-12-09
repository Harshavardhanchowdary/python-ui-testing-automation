import re

from selenium.webdriver.common.by import By

# default_wait = 30
id_regex = re.compile(r'^([#])(.+)')
xpath_regex = re.compile(r'^[\\/].+|^[(].+')
class_regex = re.compile(r'^([.])(.+)')
link_text_regex = re.compile(r'^([@])(.+)')
partial_link_text_regex = re.compile(r'^([@])(.*)([@])$')
tag_regex = re.compile(r'^([<])(.*)([>])$')
css_regex = re.compile(r'^([c][s][s][=])(.*)')
name_regex = re.compile(r'^([\[])(.*)[]]$')


def get_locator(locator_pattern):
    locator_string = None
    if id_regex.search(locator_pattern) is not None:
        return By.ID, id_regex.search(locator_pattern).group(2)
    elif xpath_regex.search(locator_pattern) is not None:
        return By.XPATH, xpath_regex.search(locator_pattern).group()
    elif class_regex.search(locator_pattern) is not None:
        return By.CLASS_NAME, class_regex.search(locator_pattern).group(2)
    elif partial_link_text_regex.search(locator_pattern) is not None:
        return By.PARTIAL_LINK_TEXT, partial_link_text_regex.search(locator_pattern).group(2)
    elif link_text_regex.search(locator_pattern) is not None:
        return By.LINK_TEXT, link_text_regex.search(locator_pattern).group(2)
    elif tag_regex.search(locator_pattern) is not None:
        return By.TAG_NAME, tag_regex.search(locator_pattern).group(2)
    elif css_regex.search(locator_pattern) is not None:
        return By.CSS_SELECTOR, css_regex.search(locator_pattern).group(2)
    elif name_regex.search(locator_pattern) is not None:
        return By.NAME, name_regex.search(locator_pattern).group(2)

    return locator_string


print(get_locator('[test]'))
