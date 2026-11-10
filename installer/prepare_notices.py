"""Collect license texts for the bundled Python runtime and dependencies."""
import importlib.metadata as metadata
from pathlib import Path
import sys
root = Path(__file__).resolve().parent
parts = ['DoceInk Setup\nSource: https://github.com/Faga250885/Doceink/tree/main/installer\nEach component retains its own license.\n']
for dist in sorted(metadata.distributions(), key=lambda d: d.metadata['Name'].lower()):
    texts = []
    for f in dist.files or []:
        if any(k in f.name.lower() for k in ('license', 'copying', 'notice')) and f.suffix not in ('.py', '.pyc', '.dll', '.exe'):
            p = dist.locate_file(f)
            if p.is_file() and p.stat().st_size < 200000:
                try: texts.append(p.read_text(encoding='utf-8'))
                except UnicodeError: pass
    if texts: parts.append('\n=== ' + dist.metadata['Name'] + ' ' + dist.version + ' ===\n' + '\n'.join(texts))
python_license = Path(sys.base_prefix) / 'LICENSE.txt'
if python_license.exists(): parts.append('\n=== Python ===\n' + python_license.read_text(encoding='utf-8'))
parts.append('\n=== Project ===\n' + (root.parent/'LICENSE').read_text(encoding='utf-8'))
(root/'payload/THIRD-PARTY.txt').write_text('\n'.join(parts), encoding='utf-8')
