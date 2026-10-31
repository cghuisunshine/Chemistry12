/* CHEMISTRY_JSDOM_PATH=/path/to/jsdom node tools/test_chemistry12_solution_format.cjs */
'use strict';
const assert=require('node:assert/strict');
const {JSDOM}=require(process.env.CHEMISTRY_JSDOM_PATH||'jsdom');
const format=require('./chemistry12-solution-format.js');
const dom=new JSDOM('<main></main>'),d=dom.window.document;
const example=String.raw`(0.450\ \mathrm{mol\,L^{-1}})(0.2500\ \mathrm{L}})\approx0.1125\ \mathrm{mol}`;
const expected=String.raw`(0.450\ \mathrm{mol\,L^{-1}})(0.2500\ \mathrm{L})\approx0.1125\ \mathrm{mol}`;
function parse(value){const el=d.createElement('div');el.innerHTML=format.text(value);return el;}
function rendered(value,annotation,display=false){
 const el=parse(value);assert.equal(el.querySelectorAll('.katex').length,1,value);
 assert.equal(el.querySelectorAll('.math-text,.katex-error').length,0,value);
 assert.equal(el.querySelector('annotation[encoding="application/x-tex"]').textContent,annotation);
 assert.equal(!!el.querySelector('.solution-math-block'),display);
 assert.ok(!el.querySelector('.katex .katex'),'Do not render math twice');
 return el;
}
// The user's exact raw example, with the extra unit brace, including every digit.
const sample=rendered(example,expected);
const visible=sample.querySelector('.katex-html').textContent;
for(const quantity of ['0.450','0.2500','0.1125','mol','L'])assert.ok(visible.includes(quantity));
assert.ok(sample.querySelector('.msupsub'),'L⁻¹ must be rendered as a unit power');
for(const [before,after,display] of [['$','$',false],['$$','$$',true],['\\(','\\)',false],['\\[','\\]',true]])rendered(before+example+after,expected,display);
rendered(String.raw`\frac{1}{2`,String.raw`\frac{1}{2}`);
rendered(String.raw`$\{x\}+\frac{1}{2}$`,String.raw`\{x\}+\frac{1}{2}`);
rendered(String.raw`$K_a=\frac{[\mathrm{H_3O^+}][\mathrm{A^-}]}{[\mathrm{HA}]}$`,String.raw`K_a=\frac{[\mathrm{H_3O^+}][\mathrm{A^-}]}{[\mathrm{HA}]}`);
rendered(String.raw`\sqrt{K_a C}`,String.raw`\sqrt{K_a C}`);
const regressions=[
 ['K_a = 10^{-5}','K_a = 10^{-5}'],
 ['10^-14','10^{-14}'],
 ['x_12 = 3','x_{12} = 3'],
 ['Q_sp = [Ag^+][Cl^-]',String.raw`Q_{\mathrm{sp}} = [Ag^+][Cl^-]`],
 ['[H₃O⁺] = 1.0e-7 M',String.raw`[H_{3}O^{+}] = 1.0\times 10^{-7} M`],
 [String.raw`$\mathrm{mol\,L^-1}$`,String.raw`\mathrm{mol\,L^{-1}}`],
 [String.raw`$\\frac{1}{2}$`,String.raw`\frac{1}{2}`],
 [String.raw`$\\mathrm{mol\,L^{-1}}$`,String.raw`\mathrm{mol\,L^{-1}}`],
 [String.raw`$\left(\frac{1}{2})$`,String.raw`(\frac{1}{2})`],
 [String.raw`$\left(\frac{1}{2}\right)$`,String.raw`\left(\frac{1}{2}\right)`],
 [String.raw`\ce{Fe^{3+} + e- -> Fe^{2+}}`,String.raw`\ce{Fe^{3+} + e- -> Fe^{2+}}`],
 [String.raw`$\ce{2H2 + O2 -> 2H2O}$`,String.raw`\ce{2H2 + O2 -> 2H2O}`],
 [String.raw`$\pu{0.450 mol L-1}$`,String.raw`\pu{0.450 mol L-1}`],
 [String.raw`\begin{aligned}n&=cV\\&=0.1125\ \mathrm{mol}\end{aligned}`,String.raw`\begin{aligned}n&=cV\\&=0.1125\ \mathrm{mol}\end{aligned}`,true],
 [String.raw`\begin{align*}n&=cV\\&=0.1125\ \mathrm{mol}\end{align*}`,String.raw`\begin{aligned}n&=cV\\&=0.1125\ \mathrm{mol}\end{aligned}`,true],
 [String.raw`\begin{equation}n=cV\end{equation}`,'n=cV',true],
 [String.raw`$$\begin{pmatrix}1&2\\3&4\end{pmatrix}$$`,String.raw`\begin{pmatrix}1&2\\3&4\end{pmatrix}`,true],
 [String.raw`$$\begin{pmatrix}1&2\\\frac{1}{2}&4\end{pmatrix}$$`,String.raw`\begin{pmatrix}1&2\\\frac{1}{2}&4\end{pmatrix}`,true],
 [String.raw`\(n=\frac{1}{2}`,String.raw`n=\frac{1}{2}`],
 [String.raw`$K_a=10^{-5}`,String.raw`K_a=10^{-5}`],
 [String.raw`K_a=10^{-5}$`,String.raw`K_a=10^{-5}`],
 [String.raw`$\text{cost \$5}$`,String.raw`\text{cost \$5}`],
];
for(const [value,expected,display=false] of regressions)rendered(value,expected,display);
assert.equal(parse(String.raw`The price is \$5 and \$10.`).textContent,'The price is $5 and $10.');
const adjacent=parse('$x=1$ and $y=2$');assert.equal(adjacent.querySelectorAll('.katex').length,2);assert.ok(adjacent.textContent.includes(' and '));
const prose=parse('Using '+example+'. Therefore the calculated amount is correct.');
assert.ok(prose.firstChild.textContent.startsWith('Using '));assert.ok(prose.lastChild.textContent.endsWith('. Therefore the calculated amount is correct.'));
const normal='The solution is acidic. Compare the acid and its conjugate base; do not change the units.';
assert.equal(parse(normal).innerHTML,normal);
const unsafe=parse(String.raw`<img src=x onerror=alert(1)> $\href{javascript:alert(1)}{x}$`);
assert.equal(unsafe.querySelectorAll('img,script,a[href]').length,0,'Untrusted generated text must not become active HTML');
assert.ok(unsafe.textContent.includes('<img'));
const unknown=parse(String.raw`$\notARealCommand{2}$`);assert.ok(unknown.querySelector('.math-text'),'Unsupported TeX remains safe text rather than disappearing');
const enhance=d.createElement('div');enhance.textContent='Amount: '+example+'. Checked.';
format.enhance(enhance);const once=enhance.innerHTML;format.enhance(enhance);assert.equal(enhance.innerHTML,once);
assert.equal(enhance.querySelectorAll('.katex').length,1);
// The same formatter is used in every field of fresh answers and worked steps.
globalThis.ChemistrySolutionFormat=format;globalThis.ChemistryAnswerKey=require('./chemistry12-answer-key.js');
const worked=require('./chemistry12-worked-solution.js');
const entry={id:'test',answer:example,steps:[example,'Check '+example],check:example,assumptions:[example],needsReview:false};
const output=d.createElement('div');output.innerHTML=worked.render(entry);assert.equal(output.querySelectorAll('.katex').length,5);assert.equal(output.querySelectorAll('.math-text').length,0);
const key={id:'test'};globalThis.ChemistryAnswerKey.apply(key,entry);output.innerHTML=key.solution;assert.equal(output.querySelectorAll('.katex').length,5);
assert.ok(globalThis.ChemistryAnswerKey.prompt({id:'test'}).includes(format.instructions));
assert.ok(worked.prompt({id:'test'},'').includes(format.instructions));
assert.equal(format.cleanStep('1. 2\\. Apply the equation.'),'Apply the equation.');
const fs=require('node:fs'),path=require('node:path');
const prebuilt=JSON.parse(fs.readFileSync(path.resolve(__dirname,'../content/chemistry12/prebuilt-answers.json'),'utf8')).answers;
let prebuiltFields=0;
for(const [id,answer] of Object.entries(prebuilt))for(const field of [answer.answer,...answer.steps,answer.check,...answer.assumptions]){
 assert.ok(!format.text(field).includes('class="math-text"'),id+' has an unrendered expression');prebuiltFields++;
}
console.log(JSON.stringify({status:'PASS',additionalRegressionCases:regressions.length,prebuiltFields,checks:['Exact reported expression','Unit exponents and retained numbers','Inline and display delimiters','Extra and missing braces','Valid escaped braces and nested fractions','Raw TeX mixed with prose','Plain prose unchanged','Safe unsupported math and HTML','Idempotent DOM enhancement','All generated answer fields','Prompt formatting requirements']}));
dom.window.close();
