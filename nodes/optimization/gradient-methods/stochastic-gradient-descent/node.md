---
tag: BTB2HV
kind: algorithm
slug: stochastic-gradient-descent
name: Stochastic gradient descent
aliases:
- SGD
- incremental gradient method
- mini-batch SGD
area: optimization/gradient-methods
level: core
summary: Updates weights using gradients estimated on random mini-batches; the basic training loop of deep learning.
solves: [stochastic-optimization]
model: real-ram
complexity:
  vars: {n: the dimension, k: the number of iterations, g: the cost of one stochastic gradient, μ: the strong convexity constant, σ: the standard deviation bound of the gradient noise, ε: the target expected squared distance to the minimizer, δ: "k0 times the initial squared distance, with k0 at least 2L/μ"}
  time: {worst: O(k (g + n))}
  space: {extra: Θ(n)}
  steps: {expected: "⌈max(δ, 4 σ^2 / μ^2) / ε⌉"}
properties: {deterministic: false, exact: false, online: true, recursive: false}
history:
  year: 1951
  people: [Herbert Robbins, Sutton Monro]
  note: Robbins and Monro (1951) introduced the stochastic approximation scheme that SGD instantiates for gradients; Kiefer and Wolfowitz (1952) gave a version with finite differences.
prereqs: [gradient-descent, stochastic-optimization, expected-value, variance]
see_also: [robbins-monro-algorithm, svrg, saga, adagrad, adam, momentum-method, learning-rate-schedule, empirical-risk-minimization]
sources:
  - paper: doi:10.1214/aoms/1177729586
    title: Herbert Robbins and Sutton Monro, A stochastic approximation method, Annals of Mathematical Statistics 22(3), 1951
    locator: pages 400 to 407, the iteration with steps whose sum diverges and whose sum of squares converges, and its convergence in mean square
  - paper: doi:10.1137/070704277
    title: Arkadi Nemirovski, Anatoli Juditsky, Guanghui Lan and Alexander Shapiro, Robust stochastic approximation approach to stochastic programming, SIAM Journal on Optimization 19(4), 2009
    locator: Section 2.1 for the 1/k rate with steps of order 1/(μk) and its sensitivity to μ, Section 2.2 for the averaged robust method with the rate O(1/√K)
  - paper: doi:10.1137/16M1080173
    title: Léon Bottou, Frank E. Curtis and Jorge Nocedal, Optimization methods for large-scale machine learning, SIAM Review 60(2), 2018
    locator: Theorems 4.6 and 4.7 for strongly convex objectives with fixed and diminishing steps, Theorems 4.8 and 4.10 for nonconvex objectives
  - paper: doi:10.1137/120880811
    title: Saeed Ghadimi and Guanghui Lan, Stochastic first- and zeroth-order methods for nonconvex stochastic programming, SIAM Journal on Optimization 23(4), 2013
    locator: Section 2.1, the randomized stochastic gradient method and its O(1/√K) bound on the expected squared gradient norm
  - paper: doi:10.1214/aoms/1177729392
    title: Jack Kiefer and Jacob Wolfowitz, Stochastic estimation of the maximum of a regression function, Annals of Mathematical Statistics 23(3), 1952
    locator: pages 462 to 466, stochastic approximation with finite difference gradient estimates
  - paper: doi:10.1137/0330046
    title: Boris T. Polyak and Anatoli B. Juditsky, Acceleration of stochastic approximation by averaging, SIAM Journal on Control and Optimization 30(4), 1992
    locator: pages 838 to 855, iterate averaging with steps larger than 1/k reaches the optimal asymptotic covariance
  - url: https://arxiv.org/abs/1109.5647
    title: Alexander Rakhlin, Ohad Shamir and Karthik Sridharan, Making gradient descent optimal for strongly convex stochastic optimization, ICML 2012
    locator: Section 3 for the log k lower bound of the plain average, Section 4 for suffix averaging with the O(1/k) rate
  - url: https://arxiv.org/abs/1812.05217
    title: Nicholas J. A. Harvey, Christopher Liaw, Yaniv Plan and Sikander Randhawa, Tight analyses for non-smooth stochastic gradient descent, COLT 2019
    locator: Section 1, the log K lower bound for the last iterate of nonsmooth SGD
---

Stochastic gradient descent (SGD) minimizes an expectation $F(x) = \mathbb{E}_\xi f(x, \xi)$ by taking a [gradient descent](/gradient-descent/) step along a random, unbiased estimate of $\nabla F(x)$, one sample or one mini-batch at a time. It is the gradient form of the [Robbins-Monro algorithm](/robbins-monro-algorithm/) for [stochastic optimization](/stochastic-optimization/). With bounded noise variance and steps of order $1/k$, the expected squared distance to the minimizer of a [strongly convex](/strong-convexity/) smooth function falls as $O(1/k)$; with averaging, the expected gap of a convex function falls as $O(1/\sqrt{k})$. Each step costs one sample, not a pass over the data, which makes SGD the basic training loop for [empirical risk minimization](/empirical-risk-minimization/).

## In plain words

You want the lowest point of a valley, but you only see a blurred map. Each blurred map points downhill on average, but each one is a little wrong.

Take a step along the map you have, then look at a new blurred map and step again. The errors in the maps are random, so they partly cancel over many steps. If you keep the steps the same size, you end up moving around near the bottom and never settle. If you make the steps smaller over time, you settle at the bottom, but slowly. This is how most neural networks are trained: each map comes from a small random batch of the data.

## The problem

Minimize $F(x) = \mathbb{E}_\xi[f(x, \xi)]$ over $x \in \mathbb{R}^n$, or over a closed [convex set](/convex-set/) $X$. The method can call an oracle that returns a random vector $G(x, \xi)$ with $\mathbb{E}[G(x, \xi)] = \nabla F(x)$ (or a subgradient), using a fresh independent sample $\xi$ at each call. For a finite sum $F = \frac{1}{N}\sum_i f_i$, the oracle picks $i$ uniformly at random and returns $\nabla f_i(x)$. The assumptions for the rates are named in each theorem: $\mu$-strong convexity, an $L$-Lipschitz gradient, a variance bound $\mathbb{E}\lVert G - \nabla F\rVert^2 \le \sigma^2$, or a second-moment bound $\mathbb{E}\lVert G\rVert^2 \le G^2$.

## The algorithm

```pseudo id=main
SGD(G, x₀, η, K, P)
L1  x ← x₀
L2  for k ← 0 to K − 1 do
L3      g ← G(x, ξₖ)                ▷ fresh sample, E[g] = ∇F(x)
L4      x ← x − ηₖ g
L5      x ← P(x)                    ▷ only for a constraint set X
L6  return x₀, …, x_K
```

The steps $\eta_k$ are fixed in advance and do not depend on the samples. The method returns all iterates, since the right output depends on the setting: the last iterate for strongly convex problems, a weighted average for convex ones, and a uniformly random iterate for nonconvex ones. A mini-batch oracle averages $b$ independent sample gradients, which divides the variance by $b$ and multiplies the cost by $b$.

## Example

Take $F(x) = \frac{1}{2}x^2$ in one dimension, with the oracle $G(x, \xi) = x + \xi$ and $\xi \sim N(0, 1)$, so $\mu = L = 1$ and $\sigma = 1$. Start at $x_0 = 4$. For this quadratic the recursion $\mathbb{E}x_{k+1}^2 = (1 - \eta_k)^2\,\mathbb{E}x_k^2 + \eta_k^2$ is exact, so the table gives exact expectations, not samples. The diminishing step uses $k_0 = 2$, so $\eta_k = 2/(k + 2)$ and the bound of Theorem 1 is $\nu/(k + 2)$ with $\nu = \max(2 \cdot 16, 4) = 32$.

| $k$ | $\mathbb{E}x_k^2$, step $2/(k + 2)$ | bound $32/(k + 2)$ | $\mathbb{E}x_k^2$, step $0.1$ | bound $0.9^k \cdot 16 + 0.1$ |
|---|---|---|---|---|
| 0 | 16 | 16 | 16 | 16.1 |
| 1 | 1.0 | 10.667 | 12.97 | 14.5 |
| 2 | 0.5556 | 8.0 | 10.5157 | 13.06 |
| 5 | 0.2444 | 4.5714 | 5.6131 | 9.5478 |
| 10 | 0.1273 | 2.6667 | 1.9915 | 5.6789 |
| 20 | 0.0651 | 1.4545 | 0.2883 | 2.0452 |
| 40 | 0.0329 | 0.7619 | 0.0561 | 0.3365 |

The diminishing step keeps falling like $1/k$. The constant step falls fast at first and then stops near $\eta/(2 - \eta) = 0.0526$, the noise floor.

## Correctness

SGD does not reach the minimizer in a finite number of steps; correctness means that the expected error goes to zero at a stated rate. All four results are proved below.

- **Strongly convex and smooth, diminishing steps.** With $k_0 \ge 2L/\mu$ and $\eta_k = 2/(\mu(k + k_0))$, $\mathbb{E}\lVert x_k - x^*\rVert^2 \le \max(k_0\lVert x_0 - x^*\rVert^2, 4\sigma^2/\mu^2)/(k + k_0)$.
- **Strongly convex and smooth, constant step.** With $\eta \le 1/L$, $\mathbb{E}\lVert x_k - x^*\rVert^2 \le (1 - \mu\eta)^k\lVert x_0 - x^*\rVert^2 + \eta\sigma^2/\mu$. The second term is a floor, and the example shows that it is attained up to a factor of 2.
- **Convex, possibly nonsmooth.** With $\mathbb{E}\lVert G\rVert^2 \le G^2$ and the weighted average $\bar{x}_K$ of the iterates, $\mathbb{E}F(\bar{x}_K) - F^* \le (R^2 + G^2\sum\eta_k^2)/(2\sum\eta_k)$, which is $RG/\sqrt{K}$ for $\eta = R/(G\sqrt{K})$.
- **Smooth nonconvex.** With $\eta \le 1/L$, $\frac{1}{K}\sum_{k<K}\mathbb{E}\lVert\nabla F(x_k)\rVert^2 \le 2\Delta/(\eta K) + L\eta\sigma^2$, which is $O(\sigma\sqrt{L\Delta/K} + L\Delta/K)$ for the best fixed step.

The key step in each proof is the same: unbiasedness turns the cross term $\langle G_k, x_k - x^*\rangle$ into $\langle\nabla F(x_k), x_k - x^*\rangle$ in conditional expectation, and the variance bound controls the squared term.

## Complexity

One step costs one oracle call and $O(n)$ arithmetic, with $\Theta(n)$ extra memory. To reach $\mathbb{E}\lVert x_k - x^*\rVert^2 \le \varepsilon$ in the strongly convex case, the first theorem needs $O(\max(\kappa\lVert x_0 - x^*\rVert^2, \sigma^2/\mu^2)/\varepsilon)$ steps, where $\kappa = L/\mu$. In the convex case, $\varepsilon$ accuracy needs $R^2G^2/\varepsilon^2$ steps. For the nonconvex case, a squared gradient norm of $\varepsilon$ needs $O(L\Delta\sigma^2/\varepsilon^2)$ steps. In each case the dependence on $\varepsilon$ and $\sigma$ matches the oracle lower bounds stated on the [stochastic optimization](/stochastic-optimization/) page, so in the worst case no method that sees only such an oracle does better by more than constant and condition number factors. The cost does not depend on the number of data points $N$ in a finite sum, which is the reason SGD is used when $N$ is large.

## Properties

- **Randomized and online.** Each step uses one new sample and the current point only, so SGD can process a data stream once.
- **Noise floor with a constant step.** The iterates do not converge; they fluctuate in a region of size of order $\eta\sigma^2/\mu$ around $x^*$. This is a feature in practice, because a constant step forgets the starting point at a linear rate.
- **Sensitive to the step for $1/k$ steps.** The step $c/k$ needs $c \ge 1/(2\mu)$ or so; with a smaller $c$ the rate can degrade to $O(k^{-2\mu c})$ (Nemirovski et al. 2009, Section 2.1). Averaging with longer steps removes this sensitivity.
- **Interpolation.** If $\sigma^2 = 0$ at the minimizer, as when a model fits all the data exactly, the constant-step bound gives a linear rate.
- **Not a descent method.** $F(x_{k+1})$ can be larger than $F(x_k)$ on any single step.

## Variants and improvements

- **Mini-batches.** Average $b$ sample gradients. This divides $\sigma^2$ by $b$ and allows parallel hardware.
- **Iterate averaging.** Polyak and Juditsky (1992) showed that averaging the iterates of a run with steps longer than $1/k$ attains the best asymptotic covariance. For strongly convex Lipschitz problems, the average of the last half of the iterates gives $O(1/k)$ in function value, while the plain average of all iterates can lose a $\log k$ factor (Rakhlin, Shamir and Sridharan 2012).
- **[Momentum](/momentum-method/).** Heavy-ball momentum is the standard variant in deep learning, used with a [learning rate schedule](/learning-rate-schedule/).
- **Variance reduction.** For finite sums, [SVRG](/svrg/) and [SAGA](/saga/) remove the noise floor and converge linearly.
- **Adaptive steps.** [AdaGrad](/adagrad/), [RMSProp](/rmsprop/) and [Adam](/adam/) scale each coordinate by past gradient sizes.
- **Projected and proximal SGD.** Line L5 handles constraints, and a proximal step handles a nonsmooth regularizer.

## When to use it

Use SGD when the data are large or arrive as a stream, when one pass over the data is too expensive per step, or when the target accuracy is about the size of the statistical error, so that high precision is wasted. It is the default for training neural networks, usually with momentum and a schedule. For a moderately sized finite sum where high accuracy matters, a variance reduced method or a full batch method converges faster.

## Pitfalls

- **Step size.** Too large a step diverges, too small a step crawls, and the $1/(\mu k)$ step needs a good estimate of $\mu$. Tune it, or use averaging.
- **Last iterate in the convex case.** The bounds above hold for the average. The last iterate of nonsmooth SGD has an extra $\log K$ factor in the worst case (Harvey, Liaw, Plan and Randhawa 2019).
- **Sampling with or without replacement.** The proofs assume independent samples. Shuffled epochs, used in practice, are a different method with a different analysis.
- **Heavy-tailed noise.** With infinite variance the bounds do not apply; [gradient clipping](/gradient-clipping/) is a common fix.
- **Stopping.** The gradient norm of a single sample does not go to zero, so it is not a valid stopping test.

## Implementations

## History

Robbins and Monro (1951) introduced stochastic approximation for finding a root of a function observed with noise, with steps whose sum diverges and whose sum of squares converges. Kiefer and Wolfowitz (1952) adapted it to maximization with finite difference estimates. Polyak and Juditsky (1992) showed that averaging the iterates gives the optimal asymptotic rate. Nemirovski, Juditsky, Lan and Shapiro (2009) gave the robust, averaged form with nonasymptotic rates. Ghadimi and Lan (2013) analysed the nonconvex case. Bottou, Curtis and Nocedal (2018) surveyed the method in its role as the main training algorithm of machine learning.

## References
