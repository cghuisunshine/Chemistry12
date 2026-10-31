import sys,math
sys.path.insert(0,'tools')
from save_chemistry12_session_answers import save
L=lambda x:-math.log10(x)
F=lambda x:format(x,'.4g')
def weak(c,k):return 2*k*c/(math.sqrt(k*k+4*k*c)+k)
def r(n,answer,s1,s2,check='Substitute the equilibrium values back into the mass-action expression and check the mole balance.',notes=None):
 return [n,answer,[s1,s2],check,notes or [],False]
a=[]
c=.050*.50/.100;k=1e-14/1.8e-5;o=weak(c,k)
a.append(r(3,f'(a) KOH+CH₃COOH→KCH₃COO+H₂O. (b) [KCH₃COO]=0.250 M. (c) pH≈{14-L(o):.2f}.','Each reactant supplies 0.0500 L×0.50 M=0.0250 mol, so both neutralize completely and form 0.0250 mol salt in 0.1000 L.','CH₃COO⁻+H₂O⇌CH₃COOH+OH⁻; Kb=Kw/Ka=5.56×10⁻¹⁰. Solve x²/(0.250−x)=Kb for OH⁻.'))
c=25.2/126.04/.500;o=weak(c,1e-7)
a.append(r(4,f'pH≈{14-L(o):.2f}.',f'[Na₂SO₃]=(25.2/126.04)/0.5000={F(c)} M; SO₃²⁻+H₂O⇌HSO₃⁻+OH⁻.','Kb=Kw/Ka(HSO₃⁻)=1.0×10⁻⁷. Solve x²/(C−x)=Kb, yielding [OH⁻]≈'+F(o)+' M.'))
h=1e-5;c=h+h*h/1e-8;m=c*.250*170.48
a.append(r(5,f'Mass CuCl₂·2H₂O≈{F(m)} g (0.43 g).','pH5.00 requires x=[H₃O⁺]=1.0×10⁻⁵ M. With the supplied hydrated-Cu²⁺ Ka=1.0×10⁻⁸, initial C=x+x²/Ka=0.01001 M.','One CuCl₂·2H₂O supplies one hydrated Cu²⁺; mass=C×0.2500×170.48 g/mol.'))
o=10**(-4.5);k=1e-14/4.9e-10;c=o+o*o/k;m=c*.300*49.01
a.append(r(6,f'Mass NaCN≈{F(m)} g (1.2 mg).','pH9.50 gives [OH⁻]=10⁻⁴·⁵⁰=3.162×10⁻⁵ M; Kb(CN⁻)=Kw/Ka(HCN)=2.04×10⁻⁵.','C=x+x²/Kb≈8.06×10⁻⁵ M; multiply by 0.3000 L and 49.01 g/mol.','The ionization is appreciable, so neglecting x compared with C is invalid.'))
c=470/117.49/5;h=weak(c,5.6e-10)
a.append(r(7,f'pH≈{L(h):.2f}.','[NH₄ClO₄]=(470/117.49)/5.0≈0.800 M. ClO₄⁻ is a spectator; NH₄⁺ is the acidic ion.','NH₄⁺+H₂O⇌NH₃+H₃O⁺ with Ka=5.6×10⁻¹⁰ gives [H₃O⁺]≈'+F(h)+' M.'))
o=10**(-5.5);k=1e-14/4.6e-4;c=o+o*o/k;m=c*.350*85.10
a.append(r(9,f'(a) Approximately {F(m)} g KNO₂ (14 g to two significant figures). (b) pH generally increases as water is removed, before solubility/other non-ideal limits intervene.','pH8.50 gives [OH⁻]=10⁻⁵·⁵⁰; Kb(NO₂⁻)=Kw/(4.6×10⁻⁴)=2.17×10⁻¹¹. Recover C=x+x²/Kb≈0.460 M and multiply by 0.3500 L and 85.10 g/mol.','Evaporation increases formal nitrite concentration. For a weak base [OH⁻]≈√(KbC), so absolute hydroxide concentration and pH rise even though percent hydrolysis falls.'))
k=1e-14/1.7e-6;h=weak(.500,k)
a.append(r(10,f'pH≈{L(h):.2f}.','N₂H₅Cl dissociates to N₂H₅⁺ and spectator Cl⁻. Ka(N₂H₅⁺)=Kw/Kb(N₂H₄)=5.88×10⁻⁹.','Set Ka=x²/(0.500−x); its positive root gives [H₃O⁺]≈'+F(h)+' M.'))
save({'section':'5.1','answers':a})
a=[]
c=(.835/204.22)/.02524
a.append(r(5,f'[NaOH]={c:.4f} M (0.162 M).','KHP is monoprotic, so n(NaOH)=n(KHP)=0.835/204.22=0.004089 mol.','Divide by the titrant volume 0.02524 L.','KHP supplies one titratable proton per formula unit.'))
m=.02156*.125/2*126.07
a.append(r(6,f'Mass H₂C₂O₄·2H₂O={F(m)} g (0.170 g).','NaOH moles=0.02156×0.125=0.002695 mol. Oxalic acid is diprotic, so acid moles are half that.','Multiply 0.0013475 mol by the dihydrate molar mass 126.07 g/mol.','Use the hydrate molar mass and two base equivalents per acid molecule.'))
v=2*.025*.156/10**(-.560)
a.append(r(7,f'Volume NaOH≈{F(v*1000)} mL (28.3 mL).','pH13.440 gives pOH0.560 and [OH⁻]=10⁻⁰·⁵⁶⁰=0.2754 M.','The diprotic acid supplies 2×0.0250×0.156=0.00780 mol acid equivalents; divide by 0.2754 M.','A diprotic acid requires two moles NaOH per mole acid.'))
v=(4.48/22.4/.400)*.025/2/.227
a.append(r(8,f'Volume Sr(OH)₂≈{F(v*1000)} mL (27.5 mL).','HCl moles in stock=4.48/22.4=0.200 mol; stock concentration=0.200/0.4000=0.500 M. The 25.0 mL aliquot contains 0.01250 mol HCl.','Each Sr(OH)₂ supplies two OH⁻; required base moles=0.006250, and volume=0.006250/0.227 L.','Neutralization is HCl:Sr(OH)₂=2:1.'))
M=.665/(.02651*.2055)
a.append(r(9,f'Molar mass HA={F(M)} g/mol (122.1 g/mol).','n(KOH)=0.02651×0.2055=0.005448 mol; the monoprotic acid has the same mole amount.','M=sample mass/acid moles=0.665/0.005448.','Do not use a factor of two for a monoprotic acid.'))
M=5.47/(.0236*.2231*10)
a.append(r(10,f'Molar mass diprotic acid≈{F(M)} g/mol (104 g/mol).','Sr(OH)₂ and the diprotic acid supply two base/acid equivalents respectively, so their molecular mole ratio is 1:1. The aliquot has 0.0236×0.2231 mol acid.','The stock flask contains ten aliquots; divide 5.47 g by ten times the aliquot mole amount.','The factor of two for the acid cancels the factor of two for Sr(OH)₂.'))
pct=.04031*.223/2*10*150.09/7.36*100
a.append(r(11,f'Percent tartaric-acid purity≈{pct:.1f}%.','NaOH moles in the aliquot titration=0.04031×0.223. Divide by 2 for diprotic tartaric acid and multiply by10 for the complete stock.','Multiply acid moles by150.09 g/mol, then divide by the 7.36 g impure sample and multiply by100.','Assume the impurities do not consume titrant.'))
pct=.02734*.178*112.13/.570*100
a.append(r(12,f'Percent sorbic-acid purity≈{pct:.1f}%.','Sorbic acid is monoprotic, so its moles equal 0.02734×0.178=0.0048665 mol KOH.','Pure acid mass=n×112.13≈0.5457 g; divide by0.570 g and multiply by100.','The entire 25.00 mL sample is titrated, so no aliquot scaling factor is needed.'))
pct=.03107*.105*2*136.15/.992*100
a.append(r(13,f'Percent phenylacetic-acid purity≈{pct:.1f}% using C₈H₈O₂ (136.15 g/mol).','Sr(OH)₂ moles=0.03107×0.105; multiply by2 to obtain monoprotic acid moles.','Mass pure phenylacetic acid=n×136.15; divide by0.992 g and multiply by100.','The two OH⁻ groups per base formula unit must both be counted.',['The printed condensed formula is faint; the answer uses the stated identity phenylacetic acid, C₆H₅CH₂COOH.']))
save({'section':'5.3','answers':a})
n=.0200*.250;v=n/.200;c=n/(.0200+v);k=1e-14/1.8e-4;o=weak(c,k)
save({'section':'5.4','answers':[r(11,f'(a) pH={L(1.8e-4):.3f}. (b) NaOH volume={v*1000:.1f} mL. (c) Equivalence pH≈{14-L(o):.2f}.','HCOOH moles=0.0200×0.250=0.00500. Half-equivalence has equal formic acid/formate, hence pH=pKa; equivalence requires 0.00500/0.200=0.0250 L NaOH.','At equivalence [HCOO⁻]=0.00500/0.0450=0.1111 M. Use Kb=Kw/Ka=5.56×10⁻¹¹ in x²/(0.1111−x)=Kb, then pH=14+log x.')]})
