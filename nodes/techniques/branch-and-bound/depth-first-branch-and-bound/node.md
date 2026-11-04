---
tag: W90WR2
kind: algorithm
slug: depth-first-branch-and-bound
name: Depth-first branch and bound
aliases:
- DFBB
- depth-first B&B
area: techniques/branch-and-bound
level: intro
summary: Branch and bound that expands the deepest live node first, keeping memory linear in tree depth.
model: word-ram
complexity:
  vars: {T: the number of nodes of the search tree, d: the depth of the tree, b: the largest number of children of a node}
  time: {worst: O(T), best: O(d b)}
  space: {extra: O(d b)}
properties: {deterministic: true, recursive: false}
prereqs: [state-space-tree, bounding-function, incumbent-solution, depth-first-search]
see_also: [breadth-first-branch-and-bound, best-first-branch-and-bound, node-selection-rule, fathoming-rule, knapsack-branch-and-bound, generic-backtracking-algorithm, branching-rule, stack]
sources:
  - book: isbn:9780929306414
    title: Ellis Horowitz, Sartaj Sahni and Sanguthevar Rajasekaran, Computer Algorithms, second edition
    locator: Chapter 8, Branch-and-Bound (live nodes, E-nodes, bounding)
  - paper: doi:10.1287/opre.14.4.699
    title: E. L. Lawler and D. E. Wood, Branch-and-bound methods, a survey, Operations Research 14(4), 1966
    locator: pp. 699 to 719
  - paper: doi:10.1287/opre.18.1.24
    title: L. G. Mitten, Branch-and-bound methods, general formulation and properties, Operations Research 18(1), 1970
    locator: pp. 24 to 34
  - paper: doi:10.1007/bf00998631
    title: Toshihide Ibaraki, Theoretical comparisons of search strategies in branch-and-bound algorithms, International Journal of Computer and Information Sciences 5(4), 1976
    locator: pp. 315 to 344
  - paper: doi:10.1287/opre.11.6.972
    title: John D. C. Little, Katta G. Murty, Dura W. Sweeney and Caroline Karel, An algorithm for the traveling salesman problem, Operations Research 11(6), 1963
    locator: pp. 972 to 989
---

Depth-first branch and bound (DFBB) searches the [state space tree](/state-space-tree/) of an optimization problem in depth-first order. It keeps the best complete solution found so far, the [incumbent](/incumbent-solution/), and it discards each node whose [bound](/bounding-function/) shows that no solution below it can beat the incumbent. The live nodes wait on a [stack](/stack/), so the memory is proportional to the depth of the tree times the number of children of a node. It is [backtracking](/generic-backtracking-algorithm/) with one more test, and it is the [node selection rule](/node-selection-rule/) that most solvers use when memory is small or when a good solution is needed early.

## In plain words

You look for the best answer in a large tree of choices. You go down one branch until you reach a full answer, and you remember it as the best so far. Then you go back up and try the other branches, one at a time, the deepest first.

At each node you compute a quick limit: no full answer below this node can be better than this number. If the limit is not better than the best answer you already have, you skip the whole branch.

Because you always finish one branch before you start the next, you only need to remember the path you are on and the brothers and sisters of the nodes on that path. A good first answer makes the skips start early.

## The problem

The input is a finite rooted tree $T$, given by a root and a function that lists the children of a node, and a value $f(x)$ for each leaf $x$. Some nodes are marked as *leaves*: they are the feasible solutions and have no children. An inner node with no children is a dead end. The task is to find a leaf of largest value. The tree is not built in advance; it is the tree of [partial solutions](/partial-solution/) of the problem, and only the nodes that the search reaches are made. The page uses maximization. For minimization, replace $f$ by $-f$, or exchange $\le$ and $\ge$ and use a lower bound.

A *bounding function* $ub$ gives for each node $N$ a number with
$$ub(N) \ge f(x) \quad \text{for every leaf } x \text{ in the subtree of } N.$$
It is usually the optimum of a relaxation of the subproblem at $N$.

## The algorithm

```pseudo id=main
DFBB(root)
L1  z ← −∞; best ← NIL                      ▷ the incumbent and its value
L2  S ← a stack that holds only root
L3  while S is not empty do
L4      N ← POP(S)
L5      if ub(N) ≤ z then continue          ▷ fathomed by the bound
L6      if N is a leaf then
L7          if f(N) > z then z ← f(N); best ← N
L8          continue
L9      for each child C of N, from the last to the first do
L10         if ub(C) > z then PUSH(S, C)
L11 return (z, best)
```

Line L9 pushes the children in reverse, so the first child is on top of the stack and is expanded first. A node is tested twice against the incumbent: at line L10 when it is made, and at line L5 when it leaves the stack, because $z$ may have grown in between. The recursive form, which calls itself on each child in order, is the same algorithm.

## Example

Take the 0-1 [knapsack problem](/knapsack-problem/) with capacity $W = 16$ and four items, already sorted by value per unit weight:

| item | 1 | 2 | 3 | 4 |
|---|---|---|---|---|
| value | 40 | 30 | 50 | 10 |
| weight | 2 | 5 | 10 | 5 |
| value / weight | 20 | 6 | 5 | 2 |

A node at depth $k$ has decided items $1, \ldots, k$; its first child takes item $k + 1$, if it fits, and its second child leaves it. The leaves are at depth 4. The bound is the [fractional knapsack](/fractional-knapsack/) bound: add the remaining items in order while they fit, then add the fitting fraction of the next one. At the root it is $40 + 30 + \frac{9}{10} \cdot 50 = 115$.

| step | node popped (items taken, depth) | $ub$ | action | $z$ |
|---|---|---|---|---|
| 1 | $\{\}$, 0 | 115 | push $\{1\}$ (115) and $\{\}$ (82) | $-\infty$ |
| 2 | $\{1\}$, 1 | 115 | push $\{1, 2\}$ (115) and $\{1\}$ (98) | $-\infty$ |
| 3 | $\{1, 2\}$, 2 | 115 | item 3 does not fit; push $\{1, 2\}$ (80) | $-\infty$ |
| 4 | $\{1, 2\}$, 3 | 80 | push $\{1, 2, 4\}$ (80) and $\{1, 2\}$ (70) | $-\infty$ |
| 5 | $\{1, 2, 4\}$, 4 | 80 | leaf of value 80 | 80 |
| 6 | $\{1, 2\}$, 4 | 70 | $70 \le 80$: fathomed | 80 |
| 7 | $\{1\}$, 2 | 98 | push $\{1, 3\}$ (98); $\{1\}$ (50) is not pushed | 80 |
| 8 | $\{1, 3\}$, 3 | 98 | item 4 does not fit; push $\{1, 3\}$ (90) | 80 |
| 9 | $\{1, 3\}$, 4 | 90 | leaf of value 90 | 90 |
| 10 | $\{\}$, 1 | 82 | $82 \le 90$: fathomed | 90 |

The answer is items 1 and 3, value 90, weight 12. The search expands 6 nodes, puts 10 nodes on the stack, counting the root, and never has more than 4 nodes on the stack. The tree of feasible partial solutions has 26 nodes. On the same instance, [best-first branch and bound](/best-first-branch-and-bound/) expands 5 nodes and [breadth-first branch and bound](/breadth-first-branch-and-bound/) expands 14. The first leaf that DFBB finds has value 80, below the optimum, so DFBB expands the node $\{1, 2\}$ at depth 3 with bound $80 < 90$, which best-first search never expands.

## Correctness

Let $z^*$ be the largest value of a leaf, or $-\infty$ if $T$ has no leaf. At the start of each iteration of line L3, the following holds: every leaf $x$ with $f(x) > z$ is in the subtree of some node on $S$. It holds at the start, when $S$ holds the root. A node leaves $S$ at line L4. If line L5 drops it, each leaf $x$ below it has $f(x) \le ub(N) \le z$. If it is a leaf, then after line L7 it has $f(N) \le z$. Otherwise each leaf below $N$ is below a child $C$, and a child that line L10 does not push has $ub(C) \le z$. As $z$ only grows, the invariant is kept. The loop ends because each node is pushed at most once and $T$ is finite. At the end $S$ is empty, so no leaf has $f(x) > z$; and $z$ is $-\infty$ or the value of the leaf $best$. So $z = z^*$ and $best$ is an optimal leaf. The [proof](proofs/correctness.md) gives the details.

## Complexity

Count one unit for each evaluation of $ub$, of $f$ and of a child. Each node is pushed at most once, and each pushed node costs $O(1)$ units when it is popped plus one unit for each of its children.

- **Worst case.** $O(T)$ units, where $T$ is the number of nodes of the tree, because no node is pushed twice. This is reached when the bound never fathoms anything, for example when $ub = +\infty$; then DFBB is a full [depth-first search](/depth-first-search/) of the tree, whose size is often exponential in the input. Most problems that DFBB is used for are [NP-hard](/np-hard/), so no bound makes the worst case polynomial unless P = NP.
- **Best case.** If the first leaf is optimal and every other child has a bound at most its value, the search expands the $d$ nodes on one path and makes at most $b$ children at each: $O(d b)$ units.
- **Space.** When a node at depth $k$ is popped, the stack holds, for each depth $j \le k$, at most $b - 1$ younger children of the node at depth $j - 1$ of the current path. So the stack never holds more than $d (b - 1) + 1$ nodes, which is $O(d b)$. For binary trees this is $O(d)$.

## Properties

- **Exact.** It returns an optimal solution when $ub$ is a valid bound.
- **Anytime.** If each inner node has at least one child, it reaches its first leaf after at most $d$ expansions, and the incumbent only improves. Stopped early, it returns a feasible solution and, with the largest bound of a node on the stack, a gap to the optimum.
- **Linear memory.** The stack is $O(d b)$, against the exponential number of live nodes that breadth-first and best-first search can hold.
- **More nodes than best-first.** DFBB may expand a node with $ub(N) < z^*$, as in step 8 of the example, while best-first search with the same bound never does. Ibaraki (1976) compares the search orders formally.
- **Deterministic.** The order of the children fixes the run. Changing it may change which optimal leaf is returned, but not the value.

## Variants and improvements

- **Update the incumbent at inner nodes.** When each partial solution is itself feasible, as in knapsack, set $z$ to its value at every node, not only at leaves. See [knapsack branch and bound](/knapsack-branch-and-bound/).
- **Start with a heuristic incumbent.** A good $z$ from a greedy or local search method, before line L3, fathoms nodes from the first step.
- **Child order.** Expand first the child with the larger bound, or the child that a heuristic likes. This is the main way to get a good incumbent early, and [diving heuristics](/diving-heuristic/) in integer programming use the same idea.
- **Hybrids.** Solvers for [mixed integer programming](/mixed-integer-programming/) dive depth-first until a leaf or a fathom, then jump to a node with a good bound, mixing DFBB with [best-first branch and bound](/best-first-branch-and-bound/).

## When to use it

Use DFBB when the tree is deep and the number of live nodes of a best-first search would not fit in memory, when a feasible solution is needed early, or when the bound is cheap and a good incumbent is easy to reach by going down. Use best-first search instead when the bound is strong and memory is enough, as then it expands fewer nodes. DFBB is the usual choice for exact search on permutations and subsets, and for constraint optimization.

## Pitfalls

- **No second test.** If line L5 is missing, nodes pushed before the incumbent improved are still expanded. The result stays correct, but the gain of the bound is lost.
- **Strict and non-strict tests.** With $ub(N) \le z$ the search finds one optimal solution. To list all optimal solutions, fathom only when $ub(N) < z$ and keep a list at line L7.
- **Invalid bounds.** A bound that is below the best leaf of some subtree can fathom the optimal solution. A heuristic estimate is not a bound. Test the bound against brute force on small instances.
- **Float bounds.** With a fractional bound, $ub(N)$ can be $89.999\ldots$ for a subtree whose best value is 90. With integer values, compare $\lfloor ub(N) \rfloor$ with $z$, or add a small tolerance in the safe direction.
- **Recursion depth.** The recursive form has depth $d$; for deep trees, use an explicit stack.

## Implementations

## History

Land and Doig (1960) used bounds from linear programs to cut down the search of an integer program, and Little, Murty, Sweeney and Karel (1963) gave the method the name *branch and bound* in their algorithm for the traveling salesman problem. Lawler and Wood (1966) and Mitten (1970) gave general formulations, and Ibaraki (1976) compared depth-first, breadth-first and best-first search in a common framework.

## References
