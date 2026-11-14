---
tag: NKFBHW
kind: technique
slug: boundary-recovery
name: Boundary recovery in 3D meshing
aliases:
- constraint recovery
- George-Hecht-Saltel boundary recovery
area: cad/mesh-generation-for-analysis
level: advanced
summary: Restores the boundary edges and faces missing from a Delaunay tetrahedralization by flips and Steiner points, so the mesh conforms to the domain.
prereqs: [constrained-delaunay-tetrahedralization, steiner-points, schonhardt-polyhedron]
see_also: [tetrahedral-delaunay-refinement, conforming-delaunay-triangulation, edge-flip, bowyer-watson-algorithm, delaunay-triangulation, sliver-tetrahedron, protecting-balls, topological-tetrahedral-mesh-improvement]
sources:
  - url: https://people.eecs.berkeley.edu/~jrs/papers/cdtbasic.pdf
    title: Jonathan Richard Shewchuk, Constrained Delaunay tetrahedralizations and provably good boundary recovery, Proceedings of the 11th International Meshing Roundtable, 2002, 193 to 204
    locator: Section 3 (edge protection and Theorem 1), Section 4 (testing edge protection), Section 5 (the two-step edge protection algorithm, the radius min of lfs, l/3 and 2d/3, Figure 11, Theorems 2 and 3, the remark that a polynomial bound on the number of vertices is unsolved), Section 6 (gift wrapping and sweep), Section 9 (symbolic perturbation)
  - paper: doi:10.1002/nme.3016
    title: Hang Si and Klaus Gärtner, 3D boundary recovery by constrained Delaunay tetrahedralization, International Journal for Numerical Methods in Engineering 85(11), 2011, 1341 to 1364
    locator: read as WIAS preprint 1530; the abstract, Section 1 (swap-based methods and their analysis), Theorem 5 (unique CDT once all segments are Delaunay edges), the segment recovery rules, Theorems 8 to 10 (facet recovery terminates, gives the CDT, expected time per facet), Section 7 (removing and relocating Steiner points), Tables I and II
  - url: https://wias-berlin.de/software/tetgen/1.5/doc/manual/manual.pdf
    title: Hang Si, TetGen, a quality tetrahedral mesh generator and a 3D Delaunay triangulator, User's Manual, version 1.6, WIAS Berlin, 2020
    locator: the description of the -p switch (constrained tetrahedralization by default, Steiner points only when flips and local operations fail), the -Y switch (no Steiner points on the boundary), the steps reported by -V, the reference of its CDT algorithm to Si and Gärtner, and the section on quality meshes (the radius-edge ratio does not remove slivers)
  - paper: doi:10.1016/0045-7825(91)90017-Z
    title: Paul-Louis George, Frédéric Hecht and Eric Saltel, Automatic mesh generator with specified boundary, Computer Methods in Applied Mechanics and Engineering 92(3), 1991, 269 to 288
    locator: boundary recovery in a Delaunay tetrahedralization by edge and face swaps with Steiner points where swaps fail (general locator, described through Si and Gärtner)
  - paper: doi:10.1002/nme.1620371203
    title: Nigel P. Weatherill and Oubay Hassan, Efficient three-dimensional Delaunay triangulation with automatic point creation and imposed boundary constraints, International Journal for Numerical Methods in Engineering 37(12), 1994, 2005 to 2039
    locator: boundary recovery by swaps and added points (general locator)
  - paper: doi:10.1002/nme.808
    title: Paul-Louis George, Houman Borouchaki and Eric Saltel, Ultimate robustness in meshing an arbitrary polyhedron, International Journal for Numerical Methods in Engineering 58(7), 2003, 1061 to 1089
    locator: recovery that always succeeds with Steiner points, and moving Steiner points off the boundary (general locator, described through Si and Gärtner)
  - paper: doi:10.1007/BF02187840
    title: Jim Ruppert and Raimund Seidel, On the difficulty of triangulating three-dimensional nonconvex polyhedra, Discrete and Computational Geometry 7(3), 1992, 227 to 253
    locator: the NP-completeness of deciding whether a polyhedron can be tetrahedralized without new vertices (general locator)
  - paper: doi:10.1137/0213031
    title: Bernard Chazelle, Convex partitions of polyhedra, a lower bound and worst-case optimal algorithm, SIAM Journal on Computing 13(3), 1984, 488 to 507
    locator: polyhedra with n vertices that need a quadratic number of convex pieces, and the quadratic upper bound (general locator)
  - paper: doi:10.1145/3618352
    title: Lorenzo Diazzi, Daniele Panozzo, Amir Vaxman and Marco Attene, Constrained Delaunay tetrahedrization, a robust and practical approach, ACM Transactions on Graphics 42(6), 2023
    locator: the robust CDT construction with indirect predicates and its test on the Thingi10k models (general locator)
  - paper: doi:10.1145/2629697
    title: Hang Si, TetGen, a Delaunay-based quality tetrahedral mesh generator, ACM Transactions on Mathematical Software 41(2), 2015
    locator: the design of TetGen, including boundary recovery by constrained Delaunay tetrahedralization (general locator)
---

Boundary recovery is the step of a Delaunay tetrahedral mesher that makes the mesh contain the boundary. A mesher first builds the [Delaunay tetrahedralization](/delaunay-triangulation/) of the boundary vertices, for example with the [Bowyer-Watson algorithm](/bowyer-watson-algorithm/). Some boundary edges and triangles are then missing, because the Delaunay tetrahedralization does not know about them. In the plane they can always be put back by [edge flips](/edge-flip/), with no new vertices. In space they cannot: [Schönhardt's polyhedron](/schonhardt-polyhedron/) has no tetrahedralization at all, and deciding whether a polyhedron has one is NP-complete. So every 3D method adds [Steiner points](/steiner-points/) somewhere. George, Hecht and Saltel's 1991 method, the classic one, swaps edges and faces and adds points when swaps get stuck; it works well and has no guarantee. Shewchuk's edge protection (2002) is a **proved bound**: it adds points only on the input segments, every new piece is at least a quarter of the local feature size long, and then the facets come back with no further points by the existence theorem for the [constrained Delaunay tetrahedralization](/constrained-delaunay-tetrahedralization/). TetGen uses the CDT approach of Si and Gärtner.

## In plain words

Imagine the boundary of a part as a set of corner points, edges and flat faces. Put all the corner points into a Delaunay mesh. Most boundary edges show up as mesh edges by themselves, but an edge that passes too close to another edge or a corner usually does not.

The fix is to break such an edge into shorter pieces. A short piece has a small sphere around it, and once the sphere is free of other points, the piece is guaranteed to be in the Delaunay mesh. Where two edges meet at a sharp angle, first cut both near the corner with a small sphere, so that halving never chases the corner forever. When every boundary edge piece is in the mesh in this strong sense, a theorem says the faces can be filled in with no more new points, using the constrained Delaunay tetrahedralization.

## When it applies

- The input is a piecewise linear complex (PLC) in 3D: vertices, segments and planar facets, for example a triangulated surface from CAD.
- The mesher is Delaunay based, so the volume is filled starting from the Delaunay tetrahedralization of the boundary vertices, as in [tetrahedral Delaunay refinement](/tetrahedral-delaunay-refinement/).
- The input may be in any position. Segments may pass close to each other and meet at small angles. Edge protection handles both, at the cost of more points.
- Steiner points on the boundary are acceptable, or they will be moved off it later. If the input surface must stay unchanged, see the TetGen `-Y` option under Variations.

## The template

The template below is the segment recovery step of Shewchuk's method, edge protection, as in the implementation. A subsegment is *strongly Delaunay* if some sphere through its two endpoints has every other vertex strictly outside; a strongly Delaunay segment is an edge of every Delaunay tetrahedralization. The local feature size $\mathrm{lfs}(u)$ of a point $u$ is the radius of the smallest ball around $u$ that meets two input vertices or segments that do not touch each other. For an input vertex $v$ it is the distance from $v$ to the nearest other vertex or segment not containing $v$. Facets are ignored.

```pseudo id=main
EDGE-PROTECT(vertices, segments)
L1  for each vertex v where two segments meet at less than 90 degrees: mark both segments clipped at v
L2  for each such v: r_v ← min(lfs(v), ℓ_v/3, 2 d_v/3)
L3  for each segment e clipped at v: insert the point where the sphere S(v, r_v) cuts e
L4  test every subsegment for being strongly Delaunay
L5  while some subsegment s is not strongly Delaunay
L6      insert the midpoint of s and retest the subsegments whose empty sphere contains it
L7  return the vertices and the subsegments
```

Here $\ell_v$ is the length of the shortest segment clipped at $v$, and $d_v$ is the length of the shortest segment at $v$ whose other end is clipped ($d_v = \infty$ if there is none). The pieces from $v$ to the points of line L3 are the *ends*. After EDGE-PROTECT, the second step builds the CDT of the augmented PLC, by gift wrapping, by a sweep, or by inserting the facets one at a time.

**Claim 1 (proved here: the ends).** Every end at $v$ has length at least $\mathrm{lfs}(v)/3$, so $|e| \ge \mathrm{lfs}(u)/4$ for every point $u$ of it. Every end is strongly Delaunay after line L3 and stays so until line L7, so line L6 never splits an end. The middle piece of a segment $t$ clipped at both ends has length at least $|t|/3 \ge \mathrm{lfs}(u)/3$ for every $u$ in it.

*Proof.* Each candidate in line L2 is at least $\mathrm{lfs}(v)/3$: segment lengths at $v$ are at least $\mathrm{lfs}(v)$, because the far endpoint is another vertex. So the end has length $r_v \ge \mathrm{lfs}(v)/3$. The function $\mathrm{lfs}$ is 1-Lipschitz, so for $u$ in the end, $\mathrm{lfs}(u) \le \mathrm{lfs}(v) + |e| \le 4|e|$.

Let the end run from $v$ to $x$, with $|vx| = r_v$. Every point of its closed diametral ball other than $x$ is at distance less than $r_v$ from $v$. Input vertices and points on segments not containing $v$ are at distance at least $\mathrm{lfs}(v) \ge r_v$ from $v$, so they are not in the ball. A segment $g$ at $v$ at an angle of 90 degrees or more stays outside it: for $y$ on $g$ and the center $m$ of the ball, $|y - m|^2 = |y - v|^2 + |m - v|^2 - 2 (y - v) \cdot (m - v) > |m - v|^2$. A segment $g$ at $v$ at a smaller angle is clipped at $v$, its own end lies on $S(v, r_v)$ or beyond, and its point at the far end is at distance $|g| - r_w \ge |g| - |g|/3 \ge r_v$ from $v$, since $r_w \le \ell_w/3 \le |g|/3$ and $r_v \le 2 d_v/3 \le 2|g|/3$. The only points of other segments that come closer than $r_v$ to $v$ are on the ends at $v$, and line L6 inserts points only on pieces that are not ends. So no vertex but $v$ and $x$ is ever inside or on the diametral sphere, and the end stays strongly Delaunay.

For the middle piece, line L2 gives $r \le \ell/3 \le |t|/3$ at each end, so it keeps at least $|t|/3$. A ball of radius $|t|$ around any $u$ on $t$ contains both endpoints of $t$, two distinct vertices, so $\mathrm{lfs}(u) \le |t|$. $\square$

**Claim 2 (cited: Shewchuk's Theorem 2, a proved bound).** EDGE-PROTECT "creates no segment shorter than one-quarter the local feature size of any point in that segment." For the pieces of line L6 Shewchuk shows $|s| \ge \mathrm{lfs}(u)/2$: a piece $s$ is created only when the piece of length $2|s|$ has a vertex off its own segment on or inside its diametral sphere. His Theorem 3 extends the bound to every edge of the final CDT: $|e| \ge \mathrm{lfs}(u) \sin(\varphi/2)/2$ when the ends of $e$ lie on two segments that meet at an angle $\varphi < 60$ degrees, and $|e| \ge \mathrm{lfs}(u)/4$ otherwise.

**Claim 3 (proved here, given Claim 2: termination and correctness).** EDGE-PROTECT stops, and its output is edge-protected, so the augmented PLC, with each facet carrying the new points on its boundary, has a CDT that contains every facet with no further Steiner points.

*Proof.* By Claim 2 every piece is at least $\frac14 \min \mathrm{lfs}$ long, and $\min \mathrm{lfs} > 0$ over a finite PLC. The segments have finite length, so only finitely many midpoints fit. When the loop of line L5 ends, every subsegment is strongly Delaunay, which is the definition of edge-protected. Shewchuk's CDT Theorem, an existence theorem, gives the CDT. $\square$

The proved bound is a lower bound on edge lengths, not a bound on the number of points. No bound polynomial in the input size is known; Shewchuk writes that the problem "is unsolved". Point counts depend on how close the segments come. In the tests, a segment passing between two others at gaps of 8, 4, 2 and 1 gets 2, 3, 4 and 5 midpoints, one more each time the gap halves.

**No guarantee without Steiner points.** No method can recover every boundary without new points, because some polyhedra have no tetrahedralization, and Ruppert and Seidel proved that deciding whether one exists is NP-complete. When new points are allowed, they may still be many: Chazelle's polyhedra with $n$ vertices need a quadratic number of convex pieces, hence $\Omega(n^2)$ tetrahedra, and Si and Gärtner note that $O(n^2)$ tetrahedra suffice for any simple polyhedron.

**What is proved, and of which kind.**

- George, Hecht and Saltel (1991), and Weatherill and Hassan (1994): methods with no guarantee. Missing edges and faces are recovered by swaps, and points are added where swaps fail. Si and Gärtner write that such methods "rely on ad hoc techniques" and that "their complexities are hard to analyze".
- George, Borouchaki and Saltel (2003): a method designed to always succeed, by adding points; they also show that a Steiner point on a boundary edge or face can be moved off it into the interior. Not all can be deleted, as Schönhardt's polyhedron shows.
- Shewchuk (2002): edge protection with the proved bounds of Claim 2, and the CDT Theorem, an existence theorem, for the facets.
- Si and Gärtner (2011): Steiner points "on segments only", chosen by rules that avoid needlessly short pieces, so that "it is theoretically guaranteed that the facets can be recovered without using Steiner points". Their Theorem 5: if all segments are Delaunay edges of vertices in general position, the PLC has a unique CDT. Theorems 8 and 9: their facet recovery terminates and returns that CDT. Theorem 10: one missing facet is recovered in expected time $O(v^2 + v \log v)$ for $v$ vertices; they give an $\Omega(f v^2)$ example, and the worst case is open.

**What TetGen does.** TetGen 1.6 follows Si and Gärtner ("TetGen's CDT algorithm is from Si and Gärtner"). Its verbose log names the steps: Delaunizing vertices, Creating surface mesh, Recovering boundaries, Removing exterior tetrahedra, Suppressing Steiner points, Recovering Delaunayness, Optimizing mesh. Its manual says that by default "TetGen generates a constrained tetrahedralization of the PLC", that "It only adds Steiner points when flips and advanced local mesh modifications cannot recover an edge or a facet", and that then "Steiner points might be added directly on the input edges or facets". With the `-Y` switch the input boundary is kept and Steiner points "appear only in the interior space of the PLC".

**Proved constants and measured ones.** The proved constant $\frac14$ is much worse than what happens. In the tests, the smallest ratio of piece length to $\mathrm{lfs}$ was between 0.315 and 0.413 on each of 10 random segment sets, 0.42 on Schönhardt's polyhedron and 0.663 on the worked example below. On six models with 460 to 57270 input vertices, Si and Gärtner report that "the number of Steiner points is in the order of the input size. This is a typical case." Their total running times were 0.26 to 7.85 seconds. Most of those points were later removed: on the Heart model, 3605 of 3622 Steiner points were deleted and the other 17 moved off the boundary.

## Classic examples

**A segment between two others.** Take $O = (0,0,0)$, $A = (20,0,0)$, $B = (16,12,0)$ with segments $OA$ and $OB$, and two short segments $CD$ from $(10,-3,1)$ to $(10,3,1)$ and $EF$ from $(10,-3,-1)$ to $(10,3,-1)$. $OA$ passes between them at distance 1 from each. $OB$, $CD$ and $EF$ are strongly Delaunay and $OA$ is not.

| Step | What happens | New points |
|---|---|---|
| L1 | $OA$ and $OB$ meet at $O$ at $36.9$ degrees, so both are clipped at $O$ | |
| L2 | $\mathrm{lfs}(O) = \sqrt{101} \approx 10.05$, the distance to $CD$; $\ell_O / 3 = 20/3$; $d_O = \infty$; so $r_O = 20/3$ | |
| L3 | the sphere $S(O, 20/3)$ cuts $OA$ and $OB$ | $(\frac{20}{3}, 0, 0)$, $(\frac{16}{3}, 4, 0)$ |
| L4, L5 | the piece from $\frac{20}{3}$ to $20$ on $OA$ is not strongly Delaunay | |
| L6 | split it at $\frac{40}{3}$; the piece from $\frac{20}{3}$ to $\frac{40}{3}$ still is not; split it at $10$ | $(\frac{40}{3}, 0, 0)$, $(10, 0, 0)$ |

The result has 4 Steiner points, and every piece is strongly Delaunay. The shortest piece compared with the local feature size is the end at $O$, with ratio $\frac{20/3}{\sqrt{101}} = 0.663$, against the proved $0.25$. The tests check every number in this table in exact arithmetic.

**Schönhardt's polyhedron.** Take the twisted prism of the implementation, with its 12 edges as segments. Every vertex has segments meeting at less than 90 degrees, so line L3 clips all 12 segments at both ends: 24 points, with radii of about 37.5. Line L6 then splits the middle piece of each of the three reflex edges once: 3 more points. Now every segment is strongly Delaunay, and by the CDT Theorem the polyhedron with its 8 subdivided facets has a CDT. Without new points it has no tetrahedralization at all.

**Flips first.** Most meshers try flips before adding points. A missing edge often crosses only a few triangles, and 2-3 and 3-2 flips remove the crossings. Liu and Baida (2000) studied how far flips alone can go. Flips are what TetGen tries first, and Schönhardt's polyhedron is the standard example where they fail.

## Variations

- **Si and Gärtner's split points.** Instead of midpoints, the split point on a missing segment is chosen with a reference point that encroaches on it and a parameter $c$, and acute vertices (angles below 60 degrees) get special rules. On their comparison example this adds 8 Steiner points where Shewchuk's algorithm adds 24.
- **Weak edge protection.** Only grazeable segments need to be strongly Delaunay for a CDT to exist, so they alone need splitting. The incremental facet insertion algorithm needs full edge protection.
- **Moving Steiner points off the boundary.** TetGen's `-Y` switch keeps boundary Steiner points off the input boundary. George, Borouchaki and Saltel showed that such points can be moved into the interior. On Si and Gärtner's four test models, "The majority of the Steiner points can be completely deleted from the mesh, only few of them have been relocated to the interior of the domain."
- **Robust CDT.** Diazzi, Panozzo, Vaxman and Attene (2023) build the CDT with exact indirect predicates, close a gap in the theory behind TetGen's facet recovery, and report success on all 4408 Thingi10k models they tried.
- **Conforming Delaunay.** A [conforming Delaunay triangulation](/conforming-delaunay-triangulation/) adds points until an ordinary Delaunay tetrahedralization contains the facets too. It needs more points, many on the facets.

## Pitfalls

- Recovery does not make good tetrahedra. The CDT may contain flat ones, and the refinement that usually follows bounds only the radius-edge ratio, which does not remove slivers, the flat [sliver tetrahedra](/sliver-tetrahedron/) with all four vertices near a circle. TetGen's manual says the same and adds the minimum dihedral angle as a second measure.
- The strongly Delaunay test is degenerate when five vertices are cospherical. Shewchuk recommends symbolic perturbation; the implementation decides the strict sphere condition exactly over rationals.
- The point where a sphere cuts a segment has a square root. The implementation rounds the distance down to a multiple of $2^{-50}$ of the segment length, which keeps the point exact and the radius at most $r_v$, and loosens the lower bound of Claim 1 by a factor of $1 - 2^{-50}$ at most.
- Steiner points on the boundary change the input. Downstream codes that match boundary faces to CAD faces must expect split triangles, or remove the points afterwards.
- Point counts grow when segments come close. In the tests, every halving of the gap between two segments adds one midpoint, and two long parallel segments close together would need very many tetrahedra for good shape in any case.
- Swap-based recovery can cycle or get stuck without a fallback. A robust code needs a rule for adding points that always works.

## Exercises

1. Show that a strongly Delaunay segment is an edge of every Delaunay tetrahedralization of the vertices.
2. In the worked example, move $CD$ and $EF$ to $z = \pm 2$. How many midpoints does line L6 insert now?
3. Show that a point $y$ on a segment at $v$ lies inside the diametral ball of a piece $[v, x]$ of another segment exactly when $|vy| < |vx| \cos \theta$, where $\theta$ is the angle at $v$. Why does line L1 clip only below 90 degrees?
4. Prove that the three reflex edges of Schönhardt's polyhedron cannot all be strongly Delaunay, using the CDT Theorem.
5. Run EDGE-PROTECT on a cube with its 12 edges and 6 face diagonals as segments. Which segments get Steiner points?

## References
