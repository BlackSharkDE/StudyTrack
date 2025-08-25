##########################################################################################################
#
# ClassTest.py
#
# Eine konkrete Klasse von "Exam". Implementiert eine Klausur.
#
##########################################################################################################

from datetime import date, datetime

from .Exam import Exam
from utils.DatabaseConnector import DatabaseConnector

class ClassTest(Exam):

    def __init__(self,writtenOn:date,courseId:str,score:int):
        """
        Konstruktor

        Args:
            writtenOn (date): Siehe Konstruktor Exam
            courseId (str)  : Siehe Konstruktor Exam
            score (int)     : Wie viele Punkte in der Klausur insgesamt erreicht wurden
        """
        super().__init__(writtenOn,courseId)
        self.score = Exam.truncatePoints(score,100)

    def __str__(self) -> str:
        """
        Überschreibe: Repräsentation für UI

        Returns:
            str: Stringrepräsentation des Objektes
        """
        s  = "\n-- Klausur --\n\n"
        s += super().__str__() + "\n"
        return s

    def points(self) -> int:
        """
        Implementiert die abstrakte Methode "points" von "Exam".
        """
        return self.score
    
    def saveToDB(self):
        """
        Implementiert die abstrakte Methode "saveToDB" von "Exam".
        """
        DatabaseConnector.execute(
            """
            INSERT INTO classtests (
                writtenOn,courseId,score
            )
            VALUES (?,?,?)
            """,
            (self.writtenOn,self.courseId,self.score,)
        )

    def getAllFromDB() -> list:
        """
        Implementiert die abstrakte, statische Methode "getAllFromDB" von "Exam"
        """

        #Alle Kurse aus DB abfragen
        examTuples = DatabaseConnector.query(
            """
            SELECT * FROM classtests;
            """
        )

        #Rückgabe
        exams = list()

        #Aus DB geladene Tuple in Objekte parsen
        for examTuple in examTuples:
            exams.append(
                ClassTest(
                    datetime.strptime(examTuple[0], "%Y-%m-%d").date(),
                    examTuple[1],
                    examTuple[2]
            )   )

        return exams