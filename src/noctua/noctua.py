import tkinter as tk
from noctua.gui import NoctuaGUI
from noctua.report import Report

# Hardware-Komponenten
from noctua.hardware.cpu import CPU
from noctua.hardware.gpu import GPU
from noctua.hardware.ram import RAM
from noctua.hardware.disk import Disk
from noctua.hardware.network import Network
from noctua.hardware.motherboard import Motherboard
from noctua.hardware.bios import BIOS
from noctua.hardware.system import System

from noctua.logger import Logger


class Noctua:
    def __init__(self, is_logging_enabled=False):
        """
        Initializes the Noctua application, including GUI setup, hardware components,
        and logging configuration in the specified 'result' folder.

        Args:
            is_logging_enabled (bool): Determines if logging to file is enabled.
        """
        self.logger = Logger(log_to_file=is_logging_enabled)
        self.logger.debug("Noctua application initialization process started")

        # Hauptfenster (Tk) erstellen
        self.application_root_window = tk.Tk()
        self.application_root_window.title("Noctua - Hardware Information Overview")
        self.logger.info("Noctua application main window created successfully")

        # Hardware-Komponenten instanzieren
        self.hardware_component_instances = self.initialize_hardware_component_instances()

        # Report-Generator instanzieren
        self.report_generator = Report(logger=self.logger)

        # GUI-Objekt erstellen
        self.noctua_user_interface = NoctuaGUI(
            root_window=self.application_root_window,
            report_generation_callback=self.generate_hardware_report,
            application_closure_callback=self.terminate_noctua_application,
        )

    def initialize_hardware_component_instances(self):
        """
        Initializes and creates instances of hardware components.

        Returns:
            tuple: A tuple containing instances of each hardware component.
        """
        self.logger.debug("Instantiating all required hardware components")
        component_instances = {}
        try:
            hardware_classes = [
                System,
                CPU,
                GPU,
                RAM,
                Disk,
                Network,
                Motherboard,
                BIOS,
            ]
            for hardware_class in hardware_classes:
                component_name = hardware_class.__name__.lower()
                component_instances[component_name] = hardware_class(self.logger)

            self.logger.info("All hardware components successfully instantiated")
            return tuple(component_instances.values())

        except Exception as initialization_error:
            self.logger.error("Hardware component instantiation failed", exc_info=True)
            raise

    def generate_hardware_report(self, system_name=""):
        """
        Generates a comprehensive (short) hardware report.

        Args:
            system_name (str): Optional system name for report identification.
        """
        self.logger.debug("Starting the hardware report generation process")
        try:
            system, cpu, gpu, ram, disk, network, motherboard, bios = (
                self.hardware_component_instances
            )
            self.report_generator.generate_report(
                system, cpu, gpu, ram, disk, network, motherboard, bios, pc_name=system_name
            )
        except Exception as report_error:
            self.logger.error(
                "Report generation process encountered an error", exc_info=True
            )

    def terminate_noctua_application(self):
        """
        Properly closes the Noctua application, ensuring a clean GUI shutdown.
        """
        self.logger.debug("Initiating Noctua application shutdown sequence")
        self.application_root_window.quit()
        self.application_root_window.destroy()

    def run(self):
        """
        Executes the main loop for the Noctua application, maintaining the GUI.
        """
        self.logger.debug("Noctua application main loop started")
        self.application_root_window.mainloop()
