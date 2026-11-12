---
tag: 4FMVJH
kind: algorithm
slug: bisecting-k-means
name: Bisecting k-means
aliases:
- bisecting k-means clustering
area: machine-learning/clustering
level: advanced
summary: "A divisive heuristic for k-means: start with one cluster and repeatedly split the largest one, or the one with the largest SSE, by 2-means."
solves: [k-means-problem]
model: real-ram
complexity:
  vars: {n: the number of points, d: the dimension, k: the number of clusters, r: the number of 2-means runs per split, t: the number of Lloyd iterations per run}
  time: {worst: "O(n k d r t)"}
  space: {extra: "O(n + k d)"}
properties: {deterministic: false, exact: false, online: false, recursive: false}
history:
  year: 2000
  people: [Michael Steinbach, George Karypis, Vipin Kumar]
  note: Introduced for document clustering, where it beat plain k-means and matched agglomerative clustering.
prereqs: [k-means]
see_also: [k-means, divisive-clustering, hierarchical-clustering-problem, agglomerative-clustering, ward-method, principal-component-analysis, x-means, g-means]
sources:
  - paper: "Michael Steinbach, George Karypis and Vipin Kumar, A comparison of document clustering techniques, KDD Workshop on Text Mining, 2000"
    locator: Section 4 (the bisecting k-means algorithm, the choice of the cluster to split and the ITER repeated bisections)
  - book: isbn:9780321321367
    title: Pang-Ning Tan, Michael Steinbach and Vipin Kumar, Introduction to Data Mining, Addison-Wesley, 2006
    locator: Section 8.2.3 (bisecting K-means, Algorithm 8.2)
  - paper: "Daniel Boley, Principal direction divisive partitioning, Data Mining and Knowledge Discovery 2(4), 1998, pages 325 to 344"
    locator: the split of a cluster by the sign of its projection on the first principal direction
  - paper: "Sergio M. Savaresi and Daniel L. Boley, A comparative analysis on the bisecting K-means and the PDDP clustering algorithms, Intelligent Data Analysis 8(4), 2004, pages 345 to 362"
    locator: the comparison of the two divisive methods
---

Bisecting k-means is a divisive heuristic for the [k-means problem](/k-means-problem/). It starts with all points in one cluster. While there are fewer than $k$ clusters, it chooses one cluster, splits it in two with [k-means](/k-means/) for $k = 2$ from several random starts, and keeps the split with the least sum of squared errors (SSE). Steinbach, Karypis and Kumar (2000) choose the cluster with the most points; another common rule, the default of scikit-learn, chooses the cluster with the largest SSE. The splits form a binary tree, so the method also gives a [divisive hierarchical clustering](/divisive-clustering/), but it has no approximation guarantee.

## In plain words

Instead of looking for all the groups at once, cut the data in two. Then pick one of the pieces and cut it in two as well. Keep going until you have the number of groups you want.

Each cut is a small k-means problem with only two groups, which is easier and less sensitive to a bad start. To make each cut good, try it a few times from different random starts and keep the best one. Which piece to cut next is a choice. You can always cut the biggest piece, or the piece whose points are the most spread out. The cuts also give a family tree of groups, which shows how the groups relate.

## The problem

The input is a list of points $x_1, \ldots, x_n \in \mathbb{R}^d$ with the Euclidean norm, the number of clusters $k$ (given), the number $r$ of 2-means runs for each split, a rule for the choice of the cluster, and a source of random numbers. For a cluster $P$ let $\mathrm{SSE}(P) = \sum_{x \in P}\|x - \mu(P)\|^2$, with $\mu(P)$ the mean. The output is a partition into $k$ clusters and the binary tree of the splits. The goal is a small total SSE. The method gives no bound relative to the optimum.

## The algorithm

```pseudo id=main
BISECTING-KMEANS(x_1..x_n, k, r, rule)
L1  L ← [ {x_1, ..., x_n} ]
L2  while |L| < k do
L3      P ← the cluster of L with the most points (rule "largest") or the largest SSE (rule "sse")
L4      repeat r times
L5          split P into (A, B) by 2-means (Lloyd's algorithm with k = 2) from two random points of P
L6      keep the split (A, B) with the least SSE(A) + SSE(B)
L7      replace P by A and B in L
L8  return L
```

Line L5 runs [Lloyd's algorithm](/k-means/) on the points of $P$ only. Line L6 is the "ITER" step of the paper. A cluster whose points all coincide cannot be split; the implementation skips it, and it stops early if no cluster can be split. Ties in line L3 go to the cluster that comes first in $L$.

## Example

Take the ten points $0, 1, 2, 3, 4, 5, 100, 101, 200, 201$ on a line and $k = 3$.

**First split.** The best 2-means split is $\{0, \ldots, 5\}$ and $\{100, 101, 200, 201\}$. Their SSE are $17.5$ and $10001$ (the mean of the right group is $150.5$, and $2 \cdot 50.5^2 + 2 \cdot 49.5^2 = 10001$).

**Second split, rule "sse".** The right group has the larger SSE, so it is split into $\{100, 101\}$ and $\{200, 201\}$. The result has total SSE $17.5 + 0.5 + 0.5 = 18.5$, which is optimal.

**Second split, rule "largest".** The left group has 6 points against 4, so it is split into $\{0, 1, 2\}$ and $\{3, 4, 5\}$. The result has total SSE $2 + 2 + 10001 = 10005$.

So the choice rule matters. The rule "largest" tends to give clusters of balanced size, which suited the document data of Steinbach and others; the rule "sse" follows the k-means objective more closely.

## Correctness

The method is a heuristic. Its claims are about the shape of the output:

- **A partition.** Line L7 replaces a cluster by two non-empty clusters whose union is the cluster, so $L$ stays a partition of the points into non-empty clusters. Each pass adds one cluster, so the loop runs $k - 1$ times when each chosen cluster can be split.
- **The SSE never rises.** For a split of $P$ into $A$ and $B$, $\mathrm{SSE}(A) + \mathrm{SSE}(B) \le \mathrm{SSE}(P)$, because $\mu(A)$ and $\mu(B)$ are the best centers of $A$ and $B$, at least as good as $\mu(P)$. In fact $\mathrm{SSE}(P) - \mathrm{SSE}(A) - \mathrm{SSE}(B) = \frac{|A||B|}{|A| + |B|}\|\mu(A) - \mu(B)\|^2$, the same quantity as the [Ward](/ward-method/) merge cost.
- **Each split is a 2-means fixed point.** Inside $P$, each point of $A$ is at least as near to $\mu(A)$ as to $\mu(B)$, and the other way round, by the correctness of Lloyd's algorithm.
- **Termination.** Each 2-means run stops, and there are $r(k - 1)$ runs.

The proofs are in the proofs section below. The final partition is in general not a fixed point of Lloyd's algorithm on the whole data, because a point is compared only with the centers of its own split. Running Lloyd's algorithm on the whole data from the final centers can lower the cost further.

## Complexity

**Time.** A 2-means run on a cluster of $m$ points costs $O(m d)$ per iteration, so $O(m d r t)$ for one split with $r$ runs of $t$ iterations each. The total depends on the sizes of the split clusters:

- **Balanced splits.** If each split halves a cluster, each point takes part in about $\log_2 k$ splits, and the time is $O(n d r t \log k)$.
- **Worst case.** If each split removes only a few points, the large cluster is split $k - 1$ times, and the time is $O(n k d r t)$.

The number $t$ of Lloyd iterations has the same worst case as for [k-means](/k-means/), but is small in practice. Each assignment step compares a point with 2 centers instead of $k$, which is why the method is fast for large $k$.

**Space.** The labels take $O(n)$ and the centers $O(kd)$. Keeping the tree adds $O(k)$.

## Properties

- **Randomized.** The splits depend on the random starts. With a fixed seed the result is fixed.
- **Hierarchical.** The splits form a binary tree with $k$ leaves; cutting the tree at fewer leaves gives the clusterings for smaller $k$ at no extra cost.
- **Greedy.** A split is never undone. A poor first split stays in the result.
- **Balanced clusters with rule "largest".** The rule tends to give clusters of similar size, which is good for document collections and bad when the true clusters differ much in size.
- **No guarantee.** There is no bound on the ratio to the optimal k-means cost, as for plain k-means.

## Variants and improvements

- **Choice rule.** Split the largest cluster, the cluster with the largest SSE, or the cluster whose split lowers the total SSE the most (this needs a trial split of every cluster).
- **Refinement.** Run Lloyd's algorithm on all points from the $k$ final centers. The paper reports that this refinement helps a little.
- **PDDP.** Boley's principal direction divisive partitioning splits a cluster by the sign of the projection on its first [principal component](/principal-component-analysis/), with no random start. It can also seed the 2-means run.
- **Choice of $k$.** [X-means](/x-means/) and [G-means](/g-means/) also split clusters in two, but use a statistical test to decide whether to split at all.
- **Agglomerative alternative.** The [Ward method](/ward-method/) builds a tree from the bottom up with the same SSE criterion.

## When to use it

Use it when $k$ is large, when you want a hierarchy of clusters, or when plain k-means from random starts gives poor results, as was the case for text documents. It is also a reasonable seeding for Lloyd's algorithm. When $k$ is small and a good seeding such as [k-means++](/k-means-plus-plus/) is available, plain k-means with restarts is usually as good and simpler.

## Pitfalls

- **Rule not stated.** Results differ much between the rules "largest" and "sse"; report which one is used.
- **Clusters that cannot be split.** A cluster of one point, or of identical points, cannot be split by 2-means. The loop must skip it or it never ends.
- **One run per split.** A single 2-means run can give a poor split that stays for ever. Use several runs ($r > 1$) and keep the best.
- **Expecting a Lloyd fixed point.** The final clusters need not be a fixed point of Lloyd's algorithm on the whole data. Refine at the end if that matters.
- **Unscaled features.** As for all k-means methods, a feature with a large range dominates the distance.

## Implementations

## History

Steinbach, Karypis and Kumar presented bisecting k-means in 2000 at the KDD workshop on text mining. On document collections it gave better clusters than plain k-means and clusters as good as or better than agglomerative clustering, at a lower cost. Boley's PDDP of 1998 is a related divisive method with a deterministic split. The method is in the textbook of Tan, Steinbach and Kumar, and scikit-learn added it in 2022 as `BisectingKMeans`.

## References
