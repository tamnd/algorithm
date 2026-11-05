---
tag: FW5F9K
kind: concept
slug: r-division
name: r-division
aliases:
- planar r-division
area: graphs/planar-graphs
level: research
summary: Partition of a planar graph into O(n/r) pieces with O(r) vertices each and O(sqrt r) boundary vertices.
prereqs: [planar-separator-theorem, planar-separator-finding, planar-face]
see_also: [planar-shortest-paths, lipton-tarjan-separator, nested-dissection, distance-oracle, monge-property, planar-embedding, divide-and-conquer-paradigm, treewidth]
sources:
  - paper: doi:10.1137/0216064
    title: Greg N. Frederickson, Fast algorithms for shortest paths in planar graphs, with applications, SIAM Journal on Computing 16(6), 1004 to 1022 (1987)
    locator: the definition of an r-division (suitable r-division), the counting of boundary vertices, and the O(n log n) construction by repeated separators
  - paper: doi:10.1006/jcss.1997.1493
    title: Monika R. Henzinger, Philip Klein, Satish Rao and Sairam Subramanian, Faster shortest-path algorithms for planar graphs, Journal of Computer and System Sciences 55(1), 3 to 23 (1997)
    locator: recursive divisions with several levels of piece sizes and their use in linear-time shortest paths
  - paper: doi:10.1145/2488608.2488672
    title: Philip N. Klein, Shay Mozes and Christian Sommer, Structured recursive separator decompositions for planar graphs in linear time, STOC 2013, 505 to 514
    locator: the definition of r-divisions with few holes and the linear-time construction of recursive r-divisions for all sizes at once
  - paper: doi:10.1137/0136016
    title: Richard J. Lipton and Robert Endre Tarjan, A separator theorem for planar graphs, SIAM Journal on Applied Mathematics 36(2), 177 to 189 (1979)
    locator: the separator theorem with O(n^(1/2)) vertices on which the division is built
---

An r-division of an $n$-vertex [planar graph](/planar-graph/) splits it into $O(n / r)$ pieces, each with $O(r)$ vertices and only $O(\sqrt{r})$ *boundary vertices*, the vertices it shares with other pieces. Frederickson introduced it in 1987 by applying the [planar separator theorem](/planar-separator-theorem/) over and over. It is the standard way to make a planar graph "look small": work inside each piece is cheap because pieces are small, and work between pieces is cheap because the total number of boundary vertices is only $O(n / \sqrt{r})$. Fast [planar shortest path](/planar-shortest-paths/) algorithms, distance oracles, and many dynamic and approximation algorithms for planar graphs are built on r-divisions.

## In plain words

Cut a map into $n / r$ districts of about $r$ towns each, so that every district has only about $\sqrt{r}$ towns on its border.

A square grid shows that this is natural: a block of $r$ cells has a border of length about $4 \sqrt{r}$. The surprise is that every planar network, however irregular, can be cut this well. To find shortest routes, you then only need, for each district, the distances between its few border towns, and you can plan long trips by hopping from border to border.

## The idea

**How the embedding is given.** The graph is given with a planar embedding as a [rotation system](/rotation-system/) $\rho$, where $\rho(v)$ lists the neighbours of $v$ counterclockwise. The embedding is needed to find cycle separators and to speak of the [faces](/planar-face/) of the pieces.

**Definition.** Let $G$ be a planar graph with $n$ vertices and let $1 \le r \le n$. A *division* of $G$ is a collection of subgraphs, the *pieces*, such that every edge belongs to exactly one piece (and every isolated vertex to one piece). A vertex is a *boundary vertex* if it belongs to more than one piece. A division is an *r-division* if

1. there are $O(n / r)$ pieces,
2. each piece has $O(r)$ vertices,
3. each piece has $O(\sqrt{r})$ boundary vertices.

Frederickson's original definition partitions vertices instead of edges, with boundary vertices being those with a neighbour in another region; the two versions are interchangeable up to constants.

**Total boundary.** By 1 and 3, the pieces have $O(n / r) \cdot O(\sqrt{r}) = O(n / \sqrt{r})$ boundary vertices in total, counted with multiplicity. With $r = \log^2 n$, for example, there are only $O(n / \log n)$ boundary vertices.

**Construction by separators.** Apply the [separator theorem](/planar-separator-theorem/) to $G$, which splits it into two parts of at most $2n/3$ vertices each, sharing a separator of $O(\sqrt{n})$ vertices. Recurse on each part until every part has at most $r$ vertices. This gives $O(n / r)$ pieces with $O(n / \sqrt{r})$ boundary vertices in total, by solving the recurrence for the boundary size $B(n) \le B(\alpha n + O(\sqrt{n})) + B((1 - \alpha) n + O(\sqrt{n})) + O(\sqrt{n})$ with $1/3 \le \alpha \le 2/3$. The pieces may still have uneven boundaries, so in a second phase every piece with too many boundary vertices is split again by a separator that balances its boundary vertices instead of its vertices. With an $O(n)$-time separator algorithm such as [Lipton-Tarjan](/lipton-tarjan-separator/) at every node of the recursion, there are $O(\log (n / r))$ levels of $O(n)$ work, so the construction takes $O(n \log (n / r))$ time.

**Holes.** A *hole* of a piece $P$ is a face of $P$ that is not a face of $G$. All boundary vertices of $P$ lie on its holes. An r-division with *few holes* has $O(1)$ holes per piece. Few holes matter because distances between boundary vertices on one hole form a matrix with the [Monge property](/monge-property/), which is what makes searches over boundary vertices fast.

**Recursive r-divisions.** For $r_1 < r_2 < \cdots < r_k$, a recursive r-division is a sequence of $r_i$-divisions in which every piece at level $i$ is the union of pieces at level $i - 1$. Klein, Mozes and Sommer (2013) showed that recursive r-divisions with few holes, for all $r_i$ growing by a constant factor, can be computed together in $O(n)$ time, removing the $\log$ factor of the separator-by-separator construction.

**Dense distance graphs.** The typical use of an r-division replaces each piece by a complete graph on its boundary vertices, with edge lengths the distances inside the piece. This *dense distance graph* has $O(n / \sqrt{r})$ vertices and $O(n / r) \cdot O(r) = O(n)$ edges, and shortest paths in it are the shortest paths of $G$ between boundary vertices.

## Examples

| graph | an r-division | boundary |
|---|---|---|
| a single vertex | one piece, the vertex | none |
| a tree: the path on $n$ vertices | consecutive subpaths of $r$ vertices, each sharing its end vertices with its neighbours | at most 2 per piece, about $2n / r$ in all |
| $K_4$ | for $r \ge 4$, one piece, the whole graph | none |
| the $5 \times 5$ grid, $r = 9$ | four $3 \times 3$ blocks sharing the middle row and column; each shared edge goes to one of its two blocks | each block has 5 boundary vertices, 9 boundary vertices in all |
| the $k \times k$ grid | blocks of $\sqrt{r} \times \sqrt{r}$ vertices | about $4 \sqrt{r}$ per piece, $O(n / \sqrt{r})$ in all, which is optimal up to constants |
| $K_5$, $K_{3,3}$ | not planar; the definition gives no guarantee | for constant size this is harmless, but non-planar families such as expanders have no division with $o(r)$ boundary vertices per piece |

The star $K_{1, n-1}$, another tree, shows that the bound is on boundary vertices per piece, not on how many pieces share one vertex: putting about $r$ leaves in each piece gives $O(n / r)$ pieces, each with one boundary vertex, the centre, which belongs to all of them.

## Where it is used

- **Shortest paths.** Frederickson's $O(n \sqrt{\log n})$ algorithm and the linear-time algorithm of Henzinger, Klein, Rao and Subramanian for [planar shortest paths](/planar-shortest-paths/) run Dijkstra on boundary vertices, using precomputed distances inside pieces.
- **Negative lengths, flows and cuts.** The dense distance graphs of recursive divisions, searched with Monge methods, give near-linear algorithms for negative lengths, max flow and min cut in planar graphs.
- **Distance oracles.** Planar [distance oracles](/distance-oracle/) store boundary-to-boundary distances of an r-division to trade space for query time.
- **Dynamic algorithms.** Updates change one piece, so only that piece and its dense distance graph are recomputed; this gives sublinear update times for dynamic planar shortest paths and connectivity.
- **Linear algebra and numerics.** The same recursive separator structure underlies [nested dissection](/nested-dissection/) for sparse linear systems on planar meshes.
- **Approximation and parameterized algorithms.** Pieces of size $r$ with small boundary allow brute force or dynamic programming inside pieces, as in algorithms based on bounded [treewidth](/treewidth/).

## References
