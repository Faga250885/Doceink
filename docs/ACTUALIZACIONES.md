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
- [Versión documentada 0.75.149](https://github.com/Faga250885/Doceink/releases/tag/v0.75.149).
- [Firmware OTA 0.75.149](https://github.com/Faga250885/Doceink/releases/download/v0.75.149/Doceink-EInk4.bin).

`Doceink-EInk4.bin` es únicamente la aplicación de actualización. No contiene el arranque, la tabla de particiones ni todo el paquete de recursos necesario para empezar desde cero. Para eso utiliza la [guía de instalación limpia](INSTALACION.md).

No utilices `Metalio-instalacion-limpia.bin` en el actualizador Wi-Fi. No intercambies los archivos por tener ambos extensión `.bin`.

## Novedades de 0.75.149

- Corregidos los repintados repetidos de Información en reposo; los botones de actualización solo se repintan cuando cambia su estado.
- Icono de DoceInk centrado, con nombre y versión debajo, sobre el botón de actualización.
- Información del firmware con borde negro fino y el mismo ancho que el panel inferior.
- Botón negro para comprobar actualizaciones y crédito pequeño centrado debajo: «Creado por faga12@gmail.com».
- Las actualizaciones por Wi-Fi conservan cuentas, ajustes y datos de la microSD.

La aplicación ocupa 4.989.152 bytes. No se atribuye un porcentaje de mejora de velocidad. Las notas anteriores están en [Releases](https://github.com/Faga250885/Doceink/releases).
