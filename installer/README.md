# Windows installer source

**English** | [Español](README.es.md)

This directory contains the GUI installer, not the complete firmware source project. End users should download the ready-to-run `.exe` from [Releases](https://github.com/Faga250885/Doceink/releases/latest).

## Build

Use Windows x64 and Python 3.14.3, matching the published build environment:

```powershell
.\installer\build.ps1
```

The script creates a local environment, installs the pinned dependencies, downloads the full firmware image, runs the installer tests and packages a windowed executable with PyInstaller. It does not open a serial port or flash hardware. You can supply `-FirmwareZip` with a local full-image ZIP.

The source distribution attached to the release includes the installer source and the unmodified esptool and PyInstaller source archives. Dependencies retain their licenses; the installed application's Licenses button shows the bundled notices. esptool is GPL-2.0-or-later; PyInstaller has a bootloader exception. See the upstream license texts in the source archives.

## Tests

`test_installer.py` checks image integrity, correct chip/flash gating, failure before writing, ambiguous-device detection, cancellation and both UI languages. Tests use a simulated esptool runner; they never open a real port.

The packaged executable also supports internal verification modes:

```powershell
.\DoceInk-Setup-0.75.146.exe --self-test result.json
.\DoceInk-Setup-0.75.146.exe --smoke-test gui.json
```

These verify included resources and the GUI without enumerating or opening serial ports. They do not replace a real hardware installation test.

The installer is a clean-install tool: only a confirmed Install action reaches `run_install()`. Normal Wi-Fi updates use the OTA application and preserve user data.
