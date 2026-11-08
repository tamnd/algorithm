---
tag: 2FTF47
kind: algorithm
slug: monte-carlo-integration
name: Monte Carlo integration
aliases:
- Monte Carlo quadrature
- plain Monte Carlo
- crude Monte Carlo
- mean-value Monte Carlo
area: numerical/quadrature
level: core
summary: Estimate an integral by the sample mean of f at random points; error is O(N^-1/2) regardless of dimension.
solves: [numerical-integration, multidimensional-integration]
model: real-ram
complexity:
  vars: {N: "the number of sample points, at least 2", s: "the dimension"}
  time: {worst: Θ(N s), average: Θ(N s), best: Θ(N s)}
  space: {extra: Θ(s)}
properties: {deterministic: false, recursive: false}
prereqs: [numerical-integration, variance, law-of-large-numbers]
see_also: [quasi-monte-carlo-integration, importance-sampling, stratified-sampling, latin-hypercube-sampling, central-limit-theorem, curse-of-dimensionality, multidimensional-integration, metropolis-hastings]
sources:
  - url: https://artowen.su.domains/mc/
    title: Art B. Owen, Monte Carlo theory, methods and examples, 2013
    locator: Chapter 2, Simple Monte Carlo (error, confidence intervals and the one-pass variance update); Chapter 8, Variance reduction
  - paper: doi:10.1017/S0962492900002804
    title: Russel E. Caflisch, Monte Carlo and quasi-Monte Carlo methods, Acta Numerica 7, 1998, 1-49
    locator: Sections 1 to 3 (Monte Carlo integration, its error and variance reduction)
  - paper: doi:10.1080/01621459.1949.10483310
    title: Nicholas Metropolis and S. Ulam, The Monte Carlo method, Journal of the American Statistical Association 44(247), 1949, 335-341
    locator: the first published account of the method
  - book: isbn:9780898712957
    title: Harald Niederreiter, Random Number Generation and Quasi-Monte Carlo Methods, SIAM, 1992
    locator: Chapter 1, Monte Carlo methods and quasi-Monte Carlo methods (Section 1.2, Monte Carlo methods)
  - book: isbn:9780122063602
    title: Philip J. Davis and Philip Rabinowitz, Methods of Numerical Integration, second edition, Academic Press, 1984
    locator: Section 5.9, Multiple integration by sampling
---

Monte Carlo integration estimates $I(f) = \int_B f(x)\,dx$ over a region $B$ of volume $V$ by $V$ times the average of $f$ at $N$ independent uniform random points of $B$. The estimate is unbiased, its root mean square error is exactly $V \sigma/\sqrt{N}$ where $\sigma^2$ is the variance of $f$ at a random point, and the same samples give an estimate of that error. The rate $N^{-1/2}$ is slow, but it does not depend on the dimension $s$ or on the smoothness of $f$, which makes Monte Carlo the method of choice for integrals in many dimensions or with rough integrands.

## In plain words

To find the average height of a landscape, you can measure at random spots and average what you see. The integral is the average height times the area, so the same trick estimates it.

Each random measurement is a noisy guess. Averaging $N$ of them shrinks the noise by a factor of $\sqrt{N}$: a hundred times more points give ten times more accuracy. That is slow, but the rule is the same in two dimensions or in a thousand, where grid methods are hopeless because a grid with even a few points per direction has too many points. The spread of the measurements also tells you how large the error probably is. The answer is random, so it comes with a probability, not a guarantee.

## The problem

The input is a function $f$ on a box $B = \prod_{k=1}^{s} [a_k, b_k]$, a sample size $N \ge 2$ and a seeded random number generator. The output is the estimate and its standard error,

$$\hat I_N = \frac{V}{N} \sum_{j=1}^{N} f(X_j), \qquad \widehat{\mathrm{se}} = |V| \sqrt{\frac{S^2}{N}}, \qquad S^2 = \frac{1}{N - 1} \sum_{j=1}^{N} \big(f(X_j) - \bar f\big)^2,$$

with $X_1, \ldots, X_N$ independent and uniform on $B$ and $\bar f$ the sample mean. Write $\sigma^2 = \operatorname{Var}(f(X))$ for $X$ uniform on $B$. Other regions are handled by a map from a box, by sampling from a density $p$ on the region and averaging $f/p$ ([importance sampling](/importance-sampling/)), or by setting $f = 0$ outside the region. The cost is the number of evaluations of $f$.

## The algorithm

```pseudo id=main
MONTE-CARLO(f, a, b, N, rng)                 ▷ box with corners a, b in R^s; N ≥ 2
L1  V ← Π_k (b_k − a_k)
L2  μ ← 0, q ← 0
L3  for j ← 1 to N do
L4      x ← (a_k + (b_k − a_k) · rng.uniform())_k     ▷ a uniform point of the box
L5      y ← f(x)
L6      δ ← y − μ;  μ ← μ + δ / j;  q ← q + δ · (y − μ)   ▷ Welford's update
L7  S² ← q / (N − 1)
L8  return V · μ, |V| · sqrt(S² / N)
```

Line L6 keeps the running mean $\mu$ and the sum $q$ of squared deviations from it in one pass, without storing the samples and without the cancellation of the formula $\sum y^2 - N \bar y^2$.

## Example

Estimate $\pi = \int_{[0,1]^2} 4 \cdot [x_1^2 + x_2^2 \le 1]\,dx$, the area of a quarter disc times 4, with seed 1. Here $V = 1$ and $\sigma^2 = \pi(4 - \pi)$, so $\sigma = 1.6422$. The first five steps:

| $j$ | point $x$ | $y$ | $\mu$ | $q$ |
|---|---|---|---|---|
| 1 | $(0.1344, 0.8474)$ | 4 | 4 | 0 |
| 2 | $(0.7638, 0.2551)$ | 4 | 4 | 0 |
| 3 | $(0.4954, 0.4495)$ | 4 | 4 | 0 |
| 4 | $(0.6516, 0.7887)$ | 0 | 3 | 12 |
| 5 | $(0.0939, 0.0283)$ | 4 | 3.2 | 12.8 |

Longer runs with the same seed:

| $N$ | $\hat I_N$ | $\widehat{\mathrm{se}}$ | $\hat I_N - \pi$ | error in standard errors |
|---|---|---|---|---|
| $10^2$ | $3.2000$ | $0.1608$ | $5.8 \times 10^{-2}$ | 0.36 |
| $10^3$ | $3.1120$ | $0.0526$ | $-3.0 \times 10^{-2}$ | 0.56 |
| $10^4$ | $3.1416$ | $0.0164$ | $7.3 \times 10^{-6}$ | 0.0004 |
| $10^5$ | $3.13784$ | $0.00520$ | $-3.8 \times 10^{-3}$ | 0.72 |
| $10^6$ | $3.14138$ | $0.00164$ | $-2.1 \times 10^{-4}$ | 0.13 |

The standard error falls by $\sqrt{10}$ per row, as $\sigma/\sqrt{N}$ predicts ($1.6422/\sqrt{N}$). The actual error is a random multiple of it: at $N = 10^4$ it is small by luck, and across seeds about 95 percent of runs land within $1.96$ standard errors.

## Correctness

The full proof is in the correctness file. The results are probabilistic, for independent uniform points:

- **Welford's update** keeps $\mu_j$ equal to the mean of the first $j$ values and $q_j$ equal to the sum of their squared deviations, so line L8 returns $\hat I_N$ and $\widehat{\mathrm{se}}$ exactly as defined.
- **Unbiased, with exact variance.** $\mathbb{E}[\hat I_N] = I$ and, if $\sigma^2 < \infty$, $\operatorname{Var}(\hat I_N) = V^2 \sigma^2/N$. The root mean square error is exactly $V\sigma N^{-1/2}$ in every dimension.
- **Convergence.** $\hat I_N \to I$ almost surely for every integrable $f$ (strong [law of large numbers](/law-of-large-numbers/)). If $\sigma^2 < \infty$, $\Pr(|\hat I_N - I| \ge t) \le V^2\sigma^2/(N t^2)$ for all $N$ (the [Chebyshev inequality](/chebyshev-inequality/)), and $\hat I_N$ is asymptotically normal (the [central limit theorem](/central-limit-theorem/)). For bounded $f$ with range in $[c, d]$, the [Hoeffding inequality](/hoeffding-inequality/) gives the nonasymptotic bound $\Pr(|\hat I_N - I| \ge t) \le 2\exp(-2N t^2/(V^2 (d - c)^2))$.
- **Standard error.** $S^2$ is unbiased for $\sigma^2$ and consistent, so $\hat I_N \pm 1.96\,\widehat{\mathrm{se}}$ is an asymptotic 95 percent confidence interval. It is not exact for finite $N$.

## Complexity

- **Evaluations.** Exactly $N$ evaluations of $f$ and $N s$ uniform variates.
- **Memory.** $\Theta(s)$ for the current point and $\Theta(1)$ for the statistics.
- **Work for a tolerance.** For a root mean square error $\tau$, $N = (V\sigma/\tau)^2$ points are needed. A tenfold gain in accuracy costs a hundredfold more work, for every dimension $s$.
- **Comparison with grids.** A product rule of order $p$ with $n$ points per direction uses $N = n^s$ points and has error $O(N^{-p/s})$, which beats $N^{-1/2}$ only when $p > s/2$; see [product quadrature](/product-quadrature/) and the [curse of dimensionality](/curse-of-dimensionality/).
- **Floating point.** The statistical error $\sigma N^{-1/2}$ dwarfs rounding for all practical $N$. Welford's update has a rounding error of about $N u$ times the data scale in the worst case, and much smaller in practice.

## Properties

- **Dimension-free rate.** The error $V\sigma N^{-1/2}$ involves no derivative of $f$ and no power of $s$. The dimension enters only through $\sigma$.
- **Minimal assumptions.** Square integrability gives the rate; integrability alone gives convergence. Jumps and kinks do not slow it.
- **Built-in error estimate.** The same samples give $\widehat{\mathrm{se}}$, unlike deterministic rules, whose error estimates come from comparing rules.
- **Embarrassingly parallel.** Independent streams can run on many processors and their means and variances can be merged; the streams must be independent, for example by [jump-ahead](/jump-ahead/) in the generator.
- **Optimal for rough functions.** On classes of functions with no smoothness, such as bounded measurable functions, no randomized method can beat $N^{-1/2}$ in the worst case, and no deterministic method converges at all.

## Variants and improvements

- **Variance reduction.** Reduce $\sigma$ instead of increasing $N$: [importance sampling](/importance-sampling/) samples from a density close to $|f|$, [stratified sampling](/stratified-sampling/) and [Latin hypercube sampling](/latin-hypercube-sampling/) spread the points, control variates subtract a function with known integral, and antithetic variables pair $x$ with $a + b - x$. For smooth $f$, stratification with one point in each of $N$ cells of $[0,1]^s$ improves the rate to $N^{-1/2 - 1/s}$.
- **Quasi-Monte Carlo.** Replace random points by low-discrepancy points, error $O(N^{-1}(\log N)^s)$ for functions of bounded variation; see [quasi-Monte Carlo integration](/quasi-monte-carlo-integration/). Randomly shifted QMC keeps an unbiased estimate and an error estimate from replications.
- **Markov chain Monte Carlo.** When the density cannot be sampled directly, Markov chain Monte Carlo, such as [Metropolis-Hastings](/metropolis-hastings/), produces dependent samples whose averages still converge; the variance formula then includes the autocorrelation.
- **Hit-or-miss.** Count the fraction of uniform points under the graph of $f$ in a bounding box. It has a larger variance than the mean-value estimate here and is mainly of historical interest; the quarter-disc example is both.
- **Multilevel Monte Carlo.** For expectations of solutions of stochastic differential equations, combine samples at several discretization levels to cut the total cost.

## When to use it

Use Monte Carlo in high dimension, say $s \ge 10$, when $f$ is rough, discontinuous or expensive to analyse, when the domain is complicated, or when you need an honest error estimate from the samples. In one to three dimensions with a smooth integrand, deterministic rules such as [Gaussian quadrature](/gaussian-quadrature/) or [adaptive quadrature](/adaptive-quadrature/) are far faster. In moderate dimension with a smooth or nearly additive integrand, try [quasi-Monte Carlo](/quasi-monte-carlo-integration/) or [sparse grids](/sparse-grid-quadrature/) first.

## Pitfalls

- **Infinite variance.** For $f(x) = (1 - x)^{-1/2}$ on $[0, 1]$ the integral is 2 but $\sigma^2 = \infty$. The estimate converges, more slowly than $N^{-1/2}$, and the standard error is meaningless: it fluctuates and usually underestimates the error. Remove the singularity by a change of variable or importance sampling.
- **One-pass variance by $\sum y^2 - N\bar y^2$.** This subtracts two large nearly equal numbers and can even go negative when $\sigma$ is small compared with the mean. Use Welford's update, as line L6 does, or two passes.
- **A bad generator.** Lattice structure in a poor generator such as [RANDU](/randu/) gives badly wrong answers in three or more dimensions. Use a well-tested generator, and fix the [seed](/seed/) for reproducibility.
- **Reusing one stream in parallel.** Workers started with the same seed return the same samples and the variance estimate is then wrong. Give each worker its own stream.
- **Reading the confidence interval as a guarantee.** The interval holds with about 95 percent probability for large $N$. For heavy-tailed $f$ and small $N$, coverage can be much lower.

## Implementations

## History

Buffon's needle problem (1777) estimates $\pi$ by a random experiment, and Laplace pointed out the connection. The modern method was developed at Los Alamos in 1946 and 1947 by Stanislaw Ulam and John von Neumann, with Nicholas Metropolis, for neutron transport, on the ENIAC; the name refers to the casino. Metropolis and Ulam published the first account in 1949. Hammersley and Handscomb's book (1964) made the variance reduction techniques standard.

## References
