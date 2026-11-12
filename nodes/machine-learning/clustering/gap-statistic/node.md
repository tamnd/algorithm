---
tag: BXW1TS
kind: concept
slug: gap-statistic
name: Gap statistic
aliases:
- Tibshirani gap statistic
- gap statistic for the number of clusters
area: machine-learning/clustering
level: advanced
summary: "Gap(k) = E*[log W_k] - log W_k, with E* over uniform reference data. Choose the smallest k with Gap(k) >= Gap(k+1) - s_(k+1). It can return k = 1."
prereqs: [elbow-method, k-means, uniform-distribution]
see_also: [silhouette-coefficient, calinski-harabasz-index, x-means, g-means, principal-component-analysis, monte-carlo-integration, cluster-validity]
sources:
  - paper: doi:10.1111/1467-9868.00293
    title: "Robert Tibshirani, Guenther Walther and Trevor Hastie, Estimating the number of clusters in a data set via the gap statistic, Journal of the Royal Statistical Society, Series B 63(2), 2001, pages 411 to 423"
    locator: the pooled dispersion W_k, the definition of Gap_n(k), the two uniform reference distributions, the computation with B reference sets and s_k, the rule for k, and the simulations
  - book: isbn:9780387848570
    title: Trevor Hastie, Robert Tibshirani and Jerome Friedman, The Elements of Statistical Learning, second edition, Springer, 2009
    locator: Section 14.3 (cluster analysis), the choice of the number of clusters with the gap statistic
---

The gap statistic chooses the number $k$ of clusters by comparing the within-cluster dispersion $W_k$ of the data with its value for data that have no clusters. For each $k$, it computes $\mathrm{Gap}(k) = E^*[\log W_k] - \log W_k$, where $E^*$ is the mean over $B$ reference data sets drawn from a uniform distribution over the range of the data. Then it takes the smallest $k$ whose gap is not clearly below the gap at $k + 1$. Tibshirani, Walther and Hastie introduced it in 2001 as a formal version of the [elbow method](/elbow-method/). Unlike the elbow and most internal [validity indices](/cluster-validity/), it can return $k = 1$: no cluster structure.

## In plain words

More groups always make the groups tighter, even when the data have no groups at all. So the drop in spread alone does not tell you if the groups are real.

The gap statistic makes fake data sets with no groups: points scattered evenly over the same region as your data. It groups the fake data in the same way, for each number of groups, and measures their spread too. If your data have real groups, then at the right number of groups your spread is much smaller than the spread of the fake data. The gap is the size of that difference.

You choose the smallest number of groups after which the gap does not clearly grow. Because the fake data are random, "clearly" uses the spread of the results over many fake data sets.

## The idea

**Setting.** $X = \{x_1, \ldots, x_n\}$ is a set of $n$ points in $\mathbb{R}^d$, and $k$ is not given. A clustering method, here [k-means](/k-means/), gives for each $k$ a clustering $C_1, \ldots, C_k$ with $n_r = |C_r|$.

**Dispersion.** With $D_r = \sum_{x, y \in C_r} \|x - y\|^2$, the sum over ordered pairs in cluster $r$,

$$W_k = \sum_{r=1}^{k} \frac{D_r}{2 n_r}.$$

For the squared Euclidean distance, $D_r/(2 n_r) = \sum_{x \in C_r} \|x - c_r\|^2$ with the centroid $c_r$, so $W_k$ is the within-cluster sum of squares of the [k-means problem](/k-means-problem/). The paper allows any dissimilarity in $D_r$.

**The gap.**

$$\mathrm{Gap}_n(k) = E^*_n[\log W_k] - \log W_k,$$

where $E^*_n$ is the expectation for a sample of size $n$ from a reference distribution. The logarithm puts the comparison on a ratio scale: a gap of 0.7 means that the data have about half the dispersion of the reference.

**The reference distribution.** The paper gives two choices:

- **(a) The box.** Uniform over the bounding box of the data: each feature uniform over its observed range.
- **(b) The principal component box.** Center the data, rotate it to its [principal components](/principal-component-analysis/), take the bounding box there, draw uniform points in that box, and rotate them back. This box follows the shape of the data, so the reference is closer to the data when the cloud is long and tilted.

The uniform law is the null model because it has no modes. The authors argue that among unimodal laws it is the one most likely to produce false clusters, and they prove a version of this for one dimension.

**Computation.**

1. Cluster the data for $k = 1, \ldots, K$ and compute $W_k$.
2. Draw $B$ reference data sets of size $n$, cluster each for $k = 1, \ldots, K$, and compute $W^*_{kb}$.
3. Let $\bar\ell_k = \frac{1}{B} \sum_b \log W^*_{kb}$, so $\mathrm{Gap}(k) = \bar\ell_k - \log W_k$. This is a [Monte Carlo](/monte-carlo-integration/) estimate of the expectation.
4. Let $\mathrm{sd}_k$ be the standard deviation of the $\log W^*_{kb}$ over $b$, and $s_k = \mathrm{sd}_k \sqrt{1 + 1/B}$. The factor accounts for the error of the mean $\bar\ell_k$ itself.
5. Choose
$$\hat k = \text{the smallest } k \text{ such that } \mathrm{Gap}(k) \ge \mathrm{Gap}(k + 1) - s_{k+1}.$$

The implementation computes $\mathrm{sd}_k$ with the divisor $B$; some software uses $B - 1$, which changes $s_k$ only a little for $B \ge 10$. If no $k < K$ meets the rule, it returns $K$, a sign that $K$ is too small. Its random choices come from a seeded `random.Random`, so a run can be repeated. The k-means inside uses k-means++ seeds and the best of 3 runs of Lloyd's algorithm.

**Cost.** $(B + 1) K$ clusterings of $n$ points. With $B = 10$ and $K = 6$, that is 66 runs of k-means, each repeated 3 times in the implementation. The extra cost over the elbow method is the price of a null model.

**Why the rule looks only at the next $k$.** The rule is a one-standard-error rule: it accepts the smaller $k$ unless the next one is better by more than the noise. This keeps $\hat k$ small. It also means that the rule can stop before a larger and much better $k$, as the third example shows.

## Examples

**Three clusters.** Draw 25, 25 and 50 points from standard normal laws centered at $(0, 0)$, $(0, 5)$ and $(5, -3)$, with $K = 6$, $B = 10$ and the box reference. One run gives:

| $k$ | 1 | 2 | 3 | 4 | 5 | 6 |
|---|---|---|---|---|---|---|
| Gap$(k)$ | 0.054 | 0.878 | 1.189 | 1.011 | 0.926 | 1.011 |
| $s_k$ | 0.047 | 0.059 | 0.056 | 0.049 | 0.049 | 0.065 |

For $k = 1$: $0.054 < 0.878 - 0.059$. For $k = 2$: $0.878 < 1.189 - 0.056$. For $k = 3$: $1.189 \ge 1.011 - 0.049$, so $\hat k = 3$. The principal component box gives the same choice, with gaps 0.016, 0.467, 0.914, 0.871, 0.710 and 0.793. Over ten random data sets of this kind, the box reference gave $\hat k = 3$ every time.

**No clusters.** For 60 points uniform in the unit square, with $K = 4$ and $B = 10$, one run gives the gaps 0.066, $-0.009$, 0.113 and 0.022, with $s_2 = 0.070$. Then $0.066 \ge -0.009 - 0.070$, so $\hat k = 1$. Over ten such data sets, the rule returned 1 nine times and 2 once. The elbow method and the indices that need $k \ge 2$ cannot give this answer.

**A pitfall: three clusters on a line.** Draw 15 points from normal laws with standard deviation 0.5 around each of $(0, 0)$, $(5, 0)$ and $(10, 0)$. One run with $K = 5$ gives

| $k$ | 1 | 2 | 3 | 4 | 5 |
|---|---|---|---|---|---|
| Gap$(k)$ | $-0.392$ | $-0.392$ | 1.070 | 0.856 | 1.002 |
| $s_k$ | 0.129 | 0.105 | 0.113 | 0.079 | 0.098 |

The largest gap is at $k = 3$, but the rule already stops at $k = 1$, because $\mathrm{Gap}(1) \ge \mathrm{Gap}(2) - s_2$. The data put more of their mass near the ends of their box than a uniform law, so $k = 1$ and $k = 2$ fit them worse than they fit the reference. A split into two clusters is no better relative to the reference than one cluster. Over ten such data sets the rule returned 1 nine times, with either reference. Plot the whole gap curve, not only $\hat k$.

## Where it is used

- Choosing $k$ for [k-means](/k-means/), [partitioning around medoids](/partitioning-around-medoids/) and [hierarchical clustering](/hierarchical-clustering-problem/) cut at $k$ clusters, as in the `clusGap` function of the R package cluster.
- Deciding whether a data set has any cluster structure at all, which internal indices such as the [silhouette coefficient](/silhouette-coefficient/) and the [Calinski-Harabasz index](/calinski-harabasz-index/) cannot do.
- As a model for other rules that compare a statistic with its value under a null reference, such as [G-means](/g-means/), which tests each cluster for a normal shape, and [X-means](/x-means/), which uses an information criterion.

## References
