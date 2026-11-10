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
- [Documented version: 0.75.148](https://github.com/Faga250885/Doceink/releases/tag/v0.75.148).
- [OTA firmware: 0.75.148](https://github.com/Faga250885/Doceink/releases/download/v0.75.148/Doceink-EInk4.bin).

`Doceink-EInk4.bin` contains only the update application. It does not include the bootloader, partition table or complete resource package needed for a fresh installation. For that, use the [clean installation guide](INSTALLATION.md).

Do not use `Metalio-instalacion-limpia.bin` in the Wi-Fi updater. These files are not interchangeable just because both end in `.bin`.

## Changes in 0.75.148

- Fixed repeated redraws in Information while idle; shared update buttons now redraw only when their busy state changes.
- Firmware information now shares a thin black outline and full width with the information panel below.
- Black Check for updates button, with a small centered email-only creator credit underneath.
- Wi-Fi updates continue to preserve user accounts, settings and microSD data.

The application is 4,989,072 bytes. No percentage speed improvement is claimed. See [Releases](https://github.com/Faga250885/Doceink/releases) for earlier versions.
