---
tag: 845EGQ
kind: algorithm
slug: minimization-of-metabolic-adjustment
name: Minimization of metabolic adjustment
aliases:
- MOMA
area: biology/systems-biology
level: advanced
summary: Predict the fluxes of a knockout mutant as the feasible flux vector closest in Euclidean distance to the wild type, by a quadratic program.
model: real-ram
complexity:
  vars: {m: the number of reactions, n: the number of metabolites}
  time: {worst: O(3^m (m + n)^3)}
  space: {extra: O((m + n)^2)}
properties: {deterministic: true, exact: true, online: false, recursive: false}
history:
  year: 2002
  people: [Daniel Segrè, Dennis Vitkup, George M. Church]
  note: Segrè, Vitkup and Church proposed that a mutant right after a knockout stays as close as it can to the wild-type flux state, instead of growing at its own optimum.
prereqs: [flux-balance-analysis, quadratic-programming]
see_also: [flux-variability-analysis, optknock, constraint-based-metabolic-modeling, kkt-conditions, convex-optimization-problem, least-squares-problem, interior-point-method, lp-duality]
sources:
  - paper: doi:10.1073/pnas.232349399
    title: Daniel Segrè, Dennis Vitkup and George M. Church, Analysis of optimality in natural and perturbed metabolic networks, PNAS 99(23), 2002, 15112-15117
    locator: the definition of MOMA as a quadratic program and its comparison with FBA on E. coli knockouts
  - paper: doi:10.1073/pnas.0406346102
    title: Tomer Shlomi, Omer Berkman and Eytan Ruppin, Regulatory on/off minimization of metabolic flux changes after genetic perturbations, PNAS 102(21), 2005, 7695-7700
    locator: ROOM, the mixed-integer variant that minimizes the number of large flux changes
  - paper: doi:10.1038/nbt.1614
    title: Jeffrey D. Orth, Ines Thiele and Bernhard O. Palsson, What is flux balance analysis?, Nature Biotechnology 28(3), 2010, 245-248
    locator: the FBA problem that gives the wild-type flux vector
---

Minimization of metabolic adjustment (MOMA) predicts the flux state of a mutant right after a gene knockout. [Flux balance analysis](/flux-balance-analysis/) predicts the mutant by maximizing growth again under the new bounds, which assumes that the mutant is already optimal. Segrè, Vitkup and Church (2002) proposed a different hypothesis: a fresh mutant has not evolved to its new optimum, and its fluxes stay as close as they can to the wild type. MOMA computes the steady-state flux vector of the mutant network that is nearest to the wild-type flux vector $w$ in the Euclidean norm. This is a [quadratic program](/quadratic-programming/) with a strictly convex objective, so its solution is unique, unlike the FBA optimum.

## In plain words

When you remove one machine from a factory, the factory does not redesign itself at once. It keeps running in nearly the old way, with the smallest change that still works without that machine. MOMA uses this idea for a cell.

First, find a normal way to run the healthy cell. Then remove the reactions of the deleted gene. Among all ways to run the changed cell that keep every inside chemical in balance, choose the one that is closest to the old way, where "closest" means the smallest sum of squared changes over all reactions. The growth rate of that state is the prediction for the mutant. It is usually lower than the best growth that the mutant could reach.

## The problem

**Input.** The $n \times m$ stoichiometric matrix $S$; a wild-type flux vector $w$, usually an FBA optimum of the wild type with $S w = 0$; and the bounds $lb \le v \le ub$ of the mutant, where each knocked-out reaction has $lb_j = ub_j = 0$.

**Output.** The flux vector

$$v^{\text{MOMA}} = \arg\min_{v} \; \|v - w\|^2 \quad \text{subject to} \quad S v = 0, \quad lb \le v \le ub,$$

or a report that the mutant has no steady state within the bounds. The predicted growth rate is the biomass flux of $v^{\text{MOMA}}$.

$v^{\text{MOMA}}$ is the orthogonal projection of $w$ onto the mutant flux polyhedron $P$. Expanding the square gives the standard QP form $\min \frac{1}{2} v^{\mathsf T} v - w^{\mathsf T} v$ over $P$.

## The algorithm

Practical MOMA codes call a convex QP solver. The implementation here solves the QP exactly for small networks by trying every active set: each reaction is at its lower bound, at its upper bound, or free. For each set, the free fluxes are the projection of $w$ onto an affine subspace, given by one linear system, and the [KKT conditions](/kkt-conditions/) decide whether the candidate is the minimizer.

```pseudo id=main
MOMA(S, lb, ub, w)
L1  for each state σ in {LOW, UP, FREE}^m, with the most FREE entries first:
L2      set v_j ← lb_j if σ_j = LOW and v_j ← ub_j if σ_j = UP; let F be the free set
L3      r ← - Σ over j not in F of S_j v_j
L4      solve x - w_F + S_F^T μ = 0, S_F x = r; skip σ if there is no solution; v_F ← x
L5      skip σ if some free v_j is outside [lb_j, ub_j]
L6      if some λ gives g = v - w + S^T λ with g_j = 0 on F, g_j ≥ 0 on LOW, g_j ≤ 0 on UP:
L7          return v
L8  return "no feasible flux vector"
```

A reaction with $lb_j = ub_j$ gets only the state LOW, and its sign condition is dropped. Line L4 is the projection of $w_F$ onto $\{x : S_F x = r\}$: its solution $x$ is unique when it exists, though $\mu$ need not be. Line L6 is a small LP feasibility problem in $\lambda$, because $\lambda$ is not unique when $S$ has dependent rows.

## Example

Take network N of the [FBA page](/flux-balance-analysis/), with reactions EX_A (uptake at most 10), RESP1 and RESP2 ($A \to 2E$), FERM ($A \to E + P$), EX_P and BIO ($A + E \to$). The wild type is the FBA vertex $w = (10, \frac{10}{3}, 0, 0, 0, \frac{20}{3})$.

**Both respiration reactions knocked out.** The mutant steady states are $v = (2g, 0, 0, g, g, g)$ with $0 \le g \le 5$: all growth must come from fermentation. FBA predicts $g = 5$. MOMA minimizes

$$(2g - 10)^2 + \left(\tfrac{10}{3}\right)^2 + g^2 + g^2 + \left(g - \tfrac{20}{3}\right)^2,$$

whose derivative $14 g - \frac{160}{3}$ is zero at $g = \frac{80}{21} \approx 3.81$. So MOMA predicts the flux vector $(\frac{160}{21}, 0, 0, \frac{80}{21}, \frac{80}{21}, \frac{80}{21})$, with growth about 24 percent below the FBA value. The squared distance to $w$ is about 53.97, against about 63.89 for the FBA optimum.

**RESP1 knocked out.** FBA predicts that RESP2 takes over the whole flux and growth stays at $\frac{20}{3} \approx 6.67$. That state has the squared distance $\frac{200}{9} \approx 22.2$ from $w$. MOMA finds a closer state, $v = (\frac{485}{51}, 0, \frac{45}{17}, \frac{40}{51}, \frac{40}{51}, \frac{310}{51})$, at squared distance about 19.93: RESP2 takes over only part of the flux, a little fermentation appears, and growth drops to $\frac{310}{51} \approx 6.08$. So MOMA predicts a small loss of growth and some secretion of $P$ where FBA predicts neither.

**RESP2 or FERM knocked out.** Both carry no flux in $w$, so $w$ itself is feasible for the mutant and MOMA returns $v = w$.

The tests check the exact solver on a one-dimensional and a two-dimensional family against a fine grid of feasible points, check that $v = w$ when $w$ is feasible, and check on random networks that the result satisfies the projection inequality $(w - v)^{\mathsf T}(p - v) \le 0$ for every vertex $p$ of the feasible polytope.

## Correctness

The objective is strictly convex and the feasible set is a closed convex polyhedron, so if the set is not empty there is exactly one minimizer. With linear constraints, the KKT conditions are necessary and sufficient for a convex QP, so a vector is the minimizer if and only if it is feasible and some multipliers satisfy the sign conditions of line L6. Each returned vector passes those checks, so it is the minimizer. Conversely, the minimizer has KKT multipliers, and the state that puts each reaction with a positive bound multiplier at that bound and leaves the others free produces exactly the minimizer at line L4, since the projection in line L4 is unique. So the loop always returns when the set is not empty. The full proof is below.

## Complexity

- **This code.** At most $3^m$ states. Each one needs one linear system of size $|F| + n \le m + n$, in $O((m + n)^3)$ operations, and one LP in $n$ variables. This is exponential and meant for toy networks and tests.
- **In practice.** MOMA is a convex QP with $m$ variables, $n$ equality rows and $2m$ bounds. Convex QPs can be solved in polynomial time, for example by [interior point methods](/interior-point-method/). This is a theorem. Active set QP solvers are fast on metabolic networks but have no polynomial bound in the worst case.
- **Knockout screens.** A screen of all single knockouts solves $m$ QPs with the same $w$, one per reaction or gene.
- **Space.** $O((m + n)^2)$ for the KKT matrix of one state.

## Properties

- **Unique.** For fixed $w$, the answer is unique, because the objective is strictly convex. The FBA optimum of a mutant is often not unique.
- **Depends on $w$.** The wild-type vector is often one of many FBA optima. Different choices of $w$ give different MOMA predictions. A $w$ from measured fluxes avoids this choice.
- **Not optimal for growth.** The MOMA growth rate is at most the FBA growth rate of the mutant, since both are computed over the same feasible set and FBA maximizes growth.
- **Feasibility is the same as for FBA.** MOMA has a solution exactly when the mutant has any steady state within the bounds.
- **A hypothesis, not a law.** That a fresh mutant stays close to the wild type is a heuristic. Segrè, Vitkup and Church compared MOMA and FBA with measured fluxes of a knockout mutant and with knockout growth data of E. coli, and reported that MOMA fits the mutant fluxes better; this is a measurement on their data.

## Variants and improvements

- **Linear MOMA.** Replace the squared Euclidean norm by the sum of absolute differences $\sum_j |v_j - w_j|$. With one extra variable per reaction this is an LP, and it is often faster. Its solution need not be unique.
- **ROOM.** Regulatory on/off minimization (Shlomi, Berkman and Ruppin 2005) minimizes the number of reactions whose flux changes by more than a small tolerance, as a mixed-integer program. It models a cell that switches a few reactions instead of shifting all of them a little.
- **Weighted MOMA.** Weight each squared difference, for example by the inverse of the measurement variance of $w_j$.
- **Lethality prediction.** A knockout is predicted lethal when the MOMA growth rate is below a small threshold, as with FBA, but the two methods can disagree on mutants with alternative routes.

## When to use it

Use MOMA to predict the flux state or the growth of a mutant shortly after a knockout, when you have a good wild-type flux vector, ideally from measurements such as 13C flux analysis. Use FBA for the mutant after laboratory evolution, which often brings the mutant to its new optimum. For a strain design problem that needs the mutant to be optimal for growth, use [OptKnock](/optknock/), whose inner problem is FBA.

## Pitfalls

- **An arbitrary $w$.** If $w$ is just the vertex that one LP solver returned, the MOMA prediction depends on that solver. Use measured fluxes, or a unique wild-type state such as the FBA optimum with the smallest norm.
- **Units and scale.** The Euclidean norm adds squared changes of all fluxes, so large fluxes dominate. A change of one unit in a large flux counts the same as a change of one unit in a small one.
- **Exchange reactions.** Including all exchange fluxes in the distance makes the result depend on the medium bounds. Some studies use only the internal fluxes in the objective.
- **Numerics.** With a floating point QP solver, fluxes that should be zero come out as small numbers. Use a tolerance before you read off which reactions are active.

## Implementations

## History

Segrè, Vitkup and Church introduced MOMA in 2002. They noted that FBA assumes an optimal mutant, and that a mutant made in the laboratory has not been under selection for that optimum. They formulated the closest feasible flux vector as a quadratic program and compared it with FBA on knockouts in E. coli. Shlomi, Berkman and Ruppin (2005) proposed ROOM as a variant with a count of changed fluxes instead of a distance. MOMA and its linear form are standard functions of the COBRA tools.

## References
