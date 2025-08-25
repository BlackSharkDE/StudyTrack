##########################################################################################################
#
# Exam.py
#
# Ein Examen (Prüfung) in einem Kurs, die man bereits bearbeitet hat.
#
##########################################################################################################

from datetime import date
from abc import ABC, abstractmethod

from utils.Settings import Settings

class Exam(ABC):
    """
    Abstrakte Basisklasse für alle Prüfungsarten
    """

    def __init__(self,writtenOn:date,courseId:str):
        """
        Konstruktor (diese Attribute haben alle Prüfungsarten gemeinsam)
        
        Args:
            writtenOn (date): Tag an dem das Examen gemacht wurde
            courseId (str)  : Die Kursnummer zu dem das Examen gehört
        """
        self.writtenOn = writtenOn
        self.courseId  = courseId

    def __str__(self) -> str:
        """
        Repräsentation für UI

        Returns:
            str: Stringrepräsentation des Objektes
        """
        #s  = "-- Examen --\n\n"
        s =  f"Bearbeitet am   : {self.writtenOn}\n"
        s += f"Kursnummer      : {self.courseId}\n"
        s += f"Punkte (von 100): {self.points()}\n"
        return s

    @staticmethod
    def truncatePoints(points:int,maxPoints:int) -> int:
        """
        Dient zum eingrenzen einer erreichten Punktzahl.

        Args:
            points (int)   : Der anzuschauende Wert
            maxPoints (int): Was die maximale Punktzahl sein kann
        
        Returns:
            int: 0, wenn Übergabe kleiner 0 und maxPoints, wenn Übergabe > maxPoints und
                 Points wenn >= 0 und <= maxPoints
        """
        if points < 0:
            return 0
        elif points >= 0 and points <= maxPoints:
            return points
        return maxPoints

    def passed(self) -> bool:
        """
        Gibt an, ob das Examen bestanden wurde.
        
        Returns:
            bool: True wenn ja / False wenn nein
        """
        return True if self.points() >= Settings._pointsToPass else False

    @abstractmethod
    def points(self) -> int:
        """
        Gibt zurück, wie viele Punkte (von 100) erzielt wurden.

        Returns:
            int: Anzahl der erreichten Gesamtpunkte des Exam
        """
        pass

    ######################################################################################################
    #-- Datenbank --

    @abstractmethod
    def saveToDB(self):
        """
        Speichert ein/das Exam in die Datenbank.
        """
        pass

    @staticmethod
    @abstractmethod
    def getAllFromDB(examType:int) -> list:
        """
        Fragt alle Exam-Objekte aus der Datenbank ab.

        Returns:
            list: Eine Liste mit Exam-Objekten (vom gegebenen Typ)
        """
        pass