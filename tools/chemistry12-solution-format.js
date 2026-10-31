/* Safe, offline math typography for current and already-cached AI solutions. */
(function(root){
'use strict';
const escape=s=>String(s).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const katex=root.katex||(typeof require==='function'?require('./vendor/katex/katex.min.js'):null);
function cleanStep(value){return String(value).replace(/^\s*(?:(?:\d+\\?[.)]|step\s+\d+\s*[:.)])\s+)+/i,'').trim();}
function tex(value){
  const sub='₀₁₂₃₄₅₆₇₈₉₊₋₌₍₎',sup='⁰¹²³⁴⁵⁶⁷⁸⁹⁺⁻⁼⁽⁾';
  return value.replace(/([A-Za-zΑ-ω])\u20d7/g,'\\vec{$1}')
    .replace(/([τFvEaKp])net\b/g,'$1_{\\mathrm{net}}')
    .replace(/[₀₁₂₃₄₅₆₇₈₉₊₋₌₍₎]+/g,s=>'_{'+[...s].map(c=>'0123456789+-=()'[sub.indexOf(c)]).join('')+'}')
    .replace(/[⁰¹²³⁴⁵⁶⁷⁸⁹⁺⁻⁼⁽⁾]+/g,s=>'^{'+[...s].map(c=>'0123456789+-=()'[sup.indexOf(c)]).join('')+'}')
    .replace(/ℓ/g,'\\ell ').replace(/°/g,'^{\\circ}').replace(/−/g,'-')
    .replace(/\b(sin|cos|tan|ln|log)\b/g,'\\$1 ');
}
function math(value,display=false,unicode=false){
  try{return '<span class="solution-math'+(display?' solution-math-block':'')+'">'+katex.renderToString(unicode?tex(value):value,{displayMode:display,throwOnError:true,trust:false,strict:'ignore',maxExpand:200,maxSize:10,output:'htmlAndMathml'})+'</span>';}
  catch{return '<span class="math-text">'+escape(value)+'</span>';}
}
// Conservative legacy recognition: only expressions with explicit operators,
// decorated variables, and single Greek symbols. Prose remains ordinary text.
const variable='(?:[Α-ωℓ]net|[A-Za-zΑ-ωℓ]{1,2}|[A-ZΑ-ωℓ]{3,6})[\\u20d7₀₁₂₃₄₅₆₇₈₉⁰¹²³⁴⁵⁶⁷⁸⁹⁺⁻]*';
const number='(?:\\d+(?:\\.\\d+)?)(?:[⁰¹²³⁴⁵⁶⁷⁸⁹⁺⁻]+|°)?';
const paren='\\([A-Za-zΑ-ωℓ\\d₀₁₂₃₄₅₆₇₈₉⁰¹²³⁴⁵⁶⁷⁸⁹+−*/. =]{1,50}\\)';
const atom='(?:'+variable+'|'+number+'|'+paren+')(?:'+paren+')*';
const expression=new RegExp('(?<![A-Za-zΑ-ωℓ\\d])(?:'+atom+'(?:[ \\t]*(?:[=+−×·*/]|\\b(?:sin|cos|tan)\\b)[ \\t]*'+atom+')+|[A-Za-zΑ-ω][\\u20d7₀₁₂₃₄₅₆₇₈₉⁰¹²³⁴⁵⁶⁷⁸⁹⁺⁻]+|[Α-ωℓ])(?![A-Za-zΑ-ωℓ\\d])','gu');
function plain(value){
  let out='',last=0;
  for(const m of value.matchAll(expression)){out+=escape(value.slice(last,m.index))+math(m[0],false,true);last=m.index+m[0].length;}
  return out+escape(value.slice(last));
}
function text(value){
  value=String(value);let out='',last=0;
  const delimited=/\$\$([\s\S]+?)\$\$|\\\[([\s\S]+?)\\\]|\\\(([\s\S]+?)\\\)|(?<![\\\d])\$([^$\n]+?)\$/g;
  for(const m of value.matchAll(delimited)){
    out+=plain(value.slice(last,m.index))+math(m[1]??m[2]??m[3]??m[4],m[1]!==undefined||m[2]!==undefined);last=m.index+m[0].length;
  }
  return out+plain(value.slice(last));
}
function enhance(container){
  // Never revisit KaTeX-generated nodes or change image-based textbook keys.
  const walker=container.ownerDocument.createTreeWalker(container,4),nodes=[];
  while(walker.nextNode())if(!walker.currentNode.parentElement.closest('.katex,.solution-math,.math-text,script,style'))nodes.push(walker.currentNode);
  for(const node of nodes){const t=container.ownerDocument.createElement('template');t.innerHTML=text(node.textContent);node.replaceWith(t.content);}
  for(const li of container.querySelectorAll('ol > li')){
    const first=li.firstChild;if(first?.nodeType===3)first.textContent=cleanStep(first.textContent);
  }
}
const api={text,cleanStep,enhance};
if(typeof module!=='undefined')module.exports=api;root.ChemistrySolutionFormat=api;
})(typeof window!=='undefined'?window:globalThis);
