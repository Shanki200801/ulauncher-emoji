#!/usr/bin/env python3
"""Paste the clipboard into the window that has focus, by faking Ctrl+V (X11).

Terminals get Ctrl+Shift+V. Does nothing if no app window is focused (e.g. the
desktop), or when not running under X11.

  autopaste.py [delay_seconds]
"""
import os
import sys
import time

TERMINALS = {
    "gnome-terminal-server", "gnome-terminal", "xterm", "uxterm", "kitty", "alacritty",
    "com.mitchellh.ghostty", "ghostty", "tilix", "konsole", "terminator", "wezterm",
    "org.wezfurlong.wezterm", "xfce4-terminal", "mate-terminal", "lxterminal", "foot",
    "st", "st-256color", "urxvt", "rxvt", "sakura", "guake", "tilda", "yakuake",
}
SKIP = {"nemo-desktop", "desktop_window", "cinnamon", "ulauncher", "xfdesktop"}


def main():
    delay = float(sys.argv[1]) if len(sys.argv) > 1 else 0.3
    if os.environ.get("XDG_SESSION_TYPE", "x11") == "wayland" or not os.environ.get("DISPLAY"):
        return
    try:
        from Xlib import X, XK, display
        from Xlib.ext import xtest
    except ImportError:
        return  # python3-xlib not installed: copy-only

    time.sleep(delay)  # let the launcher/picker close and focus return
    d = display.Display()
    root = d.screen().root
    active = root.get_full_property(d.intern_atom("_NET_ACTIVE_WINDOW"), X.AnyPropertyType)
    if not active or not active.value or not active.value[0]:
        return
    try:
        cls = d.create_resource_object("window", active.value[0]).get_wm_class() or ()
    except Exception:
        cls = ()
    names = {c.lower() for c in cls}
    if not names or names & SKIP:
        return

    keys = ["Control_L", "Shift_L", "v"] if names & TERMINALS else ["Control_L", "v"]
    codes = [d.keysym_to_keycode(XK.string_to_keysym(k)) for k in keys]
    for c in codes:
        xtest.fake_input(d, X.KeyPress, c)
    for c in reversed(codes):
        xtest.fake_input(d, X.KeyRelease, c)
    d.sync()


if __name__ == "__main__":
    main()
