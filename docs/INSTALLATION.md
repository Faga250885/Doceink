# Install DoceInk

**English** | [Español](INSTALACION.md)

[Back to the main page](../README.md)

## Windows: connect and run

1. [Download DoceInk Setup 0.75.158.1](https://github.com/Faga250885/Doceink/releases/download/v0.75.158/DoceInk-Setup-0.75.158.1.exe).
2. Connect **Metalio E-Ink4** with a USB data cable. Disable USB disk mode if it is active.
3. Open the downloaded `.exe`. It includes the installation tools and downloads the latest stable firmware from GitHub automatically. You do not need Python or terminal commands. Internet access is required.
4. Metalio is detected automatically. There is no COM-port selector. If several compatible USB devices are connected, leave only Metalio connected.
5. On an original device, keep the backup option enabled, confirm the currently installed firmware is original, then confirm the clean installation. Keep USB connected until it finishes. Metalio then restarts. If DoceInk is already installed, choose **Update DoceInk** to preserve internal settings or restore an existing backup for the same device.

The installer opens in English. Select **Español** at the top for Spanish prompts.

## macOS: app with automatic USB detection

1. Download the [Apple Silicon DMG](https://github.com/Faga250885/Doceink/releases/download/v0.75.158/DoceInk-Setup-0.75.158.1-macOS-arm64.dmg) for M1 or later, or the [Intel DMG](https://github.com/Faga250885/Doceink/releases/download/v0.75.158/DoceInk-Setup-0.75.158.1-macOS-x86_64.dmg). Requires **macOS 15 or later**.
2. Open the DMG and drag **DoceInk Setup** to Applications, then open the app.
3. Connect Metalio with a USB data cable, with USB disk mode disabled. It detects the connection automatically; no terminal commands, Python installation or port selection are needed.
4. Click **Install DoceInk** and confirm. The app downloads and verifies the latest stable firmware from GitHub before writing.

**Signing status:** the app has an ad-hoc integrity signature, but no Apple Developer ID signature or notarization. Gatekeeper may block its first launch. This is not yet a notarized, warning-free Mac distribution; do not disable Gatekeeper. The native builds and automated tests do not establish a successful physical USB installation.

Installer version **0.75.158.1** and firmware version **0.75.158** are independent. Older online installers also consult the latest release on each installation.

## What happens to my data?

**This is a clean USB installation. It replaces internal flash and erases accounts, saved networks and settings on the selected Metalio.** It asks for confirmation before writing. The microSD card is not erased. Use an empty card if you also want to start without previous books, tasks or history.

**Normal Wi-Fi updates preserve user data.** The desktop installer also offers a USB update for recognized DoceInk installations, preserving internal settings. Backup, restore and USB-update workflows have simulated tests but have not yet been validated end to end on physical hardware.

The firmware package does not include developer accounts, passwords, API keys or personal conversations. After installation, configure your own network and accounts.

## Original firmware backup

Before the first clean installation, the optional backup reads the entire internal flash twice and verifies both copies. Confirm that the current firmware really is original: a backup made after DoceInk was installed cannot recover the original firmware. It is stored unencrypted in `~/DoceInk/Backups/<device-id>` on the computer and may contain Wi-Fi passwords and account keys. Keep both backup files private and safe. It does not include the microSD.

When a matching verified backup exists, the installer offers to restore it to the same Metalio. Restoring replaces the entire internal flash, including current accounts and settings, with the saved contents; it does not erase the microSD. Device detection may restart Metalio.

## Requirements and checks

- Metalio E-Ink4, ESP32-S3, **16 MB flash**. Other boards are not supported.
- Windows 10/11 x64, or macOS 15+ (Apple Silicon or Intel), and a USB data cable.
- Each installation checks GitHub again and downloads its latest stable release. It verifies the release SHA-256 and image manifest before writing to the USB device. There is no older offline fallback.
- The installer checks the image size and SHA-256, rejects a different ESP chip, and checks for 16 MB flash before writing. These checks cannot identify every board that uses the same ESP32-S3 chip; connect only the specified Metalio model.

[SHA256SUMS.txt](../SHA256SUMS.txt) lists the executable and firmware checksums. The executable is currently unsigned, so Windows may display an unknown-publisher or SmartScreen notice. Obtain it from this repository's release and verify the download if Windows asks you to review it; no antivirus changes are required.

## If Metalio is not detected

Use **Connection help** in the installer. Check the data cable, turn off **Disco USB / USB disk** on Metalio, and close serial-terminal programs.

Most compatible USB connections can enter download mode automatically. If yours cannot, hold the physical **BOOT** button while restarting Metalio, release it, and retry. BOOT is the GPIO0 hardware button, not the red touch button in the interface. Consult the manufacturer's instructions to locate it. Detection refreshes automatically, including after reconnection. If the USB connection changes during the firmware download, the installer stops before writing and lets you retry.

Do not disconnect USB during installation. If an error occurs, the installer shows details and allows you to retry. It does not report success after a failed operation.

## After installation

Metalio should restart and show the DoceInk symbol and name for two seconds before the main screen. If it remains in download mode, restart without holding BOOT. Follow [Getting started](GETTING-STARTED.md) to configure your microSD, Wi-Fi and accounts.

## Advanced installation: Linux or manual recovery

Download the [full-image ZIP](https://github.com/Faga250885/Doceink/releases/download/v0.75.158/Metalio-0.75.158-instalacion-limpia.zip) and extract it. The image is `Metalio-instalacion-limpia.bin`; that filename is retained for compatibility. Windows and Mac users normally use the GUI installer above.

In a terminal inside the extracted folder:

```sh
python3 -m venv .venv
source .venv/bin/activate
python -m pip install esptool==4.12.0
```

Check the full image with `shasum -a 256 Metalio-instalacion-limpia.bin` on macOS or `sha256sum Metalio-instalacion-limpia.bin` on Linux. Expected SHA-256:

```text
015382ef15d4a9cb62be1f3793c77f83463ae61097fc1767289eb92288a8d34f
```

Replace `PORT` with the actual serial port. Typical names are `/dev/cu.usbmodem…` on macOS or `/dev/ttyACM…` on Linux. **This manual command writes directly, erases internal settings and does not show the Windows installer's confirmation.**

```sh
python -m esptool --chip esp32s3 --port PORT --baud 460800 write_flash --flash_mode dio --flash_freq 80m --flash_size 16MB 0x0 Metalio-instalacion-limpia.bin
```

This uses [Espressif's esptool 4.12.0](https://pypi.org/project/esptool/4.12.0/). If serial access is denied, check your operating system's device permissions. The macOS/Linux flashing route has not been tested on physical hardware.

## Validation and image contents

The firmware compiles successfully. Startup rendering and display/input regression tests passed. Installer 0.75.158.1 has sixteen automated tests covering automatic USB selection, disconnection, cancellation, firmware validation and download handling. Packaged app checks exercise resources, the bilingual interface and a verified live download without opening a USB port. macOS packages also verify and mount the DMG read-only. **The owner confirmed a clean installation from Windows on a physical Metalio. The new firmware features still need physical validation; macOS USB installation remains unverified.**

The complete image contains the bootloader, partition table, application, fonts and system resources. NVS, PHY data, the second application partition and crash-dump regions are blank. See the [manifest](releases/v0.75.158-manifest.json).

The image is 16 MB including empty space. The application is **5,114,240 bytes**. Neither the complete image nor the `.exe` is an OTA file; use `Doceink-EInk4.bin` for firmware updates.
