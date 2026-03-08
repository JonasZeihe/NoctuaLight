"""
GPU Module for fetching GPU related information (Light version).

This module defines the GPU class that can gather
basic GPU details using py3nvml, wmi, and pyopencl.
In the Light version, only a short summary is provided.
"""

import logging
import subprocess
from py3nvml import py3nvml as nvml
import wmi
import pyopencl as cl


class GPU:
    """Class representing the GPU component (Light version)."""

    def __init__(self, logger: logging.Logger):
        """
        Initialize the GPU class with a logger.

        Args:
            logger (logging.Logger): Logger instance for logging.
        """
        self.logger = logger
        self.wmi = wmi.WMI()

    def get_summary(self) -> str:
        """
        Fetch a short summary of the GPU information.

        Returns:
            str: Summary text listing integrated GPU, OpenCL GPU, and/or NVIDIA GPU info.
        """
        self.logger.info("Fetching GPU summary (Light version).")
        summary_sections = []

        # Integrierte GPU
        if self.has_integrated_gpu():
            self.logger.debug("Detected integrated GPU.")
            integrated_summary = self._fetch_integrated_gpu_info_summary()
            if integrated_summary.strip():
                summary_sections.append(integrated_summary)

        # OpenCL
        if self.has_opencl_gpu():
            self.logger.debug("Detected OpenCL-compatible GPU.")
            opencl_summary = self._fetch_opencl_gpu_info_summary()
            if opencl_summary.strip():
                summary_sections.append(opencl_summary)

        # NVIDIA
        if self.is_nvidia_smi_available():
            self.logger.debug("NVIDIA SMI found.")
            nvidia_summary = self._fetch_nvidia_gpu_info_summary()
            if nvidia_summary.strip():
                summary_sections.append(nvidia_summary)

        if not summary_sections:
            return "**GPU Information**\nNo supported GPU found.\n"

        # Fasse mehrere Ergebnisse zusammen
        return "\n".join(summary_sections)

    def get_details(self) -> str:
        """
        In NoctuaLight, detailed GPU information is not provided.
        """
        return ""

    # -----------------------------------------------------------------
    # Hilfsmethoden: Prüfen, ob bestimmte GPU-Typen existieren
    # -----------------------------------------------------------------
    def has_integrated_gpu(self) -> bool:
        """Check if the system has an integrated GPU via WMI."""
        try:
            return bool(self.wmi.Win32_VideoController())
        except wmi.x_wmi:
            return False

    def has_opencl_gpu(self) -> bool:
        """Check if the system has an OpenCL-compatible GPU."""
        try:
            platforms = cl.get_platforms()
            return any(platform.get_devices() for platform in platforms)
        except cl.LogicError:
            return False

    def is_nvidia_smi_available(self) -> bool:
        """Check if NVIDIA SMI is available."""
        try:
            subprocess.check_output(["nvidia-smi"])
            return True
        except (FileNotFoundError, subprocess.CalledProcessError):
            return False

    # -----------------------------------------------------------------
    # Summaries für integrierte, OpenCL und NVIDIA GPUs
    # -----------------------------------------------------------------
    def _fetch_integrated_gpu_info_summary(self) -> str:
        """Fetch a summary of the integrated GPU information using WMI."""
        summary_lines = []
        try:
            for gpu in self.wmi.Win32_VideoController():
                # VRAM in MB
                if gpu.AdapterRAM and int(gpu.AdapterRAM) >= 0:
                    vram = int(gpu.AdapterRAM) / 1024 / 1024
                    summary_lines.append(
                        f"**Name:** {gpu.Name}\n"
                        f"**Manufacturer:** {gpu.AdapterCompatibility}\n"
                        f"**VRAM:** {vram:.1f} MB\n"
                    )
                else:
                    summary_lines.append(
                        f"**Name:** {gpu.Name}\n"
                        f"**Manufacturer:** {gpu.AdapterCompatibility}\n"
                    )
        except wmi.x_wmi:
            self.logger.error("Failed to fetch integrated GPU summary", exc_info=True)
        return "\n".join(summary_lines)

    def _fetch_opencl_gpu_info_summary(self) -> str:
        """Fetch a summary of the OpenCL GPU information."""
        summary_lines = []
        try:
            platforms = cl.get_platforms()
            for platform in platforms:
                devices = platform.get_devices()
                for device in devices:
                    vram_mb = device.global_mem_size / 1024 / 1024
                    if vram_mb >= 0:
                        summary_lines.append(
                            f"**Name:** {device.name}\n"
                            f"**Manufacturer:** {device.vendor}\n"
                            f"**VRAM:** {vram_mb:.1f} MB\n"
                        )
                    else:
                        summary_lines.append(
                            f"**Name:** {device.name}\n"
                            f"**Manufacturer:** {device.vendor}\n"
                        )
        except cl.LogicError:
            self.logger.error("Failed to fetch OpenCL GPU summary", exc_info=True)
        return "\n".join(summary_lines)

    def _fetch_nvidia_gpu_info_summary(self) -> str:
        """Fetch a summary of the NVIDIA GPU information using NVML."""
        summary_lines = []
        try:
            nvml.nvmlInit()
            device_count = nvml.nvmlDeviceGetCount()
            for i in range(device_count):
                handle = nvml.nvmlDeviceGetHandleByIndex(i)
                name = nvml.nvmlDeviceGetName(handle).decode("utf-8")
                mem_info = nvml.nvmlDeviceGetMemoryInfo(handle)
                vram_mb = mem_info.total / 1024 / 1024
                summary_lines.append(
                    f"**Name:** {name}\n"
                    f"**Manufacturer:** NVIDIA\n"
                    f"**VRAM:** {vram_mb:.1f} MB\n"
                )
            nvml.nvmlShutdown()
        except nvml.NVMLError as error:
            self.logger.error(
                "Failed to fetch NVIDIA GPU summary: %s", error, exc_info=True
            )
        return "\n".join(summary_lines)
