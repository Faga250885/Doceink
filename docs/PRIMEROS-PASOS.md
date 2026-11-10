# Primeros pasos

[English](GETTING-STARTED.md) | **Español**

[Volver al inicio](../README.es.md)

## Controles básicos

- **Botón rojo, un toque:** retroceder una pantalla; desde una conversación abierta en el historial, volver al historial.
- **Botón rojo, pulsación prolongada:** volver a Home.
- **Mantener pulsado un icono de Home:** abrir el selector para cambiar esa aplicación. Tocar fuera o usar el botón rojo cierra el selector.
- **Deslizar:** mover las listas o cambiar de contenido en las pantallas que lo permiten. La vibración confirma el gesto realizado.

La pantalla de tinta electrónica tiene refrescos visibles. Un parpadeo durante un refresco completo no significa por sí solo que Metalio se haya reiniciado.

## Conectar Wi-Fi

En **Ajustes → Conexiones → Wi-Fi**, busca tu red y completa su conexión. El ESP32-S3 utiliza redes Wi-Fi de **2,4 GHz**. Necesitarás internet para descargar noticias y clima, iniciar conversaciones y usar el dictado.

## microSD y archivos

La microSD guarda libros, fondos, fuentes, tareas, historiales y contenido descargado. Una instalación limpia de firmware no vacía la tarjeta. Para un inicio sin contenido anterior, utiliza una microSD vacía compatible con Metalio.

El sistema organiza los datos bajo `metalio/e-ink/` en la tarjeta. Algunas ubicaciones son:

| Ruta en la microSD | Contenido |
| --- | --- |
| `metalio/e-ink/books/` | Libros |
| `metalio/e-ink/wallpaper/` | Fondos |
| `metalio/e-ink/fonts/` | Tipografías de lectura en formato `.ef` |
| `metalio/e-ink/fonts_ttf/` | Archivos TTF/OTF para el proceso de importación; no son equivalentes a una fuente `.ef` ya convertida |
| `metalio/e-ink/recordings/` | Grabaciones WAV locales |
| `metalio/e-ink/chat_log/` | Historial de conversaciones |
| `metalio/e-ink/personal_tasks.json` | Tareas personales |
| `metalio/e-ink/work_tasks.json` | Tareas de trabajo |
| `metalio/e-ink/weather.json` | Pronóstico descargado |
| `metalio/e-ink/rss_*.xml` | Cachés de las fuentes RSS |

No necesitas editar manualmente esos archivos de datos para usar las aplicaciones.

### Transferir desde el teléfono por Wi-Fi

1. Conecta el teléfono y Metalio a la misma red Wi-Fi.
2. Inserta la microSD y desactiva Disco USB si está activo.
3. En **Ajustes → Archivos**, abre **Transferir archivos por Wi-Fi**.
4. Escanea el QR y abre el enlace en el navegador.
5. Navega por las carpetas, carga archivos o descarga los existentes. En un ordenador también puedes arrastrar archivos al área de carga.
6. Cierra la transferencia en Metalio al terminar. El enlace es temporal.

El QR abre el gestor de la microSD de ese Metalio. No es un servicio de almacenamiento en la nube ni el instalador del firmware.

### Copiar por USB

Activa **Disco USB** en Ajustes → Archivos. Copia los archivos desde el ordenador y expulsa la unidad antes de desactivar ese modo. Mientras está activo, Metalio no utiliza la microSD de la misma forma que durante su funcionamiento normal.

## Libros

Carga tus libros en `books/` y ábrelos desde la biblioteca. La portada permite continuar la lectura. Los ajustes de lectura ofrecen controles de página, tamaño y tipografía.

## Noticias y clima

Añade una URL de feed RSS válida; la dirección de una página principal no siempre es un feed. Puedes guardar varias fuentes y elegirlas desde el selector.

En Clima, configura tu ciudad. Pulsa **Actualizar** para descargar datos por primera vez. Después, las dos secciones muestran las copias guardadas en la microSD y se actualizan al pulsar refrescar. Sin una copia previa no hay contenido para mostrar sin internet.

## ChatGPT y tareas

Configura tu propia clave API desde los ajustes de ChatGPT. El paquete no incluye una cuenta compartida. Comprueba que tu cuenta tenga acceso al servicio que vas a utilizar.

Una conversación nueva necesita internet. El historial guardado en la microSD se puede abrir para consultar conversaciones sin conexión. El envío de voz está bloqueado en el historial; inicia una conversación nueva para enviar mensajes.

Tareas ofrece dos listas **Personal** y **Trabajo**, guardadas localmente. El dictado utiliza Wi-Fi; esta versión no ofrece reconocimiento de voz sin conexión. No necesitas Jira.

## Grabadora local

Mantén pulsado un acceso del Home y selecciona **Grabadora**. Inserta la microSD y desactiva Disco USB; pulsa **Empezar a grabar**. El audio se escribe durante la grabación en un WAV temporal de la tarjeta, sin Wi-Fi, clave API ni servicios externos. Puedes pausar y reanudar. La grabación continúa durante standby; despierta Metalio y vuelve a Grabadora para detenerla. Confirma Detener y elige Guardar en microSD o No guardar. Los archivos quedan en `metalio/e-ink/recordings/`. La aplicación graba sonido; no transcribe la voz.

Wi-Fi permanece desconectado al arrancar hasta que lo conectes o uses una función que lo necesite, como Actualizar, dictar o iniciar una conversación. Abrir Noticias, Clima o historial guardados no solicita conexión. El idioma predeterminado al instalar desde cero es inglés; puedes elegir español o chino simplificado en Ajustes. OTA conserva tu elección.
