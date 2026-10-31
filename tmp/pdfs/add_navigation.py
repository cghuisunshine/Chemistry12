from pathlib import Path
import json
import pymupdf as fitz
from pypdf import PdfReader

source=Path('Chemistry12.pdf')
output=Path('output/pdf/Chemistry12-navigable.pdf')
doc=fitz.open(source)
# Printed textbook page 1 is physical PDF page 11. All destinations are 0-based.
def page(n): return n+9
chapters=[
 ('1 Reaction Kinetics',1,[
  ('1.1 Measuring the Rate of Chemical Reactions',2),
  ('1.2 Factors Affecting Rates of Reaction',15),
  ('1.3 Collision Theory',24),
  ('1.4 Potential Energy Diagrams',36),
  ('1.5 Reaction Mechanisms, Catalysis, and Rate Laws',50)]),
 ('2 Chemical Equilibrium',63,[
  ('2.1 Introduction to Dynamic Equilibrium',64),
  ('2.2 Le Chatelier’s Principle',74),
  ('2.3 How Equilibria Respond to Volume and Temperature Changes',86),
  ('2.4 Entropy Change versus Enthalpy Change',104),
  ('2.5 The Equilibrium Constant',115),
  ('2.6 Equilibrium Problems',129)]),
 ('3 Solubility Equilibrium',143,[
  ('3.1 The Concept of Solubility',144),
  ('3.2 Qualitative Analysis — Identifying Unknown Ions',154),
  ('3.3 The Solubility Product Constant Ksp',167),
  ('3.4 Precipitation Formation and the Solubility Product Ksp',177)]),
 ('4 Acid-Base Equilibrium',189,[
  ('4.1 Identifying Acids and Bases',190),
  ('4.2 The Strengths of Acids and Bases',199),
  ('4.3 The Ionization of Water',212),
  ('4.4 pH and pOH',219),
  ('4.5 Calculations Involving Ka and Kb',234)]),
 ('5 Applications of Acid-Base Reactions',255,[
  ('5.1 Hydrolysis of Salts — The Reactions of Ions with Water',256),
  ('5.2 The Chemistry of Buffers',272),
  ('5.3 Acid-Base Titrations — Analyzing with Volume',290),
  ('5.4 A Closer Look at Titrations',307),
  ('5.5 Non-metal and Metal Oxides in Water',337)]),
 ('6 Oxidation-Reduction and Its Applications',351,[
  ('6.1 Oxidation-Reduction',352),
  ('6.2 Balancing Oxidation-Reduction Equations',363),
  ('6.3 Using the Standard Reduction Potential (SRP) Table to Predict Redox Reactions',379),
  ('6.4 The Electrochemical Cell',392),
  ('6.5 The Electrolytic Cell',408)])]
appendix=[
 ('Table A1 Atomic Masses of the Elements',422),
 ('Table A2 Names, Formulas, and Charges of Some Common Ions',423),
 ('Table A3 Solubility of Common Compounds in Water',424),
 ('Table A4 Solubility Product Constants at 25°C',425),
 ('Table A5 Relative Strengths of Brønsted-Lowry Acids and Bases',426),
 ('Table A6 Acid-Base Indicators',427),
 ('Table A7 Standard Reduction Potentials of Half-Cells',428)]
toc=[[1,'Table of Contents',7],
     [1,'Welcome and Land Acknowledgement',5],
     [1,'Welcome to BC Science Chemistry 12',8]]
rows=[('Welcome to BC Science Chemistry 12',7)]
for title,n,sections in chapters:
 toc.append([1,title,page(n)+1])
 rows.append((title,page(n)))
 for title,n in sections:
  toc.append([2,title,page(n)+1])
  rows.append((title,page(n)))
toc.append([1,'Appendix — Reference Tables',431])
rows.append(('Appendix — Reference Tables',430))
toc.extend([2,title,page(n)+1] for title,n in appendix)
toc.extend([[1,'Glossary',439],[1,'Answer Key',444],[1,'Periodic Table of Elements',448]])
# Explicit internal GoTo destinations work without JavaScript or network access.
doc.set_toc(toc,collapse=1)
doc.xref_set_key(doc.pdf_catalog(),'PageMode','/UseOutlines')
doc.xref_set_key(doc.pdf_catalog(),'OpenAction',f'[{doc.page_xref(6)} 0 R /Fit]')
doc.set_page_labels([
 {'startpage':0,'prefix':'Cover','firstpagenum':1},
 {'startpage':1,'prefix':'Digitization','firstpagenum':1},
 {'startpage':2,'style':'r','firstpagenum':1},
 {'startpage':10,'style':'D','firstpagenum':1}])

# Visually verified row centres of the scanned contents (PDF coordinates, points).
centres=[97,126,139,151.5,164,176.5,189,
 215,228,240.5,253,265.5,278,290.5,
 316.5,329,341.5,354,366.5,
 393,405.5,418,430.5,443,455.5,
 482,494.5,507,519.5,532,544.5,
 572,584.5,597,609.5,622,634.5,662]
assert len(rows)==len(centres)==38
links=[]
for i,((title,dest),y) in enumerate(zip(rows,centres)):
 low=max(y-8.5, (centres[i-1]+y)/2 if i else y-8.5)
 high=min(y+8.5, (y+centres[i+1])/2 if i+1<len(centres) else y+8.5)
 rect=fitz.Rect(27,low,518,high)
 doc[6].insert_link({'kind':fitz.LINK_GOTO,'from':rect,'page':dest,'to':fitz.Point(0,0),'zoom':0})
 links.append({'source':7,'title':title,'destination':dest+1,'rect':list(rect)})
for i,(title,n) in enumerate(appendix):
 y=89.5+i*25.3
 rect=fitz.Rect(16,y-11,400,y+11)
 doc[430].insert_link({'kind':fitz.LINK_GOTO,'from':rect,'page':page(n),'to':fitz.Point(0,0),'zoom':0})
 links.append({'source':431,'title':title,'destination':page(n)+1,'rect':list(rect)})
doc.save(output,garbage=3,deflate=True)
doc.close()

# Validate independently through both MuPDF and pypdf after reopening.
final=fitz.open(output)
original=fitz.open(source)
assert len(final)==len(original)==448
assert final.get_toc()==toc
assert final[10].get_label()=='1'
assert final[6].get_label()=='v'
assert final[430].get_label()=='421'
assert len(final[6].get_links())==38
assert len(final[430].get_links())==7
for sourcepage in [6,430]:
 expected=[x for x in links if x['source']==sourcepage+1]
 actual=final[sourcepage].get_links()
 for a,e in zip(actual,expected):
  assert a['kind']==fitz.LINK_GOTO
  assert a['page']==e['destination']-1,(a,e)
  assert final[a['page']].get_text().strip(),e
 for i,a in enumerate(actual):
  for b in actual[i+1:]: assert not (a['from'] & b['from']).get_area()
reader=PdfReader(output)
refs={p.indirect_reference.idnum:i+1 for i,p in enumerate(reader.pages)}
count=0
for i,p in enumerate(reader.pages):
 for ref in p.get('/Annots',[]):
  a=ref.get_object()
  if a.get('/Subtype')!='/Link': continue
  action=a.get('/A')
  assert action and action['/S']=='/GoTo'
  dest=action['/D']
  assert isinstance(dest,list) and refs[dest[0].idnum] in range(1,449)
  count+=1
assert count==45
assert reader.trailer['/Root']['/OpenAction'][0].idnum==reader.pages[6].indirect_reference.idnum
# Compare every page's drawing instructions and embedded image data exactly.
# This avoids repeatedly decoding hundreds of high-resolution scanned pages.
import hashlib
checked_images=set()
for i in range(len(final)):
 assert original[i].rect==final[i].rect
 assert original[i].read_contents()==final[i].read_contents(),i+1
 a,b=original[i].get_images(full=True),final[i].get_images(full=True)
 assert len(a)==len(b),i+1
 for old,new in zip(a,b):
  assert old[2:]==new[2:],i+1
  for ox,nx in zip(old[:2],new[:2]):
   if ox and (ox,nx) not in checked_images:
    assert hashlib.sha256(original.xref_stream_raw(ox)).digest()==hashlib.sha256(final.xref_stream_raw(nx)).digest(),i+1
    checked_images.add((ox,nx))
for i in [6,430,10,388,447]:
 a=original[i].get_pixmap(matrix=fitz.Matrix(.4,.4),annots=False)
 b=final[i].get_pixmap(matrix=fitz.Matrix(.4,.4),annots=False)
 assert (a.width,a.height,a.samples)==(b.width,b.height,b.samples),f'Appearance changed on page {i+1}'
for i in [6,430,10,388,447]:
 final[i].get_pixmap(matrix=fitz.Matrix(1.3,1.3)).save(f'tmp/pdfs/verified-page-{i+1}.png')
# QA overlay, never included in the delivered PDF.
qa=fitz.open(output)
for i in [6,430]:
 for link in qa[i].get_links():
  qa[i].draw_rect(link['from'],color=(0,0.4,1),width=.6,fill=(0,.5,1),fill_opacity=.12)
 qa[i].get_pixmap(matrix=fitz.Matrix(1.6,1.6)).save(f'tmp/pdfs/link-targets-page-{i+1}.png')
Path('tmp/pdfs/navigation-validation.json').write_text(json.dumps({'output':str(output),'pages':len(final),'bookmarks':len(toc),'internal_links':count,'all_pages_visually_unchanged':True,'links':links},indent=2))
print(json.dumps({'output':str(output),'pages':len(final),'bookmarks':len(toc),'internal_links':count,'all_pages_visually_unchanged':True},indent=2))
