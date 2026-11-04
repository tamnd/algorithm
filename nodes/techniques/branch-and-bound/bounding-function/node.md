---
tag: VCMZTY
kind: definition
slug: bounding-function
name: Bounding function
aliases:
- lower bound function
- relaxation bound
area: techniques/branch-and-bound
level: core
summary: Function giving a lower (or upper, for maximisation) bound on the best objective value achievable below a node.
prereqs: [state-space-tree, incumbent-solution]
see_also: [fathoming-rule, lp-relaxation, lagrangian-relaxation, knapsack-branch-and-bound, gilmore-lawler-bound, admissible-heuristic, depth-first-branch-and-bound, best-first-branch-and-bound]
sources:
  - book: isbn:9780471283669
    title: Laurence A. Wolsey, Integer Programming
    locator: Chapter 2 (optimality, relaxation and bounds) and Chapter 7 (branch and bound)
  - paper: doi:10.1287/opre.14.4.699
    title: E. L. Lawler and D. E. Wood, Branch-and-bound methods, a survey, Operations Research 14(4), 1966
    locator: pp. 699 to 719
  - book: isbn:9780929306414
    title: Ellis Horowitz, Sartaj Sahni and Sanguthevar Rajasekaran, Computer Algorithms, second edition
    locator: Chapter 8, Branch-and-Bound (bounding, cost functions)
---

A bounding function gives, for each node of a branch and bound search, a number that no feasible solution below that node can beat: an upper bound on the objective for a maximization problem, a lower bound for a minimization problem. When this number is not better than the value of the [incumbent](/incumbent-solution/), the whole subtree is discarded. The bound is usually the optimum of a *relaxation*, an easier problem whose feasible set contains that of the node. Its quality decides how much of the tree branch and bound must explore.

## Definition

Let a branch and bound search maximize $f$ over a finite set $S$ of feasible solutions. Each node $N$ of the search tree stands for a subproblem with feasible set $S(N) \subseteq S$; the root has $S(\text{root}) = S$, and the sets of the children of $N$ cover $S(N)$. Let $f^*(N) = \max_{x \in S(N)} f(x)$, with $f^*(N) = -\infty$ if $S(N)$ is empty.

A **bounding function** is a map $ub$ from nodes to $\mathbb{R} \cup \{-\infty, +\infty\}$ that is **valid**:
$$ub(N) \ge f^*(N) \quad \text{for every node } N.$$

For minimization, a bounding function $lb$ satisfies $lb(N) \le \min_{x \in S(N)} f(x)$. Common extra properties, which are not required:

- **Exact at solutions.** If $S(N) = \{x\}$ is a single complete solution, then $ub(N) = f(x)$.
- **Monotone.** $ub(C) \le ub(N)$ for every child $C$ of $N$. A bound from a relaxation of the subproblem is monotone when the relaxation of a child is a restriction of the relaxation of its parent.
- **Stronger.** A bound $ub_1$ is stronger than $ub_2$ if $ub_1(N) \le ub_2(N)$ for all $N$. Every node fathomed by $ub_2$ is then fathomed by $ub_1$, at the same incumbent.

**Relaxation principle.** Let $R(N) \supseteq S(N)$ and let $g$ satisfy $g(x) \ge f(x)$ for $x \in S(N)$. Then $\max_{y \in R(N)} g(y) \ge f^*(N)$, because the maximum over a larger set of a larger function cannot be smaller. Most bounding functions are built this way: drop the integrality ([LP relaxation](/lp-relaxation/)), drop some constraints, or move constraints into the objective with penalties ([Lagrangian relaxation](/lagrangian-relaxation/)).

## Examples and non-examples

Take the 0-1 knapsack instance with capacity $W = 14$ and six items in ratio order:

| item | 1 | 2 | 3 | 4 | 5 | 6 |
|---|---|---|---|---|---|---|
| value | 14 | 12 | 18 | 19 | 19 | 20 |
| weight | 1 | 1 | 2 | 7 | 8 | 10 |

The optimum is 64, from items 1, 2, 3 and 6, of weight 14. A node fixes the first $k$ items; $c_v$ is the value taken so far.

**Example: the sum of the remaining values.** $ub = c_v + \sum_{j > k} v_j$ is valid, because no completion can take more than all remaining items. At the root it is 102. [Depth-first branch and bound](/depth-first-branch-and-bound/) with this bound expands 34 nodes.

**Example: the fractional bound.** $ub = c_v$ plus the optimum of the [fractional knapsack](/fractional-knapsack/) on the remaining items, which a greedy fill in ratio order computes. It is valid by the relaxation principle, since a 0-1 packing is a fractional packing. At the root it is $14 + 12 + 18 + 19 + \frac{3}{8} \cdot 19 = 70.125$. With it, the same search expands 9 nodes. It is stronger than the sum of the remaining values, and it costs $O(n)$ per node.

**Example: other problems.** The optimum of the LP relaxation in the [Land-Doig algorithm](/land-doig-algorithm/); the sum of the row and column minima of a reduced cost matrix in [Little's algorithm](/little-algorithm/) for the traveling salesman problem; the [Gilmore-Lawler bound](/gilmore-lawler-bound/) for the quadratic assignment problem; and the range of an interval extension of the objective over a box in [interval branch and bound](/interval-branch-and-bound/) are all bounding functions.

**Non-example: a greedy completion.** Fill the rest of the knapsack greedily with whole items, and use the value as $ub$. At the root this gives $14 + 12 + 18 + 19 = 63$, below the optimum 64. It is the value of one feasible completion, a lower bound on $f^*(N)$, not an upper bound. Depth-first branch and bound with it returns 63, which is wrong.

**Non-example: a heuristic estimate.** An estimate of $f^*(N)$ that is often close but sometimes below it is not a bounding function. It can be used to choose the next node, but not to fathom.

**Non-example: a fractional fill in the wrong order.** A greedy fractional fill that takes the items by weight, not by ratio, gives one fractional packing, not the best one. Its value can be below the optimum, so it is not valid in general.

## Related definitions

- [Incumbent solution](/incumbent-solution/): the value compared with the bound. A node with $ub(N) \le z$ is fathomed.
- [Fathoming rule](/fathoming-rule/): fathoming by bound is one of the rules; the others are infeasibility and optimality.
- **Root gap.** The difference between the bound at the root and the optimum, $70.125 - 64$ above, measures the bound. With a gap of 0 the search can stop at the root once a solution of that value is found.
- [Admissible heuristic](/admissible-heuristic/): in shortest path search, a heuristic that never overestimates the remaining cost; $g + h$ is then a lower bounding function for the paths through a node.
- **Dual bound.** In integer programming, the largest bound of a live node is the dual bound, and the incumbent value is the primal bound.

## References
