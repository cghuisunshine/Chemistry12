/* CHEMISTRY_JSDOM_PATH=/path/to/jsdom node tools/test_chemistry12_ai_answer.cjs */
'use strict';
const fs=require('node:fs'),path=require('node:path'),assert=require('node:assert/strict');
const {JSDOM,VirtualConsole}=require(process.env.CHEMISTRY_JSDOM_PATH||'jsdom');
const source=fs.readFileSync(path.resolve(__dirname,'../chemistry12-practice.html'),'utf8');
const bank=JSON.parse(source.match(/<script id="question-bank" type="application\/json">([\s\S]*?)<\/script>/)[1]);
const turn=()=>new Promise(r=>setTimeout(r,20));
const errors=[],vc=new VirtualConsole();vc.on('jsdomError',e=>errors.push(e.message));
const requests=[],decoded=[];let timeoutGeneration;
const dom=new JSDOM(source,{url:'https://chemistry.test/chemistry12-practice.html',runScripts:'dangerously',pretendToBeVisual:true,virtualConsole:vc,beforeParse(w){
 Object.defineProperty(w.navigator,'onLine',{value:true,configurable:true});
 w.HTMLCanvasElement.prototype.getContext=()=>new Proxy({getImageData:()=>({data:new Uint8ClampedArray([255,255,255,255])})},{get:(o,k)=>o[k]||(()=>{}),set:(o,k,v)=>{o[k]=v;return true;}});
 w.HTMLCanvasElement.prototype.toDataURL=()=> 'data:image/jpeg;base64,YQ==';
 w.HTMLMediaElement.prototype.pause=()=>{};w.HTMLElement.prototype.scrollIntoView=function(){};
 w.HTMLDialogElement.prototype.showModal=function(){this.open=true;};w.HTMLDialogElement.prototype.close=function(){this.open=false;};
 w.fetch=(url,options)=>new Promise((resolve,reject)=>requests.push({url,options,resolve,reject}));
 const original=w.setTimeout.bind(w);w.setTimeout=(fn,ms,...args)=>{if(ms===120000)timeoutGeneration=fn;return original(fn,ms,...args);};
}});
const w=dom.window,d=w.document,$=id=>d.getElementById(id);
function change(id,value){$(id).value=value;$(id).dispatchEvent(new w.Event('change'));}
function option(on,dock=false){$(dock?'dock-generate-ai-answer':'generate-ai-answer').checked=on;$(dock?'dock-generate-ai-answer':'generate-ai-answer').dispatchEvent(new w.Event('change'));}
function open(id){const q=bank.find(q=>q.id===id);change('practice-chapter',q.chapter);change('mode','chapter');change('chapter-question',q.id);return q;}
const reportedMath=String.raw`(0.450\ \mathrm{mol\,L^{-1}})(0.2500\ \mathrm{L}})\approx0.1125\ \mathrm{mol}`;
function entry(id){return {id,answer:'New AI result: '+reportedMath+' <img src=x onerror=alert(1)>',steps:['Calculate '+reportedMath,'Check using $\\mathrm{ClNO_2}$ and conserve the atoms.'],check:reportedMath,assumptions:[reportedMath],needsReview:false};}
function respond(r,id,status=200,body=null){r.resolve({ok:status===200,status,json:async()=>body||{answers:[entry(id)]}});}
(async()=>{
 await turn();w.ChemistryImageAssets.decode=async(src,signal)=>{if(signal?.aborted)throw new w.DOMException('Canceled','AbortError');decoded.push(src);return {width:500,height:300};};
 $('login-name').value='AI option test';$('login-form').dispatchEvent(new w.Event('submit',{cancelable:true}));
 const q=open('chem12-s1-3-q7');
 assert.equal($('generate-ai-answer').checked,false);$('check').click();
 assert.equal($('solution').hidden,false,JSON.stringify({errors,disabled:$('check').disabled,title:$('question-title').textContent,login:$('login-overlay').hidden,feedback:$('feedback').textContent}));assert.equal($('worked-solution').hidden,true);assert.equal(requests.length,0);
 assert.match($('solution-body').textContent,/Prebuilt AI answer/);
 // Enabling the option on an already revealed question is an explicit request.
 option(true,true);assert.ok($('generate-ai-answer').checked);await turn();
 assert.equal(requests.length,1);assert.equal($('worked-solution').hidden,false);assert.equal($('worked-solution-cancel').hidden,false);
 const first=requests[0],payload=JSON.parse(first.options.body);
 assert.equal(first.options.method,'POST');assert.match(payload.message,/ClNO₂/);
 assert.ok(payload.image);assert.ok(decoded.some(src=>src.endsWith('s1-3-q7-redrawn.png')));
 assert.ok(!decoded.some(src=>src.includes('s1-3-q7-solution')),'Do not send prebuilt solution diagrams in an independent solve');
 assert.ok(!payload.message.includes('REFERENCE ANSWER KEY'));assert.ok(!payload.message.includes('STUDENT WORK'));
 const originalKey=$('solution-body').innerHTML;
 respond(first,q.id);await turn();
 assert.match($('worked-solution-body').textContent,/New AI result/);assert.ok($('worked-solution-body').querySelector('.katex'));
 assert.ok(!$('worked-solution-body').querySelector('img'),'Escape generated HTML');
 assert.equal($('worked-solution-body').querySelectorAll('.math-text,.katex-error').length,0,'The reported malformed formula must typeset in all AI fields');
 const feedback=d.createElement('div');w.eval('renderAIReview')({verdict:'unassessed',feedback:reportedMath,answer_check:'',steps:[],next_step:''},feedback,'AI explanation',true);assert.ok(feedback.querySelector('.katex'));assert.equal(feedback.querySelectorAll('.math-text').length,0);
 assert.equal($('solution-body').innerHTML,originalKey);assert.equal(w.eval('current.solution'),q.solution);assert.equal(w.eval('current.answer'),q.answer);
 assert.equal($('attempt-count').textContent,'0');assert.match($('dock-solution-body').textContent,/Prebuilt AI answer[\s\S]*New AI result/);
 assert.equal([...Array(w.localStorage.length)].map((_,i)=>w.localStorage.key(i)).filter(k=>/AnswerKey|WorkedSolution/.test(k)).length,0,'Do not cache over prebuilt answers');
 // Retry makes a fresh request; cancellation ignores a late response.
 $('worked-solution-retry').click();await turn();assert.equal(requests.length,2);const retry=requests.at(-1);
 $('worked-solution-cancel').click();assert.ok(retry.options.signal.aborted);respond(retry,q.id);await turn();
 assert.match($('worked-solution-status').textContent,/canceled/);assert.equal($('worked-solution-body').textContent,'');assert.equal($('solution-body').innerHTML,originalKey);
 // Navigation aborts old work, and late completion cannot populate a new question.
 $('worked-solution-retry').click();await turn();const stale=requests.at(-1);open('chem12-s2-1-q1');
 assert.ok(stale.options.signal.aborted);respond(stale,q.id);await turn();assert.equal($('solution').hidden,true);assert.equal($('worked-solution-body').textContent,'');
 // An opt-in reveal still shows its original solution synchronously.
 $('check').click();assert.match($('solution-body').textContent,/Prebuilt AI answer/);assert.equal($('solution').hidden,false);await turn();
 let r=requests.at(-1);respond(r,'chem12-s2-1-q1',503);await turn();
 assert.match($('worked-solution-status').textContent,/HTTP 503/);assert.equal($('worked-solution-retry').hidden,false);assert.match($('solution-body').textContent,/Prebuilt AI answer/);
 // Invalid/mismatched structured results remain retryable.
 $('worked-solution-retry').click();await turn();r=requests.at(-1);respond(r,'wrong-question');await turn();
 assert.match($('worked-solution-status').textContent,/invalid|incomplete/i);assert.equal($('worked-solution-cancel').hidden,true);
 // An offline reveal does not even start a request.
 Object.defineProperty(w.navigator,'onLine',{value:false,configurable:true});open('chem12-s4-5-q1');const count=requests.length;$('check').click();await turn();
 assert.equal(requests.length,count);assert.match($('worked-solution-status').textContent,/offline/);assert.match($('solution-body').textContent,/Prebuilt AI answer/);
 Object.defineProperty(w.navigator,'onLine',{value:true,configurable:true});$('worked-solution-retry').click();await turn();r=requests.at(-1);
 // A network rejection and a timeout both leave the prebuilt answer usable.
 r.reject(new w.TypeError('Failed to fetch'));await turn();assert.match($('worked-solution-status').textContent,/Could not reach/);
 $('worked-solution-retry').click();await turn();r=requests.at(-1);timeoutGeneration();r.reject(new w.DOMException('Aborted','AbortError'));await turn();
 assert.ok(r.options.signal.aborted);assert.match($('worked-solution-status').textContent,/timed out/);
 $('worked-solution-retry').click();await turn();r=requests.at(-1);option(false);respond(r,'chem12-s4-5-q1');await turn();
 assert.ok(r.options.signal.aborted);assert.equal($('worked-solution').hidden,true);assert.equal($('dock-generate-ai-answer').checked,false);
 // Selecting before reveal generates only after Show answer, including from dock.
 open('chem12-s6-5-q12');const before=requests.length;option(true);await turn();assert.equal(requests.length,before);
 $('dock-check').click();assert.match($('solution-body').textContent,/Prebuilt AI answer/);await turn();r=requests.at(-1);respond(r,'chem12-s6-5-q12');await turn();
 assert.match($('worked-solution-body').textContent,/New AI result/);assert.deepEqual(errors,[]);
 // Verify the same math paths in feedback summaries, history, logs and new questions.
 const review={verdict:'correct',confidence:'high',answer_check:'Q_sp = [Ag^+][Cl^-]',feedback:String.raw`Use $\ce{Cl + ClNO2 -> Cl2 + NO2}$ and $\pu{0.1125 mol}$.`,steps:[],weak_points:[{skill:'K_a = 10^{-5}',evidence:reportedMath,practice:'Check Q_sp = [Ag^+][Cl^-].'}],next_step:''};
 assert.ok(w.eval('recordSubmittedAnswer')(true,'ai',review));await turn();
 assert.ok($('feedback').querySelector('.katex'));
 assert.equal($('dock-feedback').querySelectorAll('.katex').length,$('feedback').querySelectorAll('.katex').length,'Pinned feedback must clone rendered math, not MathML textContent');
 assert.ok($('weak-points').querySelector('.katex'));assert.ok($('ai-history-list').querySelector('.katex'));
 option(false);
 const data={id:'gen-00000000-0000-0000-0000-000000000001',anchorId:bank[0].id,skill:'calculations',level:2,title:'Math formatting check',question:String.raw`Calculate $n_e = 10^{-5}$ and interpret $\ce{H3O+}$.`,answer:reportedMath,steps:[reportedMath,'Q_sp = [Ag^+][Cl^-]'],check:String.raw`$\pu{0.1125 mol}$`};
 const generated=w.AdaptivePractice.problem(data,bank);assert.ok(generated);w.eval('show')(generated,'Formatting regression test');
 assert.equal($('statement').querySelectorAll('.katex').length,2,'AI-created questions also need the formatter');
 $('check').click();assert.ok($('solution-body').querySelector('.katex'));assert.equal($('solution-body').querySelectorAll('.math-text').length,0);
 const longReview={...review,answer_check:'Reasoning and substitution. '.repeat(20)+reportedMath};
 assert.ok(w.eval('recordSubmittedAnswer')(true,'ai',longReview));await turn();
 assert.match($('feedback').textContent,/See the full AI review below/,'Do not cut a formula at an arbitrary character limit');
 const full=d.createElement('div');w.eval('renderAIReview')(longReview,full);assert.ok(full.querySelector('.katex'));assert.equal(full.querySelectorAll('.math-text').length,0);
 assert.deepEqual(errors,[]);
 console.log(JSON.stringify({status:'PASS',checks:['Unchecked default makes no request','Opt-in generates answer and steps','Original answer is immutable and immediate','Question figures without solution/student work','Math, chemistry commands and escaped HTML','Feedback, history, learning log and adaptive question rendering','Pinned controls and answer mirror','Fresh retries','Cancellation and late responses','Question-switch race','Offline and HTTP/network errors','Invalid response','Timeout','No answer cache or grading side effects']}));
 dom.window.close();
})().catch(e=>{console.error(e);dom.window.close();process.exit(1);});
