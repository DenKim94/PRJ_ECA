# GENERAL
CREATE_LOG_FILE = False   # Optional: Create log file for debugging (To-Do)
GUI_TITLE = "Energy Costs Analyzer"
GUI_WIDTH = 550
GUI_HEIGHT = 350
GUI_MAX_WIDTH = 550
GUI_MAX_HEIGHT = 350
GUI_MIN_WIDTH = 550
GUI_MIN_HEIGHT = 350
DEF_APPEARANCE_MODE = "system"      # "dark"; "light"; "system"
DEF_COLOR_THEME = "blue"            # "blue"; "dark-blue"; "green"
DEF_FONT = "Futura"                 # e.g. Arial (Default); Courier; Times New Roman
DEF_MAIN_FRAME_PADDING = [50, 10]   # [pad_x, pad_y] in pixel
DEF_ICON_ROOT = "icons"
DEF_ICON_NAME = "ECA_icon.png"

# PARAMETERS FOR CALCULATIONS
DEF_DAYS_YEAR = 365
DEF_DAYS_MONTH = 30.44                          # Average days in a month
DEF_ADD_CREDIT_EUR = 0                          # Additional credit in EUR
DEF_ENERGY_PRICE_EUR_kWh = 0.3207               # Price in EUR/kWh
DEF_ANNUAL_BASIC_PRICE_EUR = 112.8              # Price in EUR/Year
DEF_ABS_ELECTRICITY_TAX_EUR = 0.0205            # Price in EUR/kWh; To be adjusted here if needed
DEF_MONTHLY_COSTS_EUR = 44                      # Price in EUR/Month
DEF_VA_TAX_PERCENTAGE = 19                      # Value added tax in % (0 < val < 100); To be adjusted here if needed
DEF_TAX_X_PERCENTAGE = 3                        # Additional taxes (e.g. concession fee, levies)

# CONFIGURATIONS
CONFIGS_ENTRY_WIDTH = 120
CONFIGS_LABEL_WIDTH = 200

# ICON
ICON_WIDTH = 65
ICON_HEIGHT = 65

# LABELS
LABEL_TEXT = "ICON"
LABEL_WIDTH = 160
FONT_SIZE_LABEL = 16

# BUTTONS
CURSOR_TYPE = "arrow"
BUTTON_WIDTH = 120
FONT_SIZE_BUTTON = 14

# DROPDOWN
DROPDOWN_WIDTH = 300
FONT_SIZE_DROPDOWN = 14
PLACEHOLDER_TEXT = "Keine Auswahl"

# ENTRY
ENTRY_WIDTH = 200

# DATABASE
PLACEHOLDER_DB_NAME = "<Zählernummer>_Q<Quartalzahl>_<Jahr>"
DEF_DB_ROOT = "database"    # Name of database root folder
DEF_TABLE_NAME = "used_energy"
ENTRY_WIDTH_DB = 280
DEF_INIT_ELEM_ID = 1

# EDIT DATABASE WINDOW
MIN_WINDOW_SIZE = [420, 250]  # [width, height] in pixel
MAX_WINDOW_SIZE = [420, 250]  # [width, height] in pixel

# RESULTS VISUALIZER
MIN_WINDOW_SIZE_RESULTS = [550, 350]  # [min_width, min_height] in pixel
MAX_WINDOW_SIZE_RESULTS = [850, 500]  # [max_width, max_height] in pixel



