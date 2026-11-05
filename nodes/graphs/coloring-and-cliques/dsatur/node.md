---
tag: 4C0R37
kind: algorithm
slug: dsatur
name: DSATUR
aliases:
- Brelaz's algorithm
- saturation degree ordering
area: graphs/coloring-and-cliques
level: core
summary: Greedy coloring that always picks the uncolored vertex with the most distinct colors among its neighbors.
solves: [graph-coloring]
model: word-ram
complexity:
  vars: {n: the number of vertices, m: the number of edges}
  time: {worst: Θ(n^2), best: Θ(n^2)}
  space: {extra: Θ(n + m)}
properties: {deterministic: true, recursive: false}
prereqs: [greedy-coloring, graph-coloring, bipartite-graph]
see_also: [greedy-coloring, degeneracy-ordering, welsh-powell-algorithm, recursive-largest-first, bipartite-graph-test, chromatic-number, delta-plus-one-bound, lawler-chromatic-number]
sources:
  - paper: doi:10.1145/359094.359101
    title: Daniel Brélaz, New methods to color the vertices of a graph, Communications of the ACM 22(4), 251 to 256 (1979)
    locator: the whole paper (the saturation degree rule, the tie-break by degree in the uncolored subgraph, exactness on bipartite graphs, and its use inside an exact backtracking method)
  - paper: doi:10.1016/S0012-365X(00)00439-8
    title: R. Janczewski, M. Kubale, K. Manuszewski and K. Piwakowski, The smallest hard-to-color graph for algorithm DSATUR, Discrete Mathematics 236(1 to 3), 151 to 165 (2001)
    locator: the whole paper (graphs on which some or every run of DSATUR uses more than χ colors)
---

DSATUR is a [greedy coloring](/greedy-coloring/) heuristic that chooses the next vertex while it colors, instead of fixing an order in advance. At each step it takes an uncolored vertex whose neighbors already show the most distinct colors, its *saturation degree*, and gives it the smallest color that is free. Ties go to the vertex with the most uncolored neighbors. Brélaz introduced it in 1979; it colors every [bipartite graph](/bipartite-graph/) with at most 2 colors, cycles and wheels optimally, and is a standard first heuristic for [graph coloring](/graph-coloring/), which is NP-hard in general.

## In plain words

Color the points of a network one at a time. Before each step, look at every point that has no color yet and count how many different colors its neighbors already use. Pick the point with the highest count: it has the fewest choices left, so it is the most urgent. If several points tie, pick the one with the most neighbors that still have no color. Give it the first color that none of its neighbors has.

Hard points are handled while they still have a free color, and easy points wait. This choice of order usually gives far fewer colors than coloring in a fixed order.

## The problem

The input is a simple undirected graph $G = (V, E)$ with $V = \{0, \ldots, n-1\}$, as adjacency lists. The output is a proper coloring $c : V \to \{1, 2, \ldots\}$, that is, $c(u) \ne c(v)$ for each edge $\{u, v\}$, with few colors. Finding the fewest colors, the [chromatic number](/chromatic-number/) $\chi(G)$, is NP-hard, so DSATUR is a heuristic: it always gives a proper coloring but not always with $\chi(G)$ colors.

For an uncolored vertex $v$, the saturation degree is $\mathrm{sat}(v) = |\{ c(w) : w \in N(v),\ w \text{ colored} \}|$, and the uncolored degree $\mathrm{dunc}(v)$ is the number of uncolored neighbors.

## The algorithm

```pseudo id=main
DSATUR(G)
L1  for each vertex v do c[v] ← 0, S[v] ← ∅, dunc[v] ← deg(v)
L2  repeat n times
L3      v ← an uncolored vertex with the largest |S[v]|, ties by the largest dunc[v], then the smallest index
L4      k ← the smallest integer k ≥ 1 with k ∉ S[v]
L5      c[v] ← k
L6      for each uncolored neighbor w of v do
L7          S[w] ← S[w] ∪ {k}
L8          dunc[w] ← dunc[w] − 1
L9  return c
```

$S[v]$ is the set of colors next to $v$, so $\mathrm{sat}(v) = |S[v]|$. At the first step all saturations are 0, and line L3 takes a vertex of largest degree. Lines L4 and L5 are the step of greedy coloring. Lines L6 to L8 update the uncolored neighbors of $v$; colored vertices need no update.

## Example

The graph has the vertices $0, \ldots, 6$ and the edges $01, 02, 12, 13, 23, 24, 34, 35, 45, 06, 56$. Each row lists the uncolored vertices as $v{:}(\mathrm{sat}, \mathrm{dunc})$ before line L3.

| step | uncolored vertices, (sat, dunc) | chosen $v$ | $S[v]$ | color |
|---|---|---|---|---|
| 1 | 0:(0,3) 1:(0,3) 2:(0,4) 3:(0,4) 4:(0,3) 5:(0,3) 6:(0,2) | 2 | $\emptyset$ | 1 |
| 2 | 0:(1,2) 1:(1,2) 3:(1,3) 4:(1,2) 5:(0,3) 6:(0,2) | 3 | {1} | 2 |
| 3 | 0:(1,2) 1:(2,1) 4:(2,1) 5:(1,2) 6:(0,2) | 1 | {1, 2} | 3 |
| 4 | 0:(2,1) 4:(2,1) 5:(1,2) 6:(0,2) | 0 | {1, 3} | 2 |
| 5 | 4:(2,1) 5:(1,2) 6:(1,1) | 4 | {1, 2} | 3 |
| 6 | 5:(2,1) 6:(1,1) | 5 | {2, 3} | 1 |
| 7 | 6:(2,0) | 6 | {1, 2} | 3 |

The result is $c = (2, 3, 1, 2, 3, 1, 3)$ for the vertices $0, \ldots, 6$, with 3 colors. The graph contains the triangle $\{0, 1, 2\}$, so 3 is optimal. In step 2, vertex 3 wins the tie at saturation 1 by its 3 uncolored neighbors. In step 3, vertices 1 and 4 tie on both keys and the smaller index wins.

**A graph where DSATUR is not optimal.** Take the 7 vertices $0, \ldots, 6$ and the edges $01, 02, 04, 12, 13, 16, 25, 35, 36, 45, 46$. Its chromatic number is 3, for example with the color classes $\{0, 5, 6\}$, $\{1, 4\}$, $\{2, 3\}$. DSATUR with the tie-break of line L3 returns $(2, 1, 3, 2, 3, 1, 4)$, with 4 colors: vertex 6 ends with neighbors 1, 3 and 4 in three different colors. With this tie-break, DSATUR is optimal on every graph with at most 6 vertices.

## Correctness

**Theorem.** DSATUR returns a proper coloring in which each vertex $v$ has a color $c(v) \le \mathrm{sat}(v) + 1 \le \deg(v) + 1$, where $\mathrm{sat}(v)$ is taken at the moment $v$ is colored. If $G$ is bipartite, it uses at most 2 colors.

Properness is the argument of greedy coloring: by the invariant that $S[v]$ is the set of colors of the colored neighbors of $v$, line L4 picks a color that no colored neighbor has, and later neighbors avoid it in turn. Exactness on bipartite graphs comes from the selection rule. Once a vertex of a connected component is colored, its uncolored neighbors have saturation at least 1, and every uncolored vertex of other components has saturation 0, so DSATUR finishes the component before it starts another, and each new vertex is adjacent to an already colored one. The colored part of the component is then connected, and its 2-coloring is the bipartition, so all colored neighbors of the new vertex are on the other side and share one color. The new vertex has saturation 1 and gets the other of the colors 1 and 2. The full proof is below.

## Complexity

The cost is in the [word RAM](/word-ram/) model, with adjacency lists.

- Line L1 takes $\Theta(n)$ time.
- Line L3 scans all $n$ vertices in each of the $n$ rounds: $\Theta(n^2)$ in total.
- Line L4 tests $k = 1, 2, \ldots$ and stops at $|S[v]| + 1$ at the latest, so it costs $O(\deg(v) + 1)$, with $S[v]$ stored as a bit array or hash set. Summed over $v$ this is $O(n + m)$.
- Lines L6 to L8 scan the list of $v$ once: $O(m)$ in total.

So the time is $\Theta(n^2)$, and the extra space is $\Theta(n + m)$ for the sets $S[v]$, which have at most $\deg(v)$ elements. A priority queue keyed by $(\mathrm{sat}, \mathrm{dunc})$ with decrease and increase operations gives $O((n + m) \log n)$, which is better for sparse graphs.

## Properties

- **A greedy coloring.** DSATUR is greedy coloring in a dynamic order, so all bounds of greedy coloring hold: at most $\Delta + 1$ colors, and each vertex of color $k$ has neighbors of all colors $1, \ldots, k - 1$.
- **Exact on bipartite graphs.** Unlike greedy coloring in a fixed order, which can use $n/2$ colors on a crown graph, DSATUR 2-colors every bipartite graph. It is also exact on cycles and on wheels.
- **Not exact in general.** On the 7-vertex example above it uses 4 colors where 3 suffice. Janczewski, Kubale, Manuszewski and Piwakowski studied the smallest graphs on which some run, or every run, of DSATUR is not optimal. Since graph coloring cannot be approximated within $n^{1-\varepsilon}$ unless P = NP, no polynomial heuristic, DSATUR included, has a good worst-case ratio.
- **Tie-breaking matters.** The number of colors depends on the tie-break. Brélaz's rule is the largest degree in the uncolored subgraph; implementations that break ties by index alone, or by the degree in $G$, give different results.
- **Starts with a clique.** In the first steps, while the colored vertices form a clique, a vertex adjacent to all of them has saturation equal to the number of colors used so far, the largest possible. So DSATUR tends to color a large clique first, which also gives a lower bound $\omega$.

## Variants and improvements

- **Exact DSATUR.** Brélaz used the same rule inside a backtracking search: branch on the colors $1, \ldots, \max + 1$ for the vertex chosen by the rule, and prune with the best coloring found. This branch and bound is still a strong exact method for small and medium graphs; [Lawler's algorithm](/lawler-chromatic-number/) and inclusion-exclusion methods give the best worst-case bounds.
- **Recursive largest first.** [RLF](/recursive-largest-first/) builds one color class at a time instead of one vertex at a time and often uses fewer colors, at a higher cost.
- **Fixed orders.** [Welsh-Powell](/welsh-powell-algorithm/) (largest degree first) and the [smallest-last order](/degeneracy-ordering/) choose the order before coloring and run in $O(n + m)$ or $O(n \log n + m)$ time.
- **Starting point for local search.** Tabu search and other local search methods for coloring often start from a DSATUR coloring and try to remove colors.

## When to use it

Use DSATUR as the default constructive heuristic when the number of colors matters: it is simple, deterministic, and usually better than greedy coloring in a fixed order. Use the heap version on large sparse graphs. Use the backtracking version when an exact answer is needed on small graphs. When only speed matters, or a guarantee in terms of the [degeneracy](/degeneracy/) is enough, use the smallest-last order.

## Pitfalls

- **Counting colored neighbors instead of colors.** The saturation is the number of distinct colors, not the number of colored neighbors. Two neighbors with color 1 count once. Line L7 adds to a set.
- **Updating colored vertices.** Only uncolored neighbors need new saturation values. Updating all neighbors is correct but wastes time, and code that then selects among all vertices may pick a colored one again.
- **Swapping the keys.** Line L3 compares saturation first and uncolored degree second. Code that compares degree first is the largest-first order with a tie-break, and it loses the guarantee on bipartite graphs: it can choose a vertex of saturation 0 inside a component that is already partly colored.
- **Expecting optimality.** DSATUR is exact on bipartite graphs, but a 3-colorable graph can get 4 or more colors, as the example shows.

## Implementations

## History

Daniel Brélaz published DSATUR in Communications of the ACM in 1979, as a heuristic and as the vertex rule of an exact backtracking method. He compared it with the largest-first and smallest-last orders and proved that it is exact for bipartite graphs. Janczewski, Kubale, Manuszewski and Piwakowski studied in 2001 the smallest graphs on which it fails.

## References
