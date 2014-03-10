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
  -v, --verbose           Verbose mode
```
