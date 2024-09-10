import classes.generic_widget_class as gen_widgets
import UI_constants
import customtkinter as ctk
import matplotlib
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class resultsVisualizer:
    def __init__(self, parent, calculationClass):
        self.master = parent
        self.calculation = calculationClass
        self.resultsWindow = gen_widgets.newWindow(self.master.master, UI_constants.MIN_WINDOW_SIZE_RESULTS,
                                             UI_constants.MAX_WINDOW_SIZE_RESULTS)

        self.resultsWindow.window.title("Ergebnisse")
        if self.master.disable_buttons_callback is not None:
            self.master.disable_buttons_callback()

        self.resultsWindow.window.protocol("WM_DELETE_WINDOW", self.on_window_close)

        gen_widgets.newWindow.center_window(self.resultsWindow.window,
                                            UI_constants.MAX_WINDOW_SIZE_RESULTS[0],
                                            UI_constants.MAX_WINDOW_SIZE_RESULTS[1])

    def on_window_close(self):
        if self.master.enable_buttons_callback is not None:
            self.master.enable_buttons_callback()

        # Enable run button
        self.master.analysis_is_running = False
        self.master.button_run.configure(state="normal")