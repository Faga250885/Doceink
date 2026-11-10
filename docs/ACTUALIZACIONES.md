# Actualizar conservando los datos

[Volver al inicio](../README.md)

Si Metalio ya tiene Doceink instalado, no necesitas repetir la instalación limpia.

1. Conecta Metalio a una red Wi-Fi.
2. Abre **Ajustes → Sistema → Información → Comprobar actualización**.
3. Revisa la versión ofrecida y confirma la actualización.
4. Espera a que termine y se reinicie. Después consulta la versión en Información.

Las actualizaciones normales conservan las cuentas, los ajustes y los archivos de la microSD. La primera instalación limpia por USB sí reemplaza la memoria interna.

## Descargas

- [Última versión publicada](https://github.com/Faga250885/Doceink/releases/latest).
- [Versión documentada 0.75.145](https://github.com/Faga250885/Doceink/releases/tag/v0.75.145).
- [Firmware OTA 0.75.145](https://github.com/Faga250885/Doceink/releases/download/v0.75.145/Doceink-EInk4.bin).

`Doceink-EInk4.bin` es únicamente la aplicación de actualización. No contiene el arranque, la tabla de particiones ni todo el paquete de recursos necesario para empezar desde cero. Para eso utiliza la [guía de instalación limpia](INSTALACION.md).

No utilices `Metalio-instalacion-limpia.bin` en el actualizador Wi-Fi. No intercambies los archivos por tener ambos extensión `.bin`.

## Novedades de 0.75.145

- Instalador completo distribuible sin datos personales incluidos.
- Retiradas las pantallas y el audio de pruebas de fábrica.
- Retirada la antigua limpieza de Jira al abrir Tareas.
- Conservadas las alarmas del reloj, las aplicaciones y la mejora de respuesta durante las actualizaciones de pantalla.
- Aplicación reducida en 49.440 bytes respecto a 0.75.144: **0,98 % menos**.

No se atribuye un porcentaje de mejora de velocidad a esta limpieza: no se ha medido en hardware. Las notas de cada versión están en [Releases](https://github.com/Faga250885/Doceink/releases).
