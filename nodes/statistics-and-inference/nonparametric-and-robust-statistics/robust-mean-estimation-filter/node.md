---
tag: VJ455W
kind: algorithm
slug: robust-mean-estimation-filter
name: Filter algorithm for robust mean estimation
aliases:
- spectral filtering for robust estimation
area: statistics-and-inference/nonparametric-and-robust-statistics
level: research
summary: Estimates a high-dimensional mean under epsilon contamination by repeatedly removing points far along the top eigenvector of the covariance. Its error does not grow with the dimension.
model: real-ram
complexity:
  vars: {n: the number of points, d: the dimension, k: the number of power iteration steps in a round, r: the number of rounds}
  time: {worst: O(n (n d² + k d²)), average: O(r (n d² + k d²)), best: O(n d² + k d²)}
  space: {extra: O(n + d²)}
properties: {deterministic: true, randomized: false, exact_in_exact_arithmetic: false, in_place: false, online: false}
history:
  year: 2016
  people: [Ilias Diakonikolas, Gautam Kamath, Daniel M. Kane, Jerry Li, Ankur Moitra, Alistair Stewart]
  note: Diakonikolas, Kamath, Kane, Li, Moitra and Stewart gave the filter in 2016 as the first polynomial-time estimator of a high-dimensional Gaussian mean with an error independent of the dimension. Lai, Rao and Vempala gave a related spectral method at the same conference.
prereqs: [huber-contamination-model, breakdown-point, median, covariance-matrix, power-iteration, eigenvalue]
see_also: [tukey-median, halfspace-depth, geometric-median, minimum-covariance-determinant, robust-pca, principal-component-analysis, semidefinite-programming, median-absolute-deviation]
sources:
  - paper: doi:10.1137/17M1126680
    title: Ilias Diakonikolas, Gautam Kamath, Daniel M. Kane, Jerry Li, Ankur Moitra and Alistair Stewart, Robust estimators in high-dimensions without the computational intractability, SIAM Journal on Computing 48(2), 2019
    locator: pp. 742 to 864, Section 5 (the filter for the mean of an identity-covariance Gaussian and its error bound)
  - paper: doi:10.1109/FOCS.2016.85
    title: Ilias Diakonikolas, Gautam Kamath, Daniel M. Kane, Jerry Li, Ankur Moitra and Alistair Stewart, Robust estimators in high dimensions without the computational intractability, FOCS 2016
    locator: pp. 655 to 664 (the conference version)
  - paper: doi:10.1109/FOCS.2016.76
    title: Kevin A. Lai, Anup B. Rao and Santosh Vempala, Agnostic estimation of mean and covariance, FOCS 2016
    locator: pp. 665 to 674 (a spectral method with an error that depends on log d)
  - book: isbn:9781108837811
    title: Ilias Diakonikolas and Daniel M. Kane, Algorithmic High-Dimensional Robust Statistics, Cambridge University Press, 2023
    locator: the chapters on robust mean estimation (stability, the filter and its weighted version)
  - paper: doi:10.1214/aoms/1177703732
    title: Peter J. Huber, Robust estimation of a location parameter, The Annals of Mathematical Statistics 35(1), 1964
    locator: pp. 73 to 101 (the contamination model)
---

The filter estimates the mean of a high-dimensional distribution when an $\varepsilon$ fraction of the sample is replaced by arbitrary points. It keeps a weight for every point. In each round it computes the weighted mean and the weighted covariance matrix and finds the top eigenvalue $\lambda$ and its eigenvector $v$. If $\lambda$ is close to the variance of the clean data, the outliers cannot have moved the mean much, so it returns the weighted mean. Otherwise it lowers the weight of each point in proportion to its squared projection on $v$. For a Gaussian with identity covariance, Diakonikolas et al. (2019) prove an error of $O(\varepsilon\sqrt{\log(1/\varepsilon)})$, with no factor that grows with the dimension $d$. In the [contamination model](/huber-contamination-model/) the sample mean can be moved arbitrarily far, and the coordinatewise [median](/median/) has an error that grows like $\varepsilon\sqrt d$.

## In plain words

Suppose most of the points come from a round cloud and a few were planted by an adversary. If the planted points pull the average away, they must stretch the cloud in the direction of the pull. So the algorithm looks for the direction in which the cloud is most stretched. If that stretch is about as large as for clean data, it stops and returns the average. If not, the points that lie far out along that direction are suspicious. It lowers their weights, more for points that lie farther out, and repeats. Because the planted points cause the stretch, they lose more weight than the clean points.

## The problem

The input is $N$ points $x_1, \ldots, x_N \in \mathbb R^d$ and the fraction $\varepsilon < 1/2$. In the strong contamination model an adversary draws $N$ points from $N(\mu, I_d)$, sees them, and replaces any $\varepsilon N$ of them. The goal is an estimate $\hat\mu$ with a small $\|\hat\mu - \mu\|$. Write $G$ for the indices of the clean points and $B$ for the replaced ones. The algorithm does not know $G$ and $B$.

For weights $w_i \ge 0$ with $W = \sum_i w_i > 0$, put $\mu_w = \frac1W\sum_i w_i x_i$ and $\Sigma_w = \frac1W\sum_i w_i(x_i - \mu_w)(x_i - \mu_w)^{\mathsf T}$. The threshold is $\theta = 1 + C\varepsilon\log(1/\varepsilon)$. The implementation uses $C = 3$.

## The algorithm

```pseudo id=main
FILTER(x_1..x_N, ε, θ)
L1  w_i ← 1/N for every i
L2  repeat
L3      μ ← Σ w_i x_i / Σ w_i
L4      (λ, v) ← the top eigenvalue and a unit eigenvector of Σ_w, by power iteration
L5      if λ ≤ θ then return μ
L6      τ_i ← (vᵀ(x_i − μ))² for every i
L7      τ_max ← max{τ_i : w_i > 0}; if τ_i = τ_max for every i with w_i > 0 then return μ
L8      w_i ← w_i (1 − τ_i / τ_max) for every i
```

Line L8 is the soft version of the filter. The point that lies farthest along $v$ gets weight 0, and every other point loses a part of its weight in proportion to $\tau_i$. Line L7 handles the case where all remaining points lie at the same distance along $v$.

## Example

Take $N = 10$ points in the plane with $\varepsilon = 0.2$: the eight clean points $(\pm1, 0)$, $(0, \pm1)$, $(1, 1)$, $(-1, -1)$, $(1, -1)$, $(-1, 1)$, which have mean $(0, 0)$, and two planted points at $(4, 4)$. The threshold is $\theta = 1 + 3 \cdot 0.2\log 5 = 1.966$.

**Round 0.** All weights are $0.1$. The mean is $(0.8, 0.8)$, and
$$\Sigma_w = \begin{pmatrix} 3.16 & 2.56 \\ 2.56 & 3.16 \end{pmatrix}, \qquad \lambda = 5.72, \qquad v = (1, 1)/\sqrt2.$$
Since $\lambda > \theta$, the filter acts. $\tau_i = (x_{i,1} + x_{i,2} - 1.6)^2/2$:

| point | (1,0) | (−1,0) | (0,1) | (0,−1) | (1,1) | (−1,−1) | (1,−1) | (−1,1) | (4,4) | (4,4) |
|---|---|---|---|---|---|---|---|---|---|---|
| $\tau_i$ | 0.18 | 3.38 | 0.18 | 3.38 | 0.08 | 6.48 | 1.28 | 1.28 | 20.48 | 20.48 |
| new $w_i$ | 0.0991 | 0.0835 | 0.0991 | 0.0835 | 0.0996 | 0.0684 | 0.0938 | 0.0938 | 0 | 0 |

The weighted mean of $\tau$ is $57.2/10 = 5.72 = \lambda$. The two planted points carry $40.96$ of the weighted sum $57.2$, more than half. They lose their whole weight $0.2$, and the clean points lose $16.24/204.8 = 0.0793$ together.

**Round 1.** The total weight is $0.7207$. The weighted mean is $(8/123, 8/123) \approx (0.065, 0.065)$, and $\lambda = 0.774 \le \theta$, so the filter returns it. For comparison, the sample mean is $(0.8, 0.8)$ and the coordinatewise median is $(0.5, 0.5)$. The output is not exactly $(0, 0)$, because the clean points that lay far along $v$ lost some weight too.

## Correctness

The page proves that the loop stops and that each round with a large bad share removes more bad weight than good weight. The error bound is cited, not proved. `proofs/correctness.md` has the proofs.

- **$\lambda$ is the weighted mean of $\tau$.** $\sum_i w_i\tau_i/W = v^{\mathsf T}\Sigma_w v = \lambda$.
- **Termination.** In a round that updates the weights, the points with $\tau_i = \tau_{\max}$ get weight 0, and, because line L7 did not return, some point keeps a positive weight. So the number of positive weights drops by at least 1 in each such round, and the loop returns within $N$ rounds with $W > 0$.
- **Removal lemma.** Point $i$ loses $w_i\tau_i/\tau_{\max}$. So the good points lose $\sum_G w_i\tau_i/\tau_{\max}$ and the bad points lose $\sum_B w_i\tau_i/\tau_{\max}$. If the bad points carry at least half of the weighted $\tau$, the good points lose at most as much as the bad ones.
- **Good weight is kept.** If the condition of the removal lemma holds in every round, the good points lose at most the initial bad weight $\varepsilon$, so they keep a weight of at least $1 - 2\varepsilon$.
- **The error bound (cited).** For an $\varepsilon$-corrupted sample of $N(\mu, I_d)$ of size of order $d/\varepsilon^2$ up to logarithmic factors, with high probability the condition of the removal lemma holds while $\lambda$ is above a threshold of the form $1 + C\varepsilon\log(1/\varepsilon)$, and a weighted mean with $\lambda$ below it and good weight at least $1 - 2\varepsilon$ is within $O(\varepsilon\sqrt{\log(1/\varepsilon)})$ of $\mu$ (Diakonikolas et al. 2019; Diakonikolas and Kane 2023).

## Complexity

- **One round.** The weighted mean costs $O(nd)$ and the weighted covariance matrix $O(nd^2)$. Power iteration with $k$ steps costs $O(kd^2)$. The projections cost $O(nd)$. So a round costs $O(nd^2 + kd^2)$. Without forming $\Sigma_w$, each power iteration step can multiply by $\Sigma_w$ in $O(nd)$, for $O(knd)$ in a round.
- **Rounds.** At most $n$ rounds, by the termination proof, so the worst case is $O(n(nd^2 + kd^2))$. In the tests 1 to 4 rounds were enough, because a cluster of planted points loses most of its weight in one round.
- **Space.** $O(n + d^2)$ for the weights and the covariance matrix.

## Properties

Proved on this page: termination, the identity for $\lambda$, the removal lemma, and the kept good weight under the condition of the lemma. Cited: the error bound and the sample size. Measured: everything in the tests below.

- **Error independent of $d$ (cited).** $O(\varepsilon\sqrt{\log(1/\varepsilon)})$ for $N(\mu, I_d)$, compared with $\Omega(\varepsilon)$ for any estimator, $\Theta(\varepsilon\sqrt d)$ in the worst case for the coordinatewise median, and no bound for the sample mean.
- **Measured against the sample mean.** 1000 points in $d = 10$ with 10% planted points from $N(s\,u, I)$, $u = (1, \ldots, 1)/\sqrt d$. The table shows $\|\hat\mu - \mu\|$ for two seeds. The last column is the mean of the clean points only, which no estimator can know.

| shift $s$ | seed | filter | sample mean | coordinatewise median | mean of clean points |
|---|---|---|---|---|---|
| 4 | 0 | 0.170 | 0.404 | 0.369 | 0.087 |
| 4 | 1 | 0.231 | 0.421 | 0.359 | 0.119 |
| 8 | 0 | 0.104 | 0.801 | 0.487 | 0.087 |
| 8 | 1 | 0.168 | 0.815 | 0.452 | 0.119 |

- **Measured against the dimension.** With shift 20 and 1000 points, the filter errors for $d = 5, 10, 20$ were $0.063, 0.124, 0.128$, close to the mean of the clean points ($0.045, 0.116, 0.132$). The coordinatewise median errors grew: $0.309, 0.465, 0.584$. The sample mean errors were about 2.0.
- **Measured removal condition.** In the run with shift 8, seed 0, the bad points carried more than half of the weighted $\tau$ in rounds 0 and 1, but not in round 2. Over the whole run the good points lost $0.0386$ of weight and the bad points $0.0948$.
- **Clean data.** On uncorrupted data with $\lambda \le \theta$ at the start, the filter returns the sample mean.
- **Moderate shifts are the hard case.** Planted points at shift 4 are harder to separate from the clean points than at shift 8, and the measured error was larger.

## Variants and improvements

- **Hard filter.** Remove the points whose projection on $v$ is larger than a threshold from a Gaussian tail bound (Diakonikolas et al. 2019). It has the same guarantee.
- **Unknown covariance.** Filters for the covariance matrix use the fourth moments, and the mean can then be estimated after whitening.
- **Heavy tails.** For distributions with bounded covariance, the same filter with threshold of order 1 gives error $O(\sqrt\varepsilon)$.
- **Faster versions.** Near-linear time algorithms replace the repeated eigenvector computation by matrix multiplicative weights.
- **Convex programming.** The ellipsoid-based separation method of the same paper, and sum-of-squares methods for other distributions. See [semidefinite programming](/semidefinite-programming/).
- **Related robust estimators.** The [Tukey median](/tukey-median/) has error $O(\varepsilon)$ but is hard to compute in high dimension. The [geometric median](/geometric-median/) is efficient but has an error that grows like $\varepsilon\sqrt d$.

## When to use it

Use the filter for the mean of high-dimensional data, with $d$ in the tens or more, when a fraction of the points may be corrupted in arbitrary ways and the clean distribution has a known or bounded covariance. In low dimension, the [minimum covariance determinant](/minimum-covariance-determinant/) and depth-based estimators such as the [Tukey median](/tukey-median/) are simpler and well studied. For one coordinate at a time, use the [median](/median/) or a [trimmed mean](/trimmed-mean/).

## Pitfalls

- **The threshold needs the covariance.** The rule $\lambda \le 1 + C\varepsilon\log(1/\varepsilon)$ assumes a clean covariance close to $I$. Rescale the data first, or use a version for an unknown covariance.
- **Finite samples.** The top eigenvalue of the clean sample covariance is about $(1 + \sqrt{d/N})^2$. If $N$ is not large compared with $d$, this exceeds the threshold, and the filter keeps removing clean weight.
- **Power iteration from below.** The Rayleigh quotient of an unconverged vector is below the top eigenvalue, so an early stop can pass line L5 too soon. Iterate until $\lambda$ stops changing, or use a full symmetric eigensolver.
- **$\varepsilon$ must be known.** The threshold depends on $\varepsilon$. A too small $\varepsilon$ stops the filter early.
- **Large $\varepsilon$.** The analysis needs $\varepsilon$ below a small constant, well under the [breakdown point](/breakdown-point/) $1/2$ of the median.

## Implementations

## History

Huber (1964) introduced the contamination model. In one dimension the median is optimal in it. In high dimension the Tukey median and related estimators have an error of order $\varepsilon$, but no efficient algorithm was known to compute them. In 2016, two papers at the same conference gave efficient estimators with nearly dimension-free errors. Diakonikolas, Kamath, Kane, Li, Moitra and Stewart introduced the filter and a convex programming method, with error $O(\varepsilon\sqrt{\log(1/\varepsilon)})$ for Gaussians. Lai, Rao and Vempala gave a spectral method whose error has an extra factor that grows with $\log d$. The journal version of the first paper appeared in 2019. Diakonikolas and Kane (2023) give a textbook account of this area.

## References
