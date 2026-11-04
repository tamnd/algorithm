---
tag: Z9RZB6
kind: algorithm
slug: breadth-first-branch-and-bound
name: Breadth-first branch and bound
aliases:
- BFBB
- FIFO branch and bound
area: techniques/branch-and-bound
level: core
summary: Branch and bound that expands the tree level by level using a FIFO queue of live nodes.
model: word-ram
complexity:
  vars: {T: the number of nodes of the search tree, w: the largest number of nodes of the tree at one depth}
  time: {worst: O(T)}
  space: {extra: O(w)}
properties: {deterministic: true, recursive: false}
prereqs: [state-space-tree, bounding-function, incumbent-solution, breadth-first-search]
see_also: [depth-first-branch-and-bound, best-first-branch-and-bound, node-selection-rule, fathoming-rule, knapsack-branch-and-bound, queue, bfs-layers]
sources:
  - book: isbn:9780929306414
    title: Ellis Horowitz, Sartaj Sahni and Sanguthevar Rajasekaran, Computer Algorithms, second edition
    locator: Chapter 8, Branch-and-Bound (FIFO branch-and-bound)
  - paper: doi:10.1287/opre.14.4.699
    title: E. L. Lawler and D. E. Wood, Branch-and-bound methods, a survey, Operations Research 14(4), 1966
    locator: pp. 699 to 719
  - paper: doi:10.1007/bf00998631
    title: Toshihide Ibaraki, Theoretical comparisons of search strategies in branch-and-bound algorithms, International Journal of Computer and Information Sciences 5(4), 1976
    locator: pp. 315 to 344
---

Breadth-first branch and bound searches the [state space tree](/state-space-tree/) of an optimization problem level by level. The live nodes wait in a first-in first-out [queue](/queue/), so all nodes at depth $k$ are expanded before any node at depth $k + 1$. As in every branch and bound method, the search keeps an [incumbent](/incumbent-solution/) and discards each node whose [bound](/bounding-function/) cannot beat it. Horowitz and Sahni call it FIFO branch and bound. It is simple and finds a solution of fewest decisions first, but it can keep a whole level of the tree in memory and it finds its first complete solution late.

## In plain words

You look for the best answer in a large tree of choices. You look at all choices of the first step, then all choices of the second step, and so on, one level at a time. You keep the nodes that wait for their turn in a line: new nodes join at the back, and you always take the node at the front.

At each node you compute a quick limit: no full answer below it can be better than this number. If the limit is not better than the best full answer you have, you drop the node.

The weak point is that full answers only appear at the deepest level. Until you get there, you have no best answer to compare with, so few nodes are dropped and the line can get very long.

## The problem

The input is a finite rooted tree $T$, given by a root and a function that lists the children of a node, and a value $f(x)$ for each leaf $x$. Some nodes are marked as *leaves*: they are the feasible solutions and have no children. An inner node with no children is a dead end. The task is to find a leaf of largest value. A *bounding function* $ub$ gives for each node $N$ a number with $ub(N) \ge f(x)$ for every leaf $x$ in the subtree of $N$. For minimization, replace $f$ by $-f$.

## The algorithm

```pseudo id=main
BFBB(root)
L1  z ← −∞; best ← NIL                      ▷ the incumbent and its value
L2  Q ← a FIFO queue that holds only root
L3  while Q is not empty do
L4      N ← DEQUEUE(Q)                       ▷ the oldest live node
L5      if ub(N) ≤ z then continue          ▷ fathomed by the bound
L6      if N is a leaf then
L7          if f(N) > z then z ← f(N); best ← N
L8          continue
L9      for each child C of N, in order do
L10         if ub(C) > z then ENQUEUE(Q, C)
L11 return (z, best)
```

The only difference from [depth-first branch and bound](/depth-first-branch-and-bound/) is the queue in place of the stack. Line L5 tests the bound again when a node leaves the queue, because the incumbent may have improved since the node joined it.

## Example

Take the 0-1 [knapsack problem](/knapsack-problem/) with capacity $W = 16$ and four items sorted by value per unit weight: values $40, 30, 50, 10$ and weights $2, 5, 10, 5$. A node at depth $k$ has decided items $1, \ldots, k$; its first child takes item $k + 1$ if it fits, and its second child leaves it. Leaves are at depth 4. The bound is the [fractional knapsack](/fractional-knapsack/) bound, which is 115 at the root. The table lists the nodes by depth, as the set of items taken and the bound.

| depth | nodes expanded, with $ub$ | $z$ after the level |
|---|---|---|
| 0 | $\{\}$ 115 | $-\infty$ |
| 1 | $\{1\}$ 115, $\{\}$ 82 | $-\infty$ |
| 2 | $\{1, 2\}$ 115, $\{1\}$ 98, $\{2\}$ 82, $\{\}$ 60 | $-\infty$ |
| 3 | $\{1, 2\}$ 80, $\{1, 3\}$ 98, $\{1\}$ 50, $\{2, 3\}$ 82, $\{2\}$ 40, $\{3\}$ 60, $\{\}$ 10 | $-\infty$ |
| 4 | leaves: $\{1, 2, 4\}$ 80, then $\{1, 3\}$ 90; the other 10 are fathomed | 90 |

No leaf is reached before depth 4, so no node at depths 0 to 3 is fathomed: all 14 inner nodes of the tree are expanded, and 12 leaves are in the queue at the same time. The first leaf, $\{1, 2, 4\}$, gives $z = 80$; the third, $\{1, 3\}$, gives $z = 90$, and the remaining 10 leaves have bounds at most 80 and are dropped at line L5. The answer is items 1 and 3, value 90. On the same instance, [depth-first branch and bound](/depth-first-branch-and-bound/) expands 6 nodes with at most 4 on its stack, and [best-first branch and bound](/best-first-branch-and-bound/) expands 5.

For knapsack, every node is itself a feasible packing. If the incumbent is also updated at inner nodes, breadth-first search does much better on this instance; [knapsack branch and bound](/knapsack-branch-and-bound/) uses that rule.

## Correctness

The proof for [depth-first branch and bound](/depth-first-branch-and-bound/) does not use the order in which nodes leave the container, so it applies here. At the start of each iteration, every leaf $x$ with $f(x) > z$ lies below a node in $Q$: a node leaves $Q$ only when it is fathomed with $ub(N) \le z$, when it is a leaf and $z$ is updated, or when its children with $ub(C) > z$ join $Q$. Each node joins $Q$ at most once, so the loop ends, and then no leaf beats $z$. So $z$ is the optimum and $best$ is an optimal leaf. The [proof](proofs/correctness.md) gives the details.

## Complexity

Count one unit for each evaluation of $ub$, of $f$ and of a child.

- **Time.** Each node joins the queue at most once and costs $O(1)$ units plus one unit for each child, so the time is $O(T)$ units for a tree of $T$ nodes. With no fathoming, this is a full [breadth-first search](/breadth-first-search/) of the tree.
- **Space.** By induction on the number of iterations, the depths of the nodes in the queue never decrease from front to back and differ by at most 1, so at any time the queue holds nodes of at most two consecutive depths. So the queue holds at most $2w$ nodes, where $w$ is the largest number of nodes of the tree at one depth, and the extra space is $O(w)$. For a complete $b$-ary tree of depth $d$ this is $b^d$, exponential in the depth.
- **Fathoming starts late.** If all leaves are at the same depth $d$ and no incumbent is known at the start, every node at depths below $d$ whose bound is finite is expanded, as in the example. A good starting incumbent or updates at inner nodes are needed for the bound to act.

## Properties

- **Exact.** It returns an optimal solution when $ub$ is a valid bound.
- **Level order.** Nodes are expanded in order of depth, and within one depth in the order they were made. When leaves occur at different depths, the first leaf found has the least depth.
- **Not anytime.** In trees whose leaves are all at depth $d$, no complete solution is known until the search reaches depth $d$.
- **Memory.** The queue can hold a whole level of the tree, which is much more than the $O(d b)$ of depth-first search, where $d$ is the depth and $b$ the largest number of children.
- **Compared with best-first.** With the same bound, [best-first search](/best-first-branch-and-bound/) expands only nodes whose bound is at least the optimum. Breadth-first search has no such guarantee, and the example shows a large gap.

## Variants and improvements

- **Inner-node incumbent.** When partial solutions are feasible, update $z$ at every node. For knapsack this makes breadth-first search competitive, as on the [knapsack page](/knapsack-branch-and-bound/).
- **Heuristic start.** Set $z$ from a greedy solution before line L3.
- **Beam search.** Keep only the best $k$ nodes of each level. This bounds the memory but gives up exactness.
- **Parallel expansion.** The nodes of one level do not depend on each other, so a level can be expanded in parallel, with one update of the incumbent at the end of the level.

## When to use it

Use breadth-first branch and bound when leaves occur at many depths and a solution with few decisions is wanted, when the tree is shallow and wide, or when nodes of a level are processed in parallel. For deep trees with leaves at the bottom, prefer [depth-first branch and bound](/depth-first-branch-and-bound/) for memory and [best-first branch and bound](/best-first-branch-and-bound/) for the number of nodes.

## Pitfalls

- **No second test.** Without line L5, a node that joined the queue before the incumbent improved is still expanded.
- **Memory.** The queue can grow to a whole level of the tree. Bound it, or switch to depth-first order when it grows too large.
- **No incumbent until the bottom.** Without a heuristic incumbent, the bound has nothing to compare with, and the search is close to exhaustive down to the depth of the first leaf.
- **Invalid bounds.** A heuristic estimate that can be below the best leaf of a subtree may fathom the optimum.

## Implementations

## History

Lawler and Wood (1966) described branch and bound with a choice of the next node to branch from, and Ibaraki (1976) compared the depth-first, breadth-first and best-first search strategies. Horowitz and Sahni present FIFO branch and bound, with a queue of live nodes, next to LIFO and least-cost branch and bound in their chapter on the method.

## References
