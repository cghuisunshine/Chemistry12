/* Local-file PNGs need data URLs before drawing them onto an exportable canvas.
   Companion scripts carry only image bytes and load on demand, without fetching
   file:// URLs or requiring a server. Ordinary HTTP images keep their usual path. */
(function(root){
'use strict';
const pending=new Map(),cache=new Map(),limit=16;
const localSource=/^assets\/chemistry12-practice\/[a-z0-9-]+\.png$/;
const canceled=()=>new DOMException('Image preparation canceled.','AbortError');
function remember(src,data){
  cache.delete(src);cache.set(src,data);
  while(cache.size>limit)cache.delete(cache.keys().next().value);
}
function register(src,data){
  const request=pending.get(src);
  if(request&&typeof data==='string'&&/^data:image\/png;base64,[A-Za-z0-9+/=]+$/.test(data))request.data=data;
}
function load(src){
  if(root.location.protocol!=='file:'||src.startsWith('data:')||src.startsWith('blob:'))return Promise.resolve(src);
  if(!localSource.test(src))return Promise.reject(Error('This local image is not in the textbook image collection.'));
  if(cache.has(src)){const data=cache.get(src);remember(src,data);return Promise.resolve(data);}
  if(pending.has(src))return pending.get(src).promise;
  const script=document.createElement('script'),request={data:null};
  request.promise=new Promise((resolve,reject)=>{
    const cleanup=()=>{clearTimeout(request.timer);script.onload=null;script.onerror=null;script.remove();pending.delete(src);};
    const fail=()=>{cleanup();reject(Error('Could not load the textbook image for AI review. Keep the image companion files in assets/chemistry12-practice/ and try again.'));};
    script.onload=()=>{const data=request.data;if(!data){fail();return;}remember(src,data);cleanup();resolve(data);};
    script.onerror=fail;
    request.timer=setTimeout(fail,15000);
  });
  pending.set(src,request);
  script.src=new URL(src+'.js',document.baseURI).href;
  document.head.append(script);
  return request.promise;
}
async function decode(src,signal){
  if(signal?.aborted)throw canceled();
  const data=await new Promise((resolve,reject)=>{
    const abort=()=>{signal?.removeEventListener('abort',abort);reject(canceled());};
    signal?.addEventListener('abort',abort,{once:true});
    load(src).then(value=>{signal?.removeEventListener('abort',abort);resolve(value);},error=>{signal?.removeEventListener('abort',abort);reject(error);});
  });
  if(signal?.aborted)throw canceled();
  return new Promise((resolve,reject)=>{
    const img=new Image();
    const cleanup=()=>{img.onload=null;img.onerror=null;signal?.removeEventListener('abort',abort);};
    const abort=()=>{cleanup();img.src='';reject(canceled());};
    signal?.addEventListener('abort',abort,{once:true});
    img.onload=()=>{cleanup();resolve(img);};
    img.onerror=()=>{cleanup();reject(Error('Could not prepare the question images for AI.'));};
    img.src=data;
  });
}
root.ChemistryImageAssets={register,decode};
})(window);
