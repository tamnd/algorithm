---
tag: DZDF4M
kind: problem
slug: minimum-link-path
name: Minimum link path
aliases:
- minimum-link path problem
- minimum-bend path
- link distance
- minimum turn path
area: geometry/geometric-optimization
level: advanced
summary: Find a polygonal path between two points of a polygon with the fewest segments (links). Linear time in a simple polygon after triangulation; harder among holes.
prereqs: [simple-polygon, visibility-polygon, polygon-triangulation, breadth-first-search]
see_also: [euclidean-shortest-path, lee-preparata-algorithm, funnel-algorithm, visibility-graph, euclidean-shortest-path-in-polygon, curve-simplification, rectilinear-polygon, watchman-route-problem]
sources:
  - paper: "Subhash Suri, A linear time algorithm for minimum link paths inside a simple polygon, Computer Vision, Graphics, and Image Processing 35(1), 1986"
    locator: the window partition of a simple polygon from a source point and the O(n) time algorithm after triangulation
  - paper: "Subir Kumar Ghosh, Computing the visibility polygon from a convex set and related problems, Journal of Algorithms 12(1), 1991"
    locator: an independent linear time minimum link path algorithm in a simple polygon, by weak visibility from convex sets
  - paper: "Joseph S. B. Mitchell, Günter Rote and Gerhard Woeginger, Minimum-link paths among obstacles in the plane, Algorithmica 8, 1992"
    locator: the algorithm for polygonal domains with holes, in time near the size of the visibility graph, and the Ω(n log n) lower bound
  - paper: "Simon Kahan and Jack Snoeyink, On the bit complexity of minimum link paths: superquadratic algorithms for problems solvable in linear time, Computational Geometry: Theory and Applications 12(1-2), 1999"
    locator: the turning points of minimum link paths may need many more bits than the input, so exact implementations cost more than the linear number of arithmetic operations
  - paper: "Leonidas J. Guibas, John Hershberger, Joseph S. B. Mitchell and Jack Snoeyink, Approximating polygons and subdivisions with minimum-link paths, International Journal of Computational Geometry and Applications 3(4), 1993"
    locator: minimum link paths inside a tolerance region as a tool for curve simplification
  - paper: "Joseph S. B. Mitchell, Shortest paths and networks, in Handbook of Discrete and Computational Geometry, 3rd edition, CRC Press, 2017"
    locator: the section on minimum link paths (simple polygons, domains with holes, rectilinear and higher dimensional versions)
---

The minimum link path problem asks for a polygonal path between two points $s$ and $t$ inside a polygon that has the fewest segments, or *links*. The number of links is the *link distance* $d_L(s, t)$. It measures paths by their turns, not by their length: a robot that is fast on straight lines but slow to turn, or a chain of line-of-sight radio relays, wants few links. In a [simple polygon](/simple-polygon/), Suri (1986) and Ghosh (1991) found minimum link paths in $O(n)$ time after [triangulation](/polygon-triangulation/), by growing regions of points at link distance $1, 2, 3, \ldots$ from $s$. Among polygonal holes the problem is harder, and Mitchell, Rote and Woeginger (1992) gave an algorithm near the size of the [visibility graph](/visibility-graph/). The minimum link path is in general not the [shortest path](/euclidean-shortest-path-in-polygon/).

## In plain words

You must walk from one point of a room to another along straight lines, and each time you change direction costs you. You want the route with the fewest straight pieces. Its length does not matter.

Everything you can see from the start is one straight piece away. Everything you can see from some point of that region is two pieces away, and so on. The rooms grow outward in rings, and the number of the ring that contains the goal is the answer.

To build the route, go back from the goal: choose a point in the previous ring that sees the goal, then a point in the ring before that, until you reach the start.

The shortest route bends around corners as tightly as it can; the route with fewest bends can cut wide, longer diagonals instead.

## Definition

Notation: $P$ is a closed polygonal domain with $n$ vertices, either a simple polygon or a polygon with holes. A *link path* from $s$ to $t$ is a polygonal path $s = p_0, p_1, \ldots, p_k = t$ whose segments lie in $P$; its *link length* is $k$. Two points *see* each other if the closed segment between them lies in $P$; segments may touch the boundary.

**Input.** $P$ and two points $s, t \in P$.

**Output.** A link path from $s$ to $t$ with the least link length $d_L(s, t)$.

**Regions of equal link distance.** Let $V_0 = \{s\}$ and let $V_{k+1}$ be the set of points of $P$ that see some point of $V_k$. Then $V_1$ is the [visibility polygon](/visibility-polygon/) of $s$, $V_0 \subseteq V_1 \subseteq V_2 \subseteq \cdots$, and $d_L(s, t)$ is the least $k$ with $t \in V_k$. A path is rebuilt backward: $p_k = t$, and $p_{j-1}$ is any point of $V_{j-1}$ that sees $p_j$. In a simple polygon each $V_{k+1} \setminus V_k$ is cut off from $V_k$ by chords called *windows*, and these windows form the *window partition* of $P$ from $s$. The turning points of a minimum link path need not be vertices of $P$; they can lie on windows, at points constructed from the input.

The link distance satisfies the triangle inequality and is a metric on $P$. In a connected domain it is finite. It is invariant under invertible affine maps of the plane, because these map segments to segments.

No general position is assumed. Paths may run along edges and through vertices. Some authors require the inner turning points to be proper turns; this changes nothing, because a straight turning point can be removed and the link length only drops.

## Variants

- **Rectilinear links.** Every link must be horizontal or vertical. This is the minimum bend problem of VLSI wire routing among rectilinear obstacles.
- **Domains with holes.** The regions $V_k$ are no longer separated by single windows, and the problem needs different methods.
- **Link diameter and radius.** The largest link distance between two points of $P$, and the point that minimizes the largest link distance to all others.
- **Queries.** Preprocess $P$ so that the link distance between any two query points is reported fast.
- **Bicriteria paths.** Among paths with $k$ links find the shortest, or trade length against links.
- **Curve simplification.** Given a polygonal curve and a tolerance, find a path with the fewest links that stays within the tolerance of the curve, a form of [curve simplification](/curve-simplification/).
- **Higher dimensions.** Minimum link paths among polyhedral obstacles in space, which are much harder.

## Examples

**Link path versus shortest path.** In the U-shaped polygon $(0,0), (8,0), (8,6), (5,6), (5,2), (3,2), (3,6), (0,6)$, with $s = (1,5)$ in the left arm and $t = (7,5)$ in the right arm, the segment $st$ crosses the notch between the arms, so $d_L(s, t) \ge 2$. The point $x = (4, 1/2)$ sees both: the segment $sx$ passes exactly through the corner $(3, 2)$, and the segment $xt$ through the corner $(5, 2)$. So $d_L(s, t) = 2$, with the path $s, x, t$ of length $2\sqrt{(3)^2 + (9/2)^2} = 3\sqrt{13} \approx 10.82$. The shortest path is $s, (3,2), (5,2), t$, of length $2 + 2\sqrt{13} \approx 9.21$ and with 3 links. So neither path is optimal for the other measure.

**Many links.** In a spiral polygon whose corridor winds around many times, each link covers only a bounded part of a turn, so $d_L(s, t)$ grows linearly with $n$. Link distances range from 1 (when $s$ sees $t$) to $\Theta(n)$.

**Convex and star-shaped polygons.** In a convex polygon every link distance is at most 1. In a [star-shaped polygon](/star-shaped-polygon/) it is at most 2: go through a point of the [kernel](/polygon-kernel/).

## Known algorithms

| setting | algorithm | time |
|---|---|---|
| simple polygon, from $s$ to $t$ | Suri (1986), window partition | $O(n)$ after triangulation |
| simple polygon, from $s$ to $t$ | Ghosh (1991), visibility from convex sets | $O(n)$ after triangulation |
| simple polygon, link diameter | Suri | $O(n \log n)$ |
| polygon with holes | Mitchell, Rote and Woeginger (1992) | $O(E\, \alpha(n) \log^2 n)$, with $E$ the size of the visibility graph |
| rectilinear links among rectilinear obstacles | several authors | $O(n \log n)$ |

With [Chazelle's linear time triangulation](/chazelle-polygon-triangulation/), the simple polygon case takes $\Theta(n)$ arithmetic operations. These bounds count arithmetic operations on reals. Kahan and Snoeyink (1999) showed that the turning points may need many more bits than the input coordinates, so with exact rational arithmetic the bit cost is higher than the operation count suggests.

## Bounds

- **Simple polygon.** $\Theta(n)$ in the real RAM, after or including the triangulation, since the input must be read.
- **Holes.** Mitchell, Rote and Woeginger prove an $\Omega(n \log n)$ lower bound for domains with holes, in the algebraic decision tree model.
- **Link distance and shortest path.** The two measures differ: in the example the shortest path has 3 links and the minimum link path has 2. The gap can be as large as one likes: a shortest path that wraps around a long chain of reflex vertices bends at each of them, while a path with 2 links can pass wide of the chain.
- **Bit size.** With integer input of $b$ bits, the turning points of a minimum link path can need a number of bits that grows with the number of links, not only with $b$.

## Reductions

- **To breadth-first search on regions.** The rings $V_1, V_2, \ldots$ are a [breadth-first search](/breadth-first-search/) in which each step replaces a region by the set of points it sees.
- **Visibility graph for links at vertices.** If turning points must be polygon vertices, the problem becomes breadth-first search on the visibility graph, which gives an upper bound on $d_L$ but not always the true value.
- **Rectilinear version.** Minimum bend rectilinear paths reduce to shortest paths in a graph of horizontal and vertical segments through the obstacle vertices.

## Applications

- **Robot motion.** Robots that move fast in a straight line but must stop to turn, as in [motion planning](/motion-planning/) with costly rotations.
- **Line-of-sight networks.** The number of relay stations needed between two points in a region with walls is $d_L - 1$.
- **Wire routing.** Few bends in wires on circuits and printed boards.
- **Curve and map simplification.** A polyline with the fewest segments inside a tolerance band around a curve.
- **Watchman and guard routes.** Link distance appears in [watchman route](/watchman-route-problem/) variants that charge per turn.

## References
