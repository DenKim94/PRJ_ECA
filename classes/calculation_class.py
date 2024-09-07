import UI_constants
import classes.generic_widget_class as gen_widgets
from datetime import datetime


class cost_analyzer:
    def __init__(self, parent):
        try:
            self.master = parent
            self.dataBase = self.master.dataBase
            self.min_size_cost_analyzer = UI_constants.MIN_WINDOW_SIZE
            self.max_size_cost_analyzer = UI_constants.MAX_WINDOW_SIZE
            self.usedEnergy = None
            self.timePeriod = None
            self.costsUsedEnergy = None
            self.partialBasicCosts = None
            self.netCosts = None
            self.costsCurrentTax_included = None
            self.costsVAT_included = None
            self.totalEnergyCosts = None

            # self.cost_analyzer = gen_widgets.newWindow(self.master.master, self.min_size_cost_analyzer,
            #                                            self.max_size_cost_analyzer)

            [date_tuple, energy_tuple] = self.get_stored_data()
            print(date_tuple, energy_tuple)

        except Exception as err:
            raise Exception(f">> Unexpected error @cost_analyzer: {err}")

    def get_stored_data(self):
        [date_tuple, energy_tuple] = self.dataBase.get_all_date_and_energy_values()
        date_obj = tuple(datetime.strptime(date, '%d.%m.%Y') for date in date_tuple)

        return date_obj, energy_tuple

