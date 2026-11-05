---
tag: Y44D0J
kind: problem
slug: planar-straight-line-drawing
name: Planar straight-line drawing
aliases:
- straight-line planar embedding
- planar graph drawing
area: graphs/planar-graphs
level: advanced
summary: Produce a crossing-free drawing of a planar graph with straight edges, often on a small grid.
model: word-ram
complexity:
  vars: {n: the number of vertices}
  time: {worst: O(n)}
  space: {extra: O(n)}
prereqs: [planar-graph, planar-embedding, maximal-planar-graph]
see_also: [schnyder-drawing, de-fraysseix-pach-pollack, tutte-spring-theorem, schnyder-woods, canonical-ordering, graph-drawing, crossing-number, planarity-testing]
sources:
  - paper: "István Fáry, On straight line representation of planar graphs, Acta Scientiarum Mathematicarum (Szeged) 11, 229 to 233 (1948)"
    locator: the theorem that every planar graph has a straight-line planar drawing, proved by induction on triangulations
  - paper: doi:10.1007/BF02122694
    title: Hubert de Fraysseix, János Pach and Richard Pollack, How to draw a planar graph on a grid, Combinatorica 10(1), 41 to 51 (1990)
    locator: the canonical ordering, the shift method on the (2n-4) by (n-2) grid, and the lower bound for nested triangles
  - paper: "Walter Schnyder, Embedding planar graphs on the grid, Proceedings of the First Annual ACM-SIAM Symposium on Discrete Algorithms (SODA 1990), 138 to 148"
    locator: the linear-time drawing on the (n-2) by (n-2) grid
  - paper: doi:10.1112/plms/s3-13.1.743
    title: W. T. Tutte, How to draw a graph, Proceedings of the London Mathematical Society s3-13(1), 743 to 767 (1963)
    locator: the barycentric drawing of 3-connected planar graphs with convex faces
  - book: isbn:9780133016154
    title: Giuseppe Di Battista, Peter Eades, Roberto Tamassia and Ioannis G. Tollis, Graph Drawing, Algorithms for the Visualization of Graphs, Prentice Hall, 1999
    locator: the chapters on planar straight-line drawings, grid drawings and convex drawings
---

The planar straight-line drawing problem asks for a position in the plane for each vertex of a [planar graph](/planar-graph/), such that drawing every edge as a straight segment gives no crossings. Fáry's theorem says that such a drawing always exists, so the question is not whether but how well: on how small an integer grid, how fast, and with which extra properties, such as convex faces. The classic answers are the [Schnyder drawing](/schnyder-drawing/) on an $(n - 2) \times (n - 2)$ grid and the [de Fraysseix-Pach-Pollack](/de-fraysseix-pach-pollack/) drawing on a $(2n - 4) \times (n - 2)$ grid, both in linear time, and the [Tutte drawing](/tutte-spring-theorem/) with convex faces for 3-connected graphs.

## In plain words

A planar network can be drawn on paper with no crossing lines if the lines may bend. The surprise is that bends are never needed: every planar network can be drawn with straight lines and still no crossings.

The practical question is to do this with all points on a grid of whole numbers that is not too large, so that the picture can be stored exactly and printed without points crowding together. Grids with about $n$ rows and $n$ columns are enough, and they can be found in time proportional to $n$.

## Definition

**Input.** A planar graph $G = (V, E)$ with $n$ vertices. Usually a planar embedding is given too, as a [rotation system](/rotation-system/) $\rho$ ($\rho(v)$ lists the neighbours of $v$ counterclockwise) and an outer face; if not, a [planarity test](/planarity-testing/) computes one in $O(n)$ time.

**Output.** A point $p(v) \in \mathbb{R}^2$ for each vertex, such that

1. distinct vertices get distinct points,
2. no vertex lies on the segment of an edge it does not belong to,
3. the segments of two edges meet only in a common end.

The drawing *realizes* $\rho$ if the neighbours of every vertex appear around it in the order $\rho(v)$. A *grid drawing* uses points in $\{0, \ldots, W\} \times \{0, \ldots, H\}$, and its size is $W \times H$.

For a [maximal planar graph](/maximal-planar-graph/) with $n \ge 4$, the embedding is unique up to the choice of the outer face and a mirror image, so the only real choice is the outer triangle. Every planar graph is a subgraph of a maximal planar graph on the same vertices, and a drawing of the supergraph is a drawing of the graph, so most algorithms first add edges.

## Variants

- **Grid drawings.** Minimize the grid size $W \times H$, or the area, or the ratio of the longest to the shortest edge.
- **Convex drawings.** Every inner face is a convex polygon and the outer face is the outside of a convex polygon. A planar graph has such a drawing in particular when it is 3-connected; Tutte's barycentric method gives one with real coordinates.
- **Strictly convex drawings.** No three vertices of a face are collinear; these need larger grids than convex drawings.
- **Prescribed outer face.** The outer face is fixed to a given convex polygon, as in Tutte's theorem.
- **Point-set embedding.** The vertices must use a given set of $n$ points. Every outerplanar graph can be drawn on any $n$ points in general position, while for general planar graphs this is hard to decide.
- **Drawings with bends.** If edges may bend, every planar graph has an orthogonal drawing with few bends; this is a different problem.

## Examples

| graph | drawing | smallest grid of the drawing |
|---|---|---|
| a single vertex | the point $(0, 0)$ | $0 \times 0$ |
| a tree | put each vertex at (depth, order of first visit); no two edges cross | about $n \times n$ by this rule |
| $K_4$ | outer triangle $(2, 1)$, $(0, 2)$, $(1, 0)$, inner vertex $(1, 1)$, the [Schnyder drawing](/schnyder-drawing/) | $2 \times 2$, which is optimal |
| the octahedron | outer triangle $(4, 1)$, $(0, 4)$, $(1, 0)$; inner triangle $(3, 1)$, $(1, 3)$, $(1, 1)$ | $4 \times 4$ by Schnyder |
| $K_5$, $K_{3,3}$ | none: they are not planar, every drawing has a crossing | none |

For $K_4$, the grid size $2 \times 2$ cannot be improved: in every planar drawing of $K_4$ one vertex lies strictly inside the triangle of the other three, and a lattice triangle with a lattice point strictly inside needs at least three different $x$ values and three different $y$ values. For a tree, the rule in the table puts each subtree in its own band of consecutive rows, and all edges join consecutive columns, so two edges between the same two columns keep their order and do not cross.

## Known algorithms

| method | output | time | notes |
|---|---|---|---|
| Fáry's induction (1948) | straight-line drawing, real coordinates | $O(n^2)$ naively | remove a vertex of degree at most 5, draw the rest, put the vertex back in the kernel of its neighbourhood polygon |
| [Tutte's barycentric method](/tutte-spring-theorem/) (1963) | convex drawing of a 3-connected graph | one sparse linear system, $O(n^{3/2})$ by [nested dissection](/nested-dissection/) | coordinates can need exponential precision |
| [de Fraysseix-Pach-Pollack](/de-fraysseix-pach-pollack/) (1990) | $(2n - 4) \times (n - 2)$ grid | $O(n \log n)$, later $O(n)$ | [canonical ordering](/canonical-ordering/) and shifting |
| [Schnyder](/schnyder-drawing/) (1990) | $(n - 2) \times (n - 2)$ grid | $O(n)$ | region counts in a [Schnyder wood](/schnyder-woods/) |

All methods first triangulate the graph, in $O(n)$ time, and remove the added edges at the end.

## Bounds

- **Time.** $\Theta(n)$: linear-time algorithms exist, and any algorithm must output $n$ points.
- **Grid size, upper bound.** Every planar graph with $n \ge 3$ vertices has a straight-line drawing on the $(n - 2) \times (n - 2)$ grid (Schnyder).
- **Grid size, lower bound.** The nested triangles graph, $n/3$ triangles one inside the next with consecutive triangles joined, needs a grid with about $2n/3$ rows and about $2n/3$ columns in any drawing with that nesting (de Fraysseix, Pach and Pollack). So area $\Theta(n^2)$ is necessary and sufficient in the worst case.
- **Real coordinates.** Without a grid, Tutte drawings and Fáry-style constructions can need coordinates whose ratio of largest to smallest distance is exponential in $n$; grid drawings avoid this.

## Reductions

- **From general to triangulated.** Adding edges inside faces until every face is a triangle, without creating parallel edges, reduces the problem to [maximal planar graphs](/maximal-planar-graph/) in $O(n)$ time; see line L1 of the [Schnyder drawing](/schnyder-drawing/).
- **From the abstract graph.** If only the graph is given, a [planarity test](/planarity-testing/) such as the [Boyer-Myrvold](/boyer-myrvold-planarity-test/) algorithm first computes a rotation system in $O(n)$ time.
- **Non-planar graphs.** For graphs that are not planar, the problem becomes minimizing crossings; the [crossing number](/crossing-number/) and the [planarization heuristic](/planarization-heuristic/) replace crossings by dummy vertices and then draw the resulting planar graph.

## Applications

- **Graph drawing.** Straight-line grid drawings are a basic output format of [graph drawing](/graph-drawing/) tools, and the starting point for drawings that look better.
- **Geometry and meshes.** Tutte's method flattens triangulated surfaces for texture mapping; grid drawings give exact integer coordinates for geometric algorithms.
- **VLSI and maps.** Small grids bound the area of circuit layouts and the precision needed to store maps.
- **Proofs.** Straight-line drawings turn combinatorial statements about planar graphs into geometric ones, for example in proofs about the [crossing number](/crossing-number/).

## References
