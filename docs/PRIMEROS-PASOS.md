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
| `metalio/e-ink/agenda.json` | Tareas personales/de trabajo, fechas y repeticiones |
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

## Calendario y tareas compartidas

Los iconos de las aplicaciones del Home miden 50 × 50 píxeles, sin una base adicional detrás. Usan Lucide, excepto ChatGPT, que conserva su logo original escalado proporcionalmente. Las variantes del clima siguen el mismo tamaño.

La tarjeta superior del Home ofrece Calendario, Clima de hoy y Consumo de IA experimental: desliza a los lados para cambiar entre los widgets activos. El Home recuerda la selección tras standby y reinicio. En Calendario, desliza arriba o abajo para cambiar de mes o toca el encabezado para elegir mes y año. Los indicadores son negros y el widget activo tiene el punto más grande; se ocultan si solo queda uno.

Clima muestra solo el número de temperatura y un icono grande en paneles redondeados, con una fila de pronóstico cada dos horas debajo. Toca el bloque gris para abrir Clima. La hora guardada y el icono de actualizar comparten un control transparente arriba a la derecha: toca cualquiera para conectar el Wi-Fi y actualizar el pronóstico en la microSD. Ambos se atenúan mientras descargan. Cambiar de widget usa la copia guardada sin iniciar una descarga. Abre Clima para elegir una ciudad.

El mes aparece a la izquierda del calendario y el icono de **Tareas** a la derecha, con el alto del texto del mes y sin contenedor de botón, texto, borde ni fondo. Tocar el icono abre la aplicación de Tareas. Tareas ya no ocupa ni puede elegirse en los ocho accesos inferiores; los accesos antiguos se sustituyen por una aplicación disponible sin duplicar las demás.

Los días con tareas pendientes con fecha o cumpleaños tienen un contorno negro punteado y redondeado, sin relleno; se incluyen las tareas repetidas. Hoy conserva su fondo negro. Mantén pulsado un día: Metalio vibra y pregunta si quieres agregar una tarea. Solo al aceptar se abre la misma aplicación para empezar el dictado con esa fecha; Cancelar o el botón rojo cierran la pregunta. Desliza arriba o abajo en Calendario para cambiar de mes. También puedes crear desde **Agregar tarea**, por micrófono o escritura. La pantalla inicial de dictado no tiene campo de texto. Pulsa Escribir tarea para abrir el editor, o dicta y revisa el texto reconocido en su campo editable. El texto queda centrado verticalmente y alineado a la izquierda, también con el teclado abierto. Por hacer y Hechas muestran la lista directamente debajo de las pestañas, sin franja de contador. El dictado puede detectar la fecha y la repetición; después permite Crear tarea o Editar información. Manualmente puedes elegir sin fecha o con fecha y una repetición: una sola vez, diaria, semanal, mensual o anual. Para cumpleaños utiliza repetición anual. El tab Con fecha / Sin fecha controla la fecha; los tres campos de día, mes y año abren un teclado solo numérico que escribe directamente en el campo elegido. Ciérralo con el botón rojo o tocando fuera y usa Guardar cambios en el formulario para validar y guardar la fecha. Editar permite cambiar el título, fecha y repetición; eliminar pide confirmación.

Las tareas se guardan en `metalio/e-ink/agenda.json` en la microSD. Las listas anteriores se incorporan al primer guardado y sus archivos originales se conservan. Al completar una tarea repetida, avanza a la siguiente fecha posterior a hoy; las mensuales conservan el día original y usan el último día de los meses más cortos. No se crean copias de cada repetición. Límite: 256 tareas en total. Esta agenda no añade alarmas ni notificaciones de vencimiento.

## Apariencia del Home

En **Ajustes → Pantalla → Apariencia → Widgets del Home**, activa Calendario, Clima o Consumo de IA por separado. Debe quedar al menos uno activo; con uno solo no se muestran los puntos. El Home recuerda los widgets activos y el último seleccionado tras standby y reinicio. La batería se elige con tabs **Icono / Número**. Los tabs dentro de tarjetas blancas tienen fondo gris con trama.

## Widget experimental de consumo de IA

Actualiza normalmente por Wi-Fi a **0.75.220**. Para instalar el firmware no necesitas la herramienta ni USB. Vincular las cuentas es un paso independiente:

1. Descarga [preparar-sesiones.html](https://github.com/Faga250885/Doceink/releases/download/v0.75.220/preparar-sesiones.html) y ábrelo localmente en un navegador.
2. Selecciona el archivo `auth.json` de una sesión existente de Codex (normalmente `.codex/auth.json`) y/o `.credentials.json` de Claude Code (normalmente `.claude/.credentials.json`). Deben existir previamente en tus aplicaciones con sesión iniciada. La herramienta no extrae accesos del almacén del sistema ni de cookies del navegador. Usa solo cuentas que tengas autorización para vincular.
3. Exporta `ai_usage-auth.json` y cópialo a **`metalio/e-ink/` en la microSD**. La herramienta funciona localmente sin subir los archivos seleccionados. El archivo exportado contiene accesos reales con sus permisos originales: mantenlo privado y no lo envíes por chat.
4. Activa **Consumo de IA** en Apariencia, entra a su widget del Home y toca Actualizar. Metalio consulta a los proveedores directamente por Wi-Fi, sin servidor intermedio ni ordenador encendido.

Las barras muestran **porcentajes de cuota** de sesión y semana, no tokens exactos. La lectura de OpenAI corresponde a Codex con cuenta ChatGPT y no garantiza el total de todas las conversaciones de ChatGPT. Claude Team u otras cuentas pueden devolver un error de acceso: son endpoints privados experimentales, no una integración pública garantizada. Si caduca la sesión debes importarla nuevamente; no se renuevan credenciales automáticamente. El refresco automático funciona cada 15 minutos mientras el widget está visible, además del refresco manual.

Toca un proveedor para actualizarlo o desvincularlo. Desvincular elimina su acceso local de la microSD y su lectura, sin revocar la sesión de la aplicación original. Las claves y los saldos de la API son independientes de este widget.

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

## Tipografías y notas de actualización

En Tipografía del lector encontrarás 30 familias. Las que indican Descargar necesitan Wi-Fi y la microSD montada, con Disco USB desactivado. Al elegir una se guarda con tamaños de 18, 22, 24, 25, 28, 30 y 36 px para reutilizarla sin internet. La fuente integrada está disponible sin tarjeta. Se mantiene la importación de TTF/OTF personalizados.

En Ajustes → Sistema → Información → Notas de actualización puedes consultar sin Wi-Fi los cambios de la versión instalada y la anterior.

Desliza hacia arriba para el menú, hacia abajo para las secciones y a los lados para pasar páginas. Mantén pulsada una palabra para iniciar el subrayado sobre la página original. Pulsa el nombre de la fuente entre las flechas para abrir el modal: el icono de descarga indica que falta instalarla y el check que sus tamaños del catálogo están guardados; el progreso aparece dentro de su fila. Los nombres usan la letra de la interfaz; la fuente elegida se muestra solo en el texto de ejemplo de lectura. Ajusta Espaciado entre letras debajo de Tamaño de letra. Para añadir TTF/OTF locales, cópialas a `metalio/e-ink/fonts_ttf/` y reinicia Metalio: las EF de 25px que falten se convierten en segundo plano, sin Wi-Fi. Las EF en `metalio/e-ink/fonts/` se detectan automáticamente.

Las descargas de fuentes muestran el estado de conexión Wi-Fi, porcentaje y verificación dentro de la fila; pulsa una fila con error para reintentar. El selector utiliza una lista continua con separadores y scrollbar visible. Las muestras de nombres conservan un tamaño compacto, independiente del tamaño de lectura.

El campo entre las flechas muestra el nombre con la letra de la interfaz y un chevron. Una fuente local utilizable se puede elegir sin internet aunque falten otros tamaños del catálogo. Solo puede ejecutarse una descarga a la vez; las filas desactivan temporalmente los toques y su vibración mientras trabajan. Si falla, aparece el error de tarjeta, conexión o descarga.

Los nombres de la lista usan la letra normal del sistema. La fuente elegida se muestra solo en el texto de ejemplo de lectura, también al abrir los ajustes desde la biblioteca sin un libro activo. Las flechas recorren las fuentes instaladas; solo el campo central con nombre y chevron abre el catálogo descargable.

La descarga comprueba que se puede escribir en la carpeta de fuentes antes de conectar. El standby conserva la alimentación mientras carga el wallpaper o descarga fuentes. Un fallo temporal de red reintenta una vez el archivo actual; si persiste, la notificación incluye la operación y el código. Se conservan los archivos ya verificados.

Cada familia del catálogo puede incluir siete tamaños: 18, 22, 24, 25, 28, 30 y 36 px. El check indica una familia completa. Una descarga interrumpida puede dejar tamaños locales utilizables: pulsa el nombre para usarlos sin internet, o el icono de descarga / Descargar tamaños restantes para completar la familia. Al cerrar el catálogo se actualizan las flechas de tamaño. Clima solicita conectar el Wi-Fi y comparte el trabajador de red reservado al iniciar con fuentes, noticias y actualizaciones.

## Tipografía del sistema

Abre **Ajustes → Pantalla → Apariencia → Tipografía del sistema**. Hay exactamente cuatro familias: **Atkinson** (la predeterminada original integrada), **Inter**, **Source Sans 3** y **Noto Sans**. Estas opciones son independientes del catálogo de 30 fuentes del lector y de las fuentes importadas para leer.

Atkinson funciona siempre sin tarjeta ni Wi-Fi. Al seleccionar otra familia se descarga una sola vez a la microSD su paquete específico de interfaz. El selector muestra conexión y porcentaje; desactiva Disco USB para la primera descarga. Se verifican tamaño y SHA-256 y después se puede usar sin internet. Los paquetes contienen regular y seminegrita reales para las 16 combinaciones de interfaz, dibujadas a tamaños nativos, sin reescalar imágenes de las letras de lectura.

El paquete queda cargado en PSRAM y su archivo se cierra: la interfaz sigue disponible al retirar la tarjeta o activar Disco USB. Se mantienen las dimensiones de controles y los iconos Lucide. Los caracteres ausentes usan el respaldo latino/chino original y la tipografía del libro sigue configurándose aparte. Al actualizar desde la 0.75.190 se vuelve a Atkinson. Las nuevas elecciones se conservan al reiniciar; si falta el paquete al arrancar, está disponible Atkinson sin iniciar una descarga automática.

Consulta [fuentes originales, licencias y preparación](../assets/system-fonts/v1/README.md).

## Ajustes organizados por tarea

| Grupo | Orden y ubicación |
|---|---|
| Pantalla | Primero Fondos (galería, carrusel y fondos dinámicos), después la cuadrícula de Home y al final Apariencia (widgets, batería, tipografía del sistema y refresco). |
| Conexiones | Primero Wi-Fi y después el modo y las acciones de Bluetooth; las ayudas siguen a sus controles. |
| Archivos | Transferencia por Wi-Fi, Disco USB y después estado y capacidad de la microSD. |
| Sistema | Energía (suspensión, apagado y espera de Wi-Fi), General (idioma y vibración), Reloj (automático y manual), Información (versión, actualización y notas, datos técnicos y créditos). |

Se conservan los valores elegidos. Cada sección permite scroll y al cambiar se cierran sus selectores anteriores y se detienen sus temporizadores de pantalla.

## Ajustes de lectura, perfiles y subrayados

Cada libro conserva sus preferencias de página y tipografía en la microSD. Los libros sin ajustes propios heredan los predeterminados. En el menú del lector, **Páginas** incluye espacio independiente entre párrafos, tres perfiles de lectura y acciones para usar los ajustes actuales como predeterminados o restaurar los predeterminados para ese libro. Guarda un perfil antes de aplicarlo a otro libro. Su tipografía debe estar instalada.

**Tipografía** agrega grosor Normal, Medio y Grueso, independiente de las iniciales biónicas y el espaciado entre letras. El índice resalta el capítulo actual en negro y se abre en ese capítulo.

Para guardar un subrayado, **mantén pulsada la primera palabra en la página del libro** y toca la última. La selección se dibuja con fondo negro y letras blancas sobre la misma página, con el mismo texto, posiciones y pie de lectura. Al guardar queda solo el subrayado. Puedes pasar páginas deslizando a los lados y continuar la selección, incluso entre capítulos. Al elegir la última palabra aparecen **Guardar subrayado** y **Cancelar**; tocar de nuevo la primera palabra cancela la selección. Se admite seleccionar en orden inverso. **Avanzada → Subrayados** abre una lista desplazable sin título ni botón Cerrar; se cierra con el botón rojo. Tocar cualquier parte de una fila, también si el texto está truncado, abre el fragmento completo en un modal con **Eliminar** y **Cerrar**. El botón para empezar a subrayar se ha retirado del menú. **Avanzada → Instrucciones** muestra la guía ilustrada de gestos. Los anclajes sobreviven a cambios de fuente y repaginación; las páginas de imagen no permiten seleccionar texto. Ajustes y subrayados se guardan junto al libro: conserva sus archivos asociados si lo mueves o renombras. La selección mantiene una copia temporal acotada de las páginas visitadas; una selección excesivamente larga muestra un aviso sin truncar silenciosamente lo guardado.

El editor de Home usa iconos de 48 px y una trama diagonal en la tarjeta fija de Ajustes. Esa tarjeta permanece abajo a la derecha y no se puede reasignar.

ChatGPT: al iniciar una conversación, el micrófono permanece bloqueado durante «Conectando con ChatGPT». Cuando está listo, el primer mensaje indica mantener pulsado el micrófono para preguntar y muestra una flecha a la derecha. Una pulsación iniciada antes de estar listo no comienza a grabar automáticamente al terminar la conexión.

En Información, el logo de DoceInk está dentro de la tarjeta, sobre la versión, con un tamaño un 20% menor. La batería ofrece Solo icono o Solo número (con %). El antiguo modo Icono con porcentaje pasa automáticamente a Solo icono.

La navegación táctil usa únicamente gestos. Se eliminan las zonas táctiles y su configuración, también para preferencias guardadas anteriormente. Mantener una palabra y tocar la última sigue permitiendo subrayar.

Los avisos pendientes se muestran junto al reloj: tócalos para ver la tarea. Completar una tarea de una sola fecha la envía a Hechas. Marcar como visto un recordatorio recurrente oculta solo esa aparición; vuelve en la siguiente fecha. Cerrar mantiene el aviso pendiente.

En Avanzada, las casillas de Pie de página controlan cada dato de forma independiente. Pantalla reúne orientación y frecuencia de limpieza. Los subrayados muestran capítulo y fecha/hora de guardado; los antiguos sin fecha muestran un guion. Eliminar siempre pide confirmación y Cancelar conserva la cita.
