---
tag: 9G4X3D
kind: concept
slug: spline
name: Spline
aliases:
- piecewise polynomial
area: graphics-and-signals/curves-and-surfaces
level: intro
summary: A function made of polynomial pieces of degree at most p that join with set smoothness at breakpoints. Spline curves use one spline for each coordinate.
prereqs: [polynomial]
see_also: [b-spline, knot-vector, curry-schoenberg-theorem, nurbs, cubic-spline-interpolation, natural-cubic-spline, bezier-curve, spline-evaluation]
sources:
  - book: isbn:9780387953663
    title: Carl de Boor, A Practical Guide to Splines, revised edition, Springer, 2001
    locator: Chapter VII, A representation for piecewise polynomial functions, and Chapter VIII, The spaces of piecewise polynomials and the truncated power basis
  - book: isbn:9783540615453
    title: Les Piegl and Wayne Tiller, The NURBS Book, second edition, Springer, 1997
    locator: Chapter 1, Curve and surface basics (piecewise polynomial curves), and Chapter 2, B-spline basis functions
  - paper: "Isaac J. Schoenberg, Contributions to the problem of approximation of equidistant data by analytic functions, Quarterly of Applied Mathematics 4 (1946), Part A 45 to 99 and Part B 112 to 141"
    locator: Part A, the first use of the word spline for a smooth piecewise polynomial function
  - book: isbn:9781558607378
    title: Gerald Farin, Curves and Surfaces for CAGD, A Practical Guide, fifth edition, Morgan Kaufmann, 2002
    locator: the chapters on piecewise polynomial curves and B-splines
---

A spline is a function that is a [polynomial](/polynomial/) of degree at most $p$ on each interval between consecutive breakpoints, with a set number of continuous derivatives at each breakpoint. The usual case has $p - 1$ continuous derivatives, so a cubic spline is a $C^2$ function made of cubic pieces. A spline curve in the plane or in space uses one spline for each coordinate. Splines keep the degree low and get flexibility from more pieces, which avoids the oscillation of one polynomial of high degree.

## In plain words

Before computers, a ship designer drew a smooth curve with a thin strip of wood, called a spline, held in place by lead weights. The strip bends smoothly between the weights and never makes a sharp corner.

A spline in mathematics copies this. Cut the range of the input into short intervals. On each interval use a simple curve, a polynomial of low degree such as a parabola or a cubic. Then glue the pieces together so that, at each joint, the two pieces meet with the same height, the same slope, and maybe the same bending.

The pieces are simple, so a spline is cheap to evaluate and easy to store. There are many pieces, so a spline can follow any shape. A change in one piece changes the curve only near that piece. This is why fonts, car bodies and animation paths are made of splines.

## The idea

Fix breakpoints $a = \xi_0 < \xi_1 < \cdots < \xi_l < \xi_{l+1} = b$ and a degree $p \ge 0$. A function $s : [a, b] \to \mathbb{R}$ is a **spline of degree $p$** with these breakpoints when

1. on each interval $[\xi_j, \xi_{j+1})$, $s$ equals a polynomial $s_j$ of degree at most $p$, and
2. at each interior breakpoint $\xi_j$, $1 \le j \le l$, the pieces $s_{j-1}$ and $s_j$ have equal derivatives of orders $0, 1, \ldots, p - 1$.

Some authors use the **order** $k = p + 1$ in place of the degree: a cubic spline has degree 3 and order 4. A spline of degree 0 is a step function, and a spline of degree 1 is a continuous broken line, as in [piecewise linear interpolation](/piecewise-linear-interpolation/).

The general form lets each breakpoint have its own smoothness. If $\xi_j$ has multiplicity $m_j$ with $1 \le m_j \le p + 1$, the pieces must agree in their derivatives of orders $0, \ldots, p - m_j$. Multiplicity 1 is the usual case, and multiplicity $p + 1$ asks for nothing, so $s$ can jump there. The breakpoints, each repeated by its multiplicity and with extra knots at the ends, make up the [knot vector](/knot-vector/).

**The dimension.** The splines of degree $p$ with simple breakpoints $\xi_1, \ldots, \xi_l$ form a vector space of dimension $p + 1 + l$, and the functions

$$1, x, x^2, \ldots, x^p, \quad (x - \xi_1)_+^p, \ldots, (x - \xi_l)_+^p$$

are a basis. Here $(x - \xi)_+^p$ is $(x - \xi)^p$ for $x \ge \xi$ and $0$ for $x < \xi$ (the truncated power). The proof is short. On the first interval, $s$ is any polynomial of degree at most $p$, which gives $p + 1$ free coefficients. At $\xi_j$, the difference $d = s_j - s_{j-1}$ is a polynomial of degree at most $p$ whose value and first $p - 1$ derivatives are zero at $\xi_j$. By the Taylor expansion of $d$ at $\xi_j$, this forces $d(x) = c_j (x - \xi_j)^p$ for one number $c_j$. So each breakpoint adds exactly one free coefficient, and $s(x) = s_0(x) + \sum_j c_j (x - \xi_j)_+^p$. The same count with multiplicities gives dimension $p + 1 + \sum_j m_j$; the [Curry-Schoenberg theorem](/curry-schoenberg-theorem/) proves this and shows that the [B-splines](/b-spline/) are a second basis of the same space.

The truncated power basis is easy to write down, but it is a bad basis for computation: each function is nonzero on the whole right part of the interval, and the coefficients cancel badly in floating point. The B-spline basis has small support, nonnegative values and the [partition of unity](/partition-of-unity/), and nearly all software uses it.

A **spline curve** is a map $C(u) = (x(u), y(u))$ or $(x(u), y(u), z(u))$ in which each coordinate is a spline in the parameter $u$, all with the same breakpoints; see [parametric curve](/parametric-curve/). The smoothness of the coordinates is parametric smoothness, $C^r$. Geometric smoothness $G^r$ asks less: see [parametric continuity](/parametric-continuity/).

## Examples

**The absolute value.** On $[-1, 1]$, $|x| = -x + 2 (x)_+$. It is a spline of degree 1 with one breakpoint at 0. It is continuous, and its slope jumps from $-1$ to $1$.

**A quadratic spline.** Take the breakpoints $0, 1, 2, 3$ and the pieces

$$s(x) = \begin{cases} x^2 / 2 & 0 \le x < 1, \\ (-2x^2 + 6x - 3)/2 & 1 \le x < 2, \\ (3 - x)^2 / 2 & 2 \le x \le 3. \end{cases}$$

At $x = 1$ both pieces have value $1/2$ and slope $1$. At $x = 2$ both have value $1/2$ and slope $-1$. The second derivative is $1$, then $-2$, then $1$, so it jumps, and $s$ is $C^1$ but not $C^2$. This is a spline of degree 2 with simple breakpoints. It is the uniform quadratic B-spline $N_{0,2}$ on the knots $0, 1, 2, 3$, and its values at $x = 0, 1/2, 1, 3/2, 2, 5/2, 3$ are $0, 1/8, 1/2, 3/4, 1/2, 1/8, 0$.

**A double breakpoint.** The function equal to $x^2$ for $x < 0$ and to $x$ for $x \ge 0$ is made of quadratic pieces and is continuous, but its slope jumps from $0$ to $1$. It is not a quadratic spline with a simple breakpoint at 0. It is a quadratic spline with a breakpoint of multiplicity 2 at 0, which asks only for continuity.

**Not a spline.** A function made of cubic pieces that jumps at a breakpoint is not a cubic spline with a simple breakpoint. It becomes one only if the breakpoint gets multiplicity 4.

**Interpolation.** A [cubic spline interpolant](/cubic-spline-interpolation/) through $l + 2$ data points has $l + 4$ coefficients, two more than the data. The two extra conditions pick the variant: zero second derivatives at the ends give the [natural cubic spline](/natural-cubic-spline/), and set end slopes give the complete spline. The [Runge phenomenon](/runge-phenomenon/) of one high degree polynomial does not happen, because the degree stays 3.

## Where it is used

- **Design of shapes.** CAD systems store curves and surfaces as [NURBS](/nurbs/), which are rational splines in the B-spline basis. Fonts store glyph outlines as closed spline curves: TrueType uses quadratic pieces, and PostScript and CFF fonts use cubic [Bézier](/bezier-curve/) pieces.
- **Interpolation and smoothing of data.** [Cubic spline interpolation](/cubic-spline-interpolation/), [smoothing splines](/smoothing-spline/) and least squares spline fits ([curve fitting](/curve-fitting/), [B-spline fitting](/b-spline-fitting/)) model measured data.
- **Animation.** Key frame paths use interpolating splines such as the [Catmull-Rom spline](/catmull-rom-spline/), the [Hermite spline](/hermite-spline/) and the [Kochanek-Bartels spline](/kochanek-bartels-spline/).
- **Numerical methods.** Spline spaces are the trial spaces of [collocation methods](/collocation-method/) and of the [finite element method](/finite-element-method/); isogeometric analysis uses the B-spline basis of the CAD model directly.
- **Surfaces.** A [tensor product surface](/tensor-product-surface/) uses products of two univariate spline bases.

The close pages differ as follows. This page is the general idea. [B-spline](/b-spline/) is the basis that represents every spline. [NURBS](/nurbs/) add weights and give exact conics. The [natural cubic spline](/natural-cubic-spline/), [Hermite spline](/hermite-spline/) and [Catmull-Rom spline](/catmull-rom-spline/) are particular splines fixed by interpolation conditions. [Spline evaluation](/spline-evaluation/) is the problem of computing $s(x)$.

## References
