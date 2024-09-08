import UI_constants
import classes.generic_widget_class as gen_widgets
from datetime import datetime
import math


class cost_analyzer:
    def __init__(self, parent):
        try:
            self.master = parent
            self.dataBase = self.master.dataBase

            # DEFAULT CONSTANTS
            self.ENERGY_PRICE_EUR_kWh = self.dataBase.ENERGY_PRICE_EUR_kWh
            self.ANNUAL_BASIC_PRICE_EUR = self.dataBase.ANNUAL_BASIC_PRICE_EUR
            self.MONTHLY_COSTS_EUR = self.dataBase.MONTHLY_COSTS_EUR
            self.ABS_CURRENT_TAX_EUR_kWh = self.dataBase.ABS_CURRENT_TAX_EUR_kWh
            self.ADD_CREDIT_EUR = self.dataBase.ADD_CREDIT_EUR
            self.VA_TAX_REL = UI_constants.DEF_VA_TAX_PERCENTAGE / 100
            self.TAX_X_REL = UI_constants.DEF_TAX_X_PERCENTAGE / 100
            self.min_size_cost_analyzer = UI_constants.MIN_WINDOW_SIZE
            self.max_size_cost_analyzer = UI_constants.MAX_WINDOW_SIZE

            # CALCULATED PARAMETERS
            self.annualPrepayment_EUR = None
            self.energyDifference_list = None
            self.totalUsedEnergy_kWh = None
            self.timePeriod_days = None
            self.timePeriod_months = None
            self.costsUsedEnergy_net = None
            self.partialBasicCosts_net = None
            self.netCosts = None
            self.costsCurrentTax_included = None
            self.costsVAT_EUR = None
            self.totalNetEnergyCosts_EUR = None
            self.costDifference_EUR = None

            # self.analysis_window = gen_widgets.newWindow(self.master.master, self.min_size_cost_analyzer,
            #                                              self.max_size_cost_analyzer)

        except Exception as err:
            raise Exception(f">> Unexpected error @cost_analyzer: {err}")

    def get_stored_data(self):
        try:
            [date_tuple, energy_tuple] = self.dataBase.get_all_date_and_energy_values()
            date_obj = tuple(datetime.strptime(date, '%d.%m.%Y') for date in date_tuple)
            return date_obj, energy_tuple

        except Exception as err:
            raise Exception(f">> Unexpected error @get_stored_data: {err}")

    def calculate_total_used_energy(self, meas_energy_kWh):
        try:
            self.energyDifference_list = [meas_energy_kWh[i+1] - meas_energy_kWh[i] for i in range(len(meas_energy_kWh) - 1)]
            self.totalUsedEnergy_kWh = sum(self.energyDifference_list)

        except Exception as err:
            raise Exception(f">> Unexpected error @calculate_used_energy: {err}")

    def calculate_time_period(self, date_tuple):
        try:
            self.timePeriod_days = (date_tuple[-1] - date_tuple[0]).days
            self.timePeriod_months = math.floor(self.timePeriod_days / UI_constants.DEF_DAYS_MONTH)

        except Exception as err:
            raise Exception(f">> Unexpected error @calculate_time_period_days: {err}")

    def calculate_net_costs_used_energy(self):
        try:
            self.costsUsedEnergy_net = round(self.totalUsedEnergy_kWh * self.ENERGY_PRICE_EUR_kWh *
                                             (1-self.VA_TAX_REL-self.TAX_X_REL), 2)

        except Exception as err:
            raise Exception(f">> Unexpected error @calculate_costs_used_energy: {err}")

    def calculate_partial_basic_net_costs(self):
        try:
            self.partialBasicCosts_net = round(self.ANNUAL_BASIC_PRICE_EUR * (1-self.VA_TAX_REL+self.TAX_X_REL) *
                                               self.timePeriod_days/UI_constants.DEF_DAYS_YEAR, 2)

        except Exception as err:
            raise Exception(f">> Unexpected error @calculate_partial_basic_costs: {err}")

    def calculate_total_net_costs(self):
        try:
            self.netCosts = self.partialBasicCosts_net + self.costsUsedEnergy_net

        except Exception as err:
            raise Exception(f">> Unexpected error @calculate_total_net_costs: {err}")

    def calculate_costs_current_tax_included(self):
        try:
            costsCurrentTax_EUR = self.ABS_CURRENT_TAX_EUR_kWh * self.totalUsedEnergy_kWh
            self.costsCurrentTax_included = round(costsCurrentTax_EUR + self.netCosts, 2)

        except Exception as err:
            raise Exception(f">> Unexpected error @calculate_costs_current_tax_included: {err}")

    def calculate_total_energy_costs(self):
        try:
            self.costsVAT_EUR = round(self.costsCurrentTax_included * self.VA_TAX_REL, 2)
            self.totalNetEnergyCosts_EUR = round(self.costsVAT_EUR + self.costsCurrentTax_included, 2)

        except Exception as err:
            raise Exception(f">> Unexpected error @calculate_total_energy_costs: {err}")

    def calculate_annual_prepayment_EUR(self):
        try:
            self.annualPrepayment_EUR = round(self.MONTHLY_COSTS_EUR * self.timePeriod_months, 2)

        except Exception as err:
            raise Exception(f">> Unexpected error @calculate_annual_prepayment_EUR: {err}")

    def calculate_cost_difference(self):
        try:
            self.costDifference_EUR = round((self.annualPrepayment_EUR + self.ADD_CREDIT_EUR) -
                                            self.totalNetEnergyCosts_EUR, 2)

        except Exception as err:
            raise Exception(f">> Unexpected error @calculate_cost_difference: {err}")

    def show_results(self):
        try:
            configs_output = f"""
            ############################ KONFIGURATION #############################
            * Umsatzsteuer: {UI_constants.DEF_VA_TAX_PERCENTAGE} %
            * Stromsteuer: {UI_constants.DEF_ABS_ELECTRICITY_TAX_EUR} €/kWh
            * Zusätzlicher Steuersatz (z.B. Umlagen, Konzession): {UI_constants.DEF_TAX_X_PERCENTAGE} %
            * Verbrauchspreis: {self.ENERGY_PRICE_EUR_kWh} €/kWh
            * Grundpreis: {self.ANNUAL_BASIC_PRICE_EUR} €/Jahr
            * Abschlag: {self.MONTHLY_COSTS_EUR} €/Monat
            * Guthaben (optional): {self.ADD_CREDIT_EUR} €             
            #####################################################################
            """
            print(configs_output)

            res_output = f"""
            ############################ ERGEBNISSE #############################
            * Verbrauchte Energiemenge: {self.totalUsedEnergy_kWh} kWh
            * Abrechnungszeitraum: {self.timePeriod_days} Tage
            * Einzahlungszeitraum: {self.timePeriod_months} Monate
            * Verbrauchspreis (netto): {self.costsUsedEnergy_net} EUR
            * Grundpreis (netto): {self.partialBasicCosts_net} EUR  
            * Kosten inkl. Stromsteuer: {self.costsCurrentTax_included} EUR
            * Kosten Umsatzsteuer: {self.costsVAT_EUR} EUR
            * Zusätzliches Guthaben (optional): {self.ADD_CREDIT_EUR} EUR     
            * Gesamte Stromkosten (netto): {self.totalNetEnergyCosts_EUR} EUR         
            * Vorauszahlung (gesamt): {self.annualPrepayment_EUR} EUR

            ----------------------------------------------------------------
            * Geschätztes Guthaben (Vorauszahlung - Stromkosten): {self.costDifference_EUR} EUR
            #####################################################################
            """
            print(res_output)

        except Exception as err:
            raise Exception(f">> Unexpected error @show_results: {err}")

    def run_calculations(self):
        try:
            [date_tuple, energy_tuple] = self.get_stored_data()
            self.calculate_total_used_energy(energy_tuple)
            self.calculate_time_period(date_tuple)
            self.calculate_net_costs_used_energy()
            self.calculate_partial_basic_net_costs()
            self.calculate_total_net_costs()
            self.calculate_costs_current_tax_included()
            self.calculate_total_energy_costs()
            self.calculate_annual_prepayment_EUR()
            self.calculate_cost_difference()
            self.show_results()

            self.master.analysis_is_running = False
            self.master.button_run.configure(state="normal")

        except Exception as err:
            raise Exception(f">> Unexpected error @run_calculations: {err}")