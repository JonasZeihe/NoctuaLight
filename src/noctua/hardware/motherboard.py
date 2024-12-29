"""
Motherboard Module for fetching motherboard related information.

This module defines the Motherboard class that uses the WMI library
to gather and return information about the motherboard.
"""

import logging
import wmi


class Motherboard:
    """Class representing the Motherboard component."""

    def __init__(self, logger: logging.Logger):
        """Initialize the Motherboard class with a logger."""
        self.logger = logger
        self.wmi = wmi.WMI()

    def get_summary(self) -> str:
        """Fetch a summary of the motherboard information."""
        try:
            self.logger.info("Fetching motherboard summary")
            return self._fetch_motherboard_summary()
        except wmi.x_wmi:
            self.logger.error("Failed to fetch motherboard summary", exc_info=True)
            return "**Motherboard Information**\nFailed to fetch motherboard summary.\n"
        except Exception:
            self.logger.error("An unexpected error occurred", exc_info=True)
            return "**Motherboard Information**\nAn unexpected error occurred.\n"

    def get_details(self) -> str:
        """Fetch detailed motherboard information."""
        try:
            self.logger.info("Fetching detailed motherboard information")
            return self._fetch_motherboard_details()
        except wmi.x_wmi:
            self.logger.error(
                "Failed to fetch detailed motherboard information", exc_info=True
            )
            return "**Detailed Motherboard Information**\nFailed to fetch detailed motherboard information.\n"
        except Exception:
            self.logger.error("An unexpected error occurred", exc_info=True)
            return (
                "**Detailed Motherboard Information**\nAn unexpected error occurred.\n"
            )

    def _fetch_motherboard_summary(self) -> str:
        """Internal method to fetch motherboard summary."""
        try:
            summary = ""
            for board in self.wmi.Win32_BaseBoard():
                summary += (
                    f"**Manufacturer:** {board.Manufacturer}\n"
                    f"**Product:** {board.Product}\n"
                )
            return summary
        except wmi.x_wmi:
            self.logger.error("Failed to fetch motherboard summary", exc_info=True)
            return "**Failed to fetch motherboard summary**"
        except Exception:
            self.logger.error("An unexpected error occurred", exc_info=True)
            return "**An unexpected error occurred**"

    def _fetch_motherboard_details(self) -> str:
        """Internal method to fetch detailed motherboard information."""
        try:
            details = ""
            for board in self.wmi.Win32_BaseBoard():
                details += (
                    f"**Manufacturer:** {board.Manufacturer}\n"
                    f"**Product:** {board.Product}\n"
                    f"**Serial Number:** {board.SerialNumber}\n"
                    f"**Version:** {board.Version}\n"
                    f"**BIOS Version:** {self._get_bios_version()}\n"
                    f"**Slots:**\n{self._get_motherboard_slots()}\n"
                    f"**USB Ports:**\n{self._get_usb_ports()}\n"
                    f"**PCIe Slots:**\n{self._get_pcie_slots()}\n"
                )
            return details
        except wmi.x_wmi:
            self.logger.error(
                "Failed to fetch detailed motherboard information", exc_info=True
            )
            return "**Failed to fetch detailed motherboard information**"
        except Exception:
            self.logger.error("An unexpected error occurred", exc_info=True)
            return "**An unexpected error occurred**"

    def _get_bios_version(self) -> str:
        """Fetch the BIOS version."""
        try:
            bios = self.wmi.Win32_BIOS()[0]
            return bios.SMBIOSBIOSVersion
        except wmi.x_wmi:
            self.logger.error("Failed to fetch BIOS version", exc_info=True)
            return "Unknown"
        except Exception:
            self.logger.error("An unexpected error occurred", exc_info=True)
            return "Unknown"

    def _get_motherboard_slots(self) -> str:
        """Fetch details about motherboard slots."""
        try:
            slots = self.wmi.Win32_SystemSlot()
            slot_details = ""
            for slot in slots:
                slot_details += (
                    f"Slot: {slot.SlotDesignation}, "
                    f"Type: {slot.Name}, "
                    f"Status: {slot.Status}\n"
                )
            return slot_details if slot_details else "No slot information available"
        except wmi.x_wmi:
            self.logger.error("Failed to fetch motherboard slots", exc_info=True)
            return "Failed to fetch slot information"
        except Exception:
            self.logger.error("An unexpected error occurred", exc_info=True)
            return "An unexpected error occurred"

    def _get_usb_ports(self) -> str:
        """Fetch details about USB ports."""
        try:
            usb_ports = self.wmi.Win32_USBController()
            usb_details = ""
            for port in usb_ports:
                usb_details += (
                    f"Device ID: {port.DeviceID}, "
                    f"Name: {port.Name}, "
                    f"Status: {port.Status}\n"
                )
            return usb_details if usb_details else "No USB port information available"
        except wmi.x_wmi:
            self.logger.error("Failed to fetch USB port information", exc_info=True)
            return "Failed to fetch USB port information"
        except Exception:
            self.logger.error("An unexpected error occurred", exc_info=True)
            return "An unexpected error occurred"

    def _get_pcie_slots(self) -> str:
        """Fetch details about PCIe slots."""
        try:
            pcie_slots = self.wmi.Win32_SystemSlot()
            pcie_details = ""
            for slot in pcie_slots:
                if "PCI" in slot.Name:
                    pcie_details += (
                        f"Slot: {slot.SlotDesignation}, "
                        f"Type: {slot.Name}, "
                        f"Status: {slot.Status}\n"
                    )
            return (
                pcie_details if pcie_details else "No PCIe slot information available"
            )
        except wmi.x_wmi:
            self.logger.error("Failed to fetch PCIe slot information", exc_info=True)
            return "Failed to fetch PCIe slot information"
        except Exception:
            self.logger.error("An unexpected error occurred", exc_info=True)
            return "An unexpected error occurred"
