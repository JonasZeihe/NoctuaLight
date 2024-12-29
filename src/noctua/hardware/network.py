"""
Network Module for fetching network related information.

This module defines the Network class that uses the psutil and wmi libraries
to gather and return information about the network.
"""

import logging
import subprocess
import socket
import psutil
import wmi


class Network:
    """Class representing the Network component."""

    def __init__(self, logger: logging.Logger):
        """Initialize the Network class with a logger."""
        self.logger = logger
        self.wmi = wmi.WMI()

    def get_summary(self) -> str:
        """Fetch a summary of the network information."""
        try:
            self.logger.info("Fetching network summary")
            return self._fetch_network_summary()
        except Exception:
            self.logger.error("Failed to fetch network summary", exc_info=True)
            return "**Network Information**\nFailed to fetch network summary.\n"

    def get_details(self) -> str:
        """Fetch detailed network information."""
        try:
            self.logger.info("Fetching detailed network information")
            network_details = self._fetch_network_details()
            return network_details
        except Exception:
            self.logger.error(
                "Failed to fetch detailed network information", exc_info=True
            )
            return "**Detailed Network Information**\nFailed to fetch detailed network information.\n"

    def _fetch_network_summary(self) -> str:
        """Internal method to fetch network summary."""
        addrs = psutil.net_if_addrs()
        summary = ""
        for interface, addr_list in addrs.items():
            summary += f"**Interface:** {interface}\n"
            seen_hostnames = set()
            for addr in addr_list:
                addr_type = self._get_address_type(addr.family)
                if addr_type in {"IPv4", "IPv6"}:
                    try:
                        hostname = socket.gethostbyaddr(addr.address)[0]
                        if hostname not in seen_hostnames:
                            summary += (
                                f"- **{addr_type}:** {addr.address} ({hostname})\n"
                            )
                            seen_hostnames.add(hostname)
                        else:
                            summary += f"- **{addr_type}:** {addr.address}\n"
                    except socket.herror:
                        summary += f"- **{addr_type}:** {addr.address}\n"
                else:
                    summary += f"- **{addr_type}:** {addr.address}\n"
            summary += "\n"
        summary += self._fetch_network_drives_summary()
        return summary

    def _fetch_network_details(self) -> str:
        """Internal method to fetch detailed network information."""
        details = ""
        for interface, addrs in psutil.net_if_addrs().items():
            stats = psutil.net_if_stats()[interface]
            details += (
                f"**Interface:** {interface}\n"
                f"- **Status:** {'Up' if stats.isup else 'Down'}\n"
                f"- **Max Speed:** {stats.speed} Mbps\n"
                f"- **MTU:** {stats.mtu}\n"
            )
            seen_hostnames = set()
            for addr in addrs:
                addr_type = self._get_address_type(addr.family)
                if addr_type in {"IPv4", "IPv6"}:
                    try:
                        hostname = socket.gethostbyaddr(addr.address)[0]
                        if hostname not in seen_hostnames:
                            details += (
                                f"- **{addr_type}:** {addr.address} ({hostname})\n"
                            )
                            seen_hostnames.add(hostname)
                        else:
                            details += f"- **{addr_type}:** {addr.address}\n"
                    except socket.herror:
                        details += f"- **{addr_type}:** {addr.address}\n"
                else:
                    details += f"- **{addr_type}:** {addr.address}\n"
            details += self._get_wmi_network_info(interface)
            details += "\n"
        details += self._fetch_network_drives_details()
        return details

    def _fetch_network_drives_summary(self) -> str:
        """Fetch summary of network drives."""
        try:
            drives = self._get_network_drives()
            if drives:
                summary = "**Network Drives:**\n"
                for drive in drives:
                    summary += (
                        f"- **Drive Letter:** {drive['letter']}, "
                        f"**Remote Path:** {drive['remote']} ({drive['name']})\n"
                    )
                return summary
            return ""
        except Exception:
            self.logger.error("Failed to fetch network drives summary", exc_info=True)
            return "- **Network Drives Info:** Failed to fetch network drives summary\n"

    def _fetch_network_drives_details(self) -> str:
        """Fetch details of network drives."""
        try:
            drives = self._get_network_drives()
            if drives:
                details = "**Network Drives:**\n"
                for drive in drives:
                    details += (
                        f"- **Drive Letter:** {drive['letter']}, "
                        f"**Remote Path:** {drive['remote']} ({drive['name']})\n"
                    )
                return details
            return ""
        except Exception:
            self.logger.error("Failed to fetch network drives details", exc_info=True)
            return "- **Network Drives Info:** Failed to fetch network drives details\n"

    def _get_network_drives(self) -> list:
        """Get network drives information."""
        drives = []
        try:
            result = subprocess.check_output("net use", shell=True, encoding="cp850")
            lines = result.splitlines()
            for line in lines:
                if "\\" in line and ":" in line:
                    parts = line.split()
                    drives.append(
                        {
                            "letter": parts[1],
                            "remote": parts[2],
                            "name": parts[3] if len(parts) > 3 else "Unknown",
                        }
                    )
        except Exception:
            self.logger.error("Error getting network drives", exc_info=True)
        return drives

    def _get_address_type(self, family: int) -> str:
        """Get the address type (IPv4, IPv6, MAC) based on the family."""
        if family == socket.AF_INET:
            return "IPv4"
        if family == socket.AF_INET6:
            return "IPv6"
        if family == psutil.AF_LINK:
            return "MAC"
        return "Other"

    def _get_wmi_network_info(self, interface: str) -> str:
        """Fetch additional network information using WMI."""
        try:
            for nic in self.wmi.Win32_NetworkAdapterConfiguration(IPEnabled=True):
                if interface in (nic.Description, nic.Caption):
                    return (
                        f"- **Description:** {nic.Description}\n"
                        f"- **MAC Address:** {nic.MACAddress}\n"
                        f"- **DHCP Enabled:** {nic.DHCPEnabled}\n"
                        f"- **DHCP Server:** {nic.DHCPServer}\n"
                        f"- **DNS Servers:** {', '.join(nic.DNSServerSearchOrder or [])}\n"
                        f"- **IP Address:** {', '.join(nic.IPAddress or [])}\n"
                    )
            return ""
        except Exception:
            self.logger.error("Failed to fetch WMI network information", exc_info=True)
            return "- **WMI Info:** Failed to fetch additional details\n"
