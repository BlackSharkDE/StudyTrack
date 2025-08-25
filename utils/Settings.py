##########################################################################################################
#
# Settings.py
#
# Globale Einstellungen, hier kann man Dinge ändern.
#
##########################################################################################################

from datetime import date

from models.Student import Student
from .DatabaseConnector import DatabaseConnector

class Settings:
    """
    Statische Klasse für das Speichern von Einstellungen etc.
    """

    #"Private" Attribut: User
    _student = Student(
        "Max Mustermann",
        date(2000,1,1),
        "IU12345678",
        "Bachelor Softwareentwicklung",
        list(), #Aus DB holen bzw. später setzen
        12,
        date(2025,2,2),
        180
    )

    #"Private" Attribute: Gibt an, ab wie vielen Punkten ein Exam bestanden ist (>= Wert)
    _pointsToPass = 50

    ######################################################################################################

    def __new__(cls):
        """
        Verhindere VOR der Objekterstellung, dass ein Objekt erstellt wird.
        """
        raise TypeError("Diese Klasse darf nicht instanziiert werden.")

    def __str__() -> str:
        """
        Repräsentation für UI

        Returns:
            str: Stringrepräsentation des Objektes
        """
        s  = "-- Einstellungen --\n\n"
        s += f"Anzahl benötigter Punkte zum Bestehen eines Kurses: {Settings._pointsToPass}\n"
        s += f"Datenbankdatei: {DatabaseConnector._databaseFile}\n"
        s += f"\n{str(Settings._student)}"
        return s