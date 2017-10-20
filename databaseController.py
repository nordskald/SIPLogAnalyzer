
import threading
import os.path
import re
from database import Database

class DatabaseController(threading.Thread):
    def __init__(self, databasemodule):
        threading.Thread.__init__(self)
        self.databasemodule = databasemodule
    
    def run(self):
        print("Running database in new thread!")