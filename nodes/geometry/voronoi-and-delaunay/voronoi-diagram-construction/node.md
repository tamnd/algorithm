---
tag: ZMKP8Z
kind: problem
slug: voronoi-diagram-construction
name: Voronoi diagram construction
aliases:
- computing the Voronoi diagram
- Voronoi diagram problem
area: geometry/voronoi-and-delaunay
level: core
summary: Compute the Voronoi diagram of a set of n point sites.
prereqs: [voronoi-diagram, voronoi-cell, planar-subdivision]
see_also: [delaunay-triangulation-construction, fortunes-algorithm, guibas-stolfi-algorithm, voronoi-construction-lower-bound, voronoi-complexity-theorem, voronoi-delaunay-duality, paraboloid-lifting-map, half-plane-intersection]
sources:
  - paper: doi:10.1109/SFCS.1975.8
    title: M. I. Shamos and D. Hoey, Closest-point problems, 16th Annual Symposium on Foundations of Computer Science, 1975
    locator: the divide and conquer construction in O(n log n) time and the lower bound from sorting
  - paper: doi:10.1007/BF01840357
    title: S. Fortune, A sweepline algorithm for Voronoi diagrams, Algorithmica 2, 1987
    locator: the sweep in O(n log n) worst-case time and O(n) space
  - book: isbn:9783540779735
    title: M. de Berg, O. Cheong, M. van Kreveld and M. Overmars, Computational Geometry, Algorithms and Applications, third edition, Springer, 2008
    locator: Chapter 7 (the definition, the bound on the size, the sweep and the lower bound)
  - paper: doi:10.1007/BF01758770
    title: L. J. Guibas, D. E. Knuth and M. Sharir, Randomized incremental construction of Delaunay and Voronoi diagrams, Algorithmica 7, 1992
    locator: the randomized incremental construction in O(n log n) expected time
---

The Voronoi diagram construction problem asks for the [Voronoi diagram](/voronoi-diagram/) of a finite set $P$ of $n$ point sites in the plane: the subdivision of the plane into the [cells](/voronoi-cell/) of points that have the same nearest site, with its vertices, its edges and their adjacency. The diagram has $O(n)$ size, at most $2n - 5$ vertices and $3n - 6$ edges for $n \ge 3$ sites not all on one line. The problem takes $\Theta(n \log n)$ time in the worst case, and it is equivalent in linear time to the [Delaunay triangulation construction](/delaunay-triangulation-construction/).

## In plain words

You get a set of dots, for example shops on a map. Split the map into regions, one for each shop, so that every place in a region is closer to its shop than to any other shop. The borders are straight pieces, each halfway between two shops. Where three or more regions meet there is a corner. The task is to find all the corners and all the border pieces, and which regions they separate. Border pieces of the outer shops go on forever.

## Definition

**Input.** A finite set $P$ of $n$ distinct sites $p = (x, y)$, usually with integer or rational coordinates. Repeated sites are merged.

**Output.** The Voronoi diagram of $P$ as a [planar subdivision](/planar-subdivision/):

1. the **vertices**: the points that are equally far from three or more sites and strictly farther from all other sites, each the center of an empty circle through three or more sites;
2. the **edges**: for each pair of sites $p, q$ whose cells share a part of positive length, that part of their bisector, which is a segment between two vertices, a ray from a vertex, or a whole line;
3. the **adjacency**: for each cell, its edges in counterclockwise order, and for each edge, its two cells and its two end vertices. A [doubly connected edge list](/doubly-connected-edge-list/) or a [quad-edge structure](/quad-edge-data-structure/) holds all of this.

Notation: $n = |P|$, $h$ is the number of sites on the boundary of the convex hull of $P$, $\mathrm{orient}(p, q, r)$ is positive when $p, q, r$ turn counterclockwise, and $\mathrm{incircle}(a, b, c, d)$, for counterclockwise $a, b, c$, is positive when $d$ is strictly inside their circle. Vertices are rational when the sites are; [circumcenters](/circumcenter/) can be computed exactly with fractions.

**Size.** If the sites are not all on one line and $n \ge 3$, the diagram has at most $2n - 5$ vertices and at most $3n - 6$ edges, with equality for both exactly when no four sites lie on one empty circle and $h = 3$; in general position the counts are $2n - 2 - h$ and $3n - 3 - h$ ([Voronoi complexity theorem](/voronoi-complexity-theorem/)). If the sites are on one line, the diagram is $n - 1$ parallel lines and has no vertex.

**General position.** Many algorithms assume that no four sites lie on one circle. Then every vertex has degree $3$. With four or more cocircular sites, a vertex can have higher degree; a correct output records it once, with all its edges, and has no edges of length zero.

## Variants

- **Bounded output.** Clip the diagram to a box, so that every cell is a convex polygon. Many applications need this form.
- **Furthest-point diagram.** Each cell holds the points with the same furthest site; see [farthest-point Voronoi diagram](/farthest-point-voronoi-diagram/).
- **Order-$k$ diagrams.** Each cell holds the points with the same set of $k$ nearest sites; see [order-k Voronoi diagram](/order-k-voronoi-diagram/).
- **Weighted sites.** The [power diagram](/power-diagram/) for squared distance minus a weight, and the [additively weighted diagram](/weighted-voronoi-diagram/), whose edges are hyperbola arcs.
- **Segments and polygons.** Sites that are segments give edges that are parabola arcs; for the inside of a polygon this is close to the [medial axis](/medial-axis/).
- **Higher dimensions.** In $d$ dimensions the diagram can have $\Theta(n^{\lceil d/2 \rceil})$ size; see [higher-dimensional Delaunay](/higher-dimensional-delaunay/).

## Examples

- **Six sites.** For $(2,8)$, $(6,7)$, $(0,4)$, $(4,5)$, $(8,3)$ and $(3,0)$, the hull has $h = 5$ sites and $(4,5)$ is inside it. The diagram has $5$ vertices, $(12/7, 79/14)$, $(93/38, 103/38)$, $(39/10, 71/10)$, $(56/11, 24/11)$ and $(19/3, 14/3)$, and $10$ edges, $5$ of them rays; these are $2n - 2 - h$ and $3n - 3 - h$. The cell of $(4,5)$ is the bounded pentagon with these five vertices. The [Fortune's algorithm](/fortunes-algorithm/) page builds it step by step.
- **A square.** For $(0,0)$, $(2,0)$, $(2,2)$, $(0,2)$, the four sites lie on one circle. The diagram has one vertex $(1,1)$ of degree $4$ and four rays. In general position four sites with $h = 4$ give $2$ vertices and $5$ edges; here the two vertices have merged and the edge between them has length zero, so it is not part of the output.
- **Collinear sites.** For $(0,0)$, $(1,0)$, $(3,0)$, the diagram is the two vertical lines $x = 1/2$ and $x = 2$, with no vertex.
- **Two sites.** The diagram is the bisector, one line.

## Known algorithms

| algorithm | time | kind of bound | notes |
| --- | --- | --- | --- |
| each cell as an intersection of $n - 1$ half-planes | $O(n^2 \log n)$ | worst case | [half-plane intersection](/half-plane-intersection/) per site; simple and robust |
| incremental, one site at a time | $O(n^2)$ | worst case | each new cell is cut out of the old diagram |
| divide and conquer of Shamos and Hoey (1975) | $O(n \log n)$ | worst case | merges two diagrams along a monotone chain; see [Voronoi diagram](/voronoi-diagram/) |
| [Fortune's sweep](/fortunes-algorithm/) (1987) | $O(n \log n)$ | worst case | beach line and circle events; $O(n)$ space |
| a Delaunay algorithm and [duality](/voronoi-delaunay-duality/) | $O(n \log n)$ | worst case | for example [Guibas-Stolfi](/guibas-stolfi-algorithm/); the dual takes $O(n)$ time |
| randomized incremental (Guibas, Knuth and Sharir, 1992) | $O(n \log n)$ | expected, random order | on the Delaunay side; see [randomized incremental construction](/randomized-incremental-construction/) |
| [lifting](/paraboloid-lifting-map/) and a [3D convex hull](/convex-hull-3d/) | $O(n \log n)$ | worst case | upper envelope of the tangent planes of the paraboloid |

## Bounds

In the worst case the problem takes $\Theta(n \log n)$ time. The upper bound comes from the algorithms of Shamos and Hoey and of Fortune. The lower bound $\Omega(n \log n)$ holds in the [algebraic decision tree](/algebraic-decision-tree/) model: for numbers $x_1, \ldots, x_n$, the Voronoi diagram of the sites $(x_i, 0)$ is a set of parallel lines in the order of the $x_i$, so a walk over the diagram sorts the numbers in $O(n)$ more time ([Voronoi construction lower bound](/voronoi-construction-lower-bound/)). The output has $\Theta(n)$ size, so the time is not output-bound. For sites with extra structure the time can be smaller: for points uniform in a square, [Dwyer's algorithm](/dwyer-algorithm/) builds the dual in $O(n \log \log n)$ expected time, and for sites in convex position, given in hull order, an $O(n)$ algorithm of Aggarwal, Guibas, Saxe and Shor exists.

## Reductions

- **To and from the Delaunay triangulation.** The Delaunay triangulation is the dual graph of the Voronoi diagram, and each is computed from the other in $O(n)$ time ([duality](/voronoi-delaunay-duality/)). Each Voronoi vertex is the circumcenter of a Delaunay triangle, and each Voronoi edge is part of the bisector of a Delaunay edge.
- **To a 3D convex hull.** The site $p$ gives the plane $z = 2 p \cdot x - |p|^2$, tangent to the paraboloid $z = |x|^2$ above $p$. The nearest site of $x$ is the one whose plane is highest at $x$, so the diagram is the projection of the upper envelope of the planes. By duality this is a [3D convex hull](/convex-hull-3d/) problem.
- **From sorting.** As in the bounds, sorting reduces to the problem in linear time.

## Applications

- **Nearest site queries.** With a [planar point location](/planar-point-location/) structure over the diagram, the nearest site of a query point is found in $O(\log n)$ time after $O(n \log n)$ preprocessing, the [post office problem](/post-office-problem/).
- **Largest empty circle.** The center of a largest empty circle with center in the hull is a Voronoi vertex or a point where a Voronoi edge crosses the hull boundary ([largest empty circle](/largest-empty-circle/)).
- **Proximity graphs.** The [Euclidean minimum spanning tree](/euclidean-minimum-spanning-tree/), the [relative neighbourhood graph](/relative-neighborhood-graph/), the [Gabriel graph](/gabriel-graph/) and [all nearest neighbours](/all-nearest-neighbors/) are read off the diagram or its dual.
- **Facility placement and coverage.** Service regions of shops or antennas, and the iteration of [Lloyd's algorithm](/lloyds-algorithm/) for even coverage.
- **Motion planning.** Paths that stay as far as possible from obstacles run along the Voronoi edges.

## References
