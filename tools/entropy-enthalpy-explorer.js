(function(){
 'use strict';
 const $=id=>document.getElementById(id),form=$('explorer-form'),fields=['model-h','model-s','model-t','model-q'].map($),model=globalThis.ThermodynamicsModel;
 const presets={ammonia:[-92.22,-198.11,298.15,1],endothermic:[20,100,298.15,1],melting:[6.01,22,273.15,1],both:[-20,50,298.15,1],neither:[20,-50,298.15,1]};
 const fmt=v=>(Math.abs(v)<.0005?0:v).toLocaleString('en-US',{minimumFractionDigits:3,maximumFractionDigits:3});
 function update(){
  if(!form.checkValidity()){ $('explorer-error').textContent='Enter values within the labelled ranges. Temperature and Q must be positive.';return; }
  $('explorer-error').textContent='';
  const v=model.evaluate(...fields.map(el=>Number(el.value)));
  $('result-h').textContent=fmt(v.h);$('result-ts').textContent=fmt(v.entropyTerm);$('result-g0').textContent=fmt(v.g0);$('result-q').textContent=fmt(v.correction);$('result-g').textContent=fmt(v.g);
  const log10K=v.lnK/Math.LN10;
  $('result-k').textContent=Math.abs(log10K)<5?Math.exp(v.lnK).toPrecision(4):'10^('+log10K.toFixed(3)+')';
  const direction=Math.abs(v.g)<1e-8?'At equilibrium for this Q (within numerical precision).':v.g<0?'Forward reaction lowers G at this composition.':'Reverse reaction lowers G at this composition.';
  $('result-direction').textContent=direction;
  $('result-crossover').textContent=v.crossover?'Standard-state crossover: '+v.crossover.toFixed(2)+' K (constant ΔᵣH° and ΔᵣS° approximation). This gives K = 1; the mixture is at equilibrium only if Q = 1.':'No positive-temperature standard-state crossover in this model.';
  $('temperature-plot').innerHTML=model.plot(v.h,v.s,v.t);
 }
 form.addEventListener('submit',event=>event.preventDefault());
 form.addEventListener('input',update);
 $('model-preset').addEventListener('change',event=>{if(!presets[event.target.value])return;presets[event.target.value].forEach((v,i)=>{fields[i].value=v;});update();});
 $('model-reset').addEventListener('click',()=>{$('model-preset').value='ammonia';presets.ammonia.forEach((v,i)=>{fields[i].value=v;});update();});
 $('print-lesson').addEventListener('click',()=>window.print());
 let printState=[];
 window.addEventListener('beforeprint',()=>{printState=[...document.querySelectorAll('details')].map(el=>[el,el.open]);for(const [el] of printState)el.open=true;});
 window.addEventListener('afterprint',()=>{for(const [el,open] of printState)el.open=open;printState=[];});
 update();
})();
