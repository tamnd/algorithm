---
tag: TC2TH5
kind: algorithm
slug: flux-balance-analysis
name: Flux balance analysis
aliases:
- FBA
area: biology/systems-biology
level: core
summary: Find the steady-state fluxes of a metabolic network that maximize an objective such as growth, as a linear program over S v = 0 and bounds.
model: real-ram
complexity:
  vars: {m: the number of reactions, n: the number of metabolites}
  time: {worst: O(2^(3m + n) (n + m) m), per_pivot: O((n + m) m)}
  space: {extra: O(n m)}
properties: {deterministic: true, exact: true, online: false, recursive: false}
history:
  year: 1994
  people: [Amit Varma, Bernhard O. Palsson]
  note: Linear programs over reaction stoichiometry were used in the 1980s. Varma and Palsson showed in 1994 that one such LP predicts the growth and the by-product secretion of Escherichia coli.
prereqs: [constraint-based-metabolic-modeling, stoichiometric-matrix, linear-programming-problem, simplex-method]
see_also: [flux-variability-analysis, minimization-of-metabolic-adjustment, optknock, dynamic-flux-balance-analysis, elementary-flux-mode, metabolic-network-gap-filling, lp-duality, bland-rule]
sources:
  - paper: doi:10.1038/nbt.1614
    title: Jeffrey D. Orth, Ines Thiele and Bernhard O. Palsson, What is flux balance analysis?, Nature Biotechnology 28(3), 2010, 245-248
    locator: the whole primer (the constraints, the objective and the LP)
  - paper: doi:10.1128/aem.60.10.3724-3731.1994
    title: Amit Varma and Bernhard O. Palsson, Stoichiometric flux balance models quantitatively predict growth and metabolic by-product secretion in wild-type Escherichia coli W3110, Applied and Environmental Microbiology 60(10), 1994, 3724-3731
    locator: the LP model and the comparison with measured growth and secretion
  - book: isbn:9781107038851
    title: Bernhard O. Palsson, Systems Biology, Constraint-based Reconstruction and Analysis, Cambridge University Press, 2015
    locator: the chapters on constraints and on optimization
  - paper: doi:10.1287/moor.2.2.103
    title: Robert G. Bland, New finite pivoting rules for the simplex method, Mathematics of Operations Research 2(2), 1977, 103-107
    locator: the smallest index rule and its proof of termination
  - paper: doi:10.1038/nature01149
    title: Rafael U. Ibarra, Jeremy S. Edwards and Bernhard O. Palsson, Escherichia coli K-12 undergoes adaptive evolution to achieve in silico predicted optimal growth, Nature 420(6912), 2002, 186-189
    locator: the measured growth of evolved strains against the FBA prediction
---

Flux balance analysis (FBA) computes the reaction rates of a metabolic network at steady state without any kinetic constants. It uses only the [stoichiometric matrix](/stoichiometric-matrix/) $S$, lower and upper bounds on each flux, and an objective, most often the flux of a biomass reaction that stands for growth. Steady state means $S v = 0$: each internal metabolite is made as fast as it is used. FBA picks, among all flux vectors that satisfy these linear constraints, one that maximizes the objective. This is one [linear program](/linear-programming-problem/) with $m$ variables (one per reaction) and $n$ equality rows (one per metabolite), so it is solved exactly and fast, also for genome-scale networks with thousands of reactions. The optimal value is unique. The optimal flux vector often is not, and [flux variability analysis](/flux-variability-analysis/) measures how much it can change.

## In plain words

Think of a cell as a factory with many machines. Each machine turns some parts into other parts. Parts that stay inside the factory must not pile up and must not run out, so for every inside part the machines that make it and the machines that use it must balance. Some machines have a speed limit, for example the door that lets food in.

Among all the ways to run the machines that keep every part in balance and obey the limits, FBA picks one that makes the most of one chosen output, usually new cell material. It does not need to know how each machine works inside, only what goes in and what comes out. The answer says how fast the cell can grow, and one way to run the machines that gets there. Often many other ways reach the same growth.

## The problem

**Input.** A network with $n$ internal metabolites and $m$ reactions, given by:

- the $n \times m$ stoichiometric matrix $S$, where $S_{ij}$ is the number of molecules of metabolite $i$ that reaction $j$ makes (negative if it uses them);
- bounds $lb_j \le v_j \le ub_j$ for each flux, where $lb_j$ may be $-\infty$ and $ub_j$ may be $+\infty$. An irreversible reaction has $lb_j = 0$. An uptake reaction has an upper bound set by the medium. A knocked-out gene sets $lb_j = ub_j = 0$ for its reactions;
- an objective vector $c \in \mathbb{R}^m$, usually the unit vector of the biomass reaction.

Fluxes are in mmol per gram of dry weight per hour, and the biomass flux is then the growth rate in 1/h.

**Output.** The status (optimal, infeasible or unbounded), and in the optimal case an optimal flux vector $v^*$ and the optimum $z^* = c^{\mathsf T} v^*$ of

$$\max_{v} \; c^{\mathsf T} v \quad \text{subject to} \quad S v = 0, \quad lb \le v \le ub .$$

Exchange reactions with the medium (one side of the reaction is empty) are columns of $S$ like any other, so the network is open and $S v = 0$ has non-zero solutions.

## The algorithm

FBA is the LP above. The work is in the LP solver. The version here writes the LP in the standard form $\min d^{\mathsf T} y$, $A y = b$, $y \ge 0$, and solves it with the [two-phase simplex method](/two-phase-simplex-method/) and [Bland's rule](/bland-rule/), in exact rational arithmetic.

```pseudo id=main
FBA(S, lb, ub, c)
L1  for each reaction j: v_j ← lb_j + y_j if lb_j is finite, else v_j ← ub_j - y_j if ub_j is finite, else v_j ← y_j' - y_j''
L2  rewrite each row of S v = 0 in the variables y, with the constant terms moved to the right side b
L3  for each j with lb_j and ub_j finite: add the row y_j + s_j = ub_j - lb_j with a slack s_j ≥ 0
L4  d ← the cost of -c v in the variables y
L5  (status, y) ← TWO-PHASE-SIMPLEX(A, b, d) with Bland's rule
L6  if status is infeasible or unbounded then return status
L7  v ← the fluxes from y by the formulas of line L1
L8  return (v, c v)
```

Line L1 makes every variable non-negative. A reaction with only an upper bound is reflected, and a free reaction with no finite bound is split into a forward and a backward part. Line L3 turns each finite upper bound into an equation. Line L4 changes the maximization into a minimization. Phase 1 of line L5 finds a feasible basis or shows that none exists. Phase 2 moves from vertex to vertex of the feasible polyhedron. Bland's rule picks the entering variable with the smallest index among those with a negative [reduced cost](/reduced-cost/), and the leaving variable with the smallest index among the tied rows of the ratio test, so the method cannot cycle on a degenerate vertex.

## Example

Take the toy network N with three internal metabolites: a substrate $A$, an energy carrier $E$ and a by-product $P$.

| reaction | equation | bounds |
|---|---|---|
| EX_A | $\emptyset \to A$ | $[0, 10]$ |
| RESP1 | $A \to 2E$ | $[0, \infty)$ |
| RESP2 | $A \to 2E$ | $[0, \infty)$ |
| FERM | $A \to E + P$ | $[0, \infty)$ |
| EX_P | $P \to \emptyset$ | $[0, \infty)$ |
| BIO | $A + E \to \emptyset$ | $[0, \infty)$ |

RESP1 and RESP2 are two isozymes or two routes with the same net equation. The objective is the flux of BIO. Write $a$ for the uptake, $r$ for the total respiration $v_{\text{RESP1}} + v_{\text{RESP2}}$, $f$ for the fermentation and $g$ for growth. The balance of $E$ gives $g = 2r + f$, the balance of $P$ gives $v_{\text{EX\_P}} = f$, and the balance of $A$ gives $a = r + f + g = 3r + 2f$. So $g = \frac{2}{3}a - \frac{1}{3}f$, which is largest with $a = 10$ and $f = 0$:

$$z^* = \tfrac{20}{3}, \qquad v^* = (10,\ r_1,\ \tfrac{10}{3} - r_1,\ 0,\ 0,\ \tfrac{20}{3}) \text{ for any } r_1 \in [0, \tfrac{10}{3}] .$$

The exact simplex method of the implementation returns the vertex with $r_1 = \frac{10}{3}$. The optimum is a whole segment, not a point: the growth rate is determined, but the split between RESP1 and RESP2 is not.

The [LP dual](/lp-duality/) explains the numbers. The [shadow price](/shadow-price/) of the uptake bound is $\frac{2}{3}$: one more unit of $A$ gives $\frac{2}{3}$ more growth, and $z^* = \frac{2}{3} \cdot 10$. The reduced cost of FERM is $\frac{1}{3}$: each unit of fermentation flux costs a third of a unit of growth, which matches $g = \frac{2}{3}a - \frac{1}{3}f$.

Knockouts change the bounds only. With RESP1 knocked out, RESP2 takes over and $z^* = \frac{20}{3}$ again. With both RESP1 and RESP2 knocked out, the only route left is fermentation: $a = 2f$ and $g = f$, so $z^* = 5$ with $v^* = (10, 0, 0, 5, 5, 5)$, and the cell now secretes 5 units of $P$. With EX_A knocked out, $z^* = 0$. The tests check these values, and on random small networks they compare the result with the best vertex of the flux polytope found by brute force and with the value of the dual LP.

## Correctness

The substitution of line L1 maps the box $lb \le v \le ub$ onto the set $y \ge 0$ (with the rows of line L3 for the finite upper bounds), and it is linear plus a constant, so the feasible sets of the two LPs correspond and the objectives differ only by a constant and a sign. A split free variable is covered because every real number is a difference of two non-negative numbers. So the LP of line L5 is infeasible, unbounded or optimal exactly when the FBA problem is, and an optimal $y$ maps to an optimal $v$. The two-phase simplex method with Bland's rule ends after finitely many pivots (Bland 1977), with a proof of infeasibility after phase 1, a ray of unbounded improvement, or a basis whose reduced costs are all non-negative, which is optimal by [weak duality](/weak-duality/). The full proof is below.

## Complexity

- **Size.** The LP has $m$ flux variables and $n$ equality rows, plus one variable for each free reaction and one row and one slack for each reaction with two finite bounds. So the standard form has at most $2m$ columns and $n + m$ rows.
- **Polynomial time.** Linear programming is in P ([LP in P](/lp-in-p/)), by the [ellipsoid method](/ellipsoid-method/) and by [interior point methods](/interior-point-method/). So FBA takes time polynomial in $m$, $n$ and the encoding length $L$ of the data. This is a theorem about the worst case.
- **Simplex.** Each pivot costs $O((n + m) m)$ arithmetic operations on the tableau. With Bland's rule no basis comes back within a phase, so the number of pivots is at most the number of bases. Phase 1 has at most $3m + n$ columns, which gives the crude bound $O(2^{3m + n} (n + m) m)$ of the front matter. The number of pivots can be exponential in the worst case (Avis and Chvátal 1978 gave such examples for Bland's rule, as the [Klee-Minty cube](/klee-minty-cube/) does for Dantzig's rule). On metabolic networks the simplex method is fast in practice; this is an observation, not a bound.
- **Exact arithmetic.** With rational data, the code works with fractions. The size of the numbers stays polynomial in the input if the tableau is kept in reduced form, but the constant is much larger than in floating point.
- **Space.** $O((n + m) m)$ for the tableau, which is $O(n m)$ when the bound rows are kept implicit, as bounded simplex codes do.

## Properties

- **Exact.** The optimal value is exact. With floating point LP solvers it is exact up to the solver tolerance.
- **One value, many solutions.** The optimum $z^*$ is unique, but the set of optimal flux vectors is a face of the polyhedron, often of positive dimension. Parallel routes, isozymes and internal cycles are the usual causes.
- **No kinetics.** FBA uses no rate laws and no concentrations. Its predictions depend on the bounds and the objective, which are modeling choices.
- **Steady state only.** It gives one time-independent state. Changes in the medium over time need [dynamic FBA](/dynamic-flux-balance-analysis/).
- **The objective is a hypothesis.** Maximal growth is a heuristic about what the cell does. Ibarra, Edwards and Palsson (2002) measured that E. coli grown for many generations on glycerol reached the growth rate that FBA predicted; this is a measurement under those conditions, not a law.

## Variants and improvements

- **Flux variability analysis.** The range of each flux over the optimal face ([FVA](/flux-variability-analysis/), Mahadevan and Schilling 2003).
- **Parsimonious FBA.** After maximizing growth, minimize the total flux $\sum_j |v_j|$ at that growth. It picks a sparse optimum and removes most internal cycles.
- **Loopless FBA.** Forbid flux around internal cycles with no net reaction, which breaks the second law of thermodynamics, by adding integer variables (Schellenberger, Lewis and Palsson 2011).
- **Knockout analysis.** Set the bounds of the reactions of a gene to zero and solve again. [MOMA](/minimization-of-metabolic-adjustment/) replaces the objective by the distance to the wild type, and [OptKnock](/optknock/) searches for the knockout set that couples a product to growth.
- **Dynamic FBA.** Solve one FBA problem per time step and update the medium ([dynamic FBA](/dynamic-flux-balance-analysis/)).
- **Regulatory and thermodynamic constraints.** Add Boolean rules that switch reactions off, or bounds from the Gibbs energies of the reactions.

## When to use it

Use FBA when the network is known but the kinetics are not, which is the usual case for whole-cell metabolism. It answers questions about capacity: the highest growth rate on a medium, the highest yield of a product, whether a knockout is lethal, which nutrients are essential. It is the base of the other constraint-based methods on the [constraint-based modeling](/constraint-based-metabolic-modeling/) page. Do not use one FBA solution as the flux state of the cell: report the optimum and the ranges from FVA, or add data that fix the fluxes. For concentrations, transients or regulation, a kinetic model is needed.

## Pitfalls

- **Reading one optimal vector.** The solver returns one vertex of the optimal face, and another solver or another reaction order may return another. Conclusions about single fluxes need FVA.
- **Missing uptake bounds.** If no exchange reaction is bounded, the LP is often unbounded, as in network N without the bound on EX_A.
- **Internal cycles.** A cycle of reversible reactions with no net effect can carry any flux without changing growth. It shows up as huge fluxes in the solution and as infinite ranges in FVA.
- **Signs of exchange reactions.** Conventions differ: in many models the exchange is written $A \to \emptyset$, and uptake is a negative flux with a negative lower bound. Mixing the conventions gives a wrong medium.
- **Units of the biomass reaction.** The biomass flux is a growth rate only if the coefficients of the biomass reaction are in mmol per gram of dry weight.
- **Tolerances.** Floating point solvers report values such as $10^{-9}$ for zero fluxes. Use a tolerance, or exact arithmetic on small models.

## Implementations

## History

Linear programming over reaction stoichiometry appeared in biochemical engineering in the 1980s, for example in the work of Papoutsakis on fermentations of butyric acid bacteria (1984) and of Fell and Small on fat synthesis in adipose tissue (1986). Varma and Palsson built stoichiometric models of E. coli in the early 1990s and showed in 1994 that the LP with an uptake bound and a growth objective predicts the growth rate and the secretion of acetate in aerobic and anaerobic cultures. Genome-scale reconstructions since 2000 made FBA a standard tool, and the COBRA Toolbox and COBRApy are common implementations. Orth, Thiele and Palsson (2010) wrote a short primer on the method.

## References
