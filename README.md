# Chemistry12

- [Course contents](content.html)
- [Textbook tutorial](tutorial.html)
- [Ksp from thermodynamics and mixing](ksp-thermodynamics.html)
- [Entropy versus enthalpy: thermodynamic laws and university connections](entropy-enthalpy.html)
- [Practice Studio](chemistry12-practice.html)

The standalone Ksp lesson develops the thermodynamic derivation, chemical
potentials, activity/concentration distinction and ideal entropy of mixing.
Equations are pre-rendered with the local KaTeX distribution and work offline.
Rebuild it with `node tools/build_ksp_thermodynamics.cjs`; this also restores its
link in tutorial section 3.3 if necessary.

The entropy–enthalpy lesson expands tutorial section 2.4 from the first and
second laws through Gibbs energy, microstates, the third law, chemical
potentials, equilibrium, heat-capacity corrections and statistical mechanics.
It includes worked examples and an offline temperature/composition explorer.
Rebuild with `node tools/build_entropy_enthalpy.cjs`; this also restores the
section 2.4 link. The builder shares the Ksp template's base visual style and
uses the local KaTeX renderer and fonts. Edit its source in
`tools/entropy-enthalpy-template.html` and the two explorer JavaScript modules.

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
All 373 entries have now been rewritten and individually reviewed directly in
the conversation session using the current shared teaching prompt. No entries
remain on the earlier outline-based revision. Each records its prompt/source
receipt and a question-specific review; no external AI endpoint was used.
Six additional solution diagrams cover the requested titration sketches,
bromine half-cell, formal zinc/fluorine cell, molten NaCl electrolysis and
silver plating. Their numerical plots and labelled schematics can be rebuilt
with `python3 tools/build_chemistry12_solution_diagrams.py` (requires
`rsvg-convert`), followed by rebuilding the practice page.
Check coverage and rebuild with no network calls:

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

Fresh answers and in-session authoring share the versioned teaching instructions
in `content/chemistry12/solution-prompt.json` and the same prompt constructor in
`tools/chemistry12-solution-prompt.js`. Both live prompt entry points delegate to
that constructor. Neither path supplies an old prebuilt solution as an outline.
Matching the prompt prevents drift; it does not itself establish content quality.

For each prebuilt question, export the exact prompt and source image paths:

```sh
python3 tools/save_chemistry12_session_answers.py --question chem12-s1-1-q1
```

Read that request and its sources, author a complete solution directly in the
conversation, and review its subparts, derivation, substitutions, units and check.
Save one response with `save_one(entry, request, review)` or the CLI payload
`{"entry":{...},"request":{...},"review":"question-specific review"}` before
advancing. The saver rejects a stale prompt/source receipt, preserves corrected
diagrams and source caveats, and records the prompt version and review. The saver
and builder have no network calls; the discarded endpoint authoring client is
not included. A step count or word count alone does not establish quality.

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
