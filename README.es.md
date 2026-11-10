# DoceInk · Metalio

[English](README.md) | **Español**

Firmware para **Metalio E-Ink4**, el lector de tinta electrónica con ESP32-S3 y memoria flash de 16 MB. Libros, tareas locales, ChatGPT por voz, noticias RSS, clima, reloj, calculadora y juegos en una misma interfaz.

**Versión documentada: 0.75.148.** Este repositorio reúne descargas y documentación para instalar y utilizar Metalio.

## Instalar desde cero

### [Descargar para Windows — conecta Metalio y ejecuta](https://github.com/Faga250885/Doceink/releases/download/v0.75.148/DoceInk-Setup-0.75.148.exe)

**Conecta Metalio → abre el `.exe` → pulsa Instalar.** Sin Python, comandos ni descargar el firmware por separado. Se abre en inglés y permite cambiar a español.

Sigue la **[guía de instalación paso a paso](docs/INSTALACION.md)**. Incluye requisitos, instalación por USB desde Windows, alternativa para macOS/Linux y cómo resolver problemas de conexión.

El paquete se genera con los archivos del firmware y sus recursos: **no incluye cuentas, claves API, redes Wi-Fi guardadas, conversaciones ni archivos personales del desarrollador**. Cada persona configura su propio Metalio.

> La instalación limpia reemplaza la memoria interna del Metalio de destino y borra sus cuentas y ajustes. **No borra la microSD.** Usa una tarjeta vacía si también quieres empezar sin libros, tareas o historiales anteriores.
>
> Estado de validación: compilación, pruebas de software, integridad del ZIP y regiones vacías de la imagen verificadas. La instalación completa desde cero todavía no se ha validado en un Metalio físico.

## Elegir la descarga correcta

| Quiero… | Archivo o método | Qué ocurre con mis datos |
| --- | --- | --- |
| Instalar desde cero en un Metalio compatible | `DoceInk-Setup-0.75.148.exe`, por USB | Reemplaza toda la memoria interna; conserva la microSD |
| Actualizar un Metalio que ya utiliza Doceink | Ajustes → Sistema → Información → Comprobar actualización | Conserva cuentas, ajustes y archivos |
| Obtener el firmware de actualización | `Doceink-EInk4.bin` en Releases | Es la aplicación OTA, no un instalador completo |

**No uses `Metalio-instalacion-limpia.bin` para actualizar por Wi-Fi.** Tampoco basta con copiar ese archivo a la microSD: se instala por USB siguiendo la guía.

- [Última publicación y descargas](https://github.com/Faga250885/Doceink/releases/latest)
- [Actualizar conservando los datos](docs/ACTUALIZACIONES.md)
- [Huellas SHA-256 de 0.75.148](SHA256SUMS.txt)
- [Historial de versiones](https://github.com/Faga250885/Doceink/releases)

## Qué incluye

Al encender, el icono de DoceInk aparece centrado con **DoceInk** debajo durante dos segundos antes de la pantalla principal.

| Sección | Funciones |
| --- | --- |
| Libros | Biblioteca, portadas, lectura y controles de tipografía |
| Tareas | Listas locales Personal y Trabajo; dictado por Wi-Fi |
| ChatGPT | Conversaciones por voz e historial en microSD; requiere configurar tu propia clave API |
| Noticias | Varias fuentes RSS, caché en microSD y actualización manual |
| Clima | Pronóstico guardado en microSD y actualización manual |
| Reloj | Reloj, pomodoro, cronómetro y cuenta atrás |
| Archivos | Disco USB y transferencia por Wi-Fi desde el navegador del teléfono mediante QR |
| Home y ajustes | Accesos personalizables, fondos, batería, conexión y preferencias |
| Otras aplicaciones | Calculadora y juegos |

Las conversaciones nuevas y el dictado necesitan conexión a internet y la configuración correspondiente. Los historiales y datos ya guardados se consultan desde la microSD. Noticias y Clima necesitan una primera descarga para tener contenido disponible sin conexión.

## Empezar a usarlo

1. Instala el firmware y arranca Metalio.
2. Inserta tu microSD y configura tu red Wi-Fi de 2,4 GHz.
3. Añade tus libros y fondos desde **Ajustes → Archivos**.
4. Configura tus propias fuentes RSS, ciudad y, si vas a usar ChatGPT, tu clave API.

Consulta la [guía de primeros pasos](docs/PRIMEROS-PASOS.md) para conocer los controles, las carpetas y la transferencia de archivos.

## Compatibilidad y ayuda

Este instalador está preparado **exclusivamente para Metalio E-Ink4, ESP32-S3, flash de 16 MB**. No es un firmware universal para cualquier lector o placa ESP32.

- [Preguntas frecuentes y solución de problemas](docs/PREGUNTAS-FRECUENTES.md)
- [Informar un problema](https://github.com/Faga250885/Doceink/issues/new?template=problema.md)
- [Licencia incluida con el firmware](LICENSE)

El firmware se apoya en ESP-IDF, LVGL y otros componentes de terceros, que conservan sus respectivas licencias. La licencia principal no sustituye las de esos componentes.

Creado por faga12@gmail.com
