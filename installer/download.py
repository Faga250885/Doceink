"""Fetch a complete, verified clean image from the latest public release."""
import hashlib
import json
from pathlib import Path
import re
import time
import sys
import urllib.request
import urllib.parse
import zipfile

REPO = 'Faga250885/Doceink'
LATEST = f'https://api.github.com/repos/{REPO}/releases/latest'
MAX_PACKAGE = 32 * 1024 * 1024
FLASH_BYTES = 16 * 1024 * 1024
IMAGE = 'Metalio-instalacion-limpia.bin'


def allowed_url(url):
    parsed = urllib.parse.urlsplit(url)
    return (parsed.scheme == 'https' and parsed.port in (None, 443)
            and not parsed.username and not parsed.password
            and parsed.hostname in ('api.github.com', 'github.com',
                                    'release-assets.githubusercontent.com',
                                    'objects.githubusercontent.com'))


class GitHubRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, request, fp, code, msg, headers, newurl):
        if not allowed_url(newurl):
            raise ValueError('Unexpected download redirect / Redirección no permitida')
        return super().redirect_request(request, fp, code, msg, headers, newurl)


def open_url(url, token=None):
    if not allowed_url(url):
        raise ValueError('Unexpected download host / Servidor no permitido')
    request = urllib.request.Request(url, headers={
        'User-Agent': 'DoceInk-Setup', 'Accept': 'application/vnd.github+json',
        'Cache-Control': 'no-cache', 'X-GitHub-Api-Version': '2022-11-28'})
    if token and urllib.parse.urlsplit(url).hostname == 'api.github.com':
        # CI download test only: never forward credentials on release-asset redirects.
        request.add_unredirected_header('Authorization', 'Bearer ' + token)
    handlers = [GitHubRedirect()]
    if sys.platform == 'darwin':
        # Frozen macOS Python must not depend on a developer-machine CA path.
        import ssl
        import certifi
        handlers.append(urllib.request.HTTPSHandler(context=ssl.create_default_context(cafile=certifi.where())))
    return urllib.request.build_opener(*handlers).open(request, timeout=30)


def latest_package(opener=open_url):
    with opener(LATEST) as response:
        data = response.read(2 * 1024 * 1024 + 1)
    if len(data) > 2 * 1024 * 1024:
        raise ValueError('Release response too large')
    release = json.loads(data)
    tag = release.get('tag_name', '')
    if release.get('draft') or release.get('prerelease') or not re.fullmatch(r'v\d+\.\d+\.\d+', tag):
        raise ValueError('No compatible stable release / No hay una versión estable compatible')
    version = tag[1:]
    name = f'Metalio-{version}-instalacion-limpia.zip'
    matches = [a for a in release.get('assets', []) if a.get('name') == name]
    if len(matches) != 1:
        raise ValueError('Latest release has no clean image / La última versión no incluye la imagen completa')
    asset = matches[0]
    url = f'https://github.com/{REPO}/releases/download/{tag}/{name}'
    if asset.get('browser_download_url') != url or asset.get('state') != 'uploaded':
        raise ValueError('Unexpected release asset / Archivo de publicación incorrecto')
    if not isinstance(asset.get('size'), int) or not 0 < asset['size'] <= MAX_PACKAGE:
        raise ValueError('Unexpected package size / Tamaño de paquete incorrecto')
    if not re.fullmatch(r'sha256:[0-9a-f]{64}', asset.get('digest') or ''):
        raise ValueError('Release has no SHA-256 / La publicación no tiene SHA-256')
    return version, url, asset['size'], asset['digest'][7:]


def download_latest(folder, emit, opener=open_url):
    folder = Path(folder)
    emit('stage', 'latest')
    version, url, size, digest = latest_package(opener)
    emit('firmware', version)
    emit('stage', 'downloading')
    package = folder / 'firmware.zip'
    total = 0
    hasher = hashlib.sha256()
    deadline = time.monotonic() + 300
    with opener(url) as response, package.open('wb') as output:
        while True:
            if time.monotonic() > deadline:
                raise TimeoutError('Download timed out / Se agotó el tiempo de descarga')
            chunk = response.read(256 * 1024)
            if not chunk:
                break
            total += len(chunk)
            if total > size:
                raise ValueError('Download exceeds expected size / Descarga demasiado grande')
            hasher.update(chunk)
            output.write(chunk)
            emit('progress', total * 20 / size)
    if total != size or hasher.hexdigest() != digest:
        raise ValueError('Download integrity check failed / Falló la verificación de la descarga')
    emit('stage', 'checking')
    with zipfile.ZipFile(package) as archive:
        for name, limit in (('manifest.json', 128 * 1024), (IMAGE, FLASH_BYTES)):
            entries = [entry for entry in archive.infolist() if entry.filename == name]
            if len(entries) != 1 or entries[0].is_dir() or entries[0].file_size > limit:
                raise ValueError('Invalid clean image package / Paquete de instalación incorrecto')
        manifest = json.loads(archive.read('manifest.json'))
        if (manifest.get('version') != version or manifest.get('bytes') != FLASH_BYTES
                or manifest.get('target') != 'Metalio E-Ink4 / ESP32-S3 / 16 MB'
                or manifest.get('image') != IMAGE):
            raise ValueError('Incompatible clean image / Imagen completa incompatible')
        # Extract only the two fixed filenames; never execute or extract bundled scripts.
        for name in ('manifest.json', IMAGE):
            with archive.open(name) as source, (folder / name).open('wb') as output:
                while chunk := source.read(256 * 1024):
                    output.write(chunk)
    return version
