---
tag: 6GME91
kind: model
slug: gaussian-process
name: Gaussian process
aliases:
- Gaussian process regression
area: machine-learning/probabilistic-inference
level: advanced
summary: "A distribution over functions in which every finite set of values is jointly Gaussian; GP regression gives a closed form posterior in O(n^3) time by Cholesky."
prereqs: [cholesky-decomposition, kernel-trick, bayesian-inference, covariance-matrix]
see_also: [kernel-ridge-regression, mercer-theorem, representer-theorem, marginal-likelihood, support-vector-regression, state-space-model, expectation-propagation, bayesian-network]
sources:
  - book: isbn:9780262182539
    title: Carl Edward Rasmussen and Christopher K. I. Williams, Gaussian Processes for Machine Learning, MIT Press, 2006
    locator: "Chapter 2 (Section 2.1 the weight-space view, Section 2.2 the function-space view with the predictive equations and Algorithm 2.1, Section 2.8 history), Chapter 4 (covariance functions), Section 5.4 (the marginal likelihood and its derivatives), Section 6.2 (the regularization view), Chapter 8 (approximations for large data sets)"
  - book: isbn:9780387310732
    title: Christopher M. Bishop, Pattern Recognition and Machine Learning, Springer, 2006
    locator: "Section 6.4 (Gaussian processes: linear regression revisited, GP regression, learning the hyperparameters)"
  - paper: "George S. Kimeldorf and Grace Wahba, A correspondence between Bayesian estimation on stochastic processes and smoothing by splines, Annals of Mathematical Statistics 41(2):495-502, 1970"
    title: Kimeldorf and Wahba 1970
    locator: the posterior mean of a Gaussian process prior equals the solution of a penalized least squares problem in the reproducing kernel Hilbert space
  - paper: "Christopher K. I. Williams and Carl Edward Rasmussen, Gaussian processes for regression, Advances in Neural Information Processing Systems 8, 1996"
    title: Williams and Rasmussen 1996
    locator: GP regression for machine learning, with hyperparameters fitted by the marginal likelihood
  - paper: "Joaquin Quiñonero-Candela and Carl Edward Rasmussen, A unifying view of sparse approximate Gaussian process regression, Journal of Machine Learning Research 6:1939-1959, 2005"
    title: Quiñonero-Candela and Rasmussen 2005
    locator: inducing point approximations as modified priors, with O(n m^2) cost for m inducing points
  - paper: "Michalis K. Titsias, Variational learning of inducing variables in sparse Gaussian processes, Proceedings of AISTATS 2009, PMLR 5"
    title: Titsias 2009
    locator: a variational lower bound on the marginal likelihood for choosing the inducing points
---

A Gaussian process is a distribution over functions $f : \mathcal{X} \to \mathbb{R}$ in which, for every finite set of inputs, the vector of function values has a multivariate normal distribution. It is fixed by a mean function $m$ and a positive semidefinite covariance function $k$, the *kernel*, and written $f \sim \mathcal{GP}(m, k)$. In *GP regression* with Gaussian noise, the posterior at new inputs is again Gaussian, with a mean and a variance in closed form. Algorithm 2.1 of Rasmussen and Williams computes them with one [Cholesky factorization](/cholesky-decomposition/) in $O(n^3)$ time for $n$ training points, and its posterior mean equals the prediction of [kernel ridge regression](/kernel-ridge-regression/) with $\lambda$ equal to the noise variance.

## The machine

**The prior.** A Gaussian process on an input set $\mathcal{X}$ is a family of random variables $\{f(x) : x \in \mathcal{X}\}$ such that for every $m \ge 1$ and $x_1, \ldots, x_m \in \mathcal{X}$,

$$\big(f(x_1), \ldots, f(x_m)\big) \sim \mathcal{N}\big(\mu, K\big), \qquad \mu_i = m(x_i), \quad K_{ij} = k(x_i, x_j).$$

These finite distributions are consistent with each other (a marginal of a normal vector is normal with the sub-vector and sub-matrix), so a function $k$ defines a process exactly when every such matrix $K$ is positive semidefinite. Common kernels are the squared exponential $k(x, x') = \sigma_f^2 \exp(-\|x - x'\|^2 / 2 \ell^2)$, with the signal variance $\sigma_f^2$ and the length scale $\ell$, the Matérn family, and the linear kernel $x^\top x'$. The kernel fixes the smoothness and the scale of the functions; see [Mercer's theorem](/mercer-theorem/) and the [kernel trick](/kernel-trick/). This page takes $m = 0$, which is the usual choice after centering the targets.

**The regression model.** The data are $n$ pairs $(x_i, y_i)$ with $y_i = f(x_i) + \varepsilon_i$, where the noise terms $\varepsilon_i \sim \mathcal{N}(0, \sigma_n^2)$ are independent of each other and of $f$. Write $X$ for the inputs, $K = K(X, X)$ for the $n \times n$ Gram matrix, and, for test inputs $X_\ast$, $K_\ast = K(X, X_\ast)$ and $K_{\ast\ast} = K(X_\ast, X_\ast)$. The query is the posterior of $f_\ast = f(X_\ast)$ given $y$, and the marginal likelihood $p(y \mid X)$ of the hyperparameters $\sigma_f, \ell, \sigma_n$.

**The posterior.** The vector $(y, f_\ast)$ is normal with the covariance $\begin{pmatrix} K + \sigma_n^2 I & K_\ast \\ K_\ast^\top & K_{\ast\ast} \end{pmatrix}$. Conditioning gives (Rasmussen and Williams, Section 2.2)

$$f_\ast \mid X, y, X_\ast \sim \mathcal{N}\big(\bar f_\ast, \operatorname{cov}(f_\ast)\big), \qquad \bar f_\ast = K_\ast^\top (K + \sigma_n^2 I)^{-1} y, \qquad \operatorname{cov}(f_\ast) = K_{\ast\ast} - K_\ast^\top (K + \sigma_n^2 I)^{-1} K_\ast.$$

*Proof.* Let $A = K + \sigma_n^2 I$, which is positive definite since $\sigma_n^2 > 0$, and let $w = f_\ast - K_\ast^\top A^{-1} y$. Then $\operatorname{Cov}(w, y) = K_\ast^\top - K_\ast^\top A^{-1} A = 0$. The pair $(w, y)$ is a linear image of a normal vector, so it is jointly normal, and zero covariance makes $w$ independent of $y$. Hence given $y$, $f_\ast = K_\ast^\top A^{-1} y + w$, where $w$ is normal with mean 0 and covariance $K_{\ast\ast} - 2 K_\ast^\top A^{-1} K_\ast + K_\ast^\top A^{-1} A A^{-1} K_\ast = K_{\ast\ast} - K_\ast^\top A^{-1} K_\ast$. $\square$

A prediction of a noisy target $y_\ast$ adds $\sigma_n^2$ to the variance.

## What it counts

The model gives two kinds of numbers.

- **The predictive distribution.** For each test input $x_\ast$, the mean $\bar f_\ast$ and the variance $\mathbb{V}[f_\ast]$, which give error bars.
- **The log marginal likelihood.** Since $y \sim \mathcal{N}(0, K + \sigma_n^2 I)$,
  $$\log p(y \mid X) = -\tfrac12 y^\top (K + \sigma_n^2 I)^{-1} y - \tfrac12 \log \det (K + \sigma_n^2 I) - \tfrac{n}{2} \log 2\pi.$$
  The first term rewards fit, the second penalizes complex models, and the third is a constant. It is the [marginal likelihood](/marginal-likelihood/) of the hyperparameters, and it is the usual criterion to fit them.

The cost is counted in arithmetic operations on reals, as a function of $n$ and of the number of test points. A kernel evaluation costs $O(d)$ for inputs in $\mathbb{R}^d$.

## Relation to other models

- **Kernel ridge regression.** The posterior mean $k_\ast^\top (K + \sigma_n^2 I)^{-1} y$ is the prediction $k_\ast^\top \alpha$ with $(K + \lambda I) \alpha = y$ of [kernel ridge regression](/kernel-ridge-regression/), with $\lambda = \sigma_n^2$. Equivalently, the posterior mean minimizes $\sum_i (y_i - f(x_i))^2 + \sigma_n^2 \|f\|_{\mathcal{H}}^2$ over the reproducing kernel Hilbert space $\mathcal{H}$ of $k$ (Kimeldorf and Wahba 1970; Rasmussen and Williams, Section 6.2). Kernel ridge regression gives only this point estimate. The GP adds the variance and the marginal likelihood.
- **Bayesian linear regression.** With $f(x) = \phi(x)^\top w$ and $w \sim \mathcal{N}(0, \Sigma_p)$, $f$ is a GP with the kernel $\phi(x)^\top \Sigma_p \phi(x')$. The weight-space and the function-space computations give the same posterior (Rasmussen and Williams, Section 2.1). The weight-space form costs $O(n D^2 + D^3)$ for $D$ features, and the function-space form $O(n^3)$, so the choice depends on which of $n$ and $D$ is smaller.
- **Splines and kriging.** Smoothing splines are posterior means for particular GP priors (Kimeldorf and Wahba 1970). In geostatistics the same predictor is called kriging.
- **State space models.** In one dimension, a GP with the exponential kernel $\exp(-|x - x'|/\ell)$ is a Markov process (the Ornstein-Uhlenbeck process). It is then a linear Gaussian [state space model](/state-space-model/), and a Kalman filter and smoother do the regression in $O(n)$ time after sorting the inputs.
- **Other likelihoods.** For classification, or any non-Gaussian likelihood, the posterior is no longer Gaussian. Laplace approximations and [expectation propagation](/expectation-propagation/) give Gaussian approximations (Rasmussen and Williams, Chapter 3).
- **Gaussian graphical models.** A GP restricted to finitely many inputs is a multivariate normal vector. A [Gaussian graphical model](/gaussian-graphical-model/) describes the same object by the zeros of the inverse covariance instead of by a kernel.

## Known results in the model

### Algorithm 2.1

```pseudo id=main
GP-REGRESSION(X, y, k, σ_n², x_*)
L1  L ← cholesky(K + σ_n² I)                       ▷ K_ij = k(x_i, x_j)
L2  α ← Lᵀ \ (L \ y)                                ▷ two triangular solves
L3  f̄_* ← k_*ᵀ α                                    ▷ k_* = (k(x_1, x_*), …, k(x_n, x_*))
L4  v ← L \ k_*
L5  V[f_*] ← k(x_*, x_*) − vᵀ v
L6  log p(y | X) ← −½ yᵀ α − Σ_i log L_ii − (n/2) log 2π
L7  return f̄_*, V[f_*], log p(y | X)
```

Line L2 gives $\alpha = A^{-1} y$ for $A = L L^\top$. Line L5 uses $v^\top v = k_\ast^\top L^{-\top} L^{-1} k_\ast = k_\ast^\top A^{-1} k_\ast$. Line L6 uses $\log \det A = 2 \sum_i \log L_{ii}$. No inverse is formed, and the Cholesky factor exists and is stable because $A$ has all eigenvalues at least $\sigma_n^2 > 0$.

**Cost.** Line L1 costs $\Theta(n^3)$ operations, about $n^3/3$ floating point operations, plus $O(n^2 d)$ for the Gram matrix. Line L2 costs $O(n^2)$. For each test point, line L3 costs $O(n d)$ and lines L4 and L5 cost $O(n^2)$. The memory is $\Theta(n^2)$ for $L$. These are exact, worst-case counts.

### A worked example

Take $X = (0, 1, 3)$, $y = (0.5, 1.0, -0.5)$, the squared exponential kernel with $\sigma_f^2 = 1$ and $\ell = 1$, and $\sigma_n^2 = 0.1$. Then

$$K \approx \begin{pmatrix} 1 & 0.6065 & 0.0111 \\ 0.6065 & 1 & 0.1353 \\ 0.0111 & 0.1353 & 1 \end{pmatrix}, \qquad L \approx \begin{pmatrix} 1.0488 & 0 & 0 \\ 0.5783 & 0.8750 & 0 \\ 0.0106 & 0.1477 & 1.0383 \end{pmatrix},$$

and $\alpha \approx (-0.1154, 1.0443, -0.5819)$. At $x_\ast = 2$, $k_\ast \approx (0.1353, 0.6065, 0.6065)$, so $\bar f_\ast \approx 0.2649$ and $\mathbb{V}[f_\ast] \approx 0.3674$, against the prior variance 1. At the training input $x_\ast = 1$, the mean is $0.8956$, pulled from $y = 1$ toward 0 by the noise, and the variance is $0.0867$. At $x_\ast = 10$, far from the data, the mean is 0 and the variance is 1 to within $10^{-10}$: the prior comes back. The log marginal likelihood is $-3.3473$. For the length scales $\ell = 0.3, 0.5, 1, 2, 4$ it is $-3.5800, -3.5261, -3.3473, -3.7182, -4.6762$, so of these the marginal likelihood prefers $\ell = 1$.

### The variance shrinks and does not see the targets

For every test input, $0 \le \mathbb{V}[f_\ast] \le k(x_\ast, x_\ast)$. The lower bound holds because a posterior covariance is positive semidefinite. The upper bound holds because $k_\ast^\top A^{-1} k_\ast \ge 0$ for the positive definite $A$. The variance does not depend on $y$ at all, only on where the inputs are. So a GP can plan where to measure before it measures, which is the basis of Bayesian optimization and of optimal design.

### Fitting the hyperparameters

The hyperparameters $\theta$ of $k$ and $\sigma_n^2$ are usually fitted by maximizing $\log p(y \mid X, \theta)$, called type II maximum likelihood. With $A = K + \sigma_n^2 I$ and $\alpha = A^{-1} y$, the gradient is

$$\frac{\partial}{\partial \theta_j} \log p(y \mid X, \theta) = \tfrac12 \operatorname{tr}\Big( (\alpha \alpha^\top - A^{-1}) \frac{\partial A}{\partial \theta_j} \Big)$$

(Rasmussen and Williams, Section 5.4.1), which costs $O(n^3)$ once and then $O(n^2)$ per hyperparameter. The surface can have several local maxima, for example one with a short length scale and little noise and one with a long length scale and much noise.

### Large data sets

The $O(n^3)$ time and $O(n^2)$ memory limit exact GP regression to some tens of thousands of points. Inducing point methods choose $m \ll n$ points and approximate the prior through them, at $O(n m^2)$ time; Quiñonero-Candela and Rasmussen (2005) put many of them in one frame as modified priors, and Titsias (2009) chose the inducing points by a variational lower bound on the marginal likelihood. Iterative solvers such as [conjugate gradient](/conjugate-gradient-method/) replace the factorization with matrix-vector products.

### Pitfalls

- **Inverting the matrix.** Forming $(K + \sigma_n^2 I)^{-1}$ is slower and less stable than the Cholesky solves of Algorithm 2.1.
- **No noise term.** With $\sigma_n^2 = 0$ and close inputs, $K$ is nearly singular, and the Cholesky factorization fails. Add a small jitter to the diagonal for noise-free data.
- **Variance of $f$ or of $y$.** The variance of line L5 is for the latent $f$. Add $\sigma_n^2$ for a new noisy observation.
- **Unscaled targets.** A zero mean prior pulls the predictions toward 0 away from the data. Center the targets, or use a mean function.

## References
