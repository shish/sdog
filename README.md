sdog
====

A process monitor using an extremely limited (but still useful enough for me)
subset of the systemd watchdog protocol

```
Usage: sdog [options] -- daemon-to-run [daemon options]

Options:
  -h, --help              show this help message and exit
  -t N, --timeout=N       Maximum seconds between pings
  -r N, --respawn=N       Delay between respawns
  -s FILE, --socket=FILE  Path to socket
  -T NAME, --title=NAME   Daemon name (defaults to the first param after "--")
                          (Requires setproctitle module)
  -v, --verbose           Verbose mode
```

For Daemons
===========

There is the sdog.notifier module

```
from sdog.notifier import SDNotifier

def main():
    # Create the notifier
    sd = SDNotifier()

    # Connect to the work queue and signal that we're ready to go
    work_queue = WorkQueue("localhost:1234")
    sd.ready()

    while True:
        # Get some work and signal that we're working on it
        item = work_queue.get()
        sd.status("Processing %s" % item.name)

        # Do the work then signal that we are alive and running successfully
        do_some_work(item)
        sd.watchdog()
```

Protocol
========

The daemon will be launched with `NOTIFY_SOCKET=/some/path.sock` in its
environment; it should then write datagram packets into this socket:

```
READY=1      -- signal that the daemon has loaded, and to start monitoring
WATCHDOG=1   -- must be sent at least once every $timeout seconds
STATUS=blah  -- update the current status message
```
