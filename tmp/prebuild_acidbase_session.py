import sys, math
sys.path.insert(0,'tools')
from save_chemistry12_session_answers import save
log=lambda x:-math.log10(x)
f=lambda x:format(x,'.4g')
def row(n,answer,s1,s2,check='Check the concentration product [H₃O⁺][OH⁻]=Kw and conserve acid/base equivalents.',notes=None):
    return [n,answer,[s1,s2],check,notes or [],False]
a=[]
a.append(row(1,'2NH₃(l)⇌NH₄⁺+NH₂⁻.','One ammonia molecule donates H⁺ to a second ammonia molecule.','The donor becomes NH₂⁻ and the acceptor becomes NH₄⁺.','The nitrogen/hydrogen inventories and total charge balance.'))
vals=[('OH',6.0),('H',3.2e-4),('OH',9.2e-12),('H',2.5),('OH',4.7e-5)]
rs=[]
for k,v in vals:
    h=v if k=='H' else 1e-14/v;o=1e-14/h
    rs.append(f'[H₃O⁺]={f(h)} M; [OH⁻]={f(o)} M; '+('acidic' if h>o else 'basic' if h<o else 'neutral'))
a.append(row(2,'Rows top to bottom: '+ '; '.join(rs)+'.','At 25°C, the missing ion concentration is 1.0×10⁻¹⁴ divided by the supplied ion concentration.','Compare H₃O⁺ and OH⁻ to classify the solution. Use two significant figures for the supplied two-significant-figure values.'))
a.append(row(3,'2H₂O(l)+57.1 kJ⇌H₃O⁺(aq)+OH⁻(aq). Kw increases as temperature increases.','Water autoionization is endothermic, so the energy term belongs on the reactant side.','Heating favours ion formation; at a given new temperature the product [H₃O⁺][OH⁻] is larger.','Neutral water still has equal hydronium and hydroxide concentrations at each temperature.'))
a.append(row(4,'[H₃O⁺]=0.20 M; [OH⁻]=5.0×10⁻¹⁵ M at 1°C.','HI is fully ionized, so the hydronium concentration is approximately the 0.20 M formal acid concentration.','Use the stated low-temperature Kw=1.0×10⁻¹⁵: [OH⁻]=Kw/0.20=5.0×10⁻¹⁵ M.'))
a.append(row(5,'[OH⁻]=1.6×10⁻⁸ M; the sample is acidic.','[OH⁻]=1.0×10⁻¹⁴/(6.3×10⁻⁷)=1.587×10⁻⁸ M.','Hydronium exceeds hydroxide at 25°C, so the solution is acidic.'))
a.append(row(6,'Assuming pure water: at 50°C, [H₃O⁺]=[OH⁻]=2.3×10⁻⁷ M, neutral. At 100°C, both are 7.1×10⁻⁷ M, neutral.','For neutral water, set both concentrations equal to x, so x²=Kw.','Take √(5.5×10⁻¹⁴) and √(5.1×10⁻¹³), respectively.','A neutral pH need not equal 7 outside 25°C.',['The table supplies Kw alone; equality of ion concentrations requires the intended pure-water/neutral-water assumption.']))
a.append(row(7,'Kw(D₂O,50°C)=7.9×10⁻¹⁵.','For pure heavy water, 2D₂O⇌D₃O⁺+OD⁻, so [D₃O⁺]=[OD⁻].','Kw=(8.9×10⁻⁸)²=7.921×10⁻¹⁵.','The quoted hydroxide concentration is for pure heavy water.'))
s=(4.7e-6/4)**(1/3);o=2*s
a.append(row(8,f'[OH⁻]={f(o)} M; [H₃O⁺]={f(1e-14/o)} M.', 'Ca(OH)₂(s)⇌Ca²⁺+2OH⁻ gives Ksp=s(2s)²=4s³.','s=(4.7×10⁻⁶/4)^(1/3)='+f(s)+' M, so [OH⁻]=2s and [H₃O⁺]=Kw/(2s).'))
h=(.020*.80+.010*.60-.015*1.2)/.045
a.append(row(9,f'[H₃O⁺]≈{f(h)} M and [OH⁻]≈{f(1e-14/h)} M.','Reading the cylinders as 20 mL HCl, 15 mL NaOH and 10 mL HI gives acid moles 0.016+0.006=0.022 and base moles 0.018.','Neutralization leaves 0.0040 mol H⁺ in 0.045 L, giving 0.0889 M; then divide Kw by this concentration.','The net acid excess is positive.',['Cylinder volumes are approximate graphical readings: 20,15,10 mL; use the same calculation if a more precise reading is specified.']))
m=(.150*.250+.150*.010)/2*121.63
a.append(row(10,f'Add {f(m)} g Sr(OH)₂ (about 2.37 g).','Initial acid moles=0.150×0.250=0.0375 mol; desired excess OH⁻=0.150×0.010=0.00150 mol.','Total OH⁻ needed=0.0390 mol; divide by 2 OH⁻ per Sr(OH)₂ and multiply by 121.63 g/mol.','Added hydroxide equivalents minus acid equivalents give the target excess.',['Assume negligible volume change and anhydrous Sr(OH)₂.']))
save({'section':'4.3','answers':a})

a=[]
a.append(row(1,'pH=−log₁₀[H₃O⁺]; pOH=−log₁₀[OH⁻], using concentrations in mol/L in the dilute-solution approximation.','The negative logarithm expresses many orders of magnitude on a compact scale.','Lower pH means higher hydronium; lower pOH means higher hydroxide.','For thermodynamic accuracy use dimensionless activities rather than bare dimensional concentrations.'))
a.append(row(2,'The logarithmic scales turn extremely small and widely varying concentrations into manageable numbers; a one-unit change corresponds to a tenfold concentration change.','Hydronium and hydroxide span many powers of ten across aqueous solutions.','For example, [H₃O⁺]=10⁻³ M gives pH 3, while 10⁻⁴ M gives pH 4.','A smaller pH represents a larger, not smaller, hydronium concentration.'))
a.append(row(3,'Rows ([H₃O⁺],pH,type): (3.50×10⁻⁶ M,5.456,acidic); (3.1×10⁻¹² M,11.51,basic); (0.00550 M,2.260,acidic); (1.0 M,0.00,acidic); (6.8×10⁻⁹ M,8.17,basic).','Use pH=−log[H₃O⁺] for concentration-given rows and [H₃O⁺]=10^(−pH) for pH-given rows.','The number of decimal places in a logarithmic pH equals the significant figures in its concentration.'))
a.append(row(4,'Rows ([OH⁻],pOH,type): (7.2×10⁻⁹ M,8.14,acidic); (2.8×10⁻¹⁰ M,9.55,acidic); (4.88×10⁻⁴ M,3.312,basic); (1.0×10⁻¹⁴ M,14.00,acidic); (0.000625 M,3.204,basic).','Use pOH=−log[OH⁻] or [OH⁻]=10^(−pOH).','At 25°C pOH above 7 indicates an acidic solution and pOH below 7 a basic one.'))
a.append(row(5,'(a) Basic. (b) Acidic. (c) Product. (d) Sum.','Decreasing pOH raises [OH⁻] and lowers [H₃O⁺]; decreasing pH does the reverse.','[H₃O⁺][OH⁻]=Kw implies pH+pOH=pKw after taking negative logarithms.'))
a.append(row(6,'Rows ([H₃O⁺],pOH,type): (0.0342 M,12.534,acidic); (2.512×10⁻⁶ M,8.400,acidic); (7.2×10⁻¹² M,2.86,basic); (1.641×10⁻¹¹ M,3.215,basic).','Convert by pH+pOH=14.000 at 25°C.','For pOH-given rows, [H₃O⁺]=10^(pOH−14); for concentration-given rows, pOH=14+log[H₃O⁺].'))
a.append(row(7,'pH=6.51; the pure water is neutral at 60°C.','Neutral water has equal hydronium and hydroxide activities, so pH=pOH.','pH=pKw/2=13.02/2=6.51.','A pH below 7 does not imply acidity when the neutral reference changes with temperature.'))
a.append(row(8,'pH=13.78.','Sr(OH)₂ supplies 2OH⁻ per formula unit, so [OH⁻]=2×0.30=0.60 M.','pOH=−log(0.60)=0.22 and pH=14.00−0.22=13.78.'))
a.append(row(9,'pH=13.000 (about 13.00).','Moles NaOH=2.00/40.00=0.0500 mol; [OH⁻]=0.0500/0.5000=0.100 M.','pOH=1.000 and pH=14.000−1.000=13.000.'))
a.append(row(10,'Mass HI≈0.81 g.','[H₃O⁺]=10⁻²·⁵⁰=0.003162 M; for strong HI its formal concentration is the same.','n=0.003162×2.0=0.006325 mol; mass=n×127.91≈0.809 g.'))
hs=[5.620e-5,1e-14/.000450,10**(-1.50),10**(-10.5)]
rs=[]
for h in hs:rs.append(f'({f(h)} M,{f(1e-14/h)} M,{14-log(h):.4f},{log(h):.4f},'+('acidic' if h>1e-7 else 'basic')+')')
a.append(row(11,'Top-to-bottom rows in order ([H₃O⁺],[OH⁻],pOH,pH,type): '+ '; '.join(rs)+'.','Use Kw=1.0×10⁻¹⁴ and pH+pOH=14.00 to fill each row.','For reporting, retain 4 pH decimals for 5.620×10⁻⁵ M; 3 for 0.000450 M; 2 for the pOH=12.50 row; and 1 for the pH=10.5 row.'))
h=(.075*.50-.20/40)/.200
a.append(row(12,f'pH={log(h):.3f} (about 0.79).','HNO₃ supplies 0.0750×0.50=0.0375 mol H⁺; NaOH supplies 0.20/40.00=0.0050 mol OH⁻.','Excess H⁺=0.0325 mol in 0.2000 L, so [H₃O⁺]=0.1625 M and pH=−log(0.1625).'))
o=(.300*10**(-1.5)-.200*10**(-1.5))/.500
a.append(row(13,f'pH={14-log(o):.3f} (about 11.80).','The acid and base concentrations both equal 10⁻¹·⁵⁰=0.03162 M, but the base occupies the greater volume.','OH⁻ excess=(0.300−0.200)×0.03162=0.003162 mol; divide by 0.500 L and compute pH=14+log[OH⁻].'))
o=(.500*.1-3.2/127.91)/.500
a.append(row(14,f'pH≈{14-log(o):.2f}.','Initial pH 13.00 gives [OH⁻]=0.100 M, or 0.0500 mol in 0.500 L.','HI consumes 3.2/127.91≈0.0250 mol OH⁻, leaving approximately 0.0500 M OH⁻.'))
o=(.040*.30-.025*.20-.035*.15)/.100
a.append(row(15,f'pH≈{14-log(o):.2f}.','Total acid equivalents=0.0250×0.20+0.0350×0.15=0.01025 mol; base equivalents=0.0400×0.30=0.0120 mol.','Excess OH⁻=0.00175 mol in 0.1000 L, giving 0.0175 M and pH=14+log(0.0175).'))
target=10**(11.750-14);m=(.450*.0350-.450*target)*36.46
a.append(row(16,f'Mass HCl={f(m)} g (approximately 0.482 g).','Target [OH⁻]=10^(11.750−14)=0.005623 M; target excess moles=0.4500×0.005623.','Subtract that from the initial 0.4500×0.0350 mol OH⁻; the difference is HCl moles. Multiply by 36.46 g/mol.'))
m=(.500*.0125-.500*10**(-2.75))*23.95
a.append(row(17,f'Mass LiOH={f(m)} g (approximately 0.128 g).','Initial acid moles=0.5000×0.0125=0.006250 mol. Target remaining acid moles=0.5000×10⁻²·⁷⁵.','LiOH neutralizes the difference 1:1; multiply its required moles by 23.95 g/mol.'))
save({'section':'4.4','answers':a})

a=[]
def weak(c,k):return 2*k*c/(math.sqrt(k*k+4*k*c)+k)
c=23/46.03/.5;h=weak(c,1.8e-4)
a.append(row(1,f'[H₃O⁺]={f(h)} M; [OH⁻]={f(1e-14/h)} M; pH={log(h):.3f}; pOH={14-log(h):.3f}.',f'Formal HCOOH concentration=(23.0/46.03)/0.5000={f(c)} M.','Set Ka=x²/(C−x)=1.8×10⁻⁴ and solve the positive root for x=[H₃O⁺]; obtain the other quantities from Kw and logarithms.'))
c=5.6/22.4/2.5;h=weak(c,9.1e-8)
a.append(row(2,f'pH={log(h):.2f}; percent ionization≈{f(h/c*100)}%.','H₂S concentration=(5.6/22.4)/2.50=0.100 M.','For the first ionization Ka=9.1×10⁻⁸, solve x²/(0.100−x)=Ka. Then pH=−log x and %ionization=100x/0.100.','The later ionization of HS⁻ is negligible for this acidic solution.'))
h=.100*.0134;k=h*h/(.100-h)
a.append(row(3,f'pH={log(h):.3f}; Ka≈{f(k)}, identifying acetic (ethanoic) acid.','Ionization fraction 1.34%=0.0134 gives [H₃O⁺]=0.100×0.0134=0.00134 M.','Ka=x²/(0.100−x)=1.82×10⁻⁵, matching the table value 1.8×10⁻⁵.'))
h=.01;c=h+h*h/3.5e-4;m=c*1.5*20.01
a.append(row(4,f'Approximately {f(m)} g HF (8.9 g).','pH 2.00 fixes [H₃O⁺]=0.0100 M. From Ka=x²/(C−x), C=x+x²/Ka=0.2957 M.','Mass=C×1.5 L×20.01 g/mol; include the dissociated x term rather than assuming it is negligible.'))
h=10**(-1.5);c=h+h*h/7.5e-3
a.append(row(5,f'Formal [H₃PO₄]≈{f(c)} M (0.165 M).','pOH 12.50 gives pH 1.50 and x=0.03162 M hydronium.','Using the dominant first dissociation Ka=7.5×10⁻³, C=x+x²/Ka=0.16496 M.','The second dissociation is suppressed strongly at this hydronium concentration.'))
h=10**(-2.35);c=h+h*h/.059;m=c*.250*90.04
a.append(row(6,f'About {f(m)} g anhydrous oxalic acid (0.108 g).','The pH gives x=10⁻²·³⁵=0.004467 M. Use first Ka=5.9×10⁻² to recover C=x+x²/Ka≈0.004805 M.','Multiply C by 0.2500 L and 90.04 g/mol.','The approximation neglects the relatively small second ionization.',['Use anhydrous H₂C₂O₄ for this question, not the dihydrate used in standardization exercises.']))
for n,c,pH in [(7,.020,4.62),(8,.100,14-11.34)]:
 h=10**(-pH);k=h*h/(c-h)
 a.append(row(n,f'Ka≈{f(k)}.',f'pH={pH:.2f} gives [H₃O⁺]=x={f(h)} M.',f'For the monoprotic acid, equilibrium acid concentration is {c}−x; Ka=x²/({c}−x).'))
def constrow(acid,base,ka):
 return f'{acid}/{base}: Ka={f(ka)}, pKa={log(ka):.2f}, Kb={f(1e-14/ka)}, pKb={14-log(ka):.2f}'
r=[constrow(*v) for v in [('HNO₂','NO₂⁻',4.6e-4),('H₂O₂','HO₂⁻',2.4e-12),('C₆H₅OH','C₆H₅O⁻',1.3e-10),('HSO₄⁻','SO₄²⁻',1.2e-2)]]
a.append(row(9,'Rows top to bottom: '+'; '.join(r)+'.','Obtain the conjugate acid/base formula by adding/removing one proton and read the acid Ka from Table A5.','Use pKa=−log Ka, Kb=Kw/Ka, pKb=14−pKa.','KaKb=1.0×10⁻¹⁴ for every listed conjugate pair.'))
r=[constrow(*v) for v in [('H₂PO₄⁻','HPO₄²⁻',6.2e-8),('H₂C₆H₅O₇⁻','HC₆H₅O₇²⁻',1.7e-5),('H₃BO₃','H₂BO₃⁻',7.3e-10),('HCO₃⁻','CO₃²⁻',5.6e-11)]]
a.append(row(10,'Rows top to bottom: '+'; '.join(r)+'.','For amphiprotic ions, use the Ka of the acid actually printed in the conjugate pair, not a later dissociation constant.','Calculate Kb=Kw/Ka for its paired conjugate base, then take negative logarithms.','Each pair must differ by exactly one H⁺.'))
c=5.6/22.4/.750;k=1e-14/5.6e-10;o=weak(c,k)
a.append(row(11,f'pH≈{14-log(o):.2f}.','[NH₃]₀=(5.6/22.4)/0.7500=0.3333 M; Kb=Kw/Ka(NH₄⁺)≈1.79×10⁻⁵.','Solve x²/(0.3333−x)=Kb for OH⁻, then pOH=−log x and pH=14−pOH.'))
o=weak(.60,4.7e-4)
a.append(row(12,f'pOH={log(o):.2f}; pH={14-log(o):.2f}.','Isopropylamine+H₂O⇌isopropylammonium+OH⁻, with Kb=4.7×10⁻⁴.','Solve x²/(0.60−x)=Kb to obtain [OH⁻]='+f(o)+' M; then take logarithms.'))
o=1e-4;k=1e-14/1e-7;c=o+o*o/k
a.append(row(13,f'Initial [SO₃²⁻]≈{f(c)} M (0.10 M).','pH 10.00 gives pOH 4.00 and x=[OH⁻]=1.0×10⁻⁴ M. Kb(SO₃²⁻)=Kw/Ka(HSO₃⁻)=1.0×10⁻⁷.','Rearrange Kb=x²/(C−x) to C=x+x²/Kb=0.1001 M.'))
o=10**(-2.5);c=o+o*o/6.3e-5;v=c*2.5*22.4
a.append(row(14,f'Gas volume at STP≈{f(v)} L (9.1 L).','pOH=2.50 fixes x=[OH⁻]=0.003162 M; initial amine C=x+x²/(6.3×10⁻⁵)=0.16189 M.','Moles=C×2.5 L and gas volume=n×22.4 L/mol.'))
o=10**(-2.14);k=o*o/(.10-o)
a.append(row(15,f'Kb≈{f(k)} (5.7×10⁻⁴).','[OH⁻]=10⁻²·¹⁴='+f(o)+' M; the conjugate-acid concentration is the same.','Equilibrium free ethylamine is 0.10−x, so Kb=x²/(0.10−x).'))
save({'section':'4.5','answers':a})
