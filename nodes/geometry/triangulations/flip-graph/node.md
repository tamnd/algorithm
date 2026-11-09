---
tag: G414TD
kind: concept
slug: flip-graph
name: Flip graph of triangulations
aliases:
- Triangulation flip graph
- graph of triangulations
- associahedron graph
area: geometry/triangulations
level: advanced
summary: Graph whose vertices are the triangulations of a point set and whose edges join triangulations differing by one flip.
prereqs: [edge-flip, triangulation-of-point-set, catalan-triangulation-theorem]
see_also: [flip-distance, flip-graph-diameter-theorem, lawson-flip-algorithm, number-of-triangulations, tree-rotation, regular-triangulation, delaunay-triangulation, binary-tree]
sources:
  - paper: "Charles L. Lawson, Transforming triangulations, Discrete Mathematics 3(4), 365 to 372 (1972)"
    locator: every two triangulations of a planar point set are joined by flips
  - paper: "Daniel D. Sleator, Robert E. Tarjan and William P. Thurston, Rotation distance, triangulations, and hyperbolic geometry, Journal of the American Mathematical Society 1(3), 647 to 681 (1988)"
    locator: the diameter 2n - 10 of the flip graph of a convex polygon for large n
  - paper: "Ferran Hurtado, Marc Noy and Jorge Urrutia, Flipping edges in triangulations, Discrete and Computational Geometry 22(3), 333 to 346 (1999)"
    locator: the Θ(n^2) diameter for point sets and polygons, and the bound of (n - 4)/2 flippable edges
  - paper: "Francisco Santos, A point set whose space of triangulations is disconnected, Journal of the American Mathematical Society 13(3), 611 to 637 (2000)"
    locator: a point set in dimension 6 whose flip graph is disconnected
  - book: isbn:9783642129704
    title: Jesús A. De Loera, Jörg Rambau and Francisco Santos, Triangulations, Structures for Algorithms and Applications, Springer, 2010
    locator: Chapter 3 (flips in the plane) and Chapter 5 (secondary polytopes; chapter numbers to be checked)
---

The flip graph of a point set has one vertex for each [triangulation](/triangulation-of-point-set/) of the set, and an edge between two triangulations when one becomes the other by a single [edge flip](/edge-flip/): remove an edge whose two triangles form a convex quadrilateral and insert the other diagonal. In the plane the flip graph is always connected, so flips can turn any triangulation into any other. For a convex polygon it is the graph of a polytope, the associahedron, with $C_{n-2}$ vertices, and its diameter is $2n - 10$ for $n \ge 13$. Flip graphs are the setting for the [Lawson flip algorithm](/lawson-flip-algorithm/), for random sampling of triangulations, and for the [flip distance](/flip-distance/) problem.

## In plain words

Think of all the ways to cut a shape with fixed dots into triangles as the stations of a subway map. Two stations are joined by a line if you can go from one to the other by a single small move: pick two triangles that share a side and form a convex four-sided piece, erase the shared side, and draw the other diagonal of the piece.

The map is always in one piece in the plane: you can get from any cutting to any other by such moves. How many moves you need, and how hard it is to find the shortest route, are the main questions.

## The idea

**Definition.** Let $S$ be a finite set of points in the plane. The flip graph $\mathcal{F}(S)$ has the triangulations of $S$ as vertices, and $T T'$ is an edge when $T' = T - e + e'$ for an edge $e$ of $T$ and a segment $e'$; then $e$ and $e'$ are the two diagonals of a convex quadrilateral formed by the two triangles at $e$. The same definition works for the triangulations of a simple polygon, with only diagonals as edges. Two triangulations are adjacent exactly when their edge sets differ in one edge each.

**Connectivity.** Lawson proved in 1972 that $\mathcal{F}(S)$ is connected. A short proof uses the [Delaunay triangulation](/delaunay-triangulation/): from any triangulation, flip an edge that fails the [local Delaunay criterion](/local-delaunay-criterion/). Each flip lowers the lifted surface on the [paraboloid](/paraboloid-lifting-map/), so the process stops, and it stops only at a Delaunay triangulation. So every triangulation is joined to a Delaunay triangulation, and the Delaunay triangulations (several, if points are cocircular) are joined to each other by flips of cocircular quadrilaterals.

**Distances.** The distance between two triangulations in $\mathcal{F}(S)$ is their [flip distance](/flip-distance/). Going through the Delaunay triangulation gives a path of $O(n^2)$ flips, since each Lawson flip removes an edge that never comes back and there are $O(n^2)$ segments. Hurtado, Noy and Urrutia showed that $\Theta(n^2)$ is the right diameter in the worst case, for point sets and for simple polygons. For points in convex position the diameter is linear: $2n - 10$ for $n \ge 13$, by the [flip graph diameter theorem](/flip-graph-diameter-theorem/).

**Degrees.** The degree of a triangulation is its number of flippable edges. For $n$ points in convex position every diagonal is flippable, so the graph is $(n - 3)$-regular. In general, every triangulation of $n$ points has at least $\lceil (n - 4) / 2 \rceil$ flippable edges (Hurtado, Noy and Urrutia), and the bound is tight.

**Polytopes.** For a convex polygon, $\mathcal{F}$ is the 1-skeleton of the associahedron, an $(n - 3)$-dimensional polytope; its faces correspond to partial subdivisions by non-crossing diagonals. For a general point set, the flips between [regular triangulations](/regular-triangulation/) form the 1-skeleton of the secondary polytope of Gelfand, Kapranov and Zelevinsky, which is connected because every polytope graph is. Non-regular triangulations exist from 6 points in the plane, but in the plane they are joined by flips too.

**Higher dimensions.** Flips generalize to bistellar flips. Santos found in 2000 a set of points in dimension 6 whose flip graph is disconnected, and later examples in dimension 5. In dimensions 3 and 4 the question is open.

**Binary trees.** Rooting the [dual tree](/triangulation-dual-tree/) of a convex polygon triangulation turns it into a [binary tree](/binary-tree/), and a flip becomes a [tree rotation](/tree-rotation/). So the flip graph of a convex $(n + 2)$-gon is the rotation graph of binary trees with $n$ internal nodes.

## Examples

- **The convex quadrilateral.** Two triangulations, one edge: $\mathcal{F}$ is a single edge.
- **The convex pentagon.** Five triangulations, each with two flippable diagonals; $\mathcal{F}$ is a 5-cycle, the 2-dimensional associahedron, with diameter 2.
- **The convex hexagon.** 14 triangulations, each of degree 3, with 21 flip edges. The graph is the skeleton of the 3-dimensional associahedron and has diameter 4. For the convex heptagon: 42 vertices of degree 4, 84 edges, diameter 5. These values come from enumerating all triangulations by computer.
- **A point inside a square.** For $(0,0)$, $(4,0)$, $(4,4)$, $(0,4)$ and the inside point $(1,2)$ there are 3 triangulations, and $\mathcal{F}$ is a path of length 2: the middle triangulation has two flippable edges, the two ends one each. With the inside point at the center $(2,2)$ there is only one triangulation, since both diagonals pass through the point, and $\mathcal{F}$ is a single vertex.
- **A non-example.** Removing an edge whose two triangles form a non-convex quadrilateral does not give a flip, because the other diagonal lies outside. Such edges are not flippable, and they lower the degree.

## Where it is used

- **The Lawson flip algorithm.** It walks in $\mathcal{F}$ toward the Delaunay triangulation, which is the global maximum of the angle vector and the minimum of the lifted surface.
- **Optimization by local search.** Heuristics for the [minimum weight triangulation](/min-weight-triangulation/) and for data-dependent triangulations flip edges while the cost goes down. They can stop at local optima, since only the Delaunay criterion has no false local optima.
- **Counting and sampling.** Random walks on $\mathcal{F}$ sample triangulations of a convex polygon nearly uniformly; the mixing time of the walk on the associahedron is polynomial (McShine and Tetali). See [counting triangulations](/number-of-triangulations/).
- **Rotation distance.** The rotation distance of binary trees, studied for self-adjusting search trees, is the flip distance in a convex polygon.
- **Reconfiguration and hardness.** Computing the [flip distance](/flip-distance/) is NP-hard for point sets and for simple polygons, and open for convex polygons.

## References
