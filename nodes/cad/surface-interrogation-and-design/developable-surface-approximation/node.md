---
tag: 7B7JZD
kind: problem
slug: developable-surface-approximation
name: Developable surface approximation
aliases:
- developable approximation
area: cad/surface-interrogation-and-design
level: advanced
summary: Approximate a surface or a pair of boundary curves by developable patches, for sheet metal, ship hulls and garments, by dual plane methods or optimisation.
prereqs: [developable-surface, ruled-surface]
see_also: [flat-pattern-development, mesh-segmentation, mesh-parameterization, angle-based-flattening, least-squares-conformal-maps, discrete-gaussian-curvature, minkowski-sum, gauss-newton-algorithm]
sources:
  - book: isbn:9783540420583
    title: Helmut Pottmann and Johannes Wallner, Computational Line Geometry, Springer, 2001
    locator: Chapter 6, Developable Surfaces (the dual representation, approximation by developable surfaces, and developable surfaces through given curves)
  - paper: "Helmut Pottmann and Johannes Wallner, Approximation algorithms for developable surfaces, Computer Aided Geometric Design 16(6), 539 to 556, 1999"
    title: Pottmann and Wallner 1999
    locator: a metric on the space of planes and linear approximation algorithms for developable NURBS surfaces in the dual form
  - paper: doi:10.1006/gmip.1999.0487
    title: "Hong-Yi Chen, In-Kwon Lee, Stefan Leopoldseder, Helmut Pottmann, Thomas Randrup and Johannes Wallner, On surface approximation using developable surfaces, Graphical Models and Image Processing 61(2), 1999"
    locator: pp. 110 to 124 (approximating a given surface by developable strips through its tangent planes)
  - paper: doi:10.1111/j.1467-8659.2005.00883.x
    title: "Dan Julius, Vladislav Kraevoy and Alla Sheffer, D-Charts: quasi-developable mesh segmentation, Computer Graphics Forum 24(3), 2005"
    locator: pp. 581 to 590 (segmenting a mesh into charts that are close to cones and cylinders)
  - paper: doi:10.1145/2832906
    title: "Chengcheng Tang, Pengbo Bo, Johannes Wallner and Helmut Pottmann, Interactive design of developable surfaces, ACM Transactions on Graphics 35(2), 2016"
    locator: article 12 (developable B-spline strips designed by constrained optimisation)
  - paper: doi:10.1145/3197517.3201303
    title: "Oded Stein, Eitan Grinspun and Keenan Crane, Developability of triangle meshes, ACM Transactions on Graphics 37(4), 2018"
    locator: article 77 (a vertex star energy whose minimisers are piecewise developable meshes)
---

Developable surface approximation asks for a [developable surface](/developable-surface/), or a few developable patches, that is close to a given shape: a designed surface, a scanned point cloud, or a pair of boundary curves. The output can then be made by bending flat sheet without stretching, which is how sheet metal ducts, ship hull plates, garment panels and paper or plywood models are built. A developable surface depends on functions of one variable, a general surface on functions of two, so the problem is always a compromise between closeness, the number of pieces, and fairness.

## In plain words

A flat sheet of metal can be rolled into a cylinder or a cone, or twisted into more interesting shapes, but it cannot be pressed onto a ball without wrinkles or stretching. If a designer draws a curved shape and wants to make it from sheets, the shape has to be changed a little so that every piece is one of the shapes a sheet can take. The task is to find these pieces: few of them, close to the drawing, and smooth. Sometimes the input is only two curves, such as the square opening of a duct and the round pipe it must meet, and the task is to find a sheet surface that spans between them.

## Definition

This page uses, for a surface with parametrization $r$, the unit normal $n = r_u \times r_v / |r_u \times r_v|$ and the mean curvature $H = (k_1 + k_2)/2$ for this $n$; only $K = k_1 k_2$, which does not depend on the sign of $n$, enters the statements below.

**Input.** One of:

- a target surface $\Phi$, as a parametric patch or a triangle mesh, or a point set $p_1, \dots, p_m$ sampled from it;
- two boundary curves $c_0(t)$ and $c_1(s)$;

and a tolerance $\varepsilon \ge 0$, or weights for closeness and fairness.

**Output.** A developable surface $D$, or developable patches $D_1, \dots, D_k$ that meet along curves with a prescribed continuity, such that:

- **Approximation.** The distance from $\Phi$ (or from each $p_i$) to $\bigcup D_j$ is at most $\varepsilon$, or a weighted sum of squared distances plus a fairness term is minimal. In the segmentation form, the number $k$ of patches is to be small for a given $\varepsilon$.
- **Interpolation.** $D$ is a developable strip whose rulings join a point of $c_0$ to a point of $c_1$.

Developable means $K = 0$ at every regular point. Away from planar points, $D$ is then a ruled surface $a(u) + v\, w(u)$ with $\det(a', w, w') = 0$, whose tangent plane is fixed along each ruling (see [ruled surface](/ruled-surface/) and [developable surface](/developable-surface/)). The output must also avoid the singular curve of the surface, its edge of regression, inside the region that is used.

## Variants

- **One patch, least squares.** Fit a single developable patch to a surface strip or to points, minimizing the sum of squared distances.
- **Segmentation.** Cover a surface or mesh by the fewest patches within tolerance $\varepsilon$, each close to a developable surface, with seams between them (Julius, Kraevoy and Sheffer 2005).
- **Developable lofting.** Interpolate two given boundary curves by a developable strip, as for ship hull plates and sheet metal transition pieces.
- **Discrete developability.** Change a triangle mesh as little as possible so that it becomes piecewise developable, with an angle sum of $2\pi$ at the interior vertices of each piece or straight rulings through each vertex star (Stein, Grinspun and Crane 2018); see [discrete Gaussian curvature](/discrete-gaussian-curvature/).
- **Design.** Edit a developable B-spline surface interactively while keeping it developable, by solving the developability constraints again after each edit (Tang, Bo, Wallner and Pottmann 2016).
- **Curved folding.** Allow creases along curves between developable pieces, so that a single sheet makes a sharper shape.

## Examples

### Globe gores

Approximate the sphere of radius $R$ by $n$ strips, one per range of longitude of width $2\varphi = 2\pi/n$, each strip a piece of the cylinder of radius $R$ that touches the sphere along the middle meridian. A point at latitude $\psi$ and longitude offset $\lambda$ from the middle meridian is at distance $R \sqrt{1 - \cos^2 \psi \sin^2 \lambda}$ from the cylinder axis, so its distance to the cylinder is

$$R \left(1 - \sqrt{1 - \cos^2 \psi \sin^2 \lambda}\right) \le R (1 - \cos \varphi),$$

with equality at the equator on the edge of the strip. For $n = 12$ and $R = 1$ the error is $1 - \cos 15° \approx 0.0341$. The cylinder of radius $R - R(1 - \cos \varphi)/2$ on the same axis is secant: it halves the error to $\approx 0.0170$, since all the distances to the axis lie in $[R \cos \varphi, R]$. Each strip unrolls into a gore, a lens of length $\pi R$ and greatest width $2 R \sin \varphi \approx 0.518$. For a globe of radius $150$ mm and a tolerance of $1$ mm, $n \ge \pi / \arccos(1 - 1/150) \approx 27.2$, so $28$ tangent strips are needed, or $20$ secant ones, from $n \ge \pi / \arccos(1 - 2/150) \approx 19.2$.

### A square to round transition

Join the square $[-1, 1]^2$ in the plane $z = 0$ to the circle of radius $1/2$ about the $z$ axis in the plane $z = 1$. For two curves in parallel planes, a ruling from $c_0(t)$ to $c_1(s)$ of a developable strip needs $c_0'(t)$ parallel to $c_1'(s)$: both tangents are horizontal, so if they were independent they would span the horizontal plane, and the tangent plane along the ruling, which contains them and the non-horizontal ruling, would be all of space. Matching equal tangent directions on the two convex curves, oriented the same way, gives the side surface of the convex hull of the two curves:

- each side of the square, such as $y = -1$ with direction $(1, 0)$, is matched to one circle point, here $(0, -1/2, 1)$, and spans a planar triangle with sides $2$, $3/2$ and $3/2$, base angles $48.19°$ and apex angle $83.62°$;
- each corner of the square turns through $90°$, so it is matched to a quarter circle and is the apex of a cone. From the corner $(1, -1, 0)$ the rulings to the arc have lengths from $3/2$ at the ends down to $1.3549$ in the middle, and the cone unrolls into a fan of angle $0.5075$ rad $= 29.08°$, the length of the spherical curve of ruling directions.

The tangent plane of a triangle is the tangent plane of the neighbouring cone along their common ruling, because the circle tangent at the shared point is parallel to the square side, so the surface is tangent continuous. Cutting along one slanted edge and laying out the four triangles and four fans in turn gives the flat pattern, whose curved edge has length $4 \cdot \pi/4 = \pi$, the circumference of the circle.

### Two skew segments

Let $c_0(t) = (t, 0, 0)$ and $c_1(s) = (0, 1, s)$. Then $\det(c_0', c_1(s) - c_0(t), c_1') = \det((1, 0, 0), (-t, 1, s), (0, 0, 1)) = 1$ for all $t$ and $s$, so no developable strip has its rulings joining the two segments. The straight-line surface between them is a hyperbolic paraboloid, with $K < 0$, and a sheet cannot span them without stretching or extra boundary.

## Known algorithms

- **Dual fitting.** Write a non-vertical plane as $z = u_0 + u_1 x + u_2 y$, a point $U = (u_0, u_1, u_2)$ of the space of planes. Every curve $U(t)$ with $(u_1', u_2') \ne 0$ is a developable surface: the envelope of its planes, ruled by the lines $\Pi(t) \cap \Pi'(t)$, where $\Pi'(t)$ is the vertical plane $u_0' + u_1' x + u_2' y = 0$. A metric on planes is $d(U, V)^2 = \int_\Omega (\Delta u_0 + \Delta u_1 x + \Delta u_2 y)^2\, dx\, dy$ over a region $\Omega$ of interest, a positive definite quadratic form in $\Delta U = U - V$. Given target tangent planes $V_i$ with parameters $t_i$, choose $U(t)$ as a [B-spline](/b-spline/) curve and minimize $\sum_i d(U(t_i), V_i)^2$ plus a fairness term. This is a linear least squares problem in the control planes, and every solution is developable (Pottmann and Wallner 1999; Chen et al. 1999). The rulings and the edge of regression are then computed from $U$, $U'$ and $U''$, and the used region is trimmed away from the edge of regression.
- **Primal ruled patches.** Write $D$ as a ruled Bézier or B-spline patch of degree $(m, 1)$ between curves $a$ and $b$, and impose $\det(a', b - a, b' - a') = 0$. With $w = b - a$ of degree $m$, the determinant is a polynomial in $u$ of degree at most $3m - 3$: the top term $\det(m A_m, W_m, m W_m)$ of degree $3m - 2$ vanishes because $W_m$ appears twice. So developability is $3m - 2$ cubic equations in the control points, a nonlinear constraint handled by Newton steps or by optimisation.
- **Penalty optimisation.** Minimize the distance to the target plus $\mu$ times the squared determinants at sample parameters, plus fairness, with the [Gauss-Newton algorithm](/gauss-newton-algorithm/) or another [nonlinear least squares](/nonlinear-least-squares/) method, raising $\mu$ until the developability error is within tolerance. The result is developable only up to that tolerance.
- **Developable lofting.** The rulings between $c_0$ and $c_1$ are the pairs on the zero set of $f(t, s) = \det(c_0'(t), c_1(s) - c_0(t), c_1'(s))$. On a branch $(t(\tau), s(\tau))$ of $f = 0$ the strip $(1 - v)\, c_0(t) + v\, c_1(s)$ has $\det(a', w, w') = t' s' f = 0$, so it is developable where it is regular. The branch is traced in the $(t, s)$ square from $(0, 0)$ to $(1, 1)$, for example by [marching squares](/marching-squares/) on a grid. If no branch connects the corners, as in the skew example where $f$ has no zeros, the curves bound no developable strip of this form.
- **Curves in parallel planes.** For convex polygons in parallel planes, the matching of equal edge directions is a merge of the two sorted lists of edge directions, as in the [Minkowski sum](/minkowski-sum/) of convex polygons, and takes time linear in the number of edges. It gives the triangles and cones of the side of the convex hull.
- **Segmentation.** D-charts grows charts on a mesh whose normals lie close to a circle on the unit sphere, the Gauss image of a cone or cylinder, and merges and splits charts to keep the developability error below a bound (Julius, Kraevoy and Sheffer 2005). See [mesh segmentation](/mesh-segmentation/).
- **Discrete developability.** Gradient descent on an energy over vertex stars, which is zero when the triangles around a vertex form a hinge, two planar pieces meeting along a straight line, drives a mesh to piecewise developable form with straight rulings (Stein, Grinspun and Crane 2018). The result is then flattened by [mesh parameterization](/mesh-parameterization/), for example [angle based flattening](/angle-based-flattening/) or [least squares conformal maps](/least-squares-conformal-maps/), with near zero distortion.

## Bounds

- **No exact fit.** If the target has $K \ne 0$ at a point, no developable surface agrees with it on a neighbourhood of that point (Theorem 1 of [developable surface](/developable-surface/)). So the error is positive unless the target is itself developable.
- **A lower bound near an elliptic point.** Let $\Phi$ have $K > 0$ at $p$, with the normal chosen so that $0 < k_2 \le k_1$, and let $D$ be a developable surface through $p$ and tangent to $\Phi$ there, a graph over the tangent plane on the disc of radius $r$ about $p$. Then some point of $D$ is at distance at least $\tfrac12 k_2 r^2 (1 - O(r))$ from $\Phi$.

  *Proof.* In principal coordinates over the tangent plane, $\Phi$ is $z = \phi(x, y) = \frac12 (k_1 x^2 + k_2 y^2) + O(r^3)$ and $D$ is $z = \psi(x, y) = \frac12 q(x, y) + O(r^3)$, where $q$ is the Hessian form of $\psi$ at $0$. Since $\nabla \psi(0) = 0$, $K_D(p) = \det \operatorname{Hess} \psi(0)$, which is $0$, so $q = \lambda (x \cos \theta + y \sin \theta)^2$ for some $\lambda$ and $\theta$. In the direction $e = (-\sin \theta, \cos \theta)$, $q(e) = 0$ and $\psi(r e) - \phi(r e) = -\frac12 (k_1 \sin^2 \theta + k_2 \cos^2 \theta)\, r^2 + O(r^3)$, of absolute value at least $\frac12 k_2 r^2 - O(r^3)$. On the disc of radius $2r$, $|\nabla \phi| \le L = O(r)$, and for a point $x$ of that disc, $|z_0 - \phi(x_0)| \le |z_0 - \phi(x)| + L |x - x_0| \le \sqrt{1 + L^2}\, |(x, \phi(x)) - (x_0, z_0)|$ by Cauchy and Schwarz. The nearest point of $\Phi$ to $(r e, \psi(r e))$ is within $O(r^2)$ of it, so it is in that disc, and the distance is at least $\frac12 k_2 r^2 - O(r^3)$. $\square$

  For the sphere, $k_2 = 1/R$, so a tangent strip of half width $r$ has error at least $r^2/(2R) - O(r^3)$. A gore has $r = R \sin \varphi$ and error $R (1 - \cos \varphi) = R \sin^2 \varphi / (1 + \cos \varphi)$, so the gores meet this bound to leading order, and the number of tangent strips for tolerance $\varepsilon$ grows like $\pi \sqrt{R / (2\varepsilon)}$.
- **Cost of dual fitting.** With $m$ target planes and a B-spline curve of planes of degree $k$ with $N$ control planes, each sample touches $k + 1$ control planes, the normal equations are banded with $O(k)$ bandwidth, and the fit costs $O(m k^2 + N k^2)$ arithmetic operations.
- **Segmentation.** The methods for the fewest patches within a tolerance are heuristics; we know of no algorithm with a guarantee on the number of patches.

## Reductions

- **Developable fitting to curve fitting.** In the dual form, fitting a developable surface is fitting a curve in the three-dimensional space of planes, a linear least squares problem for a fixed parametrization.
- **Lofting to curve tracing.** Developable lofting between two curves reduces to tracing the plane curve $f(t, s) = 0$ in the parameter square, and for convex curves in parallel planes to merging two sorted sequences of tangent directions.
- **Flattening.** Once the patches are developable, the flat pattern is computed by the explicit development along rulings on the [developable surface](/developable-surface/) page, or, for meshes, by a parameterization with low distortion. For sheet metal parts with flat faces and cylindrical bends, see [flat pattern development](/flat-pattern-development/).

## Applications

- **Sheet metal.** Ducts, hoppers and transition pieces such as the square to round example are developable strips between two boundary curves, cut flat and rolled.
- **Ship hulls.** Plates of single curvature can be rolled cold, while plates of double curvature need slow forming such as line heating. Designing the hull, or each plate, as nearly developable reduces this work.
- **Garments, shoes and upholstery.** Panels of cloth or leather are cut flat, so the pattern pieces of a fitted shape are developable approximations of it, with seams and darts at the segmentation boundaries. Cloth can shear a little, so the tolerance there is larger than for metal.
- **Architecture and paper craft.** Façades of bent metal or glass panels, plywood and curved folded paper are designed as developable or piecewise developable surfaces, and globes are printed on gores.

## References
