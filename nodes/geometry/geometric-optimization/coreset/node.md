---
tag: ATXA1G
kind: concept
slug: coreset
name: Coreset
aliases:
- core-set
- core-set for extent measures
- core set
- epsilon-coreset
area: geometry/geometric-optimization
level: advanced
summary: A small subset of the input, perhaps weighted, whose optimum is within a factor 1+ε of the optimum for the whole input. Sizes depend on ε and the problem, often not on n.
prereqs: [minimum-enclosing-ball, lp-type-problem]
see_also: [badoiu-clarkson-algorithm, khachiyans-algorithm, minimum-volume-enclosing-ellipsoid, clarksons-algorithm, minimum-width-annulus, polygon-width, polygon-diameter, random-sampling]
sources:
  - paper: "Pankaj K. Agarwal, Sariel Har-Peled and Kasturi R. Varadarajan, Approximating extent measures of points, Journal of the ACM 51(4), 2004"
    locator: ε-kernels for directional width of size O(1/ε^((d−1)/2)), their construction, and their use for diameter, width, minimum enclosing boxes and shells by linearization
  - paper: "Pankaj K. Agarwal, Sariel Har-Peled and Kasturi R. Varadarajan, Geometric approximation via coresets, in Combinatorial and Computational Geometry, MSRI Publications 52, Cambridge University Press, 2005"
    locator: the survey of coresets for extent measures, clustering and shape fitting, composability and the merge and reduce method for streams
  - paper: "Mihai Bădoiu, Sariel Har-Peled and Piotr Indyk, Approximate clustering via core-sets, Proceedings of the 34th ACM Symposium on Theory of Computing (STOC), 2002"
    locator: core sets of size O(1/ε²) for the minimum enclosing ball, independent of n and d, and their use for k-center clustering
  - paper: "Mihai Bădoiu and Kenneth L. Clarkson, Optimal core-sets for balls, Computational Geometry: Theory and Applications 40(1), 2008"
    locator: ε-core-sets of size ⌈1/ε⌉ for the minimum enclosing ball, tight in the worst case
  - paper: "Sariel Har-Peled and Soham Mazumdar, On coresets for k-means and k-median clustering, Proceedings of the 36th ACM Symposium on Theory of Computing (STOC), 2004"
    locator: weighted coresets for k-means and k-median in fixed dimension, and the streaming algorithm by merge and reduce
  - paper: "Kenneth L. Clarkson, Coresets, sparse greedy approximation, and the Frank-Wolfe algorithm, ACM Transactions on Algorithms 6(4), 2010"
    locator: coresets of size O(1/ε) for concave maximization over the simplex from the Frank-Wolfe method, with the minimum enclosing ball as an example
---

A coreset of a point set $P$ for an optimization problem is a small subset $Q \subseteq P$, sometimes with weights, such that solving the problem on $Q$ gives a solution within a factor $1 + \varepsilon$ of the optimum for $P$. The point is that the size of $Q$ depends on $\varepsilon$, and often on the dimension, but not on $n = |P|$. Then an expensive exact algorithm can run on $Q$ alone. For the [minimum enclosing ball](/minimum-enclosing-ball/) there are coresets of size $O(1/\varepsilon)$ in any dimension (Bădoiu and Clarkson), and the [Bădoiu-Clarkson algorithm](/badoiu-clarkson-algorithm/) finds one of size $O(1/\varepsilon^2)$ in $O(nd/\varepsilon^2)$ time. For directional width in $\mathbb{R}^d$ the coreset is called an $\varepsilon$-kernel and has size $O(1/\varepsilon^{(d-1)/2})$ (Agarwal, Har-Peled and Varadarajan 2004). A basis of an [LP-type problem](/lp-type-problem/) is an exact coreset with $\varepsilon = 0$.

## In plain words

Suppose a million points form a cloud, and you need the smallest ball around them. Most points lie deep inside and do not matter at all. A few points on the outside hold the ball in place.

A coreset is such a small group of points, picked so that the answer for the group is almost the answer for the whole cloud. You first find the group, which is cheap, and then do the slow exact work on the group only.

The surprise is how small the group can be. For the ball, a few dozen points are enough to get within a few percent, whether the cloud has a thousand points or a billion, and in any number of dimensions.

## The idea

Notation: $P$ is a set of $n$ points in $\mathbb{R}^d$; $\mu$ is a measure of point sets to be minimized or maximized, such as the radius of the smallest enclosing ball; $\varepsilon > 0$ is the accuracy. A coreset is defined for one problem at a time, and the exact form of the guarantee is part of the definition.

**Coresets for the minimum enclosing ball.** Write $B(c_Q, r_Q)$ for the smallest ball that contains $Q$. A subset $Q \subseteq P$ is an $\varepsilon$-coreset if

$$P \subseteq B\bigl(c_Q, (1 + \varepsilon)\, r_Q\bigr).$$

Then $r_Q \le r_P \le (1 + \varepsilon) r_Q$, so the expanded ball of $Q$ is a $(1 + \varepsilon)$-approximation for $P$. Several papers state the guarantee in a slightly different form, for example as a bound on $r_P / r_Q$ only, so the constants in the size bounds depend on the form.

**$\varepsilon$-kernels for extent measures.** For a unit vector $u$, the directional width of $P$ is $\omega(u, P) = \max_{p \in P} \langle u, p \rangle - \min_{p \in P} \langle u, p \rangle$. A subset $Q \subseteq P$ is an $\varepsilon$-kernel if

$$\omega(u, Q) \ge (1 - \varepsilon)\, \omega(u, P) \quad \text{for every unit vector } u.$$

An $\varepsilon$-kernel approximates every measure that is determined by directional widths: the diameter, the [width](/polygon-width/), the smallest enclosing box and others. Agarwal, Har-Peled and Varadarajan (2004) showed that $\varepsilon$-kernels of size $O(1/\varepsilon^{(d-1)/2})$ exist and can be found in near-linear time, and that this size is the best possible for points on a sphere. By linearization, such as lifting $p$ to $(p, |p|^2)$, kernels of lifted points also approximate shells such as the [minimum width annulus](/minimum-width-annulus/).

**Weighted coresets for sums.** For objectives that add up over the points, such as $k$-means, $\sum_{p} \min_j |p - c_j|^2$, a coreset is a weighted set $(Q, w)$ with

$$(1 - \varepsilon)\, \mathrm{cost}(P, C) \le \sum_{q \in Q} w(q)\, \mathrm{cost}(q, C) \le (1 + \varepsilon)\, \mathrm{cost}(P, C)$$

for every set $C$ of $k$ centers. Har-Peled and Mazumdar (2004) built such coresets for $k$-means and $k$-median in fixed dimension, of size polynomial in $k$ and $1/\varepsilon$ and logarithmic in $n$; later constructions remove the dependence on $n$.

**Two properties make coresets useful.**

- *Composability.* If $Q_1$ is a coreset of $P_1$ and $Q_2$ of $P_2$, then for the kernel and the sum definitions $Q_1 \cup Q_2$ is a coreset of $P_1 \cup P_2$ with the same $\varepsilon$.
- *Merge and reduce.* A coreset of a coreset is a coreset, with the errors multiplied: a $\delta$-coreset of an $\varepsilon$-coreset is a coreset with error about $\varepsilon + \delta$. In a stream, keep coresets of blocks of sizes $1, 2, 4, \dots$ and merge two of equal size by taking a coreset of their union, as in a binary counter; with $\varepsilon/\log n$ per level, the total error is $O(\varepsilon)$ and the memory is the coreset size times a polylogarithmic factor.

**Why sizes can be independent of $n$ and $d$.** For the ball, the [Bădoiu-Clarkson iteration](/badoiu-clarkson-algorithm/) moves the center toward the farthest point with step $1/(i + 1)$. After $k$ steps the center is within $r_P/\sqrt{k}$ of the optimal one, and the $k + 1$ points it touched form a $2/\sqrt{k}$-coreset; nothing in the argument depends on $n$ or $d$. Clarkson (2010) showed that this is the Frank-Wolfe method on the probability simplex: any concave maximization over the simplex whose curvature is bounded has an $\varepsilon$-approximate solution supported on $O(1/\varepsilon)$ vertices, and the support is the coreset.

**Lower bounds.** Coresets cannot be smaller than the "number of points that matter" in the worst case. For the regular simplex given by the unit vectors $e_1, \dots, e_m$ of $\mathbb{R}^m$, every subset $Q$ of $j < m$ vertices has $c_Q = (1/j) \sum_{i \in Q} e_i$ and $r_Q^2 = (j - 1)/j$, and a vertex $e_t \notin Q$ has $|e_t - c_Q|^2 = 1 + 1/j$. So $Q$ is an $\varepsilon$-coreset in the sense above only if

$$\frac{j + 1}{j - 1} \le (1 + \varepsilon)^2,$$

which needs $j \ge 1/\varepsilon + (1 + \varepsilon)/(2 + \varepsilon)$, about $1/\varepsilon + 1/2$. So $\Omega(1/\varepsilon)$ points are needed, and the $O(1/\varepsilon)$ bound for balls is tight up to a constant.

## Examples

**A rectangle grid, exact coreset of size 2.** For the 300 lattice points $(x, y)$ with $0 \le x \le 29$ and $0 \le y \le 9$, the smallest enclosing disk is the circle through the four corners, with center $(29/2, 9/2)$ and squared radius $461/2$. The two opposite corners $(0, 0)$ and $(29, 9)$ alone have this smallest disk, with the diagonal as diameter, so $Q = \{(0, 0), (29, 9)\}$ is a $0$-coreset. It is a basis of the LP-type problem.

**The regular simplex, sizes for $\varepsilon = 1/4$.** For the simplex above, the ratio $|e_t - c_Q| / r_Q = \sqrt{(j + 1)/(j - 1)}$ is:

| $j$ | 2 | 3 | 4 | 5 | 6 |
|---|---|---|---|---|---|
| $(j + 1)/(j - 1)$ | 3 | 2 | 5/3 | 3/2 | 7/5 |
| ratio | 1.732 | 1.414 | 1.291 | 1.225 | 1.183 |

With $\varepsilon = 1/4$ the ratio must be at most $1.25$, so a $(1/4)$-coreset of a simplex with $m \ge 6$ vertices needs 5 points.

**The Bădoiu-Clarkson core set of six points.** For $P = \{(0, 0), (10, 0), (0, 6), (4, 8), (9, 7), (5, 3)\}$, three steps of the [Bădoiu-Clarkson algorithm](/badoiu-clarkson-algorithm/) touch $(0, 0)$, $(9, 7)$, $(10, 0)$ and $(0, 6)$. These contain the three points on the optimal circle, so here the coreset is exact: its smallest disk is the optimal disk, with center $(5, 3)$ and squared radius $34$.

**Width on a line.** In $\mathbb{R}^1$ the smallest and largest points form an exact kernel of size 2 for every extent measure. In the plane, the extreme points in the directions $2\pi i / m$ for $m = O(1/\sqrt{\varepsilon})$ directions give an $\varepsilon$-kernel after an affine normalization of $P$ that makes it "fat"; this is the idea behind the $O(1/\varepsilon^{(d-1)/2})$ bound.

## Where it is used

- **Approximation in high dimension.** The minimum enclosing ball, $k$-center clustering with $(1 + \varepsilon)$ guarantees in time $2^{O((k \log k)/\varepsilon^2)}\, dn$ (Bădoiu, Har-Peled and Indyk 2002), and support vector machines, whose training problems are enclosing ball problems in disguise.
- **Shape fitting in fixed dimension.** Diameter, width, the smallest enclosing box, cylinder, annulus and slab are approximated by running an exact but slow algorithm on an $\varepsilon$-kernel, which turns $O(n^2)$ or worse into $O(n + \text{poly}(1/\varepsilon))$.
- **Streams and distributed data.** Composability and merge and reduce give one-pass algorithms with memory that depends on $\varepsilon$ and $\log n$, and coresets computed on separate machines are merged at a coordinator.
- **Ellipsoids.** For the [minimum volume enclosing ellipsoid](/minimum-volume-enclosing-ellipsoid/), [Khachiyan's algorithm](/khachiyans-algorithm/) touches $O(d(\log d + 1/\varepsilon))$ points, a coreset whose size does not depend on $n$ (Kumar and Yıldırım 2005; Todd and Yıldırım 2007).
- **Exact coresets.** In an [LP-type problem](/lp-type-problem/) of combinatorial dimension $\delta$, a basis is a set of at most $\delta$ constraints with the same optimum, and [Clarkson's algorithm](/clarksons-algorithm/) finds one by random sampling.
- **Machine learning.** Weighted coresets compress data sets for clustering, regression and mixture models, with guarantees that hold for every candidate model at once.

## References
