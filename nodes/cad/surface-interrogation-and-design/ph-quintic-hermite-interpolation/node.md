---
tag: XD0FDH
kind: algorithm
slug: ph-quintic-hermite-interpolation
name: PH quintic Hermite interpolation
aliases:
- Farouki-Neff PH interpolation
area: cad/surface-interrogation-and-design
level: advanced
summary: Farouki and Neff's construction of planar PH quintics with given end points and end derivatives by complex arithmetic. It gives four solutions, of which one is usually fair.
solves: [hermite-interpolation]
model: real-ram
complexity:
  vars: {N: the number of samples used to compare the four solutions}
  time: {worst: Θ(N), best: Θ(N)}
  space: {extra: Θ(1)}
properties: {online: false, deterministic: true, recursive: false}
history:
  year: 1995
  people: [Rida T. Farouki, C. Andrew Neff]
  note: Farouki and Neff solved the first order Hermite problem for planar PH quintics in closed form in 1995, in complex arithmetic, and showed that it has four solutions.
prereqs: [pythagorean-hodograph-curve, hermite-interpolation, bezier-curve]
see_also: [parametric-cnc-interpolator, offset-curve, arc-length-parametrization, gaussian-quadrature, newton-method-for-systems, cubic-spline-interpolation, curvature-comb, unit-quaternion-rotation]
sources:
  - paper: doi:10.1090/S0025-5718-1995-1308452-6
    title: "Rida T. Farouki and C. Andrew Neff, Hermite interpolation by Pythagorean hodograph quintics, Mathematics of Computation 64(212), 1995"
    locator: pp. 1589 to 1609 (the complex form of the problem, the four solutions, and the choice of the good one)
  - book: isbn:9783540733973
    title: Rida T. Farouki, Pythagorean-Hodograph Curves, Algebra and Geometry Inseparable, Springer, 2008
    locator: Chapter 25, planar PH quintic Hermite interpolants (pages 523 to 541), and the chapter on real-time CNC interpolators
  - paper: "Hwan Pyo Moon, Rida T. Farouki and Hyeong In Choi, Construction and shape analysis of PH quintic Hermite interpolants, Computer Aided Geometric Design 18(2), 93 to 115, 2001"
    title: Moon, Farouki and Choi 2001
    locator: the shape of the four interpolants and their comparison by the absolute rotation index
---

PH quintic Hermite interpolation builds a quintic [Pythagorean hodograph curve](/pythagorean-hodograph-curve/) with given end points and given end derivatives. Farouki and Neff wrote the curve in the complex plane as $r' = w^2$ for a complex quadratic $w$, which turns the problem into three quadratic equations that can be solved one after the other with square roots. There are four solutions. One of them is usually a fair curve, and the other three turn too much or turn back and forth, so the algorithm ends with a measured choice among the four. The result has a polynomial speed, an exact arc length and rational offsets, which is what tool path and motion planning code needs.

The model is the [real RAM](/real-ram/), with exact complex arithmetic and exact square roots. The implementation uses Python complex numbers in floating point.

## In plain words

You know where a path starts and ends, in which direction it leaves and arrives, and how fast. You want a smooth curve with these ends whose length you can compute exactly, so that a machine can move along it at a steady speed without approximations. Pythagorean hodograph curves have this property, and the simplest ones that can match all these end conditions have degree five. Their shape is fixed by three complex numbers. The start condition fixes the first, the end condition fixes the third up to a sign, and the end point fixes the middle one up to a second sign. Two signs give four curves through the same ends. Usually one of them is a calm arc, and the others swing out or wiggle. The method computes all four and keeps the calmest.

## The problem

Points and vectors of the plane are complex numbers $x + iy$. The input is two end points $p_0, p_5$ and two nonzero end derivatives $d_0, d_1$. A *PH quintic* here is a polynomial curve $r : [0, 1] \to \mathbb{C}$ with

$$r'(t) = w(t)^2, \qquad w(t) = w_0 (1 - t)^2 + w_1\, 2 (1 - t) t + w_2 t^2,$$

for complex $w_0, w_1, w_2$. By the characterization on the [PH curve](/pythagorean-hodograph-curve/) page, with $w = u + iv$ this is $x' = u^2 - v^2$, $y' = 2uv$, so the speed $\sigma = |r'| = |w|^2 = u^2 + v^2$ is a polynomial. The output is the PH quintics with

$$r(0) = p_0, \quad r(1) = p_5, \quad r'(0) = d_0, \quad r'(1) = d_1.$$

This is first order [Hermite interpolation](/hermite-interpolation/) in the class of PH quintics. A cubic Hermite interpolant always exists and is unique, but it is a PH curve only for special data. The PH quintic has the same number of real degrees of freedom, three complex coefficients for $w$ and one for $p_0$, but they enter quadratically. This page uses the left unit normal $N = i r'/|r'|$ and the signed curvature $\kappa = \operatorname{Im}(\bar r' r'')/|r'|^3$, positive where the curve turns toward $N$; the mean curvature $H$ of surfaces does not appear.

## The algorithm

The square roots are principal square roots of complex numbers.

```pseudo id=main
PH-QUINTIC-HERMITE(p_0, p_5, d_0, d_1)
L1  Δ ← p_5 − p_0
L2  w_0 ← √d_0                                    ▷ fixes the sign of w, which r' = w² does not see
L3  for ε in (+1, −1) do
L4      w_2 ← ε √d_1
L5      c ← 120 Δ − 15 (d_0 + d_1) + 10 w_0 w_2
L6      for η in (+1, −1) do
L7          w_1 ← (−3 (w_0 + w_2) + η √c) / 4
L8          p_1, ..., p_5' ← p_0 + w_0²/5, p_1 + w_0 w_1/5, p_2 + (2 w_1² + w_0 w_2)/15, p_3 + w_1 w_2/5, p_4 + w_2²/5
L9          add the curve with control points p_0, p_1, p_2, p_3, p_4, p_5' to S
L10 return S
```

The equations come from the end data. At the ends, $r'(0) = w_0^2$ and $r'(1) = w_2^2$, which gives lines L2 and L4. The squares of the quadratic Bernstein polynomials are quartic Bernstein polynomials, so $w^2$ has the quartic Bernstein coefficients $w_0^2$, $w_0 w_1$, $(2 w_1^2 + w_0 w_2)/3$, $w_1 w_2$, $w_2^2$. Integrating gives the control points of line L8, and the end point condition $r(1) = p_5$ becomes, after completing the square in $w_1$,

$$\left(4 w_1 + 3 (w_0 + w_2)\right)^2 = 120 \Delta - 15 (d_0 + d_1) + 10 w_0 w_2,$$

which line L7 solves. The last control point $p_5'$ equals $p_5$ up to rounding.

**Choosing one.** Among the four curves, choose the one with the least *absolute rotation index* $R_{\text{abs}} = \frac{1}{2\pi} \int |\kappa|\, ds$, the total turning of the tangent. Since the tangent angle of $r' = w^2$ is $2 \arg w$, this is $\frac{1}{\pi} \int_0^1 |d \arg w(t)|$. The implementation measures it by summing the changes of $\arg w$ over $N$ equal steps. The choice is a heuristic, supported by measurement and not by a theorem: it rejects curves whose tangent makes extra turns or turns back and forth, and Moon, Farouki and Choi use this measure to compare the four. Bending energy $\int \kappa^2\, ds$ is another criterion and usually agrees.

**The speed and the arc length.** The speed $\sigma = |w|^2$ has the quartic Bernstein coefficients

$$\sigma_0 = |w_0|^2, \quad \sigma_1 = \operatorname{Re}(w_0 \bar w_1), \quad \sigma_2 = \tfrac{1}{3}\left(2 |w_1|^2 + \operatorname{Re}(w_0 \bar w_2)\right), \quad \sigma_3 = \operatorname{Re}(w_1 \bar w_2), \quad \sigma_4 = |w_2|^2,$$

and the arc length is $S = (\sigma_0 + \sigma_1 + \sigma_2 + \sigma_3 + \sigma_4)/5$. The arc length function $s(t)$ is the quintic with Bernstein coefficients $0, \sigma_0/5, (\sigma_0 + \sigma_1)/5, \dots, S$.

## Example

Take $p_0 = 0$, $p_5 = 1$, $d_0 = 3i$ and $d_1 = -3i$: start at the origin going straight up, end at $(1, 0)$ going straight down, with speed $3$ at both ends. Then $\Delta = 1$, $d_0 + d_1 = 0$, and with $a = \sqrt{3/2}$,

$$w_0 = \sqrt{3i} = a (1 + i), \qquad w_2 = \varepsilon\, a (1 - i), \qquad w_0 w_2 = 3 \varepsilon, \qquad c = 120 + 30 \varepsilon.$$

| $\varepsilon$, $\eta$ | $c$ | $w_1$ | $p_2$ | $p_3$ | arc length $S$ | $R_{\text{abs}}$ |
|---|---|---|---|---|---|---|
| $+1$, $+1$ | $150$ | $a \approx 1.22474$ | $(0.3, 0.9)$ | $(0.7, 0.9)$ | $2$ | $0.5$ |
| $+1$, $-1$ | $150$ | $-2\sqrt 6 \approx -4.89898$ | $(-1.2, -0.6)$ | $(2.2, -0.6)$ | $2$ | $1.5$ |
| $-1$, $+1$ | $90$ | $(3\sqrt{10} - 3\sqrt 6\, i)/4$ | $(1.03095, 0.73095)$ | $(1.13095, -0.43095)$ | $1.5$ | $\approx 1.173$ |
| $-1$, $-1$ | $90$ | $(-3\sqrt{10} - 3\sqrt 6\, i)/4$ | $(-0.13095, -0.43095)$ | $(-0.03095, 0.73095)$ | $1.5$ | $\approx 1.173$ |

All four have $p_1 = 0.6i = (0, 0.6)$ and $p_4 = 1 + 0.6i = (1, 0.6)$, because these depend only on the end derivatives.

The first solution is an arch. Its $w_1 = a$ is real, and its control points $(0, 0)$, $(0, 0.6)$, $(0.3, 0.9)$, $(0.7, 0.9)$, $(1, 0.6)$, $(1, 0)$ are symmetric about $x = 1/2$. Its speed has the Bernstein coefficients $3, \tfrac{3}{2}, 1, \tfrac{3}{2}, 3$, so its arc length is $10/5 = 2$. At $t = 1/2$ it is at the top point $(0.5, 0.75)$, with $w = a$, $w' = w_2 - w_0 = -2ai$, speed $3/2$ and curvature $\kappa = 2 \operatorname{Im}(\bar w w')/|w|^4 = -8/3$. Its tangent turns clockwise by half a turn and never back, so $R_{\text{abs}} = 1/2$, the least possible for these end directions. The second solution has the same length, but its tangent makes a full extra turn: the curve swings out to the left, passes below the chord down to $y = -0.1875$, and comes back up on the right, so $R_{\text{abs}} = 3/2$. The third and fourth are mirror images of each other in the line $x = 1/2$ and have inflections. The rule of least $R_{\text{abs}}$ picks the arch.

As a check that is independent of the formula for $\sigma$, the tests compute $|r'(t)|$ from the control points by differencing and the de Casteljau algorithm, and integrate it by composite [Gaussian quadrature](/gaussian-quadrature/). The values agree with $S$ to about $10^{-15}$, here and on random data.

## Correctness

The proof file below proves the following, using only the product rule of Bernstein polynomials and the fact that $\mathbb{C}[t]$ has no zero divisors.

1. Each of the four curves is a PH quintic with the given end points and end derivatives. The control points of line L8 integrate $w^2$, and the three end conditions are equivalent to $w_0^2 = d_0$, $w_2^2 = d_1$ and the squared equation of line L7.
2. Every PH quintic with the given end data is one of the four. If $r' = v^2$, then $v$ or $-v$ has $v(0) = \sqrt{d_0}$, and the equations then fix $v(1)$ up to the sign $\varepsilon$ and $v_1$ up to the sign $\eta$.
3. The four are pairwise different when both radicands $c_{+1}$ and $c_{-1}$ are nonzero. Two quadratics with $w^2 = v^2$ satisfy $w = \pm v$, and with the same nonzero $w(0)$ this forces $w = v$. If $c_\varepsilon = 0$, the two solutions with this $\varepsilon$ coincide.

The speed formula and $S = \frac{1}{5} \sum \sigma_k$ follow from $|w|^2 = w \bar w$ by the same product rule. The choice among the four is a measured heuristic and is not part of the proof.

## Complexity

Lines L1 to L10 use three complex square roots and a fixed number of complex additions and multiplications, so the four curves cost $\Theta(1)$ operations. The arc length costs $\Theta(1)$ more. The measured absolute rotation index costs $\Theta(N)$ for $N$ samples per curve, which dominates. A version that splits $[0, 1]$ at the inflections, the zeros of the quadratic $\operatorname{Im}(\bar w w')$, and adds the exact changes of $\arg w$ on the pieces costs $\Theta(1)$. Extra space is $\Theta(1)$.

## Properties

- **Exact arc length.** The speed is a quartic polynomial and the arc length a quintic, with no quadrature. This is what [real-time CNC interpolators](/parametric-cnc-interpolator/) use to move at a given feed rate along the curve.
- **Rational offsets.** As for every PH curve, the offset at distance $d$ is $r + d N$ with $N = i w^2/|w|^2$, a rational curve of degree $9$ in the parameter; see [offset curve](/offset-curve/).
- **Invariant under similarities.** If all data are mapped by $z \mapsto a z + b$ with $a \ne 0$, the set of four solutions is mapped in the same way, and the lengths scale by $|a|$. The individual labels $(\varepsilon, \eta)$ can change, because the principal square root is not multiplicative. General affine maps do not preserve the PH property, so the method is not affine invariant.
- **Not linear in the data.** Doubling the end derivatives does not give a combination of earlier solutions. The shape depends on the magnitudes $|d_0|$, $|d_1|$, and not only on the directions.
- **Polynomial degree.** Five is the least degree for which PH curves can match general first order Hermite data. A PH cubic has a hodograph $w^2$ with $w$ linear, two complex coefficients, and cannot match two end points and two arbitrary end derivatives.

## Variants and improvements

- **Free tangent magnitudes.** If only the end directions are given, the magnitudes $|d_0|$ and $|d_1|$ are free parameters. Choosing them, for example to make the curve close to a given curve or to minimize bending energy, gives $G^1$ interpolation.
- **PH quintic splines.** For $C^2$ interpolation of many points by PH quintics, the coefficients of neighbouring pieces are coupled by quadratic equations that no longer decouple. They are solved by [Newton's method for systems](/newton-method-for-systems/) from the cubic spline as a starting guess, and among exponentially many formal solutions the one near the [cubic spline](/cubic-spline-interpolation/) is kept.
- **Spatial PH quintics.** In space the hodograph is written with quaternions, $r' = \mathcal{A} \mathbf{i} \mathcal{A}^*$ for a quaternion quadratic $\mathcal{A}$, see [unit quaternion rotation](/unit-quaternion-rotation/). The Hermite problem then has a two parameter family of solutions instead of four.
- **Higher order Hermite data.** Matching curvature at the ends as well needs PH curves of degree seven.

## When to use it

Use it to build tool paths, robot paths or motion curves that a controller will follow at a given speed, when the path is given by points and tangents: each span becomes a PH quintic, and the controller computes the parameter for each arc length exactly. Use it also to convert a free form curve into a chain of PH quintics, sampling points and derivatives and interpolating each span. For curves that are only drawn or intersected, an ordinary cubic Hermite or B-spline curve is simpler, and the arc length can be computed by quadrature when needed.

## Pitfalls

- **Taking any one of the four.** A fixed choice of the signs, such as $\varepsilon = \eta = +1$, gives the good curve for the example above, but not in general. Compute all four and compare.
- **Branches of the square root.** The set of four does not depend on which square roots are taken, but the labels do. Code that remembers a solution by its labels can switch to a different curve after a small change of the data that crosses the branch cut of the principal root.
- **Zero end derivatives.** For $d_0 = 0$, the normalization $w_0 = \sqrt{d_0}$ fixes nothing, and the curve has a cusp at the start. The construction requires $d_0, d_1 \ne 0$.
- **Merging solutions.** When $c_\varepsilon$ is near zero, two solutions are close to each other and sensitive to the data, through the square root.
- **Magnitudes matter.** End derivatives that are much longer or shorter than the chord can give a curve with a lot of turning even for the best choice of signs. Scale them in proportion to $|p_5 - p_0|$, for example to $|p_5 - p_0|$ or a small multiple of it.
- **Rounding of the end point.** In floating point, the last control point differs from $p_5$ by rounding. Code that needs exact continuity between spans should copy $p_5$ into it.

## Implementations

The Python file in this folder has `ph_quintic_hermite(p0, p5, d0, d1)`, which returns the four solutions with their coefficients and control points, and helpers for the speed, the arc length, the measured absolute rotation index and the choice of the fairest solution. The tests check the end data, the hodograph against the control points, the polynomial speed and arc length against composite Gauss-Legendre quadrature of $|r'|$, the distinctness of the four solutions, the solutions against Newton's method on the raw equations from random starts, and the worked example.

## History

Farouki and Sakkalis introduced PH curves in 1990 and gave the PH cubics, which are too stiff for general Hermite data. In 1995 Farouki and Neff solved the first order Hermite problem for PH quintics. In the complex form the equations decouple into square roots, and they showed that there are four solutions, of which typically only one has a reasonable shape. Later work by Moon, Farouki and Choi analysed the shape of the four interpolants, and the method became the base of PH quintic splines and of CNC interpolators for PH tool paths, collected in Farouki's book of 2008.

## References
