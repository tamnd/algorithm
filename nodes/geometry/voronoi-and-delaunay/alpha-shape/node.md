---
tag: NVRCS8
kind: data-structure
slug: alpha-shape
name: Alpha shape
aliases:
- alpha complex
- alpha filtration
- α-shape
area: geometry/voronoi-and-delaunay
level: advanced
summary: Family of shapes obtained by carving the Delaunay triangulation according to a radius parameter alpha.
model: real-ram
complexity:
  vars: {n: the number of input points, k: the number of simplices reported}
  time: {build: O(n log n), query: O(log n + k)}
  space: {extra: Θ(n)}
prereqs: [delaunay-triangulation, voronoi-diagram, circumcircle, gabriel-graph]
see_also: [voronoi-cell, regular-triangulation, power-diagram, medial-axis, convex-hull, euclidean-minimum-spanning-tree, empty-circle-property, delaunay-triangulation-construction]
sources:
  - paper: doi:10.1109/TIT.1983.1056714
    title: H. Edelsbrunner, D. G. Kirkpatrick and R. Seidel, On the shape of a set of points in the plane, IEEE Transactions on Information Theory 29(4), 1983
    locator: the whole paper (the alpha-hull and the alpha-shape of a planar point set, and their computation from the Delaunay triangulation in O(n log n) time)
  - paper: doi:10.1145/174462.156635
    title: H. Edelsbrunner and E. P. Mücke, Three-dimensional alpha shapes, ACM Transactions on Graphics 13(1), 1994
    locator: the alpha complex as a subcomplex of the Delaunay complex, the intervals of the simplices, and the filtration
  - book: isbn:9780521793094
    title: H. Edelsbrunner, Geometry and Topology for Mesh Generation, Cambridge University Press, 2001
    locator: the chapters on the union of balls and on alpha complexes and their filtrations
  - book: isbn:9781498711395
    title: J. E. Goodman, J. O'Rourke and C. D. Tóth (editors), Handbook of Discrete and Computational Geometry, third edition, CRC Press, 2017
    locator: the chapters on Voronoi diagrams and Delaunay triangulations and on topological methods (alpha shapes as a filtration of the Delaunay complex)
---

The alpha shapes of a point set $P$ are a family of shapes, one for each value of a scale parameter $\alpha$, cut out of the [Delaunay triangulation](/delaunay-triangulation/). For small $\alpha$ the shape is the points themselves. As $\alpha$ grows, edges and triangles of the Delaunay triangulation enter one at a time, and for large $\alpha$ the shape is the [convex hull](/convex-hull/). The **alpha complex** $K_\alpha$ is the set of Delaunay simplices that enter by scale $\alpha$, and the **alpha shape** is the region they cover. Each simplex has one entry value, so the whole family is stored as a list of $O(n)$ simplices sorted by value, the **alpha filtration**.

## In plain words

Draw a disk of the same size around every point. Two points get an edge when their disks touch inside the region that is closer to them than to any other point. Three points get a triangle when their three disks meet in one spot of that kind.

Now let the disks grow slowly. More edges and triangles appear, and the drawn shape fills in. Small disks show only the points. Medium disks show the outline of the cloud, with its holes and dents. Very large disks show the full convex outline.

Every edge and triangle used is one of the Delaunay triangulation. So compute the Delaunay triangulation once, give each piece the disk size at which it appears, and sort the pieces by that size. The shape for any size is then a prefix of the sorted list.

## The abstract type

The structure holds a finite set $P$ of points $p = (x, y)$ with integer coordinates and answers these operations.

- $\mathrm{insert}(p)$: add a point; return false if it is already present.
- $\mathrm{filtration}()$: all Delaunay simplices (vertices, edges, triangles), each with its entry value, sorted by value.
- $\mathrm{complex}(\alpha)$: the simplices of $K_\alpha$, those with value at most $\alpha$.
- $\mathrm{boundary}(\alpha)$: the edges of $K_\alpha$ with at most one triangle of $K_\alpha$ on them. They draw the outline of the alpha shape.

On this page $\alpha$ is a **squared radius**, as in the CGAL library; other texts use the radius, or its inverse. Notation: $n = |P|$, $D$ is the Delaunay triangulation of $P$, $V(p)$ is the [Voronoi cell](/voronoi-cell/) of $p$, and for a simplex $\sigma$ the **dual face** is $V(\sigma) = \bigcap_{p \in \sigma} V(p)$: a cell, a [Voronoi diagram](/voronoi-diagram/) edge or a Voronoi vertex. The **value** of $\sigma$ is

$$\rho(\sigma) = \min_{z \in V(\sigma)} |z - p|^2 \quad \text{for any vertex } p \text{ of } \sigma,$$

which does not depend on the choice of $p$, because $z$ is at the same distance from all vertices of $\sigma$. Then $K_\alpha = \{\sigma \in D : \rho(\sigma) \le \alpha\}$. In words, $\sigma$ is in $K_\alpha$ when the disks of squared radius $\alpha$ around its vertices have a common point in $V(\sigma)$. This is the nerve of the sets $B(p, \sqrt{\alpha}) \cap V(p)$.

## Representation

The structure stores the point list and, after the first query, the sorted filtration: a list of pairs (value, simplex), each simplex a sorted tuple of points. The values are exact fractions. A planar Delaunay triangulation has at most $3n - 6$ edges and $2n - 5$ triangles, so the list has fewer than $6n$ entries. An insertion marks the list as stale, and the next query rebuilds it. A triangulation with four or more cocircular points is not unique; the structure then uses the triangulation of its Delaunay code, and the values of its simplices are still the values $\rho$ above.

## Operations

```pseudo id=main
BUILD-FILTRATION(P)
L1  D ← the Delaunay triangulation of P
L2  ρ(v) ← 0 for each vertex v
L3  for each triangle t of D do ρ(t) ← the squared circumradius of t
L4  for each edge e = uv of D, with the vertices opposite e in its triangles do
L5      gabriel ← no opposite vertex is strictly inside the circle with diameter uv
L6      if gabriel then ρ(e) ← |u − v|² / 4
L7      else ρ(e) ← the smallest ρ(t) over the triangles t on e
L8  return all simplices of D sorted by ρ
```

- **Line L1** uses an exact Delaunay code. For collinear input there is no triangle, and $D$ is the path through the points in sorted order.
- **Line L3.** The dual face of a triangle is its [circumcenter](/circumcenter/), so its value is the squared radius of its [circumcircle](/circumcircle/).
- **Line L5** is the [Gabriel graph](/gabriel-graph/) test. The code compares $|2w - (u + v)|^2$ with $|u - v|^2$, which is four times the comparison of $|w - m|^2$ with the squared radius, with $m$ the midpoint; so it stays in integers.
- **Lines L6 and L7.** If the edge is Gabriel, the nearest point of its Voronoi edge to $u$ is the midpoint of $uv$. Otherwise it is the end of the Voronoi edge nearer to the midpoint, which is the circumcenter of one of the triangles on $e$.

The queries are short. $\mathrm{complex}(\alpha)$ returns the prefix of the list with value at most $\alpha$; the code scans the list, and a [binary search](/binary-search/) on the values gives the prefix in $O(\log n)$ time. $\mathrm{boundary}(\alpha)$ counts for each edge of the prefix the triangles of the prefix on it.

## Example

Take the six points $(0,0), (4,0), (8,0), (2,3), (6,3), (4,9)$. Their Delaunay triangulation has 9 edges and 5 triangles: three small triangles in a row at the bottom, one triangle $(2,3), (6,3), (4,9)$ above them, and two thin triangles on the left and right sides. The filtration is:

| value $\rho$ | simplices that enter | size of $K_\alpha$ |
| --- | --- | --- |
| $0$ | the 6 vertices | 6 |
| $13/4$ | the edges $(0,0)(2,3)$, $(2,3)(4,0)$, $(4,0)(6,3)$, $(6,3)(8,0)$ | 10 |
| $4$ | the edges $(0,0)(4,0)$, $(4,0)(8,0)$, $(2,3)(6,3)$ | 13 |
| $169/36$ | the three bottom triangles | 16 |
| $10$ | the edges $(2,3)(4,9)$, $(4,9)(6,3)$ | 18 |
| $100/9$ | the triangle $(2,3)(6,3)(4,9)$ | 19 |
| $6305/18$ | the edges $(0,0)(4,9)$, $(4,9)(8,0)$ and the two side triangles | 23 |

All edges of value $13/4$, $4$ and $10$ are Gabriel: for $(0,0)(4,0)$ the circle with diameter that edge has center $(2,0)$ and radius $2$, and the opposite vertex $(2,3)$ is at distance $3$. The side edge $(0,0)(4,9)$ is not Gabriel, because $(2,3)$ is inside its diametral circle. So it enters with its only triangle, at the large value $6305/18$. For $100/9 \le \alpha < 6305/18$ the alpha shape is the six-sided polygon $(0,0), (4,0), (8,0), (6,3), (4,9), (2,3)$, with a dent on each side, and for $\alpha \ge 6305/18$ it is the convex hull.

## Correctness

**Theorem.** In general position, BUILD-FILTRATION gives each simplex $\sigma$ of $D$ its value $\rho(\sigma)$. Every face of a simplex has a value no larger than the simplex, so each $K_\alpha$ is a simplicial complex.

The key facts are these. The dual face of a vertex holds the vertex, and of a triangle is its circumcenter, which gives lines L2 and L3. The dual face of an edge $uv$ is a piece of the bisector of $u$ and $v$ whose ends are the circumcenters of the triangles on $uv$ (a ray for a hull edge), and the squared distance to $u$ along the bisector grows with the distance from the midpoint. The midpoint is in the closed Voronoi edge exactly when no point of $P$ is strictly inside the circle with diameter $uv$. For a Delaunay edge, it is enough to test the opposite vertices: if a point $q$ is strictly inside that circle on one side of $uv$, the empty circumcircle of the triangle on that side must have its arc on that side inside the diametral circle, so the opposite vertex is inside it too. The face rule holds because $V(\sigma) \subseteq V(\tau)$ when $\tau \subseteq \sigma$. The full proof is in [the correctness proof](proofs/correctness/).

## Complexity

| operation | time | notes |
| --- | --- | --- |
| build (lines L1 to L8) | $O(n \log n)$ with an optimal Delaunay code | $O(n^2)$ worst case with the incremental code used here; the values take $O(n)$ and the sort $O(n \log n)$ |
| insert | $O(n)$ | the duplicate test scans the list; the list is rebuilt lazily |
| complex($\alpha$) | $O(\log n + k)$ | $k$ simplices reported, after the build; the code scans in $O(n)$ |
| boundary($\alpha$) | $O(n)$ | one pass over the prefix |
| space | $\Theta(n)$ | fewer than $6n$ simplices |

The time to compute all alpha shapes at once is dominated by the Delaunay triangulation, so it is $\Theta(n \log n)$ in the worst case, and the [lower bound](/voronoi-construction-lower-bound/) for Delaunay triangulations applies. The bounds are on the [real RAM](/real-ram/); the code uses integer and fraction arithmetic of bounded degree.

## Variants

- **Weighted alpha shapes.** Give each point a weight, use the [power diagram](/power-diagram/) in place of the Voronoi diagram and the [regular triangulation](/regular-triangulation/) in place of $D$. This models a union of disks of different radii, for example atoms in a molecule.
- **Three dimensions.** Edelsbrunner and Mücke defined the same filtration for tetrahedra, triangles, edges and vertices of the 3D Delaunay triangulation. It is the standard tool for the shape of molecules and of scanned point clouds.
- **Alpha hull.** The first definition of Edelsbrunner, Kirkpatrick and Seidel used the complement of the union of all empty disks of radius $1/\alpha$. Negative $\alpha$ gives shapes based on the [farthest-point Voronoi diagram](/farthest-point-voronoi-diagram/).
- **Persistence.** The filtration is the input to persistent homology: the values at which holes appear and disappear measure the size of the holes.

## When to use it

Use it to get the outline of a point cloud at a chosen scale, to find holes and dents, or to study the shape at all scales at once through the filtration. It costs one Delaunay triangulation and a sort. If only one scale matters and the points are dense, simpler outlines (a grid or a concave hull heuristic) can be enough, but they lack the exact link to the union of disks. The alpha shape needs a choice of $\alpha$, and the filtration helps to choose it.

## Pitfalls

- **Radius or squared radius.** Libraries differ. The values on this page and in line L3 are squared radii; a radius $r$ corresponds to $\alpha = r^2$.
- **Giving every edge the value $|u - v|^2 / 4$.** Line L7 is needed: an edge that is not Gabriel enters only with one of its triangles. Without line L7, $K_\alpha$ can contain an edge whose dual Voronoi edge is far from both ends, and the result is not the nerve of the disks.
- **Testing all points in line L5.** Only the two opposite vertices need a test, by the lemma in the correctness proof. A test against all points is correct but costs $O(n)$ per edge.
- **Float circumradii in line L3.** Two simplices with the same exact value can get different float values, so the order of the filtration and the complex at that value change. Use fractions, or compare exact rational values.

## Implementations

## History

Herbert Edelsbrunner, David Kirkpatrick and Raimund Seidel defined alpha shapes of planar point sets in 1983, as a formal version of the "shape" of a point set, and computed all of them from the Delaunay triangulation in $O(n \log n)$ time. Edelsbrunner and Ernst Mücke extended the idea to three dimensions in 1994, with the alpha complex as a filtration of the Delaunay complex, and released a widely used program. Edelsbrunner showed in 1995 that the alpha complex has the same homotopy type as the union of the disks. Alpha complexes are now a basic tool in computational topology and in the study of molecules.

## References
