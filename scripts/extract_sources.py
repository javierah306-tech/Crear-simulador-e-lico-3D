from pathlib import Path
import json
from pypdf import PdfReader

root = Path(__file__).resolve().parents[1]
source = Path(r'C:\Users\javie\OneDrive\Desktop\Lab Neiron\modelos 3D eolicos\modelos chilenos')
out = root / 'docs' / 'sources'
out.mkdir(parents=True, exist_ok=True)
manifest = []
for pdf in source.rglob('*.pdf'):
    doc = PdfReader(pdf)
    text = '\n'.join(f'\n--- PÁGINA {i+1} ---\n{p.extract_text()}' for i, p in enumerate(doc.pages))
    (out / (pdf.stem + '.txt')).write_text(text, encoding='utf-8')
    manifest.append({'file': pdf.name, 'original': str(pdf), 'pages': len(doc.pages)})
    print(pdf.name, len(doc.pages))
(out / 'manifest.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding='utf-8')
