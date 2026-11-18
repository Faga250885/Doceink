# Actualizar conservando los datos

[English](UPDATES.md) | **Español**

[Volver al inicio](../README.es.md)

Si Metalio ya tiene Doceink instalado, no necesitas repetir la instalación limpia.

1. Conecta Metalio a una red Wi-Fi.
2. Abre **Ajustes → Sistema → Información → Comprobar actualización**.
3. Revisa la versión ofrecida y confirma la actualización.
4. Espera a que termine y se reinicie. Después consulta la versión en Información.

Las actualizaciones normales conservan las cuentas, los ajustes y los archivos de la microSD. La primera instalación limpia por USB sí reemplaza la memoria interna.

## Descargas

- [Última versión publicada](https://github.com/Faga250885/Doceink/releases/latest).
- [Versión documentada 0.75.242](https://github.com/Faga250885/Doceink/releases/tag/v0.75.242).
- [Firmware OTA 0.75.242](https://github.com/Faga250885/Doceink/releases/download/v0.75.242/Doceink-EInk4.bin).

`Doceink-EInk4.bin` es únicamente la aplicación de actualización. No contiene el arranque, la tabla de particiones ni todo el paquete de recursos necesario para empezar desde cero. Para eso utiliza la [guía de instalación limpia](INSTALACION.md).

No utilices `Metalio-instalacion-limpia.bin` en el actualizador Wi-Fi. No intercambies los archivos por tener ambos extensión `.bin`.

## Novedades de 0.75.242

- La barra del reproductor de audiolibros tiene fondo blanco y conserva las medidas estándar: 64 px de alto, 8 px de padding y 8 px hasta la card inferior.
- El botón Biblioteca queda alineado a la izquierda, blanco y con borde negro, con el icono antes del texto. La portada mantiene su superficie blanca sin borde negro.

## Novedades de 0.75.241

- Reproduce M4B y M4A con audio AAC-LC sin DRM, mono o estéreo de 8 a 48 kHz, con pausa y posición guardada. Esta primera implementación no ofrece navegación por capítulos internos ni portadas incrustadas.
- Caché persistente de miniaturas de fondos en la microSD: reutiliza la vista preparada y la regenera al editar, reemplazar o eliminar una imagen.
- Biblioteca de audiolibros sin cabecera: las pestañas Lista/Miniaturas suben y el contenido aprovecha el alto disponible.
- Reproductor sin borde exterior ni contorno negro en la portada. Barra superior con botón blanco Biblioteca sin borde negro a la izquierda, con su icono; elimina el texto sobre standby.
- [Licencia del decodificador AAC](THIRD-PARTY-NOTICES.txt).

## Novedades de 0.75.240

- Nuevo reproductor con diseño Portada: imagen grande sobre un panel punteado, título y capítulo debajo, tiempos separados y controles al pie.
- Botones Pausar/Reanudar y Reiniciar con iconos Lucide; Reiniciar pide confirmación.
- La portada se carga en segundo plano y se adapta al espacio disponible. Cuando falta la imagen se muestra una cubierta con el título.
- El icono superior del reproductor vuelve a la biblioteca. Conserva los controles físicos de volumen, la reproducción en standby y las mejoras de rendimiento de 0.75.239.

## Novedades de 0.75.239

- Conserva en PSRAM los fondos seleccionados de espera y apagado. Se preparan al iniciar y al elegir o editar una imagen; el fondo fijo preparado se muestra sin releer la microSD en ese momento.
- Reemplaza o libera la caché al cambiar, desactivar o eliminar el fondo, y conserva el funcionamiento del carrusel.
- Corrige una espera del reproductor que se convertía en cero con el reloj de tareas del aparato y podía ralentizar la navegación.
- Separa la lectura y decodificación de audiolibros del núcleo de la interfaz, manteniendo la reserva de audio y el punto de pausa de 0.75.238.
- La respuesta de los menús y la continuidad del audio durante standby requieren comprobarse en Metalio tras actualizar.

## Novedades de 0.75.238

- Prepara hasta medio segundo de audio en PSRAM y prioriza salida, conversión y lectura frente al trabajo de imágenes. Conserva la reserva interna DMA anterior.
- Corrige el guardado y lectura de la posición, evitando formatos de 64 bits no admitidos por newlib nano en el aparato.
- El punto de pausa sigue las muestras entregadas a la salida, sin saltar el audio preparado. Se descarta la cola pendiente al pausar.
- La reducción de ruido durante la carga del fondo de standby necesita comprobarse en Metalio.

## Novedades de 0.75.237

- Corrige el envío de audiolibros de 44.100 y 22.050 Hz al conversor de voz, que no admite esas frecuencias y puede provocar un reinicio.
- Convierte el audio a los 16.000 Hz de la bocina con un filtro contra aliasing, conservando la duración y la continuidad entre bloques.
- Protege la ruta de voz contra frecuencias incompatibles. Se mantienen el volumen físico y la reproducción en standby.

## Novedades de 0.75.236

- Nueva aplicación **Audiolibros**, configurable en los iconos del Home: MP3 y WAV PCM de 16 bits en microSD.
- Lista y miniaturas, portadas externas opcionales, capítulos en orden natural, reproducir/pausar y empezar desde el principio con confirmación.
- Posición guardada en microSD y reproducción en segundo plano durante standby. El volumen usa los botones físicos.
- Reduce las tablas de nombres cortos FAT, manteniendo UTF-8 para nombres largos. Pruebas de tildes, chino y cirílico aprobadas.
- [Guía y MP3 de prueba](AUDIOLIBROS.md). Bluetooth y texto sincronizado quedan para más adelante.

## Novedades de 0.75.235

- Reduce los búferes internos de transmisión Wi-Fi de 6 a 3 y usa desde el inicio los 5.760 bytes de DMA de audio compactos, en lugar de 10.240.
- Añade al registro la memoria DMA disponible al trabajar con red y ante fallos de voz.
- El registro del dispositivo confirma un fallo de reserva de memoria para la microSD. Falta validar en Metalio si esta reducción recupera voz y grabación; el fallo DNS de conexión también sigue en observación.

## Novedades de 0.75.234

- Prepara la transferencia Wi-Fi con el trabajador de red reservado y pila interna, en vez de crear una tarea con pila externa.
- La notificación de conexión lista se envía mediante la cola de pantalla sincronizada.
- El fallo de voz y grabación continúa en investigación.

## Novedades de 0.75.233

- Añade códigos de diagnóstico a los errores de conexión/envío de voz y grabación.
- Diferencia saturación de la cola, captura y escritura/sincronización de microSD; la causa del fallo aún está en investigación.

## Novedades de 0.75.232

- Coordina la lectura y escritura sobre el mismo contexto TLS de voz.
- Reintenta correctamente las condiciones temporales de entrada y salida sin bloquear el contexto.

## Novedades de 0.75.231

- Detecta envíos de audio incompletos.

- Recuperación de la sesión de voz al fallar el envío o agotarse la espera.
- Protección para cerrar las ondas si se pierde el evento de soltar el botón.

## Novedades de 0.75.230

Al detener el audio se libera la memoria interna de sus búferes; el micrófono, la grabadora y las alarmas la reservan de nuevo al usarla. Si se cierra ChatGPT, se detienen sus recursos de audio cuando es seguro. La mejora de conexión debe confirmarse en el dispositivo.

## Novedades de 0.75.229

El cierre de una conversación anterior ya no cambia el estado de una nueva; cada sesión libera únicamente su propia reserva de red. ChatGPT inicia los recursos de audio después de conectar con OpenAI y muestra el motivo de error disponible. La corrección requiere confirmación en el dispositivo.

## Novedades de 0.75.228

Corrige un fallo de 0.75.227 que podía detener el Wi-Fi antes de abrir la transferencia de archivos. Se restaura por precaución el procedimiento de conexión anterior.

Cuando falla la descarga de Clima, se muestra un diagnóstico. Los fallos de descarga anteriores a 0.75.227 continúan en investigación.

## Novedades de 0.75.227

La transferencia solicita Wi-Fi automáticamente y ofrece doceink.local con código temporal. El inicio intenta primero la red guardada y busca alternativas si falla. El widget de clima centra la temperatura y ajusta su diseño al volver al Home.

## Novedades de 0.75.226

La galería de fondos abre en una lista sencilla y permite cambiar a la vista de miniaturas. Se mantienen la previsualización y la selección de fondos.

El widget de clima ajusta el espacio para mostrar completa la temperatura, incluso con cifras de distinto ancho. El widget experimental de consumo de IA se retira temporalmente del Home y sus ajustes.

Los accesos que se hubieran guardado previamente en la microSD se conservan; retirar el widget no revoca sesiones ni borra esos archivos.

## Novedades de 0.75.225

Corregido el botón para copiar el comando de vinculación. Si el navegador impide copiar, se muestra el comando para copiarlo manualmente.

## Novedades de 0.75.224

Cuando Consumo de IA no puede iniciar la vinculación, muestra un código para identificar en qué etapa falló.

## Novedades de 0.75.223

La vinculación de Consumo de IA intenta una dirección alternativa si el puerto principal no está disponible, y usa un puerto de control independiente. Si es necesario, muestra la dirección alternativa con `:8765`.

## Novedades de 0.75.222

Vincular Consumo de IA es más sencillo: abre **http://doceink.local** en el PC donde usas Codex o Claude Code, introduce el código de Metalio y pulsa **Copiar comando**. Pégalo en PowerShell para enviar el acceso directamente por Wi-Fi, sin buscar el JSON ni usar Setup. El QR y la IP siguen disponibles, así como la selección manual de archivo.

El nombre local se activa solo durante la vinculación. El enlace sigue siendo temporal y de un solo uso. No cambia el acceso experimental a las cuotas ni añade inicio de sesión de los proveedores. Consulta la [guía](PRIMEROS-PASOS.md#widget-experimental-de-consumo-de-ia).

La tabla de cambio de idioma se genera de forma más compacta, conservando las 1.653 traducciones de cada idioma.

La página de configuración Wi-Fi se guarda comprimida y la descomprime el navegador. El firmware y el paquete integrado de fuentes permanecen en flash interna, sin migrar particiones.

## Novedades de 0.75.221

La vinculación del Consumo de IA ahora usa QR: toca una cuenta, pulsa **Vincular**, escanea desde un teléfono conectado al mismo Wi-Fi y elige su archivo de sesión existente. Se guarda automáticamente en la microSD, se cierra la vinculación y se actualiza el widget. Sin copiar archivos manualmente a la tarjeta ni usar un servidor intermedio.

El enlace temporal funciona una vez, caduca a los 15 minutos y se cierra al salir del modal. Se reemplaza solo la cuenta elegida y se conserva la otra. Se envían únicamente el acceso y el identificador opcional de Codex, sin contraseña, ID token ni refresh token. Usa una red Wi-Fi de confianza. Consulta la [guía](PRIMEROS-PASOS.md#widget-experimental-de-consumo-de-ia).

Esto facilita importar el archivo; no añade inicio de sesión de los proveedores ni garantiza sus cuotas. Se mantienen los límites experimentales de acceso de la 0.75.220.

## Novedades de 0.75.220

Disponible por el actualizador Wi-Fi habitual, también desde la beta 0.75.219. En **Ajustes → Pantalla → Apariencia**, activa por separado Calendario, Clima y el widget experimental de Consumo de IA. Debe quedar al menos uno activo. Los gestos omiten los desactivados, con uno solo no hay puntos y la selección se conserva tras standby y reinicio.

El tipo de batería usa tabs **Icono / Número**. Los tabs dentro de tarjetas blancas tienen un fondo gris con trama y la opción seleccionada negra, también en pantalla monocroma.

El widget opcional de IA consulta directamente por Wi-Fi los porcentajes de cuota de sesión y semana de **Codex con cuenta ChatGPT** y **Claude**, sin servidor ni PC encendido. No cuenta tokens exactos ni garantiza mostrar el consumo de todas las conversaciones de ChatGPT. Para vincularlo, importa los accesos de una sesión existente con la [herramienta local](https://github.com/Faga250885/Doceink/releases/download/v0.75.220/preparar-sesiones.html); consulta las [instrucciones](PRIMEROS-PASOS.md#widget-experimental-de-consumo-de-ia). Los endpoints privados pueden cambiar o rechazar la cuenta, incluida Claude Team. Si la sesión caduca hay que importarla de nuevo. Las cuentas sin vincular no muestran lecturas inventadas.

## Novedades de 0.75.218

Los indicadores del Home ahora son negros: 6 px para el widget activo y 4 px para el inactivo.

Los recordatorios pendientes aparecen junto al reloj. Los de una sola fecha permanecen hasta completarlos y pasan a Hechas; los recurrentes permiten marcar la aparición como vista sin finalizar la serie. Cerrar el aviso no lo descarta. Las tareas siguen guardándose en la microSD.

La lista de subrayados muestra el capítulo y la fecha y hora de guardado debajo de cada cita. Las citas antiguas sin fecha conservan sus datos y muestran un guion. Los modales tienen esquinas redondeadas y eliminar requiere confirmación.

El menú de lectura Avanzada agrupa Subrayados e Índice, sustituye los grandes botones del pie de página por casillas compactas y reúne orientación y limpieza de tinta dentro de Pantalla. Conserva el estilo de los botones y todas las opciones.

Validación: 111 pruebas locales aprobadas, incluidos renderizado nativo, avisos y errores de guardado, metadatos y confirmación de borrado, y distribución del menú. La prueba física en Metalio queda pendiente de instalar.

## Novedades de 0.75.217

El Home recuerda el widget elegido, Calendario o Clima, después del standby, apagado y reinicio. Ambos indicadores de página son grises: el activo mide 6 px y el inactivo 4 px.

La tarjeta del clima aprovecha el alto liberado, con padding de 16 px y contenedores gris y blanco redondeados. La temperatura principal muestra solo el número. Se eliminan el horario duplicado, el separador y el resumen de máximas/mínimas. Tocar cualquier parte del bloque gris abre Clima; deslizar sigue cambiando de widget.

La hora de la última actualización guardada aparece a la izquierda de Actualizar. Ambos forman un único control transparente, sin fondo ni borde. Se puede tocar cualquiera de las dos partes y ambas se atenúan mientras descargan. La hora proviene del pronóstico guardado: se conserva si falla una descarga y permite reintentar.

Validación: las 109 pruebas locales aprobaron, incluidos renderizado RGB y de un bit, zonas táctiles combinadas, reintentos, lectura de la hora, tamaño de indicadores y restauración del widget elegido. La confirmación física queda pendiente de instalar.

## Novedades de 0.75.216

El icono del clima actual tiene su propio contenedor blanco dentro del panel gris punteado. Ocupa el ancho y alto disponibles de su columna y mantiene el icono centrado. Ambos contenedores tienen esquinas redondeadas. Se conserva la separación de 16 px entre temperatura y horario.

Validación: las 109 pruebas locales aprobaron, incluidos renderizado nativo, límites y esquinas de los paneles, centrado, gestos sobre el contenedor blanco y reintentos de actualización. La confirmación física queda pendiente de instalar.

## Novedades de 0.75.215

El icono del clima actual, la temperatura y el horario comparten un contenedor redondeado con la trama gris punteada original del Home. El panel ocupa el espacio entre el encabezado y el pronóstico, conservando los márgenes laterales del calendario. La separación visual entre la temperatura y el horario aumenta de 8 a 16 px.

Validación: 109 pruebas locales aprobadas, incluidos renderizado nativo, límites y trama del panel, espaciado, gestos y reintentos de actualización. La confirmación física queda pendiente de instalar.

## Novedades de 0.75.214

Clima de hoy en el Home comparte los márgenes laterales y la alineación del encabezado del Calendario. Se elimina la ciudad y se amplían el icono y la temperatura del tramo actual de dos horas, con el horario más cerca. Una sola fila muestra el pronóstico cada dos horas; debajo quedan la máxima y mínima del día completo.

El icono de actualizar, inmediatamente a la izquierda del acceso a Clima, conecta el Wi-Fi y guarda el pronóstico actualizado en la microSD. Muestra Actualizando mientras trabaja, evita descargas duplicadas y permite reintentar tras errores de conexión o almacenamiento. Un fallo conserva el último pronóstico guardado.

Validación: las 109 pruebas locales aprobaron, incluidos renderizado nativo, encabezados alineados, gestos, reintentos y manejo de errores. La confirmación física queda pendiente de instalar.

## Novedades de 0.75.213

La tarjeta superior del Home cambia entre Calendario y Clima de hoy al deslizar a los lados. En Calendario, deslizar arriba o abajo cambia de mes. Clima muestra el resumen del día, la ciudad, un icono grande y la temperatura del tramo actual de dos horas, máximas/mínimas y las 24 horas del pronóstico. El icono superior derecho abre Clima.

Al tocar el encabezado del calendario se abren selectores de mes y año. El botón comienza como Ir al mes actual y cambia a Ir al mes seleccionado cuando eliges otra fecha.

El widget usa el pronóstico guardado y recarga la caché local en segundo plano al cambiar de día; no abre Wi-Fi en cada gesto. Abre Clima para actualizar el pronóstico o elegir una ciudad.

Validación: 109 pruebas locales aprobadas, incluidos gestos reales, accesos sin activaciones accidentales, mes/año, horas del pronóstico, resumen diurno, unidades, datos ausentes, reintentos de caché e iconos grandes nativos. La confirmación física queda pendiente de instalar.

## Novedades de 0.75.212

Los iconos de las aplicaciones del Home miden 50 × 50 píxeles y ya no tienen una base blanca adicional detrás. Vuelve el logo original de ChatGPT, escalado proporcionalmente al nuevo tamaño. Las tarjetas mantienen sus medidas, separación y nombres.

Validación: 107 pruebas locales aprobadas, incluida la creación y reconstrucción real de las ocho tarjetas y el renderizado de iconos sobre blanco/negro, en color y monocromo. La confirmación física queda pendiente de instalar.

## Novedades de 0.75.211

Todos los iconos de las aplicaciones del Home usan Lucide, con la misma escala y grosor que Libros. ChatGPT usa el icono de asistente de Lucide. Las variantes del clima, el editor del Home y el selector comparten el conjunto. Los iconos van integrados en su tamaño de pantalla para actualizar por Wi-Fi.

Validación: 106 pruebas locales aprobadas, incluidos todos los iconos y las variantes del clima sobre blanco y negro, en color y monocromo. La confirmación física queda pendiente de instalar.

## Novedades de 0.75.210

La pantalla inicial de dictado ya no muestra un campo vacío. El campo aparece al pulsar Escribir tarea o al revisar el texto dictado. Su texto queda centrado verticalmente y alineado a la izquierda, también al abrir el teclado. Las listas siguen sin franja del contador.

Validación: 105 pruebas locales aprobadas, incluidos el momento de mostrar el campo, la alineación original y con teclado, el dictado y el guardado. La confirmación física queda pendiente de instalar.

## Novedades de 0.75.209

La creación de tareas muestra siempre arriba un campo con borde, durante el dictado, la revisión y la edición. Tocar el campo vacío del dictado abre el editor con teclado; el texto dictado se puede corregir directamente antes de guardar. Se elimina la franja adicional del contador en Por hacer y Hechas.

Validación: 105 pruebas locales aprobadas, incluida la escritura con el teclado real y el guardado del texto corregido. La confirmación física queda pendiente de instalar.

## Novedades de 0.75.208

El teclado numérico escribe directamente en el campo original de día, mes o año. Solo muestra números y un icono de retroceso: sin texto de rango, campo duplicado ni fila de aceptar/cancelar. Se cierra con el botón rojo o tocando fuera. Guardar cambios valida y guarda la fecha; las fechas incompletas o inválidas no se pueden guardar.

Validación: 105 pruebas locales aprobadas, incluido el teclado real dentro del editor de tareas. La confirmación física queda pendiente de instalar.

## Novedades de 0.75.207

El Home pinta una base blanca opaca bajo su trama para cubrir los controles de la pantalla anterior en los espacios y esquinas entre tarjetas. Se conserva la distribución y los iconos.

## Novedades de 0.75.206

La fecha se edita con tres campos en una misma fila: día, mes y año. Cada uno abre un teclado solo numérico con teclas grandes, borrar, aceptar, cancelar y validación de rangos. Dos acciones de modal siguen en una fila; tres o más se apilan y ocupan todo el ancho.

## Novedades de 0.75.205

El selector de fecha no tiene título, usa selección de borde redondeado sin relleno y responde sin animaciones ni inercia. Sin fecha oculta Repetición. Las acciones son Completar, Editar y Eliminar; Agregar tarea es negro. Se retiran encabezados de modales. El lector usa solo gestos, incluidas las preferencias antiguas, y las instrucciones tienen ilustraciones más claras y alineadas.

## Novedades de 0.75.204

Las fechas de tareas incluyen el día de la semana. El editor compacto elimina Tipo y usa un tab Con fecha / Sin fecha. Un único campo con icono de calendario abre día, mes y año con scroll; el selector solo tiene Guardar y Cancelar. Las acciones de confirmación comparten una fila: confirmar o activar a la izquierda, cancelar o desactivar a la derecha.

## Novedades de 0.75.203

El dictado detecta días de la semana, fechas relativas o explícitas y repeticiones semanales, mensuales o anuales. Una fecha detectada abre una confirmación con Crear tarea y Editar información; editar abre el formulario completo. Por hacer y Hechas sustituyen a Personal/Trabajo y al filtro adicional, conservando las tareas de ambas listas. Las fechas usan el reloj local y se pueden revisar antes de guardar.

## Novedades de 0.75.202

Alinea el mes y el acceso a Tareas con las columnas del calendario y ajusta el icono de Tareas a 34 × 34 píxeles.

## Novedades de 0.75.201

Corrige el logo de DoceInk en Información del sistema. La imagen reducida se muestra a su tamaño nativo.

## Novedades de 0.75.200

El acceso a Tareas del calendario es el propio icono pulsable, sin contenedor de botón, borde, fondo ni texto. Tiene el alto del texto del mes y queda alineado a la derecha. Tocarlo abre la misma aplicación de Tareas.

Validación: 104 pruebas locales aprobadas y compilación para ESP32-S3. La comprobación física queda pendiente de instalar esta versión.

## Novedades de 0.75.199

El calendario marca con contorno negro punteado los días con tareas pendientes con fecha o cumpleaños, incluidas las repeticiones de Personal y Trabajo. Hoy conserva el fondo negro. Mantener pulsado un día vibra y muestra una confirmación; solo al aceptar se abre la creación para esa fecha. El logo de DoceInk vuelve dentro de la tarjeta de Información, encima de la versión y un 20% más pequeño. Se retira Icono con porcentaje: quedan Solo icono y Solo número; la preferencia antigua pasa a Solo icono.

## Novedades de 0.75.198

El acceso a Tareas del calendario muestra solo su icono, sin texto, borde ni fondo. Conserva una zona cómoda para tocarlo y deja más espacio al mes. Tocar el icono abre la misma aplicación de Tareas.

Durante la selección del libro, el texto queda en negro con letras blancas; al guardar queda solo el subrayado. La lista de subrayados no tiene título ni botón Cerrar y se cierra con el botón rojo. Las filas con fragmentos largos se abren tocando cualquier parte del texto o de la fila.

## Novedades de 0.75.197

Calendario y Tareas unidos en una sola aplicación, con dictado, fechas, repeticiones y cumpleaños en microSD. Guardar tareas reutiliza un trabajador reservado para evitar asignar otra pila de RAM interna. Tareas sale de la cuadrícula y queda junto al mes. Subrayado sobre la página original y entre páginas; lista de subrayados con detalle y eliminación. Avanzada, Instrucciones en modal y espaciado de 8 px. Micrófono de ChatGPT bloqueado hasta estar listo, con indicación y flecha. Iconos de Home alineados y trama continua en Ajustes bloqueado.

Validación: 104 pruebas locales aprobadas y compilación para ESP32-S3. La comprobación física queda pendiente de instalar esta versión en Metalio.

## Novedades de 0.75.196

Nuevos atajos de lectura: deslizar hacia arriba abre el menú y hacia abajo abre las secciones del libro. Mantén pulsada una palabra para abrir el selector de subrayado con esa palabra marcada; después toca la última y guarda. Sustituye al doble toque. Los toques de las zonas táctiles vuelven a responder sin espera. Ayudas y bienvenida ilustrada actualizadas.

## Novedades de 0.75.195

Doble toque sobre una palabra mientras lees para iniciar el subrayado; toca la última palabra en el diálogo de selección y guarda. Funciona con gestos y zonas táctiles sin pasar de página con el primer toque. Subrayar ya no se bloquea por el cálculo de capítulos en segundo plano. El texto del libro no se traduce con la interfaz.

## Novedades de 0.75.194

Corregida una recarga insegura de preferencias introducida en la 0.75.193 que podía reiniciar Metalio al abrir un libro. La apertura, el cierre y la restauración de ajustes usan ahora los valores predeterminados en memoria. Además, Comprobar actualización y Ver cambios comparten el tamaño estándar de botón de 64 px.

## Novedades de 0.75.193

Capítulo actual resaltado en el índice. Ajustes por libro, tres perfiles de lectura, grosor del texto y espacio entre párrafos independientes. Subrayado con dos toques y pasajes guardados en la microSD. Iconos nítidos en el editor de Home y trama diagonal en la tarjeta de Ajustes bloqueada.

Validación: 100 pruebas locales superadas, incluidos ajustes por libro y perfiles, subrayado con dos toques en ambos sentidos, fallo con microSD exportada, grosor de letra, anclajes tras repaginar EPUB y capítulo actual en un índice de 8.000 entradas. Firmware ESP32-S3 compilado. Queda pendiente la verificación en el dispositivo físico.

## Novedades de 0.75.192

- Reordenados los ajustes según las tareas habituales. Pantalla abre primero Fondos, seguida de Home y Apariencia. La galería, el carrusel de espera y los fondos dinámicos quedan juntos. Batería, tipografía del sistema y refresco se agrupan en Apariencia.

- Sistema separa Energía, General, Reloj e Información. Energía muestra primero los tiempos de suspensión y apagado, y después la espera de ahorro de Wi-Fi. General mantiene idioma y vibración. Se conservan los valores elegidos.

- Archivos muestra primero la transferencia por Wi-Fi y Disco USB, seguidos del estado y capacidad de la microSD. Conexiones conserva Wi-Fi antes de Bluetooth, con las acciones antes de los textos de ayuda.

- Reloj sitúa la configuración automática y manual antes de la explicación detallada. Información muestra versión, comprobación de actualización y notas primero, después los datos técnicos y al final el logo y los créditos.

- Las ayudas usan un estilo secundario más pequeño, los tabs se mantienen en una línea y se conserva el funcionamiento de selectores, temporizadores y barras de scroll.

Validación: 97 pruebas locales superadas, incluidos cambios repetidos entre Fondos y Apariencia en los tres idiomas, callbacks tardíos y salida mientras se aplica una fuente. Firmware ESP32-S3 compilado. Queda pendiente la comprobación en el aparato físico.

## Novedades de 0.75.191

- Tipografía del sistema queda limitada a cuatro familias: Atkinson, la predeterminada original, Inter, Source Sans 3 y Noto Sans. Las fuentes generales de lectura ya no aparecen en este selector.

- Al actualizar desde la 0.75.190 se restaura Atkinson. Las futuras elecciones de fuentes de interfaz se guardan por separado de la preferencia anterior.

- Sustituido el escalado de imágenes y la negrita artificial por rasterización nativa con FreeType para 16 combinaciones de tamaño y peso, con regular y seminegrita reales. Cada combinación encaja en el espacio original; las letras no se estiran ni se reducen después de dibujarse.

- Los tres paquetes opcionales son independientes de las fuentes de lectura, incluyen sus licencias y se descargan únicamente al seleccionarlos. El campo muestra conexión y porcentaje. Se comprueban el tamaño y SHA-256 antes de instalar.

- El paquete elegido queda en PSRAM con el archivo cerrado: sigue disponible con Disco USB o al retirar la tarjeta. Atkinson funciona sin microSD ni Wi-Fi. Si un cambio falla se conserva la fuente anterior. Los caracteres ausentes y los signos grandes que excedan el espacio usan el respaldo interno original.

- Comprobadas métricas y mapas de píxeles de los tres paquetes en las 16 combinaciones, alineación de mayúsculas, acentos, números, archivo retirado y fallos de almacenamiento, red y memoria.

Validación: 96 pruebas locales superadas. Firmware ESP32-S3 compilado; aplicación de 5.211.904 bytes. Queda pendiente la comprobación en el aparato físico.

## Novedades de 0.75.190

- Añadida Tipografía del sistema en Ajustes → Pantalla. Permite elegir Atkinson, la fuente interna predeterminada, o una fuente de lectura guardada en la microSD. El texto del libro conserva su configuración independiente.

- La interfaz mantiene las alturas tipográficas, el tamaño de los controles y los iconos. Los caracteres que falten utilizan el respaldo interno latino/chino.

- La fuente se carga en PSRAM antes de aplicarse y se cierra el archivo de la tarjeta. La interfaz sigue dibujándose al activar Disco USB o retirar la microSD. Aplicar una fuente descargada no necesita Wi-Fi.

- La elección se conserva tras reiniciar. Si falta el archivo al arrancar, se utiliza la tipografía interna. Si un cambio falla se conserva la fuente anterior; se puede volver a Atkinson sin microSD.

- Verificadas las 30 familias del catálogo, varios tamaños y pesos de interfaz, el dibujo sin el archivo original y los fallos de almacenamiento, USB, memoria y tareas.

Validación: 96 pruebas locales superadas; firmware ESP32-S3 compilado y archivos verificados contra la compilación. Queda pendiente comprobar el nuevo control en el dispositivo físico.

## Novedades de 0.75.189

- El registro confirmó unos 5 KB de RAM interna libre y un mínimo de 0 KB, pese a unos 7 MB libres de PSRAM. Las asignaciones compatibles del sistema, Wi-Fi y TCP/IP ahora priorizan PSRAM; DMA y tareas del sistema conservan la memoria interna que necesitan.

- La tarea táctil se pausa y se reanuda en standby, en lugar de destruirse y crearse de nuevo. Despertar ya no necesita reservar otra pila táctil de 4 KB después de que Wi-Fi use RAM interna. Probados 1.000 ciclos de reactivación con la creación de tareas forzada a fallar.

- Una descarga de fuente interrumpida ya no muestra el mismo check que una familia completa. Los tamaños guardados siguen disponibles sin internet. Usa Descargar tamaños restantes o el icono de descarga para completar la familia sin cambiar la fuente elegida. Al cerrar el catálogo se actualizan las flechas de tamaño.

- Comprobados los siete tamaños, en ambos sentidos, de las 30 familias del catálogo, incluida Raleway. La recuperación contempla una fuente que solo conserva el archivo de 18 px.

- Las fuentes reutilizan un cliente HTTPS para la licencia y los siete tamaños. Si una petición falla, se descarta el cliente antes del reintento. Se reducen las asignaciones repetidas de TLS y las conexiones.

- Clima usa el trabajador de red reservado al iniciar, en lugar de crear una tarea por actualización. Ahora solicita encender el Wi-Fi cuando hace falta. Su cliente HTTP también se libera si falla una asignación de memoria.

- Al cerrar los ajustes de lectura de la biblioteca se libera su fuente cuando ya se han eliminado las etiquetas de la muestra.

- Corregida una condición del wallpaper de standby: si termina una carga antigua después de volver a entrar, la nueva pantalla inicia su propia carga en lugar de quedarse con el logo. Los fallos al reservar memoria para la imagen se gestionan conservando la selección del wallpaper.

## Novedades de 0.75.188

- El standby espera a que termine la carga del wallpaper antes de poder cortar la alimentación de los periféricos. Las descargas activas conservan alimentación, Wi-Fi y CPU; la suspensión y el carrusel esperan a que termine la transferencia.

- La descarga de fuentes prueba la escritura en su propia carpeta, crea las carpetas ausentes y elimina su archivo de prueba. Las comprobaciones de otras carpetas no rechazan una carpeta de fuentes escribible. Se conserva el error original al crear directorios.

- Los fallos temporales de red reintentan una vez el archivo afectado. Se conservan los archivos ya verificados. Los errores indican la operación y el código para distinguir almacenamiento, HTTP, respuestas incompletas y firma incorrecta.

- Comprobados los 240 archivos publicados: tamaños y firmas SHA-256 coinciden con el catálogo. Falta confirmar en Metalio la corrección del fallo intermitente.

## Novedades de 0.75.187

- La lista de tipografías utiliza exclusivamente la letra de la interfaz. Se eliminan las muestras por fila, su carga de archivos y su temporizador. La fuente elegida se muestra solo en el texto de ejemplo de lectura.

- Las flechas recorren las fuentes instaladas y la integrada. Nunca abren la lista ni inician descargas. Solo el campo central con nombre y chevron abre el catálogo completo.

- Corregido el cambio de fuente en los ajustes de lectura abiertos desde la biblioteca sin un libro activo. Se eliminan las etiquetas antiguas antes de reemplazar su fuente, tanto en la muestra como en el lector activo.

- Los cambios rápidos de preferencias comparten un único trabajador de guardado que agrupa los cambios, en lugar de crear una tarea y una pila por toque. Se conserva el último valor de cada ajuste.

- Las descargas comprueban el sistema de archivos real y coordinan el acceso con Disco USB. Un indicador de montaje desactualizado ya no rechaza una tarjeta accesible. Los errores distinguen archivos ausentes o inválidos, tarjeta inaccesible, llena, de solo lectura u ocupada y acceso por USB.

Validación: compilación y 88 pruebas aprobadas, incluidos 1.000 cambios agrupados de fuente, muestra sin libro abierto, cambios repetidos con flechas sin abrir el catálogo y comprobación de acceso a almacenamiento y USB. Falta confirmar el bloqueo en Metalio; no se dispuso de un registro USB. La OTA conserva los datos y los instaladores descargan la última versión estable.

## Novedades de 0.75.186

- El campo entre las flechas utiliza ahora la letra normal de la interfaz: solo nombre y chevron, sin muestra de la fuente ni carga tipográfica desde la microSD.

- Seleccionar una fuente local utilizable ya no exige los siete tamaños del catálogo ni inicia una descarga porque falten otros tamaños. El archivo local se comprueba antes de aplicarlo.

- La descarga lee el cierre de las respuestas HTTP por bloques antes de comprobar que estén completas. Se mantienen las verificaciones de tamaño y SHA-256.

- Solo se permite una descarga activa. Las filas bloquean los toques repetidos y su vibración mientras trabajan, y vuelven a habilitarse al terminar. Los fallos muestran el error concreto de tarjeta, conexión o descarga.

- Las muestras de nombres se retiran de las etiquetas antes de liberar su memoria al cerrar el modal o iniciar una descarga. Se pausan durante las descargas para reducir memoria y actividad de la microSD.

- Corregido el scroll de regreso en contenido estático, como Sistema → Información. Las superficies con contenido desplazable reciben los gestos aunque sus textos o tarjetas no sean botones. La corrección compartida cubre ambos sentidos en vertical y horizontal, sin activar superficies que no tengan desplazamiento.

- Retirada la subsección duplicada ChatGPT de Ajustes → Sistema. Su configuración sigue disponible dentro de la aplicación ChatGPT.

Validación: compilación y 86 pruebas de software aprobadas, incluidas familias locales incompletas, cierre HTTP por bloques, toques repetidos, fallos y 100 ciclos de cierre del modal con muestras. Falta verificar estas correcciones en Metalio; todavía no se ha capturado la causa exacta del bloqueo reportado. La OTA conserva los datos y los instaladores obtienen la última versión estable.

## Novedades de 0.75.185

- La descarga muestra Buscando Wi-Fi, Conectando, Descargando con porcentaje y Verificando dentro de la fila pulsada. Los fallos dejan un mensaje para reintentar. Se solicita la conexión de forma explícita, con un tiempo de espera de 30 segundos.

- La barra avanza mientras llegan los datos de toda la familia y su licencia; solo llega al 100% tras verificar los archivos.

- El modal de tipografías pasa a ser una lista continua con separadores inferiores, sin tarjetas redondeadas y con scrollbar visible. Elegir una fuente pendiente con las flechas abre su lista de descarga.

- Las muestras de nombres tienen un alto compacto independiente del tamaño de lectura: hasta 26px de altura de línea en el campo central y 30px en la lista. Se conservan los archivos originales y el tamaño elegido para leer.

Validación: se descargaron los siete archivos de Cabin desde GitHub y coinciden con sus copias publicadas. Compilación y 86 pruebas de software aprobadas. Falta verificar en el dispositivo. La OTA conserva los datos y el instalador descarga el último firmware estable.

## Novedades de 0.75.184

- Mantén pulsada la lectura para abrir el menú. Desliza hacia arriba o abajo para abrir el índice; los gestos horizontales pasan páginas. La bienvenida y los textos de Controles explican estos gestos.

- Tipografía reutiliza el inventario de la microSD y conserva la vista previa al cambiar de pestaña.

- Pulsa el campo central de la fuente para abrir un modal con scroll, sin título ni botón Volver. Nombres a la izquierda e iconos Lucide de descarga o instalada a la derecha. La descarga muestra su progreso dentro de la fila. Los nombres instalados usan su propia fuente mediante muestras pequeñas que liberan los archivos de la tarjeta al cargarse.

- Se retiran Gestionar tipografías e Importar. Las EF se detectan automáticamente; las TTF/OTF nuevas en fonts_ttf se convierten a 25px en segundo plano al iniciar, sin Wi-Fi ni reemplazar las EF existentes.

- Nuevo espaciado entre letras, de -1 a 4px, bajo el tamaño. Se guarda y se aplica al cálculo de líneas, paginación, justificación y selección. Las iniciales biónicas tienen un nivel menos de grosor.

- Actualización de pantalla utiliza un único control de pestañas Automático/Manual.

- Pantalla → Home reproduce la cuadrícula de ocho accesos. Permite elegir la app de cada posición editable; Configuración permanece fija y desactivada abajo a la derecha.

Validación: compilación del firmware y 86 pruebas de software aprobadas. Falta validar estos cambios en el aparato. La OTA por Wi-Fi conserva los datos. Los instaladores de Windows y Apple Silicon descargan el último firmware estable.

## Novedades de 0.75.183

- Notas de actualización en Información: cambios de la versión instalada y la anterior, traducidos y disponibles sin internet.
- El reloj muestra Configurando... mientras trabaja, con texto blanco legible sobre el botón negro.
- La justificación reparte el ancho sobrante entre palabras, respeta el final de párrafo y conserva la selección y el texto original. Las iniciales biónicas quedan más marcadas.
- Catálogo de 30 familias: solo se descarga la elegida a la microSD, con siete tamaños y su licencia OFL. Se verifica SHA-256 y se conserva la fuente actual si falla. Las guardadas funcionan sin internet.
- El paquete tipográfico interno de instalación limpia pasa de 4.985.431 a 2.585.690 bytes. Se mantienen todos los caracteres originales y los bitmaps conservados, incluidos los símbolos matemáticos. El contenido completo con firmware y recursos ocupa unos 8,29 MB frente a 10,66 MB en 0.75.182. La imagen completa sigue midiendo 16 MB porque incluye las zonas vacías.
- La OTA por Wi-Fi conserva los datos y la partición de fuentes anterior. El instalador limpio incluye el paquete interno reducido. Se conservan las fuentes existentes de la microSD.
- Compilación y 81 pruebas de software aprobadas. Falta la validación física de estos cambios.

## Novedades de 0.75.182

- Los capítulos conservan la alineación izquierda y quedan centrados verticalmente por ítem; el scrollbar permanece visible.
- Los ajustes del lector aparecen sobre un texto de muestra traducido y los elementos seleccionados del pie de lectura, conservando la posición del libro.
- El reloj detecta ciudad aproximada y zona IANA por Wi-Fi, sincroniza fecha y hora y gestiona el horario de verano; la fecha, hora y desfase UTC manuales se editan en un modal.
- Se retira Suspender con contadores: los contadores activos siempre utilizan el comportamiento compatible con standby.
- Terminar partida se alinea justo debajo del tablero.
- Compilación y pruebas de software pertinentes aprobadas. Falta validar estos cambios en el aparato.

## Novedades de 0.75.158

- Elige Celsius o Fahrenheit en los ajustes de Clima; la selección se aplica al pronóstico y a la tarjeta del Home usando los datos guardados sin conexión.
- Compilación y prueba automatizada de Clima aprobadas. Falta verificar en Metalio.

## Novedades de 0.75.157

- La probabilidad de precipitación por hora se muestra hasta 99 % para mantenerla en una línea.

## Novedades de 0.75.156

- Se reduce la memoria interna temporal al guardar fuentes RSS y comprobar actualizaciones.

## Novedades de 0.75.155

- La frecuencia de CPU configurada para standby ya no ralentiza la interfaz durante el uso normal sin conexión. El valor guardado de 80/160/240 MHz se aplica cuando standby está visible; al grabar audio y durante las transiciones de despertar se mantiene la velocidad normal.
- Se conservan la preferencia y los datos personales. Cuando corresponde, standby utiliza sueño ligero, que detiene el reloj de la CPU; el ahorro real todavía no se ha medido.
- Compilación y 65 pruebas automáticas aprobadas. Falta verificar en Metalio el standby, el despertar y la grabación.

## Novedades de 0.75.154

- Corrige la interfaz inmóvil en modo manual. Las actualizaciones parciales siguen mostrando las interacciones; la limpieza completa periódica se pospone hasta pulsar el botón del micrófono. Algunas transiciones del sistema, como standby y apagado, todavía pueden realizar una actualización completa.
- Pasan las 64 pruebas automáticas, incluida una que comprueba que las actualizaciones parciales continúan en modo manual. Queda pendiente verificarlo en Metalio.

## Novedades de 0.75.153

- La configuración inicial de Noticias aparece debajo de su toolbar desde la primera apertura. No solicita Wi-Fi al entrar; al pulsar Configurar noticias se conecta y genera el QR.
- Ajustes → Pantalla → Pantalla permite elegir actualización automática o manual. En modo manual, pulsa una vez el botón del micrófono para refrescar la pantalla. La elección se conserva al reiniciar.
- Compilación y 64 pruebas automáticas aprobadas. El modo manual y la configuración inicial de Noticias todavía requieren verificación en un Metalio físico.

## Novedades de 0.75.152

- Grabadora local: acceso desde la toolbar a las grabaciones identificadas por fecha y hora, reproducción local y borrado con confirmación. Pausa/reanudar y detener aparecen lado a lado. Un indicador avisa de la grabación en la topbar y en standby. El icono del Home usa el micrófono de Lucide.
- Los estados iniciales de Noticias y ChatGPT conservan la topbar y la toolbar, con el mensaje en la tarjeta de contenido.
- Pasan 64 pruebas automáticas, incluida la validación WAV y los estados del indicador. Falta verificar en Metalio la reproducción, el borrado, standby y la apariencia de las pantallas de configuración.

## Novedades de 0.75.151

- Corregido el reinicio al comprobar actualizaciones con Wi-Fi desconectado. Verificado en Metalio.

## Novedades de 0.75.150

- Wi-Fi se conecta bajo demanda, sin conexión automática al encender ni al volver a Home. Las acciones que requieren internet pueden solicitar conexión.
- Nueva Grabadora local: WAV mono de 16 kHz directamente en microSD, pausa y reanudación, grabación durante standby, confirmación al detener y opción de guardar o descartar. Mantén pulsado un acceso del Home y elige Grabadora para añadirla.
- El progreso del lector corresponde a todo el libro. Los capítulos pendientes ya no cuentan como una sola página; la estimación provisional se sustituye al terminar la paginación. La barra tiene un píxel más de alto y se actualiza el porcentaje guardado para Biblioteca.
- ChatGPT aprovecha el alto disponible con 8 px inferiores. El micrófono se bloquea mientras responde o reproduce audio. El historial es de solo lectura y muestra un aviso al intentar enviar voz.
- Configuración inicial de ChatGPT y Noticias centrada, con títulos grandes en negrita y botones negros. El modal de cerrar sesión se ajusta al contenido.
- Nuevo logo en el arranque y en Información, con dos segundos de presentación. Botones de Biblioteca con altura de 64 px y texto de 22 px.
- Las portadas evitan ampliar imágenes de baja resolución y usan una conversión monocroma sin trama ordenada ni el refresco lento de dos pasadas de grises.
- Inglés predeterminado al instalar desde cero. Revisión de los catálogos inglés, español y chino simplificado y de las páginas de vinculación y transferencia. OTA conserva el idioma y los datos del usuario.

Validación: pasan las 64 pruebas automáticas, compila el firmware ESP32-S3 y la imagen limpia tiene verificadas sus regiones de datos personales vacías. Firmware: 5.112.960 bytes; quedan 147.056 bytes en su partición OTA de 5 MiB. La grabación durante standby y el aspecto de las portadas requieren prueba física. El propietario confirmó previamente la instalación limpia desde Windows; la instalación USB desde macOS sigue sin validar en hardware.
