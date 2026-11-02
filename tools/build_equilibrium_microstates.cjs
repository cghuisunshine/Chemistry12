#!/usr/bin/env node
'use strict';
// Build the independent microscopic derivation with offline, pre-rendered math.
const fs=require('node:fs'),path=require('node:path');
const root=path.resolve(__dirname,'..');
const katex=require('./vendor/katex/katex.min.js');
require('./vendor/katex/mhchem.min.js');
let html=fs.readFileSync(path.join(__dirname,'equilibrium-microstates-template.html'),'utf8');
const shared=fs.readFileSync(path.join(__dirname,'ksp-thermodynamics-template.html'),'utf8').match(/<style>[\s\S]*?<\/style>/g)[1];
html=html.replace('<!-- SHARED_STYLE -->',()=>shared);
let equations=0;
function render(tex,displayMode){equations++;return katex.renderToString(tex.trim(),{displayMode,throwOnError:true,trust:false,strict:'error',output:'htmlAndMathml'});}
html=html.replace(/\\\[([\s\S]*?)\\\]/g,(_,tex)=>render(tex,true));
html=html.replace(/\\\(([\s\S]*?)\\\)/g,(_,tex)=>render(tex,false));
const css=fs.readFileSync(path.join(__dirname,'vendor/katex/katex.min.css'),'utf8').replace(/url\(fonts\//g,'url(assets/chemistry12-math/fonts/');
html=html.replace('/* KATEX_CSS */',()=>css);
fs.writeFileSync(path.join(root,'equilibrium-microstates.html'),html);
const tutorialFile=path.join(root,'tutorial.html');
let tutorial=fs.readFileSync(tutorialFile,'utf8');
if(!tutorial.includes('id="equilibrium-microstates-link"')){
 const equation='aA + bB ⇌ cC + dD: Kc = [C]ᶜ[D]ᵈ / ([A]ᵃ[B]ᵇ)';
 const marker='<div class="equation-line">'+equation+'</div>';
 if(!tutorial.includes(marker))throw Error('Could not locate the general equilibrium equation in tutorial section 2.5');
 tutorial=tutorial.replace(marker,'<div class="equation-line"><a id="equilibrium-microstates-link" href="equilibrium-microstates.html" title="Derive this equation from microscopic statistical weights">'+equation+'</a></div>');
 fs.writeFileSync(tutorialFile,tutorial);
}
console.log(JSON.stringify({output:'equilibrium-microstates.html',equations,math:'pre-rendered offline',tutorialEquationLink:true}));
