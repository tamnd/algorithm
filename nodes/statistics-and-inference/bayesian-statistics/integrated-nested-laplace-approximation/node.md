---
tag: VKP2D8
kind: algorithm
slug: integrated-nested-laplace-approximation
name: Integrated nested Laplace approximation
aliases:
- INLA
area: statistics-and-inference/bayesian-statistics
level: research
summary: Rue, Martino and Chopin's deterministic approximation of posterior marginals of latent Gaussian models by nested Laplace approximations and numerical integration.
model: real-ram
complexity:
  vars: {K: the number of grid values of the hyperparameters, G: the number of points of each marginal, I: the number of Newton steps, C: the cost of one sparse Cholesky factorization of Q + D, F: the number of non-zeros of the Cholesky factor}
  time: {worst: Θ(K G I C)}
  space: {extra: Θ(K G + F)}
properties: {deterministic: true, exact: false, online: false, recursive: false}
history:
  year: 2009
  people: [Håvard Rue, Sara Martino, Nicolas Chopin]
  note: Rue, Martino and Chopin read the paper to the Royal Statistical Society in 2008 and published it in 2009. It joined the Laplace approximations of Tierney and Kadane (1986) with fast sparse computations for Gaussian Markov random fields, and the R-INLA software made it a standard tool for spatial and hierarchical models.
prereqs: [laplace-approximation, hierarchical-bayesian-model, newton-raphson-method, cholesky-decomposition, markov-random-field]
see_also: [sparse-linear-systems, nested-dissection, generalized-linear-model, gaussian-process, marginal-likelihood, expectation-propagation, variational-inference, empirical-bayes]
sources:
  - paper: doi:10.1111/j.1467-9868.2008.00700.x
    title: "Håvard Rue, Sara Martino and Nicolas Chopin, Approximate Bayesian inference for latent Gaussian models by using integrated nested Laplace approximations, Journal of the Royal Statistical Society Series B 71(2), 2009"
    locator: "pages 319 to 392, with the discussion: latent Gaussian models, the approximation of the hyperparameter posterior by the ratio in L4, its exploration from the mode, the Gaussian, Laplace and simplified Laplace approximations of the latent marginals, and the discussion of the approximation error (general locator)"
  - paper: doi:10.1093/biostatistics/kxp053
    title: "Youyi Fong, Håvard Rue and Jon Wakefield, Bayesian inference for generalized linear mixed models, Biostatistics 11(3), 2010"
    locator: "pages 397 to 412: INLA for generalized linear mixed models, and its loss of accuracy for binary data with few observations per random effect (general locator)"
  - paper: doi:10.1080/01621459.1986.10478240
    title: "Luke Tierney and Joseph B. Kadane, Accurate approximations for posterior moments and marginal densities, Journal of the American Statistical Association 81(393), 1986"
    locator: "pages 82 to 86: the approximation of a marginal posterior density by a ratio of Laplace approximations, which L4 and L6 apply"
---

The integrated nested Laplace approximation (INLA) computes posterior marginals of a latent Gaussian model without sampling. In such a model, hyperparameters $\theta$ (few, say up to about ten) have a prior $\pi(\theta)$; a latent field $x \in \mathbb{R}^n$ is Gaussian given $\theta$, $x \sim N(0, Q(\theta)^{-1})$, with a sparse precision matrix $Q$; and each observation $y_j$ depends on one coordinate $x_j$ through a likelihood $p(y_j \mid x_j)$. INLA nests two [Laplace approximations](/laplace-approximation/). The outer one gives the hyperparameter posterior from the identity

$$\pi(\theta \mid y) \propto \frac{\pi(x, \theta, y)}{\pi(x \mid \theta, y)}\bigg|_{x = x^*(\theta)},$$

with the denominator replaced by a Gaussian at the mode $x^*(\theta)$. The inner one gives the marginal of each $x_i$ for fixed $\theta$. A weighted sum over a grid of $\theta$ values then integrates $\theta$ out. Every step is a sparse [Cholesky factorization](/cholesky-decomposition/), so models with $10^5$ latent values run in seconds or minutes.

## In plain words

Many statistical models have two layers: a large set of hidden values, such as a disease risk for each district, that vary smoothly and follow a bell-curve law, and a few settings that control how smooth they are. Sampling methods explore such models by a long random walk. INLA instead computes the answer directly. For each candidate setting it finds the most likely hidden values and replaces the true shape around them by a bell curve. How well the bell curve fits tells how plausible that setting is. It then repeats the trick one hidden value at a time to get each answer's full shape, and averages over the settings. Because each hidden value interacts with only a few neighbours, every step uses fast methods for sparse systems. The result is close to exact when the data are informative.

## The problem

**Input.** A latent Gaussian model: a prior $\pi(\theta)$ on a hyperparameter of low dimension, a sparse positive definite precision $Q(\theta)$, observations $y_1, \ldots, y_n$ with log-likelihood terms $g_j(x_j) = \log p(y_j \mid x_j)$ that are concave in $x_j$, a grid $\theta_1, \ldots, \theta_K$ with spacing $\Delta$, an index $i$, and points $z_1, \ldots, z_G$ at which to evaluate the marginal of $x_i$.

**Output.** Weights $w_k \approx \pi(\theta_k \mid y)\Delta$, and the values $\tilde\pi(x_i = z_g \mid y)$ of the posterior marginal density of $x_i$.

Write $F_\theta(x) = -\frac12 x^\top Q(\theta)x + \sum_j g_j(x_j)$, the log of the joint density up to terms in $\theta$ only.

## The algorithm

```pseudo id=main
INLA(y, Q(·), π(θ), θ₁..θ_K, i, z₁..z_G)
L1  for k ← 1 to K
L2      x* ← argmax_x F_θk(x);  P ← Q(θ_k) + diag(c(x*))    ▷ Newton: solve (Q + diag c) x_new = b
L3      factor Q(θ_k) and P by sparse Cholesky
L4      ℓ_k ← log π(θ_k) + ½ log det Q(θ_k) + F_θk(x*) - ½ log det P
L5      for g ← 1 to G
L6          x' ← argmax F_θk with x_i fixed at z_g;  f_k(z_g) ← exp(F_θk(x') - ½ log det P₋ᵢ(x'))
L7      normalize f_k so that it integrates to 1 over z
L8  w_k ← exp(ℓ_k) / Σ_m exp(ℓ_m) for each k
L9  π̃(z_g | y) ← Σ_k w_k f_k(z_g) for each g
L10 return w, π̃(z | y)
```

Here $c_j(v) = -g_j''(v) \ge 0$ is the curvature of the $j$-th log-likelihood term, and $b = \operatorname{diag}(c(x))\,x + g'(x)$. L2 is Newton's method for the mode: its step is a linear system with the matrix $Q + \operatorname{diag}(c)$, which has the sparsity of $Q$. At the mode, $N(x^*, P^{-1})$ is the Gaussian approximation $\pi_G(x \mid \theta, y)$. L4 is the outer Laplace step: the identity above with $\pi_G$ in the denominator, evaluated at $x^*$, where $\pi_G(x^* \mid \theta, y) = (2\pi)^{-n/2}\det P^{1/2}$. L6 is the inner step, the full Laplace strategy: for each value $z$ it holds $x_i = z$, maximizes over the other coordinates, and divides by the Gaussian approximation of their conditional law, whose precision is $P_{-i} = Q_{-i,-i} + \operatorname{diag}(c_{-i})$. L9 integrates $\theta$ out by the rectangle rule on the grid.

The cheap alternative to L5 to L7 is the Gaussian strategy: use the marginal $N(x^*_i, (P^{-1})_{ii})$ of $\pi_G$. It needs only the diagonal of $P^{-1}$, but it cannot show skewness.

The same weights give the [marginal likelihood](/marginal-likelihood/): $\pi(y) \approx \Delta\sum_k e^{\ell_k}$, when the constants of the prior and the likelihood are kept.

## Example

**A tiny Poisson model.** Two counts $y = (3, 7)$ with $y_j \sim \mathrm{Poisson}(e^{x_j})$, a latent pair with precision $Q = \tau\begin{pmatrix}2 & -1\\ -1 & 2\end{pmatrix}$, $\theta = \log\tau$, and $\tau \sim$ Gamma(1, 1), so $\pi(\theta) = e^{\theta}e^{-e^{\theta}}$. The grid is $\theta = -6, -5.9, \ldots, 4$ ($K = 101$, $\Delta = 0.1$), and the marginal of $x_1$ is computed at $z = -4, -3.95, \ldots, 5$. The reference values come from brute-force two-dimensional integration over $(x_1, x_2)$ with the trapezoid rule for each $\theta$; halving its spacing changes the reference mean of $x_1$ by less than $10^{-6}$.

| $\theta$ | $\tau$ | $x^*_1$ | $x^*_2$ | Gaussian sd of $x_1$ | $\tilde\pi(\theta \mid y)$ | exact $\pi(\theta \mid y)$ |
|---|---|---|---|---|---|---|
| $-3.0$ | 0.0498 | 1.0942 | 1.9261 | 0.5692 | 0.0261 | 0.0266 |
| $-2.0$ | 0.1353 | 1.0859 | 1.8923 | 0.5564 | 0.1371 | 0.1391 |
| $-1.0$ | 0.3679 | 1.0591 | 1.8023 | 0.5271 | 0.4204 | 0.4221 |
| $-0.5$ | 0.6065 | 1.0271 | 1.7129 | 0.5031 | 0.4926 | 0.4912 |
| $0.0$ | 1.0000 | 0.9690 | 1.5733 | 0.4720 | 0.3758 | 0.3722 |
| $1.0$ | 2.7183 | 0.7219 | 1.0974 | 0.3887 | 0.0364 | 0.0357 |

For small $\tau$ the prior is weak and the modes sit near $\log 3 = 1.10$ and $\log 7 = 1.95$; as $\tau$ grows, both are pulled towards $0$ and towards each other. L4 is within $2$ percent of the exact density of $\theta$ near its mode. Over the whole grid, the total variation distance between the weights and the exact ones is $0.0041$, and the posterior mean of $\theta$ is $-0.7561$ against $-0.7645$. The estimate of $\log\pi(y)$ is $-6.9272$ against $-6.9117$.

| marginal of $x_1$ | mean | sd | total variation from exact |
|---|---|---|---|
| exact (brute force) | 0.9132 | 0.5270 | 0 |
| Gaussian strategy | 1.0176 | 0.5139 | 0.056 |
| full Laplace (L6) | 0.9128 | 0.5266 | 0.0006 |

The posterior of $x_1$ is skewed to the left, because a Poisson likelihood on the log scale is. The Gaussian strategy puts its centre at the mode and misses the mean by $0.20$ standard deviations. The full Laplace step of L6 is a hundred times closer.

**More data, smaller error.** Multiplying the counts by $10$ and $100$ (with grids that follow the narrower posteriors):

| $y$ | total variation of the $\theta$ weights | Gaussian strategy: error of the mean of $x_1$, in sd | full Laplace: error of the mean of $x_1$ |
|---|---|---|---|
| (3, 7) | 0.0041 | 0.20 | 0.0004 |
| (30, 70) | 0.00002 | 0.09 | below $10^{-4}$ |
| (300, 700) | below $10^{-5}$ | 0.03 | below $10^{-4}$ |

**Binary data.** With $y = (1, 0)$ and $y_j \sim$ Bernoulli$(1/(1 + e^{-x_j}))$, the same model has much less information per latent value. The total variation of the $\theta$ weights grows to $0.012$. The exact posterior of $x_1$ has mean $0.3788$ and sd $1.1961$; full Laplace gives $0.3660$ and $1.1832$, and the Gaussian strategy $0.3264$ and $1.1010$.

**A Gaussian likelihood is exact.** If $y_j \sim N(x_j, s^2)$, then $\pi(x \mid \theta, y)$ is Gaussian, L2 converges in one step, and L4 and L6 are exact. The tests check this for four latent values: the differences of $\ell_k$ match the exact log marginal likelihood $\log N(y; 0, Q^{-1} + s^2 I)$ to $10^{-9}$.

## Correctness

The full proof is in proofs/correctness.md. It proves:

1. **The basic identity.** $\pi(\theta \mid y) = \pi(x, \theta, y)/(\pi(x \mid \theta, y)\pi(y))$ for every $x$. L4 is this identity with the Gaussian approximation in place of $\pi(x \mid \theta, y)$, evaluated at its mode; the factors $(2\pi)^{-n/2}$ cancel.
2. **The inner step.** With concave log-likelihood terms and $Q$ positive definite, $F_\theta$ is strictly concave and has a unique maximizer. The linear system of L2 is exactly the Newton step, and its only fixed point is the mode.
3. **The marginal step.** L6 is the same identity applied to the split $x = (x_i, x_{-i})$ for fixed $\theta$.
4. **Exactness for a Gaussian likelihood.** Then the Gaussian approximation is the exact conditional, so L4 is exact up to a constant, both the Gaussian and the full Laplace marginals are exact, and the only error left is the quadrature over $\theta$ in L9.
5. **The quadrature.** L8 and L9 are the rectangle rule for $\int \pi(x_i \mid \theta, y)\pi(\theta \mid y)\, d\theta$, normalized by the same rule for $\int \pi(\theta \mid y)\, d\theta$.

What is proved and what is cited: claims 1 to 5 are exact. For a non-Gaussian likelihood, the size of the error of L4 and L6 is not proved here. Tierney and Kadane (1986) show that ratios of Laplace approximations have small relative errors when the dimension is fixed and the data grow. Rue, Martino and Chopin (2009) discuss the error when the dimension grows with the data, as it does in latent Gaussian models, and Fong, Rue and Wakefield (2010) report poor accuracy for binary data with few observations per latent value. All error sizes in the example are measured against brute-force integration only.

## Complexity

For each of the $K$ grid values, L2 takes $I$ Newton steps, each one a sparse Cholesky factorization of cost $C$ and two triangular solves of cost $O(F)$, where $F$ is the number of non-zeros of the factor. The cost $C$ depends on the graph of $Q$, after a fill-reducing ordering such as [nested dissection](/nested-dissection/): $\Theta(n)$ for a time series (a band matrix), $\Theta(n^{3/2})$ for a field on a two-dimensional grid, and $\Theta(n^2)$ in three dimensions. The full Laplace step L5 to L7 repeats the inner optimization for $G$ values of one coordinate, so one marginal costs $\Theta(KGIC)$ and all $n$ marginals cost $n$ times as much. The Gaussian strategy needs the diagonal of $P^{-1}$, which recursions on the Cholesky factor give at a cost of the order of the factorization, so all its marginals cost $\Theta(KIC)$. The implementation here uses dense matrices, so $C = \Theta(n^3)$, which suits only small $n$. A grid in $m$ hyperparameters has $K$ exponential in $m$, which is why INLA is limited to a few hyperparameters. The memory holds one factor and the marginals, $\Theta(KG + F)$.

## Properties

- **Deterministic.** The same input always gives the same output, with no Monte Carlo error and no convergence diagnostics.
- **Not exact,** except for a Gaussian likelihood, where only the quadrature over $\theta$ is approximate.
- **Marginals, not the joint law.** INLA returns the marginal densities of single coordinates and of the hyperparameters. Joint quantities need extra work, such as sampling from the Gaussian approximations.
- **Byproducts.** The weights of L4 give the marginal likelihood for [Bayes factors](/bayes-factor/), and the Gaussian approximations give predictive quantities for model checking.
- **Requires a latent Gaussian structure:** each observation depends on the latent field through few coordinates, and the hyperparameters are few.

## Variants and improvements

- **Simplified Laplace.** Rue, Martino and Chopin expand the full Laplace density of L6 in $z$ to third order around the mode, which adds a skewness correction to the Gaussian strategy at a much smaller cost. It is the default in the R-INLA software.
- **Cheaper full Laplace.** Instead of a new Newton run in L6, use the conditional mean of $x_{-i}$ under $\pi_G$ given $x_i = z$, and update only the coordinates near $i$ in the graph.
- **Exploration of the hyperparameter space.** Find the mode of $\tilde\pi(\theta \mid y)$ by optimization, use its curvature to rotate and scale the coordinates, and lay out the grid in the new coordinates, stopping in each direction when $\log\tilde\pi$ has fallen by a fixed amount. For many hyperparameters, a central composite design replaces the full grid; with only the mode, INLA becomes an [empirical Bayes](/empirical-bayes/) method.
- **The stochastic partial differential equation approach.** Lindgren, Rue and Lindström (2011) represent Matérn [Gaussian processes](/gaussian-process/) by sparse Gaussian Markov random fields on a triangulation, which brings spatial [kriging](/kriging/) models into the scope of INLA.
- **Other deterministic methods.** [Expectation propagation](/expectation-propagation/) and [variational inference](/variational-inference/) also approximate the posterior of latent Gaussian models without sampling, by different criteria.

## When to use it

Use INLA for latent Gaussian models with a few hyperparameters and a large latent field: [generalized linear models](/generalized-linear-model/) with random effects, [linear mixed models](/linear-mixed-model/) with non-Gaussian responses, disease mapping, spatial and spatio-temporal models, smoothing splines, and survival models. In these models it is often orders of magnitude faster than [Gibbs sampling](/gibbs-sampling/) or [Hamiltonian Monte Carlo](/hamiltonian-monte-carlo/) at similar accuracy. Prefer a Monte Carlo method when there are many hyperparameters, when the latent field is not Gaussian, when the likelihood terms depend on many latent values at once, or when the data carry little information per latent value, as with binary data.

## Pitfalls

- **Gaussian marginals of skewed posteriors.** Taking the Gaussian strategy in place of L6 puts the marginal at the mode; in the Poisson example its mean is off by $0.20$ standard deviations. Use the full or simplified Laplace step for marginals that matter.
- **A grid that misses mass.** If the grid of L1 is too narrow, the normalization of L8 renormalizes the part it covers and the marginals lose their tails. Check that the weights at both ends of the grid are negligible; here they are below $10^{-5}$.
- **Little information per latent value.** For binary data with one observation per random effect, the Gaussian approximation of L2 is poor, and L4 inherits its error; the weights in the example are three times further from the truth than with counts. Compare with a Monte Carlo method on such data (Fong, Rue and Wakefield 2010).
- **Non-concave log-likelihood terms.** With a Student t likelihood, for example, $c_j$ can be negative, $P$ in L2 need not be positive definite, and Newton's method can fail or find a local mode. Check the factorization, and use a robust optimizer for L2.
- **Dense algebra.** Factoring $Q + \operatorname{diag}(c)$ in L3 as a dense matrix costs $\Theta(n^3)$ and makes large models infeasible. Use a [sparse](/sparse-matrix/) Cholesky factorization with a fill-reducing ordering; see [sparse linear systems](/sparse-linear-systems/).
- **Dropping the log determinants.** Omitting $\frac12\log\det Q$ or $\frac12\log\det P$ in L4 makes $\tilde\pi(\theta \mid y)$ the profile of the joint density at its mode. A weaker prior always lets the mode fit the data better, so the profile favours small $\tau$, too little smoothing: in the Poisson example, dropping both terms moves the posterior mean of $\theta$ from $-0.76$ to $-1.75$. Keep both terms.

## Implementations

## History

Laplace approximations of posterior marginals as ratios of integrals go back to Tierney and Kadane (1986). Rue and Held developed fast computations for Gaussian Markov random fields with sparse Cholesky factors in the early 2000s. Rue, Martino and Chopin combined the two in the integrated nested Laplace approximation, read to the Royal Statistical Society in 2008 and published with discussion in 2009. Fong, Rue and Wakefield (2010) studied it for generalized linear mixed models, and Lindgren, Rue and Lindström (2011) extended its reach to continuous spatial fields. The R-INLA package made the method a standard tool in epidemiology, ecology and spatial statistics.

## References
