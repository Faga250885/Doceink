# Instalación limpia de Metalio

[Volver al inicio](../README.md)

Esta guía corresponde a **0.75.145**. La instalación escribe una imagen completa de 16 MB en la memoria interna; no requiere compilar el firmware.

## Antes de empezar

Necesitas:

- Un **Metalio E-Ink4 con ESP32-S3 y flash de 16 MB**.
- Un ordenador y un cable USB que transmita datos.
- Python con el lanzador `py` en Windows, o `python3` en macOS/Linux.
- El [ZIP de instalación limpia](https://github.com/Faga250885/Doceink/releases/download/v0.75.145/Metalio-0.75.145-instalacion-limpia.zip).
- Una microSD vacía para empezar también sin contenido anterior. El instalador no formatea tarjetas.

**La instalación borra las cuentas, redes y ajustes de la memoria interna del Metalio elegido.** Copia antes los archivos de la microSD que quieras conservar. Puedes retirar la tarjeta durante la instalación. Si vuelves a insertar una tarjeta con conversaciones o tareas anteriores, el sistema podrá mostrarlas de nuevo.

Si ya utilizas Doceink y quieres conservar tus ajustes, utiliza la [actualización normal](ACTUALIZACIONES.md).

> La imagen y el instalador se han comprobado en software. La instalación completa en un Metalio físico sigue pendiente de validación. La escritura depende también del cable, el puerto y la conexión del equipo.

## 1. Descargar y extraer

Descarga el ZIP desde el enlace anterior o desde [Releases](https://github.com/Faga250885/Doceink/releases/tag/v0.75.145) y extrae su contenido en una carpeta.

Debe contener:

| Archivo | Para qué sirve |
| --- | --- |
| `Metalio-instalacion-limpia.bin` | Imagen completa del sistema, con las zonas de datos internos vacías |
| `Instalar.ps1` | Instalador para Windows; comprueba el archivo y pide confirmación |
| `manifest.json` | Modelo compatible, tamaños y huellas SHA-256 |
| `LEEME.txt` | Instrucciones disponibles sin conexión |
| `LICENSE` | Licencia principal incluida con el firmware |

El ZIP de esta versión mide **5.755.002 bytes**. Su SHA-256 es:

```text
fd87c1bd35b889833b71fa2ccfcf69bec5377b93d2730cba576de82ca5595211
```

En Windows puedes comprobarlo con:

```powershell
Get-FileHash .\Metalio-0.75.145-instalacion-limpia.zip -Algorithm SHA256
```

## 2. Preparar Windows

Instala Python desde [python.org](https://www.python.org/downloads/windows/) con su lanzador `py`. Abre PowerShell y ejecuta:

```powershell
py --version
py -m pip install esptool==4.12.0
py -m esptool version
```

Usamos [esptool 4.12.0, publicado por Espressif](https://pypi.org/project/esptool/4.12.0/), para que los comandos coincidan con los del instalador.

Conecta Metalio por USB. En el Administrador de dispositivos de Windows, identifica su puerto, por ejemplo **COM5**. Cierra programas que estén utilizando ese puerto. Si Metalio tiene activado **Disco USB**, desactívalo: ese modo sirve para copiar archivos a la microSD, no para instalar el firmware.

## 3. Instalar

Abre PowerShell en la carpeta donde extrajiste el ZIP. Sustituye `COM5` por el puerto de tu Metalio:

```powershell
.\Instalar.ps1 -Port COM5
```

Si PowerShell bloquea la ejecución del script, revisa su contenido y ejecútalo solo para este proceso con:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\Instalar.ps1 -Port COM5
```

El instalador comprueba el tamaño y SHA-256 de la imagen. Te pedirá escribir **INSTALAR** antes de escribir en el Metalio. Espera hasta que termine; no desconectes el cable durante la escritura.

Si no logra conectar automáticamente, mantén pulsado el botón físico **BOOT** al reiniciar Metalio para entrar al modo de descarga; después suéltalo. BOOT es el botón de hardware asociado a GPIO0, no el botón rojo táctil de la interfaz. Comprueba de nuevo el puerto COM, porque puede cambiar, y repite el comando. Consulta también las indicaciones del fabricante de tu unidad para acceder a BOOT.

## 4. Primer inicio

Cuando la escritura y su verificación terminen, Metalio debería reiniciarse. Si permanece en modo de descarga, reinícialo sin mantener BOOT.

Inserta tu microSD y sigue los [primeros pasos](PRIMEROS-PASOS.md). Configura tu propia red y cuentas. No hay ninguna clave API ni cuenta del desarrollador precargada.

## Alternativa: macOS o Linux

En una terminal dentro de la carpeta extraída, crea un entorno para la herramienta:

```sh
python3 -m venv .venv
source .venv/bin/activate
python -m pip install esptool==4.12.0
```

Comprueba la huella de la imagen completa antes de escribir. En macOS:

```sh
shasum -a 256 Metalio-instalacion-limpia.bin
```

En Linux:

```sh
sha256sum Metalio-instalacion-limpia.bin
```

Debe ser:

```text
c2fed1efad31383bd1d6204e87291546f3a529279b77c3c8b38f54ddda1a79cf
```

Identifica el puerto USB de Metalio: suele tener forma `/dev/cu.usbmodem…` en macOS o `/dev/ttyACM…` en Linux. Sustituye `PUERTO` por el puerto real. **Este comando escribe directamente y borra los ajustes internos; no pide la confirmación del script de Windows.**

```sh
python -m esptool --chip esp32s3 --port PUERTO --baud 460800 write_flash --flash_mode dio --flash_freq 80m --flash_size 16MB 0x0 Metalio-instalacion-limpia.bin
```

Esta alternativa utiliza la misma imagen y herramienta; no se ha probado físicamente desde macOS/Linux. Si el sistema deniega acceso al puerto, revisa los permisos de acceso a dispositivos serie de tu distribución.

## Qué se instala y qué se deja vacío

La imagen contiene el arranque, la tabla de particiones, la aplicación, el paquete de fuentes, recursos gráficos y recursos de audio del sistema. Se crea a partir de archivos de compilación, no de una copia de la memoria de un usuario.

Las regiones NVS (cuentas y configuración), datos PHY, segunda partición de aplicación y volcados de errores se entregan vacías. [Manifiesto de esta versión](releases/v0.75.145-manifest.json).

La imagen completa mide 16 MB porque también incluye el espacio vacío. La aplicación ocupa **4.985.120 bytes**, no los 16 MB completos. Esta imagen **no se puede utilizar como actualización OTA**.
