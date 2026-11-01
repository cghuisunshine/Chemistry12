/* Worked solutions are separate from final keys and student submissions. */
(function(root){
'use strict';
const prefix='chemistry12WorkedSolution.v1:';
const format=root.ChemistrySolutionFormat||(typeof require==='function'?require('./chemistry12-solution-format.js'):null);
const escape=s=>String(s).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
function hash(problem){return problem.solutionHash||JSON.stringify([problem.id,problem.questionText,problem.html,problem.solution]);}
function normalize(value,problem){
  const entry=root.ChemistryAnswerKey.normalize(value,problem);
  return entry&&entry.steps.length>=2?entry:null;
}
function parse(envelope,problem){
  const entry=normalize(root.ChemistryAnswerKey.parse(envelope,problem),problem);
  if(!entry)throw Error('The service did not return a step-by-step solution. Please retry.');
  return entry;
}
function restore(problem,storage){
  try{const saved=JSON.parse(storage.getItem(prefix+problem.id));return saved?.sourceHash===hash(problem)?normalize(saved,problem):null;}catch{return null;}
}
function save(problem,entry,storage){
  try{storage.setItem(prefix+problem.id,JSON.stringify({...entry,sourceHash:hash(problem),generatedAt:new Date().toISOString(),provenance:'cached-ai-solution'}));return true;}catch{return false;}
}
function render(entry){
  return '<p class="small">Fresh AI-generated answer and worked solution · the original prebuilt key above is unchanged.</p><p class="prebuilt-answer" style="white-space:pre-wrap"><strong>'+format.text(entry.answer)+'</strong></p><ol class="worked-steps">'+entry.steps.map(s=>'<li style="white-space:pre-wrap">'+format.text(format.cleanStep(s))+'</li>').join('')+'</ol>'+
    (entry.check?'<p style="white-space:pre-wrap"><strong>Check:</strong> '+format.text(entry.check)+'</p>':'')+
    (entry.needsReview?'<p class="small">AI solution flagged for review. Compare it with the answer key above.</p>':'')+
    (entry.assumptions.length?'<h4>Assumptions / review notes</h4><ul>'+entry.assumptions.map(s=>'<li>'+format.text(format.cleanStep(s))+'</li>').join('')+'</ul>':'');
}
function prompt(problem){const shared=root.ChemistrySolutionPrompt||(typeof require==='function'?require('./chemistry12-solution-prompt.js'):null);return shared.prompt(problem);}
const api={hash,normalize,parse,restore,save,render,prompt};
if(typeof module!=='undefined')module.exports=api;root.ChemistryWorkedSolution=api;
})(typeof window!=='undefined'?window:globalThis);
