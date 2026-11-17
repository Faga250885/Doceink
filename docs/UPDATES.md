# Update without erasing your data

**English** | [Español](ACTUALIZACIONES.md)

[Back to the main page](../README.md)

If Doceink is already installed, you do not need to repeat a clean installation.

1. Connect Metalio to Wi-Fi.
2. Open **Settings → System → Information → Check for updates**. Spanish labels: **Ajustes → Sistema → Información → Comprobar actualización**.
3. Review the offered version and confirm the update.
4. Wait for installation and restart to finish, then check the version in Information.

Normal updates preserve accounts, settings and microSD files. A clean USB installation replaces internal flash instead.

## Downloads

- [Latest release](https://github.com/Faga250885/Doceink/releases/latest).
- [Documented version: 0.75.234](https://github.com/Faga250885/Doceink/releases/tag/v0.75.234).
- [OTA firmware: 0.75.234](https://github.com/Faga250885/Doceink/releases/download/v0.75.234/Doceink-EInk4.bin).

`Doceink-EInk4.bin` contains only the update application. It does not include the bootloader, partition table or complete resource package needed for a fresh installation. For that, use the [clean installation guide](INSTALLATION.md).

Do not use `Metalio-instalacion-limpia.bin` in the Wi-Fi updater. These files are not interchangeable just because both end in `.bin`.

## What's new in 0.75.234

- Prepare Wi-Fi file transfer on the reserved internal-stack network worker instead of a task with an external stack.
- Dispatch connection-ready updates through the synchronized screen queue.
- The voice/recording failure remains under investigation.

## What's new in 0.75.233

- Add visible connection/upload and recording diagnostic codes.
- Distinguish queue saturation, capture and microSD write/sync failures; the underlying failure remains under investigation.

## What's new in 0.75.232

- Serialize voice TLS reads and writes on their shared context.
- Retry temporary read/write conditions without blocking the shared context.

## What's new in 0.75.231

- Detects incomplete audio transmissions.

- Recover the voice session after an upload failure or response timeout.
- Recover the recording indicator if the button release event is missed.

## What's new in 0.75.230

Audio releases its internal-memory buffers when stopped and reserves them again for the microphone, recorder and alarms. When ChatGPT closes its connection, audio resources stop when safe. The network improvement requires device verification.

## What's new in 0.75.229

Old conversation callbacks no longer change a new session; each session releases only its own network lease. ChatGPT starts audio after connecting to OpenAI and displays available failure details. Device verification is still needed.

## What's new in 0.75.228

Fixes a 0.75.227 issue that could stop Wi-Fi before file transfer starts and restores the previous connection procedure as a precaution.

Weather download failures display diagnostics. The pre-existing download issue remains under investigation.

## What's new in 0.75.227

File transfer requests Wi-Fi automatically and offers doceink.local with a temporary code. Startup tries the preferred saved network first, then searches for alternatives. The weather widget centers the temperature and resolves its layout when returning Home.

## What's new in 0.75.226

The wallpaper gallery opens in a simple list and can be switched to thumbnail view. Preview and selection remain available.

The weather widget adjusts the space to show the complete temperature, including digits of different widths. The experimental AI usage widget is temporarily removed from Home and settings.

Previously saved microSD credentials are retained; removing the widget does not revoke sessions or delete those files.

## What's new in 0.75.225

Fixed the pairing command copy button. If the browser blocks clipboard access, the command remains visible for manual copying.

## What's new in 0.75.224

AI Usage linking displays a diagnostic code when it cannot start.

## What's new in 0.75.223

AI Usage linking tries an alternate address when the main port is unavailable, and uses a separate control port. When necessary the displayed alternative includes `:8765`.

## What's new in 0.75.222

AI Usage linking is simpler: open **http://doceink.local** on the PC where you use Codex or Claude Code, enter Metalio's code and choose **Copy command**. Paste it into PowerShell to send the access directly over Wi-Fi, without finding the JSON or using Setup. QR, numeric IP and manual file import remain available.

The local name is active only while linking. The link remains temporary and single-use. This does not change experimental quota access or add provider sign-in. See the [guide](GETTING-STARTED.md#experimental-ai-usage-widget).

Language switching uses a more compact generated table, preserving all 1,653 strings in each language.

The Wi-Fi setup page is stored compressed and decoded by the browser. Firmware and the built-in font pack remain in internal flash, with no partition migration.

## What's new in 0.75.221

AI Usage account linking now uses a QR code: tap an account, choose **Link**, scan on a phone connected to the same Wi-Fi, and select its existing session file. The page saves automatically to Metalio microSD, closes the linking dialog and refreshes the widget. No manual card copy or intermediary server is needed.

The temporary link works once, expires after 15 minutes and closes when you leave the dialog. Only the chosen account is replaced; the other is preserved. The upload contains only the access token and optional Codex account ID, with no refresh token, password or ID token. Use a trusted Wi-Fi network. See the [setup guide](GETTING-STARTED.md#experimental-ai-usage-widget).

This changes local file import, not provider sign-in or quota availability. The experimental account-access limits from 0.75.220 still apply.

## What's new in 0.75.220

Available through the normal Wi-Fi updater, including from the 0.75.219 beta. In **Settings → Display → Appearance**, choose Calendar, Weather and the experimental AI Usage widget independently. At least one must stay enabled. Swipes skip disabled widgets, a single widget has no page dots, and the choice survives standby and restart.

Battery display now uses **Icon / Number** tabs. Tab controls inside white cards use a gray patterned rail with a black selected option, including on the monochrome display.

The optional AI widget reads current session and weekly quota percentages directly over Wi-Fi for **ChatGPT-backed Codex** and **Claude**, without a server or an always-on PC. It does not report exact token counts or guarantee usage across ordinary ChatGPT conversations. Linking requires importing existing session access credentials once using the [local helper](https://github.com/Faga250885/Doceink/releases/download/v0.75.220/preparar-sesiones.html); see the [setup instructions](GETTING-STARTED.md#experimental-ai-usage-widget). Private provider endpoints may reject the account, including Claude Team, or change; expired sessions require reimporting. Unlinked accounts show no fabricated readings.

## What's new in 0.75.218

Home widget indicators are now black: 6 px for the active widget and 4 px for the inactive one.

Pending reminders appear next to the clock. One-time reminders stay until completed and move to Done; recurring reminders can be marked as seen for the current occurrence without finishing the series. Closing a reminder does not dismiss it. Tasks remain stored on the microSD.

The highlights list shows the chapter and saved date and time below each quote. Older quotes without a timestamp keep their data and display a dash. Dialogs have rounded corners, and deletion requires confirmation.

The Advanced reader menu places Underlines and Contents together, replaces large footer buttons with compact checkboxes, and groups orientation and ink cleaning under Screen. Existing button styling and all options are preserved.

Validation: 111 local tests passed, including native rendering, reminders and save failures, highlight metadata and deletion confirmation, and menu layout. Physical testing on Metalio remains pending installation.

## What's new in 0.75.217

Home remembers the selected Calendar or Weather widget after standby, shutdown and restart. The page indicators are both gray, with a 6 px active dot and a smaller 4 px inactive dot.

The weather card uses the freed vertical space, with 16 px padding and rounded gray and white panels. The main temperature shows only its number. The duplicate time range, separator and whole-day high/low summary are removed. Tapping anywhere in the gray card opens Weather; swiping still switches widgets.

The last saved update time appears immediately left of Refresh. Together they form one transparent control, with no background or border. Either area updates the forecast, and both dim while busy. The time comes from the saved forecast; failed refreshes preserve it and allow a retry.

Validation: all 109 local tests passed, including native RGB/one-bit rendering, combined touch targets, retries, saved time parsing, page-dot sizing and widget preference restoration. Physical confirmation remains pending installation.

## What's new in 0.75.216

The current weather icon has its own white panel inside the gray dotted panel. It fills the available width and height of the icon’s column, with the icon centered. Both panels have rounded corners, and the 16 px temperature/time spacing is preserved.

Validation: all 109 local tests passed, including native rendering, panel bounds and corners, centering, swipes over the white panel and refresh retries. Physical confirmation remains pending installation.

## What's new in 0.75.215

The current weather icon, temperature and time range share a rounded panel with Home’s original gray dot pattern. The panel fills the space between the heading and hourly forecast while retaining the calendar’s side margins. The temperature and time range now have 16 px of visual separation, up from 8 px.

Validation: 109 local tests passed, including native rendering, the panel’s bounds and pattern, spacing, gestures and refresh retries. Physical confirmation remains pending installation.

## What's new in 0.75.214

Today’s Weather on Home now matches the Calendar widget’s side margins and header alignment. The city line is removed, and the current two-hour period has a larger icon and temperature with a closer time range. A single timeline shows the day in two-hour steps, with the whole-day high and low below it.

The refresh icon immediately left of the Weather shortcut connects Wi-Fi and saves the updated forecast to the microSD. It shows Updating while busy, prevents duplicate downloads and allows retries after network or storage errors. A failed refresh preserves the last saved forecast.

Validation: all 109 local tests passed, including native rendering, aligned headers, gestures, refresh retries and error handling. Physical confirmation remains pending installation.

## What's new in 0.75.213

Home’s upper card now switches between Calendar and Today’s Weather with horizontal swipes. Vertical swipes on Calendar change the month. Weather shows the day summary, city, a large icon and temperature for the current two-hour period, daily high/low and all 24 hourly forecasts. Its upper-right icon opens Weather.

Tapping the calendar heading opens month and year selectors. The action starts as Go to current month and changes to Go to selected month when the choice differs.

The weather widget uses the saved forecast and reloads the local cache in a background worker after a date change; it does not open Wi-Fi on each swipe. Open Weather to update the forecast or choose a city.

Validation: 109 local tests passed, including real gestures, shortcut isolation, month/year selection, hourly parsing, summary hours, units, missing data, cache retries and native large-icon rendering. Physical confirmation remains pending installation.

## What's new in 0.75.212

Home application icons now measure 50 × 50 pixels and no longer have a separate white plate behind them. The original ChatGPT logo returns, scaled proportionally to the new display size. Cards keep their dimensions, spacing and labels.

Validation: 107 local tests passed, including actual creation and rebuilding of all eight cards, and native icon rendering on white/black in color and monochrome buffers. Physical confirmation remains pending installation.

## What's new in 0.75.211

Home application icons now all use Lucide with the same scale and stroke as Books. ChatGPT uses Lucide's assistant icon. Forecast variants, the Home editor and application picker use the same set. Icons are bundled at their display sizes for app-only Wi-Fi updates.

Validation: 106 local tests passed, including all application icons and forecast variants rendered on white/black in color and monochrome buffers. Physical confirmation remains pending installation.

## What's new in 0.75.210

The initial task dictation screen no longer displays an empty text field. The field appears after Write task or when reviewing dictated text. Its text is vertically centered with left alignment, and keeps the same position when the keyboard opens. The lists remain without a counter strip.

Validation: 105 local tests passed, including field timing, original and keyboard text alignment, dictation and saving. Physical confirmation remains pending installation.

## What's new in 0.75.209

Task creation always shows a bordered text field at the top, during dictation, review and editing. Tapping the empty dictation field opens the keyboard editor; dictated text can be corrected directly before saving. The To do and Done lists no longer show the extra counter strip.

Validation: 105 local tests passed, including real keyboard entry and saving edited task text. Physical confirmation remains pending installation.

## What's new in 0.75.208

The numeric keypad edits the original day, month or year field directly. It shows only digits and an icon for backspace: no range hint, duplicate input or accept/cancel row. Close it with the red button or by tapping outside. The form validates and saves the date through Save changes; incomplete or invalid dates cannot be saved.

Validation: 105 local tests passed, including the real keypad inside the task editor. Physical confirmation remains pending installation.

## What's new in 0.75.207

Home now paints an opaque white base beneath its existing texture, so previous-screen controls are covered in the gaps and rounded corners between app cards. The layout and app icons are unchanged.

## What's new in 0.75.206

Date editing uses three fields in one row: day, month and year. Each opens a numeric-only keypad with large digits, delete, accept, cancel and range validation. Two modal actions remain side by side; groups of three or more are stacked at full width.

## What's new in 0.75.205

The date picker has no heading, rounded outline selection without fill, and immediate movement without animation or momentum. Undated tasks hide recurrence. Task actions read Complete, Edit and Delete; Add task is black. Standalone modal headings are removed. Reading uses gestures only; old tap-zone preferences cannot disable them. Instruction diagrams are clearer and aligned.

## What's new in 0.75.204

Task dates include the localized weekday. The compact editor removes Type, uses a With date / No date tab and one calendar field opening scrollable day, month and year columns. The picker has Save and Cancel only. Confirmation actions are arranged horizontally, with confirmation/activation on the left and cancellation/deactivation on the right.

## What's new in 0.75.203

Dictated tasks recognize Spanish weekdays, relative dates, explicit dates and monthly/yearly recurrence locally. A detected date opens a confirmation with Create task and Edit details; editing opens the full form. To do and Done replace Personal/Work and the separate filter; existing tasks from both lists remain visible. Dates follow the local clock and can be checked before saving.

## What's new in 0.75.202

Aligns the month heading and Tasks shortcut with the calendar columns and sizes the Tasks icon to 34 × 34 pixels.

## What's new in 0.75.201

Fixes the DoceInk logo display in System Information. The reduced monochrome logo is drawn at its native size.

## What's new in 0.75.200

The calendar Tasks shortcut is now the clickable icon itself, with no button container, border, background or text. Its height follows the month heading and it stays aligned on the right. Tapping it opens the same Tasks app.

Validation: 104 local tests passed; ESP32-S3 firmware compiled. Physical confirmation remains pending installation.

## What's new in 0.75.199

The calendar gives pending dated tasks and birthdays a black dotted rounded outline, including Personal/Work recurring dates. Today keeps its black fill. Holding a day vibrates and asks for confirmation; only accepting opens creation for that date. The DoceInk logo returns inside the Information card above the version, 20% smaller. Icon with percentage is removed: only Icon and Number remain; the old setting falls back to Icon.

## What's new in 0.75.198

The calendar Tasks shortcut now displays only its icon, with no text, border or background. Its touch area remains comfortable and the month heading has more room. Tapping the icon opens the same Tasks app.

Reader selection uses a black background with white text; saving leaves only the underline. The saved-highlights list has no title or Close button and closes with the red back button. Long previews open by tapping anywhere in their text or row.

## What's new in 0.75.197

Calendar and Tasks use one app with dictation, dates, repeating tasks and birthdays on microSD. Saving tasks reuses a reserved worker instead of allocating another internal stack. Tasks moves from the grid to the month header. Inline highlights can span pages; saved highlights have detail and delete dialogs. Advanced settings, an Instructions dialog and 8 px spacing. ChatGPT microphone stays blocked until ready, with an instruction and right arrow. Home icons align consistently and the locked Settings tile has a continuous hatch.

Validation: 104 local tests passed and ESP32-S3 firmware built. Physical confirmation remains pending installation on Metalio.

## Changes in 0.75.196

Updated reading shortcuts: swipe up opens the reading menu; swipe down opens the chapter index. Hold a word to open the underline selector with that word marked, then tap the final word and save. This replaces double-tap selection. Tap-zone single taps respond immediately again. Help and the illustrated welcome guide reflect the new controls.

## Changes in 0.75.195

Double-tap a word while reading to start underlining, tap the final word in the selection dialog, then save. Works with gestures and tap zones without turning the page on the first tap. The Underline action no longer gets blocked by background chapter counting. Book text remains unchanged by interface translations.

## Changes in 0.75.194

Corrects an unsafe reading-preferences reload introduced in 0.75.193 that could restart Metalio when opening a book. Opening, closing and restoring book preferences now use cached defaults instead of reopening internal storage from the interface task. Also unifies Check for updates and View changes with the standard 64 px button size.

## Changes in 0.75.193

Current chapter highlighted in the index. Per-book reading settings, three reusable profiles, font weight and separate paragraph spacing. Underline using two taps and save passages on microSD. Sharper Home editor icons and a diagonal hatch on the locked Settings card.

Validation: 100 host tests passed, including per-book settings and profile persistence, two-tap underline selection, reversed selection, microSD export failure, native font weights, EPUB reflow anchors and current-chapter highlighting in an 8,000-entry index. ESP32-S3 firmware compiled. Physical-device verification remains pending.

## Changes in 0.75.192

- Reorganized Settings by common tasks. Display now opens Wallpapers first, followed by Home and Appearance. Wallpaper gallery, standby slideshow and dynamic backgrounds stay together. Battery display, system typeface and screen refresh are grouped in Appearance.

- System now separates Energy, General, Clock and Information. Energy puts standby and shutdown timeouts before Wi-Fi power-saving delay; General keeps language and vibration. Existing preferences are preserved.

- Files puts Wi-Fi file transfer and USB Disk ahead of microSD status and capacity. Connections retains Wi-Fi before Bluetooth, with actions before help text.

- Clock puts automatic setup and manual configuration before its detailed explanation. Information puts version, update checking and release notes first, technical details next and logo/credits last.

- Help text uses a smaller secondary style, section tabs stay on one line, and selectors, timers and scrollbars keep their existing behavior.

Validation: 97 host tests passed, including repeated wallpaper/appearance switching in all three locales, late callbacks and leaving while a font applies. ESP32-S3 firmware compiled. Physical-device confirmation remains pending.

## Changes in 0.75.191

- System typeface is limited to four curated families: the original Atkinson default, Inter, Source Sans 3 and Noto Sans. Arbitrary reading fonts no longer appear in this selector.

- Updating from 0.75.190 restores Atkinson. Future choices among the dedicated UI families are saved separately from the previous reader-font preference.

- Replaced bitmap resizing and synthetic bold with native FreeType rasterization for 16 UI size/weight roles, including true regular and semibold. Each role fits the original line box; letters are not stretched or shrunk after rasterization.

- The three optional UI packs are separate from reading fonts, include their open font licenses and download only when selected. The field shows Wi-Fi/download status and progress. Downloads are verified by size and SHA-256 before installation.

- A complete selected pack stays in PSRAM with its SD file closed, so the interface remains available during USB Disk use or after card removal. Atkinson works without SD or Wi-Fi. Failed changes retain the previous face. Missing characters and out-of-box large punctuation use the original built-in fallback.

- Checked native glyph metrics and bitmap bytes for all three packs across 16 size/weight roles, capital baselines, accents, numbers, file removal and storage/network/memory failure paths.

Validation: 96 host tests passed. ESP32-S3 firmware compiled; app size 5,211,904 bytes. Physical-device confirmation remains pending.

## Changes in 0.75.190

- Added System typeface in Settings → Display. Choose Atkinson, the built-in default, or a reading font already saved on the microSD. The book body keeps its separate typography settings.

- The interface preserves its existing font heights, control sizes and icons. Missing characters use the built-in Latin/CJK fallback.

- The selected face is loaded in PSRAM before applying it and the SD file is closed. The interface continues rendering when USB Disk owns the card or the card is removed. No Wi-Fi is needed to apply a downloaded font.

- The selection is saved across restarts. If its file is unavailable at boot, the internal typeface remains usable. Failed changes retain the previous face; Atkinson can be restored without a microSD.

- Verified the 30 catalog families, multiple UI sizes and weights, resident rendering after file removal, and safe handling of storage, USB, memory and worker failures.

Validation: 96 host tests passed; ESP32-S3 firmware compiled and release assets verified against the build. Physical-device confirmation of the new system-font control remains pending.

## Changes in 0.75.189

- Serial diagnostics confirmed about 5 KB of free internal RAM, with a recorded minimum of 0 KB, despite about 7 MB of free PSRAM. Eligible general, Wi-Fi and TCP/IP allocations now prefer PSRAM; DMA and RTOS allocations retain their required internal memory.

- The touch-input task is paused and resumed across standby instead of deleted and recreated. Waking no longer needs to allocate a new 4 KB touch stack after Wi-Fi has used internal RAM. Tested 1,000 wake cycles with new task creation forced to fail.

- An interrupted font download no longer shows the same installed check as a complete family. Locally saved sizes remain usable offline. Use Download remaining sizes in the size controls or the download icon to finish the family without changing the selected font. Closing the catalog refreshes the size arrows.

- Checked all seven sizes, forwards and backwards, for all 30 catalog families, including Raleway. The repair path covers a family with only its 18 px file.

- Font downloads reuse one HTTPS client for the license and seven size files. Failed requests discard that client before retrying. This reduces repeated TLS allocations and connections.

- Weather requests use the network worker reserved at boot instead of allocating a new task for each refresh. Weather explicitly starts Wi-Fi when needed. Its HTTP client is also released if a memory allocation fails.

- Closing the library reading-preferences preview releases its unused font after the preview labels are gone.

- Fixed a standby wallpaper race: if an old decode finishes after standby has been entered again, the new overlay starts its own load instead of remaining on the logo. Decode-allocation failures are handled safely and keep the chosen wallpaper setting.

## Changes in 0.75.188

- Standby waits for the wallpaper to finish loading before it can cut peripheral power. Active font/network downloads keep power, Wi-Fi and the CPU available; standby sleep and wallpaper slideshows wait until the transfer finishes.

- Font downloads test writing to the actual font folder, create missing folders and remove their probe afterwards. Unrelated folder checks cannot reject a writable font directory. Directory creation preserves the original error.

- Transient network failures retry the affected file once. Existing verified font files are retained. Failures include the operation and error code to distinguish storage errors from HTTP, incomplete responses or checksum errors.

- Verified all 240 published font assets against catalog sizes and SHA-256 hashes. Device confirmation of the intermittent failure remains pending.

## Changes in 0.75.187

- Font lists use only the interface font. Removed all per-row font previews, SD glyph loading and preview polling; the selected typeface is shown only in the reading sample.

- The arrows cycle through installed fonts and the builtin face. They never open the list or start a download. Only the central name/chevron field opens the complete catalog.

- Fixed font changes in reading preferences opened from the library without an active book. Old sample labels are removed before replacing their font; active reader labels are also cleared before freeing a font.

- Rapid preference changes share one coalescing save worker instead of creating a task and stack for every tap. The latest value of each preference is retained.

- Downloads check the actual microSD filesystem while holding the USB/storage ownership lock. A stale mount flag no longer rejects an accessible card. Errors distinguish missing or invalid files, unavailable/full/read-only/busy storage and USB ownership.

Validation: firmware build and 88 software tests passed, including 1,000 coalesced font preference changes, preview refresh without an open book, repeated arrow changes without opening the catalog, and storage/USB ownership checks. On-device confirmation of the reported hang remains pending; no USB log was available. Wi-Fi OTA preserves user data and installers retrieve the latest stable release.

## Changes in 0.75.186

- The font field between the arrows now uses the normal interface font: name and chevron only, with no typeface preview or SD font loading.

- Selecting a usable local font no longer requires all seven catalog sizes and never starts a download just because other sizes are absent. Local files are checked before applying them.

- Font downloads consume the final HTTP chunk before verifying completion, fixing rejection of otherwise complete chunked responses while retaining size and SHA-256 checks.

- Only one download can be active. Font rows ignore repeated taps and suspend their click vibration while busy, then become available again. Failure text shows the actual storage, network or download error.

- Font-name previews are detached from labels before their memory is freed when closing the modal or starting a download. Previews pause during downloads to reduce memory and SD activity.

- Fixed reverse scrolling on static content such as System → Information. Overflowing scroll surfaces can receive drag gestures even when their text/cards are not clickable. The shared fix covers vertical and horizontal scrolling while keeping non-scrollable and non-overflowing pass-through objects inert.

- Removed the duplicate ChatGPT subsection from Settings → System. ChatGPT configuration remains available inside the ChatGPT application.

Validation: firmware build and 86 software tests passed, including partial local families, chunked HTTP completion, repeated taps, error handling and 100 preview/modal close cycles. These fixes still require on-device verification; the exact cause of the reported device hang has not been captured. Wi-Fi OTA preserves user data and installers obtain the latest stable release.

## Changes in 0.75.185

- Font downloads show Searching for Wi-Fi, Connecting, Downloading with percentage, and Verifying directly in the tapped row. Failures leave a visible retry message. The connection is requested explicitly and has a 30-second timeout.

- Progress updates as bytes arrive across the complete family, including its license; Verification must succeed before progress reaches 100%.

- The font modal is a continuous list with bottom separators, no rounded item cards, and a visible scrollbar. Arrow selection of a missing family opens its download list.

- Font-name previews use a compact, consistent height independent of the reading size. The central field is limited to 26px line height and the list to 30px; original SD font files and reading sizes are preserved.

Validation: Cabin’s seven font assets were downloaded from GitHub and matched their published copies. Firmware build and 86 software tests passed. On-device validation is pending. Wi-Fi OTA preserves user data. Installers retrieve the latest stable firmware.

## Changes in 0.75.184

- Hold the reading screen to open its menu. Swipe up or down for the chapter index; horizontal swipes turn pages. The welcome guide and Controls text use these gestures.

- Typography reuses the microSD inventory and preserves the reader preview when switching tabs.

- Tap the central font field to open a scrollable modal without a title or Back button. Names align left; Lucide download/check icons align right. Downloads show progress inside their row. Installed names use their own fonts, with small previews that release SD files immediately.

- Removed Manage fonts and Import buttons. Existing EF fonts are discovered automatically; new TTF/OTF files in fonts_ttf are converted at 25px in the background after boot, without Wi-Fi or replacing existing EF files.

- Added persistent letter spacing from -1 to 4px below font size. Text measurement, pagination, justification and selection share the same spacing. Bionic initials are one weight level lighter.

- Screen refresh uses a single segmented Automatic/Manual tab control.

- Display → Home mirrors the eight-shortcut grid. Choose each editable tile’s app; Settings stays fixed and disabled at the bottom right.

Validation: firmware build and 86 software tests passed. On-device verification of these changes is pending. Wi-Fi OTA preserves user data. The Windows and Apple Silicon installers download the latest stable firmware.

## Changes in 0.75.183

- Offline, localized Release notes in Information show changes in the installed version and its predecessor.
- Automatic clock setup displays Configuring... while busy; its white caption stays readable on the black button.
- Reader justification distributes extra width between words, preserves the final line of a paragraph, selection and original text. Bionic initials receive stronger emphasis.
- A 30-family catalog downloads only the chosen family to microSD, with seven sizes and its OFL license. Downloads verify SHA-256 and preserve the current font if they fail. Saved fonts work offline.
- The clean-install interface font pack drops from 4,985,431 to 2,585,690 bytes. All original codepoints and retained glyph bitmaps remain available, including math symbols. The complete payload, including firmware and other resources, is about 8.29 MB versus 10.66 MB in 0.75.182. Full flash images remain 16 MB including empty regions.
- Wi-Fi OTA preserves user data and the previous font partition. The smaller internal font pack is supplied by the clean installer. Existing microSD fonts are retained.
- Firmware build and 81 software tests passed. Physical validation of these changes is pending.

## Changes in 0.75.182

- Chapter titles remain left-aligned and are centered vertically within each index item; the scrollbar stays visible.
- Reader settings move above a localized sample and the selected reader-footer elements, preserving the book position.
- Clock setup detects an approximate city and IANA time zone over Wi-Fi, synchronizes date/time and handles daylight saving; manual date/time and UTC offset are edited in a modal.
- Remove the counter-standby toggle: running counters always use the supported standby behavior.
- Finished-game End game buttons align directly below the board.
- Firmware build and targeted software regressions passed. Physical verification of these changes is pending.

## Changes in 0.75.158

- Choose Celsius or Fahrenheit in Weather settings; the selection applies to the forecast and Home card using saved data offline.
- The firmware compiled and the automated Weather display test passed. On-device validation is pending.

## Changes in 0.75.157

- Hourly precipitation probabilities are displayed up to 99% to keep them on one line.

## Changes in 0.75.156

- Reduce temporary internal memory requirements when saving RSS sources and checking for updates.

## Changes in 0.75.155

- The configured standby CPU frequency no longer slows interactive use when offline. Normal use runs at the configured system frequency; the saved 80/160/240 MHz value applies while standby is visible. Audio recording and wake transitions retain normal speed.
- The preference and personal data are preserved. During eligible standby, light sleep already gates the CPU clock; actual energy savings are not yet measured.
- The firmware compiled and all 65 automated tests passed. Physical verification of standby, wake and recording remains pending.

## Changes in 0.75.154

- Fixes the frozen-looking interface in manual refresh mode. Ordinary partial updates continue to show interactions; periodic full ink cleaning is deferred until the microphone button is pressed. System transitions such as standby and shutdown can still perform a full refresh.
- All 64 automated tests passed, including a test that confirms partial updates continue in manual mode. Physical verification remains pending.

## Changes in 0.75.153

- News setup is positioned below its toolbar from the first opening. No Wi-Fi connection is requested on entry; Configure News connects on demand and generates the QR.
- Settings → Display → Display now offers automatic or manual screen refresh. In manual mode press the microphone button once to refresh the current screen. This setting persists across restarts.
- Firmware build and all 64 automated tests passed. Manual refresh and first-time News setup still require verification on physical Metalio.

## Changes in 0.75.152

- Offline Recorder: view date-stamped recordings from the toolbar, play them locally, and delete with confirmation. Pause/resume and stop are side by side. A recording indicator appears in the top bar and standby while recording. The Home icon uses the Lucide microphone.
- News and ChatGPT setup screens retain the status bar and toolbar, with the setup message inside the content card.
- 64 automated tests pass, including WAV validation and recording-indicator state. On-device verification of playback, deletion, standby and the setup layouts remains necessary.

## Changes in 0.75.151

- Fixed a reboot while checking for updates when Wi-Fi was disconnected. Verified on Metalio.

## Changes in 0.75.150

- Wi-Fi connects on demand, instead of automatically at startup or when returning to Home. Explicit online actions can request a connection.
- New offline Recorder: mono 16 kHz WAV written directly to microSD, pause/resume, recording during standby, stop confirmation and save/discard. Hold a Home shortcut and choose Recorder to add it.
- Reader progress represents the whole book. Unknown chapter lengths no longer count as one page; the provisional estimate is replaced when pagination finishes. The bar is one pixel taller and the saved library percentage is updated too.
- ChatGPT uses the available conversation height with an 8 px bottom inset. Voice input is blocked during responses and speaker playback. History is read-only and shows a notice when voice input is attempted.
- Centered ChatGPT and News setup screens with larger bold titles and black buttons. The logout confirmation fits its contents.
- New boot and Information logo, displayed for two seconds at startup. Library actions use standard 64 px buttons and 22 px labels.
- Cover previews avoid upscaling existing low-resolution images and use a single monochrome conversion without an ordered grid or slow two-pass grayscale refresh.
- English is the fresh-install default. English, Spanish and Simplified Chinese catalogs and pairing/file-transfer pages were reviewed. OTA retains the selected language and user data.

Validation: all 64 automated tests pass, ESP32-S3 compilation succeeds, and the clean image has verified blank personal-data regions. Firmware: 5,112,960 bytes, leaving 147,056 bytes in its 5 MiB OTA partition. Recorder behavior during standby and cover appearance still require on-device verification. The owner confirmed a previous clean installation from Windows; macOS USB installation remains unverified on hardware.
