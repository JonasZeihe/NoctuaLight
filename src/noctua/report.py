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
    """Generates hardware reports in Markdown format, supporting both summaries and detailed reports."""

    def __init__(
        self, components, all_components_selection, detailed_report_option, logger
    ):
        """
        Initializes the Report class to manage report generation.

        Args:
            components (dict): Mapping of component names to BooleanVar selection variables.
            all_components_selection (tk.BooleanVar): Indicates if all components are selected.
            detailed_report_option (tk.BooleanVar): Indicates if detailed information is required.
            logger (Logger): Logger instance for reporting messages.
        """
        self.logger = logger
        self.components = components
        self.all_components_selection = all_components_selection
        self.detailed_report_option = detailed_report_option

    def generate_report(
        self, system, cpu, gpu, ram, disk, network, motherboard, bios, pc_name=""
    ):
        """
        Generates a hardware report by gathering component information and saving it to a file.

        Args:
            system, cpu, gpu, ram, disk, network, motherboard, bios (Component): Component instances.
            pc_name (str): Optional PC name for report customization.
        """
        self.logger.debug("Starting report generation process.")
        try:
            report_file_path = self._build_report_file_path(pc_name)
            self.logger.info(f"Generating hardware report at: {report_file_path}")

            report_content = self._compile_report_content(
                system, cpu, gpu, ram, disk, network, motherboard, bios, pc_name
            )
            self._save_report(report_content, report_file_path)
            self.logger.info(f"Report successfully created at: {report_file_path}")

        except Exception as error:
            self.logger.error(
                "Report generation failed due to an error.", exc_info=True
            )

    def _build_report_file_path(self, pc_name):
        """
        Constructs a filename for the report, incorporating a timestamp and optional PC name.

        Args:
            pc_name (str): Optional PC name for report customization.

        Returns:
            str: The full file path for the generated report.
        """
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        sanitized_pc_name = pc_name.replace(" ", "_") if pc_name else "unnamed_pc"
        filename = f"hardware_report_{sanitized_pc_name}_{timestamp}.md"
        return os.path.join("result", filename)

    def _compile_report_content(
        self, system, cpu, gpu, ram, disk, network, motherboard, bios, pc_name
    ):
        """
        Compiles the report content based on selected components and report details.

        Args:
            system, cpu, gpu, ram, disk, network, motherboard, bios (Component): Component instances.
            pc_name (str): Optional PC name for report customization.

        Returns:
            str: Compiled report content in Markdown format.
        """
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        report_content = f"# Hardware Report\n\n**Generated on:** {timestamp}\n"
        if pc_name:
            report_content += f"**PC Name:** {pc_name}\n"

        if self.all_components_selection.get():
            self.logger.debug("Including all components in the report overview.")
            report_content += self._generate_overview(
                system, cpu, gpu, ram, disk, network, motherboard, bios
            )

        if self.detailed_report_option.get():
            self.logger.debug("Including detailed information for all components.")
            report_content += self._generate_full_details(
                system, cpu, gpu, ram, disk, network, motherboard, bios
            )
        else:
            selected_components = [
                comp_name for comp_name, var in self.components.items() if var.get()
            ]
            if selected_components:
                self.logger.debug(
                    f"Generating report for selected components: {selected_components}"
                )
                report_content += self._generate_selected_component_details(
                    system, cpu, gpu, ram, disk, network, motherboard, bios
                )
            else:
                self.logger.warning(
                    "No components selected; generating an empty report."
                )
                report_content += "\nNo components selected."

        return report_content

    def _generate_overview(self, *components):
        """
        Generates an overview of all components in Markdown format.

        Args:
            *components (Component): All components to include in the overview.

        Returns:
            str: Markdown-formatted overview content.
        """
        overview_content = "# **Hardware Overview**\n\n"
        for component in components:
            overview_content += (
                f"## **{component.__class__.__name__.upper()} Information**\n"
            )
            overview_content += component.get_summary() + "\n---\n"
        return overview_content

    def _generate_full_details(self, *components):
        """
        Generates detailed information for all components in Markdown format.

        Args:
            *components (Component): All components to include in the detailed report.

        Returns:
            str: Markdown-formatted detailed information.
        """
        details_content = ""
        for component in components:
            details_content += (
                f"\n## Detailed {component.__class__.__name__.upper()} Information\n"
            )
            details_content += component.get_details() + "\n---\n"
        return details_content

    def _generate_selected_component_details(
        self, system, cpu, gpu, ram, disk, network, motherboard, bios
    ):
        """
        Generates detailed information only for selected components in Markdown format.

        Args:
            system, cpu, gpu, ram, disk, network, motherboard, bios (Component): Component instances.

        Returns:
            str: Markdown-formatted content for the selected components.
        """
        details_content = ""
        components_map = {
            "system": system,
            "cpu": cpu,
            "gpu": gpu,
            "ram": ram,
            "disk": disk,
            "network": network,
            "motherboard": motherboard,
            "bios": bios,
        }

        for component_name, var in self.components.items():
            if var.get():
                component_instance = components_map.get(component_name)
                if component_instance:
                    self.logger.debug(f"Including details for {component_name}.")
                    details_content += (
                        f"\n## Detailed {component_name.capitalize()} Information\n"
                    )
                    details_content += component_instance.get_details() + "\n---\n"
                else:
                    self.logger.warning(f"Details not available for {component_name}.")

        return details_content

    def _save_report(self, report_content, file_path):
        """
        Saves the report content to a specified file.

        Args:
            report_content (str): The report content to save.
            file_path (str): The file path where the report will be saved.
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
