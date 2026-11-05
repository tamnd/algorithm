---
tag: 0Z0K9X
kind: concept
slug: outerplanar-graph
name: Outerplanar graph
aliases:
- outerplanar
area: graphs/planar-graphs
level: core
summary: A planar graph with an embedding where all vertices lie on the outer face.
prereqs: [planar-graph, planar-face]
see_also: [maximal-planar-graph, planar-edge-bound, book-embedding, treewidth, polygon-triangulation, wagner-theorem, kuratowski-theorem, planarity-testing]
sources:
  - paper: "Gary Chartrand and Frank Harary, Planar permutation graphs, Annales de l'Institut Henri Poincaré, Section B 3, 433 to 438 (1967)"
    locator: the characterization of outerplanar graphs by forbidden subdivisions of K4 and K2,3
  - book: isbn:9780130144003
    title: Douglas B. West, Introduction to Graph Theory, second edition, Prentice Hall, 2001
    locator: Chapter 6, Planar graphs (outerplanar graphs in Section 6.1 and the exercises of Sections 6.1 and 6.2)
  - paper: "Sandra L. Mitchell, Linear algorithms to recognize outerplanar and maximal outerplanar graphs, Information Processing Letters 9(5), 229 to 232 (1979)"
    locator: the whole paper
  - paper: "Steve Fisk, A short proof of Chvátal's watchman theorem, Journal of Combinatorial Theory, Series B 24(3), 374 (1978)"
    locator: the whole note (3-coloring a triangulated polygon)
---

An outerplanar graph is a [graph](/graph/) that has a [planar](/planar-graph/) drawing in which every vertex lies on the boundary of the outer [face](/planar-face/). Equivalently, its vertices can be put on a circle and its edges drawn inside the circle with no crossings. A graph is outerplanar if and only if it has no $K_4$ and no $K_{2,3}$ [minor](/graph-minor/), and if and only if adding one new vertex joined to all vertices gives a planar graph. Outerplanar graphs have at most $2n - 3$ edges, a vertex of degree at most 2, and [treewidth](/treewidth/) at most 2.

## In plain words

Put all the points of a graph on a circle. Draw each line as a straight chord inside the circle. If you can order the points around the circle so that no two chords cross, the graph is outerplanar.

Triangles, cycles, trees and polygons cut into triangles by non-crossing diagonals are all outerplanar. The complete graph on four points is planar but not outerplanar: one of its points is always hidden inside the triangle of the other three. Outerplanar graphs are simple enough that many hard problems become easy on them, because they can be taken apart one small piece at a time.

## The idea

**Definition.** A graph $G$ is *outerplanar* if it has a planar embedding in which every vertex lies on the boundary of the outer face. Such an embedding is an *outerplane* embedding. By an arc deformation, an outerplanar graph can be drawn with its vertices on a circle in the order in which the outer face walk meets them, and its edges as chords, with no two chords crossing.

**The apex criterion.** Let $G^+$ be $G$ plus one new vertex $a$ adjacent to every vertex of $G$. Then

$$G \text{ is outerplanar} \iff G^+ \text{ is planar}.$$

*Proof.* If $G$ is outerplane, put $a$ in the outer face and join it to every vertex: each vertex is on the boundary of that face, and the arcs can be drawn without crossings, like spokes to points on a circle. Conversely, let $G^+$ be plane. Remove $a$. The faces around $a$ merge into one face, and every neighbour of $a$, which is every vertex of $G$, lies on its boundary. Make that face the outer face. $\square$

**Forbidden minors (Chartrand and Harary, 1967).** $G$ is outerplanar if and only if $G$ contains no subdivision of $K_4$ or $K_{2,3}$, if and only if $G$ has no $K_4$ or $K_{2,3}$ minor. One direction follows from the apex criterion: $K_4^+ = K_5$, and $K_{2,3}^+$ contains $K_{3,3}$ (the apex joins the side of size 2), so neither is outerplanar, and outerplanarity is closed under subgraphs and contractions. The other direction is the analogue of [Kuratowski's theorem](/kuratowski-theorem/) and is proved from it with the apex criterion.

**Edge bound.** If $n \ge 2$, then $m \le 2n - 3$. *Proof.* $G^+$ is simple and planar with $n + 1 \ge 3$ vertices and $m + n$ edges, so by the [planar edge bound](/planar-edge-bound/), $m + n \le 3(n + 1) - 6$, which is $m \le 2n - 3$. $\square$

**Maximal outerplanar graphs.** An outerplanar graph to which no edge can be added is *maximal outerplanar*. For $n \ge 3$, such a graph is a polygon triangulation: the outer face is bounded by a Hamiltonian cycle, all other faces are triangles, and $m = 2n - 3$ (the cycle has $n$ edges and a triangulation of an $n$-gon has $n - 3$ diagonals). Its *weak dual*, the [planar dual](/planar-dual-graph/) without the vertex of the outer face, is a [tree](/tree/) with $n - 2$ nodes.

**A vertex of degree at most 2.** Every outerplanar graph with $n \ge 1$ has a vertex of degree at most 2. *Proof.* For $n \le 3$ this is clear. For $n \ge 4$, add edges to reach a maximal outerplanar graph $H$ on the same vertices; degrees only grow. The weak dual of $H$ is a tree with $n - 2 \ge 2$ nodes, so it has a leaf, a triangle $xyz$ with only one edge, say $xz$, shared with another triangle. The other two edges $xy$ and $yz$ are on the outer cycle, so $y$ has degree 2 in $H$, and at most 2 in $G$. $\square$

So outerplanar graphs are 2-[degenerate](/degeneracy/), hence 3-colorable by [greedy coloring](/greedy-coloring/) in reverse degeneracy order. Fisk used the 3-coloring of a triangulated polygon to prove the art gallery theorem: $\lfloor n/3 \rfloor$ guards always suffice for a simple polygon with $n$ corners.

**More structure.**

- Treewidth at most 2: removing a degree-2 vertex and joining its two neighbours keeps the graph outerplanar, which gives an elimination order with at most 2 later neighbours per vertex.
- A 2-connected outerplanar graph has exactly one Hamiltonian cycle, the boundary of its outer face.
- Outerplanar graphs are exactly the graphs with a [book embedding](/book-embedding/) in one page: the vertices on the spine in the circle order and all edges on one side.

## Examples

Each row below was checked with the apex criterion, by testing $G^+$ for planarity.

| graph | $n$ | $m$ | $2n - 3$ | outerplanar? | reason |
|---|---|---|---|---|---|
| a single vertex | 1 | 0 | | yes | |
| any tree | $n$ | $n - 1$ | $2n - 3$ | yes | draw it on a circle in DFS order |
| the cycle $C_n$ | $n$ | $n$ | $2n - 3$ | yes | the cycle is the circle |
| $K_4 - e$ (two triangles on an edge) | 4 | 5 | 5 | yes | a square with one diagonal; maximal outerplanar |
| the fan: a path of 4 vertices and a hub | 5 | 7 | 7 | yes | the hub first, then the path, around the circle |
| $C_5$ with the chords $02$ and $03$ | 5 | 7 | 7 | yes | a triangulated pentagon |
| $K_4$ | 4 | 6 | 5 | no | $K_4^+ = K_5$, and $6 > 5$ |
| $K_{2,3}$ | 5 | 6 | 7 | no | $K_{2,3}^+ \supseteq K_{3,3}$, though $6 \le 7$ |

The last row shows that the edge bound is not sufficient: $K_{2,3}$ has few edges but is not outerplanar, because in every planar drawing one of its three degree-2 vertices is enclosed by the cycle through the other two.

**$K_4$ and $K_{2,3}$ as embeddings.** $K_4$ has one embedding with four triangular faces, and each vertex misses one face, so no face holds all four. $K_{2,3}$ has one embedding up to symmetry, with three faces of length 4, each missing one of the three vertices of degree 2.

## Where it is used

- **Easy cases of hard problems.** [Maximum independent set](/maximum-independent-set/), [dominating set](/dominating-set/), [Hamiltonian cycle](/hamiltonian-cycle/) and many others are solvable in linear time on outerplanar graphs by dynamic programming over the weak dual tree or a [tree decomposition](/tree-decomposition/) of width 2.
- **[Baker's technique](/baker-planar-ptas/).** A planar graph is $k$-outerplanar when removing the outer face vertices $k$ times empties it. Baker's approximation schemes cut a planar graph into $k$-outerplanar pieces and solve each exactly.
- **Polygon triangulation.** A [polygon triangulation](/polygon-triangulation/) is a maximal outerplanar graph, and the art gallery theorem uses its 3-coloring.
- **Book embedding and layouts.** One-page [book embeddings](/book-embedding/) and circular layouts of networks are outerplanar drawings.
- **RNA secondary structure.** A secondary structure without pseudoknots, drawn with the backbone on a circle, is an outerplanar graph.
- **Recognition.** Outerplanarity is tested in linear time, directly (Mitchell, 1979) or by a [planarity test](/planarity-testing/) on $G^+$.

## References
