---
tag: 1PCZM8
kind: definition
slug: parametric-curve
name: Parametric curve
aliases:
- parametric representation
area: graphics-and-signals/curves-and-surfaces
level: intro
summary: A curve given as a continuous map from an interval of parameter values into the plane or space. Graphics and CAD use it because points are easy to compute and loops and space curves are allowed.
prereqs: [point-and-vector]
see_also: [bezier-curve, b-spline, rational-bezier-curve, parametric-surface, arc-length-parametrization, frenet-frame, parametric-continuity, curve-evaluation]
sources:
  - book: isbn:9780132125895
    title: Manfredo P. do Carmo, Differential Geometry of Curves and Surfaces, Prentice-Hall, 1976
    locator: Section 1-2, Parametrized Curves, and Section 1-3, Regular Curves; Arc Length
  - book: isbn:9783540615453
    title: Les Piegl and Wayne Tiller, The NURBS Book, second edition, Springer, 1997
    locator: Chapter 1, Curve and Surface Basics (implicit and parametric forms, power basis and Bezier curves)
  - book: isbn:9781558607378
    title: Gerald Farin, Curves and Surfaces for CAGD, A Practical Guide, fifth edition, Morgan Kaufmann, 2002
    locator: Chapter 10, W. Boehm, Differential Geometry I (parametric curves, reparametrization, tangent and arc length)
---

A parametric curve is a map $C : I \to \mathbb{R}^d$ from an interval $I$ of real numbers into the plane ($d = 2$) or into space ($d = 3$). The number $t \in I$ is the parameter, and $C(t) = (x_1(t), \dots, x_d(t))$ is the point at that parameter. It is the representation of curves in graphics and CAD: [Bézier curves](/bezier-curve/), [B-splines](/b-spline/) and NURBS are all parametric. A parametric curve gives points directly, one per parameter value, so it is easy to draw, to move along and to cut into pieces. It can turn back, cross itself and leave the plane, which a graph $y = f(x)$ cannot. The cost is that the question "is this point on the curve?" is hard, which an implicit equation $F(x, y) = 0$ answers at once.

## Definition

**Parametric curve.** A parametric curve in $\mathbb{R}^d$ is a continuous map $C : I \to \mathbb{R}^d$, where $I$ is an interval, usually closed, $I = [a, b]$. Its *trace* is the image set $C(I)$. A curve is *closed* if $C(a) = C(b)$, and *simple* if $C$ is one to one on $[a, b)$.

**Velocity and regularity.** If $C$ is differentiable, $C'(t)$ is the *velocity* or tangent vector and $\lVert C'(t) \rVert$ the *speed*. The curve is *regular* if $C$ is continuously differentiable and $C'(t) \ne 0$ for every $t$. At a regular point the trace has a tangent line, $C(t) + \lambda C'(t)$. Most of the geometry of curves (the [arc length](/arc-length-parametrization/), the [Frenet frame](/frenet-frame/), the curvature, the [offset curve](/offset-curve/)) is defined for regular curves only.

**Reparametrization.** Let $\varphi : J \to I$ be a continuous bijection between intervals. Then $\tilde C = C \circ \varphi$ is a reparametrization of $C$: it has the same trace and passes through it in the same order or in the reverse order. For regular curves one asks $\varphi$ to be continuously differentiable with $\varphi' \ne 0$, so that $\tilde C$ is regular too, with $\tilde C'(s) = \varphi'(s)\, C'(\varphi(s))$. The tangent direction is kept, and the speed is scaled by $|\varphi'|$. If $\varphi' > 0$, the orientation is kept. Properties that do not change under such reparametrizations, such as the trace, the length, the curvature and the tangent line, are *geometric*. Properties that change, such as the speed and the derivative values, belong to the parametrization. The [parametric continuity](/parametric-continuity/) page uses this split to define $C^k$ and $G^k$ joints.

**Polynomial and rational curves.** A curve is *polynomial* of degree $n$ if every coordinate is a polynomial of degree at most $n$ in $t$, and *rational* if the coordinates are quotients of polynomials with a common denominator, $C(t) = (X_1(t), \dots, X_d(t)) / W(t)$. Bézier and B-spline curves are piecewise polynomial. [Rational Bézier curves](/rational-bezier-curve/) and [NURBS](/nurbs/) are piecewise rational, which is needed for exact conics.

**Three ways to describe a plane curve.** A *graph* $y = f(x)$ is the special parametric curve $C(t) = (t, f(t))$: it cannot have a vertical tangent or pass twice over the same $x$. An *implicit* curve is the zero set $\{(x, y) : F(x, y) = 0\}$. A *parametric* curve is a map. Points are easy to produce from a parametric form and hard from an implicit one. Point membership and inside or outside tests are easy from an implicit form and hard from a parametric one. Converting between the two is possible for rational curves (implicitization by resultants, and parametrization of curves of genus 0), and impossible in general for other curves.

## Examples and non-examples

**A line segment.** $C(t) = (1 - t) A + t B$ for $t \in [0, 1]$ runs from $A$ to $B$ at constant speed $\lVert B - A \rVert$. The map $\varphi(s) = s^2$ on $[0, 1]$ gives $\tilde C(s) = (1 - s^2) A + s^2 B$, the same trace, but $\tilde C'(0) = 0$: a parametrization of a straight segment that is not regular at one end.

**The circle.** $C(t) = (r\cos t, r\sin t)$ for $t \in [0, 2\pi]$ is a regular closed curve with constant speed $r$. The rational map

$$C(t) = \left(\frac{1 - t^2}{1 + t^2}, \frac{2t}{1 + t^2}\right), \qquad t \in \mathbb{R},$$

traces the unit circle except the point $(-1, 0)$, which is the limit as $t \to \pm\infty$. At $t = 1$ it gives $(0, 1)$, and at $t = 1/2$ it gives $(3/5, 4/5)$. The speed is $2/(1 + t^2)$, so it is not constant.

**No polynomial circle.** No nonconstant polynomial curve has the unit circle as its trace. Proof: suppose $x(t)^2 + y(t)^2 = 1$ for all $t$, with polynomials $x, y$ not both constant. Let $k \ge 1$ be the larger of the two degrees, and let $\alpha, \beta$ be the coefficients of $t^k$ in $x$ and $y$; at least one is not zero. The coefficient of $t^{2k}$ in $x^2 + y^2$ is $\alpha^2 + \beta^2 > 0$, but the left side is the constant 1, so this coefficient must be zero, a contradiction. This is why CAD needs rational curves, and why the cubic quarter circle on the [Hermite spline](/hermite-spline/) page has a small error.

**A helix.** $C(t) = (a\cos t, a\sin t, bt)$ with $a > 0$ is a space curve on the cylinder of radius $a$, rising $2\pi b$ per turn, with constant speed $(a^2 + b^2)^{1/2}$. For $b \ne 0$ the coordinate $z$ increases, so $z$ itself can serve as the parameter: the helix is $(a\cos(z/b), a\sin(z/b), z)$. A curve in space has a graph form like this over an axis on each piece where one coordinate is strictly monotone. The [Frenet frame](/frenet-frame/) page computes its curvature and torsion.

**A cusp from a smooth map.** $C(t) = (t^2, t^3)$ is a polynomial map with derivatives of every order, but $C'(0) = (0, 0)$. The trace is the semicubical parabola $y^2 = x^3$, which has a sharp point at the origin. So a smooth parametrization does not give a smooth trace when the velocity is zero, which is the reason for the condition $C' \ne 0$ in the definition of a regular curve.

**A self-intersection.** $C(t) = (\sin t, \sin t \cos t)$ on $[0, 2\pi]$ is a regular closed curve shaped like a figure eight. It passes through the origin at $t = 0$ and at $t = \pi$, with the velocities $(1, 1)$ and $(-1, 1)$, so it crosses itself at a right angle there. It is closed but not simple.

**Non-example: a space-filling curve.** The limit of the [Hilbert curve](/hilbert-curve/) is a continuous map from $[0, 1]$ onto the whole unit square (see [space-filling curve](/space-filling-curve/)). It is a parametric curve by the definition, but nowhere differentiable, and its trace has area. Continuity alone is too weak for geometry, so the curves of graphics and CAD are piecewise smooth and usually regular.

**Non-example: the graph of $|x|$.** The curve $(t, |t|)$ is continuous and its trace has a corner at the origin. No regular parametrization of this trace exists, because a regular curve has a tangent line at every point. It is a piecewise regular curve with two pieces.

## Related definitions

- [Parametric surface](/parametric-surface/): the same idea with two parameters.
- [Bézier curve](/bezier-curve/), [B-spline](/b-spline/), [rational Bézier curve](/rational-bezier-curve/), [NURBS](/nurbs/): the polynomial and rational forms of CAD.
- [Arc-length parametrization](/arc-length-parametrization/): the reparametrization with unit speed.
- [Frenet frame](/frenet-frame/): the tangent, normal and binormal of a regular curve, with curvature and torsion.
- [Parametric continuity](/parametric-continuity/): how two parametric pieces join, $C^k$ for the map and $G^k$ for the trace.
- [Curve evaluation](/curve-evaluation/): the problem of computing $C(t)$ from control points.
- [Curve interpolation](/curve-interpolation/): find a parametric curve through given points.
- [Implicit surface](/implicit-surface/): the zero set form in space, the counterpart of an implicit plane curve.

## References
