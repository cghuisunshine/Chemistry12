#!/usr/bin/env python3
"""Install the manually reviewed practice curriculum in tutorial.html.

Reads the actual embedded question bank, not just the extraction inventory.
Changed questions/solutions require a fresh content review before rebuilding.
Uses only the standard library; no network or AI endpoint.
"""
from pathlib import Path
from html import escape as E
from collections import Counter
import hashlib,json,re

ROOT=Path(__file__).resolve().parents[1]
DATA=ROOT/'content/chemistry12/tutorial-practice-coverage.json'


def read_bank(source):
    match=re.search(r'<script id="question-bank" type="application/json">(.*?)</script>',source,re.S)
    if not match:raise ValueError('Missing embedded practice question bank')
    return json.loads(match[1])


def signature(q):
    return hashlib.sha256(json.dumps([q['id'],q['questionText'],q['answer'],q['solution'],q['html']],ensure_ascii=False,separators=(',',':')).encode()).hexdigest()


def validate(curriculum,bank):
    by_id={q['id']:q for q in bank}
    if len(by_id)!=len(bank):raise ValueError('Duplicate practice question IDs')
    expected=set(by_id)
    if set(curriculum['reviewedQuestionSignatures'])!=expected:raise ValueError('Practice inventory changed; review tutorial coverage again')
    for qid,q in by_id.items():
        if signature(q)!=curriculum['reviewedQuestionSignatures'][qid]:
            raise ValueError(f'Question or solution changed: {qid}; review its tutorial coverage before rebuilding')
        if not (q.get('hasAnswer') and q.get('hasWorkedSteps') and q.get('answerSource')=='prebuilt-ai'):
            raise ValueError(f'Missing embedded prebuilt worked solution: {qid}')
    seen_sections=set();seen_skills=set();covered=set()
    for sec in curriculum['sections']:
        n=sec['section']
        if n in seen_sections:raise ValueError('Duplicate curriculum section')
        seen_sections.add(n);section_covered=set()
        for skill in sec['skills']:
            if skill['id'] in seen_skills:raise ValueError('Duplicate curriculum skill ID')
            seen_skills.add(skill['id'])
            if not all(isinstance(skill.get(k),str) and skill[k].strip() for k in ['id','title','explanation','formula']):raise ValueError('Incomplete skill')
            if not skill['questions']:raise ValueError('Skill has no practice references')
            for qid in skill['questions']:
                if qid not in by_id or by_id[qid]['topic']!=n:raise ValueError(f'Wrong question reference: {qid}')
                section_covered.add(qid)
        actual={q['id'] for q in bank if q['topic']==n}
        if section_covered!=actual:raise ValueError(f'Incomplete coverage for section {n}: {actual-section_covered}')
        covered|=section_covered
    if covered!=expected:raise ValueError('Unmapped practice questions')
    return by_id


CSS='''/* BEGIN practice curriculum styles */
.practice-toolkit{margin:28px 0;padding:22px;border:1px solid var(--border);border-left:4px solid var(--orange);border-radius:10px;background:#fff;overflow-wrap:anywhere}
.lesson-body .practice-toolkit h4{margin:0 0 10px;text-transform:none;font-size:18px;letter-spacing:0;color:var(--ink)}
.practice-toolkit-intro{font-size:13px;color:var(--muted);margin-bottom:18px}.practice-skills{display:grid;gap:18px}
.practice-skill{padding-top:17px;border-top:1px solid var(--border);scroll-margin-top:100px}
.practice-skill h5{font-size:15px;line-height:1.5;margin:0 0 8px;color:var(--green)}
.practice-skill p{font-size:13px;line-height:1.85;margin:0 0 10px}.practice-skill .method-formula{background:var(--soft);border-radius:7px;padding:10px 13px;font-size:13px;line-height:1.75;color:var(--ink);white-space:normal;overflow-wrap:anywhere}
.practice-question-links{display:flex;flex-wrap:wrap;align-items:center;gap:7px 10px;font-size:12px;color:var(--muted)}
.practice-question-links a{display:inline-block;padding:3px 8px;border:1px solid var(--border);border-radius:5px;line-height:1.5;text-decoration:none}
.practice-question-links a:hover{background:var(--soft);text-decoration:underline}.practice-question-links a:focus-visible{outline-offset:2px}
.practice-coverage-note{padding:18px 20px;background:#fff;border:1px solid var(--border);border-radius:10px;margin:18px 0;font-size:13px;scroll-margin-top:100px}
.practice-coverage-note h2{font:24px Georgia,serif;margin:0 0 9px}.practice-coverage-note p{margin:0 0 10px}.practice-coverage-links{display:flex;flex-wrap:wrap;gap:8px 17px;font-size:12px}
@media(max-width:760px){.practice-toolkit{padding:16px}.practice-question-links a{padding:6px 10px}.practice-coverage-note{padding:16px}}
@media print{.practice-toolkit{padding:12px;border-color:#bbb;break-inside:auto}.practice-skill{break-inside:avoid}.practice-question-links,.practice-coverage-links{display:none}.practice-skill p,.practice-skill .method-formula{font-size:9pt}.practice-toolkit-intro{font-size:9pt}.practice-coverage-note{break-inside:avoid}}
/* END practice curriculum styles */'''


def build(html,curriculum,bank):
    by_id=validate(curriculum,bank)
    metadata=json.loads(re.search(r'<script[^>]*id="studyPageStructure"[^>]*>(.*?)</script>',html,re.S)[1])
    known={s['id'].removeprefix('section-').replace('-','.'):s for c in metadata for s in c['sections']}
    if set(known)!={s['section'] for s in curriculum['sections']}:raise ValueError('Tutorial and practice sections differ')
    html=re.sub(r'\n?<!-- BEGIN practice toolkit .*?<!-- END practice toolkit -->','',html,flags=re.S)
    html=re.sub(r'\n?<!-- BEGIN practice coverage overview -->.*?<!-- END practice coverage overview -->','',html,flags=re.S)
    html=re.sub(r'/\* BEGIN practice curriculum styles \*/.*?/\* END practice curriculum styles \*/\n?','',html,flags=re.S)
    for sec in curriculum['sections']:
        n=sec['section'];sid=known[n]['id'];count=sum(q['topic']==n for q in bank);skills=[]
        for skill in sec['skills']:
            links=''.join(f'<a href="chemistry12-practice.html?q={E(qid,quote=True)}" data-practice-question="{E(qid,quote=True)}" aria-label="Open section {n} review question {by_id[qid]["sourceNumber"]}">Q{by_id[qid]["sourceNumber"]}</a>' for qid in skill['questions'])
            skills.append(f'<article class="practice-skill" id="{E(skill["id"],quote=True)}"><h5>{E(skill["title"])}</h5><p>{E(skill["explanation"])}</p><p class="method-formula">{E(skill["formula"])}</p><div class="practice-question-links"><span>Apply in practice:</span>{links}</div></article>')
        block=f'''\n<!-- BEGIN practice toolkit {n} -->
<section class="practice-toolkit" id="practice-toolkit-{n.replace('.', '-')}" aria-labelledby="practice-toolkit-title-{n.replace('.', '-')}"><h4 id="practice-toolkit-title-{n.replace('.', '-')}">Practice toolkit · §{n}</h4><p class="practice-toolkit-intro">Use these methods alongside the definitions, diagrams and worked check above. This section connects all {count} review questions and their prebuilt solutions to the skills below. Question links open the matching problem in the practice page.</p><div class="practice-skills">{''.join(skills)}</div></section>
<!-- END practice toolkit -->'''
        start=html.index(f'<details class="lesson" id="{sid}"')
        at=html.index('<section class="further-explain"',start)
        next_lesson=html.find('<details class="lesson"',start+1)
        if next_lesson!=-1 and at>next_lesson:raise ValueError('Cannot find section insertion point')
        html=html[:at]+block+html[at:]
    skill_count=sum(len(s['skills']) for s in curriculum['sections']);chapter_counts=Counter(q['chapterNumber'] for q in bank)
    chapter_links=[]
    for chapter in metadata:
        first=chapter['sections'][0];num=int(first['title'].split('.')[0]);n=first['id'].removeprefix('section-')
        chapter_links.append(f'<a href="#practice-toolkit-{n}">{E(chapter["title"])} · {chapter_counts[num]} questions</a>')
    overview=f'''\n<!-- BEGIN practice coverage overview -->
<aside class="practice-coverage-note" id="practice-coverage" aria-labelledby="practice-coverage-title"><h2 id="practice-coverage-title">From the tutorial to the practice problems</h2><p><strong>{len(bank)} review questions · {len(curriculum['sections'])} sections · {skill_count} linked skills.</strong> Each lesson has a practice toolkit for the concepts, calculations and interpretation used in <a href="chemistry12-practice.html">the practice page</a> and its prebuilt solutions. Start with the explanations, then use a question link to apply a method.</p><p>Coverage includes every numbered section review question currently in the practice page. Assumptions, approximate graph readings and inconsistent printed data are identified where they affect the method; the prebuilt key is an AI-authored study aid.</p><div class="practice-coverage-links">{''.join(chapter_links)}</div></aside>
<!-- END practice coverage overview -->'''
    marker='</section><div class="search-status" id="searchStatus"'
    if html.count(marker)!=1:raise ValueError('Cannot find tutorial overview boundary')
    html=html.replace(marker,overview+marker,1)
    html=html.replace('</style>',CSS+'\n</style>',1)
    return html


def main():
    import argparse
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--check',action='store_true');args=parser.parse_args()
    curriculum=json.loads(DATA.read_text());bank=read_bank((ROOT/'chemistry12-practice.html').read_text())
    target=ROOT/'tutorial.html';old=target.read_text();new=build(old,curriculum,bank)
    if args.check:
        if old!=new:raise SystemExit('Tutorial practice curriculum is out of date; run this builder')
        print('Practice curriculum is current and all embedded questions/solutions match the review.')
    else:
        target.write_text(new)
        print(f'Updated 30 tutorial toolkits: {len(bank)} questions, {sum(len(s["skills"]) for s in curriculum["sections"])} skills.')

if __name__=='__main__':main()
