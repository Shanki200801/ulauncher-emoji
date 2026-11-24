# Emoji for Ulauncher

Search emojis by name **or everyday keyword** from [Ulauncher](https://ulauncher.io) and copy them.

`em laugh` → 😂 😆 🤣  ·  `em heart` → ❤️ 💕 🩷  ·  `em pray` → 🙏  ·  `em flag india` → 🇮🇳

## Usage

| Type | Result |
|---|---|
| `em` | Your recently used emojis |
| `em <words>` | Best matches — every word must match a name or keyword |
| Enter | Copies the emoji — paste with Ctrl+V |

- Searches CLDR keywords, not just official names ("laugh" finds 😂 *face with tears of joy*).
- One entry per emoji (text-style duplicates like ❤ vs ❤️ are removed).
- Skin-tone variants are hidden unless you type `skin`/`tone`, or enable them in the extension preferences.

## How it works

No downloads and no API keys: it reads the emoji dictionaries that ship with **IBus**
(`/usr/share/ibus/dicts/emoji-*.dict`), the input-method framework present on most Linux desktops.
It loads the full English list plus your regional variant (e.g. `en_IN`, `en_GB`) and, if available,
your own language's keywords.

## Requirements

- Ulauncher 5 (extension API v2)
- IBus with its emoji dictionaries and GObject bindings — on Debian/Ubuntu/Mint:
  `sudo apt install ibus gir1.2-ibus-1.0` (usually already installed)

## License

MIT
