# Código del instalador de escritorio

[English](README.md) | **Español**

Esta carpeta contiene el instalador gráfico para Windows y macOS, no el proyecto completo del firmware. Descarga el `.exe` o el `.dmg` correspondiente a tu Mac en [Releases](https://github.com/Faga250885/Doceink/releases/latest). El instalador 0.75.149.1 detecta el USB automáticamente y no tiene selector de puertos.

## Compilar

Utiliza Windows x64 y Python 3.14.3, como en el entorno de la publicación:

```powershell
.\installer\build.ps1
```

El script crea un entorno local, instala dependencias fijadas, ejecuta las pruebas del instalador y descarga, y genera el ejecutable con PyInstaller. Empaqueta herramientas, arte e información de licencias, nunca firmware. Al instalar, `download.py` obtiene la última versión estable de Faga250885/Doceink y verifica su SHA-256 y manifiesto antes de pasarla a la instalación confirmada.

Para macOS, compila directamente en macOS 15+ con Python 3.14.3 y Tkinter:

```sh
python3 -m venv installer/.venv
source installer/.venv/bin/activate
python -m pip install -r installer/requirements-lock.txt
python installer/build_macos.py
```

Genera una `.app` dentro de un DMG para Apple Silicon o Intel. Comprueba recursos, interfaz bilingüe, descarga real y el DMG montado en modo de solo lectura. Ninguna prueba abre puertos serie. [Build desktop installers](../.github/workflows/installers.yml) compila en ambos tipos de Mac y en Windows mediante GitHub Actions con permisos de lectura. La publicación se realiza después, por separado.

La app de macOS tiene firma ad hoc de integridad. **No se ha configurado firma Apple Developer ID ni notarización**; no se garantiza su aceptación por Gatekeeper. Consulta las [notas del paquete](MACOS.md). El instalador Windows tampoco tiene firma digital.

El paquete de código adjunto a la publicación incluye el instalador y los archivos de código originales de esptool y PyInstaller. Cada dependencia conserva su licencia; el botón Licencias muestra los avisos incluidos. esptool usa GPL-2.0-o-posterior y PyInstaller incluye una excepción para su bootloader. Consulta las licencias originales en esos archivos.

## Pruebas

`test_installer.py` comprueba integridad, chip y memoria, fallos antes de escribir, detección automática y desconexión, alias de macOS, varios dispositivos, cancelación e idiomas. Utiliza esptool simulado: nunca abre un puerto real. `test_download.py` comprueba selección de la última versión, integridad y paquetes incorrectos.

El ejecutable admite estos modos de verificación internos:

```powershell
.\DoceInk-Setup-0.75.149.1.exe --self-test result.json
.\DoceInk-Setup-0.75.149.1.exe --smoke-test gui.json
.\DoceInk-Setup-0.75.149.1.exe --download-test download.json
```

Comprueban recursos e interfaz sin enumerar ni abrir puertos serie. No sustituyen una prueba de instalación en hardware.

Solo el modo de prueba de descarga admite `DOCEINK_TEST_GITHUB_TOKEN` para evitar límites de servidores CI compartidos. Ese token temporal se envía únicamente a la API de GitHub, no se propaga en redirecciones ni se incluye en la aplicación. La interfaz normal no lo requiere.

El instalador realiza una instalación limpia solo después de confirmar Instalar. Las actualizaciones normales por Wi-Fi utilizan la aplicación OTA y conservan los datos del usuario.
