# Audiolibros en Metalio

Usa **0.75.244 o posterior** para los controles de retroceder y adelantar 15 segundos, el porcentaje con dos decimales y la barra blanca estándar con Biblioteca a la izquierda. Conserva la portada sin contorno y M4B/M4A de 0.75.241.

Disponible desde **0.75.236**. La primera versión reproduce **MP3** y **WAV PCM de 16 bits**, mono o estéreo, entre 8 y 48 kHz. Para empezar recomendamos MP3: ocupa mucho menos espacio que WAV. Los archivos deben estar en la microSD, sin protección DRM. Desde **0.75.241** también admite **M4B y M4A con AAC-LC**, mono o estéreo de 8 a 48 kHz, sin DRM y menores de 2 GB. No admite HE-AAC, ALAC ni MP4 fragmentado. Un M4B se reproduce como una sola pista: todavía no se muestran sus capítulos internos ni su portada incrustada.

## Añadir la aplicación al Home

Mantén pulsado un icono configurable del Home y elige **Audiolibros**, identificado por los auriculares. También puedes cambiar los iconos desde la configuración del Home. Ajustes conserva su posición fija.

## Subir el primer audio por Wi-Fi

1. Descarga un archivo MP3 en tu teléfono o computadora. Puedes usar el ejemplo de abajo.
2. En Metalio, abre **Ajustes → Archivos → Transferir archivos por Wi-Fi** y usa el QR o la dirección que muestra el aparato.
3. En la página de transferencia, entra en **metalio → e-ink → audiobooks** y sube el MP3.
4. Cierra la transferencia, abre **Audiolibros** ; si ya estaba abierta, sal y vuelve a entrar para releer los archivos.

Para la primera prueba basta un único MP3. Se muestra como un libro y su nombre de archivo es el título. Puedes renombrarlo, por ejemplo, a `La abeja haragana.mp3` antes de subirlo.

## Libros con capítulos y portadas

Si preparas la tarjeta desde una computadora, puedes poner cada libro en una carpeta dentro de `audiobooks`:

```text
metalio/e-ink/audiobooks/
  La abeja haragana.mp3
  La abeja haragana.jpg
  Cuentos de la selva/
    01 - La abeja haragana.mp3
    02 - Historia de dos cachorros.mp3
    cover.jpg
```

Los capítulos se ordenan por nombre, reconociendo números: 2 se reproduce antes de 10. Al acabar un capítulo, continúa el siguiente. Una carpeta puede contener MP3, WAV y M4B/M4A compatibles. Esta primera versión muestra hasta 64 libros y 512 pistas en total, con hasta 256 pistas por libro.

La portada es opcional. Para un archivo suelto, usa el mismo nombre con extensión `.jpg` o `.png`; para una carpeta, usa `cover.jpg` o `cover.png`. Sin portada, el reproductor muestra una cubierta sencilla con el título y un icono de auriculares. Las portadas incrustadas en MP3 o M4B/M4A no se extraen en esta versión.

## Escuchar y continuar después

Selecciona un libro y pulsa **Reproducir**. **Pausar** guarda la posición y libera el audio para usar la grabadora o la conversación. **Reanudar** continúa desde ese punto. Los controles **15 s**, a ambos lados de Reproducir/Pausar, retroceden o adelantan y también funcionan en pausa. Los saltos pueden cruzar archivos de capítulos y actualizan la posición guardada. El botón de icono con borde negro **Reiniciar**, arriba a la derecha en la barra blanca, pide confirmación y vuelve al primer capítulo. El volumen se ajusta con los botones físicos de Metalio.

Puedes regresar al Home o entrar en standby mientras suena. En standby se conserva el audio y el acceso a la microSD; no es una suspensión completa del procesador y no requiere Wi-Fi. La pantalla del reproductor actualiza el progreso aproximadamente cada diez segundos y deja de hacerlo durante standby. Muestra el porcentaje con dos decimales: en un libro de 23 horas, un píxel de la barra equivale a unos tres minutos; el porcentaje permite ver avances más pequeños.

La posición se guarda periódicamente y al detener la reproducción en pequeños archivos de la microSD. No los borres si quieres conservar el punto de escucha. Un apagado inesperado puede perder los últimos segundos. Tras terminar un libro, la siguiente reproducción comienza desde el inicio. La duración mostrada para MP3 es aproximada, especialmente en archivos VBR.

Esta primera versión no muestra texto sincronizado ni conecta auriculares Bluetooth. No reproduce a la vez una conversación de voz o una grabación.

## Audio de prueba

[Cuentos de la selva para los niños, de Horacio Quiroga, en LibriVox](https://librivox.org/cuentos-de-la-selva-para-los-ninos-by-horacio-quiroga/) ofrece capítulos en español.

- [Descargar «La abeja haragana» en MP3](https://archive.org/download/cuentosdelaselva_1603_librivox/cuentosdelaselva_01_quiroga_128kb.mp3), aproximadamente 13,6 MB y 14 minutos.
- [Portada del libro](https://archive.org/download/cuentosdelaselva_1603_librivox/cuentos_selva_1603.jpg).

La grabación procede de LibriVox; su página identifica la obra, los narradores y las condiciones de dominio público. El audio no está incluido en el firmware.
