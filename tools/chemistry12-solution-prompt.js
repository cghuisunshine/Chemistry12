/* One question-only teaching prompt for fresh answers and offline authoring. */
(function(root){
'use strict';
const embedded=/* SOLUTION_PROMPT_SPEC */null;
const spec=embedded||(typeof require==='function'?require('../content/chemistry12/solution-prompt.json'):null);
const format=root.ChemistrySolutionFormat||(typeof require==='function'?require('./chemistry12-solution-format.js'):null);
function prompt(problem){
  const schema={answers:[{id:problem.id,answer:'complete final answer for every subpart',steps:['substantive teaching step'],check:'independent question-specific check',assumptions:[],needsReview:false}]};
  return spec.instructions+' '+format.instructions+'\nReturn schema: '+JSON.stringify(schema)+'\nQuestion: '+JSON.stringify({id:problem.id,title:problem.title,text:problem.questionText});
}
const api={version:spec.version,prompt};
if(typeof module!=='undefined')module.exports=api;root.ChemistrySolutionPrompt=api;
})(typeof window!=='undefined'?window:globalThis);
