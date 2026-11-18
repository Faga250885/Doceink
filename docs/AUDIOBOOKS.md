# Audiobooks on Metalio

Use **0.75.240 or later** for the Cover player layout with large artwork, separate elapsed/total times and bottom controls. It retains saved positions and the performance improvements of 0.75.239.

Available in **0.75.236**. This first version supports **MP3** and **16-bit PCM WAV**, mono or stereo, at 8–48 kHz, stored on microSD. MP3 is recommended for its smaller size. M4B, M4A/AAC and DRM-protected files are not supported yet.

Long-press a configurable Home icon and choose **Audiobooks**, marked with headphones. The Settings tile keeps its fixed position.

Open **Settings → Files → Transfer files over Wi-Fi**, follow the QR/link, and upload a file into `metalio/e-ink/audiobooks`. Close the transfer and open Audiobooks; tap refresh if needed. A single MP3 is enough for the first test.

When preparing the card on a computer, you can group numbered chapter files in one folder per book. Chapters play in natural filename order, so 2 precedes 10, and playback continues automatically to the next chapter. Limits are 64 books, 512 tracks in total and 256 tracks per book.

List and thumbnail views are available. Optional covers use the same basename as a standalone audio file, with `.jpg` or `.png`, or `cover.jpg` / `cover.png` inside a chapter folder. Embedded MP3 artwork is not extracted yet.

Select a book to play, pause/resume or restart from the beginning with confirmation. The player displays large artwork or a simple title cover when artwork is missing. Use Metalio's physical volume buttons. Playback continues when leaving the app and during standby. The CPU, speaker and microSD stay powered for playback; Wi-Fi is not required. Progress updates about every ten seconds while visible, and stops updating in standby.

Position is saved periodically and when stopping in small microSD sidecar files. An unexpected power cut can lose the last few seconds. Finished books restart from the beginning on the next play. MP3 duration is approximate, especially for VBR files. Pause playback before recording or using a voice conversation.

Bluetooth headphones and synchronized text are planned for later.

For a Spanish test recording, see [Cuentos de la selva para los niños by Horacio Quiroga on LibriVox](https://librivox.org/cuentos-de-la-selva-para-los-ninos-by-horacio-quiroga/) and [download the first chapter, La abeja haragana](https://archive.org/download/cuentosdelaselva_1603_librivox/cuentosdelaselva_01_quiroga_128kb.mp3). This is about 13.6 MB and 14 minutes. LibriVox's source page lists its readers and public-domain information. Audio is not bundled in the firmware.
