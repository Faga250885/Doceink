# Getting started

**English** | [Español](PRIMEROS-PASOS.md)

[Back to the main page](../README.md)

English menu names below describe their functions. Some firmware labels may still appear in Spanish; the relevant names are included where helpful.

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

A new conversation requires internet access. History stored on microSD can be opened offline for reading; sending more messages requires a connection.

Tasks provides local **Personal** and **Work / Trabajo** lists. Dictation uses Wi-Fi; this version does not offer offline speech recognition. Jira is not required.
