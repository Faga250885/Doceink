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
- [Versión documentada 0.75.182](https://github.com/Faga250885/Doceink/releases/tag/v0.75.182).
- [Firmware OTA 0.75.182](https://github.com/Faga250885/Doceink/releases/download/v0.75.182/Doceink-EInk4.bin).

`Doceink-EInk4.bin` es únicamente la aplicación de actualización. No contiene el arranque, la tabla de particiones ni todo el paquete de recursos necesario para empezar desde cero. Para eso utiliza la [guía de instalación limpia](INSTALACION.md).

No utilices `Metalio-instalacion-limpia.bin` en el actualizador Wi-Fi. No intercambies los archivos por tener ambos extensión `.bin`.

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
