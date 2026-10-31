"""Offline content, conservation and rebuild-protection checks."""
import copy
import json
import math
import re
from unittest.mock import patch
from chemistry12_prebuilt import ROOT, fingerprint, read_answers, source_questions, valid
from build_chemistry12_practice import build

inventory=json.loads((ROOT/'content/chemistry12/practice-problems.json').read_text())
data=read_answers()
questions=list(source_questions(inventory))
assert len(questions)==len(data['answers'])==373
for q in questions:
    a=data['answers'][q['id']]
    assert valid(a,fingerprint(q)),q['id']
    assert a['provenance']=='prebuilt-ai'
    assert 'no external endpoint' in a['generatedBy']
    assert not re.search(r'answer unavailable|ask your teacher to solve|cannot view the image',a['answer'],re.I)

# Independent numerical residuals for selected multistep source calculations.
assert abs((.60-.05986264091734046)*(.60-3*.05986264091734046)**3/(2*.05986264091734046)**2-2.8)<1e-10
assert abs((12**2)/(4*9)-4)<1e-12
assert abs((.005/.045)*(1e-14/1.8e-4)-(10**(8.395-14))**2)<1e-14
assert 'higher, higher' in data['answers']['chem12-s5-4-q8']['answer']
assert 'lower, lower' in data['answers']['chem12-s5-4-q8']['answer']
assert data['answers']['chem12-s5-4-q6']['needsReview'], 'The printed colour contradiction must remain visible'
collision=next(q for q in questions if q['id']=='chem12-s1-3-q7')
collision_answer=data['answers'][collision['id']]
assert 'ClNO₂' in collision['text'] and 'ClNO₂' in collision_answer['answer']
assert 'Cl + ClNO₂ → Cl₂ + NO₂' in collision_answer['answer']
assert 'NOCl' not in collision_answer['answer']
assert collision['images'][0]['src'].endswith('s1-3-q7-redrawn.png')
for diagram in collision_answer['solutionImages']:
    assert (ROOT/diagram['src']).exists()
    assert (ROOT/(diagram['src']+'.js')).exists()

def atoms(formula):
    tokens=re.findall(r'[A-Z][a-z]?|\d+|[()]',formula)
    stack=[{}];i=0
    while i<len(tokens):
        token=tokens[i]
        if token=='(':
            stack.append({});i+=1
        elif token==')':
            group=stack.pop();i+=1
            multiplier=int(tokens[i]) if i<len(tokens) and tokens[i].isdigit() else 1
            if i<len(tokens) and tokens[i].isdigit():i+=1
            for e,n in group.items():stack[-1][e]=stack[-1].get(e,0)+multiplier*n
        else:
            i+=1;count=int(tokens[i]) if i<len(tokens) and tokens[i].isdigit() else 1
            if i<len(tokens) and tokens[i].isdigit():i+=1
            stack[-1][token]=stack[-1].get(token,0)+count
    assert len(stack)==1
    return stack[0]

def total(side):
    out={'charge':0}
    for coefficient,formula,charge in side:
        out['charge']+=coefficient*charge
        for e,n in atoms(formula).items():out[e]=out.get(e,0)+coefficient*n
    return {e:n for e,n in out.items() if n}

# Atom/charge verification for the difficult authored balances, including
# disproportionation and simultaneous oxidation of more than one element.
equations=[
 ([(3,'Sn',2),(2,'MnO4',-1),(4,'H2O',0)],[(3,'Sn',4),(2,'MnO2',0),(8,'OH',-1)]),
 ([(4,'V',2),(2,'H2SO3',0),(2,'H',1)],[(4,'V',3),(1,'S2O3',-2),(3,'H2O',0)]),
 ([(1,'IO3',-1),(5,'I',-1),(3,'H2O',0)],[(3,'I2',0),(6,'OH',-1)]),
 ([(4,'ClO3',-1),(3,'N2H4',0)],[(6,'NO',0),(4,'Cl',-1),(6,'H2O',0)]),
 ([(2,'NO3',-1),(3,'Zn',0),(4,'H2O',0)],[(3,'Zn',2),(2,'NO',0),(8,'OH',-1)]),
 ([(11,'ClO3',-1),(2,'H',1)],[(8,'ClO4',-1),(1,'Cl',-1),(1,'Cl2',0),(1,'H2O',0)]),
 ([(3,'SnS3O3',0),(16,'MnO4',-1),(5,'H2O',0)],[(16,'MnO2',0),(9,'SO4',-2),(3,'Sn',4),(10,'OH',-1)]),
 ([(2,'Mg3(AsO4)2',0),(6,'SiO2',0),(10,'C',0)],[(1,'As4',0),(6,'MgSiO3',0),(10,'CO',0)]),
 ([(1,'SeO3',-2),(4,'F',-1),(6,'H',1)],[(1,'Se',0),(2,'F2',0),(3,'H2O',0)]),
 ([(4,'ReO4',-1),(3,'Sb2O3',0),(2,'H2O',0)],[(4,'ReO2',0),(3,'Sb2O5',0),(4,'OH',-1)]),
 ([(3,'Pd',0),(4,'NO3',-1),(18,'I',-1),(16,'H',1)],[(3,'PdI6',-2),(4,'NO',0),(8,'H2O',0)]),
 ([(1,'Pb(OH)4',-2),(1,'BrO',-1)],[(1,'PbO2',0),(1,'Br',-1),(1,'H2O',0),(2,'OH',-1)]),
 ([(2,'K2Cr2O7',0),(3,'C2H6O',0),(16,'HCl',0)],[(3,'C2H4O2',0),(4,'KCl',0),(4,'CrCl3',0),(11,'H2O',0)]),
 ([(4,'NaCl',0),(2,'H2SO4',0),(1,'MnO2',0)],[(2,'Na2SO4',0),(1,'MnCl2',0),(2,'H2O',0),(1,'Cl2',0)]),
 ([(1,'C2H6O',0),(2,'Cr2O7',-2),(16,'H',1)],[(2,'CO2',0),(4,'Cr',3),(11,'H2O',0)]),
]
for i,(left,right) in enumerate(equations):assert total(left)==total(right),(i,total(left),total(right))

# A missing or stale answer must not replace the last complete production page.
before=(ROOT/'chemistry12-practice.html').read_bytes()
for mode in ['missing','stale']:
    incomplete=copy.deepcopy(data)
    if mode=='missing':incomplete['answers'].pop(questions[0]['id'])
    else:incomplete['answers'][questions[0]['id']]['sourceHash']='outdated'
    with patch('build_chemistry12_practice.read_answers',return_value=incomplete):
        try:build()
        except ValueError:pass
        else:raise AssertionError('Incomplete key was accepted')
    assert (ROOT/'chemistry12-practice.html').read_bytes()==before
print(json.dumps(dict(status='PASS',completeSolutions=373,balancedDifficultRedoxEquations=len(equations),checks=['image-byte source fingerprints','complete answer/steps/check fields','numerical equilibrium residuals','labelled source contradictions','missing/stale key blocks rebuild without changing page'])))
