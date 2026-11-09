---
tag: 53KCKX
kind: problem
slug: geometric-median
name: Geometric median
aliases:
- Fermat-Weber point
- Weber problem
- Euclidean 1-median
- spatial median
- L1-median
area: geometry/geometric-optimization
level: core
summary: Find the point with the smallest sum of Euclidean distances to n given points. It is unique unless the points are collinear, has no formula in radicals in general, and is computed by iteration.
prereqs: [euclidean-distance, convex-function, median]
see_also: [weiszfelds-algorithm, fermat-point, k-median-problem, facility-location-problem, weighted-median, second-order-cone-programming, euclidean-k-median, minimum-enclosing-circle]
sources:
  - paper: doi:10.1007/BF01584648
    title: Harold W. Kuhn, A note on Fermat's problem, Mathematical Programming 4, 1973
    locator: the existence and uniqueness of the minimizer, the optimality condition at a data point, and Weiszfeld's iteration
  - paper: doi:10.1007/BF02187906
    title: Chanderjit Bajaj, The algebraic degree of geometric optimization problems, Discrete and Computational Geometry 3, 1988
    locator: the Weber problem is in general not solvable by radicals over the rationals
  - paper: doi:10.1073/pnas.97.4.1423
    title: Yehuda Vardi and Cun-Hui Zhang, The multivariate L1-median and associated data depth, Proceedings of the National Academy of Sciences 97(4), 2000
    locator: the L1-median in statistics and the modified Weiszfeld iteration
  - paper: "Guoliang Xue and Yinyu Ye, An efficient algorithm for minimizing a sum of Euclidean norms with applications, SIAM Journal on Optimization 7(4), 1997"
    locator: the interior-point method with a polynomial bound in n, d and log(1/ε)
  - paper: doi:10.1145/2897518.2897647
    title: Michael B. Cohen, Yin Tat Lee, Gary Miller, Jakub Pachocki and Aaron Sidford, Geometric median in nearly linear time, Proceedings of the 48th ACM Symposium on Theory of Computing (STOC 2016)
    locator: the abstract (a (1 + ε)-approximation by a long-step interior-point method in O(nd log^3(1/ε)) time, and by stochastic subgradient descent in O(d/ε^2) time)
  - paper: "Alfred Weber, Über den Standort der Industrien, Tübingen, 1909"
    locator: the weighted location problem for an industrial plant
---

The geometric median of points $a_1, \ldots, a_n \in \mathbb{R}^d$ is a point $x$ that minimizes the sum of [Euclidean distances](/euclidean-distance/) $\sum_i |x - a_i|$; with positive weights it is the Weber problem of [facility location](/facility-location-problem/). The cost is a [convex function](/convex-function/), so the minimizer exists, and it is unique unless all points lie on one line. For three points it is the [Fermat point](/fermat-point/), and on a line it is the ordinary [median](/median/). For five or more points there is in general no formula in radicals (Bajaj 1988), so the median is computed by iteration, classically by [Weiszfeld's algorithm](/weiszfelds-algorithm/).

## In plain words

Put several dots on a map. You want one spot so that the straight-line distances from it to all the dots add up to as little as possible. That spot is the geometric median.

On a line the answer is the middle dot, the ordinary median. In the plane there is no simple rule like "take the middle" or "take the average". The average point is pulled hard by one far-away dot; the geometric median is not, so it gives a center that a few bad dots cannot drag far. That is why statisticians use it as a robust center.

For three dots the answer has a classical construction. For many dots one finds it by repeated improvement: start somewhere, and take steps that each make the total distance smaller.

## Definition

Notation: $a_1, \ldots, a_n \in \mathbb{R}^d$ are the data points, $w_1, \ldots, w_n > 0$ the weights, $W = \sum_i w_i$, and $f(x) = \sum_i w_i |x - a_i|$; in the plane a point is $p = (x, y)$. Copies of one point can be merged by adding their weights. For $y \ne a_i$ let $u_i(y) = (a_i - y)/|a_i - y|$.

**Input.** The points and the weights; unit weights unless stated.

**Output.** A minimizer $x^*$ of $f$, or a point $y$ with $f(y) \le (1 + \varepsilon) f(x^*)$.

**Theorem.**

1. $f$ has a minimizer, and every minimizer lies in the convex hull of the data points.
2. If the data points do not all lie on one line, the minimizer is unique.
3. A point $y$ that is not a data point is a minimizer iff $\sum_i w_i u_i(y) = 0$.
4. A data point $a_k$ is a minimizer iff $\big|\sum_{i \ne k} w_i u_i(a_k)\big| \le w_k$ (Kuhn 1973).
5. If all points lie on a line, the minimizers on that line are its weighted medians: the points with at most $W/2$ of the weight strictly on each side.

*Proof.* $f$ is convex and $f(x) \ge W(|x| - \max_i |a_i|)$, so it has a minimizer. The projection onto the convex hull does not increase any distance to a data point and decreases all of them for a point outside, which gives part 1. For part 2, along a line that misses some $a_i$ the term $|x - a_i|$ is strictly convex, so $f$ is strictly convex along every line. Parts 3 and 4 come from the one-sided derivative $f'(y; v) = \eta - \langle \sum_i w_i u_i(y), v \rangle$, where $\eta$ is the weight at $y$ (0 if $y$ is not a data point); $y$ is a minimizer iff this is at least 0 for all unit $v$. Part 5 is the one-dimensional case of part 4, and by part 1 no point off the line does better. $\square$

General position is not needed. Collinear input has a segment of minimizers when the weight splits exactly in half, and part 5 describes it.

## Variants

- **Weighted (Weber problem).** Positive weights as above; Weber's 1909 model of where to place a plant between raw materials and a market.
- **Other norms.** With the $\ell_1$ norm the cost splits into one weighted median per coordinate, so the exact answer takes $O(nd)$ time. With other norms the condition of part 3 uses a subgradient of the norm.
- **$k$-median.** Place $k$ centers and charge each point the distance to its nearest center: the [$k$-median problem](/k-median-problem/), NP-hard in the plane, with a PTAS for fixed dimension ([Euclidean $k$-median](/euclidean-k-median/)).
- **Minimax instead of sum.** Minimizing the largest distance instead of the sum gives the [minimum enclosing circle](/minimum-enclosing-circle/), which has exact linear-time algorithms.
- **Constrained.** The center must lie in a given region or on a network, or avoid forbidden regions.
- **Medians of continuous sets.** The point that minimizes the integral of the distance over a polygon or a curve.

## Examples

**On a line.** For $0, 1, 5, 9, 10$ the median is $5$, with cost $5 + 4 + 0 + 4 + 5 = 18$. For $-3, 0, 2, 7$ every point of $[0, 2]$ is a median, with cost 12.

**Three points.** The median is the Fermat point: inside the triangle, with angles of 120 degrees to the corners, unless one angle is at least 120 degrees, in which case it is that corner. For $(0, 0), (4, 0), (1, 3)$ the cost is $\sqrt{22 + 12\sqrt{3}} \approx 6.5410$; for $(0, 0), (4, 0), (-1, 1)$ the median is $(0, 0)$, with cost $4 + \sqrt{2}$.

**Four points in convex position.** For $A = (0, 0), B = (4, 0), C = (5, 3), D = (0, 4)$, $f(x) = (|xA| + |xC|) + (|xB| + |xD|) \ge |AC| + |BD|$, with equality only on both diagonals. The diagonals meet at $(5/2, 3/2)$, which is the median, with cost $\sqrt{34} + 4\sqrt{2} \approx 11.4878$.

**One point inside the triangle of the other three.** For $(0, 0), (6, 0), (0, 6), (1, 1)$ the median is the inner point $(1, 1)$. Its three unit vectors to the others are $(-1, -1)/\sqrt{2}$, $(5, -1)/\sqrt{26}$ and $(-1, 5)/\sqrt{26}$; their sum has length about $0.1094 \le 1$, so part 4 holds. In general, three unit vectors that do not lie in an open half-plane have a sum of length at most 1, so the inner point of four points is always the median.

**A pentagon.** For $(0, 0), (4, 0), (5, 3), (3, 5), (0, 4)$ no vertex passes the test of part 4. The median is about $(2.64137, 2.64137)$, on the line of symmetry $x = y$, with cost about $14.447549$. It is not the centroid $(2.4, 2.4)$, whose cost is about $14.499660$.

## Known algorithms

| method | guarantee | time |
|---|---|---|
| weighted median | exact, points on a line | $O(n)$ |
| construction | exact, $n = 3$ and $n = 4$ in the plane | $O(1)$ |
| best data point | cost at most $2 f(x^*)$ | $O(n^2 d)$ |
| [Weiszfeld's algorithm](/weiszfelds-algorithm/) with the Kuhn or Vardi-Zhang step | cost tends to $f(x^*)$ from every start | $O(nd)$ per step |
| interior-point method for the [second-order cone program](/second-order-cone-programming/) (Xue and Ye 1997) | accuracy $\varepsilon$ | polynomial in $n$, $d$ and $\log(1/\varepsilon)$ |
| Cohen, Lee, Miller, Pachocki and Sidford (2016) | factor $1 + \varepsilon$ | $O(nd \log^3(1/\varepsilon))$, as stated in their abstract |
| stochastic subgradient descent (same paper) | factor $1 + \varepsilon$, randomized | $O(d/\varepsilon^2)$ |

**The best data point is within a factor of 2.** Let $a_j$ be the data point nearest to $x^*$. Then $f(a_j) \le \sum_i w_i (|a_i - x^*| + |x^* - a_j|) = f(x^*) + W |x^* - a_j|$, and $W |x^* - a_j| \le \sum_i w_i |x^* - a_i| = f(x^*)$. So $f(a_j) \le 2 f(x^*)$.

## Bounds

- **No formula.** Bajaj (1988) shows that the Weber problem is in general not solvable by radicals over the rationals. So no exact algorithm exists in a model of computation that allows only arithmetic and the extraction of $k$-th roots, and the coordinates of the median are given only to a chosen accuracy.
- **Reading the input.** Any algorithm with a bounded approximation factor must read all $nd$ coordinates, so $\Omega(nd)$ time.
- **Robustness.** The geometric median has breakdown point $1/2$: moving fewer than half of the points (by weight) arbitrarily far moves the median only a bounded distance. The mean has breakdown point 0.

## Reductions

- **To a cone program.** Minimize $\sum_i w_i t_i$ subject to $|x - a_i| \le t_i$: a second-order cone program with $n$ cones of dimension $d + 1$.
- **From the Fermat point.** The case $n = 3$ is the [Fermat point](/fermat-point/), with the 120 degree rule.
- **To one dimension.** For collinear points, or for the $\ell_1$ norm, the problem becomes the [weighted median](/weighted-median/).
- **Inside $k$-median.** Each step of a Lloyd-type heuristic for $k$-median solves one geometric median per cluster.

## Applications

- **Facility location.** Place a warehouse, a school or an antenna to minimize the total travel distance to its users, with weights for demand.
- **Robust statistics.** The spatial median, or L1-median, is a multivariate center that resists outliers, and it leads to the data depth of Vardi and Zhang.
- **Robust aggregation.** Distributed and federated learning systems combine the updates of many clients by a geometric median, so that a minority of faulty clients cannot steer the result.
- **Clustering.** The centers of [$k$-median](/k-median-problem/) clustering are geometric medians of their clusters.

## References
