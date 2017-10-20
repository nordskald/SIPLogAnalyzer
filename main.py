
import threading
import time
import random
import logging
from database import Database


logging.basicConfig(level=logging.DEBUG,
                    format='(%(threadName)-10s) %(message)s',
                    )


def reader(db):
    logging.debug("Trying to read...")
    db.lock()
    try:
        logging.debug("Reading material...")
        time.sleep(2)
        logging.debug("Finished reading.")
    finally:
        db.unlock()
        logging.debug("Unlocked.")

def writer(db):
    logging.debug("Trying to write...")
    db.lock()
    try:
        logging.debug("Writing stuff")
        time.sleep(1)
        logging.debug("Finished writing.")
    finally:
        db.unlock()
        logging.debug("Unlocked.")


#

database = Database()

for i in range(4):
    t = threading.Thread(target=reader, args=(database,))
    t.start()
for i in range(2):
    t = threading.Thread(target=writer, args=(database,))
    t.start()

logging.debug("Wating for minions...")
main_thread = threading.currentThread()
for t in threading.enumerate():
    if t is not main_thread:
        t.join()
logging.debug("Done")
