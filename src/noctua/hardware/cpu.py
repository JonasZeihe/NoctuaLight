"""
CPU Module for fetching CPU-related information (Light version).

This module defines the CPU class that uses psutil and cpuinfo to gather
basic CPU details. Detailed information is omitted in NoctuaLight.
"""

import logging
import psutil
import cpuinfo


class CPU:
    """Class representing the CPU component (Light version)."""

    def __init__(self, logger: logging.Logger):
        """
        Initialize the CPU class with a logger.

        Args:
            logger (logging.Logger): Logger instance for logging.
        """
        self.logger = logger
        self.cpu_info = cpuinfo.get_cpu_info()

    def get_summary(self) -> str:
        """
        Fetch a short summary of the CPU information.

        Returns:
            str: Summary of the CPU (Name, Cores, Threads, Frequency, Architecture).
        """
        self.logger.info("Fetching CPU summary (Light version).")

        name = self._get_cpu_name()
        cores = self._get_cores_count()
        threads = self._get_threads_count()
        arch = self._get_architecture()

        # Wir können optional psutil.cpu_freq() verwenden, um den aktuellen CPU-Takt auszulesen.
        freqs = psutil.cpu_freq()
        frequency_mhz = f"{freqs.current:.1f}" if freqs else "Unknown"

        return (
            f"**Name:** {name}\n"
            f"**Cores:** {cores}\n"
            f"**Threads:** {threads}\n"
            f"**Base Frequency:** {frequency_mhz} MHz\n"
            f"**Architecture:** {arch}\n"
        )

    def get_details(self) -> str:
        """
        In NoctuaLight, detailed CPU information is not provided.
        """
        return ""

    # -------------------------------------------------------
    # Internal helper methods for the short summary
    # -------------------------------------------------------

    def _get_cpu_name(self) -> str:
        """
        Fetch the CPU brand/name from cpuinfo.
        """
        self.logger.debug("Fetching CPU name")
        return self.cpu_info.get("brand_raw", "Unknown")

    def _get_architecture(self) -> str:
        """
        Fetch the CPU architecture from cpuinfo (e.g. x86_64, ARM).
        """
        self.logger.debug("Fetching CPU architecture")
        return self.cpu_info.get("arch", "Unknown")

    def _get_cores_count(self) -> int:
        """
        Fetch the number of physical CPU cores.
        """
        self.logger.debug("Fetching CPU cores count")
        return psutil.cpu_count(logical=False)

    def _get_threads_count(self) -> int:
        """
        Fetch the total number of logical processors/threads.
        """
        self.logger.debug("Fetching CPU threads count")
        return psutil.cpu_count(logical=True)
