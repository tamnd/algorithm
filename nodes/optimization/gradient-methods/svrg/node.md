---
tag: F7HP8J
kind: algorithm
slug: svrg
name: SVRG
aliases:
- stochastic variance reduced gradient
- stochastic variance-reduced gradient descent
area: optimization/gradient-methods
level: advanced
summary: Variance-reduced stochastic method that periodically computes a full gradient to correct stochastic updates.
solves: [finite-sum-minimization]
model: real-ram
complexity:
  vars: {n: the number of component functions, d: the dimension, s: the number of epochs, m: the number of inner steps per epoch, κ: the condition number L/μ, δ: the initial gap F(x0) - F*, ε: the target expected gap}
  time: {worst: O(s (n + m) d)}
  space: {extra: Θ(d)}
  steps: {expected: "⌈ln(δ / ε) / ln 2⌉ (n + 2 ⌈50 κ⌉)"}
properties: {deterministic: false, exact: false, online: false, recursive: false}
history:
  year: 2013
  people: [Rie Johnson, Tong Zhang]
  note: Johnson and Zhang (2013) introduced SVRG and proved its linear rate with O(d) memory; Zhang, Mahdavi and Jin (2013) proposed a closely related mixed gradient method in the same year.
prereqs: [stochastic-gradient-descent, finite-sum-minimization, strong-convexity, smoothness]
see_also: [saga, stochastic-gradient-descent, finite-sum-minimization, gradient-descent, ridge-regression, logistic-regression, proximal-gradient-method, variance]
sources:
  - paper: "Rie Johnson and Tong Zhang, Accelerating stochastic gradient descent using predictive variance reduction, Advances in Neural Information Processing Systems 26, 2013, pages 315 to 323"
    locator: Figure 1 for the procedure with Options I and II, Theorem 1 for the linear rate with α = 1/(μη(1 - 2Lη)m) + 2Lη/(1 - 2Lη)
  - url: https://arxiv.org/abs/1403.4699
    title: Lin Xiao and Tong Zhang, A proximal stochastic gradient method with progressive variance reduction, SIAM Journal on Optimization 24(4), 2014
    locator: Section 3, Prox-SVRG for composite objectives, and the rate with sampling proportional to L_i
  - url: https://arxiv.org/abs/1603.06160
    title: Sashank J. Reddi, Ahmed Hefny, Suvrit Sra, Barnabás Póczos and Alex Smola, Stochastic variance reduction for nonconvex optimization, ICML 2016
    locator: Section 4, SVRG for smooth nonconvex finite sums with O(n + n^(2/3) / ε) component gradients
  - url: https://arxiv.org/abs/1901.08689
    title: Dmitry Kovalev, Samuel Horváth and Peter Richtárik, Don't jump through hoops and remove those loops, SVRG and Katyusha are better without the outer loop, ALT 2020
    locator: Section 2, loopless SVRG with a random snapshot update and its linear rate
  - url: https://arxiv.org/abs/1603.05953
    title: Zeyuan Allen-Zhu, Katyusha, The first direct acceleration of stochastic gradient methods, Journal of Machine Learning Research 18(221), 2018
    locator: Theorem 2.1, accelerated SVRG with O((n + √(nκ)) log(1/ε)) component gradients
  - url: https://arxiv.org/abs/1812.04529
    title: Aaron Defazio and Léon Bottou, On the ineffectiveness of variance reduced optimization for deep learning, NeurIPS 2019
    locator: Sections 3 and 4, measurements showing little variance reduction for deep networks with data augmentation and batch normalization
  - paper: "Lijun Zhang, Mehrdad Mahdavi and Rong Jin, Linear convergence with condition number independent access of full gradients, Advances in Neural Information Processing Systems 26, 2013"
    locator: the epoch gradient method with one full gradient per epoch, close to SVRG
---

SVRG (stochastic variance reduced gradient) minimizes a [finite sum](/finite-sum-minimization/) $F(x) = \frac{1}{n}\sum_if_i(x)$ by running cheap [stochastic gradient](/stochastic-gradient-descent/) steps along $\nabla f_i(x) - \nabla f_i(\tilde{x}) + \nabla F(\tilde{x})$, where the full gradient at a snapshot $\tilde{x}$ is recomputed once per epoch. This estimate is unbiased, and its [variance](/variance/) goes to zero as $x$ and $\tilde{x}$ approach the minimizer, so a constant step gives linear convergence. For smooth convex $f_i$ and a [strongly convex](/strong-convexity/) $F$ with condition number $\kappa$, it needs $O((n + \kappa)\log(1/\varepsilon))$ component gradients, against $O(n\kappa\log(1/\varepsilon))$ for [gradient descent](/gradient-descent/), with only $O(d)$ extra memory. Johnson and Zhang introduced it in 2013.

## In plain words

Plain stochastic gradient steps use the slope of one random piece of the function. That slope is noisy, so the steps must shrink, and progress is slow near the end.

SVRG computes the exact slope at a reference point from time to time. At each cheap step it takes the slope of one random piece at the current point, subtracts the slope of the same piece at the reference point, and adds the exact slope at the reference point. When the current point is close to the reference point, the two random slopes almost cancel, and what is left is close to the exact slope. So the step can stay large.

## The problem

Minimize $F(x) = \frac{1}{n}\sum_{i=1}^nf_i(x)$ over $x \in \mathbb{R}^d$, given an oracle for each $\nabla f_i$. The rate assumes that each $f_i$ is convex with an $L$-Lipschitz gradient and that $F$ is $\mu$-strongly convex, with $\kappa = L/\mu$.

## The algorithm

```pseudo id=main
SVRG(∇f₁..∇fₙ, x₀, η, m, S)
L1   x̃ ← x₀
L2   for s ← 1 to S do
L3       μ̃ ← (1/n) Σᵢ ∇fᵢ(x̃)              ▷ full gradient at the snapshot, n calls
L4       x ← x̃
L5       for t ← 0 to m − 1 do
L6           pick i uniformly from {1, …, n}
L7           v ← ∇fᵢ(x) − ∇fᵢ(x̃) + μ̃       ▷ unbiased, small variance near x̃ and x*
L8           x ← x − η v
L9       x̃ ← one of the m inner points chosen uniformly (Option II), or the last x (Option I)
L10  return the snapshots x̃₀, …, x̃_S
```

The proof uses Option II. The parameters $\eta = 1/(10L)$ and $m = \lceil50\kappa\rceil$ give a contraction factor of $\frac{1}{2}$ per epoch. In practice $m = 2n$ and $\eta$ of order $1/L$ are common.

## Example

Take $n = 3$ components $f_i(x) = \frac{c_i}{2}(x - b_i)^2$ with $c = (1, 2, 3)$ and $b = (0, 1, 5)$. Then $F'(x) = 2(x - \frac{17}{6})$, so $x^* = 17/6 \approx 2.8333$, $\mu = 2$ and $L = 3$. At $x^*$ the component gradients are $2.8333$, $3.6667$ and $-6.5$, so a plain stochastic gradient has variance $21.24$ at the solution. The SVRG estimate is $v_i = c_i(x - \tilde{x}) + F'(\tilde{x})$, with variance $\frac{2}{3}(x - \tilde{x})^2$, which is zero at the snapshot.

One epoch from $\tilde{x} = 0$, with $\tilde{\mu} = F'(0) = -5.6667$, $\eta = 0.08$, $m = 6$, a fixed index sequence and Option I:

| $t$ | $i$ | $x_t$ | $v$ | variance of SVRG | variance of SGD | $F(x_t) - F^*$ |
|---|---|---|---|---|---|---|
| 0 | 3 | 0 | −5.66667 | 0 | 44.222 | 8.02778 |
| 1 | 1 | 0.45333 | −5.21333 | 0.13701 | 39.826 | 5.66440 |
| 2 | 2 | 0.87040 | −3.92587 | 0.50506 | 36.023 | 3.85311 |
| 3 | 3 | 1.18447 | −2.11326 | 0.93531 | 33.313 | 2.71875 |
| 4 | 2 | 1.35353 | −2.95961 | 1.22136 | 31.908 | 2.18982 |
| 5 | 1 | 1.59030 | −4.07637 | 1.68603 | 30.005 | 1.54514 |
| 6 | | 1.91641 | | | | 0.84075 |

The SVRG variance stays small inside the epoch, while the SGD variance stays above $30$ on this path and is still $21.24$ at $x^*$. The next epoch recomputes $\tilde{\mu}$ at $1.91641$.

## Correctness

The proof, given in full below, has four steps.

- **Unbiased.** Averaging over $i$ gives $\mathbb{E}v = \nabla F(x)$ exactly, because the two correction terms have the same mean.
- **Variance bound.** For convex $L$-smooth $f_i$, $\frac{1}{n}\sum_i\lVert\nabla f_i(x) - \nabla f_i(x^*)\rVert^2 \le 2L(F(x) - F^*)$, and so $\mathbb{E}\lVert v\rVert^2 \le 4L(F(x) - F^*) + 4L(F(\tilde{x}) - F^*)$.
- **One step.** $\mathbb{E}\lVert x_{t+1} - x^*\rVert^2 \le \lVert x_t - x^*\rVert^2 - 2\eta(1 - 2L\eta)(F(x_t) - F^*) + 4L\eta^2(F(\tilde{x}) - F^*)$.
- **One epoch.** Summing over the epoch and using $\lVert\tilde{x} - x^*\rVert^2 \le \frac{2}{\mu}(F(\tilde{x}) - F^*)$ gives $\mathbb{E}F(\tilde{x}_s) - F^* \le \alpha\,(F(\tilde{x}_{s-1}) - F^*)$ with $\alpha = \frac{1}{\mu\eta(1 - 2L\eta)m} + \frac{2L\eta}{1 - 2L\eta}$, which is at most $\frac{1}{2}$ for $\eta = 1/(10L)$ and $m \ge 50\kappa$.

## Complexity

An epoch costs $n$ component gradients for line L3 and $2m$ for the inner loop, each with $O(d)$ arithmetic. With $m = \lceil50\kappa\rceil$ the gap halves in expectation per epoch, so $\lceil\log_2(\delta/\varepsilon)\rceil$ epochs reach $\mathbb{E}F - F^* \le \varepsilon$, for a total of $O((n + \kappa)\log(\delta/\varepsilon))$ component gradients. The extra memory is $\Theta(d)$: the snapshot and its full gradient. This rate matches that of [SAGA](/saga/) and SAG, and it is within the factor $\sqrt{\kappa/n}$ (when $\kappa > n$) of the lower bound $(n + \sqrt{n\kappa})\log(1/\varepsilon)$ stated on the [finite-sum minimization](/finite-sum-minimization/) page.

## Properties

- **Constant step.** No decay is needed, unlike [stochastic gradient descent](/stochastic-gradient-descent/).
- **Fixed point at the solution.** If $x = \tilde{x} = x^*$, then $v = 0$ for every $i$, so the iterates stay at $x^*$.
- **Low memory.** Only $O(d)$ extra numbers, against $O(nd)$ for the gradient table of SAGA on general problems.
- **Two gradients per step.** Each inner step evaluates $\nabla f_i$ at two points, so it costs twice an SGD step.
- **Randomized.** The guarantee is in expectation; the full gradient pass is deterministic.

## Variants and improvements

- **Prox-SVRG.** Replace line L8 by a [proximal gradient](/proximal-gradient-method/) step to handle a nonsmooth term such as the $\ell_1$ norm, with sampling proportional to the $L_i$ (Xiao and Zhang 2014).
- **Loopless SVRG.** Drop the outer loop and refresh the snapshot with probability $1/n$ at each step (Kovalev, Horváth and Richtárik 2020).
- **Katyusha.** Add a negative momentum term that pulls toward the snapshot, which gives the optimal $(n + \sqrt{n\kappa})\log(1/\varepsilon)$ cost (Allen-Zhu 2018).
- **Nonconvex SVRG.** For smooth nonconvex sums, $O(n + n^{2/3}/\varepsilon)$ component gradients give $\mathbb{E}\lVert\nabla F\rVert^2 \le \varepsilon$ (Reddi et al. 2016).
- **Mini-batches.** Average $b$ component corrections in line L7, which lowers the variance and suits parallel hardware.

## When to use it

Use SVRG for strongly convex or well-conditioned finite sums of moderate size where high accuracy matters, such as regularized logistic or [ridge regression](/ridge-regression/), especially when a gradient table of size $nd$ does not fit in memory. For linear models where the table needs only $n$ scalars, [SAGA](/saga/) is often simpler. For deep networks the measured variance reduction is small and SVRG is rarely better than SGD with momentum (Defazio and Bottou 2019).

## Pitfalls

- **Option I without proof.** The common last-iterate version works in practice, but the proof here covers only the random snapshot.
- **Step size.** The proof needs $\eta < 1/(2L)$. Too large a step diverges just as for gradient descent.
- **Snapshot too stale or too fresh.** The bound on $\alpha$ improves with $m$ only through the term $1/m$, while each epoch of length $m$ costs $n + 2m$. A very long epoch wastes steps, and a very short one spends most of the cost on full gradients; $m$ between $n$ and a few times $n$ is the usual compromise.
- **Data augmentation and batch normalization.** These change $f_i$ between the snapshot and the inner steps, which breaks the cancellation (Defazio and Bottou 2019).
- **Nonconvex components.** Lemma 2 needs each $f_i$ convex; for nonconvex $f_i$ use the nonconvex analysis and its smaller steps.

## Implementations

## History

Johnson and Zhang (2013) introduced SVRG with the predictive variance reduction step and proved the linear rate for Option II. In the same year Zhang, Mahdavi and Jin proposed a closely related method, and SAG (Schmidt, Le Roux and Bach) had already shown that linear rates are possible with a stored table. Xiao and Zhang (2014) extended SVRG to composite problems. Allen-Zhu (2018) accelerated it with Katyusha, and Reddi et al. (2016) analysed it for nonconvex problems.

## References
