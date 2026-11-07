---
tag: XXKK03
kind: algorithm
slug: levinson-durbin-recursion
name: Levinson-Durbin recursion
aliases:
- Levinson recursion
- Durbin recursion
- Durbin's algorithm
- numerical Levinson algorithm
area: numerical/linear-systems
level: advanced
summary: Solve Toeplitz systems in O(n^2) by recursing on the matrix size.
solves: [toeplitz-system-solving]
model: floating-point-model
complexity:
  vars: {n: "the order of the symmetric Toeplitz matrix, at least 2"}
  time: {worst: Θ(n^2), best: Θ(n^2)}
  space: {extra: Θ(n)}
  flops: {worst: "4 n^2 - 3 n - 2"}
properties: {deterministic: true, in_place: false, recursive: false}
prereqs: [toeplitz-system-solving, positive-definite-matrix, cholesky-decomposition]
see_also: [levinson-durbin-algorithm, linear-prediction, cholesky-decomposition, condition-number, growth-factor, fast-fourier-transform, preconditioning, conjugate-gradient-method]
sources:
  - paper: "Norman Levinson, The Wiener RMS (root mean square) error criterion in filter design and prediction, Journal of Mathematics and Physics 25, 1947"
    title: The Wiener RMS (root mean square) error criterion in filter design and prediction
    locator: pp. 261 to 278 (the order recursive solution of symmetric Toeplitz systems)
  - paper: "James Durbin, The fitting of time-series models, Revue de l'Institut International de Statistique 28(3), 1960"
    title: The fitting of time-series models
    locator: pp. 233 to 244 (the recursion for the Yule-Walker equations)
  - paper: doi:10.1137/0901021
    title: George Cybenko, The numerical stability of the Levinson-Durbin algorithm for Toeplitz systems of equations, SIAM Journal on Scientific and Statistical Computing 1(3), 1980
    locator: pp. 303 to 319 (residual bounds in terms of the product of 1 + |alpha_k|, and comparison with Cholesky)
  - paper: doi:10.1137/0906025
    title: James R. Bunch, Stability of methods for solving Toeplitz systems of equations, SIAM Journal on Scientific and Statistical Computing 6(2), 1985
    locator: pp. 349 to 364 (weak stability, and instability for indefinite matrices)
  - book: isbn:9781421407944
    title: Gene H. Golub and Charles F. Van Loan, Matrix Computations, fourth edition, Johns Hopkins University Press, 2013
    locator: Section 4.7, Classical Methods for Toeplitz Systems (Durbin's algorithm in 2n^2 flops, Levinson's algorithm in 4n^2 flops, and the remarks on stability)
  - paper: "A. W. Bojanczyk, R. P. Brent, F. R. de Hoog and D. R. Sweet, On the stability of the Bareiss and related Toeplitz factorization algorithms, SIAM Journal on Matrix Analysis and Applications 16(1), 1995"
    title: On the stability of the Bareiss and related Toeplitz factorization algorithms
    locator: pp. 40 to 57
---

The Levinson-Durbin recursion solves a symmetric positive definite Toeplitz system $T x = b$, where $T_{ij} = r_{|i - j|}$, in $4 n^2$ flops instead of the $n^3/3$ of [Cholesky](/cholesky-decomposition/). It solves the leading systems of order $1, 2, \ldots, n$ in turn, extending each solution with the help of the solution $y$ of the Yule-Walker equations $T_k y = -(r_1, \ldots, r_k)^T$, which Durbin's part of the recursion updates in $2 k$ flops per step. The by-products are the reflection coefficients $\alpha_k$ of linear prediction: $T$ is positive definite exactly when all $|\alpha_k| < 1$, which the recursion checks for free. In floating point the method is not backward stable, but Cybenko (1980) showed that it is weakly stable for positive definite $T$: its forward error is of the size $u\,\kappa(T)$ that a backward stable method would give. For indefinite matrices it can be unstable even when $T$ is well conditioned. The exact version over a field, without symmetry, is the [Levinson-Durbin algorithm](/levinson-durbin-algorithm/).

## In plain words

A Toeplitz matrix repeats the same number along each diagonal, so its top-left corners are all Toeplitz matrices of the same kind, each containing the previous one. Solve the problem for the $1 \times 1$ corner, then grow it one row and column at a time. Because of the repeating pattern, the new solution is the old one plus a multiple of a helper vector read backwards, and the helper itself is updated the same way. Each step costs a few sums, so the whole job takes about $n^2$ steps instead of $n^3$.

## The problem

Given $r_0 > 0, r_1, \ldots, r_{n-1}$ and $b \in \mathbb{R}^n$, with $T = (r_{|i - j|})$ symmetric positive definite, find $x = T^{-1} b$. See [Toeplitz system solving](/toeplitz-system-solving/). Scaling by $r_0$ gives $r_0 = 1$, assumed below.

**Notation.** $T_k$ is the leading $k \times k$ submatrix, $E_k$ the $k \times k$ exchange matrix that reverses the order of a vector, so $E_k T_k E_k = T_k$ (persymmetry). $y^{(k)}$ solves $T_k y^{(k)} = -(r_1, \ldots, r_k)^T$ and $x^{(k)}$ solves $T_k x^{(k)} = (b_0, \ldots, b_{k-1})^T$. The reflection coefficient $\alpha_k$ is the last entry of $y^{(k+1)}$, $\beta_k = \det T_{k+1} / \det T_k$, $\hat x$ is the computed solution, $u = 2^{-53}$, $\kappa_1(T) = \|T\|_1 \|T^{-1}\|_1$, and $\eta = \|b - T \hat x\|_\infty / (\|T\|_\infty \|\hat x\|_\infty + \|b\|_\infty)$ is the normwise backward error.

## The algorithm

Durbin's part extends $y$; Levinson's part extends $x$ with the same $\beta$.

```pseudo id=main
DURBIN(r₀ = 1, r₁, …, r_n)  ▷ solves T_n y = −(r₁, …, r_n)
L1  y ← (−r₁); α ← −r₁; β ← 1
L2  for k ← 1 to n − 1 do
L3      β ← (1 − α²) β       (fail if β ≤ 0: T is not positive definite)
L4      α ← −(r_{k+1} + Σ_{j<k} r_{k−j} y_j) / β
L5      y ← (y + α E_k y, α)
LEVINSON(r₀, …, r_{n−1}, b)  ▷ solves T x = b
L6  divide r and b by r₀
L7  x ← (b₀); y ← (−r₁); α ← −r₁; β ← 1
L8  for k ← 1 to n − 1 do
L9      β ← (1 − α²) β       (fail if β ≤ 0)
L10     μ ← (b_k − Σ_{j<k} r_{j+1} x_{k−1−j}) / β
L11     x ← (x + μ E_k y, μ)
L12     if k < n − 1 then α ← −(r_{k+1} + Σ_{j<k} r_{j+1} y_{k−1−j}) / β
L13         y ← (y + α E_k y, α)
L14 return x
```

## Example

Take $r = (1, \frac12, \frac14)$, the Kac-Murdock-Szegő matrix with $r_k = 2^{-k}$, and $b = (1, 2, 3)^T$.

| $k$ | $\beta$ | $\mu$ | $x^{(k+1)}$ | $\alpha$ | $y^{(k+1)}$ |
|---|---|---|---|---|---|
| 0 | $1$ | | $(1)$ | $-\frac12$ | $(-\frac12)$ |
| 1 | $\frac34$ | $(2 - \frac12 \cdot 1)/\frac34 = 2$ | $(1 + 2 \cdot (-\frac12), 2) = (0, 2)$ | $-(\frac14 - \frac14)/\frac34 = 0$ | $(-\frac12, 0)$ |
| 2 | $\frac34$ | $(3 - \frac12 \cdot 2 - \frac14 \cdot 0)/\frac34 = \frac83$ | $(0, \frac23, \frac83)$ | | |

Check: $T x = (\frac13 + \frac23, \frac23 + \frac43, \frac13 + \frac83) = (1, 2, 3)$. For this matrix only the first reflection coefficient is nonzero, and $\beta_k = \frac34$ for every $k \ge 1$: the prediction error of a first order autoregressive process.

## Correctness

The proofs are in `proofs/correctness.md`. Exact arithmetic.

1. **Durbin step (proved).** If $T_{k+1}$ is nonsingular and $\beta_k \ne 0$, then $y^{(k+1)} = (y^{(k)} + \alpha_k E_k y^{(k)}, \alpha_k)$ with $\alpha_k$ from line L4, and $\beta_k = 1 + r^{(k)T} y^{(k)} = (1 - \alpha_{k-1}^2)\beta_{k-1}$.
2. **Levinson step (proved).** In the same way $x^{(k+1)} = (x^{(k)} + \mu_k E_k y^{(k)}, \mu_k)$ with $\mu_k$ from line L10.
3. **Determinants and definiteness (proved).** $\beta_k = \det T_{k+1}/\det T_k = \prod_{j < k}(1 - \alpha_j^2)$, the $k$-th pivot of Cholesky or Gaussian elimination. So $T$ is positive definite if and only if $|\alpha_k| < 1$ for $k = 0, \ldots, n - 2$; the check of line L9 is exact, and a singular or indefinite matrix is reported. Conversely every sequence with $|\alpha_k| < 1$ arises from a positive definite Toeplitz matrix (the step-up recursion, used by the tests to build matrices of prescribed conditioning).
4. **Termination.** The loop runs $n - 1$ times.

**Floating point.** Three statements of different strength:

- *Residual bound (proved, Cybenko 1980).* For positive definite $T$, the residual of Durbin's computed $\hat y$ is bounded by $c(n)\,u \prod_k (1 + |\alpha_k|)$ times a norm of $\hat y$, to first order in $u$; the product can be as large as about $2^{n}$. Cybenko compares this with the bound $\kappa_1(T) \ge$ (a quantity of the same order) for the case of reflection coefficients of one sign, and concludes that the forward error is comparable to Cholesky's error bound: *weak stability*, in Bunch's term. The constants are in the paper and not restated here.
- *Not backward stable (observed).* With all $\alpha_k = \frac12$ and $n = 30$ ($\kappa_1(T) \approx 3.1 \times 10^{13}$) and $x = (1, \ldots, 1)$, the tests measure $\eta \approx 6.1 \times 10^4\, u$ for Levinson against $0.56\, u$ for Cholesky. The forward errors are $4.1 \times 10^{-3}$ and $2.0 \times 10^{-4}$, against $u\,\kappa_1 \approx 3.5 \times 10^{-3}$: both within a small multiple of the conditioning bound, Cholesky better in practice.
- *Observed constants.* On $120$ random positive definite matrices built from reflection coefficients, the tests find forward errors at most $20\,u\,\kappa_1(T)$ (when $u\,\kappa_1 < 10^{-3}$) and $\eta \le n u \prod_k (1 + |\alpha_k|)$.

For symmetric indefinite $T$ with nonzero leading minors the recursion still runs (without the definiteness check) but is not even weakly stable (Bunch 1985): for $r = (1, 1 + 10^{-12}, 0)$, $\kappa_1(T) < 20$, but $T_2$ is nearly singular and the computed solution has relative error about $6 \times 10^{-5}$.

## Complexity

Durbin's algorithm costs $2 n^2 + 2 n - 4$ flops for order $n$, Levinson's $4 n^2 - 3 n - 2$ when $r_0 = 1$, each step $k$ being two or four inner products and vector updates of length $k$. The storage is $O(n)$: the vectors $x$, $y$ and $r$, and nothing of size $n^2$. A step reads the $k$ most recent entries of $r$, $x$ and $y$, so the method streams through memory and is limited by memory traffic only for very large $n$. The span is $\Theta(n \log n)$: the $n - 1$ steps are sequential and each contains inner products of depth $O(\log k)$. Proofs are in `proofs/complexity.md`.

## Properties

- **Order recursive**: the solutions of all leading subsystems, and all reflection coefficients, come for free, which is what linear prediction and autoregressive model fitting need.
- **Built-in definiteness test**: $|\alpha_k| < 1$ for all $k$ if and only if $T$ is positive definite.
- **Implicit factorization**: the reversed vectors $(E_k y^{(k)}, 1)$, padded with zeros, are the columns of a unit upper triangular $U$ with $T^{-1} = U D^{-1} U^T$, $D = \operatorname{diag}(\beta_k)$, so $T^{-1}$ can be applied or formed in $O(n^2)$ (compare the Trench and Gohberg-Semencul formulas).
- **No pivoting**: it needs all leading minors nonzero, and is reliable only when they are all positive.
- **Weakly but not backward stable** in floating point for positive definite $T$.

## Variants and improvements

- **Trench's algorithm.** Builds $T^{-1}$ explicitly in $O(n^2)$ flops from $y^{(n)}$.
- **Nonsymmetric Levinson (Zohar, Trench).** Two helper vectors, forward and backward; about $8 n^2$ flops. See the [exact version](/levinson-durbin-algorithm/).
- **Schur (Bareiss) algorithm.** Computes the Cholesky factor of $T$, not of $T^{-1}$, via the generator; for positive definite $T$, Bojanczyk, Brent, de Hoog and Sweet (1995) prove error bounds for it comparable to those of Cholesky.
- **Look-ahead and pivoting.** For indefinite or non-strongly-regular matrices, look-ahead Levinson skips over nearly singular leading blocks, and the Gohberg-Kailath-Olshevsky method converts to a Cauchy-like matrix and uses partial pivoting in $O(n^2)$.
- **Superfast solvers.** Divide and conquer with FFTs gives $O(n \log^2 n)$ flops (Brent, Gustavson and Yun; Ammar and Gragg), with worse stability.
- **Iterative methods.** [CG](/conjugate-gradient-method/) with a circulant [preconditioner](/preconditioning/) (Strang, T. Chan) costs $O(n \log n)$ per iteration via the [FFT](/fast-fourier-transform/) and often converges in a few iterations.
- **Burg's method.** In signal processing, estimates the reflection coefficients directly from data, guaranteeing $|\alpha_k| < 1$.

## When to use it

Use it for symmetric positive definite Toeplitz systems of moderate size, especially when the reflection coefficients or all leading solutions are wanted, as in [linear prediction](/linear-prediction/), speech coding (LPC) and autoregressive spectral estimation. If $T$ is very ill conditioned and a small residual matters, or if a backward stable answer is required, use Cholesky ($n^3/3$ flops) or a stabilized Schur algorithm. For indefinite or nonsymmetric Toeplitz matrices use a pivoted method (Cauchy-like transformation). For very large $n$ use preconditioned CG with FFTs.

## Pitfalls

- **Indefinite matrices.** Without positive definiteness, a small $\beta_k$ (a nearly singular leading minor) ruins the solution even if $T$ is well conditioned; the example above loses $11$ digits.
- **Breakdown on singular leading minors.** $r = (1, 1, 0)$ gives a nonsingular $T_3$ with $\det T_2 = 0$, and the recursion divides by zero. This is not a singularity test for $T$.
- **Testing $\beta \le 0$ in floating point.** Near the boundary of definiteness the computed $\beta$ can change sign; with $\alpha_k = 0.99$ and $n = 10$, $\beta_9 = \prod (1 - \alpha^2) \approx 5 \times 10^{-16}$, and rounding the matrix entries already makes it indefinite.
- **Small residual expected.** The method can have residuals thousands of times larger than Cholesky's; do not judge it by the residual alone. One step of [iterative refinement](/iterative-refinement/) with a residual in working precision usually brings the residual down to Cholesky's level.
- **Sign conventions.** Signal processing writes the predictor as $1 + \sum a_j z^{-j}$ and the reflection coefficients with the opposite sign; mixing conventions flips the update.

## Implementations

## History

Norman Levinson derived the recursion in 1947 to compute Wiener filters; the paper was reprinted as an appendix to Wiener's 1949 book on extrapolation and smoothing of time series. James Durbin (1960) gave the simpler form for the Yule-Walker equations of autoregressive models, and William Trench (1964) and Shalhav Zohar (1969, 1974) extended it to the inverse and to nonsymmetric matrices. In signal processing it became the core of linear predictive coding of speech in the 1970s. Cybenko's 1980 analysis showed that it is about as accurate as Cholesky for positive definite matrices despite not being backward stable, and Bunch (1985) defined weak stability and showed the failure for indefinite matrices.

## References
