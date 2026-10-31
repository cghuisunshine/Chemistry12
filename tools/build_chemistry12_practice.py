#!/usr/bin/env python3
"""Build the Chemistry 12 practice studio from the supplied scanned textbook.

Run with --extract to regenerate source crops (requires PyMuPDF).
Otherwise only Python's standard library is required. Source rectangles and
the original printed question numbers are preserved in the JSON inventory.
"""
import argparse
import base64
import hashlib
import html
import json
from pathlib import Path
import re
from chemistry12_prebuilt import fingerprint, read_answers, source_questions, valid

ROOT = Path(__file__).resolve().parents[1]
TOOLS = ROOT / 'tools'
CONTENT = ROOT / 'content/chemistry12'
ASSETS = ROOT / 'assets/chemistry12-practice'
INVENTORY = CONTENT / 'practice-problems.json'
E = html.escape

# Manually checked against the scans. These labels are missing or corrupt in
# the supplied OCR; using the scan avoids dropping or merging real questions.
LABEL_OVERRIDES = {
    93: [(7, 273.3)],
    227: [(1, 59.7)],
    241: [(1, 78.4), (2, 180.3), (3, 280.2), (4, 433.0), (5, 586.6)],
    297: [(1, 50.7), (2, 101.0), (3, 176.5), (4, 239.5), (5, 365.9)],
    343: [(1, 62.8), (2, 242.2), (3, 419.2), (4, 570.0)],
    344: [(5, 34.0), (6, 165.0), (7, 357.0), (8, 488.0), (9, 579.0)],
    371: [(5, 30.9), (6, 226.4), (7, 575.0)],
    372: [(8, 43.0)],
    415: [(3, 30.2), (4, 335.1)],
}
MANUAL_TEXT = {
    (344, 5): 'Bromcresol purple changes from yellow to purple as pH increases from 5.2 through 6.8. Is bromcresol purple a stronger or weaker acid than acetic acid? Explain. Would it be a good indicator to indicate that acetic acid is acidic? Why or why not?',
    (344, 6): 'Five 0.10 M solutions labelled A–E are NaCl, K3PO4, LiHCO3, CH3COOH and HIO3. Identify each solution from the indicator results in the original table.',
    (344, 7): 'Complete the indicator table for phenol red, methyl orange and alizarin yellow: pKa, Ka, colour in pure water, 0.010 M NaOH and 0.010 M HCl.',
    (344, 8): 'Complete the weak–strong titration statements by inserting lower or higher. See the original image for all blanks and comparisons.',
    (344, 9): 'Explain the chemistry of buffers and hydrolysis when calculating the pH halfway to, and at, the equivalence point for a weak acid titrated by a strong base and a weak base titrated by a strong acid.',
}


def structure():
    text = (ROOT / 'tutorial.html').read_text()
    return json.loads(re.search(r'<script id="studyPageStructure" type="application/json">(.*?)</script>', text, re.S)[1])


def extract():
    import pymupdf as pdf
    doc = pdf.open(ROOT / 'Chemistry12.pdf')
    chapters = structure()
    sections = [(c, s) for c in chapters for s in c['sections']]
    # This cache is optional: only the small review-page subset is inspected.
    cached = ROOT / 'tmp/pdfs/review-words.json'
    words_cache = {}  # Read current PDF bytes; do not trust a stale scratch cache.
    text_cache = ROOT / 'tmp/pdfs/chemistry12.txt'
    if not text_cache.exists():
        import subprocess
        text_cache.parent.mkdir(parents=True, exist_ok=True)
        subprocess.run(['pdftotext', '-layout', str(ROOT / 'Chemistry12.pdf'), str(text_cache)], check=True)
    pages_text = text_cache.read_text().split('\f')
    ASSETS.mkdir(parents=True, exist_ok=True)
    CONTENT.mkdir(parents=True, exist_ok=True)

    def words(pg):
        if pg not in words_cache:
            words_cache[pg] = doc[pg-1].get_text('words')
        return words_cache[pg]

    def body_bottom(pg):
        page = doc[pg-1]
        footer = [w[1] for w in words(pg) if w[1] > page.rect.height - 65 and ('Edvantage' in w[4] or '©' in w[4] or re.match(r'Chapter', w[4]))]
        return min(footer) - 8 if footer else page.rect.height - 48

    def crop(pg, rect, name):
        page = doc[pg-1]
        rect = list(pdf.Rect(rect) & page.rect)
        assert rect[3] > rect[1] + 3, (pg, rect)
        path = ASSETS / (name + '.png')
        page.get_pixmap(matrix=pdf.Matrix(2, 2), clip=pdf.Rect(rect), alpha=False).save(path)
        return dict(src=str(path.relative_to(ROOT)), page=pg, rect=[round(v, 2) for v in rect], width=round(rect[2]-rect[0]))

    questions, chapter_indices, summaries = [], {}, []
    for index, (chapter, section) in enumerate(sections):
        sn = section['title'].split()[0]
        start = next(i+1 for i, t in enumerate(pages_text) if re.search(r'\b'+re.escape(sn)+r'\s+Review\s+Questions', t))
        end = sections[index+1][1]['pdfPage'] - 1 if index+1 < len(sections) else 430
        if index+1 < len(sections) and sections[index+1][0]['id'] != chapter['id']:
            end -= 1  # Exclude the following chapter's opening overview.
        events = []
        for pg in range(start, end+1):
            found = []
            for w in words(pg):
                match = re.fullmatch(r'(\d{1,2})[.,]', w[4])
                if match and w[0] < 55 and w[1] < body_bottom(pg) and (pg != start or w[1] > 44):
                    found.append(dict(page=pg, y=w[1], number=int(match[1])))
            for number, y in LABEL_OVERRIDES.get(pg, []):
                found = [e for e in found if e['number'] != number]
                found.append(dict(page=pg, y=y, number=number))
            events.extend(sorted(found, key=lambda e: e['y']))
        numbers = [e['number'] for e in events]
        assert numbers == list(range(1, max(numbers)+1)), (sn, numbers)
        chapter_number = int(sn.split('.')[0])
        for i, event in enumerate(events):
            following = events[i+1] if i+1 < len(events) else dict(page=end, y=body_bottom(end)+3)
            parts, texts = [], []
            for pg in range(event['page'], following['page']+1):
                top = event['y'] - 4 if pg == event['page'] else 10
                bottom = following['y'] - 4 if pg == following['page'] else body_bottom(pg)
                bottom = min(bottom, body_bottom(pg))
                if bottom-top < 5:
                    continue
                selected = [w for w in words(pg) if top <= w[1] < bottom]
                if pg != event['page'] and pg == following['page'] and bottom < 65:
                    continue
                if sn == '6.4' and event['number'] == 3:
                    bottom = min(bottom, 150)
                # A blank workbook page follows §4.5. It is not part of question 15.
                if pg == 264:
                    continue
                rect = [0, max(0, top), doc[pg-1].rect.width, bottom]
                part = crop(pg, rect, f's{sn.replace(".", "-")}-q{event["number"]}-{len(parts)+1}')
                parts.append(part)
                # Select cached words instead of rerunning expensive OCR extraction.
                texts.append(' '.join(w[4] for w in selected))
            assert parts, (sn, event)
            source_number = event['number']
            text = MANUAL_TEXT.get((event['page'], source_number), '\n'.join(texts))
            if sn == '4.4':
                text = 'Assume all solutions are at 25°C unless otherwise indicated.\n' + text
            context = []
            # The diagram precedes questions 4 and 5, rather than either crop.
            if sn == '6.4' and source_number in (4, 5):
                context.append(crop(415, [30, 152, 290, 327], 'context-electrochemical-cell'))
            if sn == '1.1' and source_number == 1:
                context.append(crop(12, [0, 60, doc[11].rect.width, 395], 'context-rate-warm-up'))
            chapter_indices[chapter_number] = chapter_indices.get(chapter_number, 0) + 1
            questions.append(dict(id=f'chem12-s{sn.replace(".", "-")}-q{source_number}', chapter=chapter_number,
                chapterId=chapter['id'], chapterTitle=chapter['title'].split(' ', 1)[1], number=chapter_indices[chapter_number],
                sourceNumber=source_number, section=sn, topicTitle=section['title'].split(' ', 1)[1],
                page=event['page'], printedPage=event['page']-10, images=parts, context=context, text=text,
                level=2, answers=[]))
        summaries.append(dict(section=sn, count=len(events), start=start, end=end))
        print(f'Section {sn}: {len(events)} consecutive review questions', flush=True)
    references = []
    labels = ['Atomic masses', 'Common ions', 'Solubility table', 'Solubility product constants', 'Acid and base strengths', 'Acid–base indicators', 'Standard reduction potentials']
    for pg, label in zip(range(432, 439), labels):
        references.append(dict(title=label, **crop(pg, [0, 15, doc[pg-1].rect.width, body_bottom(pg)], f'reference-{pg}')))
    inventory = dict(source='Chemistry12.pdf', printedPageOffset=10, question_count=len(questions),
        answer_count=0, scope='All numbered section Review Questions; subparts stay together. Inline Practice Problems, Quick Checks and Activities are not included.',
        sections=summaries, references=references, questions=questions)
    INVENTORY.write_text(json.dumps(inventory, ensure_ascii=False, indent=2)+'\n')
    (CONTENT/'chapters.json').write_text(json.dumps(chapters, ensure_ascii=False, indent=2)+'\n')
    print(f'Extracted {len(questions)} review questions from all 30 sections.', flush=True)


def script(name):
    text = (TOOLS/name).read_text()
    assert '</script' not in text.lower(), name
    return '<script>\n'+text+'\n</script>\n'


def img(part, alt):
    return f'<img src="{E(part["src"])}" alt="{E(alt)}" style="width:{part["width"]*2}px;max-width:100%;height:auto" loading="lazy">'


def build(require_prebuilt=True):
    inventory = json.loads(INVENTORY.read_text())
    inventory['questions'] = list(source_questions(inventory))
    prebuilt = read_answers()['answers']
    missing = [q['id'] for q in inventory['questions'] if not valid(prebuilt.get(q['id']), fingerprint(q))]
    if require_prebuilt and missing:
        raise ValueError(f'{len(missing)} complete prebuilt solutions are still required; existing page kept. First: {missing[0]}')
    bank = []
    by_id = {q['id']: q for q in inventory['questions']}
    dependencies = {'chem12-s4-2-q2': 'chem12-s4-2-q1',
                    'chem12-s5-2-q8': 'chem12-s5-2-q7',
                    'chem12-s5-2-q15': 'chem12-s5-2-q9',
                    'chem12-s5-4-q10': 'chem12-s5-4-q8'}
    for q in inventory['questions']:
        if q['id'] in dependencies:
            dependency = by_id[dependencies[q['id']]]
            q['context'] = q['context'] + [p for p in dependency['images'] if p not in q['context']]
        label = f'Section {q["section"]}, review question {q["sourceNumber"]}'
        statement = ''.join(img(p, label+(' (continued)' if i else '')+' — '+q['text'][:1300]) for i, p in enumerate(q['images']))
        if q['section'] == '4.4':
            statement = '<p class="small">Assume 25°C unless otherwise indicated.</p>' + statement
        if q['context']:
            statement += '<details class="source-context" open><summary>Referenced diagram / earlier context</summary>' + ''.join(img(p, f'Reference context for {label}') for p in q['context'])+'</details>'
        digest = hashlib.sha256(json.dumps([q['images'], q['context'], q['text']], sort_keys=True).encode()).hexdigest()
        reference_pages = {3: [434, 435], 4: [436], 5: [436, 437], 6: [438]}.get(q['chapter'], [])
        if re.search(r'\b(?:mass|grams?|moles?|molar mass)\b', q['text'], re.I):
            reference_pages = [432] + reference_pages
        entry = prebuilt.get(q['id']) if q['id'] not in missing else None
        solution = ''
        if entry:
            solution = '<div class="answer-provenance" data-answer-source="prebuilt-ai"><span class="badge">Prebuilt AI answer &amp; solution</span></div>'
            solution += '<p class="prebuilt-answer" style="white-space:pre-wrap"><strong>'+E(entry['answer'])+'</strong></p>'
            solution += '<h3>Step-by-step solution</h3><ol class="worked-steps">'+''.join('<li style="white-space:pre-wrap">'+E(step)+'</li>' for step in entry['steps'])+'</ol>'
            for diagram in entry.get('solutionImages', []):
                solution += '<figure>'+img(diagram, diagram['alt'])+'<figcaption>'+E(diagram.get('caption', ''))+'</figcaption></figure>'
            solution += '<p style="white-space:pre-wrap"><strong>Check:</strong> '+E(entry['check'])+'</p>'
            if entry['assumptions']:
                solution += '<h3>Assumptions / source notes</h3><ul>'+''.join('<li>'+E(a)+'</li>' for a in entry['assumptions'])+'</ul>'
            if entry['needsReview']:
                solution += '<p class="small">Source ambiguity flagged for review; see the notes above.</p>'
        bank.append(dict(id=q['id'], sourceId=f'{q["section"]}.{q["sourceNumber"]}', kind='textbook',
            chapter=f'chem12-ch{q["chapter"]}', chapterNumber=q['chapter'], chapterTitle=q['chapterTitle'],
            number=q['number'], sourceNumber=q['sourceNumber'], topic=q['section'], topicTitle=q['topicTitle'],
            level=q['level'], questionType='Textbook review', title=f'{label} · {q["topicTitle"]}',
            html=statement, solution=solution, answer=entry['answer'] if entry else '', answerSource='prebuilt-ai' if entry else 'pending-ai', hasAnswer=bool(entry),
            questionText=q['text'], hasWorkedSteps=bool(entry), answerHash=digest, solutionHash=hashlib.sha256(solution.encode()).hexdigest() if entry else None,
            referenceImages=[p['src'] for p in inventory['references'] if p['page'] in reference_pages],
            url=f'Chemistry12.pdf#page={q["page"]}'))
    sources = {p['src'] for q in inventory['questions'] for p in q['images']+q['context']}
    sources.update(p['src'] for p in inventory['references'])
    sources.update(p['src'] for entry in prebuilt.values() for p in entry.get('solutionImages', []))
    for src in sorted(sources):
        path = ROOT/src
        companion = Path(str(path)+'.js')
        if not companion.exists() or companion.stat().st_mtime < path.stat().st_mtime:
            data = 'data:image/png;base64,'+base64.b64encode(path.read_bytes()).decode('ascii')
            companion.write_text('window.ChemistryImageAssets.register('+json.dumps(src)+','+json.dumps(data)+');\n')
    template = (TOOLS/'chemistry12-practice-template.html').read_text()
    template = template.replace('/* SOLUTION_MATH_CSS */', (TOOLS/'vendor/katex/katex.min.css').read_text().replace('physics12-math', 'chemistry12-math'))
    template = template.replace('Model answer and worked solution', 'Answer key')
    template = template.replace('Work through a question, learn from the result, and build from there.', 'Practise the original BC Science Chemistry 12 review questions, one section at a time. <a href="tutorial.html">Study the lessons ↗</a>')
    references = '<details class="reference-tables"><summary>Textbook reference tables · constants, ions and indicators</summary>'
    references += ''.join(f'<details><summary>{E(p["title"])}</summary><a href="Chemistry12.pdf#page={p["page"]}" target="_blank" rel="noopener">Open source page {p["page"]-10} ↗</a>'+img(p, p['title'])+'</details>' for p in inventory['references'])+'</details>'
    note = f'<p class="footnote">{len(bank)} original numbered Review Questions from all 30 sections in six chapters. {len(bank)-len(missing)} prebuilt AI answers and worked solutions are embedded for immediate offline access. Show answer uses the embedded solution by default. The optional AI checkbox generates an additional answer and worked solution online while keeping the original prebuilt version visible. These solutions were authored in this session, are separate from the publisher key, and can contain mistakes; source ambiguities are labelled. All subparts, tables and diagrams stay with their question. Inline Practice Problems, Quick Checks and Activities are excluded. Questions, drawing and progress work offline. All source questions are unranked; adaptive levels are practice estimates.</p>'
    template = template.replace('<!-- CHEMISTRY12_FOOTNOTE -->', references+note)
    data = json.dumps(bank, ensure_ascii=False, separators=(',', ':')).replace('<', '\\u003c')
    scripts = '<script id="question-bank" type="application/json">'+data+'</script>\n'
    names = ['chemistry12-activity.js','chemistry12-adaptive.js','chemistry12-practice-core.js','chemistry12-photo-review.js','vendor/katex/katex.min.js','vendor/katex/mhchem.min.js','chemistry12-solution-format.js','chemistry12-answer-key.js','chemistry12-worked-solution.js','chemistry12-drawing-pad.js','chemistry12-students.js','chemistry12-live-share.js','chemistry12-image-assets.js','chemistry12-practice.js']
    scripts += ''.join(script(name) for name in names)
    (ROOT/'chemistry12-practice.html').write_text(template.replace('<!-- PRACTICE_SCRIPTS -->', scripts))
    head = re.search(r'<head>(.*?)</head>', template, re.S)[1].replace('Practice Studio', 'Student Activity')
    dialog = re.search(r'<dialog[^>]*>(.*?)</dialog>', template, re.S)[1]
    dialog = re.sub(r'<button id="activity-close".*?</button>', '', dialog)
    dialog = re.sub(r'<p><a id="activity-page-link".*?</p>', '', dialog)
    monitor = '<!doctype html><html lang="en"><head>'+head+'</head><body><header><a class="brand" href="chemistry12-practice.html">Chemistry 12 <span>/ Practice Studio</span></a><a href="content.html">Browse chapters ↗</a></header><main style="max-width:850px">'+dialog
    monitor += '<section class="panel storage"><h3>Optional sync</h3><label for="monitor-key">Firebase API key</label><input id="monitor-key" type="password" autocomplete="off"><button id="monitor-connect" class="secondary" type="button">Connect to synced history</button><p class="small">Reads Chemistry 12 history only.</p></section></main>'
    monitor += script('chemistry12-activity.js')+script('chemistry12-monitor.js')+'</body></html>'
    (ROOT/'chemistry12-monitor.html').write_text(monitor)
    print(f'Built chemistry12-practice.html with {len(bank)} textbook review questions.', flush=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--extract', action='store_true')
    parser.add_argument('--allow-missing', action='store_true', help='Development preview only; keep the production page complete')
    args = parser.parse_args()
    if args.extract:
        extract()
    build(require_prebuilt=not args.allow_missing)
