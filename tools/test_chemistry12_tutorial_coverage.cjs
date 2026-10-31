/* CHEMISTRY_JSDOM_PATH=/path/to/jsdom node tools/test_chemistry12_tutorial_coverage.cjs */
'use strict';
const assert=require('node:assert/strict'),fs=require('node:fs'),path=require('node:path'),cp=require('node:child_process');
const {JSDOM,VirtualConsole}=require(process.env.CHEMISTRY_JSDOM_PATH||'jsdom');
const root=path.resolve(__dirname,'..'),read=p=>fs.readFileSync(path.join(root,p),'utf8');
const bank=JSON.parse(read('chemistry12-practice.html').match(/<script id="question-bank" type="application\/json">([\s\S]*?)<\/script>/)[1]);
const curriculum=JSON.parse(read('content/chemistry12/tutorial-practice-coverage.json'));
const source=read('tutorial.html'),errors=[],vc=new VirtualConsole();vc.on('jsdomError',e=>errors.push(e.message));
const dom=new JSDOM(source,{url:'https://chemistry12.test/tutorial.html',runScripts:'dangerously',pretendToBeVisual:true,virtualConsole:vc,beforeParse(w){
 w.CSS={escape:s=>s};w.Element.prototype.scrollIntoView=function(){};
 w.IntersectionObserver=class{observe(){}disconnect(){}};
 w.navigator.clipboard={writeText:async()=>{}};
 w.fetch=()=>{throw new Error('Tutorial coverage must not fetch answers');};
}});
const d=dom.window.document,w=dom.window;
const byId=new Map(bank.map(q=>[q.id,q])),covered=new Set();
assert.equal(bank.length,373);assert.equal(curriculum.sections.length,30);
assert.equal(d.querySelectorAll('.practice-toolkit').length,30);
assert.equal(d.querySelectorAll('.practice-skill').length,146);
for(const section of curriculum.sections){
 const lesson=d.getElementById('section-'+section.section.replace('.','-'));
 const toolkit=lesson.querySelector('.practice-toolkit');assert.ok(toolkit);
 assert.equal(toolkit.getAttribute('aria-labelledby'),toolkit.querySelector('h4').id);
 assert.equal(toolkit.nextElementSibling.className,'further-explain','Keep the physical-chemistry explanations');
 const expected=new Set(bank.filter(q=>q.topic===section.section).map(q=>q.id)),actual=new Set();
 for(const link of toolkit.querySelectorAll('a[data-practice-question]')){
  const url=new URL(link.href),id=url.searchParams.get('q'),q=byId.get(id);
  assert.ok(q,'A link must target a real embedded question');
  assert.equal(url.pathname,'/chemistry12-practice.html');
  assert.equal(q.topic,section.section);assert.equal(id,link.dataset.practiceQuestion);
  assert.equal(link.textContent,'Q'+q.sourceNumber);assert.ok(link.getAttribute('aria-label').includes(section.section));
  actual.add(id);covered.add(id);
 }
 assert.deepEqual(actual,expected,'Every question in this section needs a teaching-method reference');
}
assert.deepEqual(covered,new Set(byId.keys()));
for(const a of d.querySelectorAll('a[href^="#"]'))assert.ok(d.getElementById(a.hash.slice(1)),a.href);
// New prerequisite explanations must participate in the existing search and navigation.
const search=d.getElementById('search');search.value='levelling effect';search.dispatchEvent(new w.Event('input'));
assert.equal(d.getElementById('section-4-2').hidden,false);assert.equal(d.getElementById('section-4-2').open,true);
assert.equal(d.getElementById('section-1-1').hidden,true);
// Open a deep-linked application method even with an unrelated active search.
const to=d.createElement('a');to.href='#practice-5-3-5';
// Native hashchange uses the tutorial's existing revealTarget listener.
w.location.hash=to.hash;w.dispatchEvent(new w.HashChangeEvent('hashchange'));
assert.equal(search.value,'');assert.equal(d.getElementById('section-5-3').open,true);
assert.equal(d.getElementById('section-5-3').hidden,false);
assert.match(d.getElementById('practice-5-3-5').textContent,/purity/);
const start=d.querySelector('.practice-coverage-links a[href="#practice-toolkit-6-1"]');start.click();
assert.ok(d.getElementById('section-6-1').open);
assert.equal(d.querySelectorAll('figure.lesson-visual').length,30,'Retain all teaching diagrams');
assert.equal(d.querySelectorAll('.worked-check').length,30);assert.equal(d.querySelectorAll('.further-explain').length,30);
const ids=[...d.querySelectorAll('[id]')].map(e=>e.id);assert.equal(ids.length,new Set(ids).size);
assert.deepEqual(errors,[]);
const checked=cp.spawnSync('python3',['tools/build_chemistry12_tutorial_coverage.py','--check'],{cwd:root,encoding:'utf8'});
assert.equal(checked.status,0,checked.stdout+checked.stderr);
const protection=cp.spawnSync('python3',['-c',`
import copy,json,sys
from pathlib import Path
sys.path.insert(0,'tools')
from build_chemistry12_tutorial_coverage import read_bank,build,validate
c=json.loads(Path('content/chemistry12/tutorial-practice-coverage.json').read_text())
b=read_bank(Path('chemistry12-practice.html').read_text());s=Path('tutorial.html').read_text()
assert build(build(s,c,b),c,b)==s
changed=copy.deepcopy(b);changed[0]['answer']='Altered solution requiring a new review'
try:validate(c,changed)
except ValueError:pass
else:raise AssertionError('Changed solutions must invalidate the old review')
missing=copy.deepcopy(c);missing['sections'][0]['skills']=[k for k in missing['sections'][0]['skills'] if 5 not in [int(q.rsplit('q',1)[1]) for q in k['questions']]]
try:validate(missing,b)
except ValueError:pass
else:raise AssertionError('Unmapped question must block the build')
assert Path('tutorial.html').read_text()==s
`],{cwd:root,encoding:'utf8'});
assert.equal(protection.status,0,protection.stdout+protection.stderr);
console.log(JSON.stringify({status:'PASS',mappedQuestions:covered.size,sections:30,skills:146,checks:['Complete question coverage','Correct question deep links','Search of added concepts','Deep links clear filters and reveal lessons','Retained diagrams and worked explanations','Unique anchors','Idempotent build','Stale solutions invalidate review','Unmapped questions block rebuild'],runtimeErrors:errors}));
w.close();
