import sqlite3
import UI_constants
import os


class dataBase:
    def __init__(self):
        self.connector = None
        self.cursor = None
        self.db_name = None
        self.db_path = None
        self.table_name = UI_constants.DEF_TABLE_NAME
        self.subfolder_path = os.path.join(os.getcwd(), UI_constants.DEF_DB_ROOT)
        self.initial_values = []    # [init_id, init_dateString, init_value]
        self.initial_elem_id = UI_constants.DEF_INIT_ELEM_ID
        self.existing_db_files = self.get_existing_db_files()

        print(f">> Existing database files: {self.existing_db_files}")

    def create_database(self, db_name, number_str, date_str):
        try:
            print(f">> @create_database: {db_name}, {number_str}, {date_str}")
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

        except sqlite3.OperationalError as err:
            raise Exception(f"Unexpected error @create_database(): {err}")
        finally:
            self.connector.close()

    def _create_db_directory(self):
        try:
            if not os.path.exists(self.subfolder_path):
                os.makedirs(self.subfolder_path)
                print(f">> @create_db_directory: {self.subfolder_path}")
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

    def get_values_by_id(self, elem_id):
        try:
            self.cursor.execute(f"""
                SELECT date, energy_value FROM {self.table_name}
                WHERE elem_id = ?
            """, (elem_id,))
            result = self.cursor.fetchone()  # [date, energy_value]
            return result

        except sqlite3.OperationalError as err:
            raise Exception(f"Unexpected error @get_values_by_elem_id(): {err}")

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
            print(f"Selected database name: {db_name}")
            print(f"new_date: {new_date}")
            print(f"new_energy_value: {new_energy_value}")

            # Open the existing database
            self.open_database(db_name)

            # Update the values in the table
            self.cursor.execute(f"""
                INSERT INTO {self.table_name} (date, energy_value)
                VALUES (?, ?)
            """, (new_date, new_energy_value))
            self.connector.commit()

        except sqlite3.OperationalError as err:
            raise Exception(f"Unexpected error @open_and_adjust_existing_db(): {err}")
        finally:
            self.connector.close()

    def open_database(self, db_name):
        try:
            # Check if the database exists
            if not self._check_for_existing_db():
                raise Exception(f"Database {db_name} does not exist")

            self.db_name = f"{db_name}"
            self.db_path = os.path.join(self.subfolder_path, self.db_name)
            self.connector = sqlite3.connect(self.db_path)
            self.cursor = self.connector.cursor()

        except sqlite3.OperationalError as err:
            raise Exception(f"Unexpected error @open_selected_database(): {err}")

    def get_last_elem_id(self):
        try:
            self.cursor.execute(f"""
                SELECT elem_id FROM {self.table_name}
                ORDER BY date DESC
                LIMIT 1
            """)
            result = self.cursor.fetchone()  # [elem_id]
            return result[0] if result else None

        except sqlite3.OperationalError as err:
            raise Exception(f"Unexpected error @get_last_elem_id(): {err}")