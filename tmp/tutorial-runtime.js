
const quizData = {"kinetics": [{"answer": 0, "explanation": "One mole of B forms for every two moles of A consumed, so its formation rate is half the A disappearance rate."}, {"answer": 1, "explanation": "A catalyst provides a faster pathway and is regenerated. It leaves the reaction endpoints and equilibrium constant unchanged."}, {"answer": 2, "explanation": "The rate ratio is 4 = 2ᵐ, so m = 2."}], "equilibrium": [{"answer": 1, "explanation": "Equal opposing rates give no net composition change; concentrations need not be equal."}, {"answer": 0, "explanation": "Forward conversion raises the product-to-reactant quotient until Q reaches K."}, {"answer": 2, "explanation": "Temperature changes K. Concentration changes alter Q, while a catalyst changes the rate of approach."}], "solubility": [{"answer": 1, "explanation": "The ions have concentrations s and 2s, so their product is s(2s)² = 4s³."}, {"answer": 0, "explanation": "Precipitation lowers the ion product toward Ksp."}, {"answer": 2, "explanation": "Its amount now occupies twice its original volume."}], "acid-base-1": [{"answer": 0, "explanation": "Removing exactly one H⁺ produces HCO₃⁻."}, {"answer": 1, "explanation": "Multiplying the two equilibrium expressions cancels the acid and conjugate-base factors, leaving Kw."}, {"answer": 2, "explanation": "The estimate replaces C − x by C and neglects water’s contribution; check both assumptions."}], "acid-base-2": [{"answer": 2, "explanation": "The conjugate base formed by neutralization hydrolyzes to produce OH⁻."}, {"answer": 0, "explanation": "The concentration ratio is one, so the logarithmic term is zero."}, {"answer": 1, "explanation": "Half the acid remains and half has become its conjugate base."}], "electrochemistry": [{"answer": 1, "explanation": "Oxidation defines the anode in both galvanic and electrolytic cells; its sign depends on cell type."}, {"answer": 0, "explanation": "Potential is energy per charge and does not scale with the amount of reaction."}, {"answer": 2, "explanation": "Divide the moles of electrons by the coefficient two."}]};


const $ = id => document.getElementById(id);
const lessons = [...document.querySelectorAll('.lesson')];
const chapters = [...document.querySelectorAll('.chapter')];
const allDetails = [...document.querySelectorAll('details')];
const toast = message => { $('toast').textContent=message; $('toast').hidden=false; clearTimeout(window.toastTimer); window.toastTimer=setTimeout(()=>$('toast').hidden=true,2600); };
function closeMenu(){document.body.classList.remove('sidebar-open');$('menuBtn').setAttribute('aria-expanded','false');}
$('menuBtn').addEventListener('click',()=>{const open=document.body.classList.toggle('sidebar-open');$('menuBtn').setAttribute('aria-expanded',String(open));});
$('backdrop').addEventListener('click',closeMenu);
document.addEventListener('keydown',e=>{if(e.key==='Escape'){closeMenu();$('menuBtn').focus();}});
document.querySelectorAll('[data-chapter-expand]').forEach(b=>b.addEventListener('click',()=>b.closest('.chapter').querySelectorAll('.lesson:not([hidden])').forEach(d=>d.open=b.dataset.chapterExpand==='true')));
let searchState=null;
function applySearch(){
 const q=$('search').value.toLocaleLowerCase().trim();
 if(q&&searchState===null)searchState=new Map(lessons.map(d=>[d,d.open]));
 let hits=0;
 lessons.forEach(d=>{const match=!q||d.textContent.toLocaleLowerCase().includes(q);d.hidden=!match;d.classList.toggle('search-hit',!!q&&match);if(q&&match){hits++;d.open=true;}});
 chapters.forEach(c=>{c.hidden=!c.querySelector('.lesson:not([hidden])');c.querySelector('.quiz').hidden=!!q;});
 $('overview').hidden=!!q;
 $('appendix').hidden=!!q&&!$('appendix').textContent.toLocaleLowerCase().includes(q);
 $('emptySearch').hidden=!q||hits>0||!$('appendix').hidden;
 $('searchStatus').textContent=q?`${hits} matching textbook section${hits===1?'':'s'}.`:'';
 if(!q&&searchState){searchState.forEach((open,d)=>d.open=open);searchState=null;}
}
$('search').addEventListener('input',applySearch);
function revealTarget(hash=location.hash){
 let id;try{id=decodeURIComponent(hash.slice(1));}catch{return null;}
 const target=$(id);if(!target)return null;
 if(target.closest('[hidden]')){$('search').value='';applySearch();}
 let p=target;while(p){if(p.tagName==='DETAILS')p.open=true;p=p.parentElement;}
 const nav=document.querySelector(`.nav-sections a[href="#${CSS.escape(id)}"]`);if(nav)nav.closest('details').open=true;
 return target;
}
document.querySelectorAll('a[href^="#"]').forEach(a=>a.addEventListener('click',()=>{revealTarget(a.hash);closeMenu();requestAnimationFrame(()=>$(a.hash.slice(1))?.scrollIntoView({block:'start'}));}));
window.addEventListener('hashchange',()=>revealTarget());
let printState=[];
window.addEventListener('beforeprint',()=>{printState=allDetails.map(d=>d.open);lessons.forEach(d=>d.open=true);});
window.addEventListener('afterprint',()=>allDetails.forEach((d,i)=>d.open=printState[i]??d.open));
$('printBtn').addEventListener('click',()=>window.print());
let saved=[];try{const v=JSON.parse(localStorage.getItem('chem12-reviewed-v1')||'[]');if(Array.isArray(v))saved=v;}catch{}
const complete=[...document.querySelectorAll('.complete')];
function updateProgress(){const checked=complete.filter(c=>c.checked);$('progressText').textContent=`${checked.length} of 6 chapters reviewed`;$('courseProgress').value=checked.length;try{localStorage.setItem('chem12-reviewed-v1',JSON.stringify(checked.map(c=>c.dataset.unit)));}catch{$('storageNote').textContent='Progress is available for this session only.';}}
complete.forEach(c=>{c.checked=saved.includes(c.dataset.unit);c.addEventListener('change',updateProgress);});updateProgress();
$('resetProgress').addEventListener('click',()=>{complete.forEach(c=>c.checked=false);updateProgress();toast('Review progress reset');});
document.querySelectorAll('.quiz').forEach(form=>form.addEventListener('submit',e=>{
 e.preventDefault();let score=0,answered=0;const id=form.dataset.unit;
 quizData[id].forEach((q,i)=>{const chosen=form.querySelector(`input[name="${id}-q${i}"]:checked`);const fb=$(`${id}-feedback${i}`);fb.hidden=false;
 if(!chosen){fb.textContent='Choose an answer, then check again.';fb.className='feedback bad';return;}
 answered++;const ok=Number(chosen.value)===q.answer;if(ok)score++;fb.textContent=(ok?'Correct. ':'Try again. ')+q.explanation;fb.className='feedback '+(ok?'good':'bad');});
 form.querySelector('.quiz-score').textContent=answered<3?`${score}/3 correct · ${3-answered} unanswered`:`${score}/3 correct${score===3?' · Well done.':''}`;
}));
async function copyEquation(el){try{await navigator.clipboard.writeText(el.innerText.trim());toast('Formula copied');}catch{const range=document.createRange();range.selectNodeContents(el);const selection=window.getSelection();selection.removeAllRanges();selection.addRange(range);toast('Formula selected — use Copy');}}
document.querySelectorAll('[data-copy]').forEach(el=>{el.addEventListener('dblclick',()=>copyEquation(el));el.addEventListener('keydown',e=>{if(e.key==='Enter'){e.preventDefault();copyEquation(el);}});});

function science(n){return n===0?'0':n.toExponential(2).replace('e+',' × 10^').replace('e-',' × 10^−');}
function rate(){const T=Number($('temperature').value),cat=$('catalyst').checked,Ea=cat?40000:50000;const ratio=Math.exp(50000/(8.314*298)-Ea/(8.314*T));$('tempValue').value=T;$('rateResult').textContent=`Relative rate constant: ${ratio.toFixed(2)}× · Eₐ = ${Ea/1000} kJ mol⁻¹${cat?' · catalyst on':''}`;}
['temperature','catalyst'].forEach(id=>$(id).addEventListener('input',rate));rate();
function equilibrium(){const a=Number($('eqH2').value),b=Number($('eqI2').value),c=Number($('eqHI').value);if(![$('eqH2'),$('eqI2'),$('eqHI')].every(x=>x.value!==''&&x.validity.valid)||a<=0||b<=0||c<0){$('eqResult').textContent='Enter H₂ and I₂ concentrations from 0.001 to 10 M and HI from 0 to 10 M.';return;}const Q=c*c/(a*b);let result=Math.abs(Q-4)<1e-8?'At equilibrium: forward and reverse rates balance.':Q<4?'Net reaction → products (HI forms).':'Net reaction ← reactants (H₂ and I₂ form).';$('eqResult').textContent=`Q = ${Q.toPrecision(3)} · K = 4.00 · ${result}`;}
['eqH2','eqI2','eqHI'].forEach(id=>$(id).addEventListener('input',equilibrium));equilibrium();
function solubility(){const a=Number($('silver').value),b=Number($('chloride').value);if(![$('silver'),$('chloride')].every(x=>x.value!==''&&x.validity.valid)){ $('solResult').textContent='Enter both concentrations between 0 and 1 M.';return;}const Q=a*b/4,K=1.8e-10;const eq=Math.abs(Q-K)<=K*1e-8;const state=eq?'Saturated: at the precipitation threshold.':Q>K?'Precipitation is favoured: AgCl(s) forms.':'Unsaturated: no precipitation predicted.';$('solResult').textContent=`Qsp = ${science(Q)} · Ksp = 1.8 × 10^−10 · ${state}`;}
['silver','chloride'].forEach(id=>$(id).addEventListener('input',solubility));solubility();
function ph(){const p=Number($('phSlider').value);$('phValue').value=p.toFixed(2);$('phMarker').style.left=`${p/14*100}%`;$('phResult').textContent=`[H₃O⁺] ≈ ${science(10**-p)} M · [OH⁻] ≈ ${science(10**-(14-p))} M · ${p<7?'Acidic':p>7?'Basic':'Neutral'} at 25 °C`;}
$('phSlider').addEventListener('input',ph);ph();
function buffer(){const log=Number($('bufferRatio').value),ratio=10**log;$('bufferValue').value=ratio.toFixed(2);$('bufferResult').textContent=`pH ≈ 4.76 + log₁₀(${ratio.toFixed(2)}) = ${(4.76+log).toFixed(2)} · ${log===0?'Equal amounts of conjugate base and acid.':log>0?'More conjugate base than acid.':'More acid than conjugate base.'}`;}
$('bufferRatio').addEventListener('input',buffer);buffer();


if('IntersectionObserver' in window){const observer=new IntersectionObserver(entries=>{const visible=entries.filter(e=>e.isIntersecting);if(!visible.length)return;const id=visible[0].target.id;document.querySelectorAll('nav a').forEach(a=>a.classList.toggle('active',a.hash==='#'+id));},{rootMargin:'-90px 0px -55% 0px',threshold:0});lessons.forEach(s=>observer.observe(s));}
revealTarget();
if(location.hash)requestAnimationFrame(()=>$(location.hash.slice(1))?.scrollIntoView({behavior:'instant',block:'start'}));
