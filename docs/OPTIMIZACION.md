# Optimización del firmware 0.75.243

Comparación del binario compilado de la aplicación para Metalio E-Ink4, con la misma tabla de particiones.

| Medida | 0.75.242 | 0.75.243 |
| --- | ---: | ---: |
| Aplicación | 5.224.304 bytes | 5.114.768 bytes |
| Margen del espacio OTA de 5 MiB | 18.576 bytes | 128.112 bytes |

Ahorro neto: **109.536 bytes** (109,5 kB; aproximadamente 2,1 % del binario). El margen disponible para actualizaciones pasa a ser unas 6,9 veces mayor.

## Cambios verificados

- Las doce piezas de ajedrez pasan de ARGB de 32 bits a una paleta indexada de tres colores: 76.800 → 4.992 bytes. Se conserva cada píxel, incluida la transparencia. La prueba compara las imágenes originales y verifica el render de LVGL.
- Los recursos y descriptores de iconos de estado y de toolbar tienen una sola definición compartida entre módulos. La comprobación de direcciones entre dos unidades de compilación y el mapa de símbolos del firmware confirman que no se duplican.
- Se retira del firmware el widget de consumo de IA que ya estaba deshabilitado, sus servicios y su antiguo importador de sesiones. La configuración de la clave API de OpenAI por QR sigue disponible. No se borran archivos existentes de la microSD.
- Audiolibros, grabadora y juegos reutilizan tarjetas y fondos de modal comunes. Conservan sus opciones y geometría.
- Las páginas web locales reutilizan una sola implementación de traducción. La tabla es estática y el procesamiento evita crear copias temporales de cada token y traducción.
- El nombre de la sección usa la etiqueta central y el temporizador existentes de la barra superior durante cinco segundos. Los mensajes de aplicación y de conexión tienen prioridad; las pantallas a pantalla completa no reciben etiquetas flotantes.

## Validación

Compilación ESP32-S3, **137 pruebas aprobadas**, integridad de paquetes, regiones vacías de la imagen de instalación limpia y comparación de recursos/particiones. Las pruebas cubren configuración de OpenAI por QR, transferencia de archivos, reproducción y reanudación de audio, títulos de sección, modales, traducciones y recursos gráficos. Los cinco segundos y sus prioridades se comprueban con el reloj simulado de LVGL.

El ahorro indicado corresponde al tamaño del firmware. No es una medición de autonomía o latencia en un dispositivo físico. Se conserva el soporte de los formatos de fuentes y de las aplicaciones activas.
