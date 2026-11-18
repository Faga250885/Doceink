# Audiobooks on Metalio

Use **0.75.248 or later** for 15-second backward/forward controls, progress to two decimal places and a floating rounded white toolbar with Library on the left and Restart on the right. Eight-pixel gaps separate it from the top bar, side edges and content. Includes a gray cover backdrop, list dividers and seek feedback on the center button. A headphone icon beside the clock indicates audiobook playback, including other screens and standby; it disappears when paused or finished. M4B/M4A support from 0.75.241 remains.

Available in **0.75.236**. This first version supports **MP3** and **16-bit PCM WAV**, mono or stereo, at 8–48 kHz, stored on microSD. MP3 is recommended for its smaller size. Since **0.75.241**, DRM-free **M4B and M4A with AAC-LC** are also supported, mono/stereo at 8–48 kHz and below 2 GB. HE-AAC, ALAC and fragmented MP4 are not supported. M4B plays as one track; internal chapters and embedded artwork are not exposed yet.

Long-press a configurable Home icon and choose **Audiobooks**, marked with headphones. The Settings tile keeps its fixed position.

Open **Settings → Files → Transfer files over Wi-Fi**, follow the QR/link, and upload a file into `metalio/e-ink/audiobooks`. Close the transfer and open Audiobooks; leave and reopen the library if it was already open. A single MP3 is enough for the first test.

When preparing the card on a computer, you can group numbered chapter files in one folder per book. Chapters play in natural filename order, so 2 precedes 10, and playback continues automatically to the next chapter. Limits are 64 books, 512 tracks in total and 256 tracks per book.

List and thumbnail views are available. Optional covers use the same basename as a standalone audio file, with `.jpg` or `.png`, or `cover.jpg` / `cover.png` inside a chapter folder. Embedded MP3 or M4B/M4A artwork is not extracted yet.

Select a book to play, pause/resume or restart from the beginning with confirmation using the black-bordered icon-only button at the right edge of the white toolbar. The player displays large artwork or a simple title cover when artwork is missing. The **15 s** controls on either side of Play/Pause move backward or forward, also while paused. They can cross chapter files and update the saved position. During seeking the center button shows **Rewinding…** or **Forwarding…** until audio resumes; paused seeking stays paused when complete. Use Metalio's physical volume buttons. Playback continues when leaving the app and during standby. The CPU, speaker and microSD stay powered for playback; Wi-Fi is not required. Progress updates about every ten seconds while visible, and stops updating in standby. A two-decimal percentage makes small advances visible: in a 23-hour book, one progress-bar pixel represents about three minutes.

Position is saved periodically and when stopping in small microSD sidecar files. An unexpected power cut can lose the last few seconds. Finished books restart from the beginning on the next play. MP3 duration is approximate, especially for VBR files. Pause playback before recording or using a voice conversation.

Synchronized text is planned for later.

For a Spanish test recording, see [Cuentos de la selva para los niños by Horacio Quiroga on LibriVox](https://librivox.org/cuentos-de-la-selva-para-los-ninos-by-horacio-quiroga/) and [download the first chapter, La abeja haragana](https://archive.org/download/cuentosdelaselva_1603_librivox/cuentosdelaselva_01_quiroga_128kb.mp3). This is about 13.6 MB and 14 minutes. LibriVox's source page lists its readers and public-domain information. Audio is not bundled in the firmware.

## Bluetooth headphones

From **0.75.249**, open **Settings → Connections → Bluetooth**, select **Headphones**, put your headphones in pairing mode, tap **Find headphones** and choose their name. Wait for confirmation before playing your audiobook. Pause playback before changing the output. Pairing and sound require a physical test on Metalio.

Tap the timer, recording or audiobook indicator beside the clock to reopen its activity. Each has a separate 44 × 44 px touch target.
