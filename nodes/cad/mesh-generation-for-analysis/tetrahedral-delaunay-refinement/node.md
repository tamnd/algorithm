---
tag: VNAEW7
kind: algorithm
slug: tetrahedral-delaunay-refinement
name: Shewchuk's tetrahedral Delaunay refinement
aliases:
- 3D Delaunay refinement
area: cad/mesh-generation-for-analysis
level: advanced
summary: Refines a Delaunay tetrahedral mesh of a polyhedral domain by inserting circumcenters of bad tetrahedra and splitting encroached faces, bounding the radius-edge ratio.
solves: [mesh-generation]
model: real-ram
complexity:
  vars: {n: the number of output vertices}
  time: {worst: O(n^2)}
  space: {extra: O(n^2)}
properties: {deterministic: true, recursive: false, exact: true}
history:
  year: 1998
  people: [Jonathan Richard Shewchuk]
  note: Shewchuk extended Ruppert's planar analysis to tetrahedra in his 1997 thesis and his 1998 SoCG paper, proving termination with radius-edge ratio at most 2 for polyhedral inputs whose angles are at least 90 degrees.
prereqs: [delaunay-refinement, ruppert-algorithm, bowyer-watson-algorithm, radius-edge-ratio]
see_also: [sliver-exudation, sliver-tetrahedron, constrained-delaunay-tetrahedralization, boundary-recovery, delaunay-surface-meshing, protecting-balls, isosurface-stuffing, mesh-sizing-function]
sources:
  - paper: doi:10.1145/276884.276894
    title: Jonathan Richard Shewchuk, Tetrahedral mesh generation by Delaunay refinement, Proceedings of the 14th Annual Symposium on Computational Geometry, 1998, 86 to 95
    locator: Section 4 (the algorithm, encroachment and its priorities), Section 5 (the projection condition), Lemma 3 and Figure 12 (insertion radii and the dataflow graph), Theorems 5 and 6 (grading constants), Section 8 (slivers and the measured results of Figure 13)
  - book: isbn:9781584887300
    title: Siu-Wing Cheng, Tamal K. Dey and Jonathan Richard Shewchuk, Delaunay Mesh Generation, CRC Press, 2013
    locator: Chapter 8, Tetrahedral meshing of PLCs (pages 185 to 204), the full termination and grading proofs; Chapter 9 for PLCs with small angles
  - paper: doi:10.1006/jagm.1995.1021
    title: Jim Ruppert, A Delaunay refinement algorithm for quality 2-dimensional mesh generation, Journal of Algorithms 18(3), 1995, 548 to 585
    locator: the local feature size and the insertion radius argument in the plane (general locator)
  - paper: doi:10.1142/S0218195992000068
    title: Tamal K. Dey, Chanderjit L. Bajaj and Kokichi Sugihara, On good triangulations in three dimensions, International Journal of Computational Geometry and Applications 2(1), 1992, 75 to 95
    locator: uniform Delaunay refinement of point sets in three dimensions (general locator)
  - paper: doi:10.1145/262839.263018
    title: L. Paul Chew, Guaranteed-quality Delaunay meshing in 3D (short version), Proceedings of the 13th Annual Symposium on Computational Geometry, 1997, 391 to 393
    locator: uniform 3D Delaunay refinement with sliver removal by random choice of the new vertex (general locator)
---

Shewchuk's tetrahedral Delaunay refinement builds a [tetrahedral mesh](/tetrahedralization/) of a polyhedral domain by keeping a Delaunay tetrahedralization and adding vertices to it. It splits boundary edges and boundary faces that are too close to other vertices, and it inserts the circumcenter of every tetrahedron whose [radius-edge ratio](/radius-edge-ratio/) exceeds a bound $B$. Shewchuk (1998) proved that it stops, with every ratio at most $B$, for every $B \ge 2$ on inputs whose angles between incident edges and faces are at least $90°$, and that the mesh is graded when $B > 2$. It is the three-dimensional form of [Ruppert's algorithm](/ruppert-algorithm/), and mesh generators such as TetGen use refinement of this kind. A ratio bound does not exclude [slivers](/sliver-tetrahedron/), so the output may still contain nearly flat tetrahedra.

## In plain words

Start with the Delaunay tetrahedralization of the corners of the domain. Then repeat three rules, in order of priority. If a boundary edge has a vertex inside or on the sphere that has the edge as a diameter, add the edge's midpoint. If a boundary triangle has a vertex inside or on its smallest sphere, add the triangle's circumcenter, unless that point would crowd a boundary edge; then split the edge instead. If a tetrahedron has a large circumsphere compared with its shortest edge, add the center of that sphere, unless it would crowd the boundary. Each new vertex lands in empty space, far from the others, so the edges cannot get shorter without limit, and the loop stops. Slivers can pass every one of these tests.

## The problem

The input is a piecewise linear complex (PLC) $X$: a set of vertices, segments and polygonal facets in $\mathbb{R}^3$, closed under intersection, that bounds the domain. The output is a Delaunay tetrahedralization of a point set that contains the vertices of $X$, that *conforms* to $X$ (each segment is a union of mesh edges, the *subsegments*, and each facet a union of mesh triangles, the *subfacets*), and in which every tetrahedron has circumradius $R$ and shortest edge $\ell$ with $R / \ell \le B$.

The *local feature size* $\mathrm{lfs}(p)$ of a point $p$ is the radius of the smallest ball centered at $p$ that meets two features of $X$ (vertices, segments or facets) that do not intersect each other. It is $1$-Lipschitz and positive on the domain; the [mesh sizing function](/mesh-sizing-function/) page uses it as a target size. The *insertion radius* $r_v$ of a vertex $v$ is the distance from $v$ to the nearest other vertex at the moment $v$ is inserted, which is the length of the shortest edge at $v$ just after a Delaunay insertion.

This page makes three kinds of claim.

- *Proved bound, cited.* If no two incident segments or facets meet at an angle below $90°$ (Shewchuk's *projection condition*: the orthogonal projection of one of two intersecting constraints onto the other does not meet the interior of the other), then for every $B \ge 2$ the algorithm stops, and every tetrahedron has radius-edge ratio at most $B$. For $B > 2$, Theorems 5 and 6 bound every insertion radius from below by $\mathrm{lfs}$ divided by $D_T = \frac{B + 1 + \sqrt2}{B - 2}$ for a tetrahedron circumcenter, $D_F = \frac{(1 + \sqrt2) B + \sqrt2}{B - 2}$ for a subfacet circumcenter and $D_S = \frac{(3 + \sqrt2) B}{B - 2}$ for a subsegment midpoint, and every vertex is at distance at least $\mathrm{lfs}(v) / (D_S + 1)$ from its nearest neighbor. For $B = 2.5$ these are $D_T \approx 9.83$, $D_F \approx 14.90$ and $D_S \approx 22.07$, so the spacing can be about 23 times below the local feature size.
- *Proved here.* For $B = 2$, a sketch of termination by insertion radius, with every edge at least $\mathrm{lfs}_{\min}/2$ long, where $\mathrm{lfs}_{\min}$ is the smallest local feature size in the domain. See `proofs/correctness.md`. It rests on Shewchuk's Lemma 3, which is cited.
- *Measured, no guarantee.* The constants are far worse than what happens. In the example below the shortest edge is $0.56$ against a proved $0.125$. On the example of Shewchuk's Figure 13 the spacing with $B = 2.5$ is 9 times below the local feature size, not 23, and the program terminates down to $B = 1.05$, where no proof applies, though it fails to terminate at $B = 1.04$. Inputs with angles below $90°$ also usually work in practice.

A radius-edge bound does not remove slivers. A sliver has four vertices near a great circle of its circumsphere, so its radius-edge ratio can be as small as $1/\sqrt2 \approx 0.71$ while its dihedral angles approach $0°$ and $180°$. Every rule above is blind to it. Shewchuk's Section 8 says the only proved guarantee for sliver removal at that time, Chew's, was too weak to give any practical assurance, and that there was no guarantee that slivers can be removed. [Sliver exudation](/sliver-exudation/) proves a dihedral angle bound, with a tiny constant.

## The algorithm

A vertex *encroaches* a subsegment if it lies inside or on its diametral sphere, the smallest sphere through its two ends. A vertex off the plane of a subfacet encroaches it if it lies inside or on its equatorial sphere, the smallest sphere through its three corners. A tetrahedron is *skinny* if $R / \ell > B$.

```pseudo id=main
DELAUNAY-REFINE(X, B)
L1  T ← the Delaunay tetrahedralization of the vertices of X; queue every skinny tetrahedron
L2  repeat while one of the rules below applies, in this order:
L3      if some subsegment s is encroached: insert the midpoint of s
L4      else if some subfacet f is encroached:
L5          c ← the circumcenter of f
L6          if c encroaches a subsegment s: reject c and split s as in L3
L7          else insert c
L8      else if some tetrahedron t is skinny:
L9          c ← the circumcenter of t
L10         if c encroaches a subsegment or subfacet: reject c, keep t queued, and split that feature as in L3 or L4 to L7
L11         else insert c
L12 return T
L13 insert v: remove every tetrahedron whose circumsphere has v strictly inside, and join v to each face of the hole (Bowyer-Watson)
```

Insertion (L13) is the [Bowyer-Watson algorithm](/bowyer-watson-algorithm/), so the mesh stays Delaunay. Inserting a vertex on a subsegment or subfacet replaces it by two subsegments or three or more subfacets. A rejected circumcenter is never inserted. When it encroaches several subfacets, Shewchuk's analysis splits one that contains its orthogonal projection, and the implementation does the same.

The implementation takes a box $[0, a] \times [0, b] \times [0, c]$ with integer sides, its 8 corners, 12 edges and 6 faces, plus optional input vertices strictly inside. All input angles are $90°$, so the projection condition holds. The domain is convex, so the subfacets are the faces of the mesh on the box, and an empty equatorial sphere makes them a Delaunay triangulation of each facet. Coordinates are integers in units of $2^{-20}$. Each midpoint or circumcenter is computed exactly and rounded once to this grid, and every test (orientation, insphere, encroachment, ratio) is exact integer or rational arithmetic. Rounding keeps a point on its box edge or face, since those coordinates are integers already. The implementation keeps a set of features found encroached and tests each new vertex against every feature and each new feature against every vertex, which makes each step $O(n)$.

## Example

Take the box $[0, 4] \times [0, 3] \times [0, 2]$ with two input vertices inside, at $(1, 1, \frac12)$ and $(\frac52, 2, 1)$, and $B = 2$. The steps come from the implementation, and the test file checks the totals.

| Steps | Rule | What happens |
|---|---|---|
| start | L1 | 10 vertices and 18 tetrahedra; 4 box edges and 12 box triangles are encroached by the inner vertices |
| 1 to 5 | L3 | 5 box edges split at their midpoints, such as $(0, \frac32, 0)$ |
| 6 to 14 | L4 to L6 | 9 subfacet circumcenters rejected, because each encroaches a subsegment; that subsegment is split instead |
| 15 to 21 | L7 | 7 subfacet circumcenters inserted, such as $(\frac{25}{16}, \frac32, 0)$ with insertion radius $0.90$ |
| 22, 23 | L4 to L6 | 2 more rejections and subsegment splits |
| end | L12 | 33 vertices (10 input, 16 on edges, 7 on faces) and 66 tetrahedra; no skinny tetrahedron was left to split |

The largest radius-edge ratio is $1.98$. The shortest edge is $0.5599$. Here the nearest pair of non-intersecting features is the vertex $(1, 1, \frac12)$ and the face $z = 0$, at distance $\frac12$, so $\mathrm{lfs}_{\min} \ge \frac14$ and the proof guarantees edges of at least $\frac18$: the measured spacing is 4.5 times better. The dihedral angles range from $6.32°$ to $166.55°$. The worst tetrahedron, with vertices $(1, 1, \frac12)$, $(\frac52, 2, 1)$, $(\frac{25}{16}, \frac32, 0)$ and $(\frac{25}{16}, \frac32, 2)$, has radius-edge ratio $1.15$ and dihedral angles $6.3°$ and $166.5°$: a sliver that passes the test. With $B = 6/5$, below the proved threshold, the same input stops at 63 vertices and 167 tetrahedra, with 4 tetrahedron circumcenters inserted, ratio at most $1.2$, and still a $4.98°$ dihedral angle.

## Correctness

*The output is what it should be when the loop stops.* Bowyer-Watson insertion keeps the tetrahedralization Delaunay. When L2 finds nothing to do, no subsegment is encroached, so each one has an empty diametral sphere and is an edge of the Delaunay tetrahedralization; likewise each subfacet has an empty equatorial sphere and is a Delaunay face. So the mesh conforms to $X$, and no tetrahedron is skinny. A circumcenter that lies outside the domain is separated from its tetrahedron by a subfacet, and it encroaches that subfacet (Chapter 8 of Cheng, Dey and Shewchuk), so a circumcenter that passes L10 lies in the domain. The implementation also checks that every inserted point lies in the box.

*The loop stops.* This is where $B \ge 2$ and the $90°$ condition enter. Shewchuk's Lemma 3 says that each new vertex $v$ either has $r_v \ge \mathrm{lfs}(v)$ or has a parent $p$, the vertex that caused it to be inserted, with $r_v \ge C\, r_p$, where $C = B$ if $v$ is a tetrahedron circumcenter and $C = 1/\sqrt2$ if $v$ is a subsegment midpoint or subfacet circumcenter. In the dataflow graph of Figure 12 the cycles are tetrahedron to tetrahedron (factor $B$), through a subfacet or a subsegment (factor $B/\sqrt2$), and through a subfacet and then a subsegment (factor $B/2$). With $B \ge 2$ no cycle shrinks the radius, so by induction every tetrahedron circumcenter has $r_v \ge \mathrm{lfs}_{\min}$, every subfacet circumcenter $r_v \ge \mathrm{lfs}_{\min}/\sqrt2$ and every midpoint $r_v \ge \mathrm{lfs}_{\min}/2$. Every edge is then at least $\mathrm{lfs}_{\min}/2$, so disjoint balls of radius $\mathrm{lfs}_{\min}/4$ fit around the vertices, and a bounded domain holds only finitely many. The sketch is in `proofs/correctness.md`; the full proof, with the case analysis of Lemma 3 and the grading bound, is in Shewchuk (1998) and in Chapter 8 of Cheng, Dey and Shewchuk.

*Why slivers survive.* The analysis only bounds $R/\ell$. A sliver has $R/\ell$ near $1/\sqrt2$, so it is never skinny, and none of the rules ever looks at it. The insertion radius argument needs the new vertex to be far from all others, which a circumcenter is; the circumcenter of a sliver is also far from all others, but nothing asks for it.

The test file checks, on 8 inputs, that every tetrahedron has an empty circumsphere by the exact insphere test against all vertices, that every ratio is at most $B$ (compared exactly as squares), that the volumes are positive and add up to the box, that faces match in pairs with the unmatched ones on the box, that the subsegments are mesh edges and cover the 12 box edges, that nothing is encroached at the end, and, for $B = 2$, that every insertion radius and every edge is at least the proved $\mathrm{lfs}_{\min}/2$.

## Complexity

Shewchuk reports that with good point location each insertion takes constant time in practice. In the worst case a Delaunay tetrahedralization of $n$ points has $\Theta(n^2)$ tetrahedra, so an insertion can take $O(n)$ time and the whole refinement $O(n^2)$; the space is $O(n^2)$ in the worst case and $O(n)$ for a mesh of bounded ratio, whose vertices have bounded degree by a result of Miller, Talmor, Teng and Walkington. The grading bound of Theorem 6 and a packing argument give $n = O\left(\int_\Omega \mathrm{lfs}(x)^{-3}\, dx\right)$ for $B > 2$. The implementation is simpler: it tests each new vertex against every subsegment and subfacet and finds a tetrahedron in conflict by a scan when it has none, so each step costs $O(n)$ and a run $O(n^2)$, enough for the few hundred vertices of the tests.

## Properties

- **Proved quality.** Radius-edge ratio at most $B$ for every $B \ge 2$, under the $90°$ input angle condition.
- **Proved grading for $B > 2$.** Edges at least $\mathrm{lfs}(v)/(D_S + 1)$ long, with the constants above.
- **No dihedral angle bound.** Slivers can remain.
- **Conforming, with Steiner points.** Segments and facets appear as unions of mesh edges and triangles; extra vertices are added on them.
- **Exact here.** All predicates are exact; the only rounding is of new vertices to the grid.
- **Deterministic.** The order of the queues fixes the output.

## Variants and improvements

- **Small input angles.** Shewchuk's thesis and Chapter 9 of Cheng, Dey and Shewchuk handle inputs with angles below $90°$ by protecting the region near sharp edges, at the cost of leaving some skinny tetrahedra near them. [Protecting balls](/protecting-balls/) do this with weighted vertices.
- **Constrained Delaunay version.** TetGen refines a [constrained Delaunay tetrahedralization](/constrained-delaunay-tetrahedralization/) instead of a conforming one, which needs fewer Steiner points on the boundary; the input faces are first recovered by [boundary recovery](/boundary-recovery/).
- **Sliver removal.** [Sliver exudation](/sliver-exudation/) assigns weights to the vertices and proves a dihedral angle bound; Chew's 1997 method inserts a random point near the circumcenter of a sliver instead of the circumcenter itself.
- **Other insertion points.** Inserting a point on the segment from the middle of the shortest edge to the circumcenter, instead of the circumcenter, gives fewer vertices in practice.
- **Smooth boundaries.** [Delaunay surface meshing](/delaunay-surface-meshing/) refines a restricted Delaunay triangulation of a curved surface first, then this algorithm fills the volume.
- **Lattice methods.** [Isosurface stuffing](/isosurface-stuffing/) proves dihedral angle bounds of about $10.78°$ but cannot keep sharp features.

## When to use it

Use it when the domain is a polyhedron given as a PLC, the mesh must contain its segments and facets, and the sizes should grade from small near small features to large in the interior. Follow it by sliver removal or mesh improvement, such as [topological mesh improvement](/topological-tetrahedral-mesh-improvement/) or [optimization-based smoothing](/optimization-based-mesh-smoothing/), when the solver needs good dihedral angles. Do not use the plain algorithm with $B < 2$ and expect a guarantee: it often works but nothing proves it.

## Pitfalls

- **Taking the ratio bound for a quality guarantee.** Slivers have small radius-edge ratios; check the dihedral angles too.
- **Small input angles.** With incident faces at angles below $90°$, splitting one feature can encroach the other forever. Either protect the sharp regions or accept skinny tetrahedra near them.
- **Wrong priorities.** Inserting a tetrahedron circumcenter that encroaches the boundary puts a vertex too close to it; the proof needs it rejected and the feature split instead.
- **Inexact predicates.** An insphere test with floating point can make the cavity of Bowyer-Watson not star-shaped and the mesh invalid. Use exact or adaptive predicates.
- **Circumcenters outside the domain.** Without the encroachment rules, a circumcenter may lie outside a nonconvex domain.
- **$B$ too small.** Shewchuk's example stops at $B = 1.05$ and runs forever at $B = 1.04$; set a vertex limit, as the implementation does.

## Implementations

## History

Chew gave the first provably good Delaunay refinement algorithm in the plane in 1989, and Ruppert (1995) proved a graded and size-optimal planar version. Dey, Bajaj and Sugihara (1992) and Chew (1997) generalized Delaunay refinement to three dimensions for point sets, with uniform meshes. Shewchuk, in his 1997 thesis and his 1998 paper, extended Ruppert's insertion radius analysis to tetrahedra and to PLC inputs, with the radius-edge bound of 2, graded meshes for $B > 2$, and the condition that input angles be at least $90°$. Cheng, Dey, Edelsbrunner, Facello and Teng then proved that sliver exudation removes slivers, and later work relaxed the angle condition. Si's TetGen refines a constrained Delaunay tetrahedralization in the same way.

## References
