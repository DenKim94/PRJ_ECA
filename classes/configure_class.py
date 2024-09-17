import customtkinter as ctk
import UI_constants
import classes.generic_widget_class as gen_widgets


class configWindow:
    def __init__(self, parent, dataBase):
        # CONSTANTS
        self.DEF_FONT = UI_constants.DEF_FONT
        self.FONT_SIZE_BUTTON = UI_constants.FONT_SIZE_BUTTON
        self.BUTTON_WIDTH = UI_constants.BUTTON_WIDTH
        self.ENTRY_WIDTH = UI_constants.CONFIGS_ENTRY_WIDTH
        self.LABEL_WIDTH = UI_constants.CONFIGS_LABEL_WIDTH
        self.CURSOR_TYPE = UI_constants.CURSOR_TYPE
        self.min_size_config_window = UI_constants.MIN_WINDOW_SIZE
        self.max_size_config_window = UI_constants.MAX_WINDOW_SIZE

        # DEFAULT SETTINGS
        self.ENERGY_PRICE_EUR_kWh = UI_constants.DEF_ENERGY_PRICE_EUR_kWh
        self.ANNUAL_BASIC_PRICE_EUR = UI_constants.DEF_ANNUAL_BASIC_PRICE_EUR
        self.MONTHLY_COSTS_EUR = UI_constants.DEF_MONTHLY_COSTS_EUR
        self.ADD_CREDIT_EUR = UI_constants.DEF_ADD_CREDIT_EUR
        self.ABS_ELEC_TAX_EUR_kWh = UI_constants.DEF_ABS_ELECTRICITY_TAX_EUR

        try:
            self.master = parent
            self.dataBase = dataBase
            self.configWindow = gen_widgets.newWindow(self.master.master, self.min_size_config_window,
                                                      self.max_size_config_window)
            self.configWindow.window.title("Einstellungen")
            gen_widgets.newWindow.center_window(self.configWindow.window, self.master.max_size_edit_window[0],
                                                self.master.max_size_edit_window[1])
            self.master.disable_buttons()

            self.error_label = ctk.CTkLabel(master=self.configWindow.container, text="", text_color="red")

            frame = ctk.CTkFrame(master=self.configWindow.container, fg_color="transparent")
            frame.pack(side='top', padx=5, pady=5)
            price_label = ctk.CTkLabel(master=frame, font=(self.DEF_FONT, self.FONT_SIZE_BUTTON),
                                       text="Verbrauchspreis in EUR/kWh:",
                                       anchor=ctk.W,
                                       width=self.LABEL_WIDTH)
            price_label.pack(side='left', padx=5, pady=1)

            self.price_entry = ctk.CTkEntry(master=frame,
                                            width=self.ENTRY_WIDTH,
                                            justify="center")
            self.price_entry.pack(side='left', padx=1, pady=1, expand=False)
            self.price_entry.configure(validate="focusout",
                                       validatecommand=(self.configWindow.window.register(
                                            lambda value: gen_widgets.newWindow.validate_number(
                                                self.error_label, self.price_entry.get())), '%P'))

            self.price_entry.insert(0, str(self.ENERGY_PRICE_EUR_kWh))

            frame = ctk.CTkFrame(master=self.configWindow.container, fg_color="transparent")
            frame.pack(side='top', padx=5, pady=5)
            basic_price_label = ctk.CTkLabel(master=frame, font=(self.DEF_FONT, self.FONT_SIZE_BUTTON),
                                             text="Grundpreis in EUR/Jahr:",
                                             anchor=ctk.W,
                                             width=self.LABEL_WIDTH)
            basic_price_label.pack(side='left', padx=5, pady=1)

            self.basic_price_entry = ctk.CTkEntry(master=frame,
                                                  width=self.ENTRY_WIDTH,
                                                  justify="center")
            self.basic_price_entry.pack(side='left', padx=1, pady=1, expand=False)
            self.basic_price_entry.configure(validate="focusout",
                                             validatecommand=(self.configWindow.window.register(
                                                lambda value: gen_widgets.newWindow.validate_number(
                                                    self.error_label, self.basic_price_entry.get())), '%P'))

            self.basic_price_entry.insert(0, str(self.ANNUAL_BASIC_PRICE_EUR))

            frame = ctk.CTkFrame(master=self.configWindow.container, fg_color="transparent")
            frame.pack(side='top', padx=5, pady=5)
            monthly_costs_label = ctk.CTkLabel(master=frame, font=(self.DEF_FONT, self.FONT_SIZE_BUTTON),
                                               text="Monatlicher Abschlag in EUR:",
                                               anchor=ctk.W,
                                               width=self.LABEL_WIDTH)
            monthly_costs_label.pack(side='left', padx=5, pady=1)

            self.monthly_costs_entry = ctk.CTkEntry(master=frame,
                                                    width=self.ENTRY_WIDTH,
                                                    justify="center")

            self.monthly_costs_entry.pack(side='left', padx=1, pady=1, expand=False)
            self.monthly_costs_entry.configure(validate="focusout",
                                               validatecommand=(self.configWindow.window.register(
                                                    lambda value: gen_widgets.newWindow.validate_number(
                                                        self.error_label, self.monthly_costs_entry.get())), '%P'))

            self.monthly_costs_entry.insert(0, str(self.MONTHLY_COSTS_EUR))

            frame = ctk.CTkFrame(master=self.configWindow.container, fg_color="transparent")
            frame.pack(side='top', padx=5, pady=5)

            add_credit_label = ctk.CTkLabel(master=frame, font=(self.DEF_FONT, self.FONT_SIZE_BUTTON),
                                            text="Guthaben (optional) in EUR:",
                                            anchor=ctk.W,
                                            width=self.LABEL_WIDTH)
            add_credit_label.pack(side='left', padx=5, pady=1)

            self.add_credit_entry = ctk.CTkEntry(master=frame,
                                                 width=self.ENTRY_WIDTH,
                                                 justify="center")

            self.add_credit_entry.pack(side='left', padx=1, pady=1, expand=False)
            self.add_credit_entry.configure(validate="focusout",
                                            validatecommand=(self.configWindow.window.register(
                                                    lambda value: gen_widgets.newWindow.validate_optional_number(
                                                        self.error_label, self.add_credit_entry.get())), '%P'))

            self.add_credit_entry.insert(0, str(self.ADD_CREDIT_EUR))

            frame = ctk.CTkFrame(master=self.configWindow.container, fg_color="transparent")
            frame.pack(side='bottom', padx=5, pady=5)

            self.ok_button = ctk.CTkButton(master=frame, text="OK",
                                           state="normal",
                                           cursor=self.CURSOR_TYPE,
                                           font=(self.DEF_FONT, self.FONT_SIZE_BUTTON),
                                           width=self.BUTTON_WIDTH,
                                           command=self.provide_configs_to_db)

            self.error_label.pack(side='top', padx=5, pady=0)
            self.ok_button.pack(side='bottom', padx=5, pady=0)
            self.configWindow.window.protocol("WM_DELETE_WINDOW", self.master.enable_buttons)

        except Exception as err:
            raise Exception(f">> Unexpected error @configWindow: {err}")

    def provide_configs_to_db(self):
        try:
            if self.validate_inputs():
                self.ENERGY_PRICE_EUR_kWh = float(self.price_entry.get())
                self.ANNUAL_BASIC_PRICE_EUR = float(self.basic_price_entry.get())
                self.MONTHLY_COSTS_EUR = float(self.monthly_costs_entry.get())
                self.ADD_CREDIT_EUR = float(self.add_credit_entry.get())

                # PROVIDE CONFIGS TO DATABASE CLASS
                self.dataBase.ENERGY_PRICE_EUR_kWh = self.ENERGY_PRICE_EUR_kWh
                self.dataBase.ANNUAL_BASIC_PRICE_EUR = self.ANNUAL_BASIC_PRICE_EUR
                self.dataBase.MONTHLY_COSTS_EUR = self.MONTHLY_COSTS_EUR
                self.dataBase.ADD_CREDIT_EUR = self.ADD_CREDIT_EUR

                # CLOSE WINDOW and ENABLE BUTTONS
                self.master.enable_buttons()
                self.configWindow.window.destroy()

        except Exception as err:
            raise Exception(f">> Unexpected error @provide_configs: {err}")

    def validate_inputs(self):
        if gen_widgets.newWindow.validate_number(self.error_label, self.price_entry.get()) and \
           gen_widgets.newWindow.validate_number(self.error_label, self.basic_price_entry.get()) and \
           gen_widgets.newWindow.validate_number(self.error_label, self.monthly_costs_entry.get()) and \
           gen_widgets.newWindow.validate_optional_number(self.error_label, self.add_credit_entry.get()):

            self.error_label.configure(text="")
            isValid = True
        else:
            isValid = False

        return isValid
