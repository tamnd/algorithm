---
tag: NY6SD7
kind: definition
slug: halfspace-depth
name: Halfspace depth
aliases:
- Tukey depth
- location depth
area: statistics-and-inference/nonparametric-and-robust-statistics
level: advanced
summary: The depth of a point is the least number of data points in a closed halfspace that contains it. It orders multivariate data from the centre outward.
prereqs: [median, order-statistic, convex-hull]
see_also: [tukey-median, helly-theorem, convex-layers, geometric-median, breakdown-point, empirical-distribution-function, chans-randomized-optimization]
sources:
  - paper: "John W. Tukey, Mathematics and the picturing of data, in R. D. James (ed.), Proceedings of the International Congress of Mathematicians, Vancouver 1974, Volume 2, Canadian Mathematical Congress, Montreal, 1975, pp. 523 to 531"
    locator: The whole paper (depth of a point as the least number of data points in a halfplane that contains it, used to draw bivariate data)
  - paper: doi:10.1214/aos/1176348890
    title: David L. Donoho and Miriam Gasko, Breakdown properties of location estimates based on halfspace depth and projected outlyingness, The Annals of Statistics 20(4), 1992
    locator: pp. 1803 to 1827 (depth regions, the bound ceil(n/(d+1)) on the maximal depth, and the breakdown of the deepest point)
  - paper: "Peter J. Rousseeuw and Ida Ruts, Algorithm AS 307: Bivariate location depth, Journal of the Royal Statistical Society, Series C (Applied Statistics) 45(4), 1996, pp. 516 to 526"
    locator: The whole paper (the depth of one point in the plane in O(n log n) time by an angular sort)
  - paper: doi:10.1214/aos/1016218226
    title: Yijun Zuo and Robert Serfling, General notions of statistical depth function, The Annals of Statistics 28(2), 2000
    locator: pp. 461 to 482 (the four properties of a depth function, and the halfspace depth as the model case)
  - paper: "Greg Aloupis, Carmen Cortés, Francisco Gómez, Michael Soss and Godfried Toussaint, Lower bounds for computing statistical depth, Computational Statistics and Data Analysis 40(2), 2002, pp. 223 to 229"
    locator: The whole paper (an Omega(n log n) lower bound for the halfspace depth of one point in the plane)
  - paper: "David S. Johnson and Franco P. Preparata, The densest hemisphere problem, Theoretical Computer Science 6(1), 1978, pp. 93 to 107"
    locator: The whole paper (the densest hemisphere problem is NP-complete when the dimension is part of the input)
  - paper: "Rainer Dyckerhoff and Pavlo Mozharovskyi, Exact computation of the halfspace depth, Computational Statistics and Data Analysis 98, 2016, pp. 19 to 30"
    locator: The whole paper (exact algorithms in O(n^d) and O(n^(d-1) log n) time in dimension d)
---

The halfspace depth of a point $x$ in a data set is the least number of data points in a closed halfspace that contains $x$. A point deep inside the cloud has many points on every side, and a point outside the [convex hull](/convex-hull/) has depth 0. In one dimension it is the familiar rank depth of the [median](/median/): the depth of $x$ is the smaller of the number of points at or below $x$ and the number at or above $x$. Tukey proposed it in 1974 to draw bivariate data, and the deepest point is the [Tukey median](/tukey-median/).

## Definition

Let $X = (x_1, \ldots, x_n)$ be a sample of points in $\mathbb{R}^d$; points may repeat, and each copy counts. For a point $x \in \mathbb{R}^d$, the **halfspace depth** of $x$ in $X$ is
$$\operatorname{hd}(x; X) = \min_{H \ni x} \#\{i : x_i \in H\},$$
where $H$ runs over the closed halfspaces that contain $x$. A closed halfspace with $x$ on its boundary contains no more points than a larger parallel one, so it is enough to use the halfspaces with $x$ on the boundary:
$$\operatorname{hd}(x; X) = \min_{\|u\| = 1} \#\{i : u^\top x_i \ge u^\top x\}.$$
Some authors divide by $n$ and use the fraction in $[0, 1]$. For a probability distribution $P$ on $\mathbb{R}^d$, the population depth is $\operatorname{hd}(x; P) = \inf\{P(H) : H \text{ a closed halfspace with } x \in H\}$, and the sample depth divided by $n$ is the depth for the empirical distribution.

The **depth region** of level $k$ is $D_k = \{x : \operatorname{hd}(x; X) \ge k\}$. The **maximal depth** is $k^* = \max_x \operatorname{hd}(x; X)$, and a point with depth $k^*$ is a deepest point.

These facts follow from the definition.

- **Affine invariance.** For an invertible matrix $A$ and a vector $b$, $\operatorname{hd}(Ax + b; AX + b) = \operatorname{hd}(x; X)$, because $x \mapsto Ax + b$ maps closed halfspaces onto closed halfspaces.
- **Depth and the hull.** $\operatorname{hd}(x; X) \ge 1$ if and only if $x$ is in the convex hull of $X$. If $x$ is outside the hull, a hyperplane strictly separates $x$ from the hull, and the closed side of $x$ holds no point. If $x$ is in the hull and a closed halfspace $H \ni x$ held no data point, then all points would lie in the open complement of $H$, and so would their convex combination $x$.
- **Regions are convex.** $D_k$ is the intersection of all closed halfspaces that hold at least $n - k + 1$ points. If $x \notin H$ for such an $H = \{y : u^\top y \le c\}$, then $u^\top x > c$, and the closed halfspace $\{y : u^\top y \ge u^\top x\}$ holds $x$ and at most $k - 1$ points, so $\operatorname{hd}(x) < k$. If $\operatorname{hd}(x) \le k - 1$ by a direction $u$, then at least $n - k + 1$ points have $u^\top x_i < u^\top x$, and a slightly lower level $c < u^\top x$ gives such an $H$ that misses $x$. So each $D_k$ with $k \ge 1$ is a compact convex set, and $D_1 \supseteq D_2 \supseteq \cdots$.
- **Monotone along rays.** If $\theta$ is a deepest point, the depth does not increase along each ray that starts at $\theta$, because each region is convex and holds $\theta$. The depth falls to 0 outside the hull. Zuo and Serfling (2000) take affine invariance, a maximum at a centre, this monotonicity and the vanishing at infinity as the axioms of a statistical depth function. Halfspace depth is their model case.
- **The range of the maximal depth.** $\lceil n/(d+1) \rceil \le k^* \le n$. The lower bound is the centerpoint theorem, a consequence of [Helly's theorem](/helly-theorem/); the proof is on the [Tukey median](/tukey-median/) page. If the points are distinct, then $k^* \le \lceil n/2 \rceil$. Take a hyperplane through $x$ that misses all data points other than $x$. If $x$ is not a data point, the smaller closed side holds at most $\lfloor n/2 \rfloor$ points. If $x$ is a data point, it holds at most $\lfloor (n-1)/2 \rfloor$ other points plus $x$, which is $\lceil n/2 \rceil$.

The depth of one point in the plane takes $O(n \log n)$ time (Rousseeuw and Ruts 1996). Sort the vectors $x_i - x$ by angle and slide a half-turn around the circle; the [Tukey median](/tukey-median/) page gives the algorithm and its proof. This is optimal: Aloupis and others (2002) prove an $\Omega(n \log n)$ lower bound. In fixed dimension $d$, exact algorithms take $O(n^{d-1} \log n)$ time (Dyckerhoff and Mozharovskyi 2016). When $d$ is part of the input, the problem is the densest hemisphere problem, which is NP-complete (Johnson and Preparata 1978). So in high dimension one uses the minimum over a finite set of random directions, which is an upper bound on the depth.

## Examples and non-examples

**One dimension.** For the sample $(1, 2, 4, 7, 9)$ a closed halfspace is a closed half-line, so $\operatorname{hd}(x) = \min(\#\{x_i \le x\}, \#\{x_i \ge x\})$. The depths of the five points are $1, 2, 3, 2, 1$, and the point 5 has depth $\min(3, 2) = 2$. The deepest point is the median 4, with depth 3. For an even sample the deepest set is the whole median interval.

**Seven points in the plane.** Take
$$X = \{(0, 0), (6, 0), (0, 6), (6, 6), (2, 3), (3, 1), (9, 9)\}.$$
The depths of the seven data points are $1, 1, 1, 2, 2, 2, 1$. For $x = (3, 3)$, the vectors $x_i - x$ in angle order are $(3,3)$, $(6,6)$, $(-3,3)$, $(-1,0)$, $(-3,-3)$, $(0,-2)$, $(3,-3)$. Every half-open half-turn of directions holds at least 3 of them, and the half-turn that starts at $(-3,-3)$ holds exactly $(-3,-3)$, $(0,-2)$ and $(3,-3)$. So $\operatorname{hd}((3,3)) = 3$. A closed halfplane that shows it: the points on or below the line through $(3,3)$ with slope $9/11$. It holds $(0,0)$, $(3,1)$ and $(6,0)$ only. The maximal depth is $k^* = 3 = \lceil 7/3 \rceil$, and $D_3$ is the segment from $(18/7, 18/7)$ to $(3,3)$. The point $(9, 9)$ is far out, but it moves no part of $D_3$ off the diagonal. The [Tukey median](/tukey-median/) page builds $D_3$ step by step.

**Points outside the hull.** For the same $X$, the point $(9, 0)$ has depth 0: the closed halfplane $y \le x - 7$ holds it and holds no data point.

**Non-example: the coordinatewise median.** The coordinatewise median is not a deepest point in general, and it can have depth 0. For the three points $(1,0,0)$, $(0,1,0)$ and $(0,0,1)$ in $\mathbb{R}^3$, the coordinatewise median is $(0,0,0)$. It is not in the convex hull (the plane $x + y + z = 1$ holds all three points), so its depth is 0. The deepest points are the triangle itself, at depth 1. The coordinatewise median is also not affine equivariant.

**Non-example: the count in a ball.** The number of data points within distance $r$ of $x$ is a density estimate, not a depth. It is large inside a dense cluster at the edge of the cloud, and it changes under a linear change of scale. Halfspace depth is large only near the centre of the whole cloud.

## Related definitions

- **[Tukey median](/tukey-median/).** The centre of gravity of the deepest region $D_{k^*}$. Its breakdown point is at least $1/(d+1)$ for data in general position (Donoho and Gasko 1992).
- **Centerpoint.** A point of depth at least $\lceil n/(d+1) \rceil$. It always exists; the [Helly theorem](/helly-theorem/) page proves it.
- **Convex hull peeling depth.** The index of the [convex layer](/convex-layers/) that holds a point. It also orders points from the outside in, but it is not the same order as halfspace depth.
- **Simplicial depth.** Liu (1990): the number of simplices with vertices in the data that contain $x$. It is another affine invariant depth, with a different deepest point.
- **[Geometric median](/geometric-median/).** The minimizer of the sum of Euclidean distances. It has breakdown point 1/2, but it is only orthogonally equivariant, not affine equivariant.
- **[Empirical distribution function](/empirical-distribution-function/).** In one dimension, $\operatorname{hd}(x)/n = \min(F_n(x), 1 - F_n(x^-))$.

## References
