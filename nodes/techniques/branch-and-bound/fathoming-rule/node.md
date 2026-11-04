---
tag: DPSX0B
kind: definition
slug: fathoming-rule
name: Fathoming rule
aliases:
- fathoming
- pruning rule
area: techniques/branch-and-bound
level: core
summary: 'Criterion under which a node is discarded: infeasible, bound no better than incumbent, or solved exactly.'
prereqs: [bounding-function, incumbent-solution]
see_also: [branching-rule, node-selection-rule, dominance-pruning, search-tree-pruning, land-doig-algorithm, knapsack-branch-and-bound, lp-relaxation]
sources:
  - book: isbn:9780471283669
    title: Laurence A. Wolsey, Integer Programming
    locator: Chapter 7, Branch and Bound (pruning by optimality, by bound and by infeasibility)
  - paper: doi:10.1287/opre.14.4.699
    title: E. L. Lawler and D. E. Wood, Branch-and-bound methods, a survey, Operations Research 14(4), 1966
    locator: pp. 699 to 719
  - paper: doi:10.1145/322003.322010
    title: Toshihide Ibaraki, The power of dominance relations in branch-and-bound algorithms, Journal of the ACM 24(2), 1977
    locator: pp. 264 to 279
---

A fathoming rule says when a branch and bound search may discard a node without splitting it, because its subtree cannot contain a solution better than the [incumbent](/incumbent-solution/) or because its best solution is already known. A node that is discarded is *fathomed*, or *pruned*. The three standard rules are fathoming by infeasibility, by bound and by optimality; dominance gives a fourth. A rule is sound when it never discards the only optimal solutions, and the strength of the rules decides the size of the tree.

## Definition

Let a branch and bound search maximize $f$ over a finite set $S$. A node $N$ stands for a subproblem with feasible set $S(N) \subseteq S$; let $f^*(N) = \max_{x \in S(N)} f(x)$, or $-\infty$ if $S(N)$ is empty. Let $z$ be the incumbent value, $ub$ a valid [bounding function](/bounding-function/), and $R(N) \supseteq S(N)$ a relaxation whose optimum gives $ub(N)$.

A node $N$ is **fathomed** when the search removes it from the set of live nodes without making its children. A **fathoming rule** is a condition on $N$ under which this is done. The standard rules are:

1. **By infeasibility.** The relaxation $R(N)$ is empty. Then $S(N)$ is empty.
2. **By bound.** $ub(N) \le z$. Then $f^*(N) \le ub(N) \le z$, so no solution below $N$ beats the incumbent.
3. **By optimality.** An optimal solution $\bar{x}$ of the relaxation lies in $S(N)$, and $f(\bar{x}) = ub(N)$. Then $f^*(N) = f(\bar{x})$; the search updates the incumbent with $\bar{x}$ if it is better, and drops $N$.
4. **By dominance.** Another node $M$, live or already processed, is known to have $f^*(M) \ge f^*(N)$, and $M$ will not be discarded by this rule in turn; see [dominance pruning](/dominance-pruning/).

A fathoming rule is **sound** if, whenever the search discards a node, the optimum over the remaining tree and the incumbent is still $\max_{x \in S} f(x)$. Rules 1 to 3 are sound for every valid bound. For minimization, rule 2 reads $lb(N) \ge z$.

Variants of rule 2:

- With an integer objective, a node can be fathomed when $\lfloor ub(N) \rfloor \le z$.
- With a tolerance $\varepsilon \ge 0$, fathoming when $ub(N) \le z + \varepsilon$ gives a solution within $\varepsilon$ of the optimum. This is how solvers stop at a given gap.
- To list all optimal solutions, fathom only when $ub(N) < z$.

## Examples and non-examples

**Example: the three rules in one run.** In the [Land-Doig algorithm](/land-doig-algorithm/) on: maximize $5 x_1 + 4 x_2$ with $6 x_1 + 4 x_2 \le 24$, $x_1 + 2 x_2 \le 6$, $x \ge 0$ integer:

- The node $x_2 = 1, x_1 = 4$ has an empty LP, since $6 \cdot 4 + 4 \cdot 1 = 28 > 24$: fathomed by infeasibility.
- The node $x_2 = 0$ has LP optimum $(4, 0)$, which is integral: fathomed by optimality, and the incumbent becomes 20.
- The nodes $x_2 = 1, x_1 = 3$, with LP value 19, and $x_2 = 2$, with LP value 18, have bound below 20: fathomed by bound.

**Example: the rounded bound.** In [knapsack branch and bound](/knapsack-branch-and-bound/) on capacity 16, values $40, 30, 50, 10$ and weights $2, 5, 10, 5$, the node that takes item 1 and leaves items 2 and 3 has fractional bound $40 + 10 = 50$. When the incumbent is 80, this node is fathomed by bound. All values are integers, so a fractional bound of $89.5$ against an incumbent of 89 would also fathom, since no packing has value 89.5.

**Example: no rule applies.** The root of the integer program above has LP solution $(3, \frac{3}{2})$, value 21, and no incumbent. It is feasible, its bound is above $-\infty$, and its LP solution is not integral, so it must be split.

**Non-example: a heuristic bound.** Discarding a node because a greedy completion has a low value is not a fathoming rule: the greedy value is a lower bound on $f^*(N)$, not an upper bound.

**Non-example: optimality with a gap.** If the LP optimum of a node is integral but the node's bound came from a different, weaker relaxation, the node is not solved: only a solution of the relaxation that gives $ub(N)$, with $f(\bar{x}) = ub(N)$, proves $f^*(N) = f(\bar{x})$.

**Non-example: dominance in a cycle.** Discarding $N$ because $M$ dominates it, and $M$ because $N$ dominates it, when the two have the same value, discards both. Dominance needs a strict order or a fixed tie-break.

## Related definitions

- [Bounding function](/bounding-function/) and [incumbent solution](/incumbent-solution/): the two sides of fathoming by bound.
- [Branching rule](/branching-rule/): applied to the nodes that are not fathomed.
- [Search tree pruning](/search-tree-pruning/): the same idea in backtracking, where the tests are feasibility tests on partial solutions.
- **Fathomed and dead nodes.** Horowitz and Sahni call a node that will not be expanded further a dead node; a fathomed node is a dead node removed by one of the rules above.

## References
