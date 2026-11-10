---
tag: 9T31K4
kind: technique
slug: linear-programming-rounding
name: Rounding of an LP solution
aliases:
- Rounding of LP solution
- LP rounding
- relax and round
area: approximation/lp-rounding
level: core
summary: Solves a linear programming relaxation of an integer problem, then converts fractional values to integers, often randomly, to get an approximate solution.
prereqs: [lp-relaxation, linear-programming-problem, integrality-gap, approximation-ratio]
see_also: [fractional-solution, threshold-rounding, randomized-rounding, iterative-rounding, primal-dual-schema, dual-fitting, configuration-lp, lp-in-p]
sources:
  - book: isbn:9780521195270
    title: David P. Williamson and David B. Shmoys, The Design of Approximation Algorithms
    locator: Chapter 1 (set cover by deterministic and randomized rounding), Chapter 4 (deterministic rounding) and Chapter 5 (random sampling and randomized rounding)
  - book: isbn:9783540653677
    title: Vijay V. Vazirani, Approximation Algorithms
    locator: Part II, Chapter 12 (introduction to LP duality) and Chapter 14 (rounding applied to set cover)
  - book: isbn:9780262046305
    title: Thomas H. Cormen, Charles E. Leiserson, Ronald L. Rivest and Clifford Stein, Introduction to Algorithms, fourth edition
    locator: Chapter 35, Section 35.4 (randomization and linear programming)
  - paper: doi:10.1007/BF02579324
    title: Prabhakar Raghavan and Clark D. Thompson, Randomized rounding, a technique for provably good algorithms and algorithmic proofs, Combinatorica 7(4), 1987
    locator: pages 365 to 374
---

LP rounding is the most common way to design an approximation algorithm for an NP-hard problem that can be written as an integer program. Write the problem as an integer program, drop the integrality constraints to get an [LP relaxation](/lp-relaxation/), solve the LP in polynomial time, and turn the [fractional solution](/fractional-solution/) into an integral one. The LP value is a bound on the optimum, so a rounding that loses at most a factor $\rho$ against the LP value is a $\rho$-approximation. The [integrality gap](/integrality-gap/) of the relaxation is the limit of this method: no rounding can be proved better than the gap against the LP value.

## In plain words

Many hard choice problems become easy when you may make half a choice, or a third of one. So first solve the easy version, where each choice is a number between zero and one. Its best value is at least as good as the best real answer, so it is a yardstick.

Then turn each number into a yes or a no. You may round up the large numbers, read each number as a chance and flip a coin, or follow a more careful plan. Show that the rounded answer is valid and costs at most some factor more than the yardstick. Then it also costs at most that factor more than the best real answer. If the easy version is much better than every real answer, no rounding can close that distance.

## When it applies

- **An integer program.** The problem has a formulation $\min \{ c \cdot x : A x \ge b, \; x \in \{0, 1\}^n \}$, or a maximization, or one with general integers, whose [LP relaxation](/lp-relaxation/) replaces $x \in \{0, 1\}^n$ by $0 \le x \le 1$.
- **A solvable LP.** The LP can be solved in polynomial time: it has polynomial size, or it has exponentially many constraints and a polynomial-time [separation oracle](/separation-oracle/), so that the [ellipsoid method](/ellipsoid-method/) applies, or exponentially many variables and a separation oracle for the dual, as for the [configuration LP](/configuration-lp/). See [LP is in P](/lp-in-p/).
- **A small integrality gap.** The ratio between the integral and the fractional optimum is bounded on all instances, by a constant or by a slowly growing function. If the gap is large, add valid inequalities first.
- **Structure to round with.** Some fact about the fractional solution, such as large values in each constraint, few fractional values at a vertex, or a decomposition into simple pieces, lets a rounding rule keep feasibility at bounded cost.

## The template

```pseudo id=main
LP-ROUND(I)
L1  write I as an integer program min c·x, Ax ≥ b, x ∈ {0,1}^n           ▷ hole: FORMULATE
L2  relax x ∈ {0,1}^n to 0 ≤ x ≤ 1, and add valid inequalities            ▷ hole: STRENGTHEN
L3  x* ← an optimal (often a vertex) solution of the LP                   ▷ ellipsoid, interior point, or simplex
L4  x̂ ← ROUND(x*)                                                        ▷ hole: threshold, random, dependent, iterative
L5  x̂ ← REPAIR(x̂)                                                        ▷ hole: fix the violated constraints, if any
L6  return x̂
```

**Claim.** If, for each feasible $x^*$, lines L4 and L5 return a feasible integral $\hat{x}$ with $c \cdot \hat{x} \le \rho \, c \cdot x^*$ (or $\mathbb{E}[c \cdot \hat{x}] \le \rho \, c \cdot x^*$), then LP-ROUND is a $\rho$-approximation (in expectation) for a minimization problem.

*Proof.* Each feasible integral solution is a feasible point of the relaxation, so $\text{LP}^* \le \text{OPT}$. With an optimal $x^*$, $c \cdot \hat{x} \le \rho \, \text{LP}^* \le \rho \, \text{OPT}$; for the expected form, take expectations of the same chain. For maximization the inequalities turn around: $\text{LP}^* \ge \text{OPT}$ and $c \cdot \hat{x} \ge \alpha \, \text{LP}^* \ge \alpha \, \text{OPT}$. $\square$

**The limit.** Suppose the relaxation has integrality gap $g = \sup_I \text{OPT}(I) / \text{LP}^*(I)$ for minimization. A rounding with $c \cdot \hat{x} \le \rho \, \text{LP}^*$ on every instance gives $\text{OPT} \le c \cdot \hat{x} \le \rho \, \text{LP}^*$, so $\rho \ge g$. For vertex cover, the complete graph $K_n$ with unit weights has $\text{LP}^* = n/2$ (all values $1/2$) and OPT $= n - 1$, so $g \ge 2 - 2/n$, and no rounding of this LP is a $(2 - \varepsilon)$-approximation against $\text{LP}^*$.

**The holes.**

- **FORMULATE.** The choice of variables matters. Assignment variables, path variables, configuration variables and time-indexed variables give LPs of very different strength.
- **STRENGTHEN.** Valid inequalities cut off fractional points with no integral point nearby. For minimum knapsack, the plain LP has unbounded gap, and the knapsack cover inequalities reduce it to 2.
- **ROUND.** The rule that turns $x^*$ into $\hat{x}$; see the classic examples and the variations below.
- **REPAIR.** When the rounding can violate some constraints, a cheap fix, such as adding the cheapest set for each uncovered element, restores feasibility at a cost that the analysis bounds.

## Classic examples

- **Threshold rounding for vertex cover.** Round up each $x_v \ge 1/2$. Each edge has an end of value at least $1/2$, so the result is a cover of weight at most $2 \, \text{LP}^*$. See [LP rounding for vertex cover](/lp-rounding-vertex-cover/) and [half-integrality](/half-integrality/).
- **Threshold rounding for set cover.** Round up each $x_S \ge 1/f$, where $f$ is the largest number of sets that contain one element; ratio $f$. See [frequency rounding](/frequency-rounding-set-cover/) and [threshold rounding](/threshold-rounding/).
- **Randomized rounding for set cover.** Take each set with probability $x_S$, in $\lceil \ln n \rceil$ rounds, and repair; ratio $O(\log n)$ in expectation. See [LP rounding for set cover](/lp-rounding-set-cover/).
- **MAX-SAT.** Set each variable true with probability $y_i$ for $1 - 1/e$, and take the better of this and fair coins for $3/4$. See [MAX-SAT LP rounding](/max-sat-lp-rounding/).
- **Congestion.** Choose one path per commodity from a path decomposition of the fractional flow, and bound the load on each edge with a Chernoff bound, for $O(\log m / \log \log m)$. See [randomized rounding](/randomized-rounding/).
- **Scheduling and assignment.** A vertex of the assignment LP has few fractional values, and they form a forest that can be rounded by a matching. See [unrelated machine scheduling](/unrelated-machine-scheduling-makespan/) and the [generalized assignment problem](/generalized-assignment-problem/).
- **Facility location.** Filter the fractional assignment and cluster the clients for a constant ratio. See [Shmoys-Tardos-Aardal facility location](/shmoys-tardos-aardal-facility-location/) and [filtering](/filtering-technique/).

## Variations

- **Deterministic threshold rounding.** Round up the values above a threshold; see [threshold rounding](/threshold-rounding/).
- **Independent randomized rounding.** Read the values as probabilities and round each variable on its own; see [randomized rounding](/randomized-rounding/) and [randomized approximation algorithms](/randomized-approximation-algorithm/).
- **Dependent rounding.** Round correlated variables together so that sums and degrees are kept exactly; see [dependent rounding](/dependent-rounding/), [pipage rounding](/pipage-rounding/) and [swap rounding](/swap-rounding/).
- **Iterative rounding.** Use the structure of vertex solutions: at each step some variable has a large value or some constraint can be dropped, then solve again; see [iterative rounding](/iterative-rounding/), [iterative relaxation](/iterative-relaxation/) and [Jain's algorithm](/jain-iterative-rounding-network-design/).
- **Rounding the dual.** Solve the dual and take the elements whose dual constraint is tight; see [frequency rounding](/frequency-rounding-set-cover/).
- **Without solving the LP.** The [primal-dual schema](/primal-dual-schema/) builds an integral primal and a feasible dual together, and [dual fitting](/dual-fitting/) analyzes a combinatorial algorithm with the LP. Both use the LP only in the proof.
- **Bicriteria rounding.** Allow a bounded violation of some constraints in exchange for a good cost; see [bicriteria approximation](/bicriteria-approximation/).
- **Stronger relaxations.** The [configuration LP](/configuration-lp/) and [semidefinite programming](/semidefinite-programming/) give smaller gaps for some problems, at the cost of harder solving and rounding.

## Pitfalls

- **Ignoring the gap.** Before you look for a better rounding, compute the integrality gap. If the gap is 2, no rounding of this LP gives a ratio below 2 against $\text{LP}^*$.
- **Rounding to the nearest integer.** Rounding each value to the nearest integer can break the constraints. For the constraint $x_1 + x_2 + x_3 \ge 1$ with all values $1/3$, all three round to 0.
- **Any optimum or a vertex.** Some roundings need a vertex solution, for example those that use the bound on the number of fractional values. An interior point method returns a point inside the optimal face, and it must be moved to a vertex first.
- **Exponentially many constraints.** The ellipsoid method needs a separation oracle and is slow in practice. Use a compact extended formulation when one exists, or column generation with the simplex method.
- **Numerical errors.** A value of $0.4999999$ in place of $1/2$ fails a threshold test. Use exact arithmetic, a tolerance with a final feasibility check, or a rounding that does not depend on exact ties.

## Exercises

1. Show that the vertex cover LP of the complete graph $K_n$ has optimum $n/2$, and conclude that its integrality gap is at least $2 - 2/n$.
2. In minimum knapsack, items $i$ have sizes $s_i$ and costs $c_i$, and the goal is a cheapest set of total size at least $D$. Take two items: size $D - 1$ with cost 0, and size $D$ with cost 1. Show that $\text{LP}^* = 1/D$ and OPT $= 1$, so the plain LP has unbounded gap.
3. Prove the claim of the template for maximization problems, with $\text{OPT} \le \text{LP}^*$.
4. For set cover, show that taking each set once with probability $x_S$ leaves a fixed element uncovered with probability at most $1/e$, and give an instance where this bound is reached in the limit.
5. Show that a vertex of $\{x \ge 0 : A x \ge b\}$, with $A$ of $r$ rows, has at most $r$ nonzero coordinates. Use this to show that rounding up all fractional values of a vertex of the knapsack LP adds at most one item.

## References
