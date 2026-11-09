#!/usr/bin/env bash
# Observa trocas de wallpaper (e de tema claro/escuro) e sincroniza
# a cor do teclado RGB com a cor dominante do wallpaper ativo.
set -uo pipefail

SYNC="$HOME/.local/bin/wallpaper-keyboard-sync.py"

"$SYNC" || true

dconf watch /org/gnome/desktop/ | while IFS= read -r line; do
    case "$line" in
        */background/picture-uri | */background/picture-uri-dark | */interface/color-scheme)
            "$SYNC" || true
            ;;
    esac
done
