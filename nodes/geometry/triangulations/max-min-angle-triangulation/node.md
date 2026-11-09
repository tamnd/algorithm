---
tag: K3BW8C
kind: problem
slug: max-min-angle-triangulation
name: Max-min angle triangulation
aliases:
- Maximum minimum angle triangulation
- angle-optimal triangulation
- equiangular triangulation
area: geometry/triangulations
level: core
summary: Find a triangulation of a point set whose smallest angle is as large as possible.
model: real-ram
complexity:
  vars: {n: the number of points}
  time: {worst: Θ(n log n)}
prereqs: [triangulation-of-point-set, delaunay-triangulation, edge-flip]
see_also: [delaunay-max-min-angle, lawson-flip-algorithm, local-delaunay-criterion, constrained-delaunay-triangulation, min-weight-triangulation, greedy-triangulation, mesh-generation, flip-graph]
sources:
  - book: isbn:9783540779735
    title: Mark de Berg, Otfried Cheong, Marc van Kreveld and Mark Overmars, Computational Geometry, Algorithms and Applications, third edition, Springer, 2008
    locator: Chapter 9, Sections 9.1 (triangulations of planar point sets, angle-optimal triangulations, edge flips) and 9.2 (the Delaunay triangulation is angle-optimal)
  - paper: "Robin Sibson, Locally equiangular triangulations, The Computer Journal 21(3), 243 to 245 (1978)"
    locator: a triangulation in which every edge is locally optimal for the angles is the Delaunay triangulation
  - paper: "Charles L. Lawson, Software for C1 surface interpolation, in Mathematical Software III, Academic Press, 161 to 194 (1977)"
    locator: the max-min angle criterion and edge flips toward it (pages to be checked)
  - paper: "Herbert Edelsbrunner, Tiow Seng Tan and Roman Waupotitsch, An O(n^2 log n) time algorithm for the minmax angle triangulation, SIAM Journal on Scientific and Statistical Computing 13(4), 994 to 1008 (1992)"
    locator: the edge insertion method for minimizing the largest angle
  - book: isbn:9781584887300
    title: Siu-Wing Cheng, Tamal K. Dey and Jonathan Richard Shewchuk, Delaunay Mesh Generation, CRC Press, 2012
    locator: Chapter 2, Two-dimensional Delaunay triangulations (the max-min angle property; ISBN to be checked)
---

The max-min angle triangulation problem asks, for a finite set of points in the plane, for a triangulation whose smallest angle is as large as possible. Small angles make thin triangles, which are bad for interpolation and for finite element methods, so this is the most basic quality criterion for a triangulation. The problem has a clean answer: the [Delaunay triangulation](/delaunay-triangulation/) is optimal. It even maximizes the whole sorted list of angles lexicographically, and it can be computed in $\Theta(n \log n)$ time. The proof, by [edge flips](/edge-flip/), is on the page [Delaunay triangulation maximizes the minimum angle](/delaunay-max-min-angle/).

## In plain words

There are many ways to connect a set of dots into triangles. Some ways make thin, needle-like triangles with a tiny corner. Others make fatter triangles. The goal is to choose the way in which the sharpest corner of all the triangles is as blunt as possible.

For four dots in convex position there are only two choices: one diagonal or the other. The better choice is the one where neither triangle has the fourth dot inside the circle through its three corners. Fixing every group of four in this way, one at a time, ends at the best answer for the whole set, and this best answer is the well-known Delaunay triangulation.

## Definition

**Input.** A set $S$ of $n$ points in the plane, not all on one line.

**Output.** A [triangulation](/triangulation/) $T$ of $S$ that maximizes $\alpha(T)$, the smallest interior angle over all triangles of $T$.

**Angle vector.** For a triangulation with $t$ triangles, let $A(T) = (\alpha_1, \ldots, \alpha_{3t})$ be its angles in increasing order. All triangulations of $S$ have the same $t = 2n - h - 2$, where $h$ is the number of points on the hull boundary, so the vectors can be compared lexicographically. A triangulation is **angle-optimal** if its vector is lexicographically largest. An angle-optimal triangulation maximizes $\alpha(T)$, then the second smallest angle, and so on.

**Exact comparison.** Angles need not be computed. Two angles $\angle(u, v)$ and $\angle(u', v')$ between integer vectors compare through the signs of the dot products and the comparison of $(u \cdot v)^2 |u'|^2 |v'|^2$ with $(u' \cdot v')^2 |u|^2 |v|^2$, all integers. For the flip decision, even this is not needed: the [in-circle test](/in-circle-test/) decides which diagonal of a quadrilateral is better.

## Variants

- **Constrained version.** Given required segments, maximize the smallest angle among triangulations that contain them. The [constrained Delaunay triangulation](/constrained-delaunay-triangulation/) is optimal, by the same flip argument applied to the unconstrained edges.
- **Min-max angle.** Minimize the largest angle. The Delaunay triangulation is not optimal for this. Edelsbrunner, Tan and Waupotitsch solve it in $O(n^2 \log n)$ time by edge insertion.
- **Other criteria.** Minimize the longest edge, or the largest smallest enclosing circle of a triangle. The Delaunay triangulation is optimal for the second (Rajan). The min-max edge length triangulation takes $O(n^2)$ time (Edelsbrunner and Tan).
- **With Steiner points.** If new points may be added, every polygonal domain without small input angles can be triangulated with all angles at least about 20.7 degrees; this is [mesh generation](/mesh-generation/) by [Ruppert's algorithm](/ruppert-algorithm/) and [Chew's second algorithm](/chew-second-algorithm/).
- **Three dimensions.** The Delaunay tetrahedralization does not maximize the smallest dihedral angle, and it can contain slivers, flat tetrahedra with four nearly cocircular corners. See [tetrahedralization](/tetrahedralization/).

## Examples

- **A quadrilateral.** Take $a = (0,0)$, $b = (6,0)$, $c = (5,3)$, $d = (0,4)$. The diagonal $ac$ gives the angles $30.96°$, $42.27°$, $59.04°$, $71.57°$, $77.47°$, $78.69°$. The diagonal $bd$ gives $22.38°$, $33.69°$, $37.87°$, $56.31°$, $90°$, $119.74°$. So $ac$ is optimal, with smallest angle $30.96°$. The in-circle test agrees: the determinant for $a, b, c, d$ is $-192 < 0$, so $d$ lies outside the circle through $a, b, c$, and $ac$ is the Delaunay edge.
- **Cocircular points.** The four corners of a square lie on one circle. Both diagonals give the smallest angle $45°$, and both triangulations are Delaunay and both are optimal. The angle-optimal triangulation need not be unique when four or more points are cocircular.
- **A non-example.** The [greedy triangulation](/greedy-triangulation/) and the [minimum weight triangulation](/min-weight-triangulation/) can have much smaller angles than the Delaunay triangulation.

## Known algorithms

| method | time | note |
|---|---|---|
| [Lawson flips](/lawson-flip-algorithm/) from any triangulation | $O(n^2)$ | flip a non-Delaunay edge until none is left |
| [Bowyer-Watson](/bowyer-watson-algorithm/) incremental insertion | $O(n \log n)$ expected | random order with a point location structure |
| [Divide and conquer](/guibas-stolfi-algorithm/) (Guibas and Stolfi) | $O(n \log n)$ | on the [quad-edge structure](/quad-edge-data-structure/) |
| [Lifting map](/paraboloid-lifting-map/) and a 3D convex hull | $O(n \log n)$ | the lower hull projects to the Delaunay triangulation |

Each flip of the Lawson method makes the angle vector lexicographically larger, so the method cannot cycle, and the triangulation reached has no illegal edge, which makes it Delaunay. There are at most $\binom{n}{2}$ flips, since an edge once flipped away never comes back.

## Bounds

- **Upper bound.** $O(n \log n)$ time on the [real RAM](/real-ram/), by any optimal Delaunay algorithm.
- **Lower bound.** $\Omega(n \log n)$ in the [algebraic decision tree](/algebraic-decision-tree/) model, because any triangulation of a point set determines the convex hull, and sorting reduces to the convex hull. See [triangulation of a point set](/triangulation-of-point-set/).
- **The optimum value.** The max-min angle can be arbitrarily small: three nearly collinear points force it. No bound in terms of $n$ alone exists without Steiner points.

## Reductions

- **To the Delaunay triangulation.** Any angle-optimal triangulation is a Delaunay triangulation, and every Delaunay triangulation (any completion of the Delaunay subdivision when points are cocircular) maximizes the smallest angle. So the problem is the same as computing a Delaunay triangulation.
- **To local tests.** An edge of a triangulation is legal when flipping it would not increase the smallest of the six angles of its quadrilateral. This holds exactly when the edge passes the [local Delaunay criterion](/local-delaunay-criterion/), so the global optimum is checked by $O(n)$ in-circle tests.
- **From sorting.** Sorting $n$ numbers reduces to it in linear time, through the convex hull.

## Applications

- **Interpolation.** Piecewise linear interpolation of terrain heights over a Delaunay triangulation avoids long thin triangles, which spread errors (Lawson's motivation).
- **Finite elements.** Small angles make the stiffness matrix badly conditioned. Angle-optimal triangulations are the start of [mesh generation](/mesh-generation/), which adds points to bound the angles.
- **Rendering and geographic information systems.** Triangulated irregular networks use the Delaunay triangulation for the same reason.

## References
