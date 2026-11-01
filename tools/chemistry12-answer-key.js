/* Missing answer keys: plain-text AI answers, cached separately from student work. */
(function(root){
'use strict';
const prefix='chemistry12AnswerKey.v1:';
const format=root.ChemistrySolutionFormat||(typeof require==='function'?require('./chemistry12-solution-format.js'):null);
function normalize(value,problem){
  const field=(v,max)=>typeof v==='string'&&v.trim()&&v.length<=max;
  if(!value||value.id!==problem.id||!field(value.answer,6000))return null;
  const steps=value.steps??[],assumptions=value.assumptions??[],check=value.check??'';
  if(!Array.isArray(steps)||steps.length>12||!steps.every(s=>field(s,4000))||!Array.isArray(assumptions)||assumptions.length>12||!assumptions.every(s=>field(s,2000))||typeof check!=='string'||check.length>4000)return null;
  if(value.needsReview!==undefined&&typeof value.needsReview!=='boolean')return null;
  return {id:problem.id,answer:value.answer.trim(),steps,check,assumptions,needsReview:value.needsReview===true};
}
function parse(envelope,problem){
  if(envelope?.ok===false||envelope?.error)throw Error('The answer service reported an error. Please retry.');
  let body=envelope?.response??envelope;
  try{if(typeof body==='string')body=JSON.parse(body.trim().replace(/^```(?:json)?\s*/i,'').replace(/\s*```$/,''));}catch{throw Error('The answer service returned an invalid answer. Please retry.');}
  const entry=Array.isArray(body?.answers)&&body.answers.length===1?normalize(body.answers[0],problem):null;
  if(!entry)throw Error('The answer service returned an incomplete answer. Please retry.');
  return entry;
}
const escape=value=>String(value).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
function apply(problem,entry){
  problem.answer=entry.answer;problem.hasAnswer=true;problem.answerSource='cached-ai';problem.hasWorkedSteps=entry.steps.length>0;
  problem.solutionHash=null;
  problem.solution='<div class="answer-provenance" data-answer-source="cached-ai"><span class="badge">AI-generated answer</span></div><p class="small">Saved on this device · separate from the textbook answer key.</p>'+
    '<p class="prebuilt-answer" style="white-space:pre-wrap"><strong>'+format.text(entry.answer)+'</strong></p>'+
    (entry.steps.length?'<h3>Step-by-step solution</h3><ol class="worked-steps">'+entry.steps.map(s=>'<li style="white-space:pre-wrap">'+format.text(format.cleanStep(s))+'</li>').join('')+'</ol>':'')+
    (entry.check?'<p style="white-space:pre-wrap"><strong>Check:</strong> '+format.text(entry.check)+'</p>':'')+
    (entry.needsReview?'<p class="small">AI answer flagged for review.</p>':'')+
    (entry.assumptions.length?'<h3>Assumptions</h3><ul>'+entry.assumptions.map(s=>'<li>'+format.text(format.cleanStep(s))+'</li>').join('')+'</ul>':'');
}
function restore(problem,storage){
  if(problem.hasAnswer||!problem.answerHash)return false;
  try{const saved=JSON.parse(storage.getItem(prefix+problem.id));if(saved?.sourceHash!==problem.answerHash)return false;const entry=normalize(saved,problem);if(!entry)return false;apply(problem,entry);return true;}catch{return false;}
}
function save(problem,entry,storage){
  apply(problem,entry);
  try{storage.setItem(prefix+problem.id,JSON.stringify({...entry,sourceHash:problem.answerHash,generatedAt:new Date().toISOString(),provenance:'cached-ai'}));return true;}catch{return false;}
}
function prompt(problem){const shared=root.ChemistrySolutionPrompt||(typeof require==='function'?require('./chemistry12-solution-prompt.js'):null);return shared.prompt(problem);}
const api={normalize,parse,apply,restore,save,prompt};
if(typeof module!=='undefined')module.exports=api;root.ChemistryAnswerKey=api;
})(typeof window!=='undefined'?window:globalThis);
