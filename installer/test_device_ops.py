import binascii
import hashlib
import json
from pathlib import Path
import struct
import tempfile
import unittest
from unittest import mock

import device_ops as ops


def partition(typ, sub, offset, size, name):
    return struct.pack('<2sBBII16sI', b'\xaa\x50', typ, sub, offset, size, name.encode(), 0)


def table():
    raw = bytearray(b'\xff' * ops.SECTOR)
    rows = [partition(1, 0, ops.OTADATA_OFFSET, 0x2000, 'otadata'),
            partition(0, 0x10, ops.SLOTS[0], ops.SLOT_SIZE, 'ota_0'),
            partition(0, 0x11, ops.SLOTS[1], ops.SLOT_SIZE, 'ota_1')]
    raw[:len(rows)*32] = b''.join(rows)
    return bytes(raw)


def app(version='0.75.158'):
    raw = bytearray(b'\xff' * 256)
    raw[0] = 0xe9; raw[32:36] = b'\x32\x54\xcd\xab'
    raw[48:80] = version.encode().ljust(32, b'\0')
    raw[80:112] = b'Metalio-E-Ink4'.ljust(32, b'\0')
    return bytes(raw)


class FakeDevice:
    def __init__(self):
        self.data = bytearray(b'\xff' * ops.FLASH_BYTES)
        self.data[ops.TABLE_OFFSET:ops.TABLE_OFFSET+ops.SECTOR] = table()
        self.data[ops.SLOTS[0]:ops.SLOTS[0]+256] = app()
        self.calls = []
        self.mac = '10:20:ba:6d:64:08'
        self.corrupt_second_read = False
        self.reads = 0
        self.fail_app_write = False
        self.corrupt_readback = False
        self.encrypted = False

    def __call__(self, args):
        self.calls.append(args[:])
        if 'flash_id' in args: print('Detected flash size: 16MB')
        elif 'get_security_info' in args:
            print('Secure Boot: Disabled')
            print('Flash Encryption: ' + ('Enabled' if self.encrypted else 'Disabled'))
        elif 'read_mac' in args: print('MAC: ' + self.mac)
        elif 'read_flash' in args:
            i = args.index('read_flash'); start, size = int(args[i+1], 0), int(args[i+2], 0)
            contents = bytes(self.data[start:start+size]); self.reads += 1
            if self.corrupt_second_read and self.reads == 2: contents = bytes([contents[0] ^ 1]) + contents[1:]
            if self.corrupt_readback and start == ops.SLOTS[1]: contents = bytes([contents[0] ^ 1]) + contents[1:]
            Path(args[i+3]).write_bytes(contents)
        elif 'write_flash' in args:
            i = args.index('write_flash'); start = int(args[-2], 0); data = Path(args[-1]).read_bytes()
            if self.fail_app_write and start == ops.SLOTS[1]: raise RuntimeError('failed write')
            self.data[start:start+len(data)] = data
        elif 'run' in args: pass
        else: raise AssertionError(args)


class DeviceTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(prefix='doceink-device-test-', dir=Path(__file__).parent)
        self.path = Path(self.tmp.name); self.device = FakeDevice(); self.emit = lambda *args: None
    def tearDown(self): self.tmp.cleanup()

    def test_inspection_and_security(self):
        result = ops.inspect('SIM', self.path, self.emit, self.device)
        self.assertEqual((result['kind'], result['version'], result['slot']), ('doceink', '0.75.158', 0))
        self.device.encrypted = True
        with self.assertRaises(ValueError): ops.inspect('SIM', self.path, self.emit, self.device)
        self.assertFalse(any('write_flash' in a for a in self.device.calls))

    def test_backup_restore_is_bound_and_verified(self):
        mac = self.device.mac
        image = ops.save_backup('SIM', mac, self.emit, self.path, self.device)
        self.assertEqual(image.stat().st_size, ops.FLASH_BYTES)
        with self.assertRaises(FileExistsError): ops.save_backup('SIM', mac, self.emit, self.path, self.device)
        self.device.mac = 'aa:bb:cc:dd:ee:ff'
        with self.assertRaises(ValueError): ops.restore_backup('SIM', mac, self.emit, self.path, self.device)
        self.assertFalse(any('write_flash' in a for a in self.device.calls))
        self.device.mac = mac
        self.device.data[ops.SLOTS[0]] = 0
        ops.restore_backup('SIM', mac, self.emit, self.path, self.device)
        self.assertEqual(self.device.data[ops.SLOTS[0]], 0xe9)
        image.write_bytes(b'bad')
        with self.assertRaises(ValueError): ops.restore_backup('SIM', mac, self.emit, self.path, self.device)

    def test_backup_mismatch_does_not_install(self):
        self.device.corrupt_second_read = True
        with self.assertRaises(ValueError): ops.save_backup('SIM', self.device.mac, self.emit, self.path, self.device)
        self.assertIsNone(ops.backup_info(self.device.mac, self.path))
        self.assertFalse(any('write_flash' in a for a in self.device.calls))

    def test_backup_rejects_device_change_before_saving(self):
        expected = self.device.mac
        def changed(args):
            self.device(args)
            if 'read_flash' in args and self.device.reads == 2:
                self.device.mac = 'aa:bb:cc:dd:ee:ff'
        with self.assertRaises(ValueError): ops.save_backup('SIM', expected, self.emit, self.path, changed)
        self.assertIsNone(ops.backup_info(expected, self.path))

    def test_update_inactive_slot_and_switch_one_sector(self):
        state = ops.inspect('SIM', self.path, self.emit, self.device)
        image = self.path / 'Metalio-instalacion-limpia.bin'
        image.write_bytes(self.device.data)
        data = app('0.75.159')
        with image.open('r+b') as f: f.seek(ops.SLOTS[0]); f.write(data)
        (self.path / 'manifest.json').write_text(json.dumps({'inputs': [{'offset': hex(ops.SLOTS[0]), 'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest()}]}))
        wrong = dict(state); wrong['table'] = b'\x00' * ops.SECTOR
        with self.assertRaises(ValueError): ops.update_existing('SIM', wrong, self.path, self.emit, self.device)
        self.assertFalse(any('write_flash' in a for a in self.device.calls))
        self.device.fail_app_write = True
        with self.assertRaises(RuntimeError): ops.update_existing('SIM', state, self.path, self.emit, self.device)
        self.assertEqual(self.device.data[ops.OTADATA_OFFSET:ops.OTADATA_OFFSET+ops.SECTOR*2], b'\xff'*(ops.SECTOR*2))
        self.device.fail_app_write = False
        self.device.corrupt_readback = True
        with self.assertRaises(ValueError): ops.update_existing('SIM', state, self.path, self.emit, self.device)
        self.assertEqual(self.device.data[ops.OTADATA_OFFSET:ops.OTADATA_OFFSET+ops.SECTOR*2], b'\xff'*(ops.SECTOR*2))
        self.device.corrupt_readback = False
        ops.update_existing('SIM', state, self.path, self.emit, self.device)
        self.assertEqual(bytes(self.device.data[ops.SLOTS[1]:ops.SLOTS[1]+256]), data)
        ota = bytearray(self.device.data[ops.OTADATA_OFFSET:ops.OTADATA_OFFSET+ops.SECTOR*2])
        with self.assertRaises(ValueError): ops.active_slot(ota)  # new image still pending boot
        struct.pack_into('<I', ota, 24, 2)  # app confirmed by firmware
        self.assertEqual(ops.active_slot(ota)[0], 1)
        self.assertEqual(bytes(self.device.data[0x9000:0xd000]), b'\xff'*0x4000)

    def test_unexpected_ota_data_is_rejected(self):
        broken = b'\x01' + b'\xff'*(ops.SECTOR*2-1)
        with self.assertRaises(ValueError): ops.active_slot(broken)

    def test_existing_slot_selection_and_pending_update(self):
        def entry(seq, state):
            sector = bytearray(b'\xff'*ops.SECTOR)
            struct.pack_into('<I', sector, 0, seq)
            struct.pack_into('<I', sector, 24, state)
            struct.pack_into('<I', sector, 28, binascii.crc32(struct.pack('<I',seq),0xffffffff)&0xffffffff)
            return bytes(sector)
        data = entry(7,2) + entry(8,2)
        self.assertEqual(ops.active_slot(data), (1,8,1))
        offset, new = ops.next_ota_sector(8,1,0)
        self.assertEqual(offset, ops.OTADATA_OFFSET)
        self.assertEqual(struct.unpack_from('<I',new)[0],9)
        self.assertEqual(struct.unpack_from('<I',new,24)[0],0)
        with self.assertRaises(ValueError): ops.active_slot(entry(7,2)+entry(8,1))

    def test_unknown_firmware_is_not_reported_as_doceink(self):
        self.device.data[ops.SLOTS[0]:ops.SLOTS[0]+256] = app('2.0.61')
        state = ops.inspect('SIM', self.path, self.emit, self.device)
        self.assertEqual(state['kind'], 'unknown')
        self.assertFalse(ops.is_doceink('0.75.158', 'Other project'))


class BackupLocationTest(unittest.TestCase):
    def test_backup_folder_is_on_actual_desktop(self):
        with mock.patch.object(ops, 'desktop_directory', return_value=Path('/synced/Desktop')):
            self.assertEqual(ops.root_directory(), Path('/synced/Desktop/Metalio - Firmware original'))


if __name__ == '__main__': unittest.main()
