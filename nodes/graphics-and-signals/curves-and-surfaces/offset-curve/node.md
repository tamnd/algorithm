---
tag: CF6X62
kind: definition
slug: offset-curve
name: Offset curve
aliases:
- parallel curve
area: graphics-and-signals/curves-and-surfaces
level: advanced
summary: The curve traced by the points at a fixed signed distance along the normals of a plane curve. It has cusps where the distance equals the radius of curvature, and is rarely polynomial.
prereqs: [parametric-curve, frenet-frame]
see_also: [curve-offsetting, minkowski-sum, medial-axis, straight-skeleton, arc-length-parametrization, parametric-continuity, nurbs, rational-bezier-curve]
sources:
  - paper: doi:10.1016/0167-8396(90)90023-K
    title: Rida T. Farouki and C. Andrew Neff, Analytic properties of plane offset curves, Computer Aided Geometric Design 7(1-4), 83-99 (1990)
    locator: the irregular points where the curvature is -1/d, their relation to the evolute, self-intersections and trimming
  - paper: doi:10.1016/0167-8396(90)90024-L
    title: Rida T. Farouki and C. Andrew Neff, Algebraic properties of plane offset curves, Computer Aided Geometric Design 7(1-4), 101-127 (1990)
    locator: the implicit equation and the degree of the offset of polynomial and rational curves
  - paper: doi:10.1147/rd.345.0736
    title: Rida T. Farouki and Takis Sakkalis, Pythagorean hodographs, IBM Journal of Research and Development 34(5), 736-752 (1990)
    locator: polynomial curves with polynomial speed, whose offsets are rational
---

The offset curve of a regular plane [parametric curve](/parametric-curve/) $C(t)$ at the signed distance $d$ is the curve

$$C_d(t) = C(t) + d\, N(t),$$

where $N$ is the unit normal. Each point moves by $d$ along the normal, so for small $|d|$ the offset is the curve parallel to $C$ at distance $|d|$ on one side. Offsets give the path of the center of a round cutter of radius $|d|$ that follows a contour, the outline of a stroke of width $2|d|$ drawn along a path, and the tolerance band around a part. The curve has two properties that make it hard to use in CAD. First, the offset of a polynomial or rational curve is not polynomial or rational in general, because $N$ contains the square root $\lVert C' \rVert$. So a CAD system cannot store it exactly as a [NURBS](/nurbs/) curve and stores an approximation instead (see [curve offsetting](/curve-offsetting/)). The exceptions are lines, circles and the Pythagorean-hodograph curves of Farouki and Sakkalis (1990). Second, on the concave side the offset has a cusp at every point where $d$ equals the radius of curvature. Where $d$ is larger, the offset runs backwards and makes loops, and these loops must be trimmed away to get the set of points at distance $|d|$ from the curve.

## Definition

**Normal and signed curvature.** Let $C(t) = (x(t), y(t))$ be regular and twice continuously differentiable. Let $T = C' / \lVert C' \rVert$ and let $N$ be $T$ turned by $+90°$, so $N = (-y', x') / \lVert C' \rVert$, which points to the left of the direction of travel. The signed curvature is

$$k = \frac{x' y'' - y' x''}{\lVert C' \rVert^3},$$

positive where the curve turns left. Then $N' = -k \lVert C' \rVert\, T$, the planar case of the [Frenet-Serret formulas](/frenet-frame/). In the plane this normal exists at every regular point, also where $k = 0$, so the failure of the space-curve frame at inflections does not occur.

**Offset curve.** For a real number $d$, the offset at distance $d$ is $C_d(t) = C(t) + d N(t)$. $d > 0$ offsets to the left and $d < 0$ to the right. The offset of a closed curve traversed counterclockwise with $d > 0$ is an inner offset.

**Derivative and regularity.** Differentiating with $N' = -k \lVert C' \rVert T$ gives

$$C_d'(t) = \bigl(1 - d\, k(t)\bigr)\, C'(t).$$

So the offset has the same tangent direction as $C$ at corresponding points, with its speed scaled by $|1 - dk|$. It is regular where $dk \ne 1$ and runs in the same direction as $C$ where $dk < 1$. Its signed curvature, in its own direction of travel, is

$$k_d = \frac{k}{|1 - d k|}.$$

**Irregular points.** Where $d\,k(t) = 1$, the offset speed is zero. At such a point $d = 1/k$ is the radius of curvature, and $C_d(t) = C + N/k$ is the center of curvature, a point of the evolute of $C$. If $dk - 1$ changes sign there, the offset reverses its direction of travel and has a cusp. If $k$ has a local extremum there, the sign does not change, and the point is instead an extraordinary point of the offset where the tangent is continuous and the curvature is infinite (Farouki and Neff 1990). Only the concave side, where $d$ and $k$ have the same sign, can have irregular points. An offset to the convex side, $dk \le 0$, is always regular, and its curvature is smaller than that of $C$ in absolute value.

**Global self-intersections.** An offset can cross itself also where it is regular, when two parts of $C$ that are far apart along the curve are closer than $2|d|$ in the plane. So the condition $|d| < 1/|k|$ everywhere prevents cusps but does not prevent loops. The set of all points at distance exactly $|d|$ from $C$ is the part of $C_d$ (together with the offset to the other side and, for an open curve, the arcs around the end points) that remains after the loops are trimmed. Its changes as $d$ grows are governed by the [medial axis](/medial-axis/) of the region. For a closed curve the trimmed outer offset is the boundary of the [Minkowski sum](/minkowski-sum/) of the region and a disc of radius $|d|$.

**Why the offset is not polynomial.** $N = (-y', x') / \sqrt{x'^2 + y'^2}$. If $C$ is a polynomial curve, $C_d$ is rational in $t$ for every $d$ if and only if $x'^2 + y'^2$ is the square of a polynomial $\sigma(t)$. These are the Pythagorean-hodograph (PH) curves. They can be built from two polynomials $u, v$ as $x' = u^2 - v^2$, $y' = 2uv$, with $\sigma = u^2 + v^2$. For every other polynomial curve the offset is not rational in $t$. Farouki and Neff (1990) show that the offset of a general polynomial curve of degree $n$ is an algebraic curve of degree $4n - 2$, so the offset of a parabola has degree 6 and the offset of a cubic has degree 10.

The implementation computes offset points, the derivative $(1 - dk) C'$, the offset curvature and the cusp parameters, and builds PH curves with exact rational offsets. Its tests check concentric circles, the distance and the derivative against finite differences on random cubics, the curvature formula on both sides of a cusp, the cusps of the parabola against the closed form, and the exact distance of PH offsets in rational arithmetic.

## Examples and non-examples

**Circle.** For the counterclockwise circle of radius $r$, $k = 1/r$ and $N$ points to the center, so $C_d$ is the circle of radius $r - d$ with the same center. For $d < r$ it has curvature $1/(r - d)$. At $d = r$ the whole offset collapses into the center, and for $d > r$ it is a circle of radius $d - r$ traversed backwards. Every point is irregular at once in the case $d = r$, because the curvature is constant.

**Parabola.** For $C(t) = (t, t^2)$, $k = 2 / (1 + 4t^2)^{3/2}$, largest at the vertex, where the radius of curvature is $1/2$. The offset toward the inside is

$$C_d(t) = \left(t - \frac{2dt}{\sqrt{1 + 4t^2}},\; t^2 + \frac{d}{\sqrt{1 + 4t^2}}\right),$$

which contains a square root and is not a rational function of $t$.

| $d$ | cusp parameters $t$ |
|---|---|
| $0.25$ | none |
| $0.5$ | $0$ (an extraordinary point, since $k$ is largest there) |
| $0.75$ | $\pm 0.27855$ |
| $1$ | $\pm 0.38321$ |
| $2$ | $\pm 0.61641$ |

For $d = 1$ the cusps are at $t = \pm \sqrt{(2^{2/3} - 1)/4} = \pm 0.38321$, at the points $(\mp 0.22510, 0.94055)$. Between them the offset runs backwards. The two outer branches cross each other on the axis at $t = \pm\sqrt3/2$, at the exact point $(0, 5/4)$, because $\sqrt{1 + 4t^2} = 2$ there. The part of the offset between $t = -\sqrt3/2$ and $t = \sqrt3/2$ is a swallowtail with two cusps, and trimming it leaves the curve of points at distance 1 above the parabola, with a corner at $(0, 5/4)$. Offsets to the outside, $d < 0$, have no cusps for any $|d|$.

**A PH cubic.** With $u = 1$ and $v = t$, $x' = 1 - t^2$, $y' = 2t$ and $\sigma = 1 + t^2$, so

$$C(t) = \left(t - \tfrac{t^3}{3},\; t^2\right), \qquad C_d(t) = \left(t - \tfrac{t^3}{3} - \frac{2dt}{1 + t^2},\; t^2 + d\,\frac{1 - t^2}{1 + t^2}\right),$$

a rational curve for every $d$. At $t = 1$, $d = 1$ it gives the exact point $(-1/3, 1)$. The curvature is $k = 2 / (1 + t^2)^2$, so for $d = 1$ the cusps are at $t = \pm\sqrt{\sqrt2 - 1} = \pm 0.64359$.

**Non-example: equal distance is not equal shape.** The offset of an ellipse is not an ellipse. It has degree 8, and for $d$ between the smallest and the largest radius of curvature it has four cusps on the inside. "Parallel" in the name means the normals are shared, not that the offset is a scaled copy.

**Non-example: a polygon.** A polygon has no normal at its vertices, so the definition does not apply directly. Its offset is defined through the Minkowski sum with a disc, which adds circular arcs at the convex vertices. The mitered version, which extends the edges instead, gives the [straight skeleton](/straight-skeleton/).

## Related definitions

- [Curve offsetting](/curve-offsetting/): the problem of computing an approximation to the offset in a given curve form, with trimming.
- [Frenet frame](/frenet-frame/): the normal and the curvature that define the offset and its cusps.
- [Minkowski sum](/minkowski-sum/): the trimmed outer offset of a closed curve bounds the sum of the region and a disc.
- [Medial axis](/medial-axis/): the locus of centers of maximal discs, where the trimmed offsets of a region change shape.
- [Straight skeleton](/straight-skeleton/): the polygon offset with mitered corners.
- [Rational Bézier curve](/rational-bezier-curve/) and [NURBS](/nurbs/): the forms that can hold a PH offset exactly.

## References
