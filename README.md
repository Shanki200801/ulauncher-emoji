# Emoji for Ulauncher

Search emojis by name **or everyday keyword** from [Ulauncher](https://ulauncher.io) and copy them.

`em laugh` → 😂 😆 🤣  ·  `em heart` → ❤️ 💕 🩷  ·  `em pray` → 🙏  ·  `em flag india` → 🇮🇳

## Usage

| Type | Result |
|---|---|
| `em` | Your recently used emojis |
| `em <words>` | Best matches — every word must match a name or keyword |
| Enter | **Pastes the emoji into the app you were typing in** (and copies it) |

- Searches CLDR keywords, not just official names ("laugh" finds 😂 *face with tears of joy*).
- One entry per emoji (text-style duplicates like ❤ vs ❤️ are removed).
- Skin-tone variants are hidden unless you type `skin`/`tone`, or enable them in the extension preferences.

## Auto-paste

After you pick an emoji, Ulauncher closes, focus returns to your app, and the extension presses
Ctrl+V for you (Ctrl+Shift+V in terminals). Nothing happens if no app window has focus.
Works on X11 and needs `python3-xlib` (`sudo apt install python3-xlib`); without it — or on
Wayland — the emoji is simply copied. Turn it off in the extension preferences.

`autopaste.py` also works on its own, e.g. bind a hotkey to a picker that copies, then run it.

## How it works

No downloads and no API keys: it reads the emoji dictionaries that ship with **IBus**
(`/usr/share/ibus/dicts/emoji-*.dict`), the input-method framework present on most Linux desktops.
It loads the full English list plus your regional variant (e.g. `en_IN`, `en_GB`) and, if available,
your own language's keywords.

## Requirements

- Ulauncher 5 (extension API v2)
- IBus with its emoji dictionaries and GObject bindings — on Debian/Ubuntu/Mint:
  `sudo apt install ibus gir1.2-ibus-1.0` (usually already installed)
- Optional, for auto-paste on X11: `python3-xlib`

## License

MIT
