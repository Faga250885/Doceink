"""Opt-in local session import into Metalio. Never logs or writes credentials.

Only the provider selected by Metalio's temporary pairing page is read.
No provider login, refresh, keychain extraction or recursive file search.
"""
from __future__ import annotations
from dataclasses import dataclass, field
import ipaddress
import json
import os
from pathlib import Path
import re
import time
import urllib.error
import urllib.parse
import urllib.request


class LinkError(Exception):
    def __init__(self, code):
        self.code = code
        super().__init__(code)  # Fixed codes only: never include paths or tokens.


@dataclass(frozen=True)
class PairLink:
    url: str = field(repr=False)
    host: str


def parse_link(value):
    if not isinstance(value, str):
        raise LinkError('invalid_link')
    value = value.strip()
    if len(value) > 160 or any(ord(c) < 33 for c in value):
        raise LinkError('invalid_link')
    try:
        p = urllib.parse.urlsplit(value)
        host = ipaddress.IPv4Address(p.hostname or '')
        allowed = any(host in ipaddress.ip_network(net) for net in
                      ('10.0.0.0/8', '172.16.0.0/12', '192.168.0.0/16'))
        if (not allowed or p.scheme != 'http' or p.port != 8765 or
                p.username is not None or p.password is not None or
                p.path != '/' or p.fragment or not re.fullmatch(r't=[a-f0-9]{32}', p.query)):
            raise ValueError
    except (ValueError, TypeError):
        raise LinkError('invalid_link') from None
    return PairLink(value, str(host))


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        raise LinkError('wrong_link')


def local_open(request):
    # Never send the session through a configured HTTP proxy or a redirect.
    return urllib.request.build_opener(urllib.request.ProxyHandler({}), NoRedirect()).open(request, timeout=8)


def header_value(value, minimum, maximum):
    return isinstance(value, str) and minimum <= len(value) <= maximum and re.fullmatch(r'[A-Za-z0-9_.+/=\-]+', value) is not None


def extract_session(provider, document, now=None):
    if provider not in ('codex', 'claude') or not isinstance(document, dict):
        raise LinkError('invalid_session')
    source = document.get(provider) or document.get('tokens' if provider == 'codex' else 'claudeAiOauth')
    if not isinstance(source, dict):
        raise LinkError('invalid_session')
    token = source.get('access_token') or source.get('accessToken')
    if (not header_value(token, 20, 8192) or token.startswith(('sk-ant-api', 'sk-ant-admin'))
            or (provider == 'codex' and token.startswith('sk-'))):
        raise LinkError('invalid_session')
    if provider == 'claude':
        scopes = source.get('scopes')
        if isinstance(scopes, list) and 'user:profile' not in scopes:
            raise LinkError('scope')
        expires = source.get('expiresAt')
        if isinstance(expires, (float, int)) and not isinstance(expires, bool):
            if expires > 100_000_000_000:
                expires /= 1000
            if expires <= (time.time() if now is None else now):
                raise LinkError('expired')
    result = {'access_token': token}
    if provider == 'codex' and 'account_id' in source:
        if not header_value(source['account_id'], 1, 128):
            raise LinkError('invalid_session')
        result['account_id'] = source['account_id']
    return {provider: result}


def session_path(provider, home=None, environ=None):
    if provider not in ('codex', 'claude'):
        raise LinkError('invalid_session')
    env = os.environ if environ is None else environ
    home = Path.home() if home is None else Path(home)
    variable, default, name = (('CODEX_HOME', '.codex', 'auth.json') if provider == 'codex'
                               else ('CLAUDE_CONFIG_DIR', '.claude', '.credentials.json'))
    folder = Path(env[variable]).expanduser() if env.get(variable) else home / default
    return folder / name


def load_session(provider, home=None, environ=None):
    try:
        with session_path(provider, home, environ).open('rb') as source:
            raw = source.read(1024 * 1024 + 1)
        if len(raw) > 1024 * 1024:
            raise LinkError('invalid_session')
        document = json.loads(raw.decode('utf-8-sig'))
    except FileNotFoundError:
        raise LinkError('missing') from None
    except (OSError, UnicodeError, ValueError, RecursionError):
        raise LinkError('invalid_session') from None
    return extract_session(provider, document)


def link_account(value, *, opener=local_open, loader=load_session, cancelled=lambda: False):
    link = parse_link(value)
    def check_cancelled():
        if cancelled():
            raise LinkError('cancelled')
    try:
        check_cancelled()
        request = urllib.request.Request(link.url, headers={'Cache-Control': 'no-store', 'User-Agent': 'DoceInk-Setup-Link/1'})
        with opener(request) as response:
            page = response.read(16 * 1024 + 1)
        if len(page) > 16 * 1024:
            raise LinkError('wrong_link')
        text = page.decode('utf-8')
        matches = re.findall(r"const p='(codex|claude)',file=", text)
        if len(matches) != 1 or 'id="file"' not in text or 'AI_USAGE' in text:
            raise LinkError('wrong_link')
        provider = matches[0]
        check_cancelled()
        # Re-validate the loader's result, even if a future storage backend changes.
        payload = json.dumps(extract_session(provider, loader(provider)), separators=(',', ':')).encode()
        check_cancelled()
        request = urllib.request.Request(link.url, data=payload, method='POST', headers={
            'Content-Type': 'application/json', 'Cache-Control': 'no-store', 'User-Agent': 'DoceInk-Setup-Link/1'})
        with opener(request) as response:
            if response.read(128) != b'OK':
                raise LinkError('save')
        return provider
    except LinkError:
        raise
    except urllib.error.HTTPError as error:
        code = 'expired_link' if error.code == 403 else 'save'
        error.close()
        raise LinkError(code) from None
    except (OSError, ValueError, UnicodeError, RecursionError):
        raise LinkError('network') from None
