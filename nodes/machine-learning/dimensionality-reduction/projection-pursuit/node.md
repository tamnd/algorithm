---
tag: WHZFZK
kind: algorithm
slug: projection-pursuit
name: Projection pursuit
aliases:
- exploratory projection pursuit
area: machine-learning/dimensionality-reduction
level: advanced
summary: "Search for the low-dimensional projections of the data that maximize an index of interest. Gaussian projections score lowest, so the index measures non-Gaussianity."
model: real-ram
complexity:
  vars: {n: the number of points, d: the dimension, k: the number of directions, R: the number of restarts, P: the number of search passes per restart}
  time: {worst: "O(n d^2 + d^3 + k R P n d^2)"}
  space: {extra: "Θ(n d)"}
properties: {deterministic: false, online: false, exact: false, recursive: false, supervised: false, linear: true}
history:
  year: 1974
  people: [Jerome H. Friedman, John W. Tukey, Peter J. Huber]
  note: Friedman and Tukey named the method in 1974 and gave the first index and optimizer. Huber's 1985 survey argued that Gaussian projections are the least interesting and linked the method to ICA-like ideas.
prereqs: [principal-component-analysis, whitening]
see_also: [independent-component-analysis, fastica, blind-source-separation, principal-component-analysis, linear-discriminant-analysis, central-limit-theorem, curse-of-dimensionality, shannon-entropy]
sources:
  - paper: doi:10.1109/T-C.1974.224051
    title: Jerome H. Friedman and John W. Tukey, A projection pursuit algorithm for exploratory data analysis, IEEE Transactions on Computers C-23(9), 1974
    locator: pp. 881 to 890 (the index as trimmed spread times local density, and the search)
  - paper: doi:10.1214/aos/1176349519
    title: Peter J. Huber, Projection pursuit, The Annals of Statistics 13(2), 1985
    locator: pp. 435 to 475 (the survey, Gaussian projections as uninteresting, entropy indices, projection pursuit regression and density estimation)
  - paper: doi:10.1080/01621459.1987.10478427
    title: Jerome H. Friedman, Exploratory projection pursuit, Journal of the American Statistical Association 82(397), 1987
    locator: pp. 249 to 266 (the Legendre index, sphering, structure removal)
  - paper: doi:10.2307/2981662
    title: M. C. Jones and Robin Sibson, What is projection pursuit?, Journal of the Royal Statistical Society, Series A 150(1), 1987
    locator: pp. 1 to 37 (the moment index from the cumulant expansion of negentropy)
  - paper: doi:10.1214/aos/1176346703
    title: Persi Diaconis and David Freedman, Asymptotics of graphical projection pursuit, The Annals of Statistics 12(3), 1984
    locator: pp. 793 to 815 (most low-dimensional projections of high-dimensional data are nearly Gaussian)
  - book: isbn:9780387848570
    title: Trevor Hastie, Robert Tibshirani and Jerome Friedman, The Elements of Statistical Learning, second edition, Springer, 2009
    locator: Section 11.2 (projection pursuit regression) and Section 14.7 (independent component analysis and exploratory projection pursuit)
---

Projection pursuit is a family of methods that search for the one- or two-dimensional projections of high-dimensional data that show the most structure, as measured by a projection index. Most projections of a large cloud of points look almost Gaussian, so the standard indices measure departure from the Gaussian: the Friedman-Tukey local density, the moment index $(\kappa_3^2 + \kappa_4^2/4)/12$, and approximations of negentropy. The data are first [sphered](/whitening/), so that the index sees only the shape of each projection and not its scale. With negentropy as the index, the search for one direction is the same as one unit of [independent component analysis](/independent-component-analysis/), and [FastICA](/fastica/) is a fast optimizer for it. Unlike [PCA](/principal-component-analysis/), which keeps the directions of largest variance, projection pursuit keeps the directions with clusters, skewness, heavy tails or other non-Gaussian shape.

## In plain words

You have points in many dimensions and you want a picture that shows something interesting, such as two separate groups. You can only look at the points from one direction at a time, as a shadow on a line or on a wall. Most shadows of a big cloud of points look like a plain bell curve and show nothing.

Projection pursuit gives each shadow a score that is low for a bell curve and high for groups, gaps, a lopsided shape or long tails. It then turns the direction step by step to raise the score, from several starting points, and it shows you the best shadows. Before it starts, it stretches the data so that every shadow has the same spread, so a shadow cannot win only by being wide.

## The problem

The input is $n$ points $x_1, \ldots, x_n \in \mathbb{R}^d$, a projection index $I$, and a number $k$ of directions. A projection index is a function of a sample of real numbers. It should be invariant under affine maps $y \mapsto a y + b$, and it should be smallest for Gaussian samples. The goal is to find unit vectors $w_1, \ldots, w_k$ in the sphered coordinates that maximize $I(w^{\top} z_1, \ldots, w^{\top} z_n)$, each one orthogonal to the earlier ones. Common indices for a standardized projection $u$:

- **Friedman-Tukey.** The trimmed spread times the local density $\sum_{i,j} f(|u_i - u_j|)$ for a decreasing $f$ that is 0 beyond a radius $R$. After sphering the spread is fixed, so the density term is what matters. It costs $\Theta(n^2)$.
- **Moment index (Jones and Sibson).** $I_M = \frac{1}{12}\bigl(\kappa_3^2 + \frac14 \kappa_4^2\bigr)$, with $\kappa_3$ the skewness and $\kappa_4$ the excess kurtosis of $u$. It is the cumulant approximation of negentropy.
- **Negentropy approximation.** $I_N = (E[\log\cosh u] - E[\log\cosh \nu])^2$ with $\nu$ standard Gaussian, where $E[\log\cosh \nu] \approx 0.374567$.
- **Friedman's Legendre index.** Transform $u$ to $[-1, 1]$ by $2\Phi(u) - 1$ and measure the departure of its density from uniform with Legendre polynomials.

## The algorithm

The search uses sphering, random restarts and a pattern search on the unit sphere. Later directions are kept orthogonal to the earlier ones in the sphered space.

```pseudo id=main
PROJECTION-PURSUIT(X, k, I, R)
L1  z_t ← V (x_t − μ) for all t                                       ▷ sphere: mean 0, covariance I
L2  for p = 1 to k do
L3      for each of R restarts: w ← a random unit vector orthogonal to w_1..w_{p−1};  h ← h₀
L4          while h > h_min do
L5              for each axis j and sign ±: w′ ← normalize(w ± h e_j projected onto the complement of w_1..w_{p−1});  score I(w′ᵀ z)
L6              if the best w′ beats I(wᵀ z) then w ← w′ else h ← h / 2
L7          keep w if its index is the best over the restarts;  w_p ← the best w
L8  return the directions w_pᵀ V and their index values
```

The direction returned in line L8 is a functional on the original data: the projection of a point $x$ is $w_p^{\top} V (x - \mu)$. Any local optimizer on the sphere can replace lines L4 to L6. Gradient ascent is common for smooth indices, and the FastICA fixed-point step is much faster for the negentropy index.

## Example

Take 1000 points in the plane with two hidden coordinates: $a = \pm 1 + 0.3\,\varepsilon$ (two clusters, variance 1.09) and $b = 2\nu$ (Gaussian, variance 4), with $\varepsilon$ and $\nu$ standard Gaussian. Rotate the plane by 30°, so the cluster axis points at 30° and the Gaussian axis at 120°.

PCA picks the direction of largest variance, which is the Gaussian axis at about 121°. Its projection is one bell curve and shows no clusters. The table gives the index values of three directions on this sample.

| direction | moment index | logcosh index |
|---|---|---|
| first principal component (121°) | 0.00075 | 0.0000077 |
| Gaussian axis (120°) | 0.00076 | 0.0000080 |
| cluster axis (30°) | 0.0579 | 0.0021 |

Projection pursuit with the moment index and 5 restarts returns the direction at 30.07°, with index 0.05795. A search over 3600 angles in the sphered plane gives the same maximum, 0.05795. The projection on this direction shows the two clusters clearly.

Index values for some standardized distributions (exact population values of the moment index): Gaussian 0, uniform 0.03, the two-point distribution $\pm 1$ about 0.0833, Laplace 0.1875, exponential about 1.083. The two-cluster coordinate above has $\kappa_4 \approx -1.68$ and index about 0.059.

## Correctness

Sphering makes every unit direction give a projection with mean 0 and variance 1, and every linear projection of the data equals one of these up to a positive scale, so the search on the sphere loses nothing. The negentropy of a projection equals the Kullback-Leibler divergence from the Gaussian with the same mean and variance, so it is never negative and is 0 only for a Gaussian: Gaussian projections are the least interesting. For ICA data $z = Q s$ with symmetric sources, the moment index of $w^{\top} z$ is $\frac{1}{48}(\sum_i q_i^4 \kappa_i)^2$ with $q = Q^{\top} w$, and it is largest exactly at a source; this makes ICA a special case. The search never lowers the index and stops after a bounded number of passes. The full proofs are below.

## Complexity

The model is the [real RAM](/real-ram/), and the costs count arithmetic operations.

- **Sphering.** $\Theta(n d^2)$ for the covariance and the transform, and $O(d^3)$ for its eigendecomposition.
- **One index evaluation.** $\Theta(n d)$ to project, plus $\Theta(n)$ for the moment and logcosh indices, $\Theta(n \log n)$ for indices based on sorted values, or $\Theta(n^2)$ for the all-pairs Friedman-Tukey density.
- **Search.** One pass of line L5 makes $2d$ evaluations. With $P$ passes per restart, $R$ restarts and $k$ directions, the moment index costs $O(n d^2 + d^3 + k R P n d^2)$.
- **Memory.** $\Theta(n d)$ for the sphered data.

## Properties

- **Affine invariance.** The result does not depend on the scale or rotation of the input, because the data are sphered and the index is affine invariant. PCA is not invariant in this way.
- **Gaussian means no structure.** By Lemma 2 of the proof, negentropy is 0 only for Gaussian projections. Diaconis and Freedman (1984) showed that for large $d$ most projections are nearly Gaussian, so a high index is a real signal, provided that $n$ is large compared with $d$.
- **Local optima.** The index is not concave on the sphere. Restarts are needed, and different restarts can find different interesting views.
- **Ignores the variance.** A direction with tiny variance and clear clusters can win over a direction with large variance. This is the point of the method, and also a risk with noise.
- **Linear.** The output is a set of linear projections, which are easy to interpret.

## Variants and improvements

- **Two-dimensional pursuit.** Search over pairs of orthonormal directions for a scatter plot. Friedman and Tukey designed the method for interactive 2D views.
- **Structure removal.** Friedman (1987) removes the structure along a found direction by transforming that coordinate to a Gaussian, instead of restricting the search to the orthogonal complement.
- **Projection pursuit regression.** Friedman and Stuetzle (1981) model a response as a sum of smooth functions of projections, $f(x) = \sum_m g_m(w_m^{\top} x)$, fitted one term at a time.
- **Projection pursuit density estimation.** Friedman, Stuetzle and Schroeder (1984) build a density as a product of corrections along interesting directions.
- **ICA.** Estimating all directions at once with an independence contrast gives [ICA](/independent-component-analysis/), and [FastICA](/fastica/) with deflation is projection pursuit with a negentropy index and a fast optimizer.
- **Grand tour.** Asimov's grand tour shows a continuous sequence of random 2D projections; projection pursuit guided tours steer the tour toward high index values.

## When to use it

Use projection pursuit for exploratory analysis when you suspect clusters, outliers or skewed structure that PCA hides because it is not in the high-variance directions. It is useful as a preprocessing step for clustering in a few chosen directions, and as a way to find a few interpretable linear features. Use [LDA](/linear-discriminant-analysis/) instead when labels are available, and nonlinear methods when the structure is not visible in any linear projection.

## Pitfalls

- **Small $n$ and large $d$.** With few points per dimension, some projection always looks non-Gaussian by chance. Compare the best index with the best index on Gaussian data of the same size.
- **No sphering.** Without sphering, the index rewards directions with unusual scale, and the method mostly rediscovers the variance structure.
- **Outliers.** Moment indices are dominated by a few extreme points. One outlier can produce a projection with a high kurtosis and nothing else in it. Robust indices such as the Legendre index avoid this.
- **Zero cumulants.** The moment index is 0 for some non-Gaussian distributions with $\kappa_3 = \kappa_4 = 0$, so it misses them.
- **Cost of density indices.** All-pairs density indices cost $\Theta(n^2)$ per evaluation. Use binning or sorted values for large $n$.

## Implementations

## History

Kruskal suggested searching for projections by a numerical index around 1969. Jerome Friedman and John Tukey gave the name and the first practical algorithm in 1974, with an index that multiplied a robust spread by a local density, for interactive views on the PRIM-9 system. Peter Huber's 1985 survey unified the field: it argued that Gaussian projections are the least interesting, proposed entropy-based indices, and related the method to regression, density estimation and deconvolution. Friedman (1987) and Jones and Sibson (1987) gave new indices. In the 1990s the ICA literature showed that ICA by maximization of non-Gaussianity is projection pursuit with a negentropy index.

## References
