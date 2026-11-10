# Código del instalador Windows

[English](README.md) | **Español**

Esta carpeta contiene el instalador gráfico, no el proyecto completo del firmware. Para instalar Metalio, descarga el `.exe` preparado en [Releases](https://github.com/Faga250885/Doceink/releases/latest).

## Compilar

Utiliza Windows x64 y Python 3.14.3, como en el entorno de la publicación:

```powershell
.\installer\build.ps1
```

El script crea un entorno local, instala dependencias fijadas, ejecuta las pruebas del instalador y descarga, y genera el ejecutable con PyInstaller. Empaqueta herramientas, arte e información de licencias, nunca firmware. Al instalar, `download.py` obtiene la última versión estable de Faga250885/Doceink y verifica su SHA-256 y manifiesto antes de pasarla a la instalación confirmada.

El paquete de código adjunto a la publicación incluye el instalador y los archivos de código originales de esptool y PyInstaller. Cada dependencia conserva su licencia; el botón Licencias muestra los avisos incluidos. esptool usa GPL-2.0-o-posterior y PyInstaller incluye una excepción para su bootloader. Consulta las licencias originales en esos archivos.

## Pruebas

`test_installer.py` comprueba integridad, validación del chip y memoria, fallos antes de escribir, detección ambigua, cancelación e idiomas. Utiliza esptool simulado: nunca abre un puerto real.

El ejecutable admite estos modos de verificación internos:

```powershell
.\DoceInk-Setup-0.75.149.exe --self-test result.json
.\DoceInk-Setup-0.75.149.exe --smoke-test gui.json
```

Comprueban recursos e interfaz sin enumerar ni abrir puertos serie. No sustituyen una prueba de instalación en hardware.

El instalador realiza una instalación limpia solo después de confirmar Instalar. Las actualizaciones normales por Wi-Fi utilizan la aplicación OTA y conservan los datos del usuario.
