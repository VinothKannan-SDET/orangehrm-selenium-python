import logging


def get_logger(name):
    """
    Create and return a configured logger instance.

    Creates a StreamHandler with a standard log format and sets
    the logger level to INFO. A handler is added only when the
    logger does not already have one to prevent duplicate logs.

    :param name: Name of the logger, usually __name__ of the calling module.
    :return: Configured logging.Logger instance.
    """

    # Step 1: Get or create a logger using the provided name
    logger = logging.getLogger(name)

    # Step 2: Check whether a handler is already configured
    # to prevent duplicate log messages
    if not logger.handlers:

        # Step 2.1: Create console/stream log handler
        handler = logging.StreamHandler()

        # Step 2.2: Define the log message format
        formatter = logging.Formatter(
            "%(asctime)s - %(levelname)s - %(message)s"
        )

        # Step 2.3: Apply the formatter to the handler
        handler.setFormatter(formatter)

        # Step 2.4: Attach the handler to the logger
        logger.addHandler(handler)

        # Step 2.5: Set logger level to INFO
        logger.setLevel(logging.INFO)

    # Step 3: Return the configured logger
    return logger