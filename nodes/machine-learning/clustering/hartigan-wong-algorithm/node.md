---
tag: RNKKMZ
kind: algorithm
slug: hartigan-wong-algorithm
name: Hartigan-Wong algorithm
aliases:
- Hartigan-Wong k-means
- Hartigan's method for k-means
- AS 136
area: machine-learning/clustering
level: advanced
summary: K-means variant that moves single points whenever the move lowers the objective.
solves: [k-means-problem]
model: real-ram
complexity:
  vars: {n: the number of points, d: the dimension, k: the number of clusters, t: the number of passes over the points}
  time: {worst: "O(n k d t)"}
  space: {extra: "O(n + k d)"}
properties: {deterministic: true, exact: false, online: false, recursive: false}
history:
  year: 1979
  people: [John A. Hartigan, Manchek A. Wong]
  note: Hartigan described the single point move method in his 1975 book; Hartigan and Wong published the Fortran routine AS 136 in 1979.
prereqs: [k-means]
see_also: [k-means, k-means-problem, k-means-plus-plus, local-search, local-optimum, mini-batch-k-means, partitioning-around-medoids]
sources:
  - paper: doi:10.2307/2346830
    title: John A. Hartigan and Manchek A. Wong, Algorithm AS 136, A K-means clustering algorithm, Journal of the Royal Statistical Society, Series C (Applied Statistics) 28(1), 1979, pages 100 to 108
    locator: the optimal transfer stage, the quick transfer stage and the live sets; the test of R2 = n_L R(I, L)^2 / (n_L + 1) against the same quantity with n_L - 1 for the own cluster
  - book: isbn:9780471356455
    title: John A. Hartigan, Clustering Algorithms, Wiley, 1975
    locator: Chapter 4 (the k-means algorithm with the reassignment of single points)
  - paper: "Matus Telgarsky and Andrea Vattani, Hartigan's method: k-means clustering without Voronoi, Proceedings of the 13th International Conference on Artificial Intelligence and Statistics (AISTATS), PMLR 9, 2010, pages 820 to 827"
    locator: the proof that the stable partitions of Hartigan's method are a subset of the fixed points of Lloyd's method, and examples where Hartigan's method improves them
  - paper: "Bodo Manthey and Jesse van Rhijn, Worst-case and smoothed analysis of Hartigan's method for k-means clustering, 41st International Symposium on Theoretical Aspects of Computer Science (STACS), LIPIcs 289, 2024; arXiv:2309.10368"
    locator: the instances that need 2^Omega(n) moves and the smoothed bound
---

The Hartigan-Wong algorithm is a [local search](/local-search/) heuristic for the [k-means problem](/k-means-problem/) that moves one point at a time. A point $x$ leaves its cluster $i$ for a cluster $j$ when $\frac{n_j}{n_j + 1} \|x - c_j\|^2 < \frac{n_i}{n_i - 1} \|x - c_i\|^2$, where $n$ is the size of a cluster and $c$ its mean, because this is exactly the condition that the move lowers the sum of squared distances. Its stable partitions are a subset of the fixed points of [Lloyd's algorithm](/k-means/), so it can escape some of the poor fixed points of Lloyd. It is still a heuristic with no approximation guarantee, and it is the default method of the `kmeans` function of R.

## In plain words

Lloyd's method for k-means moves all points at once and then moves the group centers. Hartigan's method looks at one point at a time and asks a sharper question: if this one point moves to another group, and both group centers shift to their new averages, does the total squared distance go down? If so, it moves the point now and updates the two centers at once.

The answer takes into account that the centers move too. Taking a point out of a group pulls the center away from it, so leaving saves more than the plain distance. Joining a group pulls the center toward the point, so joining costs less than the plain distance. Because of this, Hartigan's method sees some good moves that Lloyd's method misses.

## The problem

The input is a list of points $x_1, \ldots, x_n \in \mathbb{R}^d$ with the Euclidean norm, the number of clusters $k$ (given), and an initial label $a_i \in \{1, \ldots, k\}$ for each point, for example the label of the nearest center after [k-means++](/k-means-plus-plus/) or after Lloyd's algorithm. The output is a partition into $k$ clusters such that no single move of one point to another cluster lowers the cost
$$\phi(a) = \sum_{j=1}^{k} \sum_{i : a_i = j} \|x_i - c_j\|^2, \qquad c_j = \text{the mean of cluster } j .$$
Such a partition is called Hartigan stable. It is a local optimum for single moves, not an optimum: the problem is NP-hard, see [NP-hardness of k-means](/k-means-np-hardness/).

## The algorithm

```pseudo id=main
HARTIGAN(x_1..x_n, a_1..a_n)
L1  compute the size n_j and the mean c_j of each cluster j
L2  repeat
L3      moved ← false
L4      for i ← 1 to n do
L5          p ← a_i; if n_p = 1 then skip to the next i
L6          r ← n_p / (n_p − 1) · ‖x_i − c_p‖²               ▷ saving if x_i leaves p
L7          q ← an index j ≠ p that minimizes n_j / (n_j + 1) · ‖x_i − c_j‖²
L8          if n_q / (n_q + 1) · ‖x_i − c_q‖² < r then
L9              c_p ← (n_p c_p − x_i) / (n_p − 1); n_p ← n_p − 1
L10             c_q ← (n_q c_q + x_i) / (n_q + 1); n_q ← n_q + 1
L11             a_i ← q; moved ← true
L12 until not moved
```

Line L6 is the decrease of the cost of cluster $p$ when $x_i$ leaves it, and line L7 is the increase of the cost of cluster $q$ when $x_i$ joins it; both include the shift of the mean. Line L5 never empties a cluster. For an empty cluster $q$ the joining cost is 0, and line L10 makes $x_i$ its center.

This is Hartigan's move rule with a full scan of the clusters for each point. The routine AS 136 of Hartigan and Wong uses the same test, but it saves time with two devices that this page does not implement. The *optimal transfer* stage checks a point only against the clusters in a *live set*, the clusters that changed in the last $n$ steps. The *quick transfer* stage checks each point only against its two nearest centers, until no such move is left. Both stages use the rule of line L8, and the routine stops when a full optimal transfer pass makes no move.

## Example

Take the four corners $(0,0), (0,1), (2,0), (2,1)$ of a $2 \times 1$ rectangle with $k = 2$. Start from the partition bottom and top: $\{(0,0), (2,0)\}$ with mean $(1, 0)$ and $\{(0,1), (2,1)\}$ with mean $(1, 1)$. The cost is 4. Each point is at its nearest mean, so this is a fixed point of Lloyd's algorithm, and Lloyd stops here. The optimum, left and right, costs 1.

| step | point | own cluster: $\frac{n_p}{n_p - 1}\|x - c_p\|^2$ | best other: $\frac{n_q}{n_q + 1}\|x - c_q\|^2$ | move | cost |
|---|---|---|---|---|---|
| start | | | | | 4 |
| 1 | (0,0) | 2 · 1 = 2 | 2/3 · 2 = 4/3 | yes | 4 − 2/3 = 10/3 |
| 2 | (0,1) | 3/2 · 5/9 = 5/6 | 1/2 · 5 = 5/2 | no | 10/3 |
| 3 | (2,0) | own cluster has size 1 | | skip | 10/3 |
| 4 | (2,1) | 3/2 · 17/9 = 17/6 | 1/2 · 1 = 1/2 | yes | 10/3 − 7/3 = 1 |

After step 1 the clusters are $\{(2,0)\}$ and $\{(0,0), (0,1), (2,1)\}$ with mean $(2/3, 2/3)$. Step 4 then moves $(2,1)$ to the cluster of $(2,0)$. The second pass makes no move, and the result is the optimum. In step 1 the point $(0,0)$ is at squared distance 1 from its own mean and 2 from the other, so Lloyd's rule keeps it; Hartigan's rule sees that the two means shift and that the move saves $2/3$.

For a $w \times 1$ rectangle, the first move pays off when $\frac23 (w^2/4 + 1) < w^2/2$, that is when $w^2 > 2$. For a square, the partition bottom and top is already optimal and Hartigan's method keeps it.

## Correctness

The method is a heuristic. Its claims are: each move lowers the cost by the exact amount of the test, it stops, and the result is Hartigan stable and a fixed point of Lloyd's algorithm.

- **The exact change.** Adding a point $x$ to a cluster of size $m$ with mean $c$ raises its cost by $\frac{m}{m + 1}\|x - c\|^2$. Removing $x$ from a cluster of size $m \ge 2$ with mean $c$ lowers its cost by $\frac{m}{m - 1}\|x - c\|^2$. Both follow from the centroid identity of the [k-means problem](/k-means-problem/).
- **Strict decrease.** A move happens only when the increase is less than the decrease, so the cost falls strictly.
- **Termination.** The cost is a function of the partition, and there are finitely many partitions. A strictly decreasing sequence of costs cannot repeat a partition, so the loop stops.
- **Hartigan stable.** At the end a full pass made no move, so no single move lowers the cost.
- **A fixed point of Lloyd.** If $x$ is in cluster $i$ with $n_i \ge 2$ and $\|x - c_j\| < \|x - c_i\|$, then $\frac{n_j}{n_j + 1}\|x - c_j\|^2 < \|x - c_j\|^2 < \|x - c_i\|^2 < \frac{n_i}{n_i - 1}\|x - c_i\|^2$, so a move exists. If $n_i = 1$ then $x = c_i$ and its distance is 0. So in a stable partition each point is at a nearest mean.

The proofs are in the proofs section below. The last item is the result of Telgarsky and Vattani (2010): every Hartigan stable partition is a Lloyd fixed point, but not conversely, as the example shows.

## Complexity

**One pass.** For each point the method computes $k$ distances in $O(kd)$ time, and a move updates two means in $O(d)$ time. One pass over the points costs $O(nkd)$, like one iteration of Lloyd's algorithm. AS 136 is faster in practice because of the live sets and the quick transfers. The memory is $O(n)$ for the labels and $O(kd)$ for the means and sizes.

**The number of passes $t$.** It is finite but can be large. Manthey and van Rhijn (2024) give inputs, already in one dimension, on which the method needs $2^{\Omega(n)}$ moves. They also give a smoothed bound, polynomial in $n$ and $1/\sigma$ for fixed $k$ and $d$, with a factor $k^{12kd}$. In practice a few passes suffice.

## Properties

- **Deterministic.** For fixed initial labels and a fixed order of the points the result is fixed.
- **Depends on the order.** A different order of the points can lead to a different stable partition.
- **Never worse than its start.** The cost after each move is lower than before. Started from a Lloyd fixed point, it returns a partition that is at least as good.
- **Fewer local optima than Lloyd.** Every Hartigan stable partition is a Lloyd fixed point. So the method can only remove bad stopping points.
- **No guarantee.** There is no bound on the ratio to the optimum. A stable partition can still be poor.
- **No empty clusters.** A cluster with one point never gives it away, so the number of non-empty clusters never falls.

## Variants and improvements

- **AS 136.** The original Fortran routine, with live sets and quick transfers. It is the default `algorithm = "Hartigan-Wong"` of the R function `kmeans`.
- **The first improvement.** Move the point to the first cluster that passes the test, instead of the best one. The stable partitions are the same.
- **Hybrid with Lloyd.** Run Lloyd's algorithm to a fixed point first, then run Hartigan's method to leave it. This keeps the speed of the batch steps and the better local optima of single moves.
- **Kernel version.** The test needs only distances to means, so it works in a feature space with a kernel; see [kernel k-means](/kernel-k-means/).
- **Swaps of centers.** Local search that swaps a center with a data point, as in [partitioning around medoids](/partitioning-around-medoids/) or the $9 + \varepsilon$ local search for k-means, uses larger moves and has a constant factor guarantee.

## When to use it

Use it instead of, or after, Lloyd's algorithm when the cost matters more than the speed and the data fits in memory. It is a cheap way to improve a Lloyd fixed point. For very large data sets use [mini-batch k-means](/mini-batch-k-means/), and always start from a good seeding such as [k-means++](/k-means-plus-plus/).

## Pitfalls

- **Using the plain distance.** The test compares $\frac{n_j}{n_j + 1}\|x - c_j\|^2$ with $\frac{n_i}{n_i - 1}\|x - c_i\|^2$. Comparing the plain squared distances gives Lloyd's rule, and the advantage is lost.
- **Stale means.** The means of both clusters must change at once after each move. A batch update of the means after a full pass gives a different method, and the cost can then rise.
- **Clusters of size 1.** The factor $\frac{n_i}{n_i - 1}$ has a zero denominator. Skip such points.
- **Floating point.** Incremental updates of the means accumulate rounding error over many moves. Recompute the means from the data now and then, or keep the sums of the points instead of the means.
- **Ties.** Move only when the test is strict, or the method can cycle between partitions of equal cost.

## Implementations

## History

Hartigan described k-means with the reassignment of single points in his book Clustering Algorithms (1975). Hartigan and Wong published the efficient Fortran routine AS 136 in Applied Statistics in 1979, and it became the default in R. Telgarsky and Vattani (2010) proved that its stable partitions are a subset of the fixed points of Lloyd's method and gave examples where it does much better. Manthey and van Rhijn (2024) gave the first worst case and smoothed bounds on its running time.

## References
