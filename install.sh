#!/usr/bin/env bash
# Instala o wallpaper-keyboard-sync para o usuário atual.
set -euo pipefail

cd "$(dirname "${BASH_SOURCE[0]}")"

mkdir -p "$HOME/.local/bin" "$HOME/.config/systemd/user"

cp bin/wallpaper-keyboard-sync.py "$HOME/.local/bin/"
cp bin/wallpaper-keyboard-watch.sh "$HOME/.local/bin/"
chmod +x "$HOME/.local/bin/wallpaper-keyboard-sync.py" "$HOME/.local/bin/wallpaper-keyboard-watch.sh"

cp systemd/wallpaper-keyboard-sync.service "$HOME/.config/systemd/user/"

systemctl --user daemon-reload
systemctl --user enable --now wallpaper-keyboard-sync.service

echo "Instalado! Verifique com: systemctl --user status wallpaper-keyboard-sync"
