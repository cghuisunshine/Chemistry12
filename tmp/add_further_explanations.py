"""Add source-linked physical chemistry explanations without rebuilding the page."""
from pathlib import Path
from html import escape
import re

ROOT = Path(__file__).resolve().parents[1]
notes = {}

def add(number, title, intuition, steps, equation, check, scope, refs):
    notes[number] = (title, intuition, steps, equation, check, scope, refs)

add('1.1', 'Why divide a concentration slope by a coefficient?',
    'A balanced equation counts reaction events. One event of 2A → B removes two A particles for every B particle formed. The two concentration slopes therefore describe the same chemistry on different counting scales.',
    ['Introduce the extent ξ (xi): an increase of 1 mol in ξ consumes 2 mol A and forms 1 mol B. Thus n(A) = n(A)₀ − 2ξ and n(B) = n(B)₀ + ξ.',
     'At constant solution volume V, divide by V: [A] = [A]₀ − 2ξ/V and [B] = [B]₀ + ξ/V.',
     'Differentiate with respect to time. Both −½ d[A]/dt and d[B]/dt equal (1/V)dξ/dt. This common quantity is the normalized reaction rate r.',
     'For a measured interval, replace derivatives by finite changes to obtain an average rate. A tangent gives the instantaneous value.'],
    'r = (1/V)dξ/dt = −½ d[A]/dt = d[B]/dt',
    'If A disappears at 0.030 M s⁻¹, B forms at 0.015 M s⁻¹. Dividing the A slope by 2 makes the two descriptions agree.',
    'Constant volume is essential for this concentration form: dilution can change [A] without consuming A.',
    [(794, 795, '§22.2, rates and reaction extent')])

add('1.2', 'Which part of the rate does each factor change?',
    'Separate how often particles meet from how likely each encounter is to succeed. Concentration changes encounter frequency; temperature changes motion and success probability; a catalyst changes the available pathway.',
    ['For an elementary A + B reaction in a well-mixed dilute system, the encounter rate per volume scales with [A][B]. Doubling both concentrations gives four times as many encounters per volume per time at the same temperature.',
     'For a solid reacting at its surface, let j be the amount reacting per area per time. Then the amount rate is jS, where S is exposed surface area. Crushing increases S, but j may also depend on transport and surface condition.',
     'At fixed concentrations, the rate ratio equals the rate-constant ratio. In the Arrhenius model, divide k₂ = A exp(−Eₐ/RT₂) by k₁ = A exp(−Eₐ/RT₁); A cancels if it is approximately constant.'],
    'k₂/k₁ = exp[(Eₐ/R)(1/T₁ − 1/T₂)]',
    'For Eₐ = 50.0 kJ mol⁻¹, warming from 298 to 308 K gives k₂/k₁ ≈ 1.93. Another activation energy gives another factor; there is no universal doubling rule.',
    'Use kelvin and Eₐ = 50 000 J mol⁻¹ with R = 8.314 J mol⁻¹ K⁻¹. Surface rate and concentration rate have different units.',
    [(807, 809, '§22.5, temperature dependence'), (870, 871, '§24.1(a), collision frequency')])

add('1.3', 'Where does the Arrhenius exponential come from?',
    'A gas has a distribution of collision energies. Heating changes that distribution, making energetic encounters more common. A barrier therefore acts as an energy filter, rather than a requirement that every particle have the same energy.',
    ['Write a collision-model rate as encounters per volume per time multiplied by the probability of a reactive encounter.',
     'Counting A–B encounters gives a factor [A][B]. Averaging an energy-dependent reactive collision cross-section over the thermal distribution produces an exp(−Eₐ/RT) factor in the simple collision model.',
     'Put collision geometry, relative speed and orientation effects into a prefactor A. Then r = k[A][B], with k ≈ A exp(−Eₐ/RT).',
     'Take a natural logarithm: ln k = ln A − (Eₐ/R)(1/T). A plot against 1/T has slope −Eₐ/R when A and Eₐ are effectively constant.'],
    'k ≈ A exp(−Eₐ/RT)  →  ln k = ln A − Eₐ/(RT)',
    'At 298 K, lowering a model barrier by 10.0 kJ mol⁻¹ at the same A multiplies k by exp[10 000/(8.314 × 298)] ≈ 56.6.',
    'The exponential is a model result for reactive encounters; it is not an exact universal formula for the fraction of all molecules above a chosen energy. Real prefactors can depend on temperature.',
    [(807, 809, '§22.5, Arrhenius parameters'), (871, 874, '§24.1(b–c), energy and orientation requirements')])

add('1.4', 'Why can a downhill reaction still be slow?',
    'The difference between the starting and ending energy levels answers a different question from the height of the intervening barrier. A low product level does not remove the climb needed to reach the transition state.',
    ['On the same simplified energy profile, label reactants Hᵣ, products Hₚ and the transition-state level H‡.',
     'The forward climb is H‡ − Hᵣ; the reverse climb is H‡ − Hₚ. Subtract these expressions and the shared peak cancels.',
     'The result is Hₚ − Hᵣ = ΔH. A catalyst can change the peak or supply a multistep route, but it cannot change the enthalpies of the specified starting and ending states.',
     'For equilibrium direction, add the entropy contribution: ΔᵣG = ΔᵣH − TΔᵣS at the current composition. A negative ΔᵣG indicates a forward tendency; the barrier still controls how quickly change occurs.'],
    '(H‡ − Hᵣ) − (H‡ − Hₚ) = ΔH;  ΔᵣG = ΔᵣH − TΔᵣS',
    'Reactants at 0, products at −40 and a peak at +80 kJ mol⁻¹ give forward and reverse climbs of 80 and 120 kJ mol⁻¹. The energy release is 40 kJ mol⁻¹, although a barrier remains.',
    'The barrier subtraction is exact for the levels on this common enthalpy profile. Experimental Arrhenius activation energies and potential-energy barriers need not be identical in more detailed models.',
    [(95, 96, '§3.5, Gibbs energy'), (809, 809, '§22.5(b), reaction coordinate and activated complex')])

add('1.5', 'How can a mechanism create an unexpected reaction order?',
    'An intermediate links elementary steps. Its concentration may depend on earlier equilibria, so an observed rate law can contain powers that do not resemble the overall balanced equation.',
    ['Consider the model mechanism 2A ⇌ I (fast pre-equilibrium), followed by I + B → P (slow). Adding the steps gives 2A + B → P.',
     'The slow elementary step gives r ≈ k₂[I][B]. The unmeasured intermediate must be eliminated from this expression.',
     'For the fast equilibrium, define the concentration-form constant Kc,pre = [I]/[A]². Rearranging gives [I] = Kc,pre[A]².',
     'Substitute: r ≈ k₂Kc,pre[A]²[B] = kobs[A]²[B]. The measured second order in A now has a mechanistic explanation.'],
    'r ≈ k₂[I][B] ≈ k₂Kc,pre[A]²[B] = kobs[A]²[B]',
    'If Kc,pre has units M⁻¹ and k₂ has units M⁻¹ s⁻¹, kobs has units M⁻² s⁻¹. Multiplying by [A]²[B] gives the required M s⁻¹.',
    'This derivation assumes the first step stays near equilibrium while the slow step drains I. It is a proposed model, not proof of a unique mechanism. Kc,pre here uses the school concentration convention.',
    [(809, 810, '§22.6, elementary steps'), (815, 816, '§22.7(e), pre-equilibria')])

add('2.1', 'How do equal rates connect to minimum Gibbs energy?',
    'Kinetics describes the opposing molecular traffic. Thermodynamics describes the net driving tendency. At equilibrium both descriptions agree: forward and reverse events continue, but there is no preferred net conversion.',
    ['For the elementary model A ⇌ B, write rforward = kf[A] and rreverse = kr[B]. Their difference is d[B]/dt.',
     'At equilibrium the difference vanishes, so [B]/[A] = kf/kr. Equal rates do not require equal concentrations when the two rate constants differ.',
     'The chemical potential μ is the Gibbs-energy change per added mole of a species in the mixture. For A → B, ΔᵣG = μB − μA.',
     'When μA exceeds μB, forward conversion lowers G. At equilibrium μA = μB, so the slope dG/dξ is zero at the stable minimum.'],
    'kf[A]eq = kr[B]eq;  ΔᵣG = μB − μA = 0 at equilibrium',
    'If kf = 4kr, equilibrium has four times as much B as A in this model. Both directions still have equal rates.',
    'The simple rate-constant ratio follows from the stated elementary model. The Gibbs-energy criterion applies generally at fixed temperature and pressure; equilibrium does not mean that total G equals zero.',
    [(200, 203, '§§7.1–7.2, equilibrium and Gibbs energy'), (804, 805, '§22.4, reactions approaching equilibrium')])

add('2.2', 'Why does comparing Q with K predict a shift?',
    'Q measures the current product-to-reactant activity ratio. K is the ratio at equilibrium at the stated temperature. Their comparison tells us the sign of the reaction’s Gibbs-energy slope.',
    ['Start with ΔᵣG = ΔᵣG° + RT ln Q. At equilibrium Q = K and ΔᵣG = 0, giving ΔᵣG° = −RT ln K.',
     'Substitute this equilibrium relation back into the first equation: ΔᵣG = RT(ln Q − ln K) = RT ln(Q/K).',
     'Because R and absolute T are positive, Q < K makes ln(Q/K) negative: forward reaction lowers G. Q > K makes it positive, so reverse reaction lowers G.',
     'Adding a reactant normally lowers Q immediately. The subsequent reaction raises Q back toward K; it does not undo the entire externally imposed addition.'],
    'ΔᵣG = RT ln(Q/K)',
    'For K = 4 and Q = 2 at 298 K, ΔᵣG = (8.314)(298)ln(½) ≈ −1.72 kJ mol⁻¹ of reaction. The net tendency is forward.',
    'This thermodynamic equation uses dimensionless activities. A catalyst changes the speed of equilibration but changes neither K nor the sign criterion.',
    [(202, 206, '§7.2, reaction quotient and equilibrium constant')])

add('2.3', 'Why do compression and heating need different equations?',
    'Compression changes the current gas partial pressures. Heating also changes the equilibrium constant itself. Keeping those effects distinct turns the usual shift rules into a calculation.',
    ['For ideal gases, use activities aᵢ = pᵢ/p°. At constant temperature, changing V to V/f multiplies each partial pressure by f before reaction occurs.',
     'For aA + bB ⇌ cC + dD, substituting fpᵢ into Q gives Qnew = f^(c+d−a−b)Qold = f^Δn Qold. Compare this new quotient with the unchanged K.',
     'For heating, start from ln K = −ΔᵣG°/(RT). The Gibbs–Helmholtz relation d(ΔᵣG°/T)/dT = −ΔᵣH°/T² gives d ln K/dT = ΔᵣH°/(RT²).',
     'If ΔᵣH° is approximately constant, integrate between T₁ and T₂. Since the integral of 1/T² is −1/T, ln(K₂/K₁) = −(ΔᵣH°/R)(1/T₂ − 1/T₁).'],
    'Qnew = f^Δn Qold;  ln(K₂/K₁) ≈ −(ΔᵣH°/R)(1/T₂ − 1/T₁)',
    'For an exothermic reaction with ΔᵣH° = −50.0 kJ mol⁻¹, heating from 298 to 308 K gives K₂/K₁ ≈ 0.519. Heating can increase reaction rates while decreasing the equilibrium product preference.',
    'Use partial pressures and kelvin. A pure solid contributes no compression factor. The integrated temperature formula assumes nearly constant reaction enthalpy over the range.',
    [(210, 214, '§§7.3–7.4, pressure response and van ’t Hoff equation')])

add('2.4', 'Where does ΔG = ΔH − TΔS come from?',
    'Spontaneity depends on the entropy change of the system plus its surroundings. Heat released by a reaction can increase the surroundings’ entropy even when the reacting system becomes more ordered.',
    ['At constant pressure with only pressure–volume work, the heat absorbed by the system is qsystem = ΔH. A thermal reservoir at temperature T receives −ΔH.',
     'Its entropy change is therefore ΔSsurroundings = −ΔH/T. Add the system change: ΔStotal = ΔS − ΔH/T.',
     'Multiply by −T: −TΔStotal = ΔH − TΔS. Define G = H − TS; for a change at constant T this right-hand side is ΔG.',
     'Thus ΔStotal > 0 corresponds to ΔG < 0. At equilibrium, an infinitesimal reaction advancement has ΔᵣG = 0.'],
    'ΔStotal = ΔS − ΔH/T;  ΔG = ΔH − TΔS = −TΔStotal',
    'If ΔᵣH° = +20.0 kJ mol⁻¹ and ΔᵣS° = +100 J mol⁻¹ K⁻¹, then at 298 K, ΔᵣG° = 20.0 − 298(0.100) = −9.8 kJ mol⁻¹. The entropy contribution outweighs the endothermic cost.',
    'Convert entropy to kJ when enthalpy is in kJ. A standard-state ΔᵣG° predicts K; at a particular mixture composition use ΔᵣG = ΔᵣG° + RT ln Q. A sign alone does not give the reaction speed.',
    [(95, 98, '§3.5, combining the system and surroundings'), (208, 208, '§7.2, enthalpy and entropy contributions to K')])

add('2.5', 'Why do balanced coefficients become exponents in K?',
    'Each coefficient weights a species’ contribution to the reaction Gibbs energy. Chemical potential depends logarithmically on activity, so those weights become exponents when logarithms are combined.',
    ['For aA + bB ⇌ cC + dD, write ΔᵣG = cμC + dμD − aμA − bμB.',
     'Substitute μᵢ = μᵢ° + RT ln aᵢ. The standard terms sum to ΔᵣG°, and the remaining term is RT[c ln aC + d ln aD − a ln aA − b ln aB].',
     'Use n ln x = ln(xⁿ) and ln x − ln y = ln(x/y). The bracket becomes ln[(aCᶜaDᵈ)/(aAᵃaBᵇ)] = ln Q.',
     'At equilibrium, set ΔᵣG = 0 and Q = K: ln K = −ΔᵣG°/(RT). A pure solid or pure liquid in its reference state has activity 1, so its factor drops out.'],
    'Q = (aCᶜaDᵈ)/(aAᵃaBᵇ);  K = exp[−ΔᵣG°/(RT)]',
    'Doubling a reaction doubles ΔᵣG°, so Knew = exp[−2ΔᵣG°/(RT)] = K². Reversing it changes the sign, giving 1/K.',
    'Here aᵢ means activity; the coefficient a in aA is a different symbol. Thermodynamic K is dimensionless. For dilute solutes aᵢ ≈ [i]/c°, with c° = 1 M, giving the familiar school expression numerically.',
    [(204, 206, '§7.2(b), especially Justification 7.1')])

add('2.6', 'Why is there only one unknown change in an ICE table?',
    'For one independent reaction, all species changes are tied to the same reaction extent. An ICE table is conservation bookkeeping expressed in concentration units.',
    ['For A + B ⇌ C at fixed volume, let x = Δξ/V. If the initial concentrations are A₀, B₀ and C₀, the equilibrium values are A₀ − x, B₀ − x and C₀ + x.',
     'Insert these values into Kc = [C]/([A][B]), giving Kc(A₀ − x)(B₀ − x) = C₀ + x.',
     'Solve the resulting equation, then reject roots that make any concentration negative. A forward shift requires 0 ≤ x ≤ min(A₀,B₀); a reverse shift permits negative x down to −C₀.',
     'Substitute the accepted concentrations back into Q. Agreement with K checks equilibrium; the linked concentration changes check stoichiometry.'],
    'Kc = (C₀ + x)/[(A₀ − x)(B₀ − x)]',
    'With A₀ = B₀ = 0.100 M, C₀ = 0 and Kc = 10.0 M⁻¹, the equation gives x ≈ 0.0382 M or 0.2618 M. Only 0.0382 M leaves nonnegative reactants.',
    'Use post-mixing initial concentrations and a constant volume during equilibration. For 2A ⇌ B the changes are −2x and +x. Multiple independent equilibria may need multiple unknowns.',
    [(201, 201, '§7.1, extent of reaction'), (203, 207, '§7.2, stoichiometry and equilibrium composition')])

add('3.1', 'Why does a saturated solution stop gaining dissolved solute?',
    'Dissolution can be favourable at first because ions are stabilized by solvent interactions and by mixing. As dissolved activities rise, the driving tendency changes until dissolution and crystallization balance.',
    ['For MX(s) ⇌ M⁺(aq) + X⁻(aq), write ΔᵣG = ΔᵣG° + RT ln(aM⁺aX⁻). The pure solid’s activity is 1.',
     'At low dissolved activities, the logarithmic term favours dissolution. As both ion activities rise, this term becomes larger.',
     'At saturation with solid present, ΔᵣG = 0 and aM⁺aX⁻ = Ksp. More solid does not change this equilibrium relation while the same solid phase remains present.',
     'In dilute pure water with no other source of ions, a 1:1 salt gives [M⁺] = [X⁻] = s. Then the school concentration expression gives Ksp ≈ s² numerically when concentrations are entered in M.'],
    'MX(s) ⇌ M⁺ + X⁻;  Ksp = aM⁺aX⁻ ≈ ([M⁺]/c°)([X⁻]/c°)',
    'For a model 1:1 salt with Ksp = 1.0 × 10⁻¹⁰, s ≈ 1.0 × 10⁻⁵ M in pure water. Adding solid after saturation increases the undissolved amount.',
    'This applies the PDF’s activity framework to solubility. Solubility is an equilibrium amount; dissolution rate is a speed. Ion pairing, complex formation and nonideal activities can change the calculation.',
    [(161, 164, '§§5.7 and 5.9, solute and ionic activities'), (204, 206, '§7.2, heterogeneous equilibrium framework')])

add('3.2', 'How does selective precipitation identify an ion?',
    'A reagent is selective only if its concentration makes one possible salt supersaturated while another remains below its precipitation threshold. “Insoluble” is a useful table label, but the actual concentrations matter.',
    ['Suppose the possible cations M⁺ and N⁺ both form 1:1 salts with X⁻. For MX, precipitation becomes thermodynamically favourable when [M⁺][X⁻] > Ksp,MX in the school concentration convention.',
     'The threshold is therefore [X⁻]crit,M = Ksp,MX/[M⁺]. Likewise [X⁻]crit,N = Ksp,NX/[N⁺]. Use concentrations after reagent dilution.',
     'If the M threshold is smaller, choose [X⁻] between the two thresholds to begin precipitating MX selectively. Recalculate as M is removed, because its threshold then rises.',
     'Filter before testing the remaining solution. A precipitate identifies M only when the candidate list and possible interfering precipitates support that inference.'],
    'Ksp,MX/[M⁺] < [X⁻] < Ksp,NX/[N⁺]  (selective onset window)',
    'For hypothetical salts with both cations at 0.010 M and Ksp values 10⁻¹⁰ and 10⁻⁶, the thresholds are 10⁻⁸ and 10⁻⁴ M X⁻. At 10⁻⁶ M X⁻, only the first salt is initially supersaturated.',
    'This is an application of Q versus K, not a reagent recipe from the PDF. The window predicts precipitation onset, not automatically complete separation. Different stoichiometries require different powers.',
    [(204, 206, '§7.2, activities and reaction quotient')])

add('3.3', 'Why is Ksp sometimes s² and sometimes 4s³?',
    'The equilibrium expression uses free-ion concentrations. Molar solubility s counts dissolved formula units. Stoichiometry connects these quantities; they are not interchangeable.',
    ['For MₚXq(s) ⇌ pM + qX, dissolving s mol L⁻¹ in initially ion-free water gives [M] = ps and [X] = qs, provided no other reactions remove these ions.',
     'Write Ksp = aMᵖaXᑫ. With dilute activities, substitute aM ≈ ps/c° and aX ≈ qs/c°.',
     'Collect factors: Ksp ≈ pᵖqᑫ(s/c°)^(p+q). Therefore s ≈ c°[Ksp/(pᵖqᑫ)]^(1/(p+q)).',
     'For CaF₂ ⇌ Ca²⁺ + 2F⁻, p = 1 and q = 2. This gives Ksp ≈ (s/c°)(2s/c°)² = 4(s/c°)³.'],
    'CaF₂: Ksp ≈ 4(s/c°)³  →  s ≈ c°(Ksp/4)^(1/3)',
    'For a model CaF₂ value Ksp = 4.0 × 10⁻¹¹, s ≈ 2.15 × 10⁻⁴ M and [F⁻] ≈ 4.31 × 10⁻⁴ M. Substituting both ions returns the stated Ksp.',
    'This applies the general activity expression in the PDF. The school shorthand Ksp = 4s³ uses numerical concentrations in M. Common ions, acid reactions or complexes invalidate the simple ps and qs substitutions.',
    [(204, 206, '§7.2, stoichiometric powers and solid activity')])

add('3.4', 'Why must dilution be calculated before comparing Qsp and Ksp?',
    'The ions first occupy the combined volume. Precipitation then responds to their new activities. Using stock concentrations skips that immediate physical change and can predict a precipitate that should not form.',
    ['Before any reaction, use conservation of amount: [ion]mix = cstockVstock/Vtotal, assuming additive volumes.',
     'For AgCl(s) ⇌ Ag⁺ + Cl⁻, compute Qsp = aAg⁺aCl⁻. With dilute solutions, use the corresponding normalized concentrations.',
     'For dissolution, ΔᵣGdiss = RT ln(Qsp/Ksp). If Qsp > Ksp, dissolution has a positive Gibbs-energy slope; the reverse process, precipitation, is favoured.',
     'If precipitation reaches equilibrium with solid present, remove equal amounts of Ag⁺ and Cl⁻: ([Ag⁺]mix − x)([Cl⁻]mix − x) = Ksp in the school convention.'],
    'ΔᵣGprecip = −RT ln(Qsp/Ksp)',
    'Mix equal volumes of 1.0 × 10⁻⁵ M AgNO₃ and NaCl. Each ion becomes 5.0 × 10⁻⁶ M, so Qsp ≈ 2.5 × 10⁻¹¹, below Ksp = 1.8 × 10⁻¹⁰. No AgCl precipitation is predicted.',
    'The sign test is thermodynamic. Supersaturation can persist while nuclei form slowly. Below saturation, existing solid can dissolve; if none is present, no dissolution is possible.',
    [(204, 206, '§7.2, quotient and equilibrium criterion')])

add('4.1', 'Why does an acid–base reaction depend on both partners?',
    'An acid donates a proton to a base. Whether transfer is strongly favoured depends on the relative strengths of the two acids on opposite sides, not on an acid label alone.',
    ['Write HA + H₂O ⇌ H₃O⁺ + A⁻ with constant Ka(HA).',
     'Write BH⁺ + H₂O ⇌ H₃O⁺ + B with constant Ka(BH⁺), then reverse it. Reversal changes its constant to 1/Ka(BH⁺).',
     'Add the first equation to the reversed second equation. H₂O and H₃O⁺ cancel, leaving HA + B ⇌ A⁻ + BH⁺.',
     'Adding reaction Gibbs energies multiplies their equilibrium constants, so Ktransfer = Ka(HA)/Ka(BH⁺) = 10^[pKa(BH⁺) − pKa(HA)].'],
    'Ktransfer = Ka(HA)/Ka(BH⁺)',
    'If pKa(HA) = 4 and pKa(BH⁺) = 9, Ktransfer = 10⁵. Proton transfer favours the side containing the weaker acid BH⁺ and weaker base A⁻.',
    'This is an acid–base application of the PDF’s rules for combining equilibria. Constants must use the same solvent, temperature and activity conventions. A conjugate pair differs by one proton.',
    [(204, 206, '§7.2, reaction Gibbs energy and equilibrium constants')])

add('4.2', 'Why must a strong acid have a weak conjugate base?',
    'The acid and its conjugate base are two directions of a linked proton-transfer system. If HA gives up its proton readily in water, A⁻ has little tendency to take one back from water.',
    ['Write HA + H₂O ⇌ H₃O⁺ + A⁻ and A⁻ + H₂O ⇌ HA + OH⁻.',
     'Add them and cancel HA and A⁻. The net reaction is 2H₂O ⇌ H₃O⁺ + OH⁻, the ionization of water.',
     'Multiply the two activity expressions. The HA and A⁻ factors cancel, leaving the expression for Kw. Thus KaKb = Kw.',
     'Apply −log₁₀ to both sides: pKa + pKb = pKw. At 25 °C in the usual aqueous convention, pKw ≈ 14.00.'],
    'KaKb = Kw;  pKa + pKb = pKw',
    'For Ka = 1.8 × 10⁻⁵, the conjugate base has Kb ≈ (1.0 × 10⁻¹⁴)/(1.8 × 10⁻⁵) = 5.6 × 10⁻¹⁰ at 25 °C.',
    'This derives a conjugate-pair relation using the PDF’s equilibrium framework. Strong versus weak describes equilibrium tendency; concentrated versus dilute describes amount per volume.',
    [(204, 206, '§7.2, multiplying equilibria'), (161, 163, '§§5.7 and 5.9, activities')])

add('4.3', 'Why does neutrality depend on temperature?',
    'Neutrality means equal hydronium and hydroxide activities. Their common value is set by water’s equilibrium constant, which changes with temperature like any other equilibrium constant.',
    ['Start with Kw ≈ aH₃O⁺aOH⁻ when liquid-water activity is approximately 1.',
     'At neutrality, let both activities equal a. Then Kw = a², so a = √Kw.',
     'Take −log₁₀: pHneutral = −log₁₀(√Kw) = ½pKw. The familiar value 7.00 follows only when pKw = 14.00.',
     'The van ’t Hoff relation gives d ln Kw/dT = ΔᵣH°/(RT²). Because water ionization is endothermic around room temperature, warming increases Kw and lowers the neutral pH.'],
    'pHneutral = ½pKw(T)',
    'If the supplied Kw at a temperature is 4.0 × 10⁻¹⁴, the neutral activity is 2.0 × 10⁻⁷ and neutral pH ≈ 6.70. Equal acid and base activities still mean neutral.',
    'This applies the PDF’s temperature-dependence equation to water ionization. In dilute classroom calculations, activities are approximated by concentrations divided by 1 M.',
    [(161, 161, '§5.7(c), activity and pH'), (212, 214, '§7.4, temperature dependence')])

add('4.4', 'Why does a pH unit mean a factor of ten?',
    'pH compresses a very wide range of hydronium activities into a manageable scale. A logarithm turns multiplication into addition, so equal pH intervals represent equal concentration ratios.',
    ['The thermodynamic definition is pH = −log₁₀ aH₃O⁺. Undo the logarithm to get aH₃O⁺ = 10^(−pH).',
     'For two solutions, pH₂ − pH₁ = −log₁₀(a₂/a₁), so a₂/a₁ = 10^[−(pH₂ − pH₁)].',
     'From Kw = aH₃O⁺aOH⁻, take −log₁₀: pKw = pH + pOH. The number 14.00 enters only through the room-temperature value of Kw.',
     'For a dilute solution aH₃O⁺ ≈ [H₃O⁺]/c°. Multiplying the numerical activity by c° = 1 M returns the concentration.'],
    'a₂/a₁ = 10^(pH₁ − pH₂);  pH + pOH = pKw',
    'A pH 3 solution has about 100 times the hydronium concentration of a pH 5 solution in the dilute approximation. A change from pH 3 to 2.5 gives a factor 10^0.5 ≈ 3.16.',
    'log means base 10 here; ln in thermodynamic equations means base e. Activities are dimensionless. Concentrated solutions need activity corrections, and pH need not stay between 0 and 14.',
    [(161, 163, '§§5.7 and 5.9, activity definition and pH')])

add('4.5', 'Where does the square-root weak-acid formula come from?',
    'A weak acid produces hydronium and conjugate base together. The square root appears because the same reaction change x contributes to both factors in the numerator of Ka.',
    ['For a monoprotic acid of initial concentration C, assume no initial conjugate base and negligible water contribution. Then [H₃O⁺] = [A⁻] = x and [HA] = C − x.',
     'Using the school numerical concentration convention, Ka = x²/(C − x). Multiply through and collect terms: x² + Ka x − Ka C = 0.',
     'The positive quadratic root is x = [−Ka + √(Ka² + 4KaC)]/2. The other root is negative and cannot represent the ionization amount.',
     'If x is small compared with C, replace C − x by C. Then x² ≈ KaC and x ≈ √(KaC). Check x/C afterward; the usual 5% rule tests this approximation.'],
    'x = [−Ka + √(Ka² + 4KaC)]/2  ≈  √(KaC)',
    'For C = 0.100 M and Ka = 1.8 × 10⁻⁵, x ≈ 1.34 × 10⁻³ M, only 1.34% of C, giving pH ≈ 2.87. The small-change approximation is consistent.',
    'This applies activity-based equilibrium to a dilute weak acid. For the displayed numerical formula, enter C and x as molar concentration values. Extremely dilute acids require water ionization; polyprotic acids need additional equilibria.',
    [(201, 206, '§§7.1–7.2, reaction extent and equilibrium expressions')])

add('5.1', 'How does dissolving a salt change pH?',
    'Dissolving releases ions; some then transfer protons to or from water. Salt dissociation and hydrolysis are separate steps. The ion’s conjugate acid–base relationship determines whether it changes pH.',
    ['For sodium acetate, dissolution gives Na⁺ and CH₃COO⁻. In the classroom model Na⁺ is a spectator, while acetate accepts a proton: CH₃COO⁻ + H₂O ⇌ CH₃COOH + OH⁻.',
     'Use the conjugate-pair relation Kb = Kw/Ka(CH₃COOH). If the initial acetate concentration is C and hydrolysis produces x M OH⁻, Kb = x²/(C − x) in the school convention.',
     'When x ≪ C, [OH⁻] ≈ √(KbC). Calculate pOH, then use pH = pKw − pOH.',
     'For an ammonium salt, the corresponding acidic process is NH₄⁺ + H₂O ⇌ NH₃ + H₃O⁺, with Ka(NH₄⁺) = Kw/Kb(NH₃).'],
    'Conjugate-base salt: [OH⁻] ≈ √[(Kw/Ka)C]',
    'At 25 °C, 0.100 M acetate with Ka = 1.8 × 10⁻⁵ gives Kb ≈ 5.6 × 10⁻¹⁰, [OH⁻] ≈ 7.5 × 10⁻⁶ M and pH ≈ 8.87.',
    'This is an application of the PDF’s equilibrium framework. When both ions react or an ion is amphiprotic, include the competing equilibria. Not every metal cation is a spectator.',
    [(204, 206, '§7.2, combining equilibrium expressions')])

add('5.2', 'Why does a buffer obey Henderson–Hasselbalch?',
    'A buffer contains an acid that consumes added base and its conjugate base that consumes added acid. The equilibrium ratio sets pH, while the available amounts determine how much disturbance it can absorb.',
    ['Begin with Ka = aH₃O⁺aA⁻/aHA. Rearrange: aH₃O⁺ = Ka(aHA/aA⁻).',
     'Take −log₁₀ and use the quotient rule: pH = pKa + log₁₀(aA⁻/aHA). In dilute solutions this becomes pH ≈ pKa + log₁₀([A⁻]/[HA]).',
     'If strong acid is added, first use A⁻ + H₃O⁺ → HA + H₂O. Subtract the added acid moles from A⁻ and add them to HA.',
     'After that stoichiometric step, use the new ratio in the equilibrium relation. The common final volume cancels in [A⁻]/[HA] = n(A⁻)/n(HA).'],
    'pH ≈ pKa + log₁₀[n(A⁻)/n(HA)]',
    'Start with 0.100 mol of each component and add 0.010 mol strong acid. The ratio becomes 0.090/0.110; pH changes by log₁₀(0.818) ≈ −0.087.',
    'The logarithmic activity equation follows directly from Ka. Substituting post-neutralization amounts assumes both components remain and further equilibrium changes are small. This is a worked application of the PDF’s activity framework.',
    [(161, 163, '§§5.7 and 5.9, activities and pH'), (204, 206, '§7.2, equilibrium framework')])

add('5.3', 'Why does the equivalence-volume equation work?',
    'Equivalence is a stoichiometric condition: the titrant added has exactly the amount required by the balanced neutralization equation. It does not, by itself, specify pH.',
    ['For aA + bB → products, one reaction extent consumes aξ mol A and bξ mol B. At equivalence, nA/a = nB/b.',
     'Replace amount by concentration times volume. This gives cAVA/a = cBVB/b, provided each concentration refers to the corresponding reactant amount.',
     'For H₂SO₄ + 2NaOH → Na₂SO₄ + 2H₂O, complete two-proton neutralization gives n(NaOH) = 2n(H₂SO₄). The coefficient ratio cannot be dropped.',
     'A measured endpoint is the observed indicator or instrument signal. It estimates equivalence; its closeness depends on the chosen detection method.'],
    'cAVA/a = cBVB/b at equivalence',
    '25.00 mL of 0.1000 M H₂SO₄ contains 0.002500 mol acid. Complete neutralization needs 0.005000 mol NaOH, or 50.00 mL of 0.1000 M NaOH.',
    'This applies the PDF’s reaction-extent bookkeeping to titration. Use litres for n = cV. For weak acids, calculate the equivalence-point pH from the conjugate species after the stoichiometric calculation.',
    [(201, 204, '§§7.1–7.2, extent and stoichiometric numbers')])

add('5.4', 'Why does a weak-acid titration need different formulas in different regions?',
    'The solution changes character during titration. Initially it contains mostly weak acid; before equivalence it contains a buffer; at equivalence it contains the conjugate-base salt; after equivalence excess strong base usually controls pH.',
    ['Let n₀ be the initial HA amount and nb the added OH⁻ amount. Before equivalence, neutralization leaves n(HA) ≈ n₀ − nb and n(A⁻) ≈ nb. Use the buffer ratio when both are appreciable.',
     'At half-equivalence nb = n₀/2, so the ratio is 1 and pH ≈ pKa. The equality comes from equal conjugate-component amounts, not equal hydronium and hydroxide.',
     'At equivalence the buffer formula breaks down because the stoichiometric HA amount is zero. Use A⁻ hydrolysis with Csalt = n₀/Vtotal and Kb = Kw/Ka.',
     'Beyond equivalence, use [OH⁻] ≈ (nb − n₀)/Vtotal when the excess dominates hydrolysis and water ionization.'],
    'Before: pH ≈ pKa + log₁₀[nb/(n₀ − nb)];  at equivalence: [OH⁻] ≈ √(KbCsalt)',
    'Titrate 25.0 mL of 0.100 M HA (Ka = 1.8 × 10⁻⁵) with 0.100 M NaOH. At 12.5 mL added, pH ≈ 4.74. At 25.0 mL, Csalt = 0.0500 M and pH ≈ 8.72.',
    'This is an application of the PDF’s equilibrium framework. Near the start or very close to equivalence, simple buffer approximations can fail. A full calculation uses acid mass balance, charge balance, Ka and Kw together.',
    [(201, 206, '§§7.1–7.2, stoichiometry and equilibrium')])

add('5.5', 'Why do some oxides behave as acids and others as bases?',
    'Oxide behaviour can be understood through the proton-transfer and dissolution reactions available in water. An equation describes a possible pathway; its equilibrium constant determines how far it proceeds.',
    ['For a soluble basic oxide such as Na₂O, the overall equation is Na₂O + H₂O → 2Na⁺ + 2OH⁻. The oxide component accepts protons from water.',
     'For an acidic oxide, CO₂(aq) + H₂O ⇌ H₂CO₃ is followed by H₂CO₃ + H₂O ⇌ H₃O⁺ + HCO₃⁻.',
     'Add these equilibria: CO₂(aq) + 2H₂O ⇌ H₃O⁺ + HCO₃⁻. Multiplying their activity constants gives Koverall = KhydrationKa(H₂CO₃).',
     'Because much dissolved CO₂ remains unhydrated, the apparent acidity of total dissolved CO₂ is weaker than the intrinsic acidity of H₂CO₃ alone. The species named in a constant matter.'],
    'Koverall = Khydration × Ka(H₂CO₃)',
    'Adding CO₂ can lower water’s pH because the linked equilibria produce hydronium. This does not mean every dissolved CO₂ molecule becomes H₂CO₃.',
    'This applies the PDF’s method for combining reactions. Insoluble oxides may react little with water, and amphoteric oxides can react with either acid or base. The metal/non-metal trend is not a universal rule.',
    [(204, 206, '§7.2, adding reactions and combining constants')])

add('6.1', 'Why must oxidation and reduction always occur together?',
    'Electron transfer conserves charge. One reactant can lose electrons only if another process accepts them; a balanced redox reaction accounts for both sides of that transfer.',
    ['For Zn → Zn²⁺ + 2e⁻, zinc’s oxidation number rises from 0 to +2. For Cu²⁺ + 2e⁻ → Cu, copper’s oxidation number falls from +2 to 0.',
     'Add the half-reactions. The two electrons appear once on each side and cancel, leaving Zn + Cu²⁺ → Zn²⁺ + Cu.',
     'Charge is +2 before and +2 after. Atoms are also conserved. Electrons are bookkeeping intermediates in the half-reaction method, not a substance accumulating in the net equation.',
     'Zn is the reducing agent because it supplies electrons and is oxidized. Cu²⁺ is the oxidizing agent because it accepts electrons and is reduced.'],
    'Electrons lost = electrons gained;  Zn + Cu²⁺ → Zn²⁺ + Cu',
    'For a reaction transferring 2 mol electrons per mole of reaction, 0.0100 mol reaction extent transfers 0.0200 mol electrons, corresponding to about 1930 C.',
    'Oxidation numbers are formal assignments; in covalent compounds they need not be actual ionic charges. Half-reactions expose electron balance even when a redox process occurs without a separate external circuit.',
    [(216, 219, '§§7.5–7.7, half-reactions and cell reactions')])

add('6.2', 'Why are water, H⁺, OH⁻ and electrons allowed in balancing?',
    'Aqueous balancing uses species available in the stated medium. Water balances oxygen and hydrogen; acid or base supplies the appropriate proton bookkeeping; electrons then balance charge.',
    ['In acid, begin with MnO₄⁻ → Mn²⁺. Balance oxygen by adding 4H₂O on the right, then hydrogen by adding 8H⁺ on the left.',
     'The left charge is −1 + 8 = +7 and the right charge is +2. Add 5e⁻ on the left to reduce its charge to +2: MnO₄⁻ + 8H⁺ + 5e⁻ → Mn²⁺ + 4H₂O.',
     'For a basic-medium example with MnO₂ as product, first obtain MnO₄⁻ + 4H⁺ + 3e⁻ → MnO₂ + 2H₂O in acid-style bookkeeping.',
     'Add 4OH⁻ to both sides. Replace 4H⁺ + 4OH⁻ by 4H₂O and cancel 2H₂O, giving MnO₄⁻ + 2H₂O + 3e⁻ → MnO₂ + 4OH⁻.'],
    'Basic half-reaction: MnO₄⁻ + 2H₂O + 3e⁻ → MnO₂ + 4OH⁻',
    'In the basic half-reaction, each side has one Mn, six O and four H atoms; each has charge −4. After combining half-reactions, no electrons may remain in the net equation.',
    'This extends the PDF’s half-reaction bookkeeping. Balance the product specified by the chemistry: changing medium can change the product, not merely the written H⁺ and OH⁻ terms.',
    [(216, 219, '§§7.5–7.7, half-reactions and their combination')])

add('6.3', 'Why are electrode potentials subtracted but never multiplied by coefficients?',
    'Voltage measures energy per unit charge. Doubling a reaction doubles both its available energy and its transferred charge, so the voltage stays the same.',
    ['For the balanced cell reaction, ΔᵣG° = −nFE°cell, where n is moles of electrons transferred per mole of reaction and F = 96 485 C mol⁻¹.',
     'Write both table entries as reductions. The cathode reaction proceeds as listed; reverse the anode entry to represent oxidation. Subtract the anode reduction potential from the cathode reduction potential.',
     'If the net equation is multiplied by m, then ΔᵣG° becomes mΔᵣG° and n becomes mn. Dividing −mΔᵣG° by mnF leaves E° unchanged.',
     'Combine ΔᵣG° = −nFE°cell with ΔᵣG° = −RT ln K: ln K = nFE°cell/(RT). A positive standard cell potential therefore means K > 1.'],
    'E°cell = E°cathode − E°anode;  ln K = nFE°cell/(RT)',
    'For Zn/Cu, E°cell = 0.34 − (−0.76) = 1.10 V. With n = 2, ΔᵣG° ≈ −212 kJ mol⁻¹. Doubling the equation doubles that energy but leaves 1.10 V unchanged.',
    'A positive E° predicts forward preference under standard conditions. At other compositions use E and Q through the Nernst equation; a potential predicts tendency, not the speed of reaction.',
    [(219, 224, '§§7.7–7.9, Gibbs energy, standard potentials and K')])

add('6.4', 'How does composition change a cell’s voltage?',
    'The cell converts a reaction’s Gibbs-energy decrease into electrical work. As the mixture moves toward equilibrium, the chemical driving tendency decreases and so does its reversible voltage.',
    ['Start with ΔᵣG = ΔᵣG° + RT ln Q and the reversible electrical-work relations ΔᵣG = −nFE and ΔᵣG° = −nFE°.',
     'Substitute: −nFE = −nFE° + RT ln Q. Divide by −nF to obtain E = E° − (RT/nF)ln Q.',
     'At 298.15 K, use ln Q = 2.303 log₁₀Q and 2.303RT/F = 0.05916 V. This gives the familiar base-10 Nernst equation.',
     'For Zn + Cu²⁺ → Zn²⁺ + Cu, pure metals have activity 1, so Q = aZn²⁺/aCu²⁺. Accumulating Zn²⁺ or consuming Cu²⁺ raises Q and lowers E.'],
    'E = E° − (RT/nF)ln Q;  at 25 °C: E = E° − (0.05916 V/n)log₁₀Q',
    'With n = 2, E° = 1.10 V and Q = 100, E ≈ 1.10 − (0.05916/2)(2) = 1.041 V. At overall reaction equilibrium, Q = K and E = 0.',
    'E here is reversible open-circuit emf. A disconnected cell can have nonzero E because electron transfer is blocked; that is not overall reaction equilibrium. Under current, resistance and electrode kinetics reduce terminal voltage. Ions, rather than electrons, carry charge through the salt bridge.',
    [(217, 222, '§§7.6–7.7, cells and Nernst equation')])

add('6.5', 'How does current determine the amount produced by electrolysis?',
    'A power supply drives electron transfer in the chosen nonspontaneous direction. Counting the charge sent through the circuit counts the electrons available to form product.',
    ['For constant current I over time t, Qcharge = It. Since one mole of electrons carries F coulombs in magnitude, n(e⁻) = It/F.',
     'If z electrons are required per product unit, the product amount is n(product) = It/(zF). Multiplying by molar mass M gives the deposited mass.',
     'For Cu²⁺ + 2e⁻ → Cu, z = 2. A current of 1.00 A for 1930 s transfers 1930 C, or about 0.0200 mol electrons, producing 0.0100 mol Cu at 100% current efficiency.',
     'The reversible minimum electrical work for a forced reaction is its positive ΔᵣG. Since charge per mole of reaction is nF, the opposing reversible voltage magnitude is ΔᵣG/(nF). Actual operation requires additional voltage for resistance and electrode overpotentials.'],
    'n(product) = It/(zF);  mass = MIt/(zF)',
    'Using M(Cu) = 63.55 g mol⁻¹, the example deposits about 0.636 g Cu. At 80% current efficiency, the amount deposited is 0.80 × 0.636 ≈ 0.509 g.',
    'The mass formula is charge-conservation bookkeeping extending the PDF’s electrical-work relation. If current varies, use Qcharge = ∫I dt. Competing electrode reactions reduce yield; the anode is always oxidation and the cathode reduction, including in electrolysis.',
    [(219, 220, '§7.7, charge and electrical work'), (938, 939, '§25.9, electrode overpotential')])

def formatted(text):
    text = escape(text)
    # Keep the species label below the activity symbol, including its ionic charge.
    text = re.sub(r'\ba(H₃O⁺|OH⁻|Zn²⁺|Cu²⁺|M⁺|X⁻|A⁻|HA|C|D|A|B)(?![A-Za-z])',
                  lambda m: 'a<sub>' + m[1] + '</sub>', text)
    text = re.sub(r'μ([ABCD])(?![A-Za-z])', lambda m: 'μ<sub>' + m[1] + '</sub>', text)
    return text

def block(number, data):
    title, intuition, steps, equation, check, scope, refs = data
    links = []
    for start, end, label in refs:
        span = str(start) if start == end else f'{start}–{end}'
        pdfspan = str(start + 32) if start == end else f'{start + 32}–{end + 32}'
        links.append(f'<a href="Physical_Chemistry.pdf#page={start + 32}" target="_blank" rel="noopener">{escape(label)} · printed pp. {span} · PDF pp. {pdfspan} ↗</a>')
    return ('\n<section class="further-explain" aria-labelledby="further-' + number.replace('.', '-') + '">'
        + '<h4 id="further-' + number.replace('.', '-') + '">Further explain</h4>'
        + '<h5>' + escape(title) + '</h5><p>' + formatted(intuition) + '</p>'
        + '<ol class="derivation-steps">' + ''.join('<li>' + formatted(s) + '</li>' for s in steps) + '</ol>'
        + '<div class="equation" data-copy tabindex="0" aria-label="Further explanation equation for section ' + number + '; press Enter or double-click to copy">' + formatted(equation) + '</div>'
        + '<p class="further-check"><strong>Make it concrete.</strong> ' + formatted(check) + '</p>'
        + '<p class="further-scope"><strong>When this applies.</strong> ' + formatted(scope) + '</p>'
        + '<p class="further-source"><strong>Physical chemistry connection.</strong> ' + ' · '.join(links) + '</p></section>\n')

if __name__ == '__main__':
    path = ROOT / 'tutorial.html'
    html = path.read_text()
    backup = Path('/private/tmp/chemistry12-before-further-explain.html')
    if not backup.exists():
        backup.write_text(html)
    # Allow safe regeneration of only these authored blocks.
    html = re.sub(r'\n<section class="further-explain".*?</section>\n', '', html, flags=re.S)
    pattern = r'(<details class="lesson" id="section-(\d+-\d+)".*?)(<div class="section-links">)'
    seen = []
    def insert(m):
        number = m[2].replace('-', '.')
        seen.append(number)
        return m[1] + block(number, notes[number]) + m[3]
    html = re.sub(pattern, insert, html, flags=re.S)
    assert len(seen) == len(notes) == 30 and len(set(seen)) == 30
    css = '''
/* Supplemental explanations adapted from Atkins and de Paula. */
.further-explain{margin:28px 0 24px;padding:22px 24px;background:#f3f6ee;border:1px solid #dce5d4;border-left:4px solid var(--green);border-radius:10px;font-size:13px;line-height:1.85;overflow-wrap:anywhere}
.lesson-body .further-explain h4{margin:0 0 10px;color:var(--green)}
.further-explain h5{font:600 18px/1.45 system-ui,sans-serif;margin:0 0 14px;letter-spacing:-.2px}
.further-explain p{margin:12px 0}.further-explain .derivation-steps{margin:18px 0}
.further-explain .equation{padding:14px 16px;background:#fff;border:1px solid #dce5d4;border-radius:7px;font-size:14px;overflow-wrap:anywhere}
.further-check{padding-top:8px}.further-scope{color:#50645a}.further-source{border-top:1px solid #dce5d4;padding-top:13px;font-size:11px;color:var(--muted)}
@media(max-width:760px){.further-explain{padding:18px 15px}.further-explain h5{font-size:16px}.further-explain .equation{font-size:13px;padding:12px}}
@media print{.further-explain{background:#fff;border-color:#bbb;break-inside:auto}.further-explain h4,.further-explain h5{break-after:avoid}.further-explain .equation{break-inside:avoid}}
'''
    if '/* Supplemental explanations adapted' not in html:
        html = html.replace('</style>', css + '</style>', 1)
    old_note = 'Open any numbered section for definitions, concepts, equations, derivation or reasoning, and a worked check.'
    new_note = 'Open any numbered section for definitions, concepts, equations, derivation or reasoning, and a worked check. Each lesson also has a “Further explain” section that connects the topic to physical chemistry, with intermediate steps, a numerical check, assumptions, and linked source pages. These are original explanations adapted from Atkins and de Paula’s Physical Chemistry (8th edition); acid–base, solubility, and titration notes apply its general equilibrium framework. In these additions, ln is the natural logarithm and log₁₀ is base 10; ° denotes a standard state, Δᵣ a change per mole of reaction as written, R = 8.314 J mol⁻¹ K⁻¹, and T is in kelvin. Activity a is a dimensionless effective concentration: a ≈ [species]/c° in the dilute model, where c° = 1 M. This lets thermodynamic logarithms use dimensionless numbers.'
    html, intro_count = re.subn(r'(<strong>How to use this page\.</strong> ).*?(?= “Derivation”)',
                               lambda m: m[1] + new_note, html, count=1, flags=re.S)
    assert intro_count == 1
    old_scope = 'This section stays with the textbook’s qualitative comparison rather than adding a separate thermodynamics course.'
    html = html.replace(old_scope, 'The “Further explain” section below quantifies this competition using Gibbs energy.')
    path.write_text(html)
    print(f'Added {len(seen)} source-linked Further explain sections to {path}')
