#!/usr/bin/env python3

import re

from gi.repository import Gtk
from gi.repository import GLib


INTERVAL_SEC = 2.5


class RamStatusIcon(object):

    def __init__(self):

        self.icon = Gtk.StatusIcon()
        self.icon.connect("popup-menu", self.on_icon_popup_menu)
        self.label = Gtk.Label("...")

        self.window = Gtk.OffscreenWindow()
        self.window.add(self.label)
        self.window.connect("damage-event", self.on_window_damage)
        self.window.show_all()

        self.previous_value = None
        self.on_timer()
        GLib.timeout_add_seconds(1, self.on_timer)

    def on_window_damage(self, window, event):
        self.icon.set_from_pixbuf(window.get_pixbuf())

    def on_icon_popup_menu(self, icon, button, time):
        menu = Gtk.Menu()
        close_item = Gtk.MenuItem("Close App")
        menu.append(close_item)
        close_item.connect_object("activate", self.on_close_activate, "Close App")
        close_item.show()
        menu.popup(None, None, None, None, button, time)
        self._menu = menu  # prevent garbage collection

    def on_close_activate(self, data=None):
        Gtk.main_quit()

    def set_text(self, text):
        self.label.set_text(text)
        self.icon.set_from_pixbuf(self.window.get_pixbuf())

    def on_timer(self):
        kB = get_mem_available()
        if kB != self.previous_value:
            GB = kB / 1000000.0
            self.set_text("%1.1fG" % GB)
            self.previous_value = kB
        return True


# https://git.kernel.org/cgit/linux/kernel/git/torvalds/linux.git/commit/?id=34e431b0ae398fc54ea69ff85ec700722c9da773
EXPR = re.compile('^MemAvailable: +(\d+) +kB$')
def get_mem_available():
    with open("/proc/meminfo") as f:
        for line in f:
            m = EXPR.match(line)
            if m:
                s = m.groups()[0]
                return int(s)
    assert False


if __name__ == '__main__':

    # make ctrl-c work, https://bugzilla.gnome.org/show_bug.cgi?id=622084
    import signal
    signal.signal(signal.SIGINT, signal.SIG_DFL)

    RamStatusIcon()
    Gtk.main()

