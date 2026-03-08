import os
import time
from dataclasses import dataclass
from typing import Protocol


class Component(Protocol):
    """Protocol for hardware components, defining the required interface."""

    def get_summary(self) -> str:
        """Returns a summary of the component's main attributes."""
        ...

    def get_details(self) -> str:
        """Returns detailed information of the component."""
        ...


@dataclass
class ComponentDetails:
    """Data class for storing references to all hardware components."""
    system: Component
    cpu: Component
    gpu: Component
    ram: Component
    disk: Component
    network: Component
    motherboard: Component
    bios: Component
    pc_name: str = ""


class Report:
    """
    Generates hardware reports in Markdown format. 
    In NoctuaLight, only the short summary (overview) is used.
    """

    def __init__(self, logger):
        """
        Initializes the Report class to manage short-report generation.

        Args:
            logger (Logger): Logger instance for reporting messages.
        """
        self.logger = logger

    def generate_report(
        self, system, cpu, gpu, ram, disk, network, motherboard, bios, pc_name=""
    ):
        """
        Generates a short hardware report by gathering summary info from components.

        Args:
            system, cpu, gpu, ram, disk, network, motherboard, bios (Component): Component instances.
            pc_name (str): Optional PC name for the report header.
        """
        self.logger.debug("Starting short-report generation process.")
        try:
            report_file_path = self._build_report_file_path(pc_name)
            self.logger.info(f"Generating hardware report at: {report_file_path}")

            report_content = self._compile_report_content(
                system, cpu, gpu, ram, disk, network, motherboard, bios, pc_name
            )
            self._save_report(report_content, report_file_path)
            self.logger.info(f"Report successfully created at: {report_file_path}")

        except Exception:
            self.logger.error(
                "Report generation failed due to an error.", exc_info=True
            )

    def _build_report_file_path(self, pc_name):
        """
        Constructs a filename for the report, incorporating a timestamp and optional PC name.
        """
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        sanitized_pc_name = pc_name.replace(" ", "_") if pc_name else "unnamed_pc"
        filename = f"hardware_report_{sanitized_pc_name}_{timestamp}.md"
        return os.path.join("result", filename)

    def _compile_report_content(
        self, system, cpu, gpu, ram, disk, network, motherboard, bios, pc_name
    ):
        """
        Compiles the short report content. Only uses get_summary() from each component.
        """
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        report_content = "# Hardware Report\n\n"
        report_content += f"**Generated on:** {timestamp}\n"

        if pc_name:
            report_content += f"**PC Name:** {pc_name}\n"

        # Always generate the overview for all components
        report_content += self._generate_overview(
            system, cpu, gpu, ram, disk, network, motherboard, bios
        )

        return report_content

    def _generate_overview(self, *components):
        """
        Generates an overview of all components (short summary) in Markdown format.
        """
        overview_content = "\n# **Hardware Overview**\n\n"
        for component in components:
            class_name = component.__class__.__name__.upper()
            overview_content += f"## {class_name} SUMMARY\n"
            overview_content += component.get_summary() + "\n---\n"
        return overview_content

    def _save_report(self, report_content, file_path):
        """
        Saves the report content to a specified file.
        """
        try:
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            with open(file_path, "w", encoding="utf-8") as report_file:
                report_file.write(report_content)
            self.logger.info(f"Report successfully saved at: {file_path}")
        except (OSError, IOError) as save_error:
            self.logger.error(
                f"Failed to save the report due to an error: {save_error}",
                exc_info=True,
            )
