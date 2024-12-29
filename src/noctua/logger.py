import logging
import os
import time


class Logger:
    """
    This Logger class manages both console and file logging for the Noctua application.
    Logs are directed to the console by default and can be saved to a file in the 'result'
    directory if enabled.
    """

    def __init__(self, log_to_file=False, log_directory="result", logger_name="Noctua"):
        """
        Initializes the Logger instance, setting up both console and optional file logging.

        Args:
            log_to_file (bool): Enables logging to a file if set to True.
            log_directory (str): The directory where log files will be saved.
            logger_name (str): Identifier for the logger instance.
        """
        self.logger = logging.getLogger(logger_name)
        self.logger.setLevel(logging.DEBUG)

        self.log_format = logging.Formatter(
            "%(asctime)s - %(levelname)s - %(message)s [File: %(filename)s, Line: %(lineno)d]"
        )

        if not self.logger.hasHandlers():
            self._setup_console_logging()

        if log_to_file:
            self._enable_file_logging(log_directory)

    def _setup_console_logging(self):
        """
        Configures console logging to output logs directly to the terminal.
        """
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(self.log_format)
        self.logger.addHandler(console_handler)

    def _enable_file_logging(self, log_directory):
        """
        Activates file logging in the specified directory, creating a timestamped log file.

        Args:
            log_directory (str): Directory where the log file will be saved.
        """
        os.makedirs(log_directory, exist_ok=True)
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        log_filename = os.path.join(log_directory, f"noctua_log_{timestamp}.log")

        file_handler = logging.FileHandler(log_filename)
        file_handler.setFormatter(self.log_format)
        self.logger.addHandler(file_handler)

    def info(self, log_message):
        """
        Logs an informational message.

        Args:
            log_message (str): The informational message to log.
        """
        self.logger.info(log_message)

    def warning(self, log_message):
        """
        Logs a warning message.

        Args:
            log_message (str): The warning message to log.
        """
        self.logger.warning(log_message)

    def error(self, log_message, include_exception_info=False):
        """
        Logs an error message, with optional exception details.

        Args:
            log_message (str): The error message to log.
            include_exception_info (bool): If True, includes traceback details in the log.
        """
        self.logger.error(log_message, exc_info=include_exception_info)

    def debug(self, log_message):
        """
        Logs a debug message.

        Args:
            log_message (str): The debug message to log.
        """
        self.logger.debug(log_message)

    @staticmethod
    def setup_logging(log_to_file=False, log_directory="result"):
        """
        Sets up and returns a Logger instance with optional file logging.

        Args:
            log_to_file (bool): Enables logging to a file if True.
            log_directory (str): Directory for storing log files.

        Returns:
            Logger: A configured instance of the Logger class.
        """
        return Logger(log_to_file=log_to_file, log_directory=log_directory)
