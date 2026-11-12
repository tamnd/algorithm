---
tag: QPFBQ7
kind: problem
slug: knot-refinement
name: Knot refinement
area: graphics-and-signals/curves-and-surfaces
level: advanced
summary: Given a B-spline curve and a finer knot vector, find the control points of the same curve on the finer knots. The answer is unique, and each new point is a convex combination of old ones.
prereqs: [b-spline, knot-vector]
see_also: [boehm-knot-insertion, oslo-algorithm, de-boor-algorithm, curry-schoenberg-theorem, lane-riesenfeld-algorithm, chaikin-corner-cutting, nurbs, variation-diminishing-property]
sources:
  - book: isbn:9783540615453
    title: Les Piegl and Wayne Tiller, The NURBS Book, second edition, Springer, 1997
    locator: Section 5.2, Knot insertion; Section 5.3, Knot refinement (refinement of curves and surfaces, and the decomposition into Bézier pieces); Section 5.4, Knot removal
  - book: isbn:9780387953663
    title: Carl de Boor, A Practical Guide to Splines, revised edition, Springer, 2001
    locator: Chapter XI, The B-spline series, control points, and knot insertion
  - paper: doi:10.1016/0010-4485(80)90154-2
    title: Wolfgang Boehm, Inserting new knots into B-spline curves, Computer-Aided Design 12(4) (1980), 199 to 201
    locator: the formula for the control points after the insertion of one knot
  - paper: "Elaine Cohen, Tom Lyche and Richard Riesenfeld, Discrete B-splines and subdivision techniques in computer-aided geometric design and computer graphics, Computer Graphics and Image Processing 14(2) (1980), 87 to 111"
    locator: the refinement of a knot vector by discrete B-splines (the Oslo algorithm)
  - paper: doi:10.1137/0723042
    title: Tom Lyche and Knut Mørken, Making the Oslo algorithm more efficient, SIAM Journal on Numerical Analysis 23(3) (1986), 663 to 675
    locator: the improved versions of the two Oslo algorithms
  - paper: doi:10.1016/0167-8396(89)90032-0
    title: Lyle Ramshaw, Blossoms are polar forms, Computer Aided Geometric Design 6(4) (1989), 323 to 358
    locator: control points as values of the polar form at consecutive knots
  - paper: doi:10.1016/j.cma.2004.10.008
    title: T. J. R. Hughes, J. A. Cottrell and Y. Bazilevs, Isogeometric analysis, CAD, finite elements, NURBS, exact geometry and mesh refinement, Computer Methods in Applied Mechanics and Engineering 194 (2005), 4135 to 4195
    locator: h-refinement by knot insertion
---

Knot refinement asks for the control points of a given [B-spline](/b-spline/) curve on a knot vector with more knots. The curve does not change; only its description does. Every spline on the old knots is also a spline on the new knots, and the new description is unique, so the problem always has exactly one answer. Each new control point is a convex combination of at most $p + 1$ old ones, for degree $p$. [Boehm knot insertion](/boehm-knot-insertion/) adds one knot at a time, and the [Oslo algorithm](/oslo-algorithm/) computes each new control point directly. Refinement is the basic tool behind B-spline subdivision, the split of a curve into Bézier pieces, and the evaluation of a point.

## In plain words

A B-spline curve is drawn by a few control points and a list of numbers, the knots, that say where one polynomial piece ends and the next begins. Sometimes you want more control points for the same curve. For example, you want to edit one part in more detail, or you want to cut the curve into simple pieces.

You can add knots to the list. Each new knot gives one new control point. The task is to find the new points so that the curve stays exactly the same.

The new points are found by cutting corners of the old control polygon. Each new point lies on the polygon, or inside it, near the place of the new knot. Points far from the new knots do not move. When you add many knots, the polygon comes closer and closer to the curve.

## Definition

Fix a degree $p \ge 0$. The input is a [knot vector](/knot-vector/) $\tau = (\tau_0 \le \cdots \le \tau_{n+p+1})$ with control points $c_0, \ldots, c_n \in \mathbb{R}^d$, and a second knot vector $t = (t_0 \le \cdots \le t_{N+p+1})$ that contains $\tau$ as a multiset, so $N - n$ is the number of new knots. The new knots lie in the domain $[\tau_p, \tau_{n+1}]$, so that both vectors have the same domain, and no knot of $t$ has multiplicity more than $p + 1$. The output is $d_0, \ldots, d_N \in \mathbb{R}^d$ with

$$\sum_{j=0}^{N} d_j \, N^{t}_{j,p}(x) = \sum_{i=0}^{n} c_i \, N^{\tau}_{i,p}(x) \quad \text{for all } x \in [\tau_p, \tau_{n+1}),$$

where $N^\tau_{i,p}$ and $N^t_{j,p}$ are the B-splines of degree $p$ on the two knot vectors.

Since the right side is linear in the $c_i$, the answer has the form $d = A c$ for an $(N+1) \times (n+1)$ matrix $A$, the knot insertion matrix. Its entries $A_{j,i} = \alpha_{i,p}(j)$ are the discrete B-splines of Cohen, Lyche and Riesenfeld, and they are the coefficients in

$$N^\tau_{i,p} = \sum_{j} \alpha_{i,p}(j) \, N^t_{j,p} \quad \text{on the domain}.$$

**Existence and uniqueness.** By the [Curry-Schoenberg theorem](/curry-schoenberg-theorem/), the B-splines on $\tau$ span the piecewise polynomials of degree $p$ with breakpoints at the knots and smoothness $C^{p-m}$ at a knot of multiplicity $m$. A new knot either adds a breakpoint or lowers the required smoothness at an old one, so the old space is a subspace of the new one, and the $d_j$ exist. The B-splines on $t$ are linearly independent on the domain under the conditions of that theorem, so the $d_j$ are unique; the theorem's Refinement consequence states this. In terms of the polar form, or blossom, $b$ of the polynomial piece of the curve, the answer is $d_j = b(t_{j+1}, \ldots, t_{j+p})$, as Ramshaw described; that view gives the [Oslo algorithm](/oslo-algorithm/).

**Shape of the matrix.** Each row of $A$ has at most $p + 1$ nonzero entries, in consecutive columns; all entries are nonnegative, and each row sums to 1. So each $d_j$ is a convex combination of at most $p + 1$ consecutive $c_i$. The row sums are 1 because the constant function 1 has all its coefficients equal to 1 on any knot vector, by the [partition of unity](/partition-of-unity/).

## Variants

- **Single knot insertion.** Add one knot $u$. Only $p$ control points change, and [Boehm knot insertion](/boehm-knot-insertion/) gives them in closed form.
- **Repeated insertion of one value.** Insert $u$ until its multiplicity is $p$. If $u$ was not a knot, one of the new control points is the curve point $C(u)$. This is the [de Boor algorithm](/de-boor-algorithm/). Insertion up to multiplicity $p + 1$ splits the curve into two independent curves.
- **Bézier extraction.** Raise every interior knot to multiplicity $p$. Then each span carries the $p + 1$ control points of a [Bézier curve](/bezier-curve/), with shared end points.
- **Uniform subdivision.** On a uniform knot vector, insert the midpoint of every span. The result is again uniform, with half the spacing, and the matrix has the same few weights in every row. This is the [Lane-Riesenfeld algorithm](/lane-riesenfeld-algorithm/), and for $p = 2$ it is [Chaikin corner cutting](/chaikin-corner-cutting/).
- **Rational curves and surfaces.** For [NURBS](/nurbs/), refine the homogeneous points $(w_i c_i, w_i)$ and then divide. For a [tensor product surface](/tensor-product-surface/), refine each row of the control net in $u$, then each column in $v$.
- **Knot removal.** The reverse problem removes knots. It has an exact answer only when the curve already has the higher smoothness at the knot, and otherwise it is an approximation problem. The NURBS Book treats it in Section 5.4.

## Examples

**Degree 1.** Take $p = 1$, $\tau = (0, 0, 1, 2, 2)$, and the control points $(0, 0), (2, 2), (4, 0)$. The curve is the polygon itself. Refining to $t = (0, 0, 1/2, 1, 3/2, 2, 2)$ gives $(0, 0), (1, 1), (2, 2), (3, 1), (4, 0)$: the new points are the curve points $C(1/2) = (1, 1)$ and $C(3/2) = (3, 1)$.

**Degree 2, one knot.** Take $p = 2$, $\tau = (0, 0, 0, 1, 2, 3, 3, 3)$, and $c = (0, 0), (1, 2), (3, 3), (5, 1), (6, 0)$. Inserting $u = 3/2$ gives the knots $(0, 0, 0, 1, 3/2, 2, 3, 3, 3)$ and the six points

$$(0, 0),\ (1, 2),\ (5/2, 11/4),\ (7/2, 5/2),\ (5, 1),\ (6, 0).$$

The two new points are $\tfrac14 c_1 + \tfrac34 c_2$ and $\tfrac34 c_2 + \tfrac14 c_3$; the corner $c_2$ is cut off. Inserting $3/2$ a second time adds the point $(3, 21/8)$ between them, and this is $C(3/2)$.

**Degree 2, all midpoints.** Refine the same curve to $t = (0, 0, 0, 1/2, 1, 3/2, 2, 5/2, 3, 3, 3)$. The rows of $A$, as $\{i : \alpha_{i,2}(j)\}$, are

| $j$ | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 |
|---|---|---|---|---|---|---|---|---|
| row | $\{0{:}\,1\}$ | $\{0{:}\,\tfrac12, 1{:}\,\tfrac12\}$ | $\{1{:}\,\tfrac34, 2{:}\,\tfrac14\}$ | $\{1{:}\,\tfrac14, 2{:}\,\tfrac34\}$ | $\{2{:}\,\tfrac34, 3{:}\,\tfrac14\}$ | $\{2{:}\,\tfrac14, 3{:}\,\tfrac34\}$ | $\{3{:}\,\tfrac12, 4{:}\,\tfrac12\}$ | $\{4{:}\,1\}$ |

and the new control points are $(0, 0), (1/2, 1), (3/2, 9/4), (5/2, 11/4), (7/2, 5/2), (9/2, 3/2), (11/2, 1/2), (6, 0)$. In the uniform middle, the weights $3/4, 1/4$ are those of Chaikin's scheme; near the clamped ends they change.

**Bézier extraction.** Insert $1$ and $2$ once more into $\tau$ of the last example. The knots become $(0, 0, 0, 1, 1, 2, 2, 3, 3, 3)$ and the control points $(0, 0), (1, 2), (2, 5/2), (3, 3), (4, 2), (5, 1), (6, 0)$. The three quadratic Bézier pieces have the control points $(0,0), (1,2), (2,5/2)$ on $[0, 1]$, then $(2,5/2), (3,3), (4,2)$ on $[1, 2]$, then $(4,2), (5,1), (6,0)$ on $[2, 3]$.

**Not a refinement.** Moving a knot, for example from $\tau = (0, 0, 0, 1, 2, 3, 3, 3)$ to $(0, 0, 0, 1, 5/2, 3, 3, 3)$, is not a refinement: $t$ does not contain $\tau$, and in general no control points on $t$ give the same curve, because the curve can have a jump in its second derivative at 2 and none at $5/2$.

## Known algorithms

| Algorithm | Idea | Cost for $k$ new knots |
|---|---|---|
| [Boehm knot insertion](/boehm-knot-insertion/) (1980) | one knot at a time, $p$ new points each | $O(kpd)$ for the arithmetic, plus copies of the arrays |
| [Oslo algorithm](/oslo-algorithm/) (Cohen, Lyche and Riesenfeld 1980) | each row of $A$ by a triangle of $p$ rounds | $O(N p (p + d))$ |
| Improved Oslo algorithms (Lyche and Mørken 1986) | the discrete B-splines that are nonzero at one index are discrete B-splines of lower degree on fewer knots, so each row needs a smaller triangle | fewer operations than the Oslo algorithm |
| Polar forms (Ramshaw 1989) | $d_j = b(t_{j+1}, \ldots, t_{j+p})$ by a de Boor triangle with $p$ different parameters | the same as the Oslo algorithm |
| Interpolation | evaluate the curve at $N + 1$ sites that satisfy the [Schoenberg-Whitney theorem](/schoenberg-whitney-theorem/) for $t$, and solve the banded system | $O(N p^2 d)$, with rounding errors |
| [Lane-Riesenfeld algorithm](/lane-riesenfeld-algorithm/) | uniform knots only: double the points, then average $p$ times | $O(N p d)$ |

## Bounds

Every algorithm must write the $N + 1$ output points, so $\Omega(N d)$ operations are needed. Rows of $A$ for control points far from all new knots are rows of the identity: $d_j = c_{j-s}$, where $s$ is the number of new knots to the left. So at most $kp$ rows need arithmetic. Boehm insertion, done in one array from the right end to the left, as in the refinement routine of the NURBS Book, meets this with $O(N d + k p d)$ operations. Done naively, with one new array per inserted knot, it costs $O(k N d)$. The Oslo algorithm treats every row the same way and costs $O(N p^2)$ for the rows of $A$ and $O(N p d)$ to apply them. Which of the two is faster in practice depends on $p$, on $k$ and on the dimension.

## Reductions

- **Evaluation to refinement.** $C(u)$ is the middle control point after $p$ insertions of $u$ (fewer if $u$ is already a knot). The [de Boor algorithm](/de-boor-algorithm/) is exactly this, without storing the other new points. So [curve evaluation](/curve-evaluation/) reduces to refinement.
- **Splitting to refinement.** Insertion of $u$ up to multiplicity $p + 1$ separates the control points of the parts of the curve on the left and on the right of $u$.
- **Bézier conversion to refinement.** Raising all interior knots to multiplicity $p$ converts a B-spline curve into a chain of Bézier curves, which other systems and the [de Casteljau algorithm](/de-casteljau-algorithm/) can use.
- **Refinement to interpolation.** Since the answer is unique, it is the interpolant on $t$ of the old curve at any $N + 1$ sites that make the collocation matrix nonsingular. This reduces refinement to [curve interpolation](/curve-interpolation/), at a higher cost.

## Applications

- **Rendering and intersection.** Under repeated refinement the control polygon converges to the curve, so a refined polygon can be drawn as the curve, and two curves whose refined control polygons have disjoint convex hulls do not meet. This is the basis of subdivision methods.
- **Design.** A designer adds knots to get more control points in one region, and the curve does not move until the new points are moved.
- **Data exchange.** Bézier extraction converts a B-spline or [NURBS](/nurbs/) curve into the Bézier form that some formats and renderers need.
- **Fitting.** In [B-spline fitting](/b-spline-fitting/), knots are added where the error is large, and refinement gives the start values for the next fit.
- **Isogeometric analysis.** In the [finite element method](/finite-element-method/) on NURBS geometry, refinement by knot insertion, called h-refinement by Hughes, Cottrell and Bazilevs (2005), enlarges the space of trial functions without changing the geometry.
- **Shape preservation.** Each new polygon is obtained from the old one by cutting corners, so the number of crossings of the polygon with any line does not increase; this is a proof of the [variation diminishing property](/variation-diminishing-property/) of B-spline curves.

## References
