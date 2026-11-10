"""DoceInk Windows installer. MIT; bundled tools retain their own licenses."""
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

VERSION = '0.75.146'
FLASH_BYTES = 16 * 1024 * 1024
TEXT = {
 'title': ('DoceInk Setup', 'Instalar DoceInk'),
 'subtitle': ('A fresh start for your Metalio.', 'Un nuevo comienzo para tu Metalio.'),
 'connect': ('Connect Metalio with a USB data cable.', 'Conecta Metalio con un cable USB de datos.'),
 'device': ('Device', 'Dispositivo'),
 'none': ('Waiting for Metalio…', 'Esperando a Metalio…'),
 'choose': ('Choose your Metalio from the list.', 'Selecciona tu Metalio en la lista.'),
 'ready': ('Metalio connection detected. Ready to install.', 'Conexión de Metalio detectada. Listo para instalar.'),
 'install': ('Install DoceInk', 'Instalar DoceInk'),
 'notice': ('Clean installation · Internal accounts and settings will be erased.\nYour microSD card is not erased. Wi-Fi updates preserve your data.', 'Instalación limpia · Se borrarán cuentas y ajustes internos.\nLa microSD no se borra. Las actualizaciones Wi-Fi conservan tus datos.'),
 'compat': ('Only for Metalio E-Ink4 · ESP32-S3 · 16 MB flash', 'Solo para Metalio E-Ink4 · ESP32-S3 · flash de 16 MB'),
 'confirm': ('Install on {port}?\n\nThis replaces all internal firmware, accounts, Wi-Fi networks and settings. It does not erase the microSD card.\n\nConfirm that the connected device is a Metalio E-Ink4. Keep the cable connected until installation finishes.', '¿Instalar en {port}?\n\nSe reemplazarán el firmware, las cuentas, redes Wi-Fi y ajustes internos. La microSD no se borra.\n\nConfirma que conectaste un Metalio E-Ink4. Mantén el cable conectado hasta que termine.'),
 'checking': ('Checking the included firmware…', 'Comprobando el firmware incluido…'),
 'connecting': ('Connecting and checking hardware…', 'Conectando y comprobando el hardware…'),
 'writing': ('Installing… Keep USB connected.', 'Instalando… Mantén el USB conectado.'),
 'done': ('Installation complete. Metalio is restarting.', 'Instalación terminada. Metalio se está reiniciando.'),
 'error': ('Installation could not finish. See details below.', 'No se pudo completar la instalación. Revisa los detalles.'),
 'wait': ('Please wait until installation finishes. Do not unplug Metalio.', 'Espera a que termine la instalación. No desconectes Metalio.'),
 'help': ('Connection help', 'Ayuda de conexión'),
 'help_text': ('Disable USB disk mode on Metalio and close serial-terminal apps. Use a data cable. If automatic connection fails, hold the physical BOOT button while restarting Metalio, release it, then retry. BOOT is the GPIO0 hardware button, not the red on-screen key. The port may change. If several devices are listed, disconnect the others or select your Metalio.', 'Desactiva Disco USB y cierra las aplicaciones de puerto serie. Usa un cable de datos. Si no conecta automáticamente, mantén el botón físico BOOT al reiniciar Metalio, suéltalo y reintenta. BOOT es el botón de hardware GPIO0, no el botón rojo de la pantalla. El puerto puede cambiar. Si aparecen varios dispositivos, desconecta los demás o selecciona tu Metalio.'),
 'details': ('Details', 'Detalles'),
 'licenses': ('Licenses', 'Licencias'),
 'offline': ('Firmware included · No Python or commands required', 'Firmware incluido · Sin Python ni comandos'),
}


def assets() -> Path:
    return Path(getattr(sys, '_MEIPASS', Path(__file__).resolve().parent)) / 'payload'


def verify_image(folder: Path) -> Path:
    manifest = json.loads((folder / 'manifest.json').read_text(encoding='utf-8'))
    if manifest['version'] != VERSION or manifest['bytes'] != FLASH_BYTES:
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
            self.emit('progress', min(99, 10 + int(matches[-1]) * .89))
        return len(value)

    def flush(self):
        pass

    def isatty(self):
        return False


def run_install(folder, port, emit, runner=None):
    """Called only after UI confirmation. No filesystem or SD erase operations."""
    emit('stage', 'checking')
    image = verify_image(folder)
    if runner is None:
        import esptool
        runner = esptool.main
    emit('progress', 3)
    emit('stage', 'connecting')
    probe = Capture(emit)
    # The --chip guard rejects non-S3 devices before any flash write.
    with contextlib.redirect_stdout(probe), contextlib.redirect_stderr(probe):
        runner(['--chip', 'esp32s3', '--port', port, '--after', 'no_reset', 'flash_id'])
    if not re.search(r'Detected flash size:\s*16MB\b', ''.join(probe.parts)):
        raise ValueError('A 16 MB flash chip is required. Nothing was written. / Se requiere flash de 16 MB. No se escribió nada.')
    emit('stage', 'writing')
    emit('progress', 10)
    output = Capture(emit)
    with contextlib.redirect_stdout(output), contextlib.redirect_stderr(output):
        runner(['--chip', 'esp32s3', '--port', port, '--baud', '460800',
                'write_flash', '--flash_mode', 'dio', '--flash_freq', '80m',
                '--flash_size', '16MB', '0x0', str(image)])
    emit('progress', 100)
    emit('stage', 'done')


def preferred_port(ports):
    candidates = [p.device for p in ports if p.vid == 0x303a and p.pid == 0x1001]
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
        root.title('DoceInk Setup')
        root.geometry('610x720')
        root.minsize(610, 720)
        root.configure(bg='#ffffff')
        root.protocol('WM_DELETE_WINDOW', self.close)
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('TFrame', background='white')
        style.configure('TLabel', background='white', font=('Segoe UI', 11))
        style.configure('TButton', font=('Segoe UI', 11), padding=(16, 10))
        style.configure('Install.TButton', background='#111111', foreground='white', font=('Segoe UI Semibold', 12))
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
        ttk.Label(panel, text='DoceInk', font=('Segoe UI Semibold', 27)).pack()
        self.subtitle = ttk.Label(panel); self.subtitle.pack(pady=(4, 20))
        self.compat = ttk.Label(panel, foreground='#555555'); self.compat.pack()
        ttk.Label(panel, text=VERSION, foreground='#777777').pack(pady=(3, 14))
        self.connect = ttk.Label(panel); self.connect.pack(anchor='w')
        self.select = ttk.Combobox(panel, textvariable=self.port, state='readonly')
        self.select.pack(fill='x', pady=(8, 12)); self.select.bind('<<ComboboxSelected>>', lambda _: self.port_changed())
        self.status = ttk.Label(panel, wraplength=545); self.status.pack(anchor='w', pady=(0, 8))
        self.progress = ttk.Progressbar(panel, maximum=100); self.progress.pack(fill='x')
        self.install = ttk.Button(panel, style='Install.TButton', command=self.start); self.install.pack(fill='x', pady=(16, 12))
        self.notice = ttk.Label(panel, wraplength=545, foreground='#555555', font=('Segoe UI', 10)); self.notice.pack(anchor='w')
        self.offline = ttk.Label(panel, foreground='#777777', font=('Segoe UI', 9)); self.offline.pack(anchor='w', pady=(10, 8))
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
        for name in ('subtitle','compat','connect','install','notice','offline','help','details','licenses'):
            getattr(self, name).configure(text=self.text(name))
        self.status.configure(text=self.text(self.stage))
        self.install.configure(state='normal' if self.port.get() and not self.busy else 'disabled')

    def scan_ports(self):
        if not self.busy:
            from serial.tools.list_ports import comports
            try:
                ports = list(comports())
                values = [p.device for p in ports]
                self.select.configure(values=values)
                if self.port.get() not in values:
                    self.port.set(preferred_port(ports))
                elif not self.port.get():
                    self.port.set(preferred_port(ports))
                if self.stage not in ('done','error'):
                    self.stage = 'ready' if self.port.get() else ('choose' if values else 'none')
                self.translate()
            except Exception as exc:
                self.log += str(exc) + '\n'
        self.root.after(1500, self.scan_ports)

    def port_changed(self):
        self.stage = 'ready' if self.port.get() else 'none'; self.translate()

    def start(self):
        from tkinter import messagebox
        if self.busy or not self.port.get(): return
        if not messagebox.askyesno(self.text('title'), self.text('confirm').format(port=self.port.get()), parent=self.root, default='no'):
            return
        self.busy = True
        port = self.port.get()
        self.log = ''
        self.stage = 'checking'
        self.progress['value'] = 0
        self.select.configure(state='disabled')
        self.lang.configure(state='disabled')
        self.translate()
        threading.Thread(target=self.worker, args=(port,), daemon=True).start()

    def worker(self, port):
        try:
            run_install(assets(), port, lambda kind, value: self.queue.put((kind, value)))
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
                elif kind == 'finished':
                    self.busy = False
                    self.select.configure(state='readonly'); self.lang.configure(state='readonly')
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
    if len(sys.argv) == 3 and sys.argv[1] == '--self-test':
        import esptool
        from serial.tools import list_ports
        from esptool.loader import ESPLoader
        verify_image(assets())
        result = {'image_integrity': True, 'esptool': esptool.__version__}
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
