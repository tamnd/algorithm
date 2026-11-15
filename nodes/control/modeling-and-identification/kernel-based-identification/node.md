---
tag: BXFFBH
kind: algorithm
slug: kernel-based-identification
name: Kernel-based system identification
aliases:
- regularized FIR identification
- stable spline kernel method
area: control/modeling-and-identification
level: research
summary: Estimates a long impulse response by regularized least squares with a kernel, such as the TC kernel, that encodes exponential decay.
solves: [system-identification]
model: real-ram
complexity:
  vars: {N: the number of samples, d: the FIR length, G: the number of grid points}
  time: {worst: O(N d^2 + G d^3)}
  space: {extra: O(N d + d^2)}
properties: {deterministic: true, online: false, exact: true, iterative: false}
history:
  year: 2010
  people: [Gianluigi Pillonetto, Giuseppe De Nicolao]
  note: "Pillonetto and De Nicolao proposed the stable spline kernel for impulse response estimation in Automatica in 2010; Chen, Ohlsson and Ljung added the TC and DC kernels in 2012."
prereqs: [impulse-response, tikhonov-regularization, gaussian-process, marginal-likelihood]
see_also: [least-squares-arx-identification, prediction-error-method, empirical-bayes, kernel-ridge-regression, cholesky-decomposition, fir-filter, bias-variance-tradeoff, ho-kalman-algorithm]
sources:
  - paper: doi:10.1016/j.automatica.2009.10.031
    title: "Gianluigi Pillonetto and Giuseppe De Nicolao, A new kernel-based approach for linear system identification, Automatica 46(1), 81-93, 2010"
    locator: the stable spline kernel, the Gaussian prior on the impulse response, and the choice of hyperparameters by the marginal likelihood
  - paper: doi:10.1016/j.automatica.2012.05.026
    title: "Tianshi Chen, Henrik Ohlsson and Lennart Ljung, On the estimation of transfer functions, regularizations and Gaussian processes, Revisited, Automatica 48(8), 1525-1535, 2012"
    locator: the TC and DC kernels and the comparison of regularized FIR estimates with prediction error methods
  - paper: doi:10.1016/j.automatica.2014.01.001
    title: "Gianluigi Pillonetto, Francesco Dinuzzo, Tianshi Chen, Giuseppe De Nicolao and Lennart Ljung, Kernel methods in system identification, machine learning and function estimation: A survey, Automatica 50(3), 657-682, 2014"
    locator: the survey of kernels for asymptotically stable systems, empirical Bayes and the relation to regularized least squares
---

Kernel-based identification estimates the [impulse response](/impulse-response/) $g_1, g_2, \ldots, g_d$ of a linear system from input-output data. It fits a long FIR model, with $d$ much larger than the true order, by regularized least squares. The regularization matrix comes from a kernel that encodes what we know about asymptotically stable systems: the coefficients decay exponentially and neighbouring coefficients are correlated. The kernel has two or three hyperparameters, and the method chooses them by maximizing the marginal likelihood of the data. This differs from [least squares ARX identification](/least-squares-arx-identification/) and from a [prediction error method](/prediction-error-method/), which fit a model with a fixed small order and need a choice of that order. Here the model is long and the kernel controls its complexity. The estimate is also the posterior mean of a [Gaussian process](/gaussian-process/) model of the impulse response.

## In plain words

A plain least squares fit of 50 impulse response coefficients from 100 samples is very noisy: each coefficient has little data, and the tail of the estimate wanders around zero. We know more than the data say. The true coefficients get smaller as the lag grows, and they change smoothly from one lag to the next. The kernel writes this knowledge as a prior covariance: large variance for the first lags, smaller variance for later lags, and strong correlation between neighbours. Regularized least squares then pulls the estimate toward such shapes. How fast the prior decays and how large it is are not known in advance, so the method tries values on a grid and keeps the one for which the observed data are most probable.

## The problem

**Input.** Scalar samples $u_0, \ldots, u_{N-1}$ and $y_0, \ldots, y_{N-1}$, the FIR length $d < N$, a kernel family $K(\eta)$ with a finite grid of hyperparameters $\eta$, and optionally the noise variance $\sigma^2$.

**Output.** An estimate $\hat g \in \mathbb{R}^d$ of the impulse response, the chosen hyperparameters $\eta^*$, and the noise variance used.

**Model.** $y_k = \sum_{t=1}^{d} g_t u_{k-t} + e_k$ with $u_t = 0$ for $t < 0$, and $e_k$ white Gaussian noise with variance $\sigma^2$. In matrix form $y = \Phi g + e$, where $\Phi$ is the $N \times d$ regressor with $\Phi_{k,t} = u_{k-t}$.

**Kernels.** The TC (tuned/correlated) kernel is $K_{ij} = c \lambda^{\max(i,j)}$ with $c > 0$ and $0 < \lambda < 1$. It is also the first order stable spline kernel. The DC (diagonal/correlated) kernel is $K_{ij} = c \lambda^{(i+j)/2} \rho^{|i-j|}$ with $|\rho| < 1$; with $\rho = \sqrt{\lambda}$ it is the TC kernel. In both, $\lambda$ sets the decay rate and $c$ the scale.

## The algorithm

```pseudo id=main
KERNEL-FIR(u, y, d, grid, σ²)
L1  Φ ← the N × d regressor, Φ[k][t] = u_(k-t)
L2  R ← Φ^T Φ;  r ← Φ^T y;  yy ← y^T y
L3  if σ² is not given: σ² ← the residual sum of squares of the least squares FIR fit / (N - d)
L4  for each η in the grid:
L5      K ← K(η);  L ← the Cholesky factor of K;  M ← σ² I + L^T R L
L6      cost ← (yy - (L^T r)^T M⁻¹ L^T r) / σ² + (N - d) log σ² + log det M
L7      if cost < the best cost so far: keep η and the cost
L8  ĝ ← L M⁻¹ L^T r for the kept η
L9  return (ĝ, η, σ²)
```

The estimate is the minimizer of the regularized criterion

$$\lVert y - \Phi g \rVert^2 + \sigma^2 g^T K^{-1} g, \qquad \hat g = (R + \sigma^2 K^{-1})^{-1} r = K \Phi^T Z^{-1} y,$$

with $Z = \Phi K \Phi^T + \sigma^2 I_N$. If $g$ has the prior $\mathcal{N}(0, K)$, then $y$ has the distribution $\mathcal{N}(0, Z)$, and the cost of L6 is $y^T Z^{-1} y + \log \det Z$, which is minus two times the log marginal likelihood, up to a constant. Choosing $\eta$ this way is [empirical Bayes](/empirical-bayes/). The code never forms the $N \times N$ matrix $Z$. With $K = L L^T$, the push-through identity, the Woodbury identity and Sylvester's determinant identity give the $d \times d$ forms of L5, L6 and L8. They also avoid $K^{-1}$, which is badly conditioned when $\lambda^d$ is small. L3 is the unbiased estimate of the noise variance from the plain least squares fit.

## Example

Take the impulse response

$$g_k = 0.5 \cdot 0.9^{k-1} \cos(0.6 (k-1)) + 0.3 \cdot 0.6^{k-1}, \qquad k = 1, \ldots, 50,$$

a lightly damped mode plus a fast real pole, so $d = 50$. The input is Gaussian white noise with unit variance, the noise has $\sigma = 0.3$, and the random seed is 1. Measure the quality by the fit $100 (1 - \lVert \hat g - g \rVert / \lVert g \rVert)$ in percent.

The TC grid is $c \in \{0.1, 0.3, 1, 3\}$ and $\lambda \in \{0.6, 0.7, 0.8, 0.85, 0.9, 0.95\}$, 24 points. The DC grid uses the same $c$, $\lambda \in \{0.7, 0.8, 0.9\}$ and $\rho \in \{-0.5, 0, 0.5, 0.9\}$, 48 points.

With $N = 100$ samples, L3 gives $\hat\sigma^2 = 0.0887$ (the true value is $0.09$). The TC search keeps $(c, \lambda) = (0.3, 0.85)$ and the DC search keeps $(c, \lambda, \rho) = (1, 0.8, 0.9)$. The fits are:

| estimate | fit, $N = 100$ | fit, $N = 200$ |
|---|---|---|
| least squares FIR | 59.0 | 83.3 |
| TC kernel | 89.3 | 89.5 |
| DC kernel | 88.5 | 89.5 |

With 100 samples and 50 unknowns, plain least squares is poor, and the kernel estimate is much better. With 200 samples the gap is smaller but still clear. Over the seeds 1 to 5 at $N = 100$, the TC fit was between 84.6 and 89.5 and the least squares fit between 58.8 and 76.9 (measurement).

## Correctness

**Claim.** KERNEL-FIR returns the first grid point that maximizes the Gaussian marginal likelihood of $y$, and the posterior mean of $g$ under the kernel at that point, which is also the unique minimizer of the regularized criterion.

**Key invariant.** For every grid point, with $K = L L^T$ and $M = \sigma^2 I + L^T R L$, the $d \times d$ quantities equal the $N \times N$ ones: $L M^{-1} L^T r = K \Phi^T Z^{-1} y$, $(y^T y - r^T L M^{-1} L^T r)/\sigma^2 = y^T Z^{-1} y$ and $(N - d) \log \sigma^2 + \log \det M = \log \det Z$.

The TC and DC kernels are positive definite, so $L$ exists and $M$ is positive definite. The scan keeps a point only when its cost is strictly smaller. The full proof is below.

## Complexity

In the [real RAM](/real-ram/). L1 is $O(N d)$ and L2 is $O(N d^2)$. Each grid point costs a Cholesky factorization, two products of $d \times d$ matrices, a linear solve and a second Cholesky factorization for $\log \det M$, all $O(d^3)$. With $G$ grid points the total is $O(N d^2 + G d^3)$. The extra space is $O(N d)$ for $\Phi$ and $O(d^2)$ for the matrices; a streaming version forms $R$ and $r$ without storing $\Phi$ and needs $O(d^2)$.

A continuous search over $\eta$ with a quasi-Newton method costs $O(d^3)$ per evaluation of the cost, the same as one grid point.

## Properties

- **Posterior mean (theorem).** Under the Gaussian prior $g \sim \mathcal{N}(0, K)$ and Gaussian noise, $\hat g$ is the posterior mean, and the cost is minus two times the log marginal likelihood up to a constant.
- **Bias and variance (theorem).** For a fixed kernel, $\hat g$ is biased toward zero, but its variance is smaller than that of least squares. The regularization trades bias for variance; see [bias-variance tradeoff](/bias-variance-tradeoff/).
- **No order selection.** The FIR length $d$ only needs to be long enough for the response to decay. The kernel, not $d$, sets the effective number of parameters.
- **Decaying estimates.** With the TC or DC kernel the prior variance of $g_k$ decays as $\lambda^k$, so the estimate decays as well. This is a property of the prior, not a guarantee about every data set.
- **Better accuracy on short records (measurement).** In the example, the TC estimate had a fit near 89 percent where least squares had 59 percent. Chen, Ohlsson and Ljung (2012) report similar gains in Monte Carlo studies, also against prediction error methods with the order chosen by a criterion.
- **Nonconvex hyperparameter search.** The marginal likelihood is not convex in $\eta$. A grid is safe for two or three hyperparameters, but a local search can stop at a local optimum.

## Variants and improvements

- **Stable spline kernels.** Pillonetto and De Nicolao (2010) use the second order stable spline kernel, which makes the estimate smoother. The TC kernel is the first order case.
- **Other kernels.** Sums and products of kernels, kernels for resonant systems, and kernels learned from data. The survey of Pillonetto et al. (2014) describes many.
- **Multiple inputs and outputs.** One impulse response per input-output pair, each with its own kernel, or a shared kernel.
- **Continuous search.** Optimize the marginal likelihood over $\eta$ with gradients. A QR factorization of the stacked regressor gives a more accurate cost than the normal equations.
- **Other tuning criteria.** [Cross-validation](/cross-validation/) or Stein's unbiased risk estimate in place of the marginal likelihood.
- **From FIR to state space.** Fit a low order state-space model to $\hat g$, for example by the [Ho-Kalman algorithm](/ho-kalman-algorithm/) or by model reduction, when a compact model is needed.

## When to use it

Use kernel-based identification for a linear, asymptotically stable system when the data record is short, the noise is large, or the order is unknown. It gives a good impulse response and frequency response without a choice of order and without local minima in the model parameters. Use it as a reference model or as a starting point for a low order fit. For a system with a very slow mode, $d$ must be large, and the cost grows as $d^3$. For an unstable system, the kernels above are wrong.

## Pitfalls

- **$d$ too short.** If $g_d$ is not small, the truncated tail acts as extra noise and biases the result. Check that the estimate has decayed at lag $d$.
- **$K^{-1}$ in the code.** Forming $R + \sigma^2 K^{-1}$ directly fails when $\lambda^d$ is near the machine epsilon. Use the Cholesky factor of $K$ as in L5.
- **Initial conditions.** The code sets $u_t = 0$ for $t < 0$. If the system was not at rest before the record, drop the first $d$ outputs from the fit.
- **A grid that is too coarse.** If the best point is on the edge of the grid, extend the grid.
- **Unknown noise variance.** L3 needs $N > d$ and a nonsingular $R$. With $N$ close to $d$ the estimate of $\sigma^2$ is poor; estimate it from a low order model or include it in the marginal likelihood.
- **Colored noise.** The model assumes white noise. Colored noise gives a wrong marginal likelihood and a wrong choice of $\eta$.

## Implementations

## History

[Tikhonov regularization](/tikhonov-regularization/) of ill-posed least squares problems is much older than this method. The kernel approach of this page starts with Pillonetto and De Nicolao (2010), who treated the impulse response as a Gaussian process with a stable spline kernel and tuned it by the marginal likelihood. Chen, Ohlsson and Ljung (2012) introduced the TC and DC kernels and compared the method with classical prediction error methods. Pillonetto, Dinuzzo, Chen, De Nicolao and Ljung (2014) surveyed the field in Automatica.

## References
