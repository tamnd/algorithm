---
tag: JTSFJW
kind: algorithm
slug: degeneracy-ordering
name: Smallest-last ordering
aliases:
- Matula ordering
- degeneracy ordering
area: graphs/coloring-and-cliques
level: intro
summary: Repeatedly remove a minimum-degree vertex; greedy coloring in reverse removal order uses at most degeneracy plus one colors.
solves: [graph-coloring]
model: word-ram
complexity:
  vars: {n: the number of vertices, m: the number of edges}
  time: {worst: Θ(n + m), best: Θ(n + m)}
  space: {extra: Θ(n)}
properties: {deterministic: true, recursive: false}
prereqs: [degeneracy, greedy-coloring, adjacency-list]
see_also: [degeneracy, greedy-coloring, delta-plus-one-bound, k-core-decomposition, batagelj-zaversnik-algorithm, bron-kerbosch, arboricity]
sources:
  - paper: doi:10.1145/2402.322385
    title: David W. Matula and Leland L. Beck, Smallest-last ordering and clustering and graph coloring algorithms, Journal of the ACM 30(3), 417 to 427 (1983)
    locator: the whole paper (the smallest-last order, its O(n + m) implementation with buckets of degrees, and the bound of degeneracy plus one colors)
  - paper: doi:10.1016/S0021-9800(68)80081-X
    title: G. Szekeres and H. S. Wilf, An inequality for the chromatic number of a graph, Journal of Combinatorial Theory 4(1), 1 to 3 (1968)
    locator: the whole paper (χ(G) ≤ 1 + max over subgraphs of the minimum degree)
  - book: isbn:9783662536216
    title: Reinhard Diestel, Graph Theory, fifth edition, Springer, 2017
    locator: Section 5.2, Colouring vertices (the colouring number col(G) and χ(G) ≤ col(G))
---

The smallest-last ordering of a graph removes a vertex of minimum degree again and again, each time from the graph that is left, and records the removal order. The largest degree seen at a removal is the [degeneracy](/degeneracy/) $d$ of the graph, and in the reverse order each vertex has at most $d$ neighbors that come before it. So [greedy coloring](/greedy-coloring/) in the reverse removal order uses at most $d + 1$ colors. Matula and Beck showed how to compute the order in $\Theta(n + m)$ time with an array of buckets indexed by degree.

## In plain words

Find a vertex with the fewest neighbors and take it out of the graph, with its lines. Its neighbors now have one neighbor less. Again find a vertex with the fewest neighbors in what is left, and take it out. Go on until the graph is empty. Write down the number of neighbors each vertex had when you took it out. The largest of these numbers is the degeneracy.

Now color the vertices in the opposite order: the last vertex taken out is colored first. When a vertex gets its color, the neighbors that already have colors are exactly the ones it had when it was taken out. There are at most as many as the degeneracy, so one more color always suffices.

## The problem

The input is a simple undirected graph $G = (V, E)$ with $V = \{0, \ldots, n-1\}$, as adjacency lists. The output is an order $v_1, \ldots, v_n$ of $V$ (the removal order) and the number $d$ such that

$$d = \max_{1 \le i \le n} \deg_{G_i}(v_i), \qquad G_i = G - \{v_1, \ldots, v_{i-1}\},$$

with $v_i$ a vertex of minimum degree in $G_i$. This $d$ is the degeneracy of $G$, $\max_{H \subseteq G} \delta(H)$. Used for [graph coloring](/graph-coloring/), the order gives a proper coloring with at most $d + 1$ colors.

## The algorithm

```pseudo id=main
SMALLEST-LAST(G)
L1  for each vertex v do deg[v] ← |Adj[v]|, put v in bucket B[deg[v]]
L2  d ← 0, i ← 0
L3  repeat n times
L4      while B[i] is empty do i ← i + 1
L5      v ← take a vertex out of B[i]
L6      d ← max(d, i), append v to the order, mark v removed
L7      for each neighbor w of v that is not removed do
L8          move w from B[deg[w]] to B[deg[w] − 1], deg[w] ← deg[w] − 1
L9      i ← max(i − 1, 0)
L10 return the order, d
```

Each bucket is a set with insertion and deletion in $O(1)$ time, for example a doubly linked list with a pointer from each vertex to its node. The index $i$ is the smallest degree that may still have a vertex. Removing $v$ lowers each degree by at most 1, so the new minimum is at least $i - 1$, and line L9 needs to step back by only one bucket. To color, run greedy coloring on the reverse of the order.

## Example

The graph has the vertices $0, \ldots, 6$ and the 11 edges $01, 02, 12, 13, 23, 24, 34, 35, 45, 06, 56$. The degrees are $3, 3, 4, 4, 3, 3, 2$. Ties are broken by taking the vertex that entered its bucket last.

| step | non-empty buckets before the step | $i$ | removed $v$ | $d$ |
|---|---|---|---|---|
| 1 | B[2] = {6}, B[3] = {0, 1, 4, 5}, B[4] = {2, 3} | 2 | 6 | 2 |
| 2 | B[2] = {0, 5}, B[3] = {1, 4}, B[4] = {2, 3} | 2 | 5 | 2 |
| 3 | B[2] = {0, 4}, B[3] = {1, 3}, B[4] = {2} | 2 | 4 | 2 |
| 4 | B[2] = {0, 3}, B[3] = {1, 2} | 2 | 3 | 2 |
| 5 | B[2] = {0, 1, 2} | 2 | 2 | 2 |
| 6 | B[1] = {0, 1} | 1 | 1 | 2 |
| 7 | B[0] = {0} | 0 | 0 | 2 |

The removal order is $6, 5, 4, 3, 2, 1, 0$ and the degeneracy is $d = 2$. Greedy coloring in the reverse order $0, 1, 2, 3, 4, 5, 6$ gives the colors $1, 2, 3, 1, 2, 3, 2$: 3 colors, which is $d + 1$. This is optimal, because the graph has a triangle. The maximum degree is 4, so the plain $\Delta + 1$ bound would allow 5 colors.

## Correctness

**Theorem.** SMALLEST-LAST returns an order $v_1, \ldots, v_n$ in which each $v_i$ has minimum degree in $G_i = G - \{v_1, \ldots, v_{i-1}\}$, and $d = \max_i \deg_{G_i}(v_i)$ equals the degeneracy $\max_{H \subseteq G} \delta(H)$. Greedy coloring in the order $v_n, \ldots, v_1$ uses at most $d + 1$ colors.

The invariant of the loop of line L3 is: $\deg[w] = \deg_{G_i}(w)$ for each vertex $w$ of $G_i$, each such $w$ is in the bucket $B[\deg[w]]$, and the buckets below $i$ are empty. Line L4 then finds the minimum degree, and lines L7 to L9 restore the invariant for $G_{i+1}$. The value $d$ is at most the degeneracy because $\deg_{G_i}(v_i) = \delta(G_i)$ and $G_i$ is a subgraph. It is at least the degeneracy because for any subgraph $H$, the first removed vertex $v_i$ of $H$ has $\deg_{G_i}(v_i) \ge \deg_H(v_i) \ge \delta(H)$. In the reverse order the earlier neighbors of $v_i$ are its neighbors in $G_i$, at most $d$ of them, so greedy uses at most $d + 1$ colors. The full proof is below.

## Complexity

The cost is in the [word RAM](/word-ram/) model, with adjacency lists and buckets as doubly linked lists.

- Line L1 takes $\Theta(n + m)$ time: $n$ list lengths and $n$ insertions.
- Lines L7 and L8 run once for each adjacency list entry, since each vertex is removed once, so $O(m)$ moves of $O(1)$ each in total.
- The index $i$: line L9 lowers it by at most 1 in each of the $n$ rounds, and $0 \le i \le n - 1$ always. So the total number of increments at line L4 is at most $(n - 1) + n$, and the scans of line L4 cost $O(n)$ in total.

So the time is $\Theta(n + m)$ in every case, and the extra space is $\Theta(n)$ for the degrees, the buckets and the order. Greedy coloring in the reverse order adds $\Theta(n + m)$.

## Properties

- **Exact degeneracy.** The algorithm computes the degeneracy and an order that certifies it. The same loop gives the core number of each vertex, the largest $k$ such that the vertex is in the [$k$-core](/k-core/); see [$k$-core decomposition](/k-core-decomposition/).
- **Coloring bound.** $d + 1 \le \Delta + 1$, and the gap can be large: a star has $d = 1$ and $\Delta = n - 1$.
- **Planar graphs.** Each planar graph has a vertex of degree at most 5, so $d \le 5$ and greedy gives at most 6 colors. This gives a linear-time 6-coloring of planar graphs.
- **Ties matter.** The degeneracy does not depend on how ties are broken, but the order and the coloring do.
- **Optimal for the bound.** Among all orders, a smallest-last order minimizes the largest number of earlier neighbors in the reverse order, which is the *coloring number* minus one.

## Variants and improvements

- **Core decomposition.** [Batagelj and Zaversnik](/batagelj-zaversnik-algorithm/) give the same computation with arrays sorted by degree instead of linked buckets.
- **Smallest-last coloring with interchanges.** Matula and Beck also study improvements of the greedy step; [DSATUR](/dsatur/) is another dynamic order.
- **Clique listing.** The [Bron-Kerbosch algorithm](/bron-kerbosch/) with the outer loop in degeneracy order lists all maximal cliques in $O(d\, n\, 3^{d/3})$ time (Eppstein, Löffler and Strash).
- **Orientation.** Orienting each edge from the earlier removed vertex to the later one gives an acyclic orientation with out-degree at most $d$, used in [triangle listing](/triangle-listing-by-degree/).

## When to use it

Use the smallest-last order as the default order for greedy coloring of sparse graphs, as in register allocation or the coloring of planar and road-like graphs. It costs the same as greedy coloring, and it gives a guarantee in terms of the degeneracy, which is small for planar graphs, trees and most real networks. Use it also as a preprocessing step for clique and triangle algorithms. When the number of colors matters more, try [DSATUR](/dsatur/) after it, or an exact algorithm on small graphs.

## Pitfalls

- **Using the initial degrees.** Sorting the vertices once by their degree in $G$ is the [Welsh-Powell](/welsh-powell-algorithm/) order, not the smallest-last order. Line L8 must lower the degrees of the neighbors after each removal.
- **Coloring in the removal order.** The guarantee is for the reverse order. In the removal order itself, the vertex removed last can have up to $\Delta$ colored neighbors.
- **A heap instead of buckets.** A binary heap with decrease-key gives $O((n + m) \log n)$ time. The buckets of line L1 and the step of line L9 give linear time.
- **Resetting $i$ to 0.** Restarting the scan of line L4 from 0 in each round costs $\Theta(n^2)$ in the worst case. Line L9 steps back by one only.

## Implementations

## History

Szekeres and Wilf proved in 1968 that $\chi(G) \le 1 + \max_H \delta(H)$, by the argument behind this order. Matula and Beck named the smallest-last order and gave its linear-time implementation with degree buckets in their 1983 paper, which also used it for clustering and for coloring.

## References
