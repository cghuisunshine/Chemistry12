/* Offline contract checks; no AI service requests. */
'use strict';
const fs=require('node:fs'),path=require('node:path'),assert=require('node:assert/strict'),{spawnSync}=require('node:child_process');
const root=path.resolve(__dirname,'..');
const shared=require('./chemistry12-solution-prompt.js');
const keys=require('./chemistry12-answer-key.js');
globalThis.ChemistryAnswerKey=keys;
const worked=require('./chemistry12-worked-solution.js');
const html=fs.readFileSync(path.join(root,'chemistry12-practice.html'),'utf8');
const bank=JSON.parse(html.match(/<script id="question-bank" type="application\/json">([\s\S]*?)<\/script>/)[1]);
for(const q of bank){
 const input={...q,answer:'PRIVATE OLD ANSWER MARKER',solution:'PRIVATE OLD SOLUTION MARKER'};
 const p=shared.prompt(input);
 assert.equal(keys.prompt(input),p);
 assert.equal(worked.prompt(input,'PRIVATE OLD KEY MARKER'),p);
 for(const secret of ['PRIVATE OLD ANSWER MARKER','PRIVATE OLD SOLUTION MARKER','PRIVATE OLD KEY MARKER'])assert.ok(!p.includes(secret));
 assert.ok(p.includes('EVERY requested subpart'));
 assert.ok(p.includes('independent, question-specific check'));
}
const result=spawnSync('python3',['tools/save_chemistry12_session_answers.py','--question','chem12-s1-3-q7'],{cwd:root,encoding:'utf8',env:{...process.env,PYTHONDONTWRITEBYTECODE:'1'}});
assert.equal(result.status,0,result.stderr);const request=JSON.parse(result.stdout);
const q=bank.find(q=>q.id===request.id);
assert.equal(request.prompt,keys.prompt(q));assert.equal(request.promptVersion,shared.version);
assert.ok(request.images.some(p=>p.endsWith('s1-3-q7-redrawn.png')));
assert.ok(!request.images.some(p=>p.includes('s1-3-q7-solution')));
const prebuilt=JSON.parse(fs.readFileSync(path.join(root,'content/chemistry12/prebuilt-answers.json'),'utf8')).answers;
let reviewed=0;
for(const e of Object.values(prebuilt))if(e.authoring?.promptVersion===shared.version){
 assert.equal(e.authoring.mode,'one-question-at-a-time-in-session');
 assert.match(e.generatedBy,/no external endpoint/);assert.ok(e.authoring.review.trim());
 const q=bank.find(q=>q.id===e.id);
 const hash=require('node:crypto').createHash('sha256').update(shared.prompt(q)).digest('hex');
 assert.equal(e.authoring.promptHash,hash);reviewed++;
}
assert.equal(reviewed,bank.length,'Every prebuilt entry must retain its current-prompt in-session review receipt');
console.log(JSON.stringify({status:'PASS',identicalPromptQuestions:bank.length,inSessionReviewed:reviewed,pending:bank.length-reviewed,checks:['Fresh prompt aliases agree','Old answer excluded','Offline authoring exports exact live prompt','Question-only source image parity','In-session provenance and prompt receipts']}));
