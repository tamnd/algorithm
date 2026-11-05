---
tag: B70115
kind: algorithm
slug: highway-hierarchies
name: Highway hierarchies
aliases:
- highway hierarchy
area: graphs/shortest-paths
level: advanced
summary: Multilevel preprocessing that selects important road-like edges for fast long-distance queries.
solves: [single-pair-shortest-path]
model: word-ram
complexity:
  vars: {n: the number of vertices, m: the number of edges}
  time: {worst: O(m + n log n), best: Θ(1)}
  space: {extra: Θ(n + m)}
properties: {deterministic: true, recursive: false}
prereqs: [bidirectional-dijkstra, dijkstra, single-pair-shortest-path]
see_also: [contraction-hierarchies, alt-algorithm, hub-labeling, distance-oracle, distance-labeling, shortest-path-tree, bidirectional-dijkstra, single-pair-shortest-path]
sources:
  - paper: doi:10.1007/11561071_51
    title: Peter Sanders and Dominik Schultes, Highway hierarchies hasten exact shortest path queries, ESA 2005, LNCS 3669, 568 to 579
    locator: the whole paper (neighborhoods, the definition of highway edges, construction by local search, contraction to the core, and the multilevel query)
  - paper: doi:10.1007/11841036_71
    title: Peter Sanders and Dominik Schultes, Engineering highway hierarchies, ESA 2006, LNCS 4168, 804 to 816
    locator: the whole paper (the improved construction, distance tables at the top level, and experiments on continental road networks)
  - paper: doi:10.1145/2133803.2330080
    title: Peter Sanders and Dominik Schultes, Engineering highway hierarchies, ACM Journal of Experimental Algorithmics 17 (2012)
    locator: the sections on the definition of the hierarchy, the correctness of the query, and the experiments
  - paper: doi:10.1007/978-3-319-49487-6_2
    title: Hannah Bast, Daniel Delling, Andrew Goldberg, Matthias Müller-Hannemann, Thomas Pajor, Peter Sanders, Dorothea Wagner and Renato F. Werneck, Route planning in transportation networks, in Algorithm Engineering, LNCS 9220, 19 to 80 (2016)
    locator: Section 2, Shortest paths in road networks, the part on hierarchical techniques (highway hierarchies and their successors)
---

Highway hierarchies are a speed-up technique for exact [point-to-point shortest paths](/single-pair-shortest-path/) on road networks, due to Sanders and Schultes (2005). Each vertex gets a small *neighborhood*, its $H$ closest vertices. An edge is a *highway edge* if it lies on a shortest path whose source and target are both far from it: outside the neighborhood of the source, and with its tail outside the neighborhood of the target. The highway edges form a much smaller network, which is then contracted and processed again, giving levels. A query is a [bidirectional Dijkstra](/bidirectional-dijkstra/) search that leaves the lower levels as soon as it is outside the local neighborhoods, so long trips are searched almost only on the top levels. It was the first method to answer exact queries on a continental road network in about a millisecond, and its ideas led to [contraction hierarchies](/contraction-hierarchies/).

## In plain words

When you drive far, you use small streets only near the start and near the end. In between, you stay on main roads.

Highway hierarchies find these main roads from the map alone. Around every place, mark the few nearest places as its local area. A road counts as a highway if some best long trip uses it while already outside the local area of the start and not yet in the local area of the end.

To find a route, search outward from the start and backward from the end at the same time. Inside the local area of the start, any road may be used; once outside, only highways. The same holds near the end. Repeating this idea gives highways of highways, and long trips are found by looking at very few roads.

## The problem

The input is a directed graph $G = (V, E)$ with $n$ vertices and $m$ edges, a weight $w(u, v)$ on each edge, and a neighborhood size $H \ge 1$. Preprocessing builds the hierarchy once. Each query gives $s$ and $t$ and asks for $\operatorname{dist}(s, t)$ and a shortest path.

**Weight assumptions.** Weights are nonnegative real numbers; zero weights and parallel edges are allowed. Neighborhoods, the construction and the query are all Dijkstra searches, so negative weights would make them wrong; the implementation rejects any negative weight, which also rules out negative cycles. If $t$ is not reachable from $s$, the query returns $+\infty$ and no path.

## The algorithm

For a vertex $s$, let $r^\to(s)$ be the distance from $s$ to its $H$-th closest vertex (counting $s$ itself, and $\infty$ if fewer than $H$ vertices are reachable), and $N^\to(s) = \{v : \operatorname{dist}(s, v) \le r^\to(s)\}$ its forward neighborhood. The backward radius $r^\gets(t)$ and neighborhood $N^\gets(t)$ are the same on the reversed graph.

```pseudo id=main
HIGHWAY-QUERY(G, w, H; query s, t)
L1  compute r→(v) and r←(v) for every v by local Dijkstra searches
L2  mark (u, v) a highway edge if some shortest s-t path uses it with v ∉ N→(s) and u ∉ N←(t)
L3  forward Dijkstra from s, backward Dijkstra from t on reversed edges
L4      a side scanning u relaxes all its edges if its label is within its root's radius, else only highway edges
L5      at each scanned vertex u: μ ← min(μ, d→[u] + d←[u])
L6      stop when both least keys are ≥ μ
L7  return μ and the path through the best meeting vertex (∞ if none)
```

Lines L1 and L2 build one level, the *highway network*. Line L2 is stated as the definition; Sanders and Schultes compute it without all-pairs distances, by a local search from each vertex that grows a partial shortest-path tree only until all its branches have left the neighborhood, which takes time near linear on road networks. The full method then *contracts* the highway network: vertices of small degree are bypassed by shortcuts, and the remaining *core* is the graph of the next level, on which neighborhoods and highways are computed again. The full query moves up a level whenever it leaves a neighborhood of the current level, and it uses a table of distances at the top. The implementation here builds one level exactly from the definition and runs the two-level query of lines L3 to L7, which already shows the key property.

**The key property.** Along a shortest path from $s$, distances from $s$ only grow, so the path's vertices in $N^\to(s)$ form a prefix; similarly, its vertices in $N^\gets(t)$ form a suffix. Every edge between the two parts, whose head has left $N^\to(s)$ and whose tail has not entered $N^\gets(t)$, is a highway edge by definition. So each shortest path is local near $s$, highway in the middle, and local near $t$, and line L4 allows exactly that.

## Example

A main road $m_0, \ldots, m_6$ has segments of 2 km, and each $m_i$ has a driveway to a house $\ell_i$ of 1 km; all edges go both ways. Take $H = 3$.

**Neighborhoods.** For a road vertex $m_i$, the three closest vertices are $m_i$ (0), $\ell_i$ (1) and a road neighbor (2), so $r = 2$. For a house $\ell_i$, they are $\ell_i$ (0), $m_i$ (1) and a road neighbor of $m_i$ (3), so $r = 3$.

**Highway edges.** The road segments $m_1 - m_2$, $m_2 - m_3$, $m_3 - m_4$ and $m_4 - m_5$, in both directions, are highway edges: for example $m_1 \to m_2$ is on the shortest path from $\ell_0$ to $m_3$, with $\operatorname{dist}(\ell_0, m_2) = 5 > 3$ and $\operatorname{dist}(m_1, m_3) = 4 > 2$. The driveways are not: a shortest path enters $\ell_i$ only as its target, and then the tail $m_i$ is at distance 1, inside $N^\gets(\ell_i)$. The end segment $m_0 \to m_1$ is not either: a shortest path through it starts at $m_0$ or $\ell_0$, and $m_1$ is inside both neighborhoods. So 8 of the 26 directed edges are highway edges.

**Query $\ell_0$ to $\ell_6$.** The forward search uses all edges at $\ell_0$, $m_0$, $m_1$ (labels 0, 1, 3, within the radius 3), but from $m_2$ on only highway edges, so it never enters the driveways $\ell_2, \ell_3, \ldots$. The backward search behaves the same way from $\ell_6$. The answer is 14 along $\ell_0, m_0, m_1, \ldots, m_6, \ell_6$. The implementation scans 16 vertices; the same bidirectional search without the restriction scans 26.

**Unreachable target.** In the graph $0 \to 1 \to 2$, $3 \to 0$, nothing reaches 3. For the query from 0 to 3 the backward search from 3 has no edges, no vertex is scanned by both sides, and the query returns $\infty$, for every $H$.

## Correctness

**Theorem.** If all weights are nonnegative, the two-level query returns $\operatorname{dist}(s, t)$ for every $s, t$, and when it is finite, a walk of that weight (a simple path when all weights are positive).

Each side is Dijkstra's algorithm on a fixed subgraph: for the forward side, all edges out of $N^\to(s)$ plus all highway edges. A label within the radius certifies membership in $N^\to(s)$, because the shortest path from $s$ to a vertex of $N^\to(s)$ stays in $N^\to(s)$, where all edges are allowed. By the key property, a shortest $s$-$t$ path $P$ lies in the forward subgraph up to its first vertex $z$ in $N^\gets(t)$ (or $t$), and in the backward subgraph from $z$ on. So $d^\to(z) + d^\gets(z) \le w(P)$, both searches reach $z$ before their keys pass $\mu$, and the stopping rule of bidirectional Dijkstra gives $\mu = \operatorname{dist}(s, t)$. Every value of $\mu$ is the weight of a real path, so it never undershoots, and if there is no path the query returns $\infty$. The full proof is in the proof file below. For the multilevel version, Sanders and Schultes prove the same with shortcuts and level changes.

## Complexity

The model is the [word RAM](/word-ram/).

- **Query, worst case.** Each side is Dijkstra on a subgraph of $G$, so $O(m + n \log n)$ with a Fibonacci heap, no worse than bidirectional Dijkstra.
- **Query, best case.** When $s = t$ the query answers at once, $\Theta(1)$.
- **In practice.** With several levels and contraction, a query on the road network of Western Europe (about 18 million vertices) scans about a thousand vertices and takes about a millisecond, according to Sanders and Schultes; the top-level distance table makes it faster still.
- **Preprocessing.** The local construction with contraction takes minutes to hours for a continent and space linear in the graph. The implementation here tests the definition with all-pairs distances, $O(n^2 m)$ time, meant for checking.
- **Space.** Radii, highway marks and shortcuts take $\Theta(n + m)$ per level, and the levels shrink geometrically on road networks.

## Properties

- **Exact.** The answer is the true distance for every $H$; $H$ only trades preprocessing and query time.
- **Graph-only.** No coordinates are needed; the hierarchy comes from shortest paths.
- **Local-global split.** Every shortest path is local at its ends and uses only highway edges in the middle.
- **Monotone in $H$.** With $H \ge n$, every vertex's neighborhood is everything, and the query is plain bidirectional Dijkstra.
- **Directed graphs.** Forward and backward neighborhoods are separate, so one-way streets are handled.
- **Fixed weights.** A weight change can change neighborhoods and highways; the hierarchy must be rebuilt, at least locally.

## Variants and improvements

- **Contraction to the core.** After selecting highways, bypass vertices of small degree with shortcuts; the shrinking core is the next level. Taken to the extreme, one vertex per level, this became [contraction hierarchies](/contraction-hierarchies/).
- **Distance tables.** Stop the hierarchy at a small top level and store all distances between its vertices; queries meet in the table.
- **Highway-node routing.** Sanders and Schultes later replaced edge levels by vertex levels, which supports fast updates.
- **Transit-node routing.** Long trips pass through a few access nodes per region; precomputed tables answer them in microseconds, with highway hierarchies or contraction as the basis.
- **Goal direction.** Combining with [ALT](/alt-algorithm/) landmarks speeds up the query further.

## When to use it

Highway hierarchies suit large road networks with fixed weights and many queries. Today [contraction hierarchies](/contraction-hierarchies/) are usually preferred, being simpler and faster with less space, and [hub labeling](/hub-labeling/) when queries must be faster still. The highway idea remains useful to explain why road networks have small search spaces, and it underlies transit-node routing.

## Pitfalls

- **Wrong neighborhood test.** Membership in $N^\to(s)$ is decided by the label at scan time; this is exact only because all edges inside the neighborhood are allowed. Restricting edges inside the neighborhood breaks it.
- **Mixing directions.** The backward search must use backward neighborhoods and the reversed edges; forward radii give wrong answers on one-way streets.
- **Tie handling in the definition.** Ties between shortest paths must be handled consistently: either mark an edge when *some* shortest path qualifies, as here, or fix canonical shortest paths in both construction and proof.
- **Stopping at the first meeting.** As with bidirectional Dijkstra, the search must continue until both least keys reach $\mu$.

## Implementations

The Python version computes radii and highway edges of one level from all-pairs distances, by the definition, and answers queries with the restricted bidirectional search, returning the distance, a path and the number of scans.

## History

Sanders and Schultes introduced highway hierarchies at ESA 2005 and engineered them at ESA 2006, with a journal version in 2012; they were among the methods that reached millisecond queries on continental networks during the DIMACS Implementation Challenge on shortest paths (2006). Their contraction step was the seed of contraction hierarchies (2008), which largely replaced them.

## References
