import customtkinter as ctk
from classes.buttons_class import buttons_frame
from classes.selectDB_class import selectDB_frame
from classes.dataBase_class import dataBase


class sharedAppStates:
    def __init__(self, UI_constants):
        self.analysisIsRunning = False
        self.new_db_file_created = False
        self.request_delete_db_elem = False
        self.request_add_db_elem = False
        self.existing_db_files = [UI_constants.PLACEHOLDER_TEXT]


class App(ctk.CTk):     # analogy: root = ctk.CTk()
    def __init__(self, sharedStates, UI_constants):
        """
        Initializes the application window with the specified UI constants.

        Parameters:
        - UI_constants: A dictionary of UI constants.

        Returns:
        None
        """
        super().__init__()
        self.sharedAppStates = sharedStates
        self.dataBase = dataBase()

        # MAIN WINDOW
        ctk.set_appearance_mode(UI_constants.DEF_APPEARANCE_MODE)
        ctk.set_default_color_theme(UI_constants.DEF_COLOR_THEME)
        self.title(UI_constants.GUI_TITLE)      # analogy: root.title(UI_constants.GUI_TITLE)
        self.centerUI_geometry(UI_constants.GUI_WIDTH, UI_constants.GUI_HEIGHT)
        self.minsize(UI_constants.GUI_MIN_WIDTH, UI_constants.GUI_MIN_HEIGHT)
        self.maxsize(UI_constants.GUI_MAX_WIDTH, UI_constants.GUI_MAX_HEIGHT)

        # DEFINE WIDGETS
        self.mainFrame = main_frame(self, self.sharedAppStates, UI_constants)
        self.selectDB = selectDB_frame(self.mainFrame, self.dataBase, UI_constants)
        self.buttonsFrame = buttons_frame(self.mainFrame, self.dataBase, UI_constants)
        self.buttonsFrame.disable_buttons_callback = self.selectDB.handleDropDownState
        self.buttonsFrame.new_db_created_callback = self.selectDB.updateDropDownValues

        # RUN APP
        self.mainloop()

    def getScreenSize(self):
        try:
            screenWidth = self.winfo_screenwidth()
            screenHeight = self.winfo_screenheight()

            return [screenWidth, screenHeight]

        except Exception as err:
            print(f"Unexpected error @getScreenSize(): {err}")

    def centerUI_geometry(self, windowWidth, windowHeight):
        try:
            [screenWidth, screenHeight] = self.getScreenSize()
            offset_x = int(abs((windowWidth / 2) - (screenWidth / 2)))
            offset_y = int(abs((windowHeight / 2) - (screenHeight / 2)))
            self.geometry(f"{windowWidth}x{windowHeight}+{offset_x}+{offset_y}")

        except Exception as err:
            print(f"Unexpected error @centerUI(): {err}")


class main_frame(ctk.CTkFrame):
    def __init__(self, parent, sharedStates, UI_constants):
        super().__init__(parent)
        self.sharedAppStates = sharedStates
        self.pack(padx=UI_constants.DEF_MAIN_FRAME_PADDING[0],
                  pady=UI_constants.DEF_MAIN_FRAME_PADDING[1],
                  fill="both", expand=False)





