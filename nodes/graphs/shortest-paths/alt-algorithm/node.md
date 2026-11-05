---
tag: DBXZ34
kind: algorithm
slug: alt-algorithm
name: ALT algorithm
aliases:
- A* with landmarks
- landmark-based A*
area: graphs/shortest-paths
level: advanced
summary: A* with landmark-based lower bounds derived from the triangle inequality.
solves: [single-pair-shortest-path]
model: word-ram
complexity:
  vars: {n: the number of vertices, m: the number of edges, k: the number of landmarks}
  time: {worst: O(k n + m log m), best: Θ(k)}
  space: {extra: Θ(k n)}
properties: {deterministic: true, recursive: false}
prereqs: [a-star-search, dijkstra, consistent-heuristic, triangle-inequality]
see_also: [bidirectional-dijkstra, contraction-hierarchies, highway-hierarchies, hub-labeling, potential-function-reduced-costs, admissible-heuristic, distance-oracle, single-pair-shortest-path]
sources:
  - url: https://www.microsoft.com/en-us/research/publication/computing-the-shortest-path-a-search-meets-graph-theory/
    title: Andrew V. Goldberg and Chris Harrelson, Computing the shortest path, A* search meets graph theory, SODA 2005 (Microsoft Research technical report MSR-TR-2004-24)
    locator: the sections on lower bounds from landmarks and the triangle inequality, landmark selection, and the bidirectional variant
  - paper: doi:10.1007/978-3-319-49487-6_2
    title: Hannah Bast, Daniel Delling, Andrew Goldberg, Matthias Müller-Hannemann, Thomas Pajor, Peter Sanders, Dorothea Wagner and Renato F. Werneck, Route planning in transportation networks, in Algorithm Engineering, LNCS 9220, 19 to 80 (2016)
    locator: Section 2, Shortest paths in road networks, the part on goal-directed techniques (A* and landmarks)
  - paper: doi:10.1109/TSSC.1968.300136
    title: Peter E. Hart, Nils J. Nilsson and Bertram Raphael, A formal basis for the heuristic determination of minimum cost paths, IEEE Transactions on Systems Science and Cybernetics 4(2), 100 to 107 (1968)
    locator: the whole paper (A* search, admissible and consistent heuristics)
---

The ALT algorithm answers a single [shortest-path](/single-pair-shortest-path/) query from $s$ to $t$ with [A* search](/a-star-search/), using lower bounds on the distance to $t$ that come from a few precomputed *landmarks*. For a landmark $L$ with known distances to and from every vertex, the [triangle inequality](/triangle-inequality/) gives $\operatorname{dist}(v, t) \ge \operatorname{dist}(v, L) - \operatorname{dist}(t, L)$ and $\operatorname{dist}(v, t) \ge \operatorname{dist}(L, t) - \operatorname{dist}(L, v)$. The name stands for A*, Landmarks and Triangle inequality. The bounds are [consistent](/consistent-heuristic/), so the search is [Dijkstra's algorithm](/dijkstra/) on reduced weights and returns exact distances, but it scans fewer vertices, because it is pulled toward $t$. It was introduced by Goldberg and Harrelson (2005) for road networks.

## In plain words

Before any question is asked, pick a few far-away places as landmarks and measure how far every place is from each landmark, in both directions.

Now someone asks for the best route from $s$ to $t$. For any place $v$, the landmark tables give a guaranteed minimum on how far $v$ still is from $t$. If the landmark lies beyond $t$, a place that is 100 km from the landmark while $t$ is only 30 km from it must be at least 70 km from $t$.

Run the usual nearest-first search, but rank each place by distance travelled so far plus this minimum still to go. Places in the wrong direction get large minimums and wait at the back of the line. The search heads toward $t$, stops when it reaches $t$, and still finds the true best route.

## The problem

The input is a directed graph $G = (V, E)$ with $n$ vertices and $m$ edges, a weight $w(u, v)$ on each edge, and a set of $k$ landmark vertices chosen in advance. Preprocessing stores $\operatorname{dist}(L, v)$ and $\operatorname{dist}(v, L)$ for every landmark $L$ and vertex $v$. A query gives $s$ and $t$ and asks for $\operatorname{dist}(s, t)$ and a shortest path, as in the [single-pair shortest-path problem](/single-pair-shortest-path/).

**Weight assumptions.** Weights are nonnegative real numbers; zero weights are allowed. Preprocessing runs Dijkstra and the query is a form of Dijkstra, so a negative weight makes the method wrong, and the implementation rejects it with an error, which also rules out negative cycles. If $t$ is not reachable from $s$, the query returns $+\infty$ and no path. A landmark that $s$ or $t$ cannot reach, or that cannot reach them, still gives valid bounds; the terms that would be $\infty - \infty$ are skipped.

## The algorithm

```pseudo id=main
ALT(G, w, landmarks; query s, t)
L1  for each landmark L do store dist(L, ·) and dist(·, L) by Dijkstra on G and on its reverse
L2  h(v) = max(0, max over L of dist(v, L) − dist(t, L), max over L of dist(L, t) − dist(L, v))
L3  g[v] ← ∞ for all v; g[s] ← 0; Q ← {s} with key g[s] + h(s)
L4  while Q is not empty do
L5      u ← the vertex in Q with the least key g[u] + h(u); remove it
L6      if u = t then return g[t] and the path through π
L7      for each edge (u, v) out of u do
L8          if h(v) < ∞ and g[u] + w(u, v) < g[v] then
L9              g[v] ← g[u] + w(u, v); π[v] ← u; put v in Q with key g[v] + h(v)
L10 return ∞                                        ▷ t is not reachable from s
```

Line L1 is the preprocessing, done once for all queries. Line L2 is evaluated when a vertex is first touched, in $O(k)$ time; a term is skipped when it would be $\infty - \infty$, and $h(v) = \infty$ means that $v$ cannot reach $t$ (it misses a landmark that $t$ reaches, or is missed by a landmark that reaches $t$), so line L8 never enters $v$. Lines L3 to L10 are [A* search](/a-star-search/) with heuristic $h$.

**Why the bounds hold.** For any vertices, $\operatorname{dist}(v, L) \le \operatorname{dist}(v, t) + \operatorname{dist}(t, L)$, and $\operatorname{dist}(L, t) \le \operatorname{dist}(L, v) + \operatorname{dist}(v, t)$. Rearranging gives the two terms of line L2. On an undirected graph both terms say $|\operatorname{dist}(L, v) - \operatorname{dist}(L, t)| \le \operatorname{dist}(v, t)$. The bound is tight when a shortest path from $v$ to $L$ passes through $t$, which is why landmarks "behind" the target help most.

**Choosing landmarks.** Correctness holds for any choice; only speed depends on it. Goldberg and Harrelson tried random, *farthest* (each new landmark is the vertex farthest from those chosen) and *planar* (landmarks spread around the border of a map) selection. A handful to a few dozen landmarks are typical for road networks.

## Example

The vertices are $s, a, b, t, x, y, z, \ell$, and each edge goes both ways: $s - a$ (2), $a - b$ (2), $b - t$ (2), $s - x$ (1), $x - y$ (1), $y - z$ (1), $t - \ell$ (1). The query is $s$ to $t$, and $\operatorname{dist}(s, t) = 6$.

**Plain Dijkstra** scans in order of distance: $s$ (0), $x$ (1), $y$ (2), $a$ (2), $z$ (3), $b$ (4), $t$ (6). That is 7 scans, with $x, y, z$ wasted on the side away from $t$.

**ALT with the landmark $\ell$.** The bounds $h(v) = \operatorname{dist}(v, \ell) - \operatorname{dist}(t, \ell) = \operatorname{dist}(v, \ell) - 1$ are:

| vertex | $s$ | $a$ | $b$ | $t$ | $x$ | $y$ | $z$ | $\ell$ |
|---|---|---|---|---|---|---|---|---|
| $h$ | 6 | 4 | 2 | 0 | 7 | 8 | 9 | 1 |

They are exact on $s, a, b, t$, since the shortest paths from these vertices to $\ell$ pass through $t$. Scanning $s$ gives $a$ the key $2 + 4 = 6$ and $x$ the key $1 + 7 = 8$. Then $a$ is scanned and $b$ gets $4 + 2 = 6$, then $b$, and $t$ gets $6 + 0 = 6$. The search scans $s, a, b, t$, 4 vertices, returns 6 and the path $s, a, b, t$, and never touches $y$ or $z$.

**Unreachable target.** In the graph $s \to a \to b$, $q \to s$ with the landmark $b$, the query $s$ to $q$ has $\operatorname{dist}(s, b) = 2$ finite and $\operatorname{dist}(q, b) = 3$ finite, so the first term gives no proof, and the search scans $s, a, b$ and returns $\infty$. With the landmark $q$ and the query $s$ to $b$ in the graph $s \to a$, $b \to q$, the term $\operatorname{dist}(s, q) - \operatorname{dist}(b, q) = \infty - 1$ shows at once that $s$ cannot reach $b$, and the search ends with no scan.

## Correctness

**Theorem.** If all weights are nonnegative, the query returns $\operatorname{dist}(s, t)$ and a shortest path when $t$ is reachable from $s$, and $\infty$ otherwise; each vertex is scanned at most once.

The proof has three parts. First, $h$ is a lower bound with $h(t) = 0$, and it is *consistent*: $h(u) \le w(u, v) + h(v)$ for every edge with $h(u) < \infty$, because each term of line L2 has this property by the triangle inequality, and the maximum of consistent functions is consistent. Second, a vertex with $h(v) = \infty$ cannot reach $t$, so pruning it removes no $s$-$t$ path. Third, with the [reduced weights](/potential-function-reduced-costs/) $w_h(u, v) = w(u, v) - h(u) + h(v) \ge 0$, every $s$-$t$ path has reduced weight $w(P) - h(s) + h(t)$, so shortest paths do not change, and the key $g[v] + h(v)$ is the reduced distance plus the constant $h(s)$. So the query is Dijkstra's algorithm on nonnegative reduced weights, stopped when $t$ is scanned, which is correct by the [Dijkstra correctness theorem](/dijkstra-correctness/). The full proof is in the proof file below.

## Complexity

The model is the [word RAM](/word-ram/), with $k$ landmarks.

- **Preprocessing.** $2k$ runs of Dijkstra, $O(k(m + n \log n))$ time with a Fibonacci heap or $O(k\,m \log m)$ with a binary heap, and $\Theta(k n)$ words of tables.
- **Query, worst case.** Each vertex is scanned at most once and its bound is computed once in $O(k)$, and each edge pushes at most one heap entry, so the time is $O(k n + m \log m)$ with a binary heap. The worst case is no better than Dijkstra: landmarks that give $h = 0$ change nothing.
- **Query, best case.** When $s = t$, the query computes $h(s)$, scans $s$ and stops, $\Theta(k)$ time. When some bound is $\infty$ at $s$, the query ends without a scan.
- **In practice.** On road networks, ALT scans tens of times fewer vertices than Dijkstra, according to Goldberg and Harrelson; the methods based on [contraction](/contraction-hierarchies/) or [labels](/hub-labeling/) are far faster, but need heavier preprocessing.

## Properties

- **Exact.** The answer is the true distance, not an estimate; the landmarks only change the order of the scans.
- **Each vertex scanned once.** Because $h$ is consistent, a scanned vertex has its final $g$, as in Dijkstra.
- **Robust to weight increases.** If some weights increase after preprocessing, the stored distances become smaller than the new ones, so the bounds stay valid lower bounds and remain consistent (the new weight only grows); queries stay correct, only slower. A decrease requires new preprocessing.
- **Space-hungry.** The tables take $2k n$ numbers, which is the main cost on large graphs.
- **Monotone in landmarks.** Adding a landmark can only raise $h$, and a pointwise larger consistent bound never makes A* scan more vertices, apart from ties.

## Variants and improvements

- **Bidirectional ALT.** Run a forward A* toward $t$ and a backward A* toward $s$. The two potentials must agree, so both use the average $\tfrac12(h_t(v) - h_s(v))$ of the forward and backward bounds; Goldberg and Harrelson use this form, which goes back to Ikeda and others (1994). The stopping rule is as in [bidirectional Dijkstra](/bidirectional-dijkstra/).
- **Active landmarks.** For a query, use only the few landmarks that give the best bound at $s$ and $t$, and add others as the search goes on; this cuts the $O(k)$ per bound.
- **Combinations.** ALT combines with reach-based pruning (the REAL method of Goldberg, Kaplan and Werneck) and with contraction (Core-ALT, where landmarks live on a small core of important vertices).
- **Other heuristics.** For geometric graphs, the straight-line distance divided by the top speed is also a consistent bound; landmarks usually give much tighter ones on road networks.

## When to use it

Use ALT for point-to-point queries on a large graph that stays fixed or where weights only increase (for example traffic delays), when memory for $2k$ distances per vertex is available and the heavy preprocessing of [contraction hierarchies](/contraction-hierarchies/) or [hub labels](/hub-labeling/) is not. For a single query, plain or [bidirectional Dijkstra](/bidirectional-dijkstra/) is cheaper, since preprocessing costs $2k$ full searches. For negative weights, ALT does not apply.

## Pitfalls

- **Infinite distances.** A naive bound $\operatorname{dist}(v, L) - \operatorname{dist}(t, L)$ with both infinite gives $\infty - \infty$, which is NaN in floating point and breaks heap comparisons. Skip such terms.
- **Directed graphs.** Use the distances *to* the landmark on the reverse graph and the distances *from* the landmark on the forward graph; in a directed graph they differ, and swapping them gives bounds that are not valid.
- **Inconsistent bidirectional potentials.** Using the forward bound in one search and the backward bound in the other breaks the stopping rule; use averaged potentials.
- **Stopping at the first touch of $t$.** As with Dijkstra, the answer is final only when $t$ is removed from the queue, not when it is first relaxed.
- **Floating-point rounding.** With real weights, rounding can make a bound exceed the true distance by a tiny amount, which breaks consistency; with integer weights this cannot happen.

## Implementations

The Python version has a preprocessing function that runs Dijkstra from and to each landmark, and a query that computes bounds on demand, prunes vertices with infinite bounds, and returns the distance, a path and the number of scans.

## History

Hart, Nilsson and Raphael (1968) introduced A* search with lower bounds. Goldberg and Harrelson (2005) used landmarks and the triangle inequality to get bounds on graphs without geometry, named the method ALT, and studied landmark selection and the bidirectional version; Goldberg and Werneck developed it further. The survey of Bast and others (2016) places ALT among the goal-directed techniques for route planning.

## References
