---
tag: VH5CWZ
kind: concept
slug: lp-relaxation
name: LP relaxation
aliases:
- continuous relaxation
- fractional relaxation
- linear relaxation
- linear programming relaxation
area: optimization/integer-programming
level: intro
summary: Drop the integrality conditions of an integer program to get a linear program whose optimum bounds the integer optimum.
prereqs: [mixed-integer-programming, linear-programming-problem]
see_also: [integrality-gap, ideal-formulation, integer-hull, total-unimodularity, branch-and-cut, lagrangian-relaxation, cutting-plane-method-integer-programming, lp-rounding-vertex-cover]
sources:
  - book: isbn:9780471283669
    title: Laurence A. Wolsey, Integer Programming, Wiley, 1998
    locator: Chapter 1 (good and ideal formulations) and Chapter 2 (optimality, relaxation and bounds, with LP relaxation and Lagrangian relaxation)
  - book: isbn:9783319110073
    title: Michele Conforti, Gérard Cornuéjols and Giacomo Zambelli, Integer Programming, Springer, 2014
    locator: Chapter 1 (the linear programming relaxation) and Chapter 2 (formulations and their strength)
  - book: isbn:9780471828198
    title: George L. Nemhauser and Laurence A. Wolsey, Integer and Combinatorial Optimization, Wiley, 1988
    locator: Part II, Chapter 3 (duality and relaxation)
  - paper: "Arthur M. Geoffrion, Lagrangean relaxation for integer programming, Mathematical Programming Study 2 (1974), 82 to 114"
    locator: the comparison of the Lagrangian bound with the LP bound
---

The LP relaxation of an [integer program](/mixed-integer-programming/) is the [linear program](/linear-programming-problem/) that results when the integrality conditions are dropped. Its feasible set contains every feasible integer point, so its optimal value bounds the integer optimum: from above for a maximization, from below for a minimization. The bound can be computed in polynomial time, and it is the engine of [branch and cut](/branch-and-cut/), of [cutting-plane methods](/cutting-plane-method-integer-programming/) and of LP rounding [approximation algorithms](/approximation-ratio/). How good the bound is depends on the formulation, not only on the set of integer solutions.

## In plain words

An integer program is hard because some unknowns must be whole numbers. If you forget that rule, you get an ordinary linear program, which a computer solves fast. The answer of this easier problem cannot be worse than the true answer, because it had more freedom. So it gives a limit: the true best profit is never above the relaxed best profit.

Sometimes the relaxed answer is already in whole numbers. Then it is also the true answer. Often it is not, and rounding it can break a rule or give a poor answer. The value is still useful: a solver compares it with the best whole-number answer found so far, and if the two are close, it can stop early.

## The idea

Take the problem in the form

$$z_{IP} = \max \{\, c^T x : x \in S \,\}, \qquad S = \{x \in \mathbb{R}^n : Ax \le b,\ x \ge 0,\ x_j \in \mathbb{Z} \text{ for } j \in I\},$$

where $n$ is the number of variables and $m$ the number of rows of $A$. The polyhedron $P = \{x : Ax \le b,\ x \ge 0\}$ is the *formulation*, and the LP relaxation is

$$z_{LP} = \max \{\, c^T x : x \in P \,\}.$$

The LP pages use the form $\min c^T x$, $Ax = b$, $x \ge 0$. [Slack variables](/slack-variables/) and a change of sign give that form.

**Proposition.** Assume rational data.

1. If $S \ne \emptyset$ and $z_{LP}$ is finite, then $z_{IP} \le z_{LP}$.
2. If $P = \emptyset$, then $S = \emptyset$.
3. If an optimal solution $x^*$ of the relaxation lies in $S$, then $x^*$ is optimal for the integer program.
4. If $S \ne \emptyset$ and the relaxation is unbounded, then the integer program is unbounded.
5. If $P' \subseteq P$ is another formulation with $P' \cap \{x : x_I \in \mathbb{Z}^I\} = S$, then its value $z'_{LP}$ satisfies $z_{IP} \le z'_{LP} \le z_{LP}$.

*Proof.* Parts 1, 2 and 5 follow from $S \subseteq P' \subseteq P$: a maximum over a larger set is at least as large. For part 3, $x^* \in S$ gives $c^T x^* \le z_{IP}$, and part 1 gives $z_{IP} \le z_{LP} = c^T x^*$. Part 4 needs more: by Meyer's theorem the convex hull of $S$ is a rational polyhedron whose recession cone equals that of $P$. If $c^T$ has no upper bound on $P$, there is a direction $r$ of that cone with $c^T r > 0$, and $x + \lambda r$ stays in $\operatorname{conv}(S)$ for $x \in S$ and $\lambda \ge 0$. So $c^T x$ has no upper bound on $\operatorname{conv}(S)$, and hence none on $S$, since a linear function has the same supremum on a set and on its convex hull. $\square$

With irrational data part 4 fails: $\max\{x_1 : x_1 = \sqrt{2}\,x_2,\ x \ge 0,\ x \in \mathbb{Z}^2\}$ has only the integer point $(0, 0)$, while its relaxation is unbounded.

**Bounds from the dual.** Each dual feasible solution of the relaxation gives an upper bound on $z_{IP}$ by [weak duality](/weak-duality/), so a solver does not need to solve the LP to optimality to prune. At an optimal basis, $c^T x = z_{LP} - \sum_h d_h t_h$ for all $x \in P$, where $t_h \ge 0$ are the nonbasic variables and $d_h \ge 0$ are the [reduced costs](/reduced-cost/). If $x_j$ is nonbasic and integer, each $x \in S$ with $x_j \ge 1$ has $c^T x \le z_{LP} - d_j$. So when $z_{LP} - d_j$ is not above the value of a known integer solution, all better solutions have $x_j = 0$. This is *reduced cost fixing*.

**The strength of a formulation.** Many polyhedra $P$ have the same integer points. The smallest is the [integer hull](/integer-hull/) $\operatorname{conv}(S)$, and a formulation with $P = \operatorname{conv}(S)$ is [ideal](/ideal-formulation/): its relaxation gives $z_{IP}$ for each objective. The ratio of $z_{IP}$ and $z_{LP}$ in the worst case over a class of instances is the [integrality gap](/integrality-gap/). [Lagrangian relaxation](/lagrangian-relaxation/) gives a bound between the two: Geoffrion (1974) showed that for a maximization, $z_{IP} \le z_{LD} \le z_{LP}$, with equality $z_{LD} = z_{LP}$ when the constraints that stay in the subproblem define an integral polyhedron.

## Examples

**A relaxation that gives the answer.** If $A$ is [totally unimodular](/total-unimodularity/) and $b$ is integral, each vertex of $P$ is integral, so the [simplex method](/simplex-method/) returns a point of $S$, and part 3 says that it is optimal. [Bipartite matching](/bipartite-matching/), the [assignment problem](/assignment-problem/) and [maximum flow](/max-flow-problem/) are solved this way.

**Rounding fails.** Maximize $25x_1 + 16x_2$ subject to $50x_1 + 31x_2 \le 250$, $-3x_1 + 2x_2 \le 4$, $x \ge 0$ integer. The relaxation has the optimum $(376/193,\ 950/193) \approx (1.948,\ 4.922)$ with value $24600/193 \approx 127.46$. Of the four roundings $(1,4)$, $(1,5)$, $(2,4)$, $(2,5)$, only $(2, 4)$ is feasible, with value 114. The integer optimum is $(5, 0)$ with value 125, far from the LP point. [Gomory's algorithm](/gomory-cutting-plane-algorithm/) reaches it after 6 cuts.

**A weak and a strong formulation.** Two facilities with opening cost 4 each serve three customers. Facility 1 serves customers 1, 2, 3 at costs 1, 1, 5, and facility 2 at costs 5, 1, 1. Let $y_i \in \{0,1\}$ open facility $i$ and $x_{ij} \in [0, 1]$ be the part of customer $j$ served by $i$, with $\sum_i x_{ij} = 1$. Two formulations have the same integer solutions:

| formulation | linking constraints | LP value | LP solution |
|---|---|---|---|
| weak (aggregated) | $\sum_j x_{ij} \le 3 y_i$ for each $i$ | 7 | $y = (2/3, 1/3)$ |
| strong (disaggregated) | $x_{ij} \le y_i$ for each $i, j$ | 11 | $y = (1, 1)$ |

The integer optimum is 11: one facility alone costs $4 + 7 = 11$, and both cost $8 + 3 = 11$. The strong relaxation gives the exact value here. The weak one opens two thirds of facility 1, which is enough for its two customers, and one third of facility 2. The strong formulation has $mn$ linking rows instead of $m$ for $m$ facilities and $n$ customers, but solvers almost always prefer it.

**A gap that does not close.** For the vertex cover of the complete graph with $k$ vertices, the relaxation has value $k/2$ at $x = (1/2, \ldots, 1/2)$, while each cover has $k - 1$ vertices.

## Where it is used

- **[Branch and cut](/branch-and-cut/) and branch and bound.** The relaxation of each node gives the bound for pruning, and its fractional values choose the branching variable, as in [strong branching](/strong-branching/) and [pseudocost branching](/pseudocost-branching/).
- **[Cutting-plane methods](/cutting-plane-method-integer-programming/).** Cuts tighten the relaxation, from $P$ toward the integer hull.
- **Approximation algorithms.** [LP rounding for vertex cover](/lp-rounding-vertex-cover/) and [for set cover](/lp-rounding-set-cover/), and [primal-dual](/primal-dual-approximation/) methods, compare the answer with $z_{LP}$.
- **Primal heuristics.** The [feasibility pump](/feasibility-pump/), [diving](/diving-heuristic/) and [RINS](/relaxation-induced-neighborhood-search/) start from the LP solution.
- **[Presolve](/presolve/).** Bound tightening and reduced cost fixing shrink the model before the search.
- **Decomposition.** [Column generation](/column-generation/) and [branch and price](/branch-and-price/) solve the relaxation of a stronger formulation with many columns.

## References
