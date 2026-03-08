"""
Disk Module for fetching disk-related information (Light version).

Uses psutil (and optionally wmi) to gather and return minimal disk information.
"""

import logging
import psutil
import wmi

class Disk:
    """Class representing the Disk component (Light version)."""

    def __init__(self, logger: logging.Logger):
        """
        Initialize the Disk class with a logger.
        Args:
            logger (logging.Logger): Logger instance for logging.
        """
        self.logger = logger
        self.wmi = wmi.WMI()

    def get_summary(self) -> str:
        """
        Fetch a short summary of the disk information.
        
        Returns:
            str: Basic disk info (e.g. device path, total size).
        """
        try:
            self.logger.info("Fetching disk summary (Light version).")
            return self._fetch_disk_summary()
        except wmi.x_wmi:
            self.logger.error("Failed to fetch disk summary", exc_info=True)
            return "**Disk Information**\nFailed to fetch disk summary.\n"
        except Exception:
            self.logger.error("An unexpected error occurred (disk summary).", exc_info=True)
            return "**Disk Information**\nAn unexpected error occurred.\n"

    def get_details(self) -> str:
        """
        In NoctuaLight, detailed disk information is not provided.
        """
        return ""

    def _fetch_disk_summary(self) -> str:
        """
        Internal method to fetch a short disk summary for each partition.
        """
        partitions = psutil.disk_partitions()
        summary = ""
        device_counter = 0

        for partition in partitions:
            # Skip CD-ROMs or empty fstype
            if "cdrom" in partition.opts or partition.fstype == "":
                continue

            device_counter += 1
            usage = psutil.disk_usage(partition.mountpoint)
            summary += (
                f"**Device {device_counter}:**\n"
                f"- **Path:** {partition.device}\n"
                f"- **Total Size:** {self._bytes_to_gb(usage.total)} GB\n\n"
            )

        return summary if summary else "No disk partitions found."

    def _bytes_to_gb(self, bytes_value: int) -> float:
        """
        Convert bytes to gigabytes.
        """
        return round(bytes_value / (1024**3), 2)
