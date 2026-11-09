---
tag: SSG10R
kind: problem
slug: delaunay-triangulation-construction
name: Delaunay triangulation construction
aliases:
- computing the Delaunay triangulation
- Delaunay triangulation problem
- planar Delaunay triangulation
area: geometry/voronoi-and-delaunay
level: core
summary: Compute the Delaunay triangulation of a set of n points.
prereqs: [delaunay-triangulation, in-circle-test, orientation-test]
see_also: [voronoi-diagram-construction, bowyer-watson-algorithm, lawson-flip-algorithm, guibas-stolfi-algorithm, fortunes-algorithm, dwyer-algorithm, voronoi-construction-lower-bound, paraboloid-lifting-map]
sources:
  - book: isbn:9783540779735
    title: M. de Berg, O. Cheong, M. van Kreveld and M. Overmars, Computational Geometry, Algorithms and Applications, third edition, Springer, 2008
    locator: Chapter 9, Delaunay triangulations (the problem, legal triangulations, the randomized incremental algorithm and its analysis)
  - paper: doi:10.1145/282918.282923
    title: L. Guibas and J. Stolfi, Primitives for the manipulation of general subdivisions and the computation of Voronoi diagrams, ACM Transactions on Graphics 4(2), 1985, 74-123
    locator: the quad-edge structure and the divide and conquer algorithm in O(n log n) worst-case time
  - paper: doi:10.1007/BF01758770
    title: L. J. Guibas, D. E. Knuth and M. Sharir, Randomized incremental construction of Delaunay and Voronoi diagrams, Algorithmica 7, 1992, 381-413
    locator: the randomized incremental algorithm in O(n log n) expected time
  - paper: doi:10.1007/BF01840357
    title: S. Fortune, A sweepline algorithm for Voronoi diagrams, Algorithmica 2, 1987, 153-174
    locator: the sweep in O(n log n) worst-case time, and the Delaunay triangulation as its dual
  - paper: doi:10.1007/BF01840356
    title: R. A. Dwyer, A faster divide-and-conquer algorithm for constructing Delaunay triangulations, Algorithmica 2, 1987, 137-151
    locator: the strip merge and its expected time for uniform points
---

The Delaunay triangulation construction problem asks for the [Delaunay triangulation](/delaunay-triangulation/) of a finite set $P$ of $n$ points in the plane: a triangulation of $P$ in which no point is strictly inside the circumcircle of a triangle. It is one of the basic problems of computational geometry. It is equivalent in linear time to the [Voronoi diagram construction](/voronoi-diagram-construction/) and to the lower convex hull of points lifted to a paraboloid, and it needs $\Theta(n \log n)$ time in the worst case.

## In plain words

You get a set of dots. Join them into triangles that cover the region inside the outer dots, with no gaps and no overlaps, so that the circle through the three corners of any triangle has no dot inside it. The triangles you get avoid long thin shapes as much as possible. When four or more dots lie on one empty circle, as in a square grid, there is more than one correct answer, and any one of them is accepted.

## Definition

**Input.** A finite set $P$ of $n$ points $p = (x, y)$, usually with integer or rational coordinates.

**Output.** If $P$ lies on one line (this includes $n \le 2$), there is no triangle; a common answer is the empty list, or the path through the points in sorted order. Otherwise a list of triangles, each a counterclockwise triple of points of $P$, such that:

1. the triangles have pairwise disjoint interiors, meet edge to edge, cover $\operatorname{conv} P$, and have vertex set $P$;
2. for each triangle $abc$ and each $d \in P$, $\mathrm{incircle}(a, b, c, d) \le 0$.

Here $\mathrm{orient}(p, q, r)$ is positive when $p, q, r$ turn counterclockwise, and $\mathrm{incircle}(a, b, c, d)$ for counterclockwise $abc$ is positive when $d$ is strictly inside the circle through $a, b, c$ (see [in-circle test](/in-circle-test/)). With exact integer arithmetic both are exact. Such a triangulation always exists, and it is unique when no four points lie on a circle ([uniqueness](/delaunay-triangulation-uniqueness/)). The number of triangles is $2n - 2 - h$ and the number of edges is $3n - 3 - h$, where $h$ is the number of points on the boundary of the convex hull.

**General position.** Many algorithms assume that no three points are on a line and no four on a circle. Degenerate input is handled in two ways: an algorithm outputs one Delaunay triangulation, using a strict test so that it never flips between equal choices, or it outputs the **Delaunay subdivision**, in which the points on one empty circle form one convex face. The subdivision is unique, and the Delaunay triangulations are exactly its refinements by diagonals.

## Variants

- **Output as a graph.** Return the Delaunay edges, or a [quad-edge](/quad-edge-data-structure/) or [doubly connected edge list](/doubly-connected-edge-list/) with adjacency, which is what most applications use.
- **Online.** Points arrive one at a time and the triangulation is kept up to date; see [dynamic Delaunay triangulation](/dynamic-delaunay-triangulation/) for insertions and deletions.
- **With constraints.** Given segments must be edges: the [constrained Delaunay triangulation](/constrained-delaunay-triangulation/). With [Steiner points](/steiner-points/) added, a [conforming Delaunay triangulation](/conforming-delaunay-triangulation/).
- **Weighted.** The [regular triangulation](/regular-triangulation/), dual to the [power diagram](/power-diagram/).
- **Higher dimensions.** [Delaunay triangulations in $d$ dimensions](/higher-dimensional-delaunay/), whose size can be $\Theta(n^{\lceil d/2 \rceil})$.
- **Furthest-point.** The triangulation in which every circumcircle holds all points, dual to the [farthest-point Voronoi diagram](/farthest-point-voronoi-diagram/).

## Examples

- **Unique answer.** For $(0,0)$, $(6,0)$, $(3,5)$, $(3,-1)$, $(3,2)$, no four points are on a circle, so the answer is unique even though $(3,-1)$, $(3,2)$, $(3,5)$ are on a line. It has the $2 \cdot 5 - 2 - 4 = 4$ triangles $(3,-1), (3,2), (0,0)$, then $(3,-1), (6,0), (3,2)$, then $(3,5), (0,0), (3,2)$ and $(6,0), (3,5), (3,2)$. The edge from $(3,-1)$ to $(3,5)$ is not in it, because $(3,2)$ is on it.
- **Two answers.** For the square $(0,0)$, $(1,0)$, $(1,1)$, $(0,1)$, the four points are on one circle, both diagonals give a Delaunay triangulation, and the Delaunay subdivision is the square itself.
- **Many answers.** For the $3 \times 3$ grid $\{0, 1, 2\}^2$, $n = 9$ and $h = 8$, so every answer has $8$ triangles. The Delaunay subdivision has four unit squares, each with an empty circumcircle, and each square can take either diagonal, so there are $2^4 = 16$ Delaunay triangulations.
- **No answer.** For $(0,0)$, $(1,1)$, $(2,2)$, there is no triangle.

## Known algorithms

| algorithm | time | kind of bound | notes |
| --- | --- | --- | --- |
| test every triple against every point | $O(n^4)$ | worst case | finds all Delaunay triangles in general position; a test oracle |
| [Lawson flips](/lawson-flip-algorithm/) from any triangulation | $O(n^2)$ flips | worst case | at most $\binom{n}{2}$ flips; $\Omega(n^2)$ flips can be needed |
| [Bowyer-Watson](/bowyer-watson-algorithm/) insertion | $O(n^2)$ | worst case | cavity insertion; fast in practice with a good point location |
| randomized incremental, with a history DAG ([Delaunay triangulation](/delaunay-triangulation/)) | $O(n \log n)$ | expected, random order | Guibas, Knuth and Sharir (1992) |
| [Guibas-Stolfi divide and conquer](/guibas-stolfi-algorithm/) | $O(n \log n)$ | worst case | quad-edge structure; after Lee and Schachter (1980) |
| [Fortune's sweep](/fortunes-algorithm/) | $O(n \log n)$ | worst case | builds the Voronoi diagram, then its dual |
| [Dwyer's algorithm](/dwyer-algorithm/) | $O(n \log \log n)$ | expected, uniform points in a square | divide and conquer on vertical strips; $O(n \log n)$ worst case |
| [lifting](/paraboloid-lifting-map/) and a [3D convex hull](/convex-hull-3d/) | $O(n \log n)$ | worst case | lower hull of $(x, y, x^2 + y^2)$ |

## Bounds

In the worst case the problem takes $\Theta(n \log n)$ time. The upper bound is given by the algorithms of Guibas and Stolfi and of Fortune. The lower bound $\Omega(n \log n)$ holds in the [algebraic decision tree](/algebraic-decision-tree/) model, and in the algebraic computation tree model, because the [convex hull](/convex-hull-problem/) can be read from a Delaunay triangulation in $O(n)$ time: the hull edges are the edges that belong to only one triangle. So the [convex hull lower bound](/convex-hull-lower-bound/) carries over; see [Voronoi construction lower bound](/voronoi-construction-lower-bound/). The output has $O(n)$ size, so no better output-sensitive bound is possible in the worst case. For points with extra structure, faster times are known in expectation, such as for uniform random points.

## Reductions

- **To and from the Voronoi diagram.** The Voronoi diagram and the Delaunay triangulation are dual, and each is computed from the other in $O(n)$ time ([duality](/voronoi-delaunay-duality/)).
- **To a 3D convex hull.** Lift each point $p$ to $(x, y, x^2 + y^2)$. The lower faces of the convex hull of the lifted points project to the Delaunay subdivision.
- **From the convex hull.** As above, a Delaunay triangulation gives the hull in $O(n)$ time, so hull lower bounds apply.
- **Proximity problems.** From a Delaunay triangulation in $O(n)$ time: the [closest pair](/closest-pair-of-points/), [all nearest neighbours](/all-nearest-neighbors/), the [Gabriel graph](/gabriel-graph/) and the [relative neighbourhood graph](/relative-neighborhood-graph/); and in $O(n \log n)$ time the [Euclidean minimum spanning tree](/euclidean-minimum-spanning-tree/), by [Kruskal's algorithm](/kruskal/) on the Delaunay edges.

## Applications

- **Interpolation and terrain models.** [Piecewise linear interpolation](/piecewise-linear-interpolation/) of scattered measurements over the Delaunay triangles; among all triangulations, the Delaunay one gives the lowest roughness of the interpolant (Rippa 1990).
- **Mesh generation.** The first step of [Delaunay refinement](/delaunay-refinement/) and [Ruppert's algorithm](/ruppert-algorithm/), which add points until all angles are large.
- **Neighbour structure.** Natural neighbours of a point, clustering, and the Voronoi diagram for [nearest neighbour search](/nearest-neighbor-search/) and the [largest empty circle](/largest-empty-circle/).
- **Shape reconstruction.** [Alpha shapes](/alpha-shape/) and crust methods are subcomplexes of the Delaunay triangulation.

## References
