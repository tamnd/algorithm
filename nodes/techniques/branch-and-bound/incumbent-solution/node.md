---
tag: J84JJ5
kind: definition
slug: incumbent-solution
name: Incumbent solution
aliases:
- incumbent
- best known solution
area: techniques/branch-and-bound
level: intro
summary: Best feasible solution found so far, used as the threshold for pruning.
prereqs: [state-space-tree]
see_also: [bounding-function, fathoming-rule, node-selection-rule, depth-first-branch-and-bound, best-first-branch-and-bound, knapsack-branch-and-bound, mixed-integer-programming, diving-heuristic]
sources:
  - book: isbn:9780471283669
    title: Laurence A. Wolsey, Integer Programming
    locator: Chapter 7, Branch and Bound (the incumbent, primal and dual bounds, pruning)
  - paper: doi:10.1287/opre.14.4.699
    title: E. L. Lawler and D. E. Wood, Branch-and-bound methods, a survey, Operations Research 14(4), 1966
    locator: pp. 699 to 719
  - book: isbn:9780929306414
    title: Ellis Horowitz, Sartaj Sahni and Sanguthevar Rajasekaran, Computer Algorithms, second edition
    locator: Chapter 8, Branch-and-Bound (the value of the best answer node found so far)
---

The incumbent solution of a [branch and bound](/depth-first-branch-and-bound/) search is the best feasible solution that the search has found up to now. Its value is a lower bound on the optimum of a maximization problem, and an upper bound for a minimization problem. The search compares the [bound](/bounding-function/) of each node with the value of the incumbent and discards the node when the bound cannot beat it. In integer programming the value of the incumbent is also called the *primal bound*.

## Definition

Let a branch and bound search maximize $f$ over a finite set $S$ of feasible solutions, and let $z^* = \max_{x \in S} f(x)$. At each moment of the search, let $S_t \subseteq S$ be the set of feasible solutions that the search has found so far: at leaves, at inner nodes whose partial solution is feasible, or by a heuristic.

- The **incumbent** is an element $\hat{x} \in S_t$ with $f(\hat{x}) = \max_{x \in S_t} f(x)$. If $S_t$ is empty, there is no incumbent.
- The **incumbent value** is $z = f(\hat{x})$, or $z = -\infty$ if there is no incumbent. A search may also start from a value $z_0$ given in advance, with or without a solution of that value; then $z = \max(z_0, \max_{x \in S_t} f(x))$.

For minimization, replace max by min and $-\infty$ by $+\infty$.

Two facts follow at once. Since $S_t$ only grows, $z$ never decreases. Since $\hat{x} \in S$, the value satisfies $z \le z^*$, if $z$ comes from a solution. With $L$ the set of live nodes and $ub$ a valid bound, every solution not yet found lies below a live node, so
$$z \le z^* \le \max\Big(z, \max_{N \in L} ub(N)\Big).$$
The difference between the two sides is the *gap*; the search proves $\hat{x}$ optimal when the gap is 0, which happens at the latest when $L$ is empty. A node $N$ with $ub(N) \le z$ cannot contain a solution better than the incumbent; this is fathoming by bound, see [fathoming rule](/fathoming-rule/).

## Examples and non-examples

**Example: the incumbent during a knapsack search.** Take capacity 16 and items with values $40, 30, 50, 10$ and weights $2, 5, 10, 5$. In [knapsack branch and bound](/knapsack-branch-and-bound/) every node is a feasible packing, and the incumbent value takes the values $0, 40, 70, 80, 90$ over the run. When it becomes 80, the live nodes have bounds 98 and 82, so the gap is $98 - 80 = 18$. When it becomes 90, the only live node left has bound 82, so the gap is 0, and that node is fathomed. In [depth-first branch and bound](/depth-first-branch-and-bound/) that updates only at full solutions, the incumbent is $-\infty$ for the first four expansions, then 80, then 90.

**Example: a heuristic start.** The greedy packing in ratio order takes items 1, 2 and 4, value 80. If depth-first branch and bound starts with $z = 80$, it expands 5 nodes instead of 6 and holds at most 3 live nodes instead of 4 on the same instance. If it starts with $z = 89$, it still expands 5 nodes and holds at most 2.

**Example: start value without a solution.** Starting with $z_0 = 90$, the optimum, the search expands the 5 nodes whose bound exceeds 90 and finds no solution of value above 90, so it returns no incumbent. A start value is only safe when it is at most $z^*$, or when the caller has a solution of that value.

**Non-example: the best bound.** The root bound 115 in the example is not an incumbent value. It is an upper bound on $z^*$, the *dual bound* of integer programming, and no packing has this value.

**Non-example: a rounded relaxation.** The fractional solution at the root takes $9/10$ of item 3. Rounding it up to "take item 3" gives weight 17, which is not feasible, so it cannot be an incumbent. Only feasible solutions qualify.

**Non-example: an estimate.** The value that a heuristic predicts for the best leaf below a node is not an incumbent, since no solution of that value is known. Using it as $z$ can fathom the optimum.

## Related definitions

- [Bounding function](/bounding-function/): gives the other side of the gap. Branch and bound compares the bound of a node with the incumbent value.
- [Fathoming rule](/fathoming-rule/): the rules that discard a node; fathoming by bound uses the incumbent.
- [Node selection rule](/node-selection-rule/): decides how fast the incumbent improves. Depth-first order finds incumbents early; best-first order finds them late but expands the fewest nodes.
- **Primal and dual bounds.** In [mixed integer programming](/mixed-integer-programming/), the incumbent value is the primal bound and the best bound of a live node is the dual bound. Solvers report the relative gap $(ub - z) / |z|$ and stop when it is small enough.
- **Primal heuristics.** Methods that look for good feasible solutions during the search, such as [diving heuristics](/diving-heuristic/), exist only to improve the incumbent.

## References
