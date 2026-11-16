"""Small bilingual Wi-Fi linking dialog. Worker results contain no secrets."""
import queue
import threading
import tkinter as tk
from tkinter import ttk
import account_link

TEXT = {
 'title': ('Link accounts', 'Vincular cuentas'),
 'instructions': ('On Metalio, open AI Usage → account → Link. Paste the temporary QR link here. This computer and Metalio must use the same trusted Wi-Fi.', 'En Metalio, abre Consumo de IA → cuenta → Vincular. Pega aquí el enlace temporal del QR. Este ordenador y Metalio deben estar en el mismo Wi-Fi de confianza.'),
 'label': ('Metalio link', 'Enlace del Metalio'),
 'paste': ('Paste', 'Pegar'),
 'explanation': ('Setup finds the selected account in the local Codex or Claude Code session files and sends only its access to Metalio. No JSON export or USB connection is needed.', 'Setup busca la cuenta elegida en los archivos de sesión locales de Codex o Claude Code y envía solo su acceso a Metalio. No necesitas exportar JSON ni conectar USB.'),
 'send': ('Link', 'Vincular'),
 'close': ('Close', 'Cerrar'),
 'working': ('Linking…', 'Vinculando…'),
 'done_codex': ('ChatGPT · Codex linked. Metalio will refresh the widget.', 'ChatGPT · Codex vinculado. Metalio actualizará el widget.'),
 'done_claude': ('Claude linked. Metalio will refresh the widget.', 'Claude vinculado. Metalio actualizará el widget.'),
 'invalid_link': ('Paste the complete temporary QR link from Metalio.', 'Pega el enlace temporal completo del QR del Metalio.'),
 'wrong_link': ('This is not an AI Usage link. Open Link on the Metalio account again.', 'Este enlace no es de Consumo de IA. Abre otra vez Vincular en la cuenta del Metalio.'),
 'expired_link': ('The link expired or was already used. Open a new QR on Metalio.', 'El enlace caducó o ya se usó. Abre un QR nuevo en Metalio.'),
 'missing': ('No compatible local session file was found. Sign in to Codex or Claude Code on this computer. Sessions stored only in an OS vault are not imported by this version.', 'No se encontró un archivo de sesión local compatible. Inicia sesión en Codex o Claude Code en este ordenador. Esta versión no importa sesiones guardadas solo en el llavero del sistema.'),
 'invalid_session': ('The local session is not compatible. Open Codex or Claude Code and sign in again.', 'La sesión local no es compatible. Abre Codex o Claude Code e inicia sesión de nuevo.'),
 'scope': ('This Claude session does not allow profile access. Sign in again in Claude Code.', 'Esta sesión de Claude no permite consultar el perfil. Inicia sesión nuevamente en Claude Code.'),
 'expired': ('The local session expired. Renew it in Claude Code, then try again.', 'La sesión local caducó. Renuévala en Claude Code y vuelve a intentarlo.'),
 'network': ('Could not connect. Check Wi-Fi and leave the Metalio QR open.', 'No se pudo conectar. Revisa el Wi-Fi y deja abierto el QR del Metalio.'),
 'save': ('Metalio could not save the access. Check microSD, disable USB Disk and open a new QR before retrying.', 'Metalio no pudo guardar el acceso. Revisa la microSD, desactiva Disco USB y abre un QR nuevo antes de reintentar.'),
 'cancelled': ('Cancelled.', 'Cancelado.'),
}


class AccountLinkDialog:
    def __init__(self, parent, spanish=False, on_close=lambda: None):
        self.spanish, self.on_close = spanish, on_close
        self.closed = self.busy = False
        self.cancel = threading.Event()
        self.queue = queue.Queue()
        self.window = tk.Toplevel(parent)
        self.window.title(self.text('title'))
        self.window.geometry('550x430')
        self.window.minsize(500, 400)
        self.window.transient(parent)
        self.window.configure(bg='white')
        self.window.protocol('WM_DELETE_WINDOW', self.close)
        self.window.bind('<Destroy>', self.destroyed, add='+')
        self.window.bind('<Escape>', lambda _: self.close())
        if parent.winfo_viewable(): self.window.grab_set()
        panel = ttk.Frame(self.window, padding=24); panel.pack(fill='both', expand=True)
        ttk.Label(panel, text=self.text('instructions'), wraplength=490).pack(fill='x', pady=(0, 16))
        ttk.Label(panel, text=self.text('label')).pack(anchor='w')
        row = ttk.Frame(panel); row.pack(fill='x', pady=(4, 12))
        self.url = tk.StringVar()
        self.entry = ttk.Entry(row, textvariable=self.url); self.entry.pack(side='left', fill='x', expand=True)
        self.paste = ttk.Button(row, text=self.text('paste'), command=self.paste_link); self.paste.pack(side='right', padx=(8, 0))
        ttk.Label(panel, text=self.text('explanation'), wraplength=490, foreground='#555555').pack(fill='x')
        self.status = ttk.Label(panel, text='', wraplength=490); self.status.pack(fill='x', pady=16, expand=True)
        actions = ttk.Frame(panel); actions.pack(fill='x')
        self.send = ttk.Button(actions, text=self.text('send'), style='Install.TButton', command=self.start); self.send.pack(side='left', fill='x', expand=True, padx=(0, 4))
        ttk.Button(actions, text=self.text('close'), command=self.close).pack(side='right', fill='x', expand=True, padx=(4, 0))
        self.entry.focus_set()
        self.timer = self.window.after(100, self.pump)

    def text(self, key):
        return TEXT[key][int(self.spanish)]

    def paste_link(self):
        if self.busy: return
        try: self.url.set(self.window.clipboard_get().strip())
        except tk.TclError: self.status.configure(text=self.text('invalid_link'))

    def start(self):
        if self.busy or self.closed: return
        value = self.url.get()
        try: account_link.parse_link(value)
        except account_link.LinkError as error:
            self.status.configure(text=self.text(error.code)); return
        self.busy = True
        self.status.configure(text=self.text('working'))
        for control in (self.entry, self.paste, self.send): control.configure(state='disabled')
        threading.Thread(target=self.worker, args=(value,), daemon=True).start()

    def worker(self, value):
        try: self.queue.put(('done', account_link.link_account(value, cancelled=self.cancel.is_set)))
        except account_link.LinkError as error: self.queue.put(('error', error.code))
        except Exception: self.queue.put(('error', 'network'))  # No exception text in GUI or logs.

    def pump(self):
        if self.closed: return
        try:
            while True:
                kind, value = self.queue.get_nowait()
                self.busy = False
                if kind == 'done':
                    self.url.set('')
                    self.status.configure(text=self.text('done_'+value))
                else:
                    self.status.configure(text=self.text(value))
                    for control in (self.entry, self.paste, self.send): control.configure(state='normal')
        except queue.Empty: pass
        self.timer = self.window.after(100, self.pump)

    def close(self):
        if self.closed: return
        self.closed = True
        self.cancel.set()
        self.url.set('')
        try: self.window.after_cancel(self.timer)
        except tk.TclError: pass
        self.window.destroy()
        self.on_close()

    def destroyed(self, event):
        if event.widget != self.window or self.closed: return
        self.closed = True
        self.cancel.set()
        try: self.window.after_cancel(self.timer)
        except tk.TclError: pass
        self.on_close()
