DoceInk Setup for macOS — English

Requires macOS 15 or later. Choose arm64 for Apple Silicon (M1 or later),
or x86_64 for an Intel Mac. Python and installation tools are included.

1. Open the DMG and drag DoceInk Setup to Applications.
2. Open DoceInk Setup and connect Metalio with a USB data cable.
3. Detection is automatic: there is no serial-port selector.
4. For the first clean installation, confirm that the current firmware is original
   and keep the backup option enabled. On recognized DoceInk devices, choose
   Update DoceInk or restore a previously saved backup for the same device.

Internet is required. Every installation downloads and verifies the latest
stable firmware from Faga250885/Doceink on GitHub.

Clean installation erases internal accounts and settings, not the microSD.
Wi-Fi updates and the installer USB update preserve existing internal settings.
Restoring replaces current internal data with the saved flash. Backups are
unencrypted and may contain passwords; keep ~/DoceInk/Backups private.
A backup made after DoceInk installation cannot recover original firmware.
Backup, restore and USB update have not yet been validated on physical hardware.
Only Metalio E-Ink4 / ESP32-S3 / 16 MB is supported. If more than one compatible
USB device is connected, disconnect the others; the installer will not guess.

Signing status: this build has an ad-hoc integrity signature, but no Apple
Developer ID signature or notarization. Gatekeeper may block its launch.
No security settings are changed by this package. Do not disable Gatekeeper.
Software and packaged-app tests do not replace a physical USB installation test.

Created by faga12@gmail.com
https://github.com/Faga250885/Doceink

------------------------------------------------------------------------

DoceInk Setup para macOS — Español

Requiere macOS 15 o posterior. Elige arm64 para Apple Silicon (M1 o posterior)
o x86_64 para Mac Intel. Incluye Python y las herramientas de instalación.

1. Abre el DMG y arrastra DoceInk Setup a Aplicaciones.
2. Abre DoceInk Setup y conecta Metalio con un cable USB de datos.
3. Lo detecta automáticamente: no tienes que seleccionar ningún puerto.
4. Para la primera instalación limpia, confirma que el firmware actual sea
   original y deja activado el respaldo. Si ya tiene DoceInk, elige actualizar
   o restaurar un respaldo previamente guardado del mismo Metalio.

Requiere internet. Cada instalación descarga y verifica el firmware estable
más reciente de Faga250885/Doceink en GitHub.

La instalación limpia borra cuentas y ajustes internos, no la microSD.
La actualización Wi-Fi y la actualización USB conservan los ajustes internos.
Restaurar reemplaza los datos internos actuales por los del respaldo. Este no
está cifrado y puede incluir contraseñas: mantén privado ~/DoceInk/Backups.
Un respaldo posterior a instalar DoceInk no recupera el firmware original.
Respaldo, restauración y actualización USB aún requieren prueba física.
Solo admite Metalio E-Ink4 / ESP32-S3 / 16 MB. Si hay varios dispositivos USB
compatibles, desconecta los demás: el instalador no elegirá uno al azar.

Firma: tiene firma ad hoc para verificar integridad, pero todavía no tiene
firma Apple Developer ID ni notarización. Gatekeeper puede impedir abrirlo.
Este paquete no cambia ajustes de seguridad. No desactives Gatekeeper.
Las pruebas de software no sustituyen una instalación USB física.

Creado por faga12@gmail.com
https://github.com/Faga250885/Doceink
