/* Safe, offline math typography for current and already-cached AI solutions. */
(function(root){
'use strict';
const escape=s=>String(s).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const katex=root.katex||(typeof require==='function'?require('./vendor/katex/katex.min.js'):null);
if(typeof module!=='undefined'&&module.exports)require('./vendor/katex/mhchem.min.js');
function cleanStep(value){return String(value).replace(/^\s*(?:(?:\d+\\?[.)]|step\s+\d+\s*[:.)])\s+)+/i,'').trim();}
function tex(value,legacy=false){
  const sub='₀₁₂₃₄₅₆₇₈₉₊₋₌₍₎',sup='⁰¹²³⁴⁵⁶⁷⁸⁹⁺⁻⁼⁽⁾';
  const result=value.replace(/([A-Za-zΑ-ω])\u20d7/g,'\\vec{$1}')
    .replace(/([τFvEaKp])net\b/g,'$1_{\\mathrm{net}}')
    .replace(/[₀₁₂₃₄₅₆₇₈₉₊₋₌₍₎]+/g,s=>'_{'+[...s].map(c=>'0123456789+-=()'[sub.indexOf(c)]).join('')+'}')
    .replace(/[⁰¹²³⁴⁵⁶⁷⁸⁹⁺⁻⁼⁽⁾]+/g,s=>'^{'+[...s].map(c=>'0123456789+-=()'[sup.indexOf(c)]).join('')+'}')
    .replace(/ℓ/g,'\\ell ').replace(/°/g,'^{\\circ}').replace(/−/g,'-')
    .replace(/(?<![A-Za-z\\])(\d+(?:\.\d+)?)[eE]([+-]?\d+)(?![A-Za-z\d])/g,'$1\\times 10^{$2}')
    .replace(/([_^])([+-]\d+|\d{2,})/g,'$1{$2}')
    .replace(/_(sp|net|eq|total|initial|final)(?![A-Za-z])/g,'_{\\mathrm{$1}}');
  return legacy?result.replace(/(?<!\\)\b(sin|cos|tan|ln|log)\b/g,'\\$1 '):result;
}
// Repair grouping only after the original expression fails to parse. Escaped
// braces are literal symbols. No quantities, operators or unit powers change.
function balanceGroups(value){
  let out='',depth=0;
  for(let i=0;i<value.length;i++){
    const c=value[i];
    if(c==='\\'&&i+1<value.length){out+=c+value[++i];continue;}
    if(c==='{'){depth++;out+=c;}
    else if(c==='}'){if(depth){depth--;out+=c;}}
    else out+=c;
  }
  return out+'}'.repeat(depth);
}
function math(value,display=false,unicode=false){
  // A doubled command slash is a JSON-escaping mistake. Do not touch real
  // matrix/align row separators or triple-slash row-plus-command sequences.
  const normalized=value.replace(/(?<!\\)\\\\(?=(?:frac|dfrac|tfrac|sqrt|mathrm|mathbf|text|ce|pu)\b)/g,'\\')
    .replace(/^\\[[(]/,'').replace(/\\[)\]]$/,'')
    .replace(/\\(begin|end)\{(?:align\*?|split)\}/g,'\\$1{aligned}')
    .replace(/\\(begin|end)\{gather\*?\}/g,'\\$1{gathered}')
    .replace(/\\(?:begin|end)\{equation\*?\}/g,'');
  const input=tex(normalized,unicode),options={displayMode:display,throwOnError:true,trust:false,strict:'ignore',maxExpand:1000,maxSize:10,output:'htmlAndMathml'};
  const balanced=balanceGroups(input);
  for(const candidate of new Set([input,balanced,balanced.replace(/\\(?:left|right)\b/g,'')])){
    try{return '<span class="solution-math'+(display?' solution-math-block':'')+'">'+katex.renderToString(candidate,options)+'</span>';}
    catch{} // Try a grouping repair, then preserve a safe text fallback.
  }
  return '<span class="math-text">'+escape(value)+'</span>';
}
// Conservative legacy recognition: only expressions with explicit operators,
// decorated variables, and single Greek symbols. Prose remains ordinary text.
const variable='(?:[Α-ωℓ]net|[A-Za-zΑ-ωℓ]{1,2}|[A-ZΑ-ωℓ]{3,6})[\\u20d7₀₁₂₃₄₅₆₇₈₉⁰¹²³⁴⁵⁶⁷⁸⁹⁺⁻]*';
const number='(?:\\d+(?:\\.\\d+)?)(?:[⁰¹²³⁴⁵⁶⁷⁸⁹⁺⁻]+|°)?';
const paren='\\([A-Za-zΑ-ωℓ\\d₀₁₂₃₄₅₆₇₈₉⁰¹²³⁴⁵⁶⁷⁸⁹+−*/. =]{1,50}\\)';
const atom='(?:'+variable+'|'+number+'|'+paren+')(?:'+paren+')*';
const expression=new RegExp('(?<![A-Za-zΑ-ωℓ\\d])(?:'+atom+'(?:[ \\t]*(?:[=+−×·*/]|\\b(?:sin|cos|tan)\\b)[ \\t]*'+atom+')+|[A-Za-zΑ-ω][\\u20d7₀₁₂₃₄₅₆₇₈₉⁰¹²³⁴⁵⁶⁷⁸⁹⁺⁻]+|[Α-ωℓ])(?![A-Za-zΑ-ωℓ\\d])','gu');
function legacy(value){
  let out='',last=0;
  for(const m of value.matchAll(expression)){out+=escape(value.slice(last,m.index))+math(m[0],false,true);last=m.index+m[0].length;}
  return (out+escape(value.slice(last))).replace(/\\\$/g,'$');
}
// AI sometimes omits math delimiters. Recognize a maximal run of math tokens
// only when it contains a TeX command; ordinary sentence words stop the run.
// Braced command arguments may contain words (e.g. \mathrm{mol\,L^{-1}}).
function rawRun(value,start){
  if(/\s/.test(value[start]))return null;
  if(/[A-Za-zΑ-ωℓ\d]/u.test(value[start])&&start&&/[A-Za-zΑ-ωℓ\d]/u.test(value[start-1]))return null;
  let i=start,end=start,depth=0,command=false,decorated=false,operand=false;
  while(i<value.length){
    const rest=value.slice(i),c=value[i];let m;
    if(c==='\\'){
      m=rest.match(/^\\(?:[A-Za-z]+\*?|[^\r\n])/);
      if(!m)break;
      if(/^\\[A-Za-z]/.test(m[0]))command=true;
      i+=m[0].length;end=i;continue;
    }
    if(c==='{'){depth++;i++;end=i;continue;}
    if(c==='}'){depth=Math.max(0,depth-1);i++;end=i;continue;}
    if(/[ \t]/.test(c)){i++;continue;}
    if(/[\r\n]/.test(c))break;
    m=rest.match(/^(?:\d+(?:\.\d+)?|\.\d+)(?:[eE][+-]?\d+)?/);
    if(m){if(/[eE]/.test(m[0]))decorated=true;operand=true;i+=m[0].length;end=i;continue;}
    m=rest.match(/^[A-Za-zΑ-ωℓ][A-Za-zΑ-ωℓ0-9]*/u);
    if(m){
      if(!depth&&!/^(?:[A-Za-zΑ-ωℓ]|[a-z][A-Z]|[A-Z][a-z]?(?:[A-Z][a-z]?|\d)*|pH|pOH|Ksp|Ka|Kb|Kw|sp|net|eq|total|initial|final|ln|log|sin|cos|tan|exp|mol|mmol|min|Pa|kPa|atm|kJ|mL|kg)$/u.test(m[0]))break;
      operand=true;i+=m[0].length;end=i;continue;
    }
    if(depth||/[()[\]^_=+*/<>|,:!%&\-−×·≈±∞°₀-₉⁰¹²³⁴⁵⁶⁷⁸⁹⁺⁻]/u.test(c)){
      if(operand&&/[_^₀-₉⁰¹²³⁴⁵⁶⁷⁸⁹⁺⁻]/u.test(c))decorated=true;
      i++;end=i;continue;
    }
    break;
  }
  return end>start?{end,command:command||decorated}:null;
}
// Environments may contain row breaks, multiletter identifiers and text.
// Consume the complete matching environment before the inline token lexer.
function environment(value,start){
  const open=value.slice(start).match(/^\\begin\{(aligned|alignedat|align\*?|split|gathered|gather\*?|equation\*?|cases|array|[pbBvV]?matrix|smallmatrix)\}/);
  if(!open)return null;
  const name=open[1],pattern=/\\(begin|end)\{([^{}]+)\}/g;pattern.lastIndex=start;
  let depth=0,m;
  while((m=pattern.exec(value))){
    if(m[2]!==name)continue;
    depth+=m[1]==='begin'?1:-1;
    if(!depth)return {end:pattern.lastIndex,command:true,display:true};
  }
  return null;
}
function plain(value){
  let out='',last=0,i=0;
  while(i<value.length){
    const dollars=value.startsWith('$$',i)?2:value[i]==='$'?1:0,start=i+dollars;
    const run=environment(value,start)||rawRun(value,start);
    if(run?.command){
      out+=legacy(value.slice(last,i))+math(value.slice(start,run.end),!!run.display||dollars===2);last=run.end;
      if(value[last]==='$'&&!/\d/.test(value[last+1]||''))last+=value.startsWith('$$',last)?2:1;
      i=last;
    }
    else i=run?Math.max(i+1,run.end):i+1;
  }
  return out+legacy(value.slice(last));
}
function text(value){
  value=String(value);let out='',last=0;
  const delimited=/(?<!\\)\$\$([\s\S]+?)(?<!\\)\$\$|\\\[([\s\S]+?)\\\]|\\\(([\s\S]+?)\\\)|(?<![\\\d])\$((?:\\\$|[^$\n])+?)(?<!\\)\$/g;
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
const instructions=String.raw`Write every mathematical expression inside $...$ for inline math or $$...$$ for a display. Use KaTeX-compatible LaTeX, with balanced braces and matching delimiters. Write chemical species and units with \mathrm{...}, subscripts and superscripts. Chemical equations may also use \ce{...}, and units may use \pu{...}. Always brace the complete exponent, such as 10^{-14} and L^{-1}. For example: $(0.450\,\mathrm{mol\,L^{-1}})(0.2500\,\mathrm{L})\approx0.1125\,\mathrm{mol}$. Do not emit raw TeX outside math delimiters. In JSON, escape each LaTeX backslash as two backslashes. Do not number step strings or use HTML.`;
const api={text,cleanStep,enhance,instructions};
if(typeof module!=='undefined')module.exports=api;root.ChemistrySolutionFormat=api;
})(typeof window!=='undefined'?window:globalThis);
