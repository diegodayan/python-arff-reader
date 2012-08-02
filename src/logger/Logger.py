__author__ = "Diego Dayan"
__version__ = "0.1"

import time
from src.config.Config import *

class Logger(object):
    isEnabled = True
    INF = "INF"
    ERR = "ERR"
    logFile = None

    @classmethod
    def enable(cls):
        cls.isEnabled = True

    @classmethod
    def disable(cls):
        cls.isEnabled = False

    @classmethod
    def log(cls, type, msg):
        global DEBUG_ON_SCREEN
        if not cls.isEnabled:
            return
        try:
            cls.logFile = open(LOG_FILE, "a")
            if DEBUG_ON_SCREEN:
                print msg
            line = cls.now()
            line += "\t"
            line += type
            line += "\t"
            line += msg
            line += "\n"
            cls.logFile.write(line)
            cls.logFile.close()
        except Exception:
            print "Cannot write to the log file. "\
                  " Please make sure you have write permissions or disable the log"\
                  " with Logger.disable()"

    @classmethod
    def info(cls, msg):
        cls.log(cls.INF, msg)

    @classmethod
    def error(cls, msg):
        cls.log(cls.ERR, msg)

    @staticmethod
    def now():
        t = time.localtime(time.time())
        return "%04d-%02d-%02d %02d:%02d:%02d" % (
            t.tm_year,
            t.tm_mon,
            t.tm_mday,
            t.tm_hour,
            t.tm_min,
            t.tm_sec)


