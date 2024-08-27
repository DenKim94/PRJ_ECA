import customtkinter as ctk
import UI_constants


class newWindow:
    def __init__(self, parent):
        # WINDOW SIZE
        self.GUI_MIN_WIDTH = UI_constants.GUI_MIN_WIDTH
        self.GUI_MIN_HEIGHT = UI_constants.GUI_MIN_HEIGHT
        self.GUI_MAX_WIDTH = UI_constants.GUI_MAX_WIDTH
        self.GUI_MAX_HEIGHT = UI_constants.GUI_MAX_HEIGHT

        self.window = ctk.CTkToplevel(parent)
        self.window.geometry(parent.master.geometry())
        self.window.minsize(self.GUI_MIN_WIDTH, self.GUI_MIN_HEIGHT)
        self.window.maxsize(self.GUI_MAX_WIDTH, self.GUI_MAX_HEIGHT)

        self.container = ctk.CTkFrame(master=self.window, fg_color="transparent")
        self.container.pack(side='top', padx=10, pady=10, expand=True)
