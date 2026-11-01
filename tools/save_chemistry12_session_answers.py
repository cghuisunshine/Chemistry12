#!/usr/bin/env python3
"""Save AI answers authored in this session; never calls a network service.

stdin: {"section":"1.1","answers":[[1,"final answer",["step 1","step 2"],"check",["optional assumption"],false]]}
"""
from datetime import datetime, timezone
import hashlib
import json
import subprocess
import sys
from chemistry12_prebuilt import ROOT, OUTPUT, fingerprint, read_answers, source_questions, valid

def request_for(key):
    """Export the exact live prompt and original image paths, without a request."""
    inventory=json.loads((ROOT/'content/chemistry12/practice-problems.json').read_text())
    q=next(q for q in source_questions(inventory) if q['id']==key)
    problem=dict(id=key,title=f'Section {q["section"]}, review question {q["sourceNumber"]} · {q["topicTitle"]}',questionText=q['text'])
    code="const p=require('./tools/chemistry12-solution-prompt.js');let s='';process.stdin.on('data',c=>s+=c);process.stdin.on('end',()=>process.stdout.write(JSON.stringify({version:p.version,message:p.prompt(JSON.parse(s))})));"
    prompt=json.loads(subprocess.run(['node','-e',code],input=json.dumps(problem),text=True,cwd=ROOT,capture_output=True,check=True).stdout)
    return dict(**problem,prompt=prompt['message'],promptVersion=prompt['version'],promptHash=hashlib.sha256(prompt['message'].encode()).hexdigest(),sourceHash=fingerprint(q),images=[p['src'] for p in q['images']+q['context']+q['referenceTables']])

def save_one(entry,request,review):
    """Save one in-session response, preserving source notes and diagrams."""
    current=request_for(entry['id'])
    if any(request.get(k)!=current[k] for k in ['promptHash','promptVersion','sourceHash']):
        raise ValueError('Stale authoring request; reread the current prompt and source')
    if not isinstance(review,str) or not review.strip():raise ValueError('A question-specific content review is required')
    if not valid(entry):raise ValueError('Incomplete solution '+entry['id'])
    data=read_answers();previous=data['answers'][entry['id']]
    merged=dict(previous,**entry)
    merged['assumptions']=list(dict.fromkeys(entry.get('assumptions',[])+previous.get('assumptions',[])))
    merged['needsReview']=entry['needsReview'] or previous['needsReview']
    merged.update(sourceHash=current['sourceHash'],generatedBy='AI authored and individually reviewed in this session; no external endpoint',generatedAt=datetime.now(timezone.utc).isoformat(),provenance='prebuilt-ai',authoring=dict(promptVersion=current['promptVersion'],promptHash=current['promptHash'],mode='one-question-at-a-time-in-session',review=review))
    merged.pop('detailReview',None)
    if not valid(merged,current['sourceHash']):raise ValueError('Invalid merged source notes')
    data['answers'][entry['id']]=merged
    data['generationMethod']='Authored and reviewed one question at a time in the conversation session using the shared fresh-answer teaching prompt; no external endpoint.'
    temporary=OUTPUT.with_suffix('.json.tmp');temporary.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n');temporary.replace(OUTPUT)
    return merged

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
    if len(sys.argv)==3 and sys.argv[1]=='--question':
        print(json.dumps(request_for(sys.argv[2]),ensure_ascii=False,indent=2));sys.exit()
    payload=json.load(sys.stdin)
    if 'entry' in payload:
        save_one(payload['entry'],payload['request'],payload['review']);print('Saved one in-session solution: '+payload['entry']['id']);sys.exit()
    for item in payload if isinstance(payload,list) else [payload]:
        save(item)
