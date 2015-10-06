# ramicon

Shows amount of available RAM in the systray.

With Chrome, IntelliJ and some minor applications open and "only" 8GB RAM, I
was often close to RAM exhaustion, and knowing how much is left has allowed me
to avoid very unpleasant out-of-memory situations. (Quickly triggering the OOM
killer - which in my experience usually kills Chrome, which is good - manually
when the system starts to hang helps, but it's still a major headache.)

The system monitor GNOME extension with shiny graphs that I used previously did
itself leak *lots* of RAM. So I quickly hacked this here together (and upgraded
my laptop to 16GB RAM *sigh*).

It uses the `MemAvailable` metric provided by the Linux kernel in
`/proc/meminfo`, which estimates how much memory is available to new
applications without swapping.

Requires either Python 2 or Python 3.

* Author: `Felix Kaiser <felix.kaiser@fxkr.net>`
* License: revised BSD (see LICENSE)
* Dependencies:
  * Python 2 or Python 3
  * GObject (Fedora: python-gobject or python3-gobject)

