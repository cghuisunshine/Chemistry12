/* Integration checks: node tools/test_chemistry12_practice.cjs (jsdom >=26). */
'use strict';
const assert=require('node:assert/strict'),fs=require('node:fs'),path=require('node:path');
const {JSDOM,VirtualConsole}=require(process.env.CHEMISTRY_JSDOM_PATH||'jsdom');
const root=path.resolve(__dirname,'..');
const source=fs.readFileSync(path.join(root,'chemistry12-practice.html'),'utf8');
const inventory=JSON.parse(fs.readFileSync(path.join(root,'content/chemistry12/practice-problems.json'),'utf8'));
const bank=JSON.parse(source.match(/<script id="question-bank" type="application\/json">([\s\S]*?)<\/script>/)[1]);
const wait=()=>new Promise(r=>setTimeout(r,30));
let unexpectedRequests=0;
function page(storage={},url='https://chemistry.test/chemistry12-practice.html'){
  const errors=[],vc=new VirtualConsole();vc.on('jsdomError',e=>errors.push(e.message));
  const dom=new JSDOM(source,{url,runScripts:'dangerously',pretendToBeVisual:true,virtualConsole:vc,beforeParse(w){
    Object.defineProperty(w.navigator,'onLine',{value:false,configurable:true});
    w.HTMLCanvasElement.prototype.getContext=()=>new Proxy({getImageData:()=>({data:new Uint8ClampedArray([255,255,255,255])})},{get:(o,k)=>o[k]||(()=>{})});
    w.HTMLCanvasElement.prototype.toDataURL=()=> 'data:image/png;base64,YQ==';
    w.HTMLMediaElement.prototype.pause=()=>{};w.HTMLElement.prototype.scrollIntoView=()=>{};
    w.HTMLDialogElement.prototype.showModal=function(){this.open=true;};w.HTMLDialogElement.prototype.close=function(){this.open=false;};
    w.fetch=async()=>{unexpectedRequests++;throw Error('Unexpected network request');};w.confirm=()=>true;
    for(const [k,v] of Object.entries(storage))w.localStorage.setItem(k,v);
  }});
  return {dom,w:dom.window,d:dom.window.document,$:id=>dom.window.document.getElementById(id),errors};
}
function change(p,id,value){p.$(id).value=value;p.$(id).dispatchEvent(new p.w.Event('change'));}
function login(p,name){p.$('login-name').value=name;p.$('login-form').dispatchEvent(new p.w.Event('submit',{cancelable:true}));}
function storage(p){return Object.fromEntries(Array.from({length:p.w.localStorage.length},(_,i)=>{const k=p.w.localStorage.key(i);return [k,p.w.localStorage.getItem(k)];}));}
function openQuestion(p,id){const q=bank.find(q=>q.id===id);change(p,'practice-chapter',q.chapter);change(p,'mode','chapter');change(p,'chapter-question',q.id);}

(async()=>{
  assert.equal(bank.length,inventory.question_count);
  assert.equal(new Set(bank.map(q=>q.id)).size,bank.length);
  assert.equal(new Set(bank.map(q=>q.topic)).size,30);
  assert.equal(new Set(bank.map(q=>q.chapter)).size,6);
  assert.equal(inventory.sections.length,30);
  for(const group of inventory.sections){
    const qs=inventory.questions.filter(q=>q.section===group.section);
    assert.deepEqual(qs.map(q=>q.sourceNumber),Array.from({length:group.count},(_,i)=>i+1));
    assert.equal(qs[0].page,group.start);
  }
  for(const q of inventory.questions){
    assert.ok(q.images.length);
    for(const p of [...q.images,...q.context]){
      assert.ok(p.page>=12&&p.page<=430);
      assert.ok(p.rect[3]>p.rect[1]+3);
      for(const suffix of ['', '.js'])assert.ok(fs.existsSync(path.join(root,p.src+suffix)),p.src+suffix);
    }
    assert.ok(!q.images.some(i=>[73,153,199,264,265,361].includes(i.page)),'Exclude chapter overviews and blank workbook pages');
  }
  assert.equal(inventory.references.length,7);
  const p=page({'physics12PracticeStudent':'Physics student','physics12Practice.v1:ada':'physics untouched'});await wait();
  assert.deepEqual(p.errors,[]);assert.equal(p.$('login-overlay').hidden,false);
  assert.equal(p.$('practice-chapter').options.length,7);
  assert.equal(p.d.querySelectorAll('script[src]').length,0);
  assert.match(p.d.title,/Chemistry 12/);assert.ok(!source.includes('physics12'));
  const ids=[...p.d.querySelectorAll('[id]')].map(e=>e.id);assert.equal(ids.length,new Set(ids).size);
  for(const img of p.d.querySelectorAll('.reference-tables img'))assert.ok(fs.existsSync(path.join(root,img.getAttribute('src'))));
  for(const m of source.matchAll(/url\((assets\/chemistry12-math\/[^)]+)\)/g))assert.ok(fs.existsSync(path.join(root,m[1])));
  login(p,'Ada');openQuestion(p,'chem12-s1-1-q1');
  assert.match(p.$('question-title').textContent,/Section 1.1, review question 1/);
  assert.ok(p.$('source').href.endsWith('Chemistry12.pdf#page=21'));
  assert.equal(p.$('chapter-grid').children.length,40);
  assert.equal(p.$('solution').hidden,true);
  const q=bank[0];
  const prebuilt=JSON.parse(fs.readFileSync(path.join(root,'content/chemistry12/prebuilt-answers.json'),'utf8')).answers;
  assert.equal(Object.keys(prebuilt).length,373);
  for(const question of bank){
    assert.equal(question.hasAnswer,true,question.id);
    assert.equal(question.hasWorkedSteps,true,question.id);
    assert.equal(question.answerSource,'prebuilt-ai');
    assert.ok(prebuilt[question.id].steps.length>=2);
    assert.ok(prebuilt[question.id].check.trim());
    assert.match(prebuilt[question.id].generatedBy,/this session/);
    assert.match(question.solution,/data-answer-source="prebuilt-ai"/);
  }
  p.$('check').click();
  assert.equal(p.$('solution').hidden,false,'The answer is visible in the same click event without awaiting a request');
  assert.equal(p.$('attempt-count').textContent,'0','Revealing does not grade or record an attempt');
  assert.match(p.$('solution-body').textContent,/Prebuilt AI answer/);
  assert.equal(p.$('worked-solution').hidden,true,'No missing-steps request starts');
  assert.equal(unexpectedRequests,0);
  p.$('rate-practice').click();assert.equal(p.$('attempt-count').textContent,'1');assert.equal(p.$('review-count').textContent,'1');
  assert.equal(p.w.localStorage.getItem('physics12Practice.v1:ada'),'physics untouched');
  assert.ok(p.w.localStorage.getItem('chemistry12Practice.v1:ada'));
  change(p,'mode','review');assert.match(p.$('question-title').textContent,/Section 1.1, review question 1/);
  const saved=storage(p),reload=page(saved);await wait();
  assert.equal(reload.$('student-name-label').textContent,'Ada');assert.equal(reload.$('review-count').textContent,'1');
  openQuestion(reload,q.id);reload.$('check').click();await wait();
  assert.match(reload.$('solution-body').textContent,/Prebuilt AI answer/);
  reload.$('rate-correct').click();assert.equal(reload.$('review-count').textContent,'0');
  assert.equal(reload.$('attempt-count').textContent,'2');
  openQuestion(reload,'chem12-s6-4-q5');assert.ok(reload.$('statement').querySelector('.source-context img'),'Shared electrochemical diagram follows its question');
  change(reload,'practice-chapter','chem12-ch5');
  assert.equal(reload.$('topic-list').querySelectorAll('input[data-topic]').length,5);
  reload.$('topic-clear').click();assert.equal(reload.$('topic-all').disabled,false);
  reload.$('topic-all').click();assert.ok([...reload.$('topic-list').querySelectorAll('input[data-topic]')].every(i=>i.checked));
  // Every source question reveals synchronously offline with an empty answer cache.
  let reveals=0;
  for(const question of bank){
    if(reload.$('practice-chapter').value!==question.chapter)change(reload,'practice-chapter',question.chapter);
    if(reload.$('mode').value!=='chapter')change(reload,'mode','chapter');
    change(reload,'chapter-question',question.id);
    reload.$('response-input').value='A typed response';
    reload.$('check').click();
    assert.equal(reload.$('solution').hidden,false,question.id);
    assert.match(reload.$('solution-body').textContent,/Prebuilt AI answer/);
    assert.equal(reload.$('worked-solution').hidden,true);
    assert.ok(reload.$('solution-body').querySelectorAll('.worked-steps li').length>=2);
    reveals++;
  }
  assert.equal(reveals,373);assert.equal(unexpectedRequests,0,'Typed responses must not trigger automatic grading');
  // Online status must not make reveal call the service either.
  Object.defineProperty(reload.w.navigator,'onLine',{value:true,configurable:true});
  openQuestion(reload,bank[10].id);reload.$('response-input').value='Another typed answer';reload.$('check').click();
  assert.equal(unexpectedRequests,0);
  const format=reload.w.ChemistrySolutionFormat;
  const chemistryMath=format.text('Use $\\mathrm{H_3O^+}$ and $K_a=10^{-5}$; <img src=x onerror=alert(1)>');
  assert.match(chemistryMath,/katex/);assert.ok(!chemistryMath.includes('<img'));
  const linked=page(saved,'https://chemistry.test/chemistry12-practice.html?q=chem12-s4-4-q4');await wait();
  assert.match(linked.$('question-title').textContent,/Section 4.4, review question 4/);
  assert.deepEqual(p.errors,[]);assert.deepEqual(reload.errors,[]);assert.deepEqual(linked.errors,[]);
  assert.equal(unexpectedRequests,0,'Normal offline practice makes no network requests');
  for(const file of ['chemistry12-monitor.html','content.html','tutorial.html'])assert.ok(fs.existsSync(path.join(root,file)));
  for(const v of [p,reload,linked])v.dom.window.close();
  console.log(JSON.stringify({status:'PASS',questions:bank.length,sections:30,chapters:6,checks:['complete consecutive source numbering','all original crop and font assets','chapter and section filters','student storage isolation','373 synchronous offline answer reveals','no generation or automatic grading requests','safe offline math rendering','source-bound prebuilt solutions','review queue and successful retry','progress reload','shared diagrams','question deep links']},null,2));
})().catch(e=>{console.error(e);process.exit(1);});
