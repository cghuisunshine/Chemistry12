#!/usr/bin/env python3
"""Reproducible numerical plots and labelled schematics for worked solutions.

Uses only the Python standard library and rsvg-convert. No network access.
"""
from pathlib import Path
import html,json,math,subprocess
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'assets/chemistry12-practice'
INK='#183832';BLUE='#176baf';ORANGE='#b85b14';PURPLE='#7045aa'

def text(x,y,s,size=22,color=INK,anchor='start'):
 return f'<text x="{x}" y="{y}" font-size="{size}" fill="{color}" text-anchor="{anchor}">{html.escape(s)}</text>'
def line(x,y,a,b,color=INK,width=3,arrow=False,dash=False):
 return f'<path d="M{x},{y} L{a},{b}" fill="none" stroke="{color}" stroke-width="{width}"'+(' marker-end="url(#arrow)"' if arrow else '')+(' stroke-dasharray="7 6"' if dash else '')+'/>'
def box(x,y,w,h,fill='none',stroke=INK):
 return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="10" fill="{fill}" stroke="{stroke}" stroke-width="2"/>'
def svg(body,title):
 return f'<svg xmlns="http://www.w3.org/2000/svg" width="1100" height="700" viewBox="0 0 1100 700"><title>{html.escape(title)}</title><defs><marker id="arrow" markerWidth="9" markerHeight="9" refX="8" refY="4" orient="auto-start-reverse"><path d="M0,0 L8,4 L0,8 Z" fill="context-stroke"/></marker></defs><rect width="1100" height="700" fill="#fff"/><g font-family="Arial, sans-serif">{body}</g></svg>'
def write(name,body,title):
 p=OUT/(name+'.svg');p.write_text(svg(body,title))
 subprocess.run(['rsvg-convert','-o',str(p.with_suffix('.png')),str(p)],check=True)
 return dict(src=str(p.with_suffix('.png').relative_to(ROOT)),width=550,alt=title)
def root_ph(balance):
 lo,hi=-14.,0.
 for _ in range(90):
  mid=(lo+hi)/2
  if balance(10**mid)>0:hi=mid
  else:lo=mid
 return -(lo+hi)/2

def graph(title,xmax,xlabel,xticks):
 b=text(55,44,title,29)+text(30,94,'pH',22)
 for ph in range(0,15,2):
  y=570-ph*32
  b+=line(100,y,1030,y,'#dae5e2',1)+text(78,y+7,str(ph),19,anchor='end')
 for x,label in xticks:
  px=100+930*x/xmax;b+=line(px,570,px,118,'#e7edeb',1)+text(px,600,label,19,anchor='middle')
 b+=line(100,570,1040,570)+line(100,570,100,110)+text(565,638,xlabel,22,anchor='middle')
 return b

def curve(func,xmax,color):
 points=[]
 for i in range(801):
  x=xmax*i/800;ph=func(x);points.append(f'{100+930*x/xmax:.2f},{570-32*ph:.2f}')
 return f'<polyline points="{" ".join(points)}" fill="none" stroke="{color}" stroke-width="3.5"/>'

def strong(v,nb):
 c=(.1*v/1000-nb)/(.025+v/1000)
 if c>=0:h=(c+math.sqrt(c*c+4e-14))/2
 else:h=1e-14/((-c+math.sqrt(c*c+4e-14))/2)
 return -math.log10(h)
def ammonia(v):
 vol=.025+v/1000;c=.0025/vol;cl=.1*v/1000/vol;ka=5.6e-10
 return root_ph(lambda h:h+c*h/(h+ka)-1e-14/h-cl)
def diprotic(r):
 v=.025*r;vol=.025+v;c=.0025/vol;na=.1*v/vol;k1=1e-4;k2=1e-8
 return root_ph(lambda h:h+na-1e-14/h-c*(k1*h+2*k1*k2)/(h*h+k1*h+k1*k2))

def beaker(x,label,solution):
 b=box(x,250,370,280,'#eff8fb')+line(x+2,340,x+368,340,BLUE,2)
 return b+text(x+185,570,label,24,anchor='middle')+text(x+185,608,solution,22,anchor='middle')

def dc_cell(spoon=False):
 title='Silver transfer onto an aluminium spoon' if spoon else 'Electrolysis of molten NaCl (type 1)'
 b=text(40,44,title,29)+box(425,70,250,75,'#edf5ee')+text(550,101,'DC source',24,anchor='middle')
 b+=text(450,132,'+',30,ORANGE)+text(634,132,'−',30,BLUE)
 b+=line(445,145,445,185)+line(445,185,260,185)+line(260,185,260,290)
 b+=line(655,145,655,185)+line(655,185,840,185)+line(840,185,840,290)
 b+=box(125,275,850,280,'#eff8fb')+line(128,350,972,350,BLUE,2)
 b+=text(260,242,'ANODE (+)',23,ORANGE,'middle')+text(840,242,'CATHODE (−)',23,BLUE,'middle')
 b+=box(245,290,30,200,'#d3d7dc')
 if spoon:
  b+=box(830,290,18,110,'#c4cbd4')+'<ellipse cx="839" cy="444" rx="42" ry="59" fill="#d8e1ed" stroke="#176baf" stroke-width="5"/>'
  b+=text(170,327,'Ag strip',20)+text(880,327,'Al spoon',20)
  b+=text(550,398,'Electrolyte containing Ag⁺',24,anchor='middle')+text(550,435,'(idealized AgNO₃ solution)',20,anchor='middle')
  b+=line(530,480,760,480,BLUE,3,True)+text(620,465,'Ag⁺ →',21,BLUE,anchor='middle')
  b+=line(550,520,335,520,ORANGE,3,True)+text(450,508,'← NO₃⁻',21,ORANGE,anchor='middle')
  b+=text(260,593,'Ag → Ag⁺ + e⁻',25,ORANGE,'middle')+text(820,593,'Ag⁺ + e⁻ → Ag',25,BLUE,'middle')
  b+=text(550,635,'Ag anode loses mass; Ag coating on spoon grows.',23,anchor='middle')+text(550,675,'E° = 0 V for Ag transfer; applied voltage must cover real losses.',20,anchor='middle')
 else:
  b+=box(825,290,30,200,'#d3d7dc')+text(550,393,'Molten NaCl: no water',26,anchor='middle')
  b+=line(530,448,330,448,ORANGE,3,True)+text(420,428,'Cl⁻',24,ORANGE,anchor='middle')
  b+=line(570,505,770,505,BLUE,3,True)+text(660,483,'Na⁺',24,BLUE,anchor='middle')
  b+=text(260,593,'2Cl⁻ → Cl₂ + 2e⁻',25,ORANGE,'middle')+text(820,593,'Na⁺ + e⁻ → Na',25,BLUE,'middle')
  b+=text(550,635,'Collect Cl₂ and Na separately; ionic current flows in the melt.',23,anchor='middle')+text(550,675,'Table-based estimate: 4.07 V; not an exact high-temperature melt value.',20,anchor='middle')
 return b,title

def build():
 diagrams={}
 title='Section 5.4 Q14: comparison of titration curves'
 b=graph(title,60,'Added 0.10 M HCl (mL)',[(i,str(i)) for i in range(0,61,10)])
 b+=curve(lambda v:strong(v,.0025),60,'#7b8783')+curve(lambda v:strong(v,.0050),60,BLUE)+curve(ammonia,60,ORANGE)
 b+=text(440,90,'0.10 M NaOH (reference)',19,'#63706a')+text(440,117,'0.20 M NaOH',19,BLUE)+text(740,117,'0.10 M NH₃',19,ORANGE)
 b+=text(575,385,'NH₃ eq. ≈ (25 mL, 5.28)',19,ORANGE)+line(565,390,487.5,401,ORANGE,1.5)
 b+=text(645,300,'NaOH eq. = (50 mL, 7)',19,BLUE)+line(865,309,875,346,BLUE,1.5)
 b+='<circle cx="487.5" cy="401" r="5" fill="#b85b14"/><circle cx="875" cy="346" r="5" fill="#176baf"/>'
 b+=text(550,678,'Same 25 mL sample volume; calculated ideal curves at 25 °C.',20,anchor='middle')
 diagrams['chem12-s5-4-q14']=write('s5-4-q14-solution',b,title)
 title='Section 5.4 Q15: a diprotic-acid titration example'
 b=graph(title,2.5,'Added strong base / first equivalence volume (V / V₁)',[(i/2,str(i/2)) for i in range(6)])+curve(diprotic,2.5,PURPLE)
 for r,label in [(1,'First equivalence'),(2,'Second equivalence')]:
  x=100+930*r/2.5;b+=line(x,570,x,155,PURPLE,1,False,True)+text(x+12,185 if r==1 else 150,label,18,PURPLE)
 b+=text(235,490,'H₂A / HA⁻ buffer',18,PURPLE)+text(555,355,'HA⁻ / A²⁻ buffer',18,PURPLE)
 b+=text(550,678,'Illustration only: pKa₁ = 4, pKa₂ = 8. Source supplies no numerical constants.',20,anchor='middle')
 diagrams['chem12-s5-4-q15']=write('s5-4-q15-solution',b,title)
 title='Section 6.4 Q3: bromine half-cell'
 b=text(45,46,title,29)+beaker(365,'Bromine / bromide half-cell','1.0 M Br⁻ (standard schematic)')
 b+=box(485,190,24,300,'#c5cbd0')+line(497,190,497,100)+line(497,100,855,100,INK,3,True)
 b+=text(600,88,'Wire to other half-cell',22)+text(60,218,'Inert Pt conductor',24)+line(285,215,480,270,INK,2,True)
 b+=box(368,478,363,49,'#e4ad79')+text(390,511,'Br₂(l), contacting Br⁻ solution',20)
 b+=text(60,385,'Br₂ + 2e⁻ ⇌ 2Br⁻',26,BLUE)+text(60,430,'E°red = +1.09 V',24,BLUE)
 b+=text(550,666,'Pt conducts electrons; it is not consumed. Electrode role depends on the partner.',21,anchor='middle')
 diagrams['chem12-s6-4-q3']=write('s6-4-q3-solution',b,title)
 title='Section 6.4 Q6: formal zinc / fluorine cell'
 b=text(40,43,title,29)+beaker(70,'Zn anode (−)','1.0 M ZnCl₂')+beaker(660,'Pt / F₂ cathode (+)','1.0 M NaF')
 b+=box(145,220,30,260,'#c6cbd0')+box(810,220,24,260,'#c6cbd0')
 b+=line(160,220,160,130)+line(160,130,822,130,INK,3,True)+line(822,130,822,220)
 b+=text(490,112,'e⁻ through wire: Zn → Pt / F₂',23,anchor='middle')
 b+='<path d="M390,390 L390,205 Q550,150 710,205 L710,390" fill="none" stroke="#b6cabe" stroke-width="20"/>'
 b+=text(550,205,'Salt bridge',20,anchor='middle')+line(530,242,430,242,ORANGE,2,True)+line(570,242,675,242,BLUE,2,True)
 b+=text(400,275,'anions → Zn',18,ORANGE)+text(570,275,'cations → F₂',18,BLUE)
 b+=text(885,313,'F₂(g) inlet',19)+line(895,320,855,415,INK,2,True)
 for x,y in [(850,440),(865,400),(845,370)]:b+=f'<circle cx="{x}" cy="{y}" r="7" fill="none" stroke="#176baf" stroke-width="2"/>'
 b+=text(255,495,'Zn → Zn²⁺ + 2e⁻',20,ORANGE,'middle')+text(850,495,'F₂ + 2e⁻ → 2F⁻',20,BLUE,'middle')
 b+=text(550,653,'E° = 3.63 V. Formal model only: F₂ reacts with water.',22,anchor='middle')
 diagrams['chem12-s6-4-q6']=write('s6-4-q6-solution',b,title)
 for key,spoon in [('chem12-s6-5-q2',False),('chem12-s6-5-q10',True)]:
  b,title=dc_cell(spoon);diagrams[key]=write(key.replace('chem12-','')+'-solution',b,title)
 p=ROOT/'content/chemistry12/prebuilt-answers.json';data=json.loads(p.read_text())
 for key,diagram in diagrams.items():
  diagram['caption']={'chem12-s5-4-q14':'Calculated curves use the approximately 25 mL sample inferred from the source graph.', 'chem12-s5-4-q15':'Illustrative separated dissociations; two visible jumps are not guaranteed for every diprotic acid.'}.get(key,'Labelled schematic for the worked solution; consult the assumptions above.')
  data['answers'][key]['solutionImages']=[diagram]
 p.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
 print('Built six source-specific solution diagrams.')
if __name__=='__main__':build()
