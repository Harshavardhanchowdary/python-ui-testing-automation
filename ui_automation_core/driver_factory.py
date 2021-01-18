import os
import glob
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.opera import OperaDriverManager
from webdriver_manager.microsoft import IEDriverManager
from webdriver_manager.utils import os_type as get_os_type
from ui_automation_core.config.config import settings, device_config

DRIVER_VERSIONS = settings.get('driver_versions', None)


def build_headless_chrome_options():
    """
    Build the custom chrome Options

    Below config details can be found here https://peter.sh/experiments/chromium-command-line-switches/
    :return:  Chrome options
    """
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--hide-scrollbars')
    chrome_options.add_argument('--enable-logging')
    chrome_options.add_argument('--window-size=1280,1696')
    chrome_options.add_argument('--user-data-dir=/tmp/user-data')
    chrome_options.add_argument('--log-level=0')  # INFO = 0, WARNING = 1, LOG_ERROR = 2, LOG_FATAL = 3.
    chrome_options.add_argument('--v=99')
    chrome_options.add_argument('--single-process')
    chrome_options.add_argument('--data-path=/tmp/data-path')
    chrome_options.add_argument('--ignore-certificate-errors')
    chrome_options.add_argument('--homedir=/tmp')
    chrome_options.add_argument('--disk-cache-dir=/tmp/cache-dir')
    chrome_options.add_argument(
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36')
    chrome_options.binary_location = settings['chrome_headless_path']
    return chrome_options


def firefox():
    """
    Return the latest instance of Firefox Web Driver object.

    :return: Latest firefox webdriver instance
    """

    return webdriver.Firefox(executable_path=GeckoDriverManager(DRIVER_VERSIONS.get('firefox', 'latest')).install())


def chrome():
    """
    Return the latest instance of Chrome Web Driver object.

    :return: Latest Chrome webdriver instance
    """
    return webdriver.Chrome(ChromeDriverManager(DRIVER_VERSIONS.get('chrome', 'latest')).install())


def internet_explorer():
    """
    Return the latest instance of IE Web Driver object.

    :return: Latest IE webdriver instance
    """
    return webdriver.Ie(IEDriverManager(DRIVER_VERSIONS.get('ie', 'latest')).install())


def opera():
    """
    Return the latest instance of Opera Web Driver object.

    :return: Latest Opera webdriver instance
    """
    options = webdriver.ChromeOptions()
    options.add_argument('allow-elevated-browser')
    if get_os_type() == "win64" or "win32":
        paths = [f for f in glob.glob("C:\\Users\\{0}\\AppData\\Local"
                                      "\\Programs\\Opera\\"
                                      .format(os.getlogin()) + "/**",
                                      recursive=True)]
        for path in paths:
            if os.path.isfile(path) and path.endswith("opera.exe"):
                options.binary_location = path
                break
    elif ((get_os_type() == "linux64" or "linux32" or "mac64") and not
    os.path.exists('/usr/bin/opera')):
        options.binary_location = "/usr/bin/opera"
    return webdriver.Opera(executable_path=OperaDriverManager(
        DRIVER_VERSIONS.get('edge', 'latest')).install(), options=options)


def headless_firefox():
    """
    Return the latest instance of Headless Firefox Web Driver object.

    :return: Headless Firefox Web Driver object
    """
    options = webdriver.FirefoxOptions()
    options.headless = True
    return webdriver.Firefox(GeckoDriverManager(DRIVER_VERSIONS.get('firefox', 'latest')).install(),
                             firefox_options=options)


def linux_headless_chrome():
    """
    Return the latest instance of Linux Headless Chrome Web Driver object.

    :return: Linux Headless Chrome Web Driver object
    """
    return webdriver.Chrome(executable_path=settings['linux_headless_chrome'],
                            chrome_options=build_headless_chrome_options())


def no_browser():
    """
    Return  no browser string.

    :return: "no browser"
    """
    return "no browser"


def local_instance(browser):
    """
    Returns the browser object based on the browser provided
    
    :param browser: browser name whose webdriver object need to be obtained
    :return: webdriver object
    """
    switcher = {
        "firefox": firefox,
        "chrome": chrome,
        "ie": internet_explorer,
        "opera": opera,
        "headless_firefox": headless_firefox,
        "linux_headless_chrome": linux_headless_chrome,
        "no_browser": no_browser
    }
    try:
        if browser not in switcher:
            print('Not found')
            raise LookupError("Unsupported browser name: %s" % browser)
        func = switcher.get(browser, switcher.get('chrome'))
        return func()
    except Exception as ex:
        raise ex


def set_device_dimensions(driver, device='default'):
    """
    Sets browser to provided device width and height.

    :param driver: Web driver object
    :param device: device dimensions. It is set to maximize_window by default.

    """
    try:
        if device not in device_config:
            raise LookupError(f"Invalid device name: {device}")
        if device == 'default':
            driver.maximize_window()
        else:
            device_dimensions = device_config[device]
            driver.set_window_size(device_dimensions['width'], device_dimensions['height'])
    except Exception as ex:
        raise ex


def get_driver(browser, device, runner_instance, remote_server=None):
    """
    Gets the webdriver by setting the device dimensions based on the provided inputs.

    :param browser: Test execution browser name.
    :param runner_instance: To run locally or on remote server
    :param device: Device name to set the browser dimensions.
    :param remote_server: To run locally or on remote server
    :return: Web driver object
    """
    if runner_instance == 'local':
        web_driver = local_instance(browser)
    elif runner_instance == 'remote':
        try:
            if browser not in settings:
                raise LookupError(f"Unsupported browser name: {browser}")
            desired_cap = settings[browser]
            web_driver = webdriver.Remote(command_executor=f'http://{remote_server}:4444/wd/hub',
                                          desired_capabilities=desired_cap)
        except Exception as ex:
            raise ex
    else:
        raise LookupError(f"Unknown runner instance: {runner_instance}")

    set_device_dimensions(web_driver, device)
    return web_driver
