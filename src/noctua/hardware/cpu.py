"""
CPU Module for fetching CPU related information.

This module defines the CPU class that uses the psutil and cpuinfo libraries
to gather and return information about the CPU.
"""

import logging
import re
import psutil
import cpuinfo


class CPU:
    """Class representing the CPU component."""

    def __init__(self, logger: logging.Logger):
        """Initialize the CPU class with a logger.

        Args:
            logger (logging.Logger): Logger instance for logging.
        """
        self.logger = logger
        self.cpu_info = cpuinfo.get_cpu_info()

    def get_summary(self) -> str:
        """Fetch a summary of the CPU information.

        Returns:
            str: Summary of the CPU information.
        """
        self.logger.info("Fetching CPU summary")
        return (
            f"**Name:** {self.get_cpu_name()}\n"
            f"**Cores:** {self.get_cores_count()}\n"
            f"**Threads:** {self.get_threads_count()}\n"
            f"**Architecture:** {self.get_architecture()}\n"
        )

    def get_details(self) -> str:
        """Fetch detailed CPU information.

        Returns:
            str: Detailed CPU information.
        """
        self.logger.info("Fetching detailed CPU information")
        freqs = psutil.cpu_freq()
        caches = self._get_cache_info(self.cpu_info)
        flags = ", ".join(self.cpu_info.get("flags", []))

        return (
            f"**Name:** {self.get_cpu_name()}\n"
            f"**Vendor ID:** {self.cpu_info.get('vendor_id_raw', 'Unknown')}\n"
            f"**Architecture:** {self.cpu_info.get('arch', 'Unknown')}\n"
            f"**Bits:** {self.cpu_info.get('bits', 'Unknown')}\n"
            f"**Cores:** {self.get_cores_count()}\n"
            f"**Threads:** {self.get_threads_count()}\n"
            f"**Frequency:** {freqs.current:.1f} MHz\n"
            f"**Configured Frequency:** "
            f"{self._format_value(self.cpu_info.get('hz_advertised_friendly', 'Unknown'), freqs.current)} MHz\n"
            f"**Cache Sizes:** {caches}\n"
            f"**Flags:** {flags}\n"
        )

    def get_cpu_name(self) -> str:
        """Fetch the CPU name.

        Returns:
            str: CPU name.
        """
        self.logger.info("Fetching CPU name")
        return self.cpu_info.get("brand_raw", "Unknown")

    def get_architecture(self) -> str:
        """Fetch the CPU architecture.

        Returns:
            str: CPU architecture.
        """
        self.logger.info("Fetching CPU architecture")
        return self.cpu_info.get("arch", "Unknown")

    def get_cores_count(self) -> int:
        """Fetch the number of CPU cores.

        Returns:
            int: Number of CPU cores.
        """
        self.logger.info("Fetching CPU cores count")
        return psutil.cpu_count(logical=False)

    def get_threads_count(self) -> int:
        """Fetch the number of CPU threads.

        Returns:
            int: Number of CPU threads.
        """
        self.logger.info("Fetching CPU threads count")
        return psutil.cpu_count(logical=True)

    def _get_cache_info(self, cpu_info) -> str:
        """Fetch the CPU cache sizes.

        Args:
            cpu_info (dict): CPU information dictionary.

        Returns:
            str: Cache sizes.
        """
        cache_sizes = {
            "L1 Cache": cpu_info.get("l1_data_cache_size", "Unknown"),
            "L2 Cache": cpu_info.get("l2_cache_size", "Unknown"),
            "L3 Cache": cpu_info.get("l3_cache_size", "Unknown"),
        }
        return ", ".join([f"{key}: {value}" for key, value in cache_sizes.items()])

    def _format_value(self, expected_value: str, actual_value: float) -> str:
        """Format the value for display, showing native and actual values.

        Args:
            expected_value (str): The expected (native) value.
            actual_value (float): The actual value.

        Returns:
            str: Formatted value with native and actual values, highlighting differences.
        """
        try:
            expected_value_cleaned = float(re.findall(r"\d+\.\d+", expected_value)[0])
            if expected_value_cleaned == actual_value:
                return f"{actual_value:.1f}"
            return f"**{actual_value:.1f}**"
        except (IndexError, ValueError):
            self.logger.error(
                f"Failed to parse expected value: {expected_value}", exc_info=True
            )
            return f"**{actual_value:.1f}**"
