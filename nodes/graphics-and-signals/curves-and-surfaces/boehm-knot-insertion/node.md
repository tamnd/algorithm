---
tag: A1WEXZ
kind: algorithm
slug: boehm-knot-insertion
name: Boehm's knot insertion
aliases:
- knot insertion algorithm
area: graphics-and-signals/curves-and-surfaces
level: advanced
summary: Inserts one knot u into a B-spline curve of degree p. It replaces p - 1 control points near u by p convex combinations of neighbors, and the curve does not change.
solves: [knot-refinement]
model: real-ram
complexity:
  vars: {p: the degree, d: the dimension of the points, n: the index of the last control point}
  time: {worst: Θ(log n + p d + n d)}
  space: {extra: Θ(n d)}
properties: {online: false, deterministic: true, recursive: false}
history:
  year: 1980
  people: [Wolfgang Boehm]
  note: Boehm published the formula in Inserting new knots into B-spline curves, Computer-Aided Design 12 (1980). The Oslo algorithm for many knots appeared in the same year.
prereqs: [knot-refinement, b-spline]
see_also: [oslo-algorithm, de-boor-algorithm, de-casteljau-algorithm, knot-vector, nurbs, chaikin-corner-cutting, variation-diminishing-property, curry-schoenberg-theorem]
sources:
  - paper: doi:10.1016/0010-4485(80)90154-2
    title: Wolfgang Boehm, Inserting new knots into B-spline curves, Computer-Aided Design 12(4) (1980), 199 to 201
    locator: the formula for the new control points after one knot is inserted
  - book: isbn:9783540615453
    title: Les Piegl and Wayne Tiller, The NURBS Book, second edition, Springer, 1997
    locator: Section 5.2, Knot insertion (insertion of one knot several times, and the relation to the de Boor algorithm); Section 5.3, Knot refinement
  - book: isbn:9780387953663
    title: Carl de Boor, A Practical Guide to Splines, revised edition, Springer, 2001
    locator: Chapter XI, The B-spline series, control points, and knot insertion
  - book: isbn:9781558607378
    title: Gerald Farin, Curves and Surfaces for CAGD, A Practical Guide, fifth edition, Morgan Kaufmann, 2002
    locator: the chapter on B-spline curves (knot insertion)
  - paper: "Elaine Cohen, Tom Lyche and Richard Riesenfeld, Discrete B-splines and subdivision techniques in computer-aided geometric design and computer graphics, Computer Graphics and Image Processing 14(2) (1980), 87 to 111"
    locator: the Oslo algorithm, the other method for knot refinement
---

Boehm's knot insertion adds one knot $u$ to a [B-spline](/b-spline/) curve of degree $p$ and returns the control points of the same curve on the longer [knot vector](/knot-vector/). Only the control points near $u$ change: $p - 1$ old points are replaced by $p$ new points, and each new point lies on a leg of the old control polygon, at a fraction given by the knots. The work is $p$ convex combinations, so $O(p d)$ arithmetic for points in $\mathbb{R}^d$. Repeated, it solves [knot refinement](/knot-refinement/), and the insertion of $u$ up to multiplicity $p$ is the [de Boor algorithm](/de-boor-algorithm/).

## In plain words

A B-spline curve is pulled by its control points, and a list of numbers, the knots, says where its polynomial pieces join. Adding one knot gives the same curve one more control point. This algorithm finds the new control points.

Only a few points near the new knot are affected, one fewer than the degree plus one. Each of them is replaced by a point on a side of the control polygon, at a distance along the side that the nearby knots fix. The effect is that one corner of the polygon is cut off, and the new polygon is closer to the curve.

Points far from the new knot stay as they are. So the work is small, and it does not depend on the length of the curve, except for copying the lists.

## The problem

The input is a degree $p \ge 1$, a knot vector $t_0 \le \cdots \le t_{n+p+1}$ with $n \ge p$, control points $P_0, \ldots, P_n \in \mathbb{R}^d$, and a parameter $u$ with $t_p \le u < t_{n+1}$ that is a knot of multiplicity at most $p$, or no knot. The output is the knot vector $t'$ that is $t$ with $u$ added in its place, and points $Q_0, \ldots, Q_{n+1}$ with $\sum_j Q_j N^{t'}_{j,p} = \sum_i P_i N^{t}_{i,p}$ on the domain $[t_p, t_{n+1}]$. This is [knot refinement](/knot-refinement/) with one new knot. The model is the [real RAM](/real-ram/), with exact rational arithmetic in the implementation.

## The algorithm

```pseudo id=main
BOEHM-INSERT(t, p, P, u)                    ▷ t[p] ≤ u < t[n+1], mult(u) ≤ p
L1  μ ← the largest index with t[μ] ≤ u      ▷ binary search
L2  for i ← 0 to μ−p do Q[i] ← P[i]
L3  for i ← μ−p+1 to μ
L4      a ← (u − t[i]) / (t[i+p] − t[i])
L5      Q[i] ← (1 − a) · P[i−1] + a · P[i]
L6  for i ← μ+1 to n+1 do Q[i] ← P[i−1]
L7  t′ ← (t[0], …, t[μ], u, t[μ+1], …, t[n+p+1])
L8  return t′, Q
```

Line L1 finds the span $[t_\mu, t_{\mu+1})$ that contains $u$; then $p \le \mu \le n$. Line L2 keeps the points $P_0, \ldots, P_{\mu-p}$, whose B-splines end at or before $t_\mu$. Lines L3 to L5 make the $p$ new points $Q_{\mu-p+1}, \ldots, Q_\mu$. For each of them $t_i \le t_\mu \le u < t_{\mu+1} \le t_{i+p}$, so the denominator of line L4 is positive and $0 \le a \le 1$: $Q_i$ lies on the segment from $P_{i-1}$ to $P_i$. Line L6 keeps $P_\mu, \ldots, P_n$ with their index shifted by one. Line L7 puts $u$ after $t_\mu$. The weights use the old knots only.

## Example

Take $p = 2$, $t = (0, 0, 0, 1, 2, 3, 3, 3)$, the control points $P_0 = (0, 0)$, $P_1 = (1, 2)$, $P_2 = (3, 3)$, $P_3 = (5, 1)$, $P_4 = (6, 0)$, and $u = 3/2$. Line L1 gives $\mu = 3$, because $t_3 = 1 \le 3/2 < 2 = t_4$.

| Line | $i$ | knots $t_i$, $t_{i+p}$ | $a$ (L4) | new point |
|---|---|---|---|---|
| L2 | 0, 1 | | | $Q_0 = (0, 0)$, $Q_1 = (1, 2)$ |
| L5 | 2 | $0, 2$ | $3/4$ | $Q_2 = \tfrac14 (1, 2) + \tfrac34 (3, 3) = (5/2, 11/4)$ |
| L5 | 3 | $1, 3$ | $1/4$ | $Q_3 = \tfrac34 (3, 3) + \tfrac14 (5, 1) = (7/2, 5/2)$ |
| L6 | 4, 5 | | | $Q_4 = (5, 1)$, $Q_5 = (6, 0)$ |

The new knot vector is $(0, 0, 0, 1, 3/2, 2, 3, 3, 3)$. The corner $P_2$ is replaced by the two points $Q_2$ and $Q_3$ on its two legs. These are the points of round 1 of the [de Boor algorithm](/de-boor-algorithm/) at $u = 3/2$.

Insert $3/2$ a second time. Now $\mu = 4$; line L4 gives $a = (3/2 - 1)/(2 - 1) = 1/2$ for $i = 3$ and $a = 0$ for $i = 4$. The new points are $(0, 0), (1, 2), (5/2, 11/4), (3, 21/8), (7/2, 5/2), (5, 1), (6, 0)$. The middle point $(3, 21/8)$ is the curve point $C(3/2)$, and with $3/2$ of multiplicity $p = 2$ the curve passes through it.

## Correctness

The proof uses Marsden's identity $\sum_i \psi_i(y) N_{i,p}(x) = (y - x)^p$ with $\psi_i(y) = \prod_{r=1}^{p} (y - t_{i+r})$. First, lines L2 to L6 send the coefficients $\psi_i(y)$ of the old knots to the coefficients $\psi'_j(y)$ of the new knots, for every $y$. This is one line of algebra: for the new points, $(1 - a)(y - t_i) + a (y - t_{i+p}) = y - u$, and $u$ is the extra knot among $t'_{j+1}, \ldots, t'_{j+p}$. So the algorithm is right for every curve that is a polynomial $(y - x)^p$. Second, on each span of the new knots, the new points that act there depend only on the $p + 1$ old points that act there. The vectors $(\psi_i(y))_i$ for $p + 1$ distinct $y$ are a basis of these $p + 1$ coefficients, by a Vandermonde argument, so by linearity the two curves agree on each span. The full proof is below.

## Complexity

Line L1 costs $O(\log n)$ by [binary search](/binary-search/). Lines L3 to L5 do $p$ divisions and $p$ combinations of points, $\Theta(p d)$ operations. Lines L2, L6 and L7 copy $n + 2$ points and $n + p + 3$ knots, $\Theta(n d + p)$ work and space; an implementation that keeps the arrays with spare room at the end can shift only the tail and keeps the extra space at $O(p d)$. The implementation builds new lists, as in the pseudocode. So one insertion costs $\Theta(\log n + p d + n d)$ in the worst case.

## Properties

- **Local.** Only $Q_{\mu-p+1}, \ldots, Q_\mu$ are new. The points before them are the old points, and the points after them are the old points with the index shifted by one.
- **Corner cutting.** Each new point lies on the segment $P_{i-1} P_i$ of the old polygon, and the new points follow the old polygon in order. So the new polygon is the old one with the corners $P_{\mu-p+1}, \ldots, P_{\mu-1}$ cut off. This gives the [variation diminishing property](/variation-diminishing-property/): a line crosses the new polygon at most as often as the old one.
- **Convex weights.** The weights $a$ lie in $[0, 1]$, so the new points lie in the [convex hull](/convex-hull-property/) of the old ones, and rounding errors stay small.
- **Affine invariant.** The new points are affine combinations, so the algorithm commutes with affine maps of the control points.
- **Repeated insertion is de Boor.** If $u$ is not a knot, $p$ insertions of $u$ make the whole triangle of the [de Boor algorithm](/de-boor-algorithm/), and the middle point is $C(u)$. With $u$ of multiplicity $p$, the curve on the left of $u$ ends at that point and the curve on the right starts there. A $(p+1)$-th insertion only repeats the point, and it gives each half its own clamped knot vector.
- **The Bézier case.** On the knots $0^{p+1} 1^{p+1}$, all weights of line L4 equal $u$, and $p$ insertions of $u$ are the [de Casteljau algorithm](/de-casteljau-algorithm/), with its split of the Bézier curve at $u$.
- **Uniqueness.** By the [Curry-Schoenberg theorem](/curry-schoenberg-theorem/), the new B-splines are linearly independent on the domain, so the new points are the only ones that give the same curve.

## Variants and improvements

- **Insert a knot $r$ times.** Inserting the same $u$ $r \le p - s$ times, where $s$ is its old multiplicity, can be done in one routine that computes a triangle of $r$ rounds, as in the NURBS Book, Section 5.2. The rounds are the rounds of the de Boor algorithm.
- **Many knots.** For a sorted list of new knots, insert them from the largest to the smallest into one array with room for all new points, so that each point is copied once. This solves [knot refinement](/knot-refinement/) in $O(N d + k p d)$ for $k$ new knots and $N + 1$ final points. The [Oslo algorithm](/oslo-algorithm/) computes each final point directly instead.
- **NURBS.** For a [NURBS](/nurbs/) curve, apply the algorithm to the homogeneous points $(w_i P_i, w_i)$ and divide at the end. The new weights are the last coordinates.
- **Surfaces.** For a [tensor product surface](/tensor-product-surface/), insert a knot in $u$ into every row of the control net; the weights of line L4 are the same for all rows, so they are computed once.
- **Knot removal.** Lines L4 and L5 can be solved backwards for $P_{i-1}$ or $P_i$. This gives a test for whether a knot can be removed without changing the curve, and an approximate removal when it cannot.

## When to use it

Use it to add one knot, or a few knots, to a curve: to get more control points in one region, to split a curve at a parameter, or to convert a B-spline curve into Bézier pieces. It is short, exact for rational inputs, and stable. To insert many knots at once, for example in uniform subdivision, the [Oslo algorithm](/oslo-algorithm/) or the [Lane-Riesenfeld algorithm](/lane-riesenfeld-algorithm/) avoids the repeated copying of a naive loop over this algorithm. To compute only a curve point, the [de Boor algorithm](/de-boor-algorithm/) does the same arithmetic without storing the new points.

## Pitfalls

- **The order of lines L4 and L7.** Line L4 must use the old knots. An in-place version that puts $u$ into the knot array first, and then computes the weights from the changed array, finds $u$ or $t_{i+p-1}$ where it needs $t_{i+p}$, and gives wrong points.
- **The direction of an in-place line L5.** If $Q$ and $P$ share one array, line L5 must run from $i = \mu$ down to $\mu - p + 1$, after the shift of line L6. Running upward overwrites $P_{i-1}$ before the next step reads it.
- **The upper knot in line L4.** The denominator is $t_{i+p} - t_i$, the support of a B-spline of degree $p - 1$, not $t_{i+p+1} - t_i$.
- **Knots of multiplicity $p + 1$.** If $u$ already has multiplicity $p + 1$, for example $u = t_p$ on a clamped knot vector, line L4 gives $a = 0$ for every new point and a knot of multiplicity $p + 2$; the new first or last B-spline is zero on the domain and the new point is wasted. The precondition excludes this, and the implementation rejects it.
- **The right end.** For $u = t_{n+1}$ on a clamped knot vector, line L1 finds $\mu = n + p + 1$, and lines L4 and L5 read knots and points past the ends of the arrays. The domain is half-open at the right for this reason.
- **Rational curves.** For NURBS, line L5 must combine the homogeneous points $(w P, w)$. Combining the points $P$ and the weights $w$ separately changes the curve.

## Implementations

## History

Wolfgang Boehm published the insertion of one knot in "Inserting new knots into B-spline curves", Computer-Aided Design, 1980. In the same year, Elaine Cohen, Tom Lyche and Richard Riesenfeld published the Oslo algorithm, which refines a knot vector by many knots at once with discrete B-splines. The NURBS Book presents knot insertion, the insertion of one knot several times, and knot refinement as the basic tools for B-spline and NURBS curves and surfaces, and it relates repeated insertion to the de Boor algorithm.

## References
