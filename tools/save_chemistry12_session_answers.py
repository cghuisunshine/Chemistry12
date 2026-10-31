#!/usr/bin/env python3
"""Save AI answers authored in this session; never calls a network service.

stdin: {"section":"1.1","answers":[[1,"final answer",["step 1","step 2"],"check",["optional assumption"],false]]}
"""
from datetime import datetime, timezone
import json
import sys
from chemistry12_prebuilt import ROOT, OUTPUT, fingerprint, read_answers, source_questions, valid

def save(payload):
    inventory = json.loads((ROOT/'content/chemistry12/practice-problems.json').read_text())
    questions = {q['id']:q for q in source_questions(inventory)}
    data = read_answers()
    entries = {}
    for row in payload['answers']:
        key = 'chem12-s'+payload['section'].replace('.', '-')+'-q'+str(row[0])
        if key not in questions:
            raise ValueError('Unknown question '+key)
        entry = dict(id=key, answer=row[1], steps=row[2], check=row[3],
                     assumptions=row[4] if len(row)>4 else [], needsReview=row[5] if len(row)>5 else False,
                     provenance='prebuilt-ai', generatedBy='AI authored in this session; no external endpoint',
                     generatedAt=datetime.now(timezone.utc).isoformat(), sourceHash=fingerprint(questions[key]))
        if not valid(entry):
            raise ValueError('Incomplete solution '+key)
        entries[key] = entry
    data['answers'].update(entries)
    data['generationMethod'] = 'Authored by AI in this session from the supplied textbook; no external endpoint.'
    temporary = OUTPUT.with_suffix('.json.tmp')
    temporary.write_text(json.dumps(data, ensure_ascii=False, indent=2)+'\n')
    temporary.replace(OUTPUT)
    print(f'Saved section {payload["section"]}: {len(entries)} solutions; {len(data["answers"])} total.')

if __name__ == '__main__':
    payload=json.load(sys.stdin)
    for item in payload if isinstance(payload,list) else [payload]:
        save(item)
