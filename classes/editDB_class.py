import customtkinter as ctk
import UI_constants
import classes.generic_widget_class as gen_widgets
import datetime


class editDatabaseWindow:
    def __init__(self, parent):
        # CONSTANTS
        self.DEF_FONT = UI_constants.DEF_FONT
        self.FONT_SIZE_BUTTON = UI_constants.FONT_SIZE_BUTTON
        self.BUTTON_WIDTH = UI_constants.BUTTON_WIDTH
        self.ENTRY_WIDTH = UI_constants.ENTRY_WIDTH
        self.CURSOR_TYPE = UI_constants.CURSOR_TYPE
        self.min_size_add_window = UI_constants.MIN_WINDOW_SIZE
        self.max_size_add_window = UI_constants.MAX_WINDOW_SIZE
        self.max_size_delete_window = UI_constants.MAX_WINDOW_SIZE
        self.max_size_delete_window = UI_constants.MAX_WINDOW_SIZE
        self.energy_value = None
        self.date_value = None

        # WIDGETS
        self.add_db_elem = None
        self.number_entry = None
        self.date_entry = None
        self.error_label = None
        self.add_button = None
        self.delete_db = None
        self.remove_elem_button = None
        self.delete_db_button = None

        try:
            self.master = parent
            self.edit_db = gen_widgets.newWindow(self.master.master, self.master.min_size_edit_window,
                                                 self.master.max_size_edit_window)
            self.edit_db.window.title("Gewählte Datenbank bearbeiten")
            self.master.disable_buttons()
            gen_widgets.newWindow.center_window(self.edit_db.window, self.master.max_size_edit_window[0],
                                                self.master.max_size_edit_window[1])

            frame = ctk.CTkFrame(master=self.edit_db.container, fg_color="transparent")
            frame.pack(side='top', padx=5, pady=5)
            edit_label = ctk.CTkLabel(master=frame, font=(self.DEF_FONT, self.FONT_SIZE_BUTTON),
                                      text="Bitte auswählen:",
                                      width=self.ENTRY_WIDTH)
            edit_label.pack(side='top', padx=5, pady=5)
            self.add_button = ctk.CTkButton(master=self.edit_db.container, text="Daten hinzufügen",
                                            state="normal",
                                            cursor=self.CURSOR_TYPE,
                                            font=(self.DEF_FONT, self.FONT_SIZE_BUTTON),
                                            width=self.BUTTON_WIDTH,
                                            command=self.open_add_elem_window)

            self.add_button.pack(side='left', padx=10, pady=5)
            self.delete_button = ctk.CTkButton(master=self.edit_db.container, text="Daten entfernen",
                                               state="normal",
                                               cursor=self.CURSOR_TYPE,
                                               font=(self.DEF_FONT, self.FONT_SIZE_BUTTON),
                                               width=self.BUTTON_WIDTH,
                                               command=self.open_delete_elem_window)
            self.delete_button.pack(side='left', padx=10, pady=5)
            self.edit_db.window.protocol("WM_DELETE_WINDOW", self.master.enable_buttons)

        except Exception as err:
            raise Exception(f">> Unexpected error @editDatabaseWindow: {err}")

    def open_add_elem_window(self):
        try:
            self.edit_db.window.destroy()
            self.add_db_elem = gen_widgets.newWindow(self.master.master, self.min_size_add_window,
                                                     self.max_size_add_window)
            self.add_db_elem.window.title("Daten hinzufügen")
            gen_widgets.newWindow.center_window(self.add_db_elem.window, self.master.max_size_edit_window[0],
                                                self.master.max_size_edit_window[1])

            frame = ctk.CTkFrame(master=self.add_db_elem.container, fg_color="transparent")
            frame.pack(side='top', padx=5, pady=5)

            self.error_label = ctk.CTkLabel(master=self.add_db_elem.container, text="", text_color="red")

            date_label = ctk.CTkLabel(master=frame, font=(self.DEF_FONT, self.FONT_SIZE_BUTTON),
                                      text="Datum:", width=self.ENTRY_WIDTH)
            date_label.pack(side='top', padx=5, pady=5)
            self.date_entry = ctk.CTkEntry(master=frame,
                                           width=self.ENTRY_WIDTH,
                                           justify="center")
            self.date_entry.configure(validate="focusout",
                                      validatecommand=(self.add_db_elem.window.register(
                                          lambda value: gen_widgets.newWindow.validate_date(
                                              self.error_label, self.date_entry.get())), '%P'))

            self.date_entry.pack(side='top', padx=5, pady=5, expand=True)
            self.date_entry.insert(0, datetime.datetime.now().strftime("%d.%m.%Y"))

            number_label = ctk.CTkLabel(master=frame, font=(self.DEF_FONT, self.FONT_SIZE_BUTTON),
                                        text="Zählerstand in kWh:")
            number_label.pack(side='top', padx=5, pady=5)
            self.number_entry = ctk.CTkEntry(master=frame,
                                             width=self.ENTRY_WIDTH,
                                             justify="center")
            self.number_entry.pack(side='top', padx=5, pady=5, expand=True)
            self.number_entry.configure(validate="focusout",
                                        validatecommand=(self.add_db_elem.window.register(
                                            lambda value: gen_widgets.newWindow.validate_number(
                                                self.error_label, self.number_entry.get())), '%P'))

            self.error_label.pack(side='top', padx=5, pady=0)

            self.add_button = ctk.CTkButton(master=self.add_db_elem.container, text="OK",
                                            state="normal",
                                            cursor=self.CURSOR_TYPE,
                                            font=(self.DEF_FONT, self.FONT_SIZE_BUTTON),
                                            width=self.BUTTON_WIDTH,
                                            command=self.add_input)

            self.add_button.pack(side='bottom', padx=5, pady=5)
            self.add_db_elem.window.protocol("WM_DELETE_WINDOW", self.master.enable_buttons)

        except Exception as err:
            raise Exception(f">> Unexpected error @open_add_elem_window: {err}")

    def add_input(self):
        try:
            self.error_label.configure(text="")
            if (gen_widgets.newWindow.validate_date(self.error_label, self.date_entry.get()) and
                    gen_widgets.newWindow.validate_number(self.error_label, self.number_entry.get())):
                selected_db_name = self.master.sharedStates.selectedDataBase
                self.energy_value = float(self.number_entry.get())
                self.date_value = self.date_entry.get()

                data_isValid = self.master.dataBase.add_data_to_existing_db(selected_db_name,
                                                                            self.date_value,
                                                                            self.energy_value)
                if not data_isValid:
                    self.error_label.configure(text="Ungültiger Wert!", text_color="red")
                else:
                    self.error_label.configure(text="Eintrag wurde hinzugefügt.", text_color="green")

            else:
                self.error_label.configure(text="Ungültige Eingabe!")

        except Exception as err:
            raise Exception(f">> Unexpected error @add_input: {err}")

    def open_delete_elem_window(self):
        try:
            self.edit_db.window.destroy()
            self.delete_db = gen_widgets.newWindow(self.master.master, self.master.min_size_edit_window,
                                                   self.master.max_size_edit_window)
            self.delete_db.window.title("Daten entfernen")
            gen_widgets.newWindow.center_window(self.delete_db.window, self.master.max_size_edit_window[0],
                                                self.master.max_size_edit_window[1])

            frame = ctk.CTkFrame(master=self.delete_db.container, fg_color="transparent")
            frame.pack(side='top', padx=5, pady=5)
            edit_label = ctk.CTkLabel(master=frame, font=(self.DEF_FONT, self.FONT_SIZE_BUTTON),
                                      text="Bitte auswählen:",
                                      width=self.ENTRY_WIDTH)

            self.error_label = ctk.CTkLabel(master=self.delete_db.container, text="", text_color="red")

            edit_label.pack(side='top', padx=5, pady=5)
            self.remove_elem_button = ctk.CTkButton(master=self.delete_db.container, text="Letzten Eintrag löschen",
                                                    state="normal",
                                                    cursor=self.CURSOR_TYPE,
                                                    font=(self.DEF_FONT, self.FONT_SIZE_BUTTON),
                                                    width=self.BUTTON_WIDTH,
                                                    command=self.delete_last_entry_from_db)

            self.remove_elem_button.pack(side='top', padx=5, pady=5)
            self.delete_db_button = ctk.CTkButton(master=self.delete_db.container, text="Datenbank löschen",
                                                  state="normal",
                                                  cursor=self.CURSOR_TYPE,
                                                  font=(self.DEF_FONT, self.FONT_SIZE_BUTTON),
                                                  width=self.BUTTON_WIDTH,
                                                  fg_color="#FF0000",
                                                  hover_color="#8B0A0A",
                                                  command=self.delete_selected_db)

            self.delete_db_button.pack(side='top', padx=5, pady=5)
            self.delete_db.window.protocol("WM_DELETE_WINDOW", self.master.enable_buttons)

            self.error_label.pack(side='top', padx=5, pady=0)

        except Exception as err:
            raise Exception(f">> Unexpected error @open_delete_elem_window: {err}")

    def delete_last_entry_from_db(self):
        try:
            last_elem_id = self.master.dataBase.delete_last_entry_from_db(self.master.sharedStates.selectedDataBase)
            if last_elem_id is not None:
                self.error_label.configure(text="Letzter Eintrag wurde gelöscht.", text_color="green")
            else:
                self.error_label.configure(text="Kein Eintrag wurde gefunden.", text_color="red")

        except Exception as err:

            raise Exception(f">> Unexpected error @delete_last_entry_from_db: {err}")

    def delete_selected_db(self):
        try:
            self.master.dataBase.delete_selected_database(self.master.sharedStates.selectedDataBase)
            self.master.enable_buttons()
            self.delete_db.window.destroy()

        except Exception as err:
            raise Exception(f">> Unexpected error @delete_selected_db: {err}")