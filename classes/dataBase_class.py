import sqlite3
import UI_constants
import os
import datetime


class dataBase:
    def __init__(self):
        self.connector = None
        self.cursor = None
        self.db_name = None
        self.db_path = None
        self.data_isValid = None
        self.table_name = UI_constants.DEF_TABLE_NAME
        self.subfolder_path = os.path.join(os.getcwd(), UI_constants.DEF_DB_ROOT)
        self.initial_values = []    # [init_id, init_dateString, init_value]
        self.initial_elem_id = UI_constants.DEF_INIT_ELEM_ID
        self.existing_db_files = self.get_existing_db_files()
        self.remove_dropDownValue_callback = None

        self.ENERGY_PRICE_EUR_kWh = UI_constants.DEF_ENERGY_PRICE_EUR_kWh
        self.ANNUAL_BASIC_PRICE_EUR = UI_constants.DEF_ANNUAL_BASIC_PRICE_EUR
        self.MONTHLY_COSTS_EUR = UI_constants.DEF_MONTHLY_COSTS_EUR
        self.ADD_CREDIT_EUR = UI_constants.DEF_ADD_CREDIT_EUR
        self.ABS_CURRENT_TAX_EUR_kWh = UI_constants.DEF_ABS_ELECTRICITY_TAX_EUR
        self.VA_TAX_REL = UI_constants.DEF_VA_TAX_PERCENTAGE / 100
        self.min_size_cost_analyzer = UI_constants.MIN_WINDOW_SIZE
        self.max_size_cost_analyzer = UI_constants.MAX_WINDOW_SIZE

        print(f">> Vorliegende Datenbanken: {self.existing_db_files}")

    def create_database(self, db_name, number_str, date_str):
        try:
            self.db_name = f"{db_name}{'.db'}"
            self.db_path = os.path.join(self.subfolder_path, self.db_name)

            # Create a new database or connect to an existing one
            self._create_db_directory()
            self.connector = sqlite3.connect(self.db_path)
            self.cursor = self.connector.cursor()

            # Set initial values
            self.initial_values.insert(0, self.initial_elem_id)
            self.initial_values.insert(1, date_str)
            self.initial_values.insert(2, float(number_str))

            self.cursor.execute(f"""
                        CREATE TABLE IF NOT EXISTS {self.table_name} (
                            elem_id INTEGER PRIMARY KEY,
                            date TEXT NOT NULL,
                            energy_value REAL NOT NULL
                        )""")

            self.insert_values_into_table(self.initial_values[0],
                                          self.initial_values[1],
                                          self.initial_values[2])

            print(f">> Neue Datenbank wurde erstellt: {self.db_name}")

        except sqlite3.OperationalError as err:
            raise Exception(f"Unexpected error @create_database(): {err}")
        finally:
            self.connector.close()

    def _create_db_directory(self):
        try:
            if not os.path.exists(self.subfolder_path):
                os.makedirs(self.subfolder_path)

        except (FileNotFoundError, OSError) as err:
            raise Exception(f"Unexpected error @create_db_directory(): {err}")

    def insert_values_into_table(self, elem_id, date, energy_value):
        try:
            self.cursor.execute(f"""
                        INSERT INTO {self.table_name} (elem_id, date, energy_value)
                        VALUES (?, ?, ?)
                        """, (elem_id, date, energy_value))
            self.connector.commit()

        except sqlite3.OperationalError as err:
            raise Exception(f"Unexpected error @insert_values_into_table(): {err}")

    def get_all_date_and_energy_values(self):
        self.open_database(self.db_name)
        try:
            self.cursor.execute(f"""
                SELECT date, energy_value FROM {self.table_name}
            """)
            results = self.cursor.fetchall()  # [[date, energy_value], ...]
            date_tuple, energy_tuple = zip(*results)

            return date_tuple, energy_tuple

        except sqlite3.OperationalError as err:
            raise Exception(f"Unexpected error @get_date_and_energy_values(): {err}")

    def get_db_name(self):
        return self.db_name

    def get_init_db_values(self):
        return self.initial_values

    def get_db_path(self):
        return self.db_path

    def _check_for_existing_db(self):
        if os.path.exists(self.subfolder_path) and any(os.scandir(self.subfolder_path)):
            return True
        else:
            return False

    def get_existing_db_files(self):
        files = None
        if self._check_for_existing_db():
            files = [file for file in os.listdir(self.subfolder_path)
                     if os.path.isfile(os.path.join(self.subfolder_path, file))
                     and file.endswith('.db')]

        return files

    def add_data_to_existing_db(self, db_name, new_date, new_energy_value):
        try:
            # Open the existing database
            self.open_database(db_name)
            self.data_isValid = self._validate_input_data(new_date, new_energy_value)

            if self.data_isValid:
                self.cursor.execute(f"""
                    INSERT INTO {self.table_name} (date, energy_value)
                    VALUES (?, ?)
                """, (new_date, new_energy_value))
                self.connector.commit()
                print(f">> Neuer Eintrag hinzugefügt in: {db_name}")
            else:
                print(f"Invalid input data @add_data_to_existing_db(): {new_date}, {new_energy_value}")

            return self.data_isValid

        except sqlite3.OperationalError as err:
            raise Exception(f"Error @add_data_to_existing_db(): {err}")

        finally:
            self.connector.close()

    def open_database(self, db_name):
        try:
            # Check if the database exists
            if not self._check_for_existing_db():
                raise Exception("No database file found")

            self.db_path = os.path.join(self.subfolder_path, db_name)
            self.connector = sqlite3.connect(self.db_path)
            self.cursor = self.connector.cursor()

        except sqlite3.OperationalError as err:
            raise Exception(f"Unexpected error @open_selected_database(): {err}")

    def get_last_elem_id(self):
        try:
            self.cursor.execute(f"""
                SELECT MAX(elem_id) FROM {self.table_name}
            """)
            result = self.cursor.fetchone()  # [elem_id]

            return result[0] if result else None

        except sqlite3.OperationalError as err:
            raise Exception(f"Unexpected error @get_last_elem_id(): {err}")

    def delete_last_entry_from_db(self, db_name):
        try:
            # Open the existing database
            self.open_database(db_name)
            last_elem_id = self.get_last_elem_id()

            # Delete the last entry
            self.cursor.execute(f"""
                  DELETE FROM {self.table_name} WHERE elem_id = ?
              """, (last_elem_id,))
            self.connector.commit()

            print(f">> Removed last entry from database: {db_name} with the id: {last_elem_id}")

            return last_elem_id

        except sqlite3.OperationalError as err:
            raise Exception(f"Unexpected error @remove_last_entry_from_db(): {err}")
        finally:
            self.connector.close()

    def get_last_db_values_by_id(self, elem_id):
        try:
            self.cursor.execute(f"""
                SELECT date, energy_value FROM {self.table_name}
                WHERE elem_id = ?
                ORDER BY date DESC
                LIMIT 1
            """, (elem_id,))
            result = self.cursor.fetchone()  # [date_value, energy_value]
            date_value = datetime.datetime.strptime(result[0], "%d.%m.%Y")
            energy_value = float(result[1])

            return [date_value, energy_value]

        except sqlite3.OperationalError as err:
            raise Exception(f"Unexpected error @get_last_db_values_by_id(): {err}")

    def _validate_input_data(self, date_value, energy_value: float):
        try:
            [last_date_value, last_energy_value] = self.get_last_db_values_by_id(self.get_last_elem_id())
            date_diff = datetime.datetime.strptime(date_value, "%d.%m.%Y") - last_date_value

            if energy_value <= last_energy_value or date_diff.days <= 0:
                return False
            else:
                return True

        except Exception as err:
            raise Exception(f"Unexpected error @_validate_input_data(): {err}")

    def delete_selected_database(self, db_name):
        try:
            if self._check_for_existing_db():
                os.remove(os.path.join(self.subfolder_path, db_name))
                print(f">> Gelöschte Datenbank: {db_name}")
                self.existing_db_files = self.get_existing_db_files()

                if self.remove_dropDownValue_callback is not None:
                    self.remove_dropDownValue_callback(db_name)

            else:
                raise Exception(f"Selected database {db_name} does not exist.")

        except Exception as err:
            raise Exception(f"Error @delete_selected_database(): {err}")