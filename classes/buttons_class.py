import customtkinter as ctk
import classes.createDB_class as createDB
import classes.editDB_class as editDB
import classes.configure_class as configDB


class buttons_frame(ctk.CTkFrame):
    def __init__(self, parent, dataBase, UI_constants):
        # analogy: frame = ctk.CTkFrame(master=root, fg_color="transparent")
        super().__init__(parent, fg_color="transparent")
        try:
            self.dataBase = dataBase
            self.sharedStates = parent.sharedAppStates

            # CONSTANTS
            self.CURSOR_TYPE = UI_constants.CURSOR_TYPE
            self.DEF_FONT = UI_constants.DEF_FONT
            self.FONT_SIZE_BUTTON = UI_constants.FONT_SIZE_BUTTON
            self.BUTTON_WIDTH = UI_constants.BUTTON_WIDTH
            self.ENTRY_WIDTH = UI_constants.ENTRY_WIDTH

            # PARAMETERS
            self.dropDownValue = ctk.StringVar(value=self.sharedStates.selectedDataBase)
            self.dropDownValue_placeholder = UI_constants.PLACEHOLDER_TEXT
            self.min_size_edit_window = UI_constants.MIN_WINDOW_SIZE
            self.max_size_edit_window = UI_constants.MAX_WINDOW_SIZE

            # WIDGETS
            self.confirm_button = None
            self.db_name_entry = None
            self.number_entry = None
            self.date_entry = None
            self.new_db = None
            self.edit_db = None
            self.update_run_button_state_callback = None
            self.edit_button_enabled = False
            self.config_db = None
            self.add_button = None
            self.delete_button = None
            self.new_db_created_callback = None
            self.disable_buttons_callback = None

            self.pack(padx=0, pady=40, expand=True)

            self.button_create_new_db = ctk.CTkButton(master=self, text="Neue Datenbank",
                                                      cursor=UI_constants.CURSOR_TYPE,
                                                      font=(UI_constants.DEF_FONT, UI_constants.FONT_SIZE_BUTTON),
                                                      width=UI_constants.BUTTON_WIDTH,
                                                      command=self.open_new_db_window)

            self.button_edit_db = ctk.CTkButton(master=self, text="Datenbank bearbeiten",
                                                cursor=UI_constants.CURSOR_TYPE,
                                                font=(UI_constants.DEF_FONT, UI_constants.FONT_SIZE_BUTTON),
                                                width=UI_constants.BUTTON_WIDTH, command=self.open_new_edit_db_window)

            self.button_configure = ctk.CTkButton(master=self, text="Einstellungen", cursor=UI_constants.CURSOR_TYPE,
                                                  font=(UI_constants.DEF_FONT, UI_constants.FONT_SIZE_BUTTON),
                                                  width=UI_constants.BUTTON_WIDTH,
                                                  command=self.open_new_set_conf_window)

            self.button_create_new_db.pack(padx=10, pady=5, side='left', expand=True)
            self.button_edit_db.pack(padx=10, pady=5, side='left', expand=True)
            self.button_configure.pack(padx=10, pady=5, side='left', expand=True)

            self.updateEditButtonState()
        except Exception as err:
            print(f">> Unexpected error @buttons_frame: {err}")

    # METHODS
    def updateEditButtonState(self, isEnabled=False):
        try:
            if isEnabled:
                self.button_edit_db.configure(state="normal")
            else:
                self.button_edit_db.configure(state="disabled")

            self.edit_button_enabled = isEnabled

        except Exception as err:
            print(f">> Unexpected error @updateEditButtonState: {err}")

    def open_new_db_window(self):
        self.new_db = createDB.newDatabaseWindow(self)

    def enable_buttons(self):
        try:
            current_widget = self.focus_get()
            current_widget.destroy()
            self.button_create_new_db.configure(state="normal")
            self.button_configure.configure(state="normal")

            if self.update_run_button_state_callback is not None:
                self.update_run_button_state_callback(disable_run_button=False)

            if self.edit_button_enabled:
                self.button_edit_db.configure(state="normal")

            if self.disable_buttons_callback:
                self.disable_buttons_callback(False)

        except AttributeError:
            print(">> Warning @enable_buttons(): No widget in focus!")

    def disable_buttons(self):
        self.button_create_new_db.configure(state="disabled")
        self.button_edit_db.configure(state="disabled")
        self.button_configure.configure(state="disabled")

        if self.update_run_button_state_callback is not None:
            self.update_run_button_state_callback(disable_run_button=True)

        if self.disable_buttons_callback:
            self.disable_buttons_callback(True)

    def open_new_edit_db_window(self):
        self.edit_db = editDB.editDatabaseWindow(self)

    def open_new_set_conf_window(self):
        self.config_db = configDB.configWindow(self, self.dataBase)
