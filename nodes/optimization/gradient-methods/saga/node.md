---
tag: GYY34P
kind: algorithm
slug: saga
name: SAGA
aliases:
- SAGA method
- proximal SAGA
area: optimization/gradient-methods
level: advanced
summary: Variance-reduced method that stores the most recent gradient for each term instead of periodic full passes.
solves: [finite-sum-minimization]
model: real-ram
complexity:
  vars: {n: the number of component functions, d: the dimension, k: the number of iterations, κ: the condition number L/μ, δ: "the initial Lyapunov value |x0 - x*|^2 + 4 γ^2 n D0", ε: the target expected squared distance to the minimizer}
  time: {worst: O((n + k) d)}
  space: {extra: Θ(n d)}
  steps: {expected: "⌈max(6 κ, 2 n) ln(δ / ε)⌉"}
properties: {deterministic: false, exact: false, online: false, recursive: false}
history:
  year: 2014
  people: [Aaron Defazio, Francis Bach, Simon Lacoste-Julien]
  note: Defazio, Bach and Lacoste-Julien (2014) introduced SAGA, an unbiased version of SAG that supports proximal steps and adapts to strong convexity.
prereqs: [stochastic-gradient-descent, finite-sum-minimization, proximal-operator, strong-convexity]
see_also: [svrg, stochastic-gradient-descent, finite-sum-minimization, proximal-gradient-method, composite-minimization, lasso-regression, logistic-regression, coordinate-descent]
sources:
  - url: https://arxiv.org/abs/1407.0202
    title: Aaron Defazio, Francis Bach and Simon Lacoste-Julien, SAGA, A fast incremental gradient method with support for non-strongly convex composite objectives, NeurIPS 2014
    locator: Section 2 for the method and its relation to SAG and SVRG, Theorem 1 for the linear rate in the strongly convex case, Theorem 2 for the O(1/k) rate without strong convexity
  - paper: doi:10.1007/s10107-016-1030-6
    title: Mark Schmidt, Nicolas Le Roux and Francis Bach, Minimizing finite sums with the stochastic average gradient, Mathematical Programming 162, 2017
    locator: pages 83 to 112, the SAG method with a biased table average and its linear rate
  - paper: "Rie Johnson and Tong Zhang, Accelerating stochastic gradient descent using predictive variance reduction, Advances in Neural Information Processing Systems 26, 2013"
    locator: Section 2, the variance-reduced estimator with a snapshot, which SAGA replaces by a table
  - paper: doi:10.1137/140957639
    title: Julien Mairal, Incremental majorization-minimization optimization with application to large-scale machine learning, SIAM Journal on Optimization 25(2), 2015
    locator: Section 3, MISO, an incremental method with stored surrogate functions and a linear rate
  - paper: doi:10.1109/JPROC.2020.3028013
    title: Robert M. Gower, Mark Schmidt, Francis Bach and Peter Richtárik, Variance-reduced methods for machine learning, Proceedings of the IEEE 108(11), 2020
    locator: Section 3, SAGA and its Lyapunov analysis, and the memory saving for linear models
---

SAGA minimizes a [finite sum](/finite-sum-minimization/) $F(x) = \frac{1}{n}\sum_if_i(x)$, plus an optional nonsmooth term handled by its [proximal operator](/proximal-operator/), by keeping a table of the last gradient computed for each component. A step samples one component $j$ and moves along $\nabla f_j(x) - g_j + \bar{g}$, where $g_j$ is the stored gradient and $\bar{g}$ the table average; this estimate is unbiased, and its [variance](/variance/) vanishes at the solution. For smooth convex $f_i$ and a [strongly convex](/strong-convexity/) $F$, a constant step $1/(6L)$ gives linear convergence with $O((n + \kappa)\log(1/\varepsilon))$ component gradients. Defazio, Bach and Lacoste-Julien introduced it in 2014 as an unbiased form of SAG with support for [composite](/composite-minimization/) objectives.

## In plain words

The function is an average of many pieces. Taking the slope of one random piece is cheap but noisy.

SAGA remembers the last slope it saw for every piece. At each step it looks at one random piece again, and it uses the change in that piece's slope, added to the average of all remembered slopes. The remembered slopes act as a correction that cancels most of the noise. Then it saves the new slope in the table. As the method gets close to the answer, the remembered slopes become correct and the noise disappears, so the step size can stay constant.

## The problem

Minimize $F(x) + \psi(x)$ over $x \in \mathbb{R}^d$, where $F = \frac{1}{n}\sum_{i=1}^nf_i$, each $f_i$ is convex with an $L$-Lipschitz gradient, $F$ is $\mu$-strongly convex, $\kappa = L/\mu$, and $\psi$ is convex with a computable proximal map (for example $\lambda\lVert x\rVert_1$, or $0$). The method calls one $\nabla f_j$ per step.

## The algorithm

```pseudo id=main
SAGA(∇f₁..∇fₙ, prox, x₀, γ, K)
L1  x ← x₀;  gᵢ ← ∇fᵢ(x₀) for every i;  ḡ ← (1/n) Σᵢ gᵢ
L2  for k ← 0 to K − 1 do
L3      pick j uniformly from {1, …, n}
L4      u ← ∇fⱼ(x)
L5      v ← u − gⱼ + ḡ                  ▷ unbiased: E v = ∇F(x)
L6      ḡ ← ḡ + (u − gⱼ)/n;  gⱼ ← u     ▷ keep the table and its average
L7      x ← prox_γψ(x − γ v)
L8  return x₀, …, x_K
```

Line L6 keeps the invariant that $\bar{g}$ is the average of the table, and that each $g_i$ is $\nabla f_i$ at the point where component $i$ was last sampled. For a linear model $f_i(x) = \phi_i(\langle a_i, x\rangle)$, the gradient is $\phi_i'(\langle a_i, x\rangle)\,a_i$, so the table needs only the $n$ scalars $\phi_i'$, not $nd$ numbers.

## Example

Take $f_i(x) = \frac{c_i}{2}(x - b_i)^2$ with $c = (1, 2, 3)$ and $b = (0, 1, 5)$, so $L = 3$, $\mu = 2$ and $x^* = 17/6 \approx 2.8333$, with $\psi = 0$. Start at $x_0 = 0$ with the table $(0, -2, -15)$ and average $\bar{g} = -5.66667$, and use $\gamma = 1/(6L) = 1/18$ with a fixed index sequence:

| $k$ | $j$ | $x_k$ | $v$ | table after L6 | $\bar{g}$ after L6 | $x_{k+1}$ |
|---|---|---|---|---|---|---|
| 0 | 3 | 0 | −5.66667 | (0, −2, −15) | −5.66667 | 0.31481 |
| 1 | 1 | 0.31481 | −5.35185 | (0.31481, −2, −15) | −5.56173 | 0.61214 |
| 2 | 2 | 0.61214 | −4.33745 | (0.31481, −0.77572, −15) | −5.15364 | 0.85311 |
| 3 | 3 | 0.85311 | −2.59431 | (0.31481, −0.77572, −12.44067) | −4.30053 | 0.99724 |
| 4 | 2 | 0.99724 | −3.53033 | (0.31481, −0.00553, −12.44067) | −4.04379 | 1.19337 |
| 5 | 1 | 1.19337 | −3.16524 | (1.19337, −0.00553, −12.44067) | −3.75094 | 1.36921 |

At each row $\bar{g}$ equals the mean of the table, as the invariant says. The entry for component 3 is stale until it is sampled again; the correction $u - g_j$ uses exactly that staleness.

## Correctness

The proof below uses the Lyapunov function $\Psi_k = \lVert x_k - x^*\rVert^2 + 4\gamma^2nD_k$, where $D_k = \frac{1}{n}\sum_i\lVert g_i - \nabla f_i(x^*)\rVert^2$ measures how far the table is from the gradients at the solution.

- **Unbiased.** $\mathbb{E}v = \nabla F(x)$, because $\mathbb{E}g_j = \bar{g}$.
- **Variance.** For convex $L$-smooth $f_i$, $\mathbb{E}\lVert v - \nabla F(x^*)\rVert^2 \le 4LB(x) + 2D$, where $B(x) = F(x) - F(x^*) - \langle\nabla F(x^*), x - x^*\rangle$.
- **Distance and table.** One step shrinks the distance by $1 - \gamma\mu$ up to the terms in $B$ and $D$, and shrinks $D$ by $1 - 1/n$ up to a term $\frac{2L}{n}B(x)$.
- **Contraction.** For $\gamma \le 1/(6L)$ the $B$ terms cancel, and $\mathbb{E}\Psi_{k+1} \le (1 - \min(\gamma\mu, \frac{1}{2n}))\Psi_k$.

The proximal step is handled by its nonexpansiveness and the fixed point property $x^* = \operatorname{prox}_{\gamma\psi}(x^* - \gamma\nabla F(x^*))$.

## Complexity

The initial table costs $n$ component gradients. Each step then costs one component gradient, one proximal map and $O(d)$ arithmetic. With $\gamma = 1/(6L)$, $\mathbb{E}\lVert x_k - x^*\rVert^2 \le \varepsilon$ after $\lceil\max(6\kappa, 2n)\ln(\Psi_0/\varepsilon)\rceil$ steps, so the total is $O((n + \kappa)\log(1/\varepsilon))$, the same order as [SVRG](/svrg/). The table needs $\Theta(nd)$ memory in general and $\Theta(n)$ for linear models.

## Properties

- **One gradient per step.** SVRG needs two per inner step plus periodic full passes.
- **Adaptive to strong convexity.** The step $1/(6L)$ does not depend on $\mu$, and the rate adapts to it; without strong convexity SAGA still converges at the rate $O(1/k)$ (Defazio et al. 2014, Theorem 2).
- **Fixed point at the solution.** If $x = x^*$ and every $g_i = \nabla f_i(x^*)$, every step returns $x^*$.
- **Unbiased.** SAG uses $\frac{1}{n}(u - g_j) + \bar{g}$, which is biased; SAGA's estimate is unbiased, which makes the proximal extension and the proof simpler.
- **Memory.** $\Theta(nd)$ in general, which is the main cost.

## Variants and improvements

- **SAG.** Scale the correction by $1/n$; this is the earlier, biased method with a linear rate (Schmidt, Le Roux and Bach 2017).
- **MISO and Finito.** Store surrogate functions or points instead of gradients (Mairal 2015).
- **Non-uniform sampling.** Sample $j$ with probability proportional to $L_j$ and reweight, which replaces $\max_iL_i$ with the mean.
- **Mini-batches.** Update $b$ table entries per step.
- **Linear models.** Store one scalar per component, which makes SAGA practical for large logistic regression and [lasso](/lasso-regression/) problems.

## When to use it

Use SAGA for regularized linear models with many examples and a nonsmooth term, such as $\ell_1$-regularized [logistic regression](/logistic-regression/), where the table costs only $n$ scalars and the proximal step is cheap. Prefer [SVRG](/svrg/) when $nd$ numbers do not fit in memory. For deep networks, plain SGD with momentum is usually used instead.

## Pitfalls

- **Memory for general models.** A table of full gradients for a large model costs $n$ times the model size.
- **Initial table.** Initializing with zeros instead of $\nabla f_i(x_0)$ is valid but changes $D_0$ and the early behaviour; the invariant must still hold for the average.
- **Average drift.** Updating $\bar{g}$ incrementally for very many steps accumulates rounding error; recompute it from the table from time to time.
- **Step size.** The proof needs $\gamma \le 1/(6L)$; the paper's analysis uses $1/(3L)$. Larger steps can diverge.
- **Sparse gradients.** With sparse $a_i$, the dense term $\bar{g}$ makes every step dense unless the updates are delayed in a lazy way.

## Implementations

## History

Le Roux, Schmidt and Bach introduced SAG in 2012, the first incremental gradient method with a linear rate at the cost of one gradient per step, and the journal version appeared in 2017. Johnson and Zhang (2013) gave the snapshot form of variance reduction. Defazio, Bach and Lacoste-Julien (2014) combined the table of SAG with the unbiased correction of SVRG, which gave SAGA, and proved its rates for composite objectives. Mairal (2015) analysed the related MISO method.

## References
