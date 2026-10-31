/* CHEMISTRY_JSDOM_PATH=/path/to/jsdom node tools/test_chemistry12_follow_up.cjs */
'use strict';
const assert=require('node:assert/strict'),fs=require('node:fs'),path=require('node:path');
const {JSDOM,VirtualConsole}=require(process.env.CHEMISTRY_JSDOM_PATH||'jsdom');
const source=fs.readFileSync(path.resolve(__dirname,'../chemistry12-practice.html'),'utf8');
const bank=JSON.parse(source.match(/<script id="question-bank" type="application\/json">([\s\S]*?)<\/script>/)[1]);
const requests=[],errors=[];let timeoutRequest;
const vc=new VirtualConsole();vc.on('jsdomError',e=>errors.push(e.message));
const dom=new JSDOM(source,{url:'https://chemistry.test/chemistry12-practice.html',runScripts:'dangerously',pretendToBeVisual:true,virtualConsole:vc,beforeParse(w){
 Object.defineProperty(w.navigator,'onLine',{value:true,configurable:true});
 w.HTMLCanvasElement.prototype.getContext=()=>new Proxy({getImageData:()=>({data:new Uint8ClampedArray([255,255,255,255])})},{get:(o,k)=>o[k]||(()=>{}),set:(o,k,v)=>{o[k]=v;return true;}});
 w.HTMLCanvasElement.prototype.toDataURL=()=> 'data:image/jpeg;base64,YQ==';w.HTMLMediaElement.prototype.pause=()=>{};
 w.HTMLElement.prototype.scrollIntoView=function(){};w.HTMLDialogElement.prototype.showModal=function(){this.open=true;};w.HTMLDialogElement.prototype.close=function(){this.open=false;};
 w.fetch=(url,options)=>new Promise((resolve,reject)=>requests.push({url,options,resolve,reject}));
 const original=w.setTimeout.bind(w);w.setTimeout=(fn,ms,...args)=>{if(ms===120000)timeoutRequest=fn;return original(fn,ms,...args);};
}});
const w=dom.window,d=w.document,$=id=>d.getElementById(id),turn=()=>new Promise(r=>setTimeout(r,20));
function change(id,value){$(id).value=value;$(id).dispatchEvent(new w.Event('change'));}
function open(id){const q=bank.find(q=>q.id===id);change('practice-chapter',q.chapter);change('mode','chapter');change('chapter-question',q.id);return q;}
function ask(text){$('follow-up-input').value=text;$('follow-up-input').dispatchEvent(new w.Event('input'));$('follow-up-form').dispatchEvent(new w.Event('submit',{bubbles:true,cancelable:true}));}
function reply(request,text,status=200){request.resolve({ok:status===200,status,json:async()=>({response:JSON.stringify({reply:text})})});}
function option(on){$('generate-ai-answer').checked=on;$('generate-ai-answer').dispatchEvent(new w.Event('change'));}
function generated(id){return {answers:[{id,answer:'A fresh model answer.',steps:['First identify the ion.','Then use the equilibrium relation.'],check:'The units agree.',assumptions:[],needsReview:false}]};}
(async()=>{
 await turn();w.ChemistryImageAssets.decode=async()=>({width:500,height:300});
 $('login-name').value='Follow-up student';$('login-form').dispatchEvent(new w.Event('submit',{cancelable:true}));
 const q=open('chem12-s1-3-q7');assert.equal($('solution-follow-up').hidden,true);assert.equal(requests.length,0);
 $('check').click();assert.equal($('solution-follow-up').hidden,false);assert.equal($('dock-follow-up').hidden,false);assert.equal(requests.length,0);assert.ok($('follow-up-send').disabled);
 const original=$('solution-body').innerHTML;
 ask('Why must the chlorine atoms face each other?');await turn();assert.equal(requests.length,1);
 assert.equal($('follow-up-messages').querySelectorAll('article').length,1);assert.ok($('follow-up-send').disabled);assert.equal($('follow-up-cancel').hidden,false);
 const first=requests.at(-1),payload=JSON.parse(first.options.body),context=JSON.parse(payload.message.slice(payload.message.indexOf('\n')+1));
 assert.equal(context.question.id,q.id);assert.match(context.question.text,/ClNO₂/);assert.equal(context.originalPrebuiltAnswer,q.answer);assert.equal(context.freshAIResponse,null);assert.equal(context.recentConversation.length,0);assert.equal(context.studentQuestion,'Why must the chlorine atoms face each other?');assert.ok(payload.image);assert.ok(!payload.message.includes('Follow-up student'));
 reply(first,String.raw`A new $\ce{Cl-Cl}$ bond must form. The amount is $n=0.1125\,\mathrm{mol}$. <img src=x onerror=alert(1)>`);await turn();
 assert.equal($('follow-up-input').value,'');assert.ok($('follow-up-messages').querySelector('.katex'));assert.equal($('follow-up-messages').querySelectorAll('img,script').length,0);assert.equal($('solution-body').innerHTML,original);assert.equal($('attempt-count').textContent,'0');assert.equal(w.eval('current.solution'),q.solution);
 ask('Can you explain that with a different orientation?');await turn();const second=requests.at(-1),ctx2=JSON.parse(JSON.parse(second.options.body).message.split('\n').slice(1).join('\n'));
 assert.equal(ctx2.recentConversation.length,1);assert.equal(ctx2.recentConversation[0].student,'Why must the chlorine atoms face each other?');assert.match(ctx2.recentConversation[0].assistant,/new/);
 reply(second,'Rotate the molecule so the chlorine end meets the incoming chlorine atom.');await turn();assert.equal($('follow-up-messages').querySelectorAll('article').length,2);
 // Offline attempts keep the typed question and do not call the service.
 Object.defineProperty(w.navigator,'onLine',{value:false,configurable:true});const count=requests.length;ask('Could you show one more example?');await turn();assert.equal(requests.length,count);assert.match($('follow-up-status').textContent,/offline/);assert.equal($('follow-up-input').value,'Could you show one more example?');
 Object.defineProperty(w.navigator,'onLine',{value:true,configurable:true});ask('Could you show one more example?');await turn();let active=requests.at(-1);reply(active,'',503);await turn();assert.match($('follow-up-status').textContent,/HTTP 503/);assert.equal($('follow-up-retry').hidden,false);
 const cards=$('follow-up-messages').querySelectorAll('article').length;$('follow-up-retry').click();await turn();active=requests.at(-1);reply(active,'Try a case where an atom approaches the opposite side.');await turn();assert.equal($('follow-up-messages').querySelectorAll('article').length,cards,'Retry must not duplicate the student question');
 // Invalid structured responses are retryable and never replace the answer key.
 ask('Why is energy also required?');await turn();active=requests.at(-1);active.resolve({ok:true,status:200,json:async()=>({response:'{"reply":'})});await turn();assert.match($('follow-up-status').textContent,/incomplete/);assert.equal($('solution-body').innerHTML,original);
 $('follow-up-retry').click();await turn();active=requests.at(-1);$('follow-up-cancel').click();assert.ok(active.options.signal.aborted);reply(active,'This late text must not appear.');await turn();assert.ok(!$('follow-up-messages').textContent.includes('This late text'));assert.match($('follow-up-status').textContent,/canceled/);
 // An unfinished follow-up is canceled and its content cleared on navigation.
 $('follow-up-retry').click();await turn();active=requests.at(-1);open('chem12-s4-5-q1');assert.ok(active.options.signal.aborted);reply(active,'Another stale answer.');await turn();assert.equal($('solution-follow-up').hidden,true);assert.equal($('follow-up-messages').textContent,'');assert.equal($('follow-up-input').value,'');
 $('check').click();ask('How do I solve the quadratic?');await turn();active=requests.at(-1);timeoutRequest();active.reject(new w.DOMException('Aborted','AbortError'));await turn();assert.match($('follow-up-status').textContent,/timed out/);assert.equal($('follow-up-retry').hidden,false);
 $('follow-up-retry').click();await turn();active=requests.at(-1);active.reject(new w.TypeError('Failed to fetch'));await turn();assert.match($('follow-up-status').textContent,/Could not reach/);
 // Generate an additional answer and include that exact response in follow-ups.
 option(true);assert.equal($('follow-up-send').disabled,true);await turn();active=requests.at(-1);active.resolve({ok:true,status:200,json:async()=>generated('chem12-s4-5-q1')});await turn();
 ask('Why did your new answer use that equilibrium relation?');await turn();active=requests.at(-1);const fresh=JSON.parse(JSON.parse(active.options.body).message.split('\n').slice(1).join('\n'));
 assert.equal(fresh.freshAIResponse.answer,'A fresh model answer.');assert.deepEqual(fresh.freshAIResponse.steps,['First identify the ion.','Then use the equilibrium relation.']);reply(active,'The relation connects the equilibrium concentrations to the constant.');await turn();
 // A subsequent generation cancels an in-flight follow-up safely.
 ask('Explain step 2 again.');await turn();const old=requests.at(-1);$('worked-solution-retry').click();assert.ok(old.options.signal.aborted);assert.ok($('follow-up-send').disabled);await turn();reply(old,'Stale follow-up during new generation.');$('worked-solution-cancel').click();await turn();assert.ok(!$('follow-up-messages').textContent.includes('Stale follow-up'));
 // Student switches must discard the conversation, including pending replies.
 ask('Will this question be isolated?');await turn();active=requests.at(-1);w.eval('useStudent')('Another student');assert.ok(active.options.signal.aborted);reply(active,'Private previous conversation.');await turn();assert.equal($('follow-up-messages').textContent,'');assert.equal($('solution-follow-up').hidden,true);
 const protocol=w.ChemistryFollowUp;assert.equal(protocol.parse({response:'A plain text explanation.'}),'A plain text explanation.');assert.throws(()=>protocol.parse({ok:false}));assert.throws(()=>protocol.parse({reply:''}));
 const long=Array.from({length:20},(_,i)=>({question:'question '+i,reply:'x'.repeat(9000),status:'complete'}));const kept=protocol.history(long);assert.ok(kept.length>0&&kept.length<=12);assert.ok(JSON.stringify(kept).length<25000);assert.equal(kept.at(-1).student,'question 19');
 assert.deepEqual(errors,[]);assert.equal(d.querySelectorAll('[id]').length,new Set([...d.querySelectorAll('[id]')].map(n=>n.id)).size);
 console.log(JSON.stringify({status:'PASS',checks:['Available after either answer reveal','No automatic follow-up request','Question and prebuilt solution context','Multi-turn history','Exact fresh AI answer context','Math and safe HTML rendering','Original key and grades preserved','Offline draft retained','Retry without duplicate messages','HTTP/network/JSON failures','Cancellation and timeout','Question and student isolation','New generation cancels old chat','Bounded recent history']}));dom.window.close();
})().catch(e=>{console.error(e);dom.window.close();process.exit(1);});
