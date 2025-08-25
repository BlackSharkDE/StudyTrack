##########################################################################################################
#
# DatabaseConnector.py
#
# Regelt Datenbankzugriff zu SQLite.
#
##########################################################################################################

import sqlite3
from pathlib import Path

class DatabaseConnector:
    """
    Statische Klasse für das Handling der Datenbankanbingung an SQLite.
    """

    #"Protected" Attribut: Datenbankverbindung über Methoden hinweg
    _connection = None

    #"Private" Attribut: Pfad der Datenbankdatei -> Liegt im gleichen Verzeichnis wie diese Datei
    _databaseFile = Path(__file__).parent.resolve() / "studytrack.db"

    ######################################################################################################

    def __new__(cls):
        """
        Verhindere VOR der Objekterstellung, dass ein Objekt erstellt wird.
        """
        raise TypeError("Diese Klasse darf nicht instanziiert werden.")

    def __str__() -> str:
        """
        Repräsentation für UI
        """
        s = "-- DatabaseConnector -- \n\n"
        s += f"__connection  : {DatabaseConnector._connection}\n"
        s += f"__databaseFile: {DatabaseConnector._databaseFile}\n"
        return s

    ######################################################################################################
    #-- Verbindung --

    @staticmethod
    def isConnected() -> bool:
        """
        Gibt an, ob eine Verbindung zur Datenbank besteht.

        Returns:
            bool: Wenn die Verbindung besteht True, ansonsten False
        """
        return DatabaseConnector._connection is not None

    @staticmethod
    def connectToDB():
        """
        Stellt die Verbindung zur Datenbank her.
        """
        if not DatabaseConnector.isConnected():
            DatabaseConnector._connection = sqlite3.connect(DatabaseConnector._databaseFile)

    @staticmethod
    def disconnectFromDB():
        """
        Schließt die Verbindung zur Datenbank.
        """
        if DatabaseConnector.isConnected():
            DatabaseConnector._connection.close()
            DatabaseConnector._connection = None

    ######################################################################################################
    #-- Interaktion --

    @staticmethod
    def execute(sql:str,params:tuple = ()):
        """
        Führt einen SQL-Befehl in der Datenbank aus, keine Rückgabe.

        Args:
            sql (str)     : Der SQL-Befehl als prepared Statement: INSERT INTO students (name) VALUES (?)
            params (tuple): Parameter für Statement: ("Alice",)
        """
        if DatabaseConnector._connection is None:
            raise RuntimeError("Keine Verbindung zur Datenbank!")
        cursor = DatabaseConnector._connection.cursor()
        cursor.execute(sql,params)
        DatabaseConnector._connection.commit()
        cursor.close()

    @staticmethod
    def query(sql:str,params:tuple = ()):
        """
        Führt einen SQL-Befehl in der Datenbank aus, mit Rückgabe.

        Args:
            sql (str)     : Der SQL-Befehl als prepared Statement: INSERT INTO students (name) VALUES (?)
            params (tuple): Parameter für Statement: ("Alice",)
        Returns:
            misc
        """
        if DatabaseConnector._connection is None:
            raise RuntimeError("Keine Verbindung zur Datenbank!")
        cursor = DatabaseConnector._connection.cursor()
        cursor.execute(sql, params)
        results = cursor.fetchall()
        cursor.close()
        return results

    ######################################################################################################
    #-- Verwaltung --

    @staticmethod
    def createDatabase() -> bool:
        """
        Erstellt das Datenbankschema der Anwendung.

        Returns:
            bool: False = Es wurde kein Setup gemacht / True = Setup wurde gemacht
        """

        #Prüfe, ob die Datenbank bereis eingerichtet wurde
        #q = DatabaseConnector.query("SELECT name FROM sqlite_master WHERE type='table' AND name='courses';")
        #print(q)
        cursor = DatabaseConnector._connection.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='courses';")
        if not cursor.fetchone():

            #Die Statements für das Erstellen der Tabellen.
            tableSetupStatements = [
                """
                CREATE TABLE IF NOT EXISTS courses (
                    name TEXT NOT NULL,
                    courseId TEXT PRIMARY KEY,
                    description NOT NULL,
                    ects INTEGER NOT NULL,
                    startedAt DATE NOT NULL
                );
                """,
                """
                CREATE TABLE IF NOT EXISTS advancedworkbooks (
                    writtenOn DATE NOT NULL,
                    courseId TEXT NOT NULL,
                    t1 INTEGER NOT NULL,
                    t2 INTEGER NOT NULL,
                    t3 INTEGER NOT NULL,
                    t4 INTEGER NOT NULL,
                    t5 INTEGER NOT NULL,
                    t6 INTEGER NOT NULL,
                    elaboration INTEGER NOT NULL,
                    FOREIGN KEY (courseId) REFERENCES courses(courseId)
                );
                """,
                """
                CREATE TABLE IF NOT EXISTS classtests (
                    writtenOn DATE NOT NULL,
                    courseId TEXT NOT NULL,
                    score INTEGER NOT NULL,
                    FOREIGN KEY (courseId) REFERENCES courses(courseId)
                );
                """
            ]

            for tableSetupStatement in tableSetupStatements:
                DatabaseConnector.execute(tableSetupStatement)
            
            #Die Statements für das Einrichten von Demo-Daten
            demoSetupStatements = [

                #-- Kurse --
                """
                INSERT INTO courses VALUES (
                    'Einführung in das wissenschaftliche Arbeiten für IT und Technik',
                    'DLBWIRITT01',
                    'Als Forschende hält man Argumente nicht einfach für wahr, sondern geht ihnen systematisch auf den Grund.',
                    5,
                    '2025-01-28'
                );
                """,
                """
                INSERT INTO courses VALUES (
                    'Spezifikation',
                    'ISPE01',
                    'Anforderungsanalysen müssen Anforderungen an IT-Systeme präzise beschrieben werden.',
                    5,
                    '2025-02-01'
                );
                """,
                """
                INSERT INTO courses VALUES (
                    'Datenstruktur und Java-Klassenbibliothek',
                    'DLBCSDSJCL02_D',
                    'Kenntnisse der objektorientierten Programmierung werden am Beispiel von Java vertieft.',
                    5,
                    '2025-02-18'
                );
                """,
                """
                INSERT INTO courses VALUES (
                    'Algorithmen, Datenstrukturen und Programmiersprachen',
                    'DLBIADPS01-01',
                    'Geeignete Algorithmen und Datenstrukturen auswählen und diese in Programmcode umzusetzen.',
                    5,
                    '2025-03-11'
                );
                """,
                """
                INSERT INTO courses VALUES (
                    'Einführung in Data Science',
                    'DLBDSIDS01-01_D',
                    'Data Science hat sich als multidisziplinäres Feld entwickelt, das darauf abzielt, aus Daten Werte zu schaffen.',
                    5,
                    '2025-05-21'
                );
                """,

                #-- Examen -> Advanced Workbooks --
                """
                INSERT INTO advancedworkbooks VALUES (
                    '2025-02-10',
                    'DLBWIRITT01',
                    15,
                    15,
                    15,
                    15,
                    15,
                    15,
                    9
                );
                """,
                """
                INSERT INTO advancedworkbooks VALUES (
                    '2025-04-29',
                    'DLBIADPS01-01',
                    15,
                    14,
                    15,
                    12,
                    15,
                    15,
                    7
                );
                """,

                #-- Examen -> Klausuren --
                """
                INSERT INTO classtests VALUES (
                    '2025-02-20',
                    'ISPE01',
                    45
                );
                """,
                """
                INSERT INTO classtests VALUES (
                    '2025-02-20',
                    'ISPE01',
                    80
                );
                """
            ]

            for demoSetupStatement in demoSetupStatements:
                DatabaseConnector.execute(demoSetupStatement)

            #Daten committen
            DatabaseConnector._connection.commit()

            #Setup ausgeführt
            return True
        
        #Kein Setup
        return False