---
tag: WZNBN6
kind: algorithm
slug: robbins-monro-algorithm
name: Robbins-Monro algorithm
aliases:
- Robbins-Monro procedure
- Robbins-Monro iteration
area: optimization/gradient-methods
level: advanced
summary: The original stochastic approximation scheme with diminishing step sizes for finding roots of noisy functions.
solves: [stochastic-optimization]
model: real-ram
complexity:
  vars: {d: the dimension, k: the number of iterations, c: the cost of one noisy observation, μ: the strong monotonicity constant of the field, σ: "the noise level, with E|H|^2 at most σ^2 + B |x - x*|^2", ε: the target expected squared distance to the root, δ: "n0 times the initial squared distance to the root"}
  time: {worst: O(k (c + d))}
  space: {extra: Θ(d)}
  steps: {expected: "⌈max(δ, 4 σ^2 / μ^2) / ε⌉"}
properties: {deterministic: false, exact: false, online: true, recursive: false}
history:
  year: 1951
  people: [Herbert Robbins, Sutton Monro]
  note: Robbins and Monro (1951) proposed the iteration to find the level at which a response observed with noise has a given mean, and proved convergence in mean square.
prereqs: [expected-value, variance, conditional-expectation]
see_also: [stochastic-approximation, robbins-monro-conditions, stochastic-gradient-descent, stochastic-optimization, q-learning, temporal-difference-learning, quantile, martingale]
sources:
  - paper: doi:10.1214/aoms/1177729586
    title: Herbert Robbins and Sutton Monro, A stochastic approximation method, Annals of Mathematical Statistics 22(3), 1951
    locator: pages 400 to 407, the iteration x_(n+1) = x_n + a_n (α - y_n), the conditions on a_n, and convergence in mean square for a monotone regression function with bounded observations
  - paper: doi:10.1214/aoms/1177729392
    title: Jack Kiefer and Jacob Wolfowitz, Stochastic estimation of the maximum of a regression function, Annals of Mathematical Statistics 23(3), 1952
    locator: pages 462 to 466, the finite difference version for locating a maximum
  - paper: "Julius R. Blum, Approximation methods which converge with probability one, Annals of Mathematical Statistics 25(2), 1954, pages 382 to 386"
    locator: convergence with probability one of the Robbins-Monro and Kiefer-Wolfowitz procedures
  - paper: "Herbert Robbins and David Siegmund, A convergence theorem for non negative almost supermartingales and some applications, in Optimizing Methods in Statistics, Academic Press, 1971, pages 233 to 257"
    locator: the almost supermartingale convergence theorem and its application to stochastic approximation
  - book: isbn:9780387008943
    title: Harold J. Kushner and G. George Yin, Stochastic Approximation and Recursive Algorithms and Applications, second edition, Springer, 2003
    locator: Chapter 1 for examples, Chapter 5 for convergence with probability one by the ODE method, Chapter 10 for rates and averaging
  - book: isbn:9780521515924
    title: Vivek S. Borkar, Stochastic Approximation, A Dynamical Systems Viewpoint, Cambridge University Press, 2008
    locator: Chapter 2, the ODE limit of the iteration with the step conditions
  - paper: doi:10.1137/0330046
    title: Boris T. Polyak and Anatoli B. Juditsky, Acceleration of stochastic approximation by averaging, SIAM Journal on Control and Optimization 30(4), 1992
    locator: pages 838 to 855, averaged iterates with steps longer than 1/n and their optimal asymptotic covariance
---

The Robbins-Monro algorithm finds a root of a function $h(x) = \mathbb{E}_\xi H(x, \xi)$ that can only be observed with noise, by the update $x_{n+1} = x_n - a_nH(x_n, \xi_n)$ with steps $a_n$ whose sum diverges and whose sum of squares converges. These are the [Robbins-Monro conditions](/robbins-monro-conditions/). It is the founding method of [stochastic approximation](/stochastic-approximation/). When $H$ is a noisy gradient it is [stochastic gradient descent](/stochastic-gradient-descent/), and when $h$ is a Bellman residual it gives [temporal difference learning](/temporal-difference-learning/) and [Q-learning](/q-learning/).

## In plain words

You want to set a dial so that a machine gives a certain output on average, but every reading is noisy. Read the machine once at the current setting. If the reading is too high, turn the dial down a little; if it is too low, turn it up.

Make each turn smaller than the last, so the noise of single readings averages out. Do not make the turns shrink too fast, or the dial stops before it gets to the right place. Steps like one over the step number do both things.

## The problem

Given a closed [convex set](/convex-set/) $X \subseteq \mathbb{R}^d$ (often all of $\mathbb{R}^d$) and an oracle that, at any $x \in X$, returns a random vector $Y = H(x, \xi)$ with a fresh independent $\xi$ and $\mathbb{E}Y = h(x)$, find $x^* \in X$ with $h(x^*) = 0$. The original setting is one-dimensional: find the level $\theta$ at which a response with mean $M(x)$ satisfies $M(\theta) = \alpha$, so $h(x) = M(x) - \alpha$. The field $h$ need not be a gradient of anything. The rates below assume strong monotonicity $\langle h(x), x - x^*\rangle \ge \mu\lVert x - x^*\rVert^2$ and the growth bound $\mathbb{E}\lVert H(x, \xi)\rVert^2 \le A + B\lVert x - x^*\rVert^2$ on $X$, which is $\sigma^2 + B\lVert x - x^*\rVert^2$ in the notation of the front matter.

## The algorithm

```pseudo id=main
ROBBINS-MONRO(H, x₀, a, K, P)
L1  x ← x₀
L2  for n ← 0 to K − 1 do
L3      y ← H(x, ξₙ)                ▷ one noisy observation of h(x)
L4      x ← x − aₙ y
L5      x ← P(x)                    ▷ projection onto X, if X ≠ ℝ^d
L6  return x₀, …, x_K
```

The steps $a_n > 0$ are fixed in advance with $\sum_n a_n = \infty$ and $\sum_n a_n^2 < \infty$, for example $a_n = c/(n + n_0)$ or $a_n = c(n + 1)^{-\gamma}$ with $\frac{1}{2} < \gamma \le 1$. The projection is not part of the 1951 method; it keeps the iterates in a set where the assumptions hold.

## Example

Estimate the $0.25$-[quantile](/quantile/) of a uniform random variable $\xi$ on $[0, 1]$, so $x^* = 0.25$. The field is $h(x) = \Pr(\xi \le x) - 0.25$, and one observation is $Y = \mathbf{1}[\xi \le x] - 0.25$, which is $0.75$ or $-0.25$. No density or sorting is needed. Use $a_n = 1/(n + 2)$, $x_0 = 0.5$ and $X = [0, 1]$:

| $n$ | sample $\xi_n$ | $Y_n$ | $a_n$ | $x_{n+1}$ |
|---|---|---|---|---|
| 0 | 0.81 | −0.25 | 1/2 | 0.625 |
| 1 | 0.12 | 0.75 | 1/3 | 0.375 |
| 2 | 0.47 | −0.25 | 1/4 | 0.4375 |
| 3 | 0.09 | 0.75 | 1/5 | 0.2875 |
| 4 | 0.66 | −0.25 | 1/6 | 0.32917 |
| 5 | 0.33 | −0.25 | 1/7 | 0.36488 |
| 6 | 0.21 | 0.75 | 1/8 | 0.27113 |
| 7 | 0.95 | −0.25 | 1/9 | 0.29891 |

A sample below the current guess pushes the guess down by $0.75\,a_n$; a sample above pushes it up by $0.25\,a_n$. The two pushes balance on average exactly when a quarter of the samples fall below the guess. On $[0, 1]$ the field is $h(x) = x - 0.25$, so $\mu = 1$, $B = 0$ and $A = 0.75^2$.

## Correctness

Correctness means $\mathbb{E}\lVert x_n - x^*\rVert^2 \to 0$, at a rate when the steps are of order $1/n$. The proofs are below.

- **One step.** Unbiasedness turns the cross term into $\langle h(x_n), x_n - x^*\rangle \ge \mu\lVert x_n - x^*\rVert^2$, so $e_{n+1} \le (1 - 2\mu a_n + Ba_n^2)e_n + Aa_n^2$, where $e_n = \mathbb{E}\lVert x_n - x^*\rVert^2$.
- **Convergence.** If $\sum a_n = \infty$ and $\sum a_n^2 < \infty$, then $e_n \to 0$. The divergent sum drives the contraction, and the convergent sum of squares bounds the total injected noise.
- **Rate.** With $a_n = 2/(\mu(n + n_0))$ and $n_0 \ge \max(2, 2B/\mu^2)$, $e_n \le \max(n_0e_0, 4A/\mu^2)/(n + n_0)$.
- **Both conditions are needed.** With $\sum a_n < \infty$ the iterates can stop short of the root even without noise, and with a constant step the error tends to a positive limit, computed exactly for a rotation field.

## Complexity

Each step costs one observation and $O(d)$ arithmetic, with $\Theta(d)$ extra memory. By the rate theorem, $\mathbb{E}\lVert x_n - x^*\rVert^2 \le \varepsilon$ after $\lceil\max(n_0e_0, 4A/\mu^2)/\varepsilon\rceil$ steps. The $A/(\mu^2\varepsilon)$ term cannot be improved in general: for the mean of a distribution with variance $A$, even the sample mean, which is the best unbiased estimator for Gaussian data, has error $A/n$.

## Properties

- **Online and model free.** Only one observation per step is used, and no model of $h$ or of the noise is needed.
- **Not tied to gradients.** The field can be any monotone map, such as a rotation plus contraction, a Bellman operator residual or a quantile condition.
- **Almost sure convergence.** Under the weaker condition $\langle h(x), x - x^*\rangle > 0$ for $x \ne x^*$ and the same growth and step conditions, $x_n \to x^*$ with probability one (Blum 1954; Robbins and Siegmund 1971). The proof uses [martingale](/martingale/) convergence.
- **ODE limit.** For general fields, the iterates track the solutions of $\dot{x} = -h(x)$, and the limit points are stable equilibria of that ODE (Kushner and Yin 2003; Borkar 2008).
- **Sensitive to the constant.** For $a_n = c/n$, the $O(1/n)$ rate needs $c$ larger than $1/(2\mu)$; a smaller $c$ gives a slower power of $n$.

## Variants and improvements

- **Kiefer-Wolfowitz.** Replace the observation of $h$ with a finite difference of noisy function values, to find a maximum without gradients (Kiefer and Wolfowitz 1952).
- **Polyak-Ruppert averaging.** Use steps $a_n = cn^{-\gamma}$ with $\frac{1}{2} < \gamma < 1$ and return the average of the iterates. This gives the best asymptotic covariance without knowing $\mu$ (Polyak and Juditsky 1992).
- **Projected and truncated versions.** Project onto a set or restart when the iterates grow, so that the growth condition is needed only on a bounded set.
- **Two time scales.** Run two coupled iterations with steps of different orders, as in actor-critic methods (Borkar 2008).
- **Stochastic gradient descent.** The special case $H = \nabla f(x, \xi)$.

## When to use it

Use the Robbins-Monro scheme to find a root or an equilibrium of a function that you can only sample: online quantile and median tracking, dose finding, adaptive control, and the fixed points of reinforcement learning. When $h$ can be computed exactly, a deterministic root finder such as the [Newton-Raphson method](/newton-raphson-method/) or the [bisection method](/bisection-method/) is much faster.

## Pitfalls

- **Wrong step constant.** Steps $c/n$ with too small a $c$ converge at a slower power, and too large a $c$ makes the first steps overshoot. Use averaging or tune $c$.
- **Unbounded growth.** If $\lVert h(x)\rVert$ grows faster than linearly, the iterates can diverge with any step sequence. Project or truncate.
- **Correlated samples.** The theorems assume independent samples. Markov noise, as in reinforcement learning, needs extra mixing conditions.
- **Multiple roots.** Without a monotonicity condition the iteration can converge to any stable root of the ODE, and different runs can end at different roots.

## Implementations

## History

Robbins and Monro (1951) introduced the method to find the level at which a regression function attains a given value from noisy responses, and proved convergence in mean square. Kiefer and Wolfowitz (1952) extended it to locating a maximum with finite differences. Blum (1954) proved convergence with probability one, and Robbins and Siegmund (1971) gave the almost supermartingale theorem that is now the standard tool. Polyak and Juditsky (1992) showed that iterate averaging attains the optimal asymptotic rate. Kushner and Yin and Borkar developed the ODE method that covers most later uses in signal processing and reinforcement learning.

## References
