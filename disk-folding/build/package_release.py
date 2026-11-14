#!/usr/bin/env python3
"""Hash and package this manuscript without its surrounding repository."""
from pathlib import Path
import argparse
import hashlib
import json
import zipfile

ROOT = Path(__file__).resolve().parents[1]


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--output', type=Path, required=True,
                    help='Fresh ZIP filename outside the package directory')
    args = ap.parse_args()
    output = args.output.resolve()
    if output.exists() or output.with_suffix(output.suffix+'.sha256').exists():
        raise SystemExit('Choose fresh archive and checksum filenames.')
    if output.is_relative_to(ROOT):
        raise SystemExit('Archive must be outside the package tree.')
    files = sorted(p for p in ROOT.rglob('*')
                   if p.is_file() and p.name != 'RELEASE-MANIFEST.json'
                   and '__pycache__' not in p.parts and p.name != '.DS_Store')
    if any(p.is_symlink() for p in files):
        raise SystemExit('Symlink files are not accepted in this release.')
    record = {'schema':'disk-folding-release-v1', 'files':{
        str(p.relative_to(ROOT)):{'sha256':sha(p),'bytes':p.stat().st_size}
        for p in files},
        'scope':'Manuscript, finite certificates, internal reviews, and literature comparison. External human review is pending.'}
    manifest = ROOT/'RELEASE-MANIFEST.json'
    manifest.write_text(json.dumps(record,indent=2)+'\n')
    files.append(manifest)
    output.parent.mkdir(parents=True,exist_ok=True)
    with zipfile.ZipFile(output,'x',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as z:
        for path in files:
            z.write(path, str(Path(ROOT.name)/path.relative_to(ROOT)))
    digest = sha(output)
    output.with_suffix(output.suffix+'.sha256').write_text(f'{digest}  {output.name}\n')
    print(json.dumps({'archive':str(output),'sha256':digest,
                      'files':len(files),'bytes':output.stat().st_size},indent=2))


if __name__ == '__main__':
    main()
