---
tag: H7T63F
kind: definition
slug: sliver-tetrahedron
name: Sliver tetrahedron
aliases:
- sliver element
area: cad/mesh-generation-for-analysis
level: core
summary: A flat tetrahedron with four nearly cocircular, coplanar vertices, good in radius-edge ratio but near zero in volume, which Delaunay refinement alone cannot remove.
prereqs: [radius-edge-ratio, tetrahedralization]
see_also: [scaled-jacobian, mesh-quality-measures, tetrahedral-delaunay-refinement, sliver-exudation, maximum-angle-condition, isosurface-stuffing, optimization-based-mesh-smoothing, topological-tetrahedral-mesh-improvement]
sources:
  - paper: doi:10.1145/355483.355487
    title: Siu-Wing Cheng, Tamal K. Dey, Herbert Edelsbrunner, Michael A. Facello and Shang-Hua Teng, Sliver exudation, Journal of the ACM 47(5), 2000, 883 to 904
    locator: the definition of a sliver by a bounded radius-edge ratio and a small volume relative to the shortest edge, and the weighted Delaunay construction that has no slivers (general locator)
  - book: isbn:9781584887300
    title: Siu-Wing Cheng, Tamal K. Dey and Jonathan Richard Shewchuk, Delaunay Mesh Generation, CRC Press, 2012
    locator: Chapter 8, Tetrahedral meshing of PLCs (refining slivers away), Chapter 10, Sliver exudation, and Chapter 11, Refinement for sliver exudation
  - paper: "Jonathan Richard Shewchuk, What is a good linear element? Interpolation, conditioning, and quality measures, Proceedings of the 11th International Meshing Roundtable, Sandia National Laboratories, 2002, 115 to 126"
    locator: the effect of large and small dihedral angles on interpolation error and on the conditioning of the stiffness matrix (general locator)
  - paper: doi:10.1145/276884.276894
    title: Jonathan Richard Shewchuk, Tetrahedral mesh generation by Delaunay refinement, Proceedings of the 14th ACM Symposium on Computational Geometry, 1998, 86 to 95
    locator: the radius-edge bound of tetrahedral Delaunay refinement and the slivers that survive it
  - paper: doi:10.1145/335305.335338
    title: Herbert Edelsbrunner, Xiang-Yang Li, Gary Miller, Andreas Stathopoulos, Dafna Talmor, Shang-Hua Teng, Alper Üngör and Noel Walkington, Smoothing and cleaning up slivers, Proceedings of the 32nd ACM Symposium on Theory of Computing, 2000
    locator: removal of slivers by perturbation of the vertices (general locator)
---

A sliver is a tetrahedron whose four vertices lie close to one circle, so the element is almost flat although none of its edges is short. Its [radius-edge ratio](/radius-edge-ratio/) is small, as small as for good elements, while its volume and some of its dihedral angles are near zero and others are near $180°$. [Delaunay refinement](/delaunay-refinement/), which tests only the radius-edge ratio, never selects a sliver, so slivers remain in its output and need a separate step to remove them.

## Definition

For a tetrahedron $\tau$ with signed volume $V(\tau)$, shortest edge $\ell_{\min}(\tau)$ and radius-edge ratio $\rho(\tau)$, let

$$\sigma(\tau) = \frac{V(\tau)}{\ell_{\min}(\tau)^3},$$

the volume-edge ratio. It is invariant under similarities. For the regular tetrahedron, $\sigma = 1/(6\sqrt{2}) \approx 0.118$. Fix two constants $\bar\rho$ and $\bar\sigma$. Following Cheng, Dey, Edelsbrunner, Facello and Teng, a tetrahedron is a **sliver** if

$$\rho(\tau) \le \bar\rho \quad \text{and} \quad \sigma(\tau) < \bar\sigma.$$

The first condition says that no edge is short compared with the circumsphere. The second says that the element is flat. So a sliver is a flat tetrahedron that the radius-edge ratio does not detect. The constants depend on the application. The definition is a statement about the shape only, not about the mesh that holds the tetrahedron.

**The classes of bad tetrahedra.** A tetrahedron with a small volume relative to its edges falls into one of a few shapes. A needle has its vertices near a line with one short edge. A wedge has two vertices very close together, so one edge is short. A cap has one vertex close to the plane of the opposite face, inside the triangle, so it has three dihedral angles near $180°$. A sliver has its four vertices near a circle and no short edge. Needles, wedges and caps have a large radius-edge ratio, because their circumsphere is large compared with their shortest edge. Only the sliver has a small one.

**Why the four vertices are near a circle.** If $\rho \le \bar\rho$ and $V \to 0$ with $\ell_{\min}$ fixed, the circumradius stays bounded. In the limit the four vertices lie on a sphere and in a plane, so they lie on the circle where the plane cuts the sphere. A flat tetrahedron whose vertices are not on a circle would have a circumsphere whose radius tends to infinity, and then $\rho$ would not stay bounded.

**Theorem (an explicit family).** For $0 < h \le 1/\sqrt{3}$ and $a = \sqrt{1 - h^2}$, let $T_h$ have the vertices $v_1 = (a, 0, h)$, $v_2 = (0, a, -h)$, $v_3 = (-a, 0, h)$, $v_4 = (0, -a, -h)$. Then:

1. $R = 1$, $\rho(T_h) = 1/\sqrt{2 + 2h^2} < 1/\sqrt{2}$, and $V = \frac{4}{3} a^2 h$, so $\sigma(T_h) \to 0$ as $h \to 0$.
2. The four dihedral angles at the edges $v_1 v_2$, $v_2 v_3$, $v_3 v_4$, $v_4 v_1$ are $\psi = \arccos \frac{a^2}{a^2 + 4h^2}$, which tends to 0.
3. The two dihedral angles at the edges $v_1 v_3$ and $v_2 v_4$ are $\varphi = \arccos \frac{4h^2 - a^2}{4h^2 + a^2}$, which tends to $\pi$.

So for every $\bar\rho \ge 1/\sqrt{2}$ and every $\bar\sigma > 0$, the family contains slivers.

*Proof.* Part 1 is proved on the [radius-edge ratio](/radius-edge-ratio/) page: all four vertices are on the unit sphere, the shortest edges have length $\sqrt{2 + 2h^2}$, and the determinant of the edge vectors at $v_1$ is $-8a^2 h$. For part 3, the edge $v_1 v_3$ lies on the line $y = 0$, $z = h$. In the plane $x = 0$, which is perpendicular to it, the faces $v_1 v_3 v_2$ and $v_1 v_3 v_4$ leave the edge in the directions $(a, -2h)$ and $(-a, -2h)$ in the $(y, z)$ coordinates. The cosine of the angle between them is $(-a^2 + 4h^2)/(a^2 + 4h^2)$. The edge $v_2 v_4$ is the same by the isometry $(x, y, z) \mapsto (-y, x, -z)$, which maps $v_1 \to v_2 \to v_3 \to v_4 \to v_1$. For part 2, that isometry maps the four side edges onto each other, so it is enough to take $v_1 v_2$. The normals $n_1 = (v_2 - v_1) \times (v_3 - v_1) = (0, 4ah, 2a^2)$ and $n_2 = (v_2 - v_1) \times (v_4 - v_1) = (-4ah, 0, 2a^2)$ belong to the faces $v_1 v_2 v_3$ and $v_1 v_2 v_4$. Since $n_1 \cdot (v_4 - v_1) = -8a^2 h < 0$ and $n_2 \cdot (v_3 - v_1) = 8 a^2 h > 0$, the first normal points out of the tetrahedron and the second points in. So the dihedral angle at $v_1 v_2$ equals the angle between $n_1$ and $n_2$, whose cosine is $4a^4 / (16 a^2 h^2 + 4 a^4) = a^2/(a^2 + 4h^2)$. $\blacksquare$

At $h = 1/\sqrt{3}$ both formulas give $\arccos(1/3) \approx 70.53°$, the dihedral angle of the regular tetrahedron.

## Examples and non-examples

**Slivers.** The table lists $T_h$ for three values of $h$. The scaled Jacobian is defined on the [scaled Jacobian](/scaled-jacobian/) page, with ideal value 1.

| $h$ | $\rho$ | $\sigma$ | $\psi$ (4 edges) | $\varphi$ (2 edges) | scaled Jacobian |
| --- | --- | --- | --- | --- | --- |
| $1/\sqrt{3}$ | $0.612$ | $0.118$ | $70.53°$ | $70.53°$ | $1$ |
| $0.3$ | $0.677$ | $0.113$ | $44.23°$ | $115.66°$ | $0.743$ |
| $0.1$ | $0.704$ | $0.046$ | $16.02°$ | $157.27°$ | $0.279$ |
| $0.01$ | $0.707$ | $0.0047$ | $1.62°$ | $177.71°$ | $0.028$ |

The radius-edge ratio hardly moves, while $\sigma$, the dihedral angles and the scaled Jacobian show the flattening.

**Slivers in Delaunay meshes.** The 8 vertices of a cube lie on one sphere, and the 4 vertices of each face lie on one circle. After a small perturbation of the points of a cubic grid, the Delaunay tetrahedralization can hold a tetrahedron with its four vertices near one square face. It is a sliver, although the points are evenly spaced. This is why slivers are common in Delaunay tetrahedralizations of well-spaced points.

**Not slivers.**

- The cap with apex at height $0.1$ over an equilateral triangle on the unit circle: it is flat, but $\rho \approx 5.02$, so the radius-edge ratio already detects it and Delaunay refinement removes it.
- A needle or a wedge: it has a short edge, so $\rho$ is large.
- A flat triangle in the plane: there is no two-dimensional sliver. A triangle with $\rho \le B$ has all angles in $[\arcsin(1/(2B)), \pi - 2 \arcsin(1/(2B))]$, as the radius-edge ratio page proves.

**Why a sliver is harmful.** A sliver has dihedral angles near $180°$. For linear elements, a large angle spoils the interpolation of gradients; the [maximum angle condition](/maximum-angle-condition/) proves this for triangles, and the analogous condition for tetrahedra bounds dihedral and face angles away from $180°$. Its small dihedral angles make large entries in the stiffness matrix, because the entries are weighted by cotangents of the dihedral angles, and so they raise the condition number. Shewchuk's survey gives both effects.

**Why Delaunay refinement leaves slivers.** A refinement that tests only $\rho \le B$ never selects a sliver, since its ratio is below $1/\sqrt{2}$ and the usual bound is $B = 2$. To split a sliver at its circumcenter would not fit the termination proof either. The proof needs each new vertex to be farther from the other vertices than the shortest edge of the element it splits, by a factor $B > 1$. The circumcenter of a sliver is only at distance $R = \rho\, \ell_{\min} < \ell_{\min}$ from its vertices.

## Related definitions

- [Radius-edge ratio](/radius-edge-ratio/): small for slivers, which is the whole problem.
- [Scaled Jacobian](/scaled-jacobian/) and the radius ratio of the [mesh quality measures](/mesh-quality-measures/): both tend to 0 for a sliver.
- [Tetrahedral Delaunay refinement](/tetrahedral-delaunay-refinement/): bounds the radius-edge ratio and leaves slivers.
- [Sliver exudation](/sliver-exudation/): assigns weights to the vertices so that the weighted Delaunay tetrahedralization has no slivers. The proved bound on the dihedral angles is very small. Better values in practice are only measured.
- [Isosurface stuffing](/isosurface-stuffing/): fills a domain from a lattice with proved dihedral angle bounds, so slivers cannot occur.
- [Optimization-based mesh smoothing](/optimization-based-mesh-smoothing/) and [topological tetrahedral mesh improvement](/topological-tetrahedral-mesh-improvement/): remove slivers in practice by moving vertices and by flips, with no general guarantee.

## References
