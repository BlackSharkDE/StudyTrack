##########################################################################################################
#
# ConsoleUI.py
#
# Regelt Eingabe und Ausgabe (E/A) in der Konsole.
#
##########################################################################################################

import sys
import os
from datetime import date, timedelta

from models.Course import Course
from models.exams.AdvancedWorkbook import AdvancedWorkbook
from models.exams.ClassTest import ClassTest

from .Settings import Settings
from .DatabaseConnector import DatabaseConnector

class ConsoleUI:
    """
    Statische Klasse für das Handling der UI bzw. der Eingabe und Ausgaben.
    """

    #"Private" Attribut: Das Applikations-Logo
    __logo = r"""
  _________ __            .___      ___________                     __    
 /   _____//  |_ __ __  __| _/__.__.\__    ___/___________    ____ |  | __
 \_____  \\   __\  |  \/ __ <   |  |  |    |  \_  __ \__  \ _/ ___\|  |/ /
 /        \|  | |  |  / /_/ |\___  |  |    |   |  | \// __ \\  \___|    < 
/_______  /|__| |____/\____ |/ ____|  |____|   |__|  (____  /\___  >__|_ \
        \/                 \/\/                           \/     \/     \/
    """

    #"Private" Attribute: Die aktuelle Seite
    __currentPage = 0

    ######################################################################################################

    def __new__(cls):
        """
        Verhindere VOR der Objekterstellung, dass ein Objekt erstellt wird.
        """
        raise TypeError("Diese Klasse darf nicht instanziiert werden.")

    ######################################################################################################

    @staticmethod
    def showLogo():
        """
        Zeigt das Logo des Programms an
        """
        print(ConsoleUI.__logo)

    @staticmethod
    def writeLine(textToWrite:str):
        """
        Simpler Wrapper für einheitliche Textausgaben in die Konsole.

        Args:
            textToWrite (str): Was ausgegeben werden soll
        """
        print(textToWrite)

    @staticmethod
    def getInput(inputText:str = "") -> str:
        """
        Simpler Wrapper für einheitliche Texteingaben aus der Konsole. Kann auch
        als simpler "Enter drücken zum fortfahren" genutzt werden.

        Args:
            inputText (str): Was als Text vor der Eingabe stehen soll (OPTIONAL)
        
        Returns:
            str: Das was in die Konsole eingegeben wurde
        """

        #Wenn Text angegeben wurde, zeige einen Doppelpunkt
        if len(inputText) > 0:
            inputText += ": "

        return input(inputText)

    @staticmethod
    def clearConsole():
        if os.name == "nt":
           os.system('cls') 
        else:
            os.system('clear') 

    ######################################################################################################
    #-- Helpers für Menü-Pages --

    def _printSeparator(bold:bool = False):
        """
        Zeichnet eine simple Trennlinie in die Konsole.

        Args:
            bold (bool): Ob die Trennlinie dick oder dünn sein soll
        """
        if bold:
            ConsoleUI.writeLine("\n==========================================================================")
        else:
            ConsoleUI.writeLine("\n--------------------------------------------------------------------------")

    @staticmethod
    def parseIntInput(input:str):
        """
        Parst einen Eingabe-String in einen int.

        Args:
            input (str): Ein String (z.B. Rückgabe von ConsoleUI.getInput())
        
        Returns:
            int: Den geparsten String, bei ungültigem Wert wird 0 als Fallback zurückgegeben
        """
        try:
            input = int(input)
        except:
            input = 0
        
        return input

    def _showCourseSelection(coursesFromDB:list):
        """
        Zeigt eine Liste mit Kursen an, wobei die 0 für "Abbruch" reserviert ist.

        Args:
            coursesFromDB (int): Eine Liste mit "Course" Objekten aus der Datenbank
        
        Returns:
            int: Kurs-Index in "coursesFromDB"
        """

        #Auswahl anzeigen
        for i in range(len(coursesFromDB)):
            course = coursesFromDB[i]
            ConsoleUI.writeLine(f"{i + 1} = {course.name} / {course.courseId}")
        ConsoleUI.writeLine("")

        #Kurs-Nummer einlesen und ungültige Eingaben abfangen
        selectedCourse = ConsoleUI.parseIntInput(ConsoleUI.getInput("Kursnummer (0 = Abbruch)"))

        return selectedCourse

    ######################################################################################################
    #-- Menü-Pages --

    @staticmethod
    def showMainMenu():
        """
        Zeigt das Hauptmenü an.

        Seitennummer => 0
        """

        #Datenbankverbindung rückmelden
        if DatabaseConnector.isConnected():
            ConsoleUI.writeLine(f"Verbunden mit Datenbank {DatabaseConnector._databaseFile}\n")
        else:
            ConsoleUI.writeLine(f"Verbindung mit Datenbank {DatabaseConnector._databaseFile} getrennt\n")

        ConsoleUI.writeLine(f">> Hallo {Settings._student.name}! Wähle eine Option <<\n")

        #Alle möglichen Untermenüs anzeigen
        ConsoleUI.writeLine("0 = Hauptmenü anzeigen")
        ConsoleUI.writeLine("1 = Dashboard anzeigen")
        ConsoleUI.writeLine("2 = Einstellungen anzeigen")
        ConsoleUI.writeLine("3 = Alle Kurse anzeigen")
        ConsoleUI.writeLine("4 = Kurs erstellen")
        ConsoleUI.writeLine("5 = Kurs löschen")
        ConsoleUI.writeLine("6 = Examen für Kurs eintragen")
        ConsoleUI.writeLine("9 = Beenden")

    @staticmethod
    def showDashboard():
        """
        Zeigt das Dashboard.
        
        Seitennummer => 1
        """
        ConsoleUI.writeLine("<< Dashboard >>\n")

        ConsoleUI._printSeparator()

        ConsoleUI.writeLine("-- Restliche Zeit um Studium in " + str(6) + " Jahren abzuschließen --\n")
        targetDate = Settings._student.enrolled + (timedelta(days=365 * 6))
        targetDelta = (targetDate - Settings._student.enrolled).days
        ConsoleUI.writeLine(f"Tage: {targetDelta}")

        ConsoleUI._printSeparator()

        ConsoleUI.writeLine("-- Aktueller Notendurchschnitt --\n")
        alreadyPassedCourses = [course for course in Settings._student.courses if course.passed() == "Ja"]
        averageScore = 0.0
        for course in alreadyPassedCourses:
            averageScore += course.getGrade()
        ConsoleUI.writeLine(f"Durchschnitt: {round(averageScore / len(alreadyPassedCourses),2)}")

        ConsoleUI._printSeparator()

        ConsoleUI.writeLine("-- Kurs, mit der längsten Bearbeitungszeit bisher --\n")
        notYetPassedCourses = [course for course in Settings._student.courses if course.passed() == "Nein"]
        overdueCourse = None
        for course in notYetPassedCourses:
            if overdueCourse is None:
                overdueCourse = course
            if overdueCourse.startedAt > course.startedAt:
                overdueCourse = course
        if overdueCourse is not None:
            ConsoleUI.writeLine(overdueCourse.shortRepresentation())

        ConsoleUI._printSeparator()

        ConsoleUI.writeLine("-- Kurs, mit den meisten Versuchen von maximal 3 --\n")
        mostTriesCourse = None
        for course in Settings._student.courses:
            if mostTriesCourse is None:
                mostTriesCourse = course
            if course.tries() > mostTriesCourse.tries():
                mostTriesCourse = course
        if mostTriesCourse is not None:
            ConsoleUI.writeLine(mostTriesCourse.shortRepresentation())

        ConsoleUI._printSeparator()

        ConsoleUI.writeLine("-- Wie viele Kurse bereits bestanden wurden --\n")
        passedExams = 0
        for course in Settings._student.courses:
            if course.passed() == "Ja":
                passedExams += 1
        ConsoleUI.writeLine(f"Bestanden: {passedExams} / {len(Settings._student.courses)}")

        ConsoleUI._printSeparator()

        ConsoleUI.writeLine("-- Bisher erreichte ECTS --\n")
        gottenECTS = 0
        for course in Settings._student.courses:
            if course.passed() == "Ja":
                gottenECTS += course.ects
        ConsoleUI.writeLine(f"Erreicht: {gottenECTS} / {Settings._student.ects}")

    @staticmethod
    def showSettings():
        """
        Zeigt die Einstellungen an.

        Seitennummer => 2
        """
        ConsoleUI.writeLine(Settings.__str__())

    @staticmethod
    def showCourses():
        """
        Zeigt alle Kurse des Studenten an.

        Seitennummer => 3
        """
        ConsoleUI.writeLine("Alle Kurse anzeigen.")
        courses = Course.getAllFromDB()
        for course in courses:
            ConsoleUI._printSeparator()
            ConsoleUI.writeLine(course)
    
    def showCreateCourse():
        """
        Zeigt Eingabemaske für die Erstellung eines Kurses.

        Seitennummer => 4
        """
        ConsoleUI.writeLine("Kurs erstellen.")
        ConsoleUI._printSeparator()
        courses = Course.getAllFromDB()
        c = Course(
            ConsoleUI.getInput("Name"),
            ConsoleUI.getInput("Kursnummer"),
            ConsoleUI.getInput("Beschreibung"),
            ConsoleUI.parseIntInput(ConsoleUI.getInput("ECTS")),
            list(), #Leere Kursliste, wird später gesetzt
        )
        if c not in courses:
            c.saveToDB()
            Settings._student.courses = Course.getAllFromDB() #Kurse neu in Student synchronisieren
            ConsoleUI.writeLine(f"\nKurs mit der ID '{c.courseId}' in Datenbank gespeichert!")
        else:
            ConsoleUI.writeLine(f"\nKurs mit der ID '{c.courseId}' bereits in Datenbank vorhanden!")

    def showDeleteCourse():
        """
        Zeigt Menü zum Löschen eines Kurses (sollte man bei einer Eingabe einen Fehler gemacht haben)

        Seitennummer => 5
        """
        ConsoleUI.writeLine("Kurs löschen.")
        ConsoleUI._printSeparator()
        courses = Course.getAllFromDB()
        courseToDelete = ConsoleUI._showCourseSelection(courses)
        
        if courseToDelete < 0 or courseToDelete == 0 or courseToDelete > len(courses):
            #Abbruch
            return
        else:
            #-- Kurs aus DB löschen --
            courseToDelete -= 1 #Index im 1 verschoben, wegen 0-Option
            deleteCourse = courses[courseToDelete]
            DatabaseConnector.execute(
                """
                DELETE FROM courses WHERE courseId = ?;
                """,
                (deleteCourse.courseId,)
            )
            Settings._student.courses = Course.getAllFromDB() #Kurse neu in Student synchronisieren
            ConsoleUI.writeLine(f"\nKurs mit der ID '{deleteCourse.courseId}' gelöscht!")

    def showSetExam():
        """
        Zeigt Eingabemaske für das Eintragen eines gemachten Exams.

        Seitennummer => 6
        """
        ConsoleUI.writeLine("Examen für Kurs eintragen.")
        ConsoleUI._printSeparator()
        courses = Course.getAllFromDB()

        #Kurse herausfiltern: Noch nicht bestanden und weniger als 3 registrierte Versuche
        courses = [course for course in courses if course.tries() < 3 and course.passed() == "Nein"]

        courseToAddTo = ConsoleUI._showCourseSelection(courses)

        if courseToAddTo < 0 or courseToAddTo == 0 or courseToAddTo > len(courses):
            #Abbruch
            return
        else:
            #Examentyp wählen
            ConsoleUI.writeLine("\n\nExamentyp wählen:\n")
            ConsoleUI.writeLine("1 = Advanced Workbook")
            ConsoleUI.writeLine("2 = Klausur")
            ConsoleUI.writeLine("")

            #Examen-Nummer einlesen und ungültige Eingaben abfangen
            examType = ConsoleUI.parseIntInput(ConsoleUI.getInput("Examentyp (0 = Abbruch)"))

            if examType < 0 or examType == 0 or examType > 2:
                return
            else:
                #-- Examentyp eintragen --
                courseToAddTo -= 1 #Index im 1 verschoben, wegen 0-Option
                addToCourse = courses[courseToAddTo]
                match examType:
                    case 1:
                        ConsoleUI.writeLine("\n\nAdvanced Workbook eintragen:\n")
                        aw = AdvancedWorkbook(
                            date.today(),
                            addToCourse.courseId,
                            ConsoleUI.parseIntInput(ConsoleUI.getInput("Punkte bei Aufgabe 1")),
                            ConsoleUI.parseIntInput(ConsoleUI.getInput("Punkte bei Aufgabe 2")),
                            ConsoleUI.parseIntInput(ConsoleUI.getInput("Punkte bei Aufgabe 3")),
                            ConsoleUI.parseIntInput(ConsoleUI.getInput("Punkte bei Aufgabe 4")),
                            ConsoleUI.parseIntInput(ConsoleUI.getInput("Punkte bei Aufgabe 5")),
                            ConsoleUI.parseIntInput(ConsoleUI.getInput("Punkte bei Aufgabe 6")),
                            ConsoleUI.parseIntInput(ConsoleUI.getInput("Punkte in der Ausführung")),
                        )
                        aw.saveToDB()
                        ConsoleUI.writeLine(
                        f"\nAdvanced Workbook für Kurs mit der ID '{addToCourse.courseId}' eingetragen!"
                        )
                    case 2:
                        ConsoleUI.writeLine("\n\nKlausur eintragen:\n")
                        ct = ClassTest(
                            date.today(),
                            addToCourse.courseId,
                            ConsoleUI.parseIntInput(ConsoleUI.getInput("Gesamtpunktzahl")),
                        )
                        ct.saveToDB()
                        ConsoleUI.writeLine(
                            f"\nKlausur für Kurs mit der ID '{addToCourse.courseId}' eingetragen!"
                        )

    ######################################################################################################
    #-- Menü --

    @staticmethod
    def getNextPage():
        """
        Zum setzen der nächsten Menüseite.
        """
        ConsoleUI._printSeparator(True)
        
        #Nächste Seite abfragen (muss int sein)
        nextPage = ConsoleUI.getInput("Seitennummer")
        
        #Fange ungültige Eingaben ab
        nextPage = ConsoleUI.parseIntInput(nextPage)

        #Nächste Seite Setzen
        if nextPage in [0,1,2,3,4,5,6,9]:
            ConsoleUI.__currentPage = nextPage
        else:
            ConsoleUI.__currentPage = ConsoleUI.__currentPage

    @staticmethod
    def drawMenu():
        """
        Zeichnet das Menü.
        """

        ConsoleUI.showLogo()

        match ConsoleUI.__currentPage:
            case 0:
                ConsoleUI.showMainMenu()
            case 1:
                ConsoleUI.showDashboard()
            case 2:
                ConsoleUI.showSettings()
            case 3:
                ConsoleUI.showCourses()
            case 4:
                ConsoleUI.showCreateCourse()
            case 5:
                ConsoleUI.showDeleteCourse()
            case 6:
                ConsoleUI.showSetExam()
            case 9:
                ConsoleUI.writeLine("Beenden ...")
                sys.exit()
        
        #Prüfe, welche Seite als nächstes angezeigt werden soll
        ConsoleUI.getNextPage()

        #Nächster Draw
        ConsoleUI.clearConsole()
        ConsoleUI.drawMenu()