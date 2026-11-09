---
tag: F3FZVY
kind: problem
slug: triangulation-of-point-set
name: Triangulation of a point set
aliases:
- Planar point set triangulation
area: geometry/triangulations
level: intro
summary: Find a maximal non-crossing set of segments among a set of points in the plane.
model: algebraic-computation-tree
complexity:
  vars: {n: the number of points}
  time: {worst: Θ(n log n)}
prereqs: [triangulation, orientation-test, general-position]
see_also: [triangulation-counting-theorem, delaunay-triangulation, min-weight-triangulation, greedy-triangulation, max-min-angle-triangulation, constrained-triangulation, number-of-triangulations, flip-graph]
sources:
  - book: isbn:9783540779735
    title: Mark de Berg, Otfried Cheong, Marc van Kreveld and Mark Overmars, Computational Geometry, Algorithms and Applications, third edition, Springer, 2008
    locator: Chapter 9, Delaunay Triangulations (Section 9.1, Triangulations of Planar Point Sets, Theorem 9.1, and the chapter notes)
  - book: isbn:9780387961316
    title: Franco P. Preparata and Michael Ian Shamos, Computational Geometry, An Introduction, Springer, 1985
    locator: Section 6.2, Triangulations (the lower bound by reduction from sorting and the incremental and greedy methods); section number to be checked
  - book: isbn:9780521649766
    title: Joseph O'Rourke, Computational Geometry in C, second edition, Cambridge University Press, 1998
    locator: Chapter 5, Section 5.3 (Delaunay triangulations) and the exercises on triangulating point sets; to be checked
---

A triangulation of a point set joins $n$ points in the plane by straight segments that do not cross, adding segments until no more fit. The result cuts the convex hull of the points into triangles, every point is a corner, and by the [counting theorem](/triangulation-counting-theorem/) every such triangulation has the same number of triangles, $2n - h - 2$, where $h$ is the number of points on the hull boundary. Finding *some* triangulation takes $\Theta(n \log n)$ time. Most of the interest lies in finding a *good* one, such as the [Delaunay triangulation](/delaunay-triangulation/), which is just as fast, or the [minimum weight triangulation](/min-weight-triangulation/), which is NP-hard.

## In plain words

You have a set of dots on paper. Draw straight lines between pairs of dots, never crossing an earlier line and never running through a third dot, until no line can be added. What you get is a net of triangles that fills the region inside a rubber band stretched around the dots. There are many such nets for the same dots. A computer can draw one about as fast as it can sort the dots. The hard part is choosing a net with nice triangles, or with the least total ink.

## Definition

**Input.** A set $S$ of $n$ points in the plane, not all on one line. Points may be collinear; they are distinct.

**Output.** A [triangulation](/triangulation/) of $S$: a set $E$ of segments with end points in $S$ such that

1. no two segments of $E$ cross, and no segment passes through a point of $S$ other than its end points;
2. $E$ is maximal: every segment between two points of $S$ that is not in $E$ crosses a segment of $E$ or passes through a point of $S$.

Equivalently, a list of triangles with corners in $S$, meeting edge to edge, whose union is the convex hull $\mathrm{conv}(S)$ and that use every point as a corner. Every triangulation contains all edges of the convex hull boundary (between consecutive boundary points), because nothing can cross them. If $h$ points lie on the hull boundary, the output has $2n - h - 2$ triangles and $3n - h - 3$ edges.

## Variants

- **Optimal triangulations.** Choose the triangulation that optimizes a measure:
  - [Delaunay triangulation](/delaunay-triangulation/): empty circumcircles; it maximizes the minimum angle, by the [max-min angle](/max-min-angle-triangulation/) property, and is computable in $O(n \log n)$ time.
  - [Minimum weight triangulation](/min-weight-triangulation/): least total edge length; NP-hard (Mulzer and Rote 2008).
  - [Greedy triangulation](/greedy-triangulation/): add the shortest segment that does not cross the ones already chosen.
  - bottleneck measures: the min-max angle triangulation and several others are found in polynomial time by edge insertion (Bern, Edelsbrunner, Eppstein, Mitchell and Tan 1993), and the min-max edge length triangulation in $O(n^2)$ time (Edelsbrunner and Tan 1993).
- **Constrained.** Some segments are required to be edges; see [constrained triangulation](/constrained-triangulation/).
- **Steiner.** New points may be added; see [Steiner points](/steiner-points/) and [minimum Steiner triangulation](/minimum-steiner-triangulation/).
- **Counting and enumeration.** Count all triangulations of $S$, or list them; see [number of triangulations](/number-of-triangulations/) and the [flip graph](/flip-graph/).
- **Higher dimensions.** A triangulation of $n$ points in $\mathbb{R}^3$ is a [tetrahedralization](/tetrahedralization/); its number of tetrahedra is not fixed, and can be $\Theta(n^2)$.
- **Skipping points.** In the combinatorial convention of De Loera, Rambau and Santos, a triangulation may leave some points out; then sizes vary.

## Examples

- **Convex position.** If the $n$ points are the corners of a convex polygon with no three collinear, a triangulation is a triangulation of that polygon: $n - 2$ triangles, $2n - 3$ edges, and $C_{n-2}$ choices ([Catalan count](/catalan-triangulation-theorem/)). The fan from one point is one of them.
- **Square with center.** $S = \{(0,0), (2,0), (2,2), (0,2), (1,1)\}$ has $h = 4$, so 4 triangles and 8 edges, and there is only one triangulation: the edges from the center to all four corners. The segments $(0,0)(2,2)$ and $(2,0)(0,2)$ both pass through $(1,1)$ and are not allowed.
- **Square with an off-center point.** For $\{(0,0), (4,0), (4,4), (0,4), (1,2)\}$, again 4 triangles and 8 edges. The interior point has degree 3 or 4: the 4 spokes, or 3 spokes plus the diagonal from $(0,0)$ to $(4,4)$ or the one from $(4,0)$ to $(0,4)$ that misses the point. Both diagonals miss the point, so this set has exactly three triangulations.
- **Sweep triangulation.** Sort the points by $x$ (then $y$). Start with the first two points; at each new point $p$, connect $p$ to every point of the current hull boundary that it sees, then update the hull. On $(0,0), (2,3), (3,0), (5,2)$ this gives the edges $(0,0)(2,3)$, then $(3,0)$ joined to both, then $(5,2)$ joined to $(3,0)$ and $(2,3)$: 2 triangles and 5 edges, as $2 \cdot 4 - 4 - 2 = 2$ and $3 \cdot 4 - 4 - 3 = 5$.

## Known algorithms

| method | time | notes |
|---|---|---|
| Brute force: add segments by length or any order, checking all crossings | $O(n^3)$ | follows the maximality definition |
| Sweep (incremental by $x$) | $O(n \log n)$ | sort, then walk the hull from the last point; each hull edge removed is paid for once |
| Triangulate the hull, then insert points | $O(n \log n)$ expected | with point location, as in [randomized incremental construction](/randomized-incremental-construction/) |
| [Delaunay triangulation](/delaunay-triangulation/) by [Bowyer-Watson](/bowyer-watson-algorithm/), [Guibas-Stolfi](/guibas-stolfi-algorithm/) divide and conquer, or Fortune's sweep | $O(n \log n)$ | the standard choice when shape matters |
| Any triangulation, then [Lawson flips](/lawson-flip-algorithm/) to Delaunay | $O(n^2)$ flips worst case | simple; flips are local |
| [Greedy triangulation](/greedy-triangulation/) | $O(n^2 \log n)$, or $O(n \log n)$ via the Delaunay triangulation (Levcopoulos and Krznaric) | |

The sweep is the simplest exact $O(n \log n)$ method. After sorting, the new point $p$ is to the right of all earlier points, so it lies outside their hull, and the hull edges it sees form a contiguous chain on the right side. Walking from the last point added (which is always on the hull and visible from $p$) up and down the chain while the turn is right finds that chain; each removed hull edge disappears for good, so the walks cost $O(n)$ in total, the same amortization as in [Graham scan](/graham-scan/).

## Bounds

- **Upper bound.** $O(n \log n)$ time, for example by the sweep.
- **Lower bound.** $\Omega(n \log n)$ in the [algebraic computation tree](/algebraic-computation-tree/) model. Given numbers $x_1, \ldots, x_n$, map them to points $(x_i, x_i^2)$ on a parabola. These are in convex position, so every triangulation contains the hull edges, and walking around the hull from the lowest point lists the numbers in sorted order in $O(n)$ time. Sorting needs $\Omega(n \log n)$ in this model.
- **Output size.** The output has $\Theta(n)$ edges by the [counting theorem](/triangulation-counting-theorem/), so it is not the bottleneck.

## Reductions

- **Sorting to triangulation**, as in the lower bound above.
- **Convex hull from triangulation.** The hull boundary consists of the edges that lie in only one triangle, so the [convex hull](/convex-hull/) follows in $O(n)$ time from any triangulation.
- **Triangulation from Delaunay.** Any of the optimal variants that are polynomial start from or compare with the Delaunay triangulation; the [greedy triangulation](/greedy-triangulation/) can be computed from it in linear time.
- **Euclidean minimum spanning tree.** The [Euclidean minimum spanning tree](/euclidean-minimum-spanning-tree/) is a subgraph of the Delaunay triangulation, so a triangulation algorithm plus a linear-size MST computation solves it.

## Applications

- **Terrain models.** Height samples are triangulated into a triangulated irregular network (TIN), and heights are interpolated linearly in each triangle; the Delaunay triangulation is preferred because it avoids long thin triangles.
- **Finite elements.** A triangulation of the domain is the starting mesh for [mesh generation](/mesh-generation/).
- **Interpolation and graphics.** Scattered data interpolation and surface reconstruction start from a triangulation of the sample points.
- **Graph algorithms on points.** Triangulations are planar graphs with $O(n)$ edges, so they serve as sparse supergraphs: the Delaunay triangulation contains the minimum spanning tree and the nearest neighbor graph, and it is a spanner.
- **Point location.** A triangulated subdivision is the input to [Kirkpatrick's point location](/kirkpatrick-point-location/).

## References
