import customtkinter as ctk
import UI_constants


class newWindow:
    def __init__(self, parent, min_size=None, max_size=None):
        try:
            # WINDOW SIZE
            if min_size is None:
                min_size = [UI_constants.GUI_MIN_WIDTH, UI_constants.GUI_MIN_HEIGHT]

            if max_size is None:
                max_size = [UI_constants.GUI_MAX_WIDTH, UI_constants.GUI_MAX_HEIGHT]

            self.GUI_MIN_WIDTH = min_size[0]
            self.GUI_MIN_HEIGHT = min_size[1]
            self.GUI_MAX_WIDTH = max_size[0]
            self.GUI_MAX_HEIGHT = max_size[1]

            self.window = ctk.CTkToplevel(parent)
            self.window.geometry(parent.master.geometry())
            self.window.minsize(self.GUI_MIN_WIDTH, self.GUI_MIN_HEIGHT)
            self.window.maxsize(self.GUI_MAX_WIDTH, self.GUI_MAX_HEIGHT)

            self.container = ctk.CTkFrame(master=self.window, fg_color="transparent")
            self.container.pack(side='top', padx=10, pady=10, expand=True)

        except Exception as err:
            print(f">> Unexpected error @newWindow: {err}")

    @staticmethod
    def center_window(windowObj, windowWidth, windowHeight):
        try:
            [screenWidth, screenHeight] = newWindow.getScreenSize(windowObj)
            offset_x = int(abs((windowWidth / 2) - (screenWidth / 2)))
            offset_y = int(abs((windowHeight / 2) - (screenHeight / 2)))
            windowObj.geometry(f"{windowWidth}x{windowHeight}+{offset_x}+{offset_y}")

        except Exception as err:
            print(f"Unexpected error @centerUI(): {err}")

    @staticmethod
    def getScreenSize(windowObj):
        try:
            screenWidth = windowObj.winfo_screenwidth()
            screenHeight = windowObj.winfo_screenheight()

            return [screenWidth, screenHeight]

        except Exception as err:
            print(f"Unexpected error @getScreenSize(): {err}")