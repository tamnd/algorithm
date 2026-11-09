---
tag: 0J56YS
kind: data-structure
slug: farthest-point-voronoi-diagram
name: Farthest-point Voronoi diagram
aliases:
- farthest-site Voronoi diagram
- furthest-point Voronoi diagram
- order-(n-1) Voronoi diagram
area: geometry/voronoi-and-delaunay
level: advanced
summary: Voronoi diagram where each cell holds the points for which a given site is the farthest; its vertices form a tree.
model: real-ram
complexity:
  vars: {n: the number of sites, h: the number of corners of the convex hull}
  time: {build: O(n log n), query: O(log h)}
  space: {extra: O(n)}
properties: {persistent: false, concurrent: false, external: false}
prereqs: [voronoi-diagram, convex-hull, in-circle-test, edge-flip]
see_also: [minimum-enclosing-circle, order-k-voronoi-diagram, paraboloid-lifting-map, lawson-flip-algorithm, farthest-pair, polygon-diameter, minimum-width-annulus, delaunay-triangulation]
sources:
  - paper: doi:10.1109/SFCS.1975.8
    title: M. I. Shamos and D. Hoey, Closest-point problems, 16th Annual Symposium on Foundations of Computer Science, 1975
    locator: the farthest-point Voronoi diagram and its use for the smallest enclosing circle
  - book: isbn:9783540779735
    title: M. de Berg, O. Cheong, M. van Kreveld and M. Overmars, Computational Geometry, Algorithms and Applications, third edition, Springer, 2008
    locator: Chapter 7, notes and exercises on the farthest-point Voronoi diagram
  - book: isbn:9780471986355
    title: A. Okabe, B. Boots, K. Sugihara and S. N. Chiu, Spatial Tessellations, Concepts and Applications of Voronoi Diagrams, second edition, Wiley, 2000
    locator: Chapter 3 (generalized Voronoi diagrams, including the farthest-point and order-k diagrams)
  - book: isbn:9781498711395
    title: J. E. Goodman, J. O'Rourke and C. D. Toth (editors), Handbook of Discrete and Computational Geometry, third edition, CRC Press, 2017
    locator: the chapter on Voronoi diagrams and Delaunay triangulations (farthest-point diagrams and the lifting map)
---

The farthest-point Voronoi diagram of a finite set $P$ of $n$ point sites in the plane splits the plane into cells by the *farthest* site: the cell of $p$ holds the points that are at least as far from $p$ as from any other site. Only the corners of the [convex hull](/convex-hull/) of $P$ have nonempty cells, every nonempty cell is unbounded, and the vertices and edges of the diagram form a tree with at most $h - 2$ vertices and $2h - 3$ edges, where $h$ is the number of hull corners. Its dual is the farthest-point Delaunay triangulation, whose circumcircles hold all the sites. The diagram answers "which site is farthest from this point", and it gives the [smallest enclosing circle](/minimum-enclosing-circle/) of the sites.

## In plain words

Put some shops on a map. Colour every place on the map by the shop that is farthest from it. A shop in the middle of the group is never the farthest from any place, so it gets no colour. Only the shops on the outer edge of the group get a region.

Each region goes on forever, away from its shop and across the group. The lines between regions never close into a loop: they form a tree.

A corner of the tree is a place that is equally far from three shops, and every other shop is closer. So the circle around that corner through those three shops holds all the shops. The smallest circle that holds all the shops has its center at such a corner, or in the middle between two shops.

## The abstract type

The diagram is a static structure over a set of distinct sites $p = (x, y)$, here with integer coordinates. It supports:

- $\mathrm{insert}(p)$: add a site, before or between queries.
- $\mathrm{vertices}()$: the vertices of the diagram, as exact rational points.
- $\mathrm{edges}()$: for each pair of sites $\{p, q\}$ whose cells share a piece of positive length, the two ends of that piece; an end at infinity is a ray.
- $\mathrm{sitesWithCells}()$: the sites with a nonempty cell, which are the hull corners, in counterclockwise order.
- $\mathrm{farthest}(q)$: a site farthest from the query point $q$.

Notation: $P$ is the set of sites, $n = |P|$, $h$ is the number of corners of the convex hull of $P$ (sites inside a hull edge do not count), $d$ is the degree of a vertex of the diagram, $\mathrm{orient}(a, b, c)$ is positive when $a, b, c$ turn counterclockwise, and $\mathrm{incircle}(a, b, c, d)$, for counterclockwise $a, b, c$, is positive when $d$ is strictly inside their circle and negative when it is strictly outside.

**Definitions.** The farthest cell of $p$ is $F_p = \{x : |x - p| \ge |x - s| \text{ for all } s \in P\}$. The inequality $|x - p|^2 \ge |x - s|^2$ is linear in $x$, so $F_p$ is an intersection of closed half-planes and is convex. A **vertex** is a point with three or more farthest sites. An **edge** is the relative interior of $F_p \cap F_q$ when this set has positive length. A point $x$ is a vertex exactly when the circle around $x$ through its farthest sites has three or more sites on it and all sites inside it or on it.

**Properties.** These are proved in [the correctness proof](proofs/correctness/).

- A site that is not a hull corner has an empty cell, and every hull corner has an unbounded cell.
- For $h \ge 3$, the vertices and edges form a tree with $h$ rays. It has at most $h - 2$ vertices and at most $2h - 3$ edges, with equality exactly when no four hull corners lie on one circle that holds all sites.
- For $h = 2$, which includes sites all on one line, the diagram is the bisector of the two extreme sites. For $h = 1$ the cell is the whole plane.
- The farthest-point diagram is the [order-k Voronoi diagram](/order-k-voronoi-diagram/) for $k = n - 1$: the points whose $n - 1$ nearest sites are $P \setminus \{p\}$ are the points whose farthest site is $p$.

**General position.** No assumption is made. Four or more hull corners on one circle that holds all sites give one vertex of higher degree, stored once. Sites on one line give $h = 2$.

## Representation

The code keeps the list of sites and, after a build, the hull corners $s_0, \ldots, s_{h-1}$ in counterclockwise order, the farthest-point Delaunay triangulation of the corners as counterclockwise index triples, and a map from each directed edge $(u, v)$ to the triangle on its left. From it, it stores the sorted list of distinct [circumcenters](/circumcenter/) as the vertices and a map from each pair of neighbouring sites to the ends of their edge. Inserting a site only marks the stored diagram as stale; the next query rebuilds it.

A triangle $abc$ of hull corners is **farthest Delaunay** when every site lies inside its circumcircle or on it. Under the [lifting map](/paraboloid-lifting-map/) $p \mapsto (x, y, x^2 + y^2)$, this says that all lifted sites lie on or below the plane through the lifted $a$, $b$ and $c$. So the farthest-point Delaunay triangulation is the projection of the upper convex hull of the lifted sites, while the usual [Delaunay triangulation](/delaunay-triangulation/) is the projection of the lower hull.

## Operations

```pseudo id=main
FARTHEST-BUILD(P)
L1  H ← the corners s_0, …, s_{h−1} of the convex hull of P, counterclockwise
L2  T ← the fan of triangles s_0 s_k s_{k+1}, for k = 1, …, h − 2
L3  S ← a stack of all inner edges of T
L4  while S is not empty do pop ab from S; skip it if it is no longer an edge; let abc and bad be its triangles
L5      if incircle(a, b, c, d) < 0 then
L6          replace abc and bad by adc and dbc; push ad, db, bc and ca on S
L7  for each triangle t of T do c(t) ← the circumcenter of t; the vertices ← the distinct values c(t)
L8  for each edge pq of T, with t on its left and t' on its right: a ray from c(t) if t' does not exist, else the segment from c(t) to c(t') if c(t) ≠ c(t')
```

- **Line L1.** The monotone chain algorithm with the test $\mathrm{orient} \le 0$ for popping removes interior sites and sites inside hull edges, in $O(n \log n)$ time. Interior sites have no cell, so the rest of the build uses only the $h$ corners, which are in strictly convex position: no three on a line.
- **Line L2.** Since the corners are in convex position, the fan from $s_0$ is a triangulation of the hull polygon, with $h - 2$ triangles and $h - 3$ inner edges.
- **Lines L4 to L6.** This is the [Lawson flip algorithm](/lawson-flip-algorithm/) with the opposite rule: an inner edge $ab$ is [flipped](/edge-flip/) when the opposite corner $d$ is strictly *outside* the circle of $abc$. Every quadrilateral of corners is convex, so every flip is legal. Each flip makes the lifted surface go up, so no triangulation comes back, and the loop ends after at most $h(h - 3)/2$ flips.
- **Line L7.** When the stack is empty, every inner edge passes the test, and this local condition makes every circumcircle hold all sites. Triangles inside one cocircular polygon have the same circumcenter, so they give one vertex.
- **Line L8.** A hull edge $pq$, directed counterclockwise, has one triangle. Its dual is a ray from $c(t)$ along the bisector of $p$ and $q$, toward the inside of the hull: points far out on that side are far from both $p$ and $q$. An inner edge whose triangles have different circumcenters gives the segment between them; with equal circumcenters it is a diagonal of a cocircular polygon and gives no edge.

**farthest(q).** The farthest site is always a hull corner, so the code scans the $h$ corners in $O(h)$ time. With a [planar point location](/planar-point-location/) structure over the $h$ cells, the query takes $O(\log h)$ time.

**Smallest enclosing circle.** The function $x \mapsto \max_s |x - s|$ is convex, and on each cell it equals the distance to the site of that cell. Its minimum, the center of the [smallest enclosing circle](/minimum-enclosing-circle/), is a vertex of the diagram, or the midpoint of $p$ and $q$ when that midpoint lies on the closed edge of $p$ and $q$: inside the cell of $p$ the function is the distance to $p$, which has no local minimum there because $p$ is not in its own cell, and inside an edge it is the distance to $p$ along the bisector, which is smallest at the midpoint. Checking the $O(h)$ candidates against the tree takes $O(h)$ time after the build.

## Example

Take the five sites $(0,0)$, $(6,0)$, $(6,4)$, $(0,6)$ and $(3,2)$. The site $(3,2)$ is inside the hull, so $h = 4$ and it gets no cell.

- **L1.** $H = (0,0), (6,0), (6,4), (0,6)$.
- **L2 and L3.** The fan from $(0,0)$ has the triangles $(0,0), (6,0), (6,4)$ and $(0,0), (6,4), (0,6)$, and the stack holds their common edge from $(0,0)$ to $(6,4)$.
- **L4 to L6.** The circle of $(0,0), (6,0), (6,4)$ has center $(3,2)$ and squared radius $13$. The corner $(0,6)$ is at squared distance $25$ from $(3,2)$, strictly outside, so $\mathrm{incircle} < 0$ and the edge is flipped. The new triangles are $(0,0), (6,0), (0,6)$ and $(6,0), (6,4), (0,6)$. The pushed edges are hull edges and are skipped, so the loop ends.
- **L7.** The circumcenters are $(3,3)$, with squared radius $18$, and $(2,2)$, with squared radius $20$. The circle around $(3,3)$ holds $(6,4)$ at squared distance $10$, and the circle around $(2,2)$ holds $(0,0)$ at squared distance $8$.
- **L8.** The inner edge from $(6,0)$ to $(0,6)$ gives the segment from $(2,2)$ to $(3,3)$, on the line $y = x$. The four hull edges give four rays: from $(3,3)$ upward for $(0,0), (6,0)$ and to the right for $(0,6), (0,0)$, and from $(2,2)$ to the left for $(6,0), (6,4)$ and in the direction $(-1, -3)$ for $(6,4), (0,6)$.

The diagram has $2 = h - 2$ vertices and $5 = 2h - 3$ edges, a tree. The cell of $(0,0)$ is the quadrant $x \ge 3$, $y \ge 3$, so $\mathrm{farthest}((10,10)) = (0,0)$. $\mathrm{farthest}((3,2)) = (0,6)$, at squared distance $25$. The smallest enclosing circle has center $(3,3)$ and squared radius $18$: it is the circle on the diameter from $(6,0)$ to $(0,6)$, whose midpoint is the end $(3,3)$ of their edge.

For the four corners of the square $(0,0)$, $(2,0)$, $(2,2)$, $(0,2)$, both triangles have the circumcenter $(1,1)$, so there is one vertex, the diagonal gives no edge, and the four hull edges give four rays from $(1,1)$.

## Correctness

**Theorem.** For distinct integer sites, FARTHEST-BUILD returns exactly the vertices of the farthest-point Voronoi diagram and, for each pair of sites whose farthest cells share a piece of positive length, the correct ends of that piece. $\mathrm{farthest}(q)$ returns a site at the largest distance from $q$.

The proof has four steps. A strictly convex function on the hull takes its maximum only at corners, so only corners can be farthest sites. The flip loop ends, because each flip raises the piecewise linear surface through the lifted corners, and when it ends every inner edge passes the test, which makes this surface concave; a concave surface through the lifted corners is the upper hull, so every triangle is farthest Delaunay. A vertex $x$ has a plane above all lifted sites that touches them exactly at its farthest sites, and that plane is the plane of some triangle of $T$, so its center is a circumcenter. For an edge, the circles through $p$ and $q$ form a pencil: moving the center along the bisector, sites on one side of the line $pq$ enter the circle and sites on the other side leave it, so the set of centers whose circle holds all sites is an interval whose ends are the circumcenters of the two triangles on $pq$. The full proof is in [the correctness proof](proofs/correctness/).

## Complexity

- **Build.** Line L1 takes $O(n \log n)$ time. The flips take $O(h^2)$ time in the worst case, since there are at most $h(h - 3)/2$ of them, each in $O(1)$ time with constant-time dictionary operations. Lines L7 and L8 take $O(h)$ time. So the code builds in $O(n \log n + h^2)$ worst-case time. The divide and conquer method of Shamos and Hoey, or a 3D convex hull of the lifted sites, builds it in $O(n \log n)$ worst-case time.
- **Lower bound.** Reading the rays around the tree gives the hull corners in order, so building the diagram is as hard as the [convex hull](/convex-hull-lower-bound/): $\Omega(n \log n)$ in the algebraic computation tree model.
- **Queries.** $\mathrm{vertices}$, $\mathrm{edges}$ and $\mathrm{sitesWithCells}$ return stored lists in $O(h)$ time. $\mathrm{farthest}(q)$ takes $O(h)$ time by a scan and $O(\log h)$ time with point location, after $O(h \log h)$ preprocessing.
- **Space.** $O(n)$ for the sites and $O(h)$ for the diagram.

## Variants

- **Both diagrams from one lifting.** The lower hull of the lifted sites gives the Delaunay triangulation and the nearest-point diagram, and the upper hull gives the farthest-point ones. One [3D convex hull](/convex-hull-3d/) gives both.
- **Convex polygons in linear time.** When the hull corners are already known in order, the diagram can be built in $O(h)$ time by the deterministic method of Aggarwal, Guibas, Saxe and Shor, and in $O(h)$ expected time by Chew's randomized method, which removes the corners in random order and puts them back.
- **Order-k diagrams.** The farthest-point diagram is the order-$(n - 1)$ diagram, the last of the [order-k Voronoi diagrams](/order-k-voronoi-diagram/).
- **Other sites.** Farthest-point diagrams of segments or polygons, and of weighted sites in the power distance, follow the same idea; the power version is again the projection of an upper hull.
- **Higher dimensions.** In $\mathbb{R}^d$ the farthest-point diagram is the projection of the upper hull of the lifted sites in $\mathbb{R}^{d+1}$, and its cells are again the hull corners.

## When to use it

Use it for farthest-site queries on a fixed set of sites, for all farthest neighbours, for the [farthest pair](/farthest-pair/), and for the [minimum width annulus](/minimum-width-annulus/), whose center is found by overlaying the nearest-point and the farthest-point diagrams. For the smallest enclosing circle alone, Welzl's randomized algorithm in $O(n)$ expected time is simpler; the diagram is the better choice when many enclosing-circle or farthest-point questions are asked of the same sites, or when the structure of the problem is needed, as in the 1-center problem with constraints.

## Pitfalls

- **The flip rule at line L5.** The rule is the opposite of the Delaunay rule. Flipping when $d$ is strictly inside the circle gives the nearest-point Delaunay triangulation, and its circumcenters are not vertices of this diagram.
- **The ray direction at line L8.** A ray of the farthest-point diagram points toward the inside of its hull edge, the opposite of the nearest-point diagram. A ray can start outside the hull and cross it.
- **Interior sites and sites inside hull edges.** They must be dropped at line L1. Keeping a site inside a hull edge makes three collinear corners, a flat triangle with no circumcenter, and a site with an empty cell.
- **Cocircular corners at lines L7 and L8.** Four or more corners on a circle that holds all sites give several triangles with one circumcenter. Without the test for equal centers, the diagram gets an edge of length zero and a vertex twice.
- **Floating-point circumcenters.** Rounding can split one vertex in two or reverse a flip decision; use exact predicates and exact centers, as the code does with integers and fractions.
- **$h \le 2$.** Sites on one line give no triangle; the diagram is one line, the bisector of the two extreme sites, and the code stores it with both ends at infinity.

## Implementations

## History

M. I. Shamos and D. Hoey introduced the farthest-point Voronoi diagram in 1975, in the same paper as the nearest-point diagram in computational geometry, and used it to find the smallest enclosing circle in $O(n \log n)$ time. K. Q. Brown in 1979 obtained Voronoi diagrams from 3D convex hulls through an inversion, and the paraboloid form of the lifting map, with the lower hull for the nearest and the upper hull for the farthest diagram, became the standard view, extended to all orders by H. Edelsbrunner and R. Seidel in 1986. N. Megiddo in 1983 found the smallest enclosing circle in $O(n)$ time without the diagram. A. Aggarwal, L. J. Guibas, J. Saxe and P. W. Shor in 1989 gave a linear-time algorithm for the Voronoi diagram of a convex polygon, and L. P. Chew in 1990 gave a simple randomized one.

## References
