#!/usr/bin/env python3
from classes import UI_class


# Main file to run the application
if __name__ == "__main__":
    shardedAppStates = UI_class.sharedAppStates()
    App = UI_class.App(shardedAppStates)
