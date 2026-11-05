---
tag: 7T54Y1
kind: concept
slug: maximal-planar-graph
name: Maximal planar graph
aliases:
- triangulated planar graph
- planar triangulation
area: graphs/planar-graphs
level: core
summary: A planar graph to which no edge can be added while staying planar; all faces are triangles.
prereqs: [planar-graph, planar-edge-bound, planar-face]
see_also: [euler-formula, schnyder-woods, canonical-ordering, schnyder-drawing, four-color-theorem, outerplanar-graph, triangulation, k-vertex-connected-graph]
sources:
  - book: isbn:9783662536216
    title: Reinhard Diestel, Graph Theory, fifth edition, Springer, 2017
    locator: Section 4.2, Plane graphs (maximal plane graphs are plane triangulations, and the edge count 3n - 6), and Section 4.3 (3-connected graphs have a unique embedding)
  - book: isbn:9780130144003
    title: Douglas B. West, Introduction to Graph Theory, second edition, Prentice Hall, 2001
    locator: Section 6.1, Embeddings and Euler's formula (maximal planar graphs and triangulations)
  - book: isbn:9781846289699
    title: J. A. Bondy and U. S. R. Murty, Graph Theory, Graduate Texts in Mathematics 244, Springer, 2008
    locator: Chapter 10, Planar graphs (the sections on Euler's formula and on triangulations)
---

A maximal planar graph is a [simple](/simple-graph/) [planar graph](/planar-graph/) to which no edge can be added without losing planarity. For $n \ge 3$ vertices this is the same as a planar graph with exactly $3n - 6$ edges, and the same as a planar graph in which every [face](/planar-face/) of an embedding is a triangle; such a graph is also called a plane triangulation. Many planar algorithms first add edges to reach a maximal planar graph, because its rigid structure (3-connected, a unique embedding, all faces triangles) makes later steps simpler.

## In plain words

Draw a planar graph with no crossings. If some region of the drawing has four or more corners, you can draw a new line across it between two corners that are not yet joined, and the drawing still has no crossings. Keep doing this until every region is a triangle. Now no new line can be added anywhere: the graph is full.

A full planar graph with a given number of points always has the same number of lines: three times the points, minus six. It also has only one drawing, apart from mirror images and the choice of which triangle is outside.

## The idea

**Definition.** A simple graph $G$ is *maximal planar* if $G$ is planar and, for every pair of non-adjacent vertices $u, v$, the graph $G + uv$ is not planar. A *plane triangulation* is a simple plane graph in which every face is bounded by a triangle (a cycle of length 3).

**Theorem.** Let $G$ be a simple planar graph with $n \ge 3$ vertices and $m$ edges. These are equivalent:

1. $G$ is maximal planar.
2. In some planar embedding of $G$, every face is a triangle.
3. In every planar embedding of $G$, every face is a triangle.
4. $m = 3n - 6$.

*Proof.* Parts 2, 3 and 4 are equivalent by part 4 of the [planar edge bound](/planar-edge-bound/). If $m = 3n - 6$, adding any edge gives $3n - 5$ edges, which exceeds the bound, so $G$ is maximal: 4 implies 1. We show that 1 implies 2. Let $G$ be maximal planar, with a fixed embedding.

*Connected.* If $G$ had two components, an edge between them could be drawn in the outer face, against maximality.

*2-connected.* Suppose $v$ is a cut vertex. The darts at $v$ go into at least two blocks, so two darts $(v, x)$ and $(v, y)$ that are consecutive in the rotation at $v$ go into different blocks. The corner between them lies on one face, and the face walk passes $x, v, y$. Draw a new edge $xy$ inside this face, close to the two edges $vx$ and $vy$. The drawing stays planar. And $x, y$ are not adjacent, because otherwise $x, v, y$ would be a triangle and $x, y$ would be in the same block. This contradicts maximality.

*All faces are triangles.* In a 2-connected plane graph each face is bounded by a cycle (Diestel, Section 4.2). Suppose a face $f$ is bounded by a cycle $u_1 u_2 \cdots u_k$ with $k \ge 4$. If $u_1 u_3 \notin E$, a new arc inside $f$ from $u_1$ to $u_3$ keeps the drawing planar, against maximality. So $u_1 u_3 \in E$, and in the same way $u_2 u_4 \in E$. Both edges are drawn outside $f$. Now put a new vertex $p$ inside $f$, joined to $u_1, u_2, u_3, u_4$ by arcs inside $f$; the result is still planar. Contract the path $u_4 u_5 \cdots u_k u_1$ to a single edge $u_4 u_1$. The vertices $p, u_1, u_2, u_3, u_4$ are now pairwise adjacent: $p$ to all four, the cycle edges $u_1u_2$, $u_2u_3$, $u_3u_4$, $u_4u_1$, and the chords $u_1u_3$, $u_2u_4$. So a planar graph has a $K_5$ [minor](/graph-minor/). But contracting an edge of a plane graph keeps it planar, and $K_5$ is not planar ($10 > 3 \cdot 5 - 6$). This contradiction shows $k = 3$. $\blacksquare$

**Counts.** With $m = 3n - 6$, [Euler's formula](/euler-formula/) gives $f = 2n - 4$ faces. The degrees sum to $6n - 12$, so

$$\sum_{v} (6 - \deg v) = 12 .$$

**Structure for $n \ge 4$.**

- $G$ is 3-connected, so its minimum degree is at least 3, and by Whitney's theorem it has a unique embedding on the sphere up to a mirror image (Diestel, Section 4.3). Its faces are then determined by the graph alone.
- The neighbours of each vertex $v$ form a cycle (the *link* of $v$), because the faces around $v$ are triangles that share consecutive edges.
- At least 4 vertices have degree at most 5. Each term $6 - \deg v$ is at most 3, because the minimum degree is at least 3, and it is positive only when $\deg v \le 5$. If $k$ vertices have degree at most 5, the sum gives $12 \le 3k$, so $k \ge 4$.

**Maximal versus maximum.** For planar graphs, every maximal planar graph on $n \ge 3$ vertices has the maximum number of edges, $3n - 6$. This is not true for many other classes: a maximal triangle-free graph need not be a maximum one.

**Triangulating.** Any simple plane graph with $n \ge 3$ vertices can be extended to a maximal planar graph on the same vertices by adding edges inside faces. A linear-time method first makes the graph connected and 2-connected, then fans each face from one vertex, taking care not to add an edge that already exists outside the face (the case handled in the proof above). The added edges are later deleted.

## Examples

| graph | $n$ | $m$ | $3n - 6$ | degrees | maximal planar? |
|---|---|---|---|---|---|
| $K_3$ | 3 | 3 | 3 | 2, 2, 2 | yes |
| $K_4$ | 4 | 6 | 6 | four of degree 3 | yes |
| $K_5 - e$ | 5 | 9 | 9 | 3, 3, 4, 4, 4 | yes |
| the octahedron | 6 | 12 | 12 | six of degree 4 | yes |
| the icosahedron | 12 | 30 | 30 | twelve of degree 5 | yes |
| the wheel $W_5$ (a 5-cycle and a hub) | 6 | 10 | 12 | 5, 3, 3, 3, 3, 3 | no: the outer face is a 5-cycle |
| the cube $Q_3$ | 8 | 12 | 18 | eight of degree 3 | no: its faces are 4-cycles |
| a tree on $n \ge 3$ vertices | $n$ | $n - 1$ | $3n - 6$ | | no |

In each "yes" row, $\sum (6 - \deg v) = 12$: for $K_4$, $4 \cdot 3$; for the octahedron, $6 \cdot 2$; for the icosahedron, $12 \cdot 1$; for $K_5 - e$, $3 + 3 + 2 + 2 + 2$.

**Stacked triangulations.** Start with a triangle and repeatedly put a new vertex inside a face, joined to the three corners of that face. Each step adds 1 vertex, 3 edges and 2 faces, so $m = 3n - 6$ stays true. These are the Apollonian networks, or stacked triangulations. $K_4$ is the first one after the triangle.

**Small $n$.** With $n = 1$ or $n = 2$ the formula $3n - 6$ is negative, and the maximal planar graphs are $K_1$ and $K_2$.

## Where it is used

- **Algorithms that need triangles.** [Schnyder woods](/schnyder-woods/) and the [Schnyder drawing](/schnyder-drawing/), the [canonical ordering](/canonical-ordering/) and the [de Fraysseix-Pach-Pollack](/de-fraysseix-pach-pollack/) grid drawing are defined for maximal planar graphs. A general planar graph is triangulated first.
- **Separators.** The [Lipton-Tarjan separator](/lipton-tarjan-separator/) algorithm triangulates the graph so that every non-tree edge closes a short cycle with the BFS tree.
- **Coloring.** A smallest counterexample to the [four color theorem](/four-color-theorem/) would be a maximal planar graph, since adding edges only makes coloring harder. The discharging proofs start from $\sum (6 - \deg v) = 12$.
- **Tightness of bounds.** Maximal planar graphs show that the [planar edge bound](/planar-edge-bound/) is tight, and they are the worst case for the [crossing lemma](/crossing-lemma/) argument.
- **Geometry.** A [triangulation](/triangulation/) of a point set, such as the [Delaunay triangulation](/delaunay-triangulation/), has triangles as inner faces and the convex hull as the outer face. Adding one vertex outside the hull, joined to all hull vertices, makes it maximal planar.
- **Tutte's spring drawing.** A maximal planar graph with $n \ge 4$ is 3-connected, so the [Tutte spring theorem](/tutte-spring-theorem/) applies.

## References
