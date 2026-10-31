/* CHEMISTRY_JSDOM_PATH=/path/to/jsdom node tools/test_chemistry12_tutorial_visuals.cjs */
'use strict';
const assert=require('node:assert/strict'),fs=require('node:fs'),path=require('node:path');
const {JSDOM}=require(process.env.CHEMISTRY_JSDOM_PATH||'jsdom');
const root=path.resolve(__dirname,'..');
const read=p=>fs.readFileSync(path.join(root,p),'utf8');
const manifest=JSON.parse(read('content/chemistry12/tutorial-visuals.json'));
const d=new JSDOM(read('tutorial.html')).window.document;
const sections=JSON.parse(d.querySelector('#studyPageStructure').textContent).flatMap(c=>c.sections);
assert.equal(manifest.length,sections.length);
assert.equal(d.querySelectorAll('figure.lesson-visual').length,30);
for(const item of manifest){
  const section=d.getElementById('section-'+item.section.replace('.','-'));
  const meta=sections.find(s=>s.id===section.id);
  const figure=section.querySelector('figure.lesson-visual');
  assert.ok(figure,'Every section needs a diagram');
  assert.ok(figure.previousElementSibling.matches('p.concept'),'Place next to definitions and concepts');
  const img=figure.querySelector('img'),source=figure.querySelector('picture source');
  assert.equal(img.getAttribute('src'),item.image);
  assert.equal(img.alt,item.alt);assert.ok(img.alt.length>80);
  assert.equal(img.getAttribute('loading'),'lazy');
  assert.equal(source.getAttribute('media'),'(max-width: 760px)');
  assert.equal(source.getAttribute('srcset'),item.mobileImage);
  assert.equal(item.pdfPage,meta.pdfPage);assert.equal(item.printedPage,meta.page);
  assert.ok(figure.querySelector(`a[href="output/pdf/Chemistry12-navigable.pdf#page=${meta.pdfPage}"]`));
  const links=[...figure.querySelectorAll('a')];assert.ok(links.some(a=>a.textContent.includes('full-size')));
  for(const p of [item.image,item.mobileImage]){
    const svg=new JSDOM(read(p),{contentType:'image/svg+xml'}).window.document;
    assert.ok(svg.querySelector('svg[role="img"][aria-labelledby="title desc"]'));
    assert.ok(svg.getElementById('title').textContent.includes(item.section));
    assert.equal(svg.getElementById('desc').textContent,item.alt);
    assert.equal(svg.querySelectorAll('script,image,foreignObject').length,0,'Self-contained deterministic SVG');
    const bounds=svg.documentElement.getAttribute('viewBox').split(' ').map(Number);
    assert.deepEqual(bounds,p===item.image?[0,0,1000,500]:[0,0,500,960]);
  }
}
// Guard the corrected chemistry and high-risk distinctions in the visual content.
const svg=n=>read(`assets/chemistry12-tutorial/section-${n}.svg`);
assert.ok(svg('1-3').includes('Cl + ClNO₂ → Cl₂ + NO₂'));
assert.ok(svg('2-1').includes('Equal rates; concentrations need not match.'));
assert.ok(svg('3-3').includes('= s(2s)² = 4s³'));
assert.ok(svg('6-3').includes('0.34 − (−0.76) = +1.10 V'));
assert.ok(svg('6-4').includes('Anode (−)')&&svg('6-4').includes('Cathode (+)'));
assert.ok(svg('6-5').includes('Anode (+)')&&svg('6-5').includes('Cathode (−)'));
const ids=[...d.querySelectorAll('[id]')].map(e=>e.id);assert.equal(new Set(ids).size,ids.length);
console.log(JSON.stringify({status:'PASS',sections:30,desktopDiagrams:30,mobileDiagrams:30,checks:['Every lesson has a labelled diagram','Textbook section and PDF links','Accessible descriptions','Full-size links','Stacked mobile sources','Well-formed self-contained SVGs','Key chemistry distinctions','Unique HTML IDs']}));
