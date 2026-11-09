---
tag: 06RTM0
kind: technique
slug: delaunay-refinement
name: Delaunay refinement
aliases:
- Delaunay mesh refinement
- circumcenter insertion
area: geometry/triangulations
level: advanced
summary: Insert circumcentres of bad triangles to improve triangle quality while keeping Delaunay properties.
prereqs: [delaunay-triangulation, constrained-delaunay-triangulation, bowyer-watson-algorithm, steiner-points]
see_also: [ruppert-algorithm, chew-second-algorithm, mesh-generation, conforming-delaunay-triangulation, constrained-triangulation, in-circle-test, tetrahedralization, max-min-angle-triangulation]
sources:
  - paper: doi:10.1016/S0925-7721(01)00047-5
    title: Jonathan Richard Shewchuk, Delaunay refinement algorithms for triangular mesh generation, Computational Geometry 22(1-3), 21 to 74 (2002)
    locator: Section 2 (the key idea), Section 3 (Ruppert's algorithm and the insertion radius analysis), Section 4 (Chew's second algorithm), Section 6 (small input angles)
  - paper: doi:10.1006/jagm.1995.1021
    title: Jim Ruppert, A Delaunay refinement algorithm for quality 2-dimensional mesh generation, Journal of Algorithms 18(3), 548 to 585 (1995)
    locator: the algorithm with diametral circles and the termination proof
  - paper: "L. Paul Chew, Guaranteed-quality mesh generation for curved surfaces, Proceedings of the 9th Symposium on Computational Geometry, 274 to 280 (1993)"
    locator: the constrained Delaunay refinement with visibility of circumcenters
  - book: isbn:9781584887300
    title: Siu-Wing Cheng, Tamal K. Dey and Jonathan Richard Shewchuk, Delaunay Mesh Generation, CRC Press, 2012
    locator: Chapter 6 (2D Delaunay refinement) and Chapters 8 to 10 (tetrahedral refinement and sliver removal; ISBN to be checked)
  - paper: "Jonathan Richard Shewchuk, Tetrahedral mesh generation by Delaunay refinement, Proceedings of the 14th Symposium on Computational Geometry, 86 to 95 (1998)"
    locator: the three-dimensional algorithm with radius-edge ratio bound 2
---

Delaunay refinement is a technique for building good meshes: start from a Delaunay or constrained Delaunay triangulation of the input, and repeatedly insert a new vertex at the circumcenter of a badly shaped triangle, until no bad triangle is left. Input segments are protected by splitting them at their midpoints when a vertex comes too close. The circumcenter is the point of the triangle's circumcircle farthest from its corners, and the Delaunay property guarantees that no vertex is closer to it than the circumradius, so each new vertex is far from the others, and a packing argument shows that the process stops. [Ruppert's algorithm](/ruppert-algorithm/) and [Chew's second algorithm](/chew-second-algorithm/) are the two classic instances.

## In plain words

You have a triangle mesh with some thin triangles. Take a thin one and draw the circle through its three corners. Put a new point at the center of that circle and rebuild the mesh around it in the Delaunay way. The thin triangle disappears, and the new triangles near the point are fatter.

The center of the circle is a good spot because no existing point is inside the circle, so the new point is never close to an old one. Every new point has room around it, and the room cannot shrink forever, so you can only add a limited number of points before every triangle is fat.

Boundary lines need care: a new point must not land too close to a boundary line, so the line is cut in half first.

## When it applies

- **A planar or spatial domain** given as vertices and segments (a planar straight-line graph) or as polygons in space (a piecewise linear complex), to be meshed with triangles or tetrahedra.
- **A shape measure based on the circumcircle.** The technique controls the circumradius-to-shortest-edge ratio $\rho = R / \ell$ of each triangle. In the plane, $\rho = 1 / (2 \sin \theta_{\min})$, so it bounds the smallest angle.
- **Steiner points allowed.** The output has new vertices; if no new vertex is allowed, use the [constrained Delaunay triangulation](/constrained-delaunay-triangulation/) itself.
- **No small input angles,** for the guarantees. Two segments that meet at a sharp angle force small angles and can make the plain technique loop forever.

## The template

1. Build the Delaunay triangulation of the input vertices, or the constrained Delaunay triangulation of the input graph. Keep the list of **subsegments**, the pieces into which the input segments have been cut so far.
2. A subsegment is **encroached** if a vertex lies strictly inside its diametral circle (the circle with the subsegment as diameter). While some subsegment is encroached, split it at its midpoint, inserting the midpoint as a vertex.
3. A triangle is **bad** if $\rho > B$ for the chosen bound $B$, or if it is larger than a user size bound. Take a bad triangle and its circumcenter $c$.
4. If inserting $c$ would encroach some subsegments, do not insert $c$. Split those subsegments instead, and go back to step 2.
5. Otherwise insert $c$ with a Delaunay insertion step ([Bowyer-Watson](/bowyer-watson-algorithm/) or flips), and go back to step 2.
6. Stop when no subsegment is encroached and no triangle is bad. Remove the triangles outside the domain.

**Why it stops.** Give each new vertex $v$ an **insertion radius** $r_v$, the length of the shortest edge at $v$ right after its insertion. A circumcenter of a triangle with $\rho > B$ has $r_v = R > B \ell \ge B r_p$, where $p$ is the vertex that created the short edge. A midpoint $v$ of a subsegment that a rejected circumcenter $p$ encroaches has $r_v \ge r_p / \sqrt{2}$. A midpoint split because of an input vertex or a vertex on another segment has $r_v$ at least the local feature size, provided no two input segments meet at an angle less than $90°$. When $B \ge \sqrt{2}$, these inequalities chain together so that no insertion radius falls below a constant times the local feature size of the input. Every vertex then keeps an empty disk of fixed size around it, and only finitely many such disks fit in the domain.

**Exact arithmetic.** With rational input, every circumcenter and midpoint is rational, the in-circle test and the encroachment test $(a - p) \cdot (b - p) < 0$ are exact, and $\rho^2 > B^2$ is an exact comparison when $B^2$ is rational.

## Classic examples

- **[Ruppert's algorithm](/ruppert-algorithm/)** (1995). Delaunay triangulation, diametral circles, $B \ge \sqrt{2}$, so no angle below about $20.7°$, for inputs with no angle smaller than $90°$ (Shewchuk showed that $60°$ suffices); the mesh is nicely graded and size-optimal.
- **[Chew's second algorithm](/chew-second-algorithm/)** (1993). Constrained Delaunay triangulation; a circumcenter is rejected only if it is not visible from the bad triangle, and then the blocking subsegment is split and the free vertices in its diametral circle are deleted. Shewchuk proved termination for $B \ge \sqrt{5}/2$, about $26.57°$, for inputs with no angle smaller than $60°$; Chew's own version reaches $30°$ with off-center segment splits.
- **Ruppert-Chew hybrid with diametral lenses.** Encroachment is tested against a lens instead of a circle, between the two above in aggressiveness.
- **Shewchuk's Terminator** (2002). Handles small input angles by refusing to split segments near them, so that the bad triangles stay near the small angles and the algorithm always stops.
- **Tetrahedral refinement** (Shewchuk 1998). The same template in three dimensions with diametral spheres and a radius-edge bound of 2, for inputs without acute angles. Slivers survive and need other methods, such as sliver exudation by Cheng, Dey, Edelsbrunner, Facello and Teng.

## Variations

- **Off-centers.** Üngör inserts a point on the bisector of the shortest edge instead of at the circumcenter, which gives fewer vertices for the same bound.
- **Priority order.** Process the worst triangle first, or the largest one first. The guarantees hold for any order, but the output size changes.
- **Size functions.** Treat a triangle as bad also if its circumradius exceeds a given function $h(p)$ at its center, to grade the mesh to the user's needs.
- **Concentric shells.** Split a subsegment that touches a small input angle at a power of two distance from the apex, so that subsegments of two adjacent segments match and do not encroach on each other.
- **Constrained or conforming output.** Starting from a Delaunay triangulation and splitting until every segment is present gives a conforming Delaunay mesh; starting from a constrained one gives a constrained Delaunay mesh with fewer vertices.

## Pitfalls

- **Small input angles.** Two segments at $10°$ make each midpoint encroach on the other segment, and the splits never stop. Use concentric shells or the Terminator, or accept bad triangles near the small angle.
- **Bounds below the proven ones.** With $B < \sqrt{2}$ Ruppert's algorithm has no termination proof. It usually stops up to about $33°$, but not always.
- **Circumcenters outside the domain.** A bad triangle near the boundary can have its circumcenter outside. Ruppert's rule handles it: such a circumcenter always encroaches a boundary subsegment, which is split instead. Inserting the point anyway breaks the domain.
- **Rounding.** A circumcenter computed in floating point can land on the wrong side of a segment. Use exact or carefully rounded predicates, as Triangle does with adaptive arithmetic.
- **Holes.** Remove the triangles inside holes and outside the domain before refining, or the algorithm wastes points there and can be blocked by them.

## Exercises

1. Show that $\rho = R / \ell = 1 / (2 \sin \theta_{\min})$ for every triangle. Which value of $B$ gives a smallest angle of $30°$?
2. Show that in a Delaunay triangulation the circumcenter $c$ of a triangle $t$ has no vertex closer than the circumradius of $t$, and conclude that inserting $c$ creates no edge shorter than that radius.
3. Show that a point $p$ lies strictly inside the diametral circle of a segment $ab$ exactly when $(a - p) \cdot (b - p) < 0$, that is, when the angle $apb$ is obtuse.
4. Run the template by hand on the rectangle $(0,0)$, $(4,0)$, $(4,1)$, $(0,1)$ with $B = \sqrt{2}$, splitting midpoints first. How many vertices does the output have?
5. Draw two segments with a common end point at an angle of $15°$ and show that bisection on both makes the splits go on forever.

## References
