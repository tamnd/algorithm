---
tag: ZHD0F7
kind: algorithm
slug: kriging
name: Kriging
aliases:
- Gaussian process interpolation
- Wiener-Kolmogorov prediction
- ordinary kriging
- simple kriging
- best linear unbiased prediction
area: numerical/interpolation-and-approximation
level: advanced
summary: Predict a spatial field at a new point by the linear combination of data with the least mean squared error under a covariance model, solved by a Cholesky factorization. Gives a variance.
solves: [scattered-data-interpolation]
model: real-ram
complexity:
  vars: {n: "the number of data points", d: "the dimension of the points"}
  time: {setup: Θ(n^3), predict: Θ(n), variance: Θ(n^2)}
  space: {extra: Θ(n^2)}
  flops: {setup: "n^3/3", predict: "2n", variance: "n^2"}
properties: {deterministic: true, recursive: false, interpolating: "yes without a nugget", unbiased: true, exact_on: constants}
history:
  year: 1963
  people: [Danie G. Krige, Georges Matheron, Andrey Kolmogorov, Norbert Wiener, Lev S. Gandin]
  note: Krige's 1951 work on gold ore grades in South Africa was formalized by Matheron (1963), who named the method kriging; the same predictor appears in Kolmogorov (1941) and Wiener (1949) for time series and in Gandin's objective analysis in meteorology (1963).
prereqs: [radial-basis-function-interpolation, cholesky-decomposition, gaussian-process]
see_also: [scattered-data-interpolation, radial-basis-function-interpolation, shepard-interpolation, smoothing-spline, positive-definite-matrix, covariance-matrix, linear-regression, curse-of-dimensionality]
sources:
  - paper: doi:10.2113/gsecongeo.58.8.1246
    title: "Georges Matheron, Principles of geostatistics, Economic Geology 58(8) (1963) 1246-1266"
    locator: the kriging system, the variogram and the kriging variance
  - paper: "D. G. Krige, A statistical approach to some basic mine valuation problems on the Witwatersrand, Journal of the Chemical, Metallurgical and Mining Society of South Africa 52(6) (1951) 119-139"
    locator: regression of block grades on surrounding samples
  - book: isbn:9780471002550
    title: Noel A. C. Cressie, Statistics for Spatial Data, revised edition, Wiley, 1993
    locator: Chapter 3, Spatial prediction and kriging (ordinary and simple kriging, the kriging equations and variance)
  - book: isbn:9780387986296
    title: Michael L. Stein, Interpolation of Spatial Data, Some Theory for Kriging, Springer, 1999
    locator: Chapter 1 (best linear prediction, simple and ordinary kriging) and Chapter 2 (the Matérn class)
  - book: isbn:9780262182539
    title: Carl Edward Rasmussen and Christopher K. I. Williams, Gaussian Processes for Machine Learning, MIT Press, 2006
    locator: Chapter 2, Regression (the posterior mean and variance, Algorithm 2.1 with the Cholesky factorization, and the historical notes on kriging) and Chapter 6 (relationships with splines and regularization)
  - book: isbn:9780521843355
    title: Holger Wendland, Scattered Data Approximation, Cambridge University Press, 2005
    locator: Chapter 11, Error estimates for radial basis function interpolation (the power function and its equality with the kriging standard deviation), and Chapter 12 (stability and the trade-off principle)
---

Kriging predicts the value of a spatially varying quantity at a new location from scattered measurements. It models the quantity as a random field with a known covariance function $C$, and takes the linear combination of the data with the smallest expected squared error, subject to being unbiased. The weights solve a symmetric positive definite linear system built from $C$. The same computation also gives the kriging variance, an estimate of the error at every point that is zero at the data and grows away from them. In Gaussian process language the predictor is the posterior mean and the variance is the posterior variance. In approximation theory it is [radial basis function interpolation](/radial-basis-function-interpolation/) with kernel $C$, and the kriging standard deviation is the power function that bounds its error.

## In plain words

You measured something, say rainfall or ore grade, at a few places and want a value somewhere in between. Kriging guesses it as a weighted average of the measurements. The weights come from a rule that says how similar two places are as a function of their distance. Places close to the target get large weights. Measurements that are close to each other share weight, because they carry overlapping information. The weights are the ones that make the expected error as small as possible, and the same calculation tells you how large that error is likely to be at each place. The guess passes exactly through the measurements, and far from all data it falls back to the overall average.

## The problem

The input is points $x_1, \ldots, x_n \in \mathbb{R}^d$ (distinct, in any order), values $y_i$, a covariance function $C(r)$ of the distance $r$, and prediction points $x$. The model is $Z(x) = m + \varepsilon(x)$, where $\varepsilon$ is a zero-mean random field with $\operatorname{Cov}(\varepsilon(x), \varepsilon(x')) = C(\|x - x'\|)$, and $y_i = Z(x_i)$. The output is the predictor $\hat Z(x) = \sum_i\lambda_i(x)y_i$ and its variance $\sigma^2(x) = \mathbb{E}(Z(x) - \hat Z(x))^2$.

- *Simple kriging*: the mean $m$ is known. Minimize $\mathbb{E}(Z(x) - m - \sum\lambda_i(y_i - m))^2$.
- *Ordinary kriging*: $m$ is unknown and constant. Minimize the mean squared error over weights with $\sum\lambda_i = 1$, which makes $\hat Z$ unbiased for every $m$.

Notation: $K_{ij} = C(\|x_i - x_j\|)$, $k(x)_i = C(\|x - x_i\|)$, $\mathbf{1}$ the vector of ones, $C_0 = C(0)$ the sill. $C$ must be positive definite: $K$ is positive definite for every set of distinct points. The Gaussian $e^{-(r/\ell)^2}$, the exponential $e^{-r/\ell}$ and the Matérn kernel with $\nu = \frac32$, $(1 + \sqrt3r/\ell)e^{-\sqrt3r/\ell}$, are positive definite in every dimension. Costs are arithmetic operations on the [real RAM](/real-ram/), plus $n(n + 1)/2$ evaluations of $C$ in setup and $n$ per prediction.

## The algorithm

```pseudo id=main
ORDINARY-KRIGING(x[1..n], y[1..n], C)
L1  K[i][j] ← C(‖x_i − x_j‖) for all i, j                ▷ add a nugget τ² to the diagonal for noisy data
L2  L ← CHOLESKY(K)                                       ▷ K = L Lᵀ, about n³/3 operations
L3  a ← K⁻¹1;  b ← K⁻¹y;  β ← (1ᵀb)/(1ᵀa);  w ← b − β·a   ▷ two pairs of triangular solves
PREDICT(x)
L4  k[i] ← C(‖x − x_i‖) for all i
L5  Ẑ ← β + kᵀw
L6  r ← L⁻¹k;  σ² ← C(0) − rᵀr + (1 − aᵀk)²/(1ᵀa)        ▷ kriging variance, O(n²)
```

Line L3 computes $\beta$, the generalized least squares estimate of the mean, and the residual weights $w = K^{-1}(y - \beta\mathbf{1})$. For simple kriging, replace L3 by $\beta \leftarrow m$, $w \leftarrow K^{-1}(y - m\mathbf{1})$, and drop the last term of L6.

The predictor in L5 is the dual form. The textbook primal form solves the bordered system
$$\begin{pmatrix}K & \mathbf{1}\\ \mathbf{1}^T & 0\end{pmatrix}\begin{pmatrix}\lambda\\ \mu\end{pmatrix} = \begin{pmatrix}k(x)\\ 1\end{pmatrix}, \qquad \hat Z(x) = \lambda^Ty, \qquad \sigma^2(x) = C_0 - \lambda^Tk(x) - \mu,$$
for each $x$ separately, at $O(n^2)$ per point after factoring. Both give the same numbers. The weights $\lambda$ are useful for inspection; the dual form is faster when only predictions are needed.

## Example

Data on a line: $x = 0, 1, 3, 4$ with $y = 1, 2, 0, 0.5$, Gaussian covariance $C(r) = e^{-(r/1.5)^2}$ (sill 1, range 1.5).

- **Mean.** $a = K^{-1}\mathbf{1} = (0.6932, 0.4644, 0.4644, 0.6932)$, so the end points carry more weight in the mean, and $\beta = 0.8503$.
- **Prediction at $x = 2$.** The weights are $\lambda = (-0.2555, 0.7555, 0.7555, -0.2555)$, summing to 1. The outer points get negative weights, because the inner points screen them. $\hat Z(2) = 1.1278$ with kriging standard deviation $\sigma(2) = 0.4371$.
- **Far away.** At $x = 50$, $\hat Z = \beta = 0.8503$ and $\sigma^2 = C_0 + 1/(\mathbf{1}^Ta) = 1.4319$. The variance exceeds the sill because the mean itself is uncertain.
- **Simple kriging** with known mean $0$ gives $\hat Z(2) = 0.9830$ and $\sigma^2(2) = 0.1785$, with weights $(-0.3065, 0.7214, 0.7214, -0.3065)$, which do not sum to 1.

## Correctness

The full proof is in [proofs/correctness.md](proofs/correctness.md). The steps:

1. *Simple kriging.* The mean squared error of $m + \lambda^T(y - m\mathbf{1})$ is $C_0 - 2\lambda^Tk + \lambda^TK\lambda$, a strictly convex quadratic in $\lambda$ because $K$ is positive definite. Its minimizer is $\lambda = K^{-1}k$ and the minimum is $C_0 - k^TK^{-1}k$.
2. *Ordinary kriging.* With the constraint $\mathbf{1}^T\lambda = 1$, the Lagrange conditions are the bordered system above. Its solution is $\lambda = K^{-1}k + \frac{1 - \mathbf{1}^TK^{-1}k}{\mathbf{1}^TK^{-1}\mathbf{1}}K^{-1}\mathbf{1}$, which gives $\lambda^Ty = \beta + k^Tw$ (line L5) and the variance of line L6.
3. *Interpolation.* At $x = x_j$, $k = Ke_j$, so $\lambda = e_j$, $\hat Z(x_j) = y_j$ and $\sigma^2(x_j) = 0$.
4. *Unbiasedness.* $\sum\lambda_i = 1$ gives $\mathbb{E}\hat Z(x) = m = \mathbb{E}Z(x)$ for every $m$, and constant data are reproduced exactly.

**What is proved, and under which hypotheses.**

- *Optimality (proved).* If the covariance model is correct, kriging is the best linear unbiased predictor (BLUP): no other linear unbiased predictor has smaller mean squared error, and $\sigma^2(x)$ is its exact mean squared error. If $Z$ is Gaussian, simple kriging is the conditional mean $\mathbb{E}(Z(x) \mid y)$, the best predictor among all functions of the data, and $\sigma^2$ is the conditional variance.
- *Deterministic error bound (proved, Wendland Chapter 11).* For any function $f$ in the native space $\mathcal{N}_C$ of the kernel, the simple kriging interpolant $s_f$ satisfies $|f(x) - s_f(x)| \le \sigma(x)\,\|f\|_{\mathcal{N}_C}$, where $\sigma(x)$ is the simple kriging standard deviation (the power function). For ordinary kriging the same holds with the native space seminorm. For the Matérn kernels the native space is a Sobolev space, and $\sigma(x) = O(h^{\nu})$ with $h$ the fill distance, for Matérn smoothness $\nu$; for the Gaussian kernel the decay is faster than any power of $h$ (proved, with constants depending on the domain).
- *Misspecified covariance (proved asymptotics, Stein Chapter 4).* With a wrong but compatible covariance, predictions remain asymptotically optimal under infill sampling, but the reported variances can be off by a constant factor. In practice the covariance parameters are estimated from the data, and $\sigma^2$ is then an approximation.
- *Observed.* For $f(x) = \sin 2\pi x$ on $n + 1$ equispaced points in $[0, 1]$, Matérn covariance with $\nu = \frac32$ and $\ell = 0.3$, the maximum errors were $8.70 \times 10^{-2}$, $2.60 \times 10^{-2}$, $7.54 \times 10^{-3}$, $2.05 \times 10^{-3}$ for $n = 5, 10, 20, 40$, observed exponents of 1.7 to 1.9 against the proved $h^{3/2}$ for $\sigma$, and the maximum of $\sigma$ was between 2.8 and 6.4 times the actual maximum error.

## Complexity

- **Setup.** $n(n + 1)/2$ covariance evaluations, $dn^2/2$ operations for distances, the Cholesky factorization in about $n^3/3$ operations, and four triangular solves in about $4n^2$. Storage $n^2/2$ numbers for $L$.
- **Prediction.** $n$ covariance evaluations and $2n$ operations for $\beta + k^Tw$.
- **Variance.** A triangular solve, about $n^2$ operations, per point.
- **Large $n$.** For $n$ beyond a few thousand, the $n^3$ setup dominates. Practical remedies are local neighborhoods (kriging each point from its nearest 20 to 100 data, found with a [k-d tree](/kd-tree/)), compactly supported covariances giving sparse $K$, low-rank and hierarchical matrix approximations, and iterative solvers.

**Rounding and conditioning.** The [Cholesky factorization](/cholesky-decomposition/) is backward stable for a positive definite $K$, so the computed weights are accurate to about $u\,\kappa(K)$ relative error. The danger is $\kappa(K)$ itself. For points with spacing $h$ and a smooth covariance, the smallest eigenvalue of $K$ decays fast as $h$ shrinks. With $\ell = 0.3$ on $n + 1$ equispaced points in $[0, 1]$:

| $n$ | 5 | 8 | 10 | 12 | 15 |
|---|---|---|---|---|---|
| $\kappa(K)$, Gaussian | 4.3e1 | 1.5e4 | 1.8e6 | 3.3e8 | 1.6e12 |
| $\kappa(K)$, Matérn $\nu = \frac32$ | 2.3e1 | 1.4e2 | 3.4e2 | 7.0e2 | 1.7e3 |

For the Gaussian the best proved lower bounds on the smallest eigenvalue decay like $e^{-c/q^2}$ in the separation distance $q$ (Wendland Chapter 12), and the observed growth is of that kind: at $n = 20$ the Cholesky factorization fails in double precision. For the Matérn kernel the growth is polynomial in $1/q$. Smaller errors bring larger condition numbers, a trade-off known as the uncertainty principle of kernel interpolation (Schaback). The usual fixes are a small nugget $\tau^2$ on the diagonal (turning interpolation into smoothing), a rougher covariance such as Matérn, or a different basis for the same space.

## Properties

- **Interpolating** without a nugget, with zero variance at the data; **smoothing** with a nugget.
- **Unbiased** (ordinary kriging): weights sum to 1, constants are reproduced exactly.
- **Linear in the data** for a fixed covariance, but not in the covariance parameters.
- **Order independent** and works in any dimension, on any scattered point set.
- **Screening.** Data hidden behind closer data get small or negative weights, unlike in [Shepard interpolation](/shepard-interpolation/), whose weights are all positive.
- **Mean reversion.** Far from all data the prediction returns to $\beta$ (or $m$) and the variance to $C_0$ plus the mean uncertainty.
- **Variance does not depend on $y$.** $\sigma^2(x)$ depends only on the point positions and $C$, which allows designing sampling networks before measuring.

## Variants and improvements

- **Simple, ordinary and universal kriging.** Known mean, unknown constant mean, and an unknown mean that is a linear combination of given functions (a polynomial trend), with one Lagrange multiplier per trend function. Universal kriging with a linear trend and the generalized covariance $r^2\log r$ in the plane gives the thin plate spline.
- **Variogram form.** Geostatistics often specifies the variogram $\gamma(r) = C_0 - C(r)$, which also covers intrinsic random fields without a finite variance (for example $\gamma(r) = r$, Brownian motion). Ordinary kriging is then written with $\gamma$ in place of $C$.
- **Nugget and kriging with measurement error.** Add $\tau^2I$ to $K$; the predictor is then a [smoothing spline](/smoothing-spline/)-like smoother, and in Gaussian process regression it is the noisy observation model.
- **Cokriging** for several correlated variables, **block kriging** for averages over areas, **indicator kriging** for probabilities of exceedance.
- **Gaussian process regression** with covariance parameters fitted by maximum likelihood, which is the same predictor with a statistical fitting step (Rasmussen and Williams).
- **Local kriging** in moving neighborhoods, and **sparse** or **hierarchical** approximations for large $n$.

## When to use it

Use kriging for scattered data in a few dimensions when you need both a prediction and an error estimate: mining and petroleum reserves, soil and pollution mapping, meteorology, and surrogate models of expensive computer simulations (design and analysis of computer experiments, Bayesian optimization). It is the natural choice when there is a credible model of how correlation decays with distance. For a smooth interpolant without statistics, [radial basis function interpolation](/radial-basis-function-interpolation/) is the same computation. For millions of points, use local or sparse variants, or simpler methods such as [nearest neighbor](/nearest-neighbor-interpolation/) or Shepard interpolation.

## Pitfalls

- **Ill-conditioned $K$.** Gaussian covariances with dense data make Cholesky fail or produce wild weights. Use a nugget, a Matérn covariance or fewer, better spread points; never invert $K$ explicitly.
- **Repeated or nearly repeated points.** Two equal points make $K$ singular; with different values at the same place, only a nugget makes sense.
- **Covariance that is not positive definite.** Ad hoc functions, or valid ones applied to a non-Euclidean distance (such as road distance), can make $K$ indefinite; Cholesky then fails.
- **Trusting $\sigma^2$ blindly.** The variance is only as good as the covariance model, and it ignores the uncertainty of parameters estimated from the same data.
- **Anisotropy and trends.** A single isotropic $C$ on data with a strong trend or directional dependence gives poor predictions; detrend, use universal kriging or scale the coordinates.
- **Units of distance.** The range $\ell$ must be in the same units as the coordinates; mixing kilometers and degrees silently changes the model.
- **Extrapolation.** Outside the data hull the prediction relaxes to the mean, which may be far from the truth.

## Implementations

## History

Kolmogorov (1941) and Wiener (1949) developed optimal linear prediction for stationary processes, the time series form of kriging. Danie Krige, a mining engineer, used regression on nearby samples to estimate gold grades on the Witwatersrand in 1951. Georges Matheron at the École des Mines formalized the method, introduced the variogram and named it kriging in Krige's honor (1960 to 1963). Gandin (1963) independently developed the same optimal interpolation for meteorological analysis. Sacks, Welch, Mitchell and Wynn (1989) applied kriging to computer experiments, and Gaussian process regression brought it into machine learning in the 1990s. The equivalence with spline and radial basis function interpolation was observed by Matheron (1981) and by Kimeldorf and Wahba (1970) in the spline setting.

## References
