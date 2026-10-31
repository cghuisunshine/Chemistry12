"""Source-bound AI answer keys shared by the generator, builder and checks."""
import hashlib
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / 'content/chemistry12/prebuilt-answers.json'
DEPENDENCIES = {'chem12-s4-2-q2': 'chem12-s4-2-q1',
                'chem12-s5-2-q8': 'chem12-s5-2-q7',
                'chem12-s5-2-q15': 'chem12-s5-2-q9',
                'chem12-s5-4-q10': 'chem12-s5-4-q8'}


def references(q, inventory):
    pages = {3: [434, 435], 4: [436], 5: [436, 437], 6: [438]}.get(q['chapter'], [])
    if re.search(r'\b(?:mass|grams?|moles?|molar mass)\b', q['text'], re.I):
        pages = [432] + pages
    return [p for p in inventory['references'] if p['page'] in pages]


def source_questions(inventory):
    by_id = {q['id']: q for q in inventory['questions']}
    overrides_path = ROOT/'content/chemistry12/practice-overrides.json'
    overrides = json.loads(overrides_path.read_text()) if overrides_path.exists() else {}
    for original in inventory['questions']:
        q = dict(original, context=list(original['context']))
        q.update(overrides.get(q['id'], {}))
        if q['id'] in DEPENDENCIES:
            q['context'] += [p for p in by_id[DEPENDENCIES[q['id']]]['images'] if p not in q['context']]
        q['referenceTables'] = references(q, inventory)
        yield q


def fingerprint(q):
    h = hashlib.sha256(json.dumps([q['id'], q['text']], ensure_ascii=False).encode())
    for p in q['images'] + q['context'] + q.get('referenceTables', []):
        h.update(p['src'].encode())
        h.update((ROOT / p['src']).read_bytes())
    return h.hexdigest()


def valid(entry, source_hash=None):
    field = lambda v, maximum: isinstance(v, str) and bool(v.strip()) and len(v) <= maximum
    return (isinstance(entry, dict) and field(entry.get('answer'), 6000)
            and isinstance(entry.get('steps'), list) and 2 <= len(entry['steps']) <= 12
            and all(field(s, 4000) for s in entry['steps'])
            and field(entry.get('check'), 4000)
            and isinstance(entry.get('assumptions', []), list) and len(entry.get('assumptions', [])) <= 12
            and all(field(s, 2000) for s in entry.get('assumptions', []))
            and isinstance(entry.get('needsReview'), bool)
            and (source_hash is None or entry.get('sourceHash') == source_hash))


def read_answers():
    return json.loads(OUTPUT.read_text()) if OUTPUT.exists() else dict(version=1, source='Chemistry12.pdf', answers={})
