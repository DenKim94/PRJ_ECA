import classes.generic_widget_class as gen_widgets
import UI_constants
import math
import customtkinter as ctk
import matplotlib.pyplot as plt
# noinspection SpellCheckingInspection
import matplotlib.dates as mdates
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import mplcursors



class resultsVisualizer:
    def __init__(self, parent, calculationClass):
        try:
            self.master = parent
            self.appearance_mode = ctk.get_appearance_mode()
            self.calculation = calculationClass
            self.x_values = self.calculation.date_tuple[1:]
            self.y_values = self.calculation.energyDifference_list

            self.resultsWindow = gen_widgets.newWindow(self.master.master, UI_constants.MIN_WINDOW_SIZE_RESULTS,
                                                        UI_constants.MAX_WINDOW_SIZE_RESULTS)

            self.resultsWindow.window.title("Ergebnisse der Datenanalyse")
            if self.master.disable_buttons_callback is not None:
                self.master.disable_buttons_callback()

            self.resultsWindow.window.protocol("WM_DELETE_WINDOW", self.on_window_close)

            gen_widgets.newWindow.center_window(self.resultsWindow.window,
                                                UI_constants.MAX_WINDOW_SIZE_RESULTS[0],
                                                UI_constants.MAX_WINDOW_SIZE_RESULTS[1])

            frame_fig = ctk.CTkFrame(master=self.resultsWindow.container, fg_color="transparent")
            frame_fig.pack(side='top', padx=5, pady=5)

            fig, ax = plt.subplots(figsize=(9,3))
            if self.appearance_mode == "Dark":
                fig.patch.set_facecolor((36/255,36/255,36/255))
                ax.set_facecolor("black")
                ax.grid(True, which='both', axis='both', color='white', linestyle='--', linewidth=0.5)
            else:
                fig.patch.set_facecolor((235/255,235/255,235/255))
                ax.set_facecolor("white")
                ax.grid(True, which='both', axis='both', color='black', linestyle='--', linewidth=0.5)

            line, = ax.plot(self.x_values, self.y_values, color='lightgreen'
                            if self.appearance_mode == "Dark" else 'darkgreen',
                            marker='o', linestyle='-')

            ax.set_xticks(self.x_values)
            ax.xaxis.set_major_formatter(mdates.DateFormatter('%d-%m-%Y'))
            fig.autofmt_xdate()

            ax.tick_params(axis='x', colors='white' if self.appearance_mode == "Dark" else 'black')
            ax.tick_params(axis='y', colors='white' if self.appearance_mode == "Dark" else 'black')
            plt.xlabel('Datum', color='white' if self.appearance_mode == "Dark" else 'black')
            plt.ylabel('Verbrauchte Energie in kWh', color='white' if self.appearance_mode == "Dark" else 'black')

            canvas = FigureCanvasTkAgg(fig, master=frame_fig)
            canvas.get_tk_widget().config(bg='black' if self.appearance_mode == "Dark" else 'white')
            canvas.get_tk_widget().pack(side='top')

            cursor = mplcursors.cursor(line)

            @cursor.connect("add")
            def on_click(sel):
                idx = int(sel.index)
                sel.annotation.set(text=f"{self.y_values[idx]} kWh")
                sel.annotation.get_bbox_patch().set(fc="white", alpha=0.8)

            frame_left = ctk.CTkFrame(master=frame_fig, fg_color="transparent")
            frame_left.pack(side='left', padx=60, pady=20)
            frame_right = ctk.CTkFrame(master=frame_fig, fg_color="transparent")
            frame_right.pack(side='left', padx=20, pady=20)

            res_output = [f" Verbrauchte Energiemenge: {self.calculation.totalUsedEnergy_kWh} kWh",
                            f" Abrechnungszeitraum: {self.calculation.timePeriod_days} Tage",
                            f" Verbrauchspreis (netto): {self.calculation.costsUsedEnergy_net} EUR",
                            f" Grundpreis (netto): {self.calculation.partialBasicCosts_net} EUR",
                            f" Kosten Umsatzsteuer: {self.calculation.costsVAT_EUR} EUR",
                            f" Stromsteuersatz: {UI_constants.DEF_ABS_ELECTRICITY_TAX_EUR} EUR",
                            f" Kosten Stromsteuer: {round(self.calculation.totalUsedEnergy_kWh*UI_constants.DEF_ABS_ELECTRICITY_TAX_EUR,2)} EUR",
                            f" Gesamte Stromkosten (netto): {self.calculation.totalNetEnergyCosts_EUR} EUR",
                            f" Einzahlungszeitraum: {self.calculation.timePeriod_months} Monate",
                            f" Vorauszahlung (gesamt): {self.calculation.annualPrepayment_EUR} EUR",
                            f" Zusätzliches Guthaben (optional): {self.calculation.ADD_CREDIT_EUR} EUR",
                            f" Geschätzte Kostendifferenz (Vorauszahlung - Stromkosten): {self.calculation.costDifference_EUR} EUR"]

            for index, res_str in enumerate(res_output):
                if index <= (math.floor(len(res_output)/2)-1):
                    tmp_res_left = ctk.CTkLabel(master=frame_left, text=res_str, text_color='white'
                                                if self.appearance_mode == "Dark" else 'black',
                                                font=(UI_constants.DEF_FONT, UI_constants.FONT_SIZE_BUTTON),
                                                anchor=ctk.W)
                    tmp_res_left.pack(side='top', anchor='w', padx=0, pady=1)
                else:
                    if "Kostendifferenz" not in res_str:
                        tmp_res_right = ctk.CTkLabel(master=frame_right, text=res_str, text_color='white'
                        if self.appearance_mode == "Dark" else 'black',
                                                    font=(UI_constants.DEF_FONT, UI_constants.FONT_SIZE_BUTTON),
                                                    anchor=ctk.W)
                        tmp_res_right.pack(side='top', anchor='w', padx=0, pady=1)
                    else:
                        cost_diff = self.calculation.costDifference_EUR
                        color = 'lightgreen' if cost_diff >= 0 else 'red'
                        static_text = " Geschätzte Kostendifferenz (Vorauszahlung - Stromkosten): "

                        label_text = ctk.CTkLabel(master=frame_right,
                                                  text=static_text,
                                                  text_color='white' if self.appearance_mode == "Dark" else 'black',
                                                  font=(UI_constants.DEF_FONT, UI_constants.FONT_SIZE_BUTTON))
                        label_text.pack(side='left', anchor='w', padx=0, pady=1)

                        label_value = ctk.CTkLabel(master=frame_right,
                                                   text=f"{cost_diff} EUR",
                                                   text_color=color,
                                                   font=(UI_constants.DEF_FONT, UI_constants.FONT_SIZE_BUTTON))
                        label_value.pack(side='top', anchor='w', padx=0, pady=1)

            frame_button = ctk.CTkFrame(master=self.resultsWindow.container, fg_color="transparent")
            frame_button.pack(side='bottom', padx=5, pady=5)

            self.ok_button = ctk.CTkButton(master=frame_button, text="OK",
                                           state="normal",
                                           cursor=UI_constants.CURSOR_TYPE,
                                           font=(UI_constants.DEF_FONT, UI_constants.FONT_SIZE_BUTTON),
                                           width=UI_constants.BUTTON_WIDTH,
                                           command=self.on_window_close)

            self.ok_button.pack(side='bottom', padx=5, pady=0)

        except Exception as err:
            raise Exception(f">> Unexpected error @resultsVisualizer: {err}")

    def on_window_close(self):
        try:
            if self.master.enable_buttons_callback is not None:
                self.master.enable_buttons_callback()

            # Enable run button and close all figures
            self.master.analysis_is_running = False
            self.master.button_run.configure(state="normal")
            plt.close('all')
            self.resultsWindow.window.destroy()

        except Exception as err:
            raise Exception(f">> Unexpected error @on_window_close: {err}")