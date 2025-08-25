##########################################################################################################
#
# main.py
#
# Einstiegspunkt in das Programm
#
##########################################################################################################

from utils import ConsoleUI, DatabaseConnector
from utils import Settings
from models.Course import Course

##########################################################################################################

#Konsole leeren, falls nicht in eigenem Fenster gestartet
ConsoleUI.clearConsole()

#Datenbankverbindung und ggf. Setup
DatabaseConnector.connectToDB()
setupRan = DatabaseConnector.createDatabase()
if setupRan:
    ConsoleUI.writeLine("<< Datenbanksetup ausgeführt! >>")

#Kurse aus Datenbank laden
Settings._student.courses = Course.getAllFromDB()

#UI-Loop starten
ConsoleUI.drawMenu()

##########################################################################################################