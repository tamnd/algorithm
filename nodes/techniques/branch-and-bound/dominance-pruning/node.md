---
tag: TBSRAQ
kind: concept
slug: dominance-pruning
name: Dominance pruning
aliases:
- dominance rule
area: techniques/branch-and-bound
level: core
summary: Discarding a partial solution when another one is at least as good in every way that matters for completion.
prereqs: [fathoming-rule, partial-solution]
see_also: [fathoming-rule, bounding-function, knapsack-branch-and-bound, knapsack-dynamic-programming, held-karp-algorithm, branch-and-reduce, maximum-independent-set, memoization]
sources:
  - paper: doi:10.1145/322003.322010
    title: Toshihide Ibaraki, The power of dominance relations in branch-and-bound algorithms, Journal of the ACM 24(2), 1977
    locator: pp. 264 to 279
  - paper: doi:10.1145/321796.321808
    title: Walter H. Kohler and Kenneth Steiglitz, Characterization and theoretical comparison of branch-and-bound algorithms for permutation problems, Journal of the ACM 21(1), 1974
    locator: pp. 140 to 156
  - book: isbn:9780929306414
    title: Ellis Horowitz, Sartaj Sahni and Sanguthevar Rajasekaran, Computer Algorithms, second edition
    locator: Chapter 5, Dynamic Programming (0/1 knapsack, purging or dominance rule)
  - book: isbn:9783642165320
    title: Fedor V. Fomin and Dieter Kratsch, Exact Exponential Algorithms
    locator: Chapter 2, Branching (maximum independent set)
---

Dominance pruning discards a node of a search tree because some other node is known to lead to a solution at least as good. Unlike pruning by bound, it does not compare a node with the [incumbent](/incumbent-solution/) value; it compares two [partial solutions](/partial-solution/) with each other. A dominance rule can cut a tree that the bounds cannot cut, and on some problems it turns an exponential tree into a table of polynomial size, which is the link between branch and bound and dynamic programming.

## In plain words

Two hikers stand at the same point of a trail. One has more water and has walked less far than the other. Whatever the rest of the trail is, the first hiker can do everything the second one can. So there is no need to follow the second hiker any further.

In a search, two partial solutions are often in the same position: the same decisions are left, and the rest of the problem looks the same to both. If one of them has used fewer resources and gained more value, the other one can be dropped. Its subtree may hold good solutions, but each of them is matched by a solution in the subtree that is kept.

## The idea

Let a search maximize $f$, and let each node $N$ stand for a set $S(N)$ of complete solutions with best value $f^*(N)$. A **dominance relation** is a relation $M \succeq N$ between nodes such that $M \succeq N$ implies $f^*(M) \ge f^*(N)$. Then $N$ can be discarded as long as $M$, or a node that dominates $M$, stays in the search.

In most uses, the relation compares two nodes that have the same *remaining problem*. A partial solution has a state, such as the items still to decide, the cities still to visit or the vertices still in the graph, and a few resource values, such as used weight or cost. If $M$ and $N$ have the same state, and $M$ is at least as good in every resource and in the value gained so far, then every completion of $N$ is also a completion of $M$ with a value at least as large.

Rules of this kind:

- **0/1 knapsack.** After the first $k$ items are decided, a node is the pair (weight used, value gained). If $w_M \le w_N$ and $v_M \ge v_N$, then $M$ dominates $N$: any set of later items that fits after $N$ also fits after $M$.
- **Traveling salesman.** Two partial tours that start at city 1, visit the same set of cities and end at the same city have the same completions. The shorter one dominates. Keeping only one path per (set, end city) pair is the [Held-Karp algorithm](/held-karp-algorithm/).
- **Maximum independent set.** If $v$ and $w$ are adjacent and $N[v] \subseteq N[w]$, then some maximum independent set does not contain $w$: in a set that contains $w$, replace $w$ with $v$. So the branch that takes $w$ is dominated and $w$ can be deleted. [Branch and reduce](/branch-and-reduce/) algorithms use this as a reduction rule.
- **Scheduling.** If two partial sequences schedule the same set of jobs and one finishes no later and with no larger cost, the other one is dominated. Kohler and Steiglitz describe branch and bound for permutation problems in a model that includes such rules.

Some care is needed. When $M \succeq N$ and $N \succeq M$, the two nodes are equal and exactly one must be kept, so a fixed tie-break is part of the rule. When the relation compares a new node with nodes seen before, the search must store those nodes, and the memory can grow as fast as the set of states. Ibaraki studies dominance relations in a general model of branch and bound and compares how much different relations can reduce the search.

## Examples

**Knapsack levels.** Take capacity 16, values $40, 30, 50, 10$ and weights $2, 5, 10, 5$, in this order. The full tree of feasible partial solutions has 2, 4, 7 and 12 nodes at depths 1 to 4, and 26 nodes in total with the root. After each level, keep only the pairs (weight, value) that no other pair dominates:

| depth | feasible nodes | not dominated |
|---|---|---|
| 1 | 2 | 2 |
| 2 | 4 | 3 |
| 3 | 7 | 4 |
| 4 | 12 | 4 |

At depth 2, the pair $(5, 30)$, which takes only item 2, is dominated by $(2, 40)$, which takes only item 1. At depth 4 the four pairs left are $(0, 0)$, $(2, 40)$, $(7, 70)$ and $(12, 90)$, and the best value is 90. With the root, the search keeps 14 nodes instead of 26.

**A larger instance.** With capacity 14, values $14, 12, 18, 19, 19, 20$ and weights $1, 1, 2, 7, 8, 10$, the full tree has 87 feasible nodes and the dominance rule keeps 36. The number of pairs kept at any depth is at most $W + 1$, one for each weight, so the knapsack search with this rule takes $O(nW)$ time. This is the list form of [knapsack by dynamic programming](/knapsack-dynamic-programming/); Horowitz, Sahni and Rajasekaran call the step that deletes dominated pairs the purging or dominance rule.

**Independent set.** In a path $a - b - c$, $N[a] = \{a, b\} \subseteq N[b] = \{a, b, c\}$, so $b$ is deleted. Then $a$ and $c$ are isolated, and both are taken: the answer is $\{a, c\}$ with no branching.

## Where it is used

- Knapsack and other resource problems, where dominance between (resource, value) pairs gives the dynamic programming algorithms.
- Traveling salesman and sequencing problems, where partial sequences with the same set and the same last element are compared.
- [Branch and reduce](/branch-and-reduce/) algorithms for [maximum independent set](/maximum-independent-set/) and similar graph problems, where dominance gives reduction rules that remove vertices before branching.
- Branch and bound for scheduling, where dominance rules between jobs fix parts of the order in advance.
- Search with a table of visited states, as in [memoization](/memoization/), where a state that is reached again with a worse value is dropped.

## References
