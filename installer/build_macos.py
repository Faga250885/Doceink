"""Build a native macOS app and DMG. Never connects to USB hardware."""
import hashlib
import os
from pathlib import Path
import platform
import plistlib
import shutil
import subprocess
import sys
import tempfile

from app import VERSION


def run(*args, **kwargs):
    subprocess.run([str(arg) for arg in args], check=True, **kwargs)


def main():
    if sys.platform != 'darwin':
        raise SystemExit('Build on macOS, not through cross-compilation.')
    root = Path(__file__).resolve().parent
    os.chdir(root)
    arch = platform.machine()
    if arch not in ('arm64', 'x86_64'):
        raise SystemExit('Unsupported architecture')
    payload = root / 'payload'
    payload.mkdir(exist_ok=True)
    shutil.copy2(root.parent / 'assets/doceink-symbol.png', payload)
    run(sys.executable, root / 'prepare_notices.py')
    run(sys.executable, '-m', 'unittest', 'test_installer', 'test_download')
    build = root / 'build'
    build.mkdir(exist_ok=True)
    # iconutil preserves the app icon in Finder; all sizes use the original mark.
    iconset = build / 'DoceInk.iconset'
    iconset.mkdir(exist_ok=True)
    for size in (16, 32, 128, 256, 512):
        for scale in (1, 2):
            suffix = '@2x' if scale == 2 else ''
            run('sips', '-z', size * scale, size * scale, payload / 'doceink-symbol.png',
                '--out', iconset / f'icon_{size}x{size}{suffix}.png', stdout=subprocess.DEVNULL)
    icon = build / 'DoceInk.icns'
    run('iconutil', '-c', 'icns', '-o', icon, iconset)
    run(sys.executable, '-m', 'PyInstaller', '--noconfirm', '--clean', '--onedir', '--windowed',
        '--noupx', '--name', 'DoceInk Setup', '--icon', icon,
        '--osx-bundle-identifier', 'com.doceink.setup', '--target-architecture', arch,
        '--codesign-identity', '-', '--add-data', f'{payload / "doceink-symbol.png"}:payload',
        '--add-data', f'{payload / "THIRD-PARTY.txt"}:payload', '--collect-all', 'esptool',
        '--collect-data', 'certifi', '--copy-metadata', 'esptool',
        '--distpath', root / 'dist', '--workpath', build, '--specpath', root, root / 'app.py')
    bundle = root / 'dist/DoceInk Setup.app'
    info = bundle / 'Contents/Info.plist'
    data = plistlib.loads(info.read_bytes())
    data.update(CFBundleShortVersionString='0.75.149', CFBundleVersion='149.1',
                LSMinimumSystemVersion='15.0', NSHighResolutionCapable=True)
    info.write_bytes(plistlib.dumps(data))
    # Ad-hoc signing permits local integrity verification. It is NOT Developer ID/notarization.
    run('codesign', '--force', '--deep', '--sign', '-', bundle)
    run('codesign', '--verify', '--deep', '--strict', bundle)
    executable = bundle / 'Contents/MacOS/DoceInk Setup'
    for mode in ('self-test', 'smoke-test', 'download-test'):
        run(executable, '--' + mode, build / f'{mode}-{arch}.json', timeout=180)
    output = root / 'dist' / f'DoceInk-Setup-{VERSION}-macOS-{arch}.dmg'
    with tempfile.TemporaryDirectory(prefix='doceink-dmg-') as directory:
        stage = Path(directory)
        run('ditto', bundle, stage / bundle.name)
        (stage / 'Applications').symlink_to('/Applications')
        shutil.copy2(root / 'MACOS.md', stage / 'Read me - English and Español.txt')
        run('hdiutil', 'create', '-volname', 'DoceInk Setup', '-srcfolder', stage,
            '-ov', '-format', 'UDZO', output)
    run('hdiutil', 'verify', output)
    # Retest the app from the distributed disk image, mounted read-only.
    with tempfile.TemporaryDirectory(prefix='doceink-mount-') as directory:
        run('hdiutil', 'attach', '-readonly', '-nobrowse', '-mountpoint', directory, output)
        try:
            mounted = Path(directory) / bundle.name
            run('codesign', '--verify', '--deep', '--strict', mounted)
            run(mounted / 'Contents/MacOS/DoceInk Setup', '--self-test', build / f'dmg-test-{arch}.json', timeout=60)
        finally:
            run('hdiutil', 'detach', directory)
    digest = hashlib.sha256(output.read_bytes()).hexdigest()
    (root / 'dist' / f'SHA256SUMS-macOS-{arch}.txt').write_text(f'{digest}  {output.name}\n')


if __name__ == '__main__':
    main()
