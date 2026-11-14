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
- [Versión documentada 0.75.190](https://github.com/Faga250885/Doceink/releases/tag/v0.75.190).
- [Firmware OTA 0.75.190](https://github.com/Faga250885/Doceink/releases/download/v0.75.190/Doceink-EInk4.bin).

`Doceink-EInk4.bin` es únicamente la aplicación de actualización. No contiene el arranque, la tabla de particiones ni todo el paquete de recursos necesario para empezar desde cero. Para eso utiliza la [guía de instalación limpia](INSTALACION.md).

No utilices `Metalio-instalacion-limpia.bin` en el actualizador Wi-Fi. No intercambies los archivos por tener ambos extensión `.bin`.

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
