---
tag: FDKS5Z
kind: definition
slug: knot-vector
name: Knot vector
aliases:
- knot sequence
area: graphics-and-signals/curves-and-surfaces
level: advanced
summary: A non-decreasing list of parameter values. With degree p and n + 1 control points it has n + p + 2 knots, and the multiplicity of each knot sets the smoothness of the spline there.
prereqs: [spline]
see_also: [b-spline, cox-de-boor-recursion, partition-of-unity, knot-refinement, curry-schoenberg-theorem, schoenberg-whitney-theorem, nurbs, curve-interpolation]
sources:
  - book: isbn:9783540615453
    title: Les Piegl and Wayne Tiller, The NURBS Book, second edition, Springer, 1997
    locator: Section 2.2, Definition and properties of B-spline basis functions (the knot vector U, m = n + p + 1, spans and multiplicity); Section 3.2, B-spline curves (clamped knot vectors); Section 9.2, Global interpolation (the choice of knots); Section 12.2, Knot vectors (conventions in data exchange)
  - book: isbn:9780387953663
    title: Carl de Boor, A Practical Guide to Splines, revised edition, Springer, 2001
    locator: Chapter IX, The representation of piecewise polynomial functions by B-splines (knot sequences, multiplicity and smoothness); Chapter XI, The B-spline series, control points, and knot insertion (the Greville sites)
  - book: isbn:9781558607378
    title: Gerald Farin, Curves and Surfaces for CAGD, A Practical Guide, fifth edition, Morgan Kaufmann, 2002
    locator: the chapter on B-spline curves (knot sequences and end conditions)
---

A knot vector is a finite non-decreasing sequence of real numbers $t_0 \le t_1 \le \cdots \le t_m$ that, together with a degree $p$, defines the [B-spline](/b-spline/) basis functions and so the breakpoints and smoothness of a [spline](/spline/). A B-spline curve of degree $p$ with $n + 1$ control points has $m + 1 = n + p + 2$ knots. A value that appears $\mu$ times in the vector is a knot of multiplicity $\mu$, and the spline is $C^{p - \mu}$ there. The choice of the knot vector, more than the choice of the degree, decides where a spline curve is flexible and where it has corners.

## Definition

Let $p \ge 0$ be the degree and $n \ge p$. A **knot vector** for degree $p$ and $n + 1$ basis functions is a sequence

$$T = (t_0, t_1, \ldots, t_{n+p+1}), \qquad t_0 \le t_1 \le \cdots \le t_{n+p+1},$$

with $t_0 < t_{n+p+1}$. The entries are the **knots**. Some books write $U = (u_0, \ldots, u_m)$ with $m = n + p + 1$; de Boor uses the order $k = p + 1$ and the B-spline $B_{i,k}$ in place of $N_{i,p}$.

- The **multiplicity** of a value $\xi$ is the number of indices $i$ with $t_i = \xi$. A knot is **simple** when its multiplicity is 1.
- The **knot span** $i$ is the half-open interval $[t_i, t_{i+1})$. It is **nonempty** when $t_i < t_{i+1}$. The distinct knot values are the breakpoints of the spline.
- The B-spline $N_{i,p}$ is defined by the $p + 2$ knots $t_i, \ldots, t_{i+p+1}$ through the [Cox-de Boor recursion](/cox-de-boor-recursion/). It is zero outside $[t_i, t_{i+p+1})$. So on a nonempty span $[t_\mu, t_{\mu+1})$ at most the $p + 1$ functions $N_{\mu-p,p}, \ldots, N_{\mu,p}$ are nonzero.
- The **domain** of the curve is $[t_p, t_{n+1}]$. On it, and only on it, all $p + 1$ functions that can be nonzero on a span exist, and they sum to 1 (see [partition of unity](/partition-of-unity/)). The first $p$ and the last $p$ knots are needed to define the B-splines near the ends, but they are not breakpoints inside the domain.

The usual conditions on a knot vector are these. Each interior knot $t_{p+1}, \ldots, t_n$ has multiplicity at most $p + 1$, and the end spans are nonempty: $t_p < t_{p+1}$ and $t_n < t_{n+1}$. Under these conditions the $n + 1$ B-splines are linearly independent on the domain, and a knot of multiplicity $\mu$ inside the domain gives a spline that is $C^{p - \mu}$ there and smooth elsewhere; this is the [Curry-Schoenberg theorem](/curry-schoenberg-theorem/). A knot of multiplicity $p + 1$ inside the domain lets the spline jump. A knot of multiplicity $p + 2$ makes $N_{i,p}$ identically zero for the $i$ with $t_i = t_{i+p+1}$.

Common types:

- **Clamped**, also called open or nonperiodic: $t_0 = \cdots = t_p = a$ and $t_{n+1} = \cdots = t_{n+p+1} = b$. The domain is $[a, b]$, and the curve starts at the first control point and ends at the last one, tangent to the first and the last leg of the control polygon.
- **Uniform**: $t_{i+1} - t_i$ is the same for all $i$, for example $t_i = i$. Each B-spline is a shifted copy of one function. With clamped ends and equally spaced interior knots the vector is called clamped uniform.
- **Nonuniform**: any other spacing. The knots of an interpolating curve often follow the data, for example the chord length or the centripetal rule; see [curve interpolation](/curve-interpolation/).
- **Bézier**: $p + 1$ zeros and $p + 1$ ones with $n = p$. The B-splines are then the [Bernstein polynomials](/bernstein-polynomials/), and the curve is a [Bézier curve](/bezier-curve/).

The **Greville abscissae** of $T$ are $t_i^{*} = (t_{i+1} + \cdots + t_{i+p})/p$ for $p \ge 1$. They are the parameter values at which the control points of a spline function $f(x) = \sum_i c_i N_{i,p}(x)$ are drawn: with the points $(t_i^{*}, c_i)$ as control points, the curve $(x, f(x))$ has the B-spline form, because $x = \sum_i t_i^{*} N_{i,p}(x)$ on the domain.

## Examples and non-examples

**A clamped quadratic vector.** $T = (0, 0, 0, 1, 2, 3, 3, 3)$ with $p = 2$ has 8 knots, so $n + p + 2 = 8$ gives $n = 4$ and five control points. The domain is $[t_2, t_5] = [0, 3]$, with the three nonempty spans $[0, 1)$, $[1, 2)$ and $[2, 3)$. At $u = 1/2$ the five B-splines are $1/4, 5/8, 1/8, 0, 0$, and at $u = 5/2$ they are $0, 0, 1/8, 5/8, 1/4$. The interior knots 1 and 2 are simple, so the curve is $C^1$. The Greville abscissae are $0, 1/2, 3/2, 5/2, 3$.

**A uniform vector.** $T = (0, 1, 2, 3, 4, 5, 6)$ with $p = 2$ has $n = 3$. The domain is only $[t_2, t_4] = [2, 4]$. On $[0, 2)$ and $(4, 6]$ fewer than three B-splines exist, and their sum is $1/8$ at $u = 1/2$ and $7/8$ at $u = 3/2$. A program that evaluates the curve on the whole range $[0, 6]$ draws parts that are not affine combinations of the control points.

**A double knot.** $T = (0, 0, 0, 1, 1, 2, 2, 2)$ with $p = 2$: the knot 1 has multiplicity $2 = p$. The curve is only $C^0$ at $u = 1$, and it passes through the control point $P_2$ there, because $N_{2,2}(1) = 1$. This is how a corner is put into a B-spline curve.

**The Bézier case.** $T = (0, 0, 0, 0, 1, 1, 1, 1)$ with $p = 3$ gives the four cubic Bernstein polynomials on $[0, 1]$.

**Non-examples.**

- $(0, 2, 1, 3)$ is not a knot vector, because it decreases.
- For $p = 2$, five control points and the knot vector $(0, 0, 0, 1, 2, 2, 2)$ do not fit: 7 knots give $n = 3$, so four control points.
- For $p = 2$, $(0, 0, 0, 1, 1, 1, 1, 2, 2, 2)$ has the interior knot 1 with multiplicity $4 = p + 2$. Then $N_{3,2}$, which lives on $t_3 = \cdots = t_6 = 1$, is identically zero, and the basis is not linearly independent.

**Storage conventions.** Some file formats and libraries store $n + p$ knots and leave out $t_0$ and $t_{n+p+1}$, because no B-spline value in the domain depends on them. A reader must know which convention a file uses; the NURBS Book discusses this in its chapter on data exchange.

## Related definitions

- [B-spline](/b-spline/): the basis functions that a knot vector and a degree define.
- [Spline](/spline/): breakpoints are the distinct knot values, and the multiplicities set the smoothness.
- [Cox-de Boor recursion](/cox-de-boor-recursion/): computes the B-splines from the knots. The span index $\mu$ with $t_\mu \le u < t_{\mu+1}$ is found by [binary search](/binary-search/) in $O(\log m)$ steps.
- [Partition of unity](/partition-of-unity/): the B-splines sum to 1 on the domain $[t_p, t_{n+1}]$, with a rule at the right end.
- [Knot refinement](/knot-refinement/), [Boehm knot insertion](/boehm-knot-insertion/) and the [Oslo algorithm](/oslo-algorithm/): add knots and change the control points so that the curve does not change.
- [Curry-Schoenberg theorem](/curry-schoenberg-theorem/): the dimension count from the multiplicities. [Schoenberg-Whitney theorem](/schoenberg-whitney-theorem/): which interpolation sites work with a given knot vector.
- [NURBS](/nurbs/): use the same knot vectors, with weights on the control points.

## References
