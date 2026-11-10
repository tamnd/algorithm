---
tag: MQCR0W
kind: algorithm
slug: vertex-cover-2-approximation
name: Vertex cover 2-approximation via maximal matching
aliases:
- maximal matching vertex cover
- APPROX-VERTEX-COVER
area: approximation/covering-and-packing
level: intro
summary: Take both endpoints of each edge of a maximal matching; the cover has at most twice as many vertices as a smallest one, and 2 − ε is hard under the Unique Games Conjecture.
solves: [vertex-cover]
model: word-ram
complexity:
  vars: {n: the number of vertices, m: the number of edges}
  time: {worst: Θ(n + m)}
  space: {extra: Θ(n)}
properties: {deterministic: true, recursive: false, online: true}
history:
  year: 1974
  people: [Fănică Gavril, Mihalis Yannakakis]
  note: Garey and Johnson (1979) credit the maximal matching algorithm to Gavril and Yannakakis; it is the first example in most texts on approximation algorithms.
prereqs: [vertex-cover, maximal-matching, approximation-ratio]
see_also: [primal-dual-weighted-vertex-cover, lp-rounding-vertex-cover, maximal-matching, konig-theorem, vertex-cover-inapproximability, set-cover-primal-dual, parameterized-vertex-cover]
sources:
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Chapter 35, Section 35.1 (APPROX-VERTEX-COVER, Theorem 35.1)
  - book: isbn:9783540653677
    title: Vijay V. Vazirani, Approximation Algorithms
    locator: Chapter 1, Section 1.1 (lower bounding OPT by a maximal matching, and the tight example)
  - book: isbn:9780716710455
    title: Michael R. Garey and David S. Johnson, Computers and Intractability
    locator: Chapter 6 (approximation algorithms for NP-hard problems, the vertex cover example)
  - paper: doi:10.4007/annals.2005.162.439
    title: Irit Dinur and Samuel Safra, On the hardness of approximating minimum vertex cover, Annals of Mathematics 162(1), 2005
    locator: pages 439 to 485 (1.3606 is NP-hard)
  - paper: doi:10.1016/j.jcss.2007.06.019
    title: Subhash Khot and Oded Regev, Vertex cover might be hard to approximate to within 2 − ε, Journal of Computer and System Sciences 74(3), 2008
    locator: pages 335 to 349
---

The maximal matching algorithm finds a [vertex cover](/vertex-cover/) of a graph with at most twice as many vertices as a smallest one. It scans the edges, and when an edge has no endpoint in the cover yet, it puts both endpoints into the cover. The chosen edges form a [maximal matching](/maximal-matching/), and any cover needs one vertex for each edge of a matching, so the cover has at most $2 \cdot$ OPT vertices. The ratio 2 is tight for the algorithm. No polynomial-time algorithm is known with a ratio $2 - \varepsilon$ for a constant $\varepsilon > 0$, and under the [Unique Games Conjecture](/unique-games-conjecture/) none exists.

## In plain words

You must choose points of a network so that each link touches a chosen point. Look at the links one by one. When a link touches no chosen point, choose both of its ends.

The links that made you choose points share no end, because each of them touched no chosen point when you took it. Any good choice must take at least one end of each of these links, and these ends are all different. You took two ends for each of these links, so you took at most twice as many points as the best choice.

## The problem

The input is an undirected graph $G = (V, E)$ with $n$ vertices and $m$ edges and no self-loops. The output is a set $C \subseteq V$ such that each edge has at least one endpoint in $C$. The goal is a small $|C|$. OPT is the size of a smallest vertex cover, and the ratio convention is ALG $\le \rho \cdot$ OPT.

## The algorithm

```pseudo id=main
APPROX-VERTEX-COVER(G = (V, E))
L1  C ← ∅, M ← empty list
L2  for each edge {u, v} in E, in any order do
L3      if u ∉ C and v ∉ C then
L4          append {u, v} to M
L5          C ← C ∪ {u, v}
L6  return C, M
```

The list $M$ is not needed for the cover; it is the certificate for the bound, because OPT $\ge |M|$. The test in line L3 checks that the edge is not yet covered. The edges of $M$ have no common endpoints, so $M$ is a matching, and when the scan ends no edge can be added to it, so it is maximal.

## Example

The graph has the vertices 1 to 7 and nine edges, scanned in this order.

| edge | covered before? | action | $C$ after |
|---|---|---|---|
| 1-2 | no | take | 1, 2 |
| 1-3 | yes, by 1 | skip | 1, 2 |
| 2-3 | yes | skip | 1, 2 |
| 2-4 | yes, by 2 | skip | 1, 2 |
| 3-5 | no | take | 1, 2, 3, 5 |
| 4-5 | yes, by 5 | skip | 1, 2, 3, 5 |
| 4-6 | no | take | 1, 2, 3, 4, 5, 6 |
| 5-7 | yes, by 5 | skip | 1, 2, 3, 4, 5, 6 |
| 6-7 | yes, by 6 | skip | 1, 2, 3, 4, 5, 6 |

The matching is $M = \{1\text{-}2, 3\text{-}5, 4\text{-}6\}$, and the cover has 6 vertices. The matching proves OPT $\ge 3$. The real optimum is 4, for example $\{1, 2, 5, 6\}$: the triangle 1, 2, 3 needs two vertices, and the edges 4-6, 5-7 and 6-7 need two more vertices outside the triangle. So the ratio is $6/4 = 1.5$ here, and the certified ratio is $6/3 = 2$.

## Correctness

The scan keeps two facts: $M$ is a matching, and $C$ is the set of its endpoints. Each edge is covered after its turn in the scan, so at the end $C$ is a vertex cover. Any vertex cover must contain an endpoint of each edge of $M$, and these endpoints are distinct because $M$ is a matching, so OPT $\ge |M|$.

**Theorem.** APPROX-VERTEX-COVER returns a vertex cover $C$ with $|C| = 2|M| \le 2 \cdot \text{OPT}$, in the worst case.

The full proof is in the proof file below.

**The lower bound used.** The size of any matching is a lower bound on OPT. It is also a lower bound on the LP optimum: putting $y_e = 1$ on the edges of $M$ is a feasible solution of the dual of the [LP relaxation](/lp-relaxation/), the fractional matching LP. So the algorithm is also a very simple primal-dual algorithm.

**Tight examples.** The ratio 2 is tight. On a graph that is a perfect matching of $n/2$ edges, the algorithm takes all $n$ vertices, and OPT $= n/2$. On the complete bipartite graph $K_{k,k}$, each maximal matching is perfect, so the algorithm takes all $2k$ vertices, and OPT $= k$. The lower bound itself is the weak point: on $K_{2k+1}$, the complete graph, the largest matching has $k$ edges and OPT $= 2k$, so no analysis based only on a matching can prove a ratio better than 2.

**Hardness.** Approximating vertex cover within 1.3606 is NP-hard (Dinur and Safra 2005), and within $\sqrt{2} - \varepsilon$ is NP-hard (Khot, Minzer and Safra 2018). Under the Unique Games Conjecture, $2 - \varepsilon$ is hard (Khot and Regev 2008). See [vertex cover inapproximability](/vertex-cover-inapproximability/).

## Complexity

- **Time.** The scan looks at each edge once, and each test and insertion takes $O(1)$ time with a Boolean array indexed by the vertices. The array costs $\Theta(n)$ to set up. So the time is $\Theta(n + m)$ in the worst case, in the [word RAM](/word-ram/). With a hash set, as in the Python code, the time is $\Theta(m)$ expected.
- **Space.** The flags for $C$ take $\Theta(n)$ extra space, and $M$ has at most $n/2$ edges.

## Properties

- **Deterministic.** For a fixed edge order, the output depends only on the input.
- **Online.** The algorithm reads each edge once and never removes a vertex, so it works when the edges arrive one at a time. It is a 2-competitive online algorithm for vertex cover in this edge-arrival model.
- **Any order.** The bound holds for each edge order and for each maximal matching.
- **Even size.** The cover always has an even number of vertices, $2|M|$.
- **A certificate.** The matching $M$ proves the lower bound $|M| \le$ OPT, so each run reports its own error bound.

## Variants and improvements

- **Weighted vertex cover.** With vertex weights, taking both endpoints can cost far more than OPT. The [primal-dual algorithm](/primal-dual-weighted-vertex-cover/) and [LP rounding](/lp-rounding-vertex-cover/) give ratio 2 for the [weighted problem](/weighted-vertex-cover/).
- **Removing redundant vertices.** After the scan, drop each vertex whose neighbours are all in $C$. This never hurts and often helps, but the ratio 2 stays: on a perfect matching, no vertex can be dropped.
- **DFS tree.** The internal vertices of a depth-first search tree form a vertex cover of size at most $2 \cdot$ OPT (Savage 1982). This is another 2-approximation.
- **Better ratios.** The best known ratio is $2 - \Theta(1/\sqrt{\log n})$ (Karakostas 2009), by semidefinite programming. Constant ratios below 2 are known for special graphs: bipartite graphs are solved exactly by [König's theorem](/konig-theorem/), and [planar graphs](/planar-graph/) have a [PTAS](/baker-planar-ptas/).
- **Exact algorithms.** For small covers, [fixed-parameter algorithms](/parameterized-vertex-cover/) find OPT in time exponential only in OPT; a maximal matching of size more than $k$ proves that no cover of size $k$ exists.

## When to use it

Use this algorithm when you need a vertex cover fast, with a guarantee, and all vertices have the same cost. It is a single pass over the edges and works on edge streams. It also gives a quick lower bound for an exact search: a branch-and-bound or a [kernel](/crown-reduction/) can start from the matching. With weights, use the primal-dual or LP rounding algorithm instead. When quality matters more than the worst case, run a local search or an exact solver from this cover.

## Pitfalls

- **Taking one endpoint.** Taking only one endpoint of each uncovered edge, for example the one of higher degree, has no constant ratio in the worst case. The greedy that picks the vertex of largest degree has ratio $\Theta(\log n)$ on some graphs. The proof needs both endpoints.
- **A non-maximal matching.** If the scan stops early, or uses a matching that is not maximal, some edge may stay uncovered.
- **Using a maximum matching.** A maximum matching is not needed, and it does not improve the bound: the endpoints of any maximal matching give the same ratio 2.
- **Self-loops.** An edge $\{v, v\}$ is covered only by $v$. The proof assumes no self-loops; put each such $v$ in the cover first, or reject the input, as the implementation does.

## Implementations

## History

The maximal matching algorithm is one of the oldest approximation algorithms. Garey and Johnson (1979) credit it to Gavril and to Yannakakis. It appears as APPROX-VERTEX-COVER in CLRS and as the first example in Vazirani's book. Bar-Yehuda and Even (1981) and Hochbaum (1982) extended the ratio 2 to weighted vertex cover. Dinur and Safra (2005) proved the first hardness above 1.36, Khot and Regev (2008) proved that 2 is optimal under the Unique Games Conjecture, and Khot, Minzer and Safra (2018) raised the NP-hardness to $\sqrt{2} - \varepsilon$.

## References
