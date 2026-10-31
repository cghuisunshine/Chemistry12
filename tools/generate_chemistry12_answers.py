#!/usr/bin/env python3
"""Check locally authored answer coverage and rebuild; no network requests."""
import argparse,json
from chemistry12_prebuilt import ROOT,fingerprint,read_answers,source_questions,valid
p=argparse.ArgumentParser(description=__doc__);p.add_argument('--status',action='store_true');p.add_argument('--build',action='store_true');a=p.parse_args()
i=json.loads((ROOT/'content/chemistry12/practice-problems.json').read_text());d=read_answers();m=[q['id'] for q in source_questions(i) if not valid(d['answers'].get(q['id']),fingerprint(q))]
print(json.dumps(dict(required=i['question_count'],saved=i['question_count']-len(m),missing=len(m))))
if a.build:
 from build_chemistry12_practice import build
 build()
