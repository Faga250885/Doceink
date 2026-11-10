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
- [Documented version: 0.75.150](https://github.com/Faga250885/Doceink/releases/tag/v0.75.150).
- [OTA firmware: 0.75.150](https://github.com/Faga250885/Doceink/releases/download/v0.75.150/Doceink-EInk4.bin).

`Doceink-EInk4.bin` contains only the update application. It does not include the bootloader, partition table or complete resource package needed for a fresh installation. For that, use the [clean installation guide](INSTALLATION.md).

Do not use `Metalio-instalacion-limpia.bin` in the Wi-Fi updater. These files are not interchangeable just because both end in `.bin`.

## Changes in 0.75.150

- Wi-Fi connects on demand, instead of automatically at startup or when returning to Home. Explicit online actions can request a connection.
- New offline Recorder: mono 16 kHz WAV written directly to microSD, pause/resume, recording during standby, stop confirmation and save/discard. Hold a Home shortcut and choose Recorder to add it.
- Reader progress represents the whole book. Unknown chapter lengths no longer count as one page; the provisional estimate is replaced when pagination finishes. The bar is one pixel taller and the saved library percentage is updated too.
- ChatGPT uses the available conversation height with an 8 px bottom inset. Voice input is blocked during responses and speaker playback. History is read-only and shows a notice when voice input is attempted.
- Centered ChatGPT and News setup screens with larger bold titles and black buttons. The logout confirmation fits its contents.
- New boot and Information logo, displayed for two seconds at startup. Library actions use standard 64 px buttons and 22 px labels.
- Cover previews avoid upscaling existing low-resolution images and use a single monochrome conversion without an ordered grid or slow two-pass grayscale refresh.
- English is the fresh-install default. English, Spanish and Simplified Chinese catalogs and pairing/file-transfer pages were reviewed. OTA retains the selected language and user data.

Validation: all 64 automated tests pass, ESP32-S3 compilation succeeds, and the clean image has verified blank personal-data regions. Firmware: 5,095,824 bytes, leaving 147,056 bytes in its 5 MiB OTA partition. Recorder behavior during standby and cover appearance still require on-device verification. The owner confirmed a previous clean installation from Windows; macOS USB installation remains unverified on hardware.
