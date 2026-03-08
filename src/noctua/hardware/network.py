"""
Network Module for fetching basic network-related information (Light version).

This module defines the Network class that uses the psutil library
to gather and return only summarized information about the network interfaces.
"""

import logging
import psutil
import socket


class Network:
    """Class representing the Network component (Light version)."""

    def __init__(self, logger: logging.Logger):
        """
        Initialize the Network class with a logger.

        Args:
            logger (logging.Logger): Logger instance for logging.
        """
        self.logger = logger

    def get_summary(self) -> str:
        """
        Fetch a summary of the network information.

        Returns:
            str: Summary of the network interfaces and their addresses.
        """
        try:
            self.logger.info("Fetching network summary (Light version)")
            return self._fetch_network_summary()
        except Exception:
            self.logger.error("Failed to fetch network summary", exc_info=True)
            return "**Network Information**\nFailed to fetch network summary.\n"

    def get_details(self) -> str:
        """
        No detailed information is provided in the Light version.

        Returns:
            str: Empty string as detailed information is not available.
        """
        return ""

    def _fetch_network_summary(self) -> str:
        """
        Internal method to fetch network summary.

        Returns:
            str: Summary of the network interfaces and their addresses.
        """
        addrs = psutil.net_if_addrs()
        summary = ""
        for interface, addr_list in addrs.items():
            summary += f"**Interface:** {interface}\n"
            for addr in addr_list:
                addr_type = self._get_address_type(addr.family)
                if addr_type in {"IPv4", "IPv6"}:
                    summary += f"- **{addr_type}:** {addr.address}\n"
                elif addr_type == "MAC":
                    summary += f"- **MAC Address:** {addr.address}\n"
            summary += "\n"
        return summary if summary else "**Network Information**\nNo data available.\n"

    def _get_address_type(self, family: int) -> str:
        """
        Get the address type (IPv4, IPv6, MAC) based on the family.

        Args:
            family (int): Address family identifier.

        Returns:
            str: Address type as a string.
        """
        if family == socket.AF_INET:
            return "IPv4"
        if family == socket.AF_INET6:
            return "IPv6"
        if family == psutil.AF_LINK:
            return "MAC"
        return "Other"
