import customtkinter as ctk
import datetime
import UI_constants
import classes.generic_widget_class as gen_widgets


class newDatabaseWindow:
    def __init__(self, parent):
        # CONSTANTS
        self.DEF_FONT = UI_constants.DEF_FONT
        self.FONT_SIZE_BUTTON = UI_constants.FONT_SIZE_BUTTON
        self.BUTTON_WIDTH = UI_constants.BUTTON_WIDTH
        self.ENTRY_WIDTH = UI_constants.ENTRY_WIDTH
        self.ENTRY_WIDTH_DB = UI_constants.ENTRY_WIDTH_DB
        self.PLACEHOLDER_DB_NAME = UI_constants.PLACEHOLDER_DB_NAME
        self.CURSOR_TYPE = UI_constants.CURSOR_TYPE

        try:
            # Create the first input field (database name)
            self.master = parent
            self.new_db = gen_widgets.newWindow(parent.master)
            self.new_db.window.title("Neue Datenbank erstellen")
            self.master.disable_buttons()

            frame = ctk.CTkFrame(master=self.new_db.container, fg_color="transparent")
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

            self.error_label = ctk.CTkLabel(master=self.new_db.container, text="", text_color="red")

            # Create the second and third input fields (date and number)
            frame = ctk.CTkFrame(master=self.new_db.container, fg_color="transparent")
            frame.pack(side='top', padx=5, pady=5)
            number_label = ctk.CTkLabel(master=frame, font=(self.DEF_FONT, self.FONT_SIZE_BUTTON),
                                        text="Zählerstand (Initialwert) in kWh:")
            number_label.pack(side='top', padx=5, pady=5)
            self.number_entry = ctk.CTkEntry(master=frame,
                                             width=self.ENTRY_WIDTH,
                                             justify="center")
            self.number_entry.pack(side='top', padx=5, pady=5, expand=True)
            self.number_entry.configure(validate="focusout",
                                        validatecommand=(self.new_db.window.register(
                                                         lambda value: gen_widgets.newWindow.validate_number(
                                                             self.error_label, self.number_entry.get())), '%P'))

            date_label = ctk.CTkLabel(master=frame, font=(self.DEF_FONT, self.FONT_SIZE_BUTTON),
                                      text="Datum:", width=self.ENTRY_WIDTH)
            date_label.pack(side='top', padx=5, pady=5)
            self.date_entry = ctk.CTkEntry(master=frame,
                                           width=self.ENTRY_WIDTH,
                                           justify="center")
            self.date_entry.configure(validate="focusout",
                                      validatecommand=(self.new_db.window.register(
                                          lambda value: gen_widgets.newWindow.validate_date(
                                              self.error_label, self.date_entry.get())), '%P'))

            self.date_entry.pack(side='top', padx=5, pady=5, expand=True)
            self.date_entry.insert(0, datetime.datetime.now().strftime("%d.%m.%Y"))

            # Create the confirm button
            self.confirm_button = ctk.CTkButton(master=self.new_db.container, text="Bestätigen",
                                                state="normal",
                                                cursor=self.CURSOR_TYPE,
                                                font=(self.DEF_FONT, self.FONT_SIZE_BUTTON),
                                                width=self.BUTTON_WIDTH,
                                                command=self.confirm_input)

            self.confirm_button.pack(side='bottom', padx=5, pady=10)

            self.error_label.pack(side='bottom', padx=5, pady=0)

            self.new_db.window.protocol("WM_DELETE_WINDOW", self.master.enable_buttons)
            # Set up the check for input fields
            self.db_name_entry.after(100, self.check_input_fields)
            self.date_entry.after(100, self.check_input_fields)
            self.number_entry.after(100, self.check_input_fields)

        except Exception as err:
            print(f">> Unexpected error @newDatabaseWindow: {err}")

    def check_input_fields(self):
        if (self.db_name_entry.get() != "" and
                self.db_name_entry.get() != self.PLACEHOLDER_DB_NAME and
                gen_widgets.newWindow.validate_date(self.error_label, self.date_entry.get()) and
                gen_widgets.newWindow.validate_number(self.error_label, self.number_entry.get())):
            self.error_label.configure(text="")
            return True
        else:
            return False

    def confirm_input(self):
        validInputs = self.check_input_fields()
        if validInputs:
            self.error_label.configure(text="")
            self.master.dataBase.create_database(self.db_name_entry.get(),
                                                 self.number_entry.get(),
                                                 self.date_entry.get())

            self.master.sharedStates.new_db_file_created = True

            if self.master.new_db_created_callback:
                self.master.new_db_created_callback()

            self.confirm_button.configure(state="disabled")

        else:
            self.master.sharedStates.new_db_file_created = False

