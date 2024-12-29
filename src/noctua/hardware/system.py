"""
System Module for fetching system related information.

This module defines the System class that uses various libraries
to gather and return information about the system.
"""

import logging
import platform
import socket
import ctypes
from ctypes import wintypes
import wmi


class System:
    """Class representing the System component."""

    def __init__(self, logger: logging.Logger):
        """Initialize the System class with a logger."""
        self.logger = logger
        try:
            self.wmi = wmi.WMI()
        except Exception as e:
            self.logger.error("Failed to initialize WMI: %s", e)
            self.wmi = None

    def get_summary(self) -> str:
        """Fetch a summary of the system information."""
        try:
            self.logger.info("Fetching system summary")
            return self._fetch_system_summary()
        except Exception as e:
            self.logger.error("Failed to fetch system summary", exc_info=True)
            return f"**System Information**\nFailed to fetch system summary: {e}\n"

    def get_details(self) -> str:
        """Fetch detailed system information."""
        try:
            self.logger.info("Fetching detailed system information")
            return self._fetch_system_details()
        except Exception as e:
            self.logger.error(
                "Failed to fetch detailed system information", exc_info=True
            )
            return f"**Detailed System Information**\nFailed to fetch detailed system information: {e}\n"

    def _fetch_system_summary(self) -> str:
        """Internal method to fetch system summary."""
        summary = (
            f"**Computer Name:** {socket.gethostname()}\n"
            f"**Operating System:** {platform.system()} {platform.release()} "
            f"(Version {platform.version()})\n"
        )
        summary += self._fetch_usb_devices_summary()
        summary += self._fetch_display_devices(detailed=False)
        return summary

    def _fetch_system_details(self) -> str:
        """Internal method to fetch detailed system information."""
        details = (
            f"**Computer Name:** {socket.gethostname()}\n"
            f"**Operating System:** {platform.system()} {platform.release()} "
            f"(Version {platform.version()})\n"
            f"**OS Build:** {platform.platform()}\n"
            f"**OS Architecture:** {platform.architecture()[0]}\n"
        )
        details += self._fetch_usb_devices_details()
        details += self._fetch_display_devices(detailed=True)
        return details

    def _fetch_usb_devices_summary(self) -> str:
        """Fetch summary of USB devices."""
        summary = "**USB Devices:**\n"
        try:
            if self.wmi:
                usb_devices = set()
                for device in self.wmi.Win32_PnPEntity():
                    if device.Name and "USB" in device.Name:
                        usb_devices.add(device.Name)
                for device in sorted(usb_devices):
                    summary += f"- {device}\n"
            else:
                summary += "WMI not initialized.\n"
        except Exception as e:
            self.logger.error("Failed to fetch USB devices summary", exc_info=True)
            summary += f"Failed to fetch USB devices summary: {e}\n"
        return summary

    def _fetch_usb_devices_details(self) -> str:
        """Fetch details of USB devices."""
        details = "**USB Devices:**\n"
        try:
            if self.wmi:
                usb_devices = {}
                for device in self.wmi.Win32_PnPEntity():
                    if device.Name and "USB" in device.Name:
                        usb_devices[device.Name] = device
                for name, device in sorted(usb_devices.items()):
                    details += (
                        f"- **Device:** {name}\n"
                        f"  - **Manufacturer:** {getattr(device, 'Manufacturer', 'Unknown')}\n"
                        f"  - **Device ID:** {getattr(device, 'DeviceID', 'Unknown')}\n"
                    )
            else:
                details += "WMI not initialized.\n"
        except Exception as e:
            self.logger.error("Failed to fetch USB devices details", exc_info=True)
            details += f"Failed to fetch USB devices details: {e}\n"
        return details

    def _fetch_display_devices(self, detailed=False) -> str:
        """Fetch display devices using EnumDisplayDevices."""
        devices = "**Monitors:**\n"
        user32 = ctypes.windll.user32
        dev = DEVMODEW()
        dev.dm_size = ctypes.sizeof(DEVMODEW)

        display_devices = {}
        i = 0
        while True:
            display_device = DISPLAY_DEVICEW()
            display_device.cb = ctypes.sizeof(display_device)
            if not user32.EnumDisplayDevicesW(None, i, ctypes.byref(display_device), 0):
                break
            if display_device.DeviceString not in display_devices:
                display_devices[display_device.DeviceString] = display_device
            i += 1

        for device_string, display_device in display_devices.items():
            if detailed:
                if user32.EnumDisplaySettingsW(
                    display_device.DeviceName,
                    ENUM_CURRENT_SETTINGS,
                    ctypes.byref(dev),
                ):
                    devices += (
                        f"- {device_string}\n"
                        f"  - **Manufacturer:** {display_device.DeviceID}\n"
                        f"  - **Model:** {display_device.DeviceKey}\n"
                        f"  - **Screen Height:** {dev.dmPelsHeight}\n"
                        f"  - **Screen Width:** {dev.dmPelsWidth}\n"
                        f"  - **Refresh Rate:** {dev.dmDisplayFrequency} Hz\n"
                        f"  - **Status:** {'Active' if display_device.StateFlags & DISPLAY_DEVICE_ACTIVE else 'Inactive'}\n"
                    )
            else:
                if user32.EnumDisplaySettingsW(
                    display_device.DeviceName,
                    ENUM_CURRENT_SETTINGS,
                    ctypes.byref(dev),
                ):
                    devices += (
                        f"- {device_string}\n"
                        f"  - **Screen Height:** {dev.dmPelsHeight}\n"
                        f"  - **Screen Width:** {dev.dmPelsWidth}\n"
                        f"  - **Refresh Rate:** {dev.dmDisplayFrequency} Hz\n"
                    )
        return devices


class DEVMODEW(ctypes.Structure):
    """Class representing DEVMODE structure."""

    _fields_ = [
        ("dmDeviceName", wintypes.WCHAR * 32),
        ("dmSpecVersion", wintypes.WORD),
        ("dmDriverVersion", wintypes.WORD),
        ("dm_size", wintypes.WORD),
        ("dmDriverExtra", wintypes.WORD),
        ("dmFields", wintypes.DWORD),
        ("dmOrientation", wintypes.SHORT),
        ("dmPaperSize", wintypes.SHORT),
        ("dmPaperLength", wintypes.SHORT),
        ("dmPaperWidth", wintypes.SHORT),
        ("dmScale", wintypes.SHORT),
        ("dmCopies", wintypes.SHORT),
        ("dmDefaultSource", wintypes.SHORT),
        ("dmPrintQuality", wintypes.SHORT),
        ("dmColor", wintypes.SHORT),
        ("dmDuplex", wintypes.SHORT),
        ("dmYResolution", wintypes.SHORT),
        ("dmTTOption", wintypes.SHORT),
        ("dmCollate", wintypes.SHORT),
        ("dmFormName", wintypes.WCHAR * 32),
        ("dmLogPixels", wintypes.WORD),
        ("dmBitsPerPel", wintypes.DWORD),
        ("dmPelsWidth", wintypes.DWORD),
        ("dmPelsHeight", wintypes.DWORD),
        ("dmDisplayFlags", wintypes.DWORD),
        ("dmDisplayFrequency", wintypes.DWORD),
        ("dmICMMethod", wintypes.DWORD),
        ("dmICMIntent", wintypes.DWORD),
        ("dmMediaType", wintypes.DWORD),
        ("dmDitherType", wintypes.DWORD),
        ("dmReserved1", wintypes.DWORD),
        ("dmReserved2", wintypes.DWORD),
        ("dmPanningWidth", wintypes.DWORD),
        ("dmPanningHeight", wintypes.DWORD),
    ]


class DISPLAY_DEVICEW(ctypes.Structure):
    """Class representing DISPLAY_DEVICEW structure."""

    _fields_ = [
        ("cb", wintypes.DWORD),
        ("DeviceName", wintypes.WCHAR * 32),
        ("DeviceString", wintypes.WCHAR * 128),
        ("StateFlags", wintypes.DWORD),
        ("DeviceID", wintypes.WCHAR * 128),
        ("DeviceKey", wintypes.WCHAR * 128),
    ]


ENUM_CURRENT_SETTINGS = -1
DISPLAY_DEVICE_ACTIVE = 0x00000001
