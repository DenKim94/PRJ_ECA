import customtkinter as ctk
from PIL import Image
import os
import classes.calculation_class as calc_class


class selectDB_frame(ctk.CTkFrame):
    def __init__(self, parent, dataBase, UI_constants):
        try:
            # analogy: frame = ctk.CTkFrame(master=root, fg_color="transparent")
            super().__init__(parent, fg_color="transparent")
            self.dataBase = dataBase
            self.sharedStates = parent.sharedAppStates

            # MEMBER VARIABLES
            self.PLACEHOLDER = UI_constants.PLACEHOLDER_TEXT
            self.valueListDropDown = [self.PLACEHOLDER]
            self.dropDownValue = ctk.StringVar(value=UI_constants.PLACEHOLDER_TEXT)
            self.icon_path = os.path.join(UI_constants.DEF_ICON_ROOT, UI_constants.DEF_ICON_NAME)
            self.update_edit_button_state_callback = None
            self.analysis_is_running = False

            # UPDATE DATABASE LIST
            if self.dataBase.existing_db_files is not None:
                for fileName in self.dataBase.existing_db_files:
                    self.addDropDownValue(fileName)

            # WIDGETS
            logo = ctk.CTkImage(Image.open(self.icon_path), size=(UI_constants.ICON_WIDTH, UI_constants.ICON_HEIGHT))

            self.label_db = ctk.CTkLabel(master=self,
                                         image=logo,
                                         text="",
                                         font=(UI_constants.DEF_FONT, UI_constants.FONT_SIZE_LABEL),
                                         width=UI_constants.LABEL_WIDTH)

            self.dropdown_db = ctk.CTkOptionMenu(master=self,
                                                 values=self.sharedStates.existing_db_files,
                                                 variable=self.dropDownValue,
                                                 width=UI_constants.DROPDOWN_WIDTH,
                                                 fg_color="gray",
                                                 button_color="gray",
                                                 button_hover_color="gray",
                                                 text_color="white",
                                                 dropdown_fg_color="gray",
                                                 font=(UI_constants.DEF_FONT, UI_constants.FONT_SIZE_DROPDOWN),
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
            self.dropdown_db.pack(padx=5, pady=5, side='right', expand=False)
            self.button_run.pack(padx=10, pady=5, side='left')
            self.label_db = logo

            if self.sharedStates.new_db_file_created:
                self.updateDropDownValues()
                print(f">> New database file created: {self.sharedStates.new_db_file_created}")
                self.sharedStates.new_db_file_created = False

        except Exception as err:
            raise Exception(f">> Unexpected error @selectDB_frame: {err}")

    def updateRunButtonState(self, *args, disable_run_button=False):
        try:
            self.sharedStates.selectedDataBase = self.dropDownValue.get()
            if self.sharedStates.selectedDataBase != self.PLACEHOLDER:
                if not disable_run_button:
                    self.button_run.configure(state="normal")
                    self.dataBase.db_name = self.sharedStates.selectedDataBase
                else:
                    self.button_run.configure(state="disabled")

                if self.update_edit_button_state_callback is not None and not disable_run_button:
                    self.update_edit_button_state_callback(True)
            else:
                self.button_run.configure(state="disabled")
                if self.update_edit_button_state_callback is not None:
                    self.update_edit_button_state_callback(False)

        except Exception as err:
            raise Exception(f">> Unexpected error @updateRunButtonState: {err}")

    def updateNewDBFileState(self, state):
        self.sharedStates.new_db_file_created = state

    def addDropDownValue(self, newValue):
        try:
            if newValue not in self.sharedStates.existing_db_files:
                self.sharedStates.existing_db_files.append(newValue)

        except Exception as err:
            raise Exception(f"Unexpected error @addDropDownValue(): {err}")

    def updateDropDownValues(self):
        try:
            existing_db_files = self.dataBase.get_existing_db_files()
            for fileName in existing_db_files:
                self.addDropDownValue(fileName)

            self.dropdown_db.configure(values=self.sharedStates.existing_db_files)
        except Exception as err:
            raise Exception(f"Unexpected error @updateDropDownValues(): {err}")

    def removeDropDownValue(self, valueToRemove):
        try:
            if valueToRemove in self.sharedStates.existing_db_files:
                self.sharedStates.existing_db_files.remove(valueToRemove)

                if self.dropDownValue.get() == valueToRemove:
                    self.dropDownValue.set(self.PLACEHOLDER)
                self.dropdown_db.configure(values=self.sharedStates.existing_db_files)

        except Exception as err:
            raise Exception(f"Unexpected error @removeDropDownValue(): {err}")

    def replaceDropDownValue(self, oldValue, newValue):
        try:
            if oldValue in self.sharedStates.existing_db_files:
                index = self.sharedStates.existing_db_files.index(oldValue)
                self.sharedStates.existing_db_files[index] = newValue

                if self.dropDownValue.get() == oldValue:
                    self.dropDownValue.set(newValue)
                self.dropdown_db.configure(values=self.sharedStates.existing_db_files)
            else:
                print(f"Value @replaceDropDownValue(): {oldValue} not found!")

        except Exception as err:
            raise Exception(f"Unexpected error @replaceDropDownValue(): {err}")

    def handleDropDownState(self, state):
        try:
            if state:  # If buttons are disabled
                self.dropdown_db.configure(state="disabled")
            else:  # If buttons are enabled
                self.dropdown_db.configure(state="normal")
        except Exception as err:
            raise Exception(f"Unexpected error @handleDropDownState(): {err}")

    def runAnalysis(self):
        print(f">> Analyse für: {self.dropDownValue.get()}")
        self.analysis_is_running = True
        self.button_run.configure(state="disabled")
        costs_analyzer = calc_class.cost_analyzer(self)
        # CALCULATIONS
        costs_analyzer.run_calculations()

