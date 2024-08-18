import customtkinter as ctk


class selectDB_frame(ctk.CTkFrame):
    def __init__(self, parent, UI_constants):
        # analogy: frame = ctk.CTkFrame(master=root, fg_color="transparent")
        super().__init__(parent, fg_color="transparent")
        # MEMBER VARIABLES
        self.PLACEHOLDER = UI_constants.PLACEHOLDER_TEXT
        self.analysisIsRunning = False
        self.valueListDropDown = [self.PLACEHOLDER, "TEST_OPTION_01"]
        self.dropDownValue = ctk.StringVar(value=UI_constants.PLACEHOLDER_TEXT)

        # WIDGETS
        self.label_db = ctk.CTkLabel(master=self, text=UI_constants.LABEL_TEXT,
                                     font=(UI_constants.DEF_FONT, UI_constants.FONT_SIZE_LABEL),
                                     width=UI_constants.LABEL_WIDTH)

        self.dropdown_db = ctk.CTkOptionMenu(master=self,
                                             values=self.valueListDropDown,
                                             variable=self.dropDownValue,
                                             width=UI_constants.DROPDOWN_WIDTH,
                                             fg_color="gray",
                                             button_color="gray",
                                             button_hover_color="gray",
                                             text_color="white",
                                             dropdown_fg_color="gray",
                                             font=(UI_constants.DEF_FONT, UI_constants.FONT_SIZE_DROPDOWN)
                                             )
        self.dropdown_db.set(self.PLACEHOLDER)
        self.button_run = ctk.CTkButton(master=self, text="Start", cursor=UI_constants.CURSOR_TYPE,
                                        font=(UI_constants.DEF_FONT, UI_constants.FONT_SIZE_BUTTON),
                                        width=UI_constants.BUTTON_WIDTH, command=self.runAnalysis)

        # Set initial run button state
        self.updateRunButtonState()
        # Track value changes
        self.dropDownValue.trace_add("write", self.updateRunButtonState)

        self.pack(padx=5, pady=10, expand=False, side='top')
        self.label_db.pack(padx=10, pady=10, side='top')
        self.dropdown_db.pack(padx=5, pady=10, side='right', expand=False)
        self.button_run.pack(padx=10, pady=10, side='left')

    def updateRunButtonState(self, *args):
        if self.dropDownValue.get() != self.PLACEHOLDER:
            self.button_run.configure(state="normal")
        else:
            self.button_run.configure(state="disabled")

    def addDropDownValue(self, newValue):
        try:
            if newValue not in self.valueListDropDown:
                self.valueListDropDown.append(newValue)

        except Exception as err:
            print(f"Unexpected error @addDropDownValue(): {err}")

    def updateDropDownValues(self):
        self.dropdown_db.configure(values=self.valueListDropDown)

    def removeDropDownValue(self, valueToRemove):
        try:
            if valueToRemove in self.valueListDropDown:
                self.valueListDropDown.remove(valueToRemove)

                if self.dropDownValue.get() == valueToRemove:
                    self.dropDownValue.set(self.PLACEHOLDER)
                self.updateDropDownValues()

        except Exception as err:
            print(f"Unexpected error @removeDropDownValue(): {err}")

    def replaceDropDownValue(self, oldValue, newValue):
        try:
            if oldValue in self.valueListDropDown:
                index = self.valueListDropDown.index(oldValue)
                self.valueListDropDown[index] = newValue

                if self.dropDownValue.get() == oldValue:
                    self.dropDownValue.set(newValue)
                self.updateDropDownValues()
            else:
                print(f"Value: {oldValue} not found!")

        except Exception as err:
            print(f"Unexpected error @replaceDropDownValue(): {err}")

    def handleDropDownState(self, state):
        if state:  # If buttons are disabled
            self.dropdown_db.configure(state="disabled")
        else:  # If buttons are enabled
            self.dropdown_db.configure(state="normal")

    def runAnalysis(self):
        print(f">> Run Analysis for: {self.dropDownValue.get()}")
        if not self.analysisIsRunning:
            self.analysisIsRunning = True

        # TO-DO: Set analysisIsRunning = False after finishing the analysis
