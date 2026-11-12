---
tag: X2J8SA
kind: algorithm
slug: x-means
name: X-means
aliases:
- X-means clustering
area: machine-learning/clustering
level: advanced
summary: K-means that chooses k automatically by splitting clusters when the BIC improves.
solves: [k-means-problem]
model: real-ram
complexity:
  vars: {n: the number of points, d: the dimension, k: the largest number of clusters tried, t: the number of Lloyd iterations per run}
  time: {worst: "O(n k^2 d t)"}
  space: {extra: "O(n + k d)"}
properties: {deterministic: false, exact: false, online: false, recursive: false}
history:
  year: 2000
  people: [Dan Pelleg, Andrew Moore]
  note: Pelleg and Moore combined k-means, local 2-means splits and the Bayesian information criterion, with kd-trees for speed.
prereqs: [k-means]
see_also: [g-means, k-means, bisecting-k-means, gaussian-mixture-model, maximum-likelihood-estimation, minimum-description-length, elbow-method, gap-statistic]
sources:
  - paper: "Dan Pelleg and Andrew Moore, X-means: extending K-means with efficient estimation of the number of clusters, Proceedings of the 17th International Conference on Machine Learning (ICML), 2000, pages 727 to 734"
    locator: Section 3 (Improve-Params and Improve-Structure), Section 3.2 (the BIC score of a model with spherical Gaussians)
  - paper: doi:10.1214/aos/1176344136
    title: Gideon Schwarz, Estimating the dimension of a model, Annals of Statistics 6(2), 1978, pages 461 to 464
    locator: the criterion log-likelihood minus (p/2) log n
  - paper: "Greg Hamerly and Charles Elkan, Learning the k in k-means, Advances in Neural Information Processing Systems 16 (NIPS 2003), MIT Press, 2004, pages 281 to 288"
    locator: the comparison of G-means with X-means, which overfits on some data
---

X-means is a heuristic that runs [k-means](/k-means/) and also chooses the number of clusters $k$. It starts from a small $k$, runs Lloyd's algorithm, and then tries to split each cluster in two with a local 2-means run. A split is kept when it raises the Bayesian information criterion (BIC) of the points of that cluster, computed for a model of spherical Gaussians. This repeats until no split helps or $k$ reaches a limit, and the model with the best BIC is returned. Pelleg and Moore (2000) proposed it. It has no guarantee: the BIC is an asymptotic criterion, and the result depends on the model, the random splits and the exact BIC formula.

## In plain words

Plain k-means needs you to say how many groups there are. X-means tries to find out. It starts with few groups. Then it asks, for each group: would this group be better described as two groups? It tries the split and compares two scores.

The score rewards a good fit to the data, but it also charges a price for each extra number the model needs. A split always fits better, so it must fit enough better to pay its price. If it does, the group is split. The method repeats until no group wants to split, and it keeps the best scoring answer it has seen.

## The problem

The input is a list of points $x_1, \ldots, x_n \in \mathbb{R}^d$ with the Euclidean norm, a lower bound $k_{\min}$ and an upper bound $k_{\max}$ on the number of clusters, and a source of random numbers. The output is a number $k$ between $k_{\min}$ and $k_{\max}$ and a k-means clustering with $k$ clusters. The goal is a $k$ that matches the data, measured by the BIC of a model in which each cluster is a spherical Gaussian. There is no guarantee that the chosen $k$ is correct, even for data drawn from such a mixture; this is a heuristic for model selection.

**The score.** For $R$ points, $K$ clusters of sizes $R_1, \ldots, R_K$, and squared error $\mathrm{SSE}$ to the cluster means, the model has a common variance and the log-likelihood with hard assignments:
$$\hat\sigma^2 = \frac{\mathrm{SSE}}{d(R - K)}, \qquad \ell = \sum_{j} R_j \log\frac{R_j}{R} - \frac{Rd}{2}\log(2\pi\hat\sigma^2) - \frac{\mathrm{SSE}}{2\hat\sigma^2} .$$
The model has $p = (K - 1) + Kd + 1$ free parameters: the mixing weights, the means and the variance. The score is
$$\mathrm{BIC} = \ell - \frac{p}{2}\log R .$$
The paper writes the variance and the log-likelihood in a slightly different form, and published implementations differ in these details. The form above is consistent: $\ell$ is exactly the log-likelihood of the hard clustering under the model, and the tests check this.

## The algorithm

```pseudo id=main
XMEANS(x_1..x_n, k_min, k_max)
L1  run Lloyd's algorithm from the current centers (at first, k_min random points)
L2  compute the BIC of the whole model; remember the model if it is the best so far
L3  if the number of centers ≥ k_max then return the best model
L4  for each cluster j, with points X_j and center c_j do
L5      put two children at c_j ± r u (u a random unit vector, r the RMS radius of X_j), and run 2-means on X_j
L6      compute the BIC on X_j of the parent (one Gaussian) and of the children (two Gaussians)
L7      if BIC(children) > BIC(parent) then mark j
L8  if no cluster is marked then return the best model
L9  replace each marked center by its two children (best gains first, at most k_max centers); go to L1
```

Lines L1 and L2 are the "Improve-Params" step of the paper and lines L4 to L9 are the "Improve-Structure" step. The test of line L7 is local: it compares the two models only on the points of cluster $j$. Line L9 caps the number of centers at $k_{\max}$ by keeping the splits with the largest gains. The paper speeds up the 2-means runs and the assignment step with kd-trees; the implementation here does not.

## Example

Take six numbers in $d = 1$, and test one split.

**Two groups: $0, 1, 2, 10, 11, 12$.** The parent has mean 6 and $\mathrm{SSE} = 154$, so $\hat\sigma^2 = 154/5 = 30.8$ and $\mathrm{BIC} \approx -20.09$. The children $\{0, 1, 2\}$ and $\{10, 11, 12\}$ have $\mathrm{SSE} = 4$, so $\hat\sigma^2 = 4/4 = 1$ and $\mathrm{BIC} = 6\log\frac12 - 3\log(2\pi) - 2 - 2\log 6 \approx -15.26$. The children score higher, so X-means splits.

**One group: $0, 1, 2, 3, 4, 5$.** The parent has $\mathrm{SSE} = 17.5$ and $\hat\sigma^2 = 3.5$, so $\mathrm{BIC} \approx -13.56$. The children $\{0, 1, 2\}$ and $\{3, 4, 5\}$ again have $\mathrm{SSE} = 4$ and $\mathrm{BIC} \approx -15.26$. The fit is better, but not enough to pay for the two extra parameters, so X-means keeps one cluster.

## Correctness

The method is a heuristic, so the claims are about its behavior:

- **Termination.** Each pass through line L9 adds at least one center, and the number of centers never exceeds $k_{\max}$. So there are at most $k_{\max} - k_{\min} + 1$ passes, and each pass runs finitely many Lloyd iterations.
- **The output.** The returned model is the one with the highest whole-data BIC among the models of line L2.
- **The score is a log-likelihood minus a penalty.** With the variance $\hat\sigma^2$, the expression $\ell$ is the sum over the points of $\log\big(\frac{R_j}{R}\,\mathcal{N}(x \mid c_j, \hat\sigma^2 I)\big)$, the log-likelihood of the hard clustering.

The proofs are in the proofs section below. What the method does not have is a guarantee on $k$. The BIC approximates the log of the marginal likelihood of a model only for large samples and regular models, and a hard k-means clustering is not the maximum likelihood fit of a Gaussian mixture. On data with clusters that are not spherical, or of different variances, X-means tends to choose too many clusters (Hamerly and Elkan, 2003).

## Complexity

**Time.** One Lloyd iteration with $K$ centers costs $O(nKd)$. The local 2-means runs of one pass cost $O(nd)$ per iteration in total, because the clusters are disjoint. A pass with $K$ centers therefore costs $O(nKdt)$. If the number of centers grows by one per pass, the sum over $K$ up to $k$ gives $O(nk^2dt)$; if many clusters split at once, the number of passes falls to about $\log_2 k$, and the total is closer to $O(nkdt)$.

**Space.** The labels take $O(n)$ and the centers $O(kd)$. The kd-tree of the paper takes $O(nd)$ more.

## Properties

- **Randomized.** The initial centers and the split directions are random. The result depends on the seed.
- **Local decisions.** A split is judged only on the points of one cluster, which is cheap but ignores the other clusters.
- **Model based.** The score assumes spherical Gaussian clusters with one common variance. Elongated clusters are split into several spherical ones.
- **Only splits.** Clusters are never merged. A wrong split stays unless the global BIC of line L2 prefers an earlier model.
- **A cap.** The result never has more than $k_{\max}$ clusters.

## Variants and improvements

- **Other criteria.** The Akaike information criterion has a smaller penalty and splits more. The [minimum description length](/minimum-description-length/) gives a similar trade-off.
- **[G-means](/g-means/).** Hamerly and Elkan replace the BIC by a test of normality of the projection on the split direction. It is less prone to overfitting when the clusters are not spherical.
- **Full mixtures.** Fit a [Gaussian mixture model](/gaussian-mixture-model/) by EM for each $k$ and compare the BIC of the full likelihood. This is slower but uses a better model.
- **Global split test.** Compare the BIC of the whole model with and without each split, instead of the local test.
- **Other ways to choose $k$.** The [elbow method](/elbow-method/), the [gap statistic](/gap-statistic/) and the [silhouette coefficient](/silhouette-coefficient/) compare runs of k-means with different $k$.

## When to use it

Use it when the number of clusters is unknown, the clusters are compact and roughly spherical with similar spread, and you want a fast automatic choice of $k$. Give a sensible $k_{\max}$. When the clusters are elongated or of very different variances, prefer G-means or a full Gaussian mixture with BIC, and when the clusters have arbitrary shape, prefer a density method such as [DBSCAN](/dbscan/).

## Pitfalls

- **The exact BIC formula matters.** Different formulas for the variance and the number of parameters lead to different $k$. Report the formula you use.
- **Scale.** The model has one variance for all features. Standardize the features first.
- **Small clusters.** For a cluster with very few points the BIC is unreliable, and with $R \le K$ the variance is undefined. Do not test such clusters.
- **Duplicate points.** If a child has zero variance, its likelihood is infinite and the split always wins. Guard against this case.
- **Trusting $k$.** The chosen $k$ is the answer of a model. Check it with a [cluster validity](/cluster-validity/) measure or with domain knowledge.

## Implementations

## History

Pelleg and Moore presented X-means at ICML 2000. It built on their earlier work on kd-trees for fast k-means, and it used the criterion of Schwarz (1978), as justified for mixtures by Kass and Wasserman. Hamerly and Elkan (2003) observed that X-means overfits on non-spherical data and proposed G-means with a statistical test instead of BIC.

## References
