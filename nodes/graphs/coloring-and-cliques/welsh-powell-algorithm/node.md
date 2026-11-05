---
tag: NAP2ZB
kind: algorithm
slug: welsh-powell-algorithm
name: Welsh-Powell algorithm
aliases:
- largest-first coloring
area: graphs/coloring-and-cliques
level: intro
summary: Greedy coloring that processes vertices in order of decreasing degree.
solves: [graph-coloring]
model: word-ram
complexity:
  vars: {n: the number of vertices, m: the number of edges, k: the number of colors used}
  time: {worst: O(n log n + n k + m)}
  space: {extra: Θ(n)}
properties: {deterministic: true, recursive: false, online: false}
prereqs: [greedy-coloring, degree, graph-coloring]
see_also: [dsatur, recursive-largest-first, delta-plus-one-bound, degeneracy-ordering, chromatic-number, brooks-theorem]
sources:
  - paper: doi:10.1093/comjnl/10.1.85
    title: D. J. A. Welsh and M. B. Powell, An upper bound for the chromatic number of a graph and its application to timetabling problems, The Computer Journal 10(1), 85 to 86 (1967)
    locator: the whole paper (the order by non-increasing degree and the bound max over i of min(d_i + 1, i))
  - book: isbn:9780130144003
    title: Douglas B. West, Introduction to Graph Theory, second edition, Prentice Hall, 2001
    locator: Section 5.1, Vertex colorings and upper bounds (the greedy coloring algorithm and the Welsh-Powell bound)
  - book: isbn:9783662536216
    title: Reinhard Diestel, Graph Theory, fifth edition, Springer, 2017
    locator: Section 5.2, Colouring vertices (greedy colouring and the colouring number)
---

The Welsh-Powell algorithm colors a graph by sorting its vertices by non-increasing [degree](/degree/) and then building the color classes one at a time: each class takes, in the sorted order, every uncolored vertex that has no neighbor in the class yet. The result is the same coloring as [greedy coloring](/greedy-coloring/) in the sorted order. Welsh and Powell proved that it uses at most $\max_i \min(d_i + 1, i)$ colors, where $d_1 \ge d_2 \ge \cdots \ge d_n$ are the degrees. It is a fast heuristic for [graph coloring](/graph-coloring/), with no guarantee to reach the [chromatic number](/chromatic-number/).

## In plain words

Vertices with many neighbors are the hard ones to color, so color them first, while many colors are still free for them. Sort the vertices from the most neighbors to the fewest.

Take the first color. Walk down the sorted list and give this color to each vertex that has no neighbor with this color yet. Then take a second color and walk down the list again, skipping the vertices that already have a color. Go on until every vertex has a color.

## The problem

The input is a simple undirected graph $G = (V, E)$ with $V = \{0, \ldots, n-1\}$, given as [adjacency lists](/adjacency-list/). The output is a proper coloring $c : V \to \{1, \ldots, k\}$, that is $c(u) \ne c(v)$ for each edge $\{u, v\}$. The algorithm does not promise the least $k$; that problem is NP-hard (see [graph coloring](/graph-coloring/)).

## The algorithm

```pseudo id=main
WELSH-POWELL(G)
L1  σ ← the vertices sorted by non-increasing degree, ties by smaller index
L2  for each vertex v do c[v] ← 0, blocked[v] ← 0     ▷ 0 means "not colored"
L3  k ← 0
L4  for i ← 1 to n do
L5      if c[σi] = 0 then                              ▷ σi starts a new class
L6          k ← k + 1
L7          for j ← i to n do
L8              v ← σj
L9              if c[v] = 0 and blocked[v] ≠ k then
L10                 c[v] ← k
L11                 for each neighbor w of v do blocked[w] ← k
L12 return c
```

Line L5 finds the first vertex of the sorted list that has no color. Lines L7 to L11 make the class of color $k$: they scan the rest of the list and add each uncolored vertex that no member of the class has blocked. Line L11 marks all neighbors of a new member with the stamp $k$. A stamp from an older class is a smaller number, so the array never needs to be cleared. The pass can start at $i$ because all vertices before $\sigma_i$ already have a color.

## Example

Take the graph with 7 vertices and the edges $02, 04, 05, 06, 13, 23, 24, 34, 46$. The degrees are $d(0) = 4$, $d(1) = 1$, $d(2) = 3$, $d(3) = 3$, $d(4) = 4$, $d(5) = 1$ and $d(6) = 2$. So line L1 gives $\sigma = (0, 4, 2, 3, 6, 1, 5)$.

| pass | vertex scanned | action |
|---|---|---|
| $k = 1$ | 0 | color 1; block 2, 4, 5, 6 |
| | 4, 2 | blocked |
| | 3 | color 1; block 1, 2, 4 |
| | 6, 1, 5 | blocked |
| $k = 2$ | 4 | color 2; block 0, 2, 3, 6 |
| | 2, 3 | blocked or colored |
| | 6 | blocked |
| | 1 | color 2; block 3 |
| | 5 | color 2; block 0 |
| $k = 3$ | 2 | color 3; block 0, 3, 4 |
| | 3 | colored |
| | 6 | color 3; block 0, 4 |
| | 1, 5 | colored |

The classes are $\{0, 3\}$, $\{4, 1, 5\}$ and $\{2, 6\}$, so $c = (1, 2, 3, 1, 2, 2, 3)$ for the vertices $0, \ldots, 6$. The triangle $\{0, 2, 4\}$ needs 3 colors, so this is optimal. The sorted degrees are $4, 4, 3, 3, 2, 1, 1$, and the Welsh-Powell bound is $\max(1, 2, 3, 4, 3, 2, 1) = 4$. Greedy coloring in the plain order $0, 1, \ldots, 6$ uses 4 colors on this graph: vertex 4 comes after 0, 2 and 3, which have the colors 1, 2 and 3.

## Correctness

The output is a proper coloring, and it equals the greedy coloring in the order $\sigma$: each vertex gets the smallest color that none of its earlier neighbors in $\sigma$ has. The key invariant is that after pass $k$, the vertices with color $k$ are exactly those whose greedy color is $k$. The full proof, by induction on $k$ and on the position in the pass, is below.

**The bound.** Let $\sigma_i$ be the vertex at position $i$, with degree $d_i$. In the greedy view, $\sigma_i$ has at most $\min(d_i, i - 1)$ earlier neighbors, so its color is at most $\min(d_i, i - 1) + 1 = \min(d_i + 1, i)$. Hence the number of colors is at most $\max_{1 \le i \le n} \min(d_i + 1, i)$. This is at most $\Delta + 1$, the [greedy bound](/delta-plus-one-bound/), and it can be much smaller when few vertices have a high degree.

## Complexity

- **Sorting.** Line L1 takes $O(n \log n)$ with a comparison sort, or $O(n + m)$ with a bucket sort, because each degree is in $0, \ldots, n-1$.
- **Passes.** There are $k$ passes, and each pass scans at most $n$ positions, so lines L7 to L10 run $O(nk)$ times.
- **Stamps.** Line L11 runs once for each vertex, when it gets its color, so it does $\sum_v d(v) = 2m$ steps in total.

The total is $O(n \log n + nk + m)$ time and $\Theta(n)$ extra space. Since $k \le \Delta + 1$, this is $O(n \log n + n\Delta)$, and it is $\Theta(n^2)$ on the complete graph $K_n$. The equivalent greedy pass in the order $\sigma$ (with the stamp array of [greedy coloring](/greedy-coloring/)) runs in $O(n + m)$ after the sort.

## Properties

- **Deterministic.** With the tie rule of line L1, the output depends only on the graph and its labels.
- **Not optimal.** Some graphs need far more colors than $\chi$ (see the pitfalls).
- **Exact on some classes.** On a [complete graph](/complete-graph/) it uses $n$ colors, which is optimal. On a graph with no edges it uses one.
- **Offline.** It needs all degrees before it starts.

## Variants and improvements

- **Greedy in degree order.** Run [greedy coloring](/greedy-coloring/) in the order $\sigma$. It gives the same colors and is faster when $k$ is large.
- **Smallest-last order.** Use the [degeneracy ordering](/degeneracy-ordering/) instead of the degree order. Then the number of colors is at most $d + 1$, where $d$ is the [degeneracy](/degeneracy/), which is never more than the Welsh-Powell bound.
- **DSatur.** [DSatur](/dsatur/) chooses the next vertex by the number of distinct colors among its neighbors, which changes as the coloring grows. It is exact on bipartite graphs.
- **Recursive largest first.** [RLF](/recursive-largest-first/) also builds one class at a time, but it chooses the next member of the class by its degree into the uncolored part. It usually uses fewer colors and costs more time.

## When to use it

Use it when you need a valid coloring fast, for example as a first upper bound for an exact search such as [Lawler's algorithm](/lawler-chromatic-number/) or a [branch-and-bound clique search](/tomita-maximum-clique/). If the number of colors matters more than speed, DSatur or RLF usually do better, and an exact method is needed for an optimum.

## Pitfalls

- **Checking only the first vertex of the class.** A pass must test each new vertex against all members of the class, which line L9 does with the stamp. Testing only against $\sigma_i$, the vertex that started the class, can put two adjacent vertices in the same class.
- **Ascending order.** Sorting by non-decreasing degree is a different heuristic. The bound $\min(d_i + 1, i)$ needs the degrees in non-increasing order.
- **Ties.** Many graphs have many vertices of equal degree, and the tie rule decides the result. The crown graph, $K_{t,t}$ minus a perfect matching, is $(t-1)$-regular and bipartite. If the labels put the two ends of each removed edge next to each other in $\sigma$, the algorithm uses $t$ colors where 2 suffice.
- **Clearing the stamps.** Resetting the array `blocked` before each pass costs $\Theta(n)$ per pass. It is correct but needless, because the stamp $k$ is new in pass $k$.

## Implementations

## History

D. J. A. Welsh and M. B. Powell published the method and the bound $\max_i \min(d_i + 1, i)$ in The Computer Journal in 1967, with an application to exam timetables. The order by non-increasing degree is also called the largest-first order.

## References
