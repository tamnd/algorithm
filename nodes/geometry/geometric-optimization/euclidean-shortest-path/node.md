---
tag: QQ56JG
kind: problem
slug: euclidean-shortest-path
name: Euclidean shortest path among obstacles
aliases:
- geodesic shortest path in a polygon
- shortest path among polygonal obstacles
- Euclidean shortest path problem
area: geometry/geometric-optimization
level: core
summary: Find the shortest path between two points in the plane that avoids polygonal obstacles. It bends only at obstacle corners. O(n log n) time, or O(n + h log h) for h obstacles after a triangulation.
prereqs: [polygon-with-holes, euclidean-distance, single-source-shortest-paths]
see_also: [visibility-graph, euclidean-shortest-path-in-polygon, lee-preparata-algorithm, funnel-algorithm, minimum-link-path, motion-planning, shortest-path-tree, dijkstra]
sources:
  - book: isbn:9783540779735
    title: Mark de Berg, Otfried Cheong, Marc van Kreveld and Mark Overmars, Computational Geometry, Algorithms and Applications, third edition, Springer, 2008
    locator: Chapter 15, Sections 15.1 and 15.2 (shortest paths are polygonal paths through obstacle vertices; the visibility graph method)
  - paper: doi:10.1137/S0097539795289604
    title: John Hershberger and Subhash Suri, An optimal algorithm for Euclidean shortest paths in the plane, SIAM Journal on Computing 28(6), 1999
    locator: the shortest path map by continuous Dijkstra in O(n log n) time and space
  - paper: doi:10.1145/3580475
    title: Haitao Wang, A new algorithm for Euclidean shortest paths in the plane, Journal of the ACM 70(2), 2023
    locator: the abstract (O(n + h log h) time and O(n) space after a triangulation of the free space, and the matching lower bound)
  - paper: "Der-Tsai Lee and Franco P. Preparata, Euclidean shortest paths in the presence of rectilinear barriers, Networks 14(3), 1984, 393 to 410"
    locator: the linear-time funnel method for a shortest path in a triangulated simple polygon
  - paper: "John Canny and John Reif, New lower bound techniques for robot motion planning problems, 28th IEEE Symposium on Foundations of Computer Science (FOCS 1987)"
    locator: NP-hardness of shortest paths among polyhedral obstacles in three dimensions
  - paper: "Joseph S. B. Mitchell, Shortest paths among obstacles in the plane, International Journal of Computational Geometry and Applications 6(3), 1996"
    locator: the continuous Dijkstra method with O(n) space and subquadratic time
---

The Euclidean shortest path problem asks for the shortest path between two points $s$ and $t$ in the plane that does not enter the interior of any of a set of polygonal obstacles. A shortest path is a polygonal chain that bends only at obstacle vertices, so it can be found as a shortest path in the [visibility graph](/visibility-graph/), in $O(n^2 \log n)$ time for $n$ obstacle vertices. Hershberger and Suri (1999) solve it in $O(n \log n)$ time with the continuous Dijkstra method, and Wang (2023) in $O(n + h \log h)$ time after triangulation, where $h$ is the number of obstacles. Inside one simple polygon it takes $O(n)$ time by the [funnel method](/funnel-algorithm/). In three dimensions the problem is [NP-hard](/np-hard/).

## In plain words

You want to walk from one spot to another across a field with fenced areas you cannot enter. You may walk along a fence and touch its corners. What is the shortest walk?

Pull a string tight from the start to the goal, around the fenced areas. The string goes straight until it hits a fence corner, wraps around that corner, and goes straight again. So the shortest walk is made of straight pieces that meet only at fence corners.

The simple method lists which corners can see each other and runs a usual shortest route search on that list. Faster methods spread a wave out from the start, like a ripple on water that flows around the fences, and record when the wave first reaches each place.

## Definition

Notation: a polygonal domain $D$ is a closed region of the plane bounded by an outer simple polygon and $h$ disjoint simple polygonal holes inside it, a [polygon with holes](/polygon-with-holes/); the obstacles are the holes, and the outer boundary may be omitted. $n$ is the total number of vertices. A path is feasible when it lies in $D$; it may run along the boundary. $|\pi|$ is the Euclidean length of a path $\pi$, and $d(s, t)$ is the smallest length of a feasible path from $s$ to $t$, the geodesic distance.

**Input.** The domain $D$, given by its boundary polygons, and two points $s, t \in D$.

**Output.** $d(s, t)$ and a feasible path of that length, as a list of vertices.

**Structure of a solution.** A shortest path exists, and every shortest path is a polygonal chain whose inner vertices are vertices of $D$. More precisely, each inner vertex is a vertex where the path turns around the boundary: at a vertex of a hole the path bends toward the hole, and at a vertex of the outer polygon it bends toward the outside. Each segment of the chain lies in $D$, so it is an edge of the visibility graph on $s$, $t$ and the vertices of $D$. The proof is on the [visibility graph](/visibility-graph/) page.

General position is not needed. The path may be unique or not: with symmetric obstacles there can be several shortest paths. Model: real RAM. The lengths are sums of square roots, and comparing two such sums exactly is not known to be possible in polynomial time in the bit model, so exact algorithms are stated on the real RAM.

## Variants

- **Inside a simple polygon** ($h = 0$). The [Euclidean shortest path in a polygon](/euclidean-shortest-path-in-polygon/) is unique and takes $O(n)$ time after triangulation, by the [Lee-Preparata algorithm](/lee-preparata-algorithm/).
- **Single source, all targets.** The shortest path map from $s$ divides $D$ into $O(n)$ regions in which the path to $t$ has the same sequence of vertices; it answers each query $d(s, t)$ in $O(\log n)$ time. The [shortest path tree](/shortest-path-tree/) from $s$ to all vertices is its combinatorial core.
- **Two-point queries.** Preprocess $D$ so that $d(s, t)$ for any two points is answered quickly; inside a simple polygon this takes $O(\log n)$ time per query after linear preprocessing (Guibas and Hershberger 1989).
- **Fewest turns.** The [minimum link path](/minimum-link-path/) minimizes the number of segments instead of the length.
- **Other metrics.** In the $L_1$ metric with axis-parallel obstacles the problem is a rectilinear routing problem. In the weighted region problem each face has a cost per unit length, and the path refracts at face boundaries by Snell's law.
- **A robot with a shape.** A polygonal robot that translates is reduced to a point by growing the obstacles in the [configuration space](/configuration-space/), as in [motion planning](/motion-planning/).
- **Three dimensions.** Among polyhedral obstacles a shortest path bends on edges, at points that are not vertices; the problem is NP-hard (Canny and Reif 1987), and approximation schemes exist.

## Examples

**One square.** The obstacle is the square $(3, -2), (7, -2), (7, 2), (3, 2)$, with $s = (0, 0)$ and $t = (10, 0)$. The segment $st$ crosses the square. The path $(0, 0), (3, 2), (7, 2), (10, 0)$ has length $\sqrt{13} + 4 + \sqrt{13} \approx 11.2111$, and so does its mirror image below the square. Both are shortest, so the shortest path is not unique.

**Two obstacles.** With the triangle $(2, 1), (5, 0), (4, 4)$, the square $(6, 2), (8, 2), (8, 6), (6, 6)$, $s = (0, 0)$ and $t = (10, 4)$, the shortest path is $(0, 0), (5, 0), (8, 2), (10, 4)$ of length $5 + \sqrt{13} + \sqrt{8} \approx 11.4340$. It bends at a corner of each obstacle. The [visibility graph](/visibility-graph/) page builds the graph for this example.

**Inside an L-shaped polygon.** In the polygon $(0, 0), (8, 0), (8, 2), (2, 2), (2, 8), (0, 8)$, from $s = (7, 1)$ to $t = (1, 7)$, the segment $st$ leaves the polygon. The path wraps around the reflex vertex $(2, 2)$: $(7, 1), (2, 2), (1, 7)$, of length $2\sqrt{26} \approx 10.198$.

## Known algorithms

| method | time | space | notes |
|---|---|---|---|
| [visibility graph](/visibility-graph/) by rotational sweep, then [Dijkstra](/dijkstra/) | $O(n^2 \log n)$ | $O(n^2)$ | Lee 1978; the textbook method |
| visibility graph in $O(n^2)$ (Welzl 1985; Asano et al. 1986), then Dijkstra with a Fibonacci heap | $O(n^2)$ | $O(n^2)$ | |
| output-sensitive visibility graph (Ghosh and Mount 1991), then Dijkstra | $O(n \log n + m)$ | $O(m)$ | $m$ is the number of visibility edges |
| continuous Dijkstra (Mitchell 1996) | subquadratic | $O(n)$ | |
| shortest path map by continuous Dijkstra (Hershberger and Suri 1999) | $O(n \log n)$ | $O(n \log n)$ | answers later queries from $s$ in $O(\log n)$ |
| Wang (2023) | $O(n + h \log h)$ after triangulating $D$ | $O(n)$ | |
| inside a simple polygon: triangulation, then the [funnel algorithm](/funnel-algorithm/) | $O(n)$ | $O(n)$ | Lee and Preparata 1984; Chazelle's triangulation |

**Continuous Dijkstra.** The method simulates a wavefront that leaves $s$ at unit speed. At time $\tau$ the front is the set of points at geodesic distance $\tau$; it is a union of circular arcs centered at $s$ and at vertices that the front has wrapped around. The algorithm processes only the events where the combinatorial structure of the front changes, such as hitting a vertex or the collision of two arcs. The result is the shortest path map.

## Bounds

- **Lower bound.** Wang (2023) states that $O(n + h \log h)$ is optimal for the problem, by a lower bound of $\Omega(n + h \log h)$. With $h = \Theta(n)$ this is $\Omega(n \log n)$, so the Hershberger-Suri bound is also optimal in that case.
- **Size of the answer.** A shortest path has at most $n + 1$ segments, since it visits each vertex at most once, and in a spiral polygon it has $\Theta(n)$ segments. The visibility graph can have $\Theta(n^2)$ edges, so methods that build it cannot beat $\Theta(n^2)$ time in the worst case.
- **Three dimensions.** NP-hard among polyhedra (Canny and Reif 1987), by a reduction from 3-SAT in which the number of combinatorially different shortest path candidates is exponential.
- **Exact lengths.** Deciding whether one sum of square roots of integers is smaller than another is not known to be in polynomial time in the bit model, so even comparing two candidate paths exactly is a problem outside the real RAM.

## Reductions

- **To graph shortest paths.** The structure theorem reduces the problem to [single-source shortest paths](/single-source-shortest-paths/) on the visibility graph of $s$, $t$ and the vertices of $D$.
- **To the simple polygon case.** Inside one simple polygon the triangulation's dual tree fixes the sequence of triangles the path crosses, and the funnel method finds the path in that sleeve in linear time.
- **From translational motion planning.** A convex polygonal robot that translates among polygonal obstacles reduces to a point among the Minkowski sums of the obstacles with the reflected robot.

## Applications

- **Robot motion planning.** Shortest collision-free routes for a mobile robot on a map of obstacles.
- **Games and navigation.** Path finding for characters on a navigation mesh, where a channel of triangles is found by graph search and then pulled taut by the funnel method.
- **Wire routing.** Shortest connections that avoid blocked areas on a chip or a circuit board, often in the $L_1$ metric.
- **Geographic information systems.** Distances that respect lakes, buildings or no-go zones, and geodesic distance as a basis for geodesic Voronoi diagrams and centers.

## References
