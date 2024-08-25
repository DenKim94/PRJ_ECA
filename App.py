from classes import UI_class
import UI_constants


# Main file to run the application
if __name__ == "__main__":
    shardedAppStates = UI_class.sharedAppStates(UI_constants)
    App = UI_class.App(shardedAppStates, UI_constants)


