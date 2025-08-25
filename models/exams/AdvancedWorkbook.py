##########################################################################################################
#
# AdvancedWorkbook.py
#
# Eine konkrete Klasse von "Exam". Implementiert ein Advanced Workbook.
#
##########################################################################################################

from datetime import date, datetime

from .Exam import Exam
from utils.DatabaseConnector import DatabaseConnector

class AdvancedWorkbook(Exam):

    def __init__(self,writtenOn:date,courseId:str,
        t1:int,t2:int,t3:int,t4:int,t5:int,t6:int,elaboration:int
    ):
        """
        Konstruktor

        Args:
            writtenOn (date) : Siehe Konstruktor Exam
            courseId (str)   : Siehe Konstruktor Exam
            t1 (int)         : Punkte bei Aufgabe 1
            t2 (int)         : Punkte bei Aufgabe 2
            t3 (int)         : Punkte bei Aufgabe 3
            t4 (int)         : Punkte bei Aufgabe 4
            t5 (int)         : Punkte bei Aufgabe 5
            t6 (int)         : Punkte bei Aufgabe 6
            elaboration (int): Punkte in der Ausführung
        """
        super().__init__(writtenOn,courseId)
        self.t1          = Exam.truncatePoints(t1,15)
        self.t2          = Exam.truncatePoints(t2,15)
        self.t3          = Exam.truncatePoints(t3,15)
        self.t4          = Exam.truncatePoints(t4,15)
        self.t5          = Exam.truncatePoints(t5,15)
        self.t6          = Exam.truncatePoints(t6,15)
        self.elaboration = Exam.truncatePoints(elaboration,10)

    def __str__(self) -> str:
        """
        Überschreibe: Repräsentation für UI

        Returns:
            str: Stringrepräsentation des Objektes
        """
        s = "\n-- Advanced Workbook --\n\n"
        s += super().__str__() + "\n"
        s += f"Punkte bei Aufgabe 1    : {self.t1}\n"
        s += f"Punkte bei Aufgabe 2    : {self.t2}\n"
        s += f"Punkte bei Aufgabe 3    : {self.t3}\n"
        s += f"Punkte bei Aufgabe 4    : {self.t4}\n"
        s += f"Punkte bei Aufgabe 5    : {self.t5}\n"
        s += f"Punkte bei Aufgabe 6    : {self.t6}\n"
        s += f"Punkte in der Ausführung: {self.elaboration}\n"
        return s

    def points(self) -> int:
        """
        Implementiert die abstrakte Methode "points" von "Exam".
        """
        return self.t1 + self.t2 + self.t3 + self.t4 + self.t5 + self.t6 + self.elaboration

    def saveToDB(self):
        """
        Implementiert die abstrakte Methode "saveToDB" von "Exam".
        """
        DatabaseConnector.execute(
            """
            INSERT INTO advancedworkbooks (
                writtenOn,courseId,t1,t2,t3,t4,t5,t6,elaboration
            )
            VALUES (?,?,?,?,?,?,?,?,?)
            """,
            (self.writtenOn,self.courseId,
             self.t1,self.t2,self.t3,self.t4,self.t5,self.t6,self.elaboration,)
        )

    def getAllFromDB() -> list:
        """
        Implementiert die abstrakte, statische Methode "getAllFromDB" von "Exam"
        """

        #Alle Kurse aus DB abfragen
        examTuples = DatabaseConnector.query(
            """
            SELECT * FROM advancedworkbooks;
            """
        )

        #Rückgabe
        exams = list()

        #Aus DB geladene Tuple in Objekte parsen
        for examTuple in examTuples:
            exams.append(
                AdvancedWorkbook(
                    datetime.strptime(examTuple[0], "%Y-%m-%d").date(),
                    examTuple[1],
                    examTuple[2],
                    examTuple[3],
                    examTuple[4],
                    examTuple[5],
                    examTuple[6],
                    examTuple[7],
                    examTuple[8]
            )   )

        return exams