

def log_config(log_file):
    """
    Provides the log configurations
    :param log_file: where the logs should be writen to
    :return: log config
    """
    return {
            'version': 1,
            'disable_existing_loggers': False,
            # Handlers send the log messages to configured destinations, 'stdout' and 'file'
            'handlers': {
                'formatted_console': {
                    'class': 'logging.StreamHandler',
                    'level': 'INFO',
                    'formatter': 'verbose',
                    'stream': 'ext://sys.stdout',
                },
                'formatted_file': {
                    'class': 'logging.handlers.RotatingFileHandler',
                    'level': 'INFO',
                    'formatter': 'verbose',
                    'filename': log_file,
                    'maxBytes': 10000000,
                    'backupCount': 5,
                },
                'unformatted_console': {
                    'class': 'logging.StreamHandler',
                    'level': 'INFO',
                    'formatter': 'blank',
                    'stream': 'ext://sys.stdout',
                },
                'unformatted_file': {
                    'class': 'logging.handlers.RotatingFileHandler',
                    'level': 'INFO',
                    'formatter': 'blank',
                    'filename': log_file,
                    'maxBytes': 10000000,
                    'backupCount': 5,
                },
            },
            'formatters': {
                'verbose': {
                    'format': '[%(levelname)s] : %(asctime)s : %(filename)s : %(funcName)s:%(lineno)d : %(message)s',
                },
                'blank': {
                    'format': '',
                },
            },
            'loggers': {
                'formatted_log': {
                    'level': 'DEBUG',
                    'handlers': ['formatted_file', 'formatted_console']
                },
                'unformatted_log': {
                    'level': 'DEBUG',
                    'handlers': ['unformatted_file', 'unformatted_console']
                },
            }
        }

