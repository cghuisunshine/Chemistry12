# Chemistry12

- [Course contents](content.html)
- [Textbook tutorial](tutorial.html)
- [Practice Studio](chemistry12-practice.html)

The Practice Studio follows the companion Physics 12 page. It contains the
numbered **Review Questions** from every section of `Chemistry12.pdf`, with
subparts and diagrams preserved as original page crops. Inline Practice Problems,
Quick Checks and Activities are outside this question bank.

Choose a student name to keep separate local histories, then use chapter order,
adaptive textbook practice, topic selection, or the missed-question review queue.
Answers can be typed, drawn, or photographed. Backup/export and import preserve
progress. Chemistry uses its own storage and optional sync collections.

All **373 answers and worked solutions** were authored with AI in this session
and saved in `content/chemistry12/prebuilt-answers.json`. **Show answer** reveals
the embedded solution immediately, works offline, and makes no generation or
verification request. Each solution has an explicit Prebuilt AI label, worked
steps, a check, and source/assumption notes where needed. These are separate from
the publisher key and are not publisher-verified. Optional AI hints, explicit
AI checks, new generated practice questions, and sync still need internet.
The seven textbook reference tables are available below the question card.

The builder validates each answer against its question/context/table image bytes
and refuses to replace the practice page if any complete solution is missing or
stale. Check coverage and rebuild with no network calls:

```sh
python3 tools/generate_chemistry12_answers.py --status --build
```

Keep `assets/` beside the HTML pages. `Chemistry12.pdf` is needed for full-source
links. All scripts and the math renderer are embedded in the generated page;
fonts and question images are local assets. Serve the repository with
`python3 -m http.server 8000`, then open
`http://localhost:8000/chemistry12-practice.html`, or open the HTML file directly.

Rebuild HTML after changing a module:

```sh
python3 tools/build_chemistry12_practice.py
```

Regenerate question crops and inventory (requires PyMuPDF and `pdftotext`):

```sh
python3 tools/build_chemistry12_practice.py --extract
```

`content/chemistry12/practice-problems.json` records every source page and crop.
`sourceNumber` is the printed question number within a section; `number` is its
position within the chapter for navigation. All source questions are unranked.
Adaptive difficulty levels are practice estimates, not textbook labels.
