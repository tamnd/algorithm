---
tag: ECDY6T
kind: definition
slug: empty-circle-property
name: Empty circle property
aliases:
- empty circumcircle property
- Delaunay criterion
- empty sphere property
area: geometry/voronoi-and-delaunay
level: intro
summary: A triangulation is Delaunay exactly when every triangle's circumcircle contains no other site.
prereqs: [circumcircle, in-circle-test, triangulation-of-point-set]
see_also: [delaunay-triangulation, local-delaunay-criterion, delaunay-triangulation-uniqueness, voronoi-delaunay-duality, largest-empty-circle, gabriel-graph, constrained-delaunay-triangulation, regular-triangulation]
sources:
  - book: isbn:9783540779735
    title: M. de Berg, O. Cheong, M. van Kreveld and M. Overmars, Computational Geometry, Algorithms and Applications, third edition, Springer, 2008
    locator: Section 9.2 (the empty circle characterization of Delaunay triangles and edges)
  - paper: "B. Delaunay, Sur la sphere vide, Bulletin de l'Academie des Sciences de l'URSS, Classe des sciences mathematiques et naturelles 6, 1934, 793-800"
    locator: the empty sphere condition that defines the triangulation
  - book: isbn:9781584887300
    title: S.-W. Cheng, T. K. Dey and J. R. Shewchuk, Delaunay Mesh Generation, CRC Press, 2013
    locator: Chapter 2 (Delaunay and strongly Delaunay simplices, the empty circumdisk definition)
---

A triangle with corners in a point set has the empty circle property when no point of the set lies strictly inside its [circumcircle](/circumcircle/). A triangulation of the set is a [Delaunay triangulation](/delaunay-triangulation/) exactly when all its triangles have this property. Points on the circle are allowed, which is why a Delaunay triangulation exists for every set that is not on one line, but is not always unique. The test for one point and one triangle is the [in-circle test](/in-circle-test/), and the same property, for edges, says which segments can appear in some Delaunay triangulation.

## Definition

Let $P$ be a finite set of $n$ points in the plane, not all on one line. Notation: a point is $p = (x, y)$, $h$ is the number of points of $P$ on the boundary of its convex hull, $\mathrm{orient}(a, b, c)$ is positive when $a, b, c$ turn counterclockwise, and $\mathrm{incircle}(a, b, c, d)$, for counterclockwise $a, b, c$, is positive when $d$ is strictly inside the circle through $a$, $b$, $c$, zero on it, and negative outside.

- **Empty triangle.** A triangle $abc$ with $a, b, c \in P$ and $\mathrm{orient}(a, b, c) > 0$ is **Delaunay** (has the empty circle property) when $\mathrm{incircle}(a, b, c, q) \le 0$ for every $q \in P$.
- **Empty edge.** A segment $ab$ with $a, b \in P$ is **Delaunay** when some closed disc with $a$ and $b$ on its boundary has no point of $P$ in its interior. It is **strongly Delaunay** when some closed disc with $a$ and $b$ on its boundary has no other point of $P$ in it at all, on the boundary included.
- **Delaunay triangulation.** A triangulation of $P$ (triangles with corners in $P$, covering the convex hull, meeting edge to edge, with every point of $P$ as a corner) is a **Delaunay triangulation** when every triangle is Delaunay.

General position, here no four points of $P$ on one circle, is not assumed. The definition is about the open disc, so cocircular points do not break it.

**Equivalent form through the Voronoi diagram.** Let $o$ be the circumcenter of $abc$ and $R$ its radius. A point $q$ is strictly inside the circle exactly when $|q - o| < R = |a - o|$. So $abc$ is Delaunay exactly when $a$, $b$ and $c$ are among the points of $P$ nearest to $o$, that is, when $o$ is in the three [Voronoi cells](/voronoi-cell/) of $a$, $b$ and $c$. This is the base of [Voronoi-Delaunay duality](/voronoi-delaunay-duality/).

**Facts.** Proofs are on the linked pages.

- A Delaunay triangulation exists for every finite set not on one line, for example the projection of the lower hull through the [paraboloid lifting map](/paraboloid-lifting-map/), with faces of four or more points cut into triangles.
- It is enough to check each edge against the one opposite corner across it: a triangulation whose edges are all locally Delaunay is Delaunay ([local Delaunay criterion](/local-delaunay-criterion/)).
- If no four points are on one circle, the Delaunay triangulation is unique, and an edge is in it exactly when it is Delaunay ([uniqueness](/delaunay-triangulation-uniqueness/)). In general, every strongly Delaunay edge is in every Delaunay triangulation.

## Examples and non-examples

- **A good diagonal.** For $(0,0), (4,0), (5,5), (0,4)$, the triangle $(0,0), (4,0), (0,4)$ has circumcenter $(2,2)$ and squared radius $8$, and $(5,5)$ is at squared distance $18$: empty. The triangle $(4,0), (5,5), (0,4)$ has circumcenter $(\frac{17}{6}, \frac{17}{6})$ and squared radius $\frac{169}{18}$, and $(0,0)$ is at squared distance $\frac{289}{18}$: empty. So the diagonal from $(4,0)$ to $(0,4)$ gives the Delaunay triangulation.
- **A bad diagonal.** For the same four points, the triangle $(0,0), (4,0), (5,5)$ has circumcenter $(2,3)$ and squared radius $13$, and $(0,4)$ is at squared distance $5$, inside. So the diagonal from $(0,0)$ to $(5,5)$ does not give a Delaunay triangulation; one [edge flip](/edge-flip/) repairs it.
- **Cocircular points.** The corners of the rectangle $(0,0), (4,0), (4,3), (0,3)$ are on one circle. Each of the four triangles has the fourth corner on its circle, not inside, so both diagonals give a Delaunay triangulation. Each diagonal is a Delaunay edge but not strongly Delaunay.
- **A grid.** On the $3 \times 3$ integer grid, every unit square is cocircular, so each of the four squares can take either diagonal: $2^4 = 16$ Delaunay triangulations.
- **Non-example: empty but not Delaunay.** A triangle can contain no point of $P$ and still fail: in the bad diagonal above, the triangle $(0,0), (4,0), (5,5)$ holds no other point, but its circle holds $(0,4)$. Empty triangles and empty circles are different conditions.
- **Non-example: all points on a line.** $(0,0), (1,0), (2,0)$ have no triangle at all, so there is no Delaunay triangulation, although every segment between neighbours is a strongly Delaunay edge.

## Related definitions

- [In-circle test](/in-circle-test/): the predicate that decides one point against one circle.
- [Local Delaunay criterion](/local-delaunay-criterion/): the same condition checked only across each edge.
- **Gabriel edge**: an edge whose diametral disc has no other point inside; these edges form the [Gabriel graph](/gabriel-graph/), a subgraph of every Delaunay triangulation.
- **Constrained Delaunay**: the empty circle property with points hidden behind a fixed segment ignored ([constrained Delaunay triangulation](/constrained-delaunay-triangulation/)).
- **Regular triangulation**: for weighted points, the circle is replaced by the condition that no lifted point lies below a triangle's plane ([regular triangulation](/regular-triangulation/)).
- **Empty sphere**: in $d$ dimensions, the circumsphere of a simplex with no point inside ([higher-dimensional Delaunay](/higher-dimensional-delaunay/)).

## References
