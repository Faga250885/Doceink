# Instalar DoceInk

[English](INSTALLATION.md) | **Español**

[Volver al inicio](../README.es.md)

## Windows: conectar y ejecutar

1. [Descarga DoceInk Setup 0.75.149.1](https://github.com/Faga250885/Doceink/releases/download/v0.75.149/DoceInk-Setup-0.75.149.1.exe).
2. Conecta **Metalio E-Ink4** con un cable USB de datos. Desactiva Disco USB si está activo.
3. Abre el `.exe`. Incluye las herramientas y descarga automáticamente el firmware estable más reciente de GitHub. No necesitas Python ni comandos. Requiere internet.
4. Detecta Metalio automáticamente, sin selector de puertos COM. Si hay varios dispositivos USB compatibles, deja conectado solo el Metalio.
5. Elige **Español** arriba, pulsa **Instalar DoceInk**, confirma y mantén el USB conectado hasta que termine. Metalio se reiniciará.

## macOS: app con detección USB automática

1. Descarga el [DMG para Apple Silicon](https://github.com/Faga250885/Doceink/releases/download/v0.75.149/DoceInk-Setup-0.75.149.1-macOS-arm64.dmg) para M1 o posterior, o el [DMG para Intel](https://github.com/Faga250885/Doceink/releases/download/v0.75.149/DoceInk-Setup-0.75.149.1-macOS-x86_64.dmg). Requiere **macOS 15 o posterior**.
2. Abre el DMG, arrastra **DoceInk Setup** a Aplicaciones y abre la app.
3. Conecta Metalio con un cable USB de datos, con Disco USB desactivado. Detecta la conexión automáticamente: no necesitas terminal, instalar Python ni elegir puertos.
4. Pulsa **Instalar DoceInk** y confirma. Descarga y verifica el firmware estable más reciente de GitHub antes de escribir.

**Firma:** la app tiene una firma ad hoc para comprobar su integridad, pero todavía no tiene firma Apple Developer ID ni notarización. Gatekeeper podría impedir abrirla. Aún no es una distribución notarizada sin avisos; no desactives Gatekeeper. Las compilaciones nativas y las pruebas automáticas no equivalen a una instalación USB física validada.

La versión del instalador **0.75.149.1** es independiente del firmware **0.75.151**. Los instaladores online anteriores también consultan la última publicación en cada instalación.

## Qué pasa con los datos

**Esta es una instalación limpia por USB. Reemplaza la memoria interna y borra cuentas, redes y ajustes del Metalio seleccionado.** Pide confirmación antes de escribir. La microSD no se borra. Usa una tarjeta vacía si también quieres empezar sin libros, tareas ni historiales anteriores.

**Las actualizaciones normales por Wi-Fi conservan los datos del usuario.** Si ya tienes DoceInk y quieres conservar tus ajustes, utiliza [Actualizar](ACTUALIZACIONES.md), no el instalador limpio.

El paquete no contiene cuentas, contraseñas, claves API ni conversaciones personales del desarrollador. Cada usuario configura su propia red y cuentas.

## Requisitos y comprobaciones

- Metalio E-Ink4, ESP32-S3 y **flash de 16 MB**. No está preparado para otras placas.
- Windows 10/11 x64 o macOS 15+ (Apple Silicon o Intel), con cable USB de datos.
- Cada instalación consulta GitHub y descarga su última versión estable. Verifica SHA-256 y manifiesto antes de abrir el puerto USB. No recurre a una versión antigua sin conexión.
- El instalador verifica tamaño y SHA-256 de la imagen, rechaza otros chips ESP y comprueba que la memoria sea de 16 MB antes de escribir. No puede distinguir todas las placas que usan ese mismo chip; conecta únicamente el modelo de Metalio indicado.

[SHA256SUMS.txt](../SHA256SUMS.txt) contiene las huellas de los archivos. El ejecutable todavía no tiene firma digital, por lo que Windows puede mostrar un aviso de editor desconocido o SmartScreen. Descárgalo de la publicación oficial y verifica el archivo si Windows solicita revisarlo; no es necesario cambiar el antivirus.

## Si no detecta Metalio

Pulsa **Ayuda de conexión**. Revisa el cable de datos, desactiva Disco USB y cierra programas que estén usando el puerto serie.

Normalmente se puede entrar automáticamente en modo de descarga. Si tu conexión no lo permite, mantén el botón físico **BOOT** al reiniciar Metalio, suéltalo y reintenta. BOOT es el botón de hardware GPIO0, no el botón rojo táctil de la interfaz. Consulta las instrucciones del fabricante para localizarlo. La detección se actualiza automáticamente, incluso al reconectar. Si cambia la conexión durante la descarga, el instalador se detiene antes de escribir y permite reintentar.

No desconectes el USB mientras escribe. Si falla, muestra detalles y permite reintentar; no informa que terminó correctamente si la operación falló.

## Primer inicio

Metalio debería reiniciarse y mostrar el símbolo con **DoceInk** debajo durante dos segundos antes de la pantalla principal. Si permanece en modo de descarga, reinicia sin mantener BOOT. Sigue los [primeros pasos](PRIMEROS-PASOS.md) para configurar microSD, Wi-Fi y cuentas.

## Instalación avanzada: Linux o recuperación manual

Descarga el [ZIP de imagen completa](https://github.com/Faga250885/Doceink/releases/download/v0.75.151/Metalio-0.75.151-instalacion-limpia.zip) y extráelo. Su imagen se llama `Metalio-instalacion-limpia.bin`. En Windows y Mac normalmente se utiliza el instalador gráfico de arriba.

En una terminal dentro de la carpeta extraída:

```sh
python3 -m venv .venv
source .venv/bin/activate
python -m pip install esptool==4.12.0
```

Comprueba la imagen con `shasum -a 256 Metalio-instalacion-limpia.bin` en macOS o `sha256sum Metalio-instalacion-limpia.bin` en Linux. La huella debe ser:

```text
8cf305cf3c9f65e25dcdf3e5f33b9d84a88e25b8a38fee0c61ca30379fb99b71
```

Sustituye `PUERTO` por el puerto serie real, normalmente `/dev/cu.usbmodem…` en macOS o `/dev/ttyACM…` en Linux. **Este comando escribe directamente y borra los ajustes internos; no muestra la confirmación del instalador de Windows.**

```sh
python -m esptool --chip esp32s3 --port PUERTO --baud 460800 write_flash --flash_mode dio --flash_freq 80m --flash_size 16MB 0x0 Metalio-instalacion-limpia.bin
```

Se utiliza [esptool 4.12.0 de Espressif](https://pypi.org/project/esptool/4.12.0/). Si se deniega acceso al puerto, revisa los permisos del sistema. La instalación desde macOS/Linux no se ha probado físicamente.

## Validación y contenido

La compilación del firmware y las pruebas del arranque, pantalla y entrada táctil pasaron. El instalador 0.75.149.1 tiene dieciséis pruebas automáticas de detección USB, desconexión, cancelación, validación del firmware y descargas. Las comprobaciones de la aplicación empaquetada verifican recursos, interfaz bilingüe y una descarga real sin abrir puertos USB. En macOS también se comprueba el DMG y se monta en modo de solo lectura. **El propietario confirmó una instalación limpia desde Windows en un Metalio físico. Las nuevas funciones requieren prueba física; la instalación USB desde macOS sigue sin validar.**

La imagen completa incluye arranque, particiones, aplicación, fuentes y recursos del sistema. Las regiones NVS, PHY, segunda partición de aplicación y volcados de errores están vacías. Consulta el [manifiesto](releases/v0.75.151-manifest.json).

La imagen mide 16 MB porque incluye espacio vacío. La aplicación ocupa **5.095.824 bytes**. Ni la imagen completa ni el `.exe` sirven como archivo OTA: para actualizar se utiliza `Doceink-EInk4.bin`.
