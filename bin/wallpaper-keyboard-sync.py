#!/usr/bin/env python3
import subprocess
import sys
import os
import tempfile
from pathlib import Path
from urllib.parse import unquote, urlparse

from PIL import Image

STATE_FILE = Path.home() / ".cache" / "wallpaper-keyboard-color"


def gsettings_get(schema, key):
    out = subprocess.run(
        ["gsettings", "get", schema, key],
        capture_output=True, text=True, check=True,
    ).stdout.strip()
    return out.strip("'")


def active_wallpaper_path():
    scheme = gsettings_get("org.gnome.desktop.interface", "color-scheme")
    key = "picture-uri-dark" if scheme == "prefer-dark" else "picture-uri"
    uri = gsettings_get("org.gnome.desktop.background", key)
    if not uri:
        uri = gsettings_get("org.gnome.desktop.background", "picture-uri")
    if uri.startswith("file://"):
        return unquote(urlparse(uri).path)
    return uri


def dominant_color(image_path):
    with tempfile.TemporaryDirectory() as td:
        preview = os.path.join(td, "preview.png")
        subprocess.run(
            ["magick", image_path, "-resize", "200x200", preview],
            check=True, capture_output=True,
        )
        img = Image.open(preview).convert("RGB").resize((64, 64))
        quant = img.quantize(colors=8, method=2)
        palette = quant.getpalette()
        counts = sorted(quant.getcolors(), reverse=True)
        _count, idx = counts[0]
        r, g, b = palette[idx * 3: idx * 3 + 3]
        return f"{r:02x}{g:02x}{b:02x}"


def main():
    path = active_wallpaper_path()
    if not os.path.isfile(path):
        print(f"Wallpaper não encontrado: {path}", file=sys.stderr)
        return 1

    color = dominant_color(path)

    cache_key = path
    if STATE_FILE.exists():
        cached = STATE_FILE.read_text().strip().split("|", 1)
        if len(cached) == 2 and cached[0] == cache_key and cached[1] == color:
            return 0

    subprocess.run(["asusctl", "aura", "effect", "static", "-c", color], check=True)

    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    STATE_FILE.write_text(f"{cache_key}|{color}")
    print(f"Teclado atualizado para #{color} (wallpaper: {path})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
