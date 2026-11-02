(function(root){
 'use strict';
 const R=8.31446261815324;
 function evaluate(h,s,t,q=1){
  if(![h,s,t,q].every(Number.isFinite)||t<=0||q<=0)throw new RangeError('Use finite values, T > 0 and Q > 0.');
  const entropyTerm=-t*s/1000,g0=h+entropyTerm,correction=R*t*Math.log(q)/1000;
  return {h,s,t,q,entropyTerm,g0,correction,g:g0+correction,lnK:-g0*1000/(R*t),crossover:s!==0&&h*1000/s>0?h*1000/s:null};
 }
 function plot(h,s,t){
  const left=68,right=690,top=40,bottom=285;
  const lo=Math.min(200,t),hi=Math.max(1200,t),ts=Array.from({length:51},(_,i)=>lo+(hi-lo)*i/50);
  const all=ts.flatMap(v=>[h,-v*s/1000,h-v*s/1000]);
  let min=Math.min(0,...all),max=Math.max(0,...all),pad=Math.max((max-min)*.12,1);
  min-=pad;max+=pad;
  const x=v=>left+(v-lo)/(hi-lo)*(right-left),y=v=>bottom-(v-min)/(max-min)*(bottom-top),f=v=>v.toFixed(2);
  const curve=(values,color,dash)=>'<polyline fill="none" stroke="'+color+'" stroke-width="3"'+(dash?' stroke-dasharray="'+dash+'"':'')+' points="'+values.map((v,i)=>f(x(ts[i]))+','+f(y(v))).join(' ')+'"/>';
  let grid='';
  for(let i=0;i<=4;i++){
   const v=min+(max-min)*i/4,py=y(v),tv=lo+(hi-lo)*i/4;
   grid+='<line x1="68" x2="690" y1="'+f(py)+'" y2="'+f(py)+'" stroke="#e4e7df"/><text x="58" y="'+f(py+4)+'" text-anchor="end">'+v.toFixed(0)+'</text>';
   grid+='<text x="'+f(x(tv))+'" y="309" text-anchor="middle">'+tv.toFixed(0)+'</text>';
  }
  const g=h-t*s/1000;
  return '<svg viewBox="0 0 730 350" role="img" aria-labelledby="temperature-plot-title temperature-plot-desc" xmlns="http://www.w3.org/2000/svg"><title id="temperature-plot-title">Enthalpy and entropy contributions versus temperature</title><desc id="temperature-plot-desc">Constant enthalpy and entropy model, Q = 1. Solid green: standard reaction Gibbs energy. Dashed orange: enthalpy. Dotted blue: minus temperature times entropy. Marker at '+t.toFixed(2)+' K: standard Gibbs energy '+g.toFixed(3)+' kJ per mole of reaction.</desc><g font-family="system-ui,sans-serif" font-size="12" fill="#213e36">'+grid+'<text x="68" y="19">Energy / kJ mol⁻¹ of reaction</text><text x="379" y="339" text-anchor="middle">Temperature / K</text><line x1="68" x2="690" y1="'+f(y(0))+'" y2="'+f(y(0))+'" stroke="#89988b" stroke-width="1.5"/>'+curve(ts.map(()=>h),'#ad4b2e','9 5')+curve(ts.map(v=>-v*s/1000),'#325f9d','2 5')+curve(ts.map(v=>h-v*s/1000),'#235b47','')+'<line x1="'+f(x(t))+'" x2="'+f(x(t))+'" y1="40" y2="285" stroke="#6c766e" stroke-dasharray="3 5"/><circle cx="'+f(x(t))+'" cy="'+f(y(g))+'" r="6" fill="#235b47" stroke="white" stroke-width="2"/></g></svg>';
 }
 const api={R,evaluate,plot};
 if(typeof module==='object'&&module.exports)module.exports=api;else root.ThermodynamicsModel=api;
})(typeof globalThis==='object'?globalThis:this);
