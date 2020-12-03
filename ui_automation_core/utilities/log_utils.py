import logging
import os
from logging.config import dictConfig

from ui_automation_core.utilities.log_config import log_config


class LogUtils:

    def __init__(self, log_dir):
        self.log_dir = log_dir
        self.log_file = None

    def __repr__(self):
        return f'An instance of LogUtils is created and ' \
               f'`{self.log_dir.split("/")[-2:-1:][0]}` folder is created.'


    def create_log_directory(self):
        """
        Creates a logging directory based on the folder name or Path provided during class instantiation,
        if log directory does not exist.
        """
        if not os.path.exists(self.log_dir):
            print(f"Trying to create a logs directory at: {self.log_dir}")
            os.makedirs(self.log_dir)
            print(f"Directory {self.log_dir} Created")
        else:
            print(f"Directory {self.log_dir}  already exists")

    @staticmethod
    def remove_handlers():
        """
        Removes all existing handlers
        """
        for handler in logging.root.handlers[:]:
            logging.root.removeHandler(handler)

    def setup_logging(self, log_file: str):
        """Use the LOG_SETTINGS defined above and initialize the logger
        :return: None
        """
        self.log_file = self.log_dir + log_file
        self.create_log_directory()
        self.remove_handlers()
        dictConfig(self.log_settings())

    @staticmethod
    def setup_formatted_logging(context):
        """
        Sets Up Formatted logger which includes Log Level, Time Stamp, File Name, Function Name and Message
            Ex: [INFO] : 2020-12-02 12:02:59,895 : test.py : setUp:16 : Message
        :param: Holds contextual information
        :return: None
        """
        context.logger = logging.getLogger('formatted_log')
        print(f'Formatted logging setup is complete')

    @staticmethod
    def setup_unformatted_logging(context):
        """Unformatted logging doesn't include file name, timestamp and/or log levels
        :param : Holds contextual information
        :return: None
        """
        context.logger = logging.getLogger('unformatted_log')

    def read_log_file(self):
        """ To read the file log
        Ex: Message
        :param  : None
        :return : log information
        """
        with open(self.log_file, "r") as f:
            return f.read()

    def log_settings(self):
        print("Log file set to " + self.log_file)
        return log_config(self.log_file)
