import customtkinter as ctk
import datetime


class buttons_frame(ctk.CTkFrame):
    def __init__(self, parent, dataBase, UI_constants):
        # analogy: frame = ctk.CTkFrame(master=root, fg_color="transparent")
        super().__init__(parent, fg_color="transparent")
        self.dataBase = dataBase

        # CONSTANT VARIABLES
        self.GUI_MIN_WIDTH = UI_constants.GUI_MIN_WIDTH
        self.GUI_MIN_HEIGHT = UI_constants.GUI_MIN_HEIGHT
        self.GUI_MAX_WIDTH = UI_constants.GUI_MAX_WIDTH
        self.GUI_MAX_HEIGHT = UI_constants.GUI_MAX_HEIGHT
        self.CURSOR_TYPE = UI_constants.CURSOR_TYPE
        self.DEF_FONT = UI_constants.DEF_FONT
        self.FONT_SIZE_BUTTON = UI_constants.FONT_SIZE_BUTTON
        self.BUTTON_WIDTH = UI_constants.BUTTON_WIDTH
        self.ENTRY_WIDTH_DB = UI_constants.ENTRY_WIDTH_DB
        self.ENTRY_WIDTH = UI_constants.ENTRY_WIDTH
        self.PLACEHOLDER_DB_NAME = UI_constants.PLACEHOLDER_DB_NAME
        # WIDGETS
        self.request_delete_db_elem = False
        self.request_add_db_elem = False
        self.error_label = None
        self.confirm_button = None
        self.db_name_entry = None
        self.number_entry = None
        self.date_entry = None
        self.new_window = None
        self.callback = None

        self.pack(padx=0, pady=50, expand=True)

        self.button_create_new_db = ctk.CTkButton(master=self, text="Neue Datenbank",
                                                  cursor=UI_constants.CURSOR_TYPE,
                                                  font=(UI_constants.DEF_FONT, UI_constants.FONT_SIZE_BUTTON),
                                                  width=UI_constants.BUTTON_WIDTH,
                                                  command=self.open_new_db_window)

        self.button_edit_db = ctk.CTkButton(master=self, text="Datenbank bearbeiten", cursor=UI_constants.CURSOR_TYPE,
                                            font=(UI_constants.DEF_FONT, UI_constants.FONT_SIZE_BUTTON),
                                            width=UI_constants.BUTTON_WIDTH, command=self.open_new_edit_db_window)

        self.button_configure = ctk.CTkButton(master=self, text="Einstellungen", cursor=UI_constants.CURSOR_TYPE,
                                              font=(UI_constants.DEF_FONT, UI_constants.FONT_SIZE_BUTTON),
                                              width=UI_constants.BUTTON_WIDTH, command=self.open_new_set_conf_window)

        self.button_create_new_db.pack(padx=10, pady=10, side='left', expand=True)
        self.button_edit_db.pack(padx=10, pady=10, side='left', expand=True)
        self.button_configure.pack(padx=10, pady=10, side='left', expand=True)

    def open_new_db_window(self):
        print(">> Create new database ...")
        self.new_window = ctk.CTkToplevel(self.master)
        self.new_window.title("Neue Datenbank erstellen")
        self.new_window.geometry(self.master.master.geometry())
        self.new_window.minsize(self.GUI_MIN_WIDTH, self.GUI_MIN_HEIGHT)
        self.new_window.maxsize(self.GUI_MAX_WIDTH, self.GUI_MAX_HEIGHT)
        self.disable_buttons()
        # Create a container to hold the input fields
        container = ctk.CTkFrame(master=self.new_window, fg_color="transparent")
        container.pack(side='top', padx=10, pady=10, expand=True)

        # Create the first input field (database name)
        frame = ctk.CTkFrame(master=container, fg_color="transparent")
        frame.pack(side='top', padx=5, pady=5)
        db_name_label = ctk.CTkLabel(master=frame, font=(self.DEF_FONT, self.FONT_SIZE_BUTTON),
                                     text="Name der neuen Datenbank:",
                                     width=self.ENTRY_WIDTH)

        db_name_label.pack(padx=5, pady=5)
        self.db_name_entry = ctk.CTkEntry(master=frame,
                                          width=self.ENTRY_WIDTH_DB,
                                          justify="center",
                                          placeholder_text=self.PLACEHOLDER_DB_NAME)
        self.db_name_entry.pack(padx=5, pady=5, expand=True)

        # Create the second and third input fields (date and number)
        frame = ctk.CTkFrame(master=container, fg_color="transparent")
        frame.pack(side='top', padx=5, pady=5)
        number_label = ctk.CTkLabel(master=frame, font=(self.DEF_FONT, self.FONT_SIZE_BUTTON),
                                    text="Zählerstand (Initialwert) in kWh:")
        number_label.pack(side='top', padx=5, pady=5)
        self.number_entry = ctk.CTkEntry(master=frame,
                                         width=self.ENTRY_WIDTH,
                                         justify="center")
        self.number_entry.pack(side='top', padx=5, pady=5, expand=True)
        self.number_entry.configure(validate="key",
                                    validatecommand=(self.new_window.register(self.validate_number), '%P'))

        date_label = ctk.CTkLabel(master=frame, font=(self.DEF_FONT, self.FONT_SIZE_BUTTON),
                                  text="Datum:", width=self.ENTRY_WIDTH)
        date_label.pack(side='top', padx=5, pady=5)
        self.date_entry = ctk.CTkEntry(master=frame,
                                       width=self.ENTRY_WIDTH,
                                       justify="center")
        self.date_entry.configure(validate="focusout",
                                  validatecommand=(self.new_window.register(self.validate_date), '%P'))
        self.date_entry.pack(side='top', padx=5, pady=5, expand=True)
        self.date_entry.insert(0, datetime.datetime.now().strftime("%d.%m.%Y"))

        # Create the confirm button
        self.confirm_button = ctk.CTkButton(master=container, text="Bestätigen",
                                            state="normal",
                                            cursor=self.CURSOR_TYPE,
                                            font=(self.DEF_FONT, self.FONT_SIZE_BUTTON),
                                            width=self.BUTTON_WIDTH,
                                            command=self.confirm_input)

        self.confirm_button.pack(side='bottom', padx=5, pady=10)

        self.error_label = ctk.CTkLabel(master=container, text="", text_color="red")
        self.error_label.pack(side='bottom', padx=5, pady=0)

        self.new_window.protocol("WM_DELETE_WINDOW", self.enable_buttons)
        # Set up the check for input fields
        self.db_name_entry.after(100, self.check_input_fields)
        self.date_entry.after(100, self.check_input_fields)
        self.number_entry.after(100, self.check_input_fields)

    def check_input_fields(self):
        if (self.db_name_entry.get() != "" and
                self.db_name_entry.get() != self.PLACEHOLDER_DB_NAME and
                self.validate_date(self.date_entry.get()) and
                self.validate_number(self.number_entry.get())):
            self.error_label.configure(text="")
            return True
        else:
            return False

    def validate_date(self, value):
        try:
            datetime.datetime.strptime(value, "%d.%m.%Y")
            self.error_label.configure(text="")
            return True
        except ValueError:
            self.error_label.configure(text="Ungültiges Datum!")
            return False

    def confirm_input(self):
        validInputs = self.check_input_fields()
        if validInputs:
            self.error_label.configure(text="")
            self.dataBase.create_database(self.db_name_entry.get(),
                                          self.number_entry.get(),
                                          self.date_entry.get())

            self.confirm_button.configure(state="disabled")

        else:
            print(">> Invalid input values!")
            self.error_label.configure(text="Ungültige Eingaben!")

    def validate_number(self, value):
        if value == "":
            return True
        try:
            float(value)
            self.error_label.configure(text="")
            return True
        except ValueError:
            self.error_label.configure(text="Ungültige Eingabe!")
            return False

    def enable_buttons(self):
        self.new_window.destroy()
        self.button_create_new_db.configure(state="normal")
        self.button_edit_db.configure(state="normal")
        self.button_configure.configure(state="normal")
        if self.callback:
            self.callback(False)

    def disable_buttons(self):
        self.button_create_new_db.configure(state="disabled")
        self.button_edit_db.configure(state="disabled")
        self.button_configure.configure(state="disabled")
        if self.callback:
            self.callback(True)

    def open_new_edit_db_window(self):
        print(">> Edit database ...")


    def open_new_set_conf_window(self):
        print(">> Configure ...")
