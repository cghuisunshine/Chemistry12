#!/usr/bin/env node
'use strict';
// Pre-render every equation with the existing local KaTeX distribution.
// The resulting article needs no math service, CDN or runtime math script.
const fs=require('node:fs'),path=require('node:path');
const root=path.resolve(__dirname,'..');
const katex=require('./vendor/katex/katex.min.js');
require('./vendor/katex/mhchem.min.js');
let html=fs.readFileSync(path.join(__dirname,'ksp-thermodynamics-template.html'),'utf8');
// Stack enlarged views of the same exact diagram on narrow screens.
html=html.replace(/<svg viewBox="0 0 760 285"[\s\S]*?<\/svg>/,svg=>{
 const clean=svg.replace(/<defs>[\s\S]*?<\/defs>/,'');
 const panel=(view,suffix)=>clean.replace('viewBox="0 0 760 285"',`viewBox="${view}"`).replaceAll('mix-title',`mix-title-${suffix}`).replaceAll('mix-desc',`mix-desc-${suffix}`);
 return '<div class="mix-wide">'+svg+'</div><div class="mix-narrow">'+panel('10 0 320 270','before')+panel('430 0 310 270','after')+'</div>';
});
html=html.replace('</style>\n</head>','\n.mix-narrow{display:none}@media(max-width:750px){.mix-wide{display:none}.mix-narrow{display:grid;gap:12px}}@media print{.mix-wide{display:block}.mix-narrow{display:none}}\n</style>\n</head>');
let equations=0;
function render(tex,displayMode){equations++;return katex.renderToString(tex.trim(),{displayMode,throwOnError:true,trust:false,strict:'error',output:'htmlAndMathml'});}
html=html.replace(/\\\[([\s\S]*?)\\\]/g,(_,tex)=>render(tex,true));
html=html.replace(/\\\(([\s\S]*?)\\\)/g,(_,tex)=>render(tex,false));
const css=fs.readFileSync(path.join(__dirname,'vendor/katex/katex.min.css'),'utf8').replace(/url\(fonts\//g,'url(assets/chemistry12-math/fonts/');
html=html.replace('/* KATEX_CSS */',css);
const output=path.join(root,'ksp-thermodynamics.html');
fs.writeFileSync(output,html);
const tutorialFile=path.join(root,'tutorial.html');
let tutorial=fs.readFileSync(tutorialFile,'utf8');
if(!tutorial.includes('id="ksp-thermodynamics-link"')){
 const marker='<section class="further-explain" aria-labelledby="further-3-3">';
 if(!tutorial.includes(marker))throw Error('Could not locate the section 3.3 deep-dive insertion point');
 tutorial=tutorial.replace(marker,'<aside class="reading-note" id="ksp-thermodynamics-link"><p><strong>Go deeper:</strong> <a href="ksp-thermodynamics.html">Derive Ksp from thermodynamics and understand the entropy of mixing</a>. Follow the second law through chemical potentials to the concentration powers, with fully rendered equations and worked checks.</p></aside>'+marker);
 fs.writeFileSync(tutorialFile,tutorial);
}
console.log(JSON.stringify({output:'ksp-thermodynamics.html',equations,math:'pre-rendered offline',tutorialLink:true}));
