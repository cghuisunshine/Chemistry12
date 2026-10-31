const fs = require('fs');
const assert = require('assert/strict');
const {JSDOM, VirtualConsole} = require('/private/tmp/physics12-dom/node_modules/jsdom');
const source = fs.readFileSync('tutorial.html','utf8');
const errors = [];
const vc = new VirtualConsole();
vc.on('jsdomError', e => errors.push(e.message));
function load(saved){
 return new JSDOM(source, {url:'https://chemistry12.test/tutorial.html', runScripts:'dangerously', pretendToBeVisual:true, virtualConsole:vc, beforeParse(w){
  w.CSS = {escape:s=>s};
  w.Element.prototype.scrollIntoView=function(){};
  w.IntersectionObserver = class {observe(){} disconnect(){}};
  w.navigator.clipboard = {writeText:async()=>{}};
  if(saved)w.localStorage.setItem('chem12-reviewed-v1',saved);
 }});
}
const dom=load(); const w=dom.window, d=w.document;
const $=s=>d.querySelector(s);
function search(s){$('#search').value=s;$('#search').dispatchEvent(new w.Event('input'));}
function input(id,value){d.getElementById(id).value=value;d.getElementById(id).dispatchEvent(new w.Event('input'));}
assert.equal(d.querySelectorAll('.lesson').length,30);
assert.equal(d.querySelectorAll('.definition-list dt').length,91);
assert.equal(d.querySelectorAll('.worked-check').length,30);
const ids=[...d.querySelectorAll('[id]')].map(e=>e.id);
assert.equal(new Set(ids).size,ids.length);
for(const a of d.querySelectorAll('a[href^="#"]'))assert.ok(d.getElementById(a.hash.slice(1)),a.href);
const structure=JSON.parse($('#studyPageStructure').textContent);
assert.equal(structure.flatMap(c=>c.sections).length,30);
for(const c of structure){
 for(const s of c.sections){assert.equal(d.getElementById(s.id).querySelector('h3').textContent,s.title.split(' ').slice(1).join(' '));
 assert.ok(d.getElementById(s.id).querySelector('.lesson-source a').href.endsWith('#page='+s.pdfPage));}
}
assert.ok($('#section-1-1').open);
search('hydrolysis');
assert.ok(!$('#section-5-1').hidden && $('#section-5-1').open);
assert.ok($('#section-1-1').hidden);
assert.match($('#searchStatus').textContent,/matching textbook section/);
assert.ok($('#emptySearch').hidden);
search('zzzz-no-chemistry-match-zzzz'); assert.equal($('#emptySearch').hidden,false);
search(''); assert.equal($('#section-5-1').open,false);assert.equal($('#section-1-1').open,true);
search('hydrolysis');
d.querySelector('.nav-sections a[href="#section-1-3"]').click();
assert.equal($('#search').value,'');assert.ok($('#section-1-3').open);assert.ok(!$('#kinetics').hidden);
const chapter=$('#equilibrium');
chapter.querySelector('[data-chapter-expand="true"]').click();
assert.ok([...chapter.querySelectorAll('.lesson')].every(e=>e.open));
chapter.querySelector('[data-chapter-expand="false"]').click();
assert.ok([...chapter.querySelectorAll('.lesson')].every(e=>!e.open));
for(const form of d.querySelectorAll('.quiz')){
 form.dispatchEvent(new w.Event('submit',{cancelable:true}));
 assert.match(form.querySelector('.quiz-score').textContent,/3 unanswered/);
 const answers=w.eval('quizData')[form.dataset.unit];
 answers.forEach((q,i)=>form.querySelector(`input[name="${form.dataset.unit}-q${i}"][value="${q.answer}"]`).checked=true);
 form.dispatchEvent(new w.Event('submit',{cancelable:true}));
 assert.match(form.querySelector('.quiz-score').textContent,/3\/3 correct/);
}
const complete=$('.complete');complete.checked=true;complete.dispatchEvent(new w.Event('change'));
assert.match($('#progressText').textContent,/1 of 6/);
const saved=w.localStorage.getItem('chem12-reviewed-v1');
const reload=load(saved); assert.ok(reload.window.document.querySelector('.complete').checked);reload.window.close();
$('#resetProgress').click();assert.match($('#progressText').textContent,/0 of 6/);
const oldState=[...d.querySelectorAll('details')].map(e=>e.open);
w.dispatchEvent(new w.Event('beforeprint'));assert.ok([...d.querySelectorAll('.lesson')].every(e=>e.open));
w.dispatchEvent(new w.Event('afterprint'));assert.deepEqual([...d.querySelectorAll('details')].map(e=>e.open),oldState);
input('temperature','298');assert.match($('#rateResult').textContent,/1.00×/);
$('#catalyst').checked=true;$('#catalyst').dispatchEvent(new w.Event('input'));assert.match($('#rateResult').textContent,/catalyst on/);
input('eqH2','1');input('eqI2','1');input('eqHI','2');assert.match($('#eqResult').textContent,/At equilibrium/);
input('eqHI','1');assert.match($('#eqResult').textContent,/products/);
input('eqH2','');assert.match($('#eqResult').textContent,/Enter/);
input('silver','0.0001');input('chloride','0.0001');assert.match($('#solResult').textContent,/Precipitation/);
input('silver','0');assert.match($('#solResult').textContent,/Unsaturated/);
input('phSlider','7');assert.match($('#phResult').textContent,/Neutral/);
input('phSlider','3');assert.match($('#phResult').textContent,/Acidic/);
input('bufferRatio','0');assert.match($('#bufferResult').textContent,/4.76/);
input('bufferRatio','1');assert.match($('#bufferResult').textContent,/5.76/);
$('#menuBtn').click();assert.equal($('#menuBtn').getAttribute('aria-expanded'),'true');
$('#backdrop').click();assert.equal($('#menuBtn').getAttribute('aria-expanded'),'false');
assert.deepEqual(errors,[]);
console.log(JSON.stringify({status:'PASS',sections:30,definitions:91,models:6,questions:18,checks:['HTML structure and anchors','PDF section destinations','search and empty state','search state restoration','deep links reveal sections','chapter expand/collapse','quiz answers and feedback','review progress persistence/reset','print expansion/restoration','rate model','equilibrium model and validation','precipitation model','pH model','buffer model','mobile navigation toggle'],runtimeErrors:errors},null,2));
w.close();
