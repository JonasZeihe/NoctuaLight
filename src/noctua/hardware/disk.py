"""
Disk Module for fetching disk related information.

This module defines the Disk class that uses the psutil and wmi libraries
to gather and return information about the disk drives.
"""

import logging
import psutil
import wmi


class Disk:
    """Class representing the Disk component."""

    def __init__(self, logger: logging.Logger):
        """Initialize the Disk class with a logger."""
        self.logger = logger
        self.wmi = wmi.WMI()

    def get_summary(self) -> str:
        """Fetch a summary of the disk information."""
        try:
            self.logger.info("Fetching disk summary")
            return self._fetch_disk_summary()
        except wmi.x_wmi as wmi_error:
            self.logger.error("Failed to fetch disk summary", exc_info=True)
            return "**Disk Information**\nFailed to fetch disk summary.\n"
        except Exception:
            self.logger.error("An unexpected error occurred", exc_info=True)
            return "**Disk Information**\nAn unexpected error occurred.\n"

    def get_details(self) -> str:
        """Fetch detailed disk information."""
        try:
            self.logger.info("Fetching detailed disk information")
            return self._fetch_disk_details()
        except wmi.x_wmi:
            self.logger.error(
                "Failed to fetch detailed disk information", exc_info=True
            )
            return "**Detailed Disk Information**\nFailed to fetch detailed disk information.\n"
        except Exception:
            self.logger.error("An unexpected error occurred", exc_info=True)
            return "**Detailed Disk Information**\nAn unexpected error occurred.\n"

    def _fetch_disk_summary(self) -> str:
        """Internal method to fetch disk summary."""
        partitions = psutil.disk_partitions()
        summary = ""
        for idx, partition in enumerate(partitions, start=1):
            if "cdrom" in partition.opts or partition.fstype == "":
                continue
            summary += (
                f"**Device {idx}:**\n"
                f"- **Path:** {partition.device}\n"
                f"- **Total Size:** "
                f"{self.bytes_to_gb(psutil.disk_usage(partition.mountpoint).total)} GB\n"
                f"\n"
            )
        return summary

    def _fetch_disk_details(self) -> str:
        """Internal method to fetch detailed disk information."""
        partitions = psutil.disk_partitions()
        details = ""
        for idx, partition in enumerate(partitions, start=1):
            if "cdrom" in partition.opts or partition.fstype == "":
                continue
            usage = psutil.disk_usage(partition.mountpoint)
            details += (
                f"**Device {idx}:**\n"
                f"- **Path:** {partition.device}\n"
                f"- **Mount Point:** {partition.mountpoint}\n"
                f"- **File System Type:** {partition.fstype}\n"
                f"- **Total Size:** {self.bytes_to_gb(usage.total)} GB\n"
                f"- **Used:** {self.bytes_to_gb(usage.used)} GB\n"
                f"- **Free:** {self.bytes_to_gb(usage.free)} GB\n"
                f"- **Usage:** {usage.percent}%\n"
                f"\n"
            )
        details += self._fetch_physical_drive_details()
        return details

    def _fetch_physical_drive_details(self) -> str:
        """Fetch physical drive details using WMI."""
        details = ""
        for disk_drive in self.wmi.Win32_DiskDrive():
            size_gb = (
                self.bytes_to_gb(int(disk_drive.Size)) if disk_drive.Size else "Unknown"
            )
            details += (
                f"**Physical Drive:** {disk_drive.DeviceID}\n"
                f"- **Model:** {disk_drive.Model}\n"
                f"- **Serial Number:** {disk_drive.SerialNumber}\n"
                f"- **Size:** {size_gb} GB\n"
                f"\n"
            )
        return details

    def bytes_to_gb(self, bytes_value: int) -> float:
        """Convert bytes to gigabytes."""
        return round(bytes_value / (1024**3), 2)
