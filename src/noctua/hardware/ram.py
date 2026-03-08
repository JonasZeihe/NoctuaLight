"""
RAM Module for fetching RAM related information.

This module defines the RAM class that uses the psutil and WMI libraries
to gather and return information about the RAM.
"""

import logging
import psutil
import wmi


class RAM:
    """Class representing the RAM component."""

    def __init__(self, logger: logging.Logger):
        """
        Initialize the RAM class with a logger.

        Args:
            logger (logging.Logger): Logger instance for logging.
        """
        self.logger = logger
        self.wmi = wmi.WMI()

    def get_summary(self) -> str:
        """
        Fetch a summary of the RAM information.

        Returns:
            str: Summary of the RAM information.
        """
        try:
            self.logger.info("Fetching RAM summary")
            return self._fetch_ram_summary()
        except Exception as e:
            self.logger.error("Failed to fetch RAM summary", exc_info=True)
            return f"**RAM Information**\nFailed to fetch RAM summary: {str(e)}\n"

    def get_details(self) -> str:
        """
        Fetch detailed RAM information.

        Returns:
            str: Detailed RAM information.
        """
        try:
            self.logger.info("Fetching detailed RAM information")
            return self._fetch_ram_details()
        except Exception as e:
            self.logger.error("Failed to fetch detailed RAM information", exc_info=True)
            return f"**Detailed RAM Information**\nFailed to fetch detailed RAM information: {str(e)}\n"

    def _fetch_ram_summary(self) -> str:
        """
        Fetch a summary of the RAM modules.

        Returns:
            str: Summary information for all RAM modules.
        """
        mem = psutil.virtual_memory()
        summary = f"**Total Installed RAM:** {self.bytes_to_gb(mem.total)} GB\n**Modules:**\n"
        for idx, module in enumerate(self.wmi.Win32_PhysicalMemory(), start=1):
            summary += (
                f"- **Module {idx}:** {self.bytes_to_gb(int(module.Capacity))} GB, "
                f"{module.Speed} MHz, Configured Speed: {self._format_value(module.Speed, module.ConfiguredClockSpeed)} MHz\n"
            )
        return summary

    def _fetch_ram_details(self) -> str:
        """
        Fetch detailed information about the RAM modules.

        Returns:
            str: Detailed RAM module information.
        """
        mem = psutil.virtual_memory()
        details = (
            f"**Total Installed RAM:** {self.bytes_to_gb(mem.total)} GB\n"
            f"**Used RAM:** {self.bytes_to_gb(mem.used)} GB\n"
            f"**Percentage Used:** {mem.percent}%\n\n"
            f"**Physical RAM Modules:**\n"
        )
        for idx, module in enumerate(self.wmi.Win32_PhysicalMemory(), start=1):
            details += (
                f"- **Module {idx}:**\n"
                f"  - **Capacity:** {self.bytes_to_gb(int(module.Capacity))} GB\n"
                f"  - **Speed:** {module.Speed} MHz\n"
                f"  - **Configured Speed:** {self._format_value(module.Speed, module.ConfiguredClockSpeed)} MHz\n"
                f"  - **Manufacturer:** {module.Manufacturer}\n"
                f"  - **Serial Number:** {module.SerialNumber}\n"
                f"  - **Part Number:** {module.PartNumber.strip()}\n"
                f"  - **Form Factor:** {self._get_form_factor(module.FormFactor)}\n"
                f"  - **Memory Type:** {self._get_memory_type(module.MemoryType)}\n"
                f"  - **Bank Label:** {module.BankLabel}\n"
                f"  - **Data Width:** {module.DataWidth} bits\n"
                f"  - **Total Width:** {module.TotalWidth} bits\n"
                f"  - **Voltage:** {self._format_voltage(module.MinVoltage)} V\n"
                f"  - **Configured Voltage:** {self._format_voltage(module.ConfiguredVoltage)} V\n\n"
            )
        return details

    def _format_value(self, expected_value: str, actual_value: str) -> str:
        """
        Format the value to highlight discrepancies between expected and actual values.

        Args:
            expected_value (str): The expected value.
            actual_value (str): The actual value.

        Returns:
            str: Formatted value string.
        """
        if expected_value == actual_value:
            return f"{actual_value}"
        return f"**{actual_value}**"

    def _format_voltage(self, voltage: int) -> str:
        """
        Format the voltage value for display.

        Args:
            voltage (int): Voltage value in millivolts.

        Returns:
            str: Voltage value in volts, formatted as a string.
        """
        if voltage:
            return f"{voltage / 1000:.2f}"
        return "N/A"

    def _get_form_factor(self, form_factor_code: int) -> str:
        """
        Convert the form factor code to a human-readable string.

        Args:
            form_factor_code (int): Form factor code.

        Returns:
            str: Form factor description.
        """
        form_factors = {
            0: "Unknown",
            8: "DIMM",
            12: "SODIMM",
        }
        return form_factors.get(form_factor_code, "Other")

    def _get_memory_type(self, memory_type_code: int) -> str:
        """
        Convert the memory type code to a human-readable string.

        Args:
            memory_type_code (int): Memory type code.

        Returns:
            str: Memory type description.
        """
        memory_types = {
            0: "Unknown",
            20: "DDR",
            21: "DDR2",
            24: "DDR3",
            26: "DDR4",
        }
        return memory_types.get(memory_type_code, "Other")

    def bytes_to_gb(self, bytes_value: int) -> float:
        """
        Convert bytes to gigabytes.

        Args:
            bytes_value (int): Value in bytes.

        Returns:
            float: Value in gigabytes.
        """
        return round(bytes_value / (1024**3), 2)
