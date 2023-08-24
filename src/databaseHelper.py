import sqlite3
from dataclasses import dataclass

DB_PATH = "../main.sqlite"

# Abstrakte Parent-Klasse für alle Datenbanktabellen
class AbstractDatabaseHelper:
    def __init__(self, table_name=None) -> None:
        self.TABLE_NAME = table_name
        self.DB_PATH = DB_PATH
        self.connection = sqlite3.connect(self.DB_PATH)
        self.cursor = self.connection.cursor()

    def commit(self):
        self.connection.commit()
     
    def close(self):
        self.connection.close()

    def selectAll(self): 
        return self.cursor.execute(f'SELECT * FROM {self.TABLE_NAME};').fetchall()
    
    def deleteTable(self):
        return self.cursor.execute(f'DROP TABLE IF EXISTS {self.TABLE_NAME}')

# Datentyp für Personen
@dataclass
class Person:
    person_id: int = None
    name: str = ""
    title: str = ""
    university: str = ""
    department: str = ""
    scholar_id: str = ""

# Helper-Klasse für Personen Tabelle
class PersonDatabaseHelper(AbstractDatabaseHelper):
    def __init__(self) -> None:
        super().__init__(table_name="person")

    def createTable(self):
        self.cursor.execute(
            f'''
            CREATE TABLE IF NOT EXISTS {self.TABLE_NAME} (
                personId INTEGER PRIMARY KEY ASC, 
                name TEXT, 
                title TEXT, 
                university TEXT,
                department TEXT,
                scholarId TEXT
            );
            '''
        )

    def insertPerson(self, person: Person):
        insert = self.cursor.execute(
            f''' 
            INSERT INTO {self.TABLE_NAME} (name, title, university, department, scholarId)
            VALUES ("{person.name}", "{person.title}", "{person.university}", "{person.department}", "{person.scholar_id}");
            '''
        )
        return insert
    
    def insertPersons(self, persons: [Person]):
        for person in persons:
            self.insertPerson(person)
        print(f"inserted {len(persons)} rows into table {self.TABLE_NAME}")

    def updateField(self, id: int, field: str, value: str):
        self.cursor.execute(
            f'''
            UPDATE {self.TABLE_NAME}
            SET {field} = "{value}"
            WHERE personId = {str(id)};
            '''
        )
