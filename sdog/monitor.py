#!/usr/bin/env python

import socket
import os
import subprocess
from optparse import OptionParser
from time import time, sleep
from select import select
import sys

try:
    from setproctitle import setproctitle
except ImportError:
    def setproctitle(title):
        pass


def main(argv=sys.argv):
    parser = OptionParser(usage="%prog [sdog options] -- daemon-to-run [daemon options]")
    parser.add_option("-t", "--timeout", dest="timeout", type=int, default=10,
                      help="Maximum seconds between pings", metavar="N")
    parser.add_option("-r", "--respawn", dest="respawn", type=int, default=1,
                      help="Delay between respawns", metavar="N")
    parser.add_option("-T", "--title", dest="title",
                      help="Set process title", metavar="NAME")
    parser.add_option("-s", "--socket", dest="soc_loc",
                      # FIXME: probably (almost certainly) insecure,
                      # need tmpfile.NamedTemporaryFile() for sockets
                      default="/tmp/sdog-%d.sock" % os.getpid(),
                      help="Path to socket", metavar="FILE")
    parser.add_option("-v", "--verbose", dest="verbose",
                      default=False, action="store_true",
                      help="Verbose mode")
    (options, args) = parser.parse_args()

    if args:
        launch(options, args)
    else:
        parser.error("Need to specify a program to launch")


def launch(options, args):
    c = Child(options, args)
    try:
        c.watch()
    finally:
        if os.path.exists(options.soc_loc):
            os.unlink(options.soc_loc)


class Child(object):
    def __init__(self, opts, args):
        self.opts = opts
        self.args = args
        self.proc = None
        self.ready = False
        self.sock = None
        self.last_ok = 0

    def watch(self):
        self.sock = socket.socket(socket.AF_UNIX, socket.SOCK_DGRAM)
        self.sock.bind(self.opts.soc_loc)

        while True:
            try:
                self.poll()
            except Exception as e:
                print "SDog Error:", e
                self.proc = None
                sleep(5)

    def status(self, status):
        if self.opts.verbose:
            print status
        setproctitle("sdog: %s: %s" % (self.opts.title or self.args[0], status))

    def poll(self):
        if not self.proc:
            self.status("spawning: %s" % self.args)
            env = os.environ.copy()
            env["NOTIFY_SOCKET"] = self.opts.soc_loc
            self.proc = subprocess.Popen(self.args, env=env)
            self.status("launched subprocess with PID: %d" % self.proc.pid)
            self.last_ok = time()
            self.ready = False
            return

        status = self.proc.poll()
        if status is not None:
            self.status("Process exited with status code %d, respawning after %d seconds" % (status, self.opts.respawn))
            self.proc = None
            sleep(self.opts.respawn)
            return

        rs, ws, xs = select([self.sock], [], [], 1.0)

        if rs:
            packet, addr = self.sock.recvfrom(1024)
            for line in packet.split("\n"):
                k, _, v = line.partition("=")
                #print "Got message: ", k, v
                if k == "WATCHDOG" and v == "1":
                    self.last_ok = time()
                if k == "READY" and v == "1" and not self.ready:
                    self.status("Daemon is ready")
                    self.ready = True
                if k == "STATUS":
                    self.status(v)
                if k == "ERRNO":
                    self.errno = v
                if k == "BUSERROR":
                    self.buserror = v
                if k == "MAINPID":
                    self.mainpid = v

        if time() > self.last_ok + self.opts.timeout:
            self.status("No OK message for %d seconds, killing child" % (time() - self.last_ok))
            self.proc.kill()
            self.proc = None


if __name__ == "__main__":
    sys.exit(main(sys.argv))
