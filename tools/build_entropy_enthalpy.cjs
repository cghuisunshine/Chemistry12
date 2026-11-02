#!/usr/bin/env node
'use strict';
// Render equations and the initial explorer locally; reading needs no math CDN.
const fs=require('node:fs'),path=require('node:path');
const root=path.resolve(__dirname,'..');
const katex=require('./vendor/katex/katex.min.js');
require('./vendor/katex/mhchem.min.js');
const model=require('./entropy-enthalpy-model.js');
let html=fs.readFileSync(path.join(__dirname,'entropy-enthalpy-template.html'),'utf8');
const shared=fs.readFileSync(path.join(__dirname,'ksp-thermodynamics-template.html'),'utf8').match(/<style>([\s\S]*?)<\/style>/g)[1];
html=html.replace('<!-- SHARED_STYLE -->',shared);
let equations=0;
const render=(tex,displayMode)=>{equations++;return katex.renderToString(tex.trim(),{displayMode,throwOnError:true,trust:false,strict:'error',output:'htmlAndMathml'});};
html=html.replace(/\\\[([\s\S]*?)\\\]/g,(_,tex)=>render(tex,true));
html=html.replace(/\\\(([\s\S]*?)\\\)/g,(_,tex)=>render(tex,false));
html=html.replace('/* KATEX_CSS */',fs.readFileSync(path.join(__dirname,'vendor/katex/katex.min.css'),'utf8').replace(/url\(fonts\//g,'url(assets/chemistry12-math/fonts/'));
html=html.replace('<!-- INITIAL_PLOT -->',model.plot(-92.22,-198.11,298.15));
html=html.replace('<!-- MODEL_SCRIPT -->','<script>\n'+fs.readFileSync(path.join(__dirname,'entropy-enthalpy-model.js'),'utf8')+'\n</script>');
html=html.replace('<!-- EXPLORER_SCRIPT -->','<script>\n'+fs.readFileSync(path.join(__dirname,'entropy-enthalpy-explorer.js'),'utf8')+'\n</script>');
fs.writeFileSync(path.join(root,'entropy-enthalpy.html'),html);
const tutorialFile=path.join(root,'tutorial.html');
let tutorial=fs.readFileSync(tutorialFile,'utf8');
if(!tutorial.includes('id="entropy-enthalpy-link"')){
 const marker='<h4 id="further-2-4">Further explain</h4>';
 if(!tutorial.includes(marker))throw Error('Could not locate tutorial section 2.4');
 tutorial=tutorial.replace(marker,marker+'<aside class="reading-note" id="entropy-enthalpy-link"><p><strong>Go deeper:</strong> <a href="entropy-enthalpy.html">Entropy versus enthalpy: from thermodynamic laws to Gibbs energy</a>. A university-level lesson with step-by-step derivations, microstates, worked examples, chemical equilibrium and an interactive temperature explorer. Equations work offline.</p></aside>');
 fs.writeFileSync(tutorialFile,tutorial);
}
console.log(JSON.stringify({output:'entropy-enthalpy.html',equations,math:'pre-rendered offline',tutorialLink:true}));
