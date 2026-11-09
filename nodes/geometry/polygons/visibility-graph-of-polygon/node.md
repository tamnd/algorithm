---
tag: GZ08RJ
kind: problem
slug: visibility-graph-of-polygon
name: Visibility graph of a polygon
aliases:
- polygon visibility graph
- vertex visibility graph
area: geometry/polygons
level: advanced
summary: Graph whose vertices are polygon vertices and whose edges join pairs that see each other inside the polygon.
prereqs: [simple-polygon, visibility-polygon]
see_also: [visibility-graph, visibility-polygon, euclidean-shortest-path-in-polygon, funnel-algorithm, polygon-triangulation, art-gallery-problem, dijkstra, polygon-with-holes]
sources:
  - paper: "John Hershberger, An optimal visibility graph algorithm for triangulated simple polygons, Algorithmica 4, 141 to 155 (1989)"
    locator: the O(E) algorithm from a triangulation, by walking shortest path trees from each vertex
  - paper: "Subir Kumar Ghosh and David M. Mount, An output-sensitive algorithm for computing visibility graphs, SIAM Journal on Computing 20(5), 888 to 910 (1991)"
    locator: the O(n log n + E) algorithm for polygons with holes by funnel sequences in a triangulation
  - book: isbn:9780521875745
    title: Subir Kumar Ghosh, Visibility Algorithms in the Plane, Cambridge University Press, 2007
    locator: Chapter 5 on visibility graphs, and Chapter 6 on the characterization and recognition of visibility graphs
  - book: isbn:9783540779735
    title: Mark de Berg, Otfried Cheong, Marc van Kreveld and Mark Overmars, Computational Geometry, Algorithms and Applications, third edition, Springer, 2008
    locator: Chapter 15, visibility graphs of polygonal obstacles, the O(n^2 log n) rotational sweep, and shortest paths
---

The visibility graph of a [simple polygon](/simple-polygon/) $P$ has the $n$ vertices of $P$ as its nodes and an edge between two vertices whenever the segment joining them lies in $P$. It contains the $n$ boundary edges and all diagonals of $P$, so it has between $2n - 3$ edges, the number in a [triangulation](/polygon-triangulation/), and $\binom{n}{2}$, for a convex polygon. Computing it is an output-sensitive problem: with $E$ edges in the answer, Hershberger showed in 1989 how to find them in $O(E)$ time from a triangulation, which is optimal, and Ghosh and Mount extended output sensitivity to polygons with holes in $O(n \log n + E)$ time. The graph is the classic tool for shortest paths among obstacles and for guarding problems, and the question of which graphs are visibility graphs of simple polygons is still open.

## In plain words

Think of the corners of a room with walls that bend in and out. Draw a line between two corners if you could stretch a string between them without it leaving the room. The corners and these lines form the visibility graph.

Neighboring corners are always connected, along the wall. A room with no inward bends connects every pair of corners. A room with many dents connects few pairs, but it always has enough lines to cut the floor into triangles. The useful fact is that the shortest walk between two corners only turns at corners, so it follows lines of this graph.

## Definition

**Input.** A simple polygon $P$ with vertices $v_0, \ldots, v_{n-1}$, identified with its closed region.

**Output.** The graph $G(P)$ on $\{v_0, \ldots, v_{n-1}\}$ with an edge $v_i v_j$ exactly when the closed segment $v_i v_j$ lies in $P$; equivalently, a list of the $E$ visible pairs.

**Model.** The [real RAM](/real-ram/); every decision is an [orientation test](/orientation-test/) on input points, exact on integer coordinates.

**Visibility conventions.** With closed visibility, as defined here, a segment may run along the boundary or touch a reflex vertex, so in an L-shape the two outer corners on either side of the reflex vertex see each other through it. Some authors use open visibility, where the segment may meet $\partial P$ only at its ends; this removes such grazing pairs. Algorithms assume general position, no three vertices collinear, and handle collinear vertices by one of the two conventions.

## Variants

- **Polygons with holes and obstacles.** For a [polygon with holes](/polygon-with-holes/), or a set of disjoint polygonal obstacles in the plane, the visibility graph joins vertices that see each other in the free space. This is the [visibility graph](/visibility-graph/) used in motion planning; it can have $\Theta(n^2)$ edges and no triangulation-based walk covers it, so the methods differ.
- **Point and segment visibility graphs.** The nodes are points in the plane with the other points as obstacles, or segments seen from one another.
- **Edge visibility graph.** The nodes are the edges of $P$, joined when some point of one sees some point of the other.
- **Visibility from one vertex.** The neighbors of one vertex are the vertices of $P$ on its [visibility polygon](/visibility-polygon/), found in $O(n)$ time.
- **Recognition and reconstruction.** Given a graph, decide whether it is the visibility graph of some simple polygon, and build one.

## Examples

All polygons are counterclockwise; visibility is closed.

| polygon | vertices | $n$ | $E$ | diagonals |
| --- | --- | --- | --- | --- |
| concave pentagon | $(0,0), (6,0), (6,4), (3,1), (0,4)$ | 5 | 7 | $(0,0)\text{--}(3,1)$ and $(6,0)\text{--}(3,1)$ |
| L-shape | $(0,0), (2,0), (2,1), (1,1), (1,2), (0,2)$ | 6 | 12 | all pairs except $(2,1)\text{--}(1,2)$, $(2,1)\text{--}(0,2)$ and $(2,0)\text{--}(1,2)$ |
| U-shape | $(0,0), (3,0), (3,3), (2,3), (2,1), (1,1), (1,3), (0,3)$ | 8 | 16 | 8 diagonals out of 20 |
| four-pointed star | $(0,0), (2,1), (4,0), (3,2), (4,4), (2,3), (0,4), (1,2)$ | 8 | 24 | all pairs except the 4 pairs of neighboring tips |
| convex polygon | any | $n$ | $\binom{n}{2}$ | all |

- **The pentagon.** It has the fewest possible edges, $2n - 3 = 7$: its graph is a triangulation. The pairs $(0,0)\text{--}(6,4)$ and $(6,0)\text{--}(0,4)$ cut through the notch, for example at $(3,2)$, and the top vertices $(6,4)$ and $(0,4)$ are separated by the notch as well.
- **The L-shape.** $(2,0)$ and $(0,2)$ see each other through the reflex vertex $(1,1)$; under open visibility this pair is dropped.
- **The star.** The segment between two neighboring tips such as $(0,0)$ and $(4,0)$ runs outside $P$, below the reflex vertex $(2,1)$, while opposite tips see each other through the center.

## Known algorithms

| algorithm | input | time | idea |
| --- | --- | --- | --- |
| test all pairs | simple polygon | $O(n^3)$ | test each of the $\binom{n}{2}$ segments against all edges |
| visibility polygon from each vertex | simple polygon | $O(n^2)$ | $n$ runs of a linear-time [visibility polygon](/visibility-polygon/) algorithm such as [Lee's](/lee-visibility-polygon-algorithm/) |
| rotational sweep (Lee 1978; Sharir and Schorr) | obstacles | $O(n^2 \log n)$ | sort the other vertices by angle around each vertex and sweep a ray, keeping the edges it crosses in a balanced tree |
| arrangement duality (Asano et al.; Welzl, 1985) | obstacles | $O(n^2)$ | sort all angles at once by the dual line arrangement |
| Hershberger, 1989 | triangulated simple polygon | $O(E)$ | traverse the shortest path tree from each vertex in the triangulation; with Chazelle's linear triangulation, $O(n + E)$ |
| Ghosh and Mount, 1991 | polygon with holes, obstacles | $O(n \log n + E)$ | triangulate, then follow funnels of visible pairs through the triangles, with work proportional to the edges found |
| Overmars and Welzl, 1988 | obstacles | $O(E \log n)$ with $O(n)$ space | rotation trees |

**Why output sensitivity is possible in a simple polygon.** Fix $v_i$ and triangulate $P$. The vertices seen from $v_i$ are reached by walking from the triangles at $v_i$ through the [dual tree](/triangulation-dual-tree/) of the triangulation, keeping the funnel of directions from $v_i$ that are not yet blocked, as in the [funnel algorithm](/funnel-algorithm/). The walk stops in each branch as soon as the funnel is empty, and Hershberger charges every step to an edge of the visibility graph, so the total work over all $i$ is $O(E)$.

## Bounds

- **Size.** $2n - 3 \le E \le \binom{n}{2}$ for a simple polygon. The lower bound holds because a triangulation consists of the $n$ boundary edges and $n - 3$ diagonals, all of them visible pairs; the upper bound is reached exactly by convex polygons, since the two neighbors of a reflex vertex never see each other.
- **Time.** $\Omega(n + E)$, to read the input and write the output, so Hershberger's algorithm is optimal given a triangulation, and $O(n + E)$ overall with a linear-time triangulation. For obstacles and polygons with holes, $O(n \log n + E)$ (Ghosh and Mount).
- **Recognition.** Every visibility graph of a simple polygon is Hamiltonian, along the boundary, and has further necessary properties studied by Ghosh, but no characterization is known. Recognition is known to be decidable in polynomial space through the existential theory of the reals, and whether it is in NP is open.

## Reductions

- **Shortest paths to the visibility graph.** A shortest path between two points inside a polygon, with or without holes, is a polygonal path whose inner vertices are reflex vertices of $P$, and each of its segments is a visible pair. So [Dijkstra's algorithm](/dijkstra/) on the visibility graph, with the two points added, gives the [Euclidean shortest path](/euclidean-shortest-path-in-polygon/) in $O(E + n \log n)$ after the graph is built. In a simple polygon the [funnel algorithm](/funnel-algorithm/) is faster, $O(n)$ after triangulation.
- **Triangulations to the visibility graph.** The triangulations of $P$ are the maximal sets of pairwise non-crossing edges of $G(P)$.
- **Visibility polygons to the visibility graph.** The neighbors of $v_i$ are the vertices on the [visibility polygon](/visibility-polygon/) of $v_i$, which gives the $O(n^2)$ method.
- **Guarding to graph problems.** Placing guards at vertices so that every vertex is seen is a dominating set problem on $G(P)$; guarding all of $P$ is the harder [art gallery problem](/art-gallery-problem/).

## Applications

- **Motion planning.** Shortest paths for a point robot among polygonal obstacles run on the visibility graph, the oldest exact method for this problem.
- **Guarding and surveillance.** Vertex guards, cliques of mutually visible vertices, and covering problems are formulated on the visibility graph.
- **Polygon decomposition.** Decompositions into convex or star-shaped pieces, and the enumeration of triangulations, use the visible diagonals.
- **Wireless and sensor networks.** Line-of-sight links between antennas placed at corners of buildings.

## References
