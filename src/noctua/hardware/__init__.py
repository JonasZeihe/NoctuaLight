"""
Hardware Information Module.

This module provides a class to fetch and aggregate hardware information
from various components like CPU, Disk, GPU, RAM, Motherboard, BIOS, Network, and System.
"""

import logging
from .cpu import CPU
from .disk import Disk
from .gpu import GPU
from .ram import RAM
from .motherboard import Motherboard
from .bios import BIOS
from .network import Network
from .system import System


class HardwareInfo:
    """Class to fetch and aggregate hardware information."""

    def __init__(self, logger: logging.Logger):
        """Initialize the HardwareInfo class with a logger."""
        self.logger = logger
        self.system = System(logger)
        self.cpu = CPU(logger)
        self.disk = Disk(logger)
        self.gpu = GPU(logger)
        self.ram = RAM(logger)
        self.motherboard = Motherboard(logger)
        self.bios = BIOS(logger)
        self.network = Network(logger)
