import hashlib
import io
import json
from pathlib import Path
import tempfile
import unittest
import zipfile
from unittest.mock import patch
import download as d
import app


def fixture(version='0.75.999', **overrides):
    image = bytes(d.FLASH_BYTES)
    manifest = {'version': version, 'bytes': len(image), 'target': 'Metalio E-Ink4 / ESP32-S3 / 16 MB',
                'image': d.IMAGE, 'sha256': hashlib.sha256(image).hexdigest()}
    manifest.update(overrides)
    output = io.BytesIO()
    with zipfile.ZipFile(output, 'w', zipfile.ZIP_DEFLATED) as archive:
        archive.writestr('manifest.json', json.dumps(manifest))
        archive.writestr(d.IMAGE, image)
        archive.writestr('../must-not-extract.txt', 'not extracted')
    payload = output.getvalue()
    url = f'https://github.com/{d.REPO}/releases/download/v{version}/Metalio-{version}-instalacion-limpia.zip'
    release = {'tag_name': 'v'+version, 'draft': False, 'prerelease': False, 'assets': [{
        'name': f'Metalio-{version}-instalacion-limpia.zip', 'browser_download_url': url,
        'state': 'uploaded', 'size': len(payload), 'digest': 'sha256:'+hashlib.sha256(payload).hexdigest()}]}
    return release, payload


class DownloadTests(unittest.TestCase):
    def test_downloads_newer_firmware_than_installer_and_ignores_extra_paths(self):
        release, payload = fixture()
        calls = []
        def opener(url):
            calls.append(url)
            return io.BytesIO(json.dumps(release).encode() if url == d.LATEST else payload)
        with tempfile.TemporaryDirectory(dir=Path(__file__).parent) as directory:
            version = d.download_latest(directory, lambda *x: None, opener)
            self.assertEqual(version, '0.75.999')
            self.assertEqual(app.verify_image(Path(directory), version).stat().st_size, d.FLASH_BYTES)
            self.assertEqual(set(p.name for p in Path(directory).iterdir()), {'firmware.zip', 'manifest.json', d.IMAGE})
            d.download_latest(directory, lambda *x: None, opener)
        self.assertEqual(calls.count(d.LATEST), 2)

    def test_missing_asset_does_not_fall_back(self):
        release, _ = fixture(); release['assets'] = []
        with self.assertRaises(ValueError):
            d.latest_package(lambda _: io.BytesIO(json.dumps(release).encode()))

    def test_rejects_tampered_download_before_extraction(self):
        release, payload = fixture()
        with tempfile.TemporaryDirectory(dir=Path(__file__).parent) as directory:
            with self.assertRaises(ValueError):
                d.download_latest(directory, lambda *x: None, lambda url: io.BytesIO(
                    json.dumps(release).encode() if url == d.LATEST else b'x'+payload[1:]))
            self.assertFalse((Path(directory)/d.IMAGE).exists())

    def test_rejects_incompatible_manifest(self):
        release, payload = fixture(target='Another board')
        with tempfile.TemporaryDirectory(dir=Path(__file__).parent) as directory:
            with self.assertRaises(ValueError):
                d.download_latest(directory, lambda *x: None, lambda url: io.BytesIO(
                    json.dumps(release).encode() if url == d.LATEST else payload))

    def test_rejects_asset_from_another_repository_or_without_digest(self):
        release, _ = fixture()
        for field, value in [('browser_download_url','https://example.org/firmware.zip'), ('digest',None)]:
            altered = json.loads(json.dumps(release)); altered['assets'][0][field] = value
            with self.assertRaises(ValueError):
                d.latest_package(lambda _: io.BytesIO(json.dumps(altered).encode()))

    def test_download_failure_never_opens_serial(self):
        window = object.__new__(app.Window)
        import queue
        window.queue = queue.Queue()
        with tempfile.TemporaryDirectory(dir=Path(__file__).parent) as directory:
            with patch.object(app.tempfile, 'TemporaryDirectory') as tmp:
                tmp.return_value.__enter__.return_value = directory
                with patch.object(app, 'download_latest', side_effect=OSError('offline')), patch.object(app, 'run_install') as run:
                    window.worker('SIMULATED'); run.assert_not_called()
        events = list(window.queue.queue)
        self.assertIn(('stage', 'error'), events)

    def test_https_host_allowlist(self):
        self.assertTrue(d.allowed_url(d.LATEST))
        for url in ['http://github.com/x','https://github.com.evil.test/x','https://github.com@evil.test/x','https://github.com:444/x']:
            self.assertFalse(d.allowed_url(url))


if __name__ == '__main__': unittest.main()
