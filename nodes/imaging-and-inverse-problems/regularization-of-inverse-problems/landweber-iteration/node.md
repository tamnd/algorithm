---
tag: G6JZZF
kind: algorithm
slug: landweber-iteration
name: Landweber iteration
aliases:
- Landweber method
area: imaging-and-inverse-problems/regularization-of-inverse-problems
level: core
summary: Iterate x_{k+1} = x_k + omega A* (y - A x_k), a gradient descent on the residual whose iteration count acts as the regularization parameter.
solves: [fredholm-integral-equation-first-kind]
model: real-ram
complexity:
  vars: {m: "the number of data values", n: "the number of unknowns", a: "the cost of one product with A plus one product with A*", k: "the number of iterations"}
  time: {per_iteration: "O(a + m + n)", total: "O(k (a + m + n))", dense: "O(k m n)"}
  space: {extra: "O(m + n)"}
properties: {deterministic: true, iterative: true, matrix_free: true, linear_in_data: true, qualification: infinite, a_priori_stop: "k = (rho / delta)^(2 / (2 nu + 1)) / omega", discrepancy_stop: "O(delta^(-2 / (2 nu + 1)))"}
history:
  year: 1951
  people: [Louis Landweber]
  note: Landweber proposed the iteration for Fredholm integral equations of the first kind and proved that it converges for exact data.
prereqs: [gradient-descent, spectral-filter-factors, semi-convergence]
see_also: [cgls, richardson-iteration, morozov-discrepancy-principle, source-condition, qualification-of-regularization, sirt, tikhonov-regularization, iteratively-regularized-gauss-newton]
sources:
  - paper: "L. Landweber, An iteration formula for Fredholm integral equations of the first kind, American Journal of Mathematics 73(3), 1951, 615 to 624"
    locator: the iteration and its convergence for exact data
  - book: isbn:9780792341574
    title: Heinz W. Engl, Martin Hanke and Andreas Neubauer, Regularization of Inverse Problems, Kluwer, 1996
    locator: Chapter 6 (Landweber iteration as a regularization method, its rates and the discrepancy principle) and Chapter 11 (the nonlinear Landweber iteration)
  - book: isbn:9780898716962
    title: Per Christian Hansen, Discrete Inverse Problems, Insight and Algorithms, SIAM, 2010
    locator: Chapter 6 (iterative regularization, semi-convergence)
---

The Landweber iteration solves an ill-posed linear equation $A x = y$ from noisy data $y^\delta$ with $\|y^\delta - y\| \le \delta$. It starts at $x_0 = 0$ and repeats the step $x_{k+1} = x_k + \omega A^*(y^\delta - A x_k)$ with a fixed step $0 < \omega < 2/\|A\|^2$. Each step is one step of [gradient descent](/gradient-descent/) on $\frac12\|A x - y^\delta\|^2$, and costs one product with $A$ and one with the adjoint $A^*$. Run to the end, the iteration converges to the least squares solution of the noisy data, which is useless when $A$ is ill-conditioned. Stopped early, it is a regularization method: the iteration count $k$ plays the role of the parameter $1/\alpha$ of Tikhonov regularization. The usual stopping rule is the [discrepancy principle](/morozov-discrepancy-principle/), which stops at the first $k$ with $\|y^\delta - A x_k\| \le \tau\delta$.

## In plain words

The method guesses an answer, predicts the data from the guess, and moves the guess a small step in the direction that reduces the misfit. The first steps fix the large, well-measured features of the answer. Later steps fix finer and finer features, and these are exactly the features where the measurement noise is strongest. So the guess first gets better and then gets worse, as it starts to fit the noise. The method is stopped when the misfit is about as large as the noise. The number of steps is then the only tuning knob, and each step is cheap: it needs one simulation of the measurement and one of its reverse.

## The problem

Given a bounded linear operator $A: X \to Y$ between Hilbert spaces (an $m \times n$ matrix in the discrete setting), its adjoint $A^*$, data $y^\delta$ with $\|y^\delta - y\| \le \delta$ for exact data $y = A x^\dagger$, and the noise level $\delta$, find an approximation of the minimum norm solution $x^\dagger = A^\dagger y$ (see [pseudoinverse](/pseudoinverse/)) whose error tends to $0$ as $\delta \to 0$. The operator is only needed as two functions, $x \mapsto A x$ and $r \mapsto A^* r$.

## The algorithm

```pseudo id=main
LANDWEBER(A, y, ω, K, δ, τ)          ▷ 0 < ω < 2 / ‖A‖², τ > 1
L1  x ← 0
L2  for k ← 0 to K - 1 do
L3      r ← y - A x
L4      if ‖r‖ ≤ τ δ then return (x, k)
L5      x ← x + ω A* r
L6  return (x, K)
```

Line L1 starts at zero; a start $x_0 \ne 0$ makes the method converge to the solution nearest to $x_0$ instead. Line L3 computes the residual of the current iterate. Line L4 is the discrepancy principle: it returns the first iterate whose residual is at the noise level. Without a noise level the test is left out, and $K$ must be chosen in another way. Line L5 moves $x$ along $A^* r$, which is minus the gradient of $\frac12\|A x - y\|^2$. Line L6 returns after $K$ steps if the test never passed. The code also has a version for a dense matrix with the default step $\omega = 1/\|A\|_F^2$, which is safe because $\|A\| \le \|A\|_F$.

In terms of the singular system $(\sigma_j; v_j, u_j)$ of $A$, the iterate is a filtered expansion (see [spectral filter factors](/spectral-filter-factors/)):
$$x_k = \sum_j \big(1 - (1 - \omega\sigma_j^2)^k\big) \frac{\langle u_j, y^\delta\rangle}{\sigma_j} v_j.$$
The filter factor is near $1$ for components with $\omega\sigma_j^2 k \gg 1$ and near $\omega\sigma_j^2 k$ for the others. So $k$ acts like $1/(\omega\alpha)$ in Tikhonov regularization, where the filter is $\sigma^2/(\sigma^2 + \alpha)$.

## Example

**A trace.** Take $A = \mathrm{diag}(1, 0.1)$, $x^\dagger = (1, 1)$, so $y = (1, 0.1)$, and the noise $e = (0, 0.01)$, so $y^\delta = (1, 0.11)$ and $\delta = 0.01$. With $\omega = 1$ the first component is exact after one step, and the second is $x_{k,2} = 1.1\,(1 - 0.99^k)$. The discrepancy test uses $\tau = 1.5$, so $\tau\delta = 0.015$.

| $k$ | $x_k$ | $\|x_k - x^\dagger\|$ | $\|y^\delta - A x_k\|$ | L4 stops? |
|---|---|---|---|---|
| 0 | $(0, 0)$ | 1.41421 | 1.00603 | no |
| 1 | $(1, 0.01100)$ | 0.98900 | 0.10890 | no |
| 2 | $(1, 0.02189)$ | 0.97811 | 0.10781 | no |
| 3 | $(1, 0.03267)$ | 0.96733 | 0.10673 | no |
| 10 | $(1, 0.10518)$ | 0.89482 | 0.09948 | no |
| 100 | $(1, 0.69736)$ | 0.30264 | 0.04026 | no |
| 199 | $(1, 0.95113)$ | 0.04887 | 0.01489 | yes |
| 1000 | $(1, 1.09995)$ | 0.09995 | 0.00001 | |
| $\infty$ | $(1, 1.1)$ | 0.1 | 0 | |

At $k = 100$ the filter factor of the second component is $1 - 0.99^{100} = 0.63397$. Line L4 returns $k = 199$, because the residual at $k = 198$ is $0.11 \cdot 0.99^{198} = 0.01504 > 0.015$. Here the noise has the same sign as the signal, so the error has its minimum $0.0004$ near $k = 239$; in general the minimum is not known, and the discrepancy rule only guarantees the rate below.

**Rates on an integral operator.** For $(A x)(s) = \int_0^s x(t)\,dt$ on $L^2(0, 1)$ the singular values are $\sigma_j = 2/((2j - 1)\pi)$. The solution $x^\dagger(t) = 1 - t = A^* 1$ satisfies the [source condition](/source-condition/) with $\nu = \frac12$ and $\rho = 1$. The test of the code uses the first 200 singular components, $\omega = 1/\sigma_1^2$, $k = \lceil 1/\delta \rceil$, and puts the noise of size $\delta$ on the component that step $k$ amplifies most (a measurement):

| $\delta$ | $k$ | $\|x_k^\delta - x^\dagger\|$ | bound of Theorem 3 |
|---|---|---|---|
| $10^{-2}$ | 100 | 0.0986 | 0.202 |
| $10^{-3}$ | 1000 | 0.0315 | 0.0639 |
| $10^{-4}$ | 10000 | 0.0100 | 0.0202 |

The slopes of $\log$ error against $\log\delta$ are $0.496$ and $0.498$; the theory gives $2\nu/(2\nu + 1) = 0.5$. With the discrepancy rule and $\tau = 1.5$ instead, the same problem stopped at $k = 3$, $32$ and $205$ with errors $0.0509$, $0.0117$ and $0.00297$ (a measurement).

## Correctness

The proofs are in proofs/correctness.md, in exact arithmetic, with $x_0 = 0$.

- **Filter form (theorem).** By induction on $k$, $x_k$ is the filtered expansion above. The key step is that $A^*$ maps the part of $y$ outside the range of $A$ to $0$.
- **Exact data (theorem).** $x_k \to x^\dagger$ when $y$ is in the domain of $A^\dagger$, because $|1 - \omega\sigma^2| < 1$ for $0 < \sigma \le \|A\|$.
- **Monotone residual (theorem).** $\|y - A x_{k+1}\| \le \|y - A x_k\|$ for any data.
- **Error bound (theorem).** For $\omega\|A\|^2 \le 1$, the data error is at most $\sqrt{\omega k}\,\delta$. Under the source condition $x^\dagger = (A^* A)^\nu w$, $\|w\| \le \rho$, the total error is at most $(\nu/(\omega k))^\nu\rho + \sqrt{\omega k}\,\delta$. The choice $\omega k = (\rho/\delta)^{2/(2\nu+1)}$ gives $O(\rho^{1/(2\nu+1)}\delta^{2\nu/(2\nu+1)})$ for every $\nu > 0$, which is the best possible worst-case rate.
- **Termination (theorem).** If $y$ is in the range of $A$ and $\tau > 1$, line L4 passes after finitely many steps.

That the discrepancy principle also gives the rate $O(\delta^{2\nu/(2\nu+1)})$ for every $\nu > 0$ is a theorem of Engl, Hanke and Neubauer (Chapter 6); it is cited, not proved here.

## Complexity

- **Per iteration (real-ram).** Line L3 costs one product with $A$ and $m$ subtractions, line L4 a norm of length $m$, and line L5 one product with $A^*$ and $2n$ operations. That is $O(a + m + n)$, where $a$ is the cost of one product with $A$ plus one with $A^*$. For a dense matrix $a = O(m n)$; for a sparse projector, $a$ is proportional to the number of nonzeros.
- **Iterations.** The count depends on the noise and on the smoothness of $x^\dagger$, not on $m$ and $n$. The a priori choice of the corollary is $k = (\rho/\delta)^{2/(2\nu+1)}/\omega$, so $k$ grows like $\delta^{-2/(2\nu+1)}$. With the discrepancy principle, the stopping index is also $O(\delta^{-2/(2\nu+1)})$ (EHN Chapter 6). For $\nu = \frac12$ this is $k \sim \delta^{-1}$, as in the table above.
- **Total.** $O(k(a + m + n))$ time, and $O(m + n)$ extra space for $x$, $r$ and $A^* r$.

[CGLS](/cgls/) with the discrepancy principle stops after $O(\delta^{-1/(2\nu+1)})$ steps (a theorem, EHN Chapter 7), about the square root of the Landweber count. That square root is why Landweber is rarely the fastest choice.

## Properties

- **Infinite qualification.** The bias bound $(\nu/(\omega k))^\nu\rho$ (Lemma 2(c) of the proof) holds for every $\nu > 0$, so the rate does not saturate, unlike Tikhonov regularization at $\nu = 1$ (see [qualification of regularization](/qualification-of-regularization/)).
- **Linear in the data** for a fixed $k$. With the discrepancy rule, $k$ depends on the data and the map is not linear.
- **Monotone residual** and, for exact data, a monotone error $\|x_k - x^\dagger\|$. With noisy data the error shows [semi-convergence](/semi-convergence/): it decreases, then increases.
- **Matrix-free.** Only products with $A$ and $A^*$ are used. No matrix is formed or factored.
- **Smooth filter.** Its filter factors are near the Tikhonov factors with $\alpha = 1/(\omega k)$.

## Variants and improvements

- **Preconditioned and weighted forms.** $x_{k+1} = x_k + \omega M A^* D (y - A x_k)$ with diagonal weights $D$ and $M$. In tomography this is [SIRT](/sirt/), with the row and column sums of the projector as weights.
- **Projected Landweber.** Project onto a convex set (for example $x \ge 0$) after each step.
- **Accelerated methods.** The $\nu$-methods of Brakhage and Hanke and [CGLS](/cgls/) reach the same accuracy in about the square root of the number of steps (EHN Chapter 6 and 7).
- **Nonlinear Landweber.** For $y = F(x)$, use $x_{k+1} = x_k + \omega F'(x_k)^*(y^\delta - F(x_k))$ (EHN Chapter 11). The [iteratively regularized Gauss-Newton method](/iteratively-regularized-gauss-newton/) is a faster alternative.
- **Richardson iteration.** The same step on the normal equations $A^* A x = A^* y$ is the [Richardson iteration](/richardson-iteration/); Landweber is that iteration used as a regularization method.

## When to use it

Use Landweber when you have only a forward and an adjoint code, want the simplest possible method, and can afford many cheap steps. It is the reference method for the theory of iterative regularization, because its filter is explicit. It is a good choice inside nonlinear methods and with constraints such as nonnegativity, where Krylov methods are harder to use. When speed matters, use [CGLS](/cgls/) or [LSQR](/lsqr/): they need far fewer products with $A$ for the same error. For a small dense problem, [truncated SVD](/truncated-svd/) or [Tikhonov regularization](/tikhonov-regularization/) (which writes $\lambda$ for $\alpha$) with a direct solver is simpler.

## Pitfalls

- **Step too large.** With $\omega \ge 2/\|A\|^2$ at line L5, the component of the largest singular value grows and the iteration diverges. Estimate $\|A\|$ by a few steps of the power method on $A^* A$, or use $\omega = 1/\|A\|_F^2$ for a matrix.
- **No stopping rule.** Running the loop of line L2 to convergence fits the noise. The error goes up again after the best $k$ (see the trace). Keep the test of line L4, or choose $K$ from $\delta$.
- **$\tau \le 1$ at line L4.** If the data have a part outside the range of $A$, the residual tends to the norm of that part, which can be close to $\delta$, and the test may never pass. Use $\tau > 1$, for example $1.1$ to $2$.
- **A wrong adjoint at line L5.** If the code for $A^*$ is not the true adjoint of the code for $A$, the step is not a gradient step and the theory fails. Check $|\langle A x, r\rangle - \langle x, A^* r\rangle|$ on random vectors.
- **Reading the error from the residual.** The residual decreases at every step, even when the error has started to increase. A small residual does not mean a small error.

## Implementations

## History

Louis Landweber published the iteration in 1951 for Fredholm integral equations of the first kind and proved its convergence for exact data. Its role as a regularization method, with the iteration count as the parameter, the saturation-free rates under source conditions, and the discrepancy principle as a stopping rule, was worked out in the 1970s and 1980s and is summarized in Chapter 6 of Engl, Hanke and Neubauer (1996). SIRT in tomography is a weighted form of the same iteration.

## References
