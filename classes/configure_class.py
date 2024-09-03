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
        self.PRICE_EUR_kWh = UI_constants.DEF_PRICE_EUR_kWh
        self.ANNUAL_BASIC_PRICE_EUR = UI_constants.DEF_ANNUAL_BASIC_PRICE_EUR
        self.TAX_PERCENTAGE = UI_constants.DEF_TAX_PERCENTAGE
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

            self.price_entry.insert(0, str(self.PRICE_EUR_kWh))

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
            tax_percent_label = ctk.CTkLabel(master=frame, font=(self.DEF_FONT, self.FONT_SIZE_BUTTON),
                                             text="Umsatzsteuer in %:",
                                             anchor=ctk.W,
                                             width=self.LABEL_WIDTH)
            tax_percent_label.pack(side='left', padx=5, pady=1)

            self.tax_percent_entry = ctk.CTkEntry(master=frame,
                                                  width=self.ENTRY_WIDTH,
                                                  justify="center")
            self.tax_percent_entry.pack(side='left', padx=1, pady=1, expand=False)
            self.tax_percent_entry.configure(validate="focusout",
                                             validatecommand=(self.configWindow.window.register(
                                                lambda value: gen_widgets.newWindow.validate_number(
                                                    self.error_label, self.tax_percent_entry.get())), '%P'))

            self.tax_percent_entry.insert(0, str(self.TAX_PERCENTAGE))

            frame = ctk.CTkFrame(master=self.configWindow.container, fg_color="transparent")
            frame.pack(side='top', padx=5, pady=5)

            elec_tax_percent_label = ctk.CTkLabel(master=frame, font=(self.DEF_FONT, self.FONT_SIZE_BUTTON),
                                                  text="Stromsteuer in EUR/kWh:",
                                                  anchor=ctk.W,
                                                  width=self.LABEL_WIDTH)
            elec_tax_percent_label.pack(side='left', padx=5, pady=1)

            self.elec_tax_percent_entry = ctk.CTkEntry(master=frame,
                                                       width=self.ENTRY_WIDTH,
                                                       justify="center")

            self.elec_tax_percent_entry.pack(side='left', padx=1, pady=1, expand=False)
            self.elec_tax_percent_entry.configure(validate="focusout",
                                                  validatecommand=(self.configWindow.window.register(
                                                    lambda value: gen_widgets.newWindow.validate_number(
                                                        self.error_label, self.elec_tax_percent_entry.get())), '%P'))

            self.elec_tax_percent_entry.insert(0, str(self.ABS_ELEC_TAX_EUR_kWh))

            frame = ctk.CTkFrame(master=self.configWindow.container, fg_color="transparent")
            frame.pack(side='bottom', padx=5, pady=5)

            self.ok_button = ctk.CTkButton(master=frame, text="OK",
                                           state="normal",
                                           cursor=self.CURSOR_TYPE,
                                           font=(self.DEF_FONT, self.FONT_SIZE_BUTTON),
                                           width=self.BUTTON_WIDTH,
                                           command=self.provide_configs)

            self.error_label.pack(side='top', padx=5, pady=0)
            self.ok_button.pack(side='bottom', padx=5, pady=0)
            self.configWindow.window.protocol("WM_DELETE_WINDOW", self.master.enable_buttons)

        except Exception as err:
            raise Exception(f">> Unexpected error @configWindow: {err}")

    def provide_configs(self):
        try:
            if self.validate_inputs():
                self.PRICE_EUR_kWh = float(self.price_entry.get())
                self.ANNUAL_BASIC_PRICE_EUR = float(self.basic_price_entry.get())
                self.TAX_PERCENTAGE = float(self.tax_percent_entry.get())
                self.elec_tax_percent_entry = float(self.elec_tax_percent_entry.get())
                print(f">> Configs: {self.PRICE_EUR_kWh}, {self.ANNUAL_BASIC_PRICE_EUR}, {self.TAX_PERCENTAGE}, "
                      f"{self.elec_tax_percent_entry}")
                self.error_label.configure(text="Werte sind übernommen.", text_color="green")

        except Exception as err:
            raise Exception(f">> Unexpected error @provide_configs: {err}")

    def validate_inputs(self):
        if gen_widgets.newWindow.validate_number(self.error_label, self.price_entry.get()) and \
           gen_widgets.newWindow.validate_number(self.error_label, self.basic_price_entry.get()) and \
           gen_widgets.newWindow.validate_number(self.error_label, self.tax_percent_entry.get()) and \
           gen_widgets.newWindow.validate_number(self.error_label, self.elec_tax_percent_entry.get()):
            self.error_label.configure(text="")
            isValid = True
        else:
            isValid = False

        return isValid
