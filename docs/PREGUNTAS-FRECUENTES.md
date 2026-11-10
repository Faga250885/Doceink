# Preguntas frecuentes

[English](FAQ.md) | **Español**

[Volver al inicio](../README.es.md)

### ¿Sirve para cualquier ESP32 o lector de tinta electrónica?

No. El paquete completo está preparado para **Metalio E-Ink4, ESP32-S3 y flash de 16 MB**, con su pantalla y periféricos. No se ha validado para otras placas.

### ¿Se han publicado datos de otra persona dentro del instalador?

El paquete se genera a partir de archivos de compilación; no es una copia de un Metalio en uso. No incluye cuentas, contraseñas Wi-Fi, claves API, conversaciones ni contenido personal del desarrollador. Los enlaces públicos del proyecto y los recursos del sistema sí forman parte del firmware.

### ¿Instalarlo deja también vacía mi microSD?

No. La imagen completa reemplaza la memoria interna, pero no formatea la tarjeta. Usa una tarjeta vacía si quieres un inicio sin datos anteriores. Actualizar normalmente por Wi-Fi también conserva la tarjeta y los ajustes internos.

### ¿Por qué la imagen mide 16 MB si el firmware ocupa menos?

La imagen completa incluye el arranque, las fuentes, los recursos y las regiones vacías. En 0.75.148 la aplicación ocupa 4.989.072 bytes de una partición de 5 MiB. Quedan 253.808 bytes en esa partición; eso no es un espacio de usuario para guardar libros. Los archivos personales se guardan en la microSD.

### ¿Puedo instalar la imagen completa por Wi-Fi?

No. Utiliza `Doceink-EInk4.bin` para la actualización de un sistema existente. `Metalio-instalacion-limpia.bin` se escribe por USB desde el ordenador, siguiendo la guía. No hay que subirlo al actualizador OTA.

### Windows no muestra un puerto COM

Comprueba que el cable permita datos, prueba otro puerto USB y desactiva Disco USB en Metalio. Cierra programas de terminal serie. Si necesitas entrar en modo de descarga, utiliza el botón físico BOOT al reiniciar y vuelve a comprobar qué puerto aparece. Consulta los pasos de [instalación](INSTALACION.md).

### El puerto está ocupado o la conexión expira

Cierra otros programas que utilicen el COM, comprueba que has elegido el correcto y que Metalio está en modo de descarga. Si la conexión es inestable, prueba otro cable y conexión USB directa. Al informar del problema, copia el error de la herramienta.

### Windows muestra un aviso de editor desconocido

El ejecutable todavía no está firmado digitalmente. Descárgalo de la publicación oficial y compara su huella con SHA256SUMS.txt. El método principal no necesita PowerShell ni cambios en la política de ejecución.

### La imagen no supera la comprobación SHA-256

No la instales. Descarga de nuevo el ZIP de la versión indicada y extráelo completo. No mezcles el manifiesto de una versión con la imagen de otra.

### Se ha interrumpido la instalación

No significa necesariamente que Metalio quede inutilizable. Vuelve a entrar en modo de descarga por BOOT, comprueba el puerto y repite la instalación completa. Si no aparece el puerto, revisa cable y alimentación. No cambies de imagen a otra placa para intentar recuperarlo.

### Después de instalar aún aparecen mis conversaciones

Pueden estar en la microSD. El instalador no borra esa tarjeta. Para comenzar sin contenido anterior, retírala o utiliza una vacía, conservando la anterior como respaldo.

### Noticias o Clima están vacíos sin conexión

Cada aplicación necesita una descarga inicial guardada en la microSD. Conecta Wi-Fi, comprueba la fuente RSS o ciudad y pulsa Actualizar. La copia anterior se utiliza en las siguientes aperturas.

### ¿La voz funciona sin internet?

No en esta versión. ChatGPT y el dictado de tareas usan Wi-Fi. Las tareas se guardan localmente y el historial puede consultarse desde la microSD.

### ¿Dónde está el código para compilar?

Este repositorio distribuye firmware y documentación, e incluye el código del instalador Windows en `installer/`. La descarga automática «Source code» de GitHub corresponde al contenido de este repositorio; no sustituye al ZIP de instalación ni contiene el proyecto completo de compilación.

### ¿Cómo informo de un problema?

Abre un [issue](https://github.com/Faga250885/Doceink/issues/new?template=problema.md) con la versión exacta, los pasos y el mensaje de error. Si el problema ocurre al instalar, incluye tu sistema operativo y la salida de esptool. No publiques claves API, contraseñas Wi-Fi ni conversaciones privadas. Puedes adjuntar una foto del error ocultando esos datos.
