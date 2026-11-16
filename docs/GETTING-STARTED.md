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
| `metalio/e-ink/agenda.json` | Tasks, dates and recurrence |
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

## Shared calendar and tasks

The month is left aligned and the **Tasks** icon appears on the calendar's right at the height of the month text, without a button container, text, border or background. Tapping it opens the Tasks app. Tasks is removed from the eight lower shortcuts and their pickers; an old Tasks tile becomes an available app without duplicating the other shortcuts.

Home application icons measure 50 × 50 pixels without an extra plate behind them. They use Lucide, except ChatGPT, which keeps its original logo scaled proportionally. Forecast variants follow the same icon dimensions.

The upper Home card offers Calendar, Today’s Weather and experimental AI Usage: swipe sideways to switch between enabled widgets. Home remembers your selection after standby and restart. In Calendar, swipe up or down to change months, or tap the heading to choose a month and year. Black page indicators use a larger dot for the active widget and disappear when only one is enabled.

Weather shows the temperature number and a large icon in rounded panels, with a single timeline in two-hour steps below. Tap the gray card to open Weather. The saved update time and refresh icon share one transparent control at the top right; tap either to connect Wi-Fi and update the forecast on the microSD. Both dim while updating. Swiping uses the saved forecast without starting a download. Open Weather to choose a city.

Days with pending dated tasks or birthdays have a black dotted rounded outline without fill, including recurring tasks. Today keeps its black fill. Hold a day: Metalio vibrates and asks whether to add a task. Only accepting opens the same app to start dictation with that date. Cancel or the red back button dismisses the question. Swipe up or down on Calendar to change the month. **Add task** also supports dictation or typing. The initial dictation screen has no text field. Choose Write task to open the editor, or dictate and review the recognized text in its editable field. The field text is vertically centered with left alignment, including while the keyboard is open. To do and Done show the list directly below the tabs, without a counter strip. Dictation can detect the date and recurrence, then offers Create task or Edit details. Manual editing supports no date or a date, and once, daily, weekly, monthly or yearly repetition. For birthdays, use yearly repetition. The With date / No date tab controls the date; the three date fields open a numeric-only keypad that writes directly into the chosen field. Close it with the red button or tap outside, then use Save changes in the form to validate and save the date. Editing changes title, date and repetition; deletion asks for confirmation.

Tasks live in `metalio/e-ink/agenda.json` on microSD. Existing lists are incorporated on the first save and their original files are retained. Completing a repeating task advances to its next date after today. Monthly tasks retain their original day and use the final day of shorter months. Repetitions do not create extra copies. Limit: 256 tasks total. This agenda does not add due-date alarms or notifications.

## Home appearance

In **Settings → Display → Appearance → Home widgets**, enable Calendar, Weather or AI Usage independently. At least one stays enabled; with only one, page dots disappear. Home remembers the enabled widgets and last selection after standby and restart. Battery display is selected with **Icon / Number** tabs. Gray tab rails distinguish these controls inside white cards.

## Experimental AI usage widget

Update normally over Wi-Fi to **0.75.220**. Firmware installation does not require the helper or USB. Account linking is separate:

1. Download [preparar-sesiones.html](https://github.com/Faga250885/Doceink/releases/download/v0.75.220/preparar-sesiones.html) and open it locally in a browser.
2. Choose an existing Codex `auth.json` file (normally `.codex/auth.json`) and/or a Claude Code `.credentials.json` file (normally `.claude/.credentials.json`). These files must already exist from your signed-in applications. This helper does not retrieve credentials from a system vault or browser cookies. Use only an account you are authorized to connect.
3. Export `ai_usage-auth.json` and copy it to **`metalio/e-ink/` on the microSD**. The helper works locally without uploading the selected files. The export contains real access credentials with their original privileges; keep it private and never post it in chat.
4. Enable **AI Usage** in Appearance, switch to its Home card and tap Refresh. Metalio queries the providers directly over Wi-Fi. No intermediary server or always-on computer is used.

Bars show available session/weekly **quota percentages**, not exact tokens. OpenAI readings concern Codex usage backed by ChatGPT, not a guaranteed total for all ChatGPT chats. Claude Team or other accounts can return an access error: these private endpoints are experimental, not a guaranteed public integration. An expired session must be imported again; there is no automatic credential renewal. Refresh runs while the widget is visible, at most every 15 minutes automatically, plus manual refresh.

Tap a provider to refresh or unlink it. Unlinking removes its local access from the microSD and clears its reading; it does not revoke the original application session. API keys and API credit balances are unrelated to this widget.

## Books

Place your books in `books/` and open them from the library. The cover screen lets you continue reading. Reading settings provide page layout, size and typography controls.

## News and weather

Add a valid RSS feed URL; a website's homepage is not necessarily a feed. You can save multiple sources and choose them from the selector.

Set your city in Weather. Press **Refresh / Actualizar** to download data for the first time. Afterwards, both sections show their microSD copies and update when you press refresh. Without an existing download, there is no offline content to display.

## ChatGPT and tasks

Configure your own API key in ChatGPT settings. The package does not include a shared account. Make sure your account has access to the service you plan to use.

A new conversation requires internet access. History stored on microSD can be opened offline for reading; voice messages are disabled in history. Start a new conversation to send voice messages.

Tasks provides **To do** and **Done** tabs, combining tasks from the previous Personal and Work lists without an additional filter. Dictation uses Wi-Fi; this version does not offer offline speech recognition. Jira is not required.

## Offline Recorder

Hold a Home shortcut and select **Recorder**. Insert the microSD and disable USB disk mode, then press **Start recording**. Audio is written as you speak to a temporary WAV file on the card, without Wi-Fi, an API key or cloud processing. You can pause and resume. Recording continues during standby; wake Metalio and return to Recorder to stop it. Confirm Stop, then choose Save to microSD or Discard. Files are under `metalio/e-ink/recordings/`. This app records sound; it does not transcribe speech.

Wi-Fi stays disconnected at startup until you explicitly connect or use a feature that needs it, such as Refresh, dictation or a new conversation. Opening cached News, Weather or history does not request a connection.

## Reader fonts and release notes

Open the reader’s Typography controls to browse 30 families. Entries marked Download need Wi-Fi and a mounted microSD with USB disk mode turned off. A selection saves that family at 18, 22, 24, 25, 28, 30 and 36 px; the download is reused offline. The built-in font remains available without the card. Custom TTF/OTF import is still available.

Open Settings → System → Information → Release notes to read the installed version’s changes and the previous version’s changes without connecting to Wi-Fi.

Swipe up for the reading menu, down for the chapter index, and sideways to turn pages. Hold a word to underline on the original book page. Tap the central font name between the arrows to open the font modal. A download icon means the family is not installed, a check means its catalog sizes are saved, and download progress appears inside its row. The selected face is shown only in the reading sample; list names use the interface font. Adjust Letter spacing below Font size. To add local TTF/OTF fonts, copy them to `metalio/e-ink/fonts_ttf/` and restart Metalio: missing 25px EF files are converted in the background without Wi-Fi. Existing EF fonts in `metalio/e-ink/fonts/` are discovered automatically.

Font downloads display Wi-Fi connection status, live percentage and verification in the tapped row; tap a failed row to retry. The font picker uses a continuous list with separators and a visible scrollbar. Name samples stay compact regardless of reading size.

The font field between the arrows now displays its name in the interface font and a chevron. A usable local font can be selected offline even when other catalog sizes are absent. Only one font download can run at a time; rows temporarily ignore taps and click vibration while it runs. Failures show their storage, network or download error.

Font list names use the system interface font. The selected face is previewed only in the reading sample, including preferences opened from the library without an active book. Arrows cycle through installed fonts; only the central name/chevron field opens the downloadable catalog.

Font downloads verify that the font directory is writable before connecting. Standby keeps peripheral power on while loading its wallpaper or downloading fonts. A transient network failure retries the current file once; persistent failures show an operation and code in the notification. Previously verified files are retained.

A catalog family can contain seven sizes: 18, 22, 24, 25, 28, 30 and 36 px. The check indicates a complete catalog family. An interrupted download can leave usable local sizes: select the name to use them offline, or tap the download icon / Download remaining sizes to finish the family. Closing the catalog refreshes the size arrows. Weather refreshes now explicitly connect Wi-Fi and share the boot-reserved network worker with font downloads, RSS and updates.

## System typeface

Open **Settings → Display → Appearance → System typeface**. There are exactly four families: **Atkinson** (the original built-in default), **Inter**, **Source Sans 3** and **Noto Sans**. These choices are independent of the reader’s 30-font catalog and local imported reading fonts.

Atkinson always works without a card or Wi-Fi. Selecting another family downloads its dedicated native-size UI pack once to the microSD. The selector shows Wi-Fi/download status and percentage; leave USB Disk off during the first download. Packs are checked against size and SHA-256, then remain usable offline. They contain true regular and semibold faces for the 16 UI roles, rendered directly at native pixel sizes rather than resizing reading-font bitmaps.

The selected pack is loaded into PSRAM and its SD file is closed, keeping the interface usable after card removal or while USB Disk is active. Existing control sizes and Lucide icons are preserved. Missing glyphs use the original Latin/CJK fallback; reading typography remains separate. Updating from 0.75.190 starts on Atkinson. New choices persist after restart; if a saved pack is absent at boot, Atkinson remains available without automatically starting a download.

See [font sources, licenses and preparation](../assets/system-fonts/v1/README.md).

## Settings organized by task

| Group | Order and location |
|---|---|
| Display | Wallpapers first (gallery, slideshow, dynamic backgrounds), Home shortcut grid, then Appearance (widgets, battery, system typeface, screen refresh). |
| Connections | Wi-Fi setup first, then Bluetooth mode and device actions; help follows its control. |
| Files | Wi-Fi transfer, USB Disk, then microSD state and capacity. |
| System | Energy (standby, shutdown, Wi-Fi idle delay), General (language and vibration), Clock (automatic then manual), Information (version, updates and notes, device details, then credits). |

Existing settings are preserved. Each section scrolls independently and switching sections closes its old selectors and stops its page-local timers.

## Reading settings, profiles and underlines

Each book keeps its own page and typography preferences on microSD. Books without saved settings inherit the defaults. In the reader menu, **Pages** includes independent paragraph spacing, three reading profiles, and actions to use the current preferences as defaults or restore defaults for the current book. Save a profile before applying it to another book. Its selected font must already be installed.

**Typography** adds Regular, Medium and Bold text weight, independent from bionic initials and letter spacing. The chapter index highlights the current chapter in black and opens at that chapter.

To save a highlight, **hold the first word on the book page**, then tap the final word. Selection uses a black background with white text on the same page, with unchanged text positions and reader footer. Saving leaves only the underline. Swipe sideways to keep selecting across pages, including chapter boundaries. Choosing the final word reveals **Save underline** and **Cancel**; tapping the initial word again cancels selection. Reverse selection is supported. **Advanced → Underlines** opens a scrollable list without a title or Close button; close it with the red back button. Tapping anywhere in a row, including a truncated preview, opens the full passage in a detail dialog with **Delete** and **Close**. The menu's start-underlining button has been removed. **Advanced → Instructions** opens the illustrated gesture guide. Anchors survive reflow and font changes; image pages do not support text selection. Settings and highlights live alongside the book, so keep companion files when moving or renaming it. Selection uses a bounded temporary cache of visited pages; an oversized selection shows an error instead of silently truncating saved text.

The Home editor uses 48 px icons, with a diagonal hatch on the fixed Settings card. That card stays at the bottom right and cannot be reassigned.

ChatGPT: a new conversation blocks the microphone during “Connecting to ChatGPT”. Once ready, its first message says to hold the microphone to ask and shows a right arrow. A press started before readiness does not automatically begin recording when connection finishes.

In Information, the DoceInk logo is inside the card above the version and 20% smaller. Battery appearance offers Icon or Number (with %). The removed Icon with percentage mode automatically falls back to Icon.

Touch navigation now uses gestures only. Tap zones and their settings are removed, including for previously saved preferences. Holding a word and tapping the final word still selects a highlight.

Pending reminders appear next to the clock: tap to open the task. Completing a one-time task moves it to Done. Marking a recurring reminder as seen hides only that occurrence; it returns on the next date. Closing keeps the reminder pending.

In Advanced, Footer checkboxes control each item independently. Screen groups orientation and cleaning frequency. Underlines show their chapter and saved date/time; older items without a timestamp display a dash. Deletion always requires confirmation, and Cancel keeps the quote.
