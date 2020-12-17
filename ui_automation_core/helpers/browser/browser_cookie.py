# Name   : BrowserCookie.py
# Author : Harshavardhan (HK)
# Time    : 03/12/2020 12:45 pm
# Desc: BrowserCookie holds all the methods to manipulate cookies

class BrowserCookie:
    def __init__(self, context):
        self.context = context

    def delete_all_cookies(self):
        """
        Delete all cookies in the scope of the session.
        """
        try:
            self.context.driver.delete_all_cookies()
            self.context.logger.info(
                'Successfully deleted all cookies of all windows.')
        except Exception as ex:
            self.context.logger.error('Unable to delete all cookies of all windows.')
            self.context.logger.exception(ex)
            raise Exception(
                f'Unable to delete all cookies of all windows. Error: {ex}')

    def delete_a_cookie(self, cookie_name: str):
        """
        Deletes a single cookie with the given name.
        :param cookie_name: name of the cookie to be deleted
        :return: none
        Usage
        driver.delete_cookie(‘my_cookie’)
        """
        try:
            self.context.driver.delete_cookie(cookie_name)
            self.context.logger.info(
                f'Successfully deleted a cookie. Cookie:{cookie_name}')
        except Exception as ex:
            self.context.logger.error('Unable to deleted a cookie. Cookie:{cookie_name}')
            self.context.logger.exception(ex)
            raise Exception(
                f'Unable to deleted a cookie. Cookie:{cookie_name} Error: {ex}')

    def add_a_cookie(self, cookie_dict: dict):
        """
        Adds a cookie to your current session.
        :param cookie_dict: A dictionary object, with required keys - “name” and “value”;
                            optional keys - “path”, “domain”, “secure”, “expiry”
        :return: none

        Usage:
            driver.add_cookie({‘name’ : ‘foo’, ‘value’ : ‘bar’})
            driver.add_cookie({‘name’ : ‘foo’, ‘value’ : ‘bar’, ‘path’ : ‘/’})
            driver.add_cookie({‘name’ : ‘foo’, ‘value’ : ‘bar’, ‘path’ : ‘/’, ‘secure’:True})
        """
        try:
            self.context.driver.add_cookie(cookie_dict)
            self.context.logger.info(
                f'Successfully added a cookie {cookie_dict["name"]}:{cookie_dict["value"]}.')
        except Exception as ex:
            self.context.logger.error(f'Unable to add a cookie {cookie_dict["name"]}:{cookie_dict["value"]}.')
            self.context.logger.exception(ex)
            raise Exception(
                f'Unable to deleted a cookie{cookie_dict["name"]}:{cookie_dict["value"]}. Error: {ex}')

    def get_a_cookie(self, name: str):
        """
        Get a single cookie by name. Returns the cookie if found, None if not.
        :param name:
        :return:  cookie if found, None if not
        Usage:	driver.get_a_cookie(‘my_cookie’)
        """

        try:
            cookie = self.context.driver.get_cookie(name)
            self.context.logger.info(
                f'Successfully retrieved a cookie {name}.')
            return cookie
        except Exception as ex:
            self.context.logger.error(f'Unable to retrieve a cookie {name}.')
            self.context.logger.exception(ex)
            raise Exception(
                f'Unable to retrieve a cookie {name}. Error: {ex}')

    def get_all_cookies(self)->dict:
        """
        Returns a set of dictionaries, corresponding to cookies visible in the current session.
        :return:  set of dictionaries
        Usage:	driver.get_all_cookie()
        """

        try:
            cookies = self.context.driver.get_cookies()
            self.context.logger.info(
                f'Successfully retrieved all the cookies.')
            self.context.logger.info(cookies)
            return cookies
        except Exception as ex:
            self.context.logger.error(f'Unable to retrieve all the cookies.')
            self.context.logger.exception(ex)
            raise Exception(
                f'Unable to retrieve all cookies. Error: {ex}')
