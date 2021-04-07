# Steam shortcut generator
Generates a `.desktop` file complete with icon and places it in `~/.local/share/applications/steam` for each installed Steam game.

Will only work if:
- your window manager looks in `~/.local/share/applications` for shortcuts
- your window manager looks in `~/.local/share/icons/hicolor` for icons
- the Steam root folder is `~/.steam`

The  are currently highly platform specific so high chance of not working if you aren't on Ubuntu 20.04.
