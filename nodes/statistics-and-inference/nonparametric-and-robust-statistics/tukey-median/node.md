---
tag: ES2QKG
kind: algorithm
slug: tukey-median
name: Tukey median
aliases:
- halfspace median
- deepest point
area: statistics-and-inference/nonparametric-and-robust-statistics
level: research
summary: The point of maximal halfspace depth, a multivariate median with breakdown point at least 1/(d + 1). In the plane it can be computed in O(n log n) expected time.
model: real-ram
complexity:
  vars: {n: the number of points in the plane}
  time: {worst: O(n^3 log n), best: O(n^3 log n)}
  space: {extra: O(n^3)}
properties: {deterministic: true, exact_in_exact_arithmetic: true, affine_equivariant: true, in_place: false, online: false}
history:
  year: 1975
  people: [John W. Tukey, David L. Donoho, Miriam Gasko, Peter J. Rousseeuw, Ida Ruts, Timothy M. Chan]
  note: Tukey proposed halfspace depth at the 1974 International Congress of Mathematicians. Donoho and Gasko proved the breakdown bound in 1992, and Chan gave an optimal randomized algorithm for the plane in 2004.
prereqs: [halfspace-depth, median, helly-theorem, convex-hull, binary-search]
see_also: [geometric-median, convex-layers, chans-randomized-optimization, breakdown-point, line-arrangement, minimum-covariance-determinant, theil-sen-estimator]
sources:
  - paper: doi:10.1214/aos/1176348890
    title: David L. Donoho and Miriam Gasko, Breakdown properties of location estimates based on halfspace depth and projected outlyingness, The Annals of Statistics 20(4), 1992
    locator: pp. 1803 to 1827 (the maximal depth is at least ceil(n/(d+1)), the breakdown point of the deepest point, and its limit 1/3 for symmetric distributions)
  - paper: "John W. Tukey, Mathematics and the picturing of data, in R. D. James (ed.), Proceedings of the International Congress of Mathematicians, Vancouver 1974, Volume 2, Canadian Mathematical Congress, Montreal, 1975, pp. 523 to 531"
    locator: The whole paper (halfspace depth and the deepest point as a bivariate median)
  - paper: "Peter J. Rousseeuw and Ida Ruts, Constructing the bivariate Tukey median, Statistica Sinica 8(3), 1998, pp. 827 to 839"
    locator: The whole paper (the median as the centre of gravity of the deepest region, a direct O(n^5 log n) method and the HALFMED algorithm in O(n^2 log^2 n) time)
  - paper: "Peter J. Rousseeuw and Ida Ruts, Algorithm AS 307: Bivariate location depth, Journal of the Royal Statistical Society, Series C (Applied Statistics) 45(4), 1996, pp. 516 to 526"
    locator: The whole paper (the depth of one point in O(n log n) time)
  - paper: doi:10.1023/A:1023208625954
    title: K. Miller, S. Ramaswami, P. J. Rousseeuw, J. A. Sellarès, D. Souvaine, I. Streinu and A. Struyf, Efficient computation of location depth contours by methods of computational geometry, Statistics and Computing 13(2), 2003
    locator: pp. 153 to 162 (all depth contours in O(n^2) time by a topological sweep of the dual arrangement)
  - paper: "Timothy M. Chan, An optimal randomized algorithm for maximum Tukey depth, Proceedings of the Fifteenth Annual ACM-SIAM Symposium on Discrete Algorithms (SODA 2004), 2004"
    locator: The whole paper (the deepest point in the plane in O(n log n) expected time, and in O(n^(d-1)) expected time for d >= 3)
  - book: isbn:9780387953748
    title: Jiří Matoušek, Lectures on Discrete Geometry, Springer, 2002
    locator: Section 1.3 (Helly's theorem) and Section 1.4 (the centerpoint theorem)
---

The Tukey median of a cloud of points is the deepest point in the sense of [halfspace depth](/halfspace-depth/): every closed halfspace that contains it also contains many data points. In $d$ dimensions its depth is at least $\lceil n/(d+1) \rceil$, so it stays bounded while fewer than about $n/(d+1)$ points are replaced by outliers. It is affine equivariant, which the coordinatewise median and the [geometric median](/geometric-median/) are not. This page gives an exact algorithm for the plane that is easy to check, and lists the faster ones.

## In plain words

Put pins on a map, one for each data point. Pick a spot and draw any straight line through it. Count the pins on the side of the line where there are fewer. The worst count over all lines is the depth of the spot. A spot near the edge of the cloud has a line with almost no pins on one side, so it is shallow. A spot in the middle has many pins on every side.

The Tukey median is the deepest spot. If several spots tie, they form a convex region, and we take its centre of gravity. A few wild points far away cannot pull the deepest spot far, because each of them adds at most one pin to each side.

## The problem

The input is a sample $P = (p_1, \ldots, p_n)$ of points in the plane; repeated points are allowed. Let $\operatorname{hd}(x)$ be the halfspace depth of $x$ in $P$, and $D_k = \{x : \operatorname{hd}(x) \ge k\}$ the depth region of level $k$. The output is the maximal depth $k^* = \max_x \operatorname{hd}(x)$ and the Tukey median $T(P)$, the centre of gravity of $D_{k^*}$. This tie rule is the one of Donoho and Gasko (1992) and of Rousseeuw and Ruts (1998). When all points lie on one line, $D_{k^*}$ is the one-dimensional median interval on that line, and $T(P)$ is its midpoint.

## The algorithm

DEPTH computes the depth of one point. TUKEY-MEDIAN searches for the largest $k$ with $D_k \ne \emptyset$. REGION builds $D_k$ by clipping a box with one halfplane for each critical direction. For a direction $u$, the $k$-th largest of $u^\top p_1, \ldots, u^\top p_n$ is written $q_u(k)$.

```pseudo id=main
DEPTH(x, P)                                ▷ the halfspace depth of x
L1  k0 ← the number of points of P equal to x
L2  D ← the vectors p − x for the points p ≠ x;  m ← |D|
L3  sort D by polar angle, exactly             ▷ upper or lower half, then the sign of a cross product
L4  best ← m;  e ← 0
L5  for each j in 0 .. m − 1 that starts a group of equal angle do
L6      e ← max(e, j)
L7      while e < j + m and angle(D[e mod m]) ∈ [angle(D[j]), angle(D[j]) + π) do e ← e + 1
L8      best ← min(best, e − j, m − (e − j))
L9  return k0 + best

TUKEY-MEDIAN(P)
L10 if all points of P lie on one line then return the midpoint of the median interval on it
L11 U ← the two normals ±(a₂ − b₂, b₁ − a₁) of each pair of points a ≠ b
L12 for each u in U, sort the projections uᵀp, p in P, in decreasing order
L13 lo ← ⌈n/3⌉;  hi ← n                       ▷ D_lo is not empty by the centerpoint theorem
L14 while lo < hi do
L15     k ← ⌈(lo + hi)/2⌉
L16     if REGION(k) ≠ ∅ then lo ← k else hi ← k − 1
L17 R ← REGION(lo)
L18 return the centre of gravity of R, and k* = lo

REGION(k)                                  ▷ D_k as a convex polygon
L19 R ← the bounding box of P
L20 for each u in U do
L21     q ← q_u(k)                              ▷ the k-th largest projection
L22     R ← R ∩ {x : uᵀx ≤ q}                   ▷ clip a convex polygon by a halfplane
L23     if R = ∅ then return ∅
L24 return R
```

The idea of REGION is that the depth of $x$ is at least $k$ exactly when, for every direction $u$, at least $k$ points project at or beyond $x$, that is $u^\top x \le q_u(k)$. Between two directions where two projections swap, the $k$-th point does not change, so it is enough to test the directions of $U$. The centre of gravity in line L18 is the area centroid of a polygon, the midpoint of a segment, or the point itself.

## Example

Take the seven points
$$P = \{(0, 0), (6, 0), (0, 6), (6, 6), (2, 3), (3, 1), (9, 9)\}.$$
Three of the 21 pairs, on the diagonal, give the same normals, so $U$ has 32 distinct directions. The depths of the data points are $1, 1, 1, 2, 2, 2, 1$.

**Depth of one point.** For $x = (3, 3)$, line L3 sorts the seven vectors $p - x$ by angle:

| vector | angle | in the half-turn $[\theta_j, \theta_j + \pi)$ | outside |
|---|---|---|---|
| (3, 3), (6, 6) | 45° | 4 | 3 |
| (−3, 3) | 135° | 4 | 3 |
| (−1, 0) | 180° | 4 | 3 |
| (−3, −3) | 225° | 3 | 4 |
| (0, −2) | 270° | 4 | 3 |
| (3, −3) | 315° | 3 | 4 |

The smallest entry is 3, and $k_0 = 0$, so $\operatorname{hd}((3,3)) = 3$. The half-turn that starts at $(-3, -3)$ holds the points $(0,0)$, $(3,1)$ and $(6,0)$. They are the points on or below the line through $(3, 3)$ with slope $9/11$.

**The search.** Line L13 sets $lo = \lceil 7/3 \rceil = 3$ and $hi = 7$.

| step | $k$ | REGION($k$) | new range |
|---|---|---|---|
| 1 | 5 | empty | [3, 4] |
| 2 | 4 | empty | [3, 3] |

The regions of the levels that are not empty are:

| $k$ | $D_k$ |
|---|---|
| 1 | the hull, with vertices (0, 0), (6, 0), (9, 9), (0, 6) |
| 2 | the hexagon (3, 1), (6, 5), (6, 6), (11/2, 6), (2, 3), (36/19, 54/19) |
| 3 | the segment from (18/7, 18/7) to (3, 3) |

So $k^* = 3$, and the Tukey median is the midpoint of the segment, $(39/14, 39/14) \approx (2.786, 2.786)$. The mean is $(26/7, 25/7) \approx (3.71, 3.57)$; the point $(9, 9)$ pulls it up and to the right. If $(9,9)$ moves to $(900, 900)$, the program gives the same $D_3$ and the same Tukey median, while the mean moves to about $(131, 130.9)$. If it moves to $(900, -900)$, the Tukey median moves only to about $(3.06, 2.08)$, inside the hull of the six other points.

## Correctness

DEPTH is correct because the closed halfplanes through $x$ correspond to closed half-turns of directions, and the least count over closed half-turns equals the least count over the half-open half-turns $[\theta_j, \theta_j + \pi)$ and their complements; the two-pointer loop counts each of these. REGION is correct because the depth condition $u^\top x \le q_u(k)$ for the finitely many directions of $U$ implies it for all directions: between two neighbours $a, b \in U$ the $k$-th point $p_s$ is fixed, and each direction between them is a nonnegative combination of $a$ and $b$. The binary search is correct because the regions are nested and $D_{\lceil n/3 \rceil}$ is not empty.

**The centerpoint bound.** In $\mathbb{R}^d$, $k^* \ge \lceil n/(d+1) \rceil$. Let $k = \lceil n/(d+1) \rceil$. The region $D_k$ is the intersection of the closed halfspaces that hold at least $n - k + 1$ points. Replace each such halfspace by the convex hull of the points in it. Any $d + 1$ of these hulls share a data point, because together they miss at most $(d+1)(k-1) < n$ points. By [Helly's theorem](/helly-theorem/) all the hulls share a point, and it lies in $D_k$. The bound is tight: for three tight groups of $n/3$ points at the corners of a large triangle, $k^* = n/3$. The full proofs are below.

## Complexity

- **DEPTH** takes $O(n \log n)$ time for the sort, then $O(n)$ for the loop. This is optimal: Aloupis and others proved an $\Omega(n \log n)$ lower bound in 2002.
- **TUKEY-MEDIAN as written.** $|U| \le n(n-1)$. The sorts of line L12 take $O(n^3 \log n)$ time and $O(n^3)$ space. Every polygon in REGION has at most $2n + 4$ vertices, because each edge lies on a line through a data point, and at most two edge lines of a convex polygon pass through one point. So one clip takes $O(n)$ time, REGION takes $O(n^3)$, and the binary search adds a factor $O(\log n)$. The total is $O(n^3 \log n)$ time.
- **Faster algorithms.** Rousseeuw and Ruts (1998) compute the median in $O(n^2 \log^2 n)$ time with HALFMED. Miller and others (2003) compute all the depth contours in $O(n^2)$ time by a topological sweep of the dual line arrangement. Chan (2004) finds a deepest point in the plane in $O(n \log n)$ expected time, which is optimal, by his randomized optimization technique (see [Chan's randomized optimization](/chans-randomized-optimization/)). For $d \ge 3$ his algorithm takes $O(n^{d-1})$ expected time.

## Properties

- **Affine equivariant.** $T(AP + b) = A\,T(P) + b$ for each invertible $A$, because depth is affine invariant and the centre of gravity commutes with affine maps.
- **Breakdown point.** By Donoho and Gasko (1992), for data in general position in $\mathbb{R}^d$ the [breakdown point](/breakdown-point/) $\varepsilon^*_n(T, X)$ is at least $1/(d+1)$, up to rounding, and for samples from an absolutely continuous centrosymmetric distribution it tends to $1/3$ in every dimension. The idea of the lower bound: $m$ replaced points change each halfplane count by at most $m$, so while $m$ is small the clean points keep a region of depth larger than $m$ inside their hull, and no deep point can go far.
- **Not unique without a rule.** $D_{k^*}$ can be a polygon, a segment or a point. The centre of gravity is a convention. Any point of $D_{k^*}$ is a deepest point.
- **In one dimension** it is the ordinary [median](/median/), with the midpoint rule for an even sample.
- **Exact.** With integer or rational input, all the steps use exact rational arithmetic.

## Variants and improvements

- **Depth contours.** The regions $D_1 \supseteq D_2 \supseteq \cdots$ describe the shape of the cloud. The bagplot of Rousseeuw, Ruts and Tukey (1999) draws the region that holds half the points around the Tukey median, a bivariate box plot.
- **Approximate depth in high dimension.** The minimum of $N_u(x)$ over a finite random set of directions $u$ is an upper bound on the depth. Exact depth in dimension $d$ takes $O(n^{d-1} \log n)$ time (Dyckerhoff and Mozharovskyi 2016), and with $d$ in the input it is NP-hard (see [halfspace depth](/halfspace-depth/)).
- **Projection depth and other depths.** Donoho and Gasko (1992) also study a depth from projected outlyingness, $\sup_u |u^\top x - \operatorname{med}(u^\top X)| / \operatorname{MAD}(u^\top X)$, with the [median absolute deviation](/median-absolute-deviation/). Its deepest point has breakdown near 1/2, at a higher cost.
- **Regression depth.** Rousseeuw and Hubert define a depth for regression lines in the same spirit; the deepest line is a robust fit, with breakdown near 1/3, like the [Theil-Sen estimator](/theil-sen-estimator/) of about 0.29.

## When to use it

Use the Tukey median for a robust centre of two- or three-dimensional data when the answer must not depend on the units or the orientation of the axes. Use it with the depth contours to draw and to trim bivariate data. In more than a few dimensions the exact computation is too slow; there the [minimum covariance determinant](/minimum-covariance-determinant/) or a projection method is the practical choice. If rotation equivariance is enough, the [geometric median](/geometric-median/) is cheaper and breaks down at 1/2.

## Pitfalls

- **Floating-point angles.** Sorting by `atan2` puts almost parallel vectors in the wrong order, and the depth can be wrong by one. Compare angles by the half of the plane and the sign of a cross product, in exact arithmetic when you can.
- **Counting only one side.** The half-turns that start at a data direction do not cover all halfplanes. Line L8 must also use the complement $m - (e - j)$. Without it, the depth of $(0, 0)$ in the points $(0,0)$, $(4,0)$, $(0,4)$, $(4,4)$ comes out as 2, not 1.
- **Collinear data.** If all points are on one line, the two-dimensional regions are segments and the normals of $U$ are all parallel. Treat this case by the one-dimensional median, as line L10 does.
- **Repeated points.** Each copy counts in the depth. A point equal to $x$ is in every halfplane through $x$, which is why line L1 counts them apart.
- **Breakdown is not 1/2.** The Tukey median tolerates about one third of bad points in the plane, and fewer in higher dimension. A claim of 50 percent is wrong.
- **The deepest data point is not the Tukey median.** The deepest data point can be much shallower than $k^*$; in the example the data points have depth at most 2, while $k^* = 3$.

## Implementations

## History

Tukey introduced halfspace depth in his address "Mathematics and the picturing of data" at the International Congress of Mathematicians in Vancouver in 1974, published in 1975, as a tool to draw bivariate data. Donoho and Gasko (1992) studied the deepest point as an estimator and proved its breakdown properties. Rousseeuw and Ruts gave the $O(n \log n)$ depth algorithm in 1996 and the first practical median algorithm in 1998, and Miller and others computed all contours in $O(n^2)$ time in 2003. Chan closed the question of the planar time bound with an expected $O(n \log n)$ algorithm in 2004.

## References
