---
tag: 3FNQQN
kind: problem
slug: minimum-edge-cover
name: Minimum edge cover
aliases:
- minimum cardinality edge cover
area: graphs/matching
level: core
summary: Find an edge cover with the fewest edges; solvable from a maximum matching by Gallai's identity.
model: word-ram
complexity:
  vars: {n: the number of vertices, m: the number of edges}
  time: {worst: O(m n^(1/2))}
prereqs: [edge-cover, maximum-matching]
see_also: [gallai-identity, maximal-matching, konig-theorem, bipartite-maximum-independent-set, vertex-cover, edmonds-blossom, hopcroft-karp, minimum-weight-perfect-matching]
sources:
  - book: isbn:9780130144003
    title: Douglas B. West, Introduction to Graph Theory, second edition
    locator: Section 3.1, Matchings and covers (Gallai's lemma that the edge cover number plus the matching number is n, and the bipartite corollary)
  - book: isbn:9783540443896
    title: Alexander Schrijver, Combinatorial Optimization, Polyhedra and Efficiency, Springer
    locator: Chapter 19, Bipartite edge cover and stable set, and Chapter 27, Nonbipartite edge cover (Gallai's theorem, the weighted problem and its polytope)
  - book: isbn:9783662560389
    title: Bernhard Korte and Jens Vygen, Combinatorial Optimization, Theory and Algorithms, sixth edition, Springer
    locator: Chapter 10, Maximum Matchings (Gallai's theorem on edge covers)
  - paper: "Tibor Gallai, Über extreme Punkt- und Kantenmengen, Annales Universitatis Scientiarum Budapestinensis de Rolando Eötvös Nominatae, Sectio Mathematica 2, 133 to 138 (1959)"
    locator: the whole paper (the identities between matching, edge cover, vertex cover and independence numbers)
---

The minimum edge cover problem asks for the fewest edges of a graph such that each vertex is an end of at least one of them. An [edge cover](/edge-cover/) exists exactly when the graph has no isolated vertex. The problem reduces to [maximum matching](/maximum-matching/): by [Gallai's identity](/gallai-identity/), the least size of an edge cover is $n - \nu(G)$, and a maximum matching plus one edge for each exposed vertex is an optimal cover. So it is solved in $O(m \sqrt n)$ time on general graphs.

## In plain words

You must place guards on the corridors of a building so that each room opens onto at least one guarded corridor. A guard on a corridor watches both rooms at its ends. You want as few guards as possible.

The best plan uses as many corridors as possible that each cover two new rooms. Such corridors must not share a room, so they form a matching. So first take the largest set of corridors with no shared room. Every room not yet watched then needs one more corridor of its own, and any corridor at that room will do. The total is the number of rooms minus the size of the largest matching.

## Definition

Let $G = (V, E)$ be a finite undirected graph, without weights, bipartite or general, with $n = |V|$. An *edge cover* is a set $F \subseteq E$ such that each vertex of $V$ is an end of some edge of $F$. A self-loop at $v$ covers $v$; it is never needed when $v$ has another edge.

- **Input:** $G$.
- **Output:** an edge cover $F$ of least size, or "none" if $G$ has an isolated vertex.

The least size is the *edge cover number* $\rho(G)$. For the graph with no vertices, $\rho = 0$, with the empty cover.

**Gallai's identity.** If $G$ has no isolated vertex and no self-loop, then $\rho(G) + \nu(G) = n$, where $\nu(G)$ is the size of a maximum matching.

*Proof.* ($\rho \le n - \nu$.) Let $M$ be a maximum matching. It covers $2\nu$ vertices. For each of the $n - 2\nu$ exposed vertices, add one edge at it; such an edge exists, as no vertex is isolated. The result is an edge cover with at most $\nu + (n - 2\nu) = n - \nu$ edges.

($\nu \ge n - \rho$.) Let $F$ be a minimum edge cover. No edge $uv \in F$ has both ends covered by other edges of $F$, or $F \setminus \{uv\}$ would be a smaller cover. So $F$ has no cycle and no path with three edges, since the middle edge of such a path, or any edge of such a cycle, could be removed. So each connected component of the graph $(V, F)$ is a star with at least one edge. A forest on $n$ vertices with $|F|$ edges has $n - |F|$ components. Taking one edge from each star gives a matching with $n - |F| = n - \rho$ edges. $\square$

## Variants

- **Bipartite graphs.** By [Kőnig's theorem](/konig-theorem/), $\nu = \tau$, and the complement of a vertex cover is an independent set, so $\rho(G) = \alpha(G)$, the size of a [maximum independent set](/bipartite-maximum-independent-set/), when $G$ is bipartite with no isolated vertex. This is the edge form of Kőnig's theorem.
- **Weighted.** Each edge has a weight, and the cover must have least total weight. It is solvable in polynomial time by a reduction to [minimum-weight perfect matching](/minimum-weight-perfect-matching/) on a graph made of two copies of $G$; see Schrijver, Chapter 27.
- **Decision.** Given $k$, is $\rho(G) \le k$? Same cost as the search problem.
- **Covering vertices by vertices.** The [vertex cover](/vertex-cover/) problem, where vertices must cover the edges, is NP-hard. Edge cover is the dual pair of covering problems that is easy.
- **Edge dominating set.** Each *edge* must share an end with a chosen edge. This is NP-hard; its optimum equals the least size of a [maximal matching](/maximal-matching/).

## Examples

| graph | $n$ | $\nu$ | $\rho = n - \nu$ | a minimum edge cover |
|---|---|---|---|---|
| no vertices | 0 | 0 | 0 | $\emptyset$ |
| one isolated vertex | 1 | 0 | none | no cover exists |
| one edge $ab$ | 2 | 1 | 1 | $\{ab\}$ |
| triangle $abc$ | 3 | 1 | 2 | $\{ab, bc\}$ |
| path $a - b - c - d - e$ | 5 | 2 | 3 | $\{ab, bc, de\}$ |
| star $K_{1,r}$ | $r + 1$ | 1 | $r$ | all edges |
| Petersen graph | 10 | 5 | 5 | a perfect matching |

**The construction on a path.** On $a - b - c - d - e$, take the maximum matching $\{ab, cd\}$. Only $e$ is exposed, so add $de$. The cover $\{ab, cd, de\}$ has $3 = 5 - 2$ edges. The star components are $\{ab\}$ and the star $\{cd, de\}$ with center $d$.

**A graph with no perfect matching.** In the triangle $abc$ with pendant edges $ad$ and $ce$, $n = 5$ and $\nu = 2$, as $G - a$ has two odd components. So $\rho = 3$, for example $\{ab, ad, ce\}$.

**A cover from a matching that is only maximal is not optimal.** On the path $a - b - c - d$, the [maximal matching](/maximal-matching/) $\{bc\}$ plus one edge at $a$ and at $d$ gives $\{ab, bc, cd\}$, with 3 edges, while $\{ab, cd\}$ has 2.

## Known algorithms

The algorithm is: find a maximum matching $M$, then for each exposed vertex add any edge at it. The second step takes $O(n + m)$ time. So the cost is that of maximum matching.

| matching algorithm | graphs | total time |
|---|---|---|
| [Micali-Vazirani](/micali-vazirani-algorithm/) | general | $O(m \sqrt n)$ |
| [Edmonds' blossom algorithm](/edmonds-blossom/) | general | $O(n^3)$ with Gabow's implementation |
| [Hopcroft-Karp](/hopcroft-karp/) | bipartite | $O(m \sqrt n)$ |
| [Kuhn's algorithm](/kuhn-algorithm/) | bipartite | $O(nm)$ |

## Bounds

The upper bound is $O(m \sqrt n)$ in the worst case on the [word RAM](/word-ram/), from maximum matching. The two problems are equivalent up to $O(n + m)$ time in both directions: from a minimum edge cover $F$, one edge from each star of $(V, F)$ gives a maximum matching, by the second half of the proof. So any bound for one is a bound for the other. The trivial lower bound is $\Omega(n + m)$.

## Reductions

- **To maximum matching:** as above, in $O(n + m)$ extra time.
- **From maximum matching:** from a minimum edge cover, keep one edge per star component. This needs no isolated vertices; for a graph with isolated vertices, delete them first, as they do not change $\nu$.
- **Weighted to perfect matching:** the weighted edge cover problem reduces to minimum-weight perfect matching, so the [Hungarian algorithm](/hungarian-algorithm/) solves the bipartite case and [Edmonds' algorithm](/edmonds-blossom/) the general case.

## Applications

- **Sensor and guard placement.** Each sensor watches the two ends of a link, and each node must be watched.
- **Pairing with no one left out.** Each person must be in at least one pair, and pairs may share a person when needed. The construction shows that a minimum solution has as many disjoint pairs as possible and one extra pair for each person left over.
- **Bipartite independent sets.** By Kőnig and Gallai together, $\alpha(G) = \rho(G) = n - \nu(G)$ for bipartite graphs without isolated vertices. This gives the largest set of pairwise non-conflicting items in such graphs.

## References
