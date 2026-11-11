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
        self.assertEqual(a.preferred_port([SimpleNamespace(device='COM9',vid=0x1234,pid=0x1001)]),'')
        self.assertEqual(a.preferred_port([port('/dev/cu.usbmodem1'),port('/dev/tty.usbmodem1')]),'/dev/cu.usbmodem1')
    def test_detection_removes_disconnected_or_ambiguous_target(self):
        import tkinter as tk
        root=tk.Tk();root.withdraw()
        window=a.Window(root,scan=False)
        def port(name):return SimpleNamespace(device=name,vid=0x303a,pid=0x1001)
        with patch('serial.tools.list_ports.comports',return_value=[port('COM3')]):
            window.refresh_detection()
            self.assertEqual(window.port.get(),'COM3')
        for ports in ([],[port('COM3'),port('COM4')]):
            with patch('serial.tools.list_ports.comports',return_value=ports),patch('tkinter.messagebox.askyesno') as ask:
                window.start()
                self.assertEqual(window.port.get(),'')
                self.assertIn('disabled',window.install.state())
                ask.assert_not_called()
        self.assertFalse(hasattr(window,'select'))
        root.destroy()
    def test_target_changed_during_download_never_opens_serial(self):
        import queue
        window=object.__new__(a.Window);window.queue=queue.Queue()
        with patch.object(a,'download_latest',return_value='0.75.999'),patch.object(a,'verify_image'),patch('serial.tools.list_ports.comports',return_value=[]),patch.object(a,'run_install') as run:
            window.worker('SIMULATED')
            run.assert_not_called()
        self.assertIn(('stage','error'),list(window.queue.queue))
    def test_ui_cancel_never_starts_worker(self):
        import tkinter as tk
        root=tk.Tk();root.withdraw()
        with patch.object(a,'assets',return_value=PAYLOAD):
            window=a.Window(root,scan=False);window.port.set('SIMULATED')
            with patch('serial.tools.list_ports.comports',return_value=[SimpleNamespace(device='SIMULATED',vid=0x303a,pid=0x1001)]),patch('tkinter.messagebox.askyesno',return_value=False) as ask,patch.object(a.threading,'Thread') as thread:
                window.start();thread.assert_not_called();self.assertFalse(window.busy)
                ask.assert_called_once()
            window.language.set('Español');window.translate();root.update()
            self.assertEqual(window.install.cget('text'),'Instalar DoceInk')
            window.language.set('English');window.translate();root.update()
            self.assertEqual(window.install.cget('text'),'Install DoceInk')
        root.destroy()
    def test_doceink_presents_update_and_matching_restore(self):
        import tkinter as tk
        root=tk.Tk();root.withdraw()
        with patch.object(a,'assets',return_value=PAYLOAD):
            window=a.Window(root,scan=False);window.port.set('SIMULATED')
            window.device={'kind':'doceink','mac':'10:20:ba:6d:64:08'}
            window.has_backup=True;window.translate();root.update()
            self.assertEqual(window.install.cget('text'),'Update DoceInk')
            self.assertNotIn('disabled',window.restore.state())
            self.assertFalse(window.backup_option.winfo_manager())
            with patch('serial.tools.list_ports.comports',return_value=[SimpleNamespace(device='SIMULATED',vid=0x303a,pid=0x1001)]),patch('tkinter.messagebox.askyesno',return_value=True),patch.object(window,'begin_operation') as begin:
                window.start_restore();begin.assert_called_once_with('restore')
                begin.reset_mock();window.start();begin.assert_called_once_with('update')
            window.has_backup=False;window.translate()
            self.assertIn('disabled',window.restore.state())
        root.destroy()

    def test_new_install_asks_to_confirm_original_before_start(self):
        import tkinter as tk
        root=tk.Tk();root.withdraw()
        with patch.object(a,'assets',return_value=PAYLOAD):
            window=a.Window(root,scan=False);window.port.set('SIMULATED')
            window.device={'kind':'unknown','mac':'10:20:ba:6d:64:08'}
            with patch('serial.tools.list_ports.comports',return_value=[SimpleNamespace(device='SIMULATED',vid=0x303a,pid=0x1001)]),patch('tkinter.messagebox.askyesno',side_effect=[True,False]) as ask,patch.object(window,'begin_operation') as begin:
                window.start();begin.assert_not_called();self.assertEqual(ask.call_count,2)
        root.destroy()

if __name__=='__main__':unittest.main()
