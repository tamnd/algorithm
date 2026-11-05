---
tag: 82PBYC
kind: concept
slug: eccentricity
name: Eccentricity
aliases:
- vertex eccentricity
area: graphs/tree-algorithms
level: intro
summary: The greatest distance from a vertex to any other vertex.
prereqs: [shortest-path, breadth-first-search, tree]
see_also: [tree-diameter, tree-diameter-double-sweep, tree-center, centroid, all-pairs-shortest-paths, k-center-problem, network-diameter-estimation, rerooting-technique]
sources:
  - book: isbn:9780130144003
    title: Douglas B. West, Introduction to Graph Theory, second edition, Prentice Hall, 2001
    locator: Section 2.1 (Basic properties of trees), the definitions of distance, eccentricity, radius, diameter and center, and Jordan's theorem that the center of a tree is a vertex or an edge
  - book: isbn:9780201027877
    title: Frank Harary, Graph Theory, Addison-Wesley, 1969
    locator: Chapter 4 (Trees), the eccentricity of a vertex, the radius and the center of a tree
  - url: https://cses.fi/book/book.pdf
    title: Antti Laaksonen, Competitive Programmer's Handbook
    locator: Chapter 14 (Tree algorithms), Section 14.2 (Diameter) and Section 14.3 (All longest paths), the maximum distance from every node in O(n) time
  - paper: "Camille Jordan, Sur les assemblages de lignes, Journal fur die reine und angewandte Mathematik 70 (1869), 185-190"
    locator: the center of a tree as one vertex or two adjacent vertices
---

The eccentricity of a vertex $v$ in a connected graph is the largest distance from $v$ to any vertex: $ecc(v) = \max_u d(v, u)$. It measures how far the worst-placed vertex is from $v$. The smallest eccentricity is the *radius* of the graph, the largest is the *diameter*, and the vertices of least eccentricity form the *center*. In a general graph every eccentricity takes a [shortest-path](/shortest-path/) search from that vertex, but in a tree all $n$ eccentricities come from two searches, because $ecc(v)$ is the larger of the distances from $v$ to the two ends of any longest path.

## In plain words

Pick a town on a road map. Look at all the other towns and find the one that is farthest away by road. That distance is the eccentricity of your town. A town in the middle of the map has a small one, and a town at the edge has a large one.

The town with the smallest such distance is the best place for something that must reach everyone fast, like a fire station. The largest such distance over all towns is the longest trip on the map. When the roads have no loops, there is a short cut: find the two towns that are farthest apart, and then the farthest town from any place is one of those two.

## The idea

**Definitions.** Let $G = (V, E)$ be a connected undirected graph, unweighted or with non-negative edge weights, and let $d(u, v)$ be the length of a shortest path between $u$ and $v$. For $v \in V$,
$$ecc(v) = \max_{u \in V} d(v, u).$$
Then $rad(G) = \min_v ecc(v)$ is the *radius*, $diam(G) = \max_v ecc(v)$ is the *diameter*, the *center* is $\{v : ecc(v) = rad(G)\}$, and the *periphery* is $\{v : ecc(v) = diam(G)\}$. If $G$ is not connected, every eccentricity is $\infty$. For a directed graph one uses the out-eccentricity $\max_u d(v, u)$ along directed paths.

**Basic facts in any connected graph.**

- $rad(G) \le diam(G) \le 2\, rad(G)$: for $x, y$ and a center vertex $c$, $d(x, y) \le d(x, c) + d(c, y) \le 2\, rad(G)$.
- If $uv$ is an edge of weight $w$, then $|ecc(u) - ecc(v)| \le w$, by the triangle inequality. In an unweighted graph, eccentricities of neighbors differ by at most 1.
- Computing all eccentricities is an [all-pairs shortest paths](/all-pairs-shortest-paths/) problem: $n$ runs of [BFS](/breadth-first-search/), $O(nm)$ time, for an unweighted graph.

**Trees: two ends of a diameter are enough.** Let $T$ be a tree with non-negative edge weights, and let $a, b$ be the ends of a longest path $P$, so $d(a, b) = diam(T)$. Then for every vertex $v$,
$$ecc(v) = \max(d(v, a), d(v, b)).$$

*Proof.* The right side is at most $ecc(v)$. For the other direction, let $x$ be any vertex. For a vertex $y$ let $q(y)$ be the vertex of $P$ closest to $y$; the path from $y$ to any vertex of $P$ passes through $q(y)$. Since $d(x, a) = d(x, q(x)) + d(q(x), a) \le d(a, b) = d(a, q(x)) + d(q(x), b)$, we get $d(x, q(x)) \le d(q(x), b)$, and in the same way $d(x, q(x)) \le d(q(x), a)$. Suppose first that $q(x)$ is not closer to $a$ than $q(v)$ is, that is, $q(x)$ lies on the part of $P$ from $q(v)$ to $b$. The path from $v$ to $x$ goes through $q(v)$ and $q(x)$, so
$$d(v, x) = d(v, q(v)) + d(q(v), q(x)) + d(q(x), x) \le d(v, q(v)) + d(q(v), q(x)) + d(q(x), b) = d(v, b).$$
(If $q(x) = q(v)$, the first equality becomes $\le$, and the bound still holds.) If $q(x)$ lies between $a$ and $q(v)$, the same argument gives $d(v, x) \le d(v, a)$. So every $x$ is within $\max(d(v, a), d(v, b))$ of $v$. $\square$

So three searches give every eccentricity of a tree in $O(n)$ time: a search from any vertex finds a farthest vertex $a$, which is an end of a longest path (this is the [double sweep](/tree-diameter-double-sweep/)); a search from $a$ finds $b$ and all $d(\cdot, a)$; a search from $b$ gives all $d(\cdot, b)$. In a tree a [BFS](/breadth-first-search/), or an iterative DFS that adds weights, finds the distances because each path is unique.

**Center of a tree.** In an unweighted tree, the center is the middle vertex of any longest path, or the two middle vertices, so it is one vertex or two adjacent vertices (Jordan, 1869), and $diam(T) \in \{2\, rad(T) - 1, 2\, rad(T)\}$. The [tree center](/tree-center/) page gives the methods, including [leaf peeling](/tree-center-leaf-peeling/).

## Examples

The trees have vertices $0, \ldots, n-1$, are unrooted and unweighted, and $d$ counts edges.

**The 12-vertex tree** with the parent array $[-, 0, 1, 2, 3, 4, 2, 6, 0, 8, 3, 7]$ with respect to vertex 0:

```
0
├── 1
│   └── 2
│       ├── 3
│       │   ├── 4
│       │   │   └── 5
│       │   └── 10
│       └── 6
│           └── 7
│               └── 11
└── 8
    └── 9
```

A BFS from 0 reaches distance 5 at the vertices 5 and 11; take $a = 5$. A BFS from 5 reaches distance 7 at 9; take $b = 9$. The longest path is $5, 4, 3, 2, 1, 0, 8, 9$, so $diam = 7$.

| $v$ | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| $d(v, 5)$ | 5 | 4 | 3 | 2 | 1 | 0 | 4 | 5 | 6 | 7 | 3 | 6 |
| $d(v, 9)$ | 2 | 3 | 4 | 5 | 6 | 7 | 5 | 6 | 1 | 0 | 6 | 7 |
| $ecc(v)$ | 5 | 4 | 4 | 5 | 6 | 7 | 5 | 6 | 6 | 7 | 6 | 7 |

Each $ecc(v)$ in the last row is the maximum of the two rows above it, and a BFS from every vertex gives the same row. The radius is 4, the center is $\{1, 2\}$, the two middle vertices of the longest path, and $7 = 2 \cdot 4 - 1$. The periphery is $\{5, 9, 11\}$. Vertex 11 is a third end of a longest path: $d(11, 9) = 7$ as well.

Small shapes:

- **One vertex.** $ecc(0) = 0$, so the radius and the diameter are 0 and the center is $\{0\}$.
- **A path** $0 - 1 - \cdots - (n-1)$. $ecc(v) = \max(v, n - 1 - v)$. The diameter is $n - 1$, the radius is $\lceil (n-1)/2 \rceil$, and the center is the middle vertex for odd $n$ and the two middle vertices for even $n$.
- **A star** with center 0 and $n - 1 \ge 2$ leaves. $ecc(0) = 1$ and $ecc(v) = 2$ for each leaf, so the radius is 1, the diameter is 2, and the center is $\{0\}$.
- **A cycle** $C_n$, not a tree: every vertex has eccentricity $\lfloor n/2 \rfloor$, so the center is the whole graph. In a graph with cycles, the two ends of a longest shortest path do not give all eccentricities: in $C_4$ with $a = 0$ and $b = 2$, vertex 1 has distance 1 to both, but $ecc(1) = 2$.

## Where it is used

- **Center and facility location.** The vertex of least eccentricity is the best site for one emergency service that must reach every vertex within the least time; this is the 1-center problem, the case $k = 1$ of the [k-center problem](/k-center-problem/). The [tree center](/tree-center/) solves it on trees in $O(n)$ time.
- **Diameter and radius.** The [tree diameter](/tree-diameter/) is the largest eccentricity. For large graphs, the [estimation of the diameter](/network-diameter-estimation/) runs BFS from a few vertices and uses $ecc(v) \le diam \le 2\, ecc(v)$ as bounds.
- **All farthest distances in a tree.** "For each vertex, the distance to the farthest vertex" is a standard exercise for the [rerooting technique](/rerooting-technique/); the two-ends formula above solves it with three searches and no rerooting.
- **Centrality.** Eccentricity gives the *eccentricity centrality* $1/ecc(v)$, a cousin of [closeness centrality](/closeness-centrality/), which uses the sum of the distances instead of the maximum. The vertex of least total distance in a tree is the [centroid](/centroid/), which can differ from the center.
- **Networks.** In a communication network, $ecc(v)$ bounds the number of rounds that a broadcast from $v$ needs, and the radius bounds the fastest broadcast from a single source.

## References
