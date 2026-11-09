# wallpaper-keyboard-sync

Sincroniza a cor do teclado RGB de notebooks ASUS/ROG (via `asusctl`) com a
cor dominante do wallpaper ativo no GNOME — incluindo a troca automática
entre as variantes claro/escuro.

## Como funciona

- `bin/wallpaper-keyboard-sync.py`: detecta o wallpaper em uso (respeitando
  `org.gnome.desktop.interface color-scheme`), extrai a cor dominante da
  imagem (SVG, JXL, PNG, JPG — qualquer formato que o ImageMagick leia) e
  aplica no teclado com `asusctl aura effect static -c <cor>`.
- `bin/wallpaper-keyboard-watch.sh`: observa o dconf (`dconf watch
  /org/gnome/desktop/`) e dispara o script de sync sempre que o wallpaper
  ou o tema claro/escuro mudam.
- `systemd/wallpaper-keyboard-sync.service`: serviço de usuário que mantém
  o watcher rodando em segundo plano, iniciando junto com a sessão gráfica.

## Requisitos

- GNOME (usa `gsettings`/`dconf`)
- [`asusctl`](https://gitlab.com/asus-linux/asusctl) com `asusd` rodando
- ImageMagick (`magick`/`convert`)
- Python 3 com Pillow (`pip install pillow` ou pacote da distro)

## Instalação

```bash
./install.sh
```

Isso copia os scripts para `~/.local/bin`, instala o serviço em
`~/.config/systemd/user` e já habilita/inicia (`systemctl --user enable --now`).

## Uso manual

```bash
# roda a sincronização uma vez, sem o watcher
~/.local/bin/wallpaper-keyboard-sync.py

# gerenciar o serviço
systemctl --user status wallpaper-keyboard-sync
systemctl --user stop wallpaper-keyboard-sync
systemctl --user disable wallpaper-keyboard-sync
journalctl --user -u wallpaper-keyboard-sync -f
```
