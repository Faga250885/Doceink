# Getting started

**English** | [Español](PRIMEROS-PASOS.md)

[Back to the main page](../README.md)

English is the fresh-install default. Spanish and Simplified Chinese are available in Settings. OTA retains your choice.

## Basic controls

- **Red button, single tap:** go back one screen; from a conversation opened through history, return to history.
- **Red button, long press:** return to Home.
- **Hold a Home icon:** open the application selector to replace that shortcut. Tap outside or use the red button to close it.
- **Swipe:** scroll lists or change content on screens that support it. Vibration confirms the completed gesture.

E-paper has visible refresh cycles. A flash during a full refresh does not, by itself, mean Metalio has restarted.

## Connect Wi-Fi

Open **Settings → Connections → Wi-Fi** (**Ajustes → Conexiones → Wi-Fi**), find your network and connect. The ESP32-S3 uses **2.4 GHz Wi-Fi**. Internet access is needed to download news and weather, start conversations and use dictation.

## microSD and files

The microSD card stores books, wallpapers, fonts, tasks, history and downloaded content. A clean firmware installation does not erase the card. Use an empty compatible card to start without previous content.

Data is organized under `metalio/e-ink/` on the card:

| microSD path | Contents |
| --- | --- |
| `metalio/e-ink/books/` | Books |
| `metalio/e-ink/wallpaper/` | Wallpapers |
| `metalio/e-ink/fonts/` | Reading fonts in `.ef` format |
| `metalio/e-ink/fonts_ttf/` | TTF/OTF files for the import process; these are not equivalent to converted `.ef` fonts |
| `metalio/e-ink/recordings/` | Local WAV recordings |
| `metalio/e-ink/chat_log/` | Conversation history |
| `metalio/e-ink/personal_tasks.json` | Personal tasks |
| `metalio/e-ink/work_tasks.json` | Work tasks |
| `metalio/e-ink/weather.json` | Downloaded forecast |
| `metalio/e-ink/rss_*.xml` | RSS source caches |

You do not need to edit those data files manually to use the applications.

### Transfer from your phone over Wi-Fi

1. Connect your phone and Metalio to the same Wi-Fi network.
2. Insert the microSD card and disable USB disk mode if active.
3. Under **Settings → Files** (**Ajustes → Archivos**), choose **Transfer files over Wi-Fi** (**Transferir archivos por Wi-Fi**).
4. Scan the QR code and open its link in your browser.
5. Browse folders, upload files or download existing files. On a computer, you can also drag files into the upload area.
6. Close the transfer screen on Metalio when finished. The link is temporary.

The QR code opens that Metalio's microSD file manager. It is not cloud storage or the firmware installer.

### Copy over USB

Enable **USB disk / Disco USB** in Settings → Files. Copy files from your computer and eject the drive before disabling that mode. While USB disk mode is active, Metalio does not access the microSD in the same way as during normal use.

## Books

Place your books in `books/` and open them from the library. The cover screen lets you continue reading. Reading settings provide page layout, size and typography controls.

## News and weather

Add a valid RSS feed URL; a website's homepage is not necessarily a feed. You can save multiple sources and choose them from the selector.

Set your city in Weather. Press **Refresh / Actualizar** to download data for the first time. Afterwards, both sections show their microSD copies and update when you press refresh. Without an existing download, there is no offline content to display.

## ChatGPT and tasks

Configure your own API key in ChatGPT settings. The package does not include a shared account. Make sure your account has access to the service you plan to use.

A new conversation requires internet access. History stored on microSD can be opened offline for reading; voice messages are disabled in history. Start a new conversation to send voice messages.

Tasks provides local **Personal** and **Work / Trabajo** lists. Dictation uses Wi-Fi; this version does not offer offline speech recognition. Jira is not required.

## Offline Recorder

Hold a Home shortcut and select **Recorder**. Insert the microSD and disable USB disk mode, then press **Start recording**. Audio is written as you speak to a temporary WAV file on the card, without Wi-Fi, an API key or cloud processing. You can pause and resume. Recording continues during standby; wake Metalio and return to Recorder to stop it. Confirm Stop, then choose Save to microSD or Discard. Files are under `metalio/e-ink/recordings/`. This app records sound; it does not transcribe speech.

Wi-Fi stays disconnected at startup until you explicitly connect or use a feature that needs it, such as Refresh, dictation or a new conversation. Opening cached News, Weather or history does not request a connection.

## Reader fonts and release notes

Open the reader’s Typography controls to browse 30 families. Entries marked Download need Wi-Fi and a mounted microSD with USB disk mode turned off. A selection saves that family at 18, 22, 24, 25, 28, 30 and 36 px; the download is reused offline. The built-in font remains available without the card. Custom TTF/OTF import is still available.

Open Settings → System → Information → Release notes to read the installed version’s changes and the previous version’s changes without connecting to Wi-Fi.

Hold the reading screen for its menu; swipe up or down for the chapter index. Tap the central font name between the arrows to open the font modal. A download icon means the family is not installed, a check means its catalog sizes are saved, and download progress appears inside its row. The selected face is shown only in the reading sample; list names use the interface font. Adjust Letter spacing below Font size. To add local TTF/OTF fonts, copy them to `metalio/e-ink/fonts_ttf/` and restart Metalio: missing 25px EF files are converted in the background without Wi-Fi. Existing EF fonts in `metalio/e-ink/fonts/` are discovered automatically.

Font downloads display Wi-Fi connection status, live percentage and verification in the tapped row; tap a failed row to retry. The font picker uses a continuous list with separators and a visible scrollbar. Name samples stay compact regardless of reading size.

The font field between the arrows now displays its name in the interface font and a chevron. A usable local font can be selected offline even when other catalog sizes are absent. Only one font download can run at a time; rows temporarily ignore taps and click vibration while it runs. Failures show their storage, network or download error.

Font list names use the system interface font. The selected face is previewed only in the reading sample, including preferences opened from the library without an active book. Arrows cycle through installed fonts; only the central name/chevron field opens the downloadable catalog.

Font downloads verify that the font directory is writable before connecting. Standby keeps peripheral power on while loading its wallpaper or downloading fonts. A transient network failure retries the current file once; persistent failures show an operation and code in the notification. Previously verified files are retained.

A catalog family can contain seven sizes: 18, 22, 24, 25, 28, 30 and 36 px. The check indicates a complete catalog family. An interrupted download can leave usable local sizes: select the name to use them offline, or tap the download icon / Download remaining sizes to finish the family. Closing the catalog refreshes the size arrows. Weather refreshes now explicitly connect Wi-Fi and share the boot-reserved network worker with font downloads, RSS and updates.
