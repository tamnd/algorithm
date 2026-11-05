---
tag: Q8WB3G
kind: theorem
slug: gallai-identity
name: Gallai's identity
aliases:
- Gallai's theorem on edge covers
area: graphs/matching
level: core
summary: The maximum matching size plus the minimum edge cover size equals the number of vertices.
prereqs: [edge-cover]
see_also: [minimum-edge-cover, maximum-matching, vertex-cover, independent-set, konig-theorem, bipartite-maximum-independent-set, perfect-matching]
sources:
  - paper: "Tibor Gallai, Über extreme Punkt- und Kantenmengen, Annales Universitatis Scientiarum Budapestinensis de Rolando Eötvös Nominatae, Sectio Mathematica 2, 133 to 138 (1959)"
    locator: the whole paper (the identities for points and for edges)
  - book: isbn:9780130144003
    title: Douglas B. West, Introduction to Graph Theory, second edition
    locator: Section 3.1, Matchings and covers (Gallai's theorem on independence and covering numbers)
  - book: isbn:9783540443896
    title: Alexander Schrijver, Combinatorial Optimization, Polyhedra and Efficiency
    locator: Section 19.1, Matchings, edge covers, and Gallai's theorem, and Section 27.1, Minimum-size edge cover
---

Gallai's identity says that in a graph with $n$ vertices and no isolated vertex, the size $\nu(G)$ of a [maximum matching](/maximum-matching/) and the size $\rho(G)$ of a minimum [edge cover](/edge-cover/) add up to $n$. Its twin, for vertices, says that the size $\alpha(G)$ of a maximum [independent set](/independent-set/) and the size $\tau(G)$ of a minimum [vertex cover](/vertex-cover/) also add up to $n$, in every graph. Both hold for general graphs, bipartite or not, and are about sizes, not weights. The proof is constructive: it turns a maximum matching into a minimum edge cover in linear time, and back.

## Statement

Let $G = (V, E)$ be a finite undirected graph with $n = |V|$ vertices. Let $\nu(G)$ be the largest size of a matching, $\rho(G)$ the least size of an edge cover, $\alpha(G)$ the largest size of a set of pairwise non-adjacent vertices, and $\tau(G)$ the least size of a set of vertices that meets every edge.

**Theorem (Gallai, 1959).**

1. For every graph, $\alpha(G) + \tau(G) = n$.
2. If $G$ has no isolated vertex, then $\nu(G) + \rho(G) = n$.

## In plain words

Think of a dance where every person must dance with someone. Some couples dance as pairs, and the people who are left over join an existing couple as a third dancer, or dance with someone already dancing. A set of couples that covers everybody is an edge cover. The best plan uses as many separate pairs as possible, because each separate pair covers two people with one couple, while each left-over person costs one more couple. So the smallest number of couples is the number of people minus the largest number of separate pairs.

The vertex identity is simpler still: a set of people with no partner between them is exactly what is left after you remove a set that touches every possible pair.

## Proof

**Part 1.** A set $S \subseteq V$ is independent if and only if $V \setminus S$ is a vertex cover: an edge with no end in $V \setminus S$ has both ends in $S$. So complementation is a bijection between independent sets and vertex covers that maps size $k$ to size $n - k$. The largest independent set therefore corresponds to the smallest vertex cover, and $\alpha(G) = n - \tau(G)$.

**Part 2, $\rho \le n - \nu$.** Let $M$ be a maximum matching. It covers $2\nu$ vertices and leaves a set $U$ of $n - 2\nu$ free vertices. Each $u \in U$ is not isolated, so pick one edge $e_u$ at $u$. Then $F = M \cup \{e_u : u \in U\}$ covers every vertex and has at most $\nu + (n - 2\nu) = n - \nu$ edges.

**Part 2, $\nu \ge n - \rho$.** Let $F$ be a minimum edge cover. It is minimal, so by the structure result on the [edge cover](/edge-cover/) page the subgraph $(V, F)$ is a forest of stars, and each vertex lies in exactly one star, since $F$ covers all vertices. A forest with $n$ vertices and $c$ components has $n - c$ edges, so the number of stars is $c = n - |F| = n - \rho$. Pick one edge from each star. Edges from different components share no end, so these $n - \rho$ edges form a matching, and $\nu \ge n - \rho$.

The two inequalities give $\nu + \rho = n$. $\blacksquare$

## Consequences

- **Minimum edge cover in polynomial time.** The first half of the proof is an algorithm: compute a maximum matching, then add one edge at each free vertex. With [Hopcroft-Karp](/hopcroft-karp/) this takes $O(m\sqrt n)$ time for a bipartite graph, and with [Edmonds' blossom algorithm](/edmonds-blossom/) polynomial time in general. This solves the [minimum edge cover](/minimum-edge-cover/) problem. By part 1, in contrast, the vertex cover and independent set problems are equally hard, and both are [NP-complete](/np-complete/) in general graphs.
- **Kőnig's two theorems.** In a [bipartite graph](/bipartite-graph/), [Kőnig's theorem](/konig-theorem/) gives $\nu = \tau$. With both identities, $\alpha = n - \tau = n - \nu = \rho$ when there is no isolated vertex. So in a bipartite graph the largest independent set has the size of the smallest edge cover, which is how a [maximum independent set in a bipartite graph](/bipartite-maximum-independent-set/) is computed.
- **Perfect matchings.** $\rho(G) = n/2$ if and only if $G$ has a [perfect matching](/perfect-matching/). This follows from $\rho = n - \nu$ and $\nu \le n/2$.
- **Weak duality pairs.** In every graph $\nu \le \tau$ and $\alpha \le \rho$, because each edge of a matching needs its own cover vertex and each vertex of an independent set needs its own covering edge. Gallai's identities show that the two gaps are equal: $\tau - \nu = \rho - \alpha$ when there is no isolated vertex.

## Tightness

- **Isolated vertices.** In the graph with vertices $a, b, c$ and the one edge $ab$, there is no edge cover. If isolated vertices are removed first, the identity holds for the rest.
- **The empty graph.** With no vertices, $\nu = \rho = \alpha = \tau = 0$, and both identities read $0 = 0$.
- **Numbers on small graphs.** The table gives the four numbers. In each row, $\nu + \rho = \alpha + \tau = n$.

| graph | $n$ | $\nu$ | $\rho$ | $\alpha$ | $\tau$ |
|---|---|---|---|---|---|
| path $P_5$ | 5 | 2 | 3 | 3 | 2 |
| cycle $C_5$ | 5 | 2 | 3 | 2 | 3 |
| star $K_{1,4}$ | 5 | 1 | 4 | 4 | 1 |
| complete graph $K_5$ | 5 | 2 | 3 | 1 | 4 |
| Petersen graph | 10 | 5 | 5 | 4 | 6 |

In $C_5$, $K_5$ and the Petersen graph, $\nu < \tau$ and $\alpha < \rho$. This cannot happen in a bipartite graph without isolated vertices, where Kőnig's theorem makes both gaps zero.
- **No weighted version of this form.** With weights, a maximum-weight matching does not extend to a minimum-weight edge cover by the rule of the proof. In the path $abcd$ with weights $w(ab) = 1$, $w(bc) = 10$, $w(cd) = 1$, the maximum-weight matching is $\{bc\}$, which extends to an edge cover of weight 12, while $\{ab, cd\}$ is an edge cover of weight 2. The weighted edge cover problem is still solvable through a minimum-weight perfect matching in an auxiliary graph, as described in Schrijver, Chapter 27.

## History

Tibor Gallai published both identities in 1959, in a paper on extreme sets of points and of edges. They are often taught together with Kőnig's theorem, because in bipartite graphs the four numbers collapse to two.

## References
