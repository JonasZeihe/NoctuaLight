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
        """Initialize the RAM class with a logger."""
        self.logger = logger
        self.wmi = wmi.WMI()

    def get_summary(self) -> str:
        """Fetch a summary of the RAM information."""
        try:
            self.logger.info("Fetching RAM summary")
            return self._fetch_ram_summary()
        except Exception:
            self.logger.error("Failed to fetch RAM summary", exc_info=True)
            return "**RAM Information**\nFailed to fetch RAM summary.\n"

    def get_details(self) -> str:
        """Fetch detailed RAM information."""
        try:
            self.logger.info("Fetching detailed RAM information")
            return self._fetch_ram_details()
        except Exception:
            self.logger.error("Failed to fetch detailed RAM information", exc_info=True)
            return "**Detailed RAM Information**\nFailed to fetch detailed RAM information.\n"

    def _fetch_ram_summary(self) -> str:
        """Fetch RAM summary."""
        mem = psutil.virtual_memory()
        summary = f"**Total:** {self.bytes_to_gb(mem.total)} GB\n**Module:**\n"
        for idx, module in enumerate(self.wmi.Win32_PhysicalMemory(), start=1):
            summary += (
                f"- **Module {idx}:** {self.bytes_to_gb(int(module.Capacity))} GB, "
                f"{module.Speed} MHz, Configured Speed: {self._format_value(module.Speed, module.ConfiguredClockSpeed)} MHz\n"
            )
        return summary

    def _fetch_ram_details(self) -> str:
        """Fetch detailed RAM information."""
        mem = psutil.virtual_memory()
        details = (
            f"**Total:** {self.bytes_to_gb(mem.total)} GB\n"
            f"**Used:** {self.bytes_to_gb(mem.used)} GB\n"
            f"**Percentage:** {mem.percent}%\n"
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
                f"  - **Part Number:** {module.PartNumber}\n"
                f"  - **Form Factor:** {self._get_form_factor(module.FormFactor)}\n"
                f"  - **Memory Type:** {self._get_memory_type(module.MemoryType)}\n"
                f"  - **Bank Label:** {module.BankLabel}\n"
                f"  - **Data Width:** {module.DataWidth} bits\n"
                f"  - **Total Width:** {module.TotalWidth} bits\n"
                f"  - **Voltage:** {self._format_voltage(module.MinVoltage)} V\n"
                f"  - **Configured Voltage:** {self._format_voltage(module.ConfiguredVoltage)} V\n"
            )
        return details

    def _format_value(self, expected_value: str, actual_value: str) -> str:
        """Format the value for display."""
        if expected_value == actual_value:
            return f"{actual_value}"
        return f"**_{actual_value}_**"

    def _format_voltage(self, voltage: int) -> str:
        """Format the voltage value for display."""
        if voltage is not None:
            voltage_v = voltage / 1000
            return f"{voltage_v:.2f}"
        return "N/A"

    def _get_form_factor(self, form_factor_code: int) -> str:
        """Convert form factor code to string."""
        form_factors = {
            0: "Unknown",
            1: "Other",
            2: "SIP",
            3: "DIP",
            4: "ZIP",
            5: "SOJ",
            6: "Proprietary",
            7: "SIMM",
            8: "DIMM",
            9: "TSOP",
            10: "PGA",
            11: "RIMM",
            12: "SODIMM",
            13: "SRIMM",
            14: "FB-DIMM",
        }
        return form_factors.get(form_factor_code, "Unknown")

    def _get_memory_type(self, memory_type_code: int) -> str:
        """Convert memory type code to string."""
        memory_types = {
            0: "Unknown",
            1: "Other",
            2: "DRAM",
            3: "Synchronous DRAM",
            4: "Cache DRAM",
            5: "EDO",
            6: "EDRAM",
            7: "VRAM",
            8: "SRAM",
            9: "RAM",
            10: "ROM",
            11: "Flash",
            12: "EEPROM",
            13: "FEPROM",
            14: "EPROM",
            15: "CDRAM",
            16: "3DRAM",
            17: "SDRAM",
            18: "SGRAM",
            19: "RDRAM",
            20: "DDR",
            21: "DDR2",
            22: "DDR2 FB-DIMM",
            24: "DDR3",
            25: "FBD2",
        }
        return memory_types.get(memory_type_code, "Unknown")

    def bytes_to_gb(self, bytes_value: int) -> float:
        """Convert bytes to gigabytes."""
        return round(bytes_value / (1024**3), 2)
