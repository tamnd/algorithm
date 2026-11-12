---
tag: 253A61
kind: problem
slug: intrinsic-dimension-estimation
name: Intrinsic dimension estimation
aliases:
- intrinsic dimensionality estimation
area: machine-learning/dimensionality-reduction
level: advanced
summary: "Estimate the intrinsic dimension of a point cloud from local geometry or nearest-neighbour statistics."
prereqs: [intrinsic-dimension, maximum-likelihood-estimation, k-nearest-neighbor-search]
see_also: [manifold-hypothesis, principal-component-analysis, isomap, locally-linear-embedding, k-nearest-neighbor-graph, curse-of-dimensionality, intrinsic-dimensionality, hubness]
sources:
  - paper: "Elizaveta Levina and Peter J. Bickel, Maximum likelihood estimation of intrinsic dimension, Advances in Neural Information Processing Systems 17 (NIPS 2004), MIT Press, 2005, pages 777 to 784"
    locator: equation (8) (the local estimator from the k nearest neighbors, with 1/(k-1)), the remark that k-2 in place of k-1 gives an unbiased form, and equation (9) (the average over points and over k from k1 to k2)
  - paper: doi:10.1038/s41598-017-11873-y
    title: Elena Facco, Maria d'Errico, Alex Rodriguez and Alessandro Laio, Estimating the intrinsic dimension of datasets by a minimal neighborhood information, Scientific Reports 7, 2017, article 12140
    locator: equations (5) to (7) (the Pareto law f(mu) = d mu^(-d-1) of the ratio of the two nearest neighbor distances, and the line -ln(1 - F) = d ln mu), and the rule that discards the 10% of points with the largest mu
  - paper: doi:10.1103/PhysRevLett.50.346
    title: Peter Grassberger and Itamar Procaccia, Characterization of strange attractors, Physical Review Letters 50(5), 1983, pages 346 to 349
    locator: the correlation integral and the slope of ln C(r) against ln r
  - paper: "Jean-Pierre Eckmann and David Ruelle, Fundamental limitations for estimating dimensions and Lyapunov exponents in dynamical systems, Physica D 56(2-3), 1992, pages 185 to 187"
    locator: the bound 2 log10 N on correlation dimension estimates from N points
  - book: isbn:9780387393506
    title: John A. Lee and Michel Verleysen, Nonlinear Dimensionality Reduction, Springer, 2007
    locator: Chapter 3 (estimation of the intrinsic dimension; the correlation dimension, local PCA and their behavior on finite samples)
---

Intrinsic dimension estimation is the problem of finding the [intrinsic dimension](/intrinsic-dimension/) $m$ of the set or distribution that a finite sample comes from, given only the points in their ambient space $\mathbb{R}^D$. All practical estimators use the same fact: if the points near $x$ are spread about uniformly over an $m$-dimensional piece of space, the number of points within distance $r$ of $x$ grows like $r^m$. The fractal estimators, such as the correlation dimension of Grassberger and Procaccia (1983), fit this growth over a range of radii. The nearest neighbor estimators, such as the maximum likelihood estimator of Levina and Bickel (2005) and TwoNN of Facco and others (2017), read it from the ratios of neighbor distances. The answer is always tied to a scale, and all estimators tend to underestimate when $m$ is large compared with $\log n$.

## In plain words

You have many points that are given with many coordinates each, and you suspect that they really need only a few. You want to know how many.

Look at one point and count its neighbors in small balls of growing size. On a line the count doubles when the ball doubles; on a flat sheet it grows four times; in a solid it grows eight times. The growth rate tells you the dimension. The estimators turn this idea into a number, either by counting pairs at many distances or by comparing the distances to the first few neighbors of each point.

## Definition

**Input.** Points $x_1, \ldots, x_n \in \mathbb{R}^D$ (or any [metric space](/metric-space/)), assumed to be drawn independently from a distribution $\mu$ whose support has intrinsic dimension $m$, often with added noise.

**Output.** A number $\hat m$, the global estimate, or a number $\hat m(x_i)$ for each point, the local estimate. The output may be real; round it when an integer is needed.

**Model.** The common local model: for each $x$ there is a radius $R$ such that the density of $\mu$ is about constant on $B(x, R)$ and $\mu(B(x, r)) \approx c(x)\, r^m$ for $r \le R$. The problem is not well posed without such a model: a finite sample is also a set of dimension 0, and noise of size $\sigma$ adds $D - m$ dimensions below the scale $\sigma$.

## Variants

- **Global or local.** One number for the whole data set, or one for each point (useful when the data are a union of pieces of different dimension).
- **Integer or real.** Manifold and topological dimension are integers; box-counting, correlation and local dimensions can be fractions.
- **Linear or nonlinear.** Counting principal components above a variance threshold estimates the linear dimension, which overestimates a curved manifold. Local PCA (Fukunaga and Olsen 1971) applies the count in small neighborhoods.
- **Scale-dependent.** Report $\hat m$ as a function of the neighborhood size $k$ or radius $r$; a plateau over a range of scales is the evidence for a dimension.

## Examples

**A small example on a line.** Take the five points $0, 1, 3, 7, 8$ on the real line. The distances from each point to its first three neighbors are

| point | $T_1$ | $T_2$ | $T_3$ | $\mu = T_2/T_1$ | Levina-Bickel with $k = 3$ |
|---|---|---|---|---|---|
| 0 | 1 | 3 | 7 | 3 | 0.716 |
| 1 | 1 | 2 | 6 | 2 | 0.692 |
| 3 | 2 | 3 | 4 | 1.5 | 2.039 |
| 7 | 1 | 4 | 6 | 4 | 0.910 |
| 8 | 1 | 5 | 7 | 5 | 0.876 |

For the point 3, the local estimate is $(k - 1) / \sum_{j < k} \ln(T_k / T_j) = 2 / (\ln(4/2) + \ln(4/3)) = 2 / \ln(8/3) \approx 2.039$. The average over the five points is $1.047$. The TwoNN line fit through the origin on the four smallest $\mu$ (the largest has $F_{\mathrm{emp}} = 1$ and is dropped) gives $0.976$, and its maximum likelihood form $(n - 1)/\sum \ln \mu_i = 4 / \ln 180$ gives $0.770$. The ten pair distances are $1, 1, 2, 3, 4, 5, 6, 7, 7, 8$, so the correlation integral is $C(1.5) = 0.2$, $C(2.5) = 0.3$ and $C(4.5) = 0.5$. Five points are far too few for a reliable estimate; the example shows the arithmetic.

**Cubes in a higher dimension.** Take $n = 500$ points uniform in the unit cube $[0, 1]^m$, placed in $\mathbb{R}^{12}$ by a random isometry (Python `random.Random(m)`). With the Levina-Bickel estimator averaged over $k = 10, \ldots, 20$, TwoNN with 10% discarded, the TwoNN maximum likelihood form, and the correlation dimension fitted over six radii:

| $m$ | Levina-Bickel | TwoNN | TwoNN MLE | correlation dimension |
|---|---|---|---|---|
| 1 | 1.10 | 1.05 | 1.00 | 0.96 |
| 2 | 2.05 | 1.81 | 1.79 | 1.91 |
| 3 | 3.08 | 2.70 | 2.80 | 2.82 |
| 5 | 4.70 | 4.45 | 4.31 | 4.41 |
| 8 | 6.99 | 6.77 | 6.90 | 7.20 |

The ambient dimension 12 never appears. The estimates are good for small $m$ and fall below $m$ as $m$ grows: with 500 points in 8 dimensions, most neighbors are near the boundary of the cube, where a ball holds fewer points than the $r^m$ law predicts.

## Known algorithms

All three below need the $k$ nearest neighbors or the pair distances; with brute force that is $O(n^2 D)$ time, and with [nearest neighbor search](/k-nearest-neighbor-search/) structures it can be less.

**Correlation dimension (Grassberger and Procaccia 1983).** Compute $C_n(r) = \frac{2}{n(n-1)}\#\{i < j : \|x_i - x_j\| < r\}$ for radii $r_1 < \cdots < r_L$, and fit a line to the points $(\ln r_l, \ln C_n(r_l))$ by least squares; the slope is $\hat m$. The radii must be small enough that $C(r) \approx c\, r^m$ holds and large enough that each $C_n(r_l)$ counts many pairs. One sort of the $n(n-1)/2$ distances gives every $C_n(r)$.

**Maximum likelihood (Levina and Bickel 2005).** Let $T_1(x) \le T_2(x) \le \cdots$ be the distances from $x$ to its nearest neighbors. Under the local model the points near $x$ form a Poisson process in the radius with rate proportional to $r^{m - 1}$, and the maximum likelihood estimate from the first $k$ neighbors is

$$\hat m_k(x) = \Big(\frac{1}{k - 1}\sum_{j=1}^{k-1} \ln \frac{T_k(x)}{T_j(x)}\Big)^{-1}.$$

The global estimate averages $\hat m_k(x_i)$ over the points, and then averages over $k = k_1, \ldots, k_2$. Why it works: under the model, the numbers $(T_j / T_k)^m$ for $j < k$ are like $k - 1$ independent uniform numbers on $(0, 1)$, so $m \sum_{j<k} \ln(T_k / T_j)$ is a sum of $k - 1$ independent standard exponential variables. Hence $S = \sum_{j<k}\ln(T_k/T_j)$ is Gamma with shape $k - 1$ and rate $m$, $\mathbb{E}[1/S] = m/(k - 2)$, and $(k - 2)/S$ is unbiased for $m$, while $(k - 1)/S$ has mean $m(k - 1)/(k - 2)$. Levina and Bickel note this correction.

**TwoNN (Facco, d'Errico, Rodriguez and Laio 2017).** For each point let $\mu_i = T_2(x_i) / T_1(x_i)$. If the density is about constant up to the second neighbor, $\mu$ has the Pareto law with density $m \mu^{-m-1}$ on $[1, \infty)$, so $F(\mu) = 1 - \mu^{-m}$ and

$$-\ln\big(1 - F(\mu)\big) = m \ln \mu .$$

Sort the $\mu_i$, set $F_{\mathrm{emp}}$ of the $i$-th smallest to $i/n$, drop the 10% of points with the largest $\mu$ (they are the most affected by noise and by the point with $F_{\mathrm{emp}} = 1$), and fit a line through the origin to the points $(\ln \mu_i, -\ln(1 - F_{\mathrm{emp}}))$; the slope is $\hat m$. The maximum likelihood estimate under the same law is $n / \sum_i \ln \mu_i$, or $(n - 1)/\sum_i \ln \mu_i$ for an unbiased form. TwoNN uses only the two nearest neighbors, so the constant-density assumption is needed only on the smallest scale.

**Other estimators.** Local PCA counts the large eigenvalues of the [covariance matrix](/covariance-matrix/) of each neighborhood. Graph methods fit the growth of the length of a minimum spanning tree or of a [k-nearest neighbor graph](/k-nearest-neighbor-graph/) with $n$ (Costa and Hero 2004). Box counting fits $\ln N(r)$ against $\ln(1/r)$; it needs far more points than the correlation dimension in the same dimension.

## Bounds

- **Variance under the model.** If $\sum_i \ln \mu_i$ is exactly Gamma with shape $n$ and rate $m$ (as for independent $\mu_i$), the unbiased TwoNN estimate $(n - 1)/\sum_i \ln \mu_i$ has variance $m^2 / (n - 2)$, so its standard error is about $m / \sqrt{n}$. The local Levina-Bickel estimate with $k$ neighbors has variance $m^2/(k - 3)$ in its unbiased form, by the same Gamma calculation with shape $k - 1$; averaging over points reduces it, but the neighborhoods overlap and the terms are dependent.
- **Sample size grows exponentially in $m$.** To see the $r^m$ law over a range of radii with a ratio $\rho$ between the largest and the smallest, the smallest ball must still hold a few points while the largest holds $\rho^m$ times as many, so $n$ must be at least of order $\rho^m$. For the correlation dimension, Eckmann and Ruelle (1992) showed that estimates from $n$ points cannot exceed about $2 \log_{10} n$; for $n = 1000$ that is 6.
- **Underestimation.** For fixed $n$ and growing $m$ every estimator above is biased down, because of boundary effects and because the neighbors of a point lie in a thin shell, as in the table. This is one face of the [curse of dimensionality](/curse-of-dimensionality/).
- **Noise and curvature.** Noise of size $\sigma$ pushes estimates up at scales near $\sigma$; curvature with radius $\tau$ pushes them up at scales near $\tau$. A plateau of $\hat m$ over scales between $\sigma$ and $\tau$ is the practical evidence for a dimension.

## Reductions

- **To nearest neighbor search.** The Levina-Bickel and TwoNN estimators need only the $k$ nearest neighbor distances of each point, so their cost is the cost of the [k-nearest neighbor search](/k-nearest-neighbor-search/), plus $O(nk)$.
- **To pair counting.** The correlation dimension needs $C_n(r)$ at a few radii, which is range counting; tree structures and sampling of pairs make it faster than $O(n^2)$.
- **From dimension reduction.** An estimate of $m$ chooses the target dimension of [PCA](/principal-component-analysis/), [Isomap](/isomap/), [locally linear embedding](/locally-linear-embedding/) and other methods; and the distortion of a [Johnson-Lindenstrauss](/johnson-lindenstrauss-lemma/) projection does not depend on $m$, which is one reason to estimate $m$ before choosing a method.

## Applications

- **Choosing the target dimension** for manifold learning, autoencoders and PCA.
- **Chaotic dynamics.** The correlation dimension of an attractor reconstructed from a time series was the first application; a fractional value is a sign of a strange attractor.
- **Complexity of data and of learned representations.** The intrinsic dimension of image sets is far below the number of pixels, and TwoNN has been used to measure the dimension of the representations in the layers of deep networks.
- **Search cost.** The intrinsic dimension predicts the cost of nearest neighbor search and the strength of [hubness](/hubness/), better than the ambient dimension does; see [intrinsic dimensionality](/intrinsic-dimensionality/).
- **Molecular simulation.** Local estimates show how many collective coordinates describe the motion of a molecule in a simulation.

## References
