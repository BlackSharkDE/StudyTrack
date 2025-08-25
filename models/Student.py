##########################################################################################################
#
# Student.py
#
# Der User des Programms (Single-User).
#
##########################################################################################################

from datetime import date

class Student:

    def __init__(self,name:str,birthday:date,studentNumber:str,degree:str,courses:list,period:int,
        enrolled:date,ects:int
    ):
        """
        Konstruktor

        Args:
            name (str)         : Vorname, Nachname des Studenten
            birthday (date)    : Geburtstag des Studenden
            studentNumber (str): Matrikelnummer
            degree (str)       : Angestrebter Abschluss / Studiengang
            courses (list)     : Liste mit "Course"-Objekten
            period (int)       : Regelstudienzeit in Semester
            enrolled (date)    : Wann das Studium gestartet wurde
            ects (int)         : Wie viele ECTS man für den Abschluss benötigt
        """
        self.name          = name
        self.birthday      = birthday
        self.studentNumber = studentNumber
        self.degree        = degree
        self.courses       = courses
        self.period        = period
        self.enrolled      = enrolled
        self.ects          = ects

    def __str__(self) -> str:
        """
        Repräsentation für UI

        Returns:
            str: Stringrepräsentation des Objektes
        """
        s  = "-- Student --\n\n"
        s += f"Name              : {self.name}\n"
        s += f"Geburtstag        : {self.birthday}\n"
        s += f"Matrikelnummer    : {self.studentNumber}\n"
        s += f"Studiengang       : {self.degree}\n"
        s += f"Kurse             : {len(self.courses)}\n"
        s += f"Regelstudienzeit  : {self.period}\n"
        s += f"Eingeschrieben am : {self.enrolled}\n"
        s += f"ECTS für Abschluss: {self.ects}\n"
        return s