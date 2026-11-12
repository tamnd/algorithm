---
tag: D8T8TZ
kind: problem
slug: k-median-problem
name: k-median problem
aliases:
- k-median clustering
- p-median problem
area: machine-learning/clustering
level: core
summary: Choose k centers minimizing the total (not squared) distance from points to their nearest center.
prereqs: [clustering-problem, metric-space]
see_also: [k-means-problem, partitioning-around-medoids, streaming-k-median, k-center-problem, k-median-inapproximability, euclidean-k-median, facility-location-problem, geometric-median]
sources:
  - paper: "O. Kariv and S. L. Hakimi, An algorithmic approach to network location problems. II: The p-medians, SIAM Journal on Applied Mathematics 37(3), 1979, pp. 539-560"
    title: Kariv and Hakimi 1979
    locator: the NP-hardness of the p-median problem on general networks and the polynomial algorithms on trees
  - paper: doi:10.1137/S0097539702416402
    title: "V. Arya, N. Garg, R. Khandekar, A. Meyerson, K. Munagala and V. Pandit, Local search heuristics for k-median and facility location problems, SIAM Journal on Computing 33(3), 2004"
    locator: the locality gap 3 + 2/p of local search with p simultaneous swaps
  - paper: "M. Charikar, S. Guha, É. Tardos and D. B. Shmoys, A constant-factor approximation algorithm for the k-median problem, Journal of Computer and System Sciences 65(1), 2002 (STOC 1999)"
    title: Charikar, Guha, Tardos and Shmoys 2002
    locator: the first constant ratio for metric k-median, by LP rounding
  - paper: "S. Li and O. Svensson, Approximating k-median via pseudo-approximation, Proceedings of the 45th ACM Symposium on Theory of Computing (STOC), 2013"
    title: Li and Svensson 2013
    locator: the ratio 1 + √3 + ε
  - paper: "J. Byrka, T. Pensyl, B. Rybicki, A. Srinivasan and K. Trinh, An improved approximation for k-median, and positive correlation in budgeted optimization, Proceedings of the 26th ACM-SIAM Symposium on Discrete Algorithms (SODA), 2015"
    title: Byrka et al. 2015
    locator: the ratio 2.675 + ε
  - book: isbn:9780521195270
    title: David P. Williamson and David B. Shmoys, The Design of Approximation Algorithms
    locator: Sections 7.7 and 9.2 (k-median by the primal-dual method and by local search)
  - book: isbn:9780471878766
    title: Leonard Kaufman and Peter J. Rousseeuw, Finding Groups in Data, An Introduction to Cluster Analysis, Wiley, 1990
    locator: Chapter 2 (k-medoids as the clustering form of the problem)
---

The k-median problem asks for $k$ centers that make the sum of the distances from the points to their nearest center as small as possible. It is the clustering objective of the [clustering problem](/clustering-problem/) with plain distances in place of the squared distances of the [k-means problem](/k-means-problem/), so a far point counts linearly and not quadratically. It is [NP-hard](/np-hard/) in a general [metric](/metric-space/) and in the plane, it has constant factor approximations (local search with $p$ swaps gives $3 + 2/p$), and on a line it is solved exactly by dynamic programming. The hardness of approximation and the Euclidean approximation scheme have their own pages, [k-median inapproximability](/k-median-inapproximability/) and [Euclidean k-median](/euclidean-k-median/); this page is the clustering view.

## In plain words

You have a set of points and a way to measure how far apart two points are. You may pick a fixed number of them as centers. Each point then goes to its nearest center, and pays the distance to it. You want the total bill to be as small as possible.

The total groups the points into clusters, one for each center. Unlike the squared bill of k-means, one far point adds its distance once, not its distance times itself, so a few strange points cannot pull a center far from the others. The center of a cluster on a line is its middle value, not its average. Picking the best centers is hard in general, but good guesses are cheap: swap a center for another point while the bill goes down.

## Definition

The data model is a finite set of points $X = \{x_1, \ldots, x_n\}$ in a metric space $(V, d)$, a set $F \subseteq V$ of allowed centers, and an integer $k$ with $1 \le k \le |F|$. The number of clusters $k$ is given. Optional weights $w_i > 0$ count a point $w_i$ times.

For a set $C \subseteq F$ of centers, write $d(x, C) = \min_{c \in C} d(x, c)$. The cost is

$$\mathrm{cost}(C) = \sum_{i=1}^{n} w_i \, d(x_i, C).$$

The problem asks for $C \subseteq F$ with $|C| \le k$ that minimizes $\mathrm{cost}(C)$. Each center $c$ defines a cluster, the points whose nearest center is $c$ (ties broken in any fixed way), so a solution is also a partition of $X$ into at most $k$ clusters. In the other direction, a partition $X_1, \ldots, X_k$ has the cost $\sum_j \min_{c \in F} \sum_{x \in X_j} w(x) d(x, c)$, and the least such cost over all partitions is the same optimum.

- **Discrete version:** $F = X$, the centers are data points. In clustering these centers are the *medoids*, and the problem is the k-medoids problem of [partitioning around medoids](/partitioning-around-medoids/). It needs only the $n \times n$ table of dissimilarities, which need not be a metric.
- **Continuous version:** $F = V$, for example $V = \mathbb{R}^d$ with the Euclidean or the $\ell_1$ distance. For $k = 1$ in the Euclidean plane this is the [geometric median](/geometric-median/) (the Fermat-Weber point).

**The two versions differ by a factor of at most 2 in a metric.** Let $\mathrm{OPT}_X$ be the discrete and $\mathrm{OPT}_V$ the continuous optimum for the same points. Then $\mathrm{OPT}_V \le \mathrm{OPT}_X \le 2\,\mathrm{OPT}_V$. The first inequality holds because $X \subseteq V$. For the second, take an optimal continuous solution and one of its clusters $Q$ with center $c$. Let $p \in Q$ be a point of $Q$ nearest to $c$. For each $x \in Q$, the triangle inequality and $d(c, p) \le d(c, x)$ give $d(x, p) \le d(x, c) + d(c, p) \le 2 d(x, c)$. Replace each center by its $p$ and sum over all clusters. The factor 2 is tight: take $n$ leaves at pairwise distance 2 and a hub $h \in V \setminus X$ at distance 1 from each leaf. With $k = 1$, the hub costs $n$ and each leaf costs $2(n - 1)$.

## Variants

- **Decision version.** Given a bound $B$, is there a $C$ with $|C| \le k$ and $\mathrm{cost}(C) \le B$? It is NP-complete for the discrete metric version (see Reductions).
- **Weighted points.** Weights are the form that [streaming k-median](/streaming-k-median/) and other summaries produce: a center with weight $w$ stands for $w$ points.
- **Facility location.** The [facility location problem](/facility-location-problem/) drops the bound $k$ and charges an opening cost for each center. The Lagrangian relaxation of the bound $k$ turns k-median into facility location, which is the route of the primal-dual algorithm.
- **$\ell_1$ k-medians in $\mathbb{R}^d$.** Under the $\ell_1$ distance, the coordinate-wise median of a cluster is an optimal center, because the cost splits into one sum for each coordinate. The Lloyd-style alternation of nearest-center assignment and coordinate-wise medians is often called k-medians; like [k-means](/k-means/) it only reaches a local optimum.
- **k-center and k-means.** The [k-center problem](/k-center-problem/) takes the largest distance instead of the sum; the [k-means problem](/k-means-problem/) takes the sum of squared distances. With centers from the data and squared metric distances, the triangle inequality holds only up to a factor 2, which changes the constants of the analysis.
- **Outliers and capacities.** Variants may ignore the $z$ worst points, or bound the number of points that a center may serve.

## Examples

**A line with an outlier.** Take $X = \{1, 2, 3, 4, 40, 41, 42\}$ on the real line with $d(x, y) = |x - y|$.

| $k$ | optimal centers | optimal cost |
|---|---|---|
| 1 | 4 | 117 |
| 2 | 2 and 41 | 6 |
| 3 | 1, 3 and 41 | 4 |

For $k = 2$, the cluster $\{1, 2, 3, 4\}$ costs $1 + 0 + 1 + 2 = 4$ around 2 (each point of $[2, 3]$ is optimal), and $\{40, 41, 42\}$ costs 2 around 41. For $k = 3$, several solutions tie at cost 4. For $k = 1$, the 1-median is 4 while the mean, the 1-means center, is $133/7 = 19$. Add the point 400: each point of $[4, 40]$ is now an optimal 1-median, while the mean jumps to $533/8 = 66.625$. This is the robustness of the sum of distances.

**Discrete against continuous.** In the star of the Definition with 6 leaves, $\mathrm{OPT}_X = 10$ and $\mathrm{OPT}_V = 6$. For three points at the corners of an equilateral triangle with side 1 in the Euclidean plane, a corner costs 2 and the center of the triangle costs $3/\sqrt{3} = \sqrt{3} \approx 1.732$.

**A non-example.** The set of means of k-means is not a k-median solution in general: for $\{1, 2, 3, 4, 40, 41, 42, 400\}$ and $k = 1$, the mean 66.625 costs $(66.625 \cdot 7 - 133) + 333.375 = 666.75$, while the median 4 costs $(3 + 2 + 1 + 0 + 36 + 37 + 38) + 396 = 513$.

## Known algorithms

- **Brute force** tries all $\binom{|F|}{k}$ center sets, in $O(\binom{|F|}{k} k n)$ time.
- **Points on a line.** Sort the points. On a line, the points nearest to one center form a run of the sorted order, and a median of the run is an optimal center for it. With $F(c, j)$ the least cost of the first $j$ points in $c$ runs, $F(c, j) = \min_{i < j} \big(F(c - 1, i) + \mathrm{run}(i + 1, j)\big)$, where prefix sums give each run cost in $O(1)$. This is exact in $O(k n^2)$ time after the sort; the implementation below checks it against brute force. The same idea on trees gives polynomial algorithms (Kariv and Hakimi 1979).
- **[Partitioning around medoids](/partitioning-around-medoids/)** (PAM) runs a greedy BUILD and then single swaps until no swap lowers the cost. It is a heuristic in the data, but in a metric its local optimum is within a factor 5 of the optimum, by the locality gap below.
- **Local search with $p$ swaps** (Arya et al. 2004): repeat a change of at most $p$ centers while it lowers the cost by a factor $1 - \varepsilon/\mathrm{poly}(n, k)$. Each local optimum has cost at most $(3 + 2/p)\,\mathrm{OPT}_F$, and the ratio $3 + 2/p$ is tight for this method. With the factor in the stopping rule, the number of steps is polynomial, and the ratio becomes $3 + 2/p + \varepsilon$.
- **LP rounding and primal-dual.** Charikar, Guha, Tardos and Shmoys (1999, journal 2002) gave the first constant ratio, $6\tfrac{2}{3}$. Jain and Vazirani reached 6 with a [primal-dual facility location algorithm](/jain-vazirani-facility-location/) and Lagrangian relaxation. Li and Svensson (2013) reached $1 + \sqrt{3} + \varepsilon \approx 2.732$, and Byrka et al. (2015) $2.675 + \varepsilon$.
- **Euclidean space.** The [approximation scheme of Arora, Raghavan and Rao](/arora-euclidean-k-median-ptas/) gives $1 + \varepsilon$ in the plane; see [Euclidean k-median](/euclidean-k-median/).
- **Streams and large data.** [Streaming k-median](/streaming-k-median/) keeps weighted centers of pieces of the stream and gets a constant factor in one pass with $O(n^\varepsilon)$ memory.

## Bounds

- **Exact.** NP-hard for the discrete metric version (Kariv and Hakimi 1979; the reduction below) and for Euclidean points in the plane (Megiddo and Supowit 1984, cited on [Euclidean k-median](/euclidean-k-median/)). Polynomial on a line and on trees, and polynomial for fixed $k$ in the discrete version, by brute force.
- **Upper bound on the ratio.** $2.675 + \varepsilon$ in polynomial time for metric k-median (Byrka et al. 2015). A simple method with a proved constant is single-swap local search, with ratio 5 at a local optimum.
- **Lower bound on the ratio.** No polynomial algorithm has ratio below $1 + 2/e \approx 1.736$ unless NP $\subseteq$ DTIME$(n^{O(\log \log n)})$ (Jain, Mahdian and Saberi 2002); the proof is on [k-median inapproximability](/k-median-inapproximability/).
- **Discrete against continuous.** The factor 2 of the Definition loses at most 2 in the ratio when an algorithm for the discrete version serves the continuous one in the same metric.

## Reductions

**From dominating set (NP-hardness).** Let $H = (U, E)$ be a graph with $n$ vertices and $k < n$. Put $X = F = U$ and $d(u, v) = 1$ for an edge, $2$ for a non-edge, $0$ for $u = v$. Each distance between distinct points is 1 or 2, so the triangle inequality holds. For a set $C$ of $k$ centers, each of the $n - k$ points outside $C$ pays 1 or 2, so $\mathrm{cost}(C) \ge n - k$, with equality exactly when each point outside $C$ has a neighbor in $C$, that is, when $C$ is a [dominating set](/dominating-set/). So $H$ has a dominating set of size $k$ if and only if the optimum is $n - k$, and the decision version is NP-complete. The reduction takes $O(n^2)$ time. Unlike the same reduction for [k-center](/k-center-hardness/), it gives no gap of a factor 2: a non-dominating set may cost only $n - k + 1$.

**To facility location.** Add a uniform opening cost $\lambda$ for each center and drop the bound $k$. For each $\lambda$, an optimal facility location solution with exactly $k$ open centers is an optimal k-median solution. Jain and Vazirani search over $\lambda$ for this and repair the case where no $\lambda$ gives exactly $k$ centers.

## Applications

- **Robust clustering.** The center of a cluster is a median, so it does not move far for a few gross errors, as in the example above. With centers from the data, the method needs only dissimilarities, so it clusters strings, sets or rankings.
- **Location of facilities.** In operations research the $p$-median problem places $p$ warehouses or clinics to minimize the total travel of the customers.
- **Summaries of large data.** A weighted set of k-median centers is a compact summary of a stream; the [streaming k-median](/streaming-k-median/) algorithm and [coresets](/coreset/) build on this.

## References
