
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
    app.addLabel("homeTitle", "The SIP Analyzer", 0)

    app.addLabelEntry("Database path", 1)
    app.setEntry("Database path", settings["savedDatabase"])
    app.addButtons(["Select DB", "New Database"], homePress, 2)
    
    app.addLabelEntry("SIP Log", 3)
    app.setEntry("SIP Log", settings["savedLogPath"])
    app.addButtons(["Select Log"], homePress, 4)
    
    app.addButtons(["Import"], homePress, 5)

def initSettingsWidget():
    app.addLabel("settingsTitle", "Settings", 0)
    
    app.addScrolledTextArea("settingsTextArea", 1)
    app.setTextArea("settingsTextArea", settingsModule.getRawContent())
    
    app.addButtons(["Save"], settingsPress, 2)

def initDatabaseWidget():
    app.addLabel("databaseTitle", "Database", 0, 1)
    app.addLabelEntry("database", 1, 1)
    app.setEntry("database", settings["savedDatabase"])
    app.addLabelEntry("databaseQuery", 2, 1)
    app.setEntry("databaseQuery", settings["savedDatabaseQuery"])
    app.addButtons(["Save", "Execute"], databasePress, 3, 1)
    app.addScrolledTextArea("databaseQueryResult", 4, 1)
    app.addButtons(["Export"], databasePress, 5, 1)


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
        databaseModule.connect(app.getEntry("Database path"))
        #result = databaseModule.selectQuery("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name;")
        #for row in result:
        #    print(row[0])
        with open(app.getEntry("SIP Log"), 'r') as file:
            lineCount = 10000
            c_count = lineCount
            #for line in file:
            #    lineCount += 1
            
            #app.addLabel("Import Percentage", "", 5,1)
            packet = ""
            packet_call_id = ""
            packet_from_header = ""
            packet_to_header = ""
            count = 0
            for line in file:
                if re.search('^[A-Z][a-z][a-z]\s\d\d\s\d\d:\d\d:\d\d\s\d{1,3}[.]\d{1,3}[.]\d{1,3}[.]\d{1,3}\s[0-9]*:\s\*[A-Z][a-z][a-z]\s\d\d\s\d\d:\d\d:\d\d.[0-9]*:\s//', line):
                    databaseModule.insertQuery("INSERT INTO Call(id, packet) VALUES(?, ?)", [count, packet])
                    packet = ""
                    packet_call_id = ""
                elif re.search('^[A-Z][a-z][a-z]\s\d\d\s\d\d:\d\d:\d\d\s\d{1,3}[.]\d{1,3}[.]\d{1,3}[.]\d{1,3}\sCall-ID:\s', line):
                    k = re.search('(^[A-Z][a-z][a-z]\s\d\d\s\d\d:\d\d:\d\d\s\d{1,3}[.]\d{1,3}[.]\d{1,3}[.]\d{1,3}\sCall-ID:\s)(.*)', line)
                    packet_call_id = k.group(2)
                elif re.search('^[A-Z][a-z][a-z]\s\d\d\s\d\d:\d\d:\d\d\s\d{1,3}[.]\d{1,3}[.]\d{1,3}[.]\d{1,3}\sFrom:\s<sip:(.*)@', line):
                    k = re.search('^[A-Z][a-z][a-z]\s\d\d\s\d\d:\d\d:\d\d\s\d{1,3}[.]\d{1,3}[.]\d{1,3}[.]\d{1,3}\sFrom:\s<sip:(.*)@', line)
                    packet_from_header = k.group(1)
                    print("From: " + packet_from_header)
                elif re.search('^[A-Z][a-z][a-z]\s\d\d\s\d\d:\d\d:\d\d\s\d{1,3}[.]\d{1,3}[.]\d{1,3}[.]\d{1,3}\sTo:\s<sip:(.*)@', line):
                    k = re.search('^[A-Z][a-z][a-z]\s\d\d\s\d\d:\d\d:\d\d\s\d{1,3}[.]\d{1,3}[.]\d{1,3}[.]\d{1,3}\sTo:\s<sip:(.*)@', line)
                    packet_to_header = k.group(1)
                    print("To:" + packet_to_header)
                
                packet += line
                count += 1
                if count >= c_count:
                    databaseModule.commit()
                    print("Line: " + str(count))
                    c_count += lineCount
                #app.setEntry(str(count/lineCount) + "%")
        databaseModule.close()
    elif button == "New Database":
        path = app.getEntry("Database path")
        settings['savedDatabase'] = path
        databaseModule.connect(path)
        databaseModule.createQuery(settings['SipTable'])
        databaseModule.close()
        #print(path)
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
            app.setTextArea("databaseQueryResult", "")
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
    elif button == "Export":
        path = app.saveBox()
        with open(path, 'w') as file:
            file.write(app.getTextArea("databaseQueryResult"))
            file.close()

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

