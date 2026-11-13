---
tag: SFR4D3
kind: concept
slug: graph-search-vs-tree-search
name: Graph search versus tree search
aliases:
- closed list
- explored set
area: techniques/search-strategies
level: core
summary: Tree search may revisit states; graph search keeps an explored set so each state is expanded once.
prereqs: [search-tree, search-frontier, hash-table]
see_also: [search-strategy, duplicate-detection, uniform-cost-search, a-star-search, consistent-heuristic, depth-first-search, iterative-deepening-search, transposition-table]
sources:
  - book: isbn:9780134610993
    title: Stuart Russell and Peter Norvig, Artificial Intelligence, A Modern Approach, fourth edition
    locator: Chapter 3, Section 3.3.3 (redundant paths, graph search, tree-like search and the check for cycles) and Section 3.5.2 (A*, consistency and the reopening of states)
  - book: isbn:9780201055948
    title: Judea Pearl, Heuristics, Intelligent Search Strategies for Computer Problem Solving
    locator: Chapter 2 (the OPEN and CLOSED lists, and the handling of a state that is found again by a cheaper path)
  - paper: doi:10.1109/TSSC.1968.300136
    title: Peter E. Hart, Nils J. Nilsson and Bertram Raphael, A formal basis for the heuristic determination of minimum cost paths, IEEE Transactions on Systems Science and Cybernetics 4(2) (1968)
    locator: pp. 100 to 107 (A* with closed nodes that are reopened, and the consistency assumption under which no reopening is needed)
---

Tree search and graph search are two versions of the same search loop that differ in how they treat a state reached a second time. Tree-like search keeps no memory of the states it has seen, so it explores the [search tree](/search-tree/), in which a state appears once for each path to it. Graph search keeps a table of reached states (the explored set or closed list), so it explores each state at most once, or again only when it finds a cheaper path. Graph search trades memory for time: it can be exponentially faster, and it is the only one of the two that is sure to stop on a finite space with cycles.

## In plain words

You explore a town to find a shop. In the first way, you remember nothing. Each time you reach a corner, you try every street from it, even if you were at this corner before. You can walk the same streets again and again, and you can walk in a circle for ever.

In the second way, you carry a notebook. You write down each corner you reach. When you come to a corner that is already in the notebook, you do not explore it again. You never walk in a circle, and you see each corner at most once. The price is the notebook, which grows with the number of corners.

A third way is in between. You remember only the corners of the walk you are on now. This stops circles, but you can still reach the same corner by two different walks.

## The idea

### The two loops

Both versions keep a [frontier](/search-frontier/) of nodes, and both remove nodes in the order of the [search strategy](/search-strategy/). They differ in one line: the test before a child is added.

- **Tree-like search.** Add each child. A state is added once for each path that reaches it.
- **Graph search.** Keep a table *reached* that maps each state seen so far to the best path cost known for it. Add a child only if its state is not in *reached*, or if the new path cost is lower than the stored one. Then store the new cost.
- **Check for cycles on the current path.** Add a child only if its state is not already on the path from the root to the child. This removes cycles but not other redundant paths. It needs no table: depth-first search can test the path, which it already holds.

A path is *redundant* if another path reaches the same state at a cost no larger. A cycle is a special redundant path. Russell and Norvig give the three options above for the redundant paths of a problem: remember all reached states, check only for cycles, or do nothing when the problem has few redundant paths.

The table is a [hash table](/hash-table/) keyed by the state. It costs $O(1)$ expected time per test and one entry per reached state. Many older texts split it into two sets, the *open* list (the frontier) and the *closed* list (the expanded states). The single table *reached* of Russell and Norvig holds the states of both.

### What graph search guarantees

Let the state space have $V$ reachable states and $E$ transitions from them.

- **Termination.** With *reached* as the test, a state is added to the frontier only when its stored cost drops. If no state is ever added twice (the case for breadth-first and depth-first search), the loop runs at most $V$ iterations, so it stops on each finite space, with or without cycles. With costs, a state can be added again, but only on a strictly cheaper path. If each action cost is non-negative, the loop still stops on a finite space. Assume that a node added to the frontier has a path that visits a state $x$ twice. When the path first reached $x$, the stored cost of $x$ became at most the cost of that prefix, and stored costs only go down. The second visit to $x$ costs at least as much, because the cycle between the two visits has a cost of at least 0. So the test refused the second visit, a contradiction. Hence each node in the frontier is a path without a repeated state, and a finite space has finitely many of them.
- **Work.** Breadth-first and depth-first graph search expand each state at most once, so they take $O(V + E)$ time with $O(1)$ table operations. The same search as tree-like search can take time exponential in $V$.
- **Memory.** Graph search keeps one entry for each reached state. This is its cost. Depth-first search in tree-like form needs only $O(bm)$ memory for a tree of depth $m$. With a full table it needs memory for all the states it has reached, and it loses its main advantage. For this reason [iterative deepening search](/iterative-deepening-search/) and depth-first branch and bound are usually tree-like, with at most a check for cycles.

### Optimality and reopening

Graph search can lose the cost-optimality of the strategy when a state is reached first by a path that is not the cheapest, and the search refuses the cheaper path later. Two common rules avoid this.

- **Update on a cheaper path.** Re-add a state whenever a strictly cheaper path to it appears, even if it was already expanded. This is *reopening*. It keeps the optimality of A* with an [admissible heuristic](/admissible-heuristic/). It can expand a state more than once.
- **Expand in an order that makes the first expansion cheapest.** [Uniform-cost search](/uniform-cost-search/) with non-negative costs and A* with a [consistent heuristic](/consistent-heuristic/) expand each state for the first time along a cheapest path. Then a closed state never needs to be reopened, and the simple closed-list test is safe.

The same order matters for the goal test. A goal test when a node is generated is safe for breadth-first search with equal costs. For uniform-cost search it can return a costly path, because a cheaper path to the goal can still be in the frontier.

## Examples

### Three rules on a grid

A robot starts at $(0, 0)$ on the integer grid and has the moves right, left, up and down, in this order. The goal is $(3, 3)$, at depth 6. Breadth-first search with the goal test at generation gives these counts:

| rule for a repeated state | nodes generated | nodes expanded |
| --- | --- | --- |
| none (tree-like) | 1,408 | 352 |
| check for cycles on the current path | 454 | 159 |
| graph search with *reached* | 67 | 45 |

All three return a path of 6 moves. The check for cycles removes the paths that step back onto themselves, but two paths such as right then up and up then right still reach the same cell, so it keeps many redundant paths. Graph search generates each cell once. The page on the [search tree](/search-tree/) shows how the tree-like count grows like $4^d$, while the number of cells grows like $2d^2$.

### A closed list that loses the optimum

The graph has the edges S→A 1, S→B 2, A→C 3, B→C 1, C→G 3. The cheapest path is S-B-C-G with cost 6, and S-A-C-G costs 7. Run A* with the heuristic $h(S) = 0$, $h(A) = 0$, $h(B) = 3$, $h(C) = 0$, $h(G) = 0$. The true costs to the goal are 6, 6, 4, 3 and 0, so $h$ is admissible. It is not consistent, because $h(B) = 3 > c(B, C) + h(C) = 1$.

| step | frontier, as state with $g$ and $f = g + h$ | expanded |
| --- | --- | --- |
| 1 | S: $g = 0$, $f = 0$ | S |
| 2 | A: 1, 1; B: 2, 5 | A |
| 3 | C: 4, 4; B: 2, 5 | C, now closed with $g = 4$ |
| 4 | B: 2, 5; G: 7, 7 | B, which generates C with $g = 3$ |
| 5 | G: 7, 7 | G, a goal with cost 7 |

At step 4, expanding B finds C again with $g = 3 < 4$. A closed list that never reopens skips this child, and the search returns S-A-C-G with cost 7. With reopening, C goes back to the frontier with $f = 3$, it is expanded again, G gets $g = 6$, and the search returns the optimal S-B-C-G with cost 6. With a consistent heuristic, for example $h = 0$, the search expands B before C, and the problem does not appear.

### Tree-like search that never stops

Two states $u$ and $v$ with the moves $u \to v$ and $v \to u$, and a goal that cannot be reached, make tree-like depth-first search run for ever on the path $u, v, u, v, \ldots$. The check for cycles stops it after the path $u, v$. Graph search also stops after two expansions. Tree-like breadth-first search does not stop either: its frontier never becomes empty.

## Where it is used

On an explicit graph, the standard [breadth-first search](/breadth-first-search/), [depth-first search](/depth-first-search/) and [Dijkstra's algorithm](/dijkstra/) are graph searches: the visited mark on each vertex is the *reached* table. Search in AI planning and puzzle solving uses graph search when the states fit in memory, often with a hashed table of states, and tree-like search with a check for cycles when they do not, as in [iterative deepening](/iterative-deepening-search/) and [IDA*](/iterative-deepening-a-star/). Game programs keep a bounded [transposition table](/transposition-table/), a cache between the two extremes. Disk-based and memory-bounded searches use delayed [duplicate detection](/duplicate-detection/): they find repeated states in batches instead of with one table.

## References
