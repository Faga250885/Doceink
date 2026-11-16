import io
import json
from pathlib import Path
import tempfile
import threading
import unittest
from unittest.mock import patch
import urllib.error
import urllib.request
import account_link as a

TOKEN = 'test-session-12345678901234567890'
URL = 'http://192.168.1.2:8765/?t='+'a'*32


def page(provider='codex'):
    return ('<input id="file" type="file"><script>const p=\''+provider+"',file=document.getElementById('file');</script>").encode()


class LinkTests(unittest.TestCase):
    def test_only_local_metalio_pairing_urls(self):
        self.assertEqual(a.parse_link(URL).host, '192.168.1.2')
        self.assertNotIn('a'*32, repr(a.parse_link(URL)))
        for value in [None, '', URL.replace('http:', 'https:'), URL.replace(':8765', ':80'),
                      URL.replace('192.168.1.2', '8.8.8.8'), URL.replace('192.168.1.2', 'localhost'),
                      URL.replace('192.168.1.2', '127.0.0.1'), URL.replace('192.168.1.2', '0.0.0.0'),
                      URL.replace('192.168.1.2', 'evil.example'), URL.replace('192.168.1.2', 'user@192.168.1.2'),
                      URL+'#fragment', URL+'&key=secret', URL.replace('/?', '/other?'), URL+'\nHost: evil']:
            with self.subTest(value=value), self.assertRaises(a.LinkError) as error:
                a.parse_link(value)
            self.assertEqual(str(error.exception), 'invalid_link')

    def test_minimal_export_only_for_selected_provider(self):
        document = {'tokens': {'access_token': TOKEN, 'account_id': 'personal-123', 'refresh_token': 'private', 'id_token': 'private'}, 'password': 'private'}
        self.assertEqual(a.extract_session('codex', document), {'codex': {'access_token': TOKEN, 'account_id': 'personal-123'}})
        self.assertEqual(a.extract_session('claude', {'claudeAiOauth': {'accessToken': TOKEN, 'refreshToken': 'private', 'scopes': ['user:profile']}}), {'claude': {'access_token': TOKEN}})
        for provider, value, code in [('codex', {'tokens': {'access_token': 'sk-project-12345678901234567890'}}, 'invalid_session'),
                ('codex', {'tokens': {'access_token': TOKEN+'\r\nx:bad'}}, 'invalid_session'),
                ('codex', {'tokens': {'access_token': TOKEN, 'account_id': 'bad\naccount'}}, 'invalid_session'),
                ('claude', {'claudeAiOauth': {'accessToken': TOKEN, 'scopes': ['user:inference']}}, 'scope'),
                ('claude', {'claudeAiOauth': {'accessToken': TOKEN, 'expiresAt': 1000}}, 'expired'),
                ('claude', {'claudeAiOauth': {'accessToken': 'sk-ant-api03-12345678901234567890'}}, 'invalid_session')]:
            with self.assertRaises(a.LinkError) as error: a.extract_session(provider, value, now=2000)
            self.assertEqual(error.exception.code, code)

    def test_standard_and_custom_directories_without_search_or_writes(self):
        with tempfile.TemporaryDirectory() as tmp:
            home = Path(tmp)
            for name in ['.codex', '.claude', 'work']: (home/name).mkdir()
            (home/'.codex/auth.json').write_text(json.dumps({'tokens': {'access_token': TOKEN}}))
            (home/'work/.credentials.json').write_text(json.dumps({'claudeAiOauth': {'accessToken': TOKEN}}))
            original = {f: f.read_bytes() for f in home.rglob('*') if f.is_file()}
            self.assertEqual(a.load_session('codex', home, {}), {'codex': {'access_token': TOKEN}})
            self.assertEqual(a.load_session('claude', home, {'CLAUDE_CONFIG_DIR': str(home/'work')}), {'claude': {'access_token': TOKEN}})
            with self.assertRaises(a.LinkError) as error: a.load_session('claude', home, {})
            self.assertEqual(error.exception.code, 'missing')
            self.assertEqual({f: f.read_bytes() for f in home.rglob('*') if f.is_file()}, original)

    def test_bad_local_file_does_not_expose_its_contents(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp)/'.codex';path.mkdir()
            (path/'auth.json').write_text('PRIVATE-INVALID-JSON')
            with self.assertRaises(a.LinkError) as error: a.load_session('codex', tmp, {})
            self.assertEqual(str(error.exception), 'invalid_session')

    def test_direct_get_then_selected_account_post(self):
        requests = []
        def opener(req):
            requests.append(req)
            return io.BytesIO(page('claude') if req.get_method() == 'GET' else b'OK')
        def loader(provider):
            self.assertEqual(provider, 'claude')
            return {'claude': {'access_token': TOKEN, 'refresh_token': 'must-not-leave'}, 'codex': {'access_token': 'must-not-leave'}}
        self.assertEqual(a.link_account(URL, opener=opener, loader=loader), 'claude')
        self.assertEqual([r.full_url for r in requests], [URL, URL])
        self.assertEqual([r.get_method() for r in requests], ['GET', 'POST'])
        self.assertEqual(json.loads(requests[1].data), {'claude': {'access_token': TOKEN}})
        self.assertNotIn('must-not-leave', requests[1].data.decode())
        self.assertNotIn('Authorization', requests[1].headers)

    def test_wrong_link_or_expiry_never_reads_local_credentials(self):
        for content in [b'<form>API key setup</form>', page()+page(), b'x'*16385]:
            with patch.object(a, 'load_session') as load:
                with self.assertRaises(a.LinkError): a.link_account(URL, opener=lambda r: io.BytesIO(content), loader=load)
                load.assert_not_called()
        def expired(req): raise urllib.error.HTTPError(URL, 403, 'SECRET', None, None)
        with patch.object(a, 'load_session') as load:
            with self.assertRaises(a.LinkError) as error: a.link_account(URL, opener=expired, loader=load)
            self.assertEqual(str(error.exception), 'expired_link');load.assert_not_called()

    def test_cancel_before_read_and_before_send(self):
        cancelled = threading.Event()
        def opener(req): cancelled.set();return io.BytesIO(page())
        with patch.object(a, 'load_session') as load:
            with self.assertRaises(a.LinkError): a.link_account(URL, opener=opener, loader=load, cancelled=cancelled.is_set)
            load.assert_not_called()
        cancelled.clear();requests=[]
        def read(provider): cancelled.set();return {'codex': {'access_token': TOKEN}}
        def get(req): requests.append(req);return io.BytesIO(page())
        with self.assertRaises(a.LinkError): a.link_account(URL, opener=get, loader=read, cancelled=cancelled.is_set)
        self.assertEqual(len(requests), 1)

    def test_network_errors_and_rejected_saves_are_sanitized(self):
        def failed(req): raise OSError('SECRET-'+TOKEN)
        with self.assertRaises(a.LinkError) as error: a.link_account(URL, opener=failed)
        self.assertEqual(str(error.exception), 'network')
        def no(req): return io.BytesIO(page() if req.get_method() == 'GET' else b'Not saved')
        with self.assertRaises(a.LinkError) as error: a.link_account(URL, opener=no, loader=lambda p: {'codex': {'access_token': TOKEN}})
        self.assertEqual(str(error.exception), 'save')

    def test_no_proxy_or_redirects(self):
        with patch.object(urllib.request, 'build_opener') as build:
            a.local_open(urllib.request.Request(URL))
            handlers = build.call_args.args
            self.assertTrue(any(isinstance(h, urllib.request.ProxyHandler) and h.proxies == {} for h in handlers))
        with self.assertRaises(a.LinkError): a.NoRedirect().redirect_request(None, None, 302, '', {}, 'https://evil.example')


class DialogTests(unittest.TestCase):
    def test_dialog_sends_only_on_click_and_closes_without_loading(self):
        import tkinter as tk
        from account_link_ui import AccountLinkDialog
        root=tk.Tk();root.withdraw()
        with patch.object(a, 'link_account') as run:
            dialog=AccountLinkDialog(root, spanish=True)
            dialog.url.set(URL);root.update();run.assert_not_called()
            dialog.close();run.assert_not_called()
            self.assertTrue(dialog.cancel.is_set())
        root.destroy()

    def test_dialog_worker_queue_never_contains_session_or_url(self):
        import queue
        from account_link_ui import AccountLinkDialog
        dialog=object.__new__(AccountLinkDialog);dialog.cancel=threading.Event();dialog.queue=queue.Queue()
        with patch.object(a, 'link_account', return_value='claude'):
            dialog.worker(URL)
        self.assertEqual(list(dialog.queue.queue), [('done','claude')])
        with patch.object(a, 'link_account', side_effect=OSError(TOKEN)):
            dialog.worker(URL)
        self.assertEqual(list(dialog.queue.queue)[-1], ('error','network'))

if __name__ == '__main__': unittest.main()
