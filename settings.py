
import os.path
import re

class Settings:
    def __init__(self, filename="settings.yml"):
        self.filename = filename
        self.settings = {}
        self.rawContent = ""

    def getFilename(self):
        return self.filename

    def loadSettings(self):
        self.rawContent = ""
        if os.path.isfile(self.filename):
            with open(self.filename, 'r') as file:
                for line in file:
                    self.rawContent += line
                    r = re.search('^(.*):\s(.*)', line)
                    key = r.group(1)
                    value = r.group(2)
                    self.settings[key] = value
                file.close()
        else:
            self.settings = {}
            #self.settings = {"mainWindowTitle":"SIP Analyzer", "mainWindowSize":"500x300", "savedDatabase":"", "savedDatabaseQuery":"", "savedLogPath":"", "packetRegex":"", "packetID":""}
            self.saveSettings(self.settings)


    def saveSettings(self, setting):
        with open(self.filename, 'w') as file:
            for line in setting:
                file.write(line + ": " + setting[line] + "\n")
            file.close()

    def getSettings(self):
        return self.settings

    def getRawContent(self):
        return self.rawContent

    def saveRawTextSettings(self, text):
        with open(self.filename, 'w') as file:
            file.write(text)
            file.close()
        self.loadSettings()
