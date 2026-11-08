---
tag: V9PNZF
kind: concept
slug: concave-hull
name: Concave hull
aliases:
- alpha shape hull
- concave envelope
- chi-shape
- non-convex hull
area: geometry/convex-hulls
level: advanced
summary: A tighter enclosing polygon of a point set that may have concave boundary parts.
prereqs: [convex-hull, delaunay-triangulation, simple-polygon]
see_also: [alpha-shape, convex-hull-problem, delaunay-triangulation, in-circle-test, polygon-area, gabriel-graph, beta-skeleton, euclidean-minimum-spanning-tree]
sources:
  - paper: doi:10.1109/TIT.1983.1056714
    title: Herbert Edelsbrunner, David G. Kirkpatrick and Raimund Seidel, On the shape of a set of points in the plane, IEEE Transactions on Information Theory 29(4), 1983
    locator: the definition of alpha-hulls and alpha-shapes, their relation to the Delaunay triangulation, and the O(n log n) construction
  - paper: "Matt Duckham, Lars Kulik, Mike Worboys and Antony Galton, Efficient generation of simple polygons for characterizing the shape of a set of points in the plane, Pattern Recognition 41(10), 2008"
    locator: the chi-shape algorithm, which removes long boundary edges of the Delaunay triangulation while the boundary stays a simple polygon
  - paper: "Sándor P. Fekete, On simple polygonizations with optimal area, Discrete and Computational Geometry 23(1), 2000"
    locator: NP-completeness of finding a simple polygon of minimum area through all points of a set
---

A concave hull of a point set is a polygon that encloses the points more tightly than the [convex hull](/convex-hull/) does, so that it can follow dents and bays in the shape of the data. The convex hull of the points sampled from a letter C is a disk-like blob that hides the opening; a concave hull shows the C. Unlike the convex hull, the concave hull is not one well-defined object. The tightest polygon through all the points is NP-hard to find, and the methods in use, such as [alpha shapes](/alpha-shape/) and chi-shapes, each have a parameter that sets how tight the result is. Most of them start from the [Delaunay triangulation](/delaunay-triangulation/).

## In plain words

Wrap a rubber band around a set of nails in a board and you get the convex hull. The band jumps straight across every gap in the outline. Now imagine that the band can be pushed inward into the gaps, but only where the gap is wide. You get a shape that follows the outline more closely: that is a concave hull.

How far the band may go in is a choice. If it may enter any gap, it can wind between all the nails and the shape stops making sense. If it may enter no gap, you get the convex hull back. So each method has a setting, such as a radius or a length. Wide gaps get cut into and narrow gaps stay closed. There is no single right answer, only a right answer for a given setting.

## The idea

The goal is a region $R$ that contains the points $S$, is bounded by a [simple polygon](/simple-polygon/) whose corners are points of $S$, and has small area. Three facts shape the methods.

**The extreme versions are hard or useless.** If the only aim is the smallest area, the problem is to find a simple polygon through all points of $S$ (a *polygonization*) with minimum area. Fekete proved this NP-complete (2000). And a polygon of minimum area is often a thin, zigzag shape that does not look like the data. So practical methods add a scale parameter and do not optimize area exactly.

**The Delaunay triangulation is the scaffold.** The edges of the [Delaunay triangulation](/delaunay-triangulation/) join points that are close in a precise sense: an edge $pq$ is Delaunay when some disk has $p$ and $q$ on its boundary and no point of $S$ inside. The convex hull boundary is the outer boundary of the Delaunay triangulation. Removing triangles from the outside in, starting with those on long edges, carves dents into the hull. Both methods below are of this kind, and both run in $O(n \log n)$ time after (or including) the Delaunay triangulation.

**Alpha shapes (Edelsbrunner, Kirkpatrick and Seidel, 1983).** Fix a radius $r > 0$. Call an open disk of radius $r$ *empty* if it contains no point of $S$. An edge $pq$ with $p, q \in S$ is on the boundary of the *alpha shape* for $r$ if some empty disk of radius $r$ has $p$ and $q$ on its boundary circle. Think of an eraser of radius $r$ that removes everything it can reach without touching a point; the alpha shape is what is left, with its curved edges replaced by straight ones. As $r \to \infty$ the empty disks become half-planes and the alpha shape becomes the convex hull. For small $r$ it falls apart into the single points. Every alpha shape edge is a Delaunay edge, so the alpha shapes for all $r$ can be read off the Delaunay triangulation. An alpha shape can have several components, holes and dangling edges, so it is not always a simple polygon.

**Chi-shapes (Duckham, Kulik, Worboys and Galton, 2008).** Fix a length $\ell$. Start from the Delaunay triangulation, whose boundary is the convex hull. Repeat: take the longest boundary edge $pq$ with $|pq| > \ell$ whose triangle $pqr$ has its third corner $r$ not already on the boundary, and delete that triangle. The new boundary replaces $pq$ by $pr$ and $rq$. The condition on $r$ keeps the boundary a simple polygon, and each point stays on the boundary or inside. When no boundary edge can be removed, the boundary is the chi-shape. With $\ell$ at least the longest hull edge the result is the convex hull; as $\ell$ shrinks the shape gets tighter. With a priority queue on edge lengths the method runs in $O(n \log n)$ time.

**Exactness.** The decisions in both methods use the [in-circle test](/in-circle-test/) (for the Delaunay triangulation) and comparisons of squared edge lengths, which are exact with integer coordinates. Only the user's parameter $\ell$ or $r$ needs a squared value $\ell^2$ or $r^2$ for an exact test.

**Name clash.** In optimization, the *concave envelope* of a function $f$ is the smallest concave function above $f$, the mirror image of the [convex envelope](/convex-envelope/). That is a different object from the concave hull of a point set.

## Examples

**A chi-shape, step by step.** Let $S = \{(0,0), (8,0), (9,8), (-1,9), (5,5), (3,2)\}$. No three points are on a line and no four on a circle, so the Delaunay triangulation is unique; it has 6 triangles. Its boundary is the convex hull, the quadrilateral $(0,0), (8,0), (9,8), (-1,9)$, with doubled area 153 (area 76.5). The squared lengths of the hull edges are:

| edge | squared length |
| --- | --- |
| $(9,8)$ to $(-1,9)$ | 101 |
| $(-1,9)$ to $(0,0)$ | 82 |
| $(8,0)$ to $(9,8)$ | 65 |
| $(0,0)$ to $(8,0)$ | 64 |

With $\ell^2 = 90$, only the top edge is long enough. Its Delaunay triangle is $(9,8), (-1,9), (5,5)$, and $(5,5)$ is not on the boundary, so the triangle is deleted. The boundary becomes $(0,0), (8,0), (9,8), (5,5), (-1,9)$, with doubled area 119 (area 59.5): a dent of area 17 at the top. The next candidate has squared length 82, below 90, so the method stops.

With $\ell^2 = 80$ the method goes on: the edge $(-1,9)$ to $(0,0)$ has triangle $(0,0), (3,2), (-1,9)$, its third corner $(3,2)$ is inside, and the triangle is deleted. The result is the hexagon $(0,0), (8,0), (9,8), (5,5), (-1,9), (3,2)$, with area 45, and every point of $S$ is now on the boundary. The edge $(8,0)$ to $(9,8)$ (squared length 65) is below the threshold. These numbers come from a script that builds the Delaunay triangulation by brute force with the exact in-circle test.

**A letter C.** For points sampled densely along a C-shaped band with a gap of width $w$ at the opening, the convex hull closes the gap. A chi-shape or alpha shape whose parameter is smaller than $w$ but larger than the spacing of the samples opens it, and the boundary runs into the bay of the C.

## Where it is used

- **Geographic information systems.** Drawing the footprint of a set of locations, such as the area covered by a set of sensor readings or addresses, as a region on a map. The chi-shape paper came from this setting.
- **Shape reconstruction.** Recovering the outline of an object from points sampled on or inside it, in the plane and, with alpha shapes, in space. [Alpha shapes](/alpha-shape/) are also used to describe the shape of molecules, where the cavities and pockets matter.
- **Image analysis and pattern recognition.** Describing the outline of a cluster of pixels or feature points.
- **Clustering.** Related graphs such as the [Gabriel graph](/gabriel-graph/), the [beta-skeleton](/beta-skeleton/) and the [Euclidean minimum spanning tree](/euclidean-minimum-spanning-tree/) are subgraphs of the Delaunay triangulation and are used in the same way, to separate near points from far ones.
- **When the convex hull is the wrong tool.** For collision tests, diameter, width and linear programming the [convex hull problem](/convex-hull-problem/) is the right model. A concave hull is for describing what a set looks like, and its output depends on the chosen parameter.

## References
