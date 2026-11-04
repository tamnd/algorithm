---
tag: 0SPYHN
kind: algorithm
slug: best-first-branch-and-bound
name: Best-first branch and bound
aliases:
- least-cost branch and bound
- LC search
area: techniques/branch-and-bound
level: core
summary: Branch and bound that always expands the live node with the best bound, held in a priority queue.
model: word-ram
complexity:
  vars: {T: the number of nodes of the search tree, d: the depth of the tree, b: the largest number of children of a node}
  time: {worst: O(T log T), best: O(d b log(d b))}
  space: {extra: O(T)}
properties: {deterministic: true, recursive: false}
prereqs: [state-space-tree, bounding-function, incumbent-solution, priority-queue]
see_also: [depth-first-branch-and-bound, breadth-first-branch-and-bound, node-selection-rule, fathoming-rule, a-star-search, binary-heap, knapsack-branch-and-bound, little-algorithm]
sources:
  - book: isbn:9780929306414
    title: Ellis Horowitz, Sartaj Sahni and Sanguthevar Rajasekaran, Computer Algorithms, second edition
    locator: Chapter 8, Branch-and-Bound (least cost, LC, search)
  - paper: doi:10.1287/opre.14.4.699
    title: E. L. Lawler and D. E. Wood, Branch-and-bound methods, a survey, Operations Research 14(4), 1966
    locator: pp. 699 to 719
  - paper: doi:10.1007/bf00998631
    title: Toshihide Ibaraki, Theoretical comparisons of search strategies in branch-and-bound algorithms, International Journal of Computer and Information Sciences 5(4), 1976
    locator: pp. 315 to 344
  - paper: doi:10.2307/1910129
    title: A. H. Land and A. G. Doig, An automatic method of solving discrete programming problems, Econometrica 28(3), 1960
    locator: pp. 497 to 520
---

Best-first branch and bound keeps its live nodes in a [priority queue](/priority-queue/) and always expands the node with the best [bound](/bounding-function/): the largest upper bound for a maximization problem, or the smallest lower bound for a minimization problem. As in every branch and bound method, it keeps an [incumbent](/incumbent-solution/) and discards nodes whose bound cannot beat it. Its strength is that it never expands a node whose bound is worse than the optimum, so with a given bound it expands the fewest nodes of any search order, up to ties. Its weakness is memory: the queue can grow to a large part of the tree. Horowitz and Sahni call it least-cost (LC) branch and bound.

## In plain words

You look for the best answer in a large tree of choices. For each node that waits for its turn, you know a quick limit: no full answer below it can be better than this number. You always open next the node with the most promising limit.

When you open a node, you compute the limits of its children and put them in the waiting list. When you reach a full answer, you remember it if it is the best so far. When the most promising limit in the list is not better than your best answer, no waiting node can help, and you stop.

This order wastes no work on nodes that look worse than the true best answer. The cost is that the waiting list can get very long.

## The problem

The input is a finite rooted tree $T$, given by a root and a function that lists the children of a node, and a value $f(x)$ for each leaf $x$. Some nodes are marked as *leaves*: they are the feasible solutions and have no children. An inner node with no children is a dead end. The task is to find a leaf of largest value. A *bounding function* $ub$ gives for each node $N$ a number with $ub(N) \ge f(x)$ for every leaf $x$ in the subtree of $N$. For minimization, replace $f$ by $-f$ and $ub$ by $-lb$.

## The algorithm

```pseudo id=main
BEST-FIRST-BB(root)
L1  z ← −∞; best ← NIL                      ▷ the incumbent and its value
L2  H ← a max-priority queue that holds root with key ub(root)
L3  while H is not empty do
L4      N ← EXTRACT-MAX(H)                   ▷ the live node with the largest bound
L5      if ub(N) ≤ z then break             ▷ no live node can beat z
L6      if N is a leaf then
L7          if f(N) > z then z ← f(N); best ← N
L8          continue
L9      for each child C of N, in order do
L10         if ub(C) > z then INSERT(H, C, ub(C))
L11 return (z, best)
```

Line L5 stops the whole search, not only the current node: $N$ has the largest key in $H$, so if $ub(N) \le z$, every live node has a bound at most $z$. Ties between equal keys are broken by the order of insertion in the implementation, which makes the run deterministic.

## Example

Take the 0-1 [knapsack problem](/knapsack-problem/) with capacity $W = 16$ and four items sorted by value per unit weight: values $40, 30, 50, 10$ and weights $2, 5, 10, 5$. A node at depth $k$ has decided items $1, \ldots, k$; its first child takes item $k + 1$ if it fits, and its second child leaves it. Leaves are at depth 4. The bound is the [fractional knapsack](/fractional-knapsack/) bound. A node is written as the set of items taken and its depth.

| step | node taken from $H$ | $ub$ | action | live nodes after the step (bound) |
|---|---|---|---|---|
| 1 | $\{\}$, 0 | 115 | expand | $\{1\}$,1 (115); $\{\}$,1 (82) |
| 2 | $\{1\}$, 1 | 115 | expand | $\{1, 2\}$,2 (115); $\{1\}$,2 (98); $\{\}$,1 (82) |
| 3 | $\{1, 2\}$, 2 | 115 | expand; item 3 does not fit | $\{1\}$,2 (98); $\{\}$,1 (82); $\{1, 2\}$,3 (80) |
| 4 | $\{1\}$, 2 | 98 | expand | $\{1, 3\}$,3 (98); $\{\}$,1 (82); $\{1, 2\}$,3 (80); $\{1\}$,3 (50) |
| 5 | $\{1, 3\}$, 3 | 98 | expand; item 4 does not fit | $\{1, 3\}$,4 (90); $\{\}$,1 (82); $\{1, 2\}$,3 (80); $\{1\}$,3 (50) |
| 6 | $\{1, 3\}$, 4 | 90 | leaf: $z = 90$ | 3 nodes, all with bound at most 82 |
| 7 | $\{\}$, 1 | 82 | $82 \le 90$: stop | |

The answer is items 1 and 3, value 90. The search expands 5 nodes and reaches 1 leaf. The 5 expanded nodes are exactly the nodes with bound above the optimum 90 whose ancestors also have bounds above 90, so by the theorem below every branch and bound search with this bound expands them. On the same instance, [depth-first branch and bound](/depth-first-branch-and-bound/) expands 6 nodes and [breadth-first branch and bound](/breadth-first-branch-and-bound/) expands 14.

## Correctness

At the start of each iteration, every leaf $x$ with $f(x) > z$ lies below a node of $H$. A node leaves $H$ only when it is a leaf and $z$ is updated, or when its children with $ub(C) > z$ join $H$; nodes with $ub(C) \le z$ have no leaf that beats $z$. When line L5 stops the loop, every node of $H$ has a bound at most $z$, so no leaf below it beats $z$. Each node joins $H$ at most once, so the loop ends. So $z$ is the optimum and $best$ is an optimal leaf. The [proof](proofs/correctness.md) gives the details and the theorem below.

## Complexity

Count one unit for each evaluation of $ub$, of $f$ and of a child, and $O(\log |H|)$ for each operation on a [binary heap](/binary-heap/).

- **Time.** Each node joins $H$ at most once, so there are at most $T$ insertions and $T$ extractions, and the time is $O(T \log T)$.
- **Best case.** If the bound is exact, $ub(N) = \max_{x \preceq N} f(x)$ where $x \preceq N$ means that the leaf $x$ is below $N$, and the optimal leaf is unique, then only the nodes on the path to that leaf have bound $z^*$. The search goes straight down this path and stops: $d$ expansions and $O(d b)$ heap operations on a heap of at most $d b$ nodes.
- **Space.** $H$ can hold $\Theta(T)$ nodes in the worst case: for example, when all bounds are equal and larger than every leaf value until the bottom, the search is a breadth-first search. This memory, not the time, is the usual limit of best-first search.

## Properties

Let $z^*$ be the optimum. Call a node $N$ *critical* if every node on the path from the root to $N$, including $N$, has $ub > z^*$.

**Theorem.** (a) Every branch and bound search that uses the bound $ub$, keeps $z \le z^*$, and fathoms only by $ub(N) \le z$ or by reaching a leaf, expands every critical node that is not a leaf. (b) Best-first branch and bound expands only nodes with $ub(N) \ge z^*$.

*Proof.* (a) By induction on depth. The root is critical and is live at the start. A critical inner node $N$ that is live is never fathomed, as $ub(N) > z^* \ge z$, so it is expanded; its critical children have $ub(C) > z$ and become live. (b) When best-first search takes $N$ from $H$ and expands it, $ub(N) > z$. If $z = z^*$ then $ub(N) > z^*$. Otherwise an optimal leaf lies below some node $M$ of $H$ by the invariant, so $ub(N) \ge ub(M) \ge z^*$. $\square$

So, with a given bound, best-first search expands the critical nodes, which every search must expand, plus at most some nodes whose bound equals $z^*$. If no inner node has $ub(N) = z^*$, every node it expands has $ub(N) > z^*$ and was reached through expanded nodes, so it expands exactly the critical inner nodes, the least number possible. The optimality of best-first search among search strategies is studied in Ibaraki (1976).

- **Exact.** It returns an optimal solution when $ub$ is a valid bound.
- **Gap at any time.** The largest key in $H$ is an upper bound on $z^*$ at any time, so a run stopped early gives a feasible solution and a proven gap.
- **Not anytime in practice.** It may expand many nodes high in the tree before it reaches any leaf.

## Variants and improvements

- **Hybrid with depth-first search.** Solvers for [mixed integer programming](/mixed-integer-programming/) dive depth-first from the chosen node until a fathom, then take the next node by best bound, to find incumbents early without losing the global view. See [diving heuristics](/diving-heuristic/).
- **Best estimate.** Select by an estimate of the best leaf below a node, not by the bound, to find good solutions sooner; the bound is then used only to fathom.
- **Heuristic incumbent.** A good $z$ before line L3 keeps many nodes out of $H$.
- **A\* search.** For shortest paths, best-first search on the lower bound $g(N) + h(N)$ with an [admissible heuristic](/admissible-heuristic/) $h$ is [A* search](/a-star-search/); on a tree of partial paths, it is best-first branch and bound with minimization.

## When to use it

Use best-first branch and bound when the bound is strong and the number of live nodes fits in memory, and when the goal is to prove optimality with the fewest nodes. When memory is short, or a feasible solution is needed early, use [depth-first branch and bound](/depth-first-branch-and-bound/), or a hybrid.

## Pitfalls

- **Ties.** With many equal bounds, the order of ties decides how many nodes with $ub = z^*$ are expanded. Breaking ties toward deeper nodes reaches leaves sooner.
- **Stale keys.** A node's key is its bound when it joined $H$. If the bound of a node can improve later, for example by a new cut, the key is out of date; this is safe, as the stored key is still a valid bound, but the order is no longer exact.
- **Memory.** Without a good incumbent, $H$ grows fast. Monitor it and switch to depth-first order when it gets too large.
- **Wrong direction.** For minimization, the queue is a min-queue on the lower bound, and line L5 tests $lb(N) \ge z$.

## Implementations

## History

Land and Doig (1960) chose, among the live subproblems of an integer program, one with the best value of its linear program relaxation, which is best-first selection. Lawler and Wood (1966) present the selection of the node with the best bound in their survey of branch and bound methods, and Ibaraki (1976) analyzed the search strategies formally. Horowitz and Sahni use the name least-cost (LC) search.

## References
