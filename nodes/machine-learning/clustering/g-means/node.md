---
tag: 3WDD1J
kind: algorithm
slug: g-means
name: G-means
aliases:
- G-means clustering
area: machine-learning/clustering
level: advanced
summary: Increases k until every cluster passes a Gaussianity test.
solves: [k-means-problem]
model: real-ram
complexity:
  vars: {n: the number of points, d: the dimension, k: the number of clusters returned, t: the number of Lloyd iterations per run}
  time: {worst: "O(n k^2 d t + n k d^2)"}
  space: {extra: "O(n + k d + d^2)"}
properties: {deterministic: false, exact: false, online: false, recursive: false}
history:
  year: 2003
  people: [Greg Hamerly, Charles Elkan]
  note: Hamerly and Elkan replaced the BIC of X-means by an Anderson-Darling test of normality on a one dimensional projection.
prereqs: [k-means]
see_also: [x-means, k-means, bisecting-k-means, gaussian-mixture-model, principal-component-analysis, power-iteration, elbow-method, gap-statistic]
sources:
  - paper: "Greg Hamerly and Charles Elkan, Learning the k in k-means, Advances in Neural Information Processing Systems 16 (NIPS 2003), MIT Press, 2004, pages 281 to 288"
    locator: the G-means algorithm, the split initialization c ± s sqrt(2λ/π), the projection on v = c1 - c2, and the test with α = 0.0001 and critical value 1.8692
  - paper: doi:10.1080/01621459.1974.10480196
    title: M. A. Stephens, EDF statistics for goodness of fit and some comparisons, Journal of the American Statistical Association 69(347), 1974, pages 730 to 737
    locator: the normal case with estimated mean and variance, and the modified statistic A²(1 + 4/n - 25/n²)
  - paper: doi:10.1214/aoms/1177729437
    title: T. W. Anderson and D. A. Darling, Asymptotic theory of certain goodness of fit criteria based on stochastic processes, Annals of Mathematical Statistics 23(2), 1952, pages 193 to 212
    locator: the statistic with the weight 1/(F(1 - F))
  - paper: "Dan Pelleg and Andrew Moore, X-means: extending K-means with efficient estimation of the number of clusters, Proceedings of the 17th International Conference on Machine Learning (ICML), 2000, pages 727 to 734"
    locator: the BIC based method that G-means is compared with
---

G-means is a heuristic that runs [k-means](/k-means/) and also chooses the number of clusters $k$. It starts with one center. For each cluster it makes a trial split along the main principal direction, runs 2-means on the points of the cluster, and projects the points onto the line through the two new centers. If the projected values fail an Anderson-Darling test of normality, the cluster is split. This repeats until every cluster passes the test. Hamerly and Elkan (2003) proposed it and used the significance level $\alpha = 0.0001$, with the critical value $1.8692$ for the corrected statistic. It has no guarantee on $k$: the test checks one direction per cluster, and the result depends on $\alpha$.

## In plain words

You want to group points, but you do not know how many groups there are. G-means makes one assumption: a good group looks like a bell shaped cloud, a Gaussian. So it asks a question about each group: does this group look like one bell, or like two bells side by side?

To answer, it splits the group in two as a trial. Then it looks at the points along the line that joins the two halves. If the group is one bell, the values along this line also form one bell. If the group is two bells, the values form two humps. A standard statistical test tells the two cases apart. When the test says "not one bell", the group is split for real. When every group passes, the method stops.

## The problem

The input is a list of points $x_1, \ldots, x_n \in \mathbb{R}^d$ with the Euclidean norm, a significance level $\alpha$ (or its critical value), and an upper bound $k_{\max}$. The output is a number $k \le k_{\max}$ and a k-means clustering with $k$ clusters. The goal is that each cluster looks like a sample from one Gaussian. This is a heuristic for choosing $k$, not an algorithm for an exact problem: the test can accept a cluster that is not Gaussian, and with the strict level $\alpha = 0.0001$ it accepts small mixtures of two clusters that are close.

**The test.** Let $y_1, \ldots, y_n$ be values in one dimension. Standardize them with the sample mean and the sample standard deviation, and let $z_{(1)} \le \cdots \le z_{(n)}$ be the values of the standard normal distribution function $\Phi$ at the sorted standardized values. The Anderson-Darling statistic and its correction for estimated mean and variance (Stephens 1974) are
$$A^2 = -n - \frac{1}{n}\sum_{i=1}^{n} (2i - 1)\big[\ln z_{(i)} + \ln\big(1 - z_{(n+1-i)}\big)\big], \qquad A_*^2 = A^2\Big(1 + \frac{4}{n} - \frac{25}{n^2}\Big).$$
Large values mean that the values are far from a normal sample. The statistic gives extra weight to the tails, so it detects two humps well. G-means rejects normality, and splits, when $A_*^2 > 1.8692$, the critical value for $\alpha = 0.0001$ in the paper.

## The algorithm

```pseudo id=main
GMEANS(x_1..x_n, critical value, k_max)
L1  C ← {the mean of all the points}
L2  run Lloyd's algorithm from the centers C
L3  for each center c with points X (skip X if it is very small or k_max is reached) do
L4      s, λ ← the main eigenvector and eigenvalue of the covariance of X
L5      run 2-means on X from the two centers c ± s √(2λ/π), giving c_1 and c_2
L6      v ← c_1 - c_2; project each x in X to <x, v> / ||v||²
L7      A*² ← the corrected Anderson-Darling statistic of the projected values
L8      if A*² > critical value then replace c by c_1 and c_2 in C, else keep c
L9  if no center was replaced then return C and the labels; else go to L2
```

Line L5 places the children where the halves of a Gaussian would have their means: for a normal variable with variance $\lambda$, the mean of its positive half is $\sqrt{2\lambda/\pi}$. Line L6 reduces the test to one dimension. The direction $v$ is the one along which a split would separate the cluster, so it is the direction in which a mixture of two Gaussians is easiest to see. The scale of $v$ does not matter, because line L7 standardizes the values. The implementation finds $s$ by [power iteration](/power-iteration/) and skips clusters with fewer than 8 points, where the test has little power.

## Example

Take 20 numbers in $d = 1$: the two blocks $0, 1, \ldots, 9$ and $30, 31, \ldots, 39$.

| step | values | result |
|---|---|---|
| L1, L2 | one center | $c = 19.5$, variance $\lambda = 233.25$ |
| L5 | children $19.5 \pm \sqrt{2 \cdot 233.25/\pi}$ | start at $7.31$ and $31.69$; 2-means ends at $4.5$ and $34.5$ |
| L7 | $A_*^2$ of the 20 values | $2.0019 > 1.8692$, so split |
| L2 to L7 | each block $0, \ldots, 9$ | $A_*^2 = 0.1623$, so keep |
| L9 | no more splits | $k = 2$, centers $4.5$ and $34.5$ |

In one dimension the projection of line L6 is an affine map of the values, so the test sees the values themselves. Now move the second block closer, to $20, \ldots, 29$. Then $A_*^2 \approx 1.305$. This is far above the 5 percent critical value, which is below $0.8$, but below $1.8692$, so G-means keeps one cluster. With $10, \ldots, 19$ the statistic is only $0.251$: the 20 values are evenly spaced and look normal enough. The strict level makes G-means slow to split small clusters, and the tests check both cases.

## Correctness

The method is a heuristic, so the claims are about its behavior:

- **Termination.** Each pass that does not return adds at least one center, and the number of centers never exceeds $k_{\max}$. So there are at most $k_{\max}$ passes, and each pass runs finitely many Lloyd iterations.
- **The output is a Lloyd fixed point.** The returned centers come from line L2, so each center is the mean of its points and each point is with a nearest center.
- **The test is the right test.** The statistic of line L7 is the Anderson-Darling statistic for normality with estimated mean and variance, with Stephens' correction. It does not change if $v$ is scaled or its sign is flipped.

The proofs are in the proofs section below. What the method does not have is a guarantee on $k$. The test checks one direction per cluster. A cluster can be non-Gaussian in a direction that the split does not find, and with many points a cluster that is only slightly non-Gaussian is split. The level $\alpha$ is applied to each test with no correction for the many tests in a run.

## Complexity

**Time.** One Lloyd iteration with $K$ centers costs $O(nKd)$. For the tests of one pass, the covariance matrices cost $O(nd^2)$ in total and the local 2-means runs cost $O(nd)$ per iteration, because the clusters are disjoint. The statistic needs a sort, $O(n \log n)$ in total. If $k$ grows by one per pass, the total is $O(nk^2dt + nkd^2)$. If many clusters split in each pass, the number of passes is about $\log_2 k$, and the cost is closer to that of a few runs of k-means with $k$ centers.

**Space.** The labels take $O(n)$, the centers $O(kd)$, and one covariance matrix $O(d^2)$.

## Properties

- **Few parameters.** The only parameter is $\alpha$, a statistical level with a clear meaning. There is no $k$ to give, only a cap.
- **Randomized in this implementation.** Power iteration starts from a random vector. When the main eigenvalue is unique, the result does not depend on it, because a flip of $s$ only swaps the two children.
- **Local decisions.** Each test uses only the points of one cluster.
- **Model based.** The test assumes Gaussian clusters, but of any covariance: an elongated Gaussian passes, because only the projection on $v$ is tested.
- **Only splits.** Clusters are never merged. A wrong split stays.

## Variants and improvements

- **[X-means](/x-means/).** Pelleg and Moore use the Bayesian information criterion of a spherical model instead of a test. Hamerly and Elkan report that X-means chooses too many clusters on data with elongated or overlapping Gaussian clusters, where G-means is closer to the true $k$.
- **PG-means.** Feng and Hamerly (2006) fit a [Gaussian mixture model](/gaussian-mixture-model/) by EM and test random projections with the Kolmogorov-Smirnov test.
- **Dip-means.** Kalogeratos and Likas (2012) test unimodality, not normality, with the dip test, so the clusters need not be Gaussian.
- **Other tests.** Any one dimensional normality test fits line L7. The Anderson-Darling test is chosen for its power against mixtures.
- **Other ways to choose $k$.** The [elbow method](/elbow-method/), the [gap statistic](/gap-statistic/) and the [silhouette coefficient](/silhouette-coefficient/) compare runs of k-means with different $k$.

## When to use it

Use it when the number of clusters is unknown and the clusters are roughly Gaussian, even if they are elongated. It needs only a significance level, so it is easy to tune. When the clusters have arbitrary shape, prefer a density method such as [DBSCAN](/dbscan/). When you want soft assignments and full covariances, fit a Gaussian mixture model for several $k$ instead.

## Pitfalls

- **Large clusters are split too much.** With thousands of points the test detects tiny departures from normality, so real data that is only close to Gaussian is cut into many pieces. A smaller $\alpha$, or a test on a subsample, helps.
- **Small clusters are not split.** With few points the test has little power, as the example shows. Do not trust $k = 1$ on a small sample.
- **Duplicate points.** If all projected values are equal, the standard deviation is zero and the statistic is undefined. Treat the cluster as Gaussian.
- **Wrong critical value.** The critical value depends on the form of the statistic. The value $1.8692$ belongs to $A_*^2$ with Stephens' correction for estimated mean and variance; do not use it with the plain $A^2$ or with known parameters.
- **Scale.** The covariance and the distances depend on the units. Standardize the features if they have different units.

## Implementations

## History

Hamerly and Elkan presented G-means at NIPS 2003 under the title "Learning the k in k-means". It followed X-means (Pelleg and Moore, 2000), which used the BIC. The test comes from Anderson and Darling (1952), and the correction for estimated parameters from Stephens (1974). Later work replaced the test by projections of a full mixture (PG-means, 2006) and by a test of unimodality (dip-means, 2012).

## References
