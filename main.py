import json
import os
import subprocess
import sys

import gi
gi.require_version("IBus", "1.0")
from gi.repository import IBus

from ulauncher.api.client.Extension import Extension
from ulauncher.api.client.EventListener import EventListener
from ulauncher.api.shared.event import KeywordQueryEvent, ItemEnterEvent
from ulauncher.api.shared.item.ExtensionResultItem import ExtensionResultItem
from ulauncher.api.shared.action.ExtensionCustomAction import ExtensionCustomAction
from ulauncher.api.shared.action.CopyToClipboardAction import CopyToClipboardAction
from ulauncher.api.shared.action.ActionList import ActionList
from ulauncher.api.shared.action.RenderResultListAction import RenderResultListAction

ICON = "images/icon.svg"
AUTOPASTE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "autopaste.py")
MAX = 9
SKIN = set("\U0001F3FB\U0001F3FC\U0001F3FD\U0001F3FE\U0001F3FF")
RECENT = os.path.join(os.environ.get("XDG_CACHE_HOME", os.path.expanduser("~/.cache")), "ulauncher-emoji-recent.json")
DEFAULTS = ["😂", "❤️", "👍", "🙏", "😭", "🔥", "😊", "🥲", "💀"]


def dict_paths():
    """Full base-language list first, then regional files (e.g. en_IN) that add extras."""
    lang = (os.environ.get("LANG") or "en").split(".")[0]
    names = ["en", lang.split("_")[0], lang]
    seen, paths = set(), []
    for name in names:
        path = f"/usr/share/ibus/dicts/emoji-{name}.dict"
        if name not in seen and os.path.exists(path):
            seen.add(name)
            paths.append(path)
    return paths


def load_emojis():
    merged = {}  # emoji -> [description, words]
    for path in dict_paths():
        for e in IBus.EmojiData.load(path):
            ch = e.get_emoji()
            desc = e.get_description()
            words = {w.lower() for w in e.get_annotations()} | set(desc.lower().split())
            if ch in merged:
                merged[ch][1] |= words
            else:
                merged[ch] = [desc, words]
    # Drop plain-text duplicates (❤ vs ❤️): keep the fully-qualified emoji form.
    best = {}
    for ch in merged:
        key = ch.replace("\ufe0f", "")
        if key not in best or ch.count("\ufe0f") > best[key].count("\ufe0f"):
            best[key] = ch
    keep = set(best.values())
    return [(ch, d, w, any(c in SKIN for c in ch)) for ch, (d, w) in merged.items() if ch in keep]


def load_recent():
    try:
        return json.load(open(RECENT))
    except Exception:
        return []


def save_recent(ch):
    recent = [c for c in load_recent() if c != ch]
    recent.insert(0, ch)
    os.makedirs(os.path.dirname(RECENT), exist_ok=True)
    json.dump(recent[:30], open(RECENT, "w"))


def score(query_words, desc, words):
    total = 0
    d = desc.lower()
    for q in query_words:
        if q in words:
            total += 10
        elif any(w.startswith(q) for w in words):
            total += 6
        elif q in d:
            total += 3
        else:
            return 0  # every typed word must match something
    if d == " ".join(query_words):
        total += 20
    return total - len(d) / 100  # prefer shorter, more specific names


def item(ch, desc, hint="Enter: paste into the focused app (also copied)"):
    return ExtensionResultItem(
        icon=ICON, name=f"{ch}   {desc}", description=hint,
        on_enter=ActionList([CopyToClipboardAction(ch), ExtensionCustomAction(ch)]),
    )


class Query(EventListener):
    def on_event(self, event, ext):
        q = (event.get_argument() or "").lower().split()
        hint = ("Enter: paste into the focused app (also copied)" if ext.preferences.get("paste", "yes") == "yes"
                else "Enter: copy  •  then Ctrl+V to paste")
        show_skin = ext.preferences.get("skin") == "yes" or any(w in ("skin", "tone") for w in q)
        if not q:
            by_char = {ch: desc for ch, desc, _, _ in ext.emojis}
            recent = [c for c in load_recent() if c in by_char]
            picks = (recent + [c for c in DEFAULTS if c not in recent])[:MAX]
            return RenderResultListAction([item(c, by_char.get(c, ""), hint) for c in picks])
        ranked = []
        for ch, desc, words, skin in ext.emojis:
            if skin and not show_skin:
                continue
            s = score(q, desc, words)
            if s > 0:
                ranked.append((s, ch, desc))
        ranked.sort(key=lambda r: -r[0])
        if not ranked:
            return RenderResultListAction([ExtensionResultItem(icon=ICON, name="No emoji found",
                                                               description="Try another word", on_enter=None)])
        return RenderResultListAction([item(ch, desc, hint) for _, ch, desc in ranked[:MAX]])


class Enter(EventListener):
    def on_event(self, event, ext):
        save_recent(event.get_data())
        if ext.preferences.get("paste", "yes") == "yes":
            subprocess.Popen([sys.executable, AUTOPASTE, "0.35"], start_new_session=True)


class EmojiExtension(Extension):
    def __init__(self):
        super().__init__()
        self.emojis = load_emojis()
        self.subscribe(KeywordQueryEvent, Query())
        self.subscribe(ItemEnterEvent, Enter())


if __name__ == "__main__":
    EmojiExtension().run()
