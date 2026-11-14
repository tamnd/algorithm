---
tag: EADV10
kind: technique
slug: protecting-balls
name: Protecting balls for sharp features
aliases:
- weighted protecting balls
area: cad/mesh-generation-for-analysis
level: research
summary: Cheng, Dey and Ramos's weighted points around sharp edges and corners, so Delaunay refinement of piecewise smooth complexes terminates with the right topology.
prereqs: [delaunay-surface-meshing, regular-triangulation, power-diagram]
see_also: [restricted-delaunay-triangulation, tetrahedral-delaunay-refinement, delaunay-refinement, ruppert-algorithm, sliver-exudation, mesh-sizing-function, chew-second-algorithm, medial-axis]
sources:
  - paper: doi:10.1007/s00454-008-9109-3
    title: Siu-Wing Cheng, Tamal K. Dey and Edgar A. Ramos, Delaunay refinement for piecewise smooth complexes, Discrete and Computational Geometry 43(1), 2010, 121 to 166 (conference version in SODA 2007)
    locator: protection of the vertices and curves by balls that become weighted points, the refinement by four kinds of violations, termination and the homeomorphism for a small enough sample (general locator)
  - paper: doi:10.1007/978-3-540-75103-8_27
    title: Siu-Wing Cheng, Tamal K. Dey and Joshua A. Levine, A practical Delaunay meshing algorithm for a large class of domains, Proceedings of the 16th International Meshing Roundtable, 2007, 477 to 494
    locator: Section 3 (the protection properties with omega at most 0.076 and R at most 8 radii, weighted points, admissible point sets, Lemma 1), Section 4.1 (algorithm DelPSC), Section 4.2 (the radius omega/8 times min of d_x and d'_x, the march with steps of 5/6 of a radius, the two last balls of equal radius), Section 5 (Lemma 3, Theorem 1, properties T1 to T3, Theorem 2), Section 6 (Table 1, rho_0 = 1.4 and lambda at 10 percent of the bounding box)
  - paper: doi:10.1007/3-540-29090-7_20
    title: Siu-Wing Cheng, Tamal K. Dey and Tathagata Ray, Weighted Delaunay refinement for polyhedra with small angles, Proceedings of the 14th International Meshing Roundtable, 2005, 325 to 342
    locator: protecting balls turned into weighted points for polyhedral input with small angles (general locator)
  - paper: doi:10.1142/S0218195905001774
    title: Siu-Wing Cheng, Tamal K. Dey, Edgar A. Ramos and Tathagata Ray, Quality meshing of polyhedra with small angles, International Journal of Computational Geometry and Applications 15(4), 2005, 421 to 461
    locator: protection of small input angles by balls in Delaunay refinement of polyhedra (general locator)
  - book: isbn:9781584887300
    title: Siu-Wing Cheng, Tamal K. Dey and Jonathan Richard Shewchuk, Delaunay Mesh Generation, CRC Press, 2013
    locator: Chapter 15, Meshing piecewise smooth complexes, pages 349 to 384 (general locator)
  - paper: doi:10.3390/a2041327
    title: Tamal K. Dey and Joshua A. Levine, Delaunay meshing of piecewise smooth complexes without expensive predicates, Algorithms 2(4), 2009, 1327 to 1349
    locator: protection and refinement with only the disk test and Voronoi edge intersections (general locator)
  - paper: doi:10.1145/2699463
    title: Clement Jamin, Pierre Alliez, Mariette Yvinec and Jean-Daniel Boissonnat, CGALmesh, a generic framework for Delaunay mesh generation, ACM Transactions on Mathematical Software 41(4), 2015
    locator: the protection of 1-dimensional features in the CGAL 3D mesh generator (general locator)
  - url: "https://doc.cgal.org/latest/Mesh_3/index.html"
    title: CGAL 3D Mesh Generation user manual
    locator: the section on protection of 1-dimensional features (balls become weighted points, no two balls on different features intersect, no three balls intersect, the parameter edge_size bounds the distance between consecutive centers)
  - paper: doi:10.1142/S0218195901000699
    title: Michael Murphy, David M. Mount and Carl W. Gable, A point-placement strategy for conforming Delaunay tetrahedralization, International Journal of Computational Geometry and Applications 11(6), 2001, 669 to 682
    locator: balls around input vertices and edges, without weights, to get a conforming Delaunay tetrahedralization (general locator)
  - paper: doi:10.1016/j.comgeo.2004.03.001
    title: David Cohen-Steiner, Eric Colin de Verdiere and Mariette Yvinec, Conforming Delaunay triangulations in 3D, Computational Geometry 28(2 to 3), 2004, 217 to 233
    locator: protecting balls on the edges of a piecewise linear complex, without weights (general locator)
  - paper: doi:10.1142/S0218195997000223
    title: Herbert Edelsbrunner and Nimish R. Shah, Triangulating topological spaces, International Journal of Computational Geometry and Applications 7(4), 1997, 365 to 378
    locator: the closed ball property, used in its extended form for the homeomorphism (general locator)
---

Protecting balls make Delaunay refinement work on domains with sharp edges and corners at any angle. Before refinement starts, every corner and every sharp curve of the domain is covered by a chain of balls. Each ball $B(x, r)$ becomes a weighted point $(x, r^2)$ of a weighted Delaunay triangulation, the [regular triangulation](/regular-triangulation/) dual to the [power diagram](/power-diagram/). Refinement then runs as for smooth surfaces, as in [Delaunay surface meshing](/delaunay-surface-meshing/), with unweighted points. Two things follow from the weights and from simple conditions on the balls. The restricted Delaunay edges along each sharp curve are exactly the pairs of neighboring balls, whatever unweighted points are added. And a refinement point taken on a Voronoi edge never lands inside a ball. The second fact keeps refinement from closing in on a small angle forever. Cheng, Dey and Ramos introduced the weighted version for piecewise smooth complexes in 2007; the journal version appeared in 2010. Cheng, Dey and Ray had used weighted balls for polyhedra with small angles in 2005, and protecting balls without weights are older still.

## In plain words

A Delaunay mesher puts new points in the middle of empty spaces. Near a sharp edge where two surfaces meet at a small angle, the empty spaces get thinner and thinner, so it keeps adding points closer and closer to the edge and never stops.

The fix is to fence off the sharp edges first. Lay a string of beads along each edge, each bead overlapping its neighbors, and give each bead a weight equal to its size squared. In the weighted Voronoi diagram, a bead claims the part of the edge it covers more strongly than any ordinary point can. Two things follow. The edge stays meshed as the string of beads, with no point allowed to cut into it. And the mesher never finds an empty space inside a bead, so it never puts a point there. The rest of the domain is meshed as usual.

## When it applies

- The domain is a piecewise smooth complex: vertices, curves, surface patches and volumes, each smooth, glued along their boundaries. Polyhedra, CAD models with sharp edges and non-manifold surfaces are all of this kind.
- Two patches may meet at a curve, or two curves at a vertex, at an angle that is arbitrarily small. Without protection, Delaunay refinement need not terminate there. The termination proofs of [Ruppert's algorithm](/ruppert-algorithm/) and of [tetrahedral Delaunay refinement](/tetrahedral-delaunay-refinement/) assume that the input has no small angles.
- The sharp curves must be kept as curves of the mesh, which is usually what a CAD user wants.
- The mesher can maintain a weighted Delaunay triangulation and find where Voronoi edges and facets meet the curves and patches. CGAL's 3D mesh generator works this way.

## The template

The **protection properties**, in the form used by this page for straight sharp edges, are three. Neighbors along a curve form a chain $x_0, x_1, \ldots, x_m$ with centers on the curve, ending at the vertex balls.

- (a) Neighbors overlap, and neither contains the other's center: $\max(r_p, r_q) < |pq| < r_p + r_q$.
- (b) Balls that are not neighbors are disjoint.
- (c) No ball meets a piece $[p, q]$ of a chain unless it is centered at $p$ or $q$.

Cheng, Dey and Levine (2007) state the properties for curved edges as follows. Neighbors overlap significantly without containing each other's centers. No three balls have a common point. And for a constant $\omega \le 0.076$, every ball $B(p, R)$ with $R$ up to 8 times the protecting radius meets its curve in one open arc and each incident patch in a disk, with normals turning by at most $2\omega$ inside it. Their construction takes the radius $r_x = \frac{\omega}{8} \min\{d_x, d'_x\}$. Here $d_x$ is the distance at which the normal has turned by $\omega$, and $d'_x$ is the distance to the nearest point where a sphere around $x$ touches a curve or patch tangentially.

The layout below is for straight sharp edges. It is the one in the implementation. For a segment $e = uv$ of length $L$, let $H_e$ be its distance to the segments that share no endpoint with it. Let $\sigma_u$ be the sine of the smallest angle between $e$ and another segment at $u$, capped at 90 degrees, and let $\sigma_v$ be the same at $v$. Let $c$ be the size factor, $\frac14$ by default.

```pseudo id=main
PROTECT(vertices, segments, c)
L1  for each vertex v: r_v ← c · min(distance to the segments not at v, half the shortest segment at v)
L2  for each segment e = uv: ρ_e(s) ← c · min(H_e, s σ_u, (L − s) σ_v), for the point at distance s from u
L3      s_a ← the s with s = r_u + ρ_e(s)/2, and s_b ← the s with L − s = r_v + ρ_e(s)/2
L4      put centers from s_a to s_b at equal steps of Φ/m in φ(s) = ∫ ds / ρ_e(s), with m = ⌈Φ/1.4⌉; one center at the midpoint if Φ ≤ 0.7
L5      r_x ← min(ρ_e(x), 0.9 · the distance to the nearer neighbor center of x on e)
L6  check (a), (b) and (c) exactly; fail if any is violated
L7  return every ball B(x, r_x) as the weighted point (x, r_x²)
```

The meshing that follows is outside the template. Run [Delaunay refinement](/delaunay-refinement/) with these weighted points and unweighted new points. Cheng, Dey and Levine's DelPSC inserts a point where a Voronoi edge meets a patch, either when the triangles around a vertex do not form a disk or when a restricted triangle is larger than a resolution $\lambda$. It inserts the orthocenter of a tetrahedron when the radius-edge ratio exceeds $\rho_0$, unless that would delete a restricted triangle.

Power distance is $\pi_p(x) = |x - p|^2 - r_p^2$. An unweighted point has $r = 0$. The restricted pairs of a curve are the pairs of sites whose power cells share a point of the curve: the restricted Delaunay edges of [restricted Delaunay triangulation](/restricted-delaunay-triangulation/), counted with their degenerate cases.

**Claim 1 (proved here: the chain is restricted, for any unweighted points).** Let (a) and (c) hold, and let $U$ be any finite set of unweighted points, anywhere. In the power diagram of the balls and $U$, the restricted pairs of each segment are exactly the neighbors of its chain.

*Proof.* Take neighbors $p, q$ and a point $x$ of $[p, q]$. Since $|x - p| + |x - q| = |pq| < r_p + r_q$, either $|x - p| < r_p$ or $|x - q| < r_q$, so $\min(\pi_p(x), \pi_q(x)) < 0$. For $s \in U$, $\pi_s(x) = |x - s|^2 \ge 0$. For a ball $b$ other than $p, q$, (c) gives $|x - b| > r_b$, so $\pi_b(x) > 0$. So on $[p, q]$ only $p$ and $q$ can be nearest. Along the line, $\pi_p - \pi_q$ is affine, because the squared terms cancel. At $p$ it is $-r_p^2 - (|pq|^2 - r_q^2) < 0$ and at $q$ it is positive, both by (a). So it has exactly one zero on $[p, q]$: $p$ is nearest before it and $q$ after. Walking from $u$ to $v$, the nearest site runs through $x_0, x_1, \ldots, x_m$ in order, and two sites share a point of the segment exactly when they are neighbors. $\square$

**Claim 2 (proved here: Voronoi edges avoid the balls).** Let (b) hold and let every segment carry at least one ball besides its vertex balls. If a point $z$ has three or more nearest sites in power, then $z$ lies in no open ball.

*Proof.* Let $\pi^*$ be the smallest power at $z$. If one of the nearest sites is unweighted, $\pi^* = |z - s|^2 \ge 0$. Otherwise all of them are balls. If $\pi^* < 0$, $z$ lies inside three open balls, which then meet pairwise. By (b) they would be pairwise neighbors in a chain. That is impossible: neighbors are consecutive in a chain or a vertex and its first ball, and since each segment has a ball inside it, no three are pairwise neighbors. So $\pi^* \ge 0$, and $\pi_b(z) \ge \pi^* \ge 0$ for every ball $b$. $\square$

Claim 2 is the reason for the weights. DelPSC inserts points where Voronoi edges meet patches and at orthocenters of tetrahedra, which have four nearest sites. By Claim 2 none of them is inside a protecting ball, so the point set stays admissible: the weighted points plus unweighted points outside the balls. This is Lemma 3 of Cheng, Dey and Levine. With weight zero on the same centers, Voronoi edges do pass through the balls. The tests place an unweighted point just outside two neighboring balls. The point equidistant from it and the two centers then lies deep inside a ball, and those three are its nearest sites.

**Claim 3 (proved here: the layout gives (b) and (c) when $c < \frac12$).** Ignore the rounding of the centers to rationals. With $c < \frac12$, the balls of lines L1 to L5 satisfy (b) and (c).

*Proof.* For $x$ on $e$ at distance $s$ from $u$, let $f$ be another segment. If $f$ shares no endpoint with $e$, then $d(x, f) \ge H_e$. If $f$ meets $e$ at $u$ at angle $\theta$, then $d(x, f) \ge s \sin \theta$ when $\theta \le 90$ degrees, and $d(x, f) \ge s$ otherwise. So $\rho_e(x) \le c \, d(x, f)$ for every other segment $f$, and the same holds for $r_v \le c \, d(v, f)$ for $f$ not at $v$. For balls $x$ and $y$ on different segments, $r_x + r_y \le c\,d(x, f_y) + c\,d(y, f_x) \le 2c|xy| < |xy|$. The same bound covers a vertex ball and a ball on a segment not at that vertex. A ball meets no piece of another segment, because $r_x \le c\, d(x, f) < d(x, f)$. On one segment, line L5 keeps every radius below the gap to each neighbor. Line L3 puts the first center past the vertex ball, $s_a > r_u$. So a ball never reaches its neighbor's center, balls two apart are disjoint, and no ball meets a piece of its own segment that it does not end. Two vertex balls on the same segment have $r_u + r_v \le c L < L$. $\square$

The bound $c < \frac12$ is tight. At the 10 degree corner of the example below, two balls at distance $s$ from the corner, one on each edge, are $2 s \sin 5° \approx 0.1743\, s$ apart. Each has radius $c\, s \sin 10° \approx 0.1736\, c\, s$. So (b) fails as soon as $c > 0.502$. The test finds that $c = \frac12$ passes the exact check and $c = 0.55$ fails it. Property (a) is not proved for this layout, because it depends on how fast $\rho_e$ changes between neighbors. Line L6 checks it, with (b) and (c), in exact rational arithmetic.

**Claim 4 (proved here: number of balls).** Segment $e$ gets at most $\Phi/1.4 + 2$ balls besides its vertex balls, where
$$\Phi \le \frac1c \Big( \frac{L}{H_e} + \frac{\ln(L / r_u)}{\sigma_u} + \frac{\ln(L / r_v)}{\sigma_v} \Big).$$

*Proof.* Line L4 places $m + 1$ centers with $m = \lceil \Phi / 1.4 \rceil$, or one. Next, $1/\min(a, b, c') \le 1/a + 1/b + 1/c'$. Integrating over $[s_a, s_b]$ with $s_a \ge r_u$ and $L - s_b \ge r_v$ gives the bound. Here $\Phi$ is computed by a numerical integral, and the bound is for that value. $\square$

So the count grows like $1/\sigma$ times a logarithm at a small angle, not like $1/\sigma^2$. This is the graded shrinking that the weights allow near a corner.

**What the papers prove, and of which kind.** Cheng, Dey and Ramos prove termination and a homeomorphism. Termination is proved with no bound on the number of points. The homeomorphism is an existence theorem: the output is homeomorphic to the domain once the sample is dense enough, with no explicit threshold. Cheng, Dey and Levine's DelPSC keeps only the disk test. For it they state three properties. Termination is their Theorem 1. T1 says every sharp curve is meshed as the chain of its protecting balls, for every $\lambda$; it follows from their Lemma 1, which is Claim 1 for curved edges. T2 says every patch is meshed as a manifold, for every $\lambda$. T3 says there exists a $\lambda > 0$ for which the output is homeomorphic to the domain, again with no value given. They skip the proof of T2 in that paper.

**Proved constants and measured ones.** The proved conditions are very cautious, much more so than what works in practice. The radius $\frac{\omega}{8} \min\{d_x, d'_x\}$ with $\omega \le 0.076$ is under 1 percent of the distance at which the normal turns by $\omega$. Cheng, Dey and Levine write that the properties "can be satisfied in practice by using sufficiently small balls around the non-smooth edges". The topology theorem gives only the existence of some $\lambda$. Their experiments set $\lambda$ to 10 percent of the smallest side of the bounding box and $\rho_0 = 1.4$, and on their eleven models they report the right topology, with 1340 to 19810 vertices in 4.8 to 170.9 seconds. The same holds here, on a small scale. The proof of Claim 3 needs $c < \frac12$. Yet with $c = 1.2$, where the exact check fails, the chains of the example were still the restricted pairs against 60 random admissible points, with a size factor 2.4 times the proved limit. At $c = 1.6$ they were not.

## Classic examples

**A corner of 10 degrees.** Take $O = (0,0,0)$, $A = (1000,0,0)$, $B = (985,174,0)$ and $C = (0,0,1000)$, with the segments $OA$, $OB$, $AB$ and $OC$. The angle $AOB$ is $10.02$ degrees, and $OC$ is at right angles to the other two. With $c = \frac14$, PROTECT makes 98 balls and the exact check passes.

| segment | length | $\sigma$ at its ends | balls inside | smallest radius | largest radius | bound of Claim 4 |
|---|---|---|---|---|---|---|
| $OA$ | 1000.0 | 0.174, 0.996 | 38 | 5.56 | 35.34 | 47.1 |
| $OB$ | 1000.3 | 0.174, 0.996 | 38 | 5.56 | 35.36 | 47.1 |
| $AB$ | 174.6 | 0.996, 0.996 | 9 | 6.21 | 21.13 | 14.4 |
| $OC$ | 1000.0 | 1, 1 | 9 | 35.71 | 121.0 | 16.8 |

The vertex balls have radius 125 at $O$ and $C$, a quarter of half of 1000, and 21.83 at $A$ and $B$, a quarter of half of $AB$. Along $OA$, from the corner, each radius is 6.15 percent larger than the one before. Along $OC$, which meets nothing at a small angle, the step is 32.4 percent. The thin wedge between $OA$ and $OB$ is fenced off by two chains of small balls that never touch each other. Adding unweighted points anywhere does not change the chains, as Claim 1 says. Without weights, an unweighted point near the middle of a piece takes part of the edge from its two neighbors. The tests check both.

**Polyhedra with small angles.** The sharp edges of a polyhedron are straight segments, which is the case above. Cheng, Dey and Ray (2005) protected them with weighted balls and refined the rest by weighted Delaunay refinement.

**Piecewise smooth complexes.** Curved sharp edges, as in CAD models and non-manifold surfaces, need the normal conditions as well. Cheng, Dey and Ramos proved termination and topology for any input angles. Cheng, Dey and Levine made it practical with the single disk test.

**CGAL.** CGAL's 3D mesh generator protects the 1-dimensional features with balls that become weighted points. Its manual requires that no two balls centered on different features intersect, and that no three balls intersect. The user parameter `edge_size` bounds the distance between consecutive centers.

## Variations

- **Unweighted protection.** Murphy, Mount and Gable (2001) and Cohen-Steiner, Colin de Verdière and Yvinec (2002, journal 2004) protect the edges of a polyhedron with balls that carry no weights, to get a [conforming Delaunay](/conforming-delaunay-triangulation/) tetrahedralization.
- **Cheaper predicates.** Dey and Levine (2009) give a version of the piecewise smooth mesher without the expensive predicates of the 2007 algorithm, as their title says.
- **Larger balls.** The proved conditions are sufficient, not necessary. In the example, chains survived random points with a size factor of 1.2, far above the proved $\frac12$. A mesher can start with large balls and shrink only those that fail a check.

## Pitfalls

- The weights must stay. An unweighted Delaunay triangulation of the same centers lets Voronoi edges pass inside the balls, and a refinement point inserted there breaks the chain.
- Protection does not make the elements good. DelPSC refines tetrahedra by radius-edge ratio with $\rho_0 = 1.4$, and a radius-edge bound does not remove slivers, the flat [sliver tetrahedra](/sliver-tetrahedron/). Near the balls, tetrahedra are not refined at all when the orthocenter would delete a restricted triangle. Small angles in the input stay small angles in the mesh.
- The size of the balls is set by the smallest angle and the nearest other feature. A pair of sharp edges that nearly touch forces tiny balls along their whole length, and the count grows like $L/H_e$.
- The layout of this page computes in floating point and then checks exactly. A check that fails raises an error, rather than returning balls that are not safe.
- The ball conditions for curved edges need normal deviation and tangency distances, which are expensive to compute. DelPSC computes them once, before refinement.

## Exercises

1. Show that Claim 1 fails without (c). Find a ball, two neighbors $p$ and $q$ and a point of $[p, q]$ where the third ball is nearest.
2. For two segments meeting at angle $\theta$, find the largest $c$ for which balls at equal distance from the corner, one on each segment, are disjoint. Check it against the 0.502 of the example.
3. Prove that a point of the power diagram with an unweighted nearest site has nonnegative power to every site, and use it to show that DelPSC's orthocenters are never inside a ball.
4. With $\sigma_u = \sin 10°$ and $c = \frac14$, how many balls does Claim 4 allow from $r_u = 125$ out to distance 500? Compare with the 38 balls of $OA$.

## References
