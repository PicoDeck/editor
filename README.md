# Text Editor

A nano-like text editor for [PicoDeck](https://picodeck.net) on the
ClockworkPi PicoCalc. It edits any file on the SD card (it has the
`root-filesystem` requirement), and handles large files, word wrap, line
numbers and several fonts.

## Keys

| Key | Action |
|---|---|
| Ctrl+S | Save |
| Ctrl+O | Open a file |
| Ctrl+N | New file |
| Ctrl+Q | Quit |
| Ctrl+K | Delete the current line |
| Arrows | Move the cursor |
| Ctrl+Left / Ctrl+Right | Jump a word |
| Ctrl+Up / Ctrl+Down | Page up / page down |
| F1 | Help |
| F2 | Word wrap on or off |
| F3 | Line numbers on or off |
| F4 | Next font |
| Esc | Close the help, else quit |

## Install

From the **App Store** on the device (firmware 0.7.0 or later), or copy the
files listed in `files.txt` to `/apps/editor/` on the SD card.

## Development

`make e2e` runs the tests in PicoDeck's simulator. It needs a PicoDeck
checkout with the simulator built (`make simulator` there), at
`~/Projects/PicoDeck/picodeck` or `$PICODECK_ROOT`.

`make zip` builds the release zip from `files.txt`, as CI does. A tag
`v<version>` matching `app.json`'s version publishes it as a release, which
the PicoDeck store lists.

The app was part of the [PicoDeck repository](https://github.com/PicoDeck/picodeck)
until version 1.0.1; its history came with it.
