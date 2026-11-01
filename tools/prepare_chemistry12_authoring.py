#!/usr/bin/env python3
"""Prepare question-only image packets for sequential offline authoring.

Requires Pillow. Makes no network requests and never includes prebuilt solutions.
"""
import argparse,hashlib,json
from pathlib import Path
from chemistry12_prebuilt import ROOT,source_questions,fingerprint

def prepare(directory):
 from PIL import Image,ImageDraw
 directory=Path(directory);directory.mkdir(parents=True,exist_ok=True)
 packets=[]
 for q in source_questions(json.loads((ROOT/'content/chemistry12/practice-problems.json').read_text())):
  parts=list({p['src']:p for p in q['images']+q['context']+q['referenceTables']}.values())
  images=[]
  for part in parts:
   with Image.open(ROOT/part['src']) as source:
    im=source.convert('RGB');scale=min(1,1336/im.width)
    if scale<1:im=im.resize((round(im.width*scale),round(im.height*scale)))
    images.append(im)
  canvas=Image.new('RGB',(1400,160+sum(im.height+24 for im in images)),'white')
  ImageDraw.Draw(canvas).text((32,35),'ORIGINAL QUESTION AND REFERENCED FIGURES',fill='#183832');y=80
  for im in images:canvas.paste(im,(32,y));y+=im.height+24
  image_path=directory/(q['id']+'.jpg');canvas.save(image_path,quality=86)
  packets.append(dict(id=q['id'],title=f'Section {q["section"]}, review question {q["sourceNumber"]} · {q["topicTitle"]}',questionText=q['text'],sourceHash=fingerprint(q),image=str(image_path.resolve()),imageHash=hashlib.sha256(image_path.read_bytes()).hexdigest(),referenceImages=[p['src'] for p in parts]))
 (directory/'questions.json').write_text(json.dumps(packets,ensure_ascii=False,indent=2)+'\n')
 print(f'Prepared {len(packets)} separate question-only packets in {directory}')
if __name__=='__main__':
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('directory');prepare(p.parse_args().directory)
