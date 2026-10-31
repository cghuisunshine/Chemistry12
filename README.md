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
the embedded solution immediately and works offline by default. The optional AI
checkbox requests an additional fresh answer when Show answer is clicked. Each
prebuilt solution has an explicit Prebuilt AI label, worked
steps, a check, and source/assumption notes where needed. These are separate from
the publisher key and are not publisher-verified. Optional AI hints, explicit
AI checks, new generated practice questions, and sync still need internet.
The seven textbook reference tables are available below the question card.

The builder validates each answer against its question/context/table image bytes
and refuses to replace the practice page if required fields are missing or the
source is stale. These are structural checks, not a teaching-quality review.
All 373 entries now have expanded, question-specific teaching explanations,
using the revised section 1.1 question 1 as the model. The remaining 372 were
rebuilt in the authoring session with equation choices, intermediate calculations,
conceptual reasoning and checks; source ambiguities and diagram corrections are
preserved. Check coverage and rebuild with no network calls:

```sh
python3 tools/generate_chemistry12_answers.py --status --build
```

When revising prebuilt solutions, use the following teaching standard:

- Answer every requested subpart or reason explicitly.
- Read and use the original figures, tables, conditions and units. Distinguish
  supplied data from illustrative examples.
- Explain the choice of principle or equation, then show substitutions,
  intermediate results and the connection to each final answer. For conceptual
  questions, develop each reason with evidence rather than adding artificial
  calculation steps.
- Include a relevant independent check and any assumptions that affect the
  result. Keep explanations at the section's level; add advanced models only
  when they help answer the question.
- Write math inside `$...$` or `$$...$$`, with complete braced exponents. Do not
  number the step strings: the page supplies their ordered list.

Prebuilt solutions are edited and checked in the authoring session, then saved
with `tools/save_chemistry12_session_answers.py`. The save and build tools do not
call an AI endpoint. A minimum step count alone does not establish that the
reasoning is adequate.

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
