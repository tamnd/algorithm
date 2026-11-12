---
tag: CY1Y34
kind: definition
slug: frenet-frame
name: Frenet-Serret frame
aliases:
- Frenet frame
- Frenet-Serret apparatus
area: graphics-and-signals/curves-and-surfaces
level: advanced
summary: The moving orthonormal frame of tangent, principal normal and binormal along a space curve, with its curvature and torsion. It is undefined where the curvature is zero.
prereqs: [parametric-curve, arc-length-parametrization]
see_also: [parametric-continuity, offset-curve, sweep-surface, surface-curvature, fundamental-forms, curve-evaluation, ruled-surface, hermite-spline]
sources:
  - book: isbn:9780132125895
    title: Manfredo P. do Carmo, Differential Geometry of Curves and Surfaces, Prentice-Hall, 1976
    locator: Section 1-5, The Local Theory of Curves Parametrized by Arc Length (the Frenet trihedron, curvature, torsion and the Frenet formulas)
  - paper: doi:10.2307/2319846
    title: Richard L. Bishop, There is more than one way to frame a curve, The American Mathematical Monthly 82(3), 246-251 (1975)
    locator: the relatively parallel (rotation-minimizing) frame, defined also where the curvature is zero
  - paper: doi:10.1145/1330511.1330513
    title: Wenping Wang, Bert Jüttler, Dayue Zheng and Yang Liu, Computation of rotation minimizing frames, ACM Transactions on Graphics 27(1), Article 2 (2008)
    locator: the double reflection method
---

The Frenet-Serret frame of a regular space curve $C(t)$ is the orthonormal frame $(T, N, B)$ that moves along the curve: $T$ is the unit tangent, $N$ the principal normal, which points toward the side where the curve bends, and $B = T \times N$ the binormal. Two numbers go with it. The curvature $\kappa \ge 0$ tells how fast $T$ turns, and the torsion $\tau$ tells how fast the curve leaves its osculating plane, the plane of $T$ and $N$. The Frenet-Serret formulas give the derivatives of the frame in terms of the frame itself, and by the fundamental theorem of curves the two functions $\kappa(s) > 0$ and $\tau(s)$ fix the curve up to a rigid motion. The frame was found by Frenet (thesis of 1847) and independently by Serret (1851). In graphics it orients objects that move along a path and the cross-sections of [sweep surfaces](/sweep-surface/). It has one known defect: $N$ is defined only where $\kappa \ne 0$. On straight pieces and at inflection points the frame does not exist, and on either side of an inflection it turns over by $180°$. For that reason graphics programs often use a rotation-minimizing frame instead, which Bishop (1975) showed exists on every regular $C^2$ curve.

## Definition

Let $C$ be a regular curve, three times continuously differentiable, and let $s$ be its [arc-length parameter](/arc-length-parametrization/), so $\lVert dC/ds \rVert = 1$. Derivatives with respect to $s$ are written with a dot.

**Tangent and curvature.** $T = \dot C$ is the unit tangent. Since $T \cdot T = 1$, $\dot T \cdot T = 0$, so $\dot T$ is normal to the curve. The curvature is $\kappa = \lVert \dot T \rVert$.

**Normal and binormal.** Where $\kappa > 0$, the principal normal is $N = \dot T / \kappa$ and the binormal is $B = T \times N$. $(T, N, B)$ is a right-handed orthonormal frame, the Frenet-Serret frame.

**Torsion.** $\dot B$ is orthogonal to $B$, since $B$ has unit length, and orthogonal to $T$, since $\dot B = \dot T \times N + T \times \dot N = T \times \dot N$. So $\dot B$ is a multiple of $N$, and the torsion is the number $\tau$ with $\dot B = -\tau N$.

**Frenet-Serret formulas.**

$$\begin{pmatrix} \dot T \\ \dot N \\ \dot B \end{pmatrix} = \begin{pmatrix} 0 & \kappa & 0 \\ -\kappa & 0 & \tau \\ 0 & -\tau & 0 \end{pmatrix} \begin{pmatrix} T \\ N \\ B \end{pmatrix}.$$

The matrix is skew-symmetric, which is the condition for an orthonormal frame to stay orthonormal. The collection of $T, N, B, \kappa, \tau$ is the Frenet-Serret apparatus.

**Any regular parameter.** Arc length is rarely available in closed form, so the frame is computed from the derivatives $C', C'', C'''$ in the given parameter $t$:

$$T = \frac{C'}{\lVert C' \rVert}, \quad B = \frac{C' \times C''}{\lVert C' \times C'' \rVert}, \quad N = B \times T,$$

$$\kappa = \frac{\lVert C' \times C'' \rVert}{\lVert C' \rVert^3}, \qquad \tau = \frac{(C' \times C'') \cdot C'''}{\lVert C' \times C'' \rVert^2}.$$

These values do not depend on the parameter: a reparametrization with $\varphi' > 0$ gives the same frame, curvature and torsion. The quantities $\kappa^2$ and $\tau$ are rational functions of the derivatives, so for a polynomial curve with rational coefficients they can be computed exactly.

**Where the frame fails.** The frame needs $C' \times C'' \ne 0$, that is, a regular point with $\kappa \ne 0$. At a point with $\kappa = 0$ the vector $\dot T$ is zero and no direction is preferred for $N$. On a straight piece the frame is undefined on an interval. At an isolated zero of $\kappa$ the limits of $N$ from the two sides can differ: at an inflection of a plane curve they are opposite. Near a zero of $\kappa$ the torsion can be large, because the denominator $\lVert C' \times C'' \rVert^2$ is small, so the frame spins fast even where it is defined.

**Plane curves.** For a curve in the plane, $N$ can be replaced by $T$ turned by $+90°$, which exists at every regular point, and the curvature becomes the signed curvature $k = (x'y'' - y'x'') / \lVert C' \rVert^3$, negative where the curve turns clockwise. With this convention the frame of a plane curve has no defect, and $\kappa = |k|$.

**Rotation-minimizing frames.** A frame $(T, U, V)$ with $\dot U = -k_1 T$ and $\dot V = -k_2 T$ for some functions $k_1, k_2$ does not rotate about $T$. Bishop (1975) showed that such a frame exists on every regular $C^2$ curve, also where $\kappa = 0$, and is unique once $U$ is chosen at one point. Where the Frenet frame exists, $U = \cos\theta\, N - \sin\theta\, B$ with $\dot \theta = \tau$ for a suitable start angle. The double reflection method of Wang, Jüttler, Zheng and Liu (2008) computes such a frame at sample points. It reflects the previous frame in the plane that bisects the chord to the next point, and then in the plane that maps the reflected tangent onto the next tangent. The paper reports fourth-order accuracy, and the helix test of the implementation sees the error fall by a factor of 16 when the step is halved.

The implementation computes the frame, $\kappa$ and $\tau$ from three derivatives and raises an error where $C' \times C'' = 0$. It also computes $\kappa^2$ and $\tau$ exactly in rational arithmetic, and a rotation-minimizing frame by double reflection. Its tests check the closed forms for the helix and the circle, the exact torsion of the twisted cubic, the invariance of $\kappa^2$ and $\tau$ under a reparametrization, and the Frenet-Serret formulas by finite differences.

## Examples and non-examples

**Helix.** $C(t) = (a\cos t, a\sin t, bt)$ with $a > 0$ has speed $c = \sqrt{a^2 + b^2}$, and

$$T = \tfrac1c(-a\sin t, a\cos t, b), \quad N = (-\cos t, -\sin t, 0), \quad B = \tfrac1c(b\sin t, -b\cos t, a),$$

$$\kappa = \frac{a}{a^2 + b^2}, \qquad \tau = \frac{b}{a^2 + b^2}.$$

$N$ points to the axis. The helix has constant curvature and torsion, and by the fundamental theorem every curve with constant $\kappa > 0$ and constant $\tau \ne 0$ is a helix. For $a = b = 1$, $\kappa = \tau = 1/2$. A rotation-minimizing frame that starts at $U = N$ turns against the Frenet frame at the rate $\tau$ per unit length. After one turn, of length $2\pi\sqrt2$, it lags by $\tau \cdot 2\pi\sqrt2 = \pi\sqrt2$, about $254.56°$.

**Circle.** A circle of radius $r$ in the $xy$-plane has $\kappa = 1/r$, $\tau = 0$ and $B = (0, 0, 1)$. A curve with $\tau = 0$ everywhere and $\kappa > 0$ lies in a plane.

**Twisted cubic.** $C(t) = (t, t^2, t^3)$ has $C' \times C'' = (6t^2, -6t, 2)$ and $(C' \times C'') \cdot C''' = 12$, so

$$\tau = \frac{3}{9t^4 + 9t^2 + 1}, \qquad \kappa^2 = \frac{4(9t^4 + 9t^2 + 1)}{(1 + 4t^2 + 9t^4)^3}.$$

At $t = 0$ the frame is the coordinate frame, with $\kappa = 2$ and $\tau = 3$. At $t = 1$, $\kappa = \sqrt{76/14^3} \approx 0.1664$ and $\tau = 3/19$, with $B \approx (0.6882, -0.6882, 0.2294)$. The curve has $\kappa > 0$ everywhere, so the frame exists on the whole curve.

**Non-example: an inflection.** The plane curve $(t, t^3, 0)$ has $C' \times C'' = (0, 0, 6t)$, zero at $t = 0$, so the Frenet frame does not exist there. For $t < 0$ the normal points down and $B = (0, 0, -1)$; for $t > 0$ the normal points up and $B = (0, 0, 1)$. An object oriented by this frame flips over as it passes the inflection. The signed curvature $6t / (1 + 9t^4)^{3/2}$ and a rotation-minimizing frame with $U = (0, 0, 1)$ are both continuous through $t = 0$.

**Non-example: a straight segment.** On a line $C' \times C'' = 0$ for every parametrization, so there is no frame at all. A path made of two circular arcs in different planes, joined by a straight segment, has Frenet frames on the arcs that are not related: the frame jumps from one osculating plane to the other across the segment.

**Non-example: too little smoothness.** A cubic B-spline is only $C^2$ at its knots, so $C'''$ jumps there. The frame and $\kappa$ are continuous at a simple knot, but the torsion jumps.

## Related definitions

- [Arc-length parametrization](/arc-length-parametrization/): the parameter in which the Frenet-Serret formulas are written.
- [Parametric continuity](/parametric-continuity/): $G^2$ asks for a continuous $T$ and $\kappa N$, and $G^3$ also asks for a continuous torsion.
- [Offset curve](/offset-curve/): the curve $C + dN$ of a plane curve, whose cusps appear where $d = 1/\kappa$.
- [Sweep surface](/sweep-surface/): a cross-section moved along a path, oriented by a Frenet or a rotation-minimizing frame.
- [Surface curvature](/surface-curvature/) and [fundamental forms](/fundamental-forms/): the curvature of curves on a surface, split into normal and geodesic parts.

## References
