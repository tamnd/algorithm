---
tag: DCQZQB
kind: algorithm
slug: rayleigh-quotient-iteration
name: Rayleigh quotient iteration
aliases:
- RQI
- Rayleigh quotient inverse iteration
area: numerical/eigenproblems
level: core
summary: Inverse iteration whose shift is the current Rayleigh quotient. For a symmetric matrix it converges cubically to an eigenpair near the start and never increases the residual.
solves: [eigenvalue-problem]
model: floating-point-model
complexity:
  vars: {n: "the order of A", k: "the number of steps"}
  time: {worst: Θ(k n^3)}
  space: {extra: Θ(n^2)}
  flops: {worst: "k (2 n^3 / 3 + 4 n^2)"}
properties: {deterministic: true, in_place: false, recursive: false, iterative: true}
history:
  year: 1958
  people: [Alexander Ostrowski]
  note: Ostrowski proved the local cubic convergence for symmetric matrices in a series of papers from 1958 and 1959; the iteration itself was in use before.
prereqs: [inverse-iteration, rayleigh-quotient]
see_also: [power-iteration, qr-algorithm, wilkinson-shift, symmetric-eigenproblem, mrrr-algorithm, lanczos-algorithm, eigenvalue-condition-number, subspace-iteration]
sources:
  - book: isbn:9780898713619
    title: Lloyd N. Trefethen and David Bau III, Numerical Linear Algebra, SIAM, 1997
    locator: Lecture 27, Rayleigh Quotient, Inverse Iteration (Algorithm 27.3 and Theorem 27.3, cubic convergence)
  - book: isbn:9780898714029
    title: Beresford N. Parlett, The Symmetric Eigenvalue Problem, SIAM Classics in Applied Mathematics 20, 1998
    locator: Chapter 4, the sections on Rayleigh quotient iteration (local cubic convergence, monotone residuals, global convergence)
  - book: isbn:9781421407944
    title: Gene H. Golub and Charles F. Van Loan, Matrix Computations, fourth edition, Johns Hopkins University Press, 2013
    locator: Section 8.2.3, Rayleigh Quotient Iteration
  - book: isbn:9780898713893
    title: James W. Demmel, Applied Numerical Linear Algebra, SIAM, 1997
    locator: Section 5.3.2, Rayleigh Quotient Iteration
  - paper: "A. M. Ostrowski, On the convergence of the Rayleigh quotient iteration for the computation of the characteristic roots and vectors. I, Archive for Rational Mechanics and Analysis 1, 1958"
    title: On the convergence of the Rayleigh quotient iteration for the computation of the characteristic roots and vectors. I
    locator: Arch. Rational Mech. Anal. 1 (1958), pp. 233 to 241, and the later parts II to VI
  - paper: "B. N. Parlett, The Rayleigh quotient iteration and some generalizations for nonnormal matrices, Mathematics of Computation 28, 1974"
    title: The Rayleigh quotient iteration and some generalizations for nonnormal matrices
    locator: Math. Comp. 28 (1974), pp. 679 to 693
---

Rayleigh quotient iteration (RQI) finds one eigenpair of a square matrix $A$ by [inverse iteration](/inverse-iteration/) with a shift that changes at every step: the shift is the [Rayleigh quotient](/rayleigh-quotient/) $\rho(x) = x^* A x / x^* x$ of the current vector. For a symmetric or Hermitian $A$ the error in the angle is cubed at each step near convergence, so three or four solves usually take a rough start to full accuracy, and the residual never increases. For a nonsymmetric $A$ the local rate drops to quadratic. The price is a new factorization of $A - \rho I$ at every step, and the eigenvalue that is found depends on the start in a way that is hard to control.

## In plain words

Inverse iteration pulls a vector toward the hidden direction whose stretch factor is closest to a guess. The closer the guess, the stronger the pull. Rayleigh quotient iteration improves the guess at every step by reading it off the current vector, and a better vector gives a much better guess. The two improvements feed each other, so the number of correct digits roughly triples per step for a symmetric matrix. The catch is that the method chooses which direction it finds, and a start that sits exactly halfway between two directions can stay stuck.

## The problem

**Notation.** $A \in \mathbb C^{n \times n}$ with eigenvalues $\lambda_i$ and eigenvectors $v_i$; for a Hermitian $A$ the $v_i$ are orthonormal. $\rho(x) = x^* A x / x^* x$ is the Rayleigh quotient, $\theta_k = \angle(x_k, v_j)$ the angle to the eigenvector that is found, $\delta = \lambda_{\max} - \lambda_{\min}$ the spread and $\mathrm{gap}_j = \min_{i \ne j} |\lambda_i - \lambda_j|$. $u$ is the unit roundoff and $\|A\|_F$ the Frobenius norm.

Given $A$, a start $x_0 \ne 0$, a tolerance $\mathrm{tol}$ and a limit $\mathrm{maxit}$, return a scalar $\rho$ and a unit vector $x$ with $\|A x - \rho x\|_2 \le \mathrm{tol} \, \|A\|_F$ and the flag CONVERGED, or the last pair and NOT-CONVERGED. This is one eigenpair of the [eigenvalue problem](/eigenvalue-problem/); which one is not specified in advance.

## The algorithm

```pseudo id=main
RAYLEIGH-QUOTIENT-ITERATION(A, x₀, tol, maxit)
L1  x ← x₀ / ‖x₀‖₂
L2  ρ ← x* A x                                    ▷ Rayleigh quotient of the unit vector x
L3  for k ← 0 to maxit do
L4      r ← A x − ρ x
L5      if ‖r‖₂ ≤ tol · ‖A‖_F then return (ρ, x, k, CONVERGED)
L6      if k = maxit then return (ρ, x, k, NOT-CONVERGED)
L7      solve (A − ρ I) y = x                     ▷ a zero pivot is replaced by u ‖A‖_F
L8      x ← y / ‖y‖₂
L9      ρ ← x* A x
```

Lines L7 and L8 are one step of inverse iteration with the shift $\rho$, and line L9 replaces the shift by the Rayleigh quotient of the new vector. The test in line L5 is a backward error test: when it passes, $(\rho, x)$ is an exact eigenpair of $A - r x^*$, and $\|r x^*\|_2 = \|r\|_2$. Line L7 solves a nearly singular system on purpose. Gaussian elimination with partial pivoting computes a solution whose error lies almost entirely along the wanted eigenvector, so the direction of $y$ is accurate even though $y$ itself is huge. If $\rho$ equals an eigenvalue in floating point, a pivot can be exactly zero; replacing it by $u \|A\|_F$ gives the same direction as a tiny perturbation of $\rho$. The implementation uses a dense LU factorization; for a tridiagonal or Hessenberg $A$ a banded solve is used instead.

## Example

Let $A = \begin{pmatrix} 2 & 1 & 0 \\ 1 & 3 & 1 \\ 0 & 1 & 4 \end{pmatrix}$, with eigenvalues $3 - \sqrt 3$, $3$ and $3 + \sqrt 3 = 4.7320508075\ldots$, and $x_0 = (1, 1, 1)^T$. All quantities are rational, so the table was computed in exact arithmetic and then rounded. The last column is the cubic rate constant $\tan\theta_{k+1} / \tan^3\theta_k$.

| $k$ | $x_k$ | $\rho_k$ | $\lambda - \rho_k$ | $\lVert r_k \rVert_2$ | $\tan\theta_k$ | $\tan\theta_k / \tan^3\theta_{k-1}$ |
|---|---|---|---|---|---|---|
| 0 | (0.577350, 0.577350, 0.577350) | 4.3333333333 | 3.987e-01 | 9.428e-01 | 4.536e-01 | |
| 1 | (0.119855, 0.530788, 0.838987) | 4.7074171797 | 2.463e-02 | 2.219e-01 | 1.149e-01 | 1.23 |
| 2 | (0.212433, 0.578117, 0.787815) | 4.7320462724 | 4.535e-06 | 2.869e-03 | 1.599e-03 | 1.05 |
| 3 | (0.211325, 0.577350, 0.788675) | 4.7320508076 | 2.998e-17 | 7.251e-09 | 4.148e-09 | 1.01 |
| 4 | (0.211325, 0.577350, 0.788675) | 4.7320508076 | 8.901e-51 | 1.244e-25 | 7.163e-26 | 1.00 |

The number of correct digits of the vector goes 0, 1, 3, 8, 25, and the eigenvalue error is about $\tan^2\theta_k$ times a constant. In double precision the implementation reaches $\|r\|_2 = 6.3 \times 10^{-16}$ after four solves. Inverse iteration with the fixed shift $4.33$ would reduce the angle by $|4.33 - 4.73| / |4.33 - 3| = 0.30$ per step and need about 30 solves for the same accuracy.

## Correctness

**Backward error on success.** When line L5 returns, $(\rho, x)$ is an exact eigenpair of $A + E$ with $E = -r x^*$ and $\|E\|_2 = \|r\|_2 \le \mathrm{tol} \, \|A\|_F$. For a Hermitian $A$, $\rho$ is real and $x^* r = 0$, so the Hermitian $E = -(r x^* + x r^*)$ also works, with $\|E\|_2 = \|r\|_2$; by [Weyl's inequality](/weyls-inequality/) some eigenvalue of $A$ lies within $\|r\|_2$ of $\rho$.

**Local cubic convergence (Hermitian $A$).** Write $x_k = \cos\theta_k \, v_j + \sin\theta_k \, w$ with a unit $w \perp v_j$. Then $|\rho_k - \lambda_j| \le \delta \sin^2\theta_k$, and one step of inverse iteration with the shift $\rho_k$ gives

$$\tan\theta_{k+1} \le \tan\theta_k \, \frac{|\lambda_j - \rho_k|}{\min_{i \ne j} |\lambda_i - \rho_k|} \le \frac{\delta \tan^3\theta_k}{\mathrm{gap}_j - \delta \sin^2\theta_k}.$$

So if $\tan^2\theta_0 < \mathrm{gap}_j / (2 \delta)$, then $\tan\theta_{k+1} \le (2 \delta / \mathrm{gap}_j) \tan^3\theta_k$ for all $k$, the angles decrease to $0$, and the residual $\|r_k\|_2 \le \delta \sin\theta_k$ falls below $\mathrm{tol} \, \|A\|_F$ after finitely many steps.

**Monotone residuals (Hermitian $A$).** For every start, $\|r_{k+1}\|_2 \le \|r_k\|_2$. This follows from the minimal property of the Rayleigh quotient and the Cauchy-Schwarz inequality. The proofs are in the proof file.

**Nonsymmetric $A$.** For a simple eigenvalue the convergence is locally quadratic, because $|\rho_k - \lambda_j|$ is only $O(\sin\theta_k)$ when the left and right eigenvectors differ (Ostrowski; Parlett 1974). The defective case is slower: for the Jordan block $J_2(2)$ the eigenvalue error halves at each step.

## Complexity

- **Per step.** A dense LU factorization of $A - \rho I$ costs $2n^3/3$ flops, the two triangular solves $2n^2$, and the products $A x$ in lines L4 and L9 another $4n^2$ (one product can be reused). For a tridiagonal $A$ a step costs $O(n)$ flops and for an upper Hessenberg $A$ $O(n^2)$; this is why RQI is applied after a reduction to those forms. Memory is $\Theta(n^2)$ for the factors of a dense $A$.
- **Number of steps (proved, Hermitian case).** Once $(2 \delta / \mathrm{gap}_j) \tan^2\theta_k \le 1/2$, the quantity $t_k = (2\delta/\mathrm{gap}_j)^{1/2} \tan\theta_k$ satisfies $t_{k+1} \le t_k^3$, so the number of further steps to reach angle $\epsilon$ is $O(\log \log (1/\epsilon))$. For $\epsilon = 10^{-16}$ and $t_k = 1/2$ that is at most 4 steps.
- **Number of steps (observed).** From a random start, the test file finds that 50 random symmetric matrices of order 2 to 10 need 3 to 8 solves, 4.6 on average, to reach a residual of $10^{-13} \|A\|_F$. No bound on the number of steps before the local regime begins is known for general starts; the global result below only says that the iteration converges.

## Properties

- **Cubic, then quadratic.** The local order is 3 for Hermitian (more generally normal) matrices and 2 for nonnormal matrices with a simple eigenvalue.
- **Global convergence for Hermitian $A$.** The residual norms decrease monotonically, and for almost every start the iteration converges to an eigenpair; the exceptional starts, which lead to an unstable two-cycle of vectors, form a set of measure zero (Kahan and Parlett; see Parlett's book, Chapter 4).
- **Hard to aim.** The eigenvalue that is found is usually, but not always, the one closest to $\rho(x_0)$. To get a specific eigenvalue, run a few steps of inverse iteration with a fixed shift first, or use [bisection](/bisection-eigenvalue-algorithm/) to isolate it.
- **Stable steps.** Each solve is backward stable, and the ill-conditioning of $A - \rho I$ affects the size of $y$ but not its direction to first order (Parlett, Chapter 4; Wilkinson 1965).

## Variants and improvements

- **Two-sided RQI.** For nonsymmetric $A$, iterate a right vector $x$ and a left vector $z$ together with the shift $z^* A x / z^* x$. Ostrowski showed that this restores cubic convergence near a simple eigenvalue; Parlett (1974) studied it further.
- **The QR algorithm.** In one step of the shifted [QR algorithm](/qr-algorithm/), $A - \sigma I = Q R$ gives $(A - \sigma I)^{-*} e_n = Q e_n / \bar r_{nn}$, so the last column of $Q$ is one step of inverse iteration on $A^*$ from $e_n$; with the shift $\sigma = h_{nn} = \rho(e_n)$ it is one step of RQI. This is why the Rayleigh shift gives cubic convergence in symmetric QR, and the [Wilkinson shift](/wilkinson-shift/) is a safer relative.
- **Inexact solves.** For large sparse $A$ the solve in line L7 is done by an iterative method to a loose tolerance. This leads to the Jacobi-Davidson method, which solves a projected correction equation instead.
- **Block RQI.** Iterate $p$ vectors with the projected matrix $X^* A X$ in place of $\rho$; this is a shifted version of [subspace iteration](/subspace-iteration/) with [Rayleigh-Ritz](/rayleigh-ritz-method/) shifts.
- **Refinement of an eigenvector.** One or two RQI steps from a computed eigenvector and its Rayleigh quotient give a correction at almost no cost if a factorization of a nearby shift is available.

## When to use it

Use RQI to refine an approximate eigenpair of a symmetric or Hermitian matrix, for example one from a coarse model, a [Lanczos](/lanczos-algorithm/) run or a previous parameter value. It is the method of choice when a few steps of factorization are cheap, as for tridiagonal or banded matrices. To find all eigenvalues of a dense matrix use the [QR algorithm](/qr-algorithm/) or the [divide-and-conquer eigensolver](/divide-and-conquer-eigensolver/); to find one eigenvalue of a known index use bisection and then [inverse iteration](/inverse-iteration/) or [MRRR](/mrrr-algorithm/); to find the dominant eigenvalue of a huge sparse matrix with no factorization use [power iteration](/power-iteration/) or Lanczos.

## Pitfalls

- **A start halfway between two eigenvectors.** For $A = \operatorname{diag}(1, 3)$ and $x_0 = (1, 1)^T$, $\rho_0 = 2$ and the solve maps $x_0$ to a multiple of $(-1, 1)^T$, which has the same Rayleigh quotient. In exact arithmetic the iteration cycles forever with $\|r\| = 1$. In floating point the rounding error grows by a factor of about 3 per step, and the test file sees it escape after about 30 steps. The same happens for $\begin{pmatrix} 2 & 1 \\ 1 & 2 \end{pmatrix}$ with $x_0$ close to $e_1$. A limit on the number of steps is needed.
- **Complex eigenvalues from a real start.** For a real $A$ and a real $x$, $\rho$ is real, so a real start can never converge to a complex eigenvalue. For the rotation-like matrix $\begin{pmatrix} 1 & -2 \\ 2 & 1 \end{pmatrix}$ a real start keeps $\rho = 1$ and $\|r\| = 2$ forever. Use a complex start.
- **Rejecting the singular solve.** Code that stops with an error when $A - \rho I$ is singular to working precision fails exactly when the iteration has converged. Replace the zero pivot, as in line L7, or test the residual first, as lines L4 and L5 do.
- **Stopping on the change of $\rho$.** The change in $\rho$ can be tiny far from convergence, for example on the two-cycle above. Test the residual.
- **The wrong eigenvalue.** The limit is not always the eigenvalue nearest $\rho(x_0)$. Code that needs a particular eigenvalue must check the result, for example with a [Sturm sequence count](/sturm-sequence-eigenvalue-count/).

## Implementations

## History

Lord Rayleigh used the quotient that bears his name in his work on vibrations in the 1870s. The iteration that feeds the quotient back as a shift was in use by the early 1950s. Alexander Ostrowski proved in a series of six papers from 1958 and 1959 that it converges cubically for symmetric matrices and quadratically in general, and introduced the two-sided version. The global convergence theory for symmetric matrices, with the monotone decrease of the residual, is due to William Kahan and Beresford Parlett and is presented in Parlett's book. Parlett's paper of 1974 treated nonnormal matrices.

## References
