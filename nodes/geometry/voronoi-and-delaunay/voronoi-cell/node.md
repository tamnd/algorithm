---
tag: 3NYBVK
kind: definition
slug: voronoi-cell
name: Voronoi cell
aliases:
- Voronoi region
- Voronoi polygon
- Dirichlet domain
area: geometry/voronoi-and-delaunay
level: intro
summary: The region of points whose nearest site is a given site; a convex polygon for finite site sets.
prereqs: [euclidean-distance, half-plane-intersection, convex-polygon]
see_also: [voronoi-diagram, voronoi-delaunay-duality, voronoi-complexity-theorem, largest-empty-circle, centroidal-voronoi-tessellation, power-diagram, weighted-voronoi-diagram, order-k-voronoi-diagram]
sources:
  - book: isbn:9783540779735
    title: M. de Berg, O. Cheong, M. van Kreveld and M. Overmars, Computational Geometry, Algorithms and Applications, third edition, Springer, 2008
    locator: Section 7.1 (the cell as an intersection of half-planes, unbounded cells and the empty circle view)
  - book: isbn:9780471986355
    title: A. Okabe, B. Boots, K. Sugihara and S. N. Chiu, Spatial Tessellations, Concepts and Applications of Voronoi Diagrams, second edition, Wiley, 2000
    locator: Chapter 2 (definitions and basic properties of the Voronoi polygon)
  - paper: doi:10.1109/SFCS.1975.8
    title: M. I. Shamos and D. Hoey, Closest-point problems, 16th Annual Symposium on Foundations of Computer Science, 1975
    locator: the Voronoi polygon of a point as an intersection of half-planes
---

The Voronoi cell of a site $p$ in a finite set $P$ of sites is the set of points of the plane that are at least as close to $p$ as to any other site. It is the intersection of $n - 1$ closed [half-planes](/half-plane-intersection/), one for each other site, so it is a closed [convex polygon](/convex-polygon/), bounded or not, with at most $n - 1$ edges. The cells of all the sites cover the plane and have disjoint interiors; together they form the [Voronoi diagram](/voronoi-diagram/).

## Definition

Notation: $P$ is a set of $n \ge 2$ distinct sites in the plane, a point is $p = (x, y)$, $h$ is the number of sites on the boundary of the convex hull of $P$, distance is the [Euclidean distance](/euclidean-distance/) $|x - p|$, $\mathrm{orient}(a, b, c)$ is positive when $a, b, c$ turn counterclockwise, and $\mathrm{incircle}$ is the [in-circle test](/in-circle-test/).

For $p, q \in P$ with $p \ne q$, the half-plane of $p$ against $q$ is

$$H(p, q) = \{ x : |x - p| \le |x - q| \} = \{ x : 2 (q - p) \cdot x \le |q|^2 - |p|^2 \}.$$

The two forms are equal because $|x - p|^2 - |x - q|^2 = 2 (q - p) \cdot x - |q|^2 + |p|^2$. The **Voronoi cell** of $p$ is

$$V(p) = \bigcap_{q \in P,\ q \ne p} H(p, q).$$

The boundary line of $H(p, q)$ is the perpendicular bisector of $p$ and $q$. With integer sites, each half-plane has integer coefficients, so membership of a rational point is decided exactly.

No general position is assumed. Distinct sites are needed: two equal sites would have the same cell.

**Properties.** Let $p \in P$.

1. $V(p)$ is closed and convex, and $p$ is in its interior. *Proof.* It is an intersection of closed half-planes. For every $q \ne p$, $|p - p| = 0 < |p - q|$, so $p$ is strictly inside each of the finitely many $H(p, q)$, and a small disc around $p$ is in all of them. $\square$
2. The cells cover the plane, and two different cells have disjoint interiors. *Proof.* Every $x$ has a nearest site, and $x$ is in its cell. If $x$ is in the interior of $V(p)$ and of $V(q)$, then near $x$ all points are at least as close to $p$ as to $q$ and the reverse, so near $x$ all points are on the bisector of $p$ and $q$, which is a line and contains no disc. $\square$
3. **Empty circle view.** $x \in V(p)$ exactly when the open disc with center $x$ and radius $|x - p|$ holds no site. This is the definition read in another way, and it is why the vertices of the cells are centers of [empty circles](/empty-circle-property/).
4. **Unbounded cells.** $V(p)$ is unbounded exactly when $p$ is on the boundary of the convex hull of $P$. *Proof.* A nonempty closed convex set is unbounded exactly when it contains a ray $\{x_0 + t u : t \ge 0\}$ with $u \ne 0$, and then it contains such a ray from each of its points. Take $x_0 = p$. The point $p + t u$ is in $H(p, q)$ for all $t \ge 0$ exactly when $2 (q - p) \cdot (p + t u) \le |q|^2 - |p|^2$ for all $t \ge 0$; at $t = 0$ this holds, and the condition on the coefficient of $t$ is $(q - p) \cdot u \le 0$. So $V(p)$ is unbounded exactly when some $u \ne 0$ has $u \cdot q \le u \cdot p$ for all $q \in P$, that is, when the line through $p$ normal to $u$ supports $P$. A point of $P$ is on such a supporting line exactly when it is on the boundary of the convex hull. $\square$
5. **Size.** $V(p)$ has at most $n - 1$ edges, since each edge is on the bisector of $p$ and one other site, and one convex set meets a line in at most one segment. Over all cells, the number of edges is at most $2 (3n - 6)$ when the sites are not all on one line, so the mean number of edges of a cell is less than $6$ ([Voronoi complexity theorem](/voronoi-complexity-theorem/)).
6. **Neighbours.** $V(p)$ and $V(q)$ share an edge of positive length exactly when $pq$ is an edge of every Delaunay triangulation, by [duality](/voronoi-delaunay-duality/).

## Examples and non-examples

- **A bounded cell.** For the sites $(0,0)$, $(4,0)$, $(0,4)$, $(4,4)$, $(2,2)$, the half-planes of $(2,2)$ are $x + y \ge 2$, $x - y \le 2$, $y - x \le 2$ and $x + y \le 6$. The cell is the square with corners $(2,0)$, $(4,2)$, $(2,4)$, $(0,2)$. It is bounded because $(2,2)$ is inside the convex hull. The corner $(2,0)$ is at distance $2$ from $(0,0)$, $(4,0)$ and $(2,2)$, so it is the [circumcenter](/circumcenter/) of these three sites.
- **An unbounded cell.** In the same set, the half-planes of $(0,0)$ are $x \le 2$, $y \le 2$, $x + y \le 2$ and $x + y \le 4$; the last one is redundant. The cell has two vertices, $(2,0)$ and $(0,2)$, one bounded edge between them, and two rays: from $(2,0)$ down along $x = 2$, and from $(0,2)$ left along $y = 2$. It has three edges, although there are four other sites.
- **Sites on a line.** For $(0,0)$, $(2,0)$, $(4,0)$, the cells are the strips $x \le 1$, $1 \le x \le 3$ and $x \ge 3$. All three are unbounded and have no vertex. The hull is the segment, which is all boundary, so property 4 applies to the middle site too.
- **Cocircular sites.** For the four corners of the square $(0,0), (2,0), (2,2), (0,2)$, each cell is a quadrant, and the four cells meet at the single point $(1,1)$. A vertex where four or more cells meet appears exactly when four or more sites are on one empty circle.
- **Non-example: weighted distance.** With the distance $|x - p| / w_p$, the cell of a light site can be a disc and the cell of a heavy site the outside of discs, which is not convex ([weighted Voronoi diagram](/weighted-voronoi-diagram/)). The cells of the [power diagram](/power-diagram/) stay convex but can be empty.
- **Non-example: nearest-point region of a segment.** For a site that is a segment, the cell is bounded in part by parabolic arcs, so it is not a polygon; see the [medial axis](/medial-axis/).

## Related definitions

- [Voronoi diagram](/voronoi-diagram/): the subdivision formed by all cells.
- [Order-k Voronoi diagram](/order-k-voronoi-diagram/): cells of the points whose $k$ nearest sites are a given set of $k$ sites.
- [Centroidal Voronoi tessellation](/centroidal-voronoi-tessellation/): a diagram whose sites are the centroids of their cells.
- [Largest empty circle](/largest-empty-circle/): its center is a vertex of a cell, or on a cell edge at the boundary of a given region.

## References
