---
tag: TVCVSK
kind: algorithm
slug: de-boor-algorithm
name: de Boor's algorithm
aliases:
- de Boor recursion
area: graphics-and-signals/curves-and-surfaces
level: advanced
summary: Evaluates a B-spline curve of degree p at u by p rounds of convex combinations of the p + 1 control points of the span of u. It costs O(p^2) point operations and generalizes de Casteljau.
solves: [curve-evaluation, spline-evaluation]
model: real-ram
complexity:
  vars: {p: the degree, d: the dimension of the points, n: the index of the last control point}
  time: {worst: Θ(p^2 d + log n)}
  space: {extra: Θ(p d)}
properties: {online: false, deterministic: true, recursive: false}
history:
  year: 1972
  people: [Carl de Boor]
  note: De Boor gave the algorithm in On calculating with B-splines (1972), the same year as the recurrence of Cox for the basis functions.
prereqs: [b-spline, cox-de-boor-recursion]
see_also: [de-casteljau-algorithm, curve-evaluation, spline-evaluation, boehm-knot-insertion, nurbs, partition-of-unity, convex-hull-property, horner-rule]
sources:
  - paper: "Carl de Boor, On calculating with B-splines, Journal of Approximation Theory 6 (1972), 50 to 62"
    locator: the evaluation of a B-spline series by the recurrence on its coefficients
  - book: isbn:9780387953663
    title: Carl de Boor, A Practical Guide to Splines, revised edition, Springer, 2001
    locator: Chapter X, The stable evaluation of B-splines and splines (the routine BVALUE); Chapter XI, The B-spline series, control points, and knot insertion
  - book: isbn:9783540615453
    title: Les Piegl and Wayne Tiller, The NURBS Book, second edition, Springer, 1997
    locator: Section 3.2, The definition and properties of B-spline curves (CurvePoint); Section 5.2, Knot insertion (a curve point by repeated insertion of u, the de Boor algorithm)
  - book: isbn:9781558607378
    title: Gerald Farin, Curves and Surfaces for CAGD, A Practical Guide, fifth edition, Morgan Kaufmann, 2002
    locator: the chapter on B-spline curves (the de Boor algorithm and its relation to de Casteljau)
---

De Boor's algorithm computes the point $C(u) = \sum_{i=0}^{n} N_{i,p}(u) P_i$ of a [B-spline](/b-spline/) curve of degree $p$ without computing the basis values. It finds the knot span of $u$, takes the $p + 1$ control points that act on that span, and replaces them $p$ times by convex combinations of neighbors, with weights from the knots. The last point is $C(u)$. It costs $p(p + 1)/2$ point combinations, so $O(p^2)$ per point, and it solves [curve evaluation](/curve-evaluation/) for B-spline curves the way the [de Casteljau algorithm](/de-casteljau-algorithm/) solves it for Bézier curves, of which it is the generalization.

## In plain words

A B-spline curve near one parameter value is pulled by only a few control points, one more than the degree. The algorithm takes these few points and cuts corners. On the line between each pair of neighbors it picks a point, at a fraction given by the knots. That gives one point fewer. It does the same with the new points, and again, until only one point is left. That last point is on the curve.

Each new point lies between two old points, so all the work stays inside the region of the few control points, and rounding errors cannot grow much. The points made on the way are useful too: they are the control points you get when you add the parameter value as a new knot, which is how the same steps split a curve in two.

## The problem

The input is a degree $p \ge 0$, a [knot vector](/knot-vector/) $t_0 \le \cdots \le t_{n+p+1}$ with $n \ge p$ and $t_p < t_{n+1}$, control points $P_0, \ldots, P_n \in \mathbb{R}^d$, and a parameter $u$ in the domain $[t_p, t_{n+1}]$. The output is $C(u) = \sum_i N_{i,p}(u) P_i$, with the closing rule at the right end: for $u = t_{n+1}$ the output is the limit from the left, which is the end point of the drawn curve. This is [curve evaluation](/curve-evaluation/) for B-spline curves; with $d = 1$ it is [spline evaluation](/spline-evaluation/). The model is the [real RAM](/real-ram/), with exact rational arithmetic in the implementation.

## The algorithm

FIND-SPAN returns the $\mu$ with $p \le \mu \le n$ and $t_\mu \le u < t_{\mu+1}$ by [binary search](/binary-search/); for $u = t_{n+1}$ it returns the last nonempty span, with $t_\mu < t_{\mu+1} = t_{n+1}$.

```pseudo id=main
DE-BOOR(t, p, P, u)                              ▷ t[p] ≤ u ≤ t[n+1]
L1  μ ← FIND-SPAN(t, p, u)
L2  for j ← 0 to p do d[j] ← P[μ−p+j]             ▷ the p + 1 active control points
L3  for r ← 1 to p
L4      for j ← p downto r
L5          α ← (u − t[μ−p+j]) / (t[μ+j−r+1] − t[μ−p+j])
L6          d[j] ← (1 − α) · d[j−1] + α · d[j]
L7  return d[p]
```

Write $i = \mu - p + j$ for the index of the control point that started in $d[j]$. Line L5 is the weight $\alpha_{i,r} = (u - t_i)/(t_{i+p-r+1} - t_i)$. The denominator is positive: $i \le \mu$ because $j \le p$, and $i + p - r + 1 = \mu + j - r + 1 \ge \mu + 1$ because $j \ge r$, so it is at least $t_{\mu+1} - t_\mu > 0$. Also $0 \le \alpha \le 1$, so line L6 is a convex combination. Line L4 runs $j$ downward, so that $d[j-1]$ still holds the value of round $r - 1$ when line L6 reads it. After round $r$, the entries $d[r], \ldots, d[p]$ are the points of level $r$; the knots used in round $r$ come closer to $u$ as $r$ grows, and round $p$ uses only $t_\mu$ and $t_{\mu+1}$.

## Example

Take $p = 2$, $t = (0, 0, 0, 1, 2, 3, 3, 3)$, the control points $P_0 = (0, 0)$, $P_1 = (1, 2)$, $P_2 = (3, 3)$, $P_3 = (5, 1)$, $P_4 = (6, 0)$, and $u = 3/2$. Line L1 gives $\mu = 3$, and line L2 gives $d = [P_1, P_2, P_3] = [(1, 2), (3, 3), (5, 1)]$.

| Round $r$ | $j$ | $i$ | knots $t_i$, $t_{i+p-r+1}$ | $\alpha$ (L5) | new $d[j]$ (L6) |
|---|---|---|---|---|---|
| 1 | 2 | 3 | $1, 3$ | $1/4$ | $\tfrac34 (3, 3) + \tfrac14 (5, 1) = (7/2, 5/2)$ |
| 1 | 1 | 2 | $0, 2$ | $3/4$ | $\tfrac14 (1, 2) + \tfrac34 (3, 3) = (5/2, 11/4)$ |
| 2 | 2 | 3 | $1, 2$ | $1/2$ | $\tfrac12 (5/2, 11/4) + \tfrac12 (7/2, 5/2) = (3, 21/8)$ |

So $C(3/2) = (3, 21/8)$. The [Cox-de Boor recursion](/cox-de-boor-recursion/) gives the basis values $1/8, 3/4, 1/8$ at the same $u$, and $\tfrac18 (1, 2) + \tfrac34 (3, 3) + \tfrac18 (5, 1)$ is the same point. The two points of round 1, $(5/2, 11/4)$ and $(7/2, 5/2)$, are the new control points that [Boehm knot insertion](/boehm-knot-insertion/) makes when it inserts $3/2$ into this curve.

For a cubic, take $t = (0, 0, 0, 0, 1, 2, 3, 3, 3, 3)$, the control points $(0, 0), (1, 3), (3, 4), (5, 4), (7, 1), (8, 0)$ and $u = 5/2$. Then $\mu = 5$, round 1 gives $(14/3, 4), (13/2, 7/4), (15/2, 1/2)$, round 2 gives $(145/24, 37/16), (7, 9/8)$, and round 3 gives $C(5/2) = (313/48, 55/32)$.

## Correctness

The proof shows a stronger fact. For $0 \le r \le p$, let $P_i^{[r]}$ be the point in $d[j]$, $i = \mu - p + j$, after round $r$. Then $C(u) = \sum_{i=\mu-p+r}^{\mu} N_{i,p-r}(u) \, P_i^{[r]}$: the curve is a B-spline sum of degree $p - r$ over the points of level $r$. For $r = 0$ this is the definition, restricted to the indices that can be nonzero on the span. One step of the recursion of $N_{i,p-r+1}$, followed by a change of the summation index, turns the sum of level $r - 1$ into the sum of level $r$ with exactly the weights of line L5. At $r = p$ the sum is $N_{\mu,0}(u) P_\mu^{[p]} = d[p]$. The right end follows because every output is a polynomial in $u$ on the span. The full proof is below.

## Complexity

Round $r$ does $p - r + 1$ combinations, so there are $\sum_{r=1}^{p} (p - r + 1) = p(p + 1)/2$ of them, each with one division and $O(d)$ products and sums for points in $\mathbb{R}^d$. With the span search the time is $\Theta(p^2 d + \log n)$ per point in the worst case, and the extra space is the $p + 1$ points of the array, $\Theta(p d)$. For comparison, the [Cox-de Boor recursion](/cox-de-boor-recursion/) computes the $p + 1$ basis values in $\Theta(p^2)$ operations, and the sum $\sum_i N_{i,p}(u) P_i$ then costs $\Theta(p d)$. So for points of high dimension, such as the rows of a surface or [NURBS](/nurbs/) in homogeneous coordinates, the basis route is cheaper by a factor of about $d$ in the $p^2$ term.

## Properties

- **Stable.** Every step is a convex combination with a weight in $[0, 1]$, so the error of each new point is bounded by the errors of its two parents plus one rounding. No subtraction of nearly equal values occurs, unlike in the power form of a piece.
- **Inside the hull.** Every intermediate point lies in the convex hull of $P_{\mu-p}, \ldots, P_\mu$. This is the strong [convex hull property](/convex-hull-property/) of the curve.
- **Affine invariant.** The steps commute with affine maps, so evaluating the transformed control points gives the transformed point, by the [partition of unity](/partition-of-unity/).
- **De Casteljau as a special case.** For the knots $0^{p+1} 1^{p+1}$ and $n = p$, every weight of line L5 is $u$, and the algorithm is the [de Casteljau algorithm](/de-casteljau-algorithm/).
- **The triangle is knot insertion.** The points of round 1 are the control points that Boehm insertion of $u$ makes. If $u$ is not a knot, the curve with $u$ inserted $p$ times has the control points $P_0, \ldots, P_{\mu-p}$, then the left edge of the triangle $d[1]$ of round 1, $d[2]$ of round 2, up to $d[p]$ of round $p$, then the right edge $d[p]$ of rounds $p - 1$ down to 1, then $P_\mu, \ldots, P_n$. This splits the curve at $u$.

## Variants and improvements

- **Rational curves.** For [NURBS](/nurbs/), run the algorithm on the homogeneous points $(w_i P_i, w_i)$ in $\mathbb{R}^{d+1}$ and divide by the last coordinate. The implementation does this in its routine for NURBS points.
- **Derivatives.** $C'(u)$ is a B-spline curve of degree $p - 1$ on the same knots without the end knots, with control points $p (P_i - P_{i-1}) / (t_{i+p} - t_i)$. De Boor's algorithm on these points gives the tangent. The last two points $d[p-1]$ and $d[p]$ of round $p - 1$ also give it: $C'(u) = p (d[p] - d[p-1]) / (t_{\mu+1} - t_\mu)$.
- **A different parameter in each round.** If round $r$ uses its own value $u_r$ in line L5, the result is the polar form, or blossom, $b(u_1, \ldots, u_p)$ of the piece of the curve on the span. With the knots $t_{j+1}, \ldots, t_{j+p}$ of a finer knot vector as the $u_r$, this gives the [Oslo algorithm](/oslo-algorithm/) for [knot refinement](/knot-refinement/).
- **Many points on one span.** For many parameter values, convert each piece to Bézier or power form once by knot insertion, and then evaluate each point in $O(p d)$ with the [Horner rule](/horner-rule/) or a Bernstein form of it. This is faster but less stable for high degree.
- **Surfaces.** For a [tensor product surface](/tensor-product-surface/), run the algorithm in $u$ on $q + 1$ rows of control points, then once in $v$ on the results.

## When to use it

Use it to evaluate one point, or a few points, of a B-spline or NURBS curve with control points in the plane or in space, and to split a curve at a parameter. It needs no basis values and no extra storage beyond $p + 1$ points. When the same parameter is used for many curves, or for a surface with many control points, compute the basis once with the [Cox-de Boor recursion](/cox-de-boor-recursion/) and form the sums. For a Bézier curve, use the [de Casteljau algorithm](/de-casteljau-algorithm/), which is this algorithm on the Bézier knot vector.

## Pitfalls

- **The order of the inner loop.** Line L4 runs $j$ from $p$ down to $r$. A loop from $r$ up to $p$ overwrites $d[j-1]$ before line L6 reads it for $d[j]$, and the result is wrong for $p \ge 2$, with no error message.
- **The wrong knot in line L5.** The upper knot is $t_{i+p-r+1}$, so the denominator shrinks with the round. Code that keeps $t_{i+p}$ in every round is right in round 1 and wrong after it.
- **The right end of a clamped curve.** At $u = t_{n+1}$ a half-open search finds no span with $t_\mu \le u < t_{\mu+1}$ when the end knot has multiplicity $p + 1$. Line L1 must return the last nonempty span. A search that returns an empty span makes line L5 divide by zero, and a search that returns $\mu = n + p$ reads control points past the end of the array.
- **Parameters outside the domain.** For $u < t_p$ or $u > t_{n+1}$ the triangle can still run, but it computes a different polynomial piece extended past its span, not a point of the curve. Line L1 must reject such $u$, or clamp it.
- **Weights in homogeneous form.** For NURBS, line L2 must load the homogeneous points $(w_i P_i, w_i)$. Loading $(P_i, w_i)$, or running the triangle on the $P_i$ alone and then applying the weights, gives a different and wrong point. Dividing by the weight after a round is correct only if the next round multiplies by the new weights again.

## Implementations

## History

Carl de Boor described the algorithm in "On calculating with B-splines", Journal of Approximation Theory, 1972, together with the recurrence for the basis functions that Maurice Cox found independently in the same year. His Fortran routine BVALUE in A Practical Guide to Splines (1978) evaluates a B-spline series and its derivatives this way. Boehm's knot insertion (1980) uses the weights of round 1 to give the control points of the same curve with one more knot, and repeated insertion of $u$ gives the whole triangle; the NURBS Book presents the algorithm in this way.

## References
