"""
BIOS Module for fetching BIOS related information.

This module defines the BIOS class that uses the WMI library to gather and
return information about the BIOS.
"""

import logging
import wmi


class BIOS:
    """Class representing the BIOS component."""

    def __init__(self, logger: logging.Logger):
        """Initialize the BIOS class with a logger.

        Args:
            logger (logging.Logger): Logger instance for logging.
        """
        self.logger = logger
        self.wmi = wmi.WMI()

    def get_summary(self) -> str:
        """Fetch a summary of the BIOS information.

        Returns:
            str: Summary of the BIOS information.
        """
        try:
            self.logger.info("Fetching BIOS summary")
            return self._fetch_bios_summary()
        except wmi.x_wmi:
            self.logger.error("Failed to fetch BIOS summary", exc_info=True)
            return "**BIOS Information**\nFailed to fetch BIOS summary.\n"
        except Exception:
            self.logger.error("An unexpected error occurred", exc_info=True)
            return "**BIOS Information**\nAn unexpected error occurred.\n"

    def get_details(self) -> str:
        """Fetch detailed BIOS information.

        Returns:
            str: Detailed BIOS information.
        """
        try:
            self.logger.info("Fetching detailed BIOS information")
            return self._fetch_bios_details()
        except wmi.x_wmi:
            self.logger.error(
                "Failed to fetch detailed BIOS information", exc_info=True
            )
            return "**Detailed BIOS Information**\nFailed to fetch detailed BIOS information.\n"
        except Exception:
            self.logger.error("An unexpected error occurred", exc_info=True)
            return "**Detailed BIOS Information**\nAn unexpected error occurred.\n"

    def _fetch_bios_summary(self) -> str:
        """Internal method to fetch BIOS summary.

        Returns:
            str: BIOS summary.
        """
        bios_info = ""
        for bios in self.wmi.Win32_BIOS():
            bios_info = (
                f"**Manufacturer:** {bios.Manufacturer}\n"
                f"**Version:** {bios.SMBIOSBIOSVersion}\n"
            )
        return bios_info

    def _fetch_bios_details(self) -> str:
        """Internal method to fetch detailed BIOS information.

        Returns:
            str: Detailed BIOS information.
        """
        details = ""
        for bios_entry in self.wmi.Win32_BIOS():
            details += (
                f"**Manufacturer:** {bios_entry.Manufacturer}\n"
                f"**Version:** {bios_entry.SMBIOSBIOSVersion}\n"
                f"**Release Date:** {self._format_date(bios_entry.ReleaseDate)}\n"
                f"**SMBIOS Version:** {bios_entry.SMBIOSMajorVersion}."
                f"{bios_entry.SMBIOSMinorVersion}\n"
                f"**BIOS Characteristics:** "
                f"{self._get_bios_characteristics(bios_entry.BIOSCharacteristics)}\n"
                f"**BIOS Language:** {bios_entry.CurrentLanguage}\n"
                f"**Primary BIOS:** {'Yes' if bios_entry.PrimaryBIOS else 'No'}\n"
            )
        return details

    def _format_date(self, date_str: str) -> str:
        """Format the BIOS release date.

        Args:
            date_str (str): Date string to format.

        Returns:
            str: Formatted date string.
        """
        if not date_str:
            return "Unknown"
        return f"{date_str[:4]}-{date_str[4:6]}-{date_str[6:8]}"

    def _get_bios_characteristics(self, characteristics: list) -> str:
        """Convert BIOS characteristics codes to human-readable string.

        Args:
            characteristics (list): List of characteristics codes.

        Returns:
            str: Human-readable BIOS characteristics.
        """
        characteristic_descriptions = {
            0: "Reserved",
            1: "BIOS Characteristics Not Supported",
            2: "ISA is supported",
            3: "MCA is supported",
            4: "EISA is supported",
            5: "PCI is supported",
            6: "PC Card (PCMCIA) is supported",
            7: "Plug and Play is supported",
            8: "APM is supported",
            9: "BIOS is upgradeable",
            10: "BIOS shadowing is allowed",
            11: "VLB is supported",
            12: "ESCD support is available",
            13: "Boot from CD is supported",
            14: "Selectable Boot is supported",
            15: "BIOS ROM is socketed",
            16: "Boot from PCMCIA is supported",
            17: "EDD is supported",
            18: "Print screen service is supported",
            19: "8042 keyboard services are supported",
            20: "Serial services are supported",
            21: "Printer services are supported",
            22: "CGA/Mono video services are supported",
            23: "NEC PC-98",
            24: "ACPI is supported",
            25: "USB legacy is supported",
            26: "AGP is supported",
            27: "I2O boot is supported",
            28: "LS-120 boot is supported",
            29: "ATAPI ZIP drive boot is supported",
            30: "1394 boot is supported",
            31: "Smart battery is supported",
            32: "BIOS Boot Specification is supported",
            33: "Function key-initiated network boot is supported",
            34: "Targeted content distribution is supported",
            35: "UEFI is supported",
        }
        return ", ".join(
            characteristic_descriptions.get(char, "Unknown") for char in characteristics
        )
