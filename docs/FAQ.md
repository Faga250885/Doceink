# FAQ and troubleshooting

**English** | [Español](PREGUNTAS-FRECUENTES.md)

[Back to the main page](../README.md)

### Does this work on any ESP32 or e-reader?

No. The full package is built for **Metalio E-Ink4, ESP32-S3 and 16 MB of flash**, with its screen and peripherals. Other boards have not been validated.

### Does the installer include someone else's data?

The package is created from build outputs, not a dump of a Metalio in use. It contains no developer accounts, Wi-Fi passwords, API keys, conversations or personal content. Public project links and system resources remain part of the firmware.

### Does installation erase my microSD too?

No. The full image replaces internal flash but does not format the card. Use an empty card to start without previous data. Normal Wi-Fi updates also preserve the card and internal settings.

### Why is the image 16 MB if the firmware is smaller?

The full image includes the bootloader, fonts, resources and empty regions. In 0.75.149, the application uses 4,989,152 bytes of a 5 MiB partition, leaving 253,728 bytes in that partition. That is not user storage for books; personal files are stored on microSD.

### Can I install the full image over Wi-Fi?

No. Use `Doceink-EInk4.bin` to update an existing system. The full `Metalio-instalacion-limpia.bin` image is flashed over USB from a computer using the installation guide, not the OTA updater.

### Windows does not show a COM port

Check that the cable supports data, try another USB port and disable USB disk mode on Metalio. Close serial-terminal programs. If download mode is needed, use the physical BOOT button while restarting, then check which port appears. See [Installation](INSTALLATION.md).

### The port is busy or the connection times out

Close other programs using the COM port, verify that the correct port is selected and that Metalio is in download mode. For unstable connections, try another cable and a direct USB connection. Include the tool's error message when reporting the problem.

### Windows shows an unknown-publisher warning

The executable is currently unsigned. Obtain it from the official release and compare its checksum with SHA256SUMS.txt. The main installation method does not require PowerShell or changing system execution policies.

### The SHA-256 check fails

Do not flash the image. Download the ZIP for that version again and extract it completely. Do not mix one version's manifest with another version's image.

### Installation was interrupted

This does not necessarily make Metalio unusable. Enter download mode with BOOT again, check the port and repeat the complete installation. If no port appears, check the cable and power. Do not attempt recovery using firmware for a different board.

### My old conversations still appear after installation

They may be on the microSD card. The installer does not erase it. To start without previous content, remove it or use an empty card, keeping the old one as a backup.

### News or Weather is empty offline

Each application needs an initial download saved to microSD. Connect Wi-Fi, check the RSS source or city, and press Refresh. Subsequent openings use the stored copy.

### Does voice input work without internet?

Not in this version. ChatGPT and task dictation use Wi-Fi. Tasks are saved locally and history can be read from microSD.

### Do I need Python or commands on Windows?

No. Download `DoceInk-Setup-0.75.149.exe`, connect Metalio and run it. Select Spanish if preferred. The ZIP and terminal commands are optional alternatives for manual installation or other operating systems.

### Where is the source project for building the firmware?

This repository currently distributes firmware and user documentation, and includes the Windows installer source under `installer/`. GitHub's automatic “Source code” download contains this repository's files; it is not the installation ZIP or the full firmware build project.

### How do I report a problem?

[Open an issue](https://github.com/Faga250885/Doceink/issues/new?template=bug-report.md) with the exact version, steps and error message. For installation problems, include your operating system and esptool output. Do not post API keys, Wi-Fi passwords or private conversations. You can attach a photo with private details hidden.

### Chrome or Defender blocks the installer

Windows Defender reported `Trojan:Win32/Wacatac.B!ml` for the 0.75.148 executable. Do not bypass the block or disable antivirus protection. The 0.75.149 installer was rebuilt without embedded firmware; a local Microsoft Defender custom scan found no threats. This does not guarantee that Chrome or cloud-based checks will accept it, and the earlier detection has not been declared a confirmed false positive. Report any new detection with its exact name and file version. Microsoft provides a [file-analysis submission portal](https://www.microsoft.com/en-us/wdsi/filesubmission).
