"""Validate the five manually curated JSON files; never regenerate discarded variants."""
from pathlib import Path
import json
root=Path(__file__).resolve().parents[1]
models=[json.loads(p.read_text(encoding='utf-8')) for p in (root/'src/data/models').glob('*.json')]
assert len(models)==5, 'El catálogo autorizado contiene exactamente cinco modelos.'
assert {m['manufacturer'] for m in models}=={'Goldwind','Envision','Gamesa','Nordex','Vestas'}
assert len({m['manufacturer'] for m in models})==len(models), 'Un modelo por fabricante.'
print('Cinco modelos curados; referencias y supuestos conservados en sus JSON.')
