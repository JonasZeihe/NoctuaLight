import argparse
import sys
from multiprocessing import freeze_support
from noctua.logger import Logger
from noctua.noctua import Noctua


def main(entry_point_arguments=None):
    """
    Entry point for executing the Noctua application. Handles argument parsing,
    initializes the logging mechanism, and launches the Noctua application core.

    Args:
        entry_point_arguments: List of arguments for command-line execution or testing purposes.
    """
    active_logger = None
    try:
        parsed_command_line_arguments = parse_command_line_arguments(
            entry_point_arguments
        )
        is_logging_enabled = parsed_command_line_arguments.logging

        active_logger = Logger(log_to_file=is_logging_enabled)
        active_logger.debug(
            f"Parsed command-line arguments: {parsed_command_line_arguments}"
        )
        active_logger.info("Launching Noctua application instance")

        noctua_application = Noctua()
        active_logger.debug("Noctua application core initialized successfully")
        noctua_application.run()

    except Exception as execution_error:
        process_application_error(
            active_logger,
            f"An unexpected error occurred during execution: {execution_error}",
        )


def parse_command_line_arguments(entry_point_arguments=None):
    """
    Parses command-line arguments provided for the Noctua application execution.

    Args:
        entry_point_arguments: Optional list of arguments for command-line execution or testing.

    Returns:
        Namespace: Parsed command-line arguments structured as an argparse Namespace.
    """
    command_line_parser = argparse.ArgumentParser(
        description="Noctua - Comprehensive Hardware Report Generator"
    )
    command_line_parser.add_argument(
        "--logging",
        action="store_true",
        help="Enable detailed logging to file and console output.",
    )
    return command_line_parser.parse_args(entry_point_arguments)


def process_application_error(active_logger, descriptive_error_message):
    """
    Manages the handling of errors by logging or printing directly to stderr, then terminates execution.

    Args:
        active_logger: Logger instance to record the error message if available.
        descriptive_error_message: Specific error message detailing the issue encountered.
    """
    if active_logger:
        active_logger.error(descriptive_error_message)
    else:
        print(descriptive_error_message, file=sys.stderr)
    sys.exit(1)


if __name__ == "__main__":
    freeze_support()
    main()
