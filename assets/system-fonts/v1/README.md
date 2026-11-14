# Dedicated system typefaces / Tipografías de interfaz

DoceInk 0.75.191 limits the interface to Atkinson (built in) and these three optional families. This is separate from the reading-font catalog.

- [Inter](https://rsms.me/work/inter/) was designed for screen interfaces, with work on small-size rendering. These packs use the Text optical design and real 400/600 weights.
- [Source Sans 3](https://github.com/adobe-fonts/source-sans) is Adobe’s sans-serif family for user-interface environments.
- [Noto Sans](https://github.com/notofonts/noto-docs/blob/main/docs/specimen/NotoSans.md) supplies a neutral sans-serif design; absent scripts retain the firmware’s existing fallback.

The choice is an engineering selection for this UI, followed by native bitmap and layout checks; physical e-paper confirmation remains pending.

Each `.uif` contains sixteen native size/weight roles, with packed two-bit grayscale glyphs generated directly from the original outlines using FreeType autohinting. No bitmap resizing or synthetic bold is used. Native raster sizes fit the original interface line boxes. Large punctuation which cannot fit uses the original built-in fallback. `manifest.json` records the pinned source revision, original font hashes, output hashes, role sizes and actual raster sizes. Packs include copyright, attribution and the complete SIL Open Font License; copies are also provided beside them.

Rebuild using `tools/fonts/build_system_fonts.py` in the development source with the source commit recorded in the manifest. Sources come from the official Google Fonts distribution. Font files are not changed by the generation process; these are application-specific raster resources.

En Ajustes → Pantalla hay cuatro opciones: Atkinson, Inter, Source Sans 3 y Noto Sans. Las tres alternativas se descargan una vez por Wi-Fi a la microSD al seleccionarlas, se verifican con SHA-256 y se cargan en PSRAM. Los controles conservan sus dimensiones. Las fuentes de lectura y sus archivos permanecen independientes.
