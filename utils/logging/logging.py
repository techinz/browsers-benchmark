import logging


def setup_logging():
    # log format
    log_format = '%(asctime)s - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s'
    date_format = '%Y-%m-%d %H:%M:%S'
    formatter = logging.Formatter(fmt=log_format, datefmt=date_format)

    # root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)

    # setup console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    root_logger.addHandler(console_handler)

    # disable debug logging for specific libraries to reduce noise
    no_debug_loggers = ['asyncio']
    for lib in no_debug_loggers:
        lib_logger = logging.getLogger(lib)
        lib_logger.setLevel(logging.INFO)
