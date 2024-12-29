import sys
import tkinter as tk
from tkinter import ttk, PhotoImage, messagebox
import os
from noctua.logger import Logger


class NoctuaGUI:
    """
    The NoctuaGUI class is responsible for managing the graphical interface of Noctua,
    including component selection, logging options, and triggering the report generation.
    """

    def __init__(
        self,
        root_window,
        component_selection_vars,
        select_all_components_var,
        detailed_report_option_var,
        report_generation_callback,
        application_closure_callback,
    ):
        """
        Initializes the Noctua GUI interface with the provided settings.
        """
        self.root_window = root_window
        self.component_selection_vars = component_selection_vars
        self.select_all_components_var = select_all_components_var
        self.detailed_report_option_var = detailed_report_option_var
        self.report_generation_callback = report_generation_callback
        self.application_closure_callback = application_closure_callback

        self.logging_option_var = tk.BooleanVar(value=False)
        self.logger = None

        self.initialize_gui()

    def initialize_gui(self):
        """
        Initializes and configures the GUI, setting up layout, components, and event handlers.
        """
        self.configure_main_window()
        self.set_background_image("background_main.png")
        self.build_main_interface_frame()
        self.create_interface_elements()

    def configure_main_window(self):
        """
        Configures the main window's properties, including geometry, title, and background color.
        """
        self.root_window.geometry("800x600")
        self.root_window.title("Noctua Hardware Report Application")
        self.root_window.configure(background="#f4f4f4")

    def set_background_image(self, image_filename):
        """
        Loads and sets a background image for the main window.
        """
        image_path = self.resolve_image_path(image_filename)
        if image_path:
            self.background_image = PhotoImage(file=image_path)
            background_label = tk.Label(self.root_window, image=self.background_image)
            background_label.place(relwidth=1, relheight=1)

    def build_main_interface_frame(self):
        """
        Constructs the main frame that organizes and contains the GUI content.
        """
        self.main_frame = tk.Frame(
            self.root_window, bg="white", padx=20, pady=20, relief="raised", bd=5
        )
        self.main_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

    def create_interface_elements(self):
        """
        Assembles all interface elements, such as labels, text entries, checkboxes, and buttons.
        """
        self.create_welcome_label()
        self.create_pc_name_entry_field()
        self.create_logging_checkbox()
        self.create_component_selection_checkbuttons()
        self.create_action_buttons()

    def create_welcome_label(self):
        """
        Creates a welcome label to guide the user on the application's purpose.
        """
        welcome_label = tk.Label(
            self.main_frame,
            text="Welcome to Noctua!\nAnalyze your system's hardware information.",
            wraplength=350,
            bg="white",
            font=("Arial", 14, "bold"),
            fg="#333",
            justify="center",
        )
        welcome_label.grid(row=0, column=0, columnspan=2, pady=(10, 20))

    def create_pc_name_entry_field(self):
        """
        Creates a text entry field for inputting the PC name.
        """
        pc_name_label = tk.Label(
            self.main_frame, text="PC Name:", bg="white", font=("Arial", 12)
        )
        pc_name_label.grid(row=1, column=0, sticky="e", padx=10, pady=10)
        self.pc_name_entry_field = tk.Entry(
            self.main_frame, width=30, font=("Arial", 12), bd=2, relief="groove"
        )
        self.pc_name_entry_field.grid(row=1, column=1, sticky="w", padx=10, pady=10)

    def create_logging_checkbox(self):
        """
        Adds a checkbox to enable or disable logging.
        """
        logging_checkbox = ttk.Checkbutton(
            self.main_frame,
            text="Enable Logging",
            variable=self.logging_option_var,
        )
        logging_checkbox.grid(row=2, column=0, columnspan=2, pady=10)

    def create_component_selection_checkbuttons(self):
        """
        Creates checkbuttons for each component selection option.
        """
        self.create_select_all_components_checkbutton()
        self.create_detailed_report_option_checkbutton()
        self.create_individual_component_checkbuttons()

    def create_select_all_components_checkbutton(self):
        """
        Adds a checkbutton to select all hardware components for the report.
        """
        self.select_all_components_var.set(True)
        select_all_checkbox = ttk.Checkbutton(
            self.main_frame,
            text="Select All Components",
            variable=self.select_all_components_var,
            command=self.toggle_select_all_components,
        )
        select_all_checkbox.grid(row=3, column=0, columnspan=2, pady=10)

    def create_detailed_report_option_checkbutton(self):
        """
        Adds a checkbutton for enabling detailed report generation.
        """
        self.detailed_report_option_var.set(False)
        detailed_report_checkbox = ttk.Checkbutton(
            self.main_frame,
            text="Generate Detailed Report",
            variable=self.detailed_report_option_var,
            command=self.toggle_detailed_report_option,
        )
        detailed_report_checkbox.grid(row=4, column=0, columnspan=2, pady=10)

    def create_individual_component_checkbuttons(self):
        """
        Creates individual checkbuttons for each selectable hardware component.
        """
        component_frame = tk.Frame(self.main_frame, bg="white")
        component_frame.grid(row=5, column=0, columnspan=2, pady=10)

        for index, (component_name, component_var) in enumerate(
            self.component_selection_vars.items()
        ):
            row, col = divmod(index, 2)
            checkbutton = ttk.Checkbutton(
                component_frame,
                text=component_name.capitalize(),
                variable=component_var,
            )
            checkbutton.grid(row=row, column=col, padx=10, pady=5, sticky="w")

    def create_action_buttons(self):
        """
        Adds action buttons for generating the report and closing the application.
        """
        button_frame = tk.Frame(self.main_frame, bg="white")
        button_frame.grid(row=6, column=0, columnspan=2, pady=20)

        generate_button = ttk.Button(
            button_frame,
            text="Generate Report",
            command=self.confirm_report_generation,
        )
        generate_button.grid(row=0, column=0, padx=10)

        close_button = ttk.Button(
            button_frame, text="Close", command=self.application_closure_callback
        )
        close_button.grid(row=0, column=1, padx=10)

    def confirm_report_generation(self):
        """
        Validates component selection and initiates report generation.
        """
        if not self.validate_component_selection():
            result = messagebox.askokcancel(
                "No Components Selected",
                "No components selected. Generate an empty report?",
            )
            if not result:
                return

        if self.logging_option_var.get():
            self.logger = Logger(log_to_file=True)
            self.logger.info("Logging enabled from GUI")

        self.show_loading_screen("background_loading.png")

    def validate_component_selection(self):
        """
        Validates whether at least one component is selected for the report.
        """
        return (
            any(var.get() for var in self.component_selection_vars.values())
            or self.select_all_components_var.get()
        )

    def show_loading_screen(self, image_filename):
        """
        Displays a loading screen with a specified background image during report generation.
        """
        loading_image_path = self.resolve_image_path(image_filename)
        if loading_image_path:
            self.loading_image = PhotoImage(file=loading_image_path)
            loading_label = tk.Label(self.root_window, image=self.loading_image)
            loading_label.place(relwidth=1, relheight=1)
        self.root_window.after(100, self.generate_report)

    def generate_report(self):
        """
        Executes the report generation process and shows completion dialog.
        """
        try:
            pc_name = self.pc_name_entry_field.get()
            self.report_generation_callback(pc_name)
        except Exception as error:
            if self.logger:
                self.logger.error(f"Error during report generation: {error}")
            else:
                print(f"Error: {error}")
        finally:
            self.display_report_completion_message()

    def display_report_completion_message(self):
        """
        Shows a dialog indicating report generation completion.
        """
        report_path = "result/hardware_report.md"
        result = messagebox.askokcancel(
            "Report Generated",
            f"Report generated successfully:\n{report_path}\n\nClose the application?",
        )
        if result:
            self.application_closure_callback()

    def resolve_image_path(self, filename):
        """
        Determines the absolute path of an image file.
        """
        base_dir = (
            os.path.join(sys._MEIPASS, "resources", "images")  # For compiled mode
            if getattr(sys, "frozen", False)
            else os.path.abspath(
                os.path.join(
                    os.path.dirname(__file__), "..", "..", "resources", "images"
                )  # For local mode
            )
        )
        image_path = os.path.join(base_dir, filename)
        return image_path if os.path.exists(image_path) else None

    def toggle_select_all_components(self):
        """
        Toggles the selection state of all component checkbuttons.
        """
        state = self.select_all_components_var.get()
        for var in self.component_selection_vars.values():
            var.set(state)

    def toggle_detailed_report_option(self):
        """
        Toggles the selection state for generating a detailed report.
        """
        state = self.detailed_report_option_var.get()
        for var in self.component_selection_vars.values():
            var.set(state)
