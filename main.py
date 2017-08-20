
from appJar import gui
import os.path
import re
from settings import Settings
from database import Database


##
##  Settings configuration
##  Creaing, saving and loading of the settings file.
##

settingsChecklist = {"mainWindowTitle":"", "mainWindowSize":"", "savedDatabase":"", "savedDatabaseQuery":"", "savedLogPath":"", "packetRegex":"", "packetID":"", "savedLogPath":""}
settingsModule = Settings()
settingsModule.loadSettings()
settings = settingsModule.getSettings()

# Checking settings if all settingsentries are available.
for line in settings:
    settingsChecklist[line] = "X"
updateSettings = False
for line in settingsChecklist:
    if settingsChecklist[line] == "":
        settings[line] = ""
        updateSettings = True
if updateSettings:
    settingsModule.saveSettings(settings)


databaseModule = Database()

##  GUI configuration
##  GUI settings loaded from settings file.
##


app = gui(settings["mainWindowTitle"], settings["mainWindowSize"])

##
##  Menubar configuration
##

def fileMenuPress(menu):
    if menu == "About":
        app.infoBox("About", "This software is written in by Johan Andersson.\nThis software uses appJar as the GUI platform.\nLicense: GNUGPL")
    elif menu == "Close":
        app.stop()

def windowsMenuPress(menu):
    if menu == "Home":
        app.removeAllWidgets()
        initHomeWidget()
    elif menu == "Settings":
        app.removeAllWidgets()
        initSettingsWidget()
    elif menu == "Database":
        app.removeAllWidgets()
        initDatabaseWidget()


app.createMenu("File")
filesMenu = ["About", "Close"]
app.addMenuList("File", filesMenu, fileMenuPress)

app.createMenu("Windows")
windowsMenu = ["Home", "Settings", "Database"]
app.addMenuList("Windows", windowsMenu, windowsMenuPress)


##
##  Widget configuration
##


def initHomeWidget():
    app.addLabel("homeTitle", "The SIP Analyzer")

    app.addLabelEntry("Database path")
    app.setEntry("Database path", settings["savedDatabase"])
    app.addButtons(["Select DB", "New Database"], homePress)
    
    app.addLabelEntry("SIP Log")
    app.setEntry("SIP Log", settings["savedLogPath"])
    app.addButtons(["Select Log"], homePress)
    
    app.addButtons(["Import"], homePress)

def initSettingsWidget():
    app.addLabel("settingsTitle", "Settings")
    
    app.addScrolledTextArea("settingsTextArea")
    app.setTextArea("settingsTextArea", settingsModule.getRawContent())
    
    app.addButtons(["Save"], settingsPress)

def initDatabaseWidget():
    app.addLabel("databaseTitle", "Database")
    app.addLabelEntry("database")
    app.setEntry("database", settings["savedDatabase"])
    app.addLabelEntry("databaseQuery")
    app.setEntry("databaseQuery", settings["savedDatabaseQuery"])
    app.addButtons(["Save", "Execute"], databasePress)
    app.addScrolledTextArea("databaseQueryResult")
    app.setScrolledTextAreaWidths("databaseQueryResult", "100")
    app.setScrolledTextAreaHeights("databaseQueryResult", "100")


##
##  Widget button press configuration
##

def homePress(button):
    if button == "Select DB":
        path = app.openBox()
        app.setEntry("Database path", path)
    elif button == "Import":
        #First saving current configuration.
        settings["savedDatabase"] = app.getEntry("Database path")
        settings["savedLogPath"] = app.getEntry("SIP Log")
        settingsModule.saveSettings(settings)
        
        if checkDatabaseExistance(settings["savedDatabase"]): 
            databaseModule.connect(settings["savedDatabase"])
            print("Database imported.")
        else:
            print("Database does not exist.")
        print(databaseModule.selectQuery("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name;"))
    elif button == "New Database":
        path = app.getEntry("Database path")
        print(path)
    elif button == "Select Log":
        path = app.openBox()
        app.setEntry("SIP Log", path)

def settingsPress(button):
    if button == "Save":
        settingsModule.saveRawTextSettings(app.getTextArea("settingsTextArea"))
        settings = settingsModule.getSettings()

def databasePress(button):
    if button == "Execute":
        #print("Executing query on very abstract database.")
        databaseModule.connect(app.getEntry("database"))
        if re.search("^CREATE\sTABLE", app.getEntry("databaseQuery")):
            databaseModule.createQuery(app.getEntry("databaseQuery"))
        else:
            databaseModule.selectQuery(app.getEntry("databaseQuery"))
            print(databaseModule.getResult())
            result = databaseModule.getResult()
            textResult = ""
            for row in result:
                textResult += row[0]
                textResult += "\n"
            app.setTextArea("databaseQueryResult",textResult)
        databaseModule.close()
    elif button == "Save":
        #print("Saving the configuration.")
        settings["savedDatabase"] = app.getEntry("database")
        settings["savedDatabaseQuery"] = app.getEntry("databaseQuery")
        settingsModule.saveSettings(settings)

def checkDatabaseExistance(databasePath):
    if os.path.isfile(databasePath):
        return True
    else:
        if app.questionBox("Database Path Error", "This database does not exist. Would you like to create it?"):
            createDatabase(databasePath)
            return True
        return False

def createDatabase(databasePath):
    databaseModule.connect(databasePath)
    databaseModule.close()


initHomeWidget()


app.go()

