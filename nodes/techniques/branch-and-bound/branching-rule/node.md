---
tag: TMBN8X
kind: definition
slug: branching-rule
name: Branching rule
aliases:
- variable selection rule
- branching strategy
area: techniques/branch-and-bound
level: core
summary: Rule that splits a subproblem into children, such as choosing which variable or edge to fix next.
prereqs: [state-space-tree, bounding-function]
see_also: [node-selection-rule, fathoming-rule, strong-branching, pseudocost-branching, reliability-branching, land-doig-algorithm, little-algorithm, interval-branch-and-bound]
sources:
  - book: isbn:9780471283669
    title: Laurence A. Wolsey, Integer Programming
    locator: Chapter 7, Branch and Bound (branching on a fractional variable, choice of branching variable)
  - paper: doi:10.1016/j.orl.2004.04.002
    title: Tobias Achterberg, Thorsten Koch and Alexander Martin, Branching rules revisited, Operations Research Letters 33(1), 2005
    locator: pp. 42 to 54
  - paper: doi:10.1093/comjnl/8.3.250
    title: R. J. Dakin, A tree-search algorithm for mixed integer programming problems, The Computer Journal 8(3), 1965
    locator: pp. 250 to 255
  - paper: doi:10.1287/opre.11.6.972
    title: John D. C. Little, Katta G. Murty, Dura W. Sweeney and Caroline Karel, An algorithm for the traveling salesman problem, Operations Research 11(6), 1963
    locator: pp. 972 to 989
---

A branching rule tells a branch and bound search how to split a subproblem that it cannot yet discard into smaller subproblems, its children. The children must together contain every feasible solution of the parent, and each must be strictly smaller, so that no solution is lost and the search ends. A rule has two parts: *what* to branch on, such as which variable, arc or box side, and *how* to split it, such as $x_j = 0$ against $x_j = 1$. The [bounding function](/bounding-function/) and the [node selection rule](/node-selection-rule/) are the other two choices that define a branch and bound method.

## Definition

Let a branch and bound search optimize over a finite set $S$, and let each node $N$ stand for a subproblem with feasible set $S(N) \subseteq S$. A **branching rule** maps each node $N$ that is not fathomed to a finite list of children $N_1, \ldots, N_m$, $m \ge 2$, with sets $S(N_1), \ldots, S(N_m)$, such that

1. **Cover.** $S(N_1) \cup \cdots \cup S(N_m) = S(N)$.
2. **Progress.** Each $S(N_i)$ is a proper subset of $S(N)$, or, more generally, some measure of the subproblem, such as the number of free variables, strictly decreases from $N$ to each $N_i$.

The rule is a **partition** if the sets $S(N_i)$ are pairwise disjoint; then no solution is found twice. For problems over a continuous set, such as global optimization over a box, the progress condition is replaced by a shrinking size, for example the width of the box, and the search stops at a given precision.

In practice the rule has two steps. The **selection** step chooses the object to branch on: a variable, an arc, a coordinate of a box. The **split** step defines the children from it.

## Examples and non-examples

**Example: fixing a 0-1 variable.** For a 0-1 problem, choose a free variable $x_j$ and make two children with $x_j = 1$ and $x_j = 0$. The children partition $S(N)$, and each has one fewer free variable. [Knapsack branch and bound](/knapsack-branch-and-bound/) uses this rule.

**Example: the order of the variables matters.** Take the 0-1 knapsack instance with capacity 14, values $14, 12, 18, 19, 19, 20$ and weights $1, 1, 2, 7, 8, 10$, depth-first search with the fractional bound, and the child "take" first. If the variables are fixed in ratio order, the search expands 9 nodes. Over all $720$ fixed orders of the six variables, it expands between 8 and 15 nodes. The bound and the answer, 64, do not change; only the tree does.

**Example: branching on a fractional variable.** In LP-based branch and bound, let $\bar{x}$ be the optimal solution of the [LP relaxation](/lp-relaxation/) and $\bar{x}_j$ a fractional value of an integer variable. The children add $x_j \le \lfloor \bar{x}_j \rfloor$ and $x_j \ge \lceil \bar{x}_j \rceil$. No integer point lies strictly between the two, so the cover holds, and $\bar{x}$ is cut off from both children. This dichotomy is due to Dakin (1965). For the earlier rule of Land and Doig (1960), see the [Land-Doig algorithm](/land-doig-algorithm/).

**Example: choosing the fractional variable.** Rules to choose $j$ include the most fractional variable, [strong branching](/strong-branching/), which solves the LP of each candidate child and picks the variable with the best bound change, [pseudocost branching](/pseudocost-branching/), which estimates the change from past branchings, and [reliability branching](/reliability-branching/), which mixes the two. Achterberg, Koch and Martin (2005) compare these rules on test sets of mixed integer programs.

**Example: arcs in a tour.** [Little's algorithm](/little-algorithm/) for the traveling salesman problem chooses an arc $(i, j)$ and makes two children: tours that use $(i, j)$ and tours that do not.

**Example: bisection.** [Interval branch and bound](/interval-branch-and-bound/) cuts a box into two halves across its widest side.

**Non-example: a gap between the children.** With $\bar{x}_j = 3$ already an integer, the children $x_j \le 2$ and $x_j \ge 4$ lose every solution with $x_j = 3$. They do not cover $S(N)$.

**Non-example: no progress.** Branching on a variable that is already fixed, or on $x_j \le 5$ and $x_j \ge 5$ when $x_j$ is already 5 in every solution of $N$, gives a child equal to its parent, and the search can loop.

**Non-example: one child.** Fixing a variable to the only value it can take is not branching but a reduction; it has one child and does not split the problem.

## Related definitions

- [Node selection rule](/node-selection-rule/): decides which live node to process next. The branching rule decides how to split it.
- [Fathoming rule](/fathoming-rule/): decides when a node is not split at all.
- **Branching factor.** The number of children of a node; see [branching factor](/branching-factor/).
- **Symmetry.** When the problem has symmetries, a rule that respects them, such as [orbital branching](/orbital-branching/), avoids children that are copies of each other.

## References
