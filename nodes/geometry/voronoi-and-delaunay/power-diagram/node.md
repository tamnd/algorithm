---
tag: N5KV10
kind: data-structure
slug: power-diagram
name: Power diagram
aliases:
- Laguerre diagram
- Laguerre-Voronoi diagram
- radical Voronoi tessellation
area: geometry/voronoi-and-delaunay
level: advanced
summary: Voronoi-like partition using power distance to weighted sites; its dual is the regular triangulation.
model: real-ram
complexity:
  vars: {n: the number of sites}
  time: {build: O(n log n), query: O(log n)}
  space: {extra: O(n)}
properties: {persistent: false, concurrent: false, external: false}
prereqs: [voronoi-diagram, half-plane-intersection, circumcircle]
see_also: [regular-triangulation, paraboloid-lifting-map, weighted-voronoi-diagram, convex-hull-3d, alpha-shape, order-k-voronoi-diagram, centroidal-voronoi-tessellation, planar-point-location]
sources:
  - paper: "F. Aurenhammer, Power diagrams: properties, algorithms and applications, SIAM Journal on Computing 16(1), 1987, 78-96"
    locator: the definition, the lifting to a convex polyhedron, the O(n log n) construction, redundant sites and applications
  - paper: "H. Imai, M. Iri and K. Murota, Voronoi diagram in the Laguerre geometry and its applications, SIAM Journal on Computing 14(1), 1985, 93-105"
    locator: the Laguerre Voronoi diagram of circles and its O(n log n) construction
  - book: isbn:9781498711395
    title: J. E. Goodman, J. O'Rourke and C. D. Toth (editors), Handbook of Discrete and Computational Geometry, third edition, CRC Press, 2017
    locator: the chapter on Voronoi diagrams and Delaunay triangulations (power diagrams and regular triangulations)
  - book: isbn:9780471986355
    title: A. Okabe, B. Boots, K. Sugihara and S. N. Chiu, Spatial Tessellations, Concepts and Applications of Voronoi Diagrams, second edition, Wiley, 2000
    locator: Chapter 3 (weighted Voronoi diagrams, including the power diagram)
---

The power diagram of $n$ weighted sites in the plane splits the plane into cells by the *power distance* $|x - p|^2 - w_p$, where $w_p$ is the weight of the site $p$: the cell of $p$ holds the points whose power distance to $p$ is the smallest. If $w_p = r^2$, the power distance is the power of $x$ with respect to the circle of radius $r$ around $p$. The bisector of two sites is a straight line, so every cell is a convex polygon, as in the [Voronoi diagram](/voronoi-diagram/), which is the case of equal weights. Unlike there, a cell can be empty and a site can lie outside its own cell. The power diagram is the projection of a convex polyhedron in space, its dual is the [regular triangulation](/regular-triangulation/), and it is built in $O(n \log n)$ time.

## In plain words

Draw a circle around each site; a larger circle means a heavier site. For a point outside a circle, measure the length of the line from the point that just touches the circle. Colour every point by the circle with the shortest such touching line. Points inside a circle count as closer than points on it.

The border between two colours is always a straight line. For two circles that cross, it is the line through the two crossing points. So every region is a convex shape, as in the usual nearest-site map.

A big circle pushes its border away and takes space from its neighbours. A small circle near big ones can lose all its space and get no region at all.

## The abstract type

The diagram is a static structure over distinct sites $p = (x, y)$ with integer coordinates and integer weights $w_p$, which can be negative. It supports:

- $\mathrm{insert}(p, w)$: add a site with its weight, before or between queries.
- $\mathrm{cells}()$: for each site whose cell has nonempty interior, the cell clipped to a box, as a counterclockwise convex polygon with exact rational corners, and whether the cell is bounded.
- $\mathrm{isRedundant}(p)$: whether the cell of $p$ has empty interior.
- $\mathrm{vertices}()$: the vertices of the diagram, sorted.
- $\mathrm{locate}(q)$: the sites of smallest power distance at $q$; several only on a cell boundary.

Notation: $P$ is the set of sites, $n = |P|$, $h$ is the number of sites on the boundary of the convex hull, $d$ is the number of sides of a cell, $\mathrm{orient}(a, b, c)$ is positive when $a, b, c$ turn counterclockwise, and $\mathrm{incircle}(a, b, c, d)$, for counterclockwise $a, b, c$, is positive when $d$ is strictly inside their circle.

**Definitions.** The power distance of a point $x$ to the site $p$ with weight $w_p$ is $\pi_p(x) = |x - p|^2 - w_p$. The cell of $p$ is $C_p = \{x : \pi_p(x) \le \pi_q(x) \text{ for all } q \in P\}$. For two sites $p \ne q$,

$$\pi_p(x) \le \pi_q(x) \iff 2 (q - p) \cdot x \le |q|^2 - w_q - |p|^2 + w_p,$$

a closed half-plane bounded by a line perpendicular to $pq$, the **power bisector** or radical axis. So $C_p$ is an intersection of half-planes and is convex. A site is **redundant** when its cell has empty interior. A **vertex** is a corner of a cell with nonempty interior; it lies on two power bisectors that are not parallel, so it is the **radical center** of three sites, the point with equal power distance to all three.

**Properties.** These are proved in [the correctness proof](proofs/correctness/), except the size bound, which is cited.

- **Equal weights.** If all weights are equal, $C_p$ is the Voronoi cell of $p$. Adding the same constant to all weights changes nothing.
- **Shifted bisectors.** The power bisector of $p$ and $q$ lies at distance $(w_p - w_q)/(2 |p - q|)$ from the ordinary bisector, on the side of the site with the smaller weight. For two crossing circles it is the line through the two crossing points.
- **Empty cells and sites outside cells.** A site $p$ with $\pi_q(p) < \pi_p(p) = -w_p$ for some $q$ is not in its own cell, and its cell can be empty.
- **Lifting.** $\pi_p(x) = |x|^2 - \ell_p(x)$ with the affine function $\ell_p(x) = 2 p \cdot x - |p|^2 + w_p$. So $C_p$ is where $\ell_p$ is the largest: the diagram is the projection of the upper envelope of the $n$ planes $z = \ell_p(x)$. A site is not redundant exactly when the lifted point $(p, |p|^2 - w_p)$ is a corner of the lower convex hull of the lifted sites. The lower hull projects to the regular triangulation; for zero weights this is the [lifting map](/paraboloid-lifting-map/) of the Delaunay triangulation.
- **Size (cited).** With $m \ge 3$ nonredundant sites and at least one vertex, there are at most $2m - 5$ vertices and $3m - 6$ edges, by the same Euler count as in the [Voronoi complexity theorem](/voronoi-complexity-theorem/).
- **Sections of Voronoi diagrams.** For sites $(p, z_p)$ in space, the Voronoi diagram restricted to the plane $z = 0$ is the power diagram of the points $p$ with weights $-z_p^2$, because $|(x, 0) - (p, z_p)|^2 = |x - p|^2 + z_p^2$.

**General position.** No assumption is made. Three sites with collinear centers give parallel bisectors and no radical center. Four or more sites with one radical center give a vertex of higher degree. Redundant sites, including sites whose cell is a segment or a point, are reported and have no stored cell.

## Representation

The code keeps the lists of sites and weights and, after a build, a box $B$ and a dictionary from each nonredundant site to its cell clipped to $B$, with a flag for bounded cells. The box holds every site, every radical center of three sites and one point of every power bisector, with a margin of $1$. So every vertex of the diagram is strictly inside $B$, every cell with nonempty interior meets the inside of $B$, and a cell is unbounded exactly when its clipped polygon touches the boundary of $B$.

A full structure stores the diagram as a [doubly connected edge list](/doubly-connected-edge-list/), or stores the dual regular triangulation and computes the vertices as radical centers, as the [Voronoi diagram](/voronoi-diagram/) page does with circumcenters. Inserting a site only marks the stored diagram as stale; the next query rebuilds it.

## Operations

```pseudo id=main
POWER-BUILD(P, w)
L1  B ← a box that holds all sites, all radical centers of three sites and a point of every power bisector
L2  for each site p_i do
L3      C ← B
L4      for each other site p_j do
L5          C ← C ∩ {x : π_i(x) ≤ π_j(x)}, a half-plane bounded by the power bisector of p_i and p_j
L6      if C has nonempty interior then store C as the cell of p_i, bounded exactly when C does not touch the boundary of B
L7  the sites with no stored cell are redundant
```

- **Line L1.** The radical center of $p_i$, $p_j$ and $p_k$ is the crossing point of two bisector lines, found by Cramer's rule when the lines are not parallel. The point of the bisector $a x + b y = c$ nearest to the origin is $(a c, b c)/(a^2 + b^2)$. There are $O(n^3)$ candidates.
- **Lines L3 to L5.** Each step cuts a convex polygon by a half-plane, exactly, with fractions; this is a [half-plane intersection](/half-plane-intersection/) done one half-plane at a time.
- **Line L6.** A cutting step returns no polygon when the result has zero area, which happens exactly for a redundant site, because every cell with nonempty interior meets the inside of $B$. The bounded test is that all corners are strictly inside $B$.
- **vertices.** The corners of the stored polygons that are strictly inside $B$ are the vertices of the diagram.
- **locate(q).** The code compares the $n$ power distances in $O(n)$ time. With a [planar point location](/planar-point-location/) structure over the cells, a query takes $O(\log n)$ time.

**Building in O(n log n) time.** Compute the lower convex hull of the lifted points $(p, |p|^2 - w_p)$ with a [3D convex hull](/convex-hull-3d/) algorithm in $O(n \log n)$ time. Its corners are the nonredundant sites, its faces project to the regular triangulation, and the vertices of the power diagram are the points $x$ whose plane $z = 2 x \cdot y + c$ contains a face. Randomized incremental insertion, as for the Delaunay triangulation, also works in $O(n \log n)$ expected time, with an extra case for a site that is redundant when it is inserted.

## Example

Take the five sites $(0,0)$ with weight $16$, $(6,0)$ with weight $9$, $(3,5)$ with weight $16$, $(7,6)$ with weight $0$ and $(3,2)$ with weight $0$: circles of radius $4$, $3$, $4$, and two points.

- **L1.** The box is $[-9/2, 335/34] \times [-99/34, 27/2]$.
- **L2 to L5 for $(0,0)$ and $(6,0)$.** Their power bisector is $12 x \le 43$, the line $x = 43/12$. The ordinary bisector is $x = 3$; the heavier site $(0,0)$ pushes the line toward $(6,0)$.
- **L6 for $(3,2)$.** At its own position, $(3,2)$ has power distance $0$, but $(3,5)$ has power distance $9 - 16 = -7$ there, and $(0,0)$ has $13 - 16 = -3$. The cell of $(3,2)$ is empty, so it is redundant, while in the ordinary Voronoi diagram it would have a bounded cell.
- **L7.** The four other cells are unbounded. The diagram has two vertices: $(43/12, 5/4)$, the radical center of the three circles around $(0,0)$, $(6,0)$ and $(3,5)$, with power distance $-115/72$ to each, so it lies inside all three circles; and $(172/23, 165/46)$, the radical center of $(6,0)$, $(3,5)$ and $(7,6)$, with power distance $12805/2116$ to each.

The diagram has five edges: the segment between the two vertices, on the bisector of $(6,0)$ and $(3,5)$, and four rays. $\mathrm{locate}((3,2))$ returns $(3,5)$, and $\mathrm{locate}((43/12, 5/4))$ returns the three sites $(0,0)$, $(6,0)$, $(3,5)$.

## Correctness

**Theorem.** For distinct integer sites with integer weights, POWER-BUILD stores a cell exactly for the nonredundant sites, each cell clipped to $B$ is computed exactly, the bounded flag is right, $\mathrm{vertices}$ returns exactly the vertices of the diagram, and $\mathrm{locate}(q)$ returns exactly the sites of smallest power distance at $q$.

The proof rests on the box. Every vertex is a radical center, so it is strictly inside $B$. A cell with a corner meets the inside of $B$ near that corner; a cell with no corner is the plane, a half-plane or a strip, whose boundary lines are whole power bisectors, each with a point inside $B$. So clipping to $B$ loses no cell, and a bounded cell, the convex hull of its corners, lies inside $B$, while an unbounded one must cross the boundary of $B$. The full proof, with the lifting property, is in [the correctness proof](proofs/correctness/).

## Complexity

- **Build.** $O(n \log n)$ worst-case time through the 3D lower hull of the lifted points, which is optimal in the algebraic computation tree model, because equal weights give the Voronoi diagram ([lower bound](/voronoi-construction-lower-bound/)). The code takes $O(n^3)$ time: $O(n^3)$ candidates for the box, and $n$ cells, each cut $n - 1$ times, where a cut takes time linear in the polygon, which has at most $n + 3$ sides.
- **Size.** $O(n)$ vertices, edges and cells (cited above).
- **Query.** $O(\log n)$ with point location; the code takes $O(n)$.
- **Space.** $O(n)$ for the diagram; the code stores each clipped cell, $O(n)$ corners in all for the vertices plus the corners on the box.

## Variants

- **Regular triangulation.** The dual of the power diagram: two nonredundant sites are joined when their cells share an edge ([regular triangulation](/regular-triangulation/)).
- **Weighted alpha shapes.** The power diagram restricted to the union of the circles splits the union into convex pieces, one per circle; weighted [alpha shapes](/alpha-shape/) of atoms in molecules use it to compute areas and volumes of unions of balls.
- **Order-k power diagrams.** Cells by the $k$ sites of smallest power distance, again projections of levels of an arrangement of planes ([order-k Voronoi diagram](/order-k-voronoi-diagram/)).
- **Additively weighted diagram.** The distance $|x - p| - w_p$ gives hyperbolic bisectors and is a different diagram ([weighted Voronoi diagram](/weighted-voronoi-diagram/)).
- **Optimal transport and capacity constraints.** Choosing weights so that each cell has a prescribed area or mass gives the semi-discrete optimal transport map for the squared distance; these are found by a convex optimization over the weights.
- **Higher dimensions.** In $\mathbb{R}^d$ the definition is the same, and the diagram is the projection of the upper envelope of hyperplanes in $\mathbb{R}^{d+1}$.

## When to use it

Use the power diagram when sites have sizes, such as disks, atoms or service areas with different capacities, and straight borders and convex cells are wanted. It is the right tool for the union and the intersection of disks or balls, for the area of a union of disks, for weighted Delaunay meshes, for semi-discrete optimal transport, and for sections of 3D Voronoi diagrams. If the distance must be the Euclidean distance minus a radius, as for the region nearest to the boundary of a disk, use the additively weighted diagram instead.

## Pitfalls

- **Redundant sites.** A site can have an empty cell when nearby sites have much larger weights. Algorithms that assume one cell per site, such as a Delaunay-style insertion without the redundancy test, break.
- **Sites outside their cells.** Point location must not start at the site's own position: the site need not be in its cell.
- **Power bisectors are not halfway.** The bisector is shifted by $(w_p - w_q)/(2 |p - q|)$; using the midpoint gives the ordinary Voronoi diagram.
- **Weights are squared radii.** Mixing radii and squared radii gives a wrong diagram that still looks plausible.
- **Clipping box.** A box that is too small loses vertices and whole cells; the code makes the box hold every radical center and a point of every bisector.
- **Floating-point radical centers.** Nearly parallel bisectors give radical centers far away and with large rounding error; exact arithmetic avoids this.

## Implementations

## History

The power of a point with respect to a circle is classical, and the geometry of oriented circles in which it is the natural distance is named after E. Laguerre. H. Imai, M. Iri and K. Murota studied the Voronoi diagram in the Laguerre geometry in 1985 and built it in $O(n \log n)$ time. F. Aurenhammer in 1987 gave the systematic theory under the name power diagram: the lifting to a convex polyhedron, the construction through 3D convex hulls, redundant sites, and many applications. H. Edelsbrunner and coauthors used the dual regular triangulations for weighted alpha shapes and for the geometry of molecules.

## References
