---
tag: PHQ54T
kind: problem
slug: euclidean-shortest-path-in-polygon
name: Euclidean shortest path in a polygon
aliases:
- shortest path in polygon
- geodesic path in polygon
- geodesic shortest path in a simple polygon
area: geometry/polygons
level: advanced
summary: Shortest path between two points inside a simple polygon, measured in Euclidean length.
prereqs: [simple-polygon, polygon-triangulation, triangulation-dual-tree]
see_also: [funnel-algorithm, euclidean-shortest-path, visibility-graph-of-polygon, visibility-graph, dijkstra, shortest-path-tree, watchman-route-problem, motion-planning]
sources:
  - paper: "Der-Tsai Lee and Franco P. Preparata, Euclidean shortest paths in the presence of rectilinear barriers, Networks 14(3), 1984, 393 to 410"
    locator: the funnel method for the shortest path between two points in a triangulated simple polygon, in linear time
  - paper: doi:10.1007/BF01840360
    title: Leonidas J. Guibas, John Hershberger, Daniel Leven, Micha Sharir and Robert E. Tarjan, Linear-time algorithms for visibility and shortest path problems inside triangulated simple polygons, Algorithmica 2, 1987, 209 to 233
    locator: the shortest path tree from one point to all vertices and the shortest path map, in linear time after triangulation
  - paper: "John Hershberger and Jack Snoeyink, Computing minimum length paths of a given homotopy class, Computational Geometry: Theory and Applications 4(2), 1994, 63 to 97"
    locator: the funnel as a deque, and its extension to paths of a fixed homotopy class
  - paper: "Leonidas J. Guibas and John Hershberger, Optimal shortest path queries in a simple polygon, Journal of Computer and System Sciences 39(2), 1989, 126 to 152"
    locator: O(log n) time distance queries between two arbitrary points after linear preprocessing
  - paper: doi:10.1007/BF02574703
    title: Bernard Chazelle, Triangulating a simple polygon in linear time, Discrete and Computational Geometry 6, 1991, 485 to 524
    locator: the linear time triangulation, which makes the whole shortest path computation linear
  - paper: "John Hershberger and Subhash Suri, An optimal algorithm for Euclidean shortest paths in the plane, SIAM Journal on Computing 28(6), 1999, 2215 to 2256"
    locator: the O(n log n) algorithm for polygonal domains with holes
---

The problem asks for the shortest curve between two points $s$ and $t$ that stays inside a [simple polygon](/simple-polygon/), with length measured in the Euclidean metric. Paths may touch the boundary. The answer is unique: a polygonal chain from $s$ to $t$ whose inner vertices are reflex vertices of the polygon, pulled tight around them. Its length is the *geodesic distance* between $s$ and $t$ in the polygon. After a [triangulation](/polygon-triangulation/), the [funnel algorithm](/funnel-algorithm/) of Lee and Preparata finds the path in linear time. With Chazelle's linear time triangulation the whole problem is solved in $\Theta(n)$ time. In a polygon with holes the shortest path is no longer unique in general. That harder case is the [Euclidean shortest path among obstacles](/euclidean-shortest-path/), solved in $O(n \log n)$ time.

## In plain words

Imagine a room with an odd shape seen from above, and a string tied at two points in it. Pull the string tight without letting it leave the room. The string takes the shortest way between the two points.

Where it can, the string runs straight. Where a corner of the wall sticks into the room, the string bends around that corner. It never bends anywhere else, and it never bends around a corner that points out of the room.

Because the room has no pillars, there is only one way around each obstacle. So the tight string is unique. To find it quickly, cut the room into triangles, follow the chain of triangles from one point to the other, and pull the string through the doorways between them one at a time.

## Definition

**Input.** A simple polygon $P$ with vertices $v_0, \ldots, v_{n-1}$, with exact coordinates, and two points $s$ and $t$ in the closed polygon, which may lie on its boundary.

**Output.** A polygonal path $s = p_0, p_1, \ldots, p_k = t$ contained in the closed polygon $P$, with the smallest Euclidean length $\sum_i |p_i p_{i+1}|$ among all paths in $P$ from $s$ to $t$. The length is the geodesic distance $d_P(s, t)$.

**Structure.** The shortest path is unique in a simple polygon. Each inner vertex $p_i$ is a reflex vertex of $P$, and the path turns at $p_i$ towards the polygon's exterior, wrapping around the vertex. The segment $s t$ is the answer exactly when it lies in $P$. Let $T_0, \ldots, T_m$ be the triangles on the path in the [dual tree](/triangulation-dual-tree/) of any triangulation, from a triangle containing $s$ to one containing $t$. They form the *sleeve*. The shortest path stays inside the sleeve and crosses the diagonals between consecutive triangles in order.

## Variants

- **One source, all targets.** The *shortest path tree* from $s$ to every vertex of $P$, and the *shortest path map*, which splits $P$ into regions with the same last vertex before the target. Guibas, Hershberger, Leven, Sharir and Tarjan compute both in linear time after triangulation.
- **Two-point queries.** Preprocess $P$ so that the geodesic distance between any two query points comes out quickly. Guibas and Hershberger achieve $O(\log n)$ time per query after $O(n)$ preprocessing. With their structure, the path itself comes out in additional time proportional to its number of vertices.
- **Fixed homotopy class.** In a domain with holes, the shortest path among those that go around the holes in a given way. Hershberger and Snoeyink reduce it to a funnel computation in a sleeve of the universal cover.
- **Polygons with holes.** The [Euclidean shortest path among obstacles](/euclidean-shortest-path/): there may be several locally shortest paths, and the global one is found from the [visibility graph](/visibility-graph/) or by continuous Dijkstra.
- **Other metrics.** Link distance (fewest segments), rectilinear paths in the $L_1$ metric, and weighted regions lead to different problems with different algorithms.
- **Higher dimensions.** Among polyhedral obstacles in three dimensions the problem is NP-hard. Canny and Reif proved this in 1987.

## Examples

**A U-shaped room.** Take $P = (0,0), (8,0), (8,6), (5,6), (5,2), (3,2), (3,6), (0,6)$, a rectangle with a notch cut from the top. From $s = (1, 5)$ in the left arm to $t = (7, 5)$ in the right arm, the segment $s t$ crosses the notch. The shortest path goes down and around the bottom of the notch: $(1,5), (3,2), (5,2), (7,5)$. It bends at the two reflex vertices $(3,2)$ and $(5,2)$ and has length $2 + 2\sqrt{13} \approx 9.21$.

**Visible endpoints.** In a convex polygon every pair of points sees each other, and the answer is always the segment $s t$. The same holds whenever the segment lies in $P$, even if it touches the boundary. In the L-shape $(0,0), (2,0), (4,0), (4,2), (3,2), (2,2), (2,3), (2,4), (0,4), (0,2)$, which has straight vertices, the segment from $(4,0)$ to $(0,4)$ passes exactly through the reflex corner $(2,2)$. It is the shortest path, with no bend. From $(4,2)$ to $(0,4)$ the segment leaves $P$ above the corner, and the path bends at $(2,2)$.

**Collinear reflex vertices.** In the comb $(0,0), (5,0), (5,3), (4,3), (4,1), (3,1), (3,3), (2,3), (2,1), (1,1), (1,3), (0,3)$ the path from $(0,3)$ to $(5,3)$ is $(0,3), (1,1), (4,1), (5,3)$. It runs along $y = 1$ through the vertices $(2,1)$ and $(3,1)$ without bending there. A correct algorithm reports the same length whether or not it lists such straight points.

**A spiral.** In a spiral-shaped polygon with $\Theta(n)$ turns, the shortest path from the center to the outside bends at $\Theta(n)$ reflex vertices. So any algorithm that outputs the path needs $\Omega(n)$ time.

## Known algorithms

| method | time | notes |
|---|---|---|
| [visibility graph](/visibility-graph-of-polygon/) and [Dijkstra](/dijkstra/) | $O(n^2 \log n)$, or $O(n^2)$ with a careful graph construction | simple; works with holes |
| [funnel algorithm](/funnel-algorithm/) (Lee and Preparata) | $O(n)$ after triangulation | one pair $s, t$; a [deque](/deque/) of two concave chains |
| shortest path tree (Guibas, Hershberger, Leven, Sharir and Tarjan) | $O(n)$ after triangulation | all vertices from one source; repeated funnel splits |
| query structure (Guibas and Hershberger) | $O(n)$ preprocessing, $O(\log n)$ per query | any two points |
| continuous Dijkstra (Hershberger and Suri) | $O(n \log n)$ | polygons with holes |

**The funnel method.** Triangulate $P$ and find the sleeve, the path of triangles between those containing $s$ and $t$, with a [breadth-first search](/breadth-first-search/) of the dual tree. The diagonals crossed by the sleeve, called *portals*, are met in order. The shortest paths from $s$ to the two endpoints of the current portal share a prefix up to a vertex called the apex. After the apex they split into two concave chains, which together with the portal bound the *funnel*. When the next portal is added, its new endpoint either cuts off part of its own chain, or crosses the other chain, and then the apex moves forward along that chain. The chains are a deque, and every vertex is pushed and popped at most once, so the work is linear in the size of the sleeve.

**Visibility graph.** The shortest path is a path in the graph on $s$, $t$ and the vertices of $P$ whose edges join pairs that see each other inside $P$. Dijkstra's algorithm on this graph finds it. The graph can have $\Theta(n^2)$ edges, and building it costs at least that much in the worst case. This is the method to use with holes when $n$ is small, and the standard oracle to test faster methods against.

## Bounds

- **Simple polygons.** $\Theta(n)$. The lower bound holds because the path can have $\Theta(n)$ vertices, as in a spiral. The upper bound uses Chazelle's linear time triangulation and the funnel. In practice the triangulation takes $O(n \log n)$ time or is given, and the funnel step is linear.
- **Polygons with holes.** $O(n \log n)$ time and space, by Hershberger and Suri, which matches the lower bound in the algebraic decision tree model.
- **Queries.** $O(\log n)$ per distance query after $O(n)$ preprocessing in a simple polygon.

## Reductions

- **To a sleeve.** Given a triangulation, the problem reduces in linear time to the shortest path inside a sleeve, a chain of triangles that touch along diagonals. This is the input of the funnel algorithm.
- **From the shortest path tree.** One source to all vertices contains the single-target problem, and a point $t$ is reached through the vertex whose region of the shortest path map contains it.
- **To shortest paths in graphs.** In any polygonal domain, the problem reduces to a [shortest path](/dijkstra/) in the visibility graph, because every inner vertex of a shortest path is a vertex of the domain.
- **Geodesic hull and related problems.** The relative convex hull of a set of points in $P$, the geodesic diameter and the geodesic center are built from shortest paths in $P$. The [watchman route](/watchman-route-problem/) uses them as a subroutine.

## Applications

- **Robot motion planning.** A point robot that moves inside a polygonal room, or a disk robot after the walls are moved inward by its radius, as in [motion planning](/motion-planning/).
- **Navigation meshes in games.** A level is cut into convex cells, [A*](/a-star-search/) finds a corridor of cells, and the funnel algorithm pulls the path tight through the portals between them. This is often called string pulling.
- **Wire routing.** Shortest connections that avoid obstacles in VLSI and printed circuit board layout.
- **Geodesic computations.** Geodesic distances inside a shape are used for shape descriptors and for clustering points that must stay inside a region.

## References
