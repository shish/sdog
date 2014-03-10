
import ctypes
import ctypes.util


class SDNotifier(object):
    def __init__(self):
        self.sd = ctypes.CDLL(ctypes.util.find_library("systemd-daemon"))

    def ready(self):
        self.__notify("READY=1")

    def status(self, stat):
        self.__notify("STATUS=%s" % stat)

    def errno(self, errno):
        self.__notify("ERRNO=%d" % errno)

    def buserror(self, err):
        self.__notify("BUSERROR=%s" % err)

    def mainpid(self, pid):
        self.__notify("MAINPID=%d" % pid)

    def watchdog(self):
        self.__notify("WATCHDOG=1")

    def __notify(self, msg):
        #print msg
        self.sd.sd_notify(0, msg)
