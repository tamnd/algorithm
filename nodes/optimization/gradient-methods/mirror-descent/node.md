---
tag: 41N7NJ
kind: algorithm
slug: mirror-descent
name: Mirror descent
aliases:
- mirror descent method
- entropic mirror descent
- exponentiated gradient method
area: optimization/gradient-methods
level: advanced
summary: Gradient-type method that takes steps in a dual space defined by a mirror map, suited to simplex-like constraints.
solves: [convex-optimization-problem]
model: real-ram
complexity:
  vars: {n: the number of variables, k: the number of iterations, g: the cost of one subgradient of f, p: the cost of one mirror step with its Bregman projection, ε: "the target accuracy f(x̄_k) - f* ≤ ε", G: the bound on the dual norm of the subgradients, D: "a bound on the Bregman divergence from x_0 to a minimizer", σ: the strong convexity constant of the mirror map}
  time: {worst: O(k (g + p + n))}
  space: {extra: Θ(n)}
  steps: {worst: "⌈2 D G^2 / (σ ε^2)⌉"}
properties: {deterministic: true, exact: false, online: true, recursive: false}
history:
  year: 1983
  people: [Arkadi Nemirovski, David Yudin, Amir Beck, Marc Teboulle]
  note: Nemirovski and Yudin (1983) introduced mirror descent; Beck and Teboulle (2003) wrote it as a subgradient method with a Bregman divergence.
prereqs: [bregman-divergence, projected-gradient-descent, subgradient]
see_also: [multiplicative-weights-update, online-convex-optimization, regret, convex-conjugate, shannon-entropy, adagrad, natural-gradient-descent, first-order-lower-bound]
sources:
  - book: isbn:9780471103455
    title: A. S. Nemirovski and D. B. Yudin, Problem Complexity and Method Efficiency in Optimization, Wiley, 1983
    locator: Chapter 3, the mirror descent method for nonsmooth convex problems
  - paper: doi:10.1016/S0167-6377(02)00231-6
    title: Amir Beck and Marc Teboulle, Mirror descent and nonlinear projected subgradient methods for convex optimization, Operations Research Letters 31(3), 2003
    locator: pages 167 to 175, the Bregman form of the method, its rate, and the entropic version on the simplex
  - paper: doi:10.1561/2200000050
    title: Sébastien Bubeck, Convex Optimization, Algorithms and Complexity, Foundations and Trends in Machine Learning 8(3-4), 2015
    locator: Chapter 4, Sections 4.1 to 4.3 (mirror maps, mirror descent, and the standard setups)
  - book: isbn:9781611974980
    title: Amir Beck, First-Order Methods in Optimization, SIAM, 2017
    locator: Chapter 9 (mirror descent, its convergence, and the entropic version on the unit simplex)
  - paper: doi:10.1006/inco.1996.2612
    title: Jyrki Kivinen and Manfred K. Warmuth, Exponentiated gradient versus gradient descent for linear predictors, Information and Computation 132(1), 1997
    locator: pages 1 to 63, the exponentiated gradient update and its relative loss bounds
---

Mirror descent is a [subgradient](/subgradient/) method that measures distance with a [Bregman divergence](/bregman-divergence/) $D_\psi$ instead of the squared Euclidean distance. Each step maps the point to a dual space with $\nabla\psi$, takes the gradient step there, maps back, and projects onto the feasible set. With $\psi$ $\sigma$-strongly convex in a norm and subgradients bounded by $G$ in the dual norm, it reaches $f(\bar{x}_K) - f^* \le G\sqrt{2D/(\sigma K)}$. On the probability simplex with the entropy, the step is a multiplicative update and the rate depends on the dimension only through $\sqrt{\log n}$.

## In plain words

[Projected gradient descent](/projected-gradient-descent/) moves each coordinate by an amount proportional to its gradient, as if every direction were the same. On some sets that is the wrong picture. For probability vectors, a change from 0.001 to 0.002 doubles a weight, while a change from 0.5 to 0.501 hardly matters.

Mirror descent picks a way to measure distance that fits the set. On probability vectors it changes each weight by a factor: weights with a large gradient shrink, the others grow, and then all weights are scaled to sum to one. The method never leaves the set, and on large sets of this kind it needs far fewer steps.

## The problem

Minimize a convex function $f$ over a closed convex set $C \subseteq \mathbb{R}^n$. The method uses an oracle that returns a subgradient $g \in \partial f(x)$. It also uses a mirror map $\psi$, differentiable and $\sigma$-strongly convex on $C$ with respect to a norm $\lVert\cdot\rVert$, for which the step below is cheap. Notation: $\lVert\cdot\rVert_*$ is the dual norm, $\lVert g\rVert_* \le G$ for all subgradients that appear, $x^*$ is a minimizer, $D \ge D_\psi(x^*, x_0)$, and $\varepsilon$ is the target accuracy. Smoothness of $f$ is not needed.

## The algorithm

```pseudo id=main
MIRROR-DESCENT(∂f, ψ, x₀, η, K)
L1  x ← x₀                                 ▷ x₀ in C, where ∇ψ exists
L2  for k ← 0 to K − 1 do
L3      g ← a subgradient of f at x
L4      θ ← ∇ψ(x) − η_k g                  ▷ the gradient step in the dual space
L5      x ← argmin_{z ∈ C} D_ψ(z, ∇ψ*(θ))   ▷ back to the primal space, then a Bregman projection
L6  return the weighted average Σ η_k x_k / Σ η_k
```

Lines L4 and L5 together are $x_{k+1} = \operatorname{argmin}_{x \in C}\{\eta_k\langle g_k, x\rangle + D_\psi(x, x_k)\}$: a linear model of $f$ plus a penalty for moving away from $x_k$. Two standard choices:

| set | mirror map $\psi$ | norm, $\sigma$ | step | $D$ |
|---|---|---|---|---|
| any closed convex $C$ | $\frac{1}{2}\lVert x\rVert_2^2$ | $\lVert\cdot\rVert_2$, $1$ | $P_C(x - \eta g)$ | $\frac{1}{2}R^2$ |
| simplex $\Delta_n$ | $\sum_i x_i\log x_i$ | $\lVert\cdot\rVert_1$, $1$ | $x_i \leftarrow x_ie^{-\eta g_i}/Z$ | $\log n$ from the uniform $x_0$ |

The first row is the projected subgradient method. The second is the exponentiated gradient method of Kivinen and Warmuth (1997), the same update as [multiplicative weights](/multiplicative-weights-update/).

## Example

Minimize the linear function $f(x) = \langle c, x\rangle$ with $c = (0, 1, 2)$ over the simplex $\Delta_3$, so $f^* = 0$ at $e_1$. Use the entropy, $x_0 = (1/3, 1/3, 1/3)$, and $\eta = 0.5$. The gradient is always $c$, so $x_k \propto (1, e^{-k/2}, e^{-k})$. Here $G = \lVert c\rVert_\infty = 2$, $D_\psi(e_1, x_0) = \log 3$, and the bound of the theorem is $\sum_{j \le k}\eta f(x_j) \le \log 3 + (k+1)\eta^2G^2/2$.

| $k$ | $x_k$ | $f(x_k)$ | $\sum_{j \le k}\eta f(x_j)$ | bound |
|---|---|---|---|---|
| 0 | (0.3333, 0.3333, 0.3333) | 1.0000 | 0.5000 | 1.5986 |
| 1 | (0.5065, 0.3072, 0.1863) | 0.6798 | 0.8399 | 2.0986 |
| 2 | (0.6652, 0.2447, 0.0900) | 0.4248 | 1.0523 | 2.5986 |
| 3 | (0.7856, 0.1753, 0.0391) | 0.2535 | 1.1791 | 3.0986 |
| 4 | (0.8668, 0.1173, 0.0159) | 0.1491 | 1.2536 | 3.5986 |
| 5 | (0.9184, 0.0754, 0.0062) | 0.0878 | 1.2975 | 4.0986 |

All iterates stay strictly inside the simplex. The weight on the worst vertex shrinks by $e^{-1}$ in each step relative to the first one.

## Correctness

The proof has three steps. First, the optimality condition of the step in line L5, at a point $u \in C$, combined with the three-point identity of the Bregman divergence, gives $\eta_k\langle g_k, x_{k+1} - u\rangle \le D_\psi(u, x_k) - D_\psi(u, x_{k+1}) - D_\psi(x_{k+1}, x_k)$. Second, strong convexity bounds $D_\psi(x_{k+1}, x_k)$ below by $\frac{\sigma}{2}\lVert x_{k+1} - x_k\rVert^2$. This absorbs the term $\eta_k\langle g_k, x_k - x_{k+1}\rangle$ at a cost of $\eta_k^2G^2/(2\sigma)$, by the Fenchel-Young inequality for the squared norm. Third, the divergences telescope. The result is

$$\sum_{k<K}\eta_k\big(f(x_k) - f(u)\big) \le D_\psi(u, x_0) + \frac{G^2}{2\sigma}\sum_{k<K}\eta_k^2 \quad \text{for every } u \in C,$$

and Jensen's inequality moves the bound to the weighted average. The full proof is below.

## Complexity

Each iteration costs one subgradient, one mirror step and $O(n)$ vector work. The memory is $\Theta(n)$ for the iterate and the running average.

- **Rate.** The constant step $\eta = \sqrt{2\sigma D/(G^2K)}$ gives $f(\bar{x}_K) - f^* \le G\sqrt{2D/(\sigma K)}$, so $\lceil 2DG^2/(\sigma\varepsilon^2)\rceil$ iterations give accuracy $\varepsilon$. The steps $\eta_k \propto 1/\sqrt{k+1}$ give the same rate up to a factor of order $\log K$ without fixing $K$ in advance.
- **Simplex.** With the entropy, $f(\bar{x}_K) - f^* \le G_\infty\sqrt{2\log n/K}$, where $G_\infty$ bounds $\lVert g\rVert_\infty$. From the same uniform start, the guarantee of projected subgradient descent uses $\lVert g\rVert_2 \le \sqrt{n}\,G_\infty$ and $\lVert x_0 - x^*\rVert_2 < 1$, which gives only $G_\infty\sqrt{n/K}$. The entropy saves a factor of order $\sqrt{n/\log n}$.
- **Optimality.** For nonsmooth convex $f$ with bounded subgradients, the rate $O(1/\sqrt{K})$ cannot be improved by any first-order method when $K$ is at most of the order of $n$ (Nemirovski and Yudin 1983).

## Properties

- **Online.** The bound holds for every comparator $u$ and does not use that $f$ is the same at each step. With a different convex loss $f_k$ at each step it is a regret bound, which makes mirror descent a basic method of [online convex optimization](/online-convex-optimization/).
- **Anytime bound on the average.** The last iterate has no guarantee of the same form; the bound is for the weighted average or the best iterate.
- **No descent.** $f(x_k)$ can go up, as for any subgradient method.
- **Dual view.** Line L4 is a gradient step on $\theta = \nabla\psi(x)$. Without constraints and with a constant step, $\theta_K = \theta_0 - \eta\sum_k g_k$, which is the dual averaging form of the same method.

## Variants and improvements

- **Dual averaging.** Nesterov's dual averaging uses $\nabla\psi^*$ of the sum of all past gradients, instead of a recursive step. It has the same rate.
- **Stochastic mirror descent.** Replace $g_k$ by an unbiased estimate with $\mathbb{E}\lVert g_k\rVert_*^2 \le G^2$; the bound holds in expectation. This is the setting of robust [stochastic approximation](/stochastic-approximation/).
- **Smooth $f$.** If $f$ is smooth relative to $\psi$, a mirror step with the gradient gives the rate $O(1/K)$, the Bregman version of [proximal gradient](/proximal-gradient-method/).
- **Adaptive mirror maps.** [AdaGrad](/adagrad/) uses a mirror map $\frac{1}{2}x^\top H_kx$ that changes with $k$, built from the past gradients.
- **Natural gradient.** [Natural gradient descent](/natural-gradient-descent/) uses the Hessian of a divergence, in the form of the Fisher information, as a local metric.

## When to use it

Use mirror descent for nonsmooth convex problems over sets with a natural non-Euclidean geometry: probability vectors (mixture weights, zero-sum games, boosting, experts problems), and the $\ell_1$ ball or the spectraplex with a matching mirror map. For smooth problems over simple sets, an accelerated method such as [FISTA](/fista/) has a better rate. If the projection in line L5 has no closed form, the method loses its main advantage.

## Pitfalls

- **Iterates on the boundary.** The entropic step is defined only for positive weights. A start with $x_{0,i} = 0$ keeps that weight at zero forever. Start at the uniform point or at another positive point.
- **Overflow.** The product $\prod_j e^{-\eta g_{j,i}}$ can overflow or underflow. Work with $\theta = \log x$ and subtract the largest entry before the exponential.
- **The wrong norm for $G$.** For the entropy, $G$ bounds $\lVert g\rVert_\infty$, not $\lVert g\rVert_2$. A step tuned with the Euclidean norm of the gradient is too short by a factor of up to $\sqrt{n}$.
- **Reporting the last iterate.** The guarantee is for the weighted average or the best point found.

## Implementations

## History

Nemirovski and Yudin (1983) introduced mirror descent as a way to make the subgradient method fit the geometry of the set, and they proved that its rate is optimal for nonsmooth convex problems. Kivinen and Warmuth (1997) studied the exponentiated gradient update for linear prediction. Beck and Teboulle (2003) wrote mirror descent as a subgradient method with a Bregman divergence, which is the form used today, and analysed the entropic version on the simplex.

## References
