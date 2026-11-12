---
tag: MRP5YA
kind: algorithm
slug: k-means
name: k-means algorithm
aliases:
- Lloyd-Forgy algorithm
- naive k-means
- Lloyd's k-means
area: machine-learning/clustering
level: core
summary: "Lloyd's heuristic for the k-means problem: assign each point to its nearest center, move each center to the mean of its points, and repeat."
solves: [k-means-problem]
model: real-ram
complexity:
  vars: {n: the number of points, d: the dimension, k: the number of clusters, t: the number of iterations}
  time: {worst: "O(n k d t)"}
  space: {extra: "O(n + k d)"}
properties: {deterministic: true, exact: false, online: false, recursive: false}
history:
  year: 1957
  people: [Stuart P. Lloyd, Edward W. Forgy, James MacQueen]
  note: Lloyd described the method in a Bell Labs report in 1957, published in 1982. Forgy (1965) and MacQueen (1967), who named it k-means, published versions of it.
prereqs: [k-means-problem]
see_also: [k-means-plus-plus, hartigan-wong-algorithm, mini-batch-k-means, kernel-k-means, bisecting-k-means, lloyds-algorithm, gaussian-mixture-model, voronoi-diagram]
sources:
  - paper: doi:10.1109/TIT.1982.1056489
    title: Stuart P. Lloyd, Least squares quantization in PCM, IEEE Transactions on Information Theory 28(2), 1982, pages 129 to 137
    locator: the iteration of the two optimality conditions (Method I); the paper is the 1957 Bell Laboratories report, published in 1982
  - paper: "Edward W. Forgy, Cluster analysis of multivariate data, efficiency versus interpretability of classifications, Biometrics 21, 1965, pages 768 to 769"
    locator: abstract of the batch method with data points as the initial centers
  - paper: "James MacQueen, Some methods for classification and analysis of multivariate observations, Proceedings of the Fifth Berkeley Symposium on Mathematical Statistics and Probability, Volume 1, 1967, pages 281 to 297"
    locator: the name k-means and the sequential (online) update of the means
  - paper: doi:10.1007/s00454-011-9340-1
    title: Andrea Vattani, k-means requires exponentially many iterations even in the plane, Discrete and Computational Geometry 45(4), 2011, pages 596 to 616
    locator: the 2^Omega(n) lower bound on the number of iterations for points in the plane
  - paper: doi:10.1145/2027216.2027217
    title: David Arthur, Bodo Manthey and Heiko Röglin, Smoothed analysis of the k-means method, Journal of the ACM 58(5), 2011, Article 19
    locator: the polynomial bound on the expected number of iterations under Gaussian perturbations
  - paper: doi:10.1016/j.patrec.2009.09.011
    title: Anil K. Jain, Data clustering, 50 years beyond K-means, Pattern Recognition Letters 31(8), 2010, pages 651 to 666
    locator: Section 2 (the history of k-means and its variants)
  - book: isbn:9780387310732
    title: Christopher M. Bishop, Pattern Recognition and Machine Learning, Springer, 2006
    locator: Section 9.1 (K-means clustering, the two steps as coordinate descent on the distortion J)
  - book: isbn:9780387848570
    title: Trevor Hastie, Robert Tibshirani and Jerome Friedman, The Elements of Statistical Learning, second edition, Springer, 2009
    locator: Section 14.3.6 (K-means, Algorithm 14.1)
---

The k-means algorithm, also called Lloyd's algorithm, is a local search heuristic for the [k-means problem](/k-means-problem/). It starts from $k$ centers and repeats two steps: give each point to its nearest center, then move each center to the mean of its points. Neither step increases the sum of squared distances, so the method stops after finitely many iterations at a local optimum. It does not find the optimum in general, its worst case is $2^{\Omega(n)}$ iterations even in the plane, and its result depends on the initial centers, which is why it is usually started from [k-means++](/k-means-plus-plus/).

## In plain words

You want to split points into a fixed number of groups. Start with a guess: one marker for each group. Then do two things in turn. First, each point joins the group of the nearest marker. Second, each marker moves to the average position of the points in its group.

When a point moves to a nearer marker, the total of the squared distances goes down. When a marker moves to the average of its points, the total also goes down, because the average is the best place for one marker. So the total never goes up. There are only finitely many ways to split the points, so the process must stop. It stops when no point wants to change its group. The result can still be a poor split, because a bad first guess can trap the markers.

## The problem

The input is a list of points $x_1, \ldots, x_n \in \mathbb{R}^d$ with the Euclidean norm, the number of clusters $k$, and $k$ initial centers $c_1, \ldots, c_k \in \mathbb{R}^d$. The output is a label $a_i \in \{1, \ldots, k\}$ for each point and a center for each cluster. The goal is a small value of the [k-means cost](/k-means-problem/)
$$\phi(a, c) = \sum_{i=1}^{n} \|x_i - c_{a_i}\|^2 .$$
Here $n$ is the number of points, $d$ the dimension and $k$ the number of clusters, which is given. The algorithm does not promise the minimum, only a local minimum in the sense of the fixed points below.

## The algorithm

```pseudo id=main
LLOYD(x_1..x_n, c_1..c_k)
L1  a_i ← NIL for each i
L2  repeat
L3      changed ← false
L4      for i ← 1 to n do                         ▷ assignment step
L5          j ← an index that minimizes ‖x_i − c_j‖², and j = a_i if a_i is one of them
L6          if j ≠ a_i then a_i ← j, changed ← true
L7      if not changed then return (a, c)
L8      for j ← 1 to k do                         ▷ update step
L9          P_j ← { i : a_i = j }
L10         if P_j ≠ ∅ then c_j ← (1 / |P_j|) Σ_{i ∈ P_j} x_i
```

Line L5 keeps the current center of a point when that center is one of its nearest. Without this rule a point at equal distance from two centers can switch between them for ever. Line L10 leaves the center of an empty cluster where it is. Other rules exist for an empty cluster, for example to move its center to the point that pays the most; any rule that does not increase the cost keeps the proofs valid.

The initial centers are an input. Forgy's method takes $k$ distinct data points at random. The random partition method gives each point a random label and starts with the update step. [k-means++](/k-means-plus-plus/) takes data points with probability proportional to the squared distance to the centers chosen so far.

## Example

Take seven points in the plane, $x_1, \ldots, x_7 = (1,1), (2,1), (1,2), (6,5), (7,5), (6,6), (9,9)$, with $k = 2$ and the initial centers $c_1 = (1,1)$ and $c_2 = (2,1)$. These are two close points, which is a poor start.

| iteration | assignment | cost after L4 to L6 | centers after L8 to L10 | cost after L10 |
|---|---|---|---|---|
| 1 | {x1, x3}, {x2, x4, x5, x6, x7} | 228 | (1, 3/2), (6, 26/5) | 593/10 = 59.3 |
| 2 | {x1, x2, x3}, {x4, x5, x6, x7} | 2691/100 = 26.91 | (4/3, 4/3), (7, 25/4) | 217/12 ≈ 18.08 |
| 3 | no point changes | | | |

In iteration 2 the point $x_2 = (2, 1)$ is at squared distance $5/4$ from $c_1 = (1, 3/2)$ and $841/25$ from $c_2 = (6, 26/5)$, so it moves to cluster 1. In iteration 3 each point is nearest to its own center, so line L7 returns. The final cost $217/12$ is the optimum over all $2^7/2 - 1 = 63$ partitions into two non-empty clusters.

**A bad local optimum.** Take the four corners $(0,0), (0,1), (w,0), (w,1)$ of a rectangle with $w > 1$, and start from $c_1 = (0,0)$ and $c_2 = (0,1)$. The bottom points go to $c_1$ and the top points to $c_2$, so the centers move to $(w/2, 0)$ and $(w/2, 1)$, and then no point changes. The cost is $w^2$. The left and right pairs cost $4 \cdot (1/2)^2 = 1$. So a fixed point of the algorithm can be worse than the optimum by any factor, here $w^2$.

## Correctness

The algorithm is a heuristic, so "correct" means two things: it stops, and the result is a fixed point with a cost no larger than the cost at the start. Let $\phi_t$ be the cost after the update step of iteration $t$.

- **The assignment step does not increase the cost.** Each point moves only to a center at a distance no larger than before.
- **The update step does not increase the cost.** By the centroid identity of the [k-means problem](/k-means-problem/), the mean is the best center for a fixed cluster.
- **The cost falls strictly in each iteration that changes a label.** By line L5, a point changes its label only when the new center is strictly nearer.
- **Termination.** Each center at each time is an initial center or the mean of a subset of the points. So the state takes finitely many values, and so does the cost. A strictly decreasing sequence in a finite set is finite, so line L7 returns after finitely many iterations.
- **Fixed points.** At the return, each point is at a nearest center and each non-empty cluster has its mean as center.

The full proof is in the proofs section below. The cost at the end is a local minimum in this sense only. A fixed point can be arbitrarily worse than the optimum, as the rectangle shows. [Hartigan's method](/hartigan-wong-algorithm/) has a smaller set of fixed points.

## Complexity

**One iteration.** The assignment step computes $n k$ squared distances, each in $\Theta(d)$ operations, and the update step adds $n$ vectors. So one iteration costs $\Theta(n k d)$ arithmetic operations, and the memory beyond the input is $O(n)$ for the labels and $O(k d)$ for the centers.

**The number of iterations $t$.**

- **Worst case, upper bound.** No partition repeats, so $t$ is at most the number of partitions that the nearest-center rule can make. These partitions are cut by the [Voronoi diagram](/voronoi-diagram/) of $k$ centers, and there are $n^{O(k d)}$ of them, a polynomial for fixed $k$ and $d$.
- **Worst case, lower bound.** Vattani (2011) builds inputs in the plane on which the algorithm needs $2^{\Omega(n)}$ iterations, also when the initial centers are data points. An earlier bound of $2^{\Omega(\sqrt{n})}$ is due to Arthur and Vassilvitskii (2006).
- **Smoothed case.** If an adversary chooses the points and each point is then moved by independent Gaussian noise of standard deviation $\sigma$, the expected number of iterations is bounded by a polynomial in $n$ and $1/\sigma$ (Arthur, Manthey and Röglin, 2011). This explains why the bad inputs are not seen in practice.
- **Observed.** On typical data the algorithm stops after a few tens of iterations. Libraries also stop when the decrease of the cost falls below a tolerance, or after a fixed number of iterations.

## Properties

- **Deterministic.** For fixed initial centers and the tie rule of line L5, the result is fixed. The randomness of practical use is in the initialization.
- **A coordinate descent.** The cost is a function of the labels and the centers. The assignment step minimizes it over the labels with the centers fixed, and the update step over the centers with the labels fixed. This is [coordinate descent](/coordinate-descent/) in two blocks.
- **Hard limit of EM.** For a [Gaussian mixture model](/gaussian-mixture-model/) with equal weights and covariance $\sigma^2 I$, the [EM algorithm](/expectation-maximization/) tends to this algorithm as $\sigma \to 0$: the responsibilities become 0 or 1.
- **Convex clusters.** At a fixed point the clusters are the points in the Voronoi cells of the centers, so two clusters are separated by a hyperplane. The algorithm cannot find clusters that are not linearly separable, such as two rings.
- **Sensitive to scale.** The Euclidean distance mixes the features. A change of the units of one feature can change the result.

## Variants and improvements

- **Better seeding.** [k-means++](/k-means-plus-plus/) chooses the initial centers so that the expected cost is within $8(\ln k + 2)$ of the optimum before any iteration.
- **Several restarts.** Run from several initializations and keep the result with the least cost. This is the default of most libraries.
- **Faster assignment.** Elkan (2003) keeps bounds from the [triangle inequality](/triangle-inequality/) to skip most distance computations; the result is the same as the plain algorithm.
- **Single-point moves.** [Hartigan's method](/hartigan-wong-algorithm/) moves one point at a time when the move lowers the cost, with the exact change of the two means.
- **Sequential update.** MacQueen's version updates the mean of a cluster after each point. [Mini-batch k-means](/mini-batch-k-means/) updates the centers from small random samples.
- **Divisive use.** [Bisecting k-means](/bisecting-k-means/) splits one cluster at a time with $k = 2$.
- **Other spaces.** [Kernel k-means](/kernel-k-means/) runs the same two steps in a feature space. The [Lloyd relaxation](/lloyds-algorithm/) of geometry is the same iteration on a continuous density, and it converges to a [centroidal Voronoi tessellation](/centroidal-voronoi-tessellation/).
- **Choice of k.** [X-means](/x-means/) and [G-means](/g-means/) wrap the algorithm in a loop that splits clusters.

## When to use it

Use it for a fast, simple clustering of numeric data in which the clusters are compact, of similar size and roughly round, and when the number of clusters is known. Seed it with k-means++ and run it several times. Do not use it for clusters of arbitrary shape (use [DBSCAN](/dbscan/) or [spectral clustering](/spectral-clustering/)), for a general metric (use [partitioning around medoids](/partitioning-around-medoids/)), or when you need a proof of optimality (use the dynamic program in one dimension, or an exact method for small inputs).

## Pitfalls

- **Problem and algorithm.** "k-means" names both the objective and this heuristic. The algorithm does not solve the problem. Its result is a fixed point, which can be far from the optimum.
- **Initialization.** Two initial centers in the same true cluster can trap the method, as in the example. Use k-means++ and several restarts.
- **Ties.** Without the rule of line L5, a point at equal distance from two centers can make the method cycle.
- **Empty clusters.** A cluster can lose all its points. Code that divides by the size of the cluster then fails. Keep the old center, or reseed it.
- **Unscaled features.** A feature with a large range dominates the distance. Standardize the features first when their units differ.
- **The cost falls with k.** A smaller cost for a larger $k$ does not show that the larger $k$ is better. See [cluster validity](/cluster-validity/).
- **Stopping on the cost.** A test such as "stop when the cost changes by less than $10^{-4}$" can stop before a fixed point. That is fine in practice, but then the fixed-point property does not hold.

## Implementations

## History

Lloyd wrote the method in 1957 at Bell Laboratories, for the design of an optimal quantizer for pulse code modulation. The report circulated for many years and was published in 1982. Forgy described the same batch method in 1965. MacQueen gave the name k-means in 1967, for a version that updates the means one point at a time. Jain's survey also credits Steinhaus (1956) with the idea. The exponential lower bound in the plane is due to Vattani (2011), and the polynomial smoothed bound to Arthur, Manthey and Röglin (2011).

## References
