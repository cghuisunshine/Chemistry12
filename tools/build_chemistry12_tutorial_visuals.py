#!/usr/bin/env python3
"""Build textbook-aligned, accessible SVG teaching diagrams and install in tutorial.

No generation service is used. Coordinates, particle counts and relationships are
explicit. Run from any directory; existing visual blocks are replaced idempotently.
"""
from pathlib import Path
from html import escape
import json, math, re

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / 'assets/chemistry12-tutorial'
INK, GREEN, ORANGE, BLUE = '#213e36', '#235b47', '#b54f2c', '#315c88'
SOFT, LINE = '#eef2e9', '#dce2d9'

class Panel:
    def __init__(self): self.items=[]
    def raw(self,s): self.items.append(s)
    def text(self,x,y,s,size=20,color=INK,anchor='start',bold=False):
        self.raw(f'<text x="{x}" y="{y}" font-size="{size}" fill="{color}" text-anchor="{anchor}"'+(' font-weight="700"' if bold else '')+'>'+escape(s)+'</text>')
    def lines(self,x,y,lines,size=20,color=INK,gap=29):
        for i,t in enumerate(lines):self.text(x,y+i*gap,t,size,color)
    def line(self,x,y,X,Y,color=INK,width=3,dash=False):
        self.raw(f'<path d="M{x},{y}L{X},{Y}" fill="none" stroke="{color}" stroke-width="{width}"'+(' stroke-dasharray="6 5"' if dash else '')+'/>')
    def path(self,d,color=GREEN,width=4,dash=False):
        self.raw(f'<path d="{d}" fill="none" stroke="{color}" stroke-width="{width}"'+(' stroke-dasharray="7 6"' if dash else '')+'/>')
    def rect(self,x,y,w,h,fill=SOFT,stroke=LINE):
        self.raw(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="9" fill="{fill}" stroke="{stroke}" stroke-width="2"/>')
    def arrow(self,x,y,X,Y,color=INK):
        a=math.atan2(Y-y,X-x);bX,bY=X-12*math.cos(a),Y-12*math.sin(a)
        self.line(x,y,bX,bY,color)
        self.raw(f'<polygon points="{X},{Y} {bX-6*math.sin(a)},{bY+6*math.cos(a)} {bX+6*math.sin(a)},{bY-6*math.cos(a)}" fill="{color}"/>')
    def atom(self,x,y,s,r=21,color=GREEN):
        fills={GREEN:'#dfedb0',ORANGE:'#fbe0d4',BLUE:'#dbe9fa'}
        self.raw(f'<circle cx="{x}" cy="{y}" r="{r}" fill="{fills.get(color,SOFT)}" stroke="{color}" stroke-width="2"/>')
        self.text(x,y+6,s,17,color,'middle',True)
    def axes(self,ylabel='Concentration',xlabel='Time'):
        self.arrow(45,265,415,265);self.arrow(45,265,45,35)
        self.text(48,22,ylabel,18);self.text(415,295,xlabel,18,anchor='end')
    def vessel(self,x,y,w=160,h=150):
        self.path(f'M{x},{y}v{h}h{w}v-{h}',INK,3)
        self.rect(x+4,y+35,w-8,h-39,'#f0f6fc','#f0f6fc')
    def __str__(self):return ''.join(self.items)

VISUALS=[]
def add(n,left,right,caption,alt,draw):
    a,b=Panel(),Panel();draw(a,b)
    VISUALS.append(dict(section=n,left=left,right=right,caption=caption,alt=alt,a=str(a),b=str(b)))

def rate(a,b):
    a.axes();a.path('M45 70 Q170 200 405 225')
    def point(t):return ((1-t)**2*45+2*(1-t)*t*170+t*t*405,(1-t)**2*70+2*(1-t)*t*200+t*t*225)
    x1,y1=point(.15);x2,y2=point(.88);a.line(x1,y1,x2,y2,ORANGE)
    x,y=point(.57);slope=(260-210*.57)/(250+220*.57)
    a.line(x-65,y-65*slope,x+65,y+65*slope,BLUE);a.atom(x,y,'',4,BLUE)
    a.text(200,90,'Secant: average rate',19,ORANGE);a.text(155,249,'Tangent: rate at one instant',17,BLUE)
    b.axes('Amount of product','Time');b.line(50,245,380,60,GREEN);b.line(50,245,380,150,ORANGE)
    b.text(250,65,'Faster',21,GREEN);b.text(285,210,'Slower',21,ORANGE);b.text(55,330,'Compare slopes with the same units.',20)
add('1.1','Average and instantaneous rate','Steeper slope → faster change','Read the axes first. The secant averages over an interval; the tangent gives the instantaneous slope. Reactant disappearance rates use a minus sign.','A falling reactant curve with a secant and a tangent, beside two product lines with different positive slopes. Schematic graphs, not measured data.',rate)

def factors(a,b):
    for j,count in enumerate([4,9]):
        x=15+j*220;a.rect(x,45,190,170,'#fff');
        for i in range(count):a.atom(x+35+(i%3)*60,80+(i//3)*48,'A',16)
        a.text(x+95,250,['Lower c','Higher c'][j],21,anchor='middle')
    a.text(20,305,'Same volume; more particles → higher c.',19)
    def cube(x,y,side):
        d=side*.3;b.rect(x,y,side,side,'#dfedb0',GREEN)
        b.raw(f'<path d="M{x},{y}l{d},-{d}h{side}v{side}l-{d},{d}M{x+side},{y}l{d},-{d}" fill="none" stroke="{GREEN}" stroke-width="2"/>')
    cube(20,80,80);b.text(65,220,'One cube',19,anchor='middle')
    for i in range(8):cube(210+i%4*52,65+i//4*75,40)
    b.arrow(130,125,195,125);b.text(300,220,'Eight pieces',19,anchor='middle')
    b.lines(20,280,['Same solid volume; more exposed area.','Surface reactions have more available sites.'],19)
add('1.2','Concentration: particles per volume','Surface area: exposed reaction sites','These particle and solid models explain two rate factors. Temperature, catalyst and reactant identity also affect rate, as described in the section.','Equal-sized boxes contain four or nine particles. A cube is divided into eight smaller cubes, increasing total exposed surface area without changing its total volume.',factors)

def collision(a,b):
    a.lines(12,42,['Cl + ClNO₂ → Cl₂ + NO₂'],24)
    for x,s,c in [(60,'Cl',GREEN),(220,'Cl',GREEN),(310,'N',BLUE)]:a.atom(x,140,s,27,c)
    a.line(246,140,284,140);a.line(325,119,353,83);a.line(325,161,353,197);a.atom(370,65,'O',24,ORANGE);a.atom(370,215,'O',24,ORANGE)
    a.arrow(100,140,175,140);a.lines(16,280,['Suitable orientation: incoming Cl faces','the Cl end; enough energy is also needed.'],19)
    b.axes('Potential energy','Reaction coordinate');b.path('M45 210H95 C150 210 160 65 225 65 S290 235 350 235 H410')
    b.line(115,210,225,210,INK,2,True);b.arrow(180,207,180,75,ORANGE);b.text(190,148,'Eₐ',22,ORANGE)
    b.text(200,48,'Activated complex',19);b.text(55,332,'Eₐ is the barrier from the reactant level.',19)
add('1.3','Effective collision: orientation + energy','Activation energy and activated complex','ClNO₂ is drawn as a connectivity sketch, not a Lewis structure. The energy profile is schematic: it does not supply measured energies for this reaction.','An incoming chlorine atom approaches the bound chlorine of ClNO2. Beside it an energy barrier labels activation energy from reactants to the activated complex.',collision)

def energy(a,b):
    a.axes('Potential energy','Reaction coordinate');a.path('M45 150H100 C145 150 165 55 215 55 S280 225 350 225 H410');a.text(53,137,'R',20);a.text(372,213,'P',20)
    a.line(105,150,310,150,INK,2,True);a.arrow(145,148,145,60,ORANGE);a.text(155,105,'Eₐ forward',18,ORANGE);a.arrow(330,154,330,221,BLUE);a.text(340,185,'ΔH',20,BLUE);a.text(55,332,'Products lower → ΔH < 0 (exothermic).',19)
    b.axes('Potential energy','Reaction coordinate');b.path('M45 170H90 C150 170 170 50 225 50 S295 225 350 225 H410',ORANGE)
    b.path('M45 170H90 C150 170 170 120 225 120 S295 225 350 225 H410',GREEN)
    b.text(220,43,'Uncatalyzed',19,ORANGE);b.text(230,117,'Catalyzed',19,GREEN);b.text(55,332,'Same start and end → same ΔH.',20)
add('1.4','Read three separate energy levels','Catalyst: another pathway','The horizontal axis is reaction progress, not time. A catalyst lowers the barrier without changing the reactant–product enthalpy difference.','Exothermic energy curve labels forward activation energy and the negative enthalpy change. A second plot compares higher uncatalyzed and lower catalyzed barriers with identical endpoints.',energy)

def mechanism(a,b):
    a.lines(20,55,['A + B → I     slow','I + B → P     fast'],25,gap=67);a.line(15,151,420,151)
    a.text(20,196,'A + 2B → P',27,bold=True);a.lines(20,260,['I is formed, then consumed: intermediate.','A catalyst is consumed, then regenerated.'],18)
    b.text(20,45,'Slow elementary step: A + B → I',22);b.rect(20,75,395,85);b.text(215,126,'rate ≈ k[A][B]',29,anchor='middle',bold=True)
    b.lines(20,220,['Overall B coefficient = 2','B order in this mechanism = 1','Measure the overall rate law.'],21,gap=43)
add('1.5','Mechanism: steps sum to the reaction','Slow elementary step and rate law','This hypothetical mechanism illustrates intermediate cancellation. Coefficients of the overall reaction do not generally give the measured reaction orders.','Two steps A plus B to I and I plus B to P sum to A plus 2B to P. The slow first elementary step predicts a rate proportional to A and B, despite the overall coefficient 2 for B.',mechanism)

def dynamic(a,b):
    a.rect(15,40,410,190,'#fff');a.text(90,95,'A',34,anchor='middle');a.text(350,95,'B',34,anchor='middle');a.arrow(140,85,300,85,GREEN);a.arrow(300,140,140,140,ORANGE);a.text(220,190,'Equal opposing rates',22,anchor='middle');a.lines(20,280,['Closed system; constant conditions.','Molecular changes continue.'],20)
    b.axes('Reaction rate','Time');b.path('M45 60 C110 95 135 160 260 160 H410',GREEN);b.path('M45 255 C110 210 160 160 260 160 H410',ORANGE);b.line(260,35,260,265,INK,2,True)
    b.text(60,52,'Forward',18,GREEN);b.text(65,235,'Reverse',18,ORANGE);b.text(277,195,'Equal, nonzero',17);b.text(40,332,'Equal rates; concentrations need not match.',18)
add('2.1','Dynamic equilibrium: changes continue','Forward rate = reverse rate','At equilibrium each species is produced as quickly as it is consumed. Its concentration stays constant, but different species can have different concentrations.','Opposing A to B and B to A arrows inside a closed boundary. Forward and reverse rate curves converge to the same nonzero rate.',dynamic)

def lechat(a,b):
    a.text(20,40,'A ⇌ B',30,bold=True);a.rect(20,85,180,100);a.text(110,125,'Add A',24,anchor='middle');a.text(110,157,'immediate stress',17,anchor='middle');a.arrow(220,135,280,135);a.text(295,130,'Shift',21);a.text(295,160,'right',21)
    a.lines(20,260,['Some added A is consumed.','The original concentration is not restored.'],19)
    b.axes('[A]','Time');b.path('M45 175H170 V70 C195 70 230 125 290 125 H410');b.line(170,40,170,265,ORANGE,2,True);b.text(181,55,'Add A',19,ORANGE);b.text(275,112,'New equilibrium',17);b.line(45,175,410,175,INK,2,True);b.text(30,332,'Jump first; chemical adjustment follows.',19)
add('2.2','Le Chatelier: partly oppose a stress','Separate the jump from the shift','For this A ⇌ B example, adding A causes an immediate increase followed by partial consumption at fixed temperature and volume.','Adding reactant A shifts A to B. Its concentration–time graph jumps upward, then falls to a new plateau above the initial concentration.',lechat)

def volume(a,b):
    a.text(20,42,'N₂(g) + 3H₂(g) ⇌ 2NH₃(g)',23,bold=True)
    a.rect(25,90,170,135,'#fff');a.rect(280,90,100,135,'#fff');a.arrow(210,155,265,155);a.text(110,165,'V',27,anchor='middle');a.text(330,165,'V/2',27,anchor='middle')
    a.text(110,265,'Compress',22,anchor='middle');a.text(330,265,'Shift right',22,anchor='middle');a.text(20,320,'4 gas particles → 2: partial pressure relief.',18)
    b.text(20,42,'Exothermic forward reaction',22,bold=True);b.text(20,100,'Reactants ⇌ Products + heat',23)
    b.arrow(310,150,125,150,ORANGE);b.text(220,190,'Heat → shift left',22,ORANGE,'middle')
    b.arrow(125,245,310,245,GREEN);b.text(220,285,'Cool → shift right',22,GREEN,'middle');b.text(20,335,'Temperature changes K.',20)
add('2.3','Volume: count gaseous coefficients','Temperature: identify the heat side','Compression at fixed temperature favours fewer gas particles when gas coefficients differ. Heating favours the endothermic direction; cooling favours the exothermic direction.','For nitrogen plus three hydrogen to two ammonia, compression favours the two-gas-particle product side. Heating an exothermic equilibrium shifts left and cooling shifts right.',volume)

def entropy(a,b):
    a.rect(15,55,170,180,'#fff');a.rect(250,55,170,180,'#fff')
    for i in range(9):a.atom(60+i%3*40,100+i//3*40,'',10)
    for x,y in [(285,80),(390,90),(310,145),(395,180),(275,205),(350,210),(355,120),(290,175),(350,85)]:a.atom(x,y,'',10)
    a.arrow(200,145,235,145);a.text(100,278,'More ordered',19,anchor='middle');a.text(335,278,'More arrangements',19,anchor='middle');a.text(20,330,'Particle sketch: more accessible microstates.',18)
    b.text(20,45,'Two tendencies',26,bold=True);b.arrow(50,95,50,200,GREEN);b.lines(80,115,['Lower enthalpy','ΔH < 0'],22);b.arrow(50,300,50,235,ORANGE);b.lines(80,255,['Higher entropy','ΔS > 0'],22)
    b.text(20,340,'If opposed, temperature and size matter.',19)
add('2.4','Entropy: accessible arrangements','Enthalpy and entropy tendencies','The sketches illustrate an entropy trend, not a complete spontaneity test. When enthalpy and entropy tendencies oppose, temperature and their magnitudes matter.','Ordered and dispersed arrangements of the same nine particles illustrate more accessible arrangements. Separate arrows show tendencies toward lower enthalpy and higher entropy.',entropy)

def equilibrium_constant(a,b):
    a.text(15,45,'N₂(g) + 3H₂(g) ⇌ 2NH₃(g)',23,bold=True);a.text(215,125,'[NH₃]²',29,anchor='middle');a.line(100,145,335,145);a.text(215,185,'[N₂][H₂]³',29,anchor='middle');a.text(15,152,'K =',26)
    a.lines(20,260,['Coefficients become exponents.','Omit pure solids and pure liquids.'],21)
    b.line(40,130,405,130);b.atom(75,130,'Q',24,BLUE);b.atom(220,130,'K',24);b.atom(370,130,'Q',24,ORANGE)
    b.arrow(95,185,195,185,BLUE);b.arrow(350,185,250,185,ORANGE);b.text(45,230,'Q < K: right',19,BLUE);b.text(255,230,'Q > K: left',19,ORANGE);b.lines(20,300,['Q = K: equilibrium','Same expression; current vs equilibrium c.'],18)
add('2.5','K uses equilibrium concentrations','Q tells the adjustment direction','Use the same balanced expression for Q and K. Compare them at the same temperature; K alone says nothing about reaction speed.','The ammonia equilibrium expression places squared ammonia over nitrogen times cubed hydrogen. A comparison line places Q below or above K with arrows toward equilibrium.',equilibrium_constant)

def ice(a,b):
    a.text(15,35,'H₂ + I₂ ⇌ 2HI',27,bold=True)
    for x,t in [(25,''),(140,'H₂'),(245,'I₂'),(355,'HI')]:a.text(x,90,t,22)
    for i,row in enumerate([['I','1.0','1.0','0'],['C','−x','−x','+2x'],['E','1−x','1−x','2x']]):
        y=142+i*60;a.line(15,y-32,425,y-32,LINE,2)
        for x,t in zip([25,140,245,355],row):a.text(x,y,t,22)
    a.text(20,330,'Molar concentrations; change follows ratios.',18)
    b.text(20,60,'Substitute E into K',25,bold=True);b.text(20,125,'K = (2x)² / (1 − x)²',26);b.arrow(220,155,220,205)
    b.lines(20,245,['Solve → reject impossible roots','Check: concentrations ≥ 0','Substitute back into K.'],21,gap=42)
add('2.6','ICE: initial, change, equilibrium','Solve and check the equilibrium','This hypothetical starting mixture has 1.0 M each of H₂ and I₂ and no HI. The value of K is required to determine x.','An ICE table for H2 plus I2 to 2HI has changes minus x, minus x and plus 2x. The resulting expression is K equals 4x squared divided by 1 minus x squared.',ice)

def soluble(a,b):
    a.vessel(20,55,180,180);a.vessel(240,55,180,180)
    for x,y,t,c in [(60,115,'+',GREEN),(140,135,'−',BLUE),(75,190,'−',BLUE),(155,205,'+',GREEN)]:a.atom(x,y,t,19,c)
    for x,y in [(280,115),(370,135),(290,190),(370,205)]:a.atom(x,y,'M',19,ORANGE)
    a.text(110,280,'Ions carry charge',18,anchor='middle');a.text(330,280,'Neutral molecules',18,anchor='middle');a.text(20,330,'Electrolyte',21,GREEN);a.text(245,330,'Non-electrolyte',21,ORANGE)
    b.vessel(100,45,240,190)
    for x,y,s,c in [(140,115,'+',GREEN),(280,105,'−',BLUE),(225,155,'+',GREEN),(155,175,'−',BLUE)]:b.atom(x,y,s,19,c)
    b.rect(140,205,160,26,'#d7ddd1',GREEN);b.arrow(180,200,180,155);b.arrow(255,160,255,200);b.lines(20,285,['Saturated: dissolution = crystallization','when excess solid is present.'],20)
add('3.1','Electrolyte: mobile ions in solution','Saturation is a dynamic balance','Ion and molecule sketches distinguish conductivity. In a saturated solution with excess solid, ions still exchange between the solid and solution.','Mobile positive and negative ions are compared with neutral molecular solute. A saturated solution above excess solid has equal dissolution and crystallization directions.',soluble)

def qualitative(a,b):
    a.vessel(90,65,250,170);a.text(215,35,'Unknown solution + reagent',22,anchor='middle');a.arrow(220,45,220,105);a.rect(125,200,180,28,'#e8ddd0',ORANGE);a.text(215,278,'Observation: solid appears',21,anchor='middle');a.text(20,330,'Inference: a low-solubility salt formed.',19)
    b.rect(20,45,395,65);b.text(217,86,'Add selective reagent',23,anchor='middle');b.arrow(215,120,215,150);b.text(215,185,'Filter the precipitate',23,anchor='middle');b.arrow(215,205,215,235);b.lines(35,275,['Test filtrate for remaining ions.','Use confirmatory tests when needed.'],20)
add('3.2','Precipitation: evidence, then inference','Separate before the next ion test','Use the textbook solubility table to choose reagents. A precipitate alone may fit more than one possible ion, so plan selective and confirmatory tests.','A reagent is added to an unknown solution and a solid appears. A separation sequence shows selective reagent addition, filtration, then testing the remaining filtrate.',qualitative)

def ksp(a,b):
    a.text(15,40,'PbCl₂(s) ⇌ Pb²⁺(aq) + 2Cl⁻(aq)',22,bold=True)
    a.atom(90,130,'Pb²⁺',34,GREEN);a.atom(260,105,'Cl⁻',29,BLUE);a.atom(350,175,'Cl⁻',29,BLUE)
    a.text(90,210,'s',28,anchor='middle');a.text(305,240,'2s total',26,anchor='middle');a.text(20,320,'Pure water: [Pb²⁺] = s; [Cl⁻] = 2s.',20)
    b.text(20,60,'Ksp = [Pb²⁺][Cl⁻]²',28,bold=True);b.text(20,120,'= s(2s)² = 4s³',28);b.rect(20,170,395,75);b.text(215,217,'s = (Ksp / 4)⅓',27,anchor='middle')
    b.lines(20,295,['Solid omitted; temperature fixed.','A common ion changes the s relationship.'],19)
add('3.3','Molar solubility and ion ratios','Build Ksp from the balanced equation','The s and 2s relationships apply when PbCl₂ is the only source of its ions in initially pure water. A common ion requires an initial concentration term.','One dissolved PbCl2 formula unit gives one lead ion and two chloride ions. Molar solubility s leads to Ksp equals s times 2s squared, or 4s cubed.',ksp)

def precip(a,b):
    a.vessel(25,55,150,130);a.vessel(260,55,150,130);a.text(100,110,'Ag⁺',27,anchor='middle');a.text(335,110,'Cl⁻',27,anchor='middle');a.text(100,220,'c₁, V₁',24,anchor='middle');a.text(335,220,'c₂, V₂',24,anchor='middle')
    a.lines(20,285,['After mixing, before reaction:','[Ag⁺] = c₁V₁ / (V₁ + V₂)'],21)
    b.text(20,45,'Qsp = [Ag⁺][Cl⁻]',28,bold=True)
    for y,s,c in [(115,'Qsp < Ksp → unsaturated',BLUE),(185,'Qsp = Ksp → threshold',GREEN),(255,'Qsp > Ksp → precipitation',ORANGE)]:b.text(20,y,s,23,c)
    b.text(20,330,'Use mixed concentrations, not stock values.',18)
add('3.4','Mixing dilutes each ion','Compare the trial ion product to Ksp','Assume additive solution volumes. First calculate each ion’s concentration after mixing, before precipitation; then evaluate Qsp using the salt’s stoichiometry.','Separate silver and chloride solutions are mixed. Their diluted concentrations form Qsp, which is compared with Ksp for unsaturation, equilibrium threshold or precipitation.',precip)

def acidbase(a,b):
    a.text(20,50,'HA + H₂O ⇌ A⁻ + H₃O⁺',27,bold=True);a.arrow(65,95,330,95,ORANGE);a.text(200,135,'H⁺ transfer',23,ORANGE,'middle')
    a.lines(20,210,['HA: donor → acid','H₂O: acceptor → base'],23,gap=55);a.text(20,330,'Water’s role depends on its partner.',19)
    b.text(20,50,'HA / A⁻',30,bold=True);b.text(20,95,'H₂O / H₃O⁺',30,bold=True);b.lines(20,165,['Each conjugate pair differs by one H⁺.','Losing H⁺ lowers the charge by 1.','Gaining H⁺ raises the charge by 1.'],20,gap=43)
    b.text(20,330,'Example: NH₄⁺ / NH₃ is a conjugate pair.',19)
add('4.1','Brønsted–Lowry: track the proton','Conjugate pairs differ by one H⁺','These diagrams show proton transfer in water. They complement the Arrhenius definitions given above and explain how water can act as either acid or base.','HA gives a proton to water, forming A minus and hydronium. The conjugate pairs HA/A minus and water/hydronium differ by exactly one proton and one charge unit.',acidbase)

def strength(a,b):
    a.text(110,35,'Strong acid',22,anchor='middle',bold=True);a.text(330,35,'Weak acid',22,anchor='middle',bold=True)
    a.rect(15,60,190,200,'#fff');a.rect(235,60,190,200,'#fff')
    for i in range(6):
        x=50+i%2*100;y=100+i//2*60;a.atom(x,y,'+',17,ORANGE);a.atom(x+35,y,'−',17,BLUE)
        x=270+i%2*100
        if i==0:a.atom(x,y,'+',17,ORANGE);a.atom(x+35,y,'−',17,BLUE)
        else:a.atom(x+15,y,'HA',22)
    a.text(20,315,'Same formal concentration; different ionization.',17)
    b.lines(20,55,['Strength: tendency to ionize','Concentration: amount per volume'],22,gap=55);b.rect(20,170,395,65);b.text(218,211,'Larger Ka → stronger acid',23,anchor='middle');b.lines(20,285,['Stronger acid → weaker conjugate base.','Particle counts are illustrative, not exact.'],18)
add('4.2','Strong versus weak at the same C','Strength and concentration are distinct','The particle models contain the same number of original acid units. The weak-acid ionization fraction is illustrative; it depends on Ka and concentration.','Equal acid-unit counts show complete ionization for a strong acid and partial ionization for a weak acid. Labels distinguish strength from concentration and relate larger Ka to stronger acid.',strength)

def water(a,b):
    a.text(20,55,'2H₂O ⇌ H₃O⁺ + OH⁻',29,bold=True);a.atom(110,150,'H₃O⁺',40,ORANGE);a.atom(330,150,'OH⁻',40,BLUE);a.text(110,228,'10⁻⁷ M',25,anchor='middle');a.text(330,228,'10⁻⁷ M',25,anchor='middle');a.lines(20,300,['Neutral pure water at 25 °C.','Ion concentrations are equal, not zero.'],19)
    b.text(20,55,'Kw = [H₃O⁺][OH⁻]',29,bold=True);b.text(20,105,'= 1.0 × 10⁻¹⁴ at 25 °C',25);b.arrow(70,230,70,160,ORANGE);b.arrow(300,160,300,230,BLUE);b.text(70,275,'[H₃O⁺] ↑',22,ORANGE,'middle');b.text(300,275,'[OH⁻] ↓',22,BLUE,'middle');b.text(20,335,'Fixed temperature → fixed product.',21)
add('4.3','Water produces both kinds of ion','At fixed temperature, Kw is constant','Neutrality always means equal hydronium and hydroxide concentrations. The familiar 10⁻⁷ M values and neutral pH 7 apply at 25 °C.','Autoionization of two waters gives hydronium and hydroxide. Both are 10 to the minus 7 M in neutral pure water at 25 degrees C; increasing one lowers the other at fixed Kw.',water)

def ph(a,b):
    a.line(30,150,410,150,INK,4)
    for x,n in [(30,'0'),(220,'7'),(410,'14')]:a.line(x,140,x,160);a.text(x,195,n,26,anchor='middle')
    a.text(30,110,'Acidic',23,ORANGE);a.text(410,110,'Basic',23,BLUE,'end');a.text(220,245,'Neutral',22,GREEN,'middle');a.text(20,325,'Familiar dilute-solution scale at 25 °C.',19)
    b.text(20,45,'pH = −log₁₀[H₃O⁺]',28,bold=True)
    for x,n,c in [(70,'3','10⁻³ M'),(215,'4','10⁻⁴ M'),(360,'5','10⁻⁵ M')]:b.atom(x,140,n,31);b.text(x,220,c,22,anchor='middle')
    b.arrow(110,140,170,140);b.arrow(255,140,315,140);b.lines(20,285,['One pH unit higher → 10× less [H₃O⁺].','pH + pOH = 14.00 at 25 °C.'],19)
add('4.4','pH locates acidic, neutral and basic','A logarithmic step is a factor of ten','Use the dilute-solution concentration approximation here. The 0–14 range is a familiar teaching scale, not an absolute limit; Kw changes with temperature.','A pH scale marks acidic below 7, neutral at 7 and basic above 7 at 25 degrees C. Steps from pH 3 to 4 to 5 show hydronium dropping tenfold each step.',ph)

def weak(a,b):
    a.text(15,35,'HA + H₂O ⇌ A⁻ + H₃O⁺',25,bold=True)
    for x,t in [(15,''),(140,'HA'),(245,'A⁻'),(335,'H₃O⁺')]:a.text(x,90,t,22)
    for i,row in enumerate([['I','C','0','≈0'],['C','−x','+x','+x'],['E','C−x','x','x']]):
        y=142+i*60;a.line(15,y-32,425,y-32,LINE,2)
        for x,t in zip([25,140,245,355],row):a.text(x,y,t,22)
    a.text(20,330,'Percent ionization = 100x / C',23)
    b.text(20,60,'Ka = x² / (C − x)',30,bold=True);b.arrow(215,90,215,150);b.text(20,200,'If x ≪ C:  x ≈ √(KaC)',27);b.lines(20,275,['Check x/C ≤ 0.05 (5% guideline).','If it fails, solve the full equation.'],20)
add('4.5','Ionization: x relative to starting C','The square-root shortcut needs a check','This weak monoprotic acid model neglects water’s hydronium contribution. That requires x to be large compared with the hydronium from water.','A weak-acid ICE relation gives remaining HA as C minus x and each ion as x. Ka equals x squared over C minus x, approximated by x squared over C only if x is small.',weak)

def hydrolysis(a,b):
    a.text(20,45,'NaCH₃COO → Na⁺ + CH₃COO⁻',24,bold=True);a.arrow(125,90,75,155);a.arrow(300,90,320,155);a.lines(20,200,['Na⁺','Spectator'],23,gap=35);a.lines(240,200,['CH₃COO⁻','Reacts as a base'],21,gap=35);a.text(20,330,'Assess each dissolved ion separately.',20)
    b.lines(15,55,['CH₃COO⁻ + H₂O','⇌ CH₃COOH + OH⁻'],27,gap=55);b.atom(215,205,'OH⁻',45,BLUE);b.text(215,290,'Basic solution',26,BLUE,'middle');b.text(20,335,'Kb = Kw / Ka of the conjugate acid',20)
add('5.1','Salt: separate the ions first','A weak acid’s conjugate base hydrolyzes','Sodium acetate is the basic-salt example. Other salts can be acidic or neutral; amphiprotic ions and salts with two reactive ions need further comparison.','Sodium acetate dissociates into spectator sodium and acetate, which accepts a proton from water and produces hydroxide, making the solution basic.',hydrolysis)

def buffer(a,b):
    a.atom(100,135,'HA',47);a.atom(330,135,'A⁻',47,BLUE);a.text(100,230,'Weak acid',23,anchor='middle');a.text(330,230,'Conjugate base',22,anchor='middle');a.lines(20,295,['Both in appreciable amounts.','Together they resist small pH changes.'],20)
    b.text(20,45,'Added acid: A⁻ + H₃O⁺ → HA + H₂O',21);b.text(20,110,'Added base: HA + OH⁻ → A⁻ + H₂O',21);b.line(20,150,415,150,LINE,2)
    b.lines(20,205,['Ratio [A⁻]/[HA] → mainly sets pH','Total amounts → buffer capacity'],21,gap=55);b.text(20,330,'Neutralize the addition before using Ka.',20)
add('5.2','Buffer: a weak acid and its partner','Each partner removes an added reagent','Buffering works while both components remain available. Do the neutralization mole calculation first; dilution lowers capacity even if the ratio changes little.','A buffer contains a weak acid HA and conjugate base A minus. A minus consumes added hydronium, while HA consumes added hydroxide; their ratio affects pH and total amounts affect capacity.',buffer)

def titration(a,b):
    a.rect(180,35,55,145,'#f0f6fc',BLUE)
    for y in range(55,170,20):a.line(180,y,194,y,BLUE,2)
    a.line(175,188,245,188);a.line(208,180,208,220,BLUE);a.atom(208,238,'',6,BLUE)
    a.path('M150 225V250L110 300H305L265 250V225',INK,3);a.line(140,280,275,280,BLUE,3)
    a.text(15,75,'Titrant',23);a.text(15,110,'Known c',20);a.text(290,290,'Analyte',20);a.text(20,340,'Delivered volume = final − initial reading.',18)
    b.text(20,45,'At equivalence: mole ratios match.',22,bold=True);b.text(20,105,'HCl + NaOH → NaCl + H₂O',24);b.text(20,175,'1 mol : 1 mol',28);b.text(20,235,'c(HCl)V(HCl) = c(NaOH)V(NaOH)',21);b.lines(20,300,['Endpoint: the observed signal.','Choose a signal near equivalence.'],20)
add('5.3','Burette, titrant and analyte','Equivalence follows stoichiometry','The equal cV relation shown is for a 1:1 reaction. Use the balanced mole ratio for other titrations. An indicator endpoint is an experimental approximation to equivalence.','A burette of known titrant delivers drops to an analyte flask. A one-to-one HCl/NaOH reaction makes acid and base moles equal at equivalence, distinguished from the observed endpoint.',titration)

def curve(a,b):
    a.axes('pH','Volume NaOH added');a.path('M45 235 C70 190 130 170 190 160 S240 150 250 100 S260 60 300 55 L410 45');a.line(250,45,250,265,INK,2,True);a.atom(147.5,172.1,'',5,BLUE);a.atom(250,100,'',5,ORANGE)
    a.text(65,132,'½Veq: pH = pKa',19,BLUE);a.text(265,120,'Veq: pH > 7',18,ORANGE);a.text(30,330,'Weak acid + strong base, 25 °C.',20)
    b.text(20,40,'Choose the model by the region',22,bold=True)
    for y,t in [(100,'Initially → weak-acid equilibrium'),(160,'Before Veq → HA/A⁻ buffer'),(220,'At Veq → A⁻ hydrolysis'),(280,'After Veq → excess OH⁻')]:b.text(20,y,t,22)
    b.text(20,335,'Indicator range must fit the steep region.',18)
add('5.4','A titration curve shows changing species','One curve needs several pH models','Schematic curve for a weak monoprotic acid titrated with a strong base at 25 °C. Half-equivalence gives pH ≈ pKa in the usual buffer approximation; equivalence is basic.','A rising weak-acid strong-base titration curve marks half-equivalence at pH equal to pKa and equivalence above 7. The second panel assigns the appropriate calculation to each region.',curve)

def oxide(a,b):
    a.text(20,45,'Reactive metal oxide',25,bold=True);a.text(20,110,'Na₂O + H₂O → 2NaOH',26);a.atom(215,210,'OH⁻',42,BLUE);a.text(215,300,'Basic solution',25,BLUE,'middle')
    b.text(20,45,'Acid-forming non-metal oxide',23,bold=True);b.text(20,110,'SO₃ + H₂O → H₂SO₄',26);b.atom(215,210,'H₃O⁺',42,ORANGE);b.text(215,300,'Acidic solution',25,ORANGE,'middle');b.text(20,340,'H₂SO₄ ionizes in water.',20)
add('5.5','Basic anhydride: a metal-oxide example','Acidic anhydride: a non-metal example','These are representative reactive oxides, not universal rules. Some metal and non-metal oxides are unreactive, insoluble, neutral or amphoteric.','Sodium oxide reacts with water to form sodium hydroxide and a basic solution. Sulfur trioxide forms sulfuric acid, which ionizes to give an acidic solution.',oxide)

def redox(a,b):
    a.text(20,45,'Zn → Zn²⁺ + 2e⁻',28,bold=True);a.text(20,95,'Oxidation: electrons lost',23,ORANGE);a.text(20,185,'Cu²⁺ + 2e⁻ → Cu',28,bold=True);a.text(20,235,'Reduction: electrons gained',23,BLUE);a.text(20,330,'Electron loss = electron gain.',22)
    b.atom(80,150,'Zn',36);b.atom(350,150,'Cu²⁺',39,BLUE);b.arrow(135,150,290,150,ORANGE);b.text(215,125,'2e⁻',26,ORANGE,'middle');b.text(80,235,'Reducing',22,anchor='middle');b.text(80,267,'agent',22,anchor='middle');b.text(350,235,'Oxidizing',22,anchor='middle');b.text(350,267,'agent',22,anchor='middle');b.text(20,330,'The reducing agent is itself oxidized.',19)
add('6.1','Oxidation loses; reduction gains','The agent causes its partner’s change','The zinc/copper-ion example shows coupled electron transfer. Oxidation numbers increase on oxidation and decrease on reduction.','Zinc loses two electrons to become zinc 2 plus; copper 2 plus gains two electrons to become copper metal. Zinc is the reducing agent and copper ion is the oxidizing agent.',redox)

def balance(a,b):
    a.lines(20,45,['Oxidation:','Zn → Zn²⁺ + 2e⁻','Reduction (×2):','2Ag⁺ + 2e⁻ → 2Ag'],25,gap=58);a.line(15,265,425,265,LINE,2);a.text(20,315,'Zn + 2Ag⁺ → Zn²⁺ + 2Ag',25,bold=True)
    b.text(20,40,'In acidic solution',24,bold=True);b.lines(20,95,['O atoms → add H₂O','H atoms → add H⁺','Charge → add e⁻'],23,gap=48);b.text(20,260,'For basic solution',24,bold=True);b.lines(20,305,['Add OH⁻ to remove H⁺ as H₂O;','cancel excess H₂O and check charge.'],20)
add('6.2','Balance electron loss and gain','Balance atoms and charge in the medium','The simple metal example cancels two electrons. Reactions containing oxygen and hydrogen also require the water/H⁺/OH⁻ steps appropriate to the medium.','Zinc oxidation produces two electrons; two silver-ion reductions consume them, giving a balanced overall reaction. An acidic balancing guide uses water, hydrogen ions and electrons, then hydroxide for conversion to basic medium.',balance)

def potential(a,b):
    a.text(20,40,'Table entries are reductions',25,bold=True);a.rect(15,75,410,75);a.text(30,108,'Cu²⁺ + 2e⁻ → Cu',24);a.text(400,137,'+0.34 V',22,anchor='end');a.rect(15,175,410,75);a.text(30,208,'Zn²⁺ + 2e⁻ → Zn',24);a.text(400,237,'−0.76 V',22,anchor='end');a.text(20,330,'More positive → greater reduction tendency.',18)
    b.lines(20,50,['Cu²⁺ is reduced; Zn is oxidized.','E°cell = E°cathode − E°anode'],23,gap=65);b.text(20,195,'= 0.34 − (−0.76) = +1.10 V',25,bold=True);b.lines(20,275,['Positive: favourable at standard conditions.','Do not multiply E° by a coefficient.'],18)
add('6.3','Compare standard reduction potentials','Subtract the two tabulated reductions','Typical rounded Table A7 values are shown. The sign predicts standard-state thermodynamic direction; it does not establish a fast reaction.','Copper reduction at plus 0.34 volts is compared with zinc reduction at minus 0.76 volts. Copper-ion reduction with zinc oxidation gives standard cell potential plus 1.10 volts.',potential)

def galvanic(a,b):
    a.vessel(20,135,145,150);a.vessel(270,135,145,150);a.rect(65,105,22,130,'#ddd',INK);a.rect(340,105,22,130,'#ddd',INK);a.path('M77 100V55H350V100',INK,3);a.arrow(145,55,275,55,ORANGE);a.text(215,35,'e⁻ through wire',20,ORANGE,'middle')
    a.path('M130 165V115Q215 80 300 115V165',BLUE,8);a.text(215,205,'Salt bridge',18,BLUE,'middle');a.text(90,325,'Anode (−)',22,anchor='middle');a.text(345,325,'Cathode (+)',22,anchor='middle')
    b.lines(20,50,['Anode: Zn → Zn²⁺ + 2e⁻','Cathode: Cu²⁺ + 2e⁻ → Cu'],24,gap=58);b.line(20,145,415,145,LINE,2);b.arrow(220,200,60,200,BLUE);b.text(220,240,'Anions → anode',22,BLUE,'middle');b.arrow(220,270,380,270,GREEN);b.text(220,310,'Cations → cathode',22,GREEN,'middle')
add('6.4','Galvanic cell: spontaneous electricity','Electrons in wire; ions in electrolyte','Zinc/copper galvanic cell: electrons travel from the negative anode to the positive cathode. The salt bridge maintains charge balance by ion migration.','Two half-cells are connected by an external wire and salt bridge. Electrons flow from zinc anode to copper cathode. Anions migrate toward the anode and cations toward the cathode.',galvanic)

def electrolysis(a,b):
    a.rect(125,30,190,65,'#fff',ORANGE);a.text(220,72,'DC supply',24,anchor='middle');a.text(143,120,'+',26,ORANGE);a.text(290,120,'−',26,BLUE);a.line(145,95,80,145);a.line(295,95,355,145);a.vessel(25,165,390,155);a.rect(70,140,20,140,'#ddd',INK);a.rect(345,140,20,140,'#ddd',INK);a.text(105,350,'Anode (+)',22,anchor='middle');a.text(330,350,'Cathode (−)',22,anchor='middle');a.arrow(220,220,320,220,BLUE);a.text(220,260,'Na⁺',20,BLUE,'middle')
    b.text(20,40,'Molten NaCl (no water present)',22,bold=True);b.lines(20,95,['Anode: 2Cl⁻ → Cl₂ + 2e⁻','Cathode: 2Na⁺ + 2e⁻ → 2Na'],23,gap=50);b.rect(20,200,395,65);b.text(215,241,'Q = It;  mol e⁻ = Q/F',25,anchor='middle');b.lines(20,310,['In water, water can also react.','Available species determine the products.'],19)
add('6.5','Electrolysis: electrical energy drives change','Use electron stoichiometry and charge','This is molten sodium chloride, so sodium forms at the cathode. Aqueous NaCl has different competing reactants and must be assessed separately using the book’s table notes.','A DC supply connects positive anode and negative cathode in molten sodium chloride. Chloride is oxidized to chlorine and sodium ions are reduced to sodium. Charge equals current times time and electron moles equal charge over Faraday constant.',electrolysis)

CSS='''/* BEGIN textbook teaching visuals */
.lesson-visual{margin:22px 0 28px;border:1px solid var(--border);border-radius:12px;background:#fff;overflow:hidden;break-inside:avoid}
.lesson-visual>a,.lesson-visual picture{display:block;background:#fff}.lesson-visual img{display:block;width:100%;height:auto}
.lesson-visual figcaption{padding:14px 18px;border-top:1px solid var(--border);font-size:13px;line-height:1.65;color:var(--muted)}
.lesson-visual figcaption strong{color:var(--ink)}.visual-links{display:flex;flex-wrap:wrap;gap:8px 20px;margin-top:8px}
@media(max-width:760px){.lesson-visual figcaption{padding:12px;font-size:12px}}
@media print{.lesson-visual{border-color:#bbb}.visual-links{display:none}.lesson-visual figcaption{font-size:9pt}}
/* END textbook teaching visuals */'''

def main():
    ASSETS.mkdir(parents=True,exist_ok=True)
    target=ROOT/'tutorial.html';html=target.read_text()
    structure=json.loads(re.search(r'<script[^>]*id="studyPageStructure"[^>]*>(.*?)</script>',html,re.S)[1])
    sections={s['id'].removeprefix('section-').replace('-','.'):s for c in structure for s in c['sections']}
    assert set(sections)=={v['section'] for v in VISUALS}
    html=re.sub(r'<!-- BEGIN textbook visual .*?<!-- END textbook visual -->\n?','',html,flags=re.S)
    html=re.sub(r'/\* BEGIN textbook teaching visuals \*/.*?/\* END textbook teaching visuals \*/\n?','',html,flags=re.S)
    manifest=[]
    for v in VISUALS:
        n=v['section'];s=sections[n];stem='section-'+n.replace('.','-');src='assets/chemistry12-tutorial/'+stem+'.svg'
        title=f'{n}: {v["left"]}; {v["right"]}'
        svg=f'''<svg xmlns="http://www.w3.org/2000/svg" width="1000" height="500" viewBox="0 0 1000 500" role="img" aria-labelledby="title desc">
<title id="title">{escape(title)}</title><desc id="desc">{escape(v['alt'])}</desc>
<rect width="1000" height="500" fill="#fff"/><g font-family="Arial, Helvetica, sans-serif" fill="{INK}">
<text x="30" y="34" font-size="18" fill="{GREEN}">§{n} · Definitions &amp; theory · Schematic teaching model</text>
<rect x="20" y="55" width="470" height="420" rx="12" fill="#f7f9f4"/><rect x="510" y="55" width="470" height="420" rx="12" fill="#f7f9f4"/>
<text x="38" y="88" font-size="18" font-weight="700">{escape(v['left'])}</text><text x="528" y="88" font-size="18" font-weight="700">{escape(v['right'])}</text>
<g transform="translate(35 108)">{v['a']}</g><g transform="translate(525 108)">{v['b']}</g></g></svg>'''
        (ROOT/src).write_text(svg)
        # Stack the same two panels on small screens, preserving useful label size.
        mobile=src.replace('.svg','-stacked.svg')
        stacked=svg.replace('width="1000" height="500" viewBox="0 0 1000 500"','width="500" height="960" viewBox="0 0 500 960"').replace('<rect width="1000" height="500"','<rect width="500" height="960"')
        stacked=stacked.replace('x="510" y="55"','x="20" y="520"').replace('x="528" y="88"','x="38" y="553"').replace('translate(525 108)','translate(35 573)')
        stacked=stacked.replace(f'§{n} · Definitions &amp; theory · Schematic teaching model',f'§{n} · Definitions &amp; theory · Schematic')
        (ROOT/mobile).write_text(stacked)
        # Insert immediately after the concept paragraph; both definitions and theory
        # remain next to the diagram, without changing existing lesson text.
        start=html.index(f'<details class="lesson" id="{s["id"]}"')
        match=re.search(r'<p class="concept">.*?</p>',html[start:],re.S);assert match
        end=start+match.end()
        fig=f'''\n<!-- BEGIN textbook visual {n} -->
<figure class="lesson-visual" id="visual-{stem}"><a href="{src}" target="_blank" rel="noopener" aria-label="Open full-size diagram for section {n}"><picture><source media="(max-width: 760px)" srcset="{mobile}" width="500" height="960"><img src="{src}" width="1000" height="500" loading="lazy" decoding="async" alt="{escape(v['alt'],quote=True)}"></picture></a><figcaption><strong>See the definitions and theory.</strong> {escape(v['caption'])}<span class="visual-links"><a href="{src}" target="_blank" rel="noopener">Open full-size diagram ↗</a><a href="output/pdf/Chemistry12-navigable.pdf#page={s['pdfPage']}" target="_blank" rel="noopener">Textbook §{n} · p. {s['page']} onward ↗</a></span></figcaption></figure>
<!-- END textbook visual -->'''
        html=html[:end]+fig+html[end:]
        manifest.append({k:v[k] for k in ['section','left','right','caption','alt']}|dict(image=src,mobileImage=mobile,sourcePdf='Chemistry12.pdf',printedPage=s['page'],pdfPage=s['pdfPage']))
    html=html.replace('</style>',CSS+'\n</style>',1);target.write_text(html)
    (ROOT/'content/chemistry12/tutorial-visuals.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
    print(f'Built {len(VISUALS)} labelled teaching diagrams and updated tutorial.html.')

if __name__=='__main__':main()
