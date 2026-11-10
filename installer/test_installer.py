import importlib.util
import io
import json
import hashlib
from pathlib import Path
import shutil
from types import SimpleNamespace
import tempfile
import unittest
from unittest.mock import patch

spec=importlib.util.spec_from_file_location('installer',Path(__file__).with_name('app.py'))
a=importlib.util.module_from_spec(spec);spec.loader.exec_module(a)
fixture=tempfile.TemporaryDirectory(prefix='install-tests-',dir=Path(__file__).resolve().parent)
PAYLOAD=Path(fixture.name)
image=bytes(16*1024*1024)
(PAYLOAD/'Metalio-instalacion-limpia.bin').write_bytes(image)
(PAYLOAD/'manifest.json').write_text(json.dumps({'version':'0.75.999','bytes':len(image),
    'sha256':hashlib.sha256(image).hexdigest()}),encoding='utf-8')

class InstallTests(unittest.TestCase):
    def test_valid_image(self):
        self.assertEqual(a.verify_image(PAYLOAD).stat().st_size,16*1024*1024)
    def test_write_only_after_correct_probe(self):
        calls=[];events=[]
        def run(args):
            calls.append(args)
            if args[-1]=='flash_id': print('Detected flash size: 16MB')
            else: print('Writing at 0x00000000... (100 %)\nHash of data verified.')
        a.run_install(PAYLOAD,'SIMULATED',lambda *x:events.append(x),run)
        self.assertEqual(len(calls),2)
        self.assertIn('esp32s3',calls[0]);self.assertIn('write_flash',calls[1])
        self.assertEqual(calls[1][-2],'0x0')
        self.assertEqual(events[-1],('stage','done'))
    def test_wrong_flash_no_write(self):
        calls=[]
        def run(args):calls.append(args);print('Detected flash size: 8MB')
        with self.assertRaises(ValueError):a.run_install(PAYLOAD,'SIMULATED',lambda *x:None,run)
        self.assertEqual(len(calls),1)
    def test_chip_or_connection_error_no_write(self):
        calls=[]
        def run(args):calls.append(args);raise RuntimeError('Wrong chip')
        with self.assertRaises(RuntimeError):a.run_install(PAYLOAD,'SIMULATED',lambda *x:None,run)
        self.assertEqual(len(calls),1)
    def test_corrupt_image_no_serial_access(self):
        with tempfile.TemporaryDirectory(dir=PAYLOAD.parent) as tmp:
            p=Path(tmp)
            assert p.resolve().is_relative_to(PAYLOAD.parent.resolve())
            manifest=json.loads((PAYLOAD/'manifest.json').read_text())
            manifest['sha256']='0'*64
            (p/'manifest.json').write_text(json.dumps(manifest))
            shutil.copyfile(PAYLOAD/'Metalio-instalacion-limpia.bin',p/'Metalio-instalacion-limpia.bin')
            calls=[]
            with self.assertRaises(ValueError):a.run_install(p,'SIMULATED',lambda *x:None,lambda x:calls.append(x))
            self.assertFalse(calls)
    def test_ambiguous_devices_not_auto_selected(self):
        def port(name):return SimpleNamespace(device=name,vid=0x303a,pid=0x1001)
        self.assertEqual(a.preferred_port([port('COM1')]),'COM1')
        self.assertEqual(a.preferred_port([port('COM1'),port('COM2')]),'')
        self.assertEqual(a.preferred_port([]),'')
    def test_ui_cancel_never_starts_worker(self):
        import tkinter as tk
        root=tk.Tk();root.withdraw()
        with patch.object(a,'assets',return_value=PAYLOAD):
            window=a.Window(root,scan=False);window.port.set('SIMULATED')
            with patch('tkinter.messagebox.askyesno',return_value=False),patch.object(a.threading,'Thread') as thread:
                window.start();thread.assert_not_called();self.assertFalse(window.busy)
            window.language.set('Español');window.translate();root.update()
            self.assertEqual(window.install.cget('text'),'Instalar DoceInk')
            window.language.set('English');window.translate();root.update()
            self.assertEqual(window.install.cget('text'),'Install DoceInk')
        root.destroy()

if __name__=='__main__':unittest.main()
