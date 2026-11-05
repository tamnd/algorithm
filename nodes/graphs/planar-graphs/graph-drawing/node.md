---
tag: XA4WY9
kind: problem
slug: graph-drawing
name: Graph drawing
aliases:
- Drawing graphs nicely
area: graphs/planar-graphs
level: core
summary: Placing the vertices and edges of a graph in the plane so that its structure is clear and readable.
prereqs: [planar-graph, planar-embedding, crossing-number]
see_also: [planar-straight-line-drawing, de-fraysseix-pach-pollack, schnyder-drawing, tutte-spring-theorem, force-directed-layout, tree-drawing, book-embedding, fary-theorem]
sources:
  - book: "Giuseppe Di Battista, Peter Eades, Roberto Tamassia and Ioannis G. Tollis, Graph Drawing, Algorithms for the Visualization of Graphs, Prentice Hall, 1999"
    locator: Chapter 1 and Chapter 2 (drawing conventions, aesthetics and the main approaches), Chapter 4 (planar straight-line drawings), Chapter 5 (orthogonal drawings and bend minimization by network flow), Chapter 9 (layered drawings of digraphs)
  - book: "Takao Nishizeki and Md. Saidur Rahman, Planar Graph Drawing, World Scientific, 2004"
    locator: Chapter 1 (drawing styles) and the chapters on straight-line, convex and orthogonal drawings
  - paper: doi:10.1007/BF02122694
    title: Hubert de Fraysseix, János Pach and Richard Pollack, How to draw a planar graph on a grid, Combinatorica 10(1), 41 to 51 (1990)
    locator: the grid drawing in O(n log n) time on a (2n - 4) by (n - 2) grid, and the lower bound by nested triangles
  - paper: "Roberto Tamassia, On embedding a graph in the grid with the minimum number of bends, SIAM Journal on Computing 16(3), 421 to 444 (1987)"
    locator: the network flow method for bend-minimum orthogonal drawings of a plane graph with a fixed embedding
  - paper: "Michael R. Garey and David S. Johnson, Crossing number is NP-complete, SIAM Journal on Algebraic and Discrete Methods 4(3), 312 to 316 (1983)"
    locator: the main theorem
  - paper: "Kozo Sugiyama, Shojiro Tagawa and Mitsuhiko Toda, Methods for visual understanding of hierarchical system structures, IEEE Transactions on Systems, Man, and Cybernetics 11(2), 109 to 125 (1981)"
    locator: the layered drawing method in four phases
  - paper: "Ashim Garg and Roberto Tamassia, On the computational complexity of upward and rectilinear planarity testing, SIAM Journal on Computing 31(2), 601 to 625 (2001)"
    locator: NP-completeness of upward planarity testing and of rectilinear planarity testing
  - paper: "Marek Chrobak and Thomas H. Payne, A linear-time algorithm for drawing a planar graph on a grid, Information Processing Letters 54(4), 241 to 246 (1995)"
    locator: the linear-time implementation of the shift method
---

Graph drawing is the problem of mapping a graph to the plane, vertices to points and edges to curves, so that the picture shows the structure of the graph and is easy to read. Readability is made precise by a *drawing convention*, which says what a valid drawing is (for example straight edges on an integer grid), and by *aesthetic criteria*, which are quantities to minimize or bound, such as crossings, area, bends and the smallest angle. Most of these optimization problems are [NP-hard](/np-hard/) for general graphs, so the field combines exact algorithms for special classes, above all [planar graphs](/planar-graph/) and trees, with heuristics such as [force-directed layout](/force-directed-layout/).

## In plain words

You have a network: a list of items and a list of links between pairs of items. You want a readable picture of it, with a dot for each item and a line for each link.

Some pictures are better than others. Lines that cross each other are hard to follow. Bends in lines are hard to follow. A picture that is very large, or that squeezes dots together, is hard to read. Lines that leave a dot at almost the same angle blur together.

So graph drawing asks: given the network and some rules for what a picture may look like, find the picture that breaks the fewest of these goals. For some kinds of networks, such as those that can be drawn with no crossings at all, there are fast methods with guarantees. For others, people use methods that work well in practice without a guarantee.

## Definition

Let $G = (V, E)$ be a graph with $n$ vertices and $m$ edges. A **drawing** $\Gamma$ of $G$ maps each vertex $v$ to a point $\Gamma(v) \in \mathbb{R}^2$, different vertices to different points, and each edge $uv$ to a simple arc from $\Gamma(u)$ to $\Gamma(v)$ that contains no other vertex point. Two arcs that share an interior point *cross* there. The usual measures of a drawing are:

| measure | definition |
|---|---|
| crossings $\mathrm{cr}(\Gamma)$ | the number of crossing points of pairs of edges |
| area | the area of the smallest axis-parallel box around the drawing, for drawings with integer vertex coordinates |
| bends | the number of corners on the edges, for polygonal edges |
| angular resolution | the smallest angle between two edges at a common vertex |
| aspect ratio | the ratio of the longer to the shorter side of the box |

**Graph drawing problem (general form).** Given $G$, a drawing convention $\mathcal{C}$ and a measure $\mu$, find a drawing $\Gamma$ of $G$ in $\mathcal{C}$ that minimizes $\mu(\Gamma)$, or decide that $\mathcal{C}$ has no drawing of $G$.

**How the input is given.** The input is the graph alone, by adjacency lists. For planar drawings there are two versions. In the *variable embedding* version only the graph is given, and the algorithm may choose any [planar embedding](/planar-embedding/). In the *fixed embedding* version the input also gives a [rotation system](/rotation-system/) (the cyclic order of the neighbours at each vertex) and an outer face, and the drawing must have exactly these. The output is coordinates: vertex points, and bend points for polygonal edges.

## Variants

- **Planar straight-line drawing.** Every edge is a segment and no two edges cross. By [Fáry's theorem](/fary-theorem/) every simple planar graph has one; on an integer grid, area $O(n^2)$ suffices. See [planar straight-line drawing](/planar-straight-line-drawing/).
- **Convex drawing.** A planar straight-line drawing in which every face is a convex polygon. Every 3-connected planar graph has one, by [Tutte's spring theorem](/tutte-spring-theorem/).
- **Orthogonal drawing.** Edges are chains of horizontal and vertical segments, so every vertex has degree at most 4. The usual goal is to minimize bends.
- **Polyline drawing.** Edges are polygonal chains with few bends, which allows smaller area or larger angles than straight lines.
- **Layered (hierarchical) drawing.** For a [directed acyclic graph](/directed-acyclic-graph/), vertices go on horizontal lines and every edge points downward. The framework of Sugiyama, Tagawa and Toda has four phases: remove cycles (a [feedback arc set](/feedback-arc-set-problem/)), assign layers, order the vertices in each layer to reduce crossings, and assign coordinates.
- **Upward planar drawing.** A planar drawing of a digraph where every edge goes up.
- **Tree drawing.** Rooted trees drawn in layers with small width, for example by the [Reingold-Tilford layout](/reingold-tilford-layout/); see [tree drawing](/tree-drawing/).
- **Force-directed and energy-based drawing.** Model edges as springs and vertices as charges and minimize the energy; see [force-directed layout](/force-directed-layout/). Spectral drawing places vertices by eigenvectors of the [Laplacian matrix](/laplacian-matrix/), and stress majorization fits distances in the plane to graph distances, as in [multidimensional scaling](/multidimensional-scaling/).
- **Book embedding.** Vertices on a line and edges in half-planes (pages) with no crossings in a page; see [book embedding](/book-embedding/).
- **Crossing minimization.** Minimize the number of crossings in any drawing; the minimum is the [crossing number](/crossing-number/).

## Examples

Each example lists integer vertex points; edges are segments.

| graph | points | crossings | box |
|---|---|---|---|
| a single vertex | $(0, 0)$ | 0 | $0 \times 0$ |
| the path $a, b, c$ (a tree) | $(0,0), (1,0), (2,0)$ | 0 | $2 \times 0$ |
| $K_4$ | $(0,0), (4,0), (2,3), (2,1)$ | 0 | $4 \times 3$ |
| $K_5$ on the corners of a convex pentagon | $(2,0), (4,2), (3,4), (1,4), (0,2)$ | 5 | $4 \times 4$ |
| $K_5$, better | $(0,0), (6,0), (3,6), (1,1), (2,1)$ | 1 | $6 \times 6$ |
| $K_{3,3}$, parts $\{a_1, a_2, a_3\}$ and $\{b_1, b_2, b_3\}$ | $a$: $(0,0), (2,3), (4,0)$; $b$: $(1,0), (2,4), (2,2)$ | 1 | $4 \times 4$ |

$K_4$ is planar, and the drawing has 4 faces. $K_5$ and $K_{3,3}$ are not planar, so no drawing has 0 crossings; the drawings with 1 crossing are optimal, since both have [crossing number](/crossing-number/) 1. The convex pentagon drawing of $K_5$ shows that the choice of points matters: its five diagonals form a pentagram with 5 crossings.

## Known algorithms

| problem | algorithm | time | guarantee |
|---|---|---|---|
| planar straight-line grid drawing | [de Fraysseix, Pach and Pollack](/de-fraysseix-pach-pollack/), shift method on a [canonical ordering](/canonical-ordering/) | $O(n)$ with the improvement of Chrobak and Payne | grid $(2n - 4) \times (n - 2)$ |
| planar straight-line grid drawing | [Schnyder's method](/schnyder-drawing/) by [Schnyder woods](/schnyder-woods/) | $O(n)$ | grid $(n - 2) \times (n - 2)$ |
| convex drawing of a 3-connected planar graph | [Tutte's barycentric method](/tutte-spring-theorem/): fix the outer face on a convex polygon and solve a linear system | one sparse linear system | convex faces; the coordinates are rationals that can need many digits |
| bend-minimum orthogonal drawing, fixed embedding, degree at most 4 | Tamassia's method: a [minimum cost flow](/min-cost-flow-problem/) from vertices to faces, where flow units are angles and bends | polynomial | the minimum number of bends for the embedding |
| layered drawing of a digraph | Sugiyama framework | heuristic phases | none in general; crossing minimization between two layers is already NP-hard |
| general graphs | [force-directed layout](/force-directed-layout/) | $O(n^2)$ per iteration in the simple form | local minimum of an energy |
| non-planar graphs, few crossings | [planarization heuristic](/planarization-heuristic/): find a large planar subgraph, insert the other edges with few crossings, then draw the planar result | polynomial | heuristic |

A planar drawing algorithm needs a planar embedding first. [Planarity testing](/planarity-testing/) gives one in linear time, for example the [Boyer-Myrvold test](/boyer-myrvold-planarity-test/).

## Bounds

- **Area of planar straight-line grid drawings.** $O(n^2)$ suffices (de Fraysseix, Pach and Pollack; Schnyder). It is also needed: the nested triangles graph, with $n/3$ triangles each inside the next, needs a grid whose sides are both at least of order $n$, as de Fraysseix, Pach and Pollack show. So the optimal area is $\Theta(n^2)$ in the worst case.
- **Edges and crossings.** A graph with $m \ge 4n$ edges has crossing number at least $m^3 / (64 n^2)$, by the [crossing lemma](/crossing-lemma/). So dense graphs have many crossings in every drawing.
- **Hardness.** Computing the crossing number is NP-hard (Garey and Johnson, 1983). Testing whether a planar graph has an orthogonal drawing with no bends, when the embedding is free, is NP-complete, and so is testing whether a digraph has an upward planar drawing (Garg and Tamassia). So bend minimization over all embeddings is NP-hard. Minimizing crossings in a layered drawing is NP-hard already for two layers when the order of one layer is fixed.
- **Fixed versus variable embedding.** Many problems become polynomial when the embedding is fixed, as bend minimization does by Tamassia's flow method.

## Reductions

- **From non-planar to planar.** Replace each crossing of a drawing by a new vertex of degree 4. The result is a planar graph, and a planar drawing of it gives a drawing of the original graph with those crossings. This is how the [planarization heuristic](/planarization-heuristic/) reduces drawing to planar drawing.
- **From any planar graph to a triangulation.** Add edges (and, for multigraphs, vertices) until the graph is [maximal planar](/maximal-planar-graph/), draw it, and delete the added edges. Grid algorithms such as the shift method assume a triangulation for this reason.
- **Crossing number to drawing.** Deciding whether $G$ has a drawing with at most $k$ crossings is the decision version of the crossing number problem, so every hardness result for the [crossing number](/crossing-number/) applies to crossing minimization in drawing.
- **To linear algebra.** Tutte's method reduces a convex drawing to one system of linear equations, one for each inner vertex.

## Applications

Graph drawing is used to show software structure (call graphs, class diagrams, dependency graphs), networks (computer networks, social networks), biological pathways, circuit schematics and VLSI layout, database schemas, and flow charts. VLSI layout and printed circuit boards are the origin of grid and orthogonal drawings, and of the study of area and bends. Tools such as Graphviz implement the layered method and force-directed methods.

## References
