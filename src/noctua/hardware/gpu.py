"""
GPU Module for fetching GPU related information.

This module defines the GPU class that uses the py3nvml, wmi, and pyopencl libraries
to gather and return information about the GPU.
"""

import logging
import subprocess
from py3nvml import py3nvml as nvml
import wmi
import pyopencl as cl


class GPU:
    """Class representing the GPU component."""

    def __init__(self, logger: logging.Logger):
        """Initialize the GPU class with a logger."""
        self.logger = logger
        self.wmi = wmi.WMI()

    def get_summary(self) -> str:
        """Fetch a summary of the GPU information."""
        summary = []

        if self.has_integrated_gpu():
            summary.append(self._fetch_integrated_gpu_info_summary())

        if self.has_opencl_gpu():
            summary.append(self._fetch_opencl_gpu_info_summary())

        if self.is_nvidia_smi_available():
            summary.append(self._fetch_nvidia_gpu_info_summary())

        if not summary:
            return "**GPU Information**\nNo supported GPU found.\n"

        return "\n".join(summary)

    def get_details(self) -> str:
        """Fetch detailed information of the GPU."""
        details = []

        if self.has_integrated_gpu():
            details.append(self._fetch_integrated_gpu_info_detailed())

        if self.has_opencl_gpu():
            details.append(self._fetch_opencl_gpu_info_detailed())

        if self.is_nvidia_smi_available():
            details.append(self._fetch_nvidia_gpu_info_detailed())

        if not details:
            return "**Detailed GPU Information**\nNo supported GPU found.\n"

        return "\n".join(details)

    def has_integrated_gpu(self) -> bool:
        """Check if the system has an integrated GPU."""
        try:
            return bool(self.wmi.Win32_VideoController())
        except wmi.x_wmi:
            return False

    def has_opencl_gpu(self) -> bool:
        """Check if the system has an OpenCL GPU."""
        try:
            platforms = cl.get_platforms()
            return any(platform.get_devices() for platform in platforms)
        except cl.LogicError:
            return False

    def _fetch_integrated_gpu_info_summary(self) -> str:
        """Fetch a summary of the integrated GPU information using WMI."""
        summary = []
        try:
            for gpu in self.wmi.Win32_VideoController():
                if gpu.AdapterRAM and int(gpu.AdapterRAM) >= 0:
                    vram = int(gpu.AdapterRAM) / 1024 / 1024
                    summary.append(
                        f"**Name:** {gpu.Name}\n"
                        f"**Manufacturer:** {gpu.AdapterCompatibility}\n"
                        f"**VRAM:** {vram} MB\n"
                    )
                else:
                    summary.append(
                        f"**Name:** {gpu.Name}\n"
                        f"**Manufacturer:** {gpu.AdapterCompatibility}\n"
                    )
        except wmi.x_wmi:
            self.logger.error("Failed to fetch integrated GPU summary", exc_info=True)
        return "\n".join(summary)

    def _fetch_integrated_gpu_info_detailed(self) -> str:
        """Fetch detailed information of the integrated GPU using WMI."""
        details = []
        try:
            for gpu in self.wmi.Win32_VideoController():
                if gpu.AdapterRAM and int(gpu.AdapterRAM) >= 0:
                    vram = int(gpu.AdapterRAM) / 1024 / 1024
                    details.append(
                        f"**Name:** {gpu.Name}\n"
                        f"**Driver Version:** {gpu.DriverVersion}\n"
                        f"**Adapter RAM:** {vram} MB\n"
                        f"**Manufacturer:** {gpu.AdapterCompatibility}\n"
                        f"**PNP Device ID:** {gpu.PNPDeviceID}\n"
                        f"**Driver Date:** {gpu.DriverDate}\n"
                    )
                else:
                    details.append(
                        f"**Name:** {gpu.Name}\n"
                        f"**Driver Version:** {gpu.DriverVersion}\n"
                        f"**Manufacturer:** {gpu.AdapterCompatibility}\n"
                        f"**PNP Device ID:** {gpu.PNPDeviceID}\n"
                        f"**Driver Date:** {gpu.DriverDate}\n"
                    )
        except wmi.x_wmi:
            self.logger.error(
                "Failed to fetch integrated GPU detailed info", exc_info=True
            )
        return "\n".join(details)

    def _fetch_opencl_gpu_info_summary(self) -> str:
        """Fetch a summary of the OpenCL GPU information."""
        summary = []
        try:
            platforms = cl.get_platforms()
            for platform in platforms:
                devices = platform.get_devices()
                for device in devices:
                    vram = device.global_mem_size / 1024 / 1024
                    if vram >= 0:
                        summary.append(
                            f"**Name:** {device.name}\n"
                            f"**Manufacturer:** {device.vendor}\n"
                            f"**VRAM:** {vram} MB\n"
                        )
                    else:
                        summary.append(
                            f"**Name:** {device.name}\n"
                            f"**Manufacturer:** {device.vendor}\n"
                        )
        except cl.LogicError:
            self.logger.error("Failed to fetch OpenCL GPU summary", exc_info=True)
        return "\n".join(summary)

    def _fetch_opencl_gpu_info_detailed(self) -> str:
        """Fetch detailed information of the OpenCL GPU."""
        details = []
        try:
            platforms = cl.get_platforms()
            for platform in platforms:
                devices = platform.get_devices()
                for device in devices:
                    vram = device.global_mem_size / 1024 / 1024
                    if vram >= 0:
                        details.append(
                            f"**Name:** {device.name}\n"
                            f"**Manufacturer:** {device.vendor}\n"
                            f"**VRAM:** {vram} MB\n"
                            f"**Driver Version:** {device.driver_version}\n"
                            f"**OpenCL Version:** {device.opencl_c_version}\n"
                        )
                    else:
                        details.append(
                            f"**Name:** {device.name}\n"
                            f"**Manufacturer:** {device.vendor}\n"
                            f"**Driver Version:** {device.driver_version}\n"
                            f"**OpenCL Version:** {device.opencl_c_version}\n"
                        )
        except cl.LogicError:
            self.logger.error("Failed to fetch OpenCL GPU detailed info", exc_info=True)
        return "\n".join(details)

    def _fetch_nvidia_gpu_info_summary(self) -> str:
        """Fetch a summary of the NVIDIA GPU information using NVML."""
        summary = []
        try:
            nvml.nvmlInit()
            device_count = nvml.nvmlDeviceGetCount()
            for i in range(device_count):
                handle = nvml.nvmlDeviceGetHandleByIndex(i)
                name = nvml.nvmlDeviceGetName(handle).decode("utf-8")
                mem_info = nvml.nvmlDeviceGetMemoryInfo(handle)
                vram = mem_info.total / 1024 / 1024
                summary.append(
                    f"**Name:** {name}\n"
                    f"**Manufacturer:** NVIDIA\n"
                    f"**VRAM:** {vram} MB\n"
                )
            nvml.nvmlShutdown()
        except nvml.NVMLError as error:
            self.logger.error(
                "Failed to fetch NVIDIA GPU summary: %s", error, exc_info=True
            )
        return "\n".join(summary)

    def _fetch_nvidia_gpu_info_detailed(self) -> str:
        """Fetch detailed information of the NVIDIA GPU using NVML."""
        details = []
        try:
            nvml.nvmlInit()
            device_count = nvml.nvmlDeviceGetCount()
            for i in range(device_count):
                handle = nvml.nvmlDeviceGetHandleByIndex(i)
                name = nvml.nvmlDeviceGetName(handle).decode("utf-8")
                mem_info = nvml.nvmlDeviceGetMemoryInfo(handle)
                vram_total = mem_info.total / 1024 / 1024
                vram_used = mem_info.used / 1024 / 1024
                vram_free = mem_info.free / 1024 / 1024
                utilization = nvml.nvmlDeviceGetUtilizationRates(handle)
                pci_info = nvml.nvmlDeviceGetPciInfo(handle)
                temp = nvml.nvmlDeviceGetTemperature(handle, nvml.NVML_TEMPERATURE_GPU)
                details.append(
                    f"**Name:** {name}\n"
                    f"**Total Memory:** {vram_total} MB\n"
                    f"**Used Memory:** {vram_used} MB\n"
                    f"**Free Memory:** {vram_free} MB\n"
                    f"**GPU Utilization:** {utilization.gpu}%\n"
                    f"**Memory Utilization:** {utilization.memory}%\n"
                    f"**Temperature:** {temp}°C\n"
                    f"**PCI Bus ID:** {pci_info.busId}\n"
                    f"**Serial Number:** {nvml.nvmlDeviceGetSerial(handle).decode('utf-8')}\n"
                )
            nvml.nvmlShutdown()
        except nvml.NVMLError as error:
            self.logger.error(
                "Failed to fetch NVIDIA GPU detailed info: %s", error, exc_info=True
            )
        return "\n".join(details)

    def is_nvidia_smi_available(self) -> bool:
        """Check if NVIDIA SMI is available."""
        try:
            subprocess.check_output(["nvidia-smi"])
            return True
        except (FileNotFoundError, subprocess.CalledProcessError):
            return False
