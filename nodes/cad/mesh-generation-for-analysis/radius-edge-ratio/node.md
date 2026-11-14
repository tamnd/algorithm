---
tag: DA80T5
kind: definition
slug: radius-edge-ratio
name: Radius-edge ratio
aliases:
- circumradius to shortest edge ratio
area: cad/mesh-generation-for-analysis
level: core
summary: The circumradius of a simplex divided by its shortest edge. Delaunay refinement bounds it, which bounds angles in 2D but lets slivers pass in 3D.
prereqs: [circumcenter, triangulation, tetrahedralization]
see_also: [mesh-quality-measures, scaled-jacobian, sliver-tetrahedron, delaunay-refinement, ruppert-algorithm, tetrahedral-delaunay-refinement, sliver-exudation, max-min-angle-triangulation]
sources:
  - paper: doi:10.1145/225058.225286
    title: Gary L. Miller, Dafna Talmor, Shang-Hua Teng and Noel Walkington, A Delaunay based numerical method for three dimensions, generation, formulation, and partition, Proceedings of the 27th ACM Symposium on Theory of Computing, 1995, 683 to 692
    locator: the radius-edge ratio as the quality measure of three-dimensional Delaunay meshes (general locator)
  - paper: doi:10.1145/276884.276894
    title: Jonathan Richard Shewchuk, Tetrahedral mesh generation by Delaunay refinement, Proceedings of the 14th ACM Symposium on Computational Geometry, 1998, 86 to 95
    locator: the refinement with radius-edge bound 2 and the remark that slivers survive it
  - paper: doi:10.1145/355483.355487
    title: Siu-Wing Cheng, Tamal K. Dey, Herbert Edelsbrunner, Michael A. Facello and Shang-Hua Teng, Sliver exudation, Journal of the ACM 47(5), 2000, 883 to 904
    locator: the classification of bad tetrahedra and the definition of slivers as tetrahedra with a bounded radius-edge ratio and a small volume (general locator)
  - book: isbn:9781584887300
    title: Siu-Wing Cheng, Tamal K. Dey and Jonathan Richard Shewchuk, Delaunay Mesh Generation, CRC Press, 2012
    locator: Chapter 1, Introduction (quality measures), Chapter 6, Delaunay refinement in the plane, and Chapter 8, Tetrahedral meshing of PLCs
  - paper: "Jonathan Richard Shewchuk, What is a good linear element? Interpolation, conditioning, and quality measures, Proceedings of the 11th International Meshing Roundtable, Sandia National Laboratories, 2002, 115 to 126"
    locator: the comparison of the radius-edge ratio with measures that also detect slivers
---

The radius-edge ratio of a triangle or a tetrahedron is its circumradius divided by the length of its shortest edge. It is the quality measure that [Delaunay refinement](/delaunay-refinement/) controls, because the cure for a bad element is to insert its [circumcenter](/circumcenter/). In the plane a bound on the ratio is the same as a lower bound on the smallest angle. In space it is not: a [sliver tetrahedron](/sliver-tetrahedron/) has a small ratio and a volume near zero.

## Definition

Let $\sigma$ be a $d$-simplex in $\mathbb{R}^d$, with $d = 2$ (a triangle) or $d = 3$ (a tetrahedron), and with affinely independent vertices $v_0, \ldots, v_d$. A point $x$ is at the same distance from all vertices if and only if $2 (v_i - v_0) \cdot x = |v_i|^2 - |v_0|^2$ for $i = 1, \ldots, d$. The vectors $v_i - v_0$ are linearly independent, so this linear system has exactly one solution $O$, the circumcenter. The circumradius is $R(\sigma) = |v_0 - O|$, the radius of the [circumcircle](/circumcircle/) or circumsphere. Let $\ell_{\min}(\sigma) = \min_{i < j} |v_i - v_j|$. The **radius-edge ratio** is

$$\rho(\sigma) = \frac{R(\sigma)}{\ell_{\min}(\sigma)}.$$

If the vertices of a triangle are collinear, there is no circumcircle, and we set $\rho = \infty$. A flat tetrahedron is different: if its four vertices lie on one circle, $R$ and $\ell_{\min}$ have finite limits, and so does $\rho$.

**As a quality measure.** Smaller is better. The range is $[\rho_d^*, \infty)$ with $\rho_2^* = 1/\sqrt{3} \approx 0.577$ and $\rho_3^* = \sqrt{6}/4 \approx 0.612$, and the ideal value $\rho_d^*$ occurs only for the regular simplex (theorem below). A large value detects a short edge relative to the circumsphere. In the plane this is the same as a small angle. In space it detects needles, wedges and caps, but not slivers. It is one of the [mesh quality measures](/mesh-quality-measures/).

**Invariance.** A translation, a rotation or a reflection does not change $R$ or $\ell_{\min}$. A uniform scaling $x \mapsto s x$ with $s > 0$ multiplies both by $s$. So $\rho$ is invariant under similarities. It is not invariant under a general affine map: the map $(x, y) \mapsto (x, y/10)$ sends the equilateral triangle with $\rho = 0.577$ to a flat triangle with $\rho \approx 2.9$. So $\rho$ measures shape for an isotropic target size. An [anisotropic mesh](/anisotropic-mesh-adaptation/) measures it in the metric of the target size.

**The angle form in the plane.** Let a triangle have circumradius $R$ and angles $\theta_1 \le \theta_2 \le \theta_3$. By the inscribed angle theorem, the edge opposite the angle $\theta$ is a chord that subtends the central angle $2 \theta$, so its length is $2 R \sin \theta$. The angles add up to $\pi$, so $\theta_3 \le \pi - 2 \theta_1$, and all three angles are in $[\theta_1, \pi - \theta_1]$. On that interval $\sin \theta \ge \sin \theta_1$. So the shortest edge is opposite $\theta_1$, and

$$\rho = \frac{1}{2 \sin \theta_{\min}}.$$

So $\rho \le B$ holds if and only if $\theta_{\min} \ge \arcsin(1 / (2B))$. The bound $B = \sqrt{2}$ of [Ruppert's algorithm](/ruppert-algorithm/) gives about $20.7°$, and $B = 1$ gives $30°$. A lower bound on the smallest angle also bounds the largest angle by $\pi - 2 \theta_{\min}$. The [Delaunay triangulation](/delaunay-triangulation/) of a point set maximizes the smallest angle over all triangulations of the set ([max-min angle triangulation](/max-min-angle-triangulation/)), so it also minimizes the largest radius-edge ratio.

**Theorem (lower bound).** Every $d$-simplex satisfies

$$\rho(\sigma) \ge \sqrt{\frac{d}{2(d + 1)}},$$

with equality if and only if $\sigma$ is regular. For $d = 2$ this is $1/\sqrt{3}$, and for $d = 3$ it is $\sqrt{3/8} = \sqrt{6}/4$.

*Proof.* Let $c = \frac{1}{d+1} \sum_i v_i$ be the centroid and $O$ the circumcenter. Translate so that $c = 0$. Then $\sum_i v_i = 0$, and

$$\sum_{i < j} |v_i - v_j|^2 = \frac{1}{2} \sum_{i, j} \left( |v_i|^2 + |v_j|^2 - 2 v_i \cdot v_j \right) = (d+1) \sum_i |v_i|^2 - \Big| \sum_i v_i \Big|^2 = (d + 1) \sum_i |v_i|^2.$$

Also $\sum_i |v_i - O|^2 = \sum_i |v_i|^2 - 2 O \cdot \sum_i v_i + (d+1) |O|^2 = \sum_i |v_i|^2 + (d+1)|O|^2$. The left side is $(d+1) R^2$. The simplex has $\binom{d+1}{2}$ edges, each of length at least $\ell_{\min}$. Together,

$$\frac{(d+1) d}{2} \ell_{\min}^2 \le \sum_{i<j} |v_i - v_j|^2 = (d+1) \sum_i |v_i|^2 \le (d+1)^2 R^2,$$

so $\ell_{\min}^2 \le \frac{2 (d+1)}{d} R^2$, which is the bound. Equality needs equality in both steps: every edge has length $\ell_{\min}$, so the simplex is regular. Conversely, in a regular simplex every edge has the same length, and the symmetries of the simplex fix both $c$ and $O$, which are then the same point, so both steps are equalities. $\blacksquare$

**Theorem (a bounded ratio does not bound the volume).** For $0 < h \le 1/\sqrt{3}$ and $a = \sqrt{1 - h^2}$, let $T_h$ be the tetrahedron with vertices

$$v_1 = (a, 0, h), \quad v_2 = (0, a, -h), \quad v_3 = (-a, 0, h), \quad v_4 = (0, -a, -h).$$

Then $R(T_h) = 1$, $\rho(T_h) = 1/\sqrt{2 + 2h^2} < 1/\sqrt{2}$, and the volume of $T_h$ is $\frac{4}{3} a^2 h$, which tends to 0 with $h$.

*Proof.* Each vertex has $|v_i|^2 = a^2 + h^2 = 1$, so the unit sphere passes through all four. The vertices are not coplanar for $h > 0$ (the volume below is positive), so this is the circumsphere and $R = 1$. The four edges $v_1 v_2$, $v_2 v_3$, $v_3 v_4$, $v_4 v_1$ have difference vectors of the form $(\pm a, \pm a, \pm 2h)$, of length $\sqrt{2a^2 + 4h^2} = \sqrt{2 + 2h^2}$. The two edges $v_1 v_3$ and $v_2 v_4$ have length $2a$. Since $h^2 \le 1/3$, $2 + 2h^2 \le 4 - 4h^2 = 4a^2$, so $\ell_{\min} = \sqrt{2 + 2h^2}$ and $\rho = 1/\sqrt{2 + 2h^2}$. With $v_2 - v_1 = (-a, a, -2h)$, $v_3 - v_1 = (-2a, 0, 0)$ and $v_4 - v_1 = (-a, -a, -2h)$, expansion along the middle vector gives $\det(v_2 - v_1, v_3 - v_1, v_4 - v_1) = 2a \cdot (a \cdot (-2h) - (-2h)(-a)) = -8 a^2 h$. The volume is $|{-8 a^2 h}| / 6 = \frac{4}{3} a^2 h$. $\blacksquare$

At $h = 1/\sqrt{3}$, $T_h$ is the regular tetrahedron with edge $\sqrt{8/3}$ and $\rho = \sqrt{6}/4$. As $h \to 0$, $T_h$ flattens into the square with vertices $(\pm 1, 0, 0)$ and $(0, \pm 1, 0)$, inscribed in the unit circle, and $\rho$ rises only to $1/\sqrt{2}$. So every bound $B \ge 1/\sqrt{2}$ on $\rho$ admits tetrahedra of arbitrarily small volume. Tetrahedral Delaunay refinement uses $B = 2$, so a radius-edge bound does not remove slivers. They need a separate step such as [sliver exudation](/sliver-exudation/).

## Examples and non-examples

**Triangles.** The values follow from $\rho = 1/(2 \sin \theta_{\min})$.

| Triangle | $\theta_{\min}$ | $\rho$ |
| --- | --- | --- |
| equilateral | $60°$ | $1/\sqrt{3} \approx 0.577$ |
| right isosceles $(0,0), (1,0), (0,1)$ | $45°$ | $1/\sqrt{2} \approx 0.707$ |
| $30°$, $60°$, $90°$ | $30°$ | $1$ |
| needle $(0,0), (1,0), (0, 0.1)$ | $\arctan 0.1 \approx 5.71°$ | $\approx 5.02$ |
| flat obtuse $(-1,0), (1,0), (0, 0.1)$ | $\approx 5.71°$ | $\approx 5.02$ |

The flat obtuse triangle has an angle of about $168.6°$. The ratio flags it through its two small angles. In the plane every triangle with an angle near $\pi$ also has a small angle, so the ratio catches it. The [maximum angle condition](/maximum-angle-condition/) shows that the large angle, not the small one, is what spoils the interpolation of gradients.

**Tetrahedra with a large ratio.**

- A cap: the equilateral triangle with vertices on the unit circle in the plane $z = 0$, and a fourth vertex $(0, 0, \varepsilon)$. The circumcenter is $(0, 0, (\varepsilon^2 - 1)/(2\varepsilon))$, so $R = (1 + \varepsilon^2)/(2 \varepsilon)$. The shortest edges join the apex to the base, of length $\sqrt{1 + \varepsilon^2}$, so $\rho = \sqrt{1 + \varepsilon^2}/(2 \varepsilon)$. For $\varepsilon = 0.1$, $\rho \approx 5.02$, and three dihedral angles are about $160.4°$.
- A needle or a wedge: a tetrahedron with one very short edge, or two very close vertices. Then $\ell_{\min}$ is small while $R$ is at least half the longest edge, so $\rho$ is large.

**Tetrahedra with a small ratio.**

- The regular tetrahedron: $\rho = \sqrt{6}/4 \approx 0.612$, the least value.
- The non-example that matters: the slivers $T_h$ above. For $h = 0.1$, $\rho \approx 0.704$, the volume is $0.132$, and the dihedral angles are four of about $16.0°$ and two of about $157.3°$. For $h = 0.01$, $\rho \approx 0.707$, the volume is $0.0133$, and the dihedral angles are four of about $1.6°$ and two of about $177.7°$. The ratio rates this almost flat element better than a right isosceles triangle.

## Related definitions

- [Mesh quality measures](/mesh-quality-measures/): the family of measures. The radius ratio $d\, r / R$, with $r$ the inradius, is 1 for the regular simplex and tends to 0 for every flat element, slivers included.
- [Scaled Jacobian](/scaled-jacobian/): a corner measure that is near 0 for a sliver. For $T_{0.01}$ the normalized value is about $0.028$.
- [Sliver tetrahedron](/sliver-tetrahedron/): the element that a radius-edge bound lets through.
- [Delaunay refinement](/delaunay-refinement/), [Ruppert's algorithm](/ruppert-algorithm/) and [Chew's second algorithm](/chew-second-algorithm/): they insert circumcenters until every triangle has $\rho \le B$. [Tetrahedral Delaunay refinement](/tetrahedral-delaunay-refinement/) does the same in space.
- [Sliver exudation](/sliver-exudation/): removes the slivers that remain after the refinement.

## References
