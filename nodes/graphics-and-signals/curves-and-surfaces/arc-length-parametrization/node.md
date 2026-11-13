---
tag: ZB4VYJ
kind: concept
slug: arc-length-parametrization
name: Arc-length parametrization
aliases:
- unit-speed parametrization
area: graphics-and-signals/curves-and-surfaces
level: advanced
summary: Reparametrize a curve by the distance travelled along it, so that it has unit speed. For most curves this has no closed form and is computed by quadrature and root finding.
prereqs: [parametric-curve, gauss-legendre-quadrature, newton-raphson-method]
see_also: [adaptive-quadrature, gaussian-quadrature, newton-bisection-hybrid, frenet-frame, parametric-continuity, curve-evaluation, offset-curve, curve-interpolation]
sources:
  - paper: doi:10.1109/38.55155
    title: Brian Guenter and Richard Parent, Computing the arc length of parametric curves, IEEE Computer Graphics and Applications 10(3), 72-78 (1990)
    locator: arc length by adaptive Gaussian quadrature, a table of lengths, and the inverse by Newton iteration
  - book: isbn:9780132125895
    title: Manfredo P. do Carmo, Differential Geometry of Curves and Surfaces, Prentice-Hall, 1976
    locator: Section 1-3, Regular Curves; Arc Length (and the reparametrization by arc length)
  - book: isbn:9781558607378
    title: Gerald Farin, Curves and Surfaces for CAGD, A Practical Guide, fifth edition, Morgan Kaufmann, 2002
    locator: Chapter 10, W. Boehm, Differential Geometry I (arc length and the arc-length parameter)
---

The arc-length parametrization of a regular [parametric curve](/parametric-curve/) $C(t)$ uses as its parameter the distance $s$ travelled along the curve from a fixed start point. The arc length function $s(t) = \int_a^t \lVert C'(x) \rVert \, dx$ is strictly increasing, so it has an inverse $t(s)$, and the curve $\tilde C(s) = C(t(s))$ has the same trace with unit speed. Equal steps in $s$ then give equal distances along the curve, which is what an animation with constant speed, a dashed line or a machine tool at a fixed feed rate needs. The geometry of curves is written in this parameter: curvature, torsion and the [Frenet frame](/frenet-frame/) are derivatives with respect to $s$, and $G^k$ [continuity](/parametric-continuity/) is $C^k$ continuity in $s$. For the curves of CAD the parametrization is not available in closed form. The integral of the speed of a general cubic has no elementary closed form, and no polynomial curve other than a line has unit speed. So $s(t)$ is computed by [Gauss-Legendre quadrature](/gauss-legendre-quadrature/) with adaptive subdivision to a stated tolerance, and $t(s)$ by [Newton's method](/newton-raphson-method/) with a bisection safeguard.

## In plain words

A curve given by a formula is usually traced at a speed that changes. In some places a small step of the parameter moves far along the curve, in other places it hardly moves. Objects placed at equal parameter steps bunch up in some parts and spread out in others.

The fix is to measure the curve by distance. You ask for the point that lies a given distance along the curve, and you use that distance as the parameter. Then equal steps are equal lengths, and a point that moves with the parameter moves at constant speed.

For almost every curve used in practice, no simple formula gives the length. A program adds it up piece by piece until the answer is good enough. To go from a length back to a point, it guesses a point and corrects the guess a few times.

## The idea

**Arc length.** Let $C : [a, b] \to \mathbb{R}^d$ be continuously differentiable. Its arc length from $a$ to $t$ is

$$s(t) = \int_a^t \lVert C'(x) \rVert \, dx ,$$

the limit of the lengths of inscribed polygons as the vertices get dense. The length does not depend on the parametrization: for $\tilde C = C \circ \varphi$ with $\varphi' > 0$, the substitution rule gives the same integral.

**The inverse.** If the curve is regular, $s'(t) = \lVert C'(t) \rVert > 0$, so $s$ is a strictly increasing continuously differentiable bijection from $[a, b]$ onto $[0, L]$, and its inverse $t(s)$ has $t'(s) = 1 / \lVert C'(t(s)) \rVert$. The curve $\tilde C(s) = C(t(s))$ satisfies

$$\tilde C'(s) = C'(t(s))\, t'(s) = \frac{C'(t(s))}{\lVert C'(t(s)) \rVert}, \qquad \lVert \tilde C'(s) \rVert = 1 .$$

Any unit-speed parametrization of the same oriented trace differs from this one by a shift $s \mapsto s + c$, and by $s \mapsto -s$ if the orientation is reversed.

**No polynomial unit speed.** If $C$ is a polynomial curve with $\lVert C'(t) \rVert = 1$ for all $t$, then $C$ is a line. Proof: $C'$ is a polynomial curve with $\lVert C' \rVert^2 = 1$. If its largest coordinate degree $k$ were at least 1, the coefficient of $t^{2k}$ in $\lVert C' \rVert^2$ would be the sum of the squares of the leading coefficients, which is positive, but $\lVert C' \rVert^2$ is constant. So $C'$ is constant and $C$ is a line. Hence the arc-length parametrization of a polynomial spline is never polynomial, except for straight pieces, and must be approximated.

**No closed form for the length.** For a quadratic curve the speed is the square root of a quadratic in $t$, and its integral has a closed form with a square root and $\operatorname{asinh}$, as for the parabola below. For a cubic the speed is the square root of a polynomial of degree 4, and the integral is an elliptic integral, not elementary in general. The exception is the class of Pythagorean-hodograph curves, whose speed is a polynomial by construction, so $s(t)$ is a polynomial; even then $t(s)$ is not.

**Computing $s(t)$.** The $n$-point Gauss-Legendre rule is exact for polynomials of degree $2n - 1$. The speed is not a polynomial, but it is smooth where $C' \ne 0$, so the rule converges fast on short intervals. The adaptive scheme of Guenter and Parent (1990) applies the rule on an interval and on its two halves. It accepts the halves if the two results differ by at most the tolerance $\varepsilon$, and otherwise splits both halves with tolerance $\varepsilon / 2$. The accepted pieces form a table of breakpoints $t_k$ and cumulative lengths $s_k$. The difference of the two results is an estimate of the error, not a proven bound: a curve with a feature that the nodes miss can pass the test. Near a zero of the speed the integrand has a kink, and the scheme subdivides there.

**Computing $t(s)$.** Given $s^\ast$, find the piece $[t_k, t_{k+1}]$ with $s_k \le s^\ast < s_{k+1}$ by binary search in the table, and solve $g(t) = s_k + \int_{t_k}^t \lVert C' \rVert - s^\ast = 0$. Here $g'(t) = \lVert C'(t) \rVert$, so a Newton step is $t \leftarrow t - g(t) / \lVert C'(t) \rVert$. Each evaluation of $g$ is one Gauss rule on a sub-interval. The current point and the sign of $g$ keep a bracket. If a Newton step leaves the bracket, or the speed is zero, take the bisection step instead, so the iteration always converges. Where the curve is regular, Newton converges quadratically and needs two to four steps from a linear interpolation in the table.

**Cheaper approximations.** A dense table of chord lengths with linear interpolation gives $t(s)$ with an error of order $h^2$ for a step $h$, which is often enough for drawing. An animation system can also fit a spline to the samples of $s \mapsto t$ once and evaluate it at run time.

The implementation computes Gauss-Legendre nodes by Newton's method on the Legendre polynomials, the adaptive table, and the safeguarded inverse. Its tests compare with the closed forms for the circle, the helix, the parabola and the cusp $(t^2, t^3)$, and with a composite Simpson rule on 4000 intervals for random cubic Bézier curves.

## Examples

**Circle and helix.** For $C(t) = (r \cos t, r \sin t)$ the speed is $r$, so $s = rt$ and $\tilde C(s) = (r \cos(s / r), r \sin(s / r))$. For the helix $(a \cos t, a \sin t, bt)$ the speed is $\sqrt{a^2 + b^2}$ and $s = t \sqrt{a^2 + b^2}$. Every curve with constant speed is a scaled arc-length parametrization.

**Parabola.** For $C(t) = (t, t^2)$ the speed is $\sqrt{1 + 4t^2}$ and

$$s(t) = \frac{t \sqrt{1 + 4t^2}}{2} + \frac{\operatorname{asinh}(2t)}{4} .$$

The length has a closed form, but the inverse $t(s)$ does not, so even here the parameter at a given length is found numerically.

**A cubic.** For $C(t) = (t, t^3)$ on $[0, 1]$ the speed is $\sqrt{1 + 9t^4}$, and the length is $L = 1.547866$. Equal parameter steps of $1/4$ give pieces of length $0.250875$, $0.275393$, $0.390589$ and $0.631009$: the last piece is 2.5 times as long as the first. The points that cut the curve into four pieces of equal length $L/4$ are at $t = 0.380009$, $0.671363$ and $0.861289$. The accuracy of a single Gauss-Legendre rule on all of $[0, 1]$, and of the adaptive 5-point scheme, is:

| method | pieces | error |
|---|---|---|
| 1-point rule | 1 | $3.0 \times 10^{-1}$ |
| 3-point rule | 1 | $1.9 \times 10^{-3}$ |
| 5-point rule | 1 | $2.5 \times 10^{-5}$ |
| 8-point rule | 1 | $5.2 \times 10^{-8}$ |
| adaptive, $\varepsilon = 10^{-4}$ | 2 | $4.4 \times 10^{-8}$ |
| adaptive, $\varepsilon = 10^{-6}$ | 4 | $2.4 \times 10^{-11}$ |
| adaptive, $\varepsilon = 10^{-8}$ | 8 | $7.7 \times 10^{-16}$ |

The actual error is far below the tolerance here, because the test compares a 5-point rule with two 5-point rules, and the finer result is much better than the estimate suggests.

**A cusp.** $C(t) = (t^2, t^3)$ on $[-1, 1]$ has speed $|t| \sqrt{4 + 9t^2}$, zero at $t = 0$, and length $2(13^{3/2} - 8)/27 = 2.879420$. One 5-point rule on $[-1, 1]$ has error $0.105$, because the speed has a kink at 0. The adaptive scheme splits at $t = 0$ in its first step, and with $\varepsilon = 10^{-4}$ it uses 4 pieces and has an error of $1.2 \times 10^{-11}$. The inverse $t(s)$ still exists, since $s$ is strictly increasing, but $\tilde C$ is not regular at the cusp: its unit tangent turns by $180°$ there.

**A slow start.** The segment $C(t) = (1 - t^2)A + t^2 B$ has zero speed at $t = 0$. Its arc-length parametrization is $\tilde C(s) = A + s \,(B - A)/\lVert B - A \rVert$, the uniform motion along the segment. Reparametrizing by arc length removes the effect of the parametrization and keeps only the trace.

## Where it is used

- Animation and camera paths: an object moves along a spline at a speed given by an easing curve $s(\text{time})$, which needs $t(s)$ at every frame (Guenter and Parent 1990).
- Machining and robotics: a tool moves at a fixed feed rate along the path, which is a condition on $ds/d(\text{time})$. Pythagorean-hodograph curves are used here because their $s(t)$ is a polynomial.
- Drawing: dashed and dotted strokes, text along a path and evenly spaced markers.
- Resampling: points at equal arc length along a curve, as input for [curve simplification](/curve-simplification/) or for comparing two shapes.
- Differential geometry: the curvature, the torsion and the [Frenet frame](/frenet-frame/) are defined with derivatives in $s$, and the arc-length form of the [offset curve](/offset-curve/) and of $G^k$ continuity uses it.
- Parameter choice for [curve interpolation](/curve-interpolation/): chord-length parameters approximate the arc length of the curve that will be built.

## References
