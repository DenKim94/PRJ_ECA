import customtkinter as ctk
import UI_constants
import classes.generic_widget_class as gen_widgets


class editDatabaseWindow:
    def __init__(self, parent):
        self.DEF_FONT = UI_constants.DEF_FONT
        self.FONT_SIZE_BUTTON = UI_constants.FONT_SIZE_BUTTON
        self.BUTTON_WIDTH = UI_constants.BUTTON_WIDTH
        self.ENTRY_WIDTH = UI_constants.ENTRY_WIDTH
        self.CURSOR_TYPE = UI_constants.CURSOR_TYPE

        self.master = parent
        self.edit_db = gen_widgets.newWindow(parent.master, self.master.min_size_edit_window,
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

    def open_add_elem_window(self):
        print(">> Add new elements window ...")

    def open_delete_elem_window(self):
        print(">> Delete elements window ...")