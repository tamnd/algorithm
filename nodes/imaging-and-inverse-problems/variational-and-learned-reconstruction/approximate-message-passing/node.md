---
tag: SKJZMH
kind: algorithm
slug: approximate-message-passing
name: Approximate message passing
aliases:
- AMP
area: imaging-and-inverse-problems/variational-and-learned-reconstruction
level: research
summary: Iterative soft thresholding plus an Onsager correction term in the residual, which makes the error Gaussian for random matrices so that a scalar recursion, state evolution, predicts it.
solves: [sparse-signal-recovery]
model: real-ram
complexity:
  vars: {K: the number of iterations, m: the number of measurements, n: the length of the signal}
  time: {worst: O(K m n)}
  space: {extra: O(m + n)}
properties: {deterministic: true, iterative: true, matrix_free: true, guarantee: "Gaussian matrices in the large system limit"}
history:
  year: 2009
  people: [David L. Donoho, Arian Maleki, Andrea Montanari]
  note: Donoho, Maleki and Montanari derived AMP from belief propagation in 2009 and showed that its phase transition matches that of l1 minimization. Bayati and Montanari proved state evolution for Gaussian matrices in 2011.
prereqs: [iterative-shrinkage-thresholding, lasso-regression, compressed-sensing]
see_also: [belief-propagation, donoho-tanner-phase-transition, iterative-hard-thresholding, cosamp, basis-pursuit, orthogonal-matching-pursuit, lista, proximal-operator]
sources:
  - paper: doi:10.1073/pnas.0909892106
    title: David L. Donoho, Arian Maleki and Andrea Montanari, Message-passing algorithms for compressed sensing, Proceedings of the National Academy of Sciences 106(45), 2009
    locator: pages 18914 to 18919 (the iteration with the correction term, state evolution and the phase transition)
  - paper: doi:10.1109/TIT.2010.2094817
    title: Mohsen Bayati and Andrea Montanari, The dynamics of message passing on dense graphs, with applications to compressed sensing, IEEE Transactions on Information Theory 57(2), 2011
    locator: pages 764 to 785 (the state evolution theorem for Gaussian matrices)
---

Approximate message passing (AMP) recovers a sparse vector $x \in \mathbb{R}^n$ from $y = Ax + w$ with a random $m \times n$ matrix $A$. Each step looks like a step of [iterative shrinkage-thresholding](/iterative-shrinkage-thresholding/): it applies soft thresholding $\eta$ to $x^t + A^Tz^t$. The difference is the residual: AMP adds the Onsager correction $\frac{\|x^{t+1}\|_0}{m}z^t$ to $y - Ax^{t+1}$. For a matrix with i.i.d. Gaussian entries, this term makes the error in $x^t + A^Tz^t$ behave like Gaussian noise of a known variance $\tau_t^2$ in the large system limit. A scalar recursion, state evolution, then predicts the mean squared error of every iteration. Like ISTA, the fixed points of AMP solve a [LASSO](/lasso-regression/) problem, but AMP reaches them in far fewer iterations. With a well chosen threshold, its phase transition for noiseless recovery is the same as that of [basis pursuit](/basis-pursuit/), the [Donoho-Tanner phase transition](/donoho-tanner-phase-transition/). Greedy methods such as [iterative hard thresholding](/iterative-hard-thresholding/) and [CoSaMP](/cosamp/) have worst case guarantees for every matrix with a small restricted isometry constant; the theory of AMP is instead exact, but for Gaussian matrices and in the limit $n \to \infty$.

## The problem

Given $A$, $y$ and a threshold parameter, find an estimate of a sparse $x$, where $y = Ax + w$, $A$ has i.i.d. entries of mean 0 and variance $1/m$, and $w$ is noise of variance $\sigma^2$ per entry. Write $\delta = m/n$ for the undersampling ratio. The output is the estimate $x^K$, and with it the estimate $\tau_K = \|z^K\|/\sqrt m$ of the effective noise level. The column scaling matters: the theory assumes columns of norm close to 1.

## The algorithm

$\eta(v; \theta) = \operatorname{sign}(v)\max(|v| - \theta, 0)$ is soft thresholding, the [proximal operator](/proximal-operator/) of $\theta|\cdot|$, applied entry by entry.

```pseudo id=main
AMP(A, y, α, K)
L1  x ← 0, z ← y
L2  for t = 0 to K - 1
L3      τ ← ‖z‖ / √m                    ▷ estimate of the effective noise level
L4      θ ← α τ                         ▷ threshold proportional to the noise level
L5      x_new ← η(x + Aᵀ z; θ)          ▷ soft thresholding, as in ISTA
L6      b ← ‖x_new‖₀ / m                ▷ Onsager coefficient
L7      z ← y - A x_new + b z, x ← x_new ▷ residual with the correction term
L8  return x, z
```

Line L6 is the average derivative of $\eta$ divided by $\delta$: $\eta'$ is 1 where the input passes the threshold and 0 elsewhere, so $\frac1\delta\langle\eta'\rangle = \|x^{t+1}\|_0/m$. Without the term $b z$ in line L7, the loop is iterative soft thresholding with unit step and a varying threshold. The threshold rule $\theta_t = \alpha\tau_t$ is the one of Donoho, Maleki and Montanari. A fixed $\theta$ also works in the theory, but in practice it can make the loop diverge (see Pitfalls).

## Example

Take $\delta = m/n = 1/2$, no noise, and a signal whose entries are 0 with probability 0.9 and $+1$ or $-1$ with probability 0.05 each. Use $\alpha = 1.5$. State evolution starts with $\tau_0^2 = E[X^2]/\delta = 0.1/0.5 = 0.2$, because the first step sees $A^Ty = x + (A^TA - I)x$, whose error has variance $\|x\|^2/m$ per entry. Each later step sets $\tau_{t+1}^2 = \frac1\delta E[(\eta(X + \tau_tZ; \alpha\tau_t) - X)^2]$ with a standard normal $Z$.

The table compares the predicted mean squared error per entry of $x^{t+1}$ with the average over two runs with $n = 400$, $m = 200$ (seeds 10 and 11 of the test file), with and without the correction term. The run values are measurements.

| $t$ | $\tau_t^2$ | predicted MSE | AMP, measured | without correction, measured |
|---|---|---|---|---|
| 0 | 0.2000 | 0.0586 | 0.0675 | 0.0675 |
| 1 | 0.1171 | 0.0402 | 0.0482 | 0.0756 |
| 2 | 0.0803 | 0.0289 | 0.0334 | 0.0687 |
| 3 | 0.0579 | 0.0211 | 0.0230 | 0.0859 |
| 4 | 0.0422 | 0.0155 | 0.0161 | 0.0911 |
| 5 | 0.0309 | 0.0113 | 0.0113 | 0.1132 |

The first step is the same for both, since $z^0 = y$. After that, AMP follows the prediction and its error falls by a roughly constant factor per step. Without the correction the error grows. The gap at $t = 0$ comes from the finite size: the number of nonzero entries of $x$ itself varies by about 15 percent at $n = 400$.

## Correctness

The full proof is in [proofs/correctness.md](proofs/correctness.md). It proves two facts that hold for every matrix:

- The correction coefficient $\|x^{t+1}\|_0/m$ equals $\frac1\delta\langle\eta'(x^t + A^Tz^t; \theta_t)\rangle$, the form in the paper.
- If $(x, z)$ is a fixed point with threshold $\theta$ and $k = \|x\|_0 < m$, then $x$ minimizes $\tfrac12\|y - Ax\|^2 + \lambda\|x\|_1$ with $\lambda = \theta(1 - k/m)$. The $z$ equation gives $(1 - k/m)z = y - Ax$, and the fixed point of soft thresholding says that $A^Tz$ is $\theta$ times a subgradient of $\|x\|_1$. Multiplying by $1 - k/m$ gives the optimality condition of the LASSO.

The statement that the error follows state evolution is a theorem of Bayati and Montanari (2011): for i.i.d. Gaussian $A$, $n \to \infty$ with $m/n \to \delta$ and a fixed number of iterations, the empirical distribution of the pairs $(x^{t+1}_i, x_i)$ converges to that of $(\eta(X + \tau_tZ; \theta_t), X)$. It is cited, not proved here. The theorem says nothing about one finite matrix, and nothing about non-Gaussian matrices.

## Complexity

Each iteration costs one product with $A$ and one with $A^T$, which is $O(mn)$ for a dense matrix, and $O(n)$ for the threshold and the counts. So $K$ iterations cost $O(Kmn)$ time and $O(m + n)$ extra memory, the same as ISTA. With a fast operator the products are cheaper, but the theory then no longer applies directly. Under state evolution with a fixed point $\tau^* = 0$ (noiseless recovery below the phase transition), the error decreases geometrically, so the number of iterations for accuracy $\varepsilon$ is $O(\log(1/\varepsilon))$ in the large system limit. ISTA on the same problems is much slower.

## Properties

- Each step is as cheap as a step of ISTA, and the only extra work is the count in line L6.
- The effective observation $x^t + A^Tz^t$ is close to $x + \tau_tZ$ with Gaussian $Z$, so each step is a scalar denoising problem. This is why the threshold can be set from $\tau_t$, and why other denoisers can replace $\eta$.
- Fixed points are LASSO solutions, and the map from $\alpha$ to the LASSO weight $\lambda$ is given by the fixed point of state evolution.
- The predictions are exact only in the large system limit and only for i.i.d. Gaussian matrices (and, by later work, other i.i.d. sub-Gaussian matrices). For structured or ill-conditioned matrices AMP can diverge.
- It is not a descent method. The LASSO objective need not decrease at every step.

## Variants and improvements

- Bayes-optimal AMP replaces $\eta$ by the posterior mean of $X$ given $X + \tau Z = v$ for a known prior, with the correction coefficient the average derivative of that denoiser. Its state evolution predicts the minimum mean squared error in the regimes where AMP reaches it.
- Generalized AMP (GAMP, Rangan) handles nonlinear and non-Gaussian measurement channels, such as quantized or Poisson data.
- Denoising AMP uses an image denoiser in place of $\eta$, with the derivative estimated by a Monte Carlo trace estimate. It is close in spirit to plug-and-play methods.
- Vector AMP and orthogonal AMP extend the theory to right rotationally invariant matrices, which include many ill-conditioned ones, at the cost of a linear solve or an SVD per step.
- Damping, which averages the new and the old iterate, is a common heuristic fix for divergence on matrices that are not i.i.d. It has no general guarantee.
- [LISTA](/lista/) and learned AMP unroll a fixed number of iterations and train the matrices and thresholds.

## When to use it

Use AMP when the matrix is random with i.i.d. entries, or close to it, and the problem is large: it then reaches the LASSO solution or a Bayes-optimal estimate in tens of iterations, and state evolution predicts the error in advance, which helps to choose $\alpha$ or the number of measurements. For partial Fourier or other structured matrices from imaging, use vector AMP, damping, or a convex solver such as [FISTA](/fista/) or ADMM instead. When a worst case guarantee for one given matrix is needed, use methods with restricted isometry guarantees, such as [CoSaMP](/cosamp/) or [basis pursuit](/basis-pursuit/).

## Pitfalls

- AMP diverges on many matrices that are not i.i.d. Gaussian, for example ill-conditioned matrices, matrices with nonzero mean entries and some structured transforms. Check the residual and stop if it grows.
- The columns must have norm close to 1, which means entries of variance $1/m$. With another scale, the effective noise is wrong and the threshold rule fails.
- A fixed small threshold can drive the number of nonzeros up to $m$. Then the coefficient $\|x\|_0/m$ reaches 1 and $z$ blows up. In 10 runs on random Gaussian $32 \times 64$ matrices with $\theta = 0.1$ and about 10 nonzeros, all 64 entries became nonzero and $\|z\|$ passed $10^{28}$ within 200 iterations in every run. The adaptive rule $\theta_t = \alpha\tau_t$ avoids it in practice.
- State evolution predicts averages over the entries in the large system limit. At small $n$ the agreement is rough, as the example shows.
- Dropping the correction term gives a different algorithm with a different error. Do not compare "AMP" runs where the term is missing or uses the wrong count.

## Implementations

## History

The correction term has its origin in statistical physics: it is the Onsager reaction term of the Thouless-Anderson-Palmer equations for spin glasses (1977). Similar iterations appeared for CDMA multiuser detection, for example in the work of Kabashima (2003). Donoho, Maleki and Montanari (2009) derived AMP for compressed sensing from belief propagation on the dense bipartite graph of $A$, by keeping only the leading terms of the messages. They introduced state evolution as a prediction of its error and showed that, with the threshold tuned to the sparsity, the phase transition of AMP matches the Donoho-Tanner transition of $\ell_1$ minimization. Bayati and Montanari (2011) proved state evolution for Gaussian matrices. Later work extended the method to general priors, nonlinear channels and rotationally invariant matrices, and used it to compute the asymptotic risk of the LASSO.

## References
