---
tag: 29Z7ZM
kind: algorithm
slug: kernel-density-estimation
name: Kernel density estimation
aliases:
- Parzen-Rosenblatt window method
- KDE
area: statistics-and-inference/nonparametric-and-robust-statistics
level: core
summary: Estimates a density by averaging a kernel, such as a Gaussian bump, centred at each data point. The bandwidth trades bias against variance.
model: real-ram
complexity:
  vars: {n: the number of data points, q: the number of points where the estimate is wanted, m: the number of grid points}
  time: {worst: O(n q), binned: O(n + m log m)}
  space: {extra: O(m)}
properties: {deterministic: true, randomized: false, exact: true, nonnegative: true, integrates_to_one: true}
history:
  year: 1956
  people: [Murray Rosenblatt, Emanuel Parzen, V. A. Epanechnikov, Bernard W. Silverman]
  note: Rosenblatt defined the kernel estimate in 1956 and Parzen studied it in 1962. Silverman made it fast on a grid with linear binning and the FFT in 1982.
prereqs: [probability-density-function, empirical-distribution-function, bias-variance-tradeoff, convolution-via-fft]
see_also: [kde-bandwidth-selection, nadaraya-watson-estimator, local-polynomial-regression, mean-shift, gaussian-mixture-model, k-nearest-neighbors, fast-fourier-transform, cross-validation]
sources:
  - paper: doi:10.1214/aoms/1177728190
    title: Murray Rosenblatt, Remarks on some nonparametric estimates of a density function, The Annals of Mathematical Statistics 27(3), 1956
    locator: pp. 832 to 837 (the kernel estimate, its bias and variance, and the n^(-4/5) rate of the mean squared error)
  - paper: doi:10.1214/aoms/1177704472
    title: Emanuel Parzen, On estimation of a probability density function and mode, The Annals of Mathematical Statistics 33(3), 1962
    locator: pp. 1065 to 1076 (consistency and asymptotic normality for a general class of kernels)
  - paper: doi:10.1137/1114019
    title: V. A. Epanechnikov, Non-parametric estimation of a multivariate probability density, Theory of Probability and Its Applications 14(1), 1969
    locator: pp. 153 to 158 (the kernel that minimizes the asymptotic mean integrated squared error)
  - paper: doi:10.2307/2347084
    title: B. W. Silverman, Algorithm AS 176. Kernel density estimation using the fast Fourier transform, Applied Statistics 31(1), 1982
    locator: pp. 93 to 99 (the binned estimate computed by the FFT)
  - book: isbn:9780412246203
    title: B. W. Silverman, Density Estimation for Statistics and Data Analysis, Chapman and Hall, 1986
    locator: Chapter 3 (the kernel method, its bias and variance, and the choice of the smoothing parameter)
  - book: isbn:9780412552700
    title: M. P. Wand and M. C. Jones, Kernel Smoothing, Chapman and Hall, 1995
    locator: Chapter 2 (MISE, AMISE and the optimal bandwidth, Section 2.5; the exact MISE for normal mixtures) and Appendix D (binned computation)
---

Kernel density estimation (KDE) estimates the probability density of a sample without a model for its shape. Put a small bump, the kernel, on each data point, and average the bumps. The width of the bumps is the bandwidth $h$. It is the one choice that matters: a small $h$ follows the noise of the sample, and a large $h$ smooths away real features. The estimate at a point costs $O(n)$. On a grid of $m$ points, linear binning and the [FFT](/fast-fourier-transform/) give the whole curve in $O(n + m \log m)$ time.

## In plain words

A histogram counts points in fixed bins, so its shape depends on where the bins start. Kernel density estimation removes the bins. Each point spreads one unit of probability around itself as a smooth hump, for example a bell curve. The estimate at any place is the total height of the humps there, divided by the number of points. Where points are close together, many humps overlap and the estimate is high.

The width of the humps is the main choice. Narrow humps give a spiky curve with a peak at every point. Wide humps give a flat curve that can hide two separate groups. The right width shrinks slowly as the sample grows.

## The problem

The input is a sample $X_1, \ldots, X_n$ from an unknown density $f$ on the real line, a kernel $K$ and a bandwidth $h > 0$. The kernel is a symmetric density, usually the Gaussian $K(u) = e^{-u^2/2}/\sqrt{2\pi}$ or the Epanechnikov kernel $K(u) = \frac34(1 - u^2)$ on $[-1, 1]$. The output is the function
$$\hat f_h(x) = \frac{1}{nh}\sum_{i=1}^n K\!\left(\frac{x - X_i}{h}\right),$$
evaluated at the points where it is wanted, often on an equally spaced grid. The quality is measured by the mean integrated squared error $\mathrm{MISE}(h) = \mathbb{E}\int (\hat f_h - f)^2$. How to choose $h$ from the data is the separate problem of [bandwidth selection](/kde-bandwidth-selection/).

## The algorithm

Line L1 is the definition. For many points on a grid, the binned version replaces the data by grid counts and turns the sum into a discrete convolution, which the FFT computes for all grid points at once.

```pseudo id=main
KDE(x, X_1..X_n, h)
L1  return (1/(n h)) · Σ_i K((x − X_i)/h)

KDE-ON-GRID(X_1..X_n, h, lo, hi, m)             ▷ binned, with the FFT
L2  δ ← (hi − lo)/(m − 1);  c ← linear binning of the X_i onto the grid g_k = lo + kδ
L3  κ_l ← K(lδ/h)/(n h) for −L ≤ l ≤ L, with L δ at least the reach of the kernel
L4  pad c and κ with zeros to a length N ≥ m + 2L, and take their FFTs
L5  s ← the inverse FFT of the product of the two transforms
L6  return s_{k+L} for k = 0, ..., m − 1         ▷ the estimate at g_k
```

Linear binning gives a point at $g_j + t\delta$, with $0 \le t < 1$, the weight $1 - t$ at $g_j$ and $t$ at $g_{j+1}$. The binned estimate at $g_k$ is $\sum_j c_j \kappa_{k-j}$, a [convolution](/convolution-via-fft/) of the counts with the sampled kernel. The zero padding makes the cyclic convolution of the FFT equal to the ordinary one. The Gaussian kernel is cut at $8h$, where it is below $5.1 \times 10^{-15}$.

## Example

Five points $1, 2, 4, 7, 8$, the Epanechnikov kernel and $h = 2$. Each point adds $\frac{1}{10}\cdot\frac34\big(1 - ((x - X_i)/2)^2\big)$ when $|x - X_i| < 2$. At $x = 2$, the point 1 gives $u = 1/2$ and $K = 9/16$; the point 2 gives $u = 0$ and $K = 3/4$; the point 4 is at distance 2, at the edge, and adds 0. So $\hat f(2) = \frac1{10}(\frac{9}{16} + \frac34) = \frac{21}{160}$.

| $x$ | 0 | 1 | 2 | 3 | 4 | 5 | 5.5 | 6 | 7 | 7.5 | 8 | 9 | 10 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| $\hat f(x)$ | 9/160 | 21/160 | 21/160 | 9/80 | 3/40 | 9/160 | 21/320 | 9/160 | 21/160 | 9/64 | 21/160 | 9/160 | 0 |
| decimal | 0.056 | 0.131 | 0.131 | 0.113 | 0.075 | 0.056 | 0.066 | 0.056 | 0.131 | 0.141 | 0.131 | 0.056 | 0 |

The estimate has two humps, over $\{1, 2\}$ and over $\{7, 8\}$, and a dip near 5. The isolated point 4 makes the dip shallow. It is zero outside $(-1, 10)$, and its integral is exactly 1. With $h = 1$ the curve has three humps, at 1.5, 4 and 7.5. With $h = 6$ the two groups merge into one hump with its top near 4.5. The test file checks these values in exact arithmetic.

## Correctness

The estimate is a density: each scaled kernel $K_h(x - X_i) = K((x - X_i)/h)/h$ has integral 1, and the estimate is their mean. If $f''$ is bounded and continuous, a Taylor expansion inside $\mathbb{E}\,\hat f_h(x) = \int K(u) f(x - hu)\,du$ gives the bias and the variance:
$$\mathbb{E}\,\hat f_h(x) - f(x) = \frac{h^2}{2}\mu_2 f''(x) + o(h^2), \qquad \operatorname{Var}\hat f_h(x) = \frac{R(K) f(x)}{nh} + o\!\left(\frac1{nh}\right),$$
where $\mu_2 = \int u^2 K$ and $R(K) = \int K^2$. Integrated over $x$, they give
$$\mathrm{AMISE}(h) = \frac{h^4}{4}\mu_2^2 R(f'') + \frac{R(K)}{nh},$$
which is strictly convex in $h$ and has its minimum at
$$h^* = \left(\frac{R(K)}{\mu_2^2 R(f'')\,n}\right)^{1/5}, \qquad \mathrm{AMISE}(h^*) = \frac54\left(\mu_2^2 R(K)^4 R(f'')\right)^{1/5} n^{-4/5}.$$
Any bandwidth of a different order than $n^{-1/5}$ gives a larger order of error. For the binned estimate, the FFT computes the binned sum exactly, and linear binning changes the estimate by at most $\delta^2 \sup|K''|/(8h^3)$, since it replaces each kernel value by its linear interpolation between grid points. The full proofs are below; the step that integrates the pointwise remainders is quoted from Wand and Jones.

## Complexity

- **Direct.** Line L1 costs $O(n)$ kernel evaluations, so $q$ points cost $O(nq)$ time. With a compact kernel and sorted data, only the points within $h$ of $x$ count, and a search finds them.
- **Binned.** Binning is $O(n)$, and three FFTs of length less than $6m$ are $O(m \log m)$. The extra space is $O(m)$. In the test file, for $n = 2000$ and $m = 1025$, the binned estimate took 0.013 s and the direct one 0.35 s, in pure Python. This is a measurement on one machine.
- **Accuracy of binning.** For $n = 2000$ standard normal points, $h = 0.3$ and a Gaussian kernel, the largest error against the direct estimate was $7.7 \times 10^{-4}$ for $\delta/h = 0.42$, $2.1 \times 10^{-4}$ for $\delta/h = 0.21$ and $9.4 \times 10^{-6}$ for $\delta/h = 0.041$, with a peak density near 0.4. The error falls like $\delta^2$, as the bound says. These numbers are measured.

## Properties

- **A density.** With a non-negative kernel the estimate is non-negative and integrates to 1. It is as smooth as the kernel.
- **Rate.** With the best $h$, the MISE falls like $n^{-4/5}$, slower than the $n^{-1}$ of a correct parametric model, but with no assumption on the shape of $f$ beyond smoothness. Kernels of higher order (with $\mu_2 = 0$) give faster rates for smoother $f$, but they take negative values.
- **The kernel matters little.** The Epanechnikov kernel minimizes the AMISE among non-negative kernels (Epanechnikov 1969). The Gaussian kernel needs only about 5 percent more data for the same AMISE. The bandwidth matters much more.
- **Bias at peaks and valleys.** The bias $\frac{h^2}{2}\mu_2 f''$ is negative at a peak and positive in a valley, so the estimate flattens the density.
- **Linear in the data.** The estimate is a sum over points, so adding a point adds one term, and estimates for two samples combine by a weighted average.

## Variants and improvements

- **Several dimensions.** Use a product kernel or a kernel with a bandwidth matrix $H$: $\hat f(x) = n^{-1}\sum_i |H|^{-1/2} K(H^{-1/2}(x - X_i))$. The rate becomes $n^{-4/(d+4)}$, which is very slow in high dimensions.
- **Adaptive bandwidth.** A bandwidth that grows where the data are sparse, for example in proportion to $\hat f(X_i)^{-1/2}$ from a pilot estimate (Abramson), or to the distance to the $k$-th nearest neighbour, as in [k-nearest neighbours](/k-nearest-neighbors/).
- **Boundaries.** Near the edge of a bounded support, the plain estimate puts mass outside it. Reflection of the data, boundary kernels, or a transform of the data fix this.
- **Fast summation.** For many evaluation points off a grid, tree methods and the fast Gauss transform approximate the sums in about $O(n + q)$ time.
- **Regression.** The same weights give the [Nadaraya-Watson estimator](/nadaraya-watson-estimator/) and [local polynomial regression](/local-polynomial-regression/) for a mean function.
- **Modes and clusters.** [Mean shift](/mean-shift/) climbs the gradient of a kernel density estimate to its modes.

## When to use it

Use it to look at the shape of one or two variables, as a smooth replacement for a histogram: to see skewness, several modes or heavy tails. It also gives a density for a likelihood ratio, a classifier or a simulation. When the data come from a known family with a few parameters, fit that family instead, because it converges faster. In more than about four or five dimensions, kernel estimates need very many points; a [Gaussian mixture](/gaussian-mixture-model/) or another model is usually better.

## Pitfalls

- **The default bandwidth.** Software often uses a normal reference rule, which oversmooths densities with several modes. Look at several bandwidths, or use a plug-in or cross-validation selector.
- **Bounded data.** For data that cannot be negative, such as waiting times, the estimate leaks mass below 0 and is biased near 0.
- **Grid too coarse.** The binning error grows like $(\delta/h)^2$. Keep $\delta$ well below $h$; a few hundred grid points are usually enough in one dimension.
- **Data outside the grid.** Linear binning drops points outside $[\mathrm{lo}, \mathrm{hi}]$. Extend the grid by a few bandwidths beyond the data.
- **Heavy tails.** A fixed bandwidth that suits the centre leaves spikes in the tails; an adaptive bandwidth or a transform helps.
- **Discrete data.** Ties and rounded values create false modes when $h$ is smaller than the rounding.

## Implementations

## History

Fix and Hodges studied nonparametric discrimination in 1951, an early use of local density estimates. Rosenblatt defined the kernel estimate in 1956 and found the $n^{-4/5}$ rate of its mean squared error. Parzen (1962) proved its consistency and asymptotic normality for general kernels, and the estimate is often called the Parzen window in pattern recognition. Epanechnikov (1969) found the optimal kernel. Silverman (1982) published the FFT algorithm with binning, and Jones and Lotwick improved the binning to the linear form. His 1986 book made the method standard. Wand and Jones (1995) gave the usual modern account.

## References
