---
tag: SZNCYY
kind: problem
slug: polygon-simplification
name: Polygon simplification
aliases:
- Simplifying polygons
- polyline simplification
- line simplification
- polygonal approximation
area: geometry/polygons
level: core
summary: Reducing the number of vertices of a polygon or polyline while keeping its shape within an allowed error.
prereqs: [polygon, point-to-segment-distance]
see_also: [ramer-douglas-peucker, visvalingam-whyatt, hausdorff-distance, frechet-distance, minimum-link-path, point-to-segment-distance, polygon-simplicity-test]
sources:
  - paper: doi:10.3138/FM57-6770-U75U-7727
    title: David H. Douglas and Thomas K. Peucker, Algorithms for the reduction of the number of points required to represent a digitized line or its caricature, The Canadian Cartographer 10(2), 112 to 122 (1973)
    locator: the recursive farthest-point method for a tolerance band
  - paper: "Hiroshi Imai and Masao Iri, Polygonal approximations of a curve, formulations and algorithms, in Computational Morphology, North-Holland, 71 to 86 (1988)"
    locator: the min-# and min-ε formulations, and the shortcut graph with a shortest path for the optimal subsequence
  - paper: "W. S. Chan and F. Chin, Approximation of polygonal curves with minimum number of line segments or minimum error, International Journal of Computational Geometry and Applications 6(1), 59 to 77 (1996)"
    locator: the O(n^2) construction of the shortcut graph and the O(n^2 log n) min-ε algorithm
  - paper: doi:10.1179/000870493786962263
    title: M. Visvalingam and J. D. Whyatt, Line generalisation by repeated elimination of points, The Cartographic Journal 30(1), 46 to 51 (1993)
    locator: the effective-area ranking of vertices and the removal of the smallest triangle
---

Polygon simplification asks for a polygon or polyline with fewer vertices that stays close to a given one. With $n$ input vertices and a tolerance $\varepsilon$, the **min-#** problem asks for the fewest vertices whose polyline is within $\varepsilon$, and the **min-ε** problem asks for the smallest error that $k$ vertices can achieve. The answer depends on how the error is measured: the distance of each dropped vertex to the segment that replaces it, the [Hausdorff distance](/hausdorff-distance/), or the [Fréchet distance](/frechet-distance/). The heuristics used in practice, [Ramer-Douglas-Peucker](/ramer-douglas-peucker/) and [Visvalingam-Whyatt](/visvalingam-whyatt/), are fast but not optimal; the exact min-# problem over subsequences is a shortest path in a graph of allowed shortcuts (Imai and Iri), in $O(n^2)$ time after the work of Chan and Chin. Keeping a closed polygon simple, or a map of many polygons consistent, makes the problem much harder.

## In plain words

A coastline traced from a satellite image may have a million corners, far more than a map on a phone needs. You want to draw it with fewer corners, but without moving any part of the line by more than a set distance.

One way keeps only some of the original corners and connects them by straight lines. Each straight line skips some corners, and it is allowed only if every skipped corner is close enough to it. Among all allowed choices you may want the one with the fewest corners. Quick methods pick corners greedily, for example by keeping the corner farthest from a straight line and repeating on both halves, and they usually give a good answer, but not always the smallest.

## Definition

**Input.** A polyline $P = (v_0, \ldots, v_{n-1})$ in the plane, or a closed [polygon](/polygon/), and a tolerance $\varepsilon > 0$ (or a vertex budget $k$).

**Output.** A polyline $Q = (v_{i_0}, v_{i_1}, \ldots, v_{i_{m-1}})$ with $0 = i_0 < i_1 < \cdots < i_{m-1} = n - 1$, a subsequence of the vertices of $P$ that keeps the end points, such that the error of $Q$ with respect to $P$ is at most $\varepsilon$, and $m$ is as small as possible (min-#). In the min-ε version, $m \le k$ is fixed and the error is minimized.

**Error measures.** For one shortcut $v_i v_j$ with $i < j$:

- **Tolerance zone.** Every vertex $v_l$ with $i < l < j$ is within distance $\varepsilon$ of the segment $v_i v_j$ ([point to segment distance](/point-to-segment-distance/)). As the zone around a segment is convex, the whole piece of $P$ between $v_i$ and $v_j$ then lies in it, so this is the one-sided Hausdorff distance from that piece to the segment.
- **Hausdorff.** The two-sided [Hausdorff distance](/hausdorff-distance/) between the piece and the segment.
- **Fréchet.** The [Fréchet distance](/frechet-distance/) between the piece and the segment, which also respects the order along the curve, so a shortcut cannot skip a part that doubles back.

The error of $Q$ is the maximum over its shortcuts (the local version). Global versions compare all of $P$ with all of $Q$ at once.

**Model.** The [real RAM](/real-ram/). On integer input every test compares squared distances, which are rational, so the decisions are exact.

**Degenerate input.** Repeated vertices are removed first. Collinear vertices are always dropped by an optimal solution, since a shortcut through them has error 0.

## Variants

- **Vertices not restricted.** The output vertices may be any points, not only input vertices. Under the tolerance-zone criterion this is a [minimum link path](/minimum-link-path/) problem inside the $\varepsilon$-neighborhood of $P$, which Guibas, Hershberger, Mitchell and Snoeyink solved in near-linear time for several error measures.
- **Closed polygons.** The start vertex is free. Trying every start multiplies the time by $n$; one can also fix one vertex that every good solution must keep, for example a vertex far from all others.
- **Preserving simplicity.** The output must again be a [simple polygon](/simple-polygon/), and for a map with several polygons the outputs must not cross each other or move a point, such as a city, to the wrong side. Both [Ramer-Douglas-Peucker](/ramer-douglas-peucker/) and [Visvalingam-Whyatt](/visvalingam-whyatt/) can create self-intersections; the result can be tested with a [polygon simplicity test](/polygon-simplicity-test/).
- **Area-based measures.** [Visvalingam-Whyatt](/visvalingam-whyatt/) removes the vertex whose triangle with its two neighbors has the smallest area, which controls the area change instead of the distance.
- **Streaming.** For GPS tracks, the simplification is computed online with a window of recent points.
- **Higher dimensions.** The same problems for curves in $\mathbb{R}^3$ and for trajectories with time stamps.

## Examples

Take $P = (0,2), (2,2), (4,3), (6,3), (8,0), (10,0)$ with the tolerance-zone criterion and $\varepsilon = 1$; distances are compared through their squares.

- **Ramer-Douglas-Peucker.** The chord $(0,2)\text{--}(10,0)$ has farthest vertex $(6,3)$, at squared distance $\frac{121}{26} > 1$, so it is kept. On the left, the chord $(0,2)\text{--}(6,3)$ has both $(2,2)$ and $(4,3)$ at squared distance $\frac{4}{37}$, so they are dropped. On the right, $(8,0)$ is at squared distance $\frac{36}{25} > 1$ from $(6,3)\text{--}(10,0)$ and is kept. The output $(0,2), (6,3), (8,0), (10,0)$ has 4 vertices.
- **Optimal.** $(0,2), (4,3), (10,0)$ has 3 vertices and is allowed: $(2,2)$ is at squared distance $\frac{4}{17}$ from $(0,2)\text{--}(4,3)$, and $(6,3)$ and $(8,0)$ are both at squared distance $\frac45$ from $(4,3)\text{--}(10,0)$. No 2-vertex output works, since $(6,3)$ is too far from the full chord. So the greedy split at the farthest vertex can lose.
- **Collinear points.** $(0,0), (1,0), (2,0), (3,1)$ simplifies to $(0,0), (2,0), (3,1)$ for every $\varepsilon \ge 0$.

## Known algorithms

| algorithm | output | time | notes |
| --- | --- | --- | --- |
| [Ramer-Douglas-Peucker](/ramer-douglas-peucker/), 1972 and 1973 | subsequence, tolerance zone | $O(n^2)$ worst, $O(n \log n)$ on balanced splits | split at the farthest vertex and recurse; not optimal; Hershberger and Snoeyink gave an $O(n \log n)$ worst-case implementation |
| [Visvalingam-Whyatt](/visvalingam-whyatt/), 1993 | subsequence, area criterion | $O(n \log n)$ | remove the vertex of smallest effective area, kept in a heap |
| radial distance, perpendicular distance, Reumann-Witkam | subsequence | $O(n)$ | one pass with simple local rules; crude |
| Imai and Iri, 1988 | optimal subsequence | $O(n^3)$ directly, $O(n^2)$ with the construction of Chan and Chin | the shortcut graph has an arc $i \to j$ when $v_i v_j$ is within $\varepsilon$; a breadth-first search from $v_0$ to $v_{n-1}$ gives the fewest vertices |
| min-ε by search over candidate errors | optimal subsequence | $O(n^2 \log n)$ (Chan and Chin) | the optimal error is one of $O(n^2)$ critical values, found by binary search with the min-# test |
| [minimum link path](/minimum-link-path/) in the $\varepsilon$-tube | free vertices | near-linear | Guibas, Hershberger, Mitchell and Snoeyink, 1993 |

**The shortcut graph.** For each pair $i < j$, the arc $i \to j$ exists when every $v_l$ with $i < l < j$ lies within $\varepsilon$ of the segment $v_i v_j$. A path from $0$ to $n - 1$ is exactly an allowed simplification, with one vertex per node, so the shortest path in arcs is a min-# solution. Testing all pairs directly costs $O(n)$ per pair; Chan and Chin compute all arcs leaving $v_i$ in $O(n)$ total by keeping the interval of directions from $v_i$ whose rays pass within $\varepsilon$ of all vertices seen so far, which shrinks as $j$ grows, and doing the same from the other end of each shortcut; an arc exists when both tests pass.

## Bounds

- **Lower bound.** $\Omega(n)$, since every vertex can decide whether a shortcut is allowed. No better general lower bound is known for min-# over subsequences.
- **Upper bounds.** $O(n^2)$ for min-# under the tolerance-zone criterion and $O(n^2 \log n)$ for min-ε, by the shortcut graph; the graph can have $\Theta(n^2)$ arcs, for example on a nearly straight polyline, so methods that build it are quadratic.
- **Greedy quality.** Ramer-Douglas-Peucker and Visvalingam-Whyatt have no constant-factor guarantee on the number of vertices for a given error; the example above loses one vertex out of three.
- **Preserving simplicity.** Finding the fewest vertices for a set of polygons or polylines so that the simplified ones stay simple and do not cross each other is NP-hard (Estkowski and Mitchell, 2001).

## Reductions

- **Min-# to shortest path.** The shortcut graph is a directed acyclic graph, so the min-# problem over subsequences is a breadth-first search, and weighted versions, such as minimizing a sum of errors, are shortest paths in the same DAG.
- **Min-ε to min-#.** Binary search on $\varepsilon$ over the critical values, with min-# as the test.
- **Free vertices to minimum link paths.** With output vertices anywhere, simplification under the tolerance criterion is a [minimum link path](/minimum-link-path/) in the $\varepsilon$-neighborhood of the curve.
- **Validation.** Checking that a simplified polygon is still simple is the [polygon simplicity test](/polygon-simplicity-test/).

## Applications

- **Cartography and GIS.** Map generalization: drawing coastlines, borders and roads with fewer points at smaller scales. Ramer-Douglas-Peucker and Visvalingam-Whyatt are the standard tools, built into GIS libraries and map tile servers.
- **GPS tracks and trajectories.** Compressing a recorded track while keeping it within a known error.
- **Vector graphics and fonts.** Reducing the points of traced outlines and digitized curves.
- **Rendering and games.** Levels of detail for outlines and collision polygons.
- **Computer vision.** Approximating contours extracted from images by polygons with few sides, for example to detect quadrilaterals.

## References
