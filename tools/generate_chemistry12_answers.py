#!/usr/bin/env python3
"""Check locally authored answer coverage and rebuild; no network requests."""
import argparse,json
from chemistry12_prebuilt import ROOT,fingerprint,read_answers,source_questions,valid
p=argparse.ArgumentParser(description=__doc__);p.add_argument('--status',action='store_true');p.add_argument('--build',action='store_true');a=p.parse_args()
i=json.loads((ROOT/'content/chemistry12/practice-problems.json').read_text());d=read_answers();m=[q['id'] for q in source_questions(i) if not valid(d['answers'].get(q['id']),fingerprint(q))]
version=json.loads((ROOT/'content/chemistry12/solution-prompt.json').read_text())['version']
reviewed=sum(e.get('authoring',{}).get('promptVersion')==version and e.get('authoring',{}).get('mode')=='one-question-at-a-time-in-session' for e in d['answers'].values())
print(json.dumps(dict(required=i['question_count'],saved=i['question_count']-len(m),missing=len(m),promptVersion=version,reviewedWithCurrentPrompt=reviewed,pendingDetailReview=i['question_count']-reviewed)))
if a.build:
 from build_chemistry12_practice import build
 build()
