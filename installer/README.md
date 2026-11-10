# Desktop installer source

**English** | [Español](README.es.md)

This directory contains the Windows/macOS GUI installer, not the complete firmware source project. End users should download the `.exe` or architecture-specific `.dmg` from [Releases](https://github.com/Faga250885/Doceink/releases/latest). Installer 0.75.149.1 detects USB automatically and has no port selector.

## Build

Use Windows x64 and Python 3.14.3, matching the published build environment:

```powershell
.\installer\build.ps1
```

The script creates a local environment, installs pinned dependencies, runs the installer/download tests and packages a windowed executable with PyInstaller. It bundles tools, artwork and licenses, never firmware. At installation time `download.py` fetches the latest stable release from Faga250885/Doceink, verifies its asset digest and image manifest, and passes the verified image to the confirmed installation flow.

For macOS, build natively on macOS 15+ with Python 3.14.3 and Tkinter:

```sh
python3 -m venv installer/.venv
source installer/.venv/bin/activate
python -m pip install -r installer/requirements-lock.txt
python installer/build_macos.py
```

The build creates an architecture-specific `.app` inside a DMG for Apple Silicon or Intel. It tests resources, the bilingual UI, live download verification and the read-only mounted DMG. No test opens a serial port. [Build desktop installers](../.github/workflows/installers.yml) runs this on both Mac architectures and Windows through GitHub Actions, with read-only repository permissions. Builds are uploaded as CI artifacts; publication is a separate step.

The macOS app uses an ad-hoc integrity signature. **Apple Developer ID signing and notarization are not configured**; Gatekeeper acceptance is not claimed. See [macOS package notes](MACOS.md). Windows installers are unsigned as well.

The source distribution attached to the release includes the installer source and the unmodified esptool and PyInstaller source archives. Dependencies retain their licenses; the installed application's Licenses button shows the bundled notices. esptool is GPL-2.0-or-later; PyInstaller has a bootloader exception. See the upstream license texts in the source archives.

## Tests

`test_installer.py` checks image integrity, correct chip/flash gating, failure before writing, automatic detection and disconnection, macOS aliases, ambiguous devices, cancellation and both UI languages. Tests use a simulated esptool runner; they never open a real port. `test_download.py` checks latest-release selection, newer firmware, download integrity, invalid packages and failure before USB access.

The packaged executable also supports internal verification modes:

```powershell
.\DoceInk-Setup-0.75.149.1.exe --self-test result.json
.\DoceInk-Setup-0.75.149.1.exe --smoke-test gui.json
.\DoceInk-Setup-0.75.149.1.exe --download-test download.json
```

These verify included resources and the GUI without enumerating or opening serial ports. They do not replace a real hardware installation test.

The download test can use `DOCEINK_TEST_GITHUB_TOKEN` to avoid shared CI runner rate limits. This ephemeral token is read only in that test mode, is sent only to the GitHub API without forwarding to download redirects, and is never bundled or required by the GUI.

The installer is a clean-install tool: only a confirmed Install action reaches `run_install()`. Normal Wi-Fi updates use the OTA application and preserve user data.
