##########################################################################################################
#
# Course.py
#
# Ein zu überwachender Kurs.
#
##########################################################################################################

from datetime import date, datetime

from utils.DatabaseConnector import DatabaseConnector

from .exams.AdvancedWorkbook import AdvancedWorkbook
from .exams.ClassTest import ClassTest
from .exams.Exam import Exam
from typing import Optional

class Course:

    def __init__(self,name:str,courseId:str,description:str,ects:int,
        exams:list,startedAt:date = date.today()
    ):
        """
        Konstruktor
        
        Args:
            name (str)       : Der Kursname
            courseId (str)   : Die Kursnummer / ID (kann Zahlen und Buchstaben haben) ; Ist PrimaryKey in DB
            description (str): Beschreibung des Kurses und seiner Inhalte
            ects (int)       : Wie viele ECTS der Kurs bringt
            exams (list)     : Liste mit "Exam"-Objekten => Alle geschriebenen Prüfungen
            startedAt (date) : Wann der Kurs gestartet wurde (Automatisch, kann manuell gesetzt werden)
        """
        self.name         = name
        self.courseId     = courseId
        self.description  = description
        self.ects         = ects
        self.exams        = exams
        self.startedAt    = startedAt

    def __str__(self) -> str:
        """
        Repräsentation für UI

        Returns:
            str: Stringrepräsentation des Objektes
        """
        s  = "-- Kurs --\n\n"
        s += f"Name        : {self.name}\n"
        s += f"Kursnummer  : {self.courseId}\n"
        s += f"Beschreibung: {self.description}\n"
        s += f"ECTS        : {self.ects}\n"
        s += f"Gestartet am: {self.startedAt}\n"
        s += f"Bestanden   : {self.passed()}\n"
        s += f"Versuche    : {self.tries()}\n"
        s += f"Note        : {self.getGrade()}\n"
        for exam in self.exams:
            s += exam.__str__()
        return s

    def shortRepresentation(self) -> str:
        """
        Repräsentation für UI (ohne Kurse und Headline)

        Returns:
            str: Stringrepräsentation des Objektes in Kurzform
        """
        s  = f"Name        : {self.name}\n"
        s += f"Kursnummer  : {self.courseId}\n"
        s += f"Beschreibung: {self.description}\n"
        s += f"ECTS        : {self.ects}\n"
        s += f"Gestartet am: {self.startedAt}\n"
        s += f"Bestanden   : {self.passed()}\n"
        s += f"Versuche    : {self.tries()}\n"
        s += f"Note        : {self.getGrade()}\n"
        return s

    def __eq__(self,other) -> bool:
        """
        Gleichheit

        Returns:
            bool: True wenn beide gleich sind
        """
        return self.courseId == other.courseId

    ######################################################################################################

    def getFirstPassedExam(self) -> Optional[Exam]:
        """
        Gibt das erste gefundene Examen zurück, welches als bestanden markiert ist.

        Returns:
            Exam: Bzw. eines der Unterklassen oder None wenn kein Examen gefunden wurde
        """
        for exam in self.exams:
            if exam.passed():
                return exam
        return None

    def passed(self) -> str:
        """
        Prüft, ob der Kurs bereits bestanden wurde (es muss ein Exam verknüpft sein, welches als bestanden
        markiert wurde).

        Returns:
            str: "Ja" / "Nein" / "Endgültig nicht"
        """

        #Prüfe, ob es ein bestandenes Examen gibt
        if self.getFirstPassedExam() is not None:
            return "Ja"

        #Wenn es kein bestandenes Examen gibt und es 3 oder mehr Versuche sind, ist der Kurs endgültig
        #nicht bestanden
        if self.tries() >= 3:
            return "Endgültig nicht"

        #Wenn es kein bestandenes Examen gibt, aber noch weniger als 3 Versuche sind, kann der Kurs noch
        #bestanden werden
        return "Nein"
    
    def tries(self) -> int:
        """
        Wie viele Versuche für den Kurs bereits absolviert wurden (hängt an Anzahl verknüpfter Examen).

        Returns:
            int: Anzahl der Examen
        """
        return len(self.exams)

    def getGrade(self) -> float:
        """
        Gibt die Note aus den Punkten zurück. Implementiert den Notenschlüssel der IU.

        Returns:
            float: 1.0, 1.3, 1.7 etc. / 0.0 wenn kein bestandenes Examen verknüpft ist
        """

        passedExam = self.getFirstPassedExam()
        if passedExam is None:
            return 0.0

        grades = [
            (96,100,1.0),
            (91,95.9,1.3),
            (86,90.9,1.7),
            (81,85.9,2.0),
            (76,80.9,2.3),
            (71,75.9,2.7),
            (66,70.9,3.0),
            (61,65.9,3.3),
            (56,60.9,3.7),
            (50,55.9,4.0),
            (0,49.9,5.0)
        ]

        for minPoints, maxPoints, grade in grades:
            if minPoints <= passedExam.points() <= maxPoints:
                return grade

    ######################################################################################################
    #-- Datenbank --

    def saveToDB(self):
        """
        Speichert einen/den Course in die Datenbank.
        """
        DatabaseConnector.execute(
            """
            INSERT INTO courses (name,courseId,description,ects,startedAt) VALUES (?,?,?,?,?)
            """,
            (self.name,self.courseId,self.description,self.ects,self.startedAt,)
        )

    @staticmethod
    def getAllFromDB() -> list:
        """
        Fragt alle Course-Objekte aus der Datenbank ab.

        Returns:
            list: Eine Liste mit Course-Objekten
        """

        #Alle Kurse aus DB abfragen
        courseTuples = DatabaseConnector.query(
            """
            SELECT * FROM courses;
            """
        )

        #Hole alle Exams aus der Datenbank
        aws = AdvancedWorkbook.getAllFromDB()
        cts = ClassTest.getAllFromDB()

        #Rückgabe
        courses = list()

        #Aus DB geladene Tuple in Objekte parsen
        for courseTuple in courseTuples:

            #Um mehrfachzugriffe zu vermeiden
            courseId = courseTuple[1]

            #Suche alle Exams heraus, die zu der "courseId" des aktuellen Kurses passen
            courseAws = [aw for aw in aws if aw.courseId == courseId]
            courseCts = [ct for ct in cts if ct.courseId == courseId]

            #Merge aller gefundenen Exams
            examsForCourse = courseAws + courseCts

            courses.append(
                Course(
                    courseTuple[0],
                    courseId,
                    courseTuple[2],
                    courseTuple[3],
                    examsForCourse,
                    datetime.strptime(courseTuple[4],"%Y-%m-%d").date()
                )   
            )

        return courses