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
from download import download_latest

VERSION = '0.75.149.1'
FLASH_BYTES = 16 * 1024 * 1024
TEXT = {
 'title': ('DoceInk Setup', 'Instalar DoceInk'),
 'subtitle': ('A fresh start for your Metalio.', 'Un nuevo comienzo para tu Metalio.'),
 'connect': ('Connect Metalio with a USB data cable.', 'Conecta Metalio con un cable USB de datos.'),
 'none': ('Waiting for Metalio…', 'Esperando a Metalio…'),
 'choose': ('Several compatible USB devices detected. Leave only Metalio connected.', 'Hay varios dispositivos USB compatibles. Deja conectado solo el Metalio.'),
 'detect_error': ('Could not detect Metalio. Check the USB connection.', 'No se pudo detectar Metalio. Revisa la conexión USB.'),
 'ready': ('Metalio connection detected. Ready to install.', 'Conexión de Metalio detectada. Listo para instalar.'),
 'install': ('Install DoceInk', 'Instalar DoceInk'),
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
 'offline': ('Downloads the latest firmware · Internet required', 'Descarga el firmware más reciente · Requiere internet'),
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


def run_install(folder, port, emit, runner=None, expected_version=None):
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
        self.language = tk.StringVar(value='English')
        self.port = tk.StringVar()
        self.stage = 'none'
        self.rows = []
        font = 'Helvetica Neue' if sys.platform == 'darwin' else 'Segoe UI'
        root.title('DoceInk Setup')
        root.geometry('610x720')
        root.minsize(610, 720)
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
        self.subtitle = ttk.Label(panel); self.subtitle.pack(pady=(4, 20))
        self.compat = ttk.Label(panel, foreground='#555555'); self.compat.pack()
        self.firmware = ttk.Label(panel, text='Installer '+VERSION, foreground='#777777')
        self.firmware.pack(pady=(3, 14))
        self.connect = ttk.Label(panel); self.connect.pack(anchor='w')
        self.status = ttk.Label(panel, wraplength=545); self.status.pack(anchor='w', pady=(16, 16))
        self.progress = ttk.Progressbar(panel, maximum=100); self.progress.pack(fill='x')
        self.install = ttk.Button(panel, style='Install.TButton', command=self.start); self.install.pack(fill='x', pady=(16, 12))
        self.notice = ttk.Label(panel, wraplength=545, foreground='#555555', font=(font, 10)); self.notice.pack(anchor='w')
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
        for name in ('subtitle','compat','connect','install','notice','offline','help','details','licenses','credit'):
            getattr(self, name).configure(text=self.text(name))
        self.status.configure(text=self.text(self.stage))
        self.install.configure(state='normal' if self.port.get() and not self.busy else 'disabled')

    def scan_ports(self):
        if not self.busy:
            self.refresh_detection()
        self.root.after(1500, self.scan_ports)

    def refresh_detection(self):
        from serial.tools.list_ports import comports
        try:
            ports = list(comports())
            self.port.set(preferred_port(ports))
            if self.stage not in ('done', 'error'):
                self.stage = 'ready' if self.port.get() else ('choose' if matching_ports(ports) else 'none')
        except Exception as exc:
            self.port.set('')
            self.stage = 'detect_error'
            self.log = (self.log + str(exc) + '\n')[-100000:]
        self.translate()

    def start(self):
        from tkinter import messagebox
        if self.busy: return
        self.refresh_detection()
        if not self.port.get(): return
        if not messagebox.askyesno(self.text('title'), self.text('confirm'), parent=self.root, default='no'):
            return
        self.busy = True
        port = self.port.get()
        self.log = ''
        self.stage = 'latest'
        self.progress['value'] = 0
        self.lang.configure(state='disabled')
        self.translate()
        threading.Thread(target=self.worker, args=(port,), daemon=True).start()

    def worker(self, port):
        try:
            emit = lambda kind, value: self.queue.put((kind, value))
            # Every installation fetches latest anew; no bundled or cached fallback.
            with tempfile.TemporaryDirectory(prefix='DoceInk-') as directory:
                folder = Path(directory)
                version = download_latest(folder, emit)
                from serial.tools.list_ports import comports
                if preferred_port(list(comports())) != port:
                    raise RuntimeError('USB connection changed. Reconnect only Metalio and retry. / La conexión USB cambió. Reconecta solo el Metalio y reintenta.')
                run_install(folder, port, emit, expected_version=version)
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
                elif kind == 'finished':
                    self.busy = False
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
        with tempfile.TemporaryDirectory(prefix='DoceInk-check-') as directory:
            version = download_latest(directory, lambda *args: None)
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
