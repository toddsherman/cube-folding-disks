#!/usr/bin/env python3
"""Assemble Markdown, portable LaTeX, Typst, and PDF from reviewed sections.

Build-only dependencies: pypandoc_binary==1.17, typst==0.15.2.
The mathematical supplement does not use these packages.
"""
from pathlib import Path
import datetime
import hashlib
import importlib.metadata
import json
import re
import subprocess

import pypandoc
import typst

ROOT = Path(__file__).resolve().parents[1]
SECTION_NAMES = [
    '00-introduction.md', '01-model-and-realization.md',
    '02-crease-reduction.md', '03-finite-certificate.md',
    '04-layer-construction.md', '05-main-theorem.md',
    '06-counterexample.md', '07-references.md',
]


def main():
    parts = []
    hashes = {}
    for name in SECTION_NAMES:
        path = ROOT / 'sections' / name
        body = path.read_text()
        hashes[f'sections/{name}'] = hashlib.sha256(path.read_bytes()).hexdigest()
        # Standalone section authors used H1; preserve the reviewed text while
        # normalizing its heading hierarchy only in the combined manuscript.
        if name != '00-introduction.md' and re.match(r'^# \d', body):
            body = re.sub(r'^(#+) ', r'#\1 ', body, flags=re.MULTILINE)
        body = body.replace('](../examples/', '](examples/')
        parts.append(body.rstrip())
    merged = '\n\n'.join(parts) + '\n'
    (ROOT / 'manuscript.md').write_text(merged)
    pandoc = pypandoc.get_pandoc_path()
    common = [pandoc, str(ROOT/'manuscript.md'),
              '--from=markdown+tex_math_single_backslash', '--standalone']
    subprocess.run(common + ['--to=latex', '--variable=geometry:margin=1in',
                              '--variable=fontsize:11pt',
                              '-o', str(ROOT/'manuscript.tex')], check=True)
    # Typst uses vector mathematics and supports the same portable source.
    subprocess.run(common + ['--to=typst', '--variable=papersize:a4',
                              '--variable=fontsize:10.5pt',
                              '-o', str(ROOT/'manuscript.typ')], check=True)
    tp = ROOT/'manuscript.typ'
    text = tp.read_text()
    # Place page numbers and keep headings with their following paragraphs.
    text += '\n'
    # Pandoc 3.9 emits the old intersection alias for \cap; Typst 0.15
    # names this symbol `inter`. Define the alias without changing mathematics.
    # Lists may break across pages (2026-11-09); unbreakable lists had
    # stranded several lemma lead-ins at page bottoms. Tables are kept
    # whole (Typst's default for figures): when they were allowed to
    # break, reflow twice left a single data row apart from its table.
    text = ('#let sect = sym.inter\n'
            '#set page(numbering: "1", margin: 25mm)\n'
            '#set par(justify: true)\n'
            + text)
    # Subscripted order relations such as <_F: set the subscript to the
    # right of the relation rather than beneath it.
    text = re.sub(r'(?<=[\s$])<_(?=[A-Z])', 'scripts(<)_', text)
    text = text.replace('== References\n', '#pagebreak(weak: true)\n\n== References\n')
    text = text.replace('#link("examples/', '#link("../../examples/')
    # Pandoc's template sets document(title: none); restate the H1 title
    # after it so that the PDF carries a /Title entry.
    head = merged.split('\n')
    title = head[0].removeprefix('# ')
    # The author's name is the paragraph after the title (added 2026-11-14).
    author = head[2].strip()
    assert author and not author.startswith(('#', 'Research manuscript')), 'author line missing'
    text = text.replace('  doc,\n)\n', f'  doc,\n)\n#set document(title: "{title}", author: "{author}")\n', 1)
    tp.write_text(text)
    output = ROOT/'output/pdf/disk-folding-manuscript.pdf'
    output.parent.mkdir(parents=True, exist_ok=True)
    typst.compile(str(tp), output=str(output),
                  # Pinned for byte-reproducible builds; set to the latest
                  # revision date (the 5 and 7 November PDFs used 2026-11-05, the
                  # builds of 9 November and the first two of 14 November 2026-11-09).
                  timestamp=datetime.datetime(2026,11,14,tzinfo=datetime.timezone.utc))
    record = {
        'section_sha256': hashes,
        'build_dependencies': {n: importlib.metadata.version(n)
                               for n in ('pypandoc_binary','typst')},
        'pandoc_version': str(pypandoc.get_pandoc_version()),
        'outputs': {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest()
                    for p in (ROOT/'manuscript.md', ROOT/'manuscript.tex',
                              ROOT/'manuscript.typ', output)},
        'notes': ['Heading depth normalized in combined manuscript only.',
                  'LaTeX exported but not compiled here; PDF compiled with Typst.',
                  'Build packages are not mathematical-verification dependencies.'],
    }
    (ROOT/'build/build-record.json').write_text(json.dumps(record,indent=2)+'\n')
    print(json.dumps({'pdf': str(output), 'words':len(merged.split()),
                      'sections':len(hashes)},indent=2))


if __name__ == '__main__':
    main()
