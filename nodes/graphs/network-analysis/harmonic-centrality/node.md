---
tag: 3MDVJ6
kind: definition
slug: harmonic-centrality
name: Harmonic centrality
aliases:
- harmonic closeness
area: graphs/network-analysis
level: intro
summary: Sum of inverse distances to all other nodes, defined for disconnected graphs.
prereqs: [centrality, closeness-centrality, shortest-path, breadth-first-search]
see_also: [closeness-centrality, degree-centrality, betweenness-centrality, katz-centrality, neighborhood-function, all-pairs-shortest-paths, hyperloglog]
sources:
  - paper: doi:10.1080/15427951.2013.865686
    title: Paolo Boldi and Sebastiano Vigna, Axioms for centrality, Internet Mathematics 10(3-4), 222 to 262 (2014)
    locator: Section 2 (the definition of harmonic centrality and its relation to closeness) and the sections on the axioms of size, density and score monotonicity
  - paper: doi:10.1016/S0378-4371(00)00311-3
    title: Massimo Marchiori and Vito Latora, Harmony in the small-world, Physica A 285(3-4), 539 to 546 (2000)
    locator: the whole paper (the sum of inverse distances as a measure of a network that need not be connected)
  - book: isbn:9780199206650
    title: M. E. J. Newman, Networks, An Introduction, Oxford University Press, 2010
    locator: Chapter 7, Measures and metrics (the section on closeness centrality, with the harmonic mean form for networks with more than one component)
---

Harmonic centrality is the [centrality](/centrality/) measure that scores a [vertex](/vertex/) $v$ by the sum of the inverses of its [shortest-path](/shortest-path/) distances to the other vertices, with $1/\infty = 0$. It is the fix of [closeness centrality](/closeness-centrality/) for graphs that are not connected: a vertex that cannot reach another vertex just gets nothing for it, and the score stays finite and meaningful. Near vertices count much more than far ones, so the score mixes the local view of [degree centrality](/degree-centrality/) with the global view of closeness.

## Definition

Let $G = (V, E)$ be a graph with $n \ge 2$ vertices, and let $d(u, v) \in \{0, 1, 2, \ldots\} \cup \{\infty\}$ be the number of edges on a shortest path from $u$ to $v$, with $d(u, v) = \infty$ when there is no path. The **harmonic centrality** of $v$ is

$$H(v) = \sum_{u \in V,\ u \ne v} \frac{1}{d(u, v)}, \qquad \text{where } \frac{1}{\infty} = 0.$$

The **normalized** score is $H(v)/(n - 1)$. Each term is at most 1, with equality exactly when $u$ is adjacent to $v$, so $0 \le H(v)/(n-1) \le 1$, with 1 exactly when $v$ is adjacent to every other vertex and 0 exactly when no other vertex can reach $v$.

**Undirected graphs.** Then $d(u, v) = d(v, u)$, and the sum is the same in both directions.

**Directed graphs.** Boldi and Vigna sum over the distances *to* $v$, $d(u, v)$, so that a vertex is central when many vertices reach it in few steps, as for a web page that many pages point to. The *out* version uses $d(v, u)$ instead. The two can differ a lot: on the path $0 \to 1 \to 2$ with the extra arc $3 \to 2$, vertex 2 has the in-score $1 + \tfrac12 + 1 = \tfrac52$ and the out-score 0.

**Weighted graphs.** If each edge has a length $w(e) > 0$, $d$ is the weighted shortest-path distance. A weight that measures the strength of a tie must first be turned into a length, for example $1/w$. A length of 0 is not allowed, since it gives a term $1/0$.

**Disconnected graphs.** No special case is needed. A vertex $u$ that cannot reach $v$ adds $0$, and an isolated vertex has the score 0.

**Ties.** Equal scores are common, for example for vertices that an automorphism of the graph maps to each other. The definition gives scores, not an order, so a ranking must state how it breaks ties.

**Relation to closeness.** For a connected graph, the normalized closeness $(n-1)/\sum_u d(u,v)$ is the inverse of the arithmetic mean of the $n - 1$ distances to $v$, and the normalized harmonic score $H(v)/(n-1)$ is the inverse of their harmonic mean. The arithmetic mean is at least the harmonic mean, so $H(v)/(n-1)$ is at least the normalized closeness, with equality exactly when all the distances are equal. Some vertex is adjacent to $v$, so this happens exactly when all the distances are 1.

**Cost.** The scores of all vertices need the distances of all pairs: $O(nm)$ time by one [breadth-first search](/breadth-first-search/) from each vertex in an unweighted graph, and $O(nm + n^2 \log n)$ time with [Dijkstra's algorithm](/dijkstra/) in a weighted one. For a directed graph, the searches run on the [transpose](/graph-transpose/) to get the distances to each vertex. For very large graphs, the [neighbourhood function](/neighborhood-function/) gives an estimate: with $N_v(t)$ the number of vertices at distance at most $t$ from $v$, $H(v) = \sum_{t \ge 1} \frac{N_v(t) - N_v(t-1)}{t}$, and $N_v(t)$ can be approximated with [HyperLogLog](/hyperloglog/) counters, as in the [ANF algorithm](/anf-algorithm/).

## Examples and non-examples

**A worked example.** Take the undirected graph with the vertices 0 to 6 and the 9 edges $\{0,1\}$, $\{0,2\}$, $\{1,2\}$, $\{1,3\}$, $\{2,3\}$, $\{3,4\}$, $\{4,5\}$, $\{4,6\}$, $\{5,6\}$, the example of the [closeness](/closeness-centrality/) page. The distances from vertex 3 are $2, 1, 1, 1, 2, 2$ to the vertices $0, 1, 2, 4, 5, 6$, so $H(3) = \tfrac12 + 1 + 1 + 1 + \tfrac12 + \tfrac12 = \tfrac92$.

| $v$ | distances to the others | $H(v)$ | $H(v)/6$ |
|---|---|---|---|
| 0 | 1 1 2 3 4 4 | $10/3 \approx 3.333$ | 0.556 |
| 1, 2 | 1 1 1 2 3 3 | $25/6 \approx 4.167$ | 0.694 |
| 3 | 2 1 1 1 2 2 | $9/2 = 4.5$ | 0.750 |
| 4 | 3 2 2 1 1 1 | $13/3 \approx 4.333$ | 0.722 |
| 5, 6 | 4 3 3 2 1 1 | $41/12 \approx 3.417$ | 0.569 |

On this connected graph the order is the same as for closeness: $3$, then $4$, then $1$ and $2$, then $5$ and $6$, then $0$.

**A disconnected graph.** Take the vertices 0 to 5 with the edges $\{0,1\}$, $\{1,2\}$, $\{2,3\}$, $\{1,3\}$ and the separate edge $\{4,5\}$, so $n = 6$.

| $v$ | distances to the others | $H(v)$ | closeness inside the component |
|---|---|---|---|
| 0 | 1 2 2 $\infty$ $\infty$ | 2 | 3/5 = 0.6 |
| 1 | 1 1 1 $\infty$ $\infty$ | 3 | 3/3 = 1 |
| 2, 3 | 2 1 1 $\infty$ $\infty$ | 5/2 | 3/4 = 0.75 |
| 4, 5 | $\infty$ $\infty$ $\infty$ $\infty$ 1 | 1 | 1/1 = 1 |

Closeness computed inside each component gives vertex 1, which touches every vertex of its group of four, the same score as vertex 4, which touches one vertex. Harmonic centrality gives 3 to vertex 1 and 1 to vertex 4, since vertex 1 reaches three vertices in one step and vertex 4 only one.

**Non-examples.**

- The inverse of the sum of the distances, $1/\sum_u d(u, v)$, is Sabidussi's closeness, not harmonic centrality. On the graph above it is 0 for every vertex, because each sum holds an infinite term.
- The sum of the distances with the infinite terms dropped, $\sum_{u: d(u,v) < \infty} d(u, v)$, is not a substitute either. Vertex 4 gets the sum 1 and vertex 1 the sum 3, so by this farness vertex 4 looks the most central of all.
- Degree centrality is not harmonic centrality, even though it is the first term of it. In the first example, the vertices 1, 2, 3 and 4 all have degree 3, while their harmonic scores are $25/6$, $25/6$, $9/2$ and $13/3$.

## Related definitions

- [Closeness centrality](/closeness-centrality/): the inverse of the mean distance, defined only when all distances are finite.
- [Degree centrality](/degree-centrality/): only the terms with $d(u, v) = 1$.
- [Katz centrality](/katz-centrality/): a sum over all walks, not only shortest paths, damped by length.
- [Betweenness centrality](/betweenness-centrality/): counts shortest paths through a vertex, not their lengths.
- [Neighbourhood function](/neighborhood-function/): the counts of vertices within each distance, from which harmonic centrality can be computed.
- The global *efficiency* of Marchiori and Latora is the mean of $1/d(u, v)$ over all ordered pairs $u \ne v$, that is $\frac{1}{n(n-1)} \sum_v H(v)$.
- Boldi and Vigna state three axioms for a centrality on directed graphs, called size, density and score monotonicity. In their paper, harmonic centrality is the only measure among those they study that satisfies all three.

## References
