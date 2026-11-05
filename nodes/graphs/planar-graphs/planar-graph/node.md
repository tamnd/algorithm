---
tag: 5ZRYH5
kind: concept
slug: planar-graph
name: Planar graph
aliases:
- planar graphs
area: graphs/planar-graphs
level: intro
summary: A graph that can be drawn in the plane with no edge crossings.
prereqs: [graph, simple-graph]
see_also: [euler-formula, planar-edge-bound, kuratowski-theorem, planar-embedding, rotation-system, planarity-testing, planar-dual-graph, planar-separator-theorem]
sources:
  - book: isbn:9783662536216
    title: Reinhard Diestel, Graph Theory, fifth edition, Springer, 2017
    locator: Chapter 4, Planar graphs (Section 4.2 plane graphs, Section 4.4 planar graphs and Kuratowski's theorem)
  - book: isbn:9780130144003
    title: Douglas B. West, Introduction to Graph Theory, second edition, Prentice Hall, 2001
    locator: Section 6.1, Embeddings and Euler's formula, and Section 6.2, Characterization of planar graphs
  - book: isbn:9780801866890
    title: Bojan Mohar and Carsten Thomassen, Graphs on Surfaces, Johns Hopkins University Press, 2001
    locator: Chapter 2, Planar graphs, and Chapters 3 and 4 (embeddings described by rotation systems)
  - paper: doi:10.1145/321850.321852
    title: John Hopcroft and Robert Tarjan, Efficient planarity testing, Journal of the ACM 21(4), 549 to 568 (1974)
    locator: the whole paper (the first linear-time planarity test)
---

A planar graph is a [graph](/graph/) that can be drawn in the plane so that no two edges cross. A graph together with one such drawing is a *plane graph*, and the drawing cuts the plane into regions called [faces](/planar-face/). Planar graphs are sparse (a [simple](/simple-graph/) planar graph with $n \ge 3$ vertices has at most $3n - 6$ edges), they have small separators, and many problems that are hard on general graphs become easier on them.

## In plain words

Draw the vertices of a graph as dots on paper and its edges as curves between the dots. If you can do this so that no two curves cross, the graph is planar. A road map with a bridge or a tunnel at each crossing is not a planar drawing, but the graph can still be planar if some other drawing has no crossings.

Some graphs can never be drawn this way. Five dots that are all joined to each other always give a crossing. So do three houses that each need a line to each of three utilities. A famous theorem says that every non-planar graph contains one of these two graphs in a stretched form.

## The idea

**Drawings.** A *drawing* of a graph $G = (V, E)$ maps each vertex to a distinct point of $\mathbb{R}^2$ and each edge $uv$ to a simple arc (a continuous injective image of $[0, 1]$) from the point of $u$ to the point of $v$, which passes through no other vertex point. The drawing is *planar*, or an *embedding*, when two arcs meet only at a common end. $G$ is **planar** when it has a planar drawing. A **plane graph** is a graph with a fixed planar drawing.

**Sphere and plane.** A graph embeds in the plane if and only if it embeds in the sphere $S^2$. Stereographic projection from a point of the sphere that is not on the drawing maps one to the other. On the sphere no face is special, so any face of a plane graph can be made the outer face of another drawing of the same graph.

**How an embedding is given to an algorithm.** A program cannot store arcs. It stores one of three equivalent forms:

- a **rotation system**: for each vertex, the cyclic order of its neighbours around it in the drawing. For a connected graph this determines the faces, and so the embedding up to a homeomorphism of the sphere. See [rotation system](/rotation-system/).
- a **combinatorial map** or an edge list with pointers, such as the [doubly connected edge list](/doubly-connected-edge-list/), which stores for each half-edge its twin, the next half-edge of its face and its face.
- **coordinates**: a point for each vertex such that straight segments for the edges do not cross. [Fáry's theorem](/fary-theorem/) says that each simple planar graph has such a drawing.

Most planar graph algorithms take the first or second form as input. The step that computes it from a plain [adjacency list](/adjacency-list/) is the [planar embedding](/planar-embedding/) problem.

**Characterizations.** These conditions on a finite graph $G$ are equivalent:

1. $G$ is planar.
2. $G$ contains no subdivision of $K_5$ or $K_{3,3}$ ([Kuratowski's theorem](/kuratowski-theorem/), 1930).
3. $G$ has no $K_5$ or $K_{3,3}$ as a [minor](/graph-minor/) ([Wagner's theorem](/wagner-theorem/), 1937).
4. $G$ has a rotation system whose number of faces $f$ satisfies $n - m + f = 1 + c$, where $c$ is the number of components (the combinatorial form of [Euler's formula](/euler-formula/)).

**Sparsity.** By Euler's formula, a simple planar graph with $n \ge 3$ vertices has at most $3n - 6$ edges, and at most $2n - 4$ when it has no triangle (the [planar edge bound](/planar-edge-bound/)). So the average degree is less than 6, and every simple planar graph has a vertex of degree at most 5. The class is closed under taking subgraphs and minors, so every subgraph and every contraction of a planar graph is again planar.

**Separators.** Every planar graph on $n$ vertices has a set of $O(\sqrt n)$ vertices whose removal leaves components of at most $2n/3$ vertices ([planar separator theorem](/planar-separator-theorem/)). This drives divide and conquer on planar graphs.

## Examples

| graph | $n$ | $m$ | planar? | reason |
|---|---|---|---|---|
| a single vertex | 1 | 0 | yes | a point is a drawing |
| any [tree](/tree/) | $n$ | $n - 1$ | yes | draw it level by level, children below their parent |
| $K_4$ | 4 | 6 | yes | a triangle with the fourth vertex inside, joined to the three corners |
| the cube graph $Q_3$ | 8 | 12 | yes | a small square inside a large square, corners joined |
| $K_5$ | 5 | 10 | no | $10 > 3 \cdot 5 - 6 = 9$ |
| $K_{3,3}$ | 6 | 9 | no | it has no triangle and $9 > 2 \cdot 6 - 4 = 8$ |
| the Petersen graph | 10 | 15 | no | it has girth 5 and $15 > \frac{5}{3}(10 - 2) = 13.3$; it also has a $K_{3,3}$ subdivision |
| $K_5 - e$ | 5 | 9 | yes | it meets $3n - 6$ with equality, and a drawing exists |

The Petersen bound uses the generalization of the edge bound: a planar graph with girth $g \ge 3$ and a cycle has $m \le \frac{g}{g-2}(n-2)$, because each face then has at least $g$ edge sides.

The edge bound is necessary but not sufficient. The graph made of $K_{3,3}$ plus 3 isolated vertices has 9 vertices and 9 edges, far below $3 \cdot 9 - 6 = 21$, and it is still not planar.

**Same graph, two embeddings.** In $K_{2,4}$, the vertices $a$ and $c$ are joined by four paths of length 2, through $x_1, x_2, x_3, x_4$. In one drawing the paths leave $a$ in the order $x_1, x_2, x_3, x_4$, and the four faces are the 4-cycles through $\{x_1, x_2\}$, $\{x_2, x_3\}$, $\{x_3, x_4\}$ and $\{x_4, x_1\}$. In another drawing the order is $x_1, x_3, x_2, x_4$, and the cycle through $x_1$ and $x_2$ is no longer a face. So a planar graph can have embeddings with different faces. A 3-connected planar graph has only one embedding on the sphere, up to a mirror image (Whitney's theorem; Diestel, Section 4.3). So $K_4$ has one embedding, and its four faces are always its four triangles.

## Where it is used

- **Testing and embedding.** The [planarity testing](/planarity-testing/) problem is solvable in linear time by the [Hopcroft-Tarjan test](/hopcroft-tarjan-planarity-test/) and the [Boyer-Myrvold test](/boyer-myrvold-planarity-test/).
- **Map coloring.** The faces of a map are the vertices of its [planar dual](/planar-dual-graph/). The [four color theorem](/four-color-theorem/) and the [five color theorem](/five-color-theorem/) are statements about planar graphs; see [planar graph coloring](/planar-graph-coloring/).
- **Divide and conquer.** [Planar separators](/planar-separator-theorem/), [r-divisions](/r-division/) and [nested dissection](/nested-dissection/) give fast [shortest paths](/planar-shortest-paths/) and sparse linear solvers on planar meshes.
- **Approximation.** [Baker's technique](/baker-planar-ptas/) gives polynomial-time approximation schemes for problems such as [maximum independent set](/maximum-independent-set/) on planar graphs.
- **Drawing.** [Graph drawing](/graph-drawing/) uses planar embeddings to draw networks with no crossings, as in the [Schnyder drawing](/schnyder-drawing/) on a grid.
- **Geometry.** A [planar subdivision](/planar-subdivision/), a [Delaunay triangulation](/delaunay-triangulation/) and a [Voronoi diagram](/voronoi-diagram/) are plane graphs.
- **Isomorphism.** [Planar graph isomorphism](/planar-graph-isomorphism/) is solvable in polynomial time, unlike the general case, whose complexity is open.

## References
