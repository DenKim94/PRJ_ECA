import customtkinter as ctk
from classes.buttons_class import buttons_frame
from classes.selectDB_class import selectDB_frame
from classes.dataBase_class import dataBase
import classes.generic_widget_class as gen_widgets
import UI_constants


class sharedAppStates:
    def __init__(self):
        self.analysisIsRunning = False
        self.new_db_file_created = False
        self.db_file_removed = False
        self.request_delete_db_elem = False
        self.request_add_db_elem = False
        self.selectedDataBase = None
        self.existing_db_files = [UI_constants.PLACEHOLDER_TEXT]


class App(ctk.CTk):     # analogy: root = ctk.CTk()
    """
    A GUI application to manage energy costs.

    The application provides a graphical user interface to easily manage energy costs.
    It allows users to create, edit and delete databases, containing energy costs data.
    The application displays a graphical representation of the data and allows users to
    add new entries to the database.

    """
    def __init__(self, sharedStates):
        """
        Initializes the application window with the specified UI constants.

        Parameters:
        - UI_constants: A dictionary of UI constants.

        Returns:
        None
        """
        super().__init__()
        print("############## Energy Costs Analyzer ##############")
        try:
            self.sharedAppStates = sharedStates
            self.dataBase = dataBase()

            # MAIN WINDOW
            ctk.set_appearance_mode(UI_constants.DEF_APPEARANCE_MODE)
            ctk.set_default_color_theme(UI_constants.DEF_COLOR_THEME)
            self.title(UI_constants.GUI_TITLE)      # analogy: root.title(UI_constants.GUI_TITLE)
            gen_widgets.newWindow.center_window(self, UI_constants.GUI_WIDTH, UI_constants.GUI_HEIGHT)
            self.minsize(UI_constants.GUI_MIN_WIDTH, UI_constants.GUI_MIN_HEIGHT)
            self.maxsize(UI_constants.GUI_MAX_WIDTH, UI_constants.GUI_MAX_HEIGHT)

            # DEFINE WIDGETS
            self.mainFrame = main_frame(self, self.sharedAppStates, UI_constants)
            self.selectDB = selectDB_frame(self.mainFrame, self.dataBase, UI_constants)
            self.dataBase.remove_dropDownValue_callback = self.selectDB.removeDropDownValue
            self.buttonsFrame = buttons_frame(self.mainFrame, self.dataBase, UI_constants)
            self.buttonsFrame.disable_buttons_callback = self.selectDB.handleDropDownState
            self.buttonsFrame.new_db_created_callback = self.selectDB.updateDropDownValues
            self.selectDB.update_edit_button_state_callback = self.buttonsFrame.updateEditButtonState
            self.selectDB.disable_buttons_callback = self.buttonsFrame.disable_buttons
            self.selectDB.enable_buttons_callback = self.buttonsFrame.enable_buttons
            self.buttonsFrame.update_run_button_state_callback = self.selectDB.updateRunButtonState

            # RUN APP
            self.mainloop()

        except Exception as err:
            print(f">> Unexpected error @App: {err}")


class main_frame(ctk.CTkFrame):
    def __init__(self, parent, sharedStates, UI_constants):
        super().__init__(parent)
        self.sharedAppStates = sharedStates
        self.pack(padx=UI_constants.DEF_MAIN_FRAME_PADDING[0],
                  pady=UI_constants.DEF_MAIN_FRAME_PADDING[1],
                  fill="both", expand=False)
