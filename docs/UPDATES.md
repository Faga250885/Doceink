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
- [Documented version: 0.75.194](https://github.com/Faga250885/Doceink/releases/tag/v0.75.194).
- [OTA firmware: 0.75.194](https://github.com/Faga250885/Doceink/releases/download/v0.75.194/Doceink-EInk4.bin).

`Doceink-EInk4.bin` contains only the update application. It does not include the bootloader, partition table or complete resource package needed for a fresh installation. For that, use the [clean installation guide](INSTALLATION.md).

Do not use `Metalio-instalacion-limpia.bin` in the Wi-Fi updater. These files are not interchangeable just because both end in `.bin`.

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
