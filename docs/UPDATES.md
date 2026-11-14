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
- [Documented version: 0.75.185](https://github.com/Faga250885/Doceink/releases/tag/v0.75.185).
- [OTA firmware: 0.75.185](https://github.com/Faga250885/Doceink/releases/download/v0.75.185/Doceink-EInk4.bin).

`Doceink-EInk4.bin` contains only the update application. It does not include the bootloader, partition table or complete resource package needed for a fresh installation. For that, use the [clean installation guide](INSTALLATION.md).

Do not use `Metalio-instalacion-limpia.bin` in the Wi-Fi updater. These files are not interchangeable just because both end in `.bin`.

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
