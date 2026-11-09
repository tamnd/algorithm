---
tag: NZ3VS5
kind: problem
slug: minimum-enclosing-ball
name: Minimum enclosing ball
aliases:
- smallest enclosing ball
- minimum bounding sphere
- smallest enclosing sphere
- Euclidean 1-center problem in d dimensions
area: geometry/geometric-optimization
level: core
summary: Find the smallest ball that contains n points in d dimensions. It is unique and fixed by at most d+1 points; linear time in fixed dimension, and core-set approximations in high dimension.
prereqs: [minimum-enclosing-circle, convex-set, caratheodory-theorem, convex-optimization-problem]
see_also: [welzls-algorithm, badoiu-clarkson-algorithm, lp-type-problem, clarksons-algorithm, megiddo-fixed-dimension-lp, coreset, minimum-volume-enclosing-ellipsoid, k-center-problem]
sources:
  - paper: doi:10.1007/BFb0038202
    title: Emo Welzl, Smallest enclosing disks (balls and ellipsoids), in New Results and New Trends in Computer Science, Lecture Notes in Computer Science 555, Springer, 1991
    locator: Section 3, Balls (Lemma 1 with d + 1 in place of 3, and Theorem 3, expected O(δ δ! n) time with δ = d + 1)
  - paper: doi:10.1145/2422.322418
    title: Nimrod Megiddo, Linear programming in linear time when the dimension is fixed, Journal of the ACM 31(1), 1984
    locator: the prune-and-search method in fixed dimension that the one-center algorithms build on
  - paper: "Martin E. Dyer, On a multidimensional search technique and its application to the Euclidean one-centre problem, SIAM Journal on Computing 15(3), 1986"
    locator: the deterministic linear-time algorithm for the Euclidean one-center problem in fixed dimension
  - paper: "Mihai Bădoiu and Kenneth L. Clarkson, Optimal core-sets for balls, Computational Geometry 40(1), 2008"
    locator: core sets of size ceil(1/ε) for the (1 + ε)-approximate minimum enclosing ball, and the matching lower bound
  - paper: "Bernd Gärtner, Fast and robust smallest enclosing balls, Proceedings of the 7th European Symposium on Algorithms (ESA 1999), Lecture Notes in Computer Science 1643, Springer, 1999"
    locator: the move-to-front and pivoting code for balls in moderate dimension
  - paper: "Heinrich Jung, Über die kleinste Kugel, die eine räumliche Figur einschliesst, Journal für die reine und angewandte Mathematik 123, 1901"
    locator: the bound r ≤ D (d / (2(d + 1)))^(1/2) between the radius and the diameter
---

The minimum enclosing ball problem asks for the ball of smallest radius that contains $n$ given points in $\mathbb{R}^d$. It is the $d$-dimensional form of the [minimum enclosing circle](/minimum-enclosing-circle/). The ball is unique, its center lies in the convex hull of the points on its sphere, and at most $d + 1$ of those points fix it. In fixed dimension it takes $O(n)$ time, by [prune and search](/prune-and-search/) or by [Welzl's algorithm](/welzls-algorithm/); in high dimension one computes a $(1 + \varepsilon)$-approximation with a [coreset](/coreset/) of only $\lceil 1/\varepsilon \rceil$ points.

## In plain words

You have a cloud of points in space, maybe in many dimensions, and you want the smallest round ball that holds them all. The ball touches a few of the points on its surface, and those few points decide it: in the plane two or three points, in space at most four, and in general one more than the number of dimensions. The center of the ball lies among the touching points, never off to one side of all of them.

In two or three dimensions there are exact methods that look at each point only a few times. In hundreds of dimensions those methods become too slow, but a simple loop that walks the center toward the farthest point gets within any wanted fraction of the best radius, and it needs only a handful of the points to do it.

## Definition

Notation: $P = \{p_1, \ldots, p_n\} \subset \mathbb{R}^d$ is the input point set, $n = |P|$, $d$ the dimension, and $B(z, r) = \{x : |x - z| \le r\}$ a closed ball.

**Input.** A finite nonempty set $P \subset \mathbb{R}^d$.

**Output.** The center $z^*$ and the radius $r^*$ of the smallest ball that contains $P$:

$$r^* = \min_{z \in \mathbb{R}^d} \max_{1 \le i \le n} |p_i - z|.$$

**Theorem.** (a) The minimum is attained at exactly one center $z^*$. (b) Let $S^* = \{p \in P : |p - z^*| = r^*\}$. Then $z^* \in \operatorname{conv} S^*$. (c) Some set of at most $d + 1$ points of $S^*$, affinely independent, has the same smallest ball. (d) A ball that contains $P$ and whose center lies in the convex hull of the points of $P$ on its sphere is the smallest one.

*Proof.* (a) The function $g(z) = \max_i |p_i - z|^2$ is strictly convex, as a maximum of strictly convex functions, and it tends to infinity, so it has exactly one minimizer. (b) If $z^* \notin \operatorname{conv} S^*$, the separation theorem gives a unit vector $u$ with $\langle s - z^*, u \rangle > 0$ for all $s \in S^*$. For small $\tau > 0$, $|s - z^* - \tau u|^2 = r^{*2} - 2\tau \langle s - z^*, u \rangle + \tau^2 < r^{*2}$, and the other points stay strictly inside, so $g(z^* + \tau u) < g(z^*)$, a contradiction. (c) By [Carathéodory's theorem](/caratheodory-theorem/), $z^*$ is a convex combination $\sum_{s \in T} \lambda_s s$ of an affinely independent set $T \subseteq S^*$ with $|T| \le d + 1$. Part (d) applied to $T$ shows that the smallest ball of $T$ is the same ball. (d) Let $z = \sum_s \lambda_s s$ be such a center, with $\lambda \ge 0$, $\sum \lambda_s = 1$, and all $s$ at distance $r$. For any $w$, $\sum_s \lambda_s \langle s - z, w - z \rangle = 0$, so some $s$ has $\langle s - z, w - z \rangle \le 0$, and then $|s - w|^2 = r^2 + |w - z|^2 - 2 \langle s - z, w - z \rangle \ge r^2$. So no ball with another center and a smaller radius contains $P$. $\square$

**Duality.** For weights $\lambda$ in the simplex $\Delta_n = \{\lambda \ge 0, \sum_i \lambda_i = 1\}$ let $c_\lambda = \sum_i \lambda_i p_i$ and $\varphi(\lambda) = \sum_i \lambda_i |p_i|^2 - |c_\lambda|^2$. Then

$$r^{*2} = \max_{\lambda \in \Delta_n} \varphi(\lambda), \qquad z^* = c_{\lambda^*}.$$

Weak duality: for every $z$, $\max_i |p_i - z|^2 \ge \sum_i \lambda_i |p_i - z|^2 = \varphi(\lambda) + |c_\lambda - z|^2 \ge \varphi(\lambda)$. Equality: take $\lambda^*$ from part (b), supported on $S^*$; then $\varphi(\lambda^*) = \sum_s \lambda^*_s |s - z^*|^2 = r^{*2}$. The dual is a concave [quadratic program](/quadratic-programming/) over the simplex, which is the form that Frank-Wolfe style methods such as [Badoiu-Clarkson](/badoiu-clarkson-algorithm/) work on.

General position is not needed. Points on the sphere may be many and affinely dependent, and duplicates change nothing.

## Variants

- **Plane.** $d = 2$ is the [minimum enclosing circle](/minimum-enclosing-circle/).
- **Balls of balls.** The smallest ball that contains given balls; it is still [LP-type](/lp-type-problem/), but its base cases need more care than for points.
- **Ellipsoids.** The [minimum-volume enclosing ellipsoid](/minimum-volume-enclosing-ellipsoid/), which is affine invariant where the ball is not.
- **$k$ centers.** Cover the points by $k$ balls of the smallest common radius: the [k-center problem](/k-center-problem/), NP-hard when $k$ is part of the input.
- **Outliers and streams.** Smallest ball of all but $k$ points; and one-pass streaming approximations.
- **Kernel version.** In a feature space given by a kernel, the smallest enclosing ball is the core step of support vector data description and of core-set training of [support vector machines](/support-vector-machine/).

## Examples

All values are exact; a ball is given by its center and its squared radius.

| points | center | $r^2$ | fixed by |
|---|---|---|---|
| the 8 corners of the cube $\{0, 2\}^3$ | (1, 1, 1) | 3 | any two opposite corners |
| (0, 0, 0), (4, 0, 0), (0, 4, 0), (0, 0, 4) | (4/3, 4/3, 4/3) | 32/3 | the face (4, 0, 0), (0, 4, 0), (0, 0, 4) |
| (0, 0, 0), (2, 0, 0), (0, 2, 0), (0, 0, 2), (1, 1, 1) | (2/3, 2/3, 2/3) | 8/3 | the face (2, 0, 0), (0, 2, 0), (0, 0, 2) |

The second row is the trap of this problem. The sphere through all four points has center $(2, 2, 2)$ and $r^2 = 12$. But $(2, 2, 2)$ lies outside the tetrahedron, because its coordinates sum to $6 > 4$, so by part (b) that sphere is not the answer. The smallest ball is the circumscribed ball of the far face: its center $(4/3, 4/3, 4/3)$ is the centroid of that face, the three face vertices are at squared distance $32/3$, and the origin is at squared distance $16/3$. In the third row the point $(1, 1, 1)$ is at squared distance $1/3$ from the center, deep inside.

## Known algorithms

| algorithm | time | kind |
|---|---|---|
| all subsets of at most $d + 1$ points | $O(n^{d+2})$ | exact, brute force |
| Megiddo (1984), Dyer (1986) | $O(n)$ for fixed $d$, with a constant exponential in $d^2$ or worse | deterministic |
| [Welzl's algorithm](/welzls-algorithm/) (1991) | $O((d + 1)!\, n)$ expected containment tests | randomized, exact |
| [Clarkson's algorithm](/clarksons-algorithm/) and other [LP-type](/lp-type-problem/) solvers | $O(d^2 n)$ plus terms of lower order in $n$ (of order $\sqrt{n} \log n$ and $\log n$, times factors in $d$), expected | randomized, exact |
| Gärtner's code (1999) | fast in practice up to moderate $d$ | move-to-front with pivoting |
| [Badoiu-Clarkson](/badoiu-clarkson-algorithm/) iteration | $O(nd / \varepsilon^2)$ | $(1 + \varepsilon)$-approximation, any $d$ |
| core-set methods with a solver for small instances | $O(nd / \varepsilon)$ plus a term in $d$ and $1/\varepsilon$ | $(1 + \varepsilon)$-approximation |
| interior-point methods for the [second-order cone program](/second-order-cone-programming/) | polynomial in $n$, $d$ and $\log(1/\varepsilon)$ | additive accuracy $\varepsilon$ |

## Bounds

- **Fixed dimension.** $\Theta(n)$: each point must be read, and $O(n)$ is achieved deterministically and in expectation.
- **Dimension as a parameter.** Reading the input takes $\Omega(nd)$. The exact algorithms above pay at least a factor exponential or subexponential in $d$; no exact algorithm polynomial in both $n$ and $d$ is claimed here.
- **Core sets.** For every $\varepsilon > 0$ there is a subset of $\lceil 1/\varepsilon \rceil$ points whose smallest ball, grown by the factor $1 + \varepsilon$, contains $P$, independent of $n$ and $d$. Bădoiu and Clarkson show that this size is optimal in the worst case.
- **Jung's theorem.** $\frac{1}{2} D \le r^* \le D \sqrt{d / (2(d + 1))}$, where $D$ is the diameter of $P$; the upper bound holds with equality for a regular simplex.

## Reductions

- **To a second-order cone program.** Minimize $r$ subject to $|p_i - z| \le r$ for all $i$.
- **To a quadratic program.** The dual above: maximize $\varphi$ over the simplex.
- **As an LP-type problem.** The constraints are the points, the value is $r^*$ of a subset, and the combinatorial dimension is $d + 1$. Every LP-type algorithm applies, with the base case "smallest ball of at most $d + 2$ points".
- **Lifting.** The map $p \mapsto (p, |p|^2)$ in $\mathbb{R}^{d+1}$ turns "the ball contains $p$" into a linear inequality in $(z, r^2 - |z|^2)$, but the objective stays quadratic.

## Applications

- **Bounding volumes.** Spheres are the cheapest bounding volume for [collision detection](/collision-detection/) and for culling in graphics.
- **Facility location.** The minimax placement of one center ([facility location](/facility-location-problem/)).
- **Machine learning.** Support vector data description, core vector machines, and the radius term in margin bounds.
- **Clustering and nearest-neighbor search.** Ball trees and $k$-center clustering use enclosing balls of groups.

## References
