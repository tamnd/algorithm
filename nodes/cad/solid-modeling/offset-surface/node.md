---
tag: 8YJHX6
kind: definition
slug: offset-surface
name: Offset surface
aliases:
- parallel surface
area: cad/solid-modeling
level: core
summary: The surface at a constant distance d along the normal of a given surface, which can self-intersect where d exceeds the radius of curvature.
prereqs: [parametric-surface, surface-curvature, offset-curve]
see_also: [curve-offsetting, solid-offsetting, rossignac-requicha-offsetting, rolling-ball-blend, medial-axis, signed-distance-function, cutter-location-data, fundamental-forms]
sources:
  - book: isbn:9783540424543
    title: Nicholas M. Patrikalakis and Takashi Maekawa, Shape Interrogation for Computer Aided Design and Manufacturing, Springer, 2002
    locator: Chapter 11, Offset curves and surfaces, Section 11.3, Offset surfaces, Section 11.4, Pythagorean hodograph, and Section 11.5, General offsets
  - paper: "Takashi Maekawa, An overview of offset curves and surfaces, Computer-Aided Design 31(3), 165 to 173, 1999"
    locator: the whole survey (the definition, the rationality question, approximation methods and self-intersections of offsets)
  - paper: "Rida T. Farouki, The approximation of non-degenerate offset surfaces, Computer Aided Geometric Design 3(1), 15 to 43, 1986"
    locator: the whole paper (the regularity of the offset in terms of the principal radii of curvature, and the approximation of offsets by bicubic patches)
  - paper: doi:10.1016/0167-8396(86)90017-8
    title: Jaroslaw R. Rossignac and Aristides A. G. Requicha, Offsetting operations in solid modelling, Computer Aided Geometric Design 3(2), 129 to 148, 1986
    locator: the offsets of faces, edges and vertices that make up the offset of a solid
---

The offset surface of a regular [parametric surface](/parametric-surface/) $S(u, v)$ at the signed distance $d$ is the surface $O_d(u, v) = S(u, v) + d \, N(u, v)$, where $N$ is the unit normal. It is the 3D analog of the [offset curve](/offset-curve/). An offset has the same normal as the surface at corresponding points, and its principal curvatures follow from those of the surface. Where $d$ reaches a principal radius of curvature on the concave side, the offset has a singular point, and beyond that it folds over and intersects itself. The unit normal contains a square root, so the offset of a polynomial or rational surface is not rational in general, and CAD systems store an approximation.

## Definition

Let $S : D \to \mathbb{R}^3$ be a regular parametric surface, with unit normal

$$N(u, v) = \frac{S_u \times S_v}{\left| S_u \times S_v \right|}.$$

For a real number $d$, the **offset surface** of $S$ at distance $d$ is the map

$$O_d(u, v) = S(u, v) + d \, N(u, v), \qquad (u, v) \in D.$$

For $d > 0$ it lies on the side of $N$, and for $d < 0$ on the other side. For an implicit surface $f = 0$ with $\nabla f \ne 0$, the same definition uses $N = \nabla f / |\nabla f|$.

Three facts follow from the derivatives. Write $\kappa_1, \kappa_2$ for the principal curvatures of $S$ with the sign convention that $N_u = -\kappa_i S_u$ along a principal direction (the Weingarten equations; see [fundamental forms](/fundamental-forms/) and [surface curvature](/surface-curvature/)), and $H = (\kappa_1 + \kappa_2)/2$, $K = \kappa_1 \kappa_2$.

1. **Same tangent plane.** $N_u$ and $N_v$ are perpendicular to $N$, since $N \cdot N = 1$. So $O_u = S_u + d N_u$ and $O_v = S_v + d N_v$ lie in the tangent plane of $S$, and $O_d$ has the normal $\pm N$ wherever it is regular.
2. **The area factor.** $O_u \times O_v = (1 - 2Hd + Kd^2) \, (S_u \times S_v) = (1 - d\kappa_1)(1 - d\kappa_2) \, (S_u \times S_v)$. So $O_d$ is regular exactly where $d \ne 1/\kappa_1$ and $d \ne 1/\kappa_2$. Its normal is $+N$ where the factor is positive and $-N$ where it is negative.
3. **Curvatures of the offset.** At a regular point, $O_d$ has the same principal directions as $S$ and the principal curvatures $\kappa_i / (1 - d\kappa_i)$, equivalently the principal radii $1/\kappa_i - d$.

So the offset is regular for all $|d| < \rho_{\min}$, where $\rho_{\min}$ is the smallest principal radius of curvature $1/|\kappa_i|$ over the surface. Past a radius of curvature, the factor in fact 2 changes sign, the offset turns over along a cusp edge, and it intersects itself. A second kind of self-intersection is global: two points of $S$ that are far apart along the surface but close in space give offset points that meet. Both kinds must be removed to get the *trimmed offset*, the part of $O_d$ whose points are at distance exactly $|d|$ from $S$. The trimmed offset of a closed surface is a level set of the unsigned distance to $S$, which for the boundary of a solid is a level set of the [signed distance function](/signed-distance-function/).

**Rationality.** If $S$ is polynomial or rational, $S_u \times S_v$ is polynomial or rational, but its length is the square root of a polynomial, and in general $O_d$ is not rational. The exceptions include planes, spheres, circular cylinders and cones, and tori, whose offsets are surfaces of the same type, and the surfaces with a rational unit normal, the analog of Pythagorean hodograph curves.

## Examples and non-examples

- **A plane.** $S(u, v) = (u, v, 0)$ has $N = (0, 0, 1)$, both curvatures $0$, and $O_d(u, v) = (u, v, d)$. Every offset is regular.
- **A sphere.** The sphere of radius $R$ with the outward normal has $\kappa_1 = \kappa_2 = -1/R$ in the convention above. The factor is $(1 + d/R)^2$ and the offset is the sphere of radius $R + d$. At $d = -R$ the whole offset collapses to the center, and for $d < -R$ it is the sphere of radius $|R + d|$ with the normal turned inward.
- **A cylinder.** The cylinder of radius $R$ has the radii $R$ around the axis and $\infty$ along it. The offset is the coaxial cylinder of radius $R + d$, which collapses to the axis at $d = -R$.
- **A torus.** The torus with axis radius $R$ and tube radius $r < R$ offsets to the torus with radii $R$ and $r + d$. At $d = -r$ the tube collapses to its core circle.
- **A paraboloid.** $z = (x^2 + y^2)/2$ with the upward normal has both principal radii equal to $1$ at the origin, with the centers of curvature above the surface. The offset with $d > 1$ has a fold near the axis: the points of the offset near $x = y = 0$ come from a ring of surface points and overlap. A ball of radius $d > 1$ cannot touch the inside of the paraboloid at its bottom point. This is the case of a ball-end cutter that is too large for a concave region.
- **A bicubic patch.** The offset of a general bicubic patch is not a polynomial or rational surface. It is approximated, for example by fitting bicubic patches to sampled offset points and checking the error, as Farouki did.

Non-examples:

- **A surface with a crease.** At an edge where two faces meet at an angle, the normal jumps. The two face offsets leave a gap on the convex side and overlap on the concave side. The offset of a solid with edges fills the gap with a piece of a cylinder around the edge, which is not an offset surface of either face; see [solid offsetting](/solid-offsetting/).
- **A displacement by a non-unit normal.** $S + d \, (S_u \times S_v)$ is rational, but its points are not at a constant distance from $S$, so it is not an offset.

## Related definitions

- The [offset curve](/offset-curve/) is the same construction for a plane curve, and [curve offsetting](/curve-offsetting/) is its approximation problem. The surface case has two radii of curvature per point instead of one.
- [Solid offsetting](/solid-offsetting/) grows or shrinks a solid by a distance $r$. Its boundary consists of trimmed offsets of the faces and of pieces around the edges and vertices, which the [Rossignac and Requicha method](/rossignac-requicha-offsetting/) builds from a CSG tree.
- The spine of a [rolling-ball blend](/rolling-ball-blend/) of radius $r$ is the intersection of the offsets at distance $r$ of the two surfaces.
- The cutter location surface of a ball-end mill of radius $r$ is the offset of the part surface at distance $r$; see [cutter location data](/cutter-location-data/).
- The self-intersections of offsets occur near the [medial axis](/medial-axis/): the global self-intersections of the inward offset at distance $d$ lie on the medial axis, at the centers of the balls of radius $d$ inside the solid that touch its boundary at two or more points.

## References
