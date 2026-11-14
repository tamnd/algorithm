---
tag: PW764Q
kind: definition
slug: pythagorean-hodograph-curve
name: Pythagorean hodograph curve
aliases:
- PH curve
area: cad/surface-interrogation-and-design
level: advanced
summary: A polynomial curve whose speed is a polynomial, x'^2 + y'^2 = s^2, so its arc length is a polynomial and its offsets are rational, after Farouki and Sakkalis.
prereqs: [parametric-curve, offset-curve, polynomial-gcd]
see_also: [ph-quintic-hermite-interpolation, offset-curve, curve-offsetting, arc-length-parametrization, parametric-cnc-interpolator, bezier-curve, rational-bezier-curve, unit-quaternion-rotation]
sources:
  - paper: doi:10.1147/rd.345.0736
    title: "Rida T. Farouki and Takis Sakkalis, Pythagorean hodographs, IBM Journal of Research and Development 34(5), 1990"
    locator: pp. 736 to 752 (the definition, the characterization x' = w(u^2 - v^2), y' = 2wuv, polynomial arc length, rational offsets, and the Bézier form of PH cubics)
  - paper: doi:10.2307/2317570
    title: "K. K. Kubota, Pythagorean triples in unique factorization domains, American Mathematical Monthly 79(5), 1972"
    locator: pp. 503 to 505 (the form of all solutions of a^2 + b^2 = c^2 in a unique factorization domain)
  - book: isbn:9783540733973
    title: Rida T. Farouki, Pythagorean-Hodograph Curves, Algebra and Geometry Inseparable, Springer, 2008
    locator: Chapter 17, Pythagorean-hodograph curves; Chapter 19, Complex representation; Chapter 22, Quaternion representation (spatial PH curves)
---

A Pythagorean hodograph (PH) curve is a polynomial plane curve $r(t) = (x(t), y(t))$ whose derivative, the hodograph, satisfies $x'(t)^2 + y'(t)^2 = \sigma(t)^2$ for a polynomial $\sigma$. So the speed $|r'(t)|$ is a polynomial in $t$, not the square root of one. As a result the arc length of a PH curve is a polynomial, its unit tangent and normal are rational, and its [offset curves](/offset-curve/) are exactly rational, which makes PH curves useful for tool paths and for motion at constant speed. Farouki and Sakkalis introduced them in 1990 and showed that all of them come from two polynomials $u, v$ by $x' = u^2 - v^2$, $y' = 2uv$, up to a common factor.

## Definition

A polynomial curve $r(t) = (x(t), y(t))$ with $x, y \in \mathbb{R}[t]$ is a *Pythagorean hodograph curve* if there is $\sigma \in \mathbb{R}[t]$ with

$$x'(t)^2 + y'(t)^2 = \sigma(t)^2 \quad \text{for all } t.$$

Then $|r'(t)| = |\sigma(t)|$. This page uses the left unit normal $N = (-y', x')/\sigma$, which is $r'$ turned by $+90°$ when $\sigma > 0$, and the signed curvature $\kappa = (x' y'' - y' x'')/|r'|^3$, positive where the curve turns toward $N$. The mean curvature $H$ of surfaces does not appear on this page.

### The characterization

**Theorem** (Farouki and Sakkalis 1990, from Kubota 1972). Let $a, b, c \in \mathbb{R}[t]$. Then $a^2 + b^2 = c^2$ if and only if there are $w, u, v \in \mathbb{R}[t]$ with $\gcd(u, v) = 1$ and

$$a = w (u^2 - v^2), \qquad b = 2 w u v, \qquad c = \pm w (u^2 + v^2).$$

So $r$ is a PH curve if and only if $x' = w(u^2 - v^2)$ and $y' = 2wuv$ for such $w, u, v$, and then $\sigma = \pm w (u^2 + v^2)$.

*Proof.* "If": $(u^2 - v^2)^2 + (2uv)^2 = u^4 + 2u^2v^2 + v^4 = (u^2 + v^2)^2$, and multiply by $w^2$.

"Only if". If $a = b = 0$, then $c = 0$; take $w = 0$, $u = 1$, $v = 0$. Otherwise let $w = \gcd(a, b)$ in $\mathbb{R}[t]$ (see [polynomial GCD](/polynomial-gcd/)), and write $a = w a_1$, $b = w b_1$ with $\gcd(a_1, b_1) = 1$. Then $w^2 (a_1^2 + b_1^2) = c^2$, so $w^2$ divides $c^2$, and since $\mathbb{R}[t]$ is a unique factorization domain, $w$ divides $c$. Write $c = w c_1$, so that $a_1^2 + b_1^2 = c_1^2$.

Work in $\mathbb{C}[t]$, also a unique factorization domain, and put $A = a_1 + i b_1$ and $\bar A = a_1 - i b_1$. Then $A \bar A = c_1^2$.

- *$A$ and $\bar A$ are coprime.* A common factor $p$ of $A$ and $\bar A$ divides $A + \bar A = 2a_1$ and $A - \bar A = 2i b_1$. Since $\gcd(a_1, b_1) = 1$ in $\mathbb{R}[t]$, there are $s, q \in \mathbb{R}[t]$ with $s a_1 + q b_1 = 1$, so $p$ divides $1$ and is a unit.
- *$A$ is a constant times a square.* Each linear factor $t - z$ of $c_1^2$ has even multiplicity. Since $A$ and $\bar A$ are coprime, each such factor divides only one of them, with its full even multiplicity. So $A = \lambda h^2$ with $\lambda \in \mathbb{C} \setminus \{0\}$ and $h \in \mathbb{C}[t]$.
- *Take a complex square root.* Write $\lambda = \mu^2$ with $\mu \in \mathbb{C}$, and let $u, v \in \mathbb{R}[t]$ be the real and imaginary parts of $\mu h$. Then $A = (u + iv)^2 = (u^2 - v^2) + i (2uv)$, so $a_1 = u^2 - v^2$ and $b_1 = 2uv$.

A common factor of $u$ and $v$ in $\mathbb{R}[t]$ would divide $a_1$ and $b_1$, so $\gcd(u, v) = 1$. Finally $c_1^2 = a_1^2 + b_1^2 = (u^2 + v^2)^2$, so $(c_1 - (u^2 + v^2))(c_1 + (u^2 + v^2)) = 0$, and $c_1 = \pm (u^2 + v^2)$ because $\mathbb{R}[t]$ has no zero divisors. Multiply by $w$. $\square$

No exchange of $x'$ and $y'$ is needed: the complex square root $\mu$ absorbs the rotation that an exchange would give. In complex form the theorem says that the hodograph $x' + i y'$ of a PH curve is $w(t)\, z(t)^2$ with $z = u + iv \in \mathbb{C}[t]$ (Farouki 2008, Chapter 19).

**Degree.** If $w = 1$ and $m = \max(\deg u, \deg v)$, then $r$ has degree $2m + 1$, which is odd. The PH cubics come from linear $u, v$, and the PH quintics from quadratic $u, v$. A quintic has enough free parameters to match end points and end tangents, which is the [PH quintic Hermite interpolation](/ph-quintic-hermite-interpolation/) problem.

### What the property gives

- **Polynomial arc length.** The arc length from $0$ to $t$ is $s(t) = \int_0^t |\sigma(\tau)|\, d\tau$. If $\sigma$ has no sign change on $[0, t]$, this is $\pm \int_0^t \sigma$, a polynomial in $t$ of degree $\deg \sigma + 1$. When $w = 1$, $\sigma = u^2 + v^2 \ge 0$, so $s$ is a polynomial on every interval. Then the inverse problem of [arc length parametrization](/arc-length-parametrization/), finding $t$ with $s(t) = S$, is the root of a monotone polynomial, which a [parametric CNC interpolator](/parametric-cnc-interpolator/) solves in real time by a few Newton steps.
- **Rational normal and offsets.** Where $\sigma \ne 0$, $N = (-y', x')/\sigma$ is rational, so the offset $r_d = r + d N = (\sigma r + d(-y', x'))/\sigma$ is a rational curve for every distance $d$. If $r$ has degree $n$, the numerator has degree at most $2n - 1$ and the denominator degree $n - 1$. For a general polynomial curve the offset is not rational (see [offset curve](/offset-curve/)).
- **Rational curvature.** With $w = 1$ and $z = u + iv$, $r' = z^2$ and $r'' = 2 z z'$, so $x' y'' - y' x'' = \operatorname{Im}(\bar z^2 \cdot 2 z z') = 2 |z|^2 \operatorname{Im}(\bar z z')$, and

$$\kappa = \frac{2 (u v' - u' v)}{(u^2 + v^2)^2}.$$

- **Bézier form of PH cubics.** A cubic [Bézier curve](/bezier-curve/) with control polygon legs $L_1, L_2, L_3$ is a PH curve if and only if $|L_2| = \sqrt{|L_1| |L_3|}$ and the angle between $L_1$ and $L_2$ equals the angle between $L_2$ and $L_3$ (Farouki and Sakkalis 1990).

## Examples and non-examples

### The PH cubic

$u = 1$, $v = t$ give $r(t) = (t - t^3/3,\ t^2)$ with $\sigma = 1 + t^2$; its exact offset and its cusps are on the [offset curve](/offset-curve/) page. Its arc length from $0$ to $1$ is $\int_0^1 (1 + t^2)\, dt = 4/3$. On $[0, 1]$ its Bézier control points are $(0, 0)$, $(1/3, 0)$, $(2/3, 1/3)$, $(2/3, 1)$, with legs $(1/3, 0)$, $(1/3, 1/3)$, $(0, 2/3)$ of lengths $1/3$, $\sqrt 2/3$, $2/3$. So $|L_2|^2 = 2/9 = |L_1| |L_3|$, and both angles are $45°$.

### A PH quintic

Take $z = (1 + it)^2$, that is $u = 1 - t^2$ and $v = 2t$, with $\gcd(u, v) = 1$. Then

$$x' = (1 - t^2)^2 - 4t^2 = 1 - 6t^2 + t^4, \qquad y' = 4t(1 - t^2), \qquad \sigma = (1 + t^2)^2,$$

$$r(t) = \left(t - 2t^3 + \tfrac{t^5}{5},\ 2t^2 - t^4\right).$$

- The arc length from $0$ to $1$ is $\int_0^1 (1 + 2t^2 + t^4)\, dt = 1 + 2/3 + 1/5 = 28/15$.
- $uv' - u'v = 2(1 - t^2) + 4t^2 = 2(1 + t^2)$, so $\kappa = 4/(1 + t^2)^3 > 0$, and the curve has no inflection.
- At $t = 1$, $r = (-4/5, 1)$, $r' = (-4, 0)$ and $\sigma = 4$, so $N = (0, -1)$, and the offset point at distance $d$ is $(-4/5, 1 - d)$, exactly.

### Non-example: the parabola

$r(t) = (t, t^2)$ has $x'^2 + y'^2 = 1 + 4t^2$. This polynomial has the simple complex roots $\pm i/2$, and a square of a polynomial has only roots of even multiplicity, so it is not a square. The arc length $\int_0^1 \sqrt{1 + 4t^2}\, dt = \frac{\sqrt 5}{2} + \frac{1}{4} \operatorname{asinh} 2 \approx 1.478943$ is not a polynomial value, and the offsets of the parabola are not rational.

### Degenerate cases

- **Lines.** Every polynomial parametrization of a line is a PH curve: $x' = p(t) \cos \phi$, $y' = p(t) \sin \phi$ has $\sigma = p$. In the theorem, $w = p$ and $u + iv$ is a constant.
- **Cusps.** If $w$ has a real root in the interval, then $r' = 0$ there and the curve can have a cusp. There $\sigma$ changes sign, the arc length is only piecewise polynomial, and the normal $N$ flips. Designs usually take $w = 1$.

## Related definitions

- **Spatial PH curves.** Polynomial space curves with $x'^2 + y'^2 + z'^2 = \sigma^2$. They are described by a quaternion polynomial $\mathcal{A}(t)$ with $r' = \mathcal{A}\, \mathbf{i}\, \mathcal{A}^*$, the analogue of $z^2$ in the plane (Farouki 2008, Chapter 22), related to [unit quaternion rotation](/unit-quaternion-rotation/).
- **PH quintic Hermite interpolation.** The construction of a planar PH quintic with given end points and end derivatives; see [PH quintic Hermite interpolation](/ph-quintic-hermite-interpolation/).
- **Offset curve.** The curve at constant normal distance; see [offset curve](/offset-curve/) and [curve offsetting](/curve-offsetting/).
- **Rational curves.** The exact offset of a PH curve is a [rational Bézier curve](/rational-bezier-curve/) on each interval where $\sigma \ne 0$.

## References
