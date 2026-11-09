---
tag: 6MC1K7
kind: data-structure
slug: voronoi-diagram
name: Voronoi diagram
aliases:
- Dirichlet tessellation
- Thiessen polygons
- Voronoi tessellation
- nearest-site diagram
area: geometry/voronoi-and-delaunay
level: intro
summary: Partition of the plane into cells, one per site, each holding the points closest to that site.
model: real-ram
complexity:
  vars: {n: the number of sites}
  time: {build: O(n log n), query: O(log n)}
  space: {extra: O(n)}
properties: {persistent: false, concurrent: false, external: false}
prereqs: [euclidean-distance, planar-subdivision, convex-polygon]
see_also: [voronoi-cell, delaunay-triangulation, voronoi-delaunay-duality, voronoi-complexity-theorem, fortunes-algorithm, voronoi-diagram-construction, post-office-problem, planar-point-location]
sources:
  - paper: doi:10.1109/SFCS.1975.8
    title: M. I. Shamos and D. Hoey, Closest-point problems, 16th Annual Symposium on Foundations of Computer Science, 1975
    locator: the Voronoi diagram in computational geometry, the divide and conquer construction with the merge along a monotone chain, and its uses for closest-point problems
  - paper: doi:10.1007/BF01840357
    title: S. Fortune, A sweepline algorithm for Voronoi diagrams, Algorithmica 2, 1987
    locator: the O(n log n) sweep
  - book: isbn:9783540779735
    title: M. de Berg, O. Cheong, M. van Kreveld and M. Overmars, Computational Geometry, Algorithms and Applications, third edition, Springer, 2008
    locator: Chapter 7 (definition, cells as intersections of half-planes, size, empty circle characterization of vertices and edges, the sweep)
  - book: isbn:9780471986355
    title: A. Okabe, B. Boots, K. Sugihara and S. N. Chiu, Spatial Tessellations, Concepts and Applications of Voronoi Diagrams, second edition, Wiley, 2000
    locator: Chapters 1 and 2 (history of the diagram and its basic properties)
  - paper: doi:10.1145/282918.282923
    title: L. J. Guibas and J. Stolfi, Primitives for the manipulation of general subdivisions and the computation of Voronoi diagrams, ACM Transactions on Graphics 4(2), 1985
    locator: the quad-edge structure that holds the diagram and its dual together
---

The Voronoi diagram of a finite set $P$ of $n$ point sites in the plane splits the plane into $n$ cells, one for each site: the [cell](/voronoi-cell/) of $p$ holds the points that are at least as close to $p$ as to any other site. Each cell is a convex polygon, bounded or not. The cells meet along Voronoi edges, which are pieces of bisectors of two sites, and at Voronoi vertices, which are centers of empty circles through three or more sites. The diagram has $O(n)$ vertices and edges, it is built in $O(n \log n)$ time, and with a point location structure it answers "which site is nearest to this point" in $O(\log n)$ time. Its dual is the [Delaunay triangulation](/delaunay-triangulation/), and this page builds it from that dual.

## In plain words

Put some shops on a map. Colour every place on the map by the shop that is nearest to it. Each shop gets one region, and every region is a convex shape with straight sides.

A side between two regions is part of the line that is halfway between two shops. A corner where three regions meet is a place that is equally far from three shops, and no shop is nearer to it. A circle around that corner through the three shops has no shop inside.

The regions of the outer shops go on forever. The regions of the inner shops are closed.

## The abstract type

The diagram is a static structure over a set of distinct sites $p = (x, y)$, here with integer coordinates. It supports:

- $\mathrm{insert}(p)$: add a site, before or between queries.
- $\mathrm{vertices}()$: the Voronoi vertices, as exact rational points.
- $\mathrm{edges}()$: for each pair of sites $\{p, q\}$ whose cells share a piece of positive length, the two ends of that piece; an end at infinity is a ray.
- $\mathrm{cell}(p)$: the vertices of the cell of $p$ in counterclockwise order, and whether the cell is bounded.
- $\mathrm{neighbors}(p)$: the sites whose cells share an edge with the cell of $p$.
- $\mathrm{nearest}(q)$: a site nearest to the query point $q$.

Notation: $P$ is the set of sites, $n = |P|$, $h$ is the number of sites on the boundary of the convex hull, $d$ is the degree of a site in the Delaunay graph, $\mathrm{orient}(a, b, c)$ is positive when $a, b, c$ turn counterclockwise, and $\mathrm{incircle}(a, b, c, d)$, for counterclockwise $a, b, c$, is positive when $d$ is strictly inside their circle.

**Definitions.** The cell of $p$ is $V_p = \{x : |x - p| \le |x - s| \text{ for all } s \in P\}$, the intersection of the $n - 1$ closed half-planes bounded by the bisectors of $p$ and the other sites, so it is convex. A **Voronoi vertex** is a point with three or more nearest sites. A **Voronoi edge** is the relative interior of $V_p \cap V_q$ when this set has positive length; on it, $p$ and $q$ are the only nearest sites. A point $x$ is a vertex exactly when some circle around $x$ has three or more sites on it and none strictly inside, the *empty circle* property.

**Size.** For $n \ge 3$ sites not all on one line there are at most $2n - 5$ vertices and $3n - 6$ edges ([Voronoi complexity theorem](/voronoi-complexity-theorem/)). A cell is unbounded exactly when its site is on the boundary of the convex hull. If all sites are on one line, the diagram is $n - 1$ parallel lines.

**General position.** No assumption is made. Four or more sites on one empty circle give one vertex of higher degree, stored once, and no edge of length zero. Collinear sites give parallel lines.

## Representation

The diagram is stored through its dual. The code keeps the list of sites and, after a build, a [Delaunay triangulation](/delaunay-triangulation/) as counterclockwise index triples, with a map from each directed edge $(u, v)$ to the triangle on its left. From it, it stores the [circumcenter](/circumcenter/) of every triangle, the sorted list of distinct circumcenters as the vertices, a map from each pair of neighbouring sites to the ends of their edge, and the Delaunay adjacency lists. A [quad-edge structure](/quad-edge-data-structure/) or a [doubly connected edge list](/doubly-connected-edge-list/) holds the same information with pointers; the quad-edge structure stores the diagram and the triangulation at once.

Inserting a site only marks the stored diagram as stale; the next query rebuilds it.

## Operations

```pseudo id=main
BUILD(P)
L1  D ← a Delaunay triangulation of P
L2  for each triangle t of D do c(t) ← the circumcenter of t
L3  the vertices ← the distinct values c(t)
L4  for each edge pq of D, with triangle t on its left and t' on its right do
L5      if t' does not exist then ends ← (c(t), ∞): a ray, pq is a hull edge
L6      else if c(t) = c(t') then skip pq, else ends ← (c(t), c(t'))
L7      record the Voronoi edge of {p, q} with these ends
```

- **Line L1.** The code uses a Bowyer-Watson insertion with ghost triangles, which handles cocircular and collinear points. Any Delaunay algorithm works; with an $O(n \log n)$ algorithm the build takes $O(n \log n)$ time. If all sites are on one line there is no triangle, and the code stores the $n - 1$ bisectors of consecutive sites as lines with both ends at infinity.
- **Line L2.** The circumcenter is computed exactly with fractions. Each triangle of $D$ has an empty circumcircle, so its center is a Voronoi vertex.
- **Line L3.** Triangles inside one cocircular polygon have the same circumcenter, so they give one vertex.
- **Line L5.** A hull edge $pq$ has one triangle. Its dual is a ray from $c(t)$ along the bisector of $p$ and $q$, away from the third vertex of $t$.
- **Line L6.** Two triangles with the same circumcenter lie on one empty circle; the edge between them is a diagonal of a cocircular polygon and has no Voronoi edge, since its two cells meet only at the vertex.
- **Line L7.** Otherwise the edge of the cells of $p$ and $q$ is the segment between the two circumcenters.

**cell(p).** Walk around $p$ through the triangles of $D$ that have $p$ as a corner, in counterclockwise order, and list their circumcenters, dropping repeats. If $p$ is inside the hull the walk closes and the cell is bounded; otherwise it starts and ends at the two hull edges at $p$, and the cell is unbounded, with the two rays of those edges. Time $O(d)$.

**nearest(q).** Start at any site and move to a Delaunay neighbour that is strictly closer to $q$, as long as one exists. The walk stops at a nearest site, because a site that is not nearest always has a Delaunay neighbour that is closer. Time $O(n)$ in the worst case. With a [planar point location](/planar-point-location/) structure over the cells, the query takes $O(\log n)$ time after $O(n \log n)$ preprocessing; this is the [post office problem](/post-office-problem/).

**Building by divide and conquer (Shamos and Hoey).** Sort the sites by $x$-coordinate and split them by the median into a left set $L$ and a right set $R$. Build the two diagrams recursively. Then merge: the merge chain is the set of points that are equally far from their nearest site in $L$ and their nearest site in $R$. Left of the chain the diagram is that of $L$, right of it that of $R$, and the chain itself is made of pieces of bisectors of a left and a right site. For distinct $x$-coordinates the chain is monotone in $y$: on a horizontal line, each difference $|x - l|^2 - |x - r|^2$ with $l \in L$ and $r \in R$ is affine with slope $2(r_x - l_x) > 0$ in $x$, so $\min_l |x - l|^2 - \min_r |x - r|^2 = \min_l \max_r (|x - l|^2 - |x - r|^2)$ is strictly increasing and has exactly one zero. The chain starts with the bisector of the upper common tangent of the two hulls, far up, and is traced downward: at each step the current bisector of $l$ and $r$ leaves the cell of $l$ in the left diagram or the cell of $r$ in the right diagram, and the site on that side changes. By scanning the left cells counterclockwise and the right cells clockwise, the merge takes $O(n)$ time, so the whole algorithm takes $O(n \log n)$ time. The [Guibas-Stolfi algorithm](/guibas-stolfi-algorithm/) does the same merge on the Delaunay side.

## Example

Take the six sites $(2,8)$, $(6,7)$, $(0,4)$, $(4,5)$, $(8,3)$ and $(3,0)$. The five outer sites are the corners of the hull, so $h = 5$, and $(4,5)$ is inside.

- **L1.** The Delaunay triangulation joins $(4,5)$ to the five hull sites: $5$ triangles.
- **L2 and L3.** Their circumcenters, all different, are the five vertices: $(56/11, 24/11)$ for the triangle with $(3,0)$ and $(8,3)$, $(19/3, 14/3)$ with $(8,3)$ and $(6,7)$, $(39/10, 71/10)$ with $(6,7)$ and $(2,8)$, $(12/7, 79/14)$ with $(2,8)$ and $(0,4)$, and $(93/38, 103/38)$ with $(0,4)$ and $(3,0)$.
- **L4 to L7.** The five inner Delaunay edges from $(4,5)$ give five segments, for example the edge of $(4,5)$ and $(8,3)$ from $(56/11, 24/11)$ to $(19/3, 14/3)$. The five hull edges give five rays, for example the ray of $(3,0)$ and $(8,3)$ from $(56/11, 24/11)$. In total there are $10 = 3n - 3 - h$ edges and $5 = 2n - 2 - h$ vertices.

$\mathrm{cell}((4,5))$ is the bounded pentagon $(12/7, 79/14)$, $(93/38, 103/38)$, $(56/11, 24/11)$, $(19/3, 14/3)$, $(39/10, 71/10)$, in counterclockwise order. $\mathrm{cell}((3,0))$ is unbounded, with the two vertices $(56/11, 24/11)$ and $(93/38, 103/38)$ and two rays. $\mathrm{nearest}((5,1))$ starts at $(2,8)$, at squared distance $58$, moves to $(4,5)$ at $17$ and then to $(3,0)$ at $5$; no neighbour of $(3,0)$ is closer, so it returns $(3,0)$.

For the four corners of the square $(0,0)$, $(2,0)$, $(2,2)$, $(0,2)$, the two triangles have the same circumcenter $(1,1)$, so there is one vertex, the diagonal is skipped at line L6, and the four hull edges give four rays from $(1,1)$.

## Correctness

**Theorem.** For distinct integer sites, BUILD returns exactly the Voronoi vertices and, for each pair of sites whose cells share a piece of positive length, the correct ends of that piece. $\mathrm{cell}(p)$ returns the vertices of $V_p$ in counterclockwise order and says correctly whether $V_p$ is bounded, and $\mathrm{nearest}(q)$ returns a site at the smallest distance from $q$.

The proof rests on [Voronoi-Delaunay duality](/voronoi-delaunay-duality/): the Voronoi vertices are the centers of the Delaunay circles, the triangles of any Delaunay triangulation group by their circumcircle into the faces of the Delaunay subdivision, and the Voronoi edges are dual to the sides of these faces, with rays exactly for the hull edges. For the nearest site walk, if $p$ is not nearest to $q$, follow the segment from $p$ to $q$ until it leaves $V_p$; the site on the other side, or the circle neighbour of $p$ at the vertex where the segment leaves, is a Delaunay neighbour of $p$ that is closer to $q$. The full proof is in [the correctness proof](proofs/correctness/).

## Complexity

- **Build.** $O(n \log n)$ worst-case time with an optimal Delaunay algorithm, such as [Fortune's algorithm](/fortunes-algorithm/) on the Voronoi side or the Guibas-Stolfi divide and conquer on the Delaunay side; lines L2 to L7 take $O(n)$ time, since the triangulation has $O(n)$ triangles and edges. This is optimal: the [lower bound](/voronoi-construction-lower-bound/) is $\Omega(n \log n)$ in the algebraic decision tree model. The code uses a simple Bowyer-Watson insertion that finds the first conflicting triangle by a linear search, which takes $O(n^2)$ time in the worst case.
- **Queries.** $\mathrm{vertices}$ and $\mathrm{edges}$ return the stored lists in $O(n)$ time. $\mathrm{cell}(p)$ takes $O(d)$ time. $\mathrm{neighbors}(p)$ takes $O(n)$ time in the code, which scans all edges, and $O(d)$ with adjacency lists. $\mathrm{nearest}(q)$ visits each site at most once, because the distance to $q$ strictly decreases, and looks at the neighbours of each visited site, so it takes $O(n)$ time, since the degrees sum to less than $6n$; with point location it takes $O(\log n)$ time.
- **Space.** $O(n)$, since the diagram and its dual have $O(n)$ vertices, edges and faces.
- **Insert.** The code rebuilds; a dynamic structure inserts a site in $O(\log n)$ expected time in random order ([dynamic Delaunay triangulation](/dynamic-delaunay-triangulation/)).

## Variants

- **Farthest-point diagram.** Cells by the farthest site; only hull vertices have cells, and the diagram is a tree ([farthest-point Voronoi diagram](/farthest-point-voronoi-diagram/)).
- **Order-$k$ diagram.** Cells by the set of the $k$ nearest sites ([order-k Voronoi diagram](/order-k-voronoi-diagram/)).
- **Weighted sites.** The [power diagram](/power-diagram/) uses $|x - p|^2 - w_p$ and keeps straight edges; the additively weighted diagram uses $|x - p| - w_p$ and has hyperbolic edges ([weighted Voronoi diagram](/weighted-voronoi-diagram/)).
- **Other sites and metrics.** Segments and polygons as sites give parabolic edges, and the inside of a polygon gives the [medial axis](/medial-axis/); the $L_1$ and $L_\infty$ metrics give diagrams with axis-parallel and diagonal edges.
- **Higher dimensions.** In $\mathbb{R}^d$ the cells are convex polyhedra and the diagram can have $\Theta(n^{\lceil d/2 \rceil})$ faces ([higher-dimensional Delaunay](/higher-dimensional-delaunay/)).
- **Centroidal tessellations.** Sites placed at the centroids of their own cells ([centroidal Voronoi tessellation](/centroidal-voronoi-tessellation/)), computed by [Lloyd's algorithm](/lloyds-algorithm/).

## When to use it

Use the Voronoi diagram for nearest-site questions on a fixed set of sites: service areas of shops, antennas or schools, the [largest empty circle](/largest-empty-circle/), and as the source of proximity graphs such as the [Euclidean minimum spanning tree](/euclidean-minimum-spanning-tree/). When only the graph structure is needed, store the Delaunay triangulation instead: it has the same information, simpler records and exact predicates. For a few nearest-neighbour queries in high dimension, use other [nearest neighbour search](/nearest-neighbor-search/) structures, since the diagram becomes too large.

## Pitfalls

- **Cocircular sites in line L6.** Four sites on an empty circle give two triangles with the same circumcenter. Without the test, the diagram gets an edge of length zero and a vertex twice.
- **Rays in line L5.** The ray of a hull edge points away from the third vertex of its triangle. The circumcenter can lie outside the hull, for an obtuse triangle, and the ray then starts outside the hull.
- **Floating-point circumcenters in line L2.** Rounding can make two equal circumcenters differ, or make the order of vertices around a cell wrong. Use exact arithmetic, or merge vertices with a tolerance and accept the risk.
- **Collinear sites.** There is no triangle and no vertex; the diagram is parallel lines, which a triangle-based build must treat on its own.
- **Unbounded cells.** Many uses need closed polygons. Clip the cells to a box, and do not compute areas or centroids of unclipped hull cells.
- **The greedy walk needs the Delaunay graph.** On other graphs, such as a path through the sites or a triangulation that is not Delaunay, a site that is not nearest can have no closer neighbour, and the walk stops too early.

## Implementations

## History

Descartes used regions of influence around stars in 1644, and Dirichlet in 1850 and Voronoi in 1908 defined the cells for points of a lattice, in the study of quadratic forms. The diagram was found again many times: Thiessen polygons for rainfall data in 1911, Wigner-Seitz cells in physics in 1933, and Delaunay's dual subdivision in 1934. In computational geometry, M. I. Shamos and D. Hoey gave the $O(n \log n)$ divide and conquer algorithm in 1975 and showed its many uses for closest-point problems. D. T. Lee and B. J. Schachter in 1980 and L. J. Guibas and J. Stolfi in 1985 built it through the Delaunay triangulation, and S. Fortune gave the plane sweep in 1987.

## References
