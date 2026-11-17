---
tag: 3ZQX3G
kind: algorithm
slug: flux-variability-analysis
name: Flux variability analysis
aliases:
- FVA
area: biology/systems-biology
level: core
summary: For each reaction, minimize and maximize its flux by linear programming over all solutions within a fraction of the optimal objective.
model: real-ram
complexity:
  vars: {m: the number of reactions, n: the number of metabolites, T: the time of one FBA linear program}
  time: {worst: O(m T), linear_programs: 2m + 1}
  space: {extra: O(n m)}
properties: {deterministic: true, exact: true, online: false, recursive: false}
history:
  year: 2003
  people: [Radhakrishnan Mahadevan, Christophe H. Schilling]
  note: Mahadevan and Schilling used the minimum and maximum of each flux over the optimal set of an FBA problem to measure the effect of alternate optimal solutions in a genome-scale model of Escherichia coli.
prereqs: [flux-balance-analysis]
see_also: [constraint-based-metabolic-modeling, minimization-of-metabolic-adjustment, elementary-flux-mode, metabolic-network-gap-filling, lp-duality, parametric-linear-programming, linear-programming-problem, simplex-method]
sources:
  - paper: doi:10.1016/j.ymben.2003.09.002
    title: Radhakrishnan Mahadevan and Christophe H. Schilling, The effects of alternate optimal solutions in constraint-based genome-scale metabolic models, Metabolic Engineering 5(4), 2003, 264-276
    locator: the definition of the two LPs per reaction over the optimal set, and their use on the E. coli model
  - paper: doi:10.1186/1471-2105-11-489
    title: Steinn Gudmundsson and Ines Thiele, Computationally efficient flux variability analysis, BMC Bioinformatics 11, 2010, 489
    locator: the fast implementation that reuses the optimal basis between the LPs
  - paper: doi:10.1038/nbt.1614
    title: Jeffrey D. Orth, Ines Thiele and Bernhard O. Palsson, What is flux balance analysis?, Nature Biotechnology 28(3), 2010, 245-248
    locator: the section on the types of analysis built on FBA, including flux variability
  - book: isbn:9781107038851
    title: Bernhard O. Palsson, Systems Biology, Constraint-based Reconstruction and Analysis, Cambridge University Press, 2015
    locator: the chapter on the capabilities of reconstructed networks (alternate optima and flux ranges)
---

Flux variability analysis (FVA) answers the question that one [flux balance analysis](/flux-balance-analysis/) solution leaves open: how much can each flux change while the network still reaches the optimal objective, or a given fraction of it? FBA returns one optimal flux vector, but the set of optimal vectors is often a whole face of the flux polyhedron. FVA first solves the FBA problem for its optimum $z^*$. Then, for each of the $m$ reactions, it solves two more [linear programs](/linear-programming-problem/): the minimum and the maximum of that flux over all steady states with objective at least a threshold near $z^*$. The result is one interval per reaction. A reaction with the interval $[0, 0]$ is blocked, a reaction whose interval does not contain 0 is required, and a wide interval shows a choice of routes.

## In plain words

FBA tells you how fast the cell can grow and gives one way to get there. Often there are many ways. FVA takes each reaction in turn and asks two questions: what is the least flux this reaction can carry while the cell still grows at the best rate, and what is the most? Each question is a small optimization problem of the same kind as FBA.

The answer is a range for each reaction. If the range is only zero, the reaction is never used. If the range does not include zero, the cell must use it. If the range is wide, other reactions can take its place. You can also allow a little less than the best growth, which usually makes the ranges wider.

## The problem

**Input.** An $n \times m$ stoichiometric matrix $S$, flux bounds $lb \le v \le ub$ (some may be infinite), an objective $c$, and a fraction $f \in [0, 1]$.

**Output.** The FBA optimum $z^* = \max \{c^{\mathsf T} v : S v = 0, \; lb \le v \le ub\}$ and, for each reaction $j$,

$$v_j^{\min} = \min_{v \in P_f} v_j, \qquad v_j^{\max} = \max_{v \in P_f} v_j, \qquad P_f = \{v : S v = 0, \; lb \le v \le ub, \; c^{\mathsf T} v \ge t\},$$

with the threshold $t = z^* - (1 - f) |z^*|$. For $f = 1$, $P_1$ is the set of FBA optima. For $z^* \ge 0$ the threshold is $t = f z^*$. A minimum or maximum can be $-\infty$ or $+\infty$ when the bounds do not close the polyhedron.

## The algorithm

```pseudo id=main
FVA(S, lb, ub, c, f)
L1  z* ← FBA(S, lb, ub, c); stop if it is infeasible or unbounded
L2  t ← z* - (1 - f) |z*|
L3  for j ← 1 to m:
L4      lo_j ← min v_j subject to S v = 0, lb ≤ v ≤ ub, c v ≥ t   (or -∞ if unbounded)
L5      hi_j ← max v_j subject to the same constraints   (or +∞ if unbounded)
L6      append [lo_j, hi_j] to the result
L7  return (z*, the list of intervals)
```

The $2m$ LPs of lines L4 and L5 have the same constraints and differ only in the objective. They are never infeasible, because the FBA optimum of line L1 satisfies all of them. The code solves every LP from scratch with the exact [simplex method](/simplex-method/) of the FBA page.

## Example

Take network N of the [FBA page](/flux-balance-analysis/): uptake EX_A of a substrate $A$ (at most 10), two parallel respiration reactions RESP1 and RESP2 ($A \to 2E$), fermentation FERM ($A \to E + P$), secretion EX_P of $P$, and growth BIO ($A + E \to$). The FBA optimum is $z^* = \frac{20}{3}$. The intervals for three fractions are:

| reaction | $f = 1$ | $f = 0.9$ | $f = 0$ |
|---|---|---|---|
| EX_A | $[10, 10]$ | $[9, 10]$ | $[0, 10]$ |
| RESP1 | $[0, \frac{10}{3}]$ | $[0, \frac{10}{3}]$ | $[0, \frac{10}{3}]$ |
| RESP2 | $[0, \frac{10}{3}]$ | $[0, \frac{10}{3}]$ | $[0, \frac{10}{3}]$ |
| FERM | $[0, 0]$ | $[0, 2]$ | $[0, 5]$ |
| EX_P | $[0, 0]$ | $[0, 2]$ | $[0, 5]$ |
| BIO | $[\frac{20}{3}, \frac{20}{3}]$ | $[6, \frac{20}{3}]$ | $[0, \frac{20}{3}]$ |

At $f = 1$ the uptake and the growth are fixed, and fermentation is off. But each respiration reaction can carry anything from 0 to $\frac{10}{3}$, because the other one takes the rest: the optimum that FBA returns, with RESP1 at $\frac{10}{3}$ and RESP2 at 0, is one end of a segment. The intervals do not say that every combination is possible: RESP1 and RESP2 together must carry exactly $\frac{10}{3}$. At $f = 0.9$ the growth may drop to 6. Growth is $g = \frac{2}{3}a - \frac{1}{3}v_{\text{FERM}}$, so $g \ge 6$ with $a \le 10$ allows up to 2 units of fermentation, and the uptake may drop to 9. At $f = 0$ the threshold is 0, and the ranges are those of all steady states: the fermentation alone can carry at most 5, with $a = 10$ split as 5 for FERM and 5 for growth.

The tests check these ranges against the minimum and maximum of each flux over the vertices of the polyhedron $P_f$, found by brute force, and check that the FBA optimum lies in every interval.

## Correctness

The minimization and the maximization of $v_j$ over the polyhedron $P_f$ are linear programs, and the exact simplex method solves them, with the status "unbounded" for an infinite end. None of them is infeasible, since $t \le z^*$ and the FBA optimum is in $P_f$. $P_f$ is convex, so the set of values of $v_j$ on it is an interval, and every value between $v_j^{\min}$ and $v_j^{\max}$ is the flux of some vector in $P_f$. For $f = 1$, $c^{\mathsf T} v \ge z^*$ on the feasible set means $c^{\mathsf T} v = z^*$, so $P_1$ is the optimal face. The full proof is below.

## Complexity

- **Number of LPs.** One FBA problem and $2m$ range problems, so $2m + 1$ LPs. Each has $m$ variables and $n + 1$ rows, plus the bound rows. With an LP time $T$, the total time is $O(m T)$, and the LPs are polynomial ([LP in P](/lp-in-p/)). This is a theorem.
- **Warm starts.** The range LPs share their constraints with each other and with the FBA problem, so a solver can start each one from the optimal basis of the last. Gudmundsson and Thiele (2010) do this and solve the LPs in parallel; on genome-scale models they report large speed-ups over a plain loop. This is a measurement on their test models.
- **Fewer LPs.** Each optimal vertex found on the way gives a lower bound for every $v_j^{\max}$ and an upper bound for every $v_j^{\min}$. Reactions whose bound already meets the bound in $lb$ or $ub$ need no LP. This is a heuristic: it saves LPs in practice but not in the worst case.
- **Space.** One LP at a time, $O(n m)$ for the dense tableau.

## Properties

- **Exact.** With exact arithmetic the intervals are exact. With a floating point solver they are exact up to the solver tolerance.
- **Projection, not shape.** The intervals are the projections of $P_f$ onto each axis. They lose the coupling between fluxes: the box of all intervals is larger than $P_f$, as the example shows for RESP1 and RESP2.
- **Monotone in the fraction.** If $f' \le f$, then $t' \le t$, so $P_f \subseteq P_{f'}$ and every interval for $f'$ contains the interval for $f$.
- **Blocked reactions.** With $c = 0$, $P_f$ is the set of all steady states that obey the bounds, and a reaction with interval $[0, 0]$ is blocked. The code gives this as blocked_reactions. Blocked reactions are the starting point of [gap filling](/metabolic-network-gap-filling/).
- **Deterministic.** The intervals do not depend on the order of the reactions or the solver, unlike the single vector that FBA returns.

## Variants and improvements

- **Fast FVA.** Warm starts from the last basis and parallel LPs (Gudmundsson and Thiele 2010).
- **Loopless FVA.** With internal cycles, a flux can grow without bound around the cycle, which gives infinite or very wide intervals. Adding the loopless constraints removes these and gives the ranges over thermodynamically feasible states, at the cost of a mixed-integer program per bound.
- **Flux coupling.** The ratio of two fluxes can be minimized and maximized over the flux cone with LPs of the same kind. This finds pairs of reactions that always carry flux together.
- **Sampling.** Random sampling of points in $P_f$ estimates the distribution of each flux inside its interval. FVA gives only the ends.
- **Range of the objective under a constraint.** A production envelope, the maximum product flux as a function of the growth rate, is a sequence of LPs of the same form. It shows whether a product is coupled to growth, which [OptKnock](/optknock/) tries to achieve.

## When to use it

Use FVA after every FBA study that draws conclusions about single fluxes, because one optimal vector is not unique. It is the standard way to find blocked reactions, reactions required for growth on a medium, and reactions whose flux is fixed by the optimum. Use a fraction below 1 when the cell may not grow at the exact optimum, as is usual in experiments. If you need the joint distribution of fluxes or the coupling between them, use sampling or flux coupling analysis instead.

## Pitfalls

- **Reading the box as the feasible set.** Each interval is attained, but the ends of different intervals are not attained together.
- **Infinite intervals.** A reversible cycle with no net effect can carry any flux. FVA shows this as an infinite or a very large interval, set only by the default bound of the model (often 1000).
- **The fraction for a negative optimum.** The threshold $f z^*$ is stricter than the optimum when $z^* < 0$. The form $z^* - (1 - f)|z^*|$ of this page avoids that.
- **Tolerances.** With a floating point solver, the constraint $c^{\mathsf T} v \ge z^*$ can be infeasible by rounding. Solvers relax it by a small tolerance, which can widen the intervals a little.
- **Counting LPs.** $2m$ LPs on a model with ten thousand reactions take long without warm starts or parallel runs.

## Implementations

## History

Mahadevan and Schilling (2003) showed that FBA problems on genome-scale models have many alternate optima, and they defined the two LPs per reaction to measure the range of each flux over the optimal set. They applied it to a genome-scale model of Escherichia coli and studied how far the fluxes can vary at maximal growth. Gudmundsson and Thiele (2010) made it fast with warm starts and parallel LPs. FVA is now a standard function of the COBRA Toolbox and COBRApy.

## References
