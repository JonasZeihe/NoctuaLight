"""
Motherboard Module for fetching motherboard related information (Light version).

This module defines the Motherboard class that uses the WMI library
to gather and return only summarized information about the motherboard.
"""

import logging
import wmi


class Motherboard:
    """Class representing the Motherboard component (Light version)."""

    def __init__(self, logger: logging.Logger):
        """
        Initialize the Motherboard class with a logger.

        Args:
            logger (logging.Logger): Logger instance for logging.
        """
        self.logger = logger
        self.wmi = wmi.WMI()

    def get_summary(self) -> str:
        """
        Fetch a summary of the motherboard information.

        Returns:
            str: Summary of the motherboard information.
        """
        try:
            self.logger.info("Fetching motherboard summary (Light version)")
            return self._fetch_motherboard_summary()
        except wmi.x_wmi:
            self.logger.error("Failed to fetch motherboard summary", exc_info=True)
            return "**Motherboard Information**\nFailed to fetch motherboard summary.\n"
        except Exception:
            self.logger.error("An unexpected error occurred", exc_info=True)
            return "**Motherboard Information**\nAn unexpected error occurred.\n"

    def get_details(self) -> str:
        """
        No detailed information is provided in the Light version.

        Returns:
            str: Empty string as detailed information is not available.
        """
        return ""

    def _fetch_motherboard_summary(self) -> str:
        """
        Internal method to fetch motherboard summary.

        Returns:
            str: Summary of the motherboard's key details.
        """
        try:
            summary = ""
            for board in self.wmi.Win32_BaseBoard():
                summary += (
                    f"**Manufacturer:** {board.Manufacturer}\n"
                    f"**Product:** {board.Product}\n"
                )
            return summary if summary else "**Motherboard Information**\nNo data available.\n"
        except wmi.x_wmi:
            self.logger.error("Failed to fetch motherboard summary", exc_info=True)
            return "**Failed to fetch motherboard summary**"
        except Exception:
            self.logger.error("An unexpected error occurred", exc_info=True)
            return "**An unexpected error occurred**"
