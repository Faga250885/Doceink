"""Verified, device-bound flash backups and data-preserving DoceInk updates."""
from __future__ import annotations

import binascii
import contextlib
import hashlib
import io
import json
import os
from pathlib import Path
import re
import struct
import tempfile

FLASH_BYTES = 16 * 1024 * 1024
SECTOR = 4096
TABLE_OFFSET = 0x8000
OTADATA_OFFSET = 0xD000
SLOTS = (0x80000, 0x580000)
SLOT_SIZE = 5 * 1024 * 1024


def digest(path: Path) -> str:
    h = hashlib.sha256()
    with path.open('rb') as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b''):
            h.update(chunk)
    return h.hexdigest()


def root_directory() -> Path:
    return Path.home() / 'DoceInk' / 'Backups'


def key_for_mac(mac: str) -> str:
    if not re.fullmatch(r'(?:[0-9a-f]{2}:){5}[0-9a-f]{2}', mac):
        raise ValueError('Invalid Metalio identifier / Identificador de Metalio no válido')
    return mac.replace(':', '')


def run_tool(port, args, emit, runner=None):
    if runner is None:
        import esptool
        runner = esptool.main
    class Output(io.StringIO):
        def write(self, value):
            result = super().write(value)
            emit('log', value)
            match = re.search(r'\((\d+)\s*%\)', value)
            if match:
                emit('progress', min(99, int(match.group(1))))
            return result
    captured = Output()
    with contextlib.redirect_stdout(captured), contextlib.redirect_stderr(captured):
        runner(['--chip', 'esp32s3', '--port', port, '--after', 'no_reset'] + args)
    text = captured.getvalue()
    return text


def probe(port, emit, runner=None):
    flash = run_tool(port, ['flash_id'], emit, runner)
    if not re.search(r'Detected flash size:\s*16MB\b', flash):
        raise ValueError('A 16 MB ESP32-S3 is required / Se requiere un ESP32-S3 de 16 MB')
    security = run_tool(port, ['get_security_info'], emit, runner)
    if not re.search(r'Secure Boot:\s*Disabled', security) or not re.search(r'Flash Encryption:\s*Disabled', security):
        raise ValueError('Encrypted or secure-boot devices are not supported / No se admiten equipos cifrados o con arranque seguro')
    output = run_tool(port, ['read_mac'], emit, runner)
    found = re.search(r'\bMAC:\s*((?:[0-9a-fA-F]{2}:){5}[0-9a-fA-F]{2})', output)
    if not found:
        raise ValueError('Could not read device identity / No se pudo identificar Metalio')
    return found.group(1).lower()


def read_flash(port, address, size, target, emit, runner=None):
    run_tool(port, ['--baud', '460800', 'read_flash', hex(address), hex(size), str(target)], emit, runner)
    if not target.is_file() or target.stat().st_size != size:
        raise ValueError('Incomplete flash read / Lectura incompleta de la memoria')


def valid_table(table):
    """Accept only DoceInk's exact safe app/OTA map and reject encrypted entries."""
    if len(table) != SECTOR:
        return False
    entries = {}
    for offset in range(0, 0xC00, 32):
        row = table[offset:offset+32]
        if row[:2] == b'\xeb\xeb' or row == b'\xff' * 32:
            break
        magic, typ, sub, start, size, label, flags = struct.unpack('<2sBBII16sI', row)
        if magic != b'\xaa\x50' or flags & 1:
            return False
        entries[(typ, sub)] = (start, size)
    return (entries.get((1, 0)) == (OTADATA_OFFSET, 0x2000) and
            entries.get((0, 0x10)) == (SLOTS[0], SLOT_SIZE) and
            entries.get((0, 0x11)) == (SLOTS[1], SLOT_SIZE))


def active_slot(otadata):
    if len(otadata) != SECTOR * 2:
        raise ValueError('Invalid OTA data / Datos de arranque no válidos')
    valid = []
    for index in range(2):
        entry = otadata[index * SECTOR:index * SECTOR + 32]
        seq, state, crc = struct.unpack_from('<I20xII', entry)
        expected = binascii.crc32(struct.pack('<I', seq), 0xFFFFFFFF) & 0xffffffff
        if 0 < seq < 0xffffffff and state not in (3, 4) and crc == expected:
            valid.append((seq, index, state))
    if not valid:
        if otadata == b'\xff' * len(otadata):
            return 0, 0, None
        raise ValueError('Could not determine boot slot / No se pudo identificar la partición activa')
    seq, index, state = max(valid, key=lambda item: (item[0], -item[1]))
    if state in (0, 1):
        raise ValueError('An update is awaiting confirmation; start Metalio first / Hay una actualización pendiente; inicia Metalio primero')
    return (seq - 1) % 2, seq, index


def next_ota_sector(seq, old_index, target):
    next_seq = seq + 1 if seq else target + 1
    if next_seq >= 0xffffffff or (next_seq - 1) % 2 != target:
        raise ValueError('Unexpected boot sequence / Secuencia de arranque inesperada')
    entry = bytearray(b'\xff' * SECTOR)
    struct.pack_into('<I', entry, 0, next_seq)
    # ESP_OTA_IMG_NEW: let the bootloader roll back if the new image cannot start.
    struct.pack_into('<I', entry, 24, 0)
    struct.pack_into('<I', entry, 28, binascii.crc32(struct.pack('<I', next_seq), 0xffffffff) & 0xffffffff)
    sector_index = 1 - old_index if old_index is not None else 0
    return OTADATA_OFFSET + sector_index * SECTOR, bytes(entry)


def app_description(header):
    if len(header) < 112 or header[0] != 0xe9 or header[32:36] != b'\x32\x54\xcd\xab':
        return '', ''
    return (header[48:80].split(b'\0', 1)[0].decode('ascii', 'ignore'),
            header[80:112].split(b'\0', 1)[0].decode('ascii', 'ignore'))


def is_doceink(version, project):
    # 0.x is DoceInk's own version series; original Metalio firmware uses a
    # different series. Unknown versions must never be silently classified.
    return project == 'Metalio-E-Ink4' and bool(re.fullmatch(r'0\.\d+\.\d+', version))


def inspect(port, folder, emit, runner=None):
    mac = probe(port, emit, runner)
    table_path = folder / 'partition-table.bin'
    read_flash(port, TABLE_OFFSET, SECTOR, table_path, emit, runner)
    table = table_path.read_bytes()
    if not valid_table(table):
        return {'mac': mac, 'kind': 'unknown', 'version': '', 'table': table}
    ota_path = folder / 'ota-data.bin'
    read_flash(port, OTADATA_OFFSET, SECTOR * 2, ota_path, emit, runner)
    otadata = ota_path.read_bytes()
    slot, seq, sector = active_slot(otadata)
    head_path = folder / 'app-header.bin'
    read_flash(port, SLOTS[slot], 256, head_path, emit, runner)
    version, project = app_description(head_path.read_bytes())
    return {'mac': mac, 'kind': 'doceink' if is_doceink(version, project) else 'unknown',
            'version': version, 'table': table, 'otadata': otadata,
            'slot': slot, 'seq': seq, 'sector': sector}


def backup_paths(mac, root=None):
    directory = (root or root_directory()) / key_for_mac(mac)
    return directory, directory / 'original-flash.bin', directory / 'original-flash.json'


def backup_info(mac, root=None):
    directory, image, metadata = backup_paths(mac, root)
    if not image.is_file() or not metadata.is_file():
        return None
    data = json.loads(metadata.read_text(encoding='utf-8'))
    if (data.get('mac') != mac or data.get('bytes') != FLASH_BYTES or
            image.stat().st_size != FLASH_BYTES or digest(image) != data.get('sha256')):
        raise ValueError('Backup verification failed / El respaldo no supera la verificación')
    return image


def save_backup(port, mac, emit, root=None, runner=None):
    directory, image, metadata = backup_paths(mac, root)
    if image.exists() or metadata.exists():
        raise FileExistsError('A backup already exists; it will not be overwritten / Ya existe un respaldo y no se sobrescribirá')
    if probe(port, emit, runner) != mac:
        raise ValueError('Connected Metalio changed / Cambió el Metalio conectado')
    directory.mkdir(parents=True, exist_ok=True, mode=0o700)
    with tempfile.TemporaryDirectory(prefix='capture-', dir=directory) as tmp:
        first, second = Path(tmp) / 'first.bin', Path(tmp) / 'second.bin'
        emit('stage', 'backup_read')
        read_flash(port, 0, FLASH_BYTES, first, emit, runner)
        emit('stage', 'backup_verify')
        read_flash(port, 0, FLASH_BYTES, second, emit, runner)
        checksum = digest(first)
        if checksum != digest(second):
            raise ValueError('Backup reads differ; nothing was installed / Las lecturas del respaldo no coinciden; no se instaló nada')
        if probe(port, emit, runner) != mac:
            raise ValueError('Connected Metalio changed / Cambió el Metalio conectado')
        # Exclusive creation protects an existing original backup against replacement.
        fd = os.open(image, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
        try:
            with os.fdopen(fd, 'wb') as output, first.open('rb') as source:
                while chunk := source.read(1024 * 1024): output.write(chunk)
                output.flush(); os.fsync(output.fileno())
            payload = {'format': 1, 'mac': mac, 'bytes': FLASH_BYTES, 'sha256': checksum}
            fd = os.open(metadata, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
            with os.fdopen(fd, 'w', encoding='utf-8') as output:
                json.dump(payload, output); output.flush(); os.fsync(output.fileno())
        except BaseException:
            # A partial file remains visible and can never be mistaken for a verified backup.
            raise
    if backup_info(mac, root) is None:
        raise ValueError('Backup could not be verified / No se pudo verificar el respaldo')
    return image


def restore_backup(port, expected_mac, emit, root=None, runner=None):
    image = backup_info(expected_mac, root)
    if image is None:
        raise ValueError('No backup exists for this Metalio / No existe un respaldo para este Metalio')
    if probe(port, emit, runner) != expected_mac:
        raise ValueError('Connected Metalio changed / Cambió el Metalio conectado')
    emit('stage', 'restoring')
    run_tool(port, ['--baud', '460800', 'write_flash', '--flash_mode', 'keep', '--flash_freq', 'keep',
                    '--flash_size', 'keep', '0x0', str(image)], emit, runner)
    with tempfile.TemporaryDirectory(prefix='restore-check-', dir=image.parent) as tmp:
        check = Path(tmp) / 'verify.bin'
        read_flash(port, 0, FLASH_BYTES, check, emit, runner)
        if digest(check) != digest(image):
            raise ValueError('Restored flash verification failed / Falló la verificación del respaldo restaurado')
    run_tool(port, ['run'], emit, runner)
    emit('progress', 100)
    emit('stage', 'restored')


def update_existing(port, device, folder, emit, runner=None):
    """Write inactive OTA slot first, then switch one OTA data sector."""
    image = folder / 'Metalio-instalacion-limpia.bin'
    manifest = json.loads((folder / 'manifest.json').read_text(encoding='utf-8'))
    records = [r for r in manifest.get('inputs', []) if int(r['offset'], 16) == SLOTS[0]]
    if len(records) != 1 or not 0 < records[0]['bytes'] <= SLOT_SIZE:
        raise ValueError('Invalid update image / Imagen de actualización no válida')
    if device.get('kind') != 'doceink' or probe(port, emit, runner) != device['mac']:
        raise ValueError('Connected Metalio changed / Cambió el Metalio conectado')
    with image.open('rb') as stream:
        stream.seek(TABLE_OFFSET); clean_table = stream.read(SECTOR)
        if clean_table != device['table']:
            raise ValueError('Partition layout differs; use Wi-Fi update / El mapa de particiones no coincide; actualiza por Wi-Fi')
        stream.seek(SLOTS[0]); app = stream.read(records[0]['bytes'])
    if hashlib.sha256(app).hexdigest() != records[0]['sha256']:
        raise ValueError('Firmware integrity check failed / Falló la verificación del firmware')
    target = 1 - device['slot']
    ota_offset, entry = next_ota_sector(device['seq'], device['sector'], target)
    app_file, ota_file = folder / 'update-app.bin', folder / 'update-otadata.bin'
    app_file.write_bytes(app); ota_file.write_bytes(entry)
    emit('stage', 'updating')
    run_tool(port, ['--baud', '460800', 'write_flash', hex(SLOTS[target]), str(app_file)], emit, runner)
    check_app = folder / 'update-app-check.bin'
    read_flash(port, SLOTS[target], len(app), check_app, emit, runner)
    if digest(check_app) != records[0]['sha256']:
        raise ValueError('Written update verification failed / Falló la verificación de la actualización')
    if probe(port, emit, runner) != device['mac']:
        raise ValueError('Connected Metalio changed / Cambió el Metalio conectado')
    # Never switch the active slot unless the application write was verified.
    emit('stage', 'switching')
    run_tool(port, ['--baud', '460800', 'write_flash', hex(ota_offset), str(ota_file)], emit, runner)
    check_ota = folder / 'update-ota-check.bin'
    read_flash(port, ota_offset, SECTOR, check_ota, emit, runner)
    if check_ota.read_bytes() != entry:
        raise ValueError('Boot selection verification failed / Falló la verificación del arranque')
    run_tool(port, ['run'], emit, runner)
    emit('progress', 100)
    emit('stage', 'updated')
