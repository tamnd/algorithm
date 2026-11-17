---
tag: Y63QD4
kind: concept
slug: constraint-based-metabolic-modeling
name: Constraint-based metabolic modeling
aliases:
- "COBRA approach"
area: biology/systems-biology
level: core
summary: Describe a cell's metabolism by the steady-state constraint S v = 0 and bounds on fluxes, instead of a kinetic model with unknown rates.
prereqs: [stoichiometric-matrix, linear-programming-problem]
see_also: [flux-balance-analysis, flux-variability-analysis, elementary-flux-mode, minimization-of-metabolic-adjustment, optknock, dynamic-flux-balance-analysis, metabolic-network-gap-filling, quasi-steady-state-approximation]
sources:
  - book: isbn:9781107038851
    title: Bernhard O. Palsson, Systems Biology, Constraint-based Reconstruction and Analysis, Cambridge University Press, 2015
    locator: the chapters on the stoichiometric matrix, on the constraints that define the space of allowed flux states, and on optimization over that space
  - paper: doi:10.1038/nbt.1614
    title: Jeffrey D. Orth, Ines Thiele and Bernhard O. Palsson, What is flux balance analysis?, Nature Biotechnology 28(3), 2010, 245-248
    locator: the description of mass balance and flux bounds as constraints that define a solution space, and the list of analyses built on it
  - paper: doi:10.1038/nrmicro2737
    title: Nathan E. Lewis, Harish Nagarajan and Bernhard O. Palsson, Constraining the metabolic genotype-phenotype relationship using a phylogeny of in silico methods, Nature Reviews Microbiology 10(4), 2012, 291-305
    locator: the survey and family tree of constraint-based methods and their applications
  - paper: doi:10.1038/nature01149
    title: Rafael U. Ibarra, Jeremy S. Edwards and Bernhard O. Palsson, Escherichia coli K-12 undergoes adaptive evolution to achieve in silico predicted optimal growth, Nature 420(6912), 2002, 186-189
    locator: the comparison of the growth of evolved strains with the optimal growth computed from the model
---

Constraint-based metabolic modeling describes the metabolism of a cell by the conditions that every flux state must satisfy, not by rate laws. The main condition is mass balance at steady state: for the [stoichiometric matrix](/stoichiometric-matrix/) $S$ and the vector $v$ of reaction fluxes, $S v = 0$. The other conditions are bounds $lb \le v \le ub$ that encode the direction of irreversible reactions, the capacity of enzymes, and the nutrients in the medium. Together they define a convex set of allowed flux states. The methods of the approach ask questions about this set, mostly with [linear programs](/linear-programming-problem/). The approach needs the reactions of the organism, which genome annotation gives, but no kinetic constants, which are mostly unknown. This is why it works at the scale of whole genomes. It is often called the COBRA approach, after the COBRA Toolbox, a common software package for it.

## In plain words

A cell turns food into energy and new cell material through thousands of chemical reactions. To predict what happens, you would like to know how fast each reaction runs. For most reactions, nobody has measured the numbers you need for that.

This approach asks a simpler question. Which patterns of reaction rates are possible at all? Each substance inside the cell must be made as fast as it is used, or it would pile up or run out. Some reactions only run one way. The cell can take in only so much food. These rules leave a set of possible patterns. You can then ask for the pattern with the fastest growth, the range of each rate, or the effect of removing a gene. The answers are often good, even though the model knows very little.

## The idea

**The constraints.** A network has $n$ internal metabolites and $m$ reactions. Column $j$ of $S$ lists how much of each metabolite reaction $j$ makes (positive) or uses (negative). The concentration vector $x$ changes as $\dot x = S v$. Internal metabolites turn over fast compared with growth and regulation, so the model takes $\dot x = 0$, which gives $S v = 0$. This step is the steady-state assumption, a modelling choice in the spirit of the [quasi-steady-state approximation](/quasi-steady-state-approximation/), not a theorem. The bounds add:

- $v_j \ge 0$ for each irreversible reaction (thermodynamics),
- $v_j \le ub_j$ for a known enzyme capacity or measured rate,
- bounds on the exchange reactions, which define the medium: a nutrient that is absent has uptake bound 0.

**The solution space.** The set $P = \{v : S v = 0, \; lb \le v \le ub\}$ is a [polyhedron](/polyhedron/). Without the finite bounds it is the flux cone, which the [elementary flux modes](/elementary-flux-mode/) generate. Each new constraint makes $P$ smaller, and the approach is to add the constraints that are known until the remaining set says something useful. The model does not pick one flux state. It describes the whole set of states that the known facts allow.

**Questions on the set.** The common methods differ in what they ask:

| question | method | tool |
|---|---|---|
| the best value of an objective, such as growth | [flux balance analysis](/flux-balance-analysis/) | one LP |
| the range of each flux at or near the optimum | [flux variability analysis](/flux-variability-analysis/) | $2m + 1$ LPs |
| all minimal routes through the network | [elementary flux mode enumeration](/elementary-flux-mode-enumeration/) | double description method |
| the state after a gene knockout | [MOMA](/minimization-of-metabolic-adjustment/) | a [quadratic program](/quadratic-programming/) |
| the knockouts that couple a product to growth | [OptKnock](/optknock/) | a bilevel program solved as a [MILP](/mixed-integer-programming/) |
| the change of biomass and medium over time | [dynamic FBA](/dynamic-flux-balance-analysis/) | one LP per time step |
| the reactions missing from a draft model | [gap filling](/metabolic-network-gap-filling/) | a MILP |

**Genes.** Gene-protein-reaction rules state which genes are needed for each reaction, as Boolean formulas such as "gene a and gene b" for an enzyme complex or "gene a or gene b" for two isozymes. A gene knockout sets the bounds of every reaction whose rule becomes false to 0. This links the model to genetic experiments.

**Objectives.** Optimizing an objective, usually the biomass reaction, is a second assumption: that evolution has tuned the cell to grow as fast as it can in the given medium. It is a heuristic. Ibarra, Edwards and Palsson (2002) found that strains of Escherichia coli adapted in the laboratory to a medium where they first grew below the computed optimum reached the computed optimal growth after many generations, which is a measurement in support of it for that case. It is not expected to hold for cells that are not under selection for growth.

## Examples

**Network N.** Take a substrate $A$ with uptake EX_A at most 10, two respiration reactions RESP1 and RESP2 ($A \to 2E$, where $E$ is energy), fermentation FERM ($A \to E + P$), secretion EX_P of $P$, and growth BIO ($A + E \to$), all irreversible. The constraints $S v = 0$ for $A$, $E$ and $P$ and the bounds define a polyhedron in $\mathbb{R}^6$. Maximizing growth gives $\frac{20}{3}$, with all of the substrate used by respiration and growth. The range of RESP1 at this optimum is $[0, \frac{10}{3}]$, because RESP2 can take its place. If both respiration genes are knocked out, the bounds of RESP1 and RESP2 become 0, and the best growth drops to 5, now with fermentation. These numbers come from the FBA, FVA and MOMA pages, where they are computed exactly.

**The medium.** The same model on a medium without $A$ has the uptake bound 0, so $P = \{0\}$ and no growth is possible. Changing exchange bounds is how one model predicts growth on many media.

**Not a constraint-based model.** A kinetic model with Michaelis-Menten rate laws for each enzyme (see [Michaelis-Menten kinetics](/michaelis-menten-kinetics/)) predicts concentrations over time, but it needs the kinetic constants of every enzyme. A constraint-based model of the same network predicts only fluxes, at steady state, and only up to the set $P$.

## Where it is used

- **Genome-scale models.** Models with thousands of reactions are built from genome annotations and the literature, then checked and completed by gap filling. Palsson (2015) describes the reconstruction process.
- **Gene essentiality.** A gene is predicted to be essential if the knockout leaves no flux state with positive growth. The predictions are compared with knockout libraries.
- **Metabolic engineering.** OptKnock and related methods search for knockouts that make a production strain.
- **Data integration.** Measured fluxes, gene expression and other data become new bounds or objectives. Lewis, Nagarajan and Palsson (2012) survey many such methods and group them into a family tree.
- **Communities and dynamics.** Several organisms can share one medium, and dynamic FBA follows a batch culture over time.

## References
