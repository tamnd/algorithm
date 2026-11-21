---
tag: 7EBBWK
kind: algorithm
slug: truncated-svd
name: Truncated singular value decomposition
aliases:
- TSVD
- truncated SVD
area: imaging-and-inverse-problems/regularization-of-inverse-problems
level: core
summary: "Regularize A x = y by keeping the k largest singular components of the pseudoinverse solution and dropping the rest. Choose k from the noise level, for example by the discrepancy principle."
solves: [fredholm-integral-equation-first-kind]
model: floating-point-model
complexity:
  vars: {m: the number of rows of A, n: the number of columns of A with m >= n, k: the truncation index}
  time: {worst: O(m n^2 + k (m + n))}
  space: {extra: O(m n)}
properties: {deterministic: true, linear_in_data: true, direct: true, iterative: false}
history:
  year: 1987
  people: [Per Christian Hansen]
  note: Hanson (1971) and others used truncated singular value expansions for first-kind integral equations; Hansen (1987) analyzed TSVD as a regularization method and compared it with Tikhonov.
prereqs: [regularization-method, singular-value-decomposition, spectral-filter-factors, condition-number]
see_also: [tikhonov-regularization, picard-condition, morozov-discrepancy-principle, pseudoinverse, rank-revealing-factorization, golub-kahan-svd-algorithm, l-curve-method, resolution-matrix]
sources:
  - paper: doi:10.1007/BF01937276
    title: Per Christian Hansen, The truncated SVD as a method for regularization, BIT 27(4), 1987, 534 to 553
    locator: the TSVD solution, its perturbation bounds, and its relation to Tikhonov regularization
  - paper: doi:10.1007/BF02288367
    title: Carl Eckart and Gale Young, The approximation of one matrix by another of lower rank, Psychometrika 1(3), 1936, 211 to 218
    locator: the best approximation of lower rank by truncating the canonical (singular value) form
  - paper: doi:10.1093/qmath/11.1.50
    title: L. Mirsky, Symmetric gauge functions and unitarily invariant norms, Quarterly Journal of Mathematics 11(1), 1960, 50 to 59
    locator: the extension of the best low-rank approximation to every unitarily invariant norm
  - paper: doi:10.1137/0708058
    title: "Richard J. Hanson, A numerical method for solving Fredholm integral equations of the first kind using singular values, SIAM Journal on Numerical Analysis 8(3), 1971, 616 to 622"
    locator: the solution of a discretized first-kind equation from its leading singular components
  - book: isbn:9780898714036
    title: Per Christian Hansen, Rank-Deficient and Discrete Ill-Posed Problems, Numerical Aspects of Linear Inversion, SIAM, 1998
    locator: Chapter 3 (numerical rank and truncated SVD) and Chapter 7 (the discrepancy principle)
  - book: isbn:9780792341574
    title: Heinz W. Engl, Martin Hanke and Andreas Neubauer, Regularization of Inverse Problems, Kluwer, 1996
    locator: Chapters 3 and 4 (truncated singular value expansion as a regularization method, its infinite qualification)
---

The truncated singular value decomposition (TSVD) solves an ill-conditioned linear system $A x = y$ by keeping the $k$ largest singular components of the pseudoinverse solution and dropping the rest: $x_k = \sum_{i=1}^{k} \frac{u_i^T y}{\sigma_i} v_i$. Dropping the components with small $\sigma_i$ removes the ones that amplify noise most, at the cost of a bias, and the index $k$ is the regularization parameter. It costs one [SVD](/singular-value-decomposition/), $O(m n^2)$ for $m \ge n$, after which each $x_k$ costs $O(k(m + n))$ and all residual norms together $O(m n)$. It is the simplest [regularization method](/regularization-method/) and the sharp-cutoff case of [spectral filter factors](/spectral-filter-factors/); [Tikhonov regularization](/tikhonov-regularization/) is the smooth-cutoff case, and on discrete ill-posed problems the two give solutions of similar quality.

## In plain words

The SVD splits a matrix into independent channels, each with a gain. Solving the system means dividing the data in each channel by its gain. The channels with tiny gains are the trouble: the true signal in them is tiny too, so what you measure there is mostly noise, and dividing by a tiny gain makes that noise huge. The truncated method simply ignores those channels. You keep the strong channels, where the signal is well above the noise, and set the rest of the answer to zero. The number of channels you keep is the one knob. A good rule is to keep adding channels until the solution explains the data about as well as the noise level allows, and then stop.

## The problem

Given an $m \times n$ real matrix $A$, data $y^\delta \in \mathbb{R}^m$ with $y^\delta = A x^{\mathrm{true}} + e$, and either a noise bound $\|e\|_2 \le \delta$ or a target rank, find an approximation of the minimum norm solution $x^\dagger = A^\dagger y$ of the noise-free problem that is stable against $e$. Typically $A$ is the discretization of a compact operator, such as a [Fredholm integral equation of the first kind](/fredholm-integral-equation-first-kind/), and its singular values decay with no gap. The same algorithm also computes the minimum norm least squares solution of a rank-deficient system when $k$ equals the numerical rank.

## The algorithm

Write the thin SVD as $A = U \Sigma V^T = \sum_{i=1}^{p} \sigma_i u_i v_i^T$ with $p = \min(m, n)$ and $\sigma_1 \ge \cdots \ge \sigma_p \ge 0$. Let $r$ be the number of positive $\sigma_i$.

```pseudo id=main
TSVD(A, y, k)                              ▷ 0 ≤ k ≤ r
L1  (U, Σ, V) ← SVD(A)                     ▷ σ_1 ≥ σ_2 ≥ … ≥ σ_p
L2  x ← 0 ∈ ℝ^n
L3  for i ← 1 to k do
L4      c ← (u_iᵀ y) / σ_i
L5      x ← x + c · v_i
L6  return x

TSVD-PATH(U, Σ, y, δ, τ)                   ▷ residual norms ρ_k = ‖A x_k - y‖ for k = 0 … r
L7  β_i ← u_iᵀ y for i = 1 … r;  ρ_r² ← ‖y - Σ_{i ≤ r} β_i u_i‖²
L8  for k ← r - 1 down to 0 do
L9      ρ_k² ← ρ_{k+1}² + β_{k+1}²
L10 return the smallest k with ρ_k ≤ τ δ, or "none"
```

TSVD computes the SVD once (L1) and then sums the first $k$ terms of the pseudoinverse expansion (L2 to L5). TSVD-PATH uses the same SVD to get the residual norm for every $k$ at once. The part $y - \sum_{i \le r} \beta_i u_i$ of the data lies outside the range of $A$; no $x_k$ can fit it. Each extra component $k + 1$ removes $\beta_{k+1}^2$ from the squared residual. Line L10 is the [discrepancy principle](/morozov-discrepancy-principle/): stop at the first $k$ whose residual is at the noise level, with a safety factor $\tau > 1$ (the code uses $\tau = 1.1$; the factor is a choice).

## Example

**A trace.** Let $A = \operatorname{diag}(1,\ 0.1,\ 0.001)$, so that $U = V = I$, $x^{\mathrm{true}} = (1, 1, 1)$ and $e = (0,\ 0.01,\ 0.01)$, with $\|e\| = \delta = 0.014142$. The data are $y = (1,\ 0.11,\ 0.011)$.

| $k$ | $c_k = \beta_k/\sigma_k$ | $x_k$ | $\|x_k - x^{\mathrm{true}}\|$ | $\rho_k = \|A x_k - y\|$ |
|---|---|---|---|---|
| 0 | | $(0, 0, 0)$ | 1.7321 | 1.00609 |
| 1 | 1 | $(1, 0, 0)$ | 1.4142 | 0.11055 |
| 2 | 1.1 | $(1, 1.1, 0)$ | 1.0050 | 0.011 |
| 3 | 11 | $(1, 1.1, 11)$ | 10.0005 | 0 |

Line L7 gives $\beta = (1,\ 0.11,\ 0.011)$ and $\rho_3 = 0$, since $A$ is square and nonsingular. Lines L8 and L9 add $0.011^2$, then $0.11^2$, then $1^2$. With $\tau\delta = 0.015556$, line L10 returns $k = 2$. The third component has $\sigma_3 = 0.001$, and its datum $0.011$ is ten parts noise to one part signal; dividing by $\sigma_3$ turns the noise $0.01$ into an error of $10$.

**A discretized integral equation.** Take the rectangle-rule matrix of the integration operator $(A x)(s) = \int_0^s x(t)\,dt$ with $n = 24$ ($h = 1/24$ on and below the diagonal), with singular values from $\sigma_1 = 0.64999$ down to $\sigma_{24} = 0.02088$. Let $x_j = \sin(\pi t_j)$ at the midpoints $t_j = (j + \tfrac12)/24$, so $\|x\| = 3.464$, and add Gaussian noise (seed 15) scaled to $\|e\| = \delta = 10^{-2}$.

| $k$ | 0 | 3 | 6 | 9 | 12 | 18 | 24 |
|---|---|---|---|---|---|---|---|
| $\|x_k - x\|$ | 3.464 | 0.245 | 0.108 | 0.063 | 0.118 | 0.221 | 0.416 |
| $\rho_k$ | 1.964 | 0.0216 | 0.0103 | 0.0096 | 0.0089 | 0.0075 | 0 |

The error falls while $k$ adds signal and rises when $k$ adds mostly noise; the best $k$ is $9$. The discrepancy principle with $\tau = 1.1$ stops at $k = 6$ ($\rho_5 = 0.0115 > 0.011 \ge \rho_6 = 0.0103$), with an error within a factor $1.7$ of the best. A Picard plot of this problem is on the page [Picard condition](/picard-condition/).

## Correctness

TSVD returns $x_k = A_k^\dagger y$, where $A_k = \sum_{i \le k} \sigma_i u_i v_i^T$ is the truncated matrix: $x_k$ is the minimum norm minimizer of $\|A_k x - y\|$. By the Eckart-Young theorem, $A_k$ is the closest matrix of rank at most $k$ to $A$ in the 2-norm (error $\sigma_{k+1}$) and in the Frobenius norm (error $(\sum_{i > k} \sigma_i^2)^{1/2}$); Mirsky extended this to every unitarily invariant norm. The residual and the solution norm are $\|A x_k - y\|^2 = \|y_\perp\|^2 + \sum_{i > k} \beta_i^2$ and $\|x_k\|^2 = \sum_{i \le k} (\beta_i/\sigma_i)^2$, so L7 to L9 compute the residuals exactly, the residual does not increase with $k$, and L10 finds the first crossing. For noisy data with $\|y^\delta - y\| \le \delta$ and $y = A x^\dagger$,
$$\|x_k^\delta - x^\dagger\| \le \frac{\delta}{\sigma_k} + \Big\| \sum_{i > k} \frac{u_i^T y}{\sigma_i} v_i \Big\|,$$
and under the [source condition](/source-condition/) $x^\dagger = (A^T A)^\nu w$ with $\|w\| \le C$, the choice of the largest $k$ with $\sigma_k \ge \delta^{1/(2\nu+1)}$ gives an error at most $(1 + C)\, \delta^{2\nu/(2\nu+1)}$, for every $\nu > 0$. The proofs are in proofs/correctness.md.

## Complexity

- **The SVD (L1).** $O(m n^2)$ flops for $m \ge n$ with the Golub-Kahan bidiagonalization and the QR iteration (see [Golub-Kahan SVD algorithm](/golub-kahan-svd-algorithm/)). The reference code uses one-sided Jacobi, which costs $O(m n^2)$ per sweep and needs a small number of sweeps in practice. If $m < n$, apply the method to $A^T$; the cost is $O(n m^2)$.
- **One solution (L2 to L6).** $k$ inner products of length $m$ and $k$ vector updates of length $n$: $O(k(m + n))$.
- **All residuals (L7 to L10).** $O(m r)$ for the coefficients and the out-of-range part, then $O(r)$ for the tail sums and the search. Every solution norm $\|x_k\|$ also costs $O(r)$ in total. So the whole L-curve or discrepancy curve costs $O(m n)$ after the SVD.
- **Space.** $O(m n)$ for $U$ and $V$; the thin SVD stores $m p + p + n p$ numbers.

For one value of $k$ and a large sparse $A$, a full SVD is wasteful. A partial SVD by Lanczos bidiagonalization, or an iterative method such as [LSQR](/lsqr/), costs only products with $A$ and $A^T$.

## Properties

- **Linear in the data.** $x_k = V_k \Sigma_k^{-1} U_k^T y$ for a fixed $k$. With the discrepancy principle, $k$ depends on $y$ and the map is no longer linear.
- **Filter factors.** $f_i = 1$ for $i \le k$ and $0$ otherwise. The noise amplification is $\|A_k^\dagger\| = 1/\sigma_k$.
- **Infinite qualification.** Under the source condition the bias is at most $\sigma_{k+1}^{2\nu} \|w\|$ for every $\nu$, so TSVD does not saturate as Tikhonov does at $\nu = 1$ (see [qualification of regularization](/qualification-of-regularization/)).
- **Monotone curves.** As $k$ grows, $\|A x_k - y\|$ does not increase and $\|x_k\|$ does not decrease.
- **Resolution.** The [resolution matrix](/resolution-matrix/) $V_k V_k^T$ is an orthogonal projection of trace $k$.
- **Sign invariance.** Each term $(u_i^T y) v_i$ is unchanged if the SVD returns $-u_i$ and $-v_i$, so the arbitrary signs of a computed SVD do not matter.

## Variants and improvements

- **Truncated GSVD.** With a regularization matrix $L$ (for example a difference operator), truncate the generalized SVD of the pair $(A, L)$ instead. This penalizes roughness rather than size.
- **Damped or smoothed truncation.** Replace the sharp cutoff by a smooth one; Tikhonov is the standard choice, with $f_i = \sigma_i^2/(\sigma_i^2 + \alpha)$.
- **Truncated rank-revealing QR.** A [rank-revealing factorization](/rank-revealing-factorization/) gives a cheaper approximation of the dominant subspace when there is a clear gap.
- **Partial and randomized SVD.** For a large $A$, compute only the first $k$ triples by Lanczos bidiagonalization or by a randomized range finder.
- **Other parameter rules.** The [L-curve](/l-curve-method/) and generalized cross-validation choose $k$ without $\delta$; they are heuristics (see [Bakushinskii veto](/bakushinskii-veto/)).

## When to use it

Use TSVD on small and medium dense problems, where one SVD is affordable (up to a few thousand unknowns), and when you want to see the problem: the singular values, the Picard plot and the effect of each $k$ all come from the same SVD. It is the natural method when the singular values have a clear gap, because then the numerical rank is well defined. When the singular values decay without a gap, Tikhonov regularization gives similar errors with a smoother solution and a continuous parameter. For large or sparse problems use an iterative method such as LSQR or CGLS, which regularize by the number of steps.

## Pitfalls

- **Forming $A^T A$.** Computing the SVD from the eigenvalues of $A^T A$ squares the condition number. Singular values below $\sqrt{u}\,\sigma_1$, with $u = 2^{-53}$, are then lost. Use an SVD of $A$ itself.
- **Truncating below the rounding level.** In the [floating-point model](/floating-point-model/), a backward stable SVD returns the exact SVD of $A + E$ with $\|E\| \le c\, u \|A\|$, so each computed $\sigma_i$ has an absolute error of about $u\,\sigma_1$. Components with $\sigma_i$ near $u\,\sigma_1$ are rounding noise even for exact data; never choose $k$ beyond them.
- **Close singular values at the cut.** If $\sigma_k$ and $\sigma_{k+1}$ are close, the individual vectors $v_k$ and $v_{k+1}$ are ill determined, and $x_k$ changes a lot with small changes of $A$. The space of the first $k$ vectors is stable only when the gap $\sigma_k - \sigma_{k+1}$ is large compared with the perturbation (see [Davis-Kahan theorem](/davis-kahan-theorem/)).
- **Looking for a gap that is not there.** For a discretized compact operator the singular values decay smoothly. The choice of $k$ must come from the noise level, not from a gap.
- **Gibbs-like ringing.** The sharp cutoff makes the rows of the resolution matrix oscillate, with negative side lobes, so TSVD solutions can ring near jumps. A smooth filter rings less.
- **Out-of-range data.** If $m > n$, the part of $y$ outside the range of $A$ stays in every residual. The discrepancy principle then needs $\delta$ to include it, or no $k$ satisfies L10.

## Implementations

## History

Erhard Schmidt proved in 1907 that the truncated singular expansion gives the best approximation of an integral operator by one of finite rank. Eckart and Young proved the matrix version in 1936, and Mirsky extended it to all unitarily invariant norms in 1960. After Golub and Kahan made the SVD computable in 1965, Hanson (1971) and others solved discretized first-kind integral equations from their leading singular components. Hansen (1987) analyzed TSVD as a regularization method, gave its perturbation bounds and showed that under the discrete Picard condition it gives solutions close to those of Tikhonov regularization.

## References
