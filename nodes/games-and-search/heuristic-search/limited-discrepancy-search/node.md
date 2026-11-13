---
tag: Y4C1CW
kind: algorithm
slug: limited-discrepancy-search
name: Limited discrepancy search
aliases:
- LDS
area: games-and-search/heuristic-search
level: advanced
summary: A tree search that first follows the heuristic choice everywhere, then allows one choice against it, then two, and so on. It finds goals that the heuristic misses at only a few points.
solves: [state-space-search]
model: word-ram
complexity:
  vars: {d: the depth of the tree, k: the number of discrepancies allowed in an iteration}
  time: {lds: O(d 2^d), ilds: O(2^d), iteration: O(d^(k+1))}
  space: {extra: O(d)}
properties: {deterministic: true, recursive: true}
history:
  year: 1995
  people: [William D. Harvey, Matthew L. Ginsberg]
  note: Harvey and Ginsberg introduced LDS at IJCAI-95 for search trees where a good heuristic is wrong at only a few choices.
prereqs: [depth-first-search, heuristic-function, chronological-backtracking]
see_also: [iterative-deepening-search, beam-search, beam-stack-search, greedy-best-first-search, constraint-satisfaction-problem, variable-ordering-heuristics, depth-first-branch-and-bound, iterative-broadening]
sources:
  - paper: William D. Harvey and Matthew L. Ginsberg, Limited discrepancy search, Proceedings of the 14th International Joint Conference on Artificial Intelligence (IJCAI-95)
    locator: pp. 607 to 613 (the definition of a discrepancy, the procedure with right children first, and the analysis for binary trees)
  - paper: Richard E. Korf, Improved limited discrepancy search, Proceedings of the 13th National Conference on Artificial Intelligence (AAAI-96)
    locator: pp. 286 to 291 (ILDS, which visits in iteration k only the leaves with exactly k discrepancies, and its node count)
---

Limited discrepancy search (LDS) is a way to search a tree when a heuristic orders the children of each node and is right most of the time. A *discrepancy* is a choice of a child other than the one the heuristic prefers. LDS runs iterations $k = 0, 1, 2, \ldots$. Iteration $k$ is a [depth-first search](/depth-first-search/) that only follows paths with at most $k$ discrepancies. So iteration 0 is the one path that the heuristic picks, iteration 1 adds each path that goes against the heuristic once, and so on. If the heuristic is wrong at only a few choices on the way to a goal, LDS finds the goal in an early iteration, while plain [chronological backtracking](/chronological-backtracking/) can be stuck under a wrong choice near the root for a very long time. Harvey and Ginsberg introduced it in 1995, and Korf improved it in 1996 so that each iteration visits only the new leaves.

## In plain words

You follow a map that is good but not perfect. At each fork it tells you which way to go. First you do exactly what it says. If that fails, you try each route where you ignore the map at one fork only. Then the routes where you ignore it at two forks, and so on.

The idea is that a good map is wrong only a few times. Plain backtracking always undoes the last choice first, so if the map was wrong at the very first fork, it tries every route after that fork before it fixes the real mistake. Counting the times you ignore the map fixes a mistake at any fork early.

## The problem

The input is a finite tree given by a root and a function CHILDREN that lists the children of a node in the order the heuristic prefers, with the first child the preferred one, a goal test IS-GOAL, and a largest number of discrepancies $k_{\max}$. The output is a path from the root to a goal node, or *failure*. In a node with more than two children, this page counts each choice of a child other than the first as one discrepancy. For a [state-space search](/state-space-search/) problem, the tree is the tree of paths from the start, with the successors of a state ordered by a [heuristic](/heuristic-function/) $h$ and a limit on the depth.

## The algorithm

```pseudo id=main
LDS(root, CHILDREN, IS-GOAL, kmax)
L1  for k ← 0 to kmax do
L2      r ← PROBE(root, k)
L3      if r ≠ failure then return r            ▷ when the loop ends, return failure
L4  PROBE(n, k)
L5      if IS-GOAL(n) then return the path to n
L6      if n has no children then return failure
L7      if k = 0 then return PROBE(the first child of n, 0)
L8      for each child c of n other than the first do r ← PROBE(c, k − 1); if r ≠ failure then return r
L9      return PROBE(the first child of n, k)
```

This is the procedure of Harvey and Ginsberg. With $k > 0$ discrepancies left, PROBE first spends one of them on the other children, line L8, and only then follows the heuristic with all $k$ kept, line L9. So within an iteration, paths with their discrepancies near the root come first. The paper argues that this is where a heuristic tends to be wrong, since it has the least information there.

Iteration $k$ visits each leaf with at most $k$ discrepancies, not only the leaves with exactly $k$. So each iteration repeats the work of the ones before. **Korf's improved LDS (ILDS)** fixes this when all leaves are at a known depth $d$. Its PROBE carries the number of levels left, follows the first child only if there are more levels left than discrepancies still to spend, and spends a discrepancy on the other children only if $k > 0$. Then iteration $k$ visits exactly the leaves with $k$ discrepancies, each once. Korf also tries the preferred child first, so in ILDS the discrepancies fall near the leaves first. The implementation has both procedures, and a function that runs LDS on a state-space problem with the successors sorted by $h$, the states of the current path left out, and a depth limit.

## Example

**Order of the leaves.** Take a binary tree of depth 3 and name each leaf by its three choices from the root, with 0 for the preferred child and 1 for the other. The number of 1s is the number of discrepancies.

| iteration | LDS visits | ILDS visits |
| --- | --- | --- |
| 0 | 000 | 000 |
| 1 | 100, 010, 001, 000 | 001, 010, 100 |
| 2 | 110, 101, 100, 011, 010, 001, 000 | 011, 101, 110 |
| 3 | all 8 leaves | 111 |

In iteration 1, LDS first spends its one discrepancy at the root, line L8, and reaches 100. Then it follows the preferred child at the root with its discrepancy kept, line L9, and spends it one level down, at 010, then at 001, and finally reaches 000 with no discrepancy spent. ILDS visits only the three new leaves, and starts with the discrepancy at the bottom.

**A wrong first choice.** Suppose that the goal is the leaf 1000…0 of a binary tree of depth $d$: the heuristic is wrong at the root and right below it. Depth-first search in the heuristic order visits all $2^{d-1}$ leaves under the preferred child of the root before it reaches the goal. LDS visits the leaf 00…0 in iteration 0 and the goal as its first leaf in iteration 1, so it visits 2 leaves. For $d = 20$, that is 2 leaves against 524,289.

**Node counts.** When no goal exists, all iterations together visit the following numbers of nodes in a complete binary tree of depth $d$, counted by the tests of the implementation:

| depth $d$ | LDS, iterations 0 to $d$ | ILDS, iterations 0 to $d$ | one depth-first search |
| --- | --- | --- | --- |
| 3 | 43 | 26 | 15 |
| 6 | 568 | 247 | 127 |
| 10 | 13,300 | 4,083 | 2,047 |

ILDS visits $2^{d+2} - d - 3$ nodes, less than twice a full depth-first search. LDS visits a leaf with $i$ discrepancies $d - i + 1$ times, so its total grows like $d\,2^d$.

## Correctness

The [proof](proofs/correctness.md) shows, for a finite tree:

- **What an iteration visits.** PROBE$(n, k)$ visits exactly the nodes below $n$ whose path from $n$ has at most $k$ discrepancies, each once, unless it stops at a goal. So iteration $k$ of LDS visits each leaf with at most $k$ discrepancies once.
- **ILDS.** In a tree with all leaves at depth $d$, iteration $k$ of ILDS visits exactly the leaves with $k$ discrepancies, each once.
- **The answer.** A returned path leads from the root to a goal. LDS returns in iteration $k^*$, the least number of discrepancies on a path to a goal, and returns failure only if no goal has at most $k_{\max}$ discrepancies. With $k_{\max}$ at least the depth, it is complete.
- **The counts.** Summed over all iterations, ILDS visits $2^{d+2} - d - 3$ nodes of a complete binary tree of depth $d$, and LDS visits $O(d\,2^d)$.

## Complexity

Costs are in the [word RAM](/word-ram/), with each call of CHILDREN and IS-GOAL counted as $O(1)$, for a binary tree of depth $d$.

**One iteration.** Iteration $k$ of ILDS visits the $\binom{d}{k}$ leaves with $k$ discrepancies and the nodes on their paths, so $O(d \binom{d}{k}) = O(d^{k+1})$ nodes. Iteration $k$ of LDS visits the $\sum_{i \le k} \binom{d}{i}$ leaves with at most $k$ discrepancies, which is also $O(d^{k+1})$ for a fixed $k$. This is the point of LDS: when the heuristic is wrong at only $k$ choices, the cost is polynomial in the depth, not exponential.

**All iterations.** A node at depth $j$ with $i$ discrepancies is visited by LDS in each iteration from $i$ to $d$, and by ILDS in each iteration from $i$ to $i + d - j$. The sums give $O(d\,2^d)$ for LDS and $2^{d+2} - d - 3 = O(2^d)$ for ILDS, against $2^{d+1} - 1$ for one depth-first search.

**Space.** PROBE recurses once per level, so the stack has $O(d)$ frames, plus the current path. Like depth-first search, LDS stores no closed list. On a graph with cycles, the tree of paths must be cut by a depth limit or by leaving out the states on the current path, as the implementation does.

## Properties

- **Complete** on a finite tree once $k_{\max}$ reaches the depth, but **not optimal**: it returns the goal with the fewest discrepancies, not the cheapest one.
- **Linear space**, like depth-first search.
- **Redundant**: plain LDS revisits the leaves of earlier iterations, ILDS does not.
- **Order-sensitive**: it is only as good as the order of the children.
- **Deterministic and recursive.**

## Variants and improvements

- **Improved LDS (Korf 1996).** Each iteration visits only the leaves with exactly $k$ discrepancies, as above. It needs the depth of the tree.
- **Depth-bounded discrepancy search.** Walsh (1997) lets iteration $k$ take any choice in the top $k$ levels of the tree and only preferred children below them, which pushes the search further toward early mistakes.
- **Discrepancies in branch and bound.** For optimization, LDS gives the order in which a [depth-first branch and bound](/depth-first-branch-and-bound/) explores the tree, so that good solutions, and so good bounds, come early.
- **Constraint solvers.** In [constraint satisfaction](/constraint-satisfaction-problem/), the heuristic is the value order of a [variable ordering](/variable-ordering-heuristics/) scheme, and LDS is one of the standard search strategies next to plain backtracking.

## When to use it

Use LDS when the search tree is too large to explore, a value-ordering heuristic is right at most choices, and a goal, not the cheapest goal, is what you need: scheduling, timetabling and constraint problems are the classic cases. It also gives a cheap way to use a time limit, since each iteration explores a larger and larger part of the tree around the heuristic path. If the heuristic is poor, LDS does more work than plain depth-first search, because of the iterations. If you need an optimal path in a graph, use [A*](/a-star-search/) or [IDA*](/iterative-deepening-a-star/).

## Pitfalls

- **Counting the leaves of earlier iterations twice.** Plain LDS visits the leaves with fewer than $k$ discrepancies again in iteration $k$. Use ILDS when the depth is known.
- **Many children.** With $b$ children, counting each nonpreferred child as one discrepancy makes iteration 1 visit $(b - 1) d$ leaves, not $d$. Some programs count the $j$-th child as $j - 1$ discrepancies instead, which changes the order.
- **Graphs.** On a graph, the same state can be reached by many paths, and the tree of paths can be infinite. Bound the depth and leave out the states on the current path.
- **Deep trees in a language with a small stack.** PROBE recurses once per level. The implementation in Python must stay well below the limit of about 1,000 frames.

## Implementations

## History

Harvey and Ginsberg presented LDS at IJCAI-95. They observed that a good heuristic leads to a goal with only a few wrong choices, and that chronological backtracking spends most of its time below an early wrong choice. They tried discrepancies near the root first, where a heuristic has the least information. Korf noticed in 1996 that each iteration of LDS repeats the leaves of the earlier ones, and gave ILDS, which visits each leaf once in all. Walsh followed in 1997 with depth-bounded discrepancy search, and discrepancy-based orders became a standard tool of constraint programming systems.

## References
