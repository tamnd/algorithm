---
tag: NEQJ8H
kind: algorithm
slug: sparse-polynomial-chaos
name: Sparse polynomial chaos by compressive sampling
aliases:
- compressive sensing polynomial chaos
- l1-minimization polynomial chaos
area: scientific-computing/uncertainty-quantification
level: research
summary: Recovers a polynomial chaos expansion with few large coefficients from fewer runs than terms by l1 minimization.
solves: [forward-uncertainty-propagation]
model: real-ram
complexity:
  vars: {d: "the number of inputs", P: "the number of chaos terms", N: "the number of model runs (N can be less than P)", K: "the number of ISTA iterations", C: "the cost of one model run"}
  time: {worst: O(N C + (K + d) N P + N^3)}
  space: {extra: O(N P)}
properties: {deterministic: false, intrusive: false, exact: false}
history:
  year: 2011
  people: [Alireza Doostan, Houman Owhadi, Geraud Blatman, Bruno Sudret, Holger Rauhut, Rachel Ward]
  note: Doostan and Owhadi brought compressive sampling to polynomial chaos in 2011, and in the same year Blatman and Sudret built sparse expansions by least angle regression. Rauhut and Ward proved recovery guarantees for sparse Legendre expansions in 2012.
prereqs: [regression-polynomial-chaos, compressed-sensing, proximal-gradient-method]
see_also: [basis-pursuit, iterative-shrinkage-thresholding, orthogonal-matching-pursuit, restricted-isometry-property, sparse-signal-recovery, cross-validation, power-iteration, sobol-indices]
sources:
  - paper: doi:10.1016/j.jcp.2011.01.002
    title: Alireza Doostan and Houman Owhadi, A non-adapted sparse approximation of PDEs with stochastic inputs, Journal of Computational Physics 230(8), 2011, 3015-3034
    locator: the recovery of sparse chaos coefficients of PDE solutions by l1 minimization from fewer random samples than basis functions
  - paper: doi:10.1016/j.jat.2012.01.008
    title: Holger Rauhut and Rachel Ward, Sparse Legendre expansions via l1-minimization, Journal of Approximation Theory 164(5), 2012, 517-533
    locator: the recovery guarantee for sparse Legendre expansions from random samples of the Chebyshev law with a preconditioned system
  - paper: doi:10.1137/080716542
    title: Amir Beck and Marc Teboulle, A fast iterative shrinkage-thresholding algorithm for linear inverse problems, SIAM Journal on Imaging Sciences 2(1), 2009, 183-202
    locator: Theorem 3.1 (the O(1/k) rate of ISTA with a constant step) and Theorem 4.4 (the O(1/k^2) rate of FISTA)
  - paper: doi:10.1016/j.jcp.2010.12.021
    title: Geraud Blatman and Bruno Sudret, Adaptive sparse polynomial chaos expansion based on least angle regression, Journal of Computational Physics 230(6), 2011, 2345-2367
    locator: the sparse chaos expansion by least angle regression with the basis chosen by the leave-one-out error
---

Sparse polynomial chaos finds a [polynomial chaos expansion](/polynomial-chaos-expansion/) from fewer model runs than the expansion has terms. It uses the fact that the expansion of many outputs has only a few large coefficients. Ordinary [least squares](/regression-polynomial-chaos/) needs at least as many runs $N$ as terms $P$, but when $N < P$ the linear system $A c = y$ has many solutions. The method picks the one with the smallest $\ell_1$ norm, as in [compressed sensing](/compressed-sensing/), because the $\ell_1$ norm favors vectors with few nonzero entries. This page solves the penalized form, the LASSO, by the iterative shrinkage-thresholding algorithm (ISTA), and then refits the coefficients it keeps by least squares. In the example below, 25 random runs recover exactly a five term polynomial in five inputs, out of 56 candidate terms.

## In plain words

You want a polynomial formula for a slow model, but the formula has more unknown weights than you can afford runs. Usually that is hopeless: too few equations for the unknowns. But if most of the weights are really zero, there is hope, because you only have to find the few that are not. The trick is to ask for the solution that fits the runs and has the smallest sum of absolute weights. That choice tends to set most weights exactly to zero. A simple loop finds it: take a small step that improves the fit, then pull every weight toward zero by a fixed amount, and set it to zero if it crosses. At the end, fit the surviving weights again by plain least squares to undo the pull.

## The problem

The input $\xi = (\xi_1, \ldots, \xi_d)$ has independent components with laws $\rho_k$, the output is $Q = q(\xi)$, and $\Psi_\alpha$, $\alpha \in \Lambda$, is the orthonormal chaos basis of total degree $p$, with $P = |\Lambda|$ terms. Given $N$ runs $y_i = q(x_i)$ at points drawn from the input law, possibly with $N < P$, find coefficients $c$ with few nonzero entries such that $\sum_\alpha c_\alpha \Psi_\alpha$ fits the runs. With the scaled design matrix $A[i, \alpha] = \Psi_\alpha(x_i) / \sqrt{N}$ and the scaled outputs $y_i / \sqrt{N}$, the convex problem is

$$\min_{c \in \mathbb{R}^P} F(c) = \tfrac{1}{2} \|A c - y\|^2 + \lambda \|c\|_1, \qquad \lambda > 0.$$

The scaling makes $\mathbb{E}[A^{\mathsf T} A] = I$, so $\lambda$ has the same meaning for every $N$.

## The algorithm

```pseudo id=main
SPARSE-PCE(q, ρ, p, N, λ, K)
L1  Λ ← all α ∈ ℕ^d with |α| ≤ p;  draw x_1, ..., x_N from ρ      ▷ N may be smaller than P
L2  y_i ← q(x_i) / √N;  A[i, α] ← Ψ_α(x_i) / √N                   ▷ N model runs
L3  L ← ‖A‖_2^2 by power iteration;  c ← 0
L4  repeat K times:  c ← S_{λ/L}(c - (1/L) A^T (A c - y))           ▷ ISTA step
L5  S ← {α : c_α ≠ 0}
L6  if |S| < N:  c ← least-squares fit of y on the columns S of A    ▷ debias
L7  return c
```

Lines L1 and L2 draw the points and run the model, as in regression. Line L3 bounds the Lipschitz constant $L$ of the gradient $A^{\mathsf T} (A c - y)$ by the largest eigenvalue of $A^{\mathsf T} A$; the reference code runs 200 steps of [power iteration](/power-iteration/) and adds 1 percent, so the step $1/L$ is safe. Line L4 is the [proximal gradient](/proximal-gradient-method/) step of [ISTA](/iterative-shrinkage-thresholding/): a gradient step on the smooth part, then the soft threshold $S_\tau(t) = \operatorname{sign}(t) \max(|t| - \tau, 0)$ in each entry, which is the proximal map of $\tau |t|$. Entries that the gradient step leaves smaller than $\lambda / L$ become exactly zero. The reference code takes $\lambda$ as a fraction of $\|A^{\mathsf T} y\|_\infty$, because for $\lambda \ge \|A^{\mathsf T} y\|_\infty$ the solution is $c = 0$. Line L5 reads the support. Line L6 refits on the support without the penalty, which removes the shrinkage of every kept coefficient by about $\lambda$.

## Example

**Exact recovery.** Take $d = 5$ uniform inputs, total degree $p = 3$, so $P = 56$, and a true expansion with the constant 1 and four other nonzero coefficients of size between 0.5 and 1.5 at random positions. The run uses $\lambda = 0.01 \|A^{\mathsf T} y\|_\infty$ and $K = 2000$. A trial counts as recovered if every coefficient is within $10^{-8}$ of the truth. This is a measurement over 20 seeds.

| runs $N$ | $N/P$ | recovered |
|---|---|---|
| 10 | 0.18 | 0 of 20 |
| 12 | 0.21 | 1 of 20 |
| 14 | 0.25 | 2 of 20 |
| 16 | 0.29 | 2 of 20 |
| 18 | 0.32 | 12 of 20 |
| 20 | 0.36 | 18 of 20 |
| 25 | 0.45 | 20 of 20 |

Least squares cannot even start below 56 runs. The sharp change from failure to success is typical of compressed sensing.

**The Ishigami function.** $Q = \sin x_1 + 7 \sin^2 x_2 + 0.1\, x_3^4 \sin x_1$ with $x_k = \pi \xi_k$, $\xi_k$ uniform on $[-1, 1]$, has mean 3.5 and variance 13.84459. The basis is Legendre of total degree 8, so $P = 165$, with $\lambda = 0.01 \|A^{\mathsf T} y\|_\infty$ and $K = 1500$. The validation error is the mean squared error on 1000 fresh points divided by the variance. This is a measurement over seeds 0 to 4.

| $N$ | kept terms | mean, range | median validation error |
|---|---|---|---|
| 50 | 33 to 49 | 3.476 to 3.632 | $6.3 \times 10^{-2}$ |
| 75 | 18 to 44 | 3.471 to 3.510 | $1.1 \times 10^{-3}$ |
| 100 | 15 to 27 | 3.489 to 3.510 | $5.2 \times 10^{-4}$ |
| 150 | 13 to 21 | 3.489 to 3.507 | $4.5 \times 10^{-4}$ |

With 100 runs the error is below that of [least squares](/regression-polynomial-chaos/) on the same basis with 495 runs (median $1.5 \times 10^{-3}$), because the fit keeps only about 20 terms. The error stops falling near $4 \times 10^{-4}$, the error of a sparse expansion of degree 8.

## Correctness

The objective $F$ is convex, and a minimizer exists because $F(c) \ge \lambda \|c\|_1 \to \infty$. ISTA is the proximal gradient method for $F$. With the step $1/L$ and $L \ge \|A\|_2^2$, each step does not increase $F$, and Beck and Teboulle proved (their Theorem 3.1) that $F(c_k) - F(c^*) \le L \|c_0 - c^*\|^2 / (2k)$ for every minimizer $c^*$. A fixed point of the step is exactly a point that satisfies the optimality conditions: $(A^{\mathsf T}(y - A c))_\alpha = \lambda \operatorname{sign}(c_\alpha)$ where $c_\alpha \ne 0$ and $|(A^{\mathsf T}(y - A c))_\alpha| \le \lambda$ elsewhere. The proof file proves the descent property, the rate and the fixed point characterization. The debias step is exact on the support: if $S$ contains the true support of a polynomial $q$ in the span and the columns $S$ of $A$ are independent, the refit returns the true coefficients.

That the $\ell_1$ solution finds the true support is a separate, probabilistic claim. It holds when the matrix $A$ satisfies a [restricted isometry property](/restricted-isometry-property/) or a null space property of order $s$. For bounded orthonormal systems, random samples from the orthogonality law give such a matrix with high probability when $N$ is of order $s$ times a power of $\log P$. Rauhut and Ward proved this for Legendre polynomials with samples from the Chebyshev law and a preconditioned system; the constants are large, and the run counts in the example are measurements, not consequences of the theorem.

## Complexity

In the [real RAM](/real-ram/) model, line L2 costs $N C$ for the runs plus $O(d N P)$ for the design matrix. Each power iteration step and each ISTA step costs $O(N P)$, for two products with $A$; with 200 power steps and $K \ge 200$, lines L3 and L4 cost $O(K N P)$. The refit on $|S| < N$ columns costs $O(N |S|^2 + |S|^3) = O(N^3)$. The total is $O(N C + (K + d) N P + N^3)$ time and $O(N P)$ space. ISTA may need many iterations: its rate is only $O(1/k)$, and FISTA, its accelerated form, reaches $O(1/k^2)$ at the same cost per step.

## Properties

- **Fewer runs than terms.** It can work with $N < P$, if the expansion is sparse or nearly sparse.
- **Convex.** The LASSO problem has no spurious local minima, and ISTA converges from any start.
- **Randomized.** The points are random, and recovery holds with high probability, not always.
- **Non-intrusive.** The model is a black box.
- **Biased without refit.** The $\ell_1$ penalty shrinks every kept coefficient; the refit of line L6 removes this.
- **Parameter dependent.** The result depends on $\lambda$, which has to be chosen, for example by cross-validation.

## Variants and improvements

- **Basis pursuit.** Solve $\min \|c\|_1$ subject to $A c = y$ exactly, by [linear programming](/basis-pursuit/), or with $\|A c - y\| \le \delta$ for noisy data.
- **FISTA.** Add a momentum step to ISTA; the rate becomes $O(1/k^2)$ (Beck and Teboulle, Theorem 4.4).
- **Greedy methods.** [Orthogonal matching pursuit](/orthogonal-matching-pursuit/) adds one basis function at a time, and least angle regression follows the whole LASSO path; Blatman and Sudret choose the stopping point by the leave-one-out error.
- **Weighted $\ell_1$ and preconditioning.** Weights that grow with the degree, or sampling from the Chebyshev law with a preconditioner, improve recovery for Legendre bases.
- **Adaptive bases.** Grow the candidate set $\Lambda$ around the terms already found, instead of fixing a total degree.

## When to use it

Use sparse polynomial chaos when runs are expensive, the number of inputs is moderate to large, and you expect only a few inputs and low order interactions to matter, so that most coefficients are small. Choose $\lambda$ by cross-validation, and check the result on runs that were not used. Use [least squares](/regression-polynomial-chaos/) when you can afford two or three times $P$ runs, and [spectral projection](/non-intrusive-spectral-projection/) for few inputs on a grid.

## Pitfalls

- **Dense expansions.** If many coefficients have similar size, no sparse solution fits, and the $\ell_1$ fit is a poor approximation. The validation error shows this.
- **A step larger than $1/L$.** ISTA then can diverge. Estimate $L$ from above, not from below; power iteration approaches $\|A\|_2^2$ from below, so add a margin.
- **Unscaled $\lambda$.** A fixed $\lambda$ means different things for different $N$ and output scales. Scale it by $\|A^{\mathsf T} y\|_\infty$ or by the noise level.
- **Refit on a large support.** If the support has $N$ or more entries, the least-squares refit is not unique; the reference code then keeps the ISTA result.
- **Slow convergence.** ISTA can need thousands of steps for a small $\lambda$. Stop on the change in $F$, or use FISTA.

## Implementations

## History

The $\ell_1$ norm as a proxy for sparsity goes back to work in geophysics and statistics, and became the basis of compressed sensing in the mid 2000s. Iterative soft thresholding for $\ell_1$ penalized least squares was analyzed in the same years, and Beck and Teboulle proved its $O(1/k)$ rate and gave the accelerated FISTA in 2009. Doostan and Owhadi applied compressive sampling to the chaos coefficients of PDEs with random inputs in 2011. In the same year Blatman and Sudret built sparse expansions by least angle regression with a leave-one-out stopping rule. Rauhut and Ward proved in 2012 that sparse Legendre expansions are recovered from a number of samples that grows only with the sparsity and logarithmically with the number of terms.

## References
