from pathlib import Path
from html import escape
from html.parser import HTMLParser
import ast, json, re

ROOT = Path(__file__).resolve().parents[1]
OLD = Path('/private/tmp/chemistry12-tutorial-before-reorganization.html').read_text()
tree = ast.parse((ROOT/'tmp/pdfs/add_navigation.py').read_text())
chapters = ast.literal_eval(next(n.value for n in tree.body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='chapters' for t in n.targets)))
appendix = ast.literal_eval(next(n.value for n in tree.body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='appendix' for t in n.targets)))
lessons = {}

def add(number, definitions, concept, equations, steps, example, caution):
    lessons[number] = dict(definitions=definitions, concept=concept, equations=equations, steps=steps, example=example, caution=caution)

add('1.1', [
 ('Chemical kinetics','The study of reaction rates and the factors that control them.'),
 ('Average rate','The change in a measured quantity divided by the elapsed time over an interval.'),
 ('Instantaneous rate','The rate at one instant: the slope of the tangent to a quantity–time graph.')],
 'Follow a measurable property that tracks reactant consumption or product formation: concentration, gas volume, mass loss, colour, or pressure. A measurement is useful only if its change can be connected to the reacting amount. For a concentration graph, a steeper slope means a faster change. Rates measured from different species are related by the balanced equation.',
 ['Average disappearance rate of A = −Δ[A]/Δt', 'For aA → bB: r = −(1/a) Δ[A]/Δt = (1/b) Δ[B]/Δt', 'Concentration-rate units: mol L⁻¹ s⁻¹'],
 ['Start from the definition Δ[A] = [A]final − [A]initial and Δt = tfinal − tinitial.',
 'A reactant is consumed, so Δ[A] is negative. The minus sign makes its disappearance rate positive.',
 'For each a mol of A consumed, b mol of B form. At fixed volume, −Δ[A]/a = Δ[B]/b.',
 'Divide this stoichiometric equality by Δt. Taking a progressively smaller time interval gives the instantaneous rate, using derivatives instead of finite changes.'],
 'For 2A → B, [A] falls from 0.80 to 0.60 M in 10 s. A disappears at (0.80 − 0.60)/10 = 0.020 M s⁻¹. The normalized reaction rate and B formation rate are both 0.010 M s⁻¹.',
 'A gas-volume rate in mL s⁻¹ and a concentration rate in M s⁻¹ cannot be compared directly without conversion. Use the graph’s axes and the question’s definition of rate.')

add('1.2', [
 ('Concentration','Amount of solute per solution volume; molarity c = n/V.'),
 ('Surface area','The exposed area of a solid that is accessible to other reactants.'),
 ('Catalyst','A substance that participates in a reaction pathway and is regenerated overall, increasing the rate.')],
 'Reaction rate depends on the nature of the reactants, concentration, temperature, exposed surface area, and catalysts. More particles per volume usually increases collision frequency. Crushing a solid exposes more reaction sites. Heating increases molecular motion and the fraction of collisions energetic enough to react. A catalyst changes the pathway. These explanations connect the observations to collision theory in §1.3.',
 ['c = n/V', 'Same n, half the volume: cnew = n/(V/2) = 2c', 'For equal cubic pieces of side ℓ: total surface area / total volume = 6/ℓ'],
 ['Concentration is defined as amount divided by volume. Holding amount constant and reducing volume raises concentration.',
 'A cube has six faces, each with area ℓ², and volume ℓ³. Its area-to-volume ratio is 6ℓ²/ℓ³ = 6/ℓ.',
 'For a fixed total solid volume, making the pieces smaller raises total exposed area. This can increase the rate of a reaction occurring at the surface.',
 'Temperature and catalyst effects need the energy-and-pathway explanation of §§1.3–1.5; geometry alone does not derive their size.'],
 'Splitting one 1 cm cube into eight 0.5 cm cubes keeps the total volume at 1 cm³. The area rises from 6 cm² to 8 × 6 × (0.5)² = 12 cm². More surface is available, although the rate need not exactly double.',
 'There is no universal rule that doubling concentration doubles rate, or that a 10 °C increase doubles rate. Determine the relevant rate law and conditions.')

add('1.3', [
 ('Effective collision','A collision with sufficient energy and a suitable molecular orientation to form products.'),
 ('Activation energy, Eₐ','The energy barrier between reactants and the activated configuration along a pathway.'),
 ('Activated complex','The unstable arrangement of atoms near the top of the reaction barrier.')],
 'Colliding is necessary in a collision model, but many encounters fail to react. Particles may lack the required energy or present the wrong atoms to one another. At higher temperature, a greater fraction can cross the barrier. A catalyst supplies another pathway with a lower effective barrier; it does not increase the sample’s temperature.',
 ['Possible unlike-particle pairs = NA × NB', 'For a simple elementary A + B step: r = k[A][B]', 'Effective encounters = total encounters × energetic fraction × orientation fraction'],
 ['If there are NA particles of A, each can encounter any of the NB particles of B. Counting the possible unlike pairs gives NA NB.',
 'At fixed volume and comparable conditions, the concentration factors for these pair encounters are proportional to [A][B].',
 'Only a fraction of encounters have enough energy and a productive orientation. For this simple model, include those factors in k.',
 'This motivates a bimolecular elementary-step rate law. It does not prove that a multistep overall reaction has the same concentration exponents.'],
 'Three A particles and four B particles have 3 × 4 = 12 possible unlike pairs. Doubling A gives 24 pairs. This is a collision-counting model, not a count of successful reactions in one second.',
 'The average particle energy is not the activation energy. A temperature distribution contains both higher- and lower-energy particles; the fraction above the barrier matters.')

add('1.4', [
 ('Enthalpy change, ΔH','The difference Hproducts − Hreactants; at constant pressure with only pressure–volume work it equals heat absorbed by the system.'),
 ('Exothermic / endothermic','An exothermic reaction has ΔH < 0; an endothermic reaction has ΔH > 0.'),
 ('Reaction coordinate','A measure of progress along a molecular reaction pathway, used for the horizontal axis of an energy diagram.')],
 'Read the starting level, ending level, and barrier separately. The height from reactants to the peak is the forward activation energy. The difference between the product and reactant levels gives the reaction energy change. Breaking bonds requires energy; making bonds releases energy. A catalyst changes the barrier and can introduce multiple peaks, while leaving the initial and final states unchanged.',
 ['ΔH = HP − HR', 'Eₐ,forward = H‡ − HR; Eₐ,reverse = H‡ − HP', 'ΔH = Eₐ,forward − Eₐ,reverse', 'ΔH ≈ Σ(bond energies broken) − Σ(bond energies formed)'],
 ['Label the reactant level HR, product level HP, and common peak H‡ on the same energy scale.',
 'Subtract the reactant level from the peak to find the forward barrier; subtract the product level to find the reverse barrier.',
 'Subtract the two barriers: (H‡ − HR) − (H‡ − HP) = HP − HR = ΔH.',
 'For the bond-energy estimate, imagine breaking reactant bonds to separated atoms, then forming product bonds. Add the energy cost of breaking and the negative energy change of forming. Average bond energies give an approximation.'],
 'If HR = 20, HP = −30, and H‡ = 100 kJ mol⁻¹, then Eₐ,forward = 80, Eₐ,reverse = 130, and ΔH = −50 kJ mol⁻¹. The reaction is exothermic even though it has a substantial barrier.',
 'The horizontal axis is reaction progress, not time. A negative ΔH alone does not establish a fast reaction or determine equilibrium composition.')

add('1.5', [
 ('Reaction mechanism','A proposed sequence of elementary steps that sums to the overall reaction.'),
 ('Intermediate / catalyst','An intermediate is formed and later consumed; a catalyst is consumed and later regenerated.'),
 ('Rate law / reaction order','A rate law relates rate to concentration; each concentration exponent is its order with respect to that reactant.')],
 'A mechanism must reproduce the overall balanced equation and be compatible with the measured rate law. A slow step can control the overall rate when later steps are sufficiently fast. Elementary-step molecularity can determine a step’s rate law; overall reaction coefficients generally cannot. If a proposed rate law contains an intermediate, an additional justified relation is needed to express it in measurable reactant concentrations.',
 ['r = k[A]ᵐ[B]ⁿ; overall order = m + n', 'At fixed [B] and temperature: r₂/r₁ = ([A]₂/[A]₁)ᵐ', 'm = log(r₂/r₁) / log([A]₂/[A]₁)'],
 ['Write the empirical rate law for two experiments at the same temperature.',
 'Divide the two equations. With [B] unchanged, k and [B]ⁿ cancel, leaving the concentration ratio raised to m.',
 'Take logarithms and solve for m. Repeat with A fixed to determine n.',
 'For a simple mechanism A + B → I (slow), then I + B → P (fast), the steps sum to A + 2B → P. The slow elementary step predicts r ≈ k[A][B], showing why the overall B coefficient need not be its order.'],
 'If doubling [A] at constant [B] makes the rate four times larger, 4 = 2ᵐ, so m = 2. If doubling [B] leaves the rate unchanged, n = 0. Then r = k[A]², and k has units M⁻¹ s⁻¹.',
 'An empirical rate law must be measured; it is not derived merely by balancing the overall equation. Matching one rate law supports a mechanism but does not uniquely prove it.')

add('2.1', [
 ('Reversible reaction','A reaction for which forward and reverse conversions are possible under the stated conditions.'),
 ('Dynamic equilibrium','A state in which forward and reverse reaction rates are equal, while both processes continue.'),
 ('Equilibrium position','The relative amounts of reactants and products present at equilibrium.')],
 'A closed reacting system can reach constant composition without stopping its molecular changes. Initially, a reactant-rich mixture often forms products faster than it reforms reactants. As composition changes, the rates approach equality. At equilibrium, measurable macroscopic properties remain constant at fixed conditions, but reactant and product concentrations need not be equal.',
 ['At equilibrium: rforward = rreverse', 'For A ⇌ B at fixed volume: Δ[B]/Δt = rforward − rreverse = 0'],
 ['Formation of B adds to [B], while the reverse reaction removes B. The net change is the forward rate minus the reverse rate.',
 'At equilibrium those two rates are equal, so their difference is zero.',
 'Zero net concentration change follows from equal opposing rates. It does not require either rate to be zero.',
 'For reactions with other coefficients, include the appropriate stoichiometric factors when converting reaction rate to each species’ concentration change.'],
 'A mixture can contain 0.20 M A and 0.80 M B while both directions proceed at 0.010 M s⁻¹. The concentrations stay constant even though they are unequal.',
 'A constant-looking sample is not sufficient evidence of dynamic equilibrium: a reaction may instead be too slow to detect or have run effectively to completion.')

add('2.2', [
 ('Le Chatelier’s principle','When a system at equilibrium is disturbed, its net reaction tends to partially oppose the disturbance as equilibrium is re-established.'),
 ('Shift right / left','Net conversion toward products / toward reactants after a disturbance.'),
 ('Common-ion effect','A shift caused by adding an ion already involved in an equilibrium.')],
 'Adding a dissolved reactant usually favours its consumption; removing a product usually favours its replacement. The immediate change imposed by the experiment and the later chemical response are separate events. A shift partially offsets a concentration disturbance; it need not restore the original concentration. A catalyst speeds both directions and does not change the equilibrium composition.',
 ['A ⇌ B: Q = [B]/[A]', 'Q < K: net forward; Q > K: net reverse; Q = K: equilibrium'],
 ['Begin at equilibrium, where [B]/[A] = K. Keep temperature fixed so K is unchanged.',
 'Add A without appreciably changing volume. The denominator increases immediately, so the new ratio is below K.',
 'Net conversion of A to B raises the numerator and reduces the denominator until the ratio returns to K.',
 'The quotient reasoning, developed fully in §2.5, explains the concentration shift rather than treating it as a memorized arrow rule.'],
 'If K = 4, [A] = 0.10 M and [B] = 0.40 M are at equilibrium. Immediately increasing [A] to 0.20 M gives Q = 2. The subsequent net reaction forms B.',
 'Adding more pure solid does not change the equilibrium position while that solid phase is already present. Its amount is not included as a variable concentration in K.')

add('2.3', [
 ('Partial pressure','The contribution a gas makes to the total pressure of a mixture.'),
 ('Volume disturbance','A change that simultaneously changes concentrations or partial pressures.'),
 ('Temperature disturbance','A change that alters the equilibrium constant as well as reaction rates.')],
 'At constant temperature, compressing an ideal gaseous equilibrium favours the side with fewer gas particles when the gas coefficients differ. Expansion favours the side with more. In the simple dilute-solution model, dilution similarly favours the side with more dissolved particles counted in the equilibrium expression; omit pure solids and the liquid solvent. Heating favours the endothermic direction; cooling favours the exothermic direction. Treat heat as a bookkeeping term on the appropriate side of a thermochemical equation, not as a concentration term in K.',
 ['For aA(g) + bB(g) ⇌ cC(g) + dD(g): Δn = c + d − a − b', 'If every gas concentration is multiplied by f: Qnew = f^Δn Qold', 'At fixed n and T: concentration ∝ 1/V'],
 ['At fixed gas amounts, reducing the volume by a factor f multiplies every gas concentration by f.',
 'Insert f[A], f[B], f[C], and f[D] into the quotient. The numerator gains f^(c+d), and the denominator gains f^(a+b).',
 'Therefore Qnew = f^Δn K for an initially equilibrated mixture. For compression f > 1 and fewer gas moles on the product side, Δn < 0, so Qnew < K and the reaction shifts forward.',
 'The same scaling applies to aqueous concentration factors when the dilute model holds. If dilution halves every included concentration, f = 1/2; use the coefficient difference for dissolved species to find the immediate Q change. Pure solids and liquids do not contribute factors of f.',
 'For temperature, use the reaction’s heat direction. Heating an exothermic forward reaction favours reverse conversion and lowers its K; heating an endothermic forward reaction raises its K.'],
 'For N₂(g) + 3H₂(g) ⇌ 2NH₃(g), halving volume gives f = 2 and Δn = −2. Immediately Qnew = K/4, so ammonia formation is favoured. If the forward reaction is exothermic, heating instead favours reactants.',
 'Adding inert gas at constant volume changes total pressure but not reactant partial pressures in the ideal model, so there is no shift. At constant total pressure, adding inert gas expands the mixture and can cause a shift.')

add('2.4', [
 ('Entropy, S','A state property connected to the number of accessible microscopic arrangements and the dispersal of energy; molar entropy has units J mol⁻¹ K⁻¹.'),
 ('Enthalpy tendency','Other factors equal, lower enthalpy favours a state energetically.'),
 ('Entropy tendency','More accessible arrangements favour a state statistically; the entropy of system plus surroundings controls spontaneity.')],
 'The book compares the tendency toward lower enthalpy with the tendency toward higher entropy. Increasing gas particles or changing a substance from solid to liquid to gas often increases entropy. These are useful trends, not universal proofs. When the two tendencies oppose, temperature and their magnitudes matter. Equilibrium can contain appreciable reactants and products; opposing tendencies alone do not quantify their proportions.',
 ['ΔH = Hproducts − Hreactants', 'ΔS°reaction = ΣνS°products − ΣνS°reactants', 'For the same substance, typically: S(gas) > S(liquid) > S(solid)'],
 ['A reaction property change is the final total minus the initial total. Each balanced coefficient ν counts how many moles contribute.',
 'Multiply each tabulated standard molar entropy by its coefficient, add the product contributions, and subtract the reactant contributions.',
 'A positive result means the system’s entropy increases in the forward direction. A negative enthalpy change means the forward direction releases heat at constant pressure.',
 'If ΔH < 0 and ΔS > 0, both classroom tendencies favour products. If ΔH > 0 and ΔS < 0, both oppose forward reaction. If the signs match, the tendencies compete; these sign arguments do not supply K.'],
 'For exothermic N₂(g) + 3H₂(g) ⇌ 2NH₃(g), the enthalpy tendency favours products. The reduction from four to two gas particles suggests the entropy tendency favours reactants. This explains the competition qualitatively; it does not establish a numerical yield.',
 '“Disorder” is a memory aid. Do not claim that all dissolving increases entropy, or that every exothermic process is spontaneous. This section stays with the textbook’s qualitative comparison rather than adding a separate thermodynamics course.')

add('2.5', [
 ('Equilibrium constant, K','At a specified temperature, the equilibrium value of the product-to-reactant expression for a particular balanced reaction.'),
 ('Reaction quotient, Q','The same expression evaluated using the current composition, which may not be at equilibrium.'),
 ('Homogeneous / heterogeneous equilibrium','An equilibrium involving one phase / more than one phase.')],
 'Write each dissolved or gaseous species to the power of its balanced coefficient, with products above reactants. Omit pure solids and pure liquids. A large K favours products in the expression, but does not imply a fast reaction. Temperature changes K; changing concentration at fixed temperature changes Q. Here the school concentration convention is used. Thermodynamic constants use dimensionless activities; dilute-solution concentrations approximate them.',
 ['aA + bB ⇌ cC + dD: Kc = [C]ᶜ[D]ᵈ / ([A]ᵃ[B]ᵇ)', 'For H₂ + I₂ ⇌ 2HI: Kc = [HI]² / ([H₂][I₂])', 'Reverse the equation: Knew = 1/K; multiply coefficients by n: Knew = Kⁿ'],
 ['The textbook motivates the H₂/I₂ expression using the model rate laws rf = kf[H₂][I₂] and rr = kr[HI]².',
 'At equilibrium set rf = rr and rearrange: kf/kr = [HI]²/([H₂][I₂]). At a fixed temperature the rate-constant ratio is a constant in this model.',
 'For general reactions, use the law of mass action to construct K from stoichiometric coefficients. The simple rate-law argument is illustrative; overall coefficients do not generally determine experimental rate laws.',
 'Reversing the reaction swaps numerator and denominator. Multiplying every coefficient raises each factor, and therefore K, to the same power. Adding reactions multiplies their K values.'],
 'For H₂ + I₂ ⇌ 2HI, equilibrium concentrations 0.20 M, 0.20 M, and 0.40 M give Kc = 0.40²/(0.20 × 0.20) = 4.0. For 2HI ⇌ H₂ + I₂, Kc = 0.25.',
 'Use equilibrium concentrations for K, current concentrations for Q. The omission of a pure phase assumes that phase exists; the constant does not guarantee an unlimited supply of solid.')

add('2.6', [
 ('ICE table','A table of initial concentrations, stoichiometric changes, and equilibrium concentrations.'),
 ('Change variable, x','A concentration change scaled so other changes follow the balanced coefficients.'),
 ('Small-change approximation','Neglecting a concentration change only when it is small relative to the concentration from which it is subtracted.')],
 'First balance the reaction and convert all starting amounts to concentrations in the final volume. Use Q to decide the net direction when needed. Write changes in coefficient ratios, substitute equilibrium values into K, solve, and reject roots that give negative concentrations. Check any approximation after solving and substitute the answer back into K.',
 ['A ⇌ B: [A]eq = [A]₀ − x; [B]eq = [B]₀ + x', 'K = ([B]₀ + x)/([A]₀ − x)', 'Approximation check: 100|νx|/C ≤ 5% for each neglected change'],
 ['If x M of A converts to B at fixed volume, conservation requires A to decrease by x and B to increase by x.',
 'Substitute those concentrations into K. This turns the equilibrium condition into an equation for x.',
 'For an initially product-free 1:1 system, K = x/(C − x), so KC − Kx = x and x = KC/(1 + K).',
 'For more complicated stoichiometry, keep the coefficients in both the change row and the powers in K. Solve the resulting algebra and check 0 ≤ x ≤ the limiting allowed change.'],
 'Initially [A] = 0.50 M, [B] = 0 and K = 4.0 for A ⇌ B. Then x = 4.0 × 0.50/5.0 = 0.40 M. Thus [A]eq = 0.10 M and [B]eq = 0.40 M; the ratio is 4.0.',
 'Do not subtract x from every reactant regardless of coefficient. For A + 2B ⇌ C, changes are −x, −2x, and +x. A 5% check applies to every term simplified, not just one.')

add('3.1', [
 ('Solubility','The amount of a substance that can dissolve in a specified amount of solvent or solution at stated conditions.'),
 ('Saturated solution','A solution at the equilibrium solubility limit; with excess solid present, dissolution and crystallization balance.'),
 ('Electrolyte','A substance that produces mobile ions in solution and allows the solution to conduct electricity.')],
 'Dissolving an ionic solid separates its ions and surrounds them with water molecules. It does not destroy the ions. A soluble ionic compound is written as separated aqueous ions in a complete ionic equation; a precipitate, weak electrolyte, or pure liquid is left intact. Cancel identical spectator ions to obtain a net ionic equation. Use Table A3 to predict which compounds are soluble.',
 ['Molar solubility s = ndissolved / Vsolution', 'Mass solubility (g L⁻¹) = s × molar mass (g mol⁻¹)', 'Ag⁺(aq) + Cl⁻(aq) → AgCl(s)'],
 ['Start with a formula equation: AgNO₃(aq) + NaCl(aq) → AgCl(s) + NaNO₃(aq).',
 'Separate the soluble strong electrolytes into ions, retaining their coefficients and charges.',
 'Na⁺ and NO₃⁻ occur unchanged on both sides, so cancel them. The remaining ions and solid give the net ionic equation.',
 'For a solubility conversion, multiply mol L⁻¹ by g mol⁻¹. The mole units cancel and leave g L⁻¹.'],
 'If a salt of molar mass 100.0 g mol⁻¹ has molar solubility 2.0 × 10⁻³ mol L⁻¹, its mass solubility is 0.20 g L⁻¹. The amount of each dissolved ion then follows from the salt’s formula.',
 'Soluble does not mean infinitely soluble. Strong electrolyte describes dissociation of the amount that dissolves; it does not itself specify how much dissolves.')

add('3.2', [
 ('Qualitative analysis','Identifying which species are present, rather than measuring their amounts.'),
 ('Selective precipitation','Removing one ion as a precipitate under conditions that leave another ion dissolved.'),
 ('Confirmatory test','An additional characteristic reaction used to support an ion identification.')],
 'Choose reagents by comparing possible products with the solubility table. Add a reagent to a separate sample or follow a planned separation sequence. Filter a precipitate before testing the filtrate further. A precipitate shows that some compatible ion is present; when several ions could give that result, a second selective test is required. Record observations separately from inferences.',
 ['Ba²⁺(aq) + SO₄²⁻(aq) → BaSO₄(s)', 'Ag⁺(aq) + Cl⁻(aq) → AgCl(s)', 'Charge check: sum of reactant charges = sum of product charges'],
 ['List the candidate ions and all precipitates each possible reagent might form, using Table A3.',
 'Select a reagent that separates candidates. For example, if the only candidates are Ba²⁺ and Na⁺, sulfate can precipitate BaSO₄ while sodium remains dissolved.',
 'Write the net ionic equation and check atom and charge conservation. For BaSO₄, +2 + (−2) = 0, matching the neutral solid.',
 'Test or separate additional portions to resolve competing explanations. The reasoning derives from solubility rules and conservation, rather than a universal identification equation.'],
 'For a sample known to contain either NaCl or Na₂SO₄, adding Ba(NO₃)₂ gives BaSO₄(s) only for the sulfate candidate under suitable concentrations. The conclusion depends on the stated candidate list.',
 'A single white precipitate rarely identifies an unrestricted unknown. Reagent contamination, inadequate concentrations, or an unremoved earlier reagent can give misleading results.')

add('3.3', [
 ('Solubility product, Ksp','The equilibrium product of dissolved-ion concentration factors for dissolution of a sparingly soluble ionic solid.'),
 ('Molar solubility, s','Moles of formula units dissolved per litre of saturated solution.'),
 ('Common ion','An ion supplied by more than one dissolved source in the same equilibrium system.')],
 'Write a balanced dissolution equation before constructing Ksp. The solid is omitted, and ion coefficients become exponents. Relate each ion concentration to s through its coefficient. A common ion contributes an initial concentration and usually lowers solubility. Ksp and s are different quantities; comparing Ksp values alone can mis-rank solubilities when salt stoichiometries differ.',
 ['MₐXᵦ(s) ⇌ aM(aq) + bX(aq): Ksp = [M]ᵃ[X]ᵇ', 'In initially ion-free water: [M] = as; [X] = bs', 'Ksp = aᵃbᵇs^(a+b); for MX₂: Ksp = 4s³', 'MX₂ with initial [X] = C: Ksp = s(C + 2s)²'],
 ['Dissolving s mol L⁻¹ of formula units creates as mol L⁻¹ of M ions and bs mol L⁻¹ of X ions.',
 'Insert those concentrations into Ksp: (as)ᵃ(bs)ᵇ = aᵃbᵇs^(a+b). Ion charges are left out of the generic labels here; the actual dissolution equation must balance charge.',
 'For MX₂, one M and two X ions form, so Ksp = s(2s)² = 4s³. Therefore s = (Ksp/4)^(1/3).',
 'If X is already present at concentration C, add its contribution: [X]eq = C + 2s. If 2s is negligible relative to C, Ksp ≈ sC²; verify that approximation.'],
 'For a hypothetical MX₂ with Ksp = 4.0 × 10⁻¹², s = (10⁻¹²)^(1/3) = 1.0 × 10⁻⁴ M in pure water. Then [M] = 1.0 × 10⁻⁴ M and [X] = 2.0 × 10⁻⁴ M.',
 'These solubility relations assume no significant hydrolysis, complex formation, or other side reaction. Use free-ion concentrations, not the total analytical amount of an ion bound in other species.')

add('3.4', [
 ('Trial ion product, TIP or Qsp','The Ksp expression evaluated from current ion concentrations before a proposed precipitation change.'),
 ('Precipitation threshold','The condition Qsp = Ksp, at the onset of saturation.'),
 ('Dilution on mixing','The reduction in an ion’s concentration when its amount occupies the combined solution volume.')],
 'Before predicting a precipitate, calculate ion concentrations after mixing but before precipitation. Qsp > Ksp means precipitation is favoured; Qsp < Ksp means an unsaturated solution; Qsp = Ksp is the equilibrium threshold. The threshold also lets you calculate which ion precipitates first during a selective separation. The final amount of solid requires an additional stoichiometric and equilibrium calculation.',
 ['[ion]mixed = nion / Vtotal = cstock Vstock × ion coefficient / Vtotal', 'Qsp > Ksp: precipitation favoured; Qsp < Ksp: unsaturated', 'For MX(s) ⇌ M⁺ + X⁻: [X⁻]threshold = Ksp/[M⁺]'],
 ['Calculate moles of each relevant ion from each stock solution. Account for coefficients such as two chloride ions per CaCl₂ formula unit.',
 'Add the solution volumes when volume additivity is assumed. Divide each ion amount by that total volume.',
 'Insert the mixed concentrations into the ion product. Compare with Ksp for the same temperature.',
 'At the onset of MX precipitation, set [M⁺][X⁻] = Ksp and rearrange for the required added ion. Compare threshold values to predict the first precipitate.'],
 'Mix equal volumes of 1.0 × 10⁻⁴ M AgNO₃ and 1.0 × 10⁻⁴ M NaCl. Each ion is diluted to 5.0 × 10⁻⁵ M. Qsp = 2.5 × 10⁻⁹, exceeding Ksp(AgCl) ≈ 1.8 × 10⁻¹⁰ at 25 °C, so precipitation is favoured.',
 'Qsp predicts the initial tendency, not the final precipitate mass. After a precipitate forms, the remaining free ions must satisfy Ksp if equilibrium with the solid is reached.')

add('4.1', [
 ('Arrhenius acid / base','In water, an acid increases hydronium concentration and a base increases hydroxide concentration.'),
 ('Brønsted–Lowry acid / base','An acid donates a proton; a base accepts a proton.'),
 ('Conjugate pair / amphiprotic species','A conjugate acid–base pair differs by one H⁺; an amphiprotic species can donate or accept H⁺.')],
 'Track the actual proton transfer. The donor becomes its conjugate base, while the acceptor becomes its conjugate acid. Water can accept a proton from an acid or donate one to a base. Hydronium, H₃O⁺, represents protonated water; H⁺ is common shorthand in aqueous equations. A species’ role depends on its reaction partner.',
 ['HA + B ⇌ A⁻ + BH⁺', 'HA + H₂O ⇌ A⁻ + H₃O⁺', 'NH₃ + H₂O ⇌ NH₄⁺ + OH⁻'],
 ['Remove one H⁺ from the proposed acid. Its hydrogen count decreases by one and its charge decreases by +1, yielding the conjugate base.',
 'Add that same H⁺ to the proposed base. Its hydrogen count increases by one and its charge increases by +1, yielding the conjugate acid.',
 'For HA with water, the pairs are HA/A⁻ and H₃O⁺/H₂O. For ammonia with water, they are NH₄⁺/NH₃ and H₂O/OH⁻.',
 'Confirm that atoms and net charge balance. This constructs the proton-transfer equation from the definitions.'],
 'In HCO₃⁻ + H₂O ⇌ CO₃²⁻ + H₃O⁺, bicarbonate donates H⁺ and acts as an acid. In HCO₃⁻ + H₂O ⇌ H₂CO₃ + OH⁻, it accepts H⁺ and acts as a base.',
 'Conjugate partners differ by exactly one proton. CO₃²⁻ is not the immediate conjugate base of H₂CO₃; HCO₃⁻ is.')

add('4.2', [
 ('Strong / weak acid','A strong acid reacts essentially completely with water under usual dilute aqueous conditions; a weak acid establishes a partial-ionization equilibrium.'),
 ('Acid strength versus concentration','Strength describes ionization tendency; concentration describes the amount initially dissolved per volume.'),
 ('Ka / Kb','Equilibrium constants for proton donation to water / proton acceptance from water.')],
 'For comparable conditions, a larger Ka indicates a stronger acid and a smaller pKa. A stronger acid has a weaker conjugate base. Use Table A5 to compare proton donors and acceptors, then predict transfer toward the weaker acid–base pair. A low-solubility hydroxide can be strongly dissociated in the fraction that dissolves; solubility and base strength answer different questions.',
 ['Ka(HA) = [H₃O⁺][A⁻]/[HA]', 'Kb(B) = [BH⁺][OH⁻]/[B]', 'HA + B ⇌ A⁻ + BH⁺: K = Ka(HA)/Ka(BH⁺)'],
 ['Write HA + H₂O ⇌ A⁻ + H₃O⁺ and its Ka expression.',
 'Write BH⁺ + H₂O ⇌ B + H₃O⁺, then reverse it to consume the hydronium made by HA. Reversing takes the reciprocal of its Ka.',
 'Add the equations and cancel water and hydronium. The net reaction is HA + B ⇌ A⁻ + BH⁺.',
 'Multiplying the equilibrium expressions cancels [H₃O⁺] and gives K = Ka(HA)/Ka(BH⁺). A ratio above one favours proton transfer to B.'],
 'A 0.0010 M HCl solution is a dilute strong acid; 0.10 M acetic acid is a more concentrated weak acid. The words strong and concentrated cannot replace one another.',
 'Use the relevant stepwise Ka for a polyprotic acid. Do not assume every acidic hydrogen ionizes completely or that an acid’s formula directly gives its equilibrium [H₃O⁺].')

add('4.3', [
 ('Autoionization of water','Proton transfer between two water molecules, producing hydronium and hydroxide.'),
 ('Ion-product constant, Kw','The equilibrium product of hydronium and hydroxide concentration factors in the dilute aqueous convention.'),
 ('Neutral solution','An aqueous solution with equal hydronium and hydroxide concentrations.')],
 'Both H₃O⁺ and OH⁻ are present in aqueous solutions. Added acid raises one and suppresses the other; added base does the reverse. Neutrality means equality, not the absence of ions. Kw depends on temperature; 1.0 × 10⁻¹⁴ is the familiar value at 25 °C.',
 ['2H₂O(l) ⇌ H₃O⁺(aq) + OH⁻(aq)', 'Kw = [H₃O⁺][OH⁻] = 1.0 × 10⁻¹⁴ at 25 °C', 'Neutral water: [H₃O⁺] = [OH⁻] = √Kw', 'For a conjugate pair: KaKb = Kw'],
 ['Apply the equilibrium-expression rule to water autoionization. Pure liquid water is omitted, leaving the ion product Kw.',
 'In pure water, the ions form in equal amounts. Setting each concentration to x gives x² = Kw, hence x = √Kw = 1.0 × 10⁻⁷ M at 25 °C.',
 'For HA, write Ka = [H₃O⁺][A⁻]/[HA]. For its conjugate base, Kb = [HA][OH⁻]/[A⁻].',
 'Multiply: [HA] and [A⁻] cancel, leaving KaKb = [H₃O⁺][OH⁻] = Kw. Both constants must refer to the same conjugate pair and temperature.'],
 'If [H₃O⁺] = 2.0 × 10⁻³ M at 25 °C, then [OH⁻] = 1.0 × 10⁻¹⁴/(2.0 × 10⁻³) = 5.0 × 10⁻¹² M. The solution is acidic because hydronium exceeds hydroxide.',
 'Neutral pH is 7.00 only when pKw = 14.00. Very dilute added acid or base may require water’s contribution instead of assuming [H₃O⁺] or [OH⁻] equals the added concentration.')

add('4.4', [
 ('pH / pOH','Negative base-10 logarithms of hydronium / hydroxide activity; the school dilute-solution model substitutes numerical molar concentrations.'),
 ('pKw','The negative base-10 logarithm of Kw.'),
 ('Logarithmic scale','A scale in which one unit corresponds to a multiplicative factor of ten.')],
 'The logarithm compresses the large concentration range encountered in acid–base chemistry. Lower pH means greater hydronium activity. Use base-10 logarithms and keep enough digits until the final answer. The usual 0–14 classroom scale is not an absolute limit. The interactive model below uses the dilute-solution approximation at 25 °C.',
 ['pH ≈ −log₁₀([H₃O⁺]/c°); pOH ≈ −log₁₀([OH⁻]/c°)', '[H₃O⁺] ≈ c° × 10^(−pH); c° = 1 mol L⁻¹', 'pH + pOH = pKw = 14.00 at 25 °C', '[H₃O⁺]₁/[H₃O⁺]₂ ≈ 10^(pH₂ − pH₁)'],
 ['In the concentration convention, begin with Kw = [H₃O⁺][OH⁻], with standard-concentration factors implicit.',
 'Take −log₁₀ of both sides. The logarithm of a product is the sum of the logarithms, yielding pKw = pH + pOH.',
 'From pH = −log₁₀([H₃O⁺]/c°), reverse the logarithm with a power of ten to obtain [H₃O⁺] ≈ c°10^(−pH).',
 'For two solutions, divide their powers of ten. Subtracting exponents gives the concentration ratio.'],
 'At 25 °C, pH = 3.40 gives [H₃O⁺] ≈ 10⁻³·⁴⁰ = 4.0 × 10⁻⁴ M, pOH = 10.60, and [OH⁻] ≈ 2.5 × 10⁻¹¹ M. A pH 3 solution has 100 times the hydronium of a pH 5 solution.',
 'Do not average pH values when mixing solutions. React the acid and base amounts first, find the remaining concentration, and only then take the logarithm.')

add('4.5', [
 ('Formal concentration, C','The amount of acid or base introduced per litre before accounting for its equilibrium redistribution.'),
 ('Percent ionization','The fraction of the original acid molecules that ionize, expressed as a percentage.'),
 ('Weak-acid/base ICE model','A conservation table coupled to Ka or Kb to determine equilibrium concentrations.')],
 'For a weak monoprotic acid alone in water, let x be the hydronium formed. The same x of conjugate base forms and C − x of acid remains. A weak base gives an analogous hydroxide equation. For a base calculation, convert pOH to pH at the stated temperature. The square-root approximation needs a small ionized fraction and negligible contribution from water.',
 ['HA + H₂O ⇌ H₃O⁺ + A⁻: Ka = x²/(C − x)', 'x² + Ka x − Ka C = 0', 'x = (√(Ka² + 4KaC) − Ka)/2', 'If x ≪ C: [H₃O⁺] ≈ √(KaC); for B: [OH⁻] ≈ √(KbC)', 'Percent ionization = 100x/C'],
 ['Use the ICE concentrations C − x, x, and x. Insert them into Ka to give Ka = x²/(C − x).',
 'Multiply by C − x and collect terms to get the quadratic. The positive root gives the physically allowed x.',
 'If x is small relative to C, replace C − x by C, so x² ≈ KaC and x ≈ √(KaC).',
 'Check 100x/C ≤ 5% for this course shortcut. If it fails, solve the quadratic. If water, a common ion, or another ionization matters, construct the fuller equilibrium model.',
 'For a weak base, repeat with Kb and OH⁻, then calculate pOH = −log₁₀[OH⁻] and pH = pKw − pOH.'],
 'For 0.10 M HA with Ka = 1.8 × 10⁻⁵, x ≈ √(1.8 × 10⁻⁶) = 1.34 × 10⁻³ M. The change is 1.34%, so the approximation passes. pH ≈ 2.87.',
 'The quadratic is exact only within this single-equilibrium model. Neither it nor the square-root formula automatically accounts for water autoionization, multiple acidic protons, or nonideal solutions.')

add('5.1', [
 ('Salt hydrolysis','An acid–base reaction of a dissolved ion with water that produces hydronium or hydroxide.'),
 ('Spectator ion','An ion whose acid–base reaction with water is negligible in the problem’s model.'),
 ('Amphiprotic ion','An ion able to act as either a proton donor or a proton acceptor.')],
 'Dissociate the salt and assess its ions separately. The conjugate base of a weak acid can make a solution basic, while the conjugate acid of a weak base can make it acidic. Alkali-metal cations and conjugate bases of strong acids are usually spectators in this course. Some small highly charged hydrated metal ions are acidic. If both ions react, compare their acid and base constants rather than guessing from the word salt.',
 ['A⁻ + H₂O ⇌ HA + OH⁻; Kb(A⁻) = Kw/Ka(HA)', 'BH⁺ + H₂O ⇌ B + H₃O⁺; Ka(BH⁺) = Kw/Kb(B)', 'For one weakly hydrolyzing ion at concentration C: x ≈ √(KC)'],
 ['Identify the parent weak acid or weak base of the ion. Write the hydrolysis reaction explicitly.',
 'Use KaKb = Kw to obtain the ion’s hydrolysis constant from its conjugate partner’s constant.',
 'If the reacting ion starts at C with negligible initial product, its ICE concentrations give K = x²/(C − x).',
 'When x ≪ C, use x ≈ √(KC), verify the approximation, and calculate pH from the hydronium or hydroxide produced.'],
 'For 0.10 M sodium acetate, Na⁺ is a spectator and acetate accepts a proton from water. With Ka(acetic acid) = 1.8 × 10⁻⁵, Kb = 5.6 × 10⁻¹⁰ and [OH⁻] ≈ 7.5 × 10⁻⁶ M. At 25 °C, pH ≈ 8.87.',
 'A neutralization reaction need not leave a neutral solution. For amphiprotic ions such as HCO₃⁻, consider both proton donation and acceptance; one square-root calculation alone may be insufficient.')

add('5.2', [
 ('Buffer','A solution that resists pH changes when relatively small amounts of strong acid or base are added.'),
 ('Conjugate buffer pair','A weak acid and its conjugate base, both present in appreciable amounts.'),
 ('Buffer capacity','The amount of added acid or base a buffer can absorb before its pH changes substantially.')],
 'The conjugate base consumes added acid, while the weak acid consumes added base. Do the neutralization stoichiometry before applying the equilibrium relation. The acid/base ratio mainly determines pH; their total amounts determine how much added reagent the buffer can accommodate. Diluting both components by the same factor changes their ratio little, but lowers capacity and eventually makes other contributions important.',
 ['A⁻ + H₃O⁺ → HA + H₂O; HA + OH⁻ → A⁻ + H₂O', 'Ka = [H₃O⁺][A⁻]/[HA]', 'pH ≈ pKa + log₁₀([A⁻]/[HA])', 'After neutralization in one volume: [A⁻]/[HA] = n(A⁻)/n(HA)'],
 ['Rearrange the acid equilibrium expression to [H₃O⁺] = Ka[HA]/[A⁻].',
 'Take −log₁₀. The result is pH ≈ pKa + log₁₀([A⁻]/[HA]), the concentration form of the buffer relation.',
 'After an added strong acid or base reacts, update the amounts of both components. Their common final volume cancels from the ratio.',
 'Use those amounts only if both buffer components remain and their further equilibrium changes are small. A useful working range is roughly 0.1 ≤ [A⁻]/[HA] ≤ 10.'],
 'A buffer starts with 0.100 mol HA and 0.100 mol A⁻, with pKa = 4.76. Adding 0.010 mol HCl leaves 0.110 mol HA and 0.090 mol A⁻. pH ≈ 4.76 + log₁₀(0.090/0.110) = 4.67.',
 'A strong acid–strong base mixture is not a buffer. If one component is exhausted, use excess strong reagent or the appropriate remaining-species equilibrium instead of the buffer equation.')

add('5.3', [
 ('Titration','Determining an amount by measuring the volume of a known-concentration reagent needed for a stoichiometric reaction.'),
 ('Titrant / analyte','The measured reagent added from the burette / the sample being analyzed.'),
 ('Equivalence point / endpoint','The stoichiometric completion point / the observed signal used to stop the titration.')],
 'A suitable titration reaction has known stoichiometry, proceeds rapidly and essentially completely, and has a detectable completion signal. Read delivered volume as final minus initial burette reading. Use the balanced equation to connect moles, then calculate the unknown concentration. An indicator endpoint approximates the equivalence point; their difference can cause systematic error.',
 ['ndelivered = ctitrant(Vfinal − Vinitial)', 'For aA + bB → products at equivalence: nA/a = nB/b', 'cAVA/a = cBVB/b', 'For a monoprotic acid with a monohydroxide base: cAVA = cBVB'],
 ['Convert the delivered titrant volume to litres if concentration is in mol L⁻¹, and multiply by concentration to find moles.',
 'The balanced equation states that a mol A react with b mol B. Dividing each reacting amount by its coefficient gives equal reaction amounts at equivalence.',
 'Substitute n = cV for each species and isolate the unknown concentration.',
 'For a pure dilution, conservation gives c₁V₁ = c₂V₂ instead. Its similar appearance must not hide the different reason: dilution conserves one solute, whereas titration uses a reaction ratio.'],
 'A 25.00 mL HCl sample requires 20.00 mL of 0.1000 M NaOH. The 1:1 reaction gives n(HCl) = 0.1000 × 0.02000 = 0.002000 mol, so c(HCl) = 0.002000/0.02500 = 0.08000 M.',
 'Do not use cAVA = cBVB for every acid/base formula. For H₂SO₄ + 2NaOH → Na₂SO₄ + 2H₂O at full neutralization, n(NaOH) = 2n(H₂SO₄).')

add('5.4', [
 ('Titration curve','A graph of pH against the amount or volume of titrant added.'),
 ('Half-equivalence point','For a monoprotic weak acid titrated with strong base, the point where half the initial acid has been neutralized.'),
 ('Acid–base indicator','A weak acid or base whose conjugate forms have different colours.')],
 'Choose the pH calculation by the species present. Initially use the original acid or base model. Before equivalence in a weak-acid/strong-base titration, use the remaining acid and formed conjugate base. At equivalence, use the salt’s hydrolysis. After equivalence, excess strong titrant usually controls pH. For strong acid with strong base, the equivalence solution is neutral; a weak-acid/strong-base equivalence is basic, and a weak-base/strong-acid equivalence is acidic.',
 ['Before equivalence: pH ≈ pKa + log₁₀[n(A⁻)/n(HA)]', 'At half-equivalence: n(A⁻) = n(HA), so pH ≈ pKa', 'After excess strong base: [OH⁻] ≈ nexcess(OH⁻)/Vtotal', 'HIn + H₂O ⇌ H₃O⁺ + In⁻: pH ≈ pKa,In + log₁₀([In⁻]/[HIn])'],
 ['For an initial n₀ of HA and added n of OH⁻ before equivalence, neutralization leaves n₀ − n of HA and forms n of A⁻.',
 'At n = n₀/2 the two amounts are equal. Their ratio is one, log₁₀1 = 0, and the buffer relation gives pH ≈ pKa.',
 'At equivalence no appreciable original HA remains after stoichiometry, so use A⁻ hydrolysis with Kb = Kw/Ka and the diluted salt concentration.',
 'The indicator expression is the same acid equilibrium rearrangement. If its visible colour transition corresponds roughly to ratios 0.1–10, its transition range is approximately pKa,In ± 1. Choose an indicator whose range lies inside the curve’s steep region.'],
 'For 25.0 mL of 0.100 M HA titrated with 0.100 M NaOH, equivalence occurs at 25.0 mL. At 12.5 mL, pH ≈ pKa. At equivalence, [A⁻] ≈ 0.00250 mol/0.0500 L = 0.0500 M, which is the concentration used for hydrolysis.',
 'Equivalence does not always mean pH 7, and endpoint does not mean exact equivalence. All concentrations after mixing must use total volume.')

add('5.5', [
 ('Basic anhydride','An oxide that forms a base on reaction with water; commonly a reactive metal oxide.'),
 ('Acidic anhydride','An oxide that forms an acid on reaction with water; commonly a non-metal oxide.'),
 ('Acid deposition','Acidic material deposited from the atmosphere, including acids formed from sulfur and nitrogen oxides.')],
 'Reactive ionic metal oxides often generate hydroxide in water; many covalent non-metal oxides generate acids. Predict the acid or base product, balance atoms, then consider dissociation or ionization. CO₂ forms a weak carbonic-acid system; sulfur and nitrogen oxide chemistry can produce stronger environmental acidity. Some oxides are insoluble, unreactive, neutral, or amphoteric, so use these as trends rather than rules without exceptions.',
 ['Na₂O + H₂O → 2NaOH', 'O²⁻ + H₂O → 2OH⁻', 'SO₃ + H₂O → H₂SO₄', 'CO₂ + H₂O ⇌ H₂CO₃; H₂CO₃ + H₂O ⇌ H₃O⁺ + HCO₃⁻'],
 ['Oxide ion is a strong proton acceptor. Transferring one H⁺ from water to O²⁻ creates OH⁻ from the oxide and another OH⁻ from the water.',
 'The net ionic equation is O²⁻ + H₂O → 2OH⁻. Adding the sodium spectator ions gives the balanced Na₂O reaction.',
 'For SO₃, adding one H₂O supplies two H and one more O, giving H₂SO₄. Its aqueous ionization then produces hydronium.',
 'Separate oxide hydration from acid ionization. Formation of an acid formula does not imply that every resulting acid ionizes completely.'],
 'One mole of Na₂O that reacts completely produces two moles of NaOH. If 0.0100 mol reacts and the final volume is 1.00 L, [OH⁻] ≈ 0.0200 M. At 25 °C, pOH = 1.70 and pH = 12.30.',
 'Do not assume every metal oxide dissolves or every non-metal oxide is acidic. For example, some metal oxides are amphoteric and carbon monoxide is not a typical acid-forming oxide.')

add('6.1', [
 ('Oxidation / reduction','Oxidation is electron loss and an increase in oxidation number; reduction is electron gain and a decrease in oxidation number.'),
 ('Oxidizing / reducing agent','The oxidizing agent accepts electrons and is reduced; the reducing agent supplies electrons and is oxidized.'),
 ('Oxidation number','A formal electron-accounting number assigned by agreed rules; it is not generally an atom’s actual charge in a covalent molecule.')],
 'Oxidation and reduction occur together because electrons lost must equal electrons gained. An element in its elemental form has oxidation number zero; a monatomic ion’s oxidation number equals its charge. Oxidation numbers sum to the overall species charge. Oxygen is usually −2, with exceptions such as peroxides; hydrogen is usually +1, except in metal hydrides.',
 ['Σ(number of atoms × oxidation number) = net species charge', 'Zn → Zn²⁺ + 2e⁻; Cu²⁺ + 2e⁻ → Cu', 'Net: Zn + Cu²⁺ → Zn²⁺ + Cu'],
 ['Assign the known oxidation numbers and use the net charge to solve for an unknown one.',
 'Compare an element before and after reaction. An increase means formal electron loss; a decrease means formal electron gain.',
 'Write electrons on the product side for oxidation and on the reactant side for reduction.',
 'Add matched half-reactions and cancel electrons. The species losing electrons is the reducing agent, and the species gaining them is the oxidizing agent.'],
 'In MnO₄⁻, let Mn be x. Then x + 4(−2) = −1, so x = +7. Conversion to Mn²⁺ lowers its oxidation number by five and requires five electrons per manganese atom.',
 'The oxidizing agent is reduced. Do not swap the agent’s effect on another species with the change the agent itself undergoes.')

add('6.2', [
 ('Half-reaction','An equation showing either the oxidation or reduction part of a redox process, including electrons.'),
 ('Electron balance','Equality of the total electrons lost and gained in the overall reaction.'),
 ('Acidic / basic balancing medium','The stated environment that determines whether H⁺ or OH⁻ may remain in the final equation.')],
 'Balance each half-reaction for atoms and charge before combining them. In acid, balance oxygen with H₂O, hydrogen with H⁺, and charge with electrons. Multiply to equalize electrons, add, and cancel. For basic solution, add OH⁻ to both sides to eliminate any H⁺, combine H⁺ with OH⁻ into water, and cancel excess water.',
 ['MnO₄⁻ + 8H⁺ + 5e⁻ → Mn²⁺ + 4H₂O', 'Fe²⁺ → Fe³⁺ + e⁻', 'MnO₄⁻ + 8H⁺ + 5Fe²⁺ → Mn²⁺ + 4H₂O + 5Fe³⁺'],
 ['Balance Mn first. Four oxygen atoms on the left require four H₂O on the right.',
 'Those four waters contain eight H, so add eight H⁺ on the left. The left charge is now +7 and the right charge +2.',
 'Add five electrons to the left to reduce +7 to +2. The reduction half-reaction now conserves both atoms and charge.',
 'Multiply Fe²⁺ → Fe³⁺ + e⁻ by five, add the equations, and cancel five electrons.',
 'Check the final equation: left charge −1 + 8 + 10 = +17; right charge +2 + 15 = +17. All atom counts also match.'],
 'For chlorine disproportionation in base, the balanced net equation is Cl₂ + 2OH⁻ → Cl⁻ + ClO⁻ + H₂O. Chlorine changes from 0 to −1 and +1, so equal electron loss and gain occur within the same starting species.',
 'Use the reaction products specified by the question; balancing does not predict which products actually form. Never change subscripts to balance an equation, and leave no uncancelled electrons in a complete redox reaction.')

add('6.3', [
 ('Standard reduction potential, E°red','A half-cell potential measured relative to the standard hydrogen electrode under specified standard conditions.'),
 ('Standard cell potential, E°cell','The difference between the reduction potentials of the cathode and anode half-cells.'),
 ('Spontaneous redox direction','The direction that can operate as a galvanic cell under the specified conditions.')],
 'Table A7 writes half-reactions as reductions. A more positive reduction potential indicates a greater reduction tendency under the tabulated conditions. Choose the species available, keep the reduction half-reaction, reverse the oxidation half-reaction, and balance electrons. A positive E°cell indicates a thermodynamically favourable direction at standard conditions; the rate may still be slow.',
 ['E°cell = E°red(cathode) − E°red(anode)', 'Equivalently: E°cell = E°reduction + E°oxidation', '1 V = 1 J C⁻¹; do not multiply E° by a balancing coefficient'],
 ['Both tabulated values are reduction potentials measured against the same reference electrode.',
 'The cathode carries out the chosen reduction. The anode carries out the reverse of its tabulated reduction, changing the sign of that contribution.',
 'Adding the reduction and oxidation contributions therefore gives a difference of reduction potentials.',
 'Voltage is energy per charge. Doubling a reaction doubles both transferred charge and associated energy, leaving their ratio unchanged. Thus electron-balancing coefficients do not multiply E°.'],
 'For Cu²⁺/Cu at +0.34 V and Zn²⁺/Zn at −0.76 V, Zn oxidation paired with Cu²⁺ reduction gives E°cell = 0.34 − (−0.76) = +1.10 V. Reversing the overall reaction gives −1.10 V.',
 'The ° symbol specifies standard conditions, not every possible mixture. Concentrations and reaction conditions can alter the actual voltage and direction; use the textbook’s stated conditions and notes on Table A7.')

add('6.4', [
 ('Electrochemical / galvanic cell','A device that converts energy from a spontaneous redox reaction into electrical energy.'),
 ('Anode / cathode','The electrode where oxidation / reduction occurs.'),
 ('Salt bridge','An ionic connection that completes the internal circuit and helps maintain bulk electrical neutrality.')],
 'Separate the half-reactions so electrons travel through an external wire from anode to cathode. Ions, rather than electrons, carry current through the solution and salt bridge. In a galvanic cell, the anode is negative and the cathode positive. A metal anode can lose mass as it dissolves; a metal-ion cathode can gain mass as metal plates out. An inert electrode provides a conducting surface when the reacting species are not a solid metal electrode.',
 ['Zn(s) | Zn²⁺(aq) || Cu²⁺(aq) | Cu(s)', 'Anode: Zn → Zn²⁺ + 2e⁻; cathode: Cu²⁺ + 2e⁻ → Cu', 'Electron flow in the wire: anode → cathode'],
 ['Oxidizing one Zn atom creates Zn²⁺ in the anode solution and releases two electrons to the wire.',
 'At the cathode, Cu²⁺ accepts those electrons and deposits as copper metal.',
 'Without ion migration, the anode compartment becomes more positively charged and the cathode compartment loses positive charge. That charge separation opposes further current.',
 'For this cell, salt-bridge anions migrate toward the anode compartment and cations toward the cathode compartment. This balances ionic charge without transporting electrons through the bridge.'],
 'If 0.010 mol Zn dissolves in an ideal Zn/Cu cell, 0.020 mol electrons pass through the external circuit and 0.010 mol Cu deposits. The anode loses zinc mass and the cathode gains copper mass.',
 'Anode always means oxidation and cathode always means reduction. Their signs change in an electrolytic cell; memorizing only electrode signs leads to errors.')

add('6.5', [
 ('Electrolysis / electrolytic cell','An externally powered redox process / the apparatus driving that process.'),
 ('Current, I','The rate of electric charge flow, measured in amperes: 1 A = 1 C s⁻¹.'),
 ('Faraday constant, F','The magnitude of charge per mole of electrons, approximately 96485 C mol⁻¹.'),
 ('Overpotential','Additional electrode potential needed in practice to drive a reaction at an appreciable rate.')],
 'An external supply drives a redox direction that would not run as the chosen spontaneous cell. Oxidation remains at the anode and reduction at the cathode; for a simple electrolytic cell the anode is positive and the cathode negative. In molten salts, the ions are the available reactants. In aqueous electrolysis, water can compete with solute ions; reactive electrodes and overpotential can also change which products form. Use the book’s Table A7 notes when comparing these candidates.',
 ['Qcharge = It for constant current; n(e⁻) = Qcharge/F', 'Mᶻ⁺ + ze⁻ → M: n(M) = It/(zF)', 'Deposited mass m = It × molar mass/(zF)', 'Molten NaCl: 2Na⁺ + 2e⁻ → 2Na; 2Cl⁻ → Cl₂ + 2e⁻'],
 ['The definition of constant current is I = Qcharge/t, so Qcharge = It. Here Qcharge is electric charge, not the reaction quotient Q.',
 'Divide the charge by F to convert coulombs to moles of electrons.',
 'Read the balanced half-reaction: z mol electrons deposit one mole of metal. Divide by z to find moles of metal.',
 'Multiply by the molar mass to obtain grams. This gives m = ItM/(zF), assuming the stated current deposits that metal with 100% current efficiency.',
 'For molten NaCl, add the two half-reactions and cancel electrons, giving 2NaCl(l) → 2Na + Cl₂. Aqueous NaCl requires considering water and does not give the same cathode product.'],
 'For Cu²⁺ + 2e⁻ → Cu at 1.00 A for 600 s, Qcharge = 600 C, n(e⁻) = 600/96485 = 0.00622 mol, n(Cu) = 0.00311 mol, and m(Cu) = 0.1976 g using 63.55 g mol⁻¹.',
 'Use seconds for time and include the electron coefficient. Real deposition can be lower because of competing reactions. A thermodynamic minimum voltage alone does not include overpotential or electrical resistance.')

# Keep the six useful models from the existing tutorial, placed within their matching PDF sections.
class ExtractModels(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=False)
        self.lines = OLD.splitlines(keepends=True)
        self.offsets = [0]
        for line in self.lines: self.offsets.append(self.offsets[-1] + len(line))
        self.stack = []
        self.models = []
    def source_position(self):
        line, col = self.getpos()
        return self.offsets[line-1] + col
    def handle_starttag(self, tag, attrs):
        if tag in {'area','base','br','col','embed','hr','img','input','link','meta','param','source','track','wbr'}: return
        self.stack.append((tag, self.source_position(), dict(attrs).get('class') == 'lab'))
    def handle_endtag(self, tag):
        if not self.stack: return
        assert self.stack[-1][0] == tag, (tag, self.stack[-1], self.getpos())
        _, start, wanted = self.stack.pop()
        if wanted: self.models.append(OLD[start:self.source_position()+len(tag)+3])

extractor = ExtractModels()
extractor.feed(OLD)
assert len(extractor.models) == 6
models = dict(zip(['1.3','2.5','3.4','4.4','5.2','6.4'], extractor.models))

quiz = [
 [('For 2A → B, A disappears at 0.040 M s⁻¹. What is the B formation rate?', ['0.020 M s⁻¹','0.040 M s⁻¹','0.080 M s⁻¹'],0,'One mole of B forms for every two moles of A consumed, so its formation rate is half the A disappearance rate.'),
  ('Which change does a catalyst make?', ['It changes ΔH.','It provides another reaction pathway.','It increases the equilibrium constant.'],1,'A catalyst provides a faster pathway and is regenerated. It leaves the reaction endpoints and equilibrium constant unchanged.'),
  ('Doubling [A] at fixed [B] quadruples the rate. What is the order in A?', ['Zero','First','Second'],2,'The rate ratio is 4 = 2ᵐ, so m = 2.')],
 [('What is equal at dynamic equilibrium?', ['Reactant and product concentrations','Forward and reverse rates','Initial and final amounts'],1,'Equal opposing rates give no net composition change; concentrations need not be equal.'),
  ('At a fixed temperature, Q < K. What is the net direction?', ['Toward products','Toward reactants','No net reaction'],0,'Forward conversion raises the product-to-reactant quotient until Q reaches K.'),
  ('Which change can alter K for a specified reaction?', ['Adding a catalyst','Adding a reactant at fixed temperature','Changing temperature'],2,'Temperature changes K. Concentration changes alter Q, while a catalyst changes the rate of approach.')],
 [('MX₂(s) ⇌ M²⁺ + 2X⁻ in initially ion-free water. Which relation holds?', ['Ksp = s²','Ksp = 4s³','Ksp = 2s²'],1,'The ions have concentrations s and 2s, so their product is s(2s)² = 4s³.'),
  ('After mixing, Qsp > Ksp. What is favoured?', ['Precipitation','Further dissolution only','No net change'],0,'Precipitation lowers the ion product toward Ksp.'),
  ('Equal volumes of two ion solutions are combined. Before precipitation, each ion concentration is…', ['Unchanged','Doubled','Halved, if present in only one starting solution'],2,'Its amount now occupies twice its original volume.')],
 [('What is the immediate conjugate base of H₂CO₃?', ['HCO₃⁻','CO₃²⁻','H₃CO₃⁺'],0,'Removing exactly one H⁺ produces HCO₃⁻.'),
  ('For a conjugate pair at the same temperature, KaKb equals…', ['Ka + Kb','Kw','1 in every case'],1,'Multiplying the two equilibrium expressions cancels the acid and conjugate-base factors, leaving Kw.'),
  ('For a weak monoprotic acid alone in water, when is √(KaC) a useful estimate?', ['For every concentration','Only for strong acids','When ionization is small and water contributes negligibly'],2,'The estimate replaces C − x by C and neglects water’s contribution; check both assumptions.')],
 [('At equivalence in a weak-acid/strong-base titration at 25 °C, the solution is usually…', ['Acidic','Neutral','Basic'],2,'The conjugate base formed by neutralization hydrolyzes to produce OH⁻.'),
  ('A buffer has equal equilibrium concentrations of HA and A⁻. Its pH is approximately…', ['pKa','7 in every case','pKw'],0,'The concentration ratio is one, so the logarithmic term is zero.'),
  ('A monoprotic weak acid is half-neutralized by a strong base. Which species form the buffer?', ['Only strong base','Remaining HA and formed A⁻','Only water'],1,'Half the acid remains and half has become its conjugate base.')],
 [('Which statement always defines the anode?', ['It is positive.','Oxidation occurs there.','Reduction occurs there.'],1,'Oxidation defines the anode in both galvanic and electrolytic cells; its sign depends on cell type.'),
  ('When balancing electrons, what happens to tabulated E° values?', ['They are not multiplied by coefficients.','They are multiplied by electron counts.','They are all made positive.'],0,'Potential is energy per charge and does not scale with the amount of reaction.'),
  ('For M²⁺ + 2e⁻ → M, 0.020 mol electrons deposit how much M at full efficiency?', ['0.040 mol','0.020 mol','0.010 mol'],2,'Divide the moles of electrons by the coefficient two.')]
]

def pdf_link(start, end=None, label=None):
    label = label or (f'Textbook pp. {start}–{end}' if end and end != start else f'Textbook p. {start}')
    return f'<a href="output/pdf/Chemistry12-navigable.pdf#page={start+10}" target="_blank" rel="noopener">{escape(label)} <span aria-hidden="true">↗</span></a>'

ids = ['kinetics','equilibrium','solubility','acid-base-1','acid-base-2','electrochemistry']
intro = [
 'Measure change, explain effective collisions, and connect energy diagrams to reaction pathways.',
 'Follow a reversible system from dynamic balance to equilibrium expressions and calculations.',
 'Identify ions, quantify solubility, and predict precipitation after mixing.',
 'Follow proton transfer, define acidity, and calculate weak-acid and weak-base equilibria.',
 'Use acid–base equilibria to explain salts, buffers, titrations, and oxides in water.',
 'Balance electron transfer, predict redox direction, and explain galvanic and electrolytic cells.'
]

# Reuse the established page palette and model styles; the new course layout is below.
base_css = OLD.split('<style>',1)[1].split('/* Tutor explanations:',1)[0]
css = base_css + '''
.sidebar{width:290px;padding:25px 20px}.shell{margin-left:290px}.content{max-width:1150px;padding-top:34px}.sidebar nav{gap:12px}.sidebar nav a{display:block;padding:7px 8px;line-height:1.45}.nav-chapter{font-size:12px}.nav-chapter>summary{cursor:pointer;font-weight:650;list-style:none;display:flex;gap:9px;align-items:baseline;line-height:1.5;padding:8px}.nav-chapter>summary:before{content:'+';color:var(--orange);width:9px;flex:none}.nav-chapter[open]>summary:before{content:'−'}.nav-sections{margin-left:14px;padding-left:10px;border-left:1px solid var(--border)}.nav-sections a{font-size:11px;font-weight:400}.nav-sections b{color:var(--orange);font-weight:500;margin-right:5px}.side-foot{font-size:10px}.side-progress{margin-top:24px}.topbar{height:70px}.top-actions{flex-wrap:wrap}.hero{display:block;padding:5px 0 28px}.hero h1{font-size:clamp(40px,5vw,62px);max-width:760px;letter-spacing:-2px}.hero p{max-width:680px;font-size:14px}.hero-actions{flex-wrap:wrap}.stats{gap:25px}.source-pill{display:inline-block;border:1px solid var(--border);border-radius:7px;padding:7px 12px;font-size:12px;text-decoration:none}.contents-grid{display:grid;grid-template-columns:1fr 1fr;gap:15px}.contents-card{background:#fff;border:1px solid var(--border);border-radius:12px;padding:22px}.contents-card h3{font-size:16px;line-height:1.5;margin-bottom:15px}.contents-card h3 a{text-decoration:none}.contents-card ol{list-style:none;padding:0;margin:0}.contents-card li a{display:grid;grid-template-columns:26px 1fr auto;gap:7px;align-items:baseline;text-decoration:none;font-size:12px;padding:8px 0;border-top:1px solid #eef0e9}.contents-card li a:hover .toc-label{text-decoration:underline}.toc-num{color:var(--orange);font-size:11px}.toc-page{color:var(--muted);font-size:10px}.reading-note{padding:16px 19px;background:var(--soft);font-size:12px;border-radius:8px;margin:20px 0}.reading-note p{margin:0}.chapter{border-top:1px solid var(--border);margin-top:45px;padding-top:32px;scroll-margin-top:90px}.chapter-head{display:flex;gap:18px;align-items:flex-start;margin-bottom:18px}.chapter-head .big-num{font-size:38px}.chapter-head h2{font:400 32px/1.2 Georgia,serif;letter-spacing:-.6px;margin:3px 0 9px}.chapter-head p{font-size:13px;color:var(--muted);max-width:650px;margin-bottom:9px}.source-link{font-size:11px}.chapter-tools{display:flex;gap:12px;align-items:center;justify-content:space-between;flex-wrap:wrap;margin:20px 0}.chapter-tools button{font-size:11px}.lesson{scroll-margin-top:90px}.lesson>summary{align-items:baseline;padding:18px 20px;line-height:1.5}.lesson>summary h3{font-size:15px;margin:0;font-weight:650;flex:1}.lesson-index{white-space:nowrap}.page-label{font-size:10px;font-weight:400;color:var(--muted);white-space:nowrap}.lesson-body{max-width:none;padding:22px 26px}.lesson-source{font-size:11px;color:var(--muted);margin-bottom:24px}.lesson-body h4{font-size:11px;letter-spacing:1.2px;text-transform:uppercase;margin:26px 0 12px;color:var(--green)}.lesson-body h4:first-of-type{margin-top:0}.definition-list{margin:0;display:grid;grid-template-columns:1fr 1fr;gap:12px}.definition-list>div{padding:13px 15px;background:var(--bg);border:1px solid #e8ebe3;border-radius:7px}.definition-list dt{font-size:12px;font-weight:700;margin-bottom:5px}.definition-list dd{font-size:12px;line-height:1.75;margin:0;color:#50645a}.concept{font-size:14px;line-height:1.85;max-width:790px}.equation{font-size:13px;line-height:1.9;margin:0}.equation-line+.equation-line{border-top:1px solid #dce6d3;margin-top:8px;padding-top:8px}.derivation-steps{padding-left:23px;font-size:13px;line-height:1.85;margin:0}.derivation-steps li{padding-left:6px;margin:10px 0}.worked-check{background:#edf3e8;border-radius:8px;margin-top:24px;padding:17px 19px;font-size:13px}.worked-check h4{margin-top:0;margin-bottom:8px}.worked-check p{margin-bottom:0}.trap{line-height:1.8}.section-links{display:flex;justify-content:space-between;gap:14px;margin-top:22px;font-size:11px}.section-links a{text-decoration:none}.quiz{margin-bottom:24px}.quiz legend{font-size:13px}.quiz>p{font-size:12px}.lab{margin-top:25px}.appendix{margin-top:45px;border-top:1px solid var(--border);padding-top:30px;scroll-margin-top:90px}.appendix h2{font:32px Georgia,serif}.table-wrap{overflow-x:auto;border:1px solid var(--border);border-radius:10px;background:#fff}table{width:100%;border-collapse:collapse;font-size:12px}th,td{text-align:left;padding:13px 16px;border-bottom:1px solid var(--border);vertical-align:top}th{font-size:10px;letter-spacing:1px;text-transform:uppercase;background:var(--soft)}tr:last-child td{border-bottom:0}.footer{font-size:11px}.empty{font-size:14px}.search-status{font-size:12px;color:var(--muted)}.chapter[hidden],.lesson[hidden]{display:none!important}.review-count{font-size:11px;color:var(--muted)}.equation:focus-visible{outline:3px solid var(--orange);outline-offset:3px}.sidebar-top{font-size:12px}.complete-label{font-size:12px}
@media(max-width:1100px){.sidebar{width:260px}.shell{margin-left:260px}.topbar{padding:0 4%}.top-actions{margin-left:0}.contents-grid{grid-template-columns:1fr}.breadcrumb{display:none}}
@media(max-width:760px){.sidebar{width:285px}.shell{margin-left:0}.topbar{height:auto;min-height:65px;gap:10px;padding:12px 16px}.top-actions{margin-left:auto;flex-wrap:nowrap}.search{width:145px}.content{padding:26px 18px 45px}.hero h1{font-size:43px}.hero{padding-top:0}.hero-actions{gap:10px}.stats{gap:15px;font-size:10px}.chapter-head h2{font-size:28px}.chapter-head{gap:12px}.chapter-head .big-num{font-size:30px}.lesson>summary{gap:9px;padding:15px}.lesson>summary h3{font-size:13px}.lesson-body{padding:18px}.definition-list{grid-template-columns:1fr}.contents-card{padding:18px}.page-label{display:none}.section-links{flex-wrap:wrap}.chapter-tools{gap:10px}.equation{font-size:12px}.lab .controls input[type=range]{width:100%;max-width:220px}.contents-card li a{font-size:11px}.footer{gap:15px}.chapter{scroll-margin-top:88px}}
@media(max-width:380px){.top-actions button{font-size:10px;padding:8px}.search{width:122px}.stats{flex-wrap:wrap;gap:8px 15px}.hero h1{font-size:38px}}
@media print{.sidebar,.topbar,.chapter-tools,.section-links,.contents-grid,.search-status,.quiz,.lab,.hero-actions,.footer button,.reading-note{display:none!important}.shell{margin:0}.content{max-width:none;padding:0}.chapter{break-before:page;border:0;margin:0;padding-top:0}.hero h1{font-size:28pt}.lesson[open]>summary{border-bottom:1px solid #ccc}.lesson{border-color:#bbb}.lesson-body{padding:14px}.definition-list{grid-template-columns:1fr 1fr}.worked-check,.definition-list>div{break-inside:avoid}.equation{font-size:9pt;cursor:default}.lesson[hidden],.chapter[hidden],.appendix[hidden],#overview[hidden]{display:block!important}.page-label{display:block}.appendix{break-before:page}a{color:#000}.lesson-source a:after{content:none}}
'''

html = ['<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><meta name="theme-color" content="#235b47"><meta name="description" content="Chemistry 12 tutorial organized by all 30 sections of the BC Science Chemistry 12 PDF, with definitions, concepts, equations, step-by-step derivations, worked examples, and interactive models."><title>Chemistry 12 — Textbook study companion</title><style>', css, '</style></head><body><a class="skip" href="#main">Skip to tutorial</a><button class="backdrop" id="backdrop" aria-label="Close navigation"></button>']
html.append('<aside class="sidebar" id="sidebar" aria-label="Textbook table of contents"><a class="brand" href="#overview"><span class="brand-icon" aria-hidden="true">C</span> Chemistry 12</a><div class="eyebrow">Textbook contents</div><nav><a class="sidebar-top active" href="#overview">Course contents</a>')
for i,(title,p,sections) in enumerate(chapters):
    html.append(f'<details class="nav-chapter" {"open" if i==0 else ""}><summary>{escape(title)}</summary><div class="nav-sections"><a href="#{ids[i]}">Chapter overview</a>')
    for name,start in sections:
        num, label = name.split(' ',1)
        html.append(f'<a href="#section-{num.replace(".","-")}"><b>{num}</b> {escape(label)}</a>')
    html.append('</div></details>')
html.append('<a class="sidebar-top" href="#appendix">Appendix — Reference Tables</a></nav><div class="side-progress"><p><strong>Chapter review progress</strong></p><progress id="courseProgress" max="6" value="0" aria-label="Chapters reviewed"></progress><p id="progressText">0 of 6 chapters reviewed</p><small id="storageNote">Saved in this browser.</small></div><div class="side-foot">Structure follows the PDF’s contents, p. v.<br>'+pdf_link(-3,label='Open the PDF table of contents')+'<br>Page labels in the tutorial refer to printed textbook pages.</div></aside>')
html.append('<div class="shell"><header class="topbar"><button class="mobile-toggle" id="menuBtn" aria-controls="sidebar" aria-expanded="false" aria-label="Open navigation">☰</button><div class="breadcrumb">BC Science / <strong>Chemistry 12</strong></div><div class="top-actions"><input class="search" id="search" type="search" aria-label="Search definitions, concepts, and equations" placeholder="Search this tutorial…"><button type="button" id="printBtn">Print / PDF</button></div></header><main class="content" id="main"><section id="overview" aria-labelledby="course-title"><div class="hero"><span class="tag"><span class="dot"></span> BC Science Chemistry 12</span><h1 id="course-title">Follow the book.<br><em>Understand the chemistry.</em></h1><p>One study path, in the exact order of the textbook’s table of contents. Start with definitions, connect the concepts, then build each equation through algebra, conservation, or a clearly stated model.</p><div class="hero-actions"><a class="primary source-pill" href="#section-1-1">Start with section 1.1 →</a>'+pdf_link(-3,label='Open PDF contents')+'</div><div class="stats"><span><strong>6</strong> chapters</span><span><strong>30</strong> textbook sections</span><span><strong>30</strong> worked checks</span></div></div><div class="section-title"><h2>Table of contents</h2><span>Printed textbook pages</span></div><div class="contents-grid">')
for i,(title,p,sections) in enumerate(chapters):
    html.append(f'<article class="contents-card"><h3><a href="#{ids[i]}">{escape(title)}</a></h3><ol>')
    for name,start in sections:
        num,label = name.split(' ',1)
        html.append(f'<li><a href="#section-{num.replace(".","-")}"><span class="toc-num">{num}</span><span class="toc-label">{escape(label)}</span><span class="toc-page">{start}</span></a></li>')
    html.append('</ol></article>')
html.append('</div><p class="source-link"><a href="#appendix">Appendix — Reference Tables</a> · printed p. 421</p><div class="reading-note"><p><strong>How to use this page.</strong> Open any numbered section for definitions, concepts, equations, derivation or reasoning, and a worked check. “Derivation” means algebra or a model-based argument where appropriate; empirical laws and definitions are identified as such. Formula boxes can be copied by double-clicking or by pressing Enter when focused. Concentrations use mol L⁻¹ (M); aqueous calculations use the dilute-solution approximation, usually at 25 °C.</p></div></section><div class="search-status" id="searchStatus" role="status" aria-live="polite"></div><div id="emptySearch" class="empty" hidden>No matching sections. Try a term such as “buffer”, “precipitation”, or “activation”.</div>')

all_nums = list(lessons)
quiz_data = {}
for i,(title,start,sections) in enumerate(chapters):
    end = chapters[i+1][1]-1 if i<5 else 420
    html.append(f'<section class="chapter lesson-unit" id="{ids[i]}" aria-labelledby="chapter-title-{i+1}"><div class="chapter-head"><span class="big-num">{i+1:02}</span><div><h2 id="chapter-title-{i+1}">{escape(title.split(" ",1)[1])}</h2><p>{intro[i]}</p><div class="source-link">{pdf_link(start,end)} · {len(sections)} sections</div></div></div><div class="chapter-tools"><div><button type="button" data-chapter-expand="true">Expand chapter</button> <button type="button" data-chapter-expand="false">Collapse chapter</button></div><label class="complete-label"><input class="complete" type="checkbox" data-unit="{ids[i]}"> Mark chapter reviewed</label></div>')
    for j,(name,p) in enumerate(sections):
        num,label=name.split(' ',1)
        d=lessons[num]
        last=sections[j+1][1]-1 if j+1<len(sections) else end
        html.append(f'<details class="lesson" id="section-{num.replace(".","-")}" {"open" if num=="1.1" else ""}><summary><span class="lesson-index">{num}</span><h3>{escape(label)}</h3><span class="page-label">p. {p}</span></summary><div class="lesson-body"><p class="lesson-source">{pdf_link(p,last)} · PDF pages {p+10}–{last+10}</p><h4>Definitions</h4><dl class="definition-list">')
        for term,definition in d['definitions']:
            html.append(f'<div><dt>{escape(term)}</dt><dd>{escape(definition)}</dd></div>')
        html.append(f'</dl><h4>Concepts</h4><p class="concept">{escape(d["concept"])}</p><h4>Equations & relationships</h4><div class="equation" data-copy tabindex="0" aria-label="Equations for section {num}; press Enter or double-click to copy">')
        html.extend(f'<div class="equation-line">{escape(eq)}</div>' for eq in d['equations'])
        html.append('</div><h4>Derivation & reasoning</h4><ol class="derivation-steps">')
        html.extend(f'<li>{escape(s)}</li>' for s in d['steps'])
        html.append(f'</ol><div class="worked-check"><h4>Worked check</h4><p>{escape(d["example"])}</p></div><div class="trap"><strong>Assumptions & common mistakes</strong>{escape(d["caution"])}</div>')
        if num in models: html.append(models[num])
        k=all_nums.index(num)
        html.append('<div class="section-links">')
        html.append(f'<a href="#section-{all_nums[k-1].replace(".","-")}">← {all_nums[k-1]}</a>' if k else '<a href="#overview">← Contents</a>')
        html.append(f'<a href="#section-{all_nums[k+1].replace(".","-")}">Next: {all_nums[k+1]} →</a>' if k+1<len(all_nums) else '<a href="#appendix">Reference tables →</a>')
        html.append('</div></div></details>')
    html.append(f'<form class="quiz" data-unit="{ids[i]}" aria-label="Chapter {i+1} review"><h3>Chapter {i+1} review</h3><p>Three questions to check the ideas before moving on.</p>')
    quiz_data[ids[i]]=[]
    for qi,(question,options,answer,explanation) in enumerate(quiz[i]):
        html.append(f'<fieldset><legend>{qi+1}. {escape(question)}</legend><div class="options">')
        for oi,option in enumerate(options):
            html.append(f'<label class="option"><input type="radio" name="{ids[i]}-q{qi}" value="{oi}">{escape(option)}</label>')
        html.append(f'</div><p class="feedback" id="{ids[i]}-feedback{qi}" hidden></p></fieldset>')
        quiz_data[ids[i]].append({'answer':answer,'explanation':explanation})
    html.append('<div class="quiz-footer"><button class="primary" type="submit">Check answers</button><span class="quiz-score" role="status" aria-live="polite"></span></div></form></section>')

uses = ['Molar masses for amount–mass conversions.','Identify ion formulas and charges before balancing.','Predict precipitates and choose qualitative-analysis reagents.','Use Ksp values with temperature and salt stoichiometry.','Compare conjugate pairs and obtain Ka data.','Match a colour-transition interval to a titration curve.','Select half-reactions and calculate standard cell potentials.']
html.append('<section class="appendix" id="appendix" aria-labelledby="appendix-title"><h2 id="appendix-title">Appendix — Reference Tables</h2><p class="source-link">'+pdf_link(421,label='Open the appendix contents')+'</p><p class="concept">Use the book’s reference tables alongside the matching tutorial sections. Values and exceptions should be read from the supplied PDF.</p><div class="table-wrap"><table><thead><tr><th scope="col">Reference table</th><th scope="col">Use it for</th><th scope="col">Printed page</th></tr></thead><tbody>')
for (title,p),use in zip(appendix,uses):
    html.append(f'<tr><td>{pdf_link(p,label=title)}</td><td>{use}</td><td>{p}</td></tr>')
html.append('</tbody></table></div><div class="reading-note"><p><strong>Source and scope.</strong> The chapter hierarchy, section titles, and reading links follow <a href="output/pdf/Chemistry12-navigable.pdf#page=7" target="_blank" rel="noopener">BC Science Chemistry 12, table of contents (printed p. v)</a>. Explanations and worked checks are original study notes aligned to those topics. Definitions and empirical relationships are distinguished from algebraic derivations. For scanned diagrams, full examples, exercises, and reference data, use the linked textbook pages.</p></div></section><footer class="footer"><span>BC Science Chemistry 12 · Textbook study companion</span><button type="button" id="resetProgress">Reset review progress</button><a href="#overview">Back to contents ↑</a></footer></main></div><div class="toast" id="toast" role="status" hidden></div>')
structure = [{'id':ids[i],'title':t,'sections':[{'id':'section-'+n.split()[0].replace('.','-'),'title':n,'page':p,'pdfPage':p+10} for n,p in ss]} for i,(t,_,ss) in enumerate(chapters)]
html.append('<script id="studyPageStructure" type="application/json">'+json.dumps(structure,ensure_ascii=False)+'</script>')
html.append('<script>\nconst quizData = '+json.dumps(quiz_data,ensure_ascii=False)+';\n')
html.append('''
const $ = id => document.getElementById(id);
const lessons = [...document.querySelectorAll('.lesson')];
const chapters = [...document.querySelectorAll('.chapter')];
const allDetails = [...document.querySelectorAll('details')];
const toast = message => { $('toast').textContent=message; $('toast').hidden=false; clearTimeout(window.toastTimer); window.toastTimer=setTimeout(()=>$('toast').hidden=true,2600); };
function closeMenu(){document.body.classList.remove('sidebar-open');$('menuBtn').setAttribute('aria-expanded','false');}
$('menuBtn').addEventListener('click',()=>{const open=document.body.classList.toggle('sidebar-open');$('menuBtn').setAttribute('aria-expanded',String(open));});
$('backdrop').addEventListener('click',closeMenu);
document.addEventListener('keydown',e=>{if(e.key==='Escape'){closeMenu();$('menuBtn').focus();}});
document.querySelectorAll('[data-chapter-expand]').forEach(b=>b.addEventListener('click',()=>b.closest('.chapter').querySelectorAll('.lesson:not([hidden])').forEach(d=>d.open=b.dataset.chapterExpand==='true')));
let searchState=null;
function applySearch(){
 const q=$('search').value.toLocaleLowerCase().trim();
 if(q&&searchState===null)searchState=new Map(lessons.map(d=>[d,d.open]));
 let hits=0;
 lessons.forEach(d=>{const match=!q||d.textContent.toLocaleLowerCase().includes(q);d.hidden=!match;d.classList.toggle('search-hit',!!q&&match);if(q&&match){hits++;d.open=true;}});
 chapters.forEach(c=>{c.hidden=!c.querySelector('.lesson:not([hidden])');c.querySelector('.quiz').hidden=!!q;});
 $('overview').hidden=!!q;
 $('appendix').hidden=!!q&&!$('appendix').textContent.toLocaleLowerCase().includes(q);
 $('emptySearch').hidden=!q||hits>0||!$('appendix').hidden;
 $('searchStatus').textContent=q?`${hits} matching textbook section${hits===1?'':'s'}.`:'';
 if(!q&&searchState){searchState.forEach((open,d)=>d.open=open);searchState=null;}
}
$('search').addEventListener('input',applySearch);
function revealTarget(hash=location.hash){
 let id;try{id=decodeURIComponent(hash.slice(1));}catch{return null;}
 const target=$(id);if(!target)return null;
 if(target.closest('[hidden]')){$('search').value='';applySearch();}
 let p=target;while(p){if(p.tagName==='DETAILS')p.open=true;p=p.parentElement;}
 const nav=document.querySelector(`.nav-sections a[href="#${CSS.escape(id)}"]`);if(nav)nav.closest('details').open=true;
 return target;
}
document.querySelectorAll('a[href^="#"]').forEach(a=>a.addEventListener('click',()=>{revealTarget(a.hash);closeMenu();requestAnimationFrame(()=>$(a.hash.slice(1))?.scrollIntoView({block:'start'}));}));
window.addEventListener('hashchange',()=>revealTarget());
let printState=[];
window.addEventListener('beforeprint',()=>{printState=allDetails.map(d=>d.open);lessons.forEach(d=>d.open=true);});
window.addEventListener('afterprint',()=>allDetails.forEach((d,i)=>d.open=printState[i]??d.open));
$('printBtn').addEventListener('click',()=>window.print());
let saved=[];try{const v=JSON.parse(localStorage.getItem('chem12-reviewed-v1')||'[]');if(Array.isArray(v))saved=v;}catch{}
const complete=[...document.querySelectorAll('.complete')];
function updateProgress(){const checked=complete.filter(c=>c.checked);$('progressText').textContent=`${checked.length} of 6 chapters reviewed`;$('courseProgress').value=checked.length;try{localStorage.setItem('chem12-reviewed-v1',JSON.stringify(checked.map(c=>c.dataset.unit)));}catch{$('storageNote').textContent='Progress is available for this session only.';}}
complete.forEach(c=>{c.checked=saved.includes(c.dataset.unit);c.addEventListener('change',updateProgress);});updateProgress();
$('resetProgress').addEventListener('click',()=>{complete.forEach(c=>c.checked=false);updateProgress();toast('Review progress reset');});
document.querySelectorAll('.quiz').forEach(form=>form.addEventListener('submit',e=>{
 e.preventDefault();let score=0,answered=0;const id=form.dataset.unit;
 quizData[id].forEach((q,i)=>{const chosen=form.querySelector(`input[name="${id}-q${i}"]:checked`);const fb=$(`${id}-feedback${i}`);fb.hidden=false;
 if(!chosen){fb.textContent='Choose an answer, then check again.';fb.className='feedback bad';return;}
 answered++;const ok=Number(chosen.value)===q.answer;if(ok)score++;fb.textContent=(ok?'Correct. ':'Try again. ')+q.explanation;fb.className='feedback '+(ok?'good':'bad');});
 form.querySelector('.quiz-score').textContent=answered<3?`${score}/3 correct · ${3-answered} unanswered`:`${score}/3 correct${score===3?' · Well done.':''}`;
}));
async function copyEquation(el){try{await navigator.clipboard.writeText(el.innerText.trim());toast('Formula copied');}catch{const range=document.createRange();range.selectNodeContents(el);const selection=window.getSelection();selection.removeAllRanges();selection.addRange(range);toast('Formula selected — use Copy');}}
document.querySelectorAll('[data-copy]').forEach(el=>{el.addEventListener('dblclick',()=>copyEquation(el));el.addEventListener('keydown',e=>{if(e.key==='Enter'){e.preventDefault();copyEquation(el);}});});
''')
# The retained models use the same inputs and readouts as before.
model_js = OLD.split('function science(n)',1)[1].split("if('IntersectionObserver'",1)[0]
html.append('function science(n)'+model_js)
html.append('''
if('IntersectionObserver' in window){const observer=new IntersectionObserver(entries=>{const visible=entries.filter(e=>e.isIntersecting);if(!visible.length)return;const id=visible[0].target.id;document.querySelectorAll('nav a').forEach(a=>a.classList.toggle('active',a.hash==='#'+id));},{rootMargin:'-90px 0px -55% 0px',threshold:0});lessons.forEach(s=>observer.observe(s));}
revealTarget();
if(location.hash)requestAnimationFrame(()=>$(location.hash.slice(1))?.scrollIntoView({behavior:'instant',block:'start'}));
</script></body></html>
''')
assert len(lessons)==30
(ROOT/'tutorial.html').write_text('\n'.join(html))
print(f'Wrote {len(lessons)} sections, {len(models)} models, and {sum(map(len,quiz))} review questions to tutorial.html')
