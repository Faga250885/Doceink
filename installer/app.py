"""DoceInk USB installer for Windows and macOS. MIT; tools retain their licenses."""
from __future__ import annotations
import contextlib
import hashlib
import io
import json
from pathlib import Path
import queue
import re
import sys
import threading
import tempfile
import time
from download import download_latest
import device_ops

VERSION = '0.75.158.1'
FLASH_BYTES = 16 * 1024 * 1024
TEXT = {
 'title': ('DoceInk Setup', 'Instalar DoceInk'),
 'subtitle': ('Install, update or restore your Metalio.', 'Instala, actualiza o restaura tu Metalio.'),
 'connect': ('Connect Metalio with a USB data cable.', 'Conecta Metalio con un cable USB de datos.'),
 'none': ('Waiting for Metalio…', 'Esperando a Metalio…'),
 'choose': ('Several compatible USB devices detected. Leave only Metalio connected.', 'Hay varios dispositivos USB compatibles. Deja conectado solo el Metalio.'),
 'detect_error': ('Could not detect Metalio. Check the USB connection.', 'No se pudo detectar Metalio. Revisa la conexión USB.'),
 'ready': ('Metalio connection detected. Ready to install.', 'Conexión de Metalio detectada. Listo para instalar.'),
 'install': ('Install DoceInk', 'Instalar DoceInk'),
 'update': ('Update DoceInk', 'Actualizar DoceInk'),
 'restore': ('Restore original backup', 'Restaurar respaldo original'),
 'backup_option': ('Back up current firmware before installation', 'Respaldar el firmware actual antes de instalar'),
 'backup_location': ('Backups are stored on this computer and may contain accounts and passwords.', 'Los respaldos se guardan en este ordenador y pueden contener cuentas y contraseñas.'),
 'identifying': ('Checking connected Metalio… It may restart.', 'Comprobando el Metalio conectado… Puede reiniciarse.'),
 'detected_doceink': ('DoceInk detected. Choose an update or restore a saved original backup.', 'DoceInk detectado. Elige actualizar o restaurar un respaldo original.'),
 'detected_doceink_no_backup': ('DoceInk detected. No original backup was found on this computer.', 'DoceInk detectado. No se encontró un respaldo original en este ordenador.'),
 'detected_original': ('Metalio detected. Back up its current firmware before installing.', 'Metalio detectado. Respalda su firmware actual antes de instalar.'),
 'identify': ('Check Metalio', 'Comprobar Metalio'),
 'notice_update': ('Updates preserve internal accounts, settings and microSD files. Restoring a backup replaces internal data.', 'Actualizar conserva las cuentas, ajustes y archivos de la microSD. Restaurar un respaldo reemplaza los datos internos.'),
 'no_backup': ('No original backup for this Metalio was found on this computer.', 'No se encontró un respaldo original de este Metalio en este ordenador.'),
 'backup_read': ('Backing up the original firmware… Keep USB connected.', 'Respaldando el firmware original… Mantén el USB conectado.'),
 'backup_verify': ('Verifying the backup… Keep USB connected.', 'Verificando el respaldo… Mantén el USB conectado.'),
 'restoring': ('Restoring backup… Keep USB connected.', 'Restaurando respaldo… Mantén el USB conectado.'),
 'restored': ('Original backup restored. Metalio is restarting.', 'Respaldo original restaurado. Metalio se está reiniciando.'),
 'updating': ('Updating DoceInk… Keep USB connected.', 'Actualizando DoceInk… Mantén el USB conectado.'),
 'switching': ('Finishing update… Keep USB connected.', 'Finalizando actualización… Mantén el USB conectado.'),
 'updated': ('DoceInk updated. Metalio is restarting.', 'DoceInk actualizado. Metalio se está reiniciando.'),
 'confirm_backup': ('Is the current firmware the original you want to preserve?\n\nAn unencrypted backup, including internal settings and credentials, will be saved on this computer. Keep it private. The microSD is not included.', '¿El firmware actual es el original que quieres conservar?\n\nSe guardará en este ordenador un respaldo sin cifrar, incluidos ajustes y credenciales internos. Guárdalo en privado. La microSD no está incluida.'),
 'confirm_update': ('Update DoceInk on this Metalio?\n\nAccounts, settings and microSD files will be preserved. Keep USB connected until it finishes.', '¿Actualizar DoceInk en este Metalio?\n\nSe conservarán las cuentas, los ajustes y los archivos de la microSD. Mantén el USB conectado hasta que termine.'),
 'confirm_restore': ('Restore the original backup for this Metalio?\n\nCurrent internal firmware, accounts and settings will be replaced by the contents of the backup. The microSD is not erased. Keep USB connected.', '¿Restaurar el respaldo original de este Metalio?\n\nEl firmware, las cuentas y los ajustes internos actuales serán reemplazados por los del respaldo. La microSD no se borra. Mantén el USB conectado.'),
 'notice': ('Clean installation · Internal accounts and settings will be erased.\nYour microSD card is not erased. Wi-Fi updates preserve your data.', 'Instalación limpia · Se borrarán cuentas y ajustes internos.\nLa microSD no se borra. Las actualizaciones Wi-Fi conservan tus datos.'),
 'compat': ('Only for Metalio E-Ink4 · ESP32-S3 · 16 MB flash', 'Solo para Metalio E-Ink4 · ESP32-S3 · flash de 16 MB'),
 'confirm': ('Install on the connected Metalio?\n\nThis replaces all internal firmware, accounts, Wi-Fi networks and settings. It does not erase the microSD card.\n\nConfirm that the connected device is a Metalio E-Ink4. Keep the cable connected until installation finishes.', '¿Instalar en el Metalio conectado?\n\nSe reemplazarán el firmware, las cuentas, redes Wi-Fi y ajustes internos. La microSD no se borra.\n\nConfirma que conectaste un Metalio E-Ink4. Mantén el cable conectado hasta que termine.'),
 'latest': ('Checking the latest GitHub release…', 'Consultando la última versión en GitHub…'),
 'downloading': ('Downloading the latest firmware…', 'Descargando la última versión del firmware…'),
 'checking': ('Verifying downloaded firmware…', 'Verificando el firmware descargado…'),
 'connecting': ('Connecting and checking hardware…', 'Conectando y comprobando el hardware…'),
 'writing': ('Installing… Keep USB connected.', 'Instalando… Mantén el USB conectado.'),
 'done': ('Installation complete. Metalio is restarting.', 'Instalación terminada. Metalio se está reiniciando.'),
 'error': ('Installation could not finish. See details below.', 'No se pudo completar la instalación. Revisa los detalles.'),
 'wait': ('Please wait until installation finishes. Do not unplug Metalio.', 'Espera a que termine la instalación. No desconectes Metalio.'),
 'help': ('Connection help', 'Ayuda de conexión'),
 'help_text': ('Disable USB disk mode on Metalio and close serial-terminal apps. Use a data cable. If automatic connection fails, hold the physical BOOT button while restarting Metalio, release it, then retry. BOOT is the GPIO0 hardware button, not the red on-screen key. Detection updates automatically. If several compatible devices are connected, leave only Metalio connected.', 'Desactiva Disco USB y cierra las aplicaciones de puerto serie. Usa un cable de datos. Si no conecta automáticamente, mantén el botón físico BOOT al reiniciar Metalio, suéltalo y reintenta. BOOT es el botón de hardware GPIO0, no el botón rojo de la pantalla. La detección se actualiza automáticamente. Si hay varios dispositivos compatibles, deja conectado solo el Metalio.'),
 'details': ('Details', 'Detalles'),
 'licenses': ('Licenses', 'Licencias'),
 'credit': ('Created by faga12@gmail.com', 'Creado por faga12@gmail.com'),
 'offline': ('Install/update require internet · Restore works offline', 'Instalar o actualizar requiere internet · Restaurar funciona sin conexión'),
}


def assets() -> Path:
    return Path(getattr(sys, '_MEIPASS', Path(__file__).resolve().parent)) / 'payload'


def verify_image(folder: Path, expected_version=None) -> Path:
    manifest = json.loads((folder / 'manifest.json').read_text(encoding='utf-8'))
    if ((expected_version is not None and manifest['version'] != expected_version)
            or not re.fullmatch(r'\d+\.\d+\.\d+', manifest['version'])
            or manifest['bytes'] != FLASH_BYTES):
        raise ValueError('Unexpected firmware version or size / Versión o tamaño incorrectos')
    image = folder / 'Metalio-instalacion-limpia.bin'
    if image.stat().st_size != FLASH_BYTES:
        raise ValueError('Incomplete firmware / Firmware incompleto')
    h = hashlib.sha256()
    with image.open('rb') as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b''):
            h.update(chunk)
    if h.hexdigest() != manifest['sha256']:
        raise ValueError('Firmware integrity check failed / Falló la verificación del firmware')
    return image


class Capture(io.TextIOBase):
    def __init__(self, emit):
        self.emit = emit
        self.parts = []
        self.tail = ''

    def write(self, value):
        self.parts.append(value)
        self.emit('log', value)
        self.tail = (self.tail + value)[-300:]
        matches = re.findall(r'\((\d+)\s*%\)', self.tail)
        if matches:
            self.emit('progress', min(99, 30 + int(matches[-1]) * .69))
        return len(value)

    def flush(self):
        pass

    def isatty(self):
        return False


def run_install(folder, port, emit, runner=None, expected_version=None, expected_mac=None):
    """Called only after UI confirmation. No filesystem or SD erase operations."""
    emit('stage', 'checking')
    image = verify_image(folder, expected_version)
    if runner is None:
        import esptool
        runner = esptool.main
    emit('progress', 25)
    emit('stage', 'connecting')
    probe = Capture(emit)
    # The --chip guard rejects non-S3 devices before any flash write.
    with contextlib.redirect_stdout(probe), contextlib.redirect_stderr(probe):
        runner(['--chip', 'esp32s3', '--port', port, '--after', 'no_reset', 'flash_id'])
    if not re.search(r'Detected flash size:\s*16MB\b', ''.join(probe.parts)):
        raise ValueError('A 16 MB flash chip is required. Nothing was written. / Se requiere flash de 16 MB. No se escribió nada.')
    if expected_mac is not None and device_ops.probe(port, emit, runner) != expected_mac:
        raise ValueError('Connected Metalio changed / Cambió el Metalio conectado')
    emit('stage', 'writing')
    emit('progress', 30)
    output = Capture(emit)
    with contextlib.redirect_stdout(output), contextlib.redirect_stderr(output):
        runner(['--chip', 'esp32s3', '--port', port, '--baud', '460800',
                'write_flash', '--flash_mode', 'dio', '--flash_freq', '80m',
                '--flash_size', '16MB', '0x0', str(image)])
    emit('progress', 100)
    emit('stage', 'done')


def matching_ports(ports):
    # macOS can expose callout and dial-in aliases for the same USB interface.
    return sorted({p.device.replace('/dev/tty.', '/dev/cu.', 1)
                   for p in ports if p.vid == 0x303a and p.pid == 0x1001})


def preferred_port(ports):
    candidates = matching_ports(ports)
    return candidates[0] if len(candidates) == 1 else ''


class Window:
    def __init__(self, root, scan=True):
        import tkinter as tk
        from tkinter import ttk
        self.root, self.tk, self.ttk = root, tk, ttk
        self.queue = queue.Queue()
        self.busy = False
        self.scan = scan
        self.device = None
        self.device_port = ''
        self.has_backup = False
        self.ignore_disconnect_until = 0.0
        self.language = tk.StringVar(value='English')
        self.port = tk.StringVar()
        self.make_backup = tk.BooleanVar(value=True)
        self.stage = 'none'
        self.rows = []
        font = 'Helvetica Neue' if sys.platform == 'darwin' else 'Segoe UI'
        root.title('DoceInk Setup')
        root.geometry('610x800')
        root.minsize(610, 800)
        root.configure(bg='#ffffff')
        root.protocol('WM_DELETE_WINDOW', self.close)
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('TFrame', background='white')
        style.configure('TLabel', background='white', font=(font, 11))
        style.configure('TButton', font=(font, 11), padding=(16, 10))
        style.configure('Install.TButton', background='#111111', foreground='white', font=(font, 12, 'bold'))
        style.map('Install.TButton', background=[('active', '#333333'), ('disabled', '#e4e4e4')], foreground=[('disabled', '#777777')])
        panel = ttk.Frame(root, padding=28)
        panel.pack(fill='both', expand=True)
        top = ttk.Frame(panel); top.pack(fill='x')
        self.lang = ttk.Combobox(top, textvariable=self.language, values=['English', 'Español'], state='readonly', width=12)
        self.lang.pack(side='right'); self.lang.bind('<<ComboboxSelected>>', lambda _: self.translate())
        try:
            self.icon = tk.PhotoImage(file=str(assets() / 'doceink-symbol.png')).subsample(2, 2)
            ttk.Label(panel, image=self.icon).pack(pady=(4, 10))
            root.iconphoto(True, self.icon)
        except tk.TclError:
            pass
        ttk.Label(panel, text='DoceInk', font=(font, 27, 'bold')).pack()
        self.subtitle = ttk.Label(panel); self.subtitle.pack(pady=(4, 10))
        self.compat = ttk.Label(panel, foreground='#555555'); self.compat.pack()
        self.firmware = ttk.Label(panel, text='Installer '+VERSION, foreground='#777777')
        self.firmware.pack(pady=(3, 14))
        self.connect = ttk.Label(panel); self.connect.pack(anchor='w')
        self.status = ttk.Label(panel, wraplength=545); self.status.pack(anchor='w', pady=(10, 10))
        self.progress = ttk.Progressbar(panel, maximum=100); self.progress.pack(fill='x')
        self.install = ttk.Button(panel, style='Install.TButton', command=self.start); self.install.pack(fill='x', pady=(12, 4))
        self.restore = ttk.Button(panel, command=self.start_restore); self.restore.pack(fill='x', pady=(4, 4))
        self.backup_option = ttk.Checkbutton(panel, variable=self.make_backup); self.backup_option.pack(anchor='w', pady=(4, 4))
        self.notice = ttk.Label(panel, wraplength=545, foreground='#555555', font=(font, 10)); self.notice.pack(anchor='w')
        self.backup_location = ttk.Label(panel, wraplength=545, foreground='#555555', font=(font, 9)); self.backup_location.pack(anchor='w', pady=(4, 0))
        self.offline = ttk.Label(panel, foreground='#777777', font=(font, 9)); self.offline.pack(anchor='w', pady=(10, 8))
        self.credit = ttk.Label(panel, foreground='#555555', font=(font, 10)); self.credit.pack(anchor='w', pady=(0, 12))
        bottom = ttk.Frame(panel); bottom.pack(fill='x')
        self.help = ttk.Button(bottom, command=self.show_help); self.help.pack(side='left')
        self.details = ttk.Button(bottom, command=self.show_details); self.details.pack(side='left', padx=8)
        self.licenses = ttk.Button(bottom, command=self.show_licenses); self.licenses.pack(side='right')
        self.log = ''
        self.translate()
        self.root.after(100, self.pump)
        if scan: self.root.after(100, self.scan_ports)

    def text(self, key):
        return TEXT[key][int(self.language.get() == 'Español')]

    def translate(self):
        self.root.title(self.text('title'))
        for name in ('subtitle','compat','connect','offline','help','details','licenses','credit','restore','backup_option'):
            getattr(self, name).configure(text=self.text(name))
        doceink = bool(self.device and self.device.get('kind') == 'doceink')
        unknown = self.scan and self.port.get() and not self.device
        self.install.configure(text=self.text('identify' if unknown else 'update' if doceink else 'install'))
        self.notice.configure(text=self.text('notice_update' if doceink else 'notice'))
        self.backup_location.configure(text=self.text('backup_location') + '\n' + str(device_ops.root_directory()))
        if doceink:
            self.backup_option.pack_forget()
        elif not self.backup_option.winfo_manager():
            self.backup_option.pack(anchor='w', pady=(4, 4), before=self.notice)
        self.status.configure(text=self.text(self.stage))
        ready = bool(self.port.get() and not self.busy and (self.device or not self.scan))
        self.install.configure(state='normal' if self.port.get() and not self.busy else 'disabled')
        self.restore.configure(state='normal' if ready and doceink and self.has_backup else 'disabled')
        self.backup_option.configure(state='normal' if ready and not doceink else 'disabled')

    def scan_ports(self):
        if not self.busy:
            self.refresh_detection()
        self.root.after(1500, self.scan_ports)

    def refresh_detection(self):
        from serial.tools.list_ports import comports
        try:
            ports = list(comports())
            detected = preferred_port(ports)
            if not detected and self.device and time.monotonic() < self.ignore_disconnect_until:
                return
            self.port.set(detected)
            if not detected:
                self.device = None
                self.device_port = ''
                self.has_backup = False
                self.stage = 'choose' if matching_ports(ports) else 'none'
            elif self.scan and detected != self.device_port:
                self.device = None
                self.has_backup = False
                self.device_port = detected
                self.busy = True
                self.stage = 'identifying'
                threading.Thread(target=self.inspect_worker, args=(detected,), daemon=True).start()
            elif not self.scan and self.stage not in ('done', 'error'):
                self.stage = 'ready'
        except Exception as exc:
            self.port.set('')
            self.stage = 'detect_error'
            self.log = (self.log + str(exc) + '\n')[-100000:]
        self.translate()

    def inspect_worker(self, port):
        emit = lambda kind, value: self.queue.put((kind, value))
        try:
            try:
                with tempfile.TemporaryDirectory(prefix='DoceInk-inspect-') as directory:
                    device = device_ops.inspect(port, Path(directory), emit)
                    has_backup = device_ops.backup_info(device['mac']) is not None
            finally:
                try: device_ops.run_tool(port, ['run'], emit)
                except (Exception, SystemExit): pass
            self.queue.put(('inspected', (port, device, has_backup)))
        except (Exception, SystemExit) as exc:
            self.queue.put(('log', '\n' + str(exc) + '\n'))
            self.queue.put(('inspection_failed', port))

    def start(self):
        from tkinter import messagebox
        if self.busy: return
        self.refresh_detection()
        if self.busy: return
        if not self.port.get(): return
        if self.scan and not self.device:
            self.device_port = ''
            self.refresh_detection()
            return
        doceink = bool(self.device and self.device.get('kind') == 'doceink')
        if not messagebox.askyesno(self.text('title'), self.text('confirm_update' if doceink else 'confirm'), parent=self.root, default='no'):
            return
        if not doceink and self.make_backup.get() and not self.has_backup:
            if not messagebox.askyesno(self.text('title'), self.text('confirm_backup'), parent=self.root, default='no'):
                return
        self.begin_operation('update' if doceink else 'install')

    def start_restore(self):
        from tkinter import messagebox
        if self.busy or not self.device or self.device.get('kind') != 'doceink' or not self.has_backup: return
        self.refresh_detection()
        if self.busy or not self.port.get() or not self.device: return
        if not messagebox.askyesno(self.text('title'), self.text('confirm_restore'), parent=self.root, default='no'):
            return
        self.begin_operation('restore')

    def begin_operation(self, action):
        self.busy = True
        port = self.port.get()
        expected = self.device['mac'] if self.device else None
        create_backup = self.make_backup.get()
        self.log = ''
        self.stage = 'connecting' if action == 'restore' else 'latest'
        self.progress['value'] = 0
        self.lang.configure(state='disabled')
        self.translate()
        threading.Thread(target=self.worker, args=(port, action, expected, create_backup), daemon=True).start()

    def worker(self, port, action='install', expected=None, create_backup=True):
        try:
            emit = lambda kind, value: self.queue.put((kind, value))
            with tempfile.TemporaryDirectory(prefix='DoceInk-') as directory:
                folder = Path(directory)
                from serial.tools.list_ports import comports
                version = None
                if action != 'restore':
                    # Always verify the latest complete image before touching flash.
                    version = download_latest(folder, emit)
                    verify_image(folder, version)
                if preferred_port(list(comports())) != port:
                    raise RuntimeError('USB connection changed. Reconnect only Metalio and retry. / La conexión USB cambió. Reconecta solo el Metalio y reintenta.')
                if action == 'restore':
                    device_ops.restore_backup(port, expected, emit)
                else:
                    state = device_ops.inspect(port, folder, emit)
                    if expected and state['mac'] != expected:
                        raise RuntimeError('Connected Metalio changed / Cambió el Metalio conectado')
                    if action == 'update':
                        device_ops.update_existing(port, state, folder, emit)
                    else:
                        if state['kind'] == 'doceink':
                            raise RuntimeError('DoceInk is already installed. Use Update. / DoceInk ya está instalado. Usa Actualizar.')
                        if create_backup and device_ops.backup_info(state['mac']) is None:
                            device_ops.save_backup(port, state['mac'], emit)
                        run_install(folder, port, emit, expected_version=version, expected_mac=state['mac'])
        except (Exception, SystemExit) as exc:
            self.queue.put(('log', '\n' + str(exc) + '\n'))
            self.queue.put(('stage','error'))
        finally:
            self.queue.put(('finished', None))

    def pump(self):
        try:
            while True:
                kind, value = self.queue.get_nowait()
                if kind == 'log': self.log = (self.log + value)[-100000:]
                elif kind == 'progress': self.progress['value'] = value
                elif kind == 'stage': self.stage = value; self.translate()
                elif kind == 'firmware': self.firmware.configure(text='Firmware '+value)
                elif kind == 'inspected':
                    port, device, backup = value
                    if self.port.get() == port:
                        self.device, self.has_backup = device, backup
                        self.stage = ('detected_doceink' if backup else 'detected_doceink_no_backup') if device['kind'] == 'doceink' else 'detected_original'
                    self.ignore_disconnect_until = time.monotonic() + 5
                    self.busy = False
                    self.translate()
                elif kind == 'inspection_failed':
                    if self.port.get() == value: self.stage = 'detect_error'
                    self.busy = False
                    self.translate()
                elif kind == 'finished':
                    self.busy = False
                    self.device = None
                    self.device_port = ''
                    self.ignore_disconnect_until = time.monotonic() + 5
                    self.lang.configure(state='readonly')
                    self.translate()
                    if self.stage == 'error': self.show_details()
        except queue.Empty:
            pass
        self.root.after(100, self.pump)

    def show_help(self):
        from tkinter import messagebox
        messagebox.showinfo(self.text('help'), self.text('help_text'), parent=self.root)

    def show_text(self, title, content):
        dialog = self.tk.Toplevel(self.root); dialog.title(title); dialog.geometry('640x400')
        field = self.tk.Text(dialog, wrap='word', font=('Consolas', 10)); field.pack(fill='both', expand=True, padx=12, pady=12)
        field.insert('1.0', content); field.configure(state='disabled')

    def show_details(self):
        self.show_text(self.text('details'), self.log or self.text('help_text'))

    def show_licenses(self):
        self.show_text(self.text('licenses'), (assets()/'THIRD-PARTY.txt').read_text(encoding='utf-8'))

    def close(self):
        from tkinter import messagebox
        if self.busy: messagebox.showinfo(self.text('title'), self.text('wait'), parent=self.root)
        else: self.root.destroy()


def main():
    # Test entry points never enumerate or open a serial port.
    if len(sys.argv) == 3 and sys.argv[1] == '--download-test':
        import os
        from functools import partial
        from download import open_url
        # CI uses an ephemeral read-only token to avoid shared-runner API limits.
        # The GUI does not read or require this token; none is bundled in the app.
        opener = partial(open_url, token=os.environ.get('DOCEINK_TEST_GITHUB_TOKEN'))
        with tempfile.TemporaryDirectory(prefix='DoceInk-check-') as directory:
            version = download_latest(directory, lambda *args: None, opener)
            image = verify_image(Path(directory), version)
            Path(sys.argv[2]).write_text(json.dumps({'version': version, 'bytes': image.stat().st_size, 'verified': True}), encoding='utf-8')
        return
    if len(sys.argv) == 3 and sys.argv[1] == '--self-test':
        import esptool
        from serial.tools import list_ports
        from esptool.loader import ESPLoader
        assert (assets() / 'doceink-symbol.png').is_file()
        assert (assets() / 'THIRD-PARTY.txt').is_file()
        from download import LATEST
        result = {'latest_endpoint': LATEST, 'esptool': esptool.__version__}
        # Load the exact ESP32-S3 stub resource the real installer will need.
        from esptool.targets.esp32s3 import ESP32S3ROM
        from esptool.loader import StubFlasher
        StubFlasher(ESP32S3ROM)
        result['esp32s3_stub'] = True
        Path(sys.argv[2]).write_text(json.dumps(result), encoding='utf-8')
        return
    import tkinter as tk
    root = tk.Tk()
    smoke = len(sys.argv) == 3 and sys.argv[1] == '--smoke-test'
    if smoke: root.withdraw()
    window = Window(root, scan=not smoke)
    if smoke:
        root.update()
        window.language.set('Español'); window.translate(); root.update()
        window.language.set('English'); window.translate(); root.update()
        Path(sys.argv[2]).write_text(json.dumps({'gui':True,'languages':['en','es']}),encoding='utf-8')
        root.destroy()
        return
    root.mainloop()

if __name__ == '__main__':
    main()
