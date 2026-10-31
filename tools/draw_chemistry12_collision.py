#!/usr/bin/env python3
"""Exact, labelled vector redraws for section 1.3 review question 7.

Run with PyMuPDF installed to regenerate the SVG and high-resolution PNG assets.
These are connectivity sketches, not Lewis structures or scale models.
"""
from pathlib import Path
import math
import pymupdf as pdf

ROOT=Path(__file__).resolve().parents[1]
ASSETS=ROOT/'assets/chemistry12-practice'
INK='#183832'
def atom(x,y,element):
    fill,stroke={'Cl':('#e0edb5','#486b27'),'N':('#dbe9fa','#315c88'),'O':('#fbe0d4','#9a4c34')}[element]
    return f'<circle cx="{x}" cy="{y}" r="30" fill="{fill}" stroke="{stroke}" stroke-width="2.5"/><text x="{x}" y="{y+8}" text-anchor="middle" font-size="24" font-weight="700">{element}</text>'
def bond(x1,y1,x2,y2):
    return f'<path d="M{x1} {y1}L{x2} {y2}" fill="none" stroke="{INK}" stroke-width="5"/>'
def arrow(x1,y1,x2,y2):
    length=math.hypot(x2-x1,y2-y1)
    ux,uy=(x2-x1)/length,(y2-y1)/length
    bx,by=x2-18*ux,y2-18*uy
    return (f'<path d="M{x1} {y1}L{bx} {by}" stroke="{INK}" stroke-width="4" fill="none"/>'
            f'<polygon points="{x2},{y2} {bx-10*uy},{by+10*ux} {bx+10*uy},{by-10*ux}" fill="{INK}"/>')
def text(x,y,s,size=21,**attrs):
    properties=' '.join(f'{k.replace("_","-")}="{v}"' for k,v in attrs.items())
    return f'<text x="{x}" y="{y}" font-size="{size}" {properties}>{s}</text>'
def molecule(nx,ny,cx,cy,ox1,oy1,ox2,oy2):
    return ''.join([bond(nx,ny,cx,cy),bond(nx,ny,ox1,oy1),bond(nx,ny,ox2,oy2),atom(nx,ny,'N'),atom(cx,cy,'Cl'),atom(ox1,oy1,'O'),atom(ox2,oy2,'O')])
def frame(height,title,description):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="1000" height="{height}" viewBox="0 0 1000 {height}" role="img" aria-labelledby="title desc">
<title id="title">{title}</title><desc id="desc">{description}</desc>
<defs><marker id="arrow" markerWidth="10" markerHeight="10" refX="8" refY="4" orient="auto" markerUnits="strokeWidth"><path d="M0 0L8 4L0 8Z" fill="{INK}"/></marker></defs>
<rect width="1000" height="{height}" rx="16" fill="#ffffff"/>
<g font-family="sans-serif" fill="{INK}">'''
def save(name,svg):
    svg+='</g></svg>'
    (ASSETS/(name+'.svg')).write_text(svg)
    doc=pdf.open(stream=svg.encode(),filetype='svg')
    doc[0].get_pixmap(matrix=pdf.Matrix(2,2),alpha=False).save(ASSETS/(name+'.png'))
    doc.close()

def main():
    question=frame(455,'ClNO₂ and a chlorine atom: the given collision','ClNO₂ is on the left with its chlorine pointing upper left. A separate Cl atom approaches from the right toward the oxygen side. Arrows show the particles moving toward each other.')
    question+=text(36,43,'7  Collision theory: ClNO₂ + Cl',26,font_weight='700')
    question+=text(36,79,'With sufficient collision energy, is the orientation below likely to form Cl₂ and NO₂?',20)
    question+=text(36,109,'If not, redraw the particles so that a successful collision would be likely.',20)
    question+=molecule(260,245,170,185,335,185,285,325)
    question+=atom(785,245,'Cl')+arrow(400,245,520,245)+arrow(680,245,560,245)
    question+=text(240,382,'ClNO₂',23,text_anchor='middle',font_weight='700')
    question+=text(785,382,'Cl atom',23,text_anchor='middle',font_weight='700')
    question+=text(36,426,'Redrawn from the original orientation. Connectivity sketch; not a Lewis structure or to scale.',16,fill='#60736b')
    save('s1-3-q7-redrawn',question)

    solution=frame(670,'Productive Cl–Cl approach and products','In the corrected orientation the chlorine attached to nitrogen faces the incoming chlorine atom. A new chlorine–chlorine bond forms while the nitrogen–chlorine bond breaks, leaving nitrogen dioxide and chlorine gas.')
    solution+=text(36,44,'Corrected orientation',27,font_weight='700')
    solution+=text(36,80,'Aim the incoming Cl atom at the chlorine end of ClNO₂.',22)
    solution+=molecule(250,205,375,205,155,135,155,275)
    solution+=atom(785,205,'Cl')+arrow(445,205,535,205)+arrow(675,205,585,205)
    solution+=text(250,334,'ClNO₂',23,text_anchor='middle',font_weight='700')
    solution+=text(785,334,'Cl atom',23,text_anchor='middle',font_weight='700')
    solution+=text(500,378,'N–Cl breaks; a new Cl–Cl bond forms.',22,text_anchor='middle')
    solution+='<path d="M36 402H964" stroke="#dce2d9" stroke-width="2"/>'
    solution+=text(36,432,'Products',25,font_weight='700')
    solution+=bond(260,520,175,470)+bond(260,520,175,570)
    solution+=atom(260,520,'N')+atom(175,470,'O')+atom(175,570,'O')
    solution+=text(490,530,'+',34,text_anchor='middle')
    solution+=bond(685,520,785,520)+atom(685,520,'Cl')+atom(785,520,'Cl')
    solution+=text(240,620,'NO₂',24,text_anchor='middle',font_weight='700')
    solution+=text(735,620,'Cl₂',24,text_anchor='middle',font_weight='700')
    solution+=text(36,653,'Connectivity sketch only. Labels identify the atoms; colours are supplementary.',16,fill='#60736b')
    save('s1-3-q7-solution',solution)
    print('Created labelled SVGs and 2× PNGs for section 1.3 question 7.')

if __name__=='__main__':main()
