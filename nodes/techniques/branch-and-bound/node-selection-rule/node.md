---
tag: 8WW9H4
kind: definition
slug: node-selection-rule
name: Node selection rule
aliases:
- search strategy in branch and bound
area: techniques/branch-and-bound
level: core
summary: 'Order in which live subproblems are explored: depth-first, best-first or breadth-first.'
prereqs: [state-space-tree, bounding-function, incumbent-solution]
see_also: [depth-first-branch-and-bound, breadth-first-branch-and-bound, best-first-branch-and-bound, branching-rule, fathoming-rule, diving-heuristic, priority-queue, a-star-search]
sources:
  - paper: doi:10.1007/bf00998631
    title: Toshihide Ibaraki, Theoretical comparisons of search strategies in branch-and-bound algorithms, International Journal of Computer and Information Sciences 5(4), 1976
    locator: pp. 315 to 344
  - book: isbn:9780929306414
    title: Ellis Horowitz, Sartaj Sahni and Sanguthevar Rajasekaran, Computer Algorithms, second edition
    locator: Chapter 8, Branch-and-Bound (FIFO, LIFO and LC search)
  - book: isbn:9780471283669
    title: Laurence A. Wolsey, Integer Programming
    locator: Chapter 7, Branch and Bound (choice of node)
  - paper: doi:10.1287/opre.14.4.699
    title: E. L. Lawler and D. E. Wood, Branch-and-bound methods, a survey, Operations Research 14(4), 1966
    locator: pp. 699 to 719
---

The node selection rule of a branch and bound search decides which live node, among the subproblems that wait to be processed, the search takes next. The three basic rules are depth-first (the newest node, from a stack), breadth-first (the oldest node, from a queue) and best-first (the node with the best bound, from a priority queue). The rule does not change the answer, but it decides how many nodes are expanded, how much memory the live nodes take, and how soon a good [incumbent](/incumbent-solution/) appears.

## Definition

During a branch and bound search, a node is **live** if it has been made but not yet processed. Let $L_t$ be the set of live nodes before step $t$. A **node selection rule** is a function $\sigma$ that, given $L_t$ and the state of the search (incumbent, bounds, the order in which the nodes were made), returns a node $\sigma(L_t) \in L_t$, which the search processes in step $t$.

Let a node $N$ have bound $ub(N)$ (maximization) and depth $d(N)$, and let $\tau(N)$ be the time it was made. The basic rules are:

- **Depth-first, or LIFO.** $\sigma(L)$ is the node of $L$ with the largest $\tau$. With the children made in a fixed order, this is depth-first search; the live nodes form a stack. See [depth-first branch and bound](/depth-first-branch-and-bound/).
- **Breadth-first, or FIFO.** $\sigma(L)$ is the node with the smallest $\tau$; the live nodes form a queue. See [breadth-first branch and bound](/breadth-first-branch-and-bound/).
- **Best-first, or best bound, or least cost.** $\sigma(L)$ is a node with the largest $ub$ (the smallest lower bound for minimization), with a fixed tie-break; the live nodes form a [priority queue](/priority-queue/). See [best-first branch and bound](/best-first-branch-and-bound/).
- **Best estimate.** $\sigma(L)$ maximizes an estimate $e(N)$ of the best solution below $N$, which need not be a bound.

A rule is **correct** for any choice: the proof of branch and bound uses only that each live node is processed or fathomed, not the order. Hybrid rules change between these during the search, for example by going depth-first from a node until it is fathomed, and then taking the next node by best bound.

## Examples and non-examples

Take the 0-1 knapsack instance with capacity 14, values $14, 12, 18, 19, 19, 20$ and weights $1, 1, 2, 7, 8, 10$, already in ratio order, with the fractional bound, the take child made before the leave child, and the incumbent updated only at complete solutions. The optimum is 64.

| rule | nodes expanded | most live nodes at one time |
|---|---|---|
| depth-first | 9 | 5 |
| breadth-first | 55 | 32 |
| best-first | 9 | 7 |

Best-first search expands only nodes with bound at least 64, and every search with this bound expands the nodes whose bound, and whose ancestors' bounds, are above 64. Depth-first search reaches the optimum early on this instance and matches it with less memory. Breadth-first search finds no complete solution before depth 6 and so fathoms nothing at depths 0 to 5.

**Example: the order of the children.** Depth-first search on the same instance, but with the leave child before the take child, expands 47 nodes instead of 9: its first complete solutions are poor, so the bound cannot act. For depth-first search, the order in which the children are tried is part of the selection rule.

**Example: the earlier instance.** On capacity 16, values $40, 30, 50, 10$ and weights $2, 5, 10, 5$, the three rules expand 6, 14 and 5 nodes.

**Non-example: dropping a live node.** A rule that removes a live node without processing it, for example a beam search that keeps only the best $k$ nodes at each depth, is not a node selection rule of an exact branch and bound method: it can lose the optimum.

**Non-example: the branching rule.** The choice of which variable to fix at a node is a [branching rule](/branching-rule/), not a node selection rule. The two choices are independent.

## Related definitions

- [Branching rule](/branching-rule/): how a selected node is split.
- [Fathoming rule](/fathoming-rule/): when a selected node is discarded without being split.
- **Critical nodes.** With a fixed bound, a node whose bound and whose ancestors' bounds all exceed the optimum is processed under every rule. Best-first search processes only these and nodes whose bound equals the optimum; this is why it minimizes the number of nodes. Ibaraki (1976) compares the rules in this way.
- **Diving.** In integer programming, a [diving heuristic](/diving-heuristic/) is a depth-first run from a node to find an incumbent; it is the depth-first part of a hybrid rule.
- [A* search](/a-star-search/): best-first selection by $g + h$ in a graph of states, the same rule as best-first branch and bound with a lower bound.

## References
