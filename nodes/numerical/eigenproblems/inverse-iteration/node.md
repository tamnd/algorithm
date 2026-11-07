---
tag: GR2E1P
kind: algorithm
slug: inverse-iteration
name: Inverse iteration
aliases:
- inverse power method
- Wielandt iteration
- shifted inverse iteration
area: numerical/eigenproblems
level: core
summary: Power iteration on (A − σI)⁻¹. It converges to the eigenvector of the eigenvalue nearest the shift σ, at the rate of the ratio of the nearest and second nearest distances to σ.
solves: [eigenvalue-problem]
model: floating-point-model
complexity:
  vars: {n: "the order of A", k: "the number of steps"}
  time: {worst: O(n^3 + k n^2)}
  space: {extra: Θ(n^2)}
  flops: {worst: "2n^3/3 + 4k n^2 + O(k n)", tridiagonal: "O(k n)"}
properties: {deterministic: true, in_place: false, recursive: false, iterative: true}
history:
  year: 1944
  people: [Helmut Wielandt]
  note: Ipsen's survey credits the method to Wielandt (1944). Wilkinson made it the standard way to get eigenvectors from computed eigenvalues.
prereqs: [power-iteration, lup-decomposition, eigenvector]
see_also: [rayleigh-quotient-iteration, power-iteration, bisection-eigenvalue-algorithm, rayleigh-quotient, deflation, mrrr-algorithm, residual, eigenvalue-condition-number]
sources:
  - paper: doi:10.1137/S0036144596300773
    title: Ilse C. F. Ipsen, Computing an eigenvector with inverse iteration, SIAM Review 39(2), 1997
    locator: pp. 254 to 291 (the history, the residual and backward error, why ill-conditioned solves do no harm, and the choice of the start vector)
  - paper: doi:10.1137/1021052
    title: G. Peters and J. H. Wilkinson, Inverse iteration, ill-conditioned equations and Newton's method, SIAM Review 21(3), 1979
    locator: pp. 339 to 360
  - book: isbn:9781421407944
    title: Gene H. Golub and Charles F. Van Loan, Matrix Computations, fourth edition, Johns Hopkins University Press, 2013
    locator: Section 7.6.1 (selected eigenvectors via inverse iteration) and Section 8.2 (power iterations for symmetric matrices)
  - book: isbn:9780898713619
    title: Lloyd N. Trefethen and David Bau III, Numerical Linear Algebra, SIAM, 1997
    locator: Lecture 27, Rayleigh Quotient, Inverse Iteration (Theorem 27.2 on the convergence rate)
  - book: "J. H. Wilkinson, The Algebraic Eigenvalue Problem, Oxford University Press, 1965"
    title: J. H. Wilkinson, The Algebraic Eigenvalue Problem
    locator: Chapter 9, Iterative methods (inverse iteration and its error analysis)
---

Inverse iteration computes an [eigenvector](/eigenvector/) of a square matrix $A$ for the [eigenvalue](/eigenvalue/) nearest a given shift $\sigma$. It is [power iteration](/power-iteration/) applied to $(A - \sigma I)^{-1}$, whose dominant eigenvalue is $1/(\lambda_J - \sigma)$ for the eigenvalue $\lambda_J$ closest to $\sigma$. The direction converges linearly with the ratio $|\lambda_J - \sigma| / |\lambda_K - \sigma|$, where $\lambda_K$ is the second closest eigenvalue, so a shift close to $\lambda_J$ gives a ratio near zero and convergence in one to three steps. It is the standard way to get eigenvectors once the eigenvalues are known, for example after [bisection](/bisection-eigenvalue-algorithm/).

## In plain words

Repeated multiplication by a matrix turns almost every vector toward the direction with the largest stretch. Inverse iteration uses this trick on a different matrix. It subtracts a guess from the diagonal and then undoes the matrix, by solving a linear system instead of multiplying. Undoing the matrix turns the smallest stretch into the largest one. After the subtraction, the smallest stretch belongs to the eigenvalue nearest the guess. So each solve pulls the vector toward the direction for the eigenvalue nearest the guess, and the closer the guess, the stronger the pull.

The system to solve is close to singular when the guess is good. This seems dangerous, but the error that rounding makes lies almost entirely along the wanted direction, so it is harmless.

## The problem

**Notation.** $A \in \mathbb{C}^{n \times n}$ with eigenvalues $\lambda_1, \dots, \lambda_n$ and eigenvectors $v_i$; $\sigma \in \mathbb{C}$ is the shift; $\lambda_J$ is the eigenvalue nearest $\sigma$ and $\lambda_K$ the next nearest one that is different from $\lambda_J$. The ratio is $r = |\lambda_J - \sigma| / |\lambda_K - \sigma|$. The Rayleigh quotient is $\rho(x) = x^* A x / x^* x$ and $u$ is the unit roundoff.

Given $A$, $\sigma$, a start vector $x_0$, a tolerance $\mathrm{tol}$ and a step limit $\mathrm{kmax}$, return a unit vector $x$ and $\theta = \rho(x)$ with $\|A x - \theta x\|_2 \le \mathrm{tol} \cdot \|A\|_F$ and the flag CONVERGED, or the last iterate and NOT-CONVERGED. The method is meant for the case where $\lambda_J$ is the unique nearest eigenvalue, $r < 1$.

## The algorithm

```pseudo id=main
INVERSE-ITERATION(A, σ, x₀, tol, kmax)
L1  factor P (A − σI) = L U                 ▷ once; a zero pivot becomes u ‖A‖_F
L2  x ← x₀ / ‖x₀‖₂
L3  for k ← 1 to kmax do
L4      solve (A − σI) y = x  with L and U
L5      x ← y / ‖y‖₂
L6      θ ← x* A x                          ▷ the Rayleigh quotient of the unit vector x
L7      r ← A x − θ x
L8      if ‖r‖₂ ≤ tol · ‖A‖_F then return (θ, x, CONVERGED)
L9  return (θ, x, NOT-CONVERGED)
```

The factorization of line L1 is done once, so each step costs only two triangular solves. If $\sigma$ is exactly an eigenvalue in floating point, a pivot becomes zero; replacing it by $u \|A\|_F$ is the same as moving $\sigma$ by a rounding-level amount, and the method then works as usual. Lines L6 and L7 are the stopping test: the residual of a unit vector is its backward error. A code that only needs the vector can skip L6 and use the cheaper test $1/\|y\|_2 \le \mathrm{tol} \cdot \|A\|_F$, which bounds the residual of the pair $(\sigma, x)$.

## Example

Let $A$ be the $4 \times 4$ tridiagonal matrix with 2 on the diagonal and $-1$ beside it. Its eigenvalues are $2 - 2\cos(k\pi/5)$: about $0.381966$, $1.381966$, $2.618034$ and $3.618034$. Take $\sigma = 1.3$ and $x_0 = e_1$. The nearest eigenvalue is $\lambda_J = 1.381966$, at distance $0.081966$; the next is $0.381966$, at distance $0.918034$. So $r = 0.089284$.

| $k$ | $\theta_k$ | $\lvert\theta_k - \lambda_J\rvert$ | $\sin\angle(x_k, v_J)$ | ratio of sines | $\lVert A x_k - \theta_k x_k \rVert_2$ |
|---|---|---|---|---|---|
| 1 | 1.384748769682 | $2.78 \times 10^{-3}$ | $8.57 \times 10^{-2}$ | | $1.06 \times 10^{-1}$ |
| 2 | 1.381961560807 | $4.45 \times 10^{-6}$ | $6.31 \times 10^{-3}$ | 0.0737 | $7.08 \times 10^{-3}$ |
| 3 | 1.381965890919 | $1.20 \times 10^{-7}$ | $5.02 \times 10^{-4}$ | 0.0796 | $5.34 \times 10^{-4}$ |
| 4 | 1.381966009986 | $1.26 \times 10^{-9}$ | $4.20 \times 10^{-5}$ | 0.0837 | $4.35 \times 10^{-5}$ |
| 5 | 1.381966011239 | $1.12 \times 10^{-11}$ | $3.63 \times 10^{-6}$ | 0.0863 | $3.69 \times 10^{-6}$ |
| 6 | 1.381966011250 | $9.35 \times 10^{-14}$ | $3.18 \times 10^{-7}$ | 0.0877 | $3.21 \times 10^{-7}$ |

The ratio of successive sines tends to $r = 0.0893$, and the eigenvalue error falls like the square of the sine, as the theory for a symmetric matrix predicts. With the default tolerance $10 n u$ the implementation stops after 13 steps. The start $x_0 = (1, 1, 1, 1)^T$ would be a bad choice here: it is orthogonal to $v_J = (\sin(2j\pi/5))_{j=1}^4$, so in exact arithmetic the iteration would converge to the eigenvector of $0.381966$ instead.

## Correctness

The full proof is in [proofs/correctness.md](proofs/correctness.md). Line L4 computes $(A - \sigma I)^{-1} x$, so $x_k$ is the unit vector along $(A - \sigma I)^{-k} x_0$. The matrix $(A - \sigma I)^{-1}$ has the eigenvalues $\mu_i = 1/(\lambda_i - \sigma)$ with the eigenvectors $v_i$, and $\lambda_J$ gives the largest $|\mu_i|$.

1. **Convergence.** If $A$ is diagonalizable, $\lambda_J$ is the unique nearest eigenvalue and $x_0$ has a nonzero component along its eigenspace, then $\sin\angle(x_k, \operatorname{null}(A - \lambda_J I)) \le C r^k / (1 - C r^k)$, with $C$ set by the start vector. The convergence is linear with the rate $r$, and the rate is attained when $x_0$ has a component along $v_K$.
2. **Eigenvalue estimate.** For a Hermitian $A$ and a simple $\lambda_J$, $|\theta_k - \lambda_J| \le (\lambda_{\max} - \lambda_{\min}) \sin^2\angle(x_k, v_J)$, so the eigenvalue converges at the rate $r^2$ (Trefethen and Bau, Theorem 27.2).
3. **What the answer means.** On return with CONVERGED, $(\theta, x)$ is an exact eigenpair of $A + E$ with $E = -r x^*$ and $\|E\|_2 \le \mathrm{tol} \cdot \|A\|_F$.

**Floating point.** The computed $\hat y$ solves $(A - \sigma I + E)\hat y = x$ with $\|E\|_2$ of order $n u \rho_n \|A\|_2$, where $\rho_n$ is the growth factor of the LU factorization. So the unit vector $\hat x$ satisfies $\|(A - \sigma I)\hat x\|_2 \le 1/\|\hat y\|_2 + \|E\|_2$. When $\sigma$ is within $O(u \|A\|)$ of an eigenvalue, as it is after a backward stable eigenvalue solver, $\|\hat y\|_2$ is of order $1/(u\|A\|)$ and one step already gives a backward stable eigenvector. The near singularity of $A - \sigma I$ is what makes this work (Peters and Wilkinson 1979; Ipsen 1997). The forward error of $x$ is still bounded only by the residual over the gap between $\lambda_J$ and the rest of the spectrum ([Davis-Kahan](/davis-kahan-theorem/) for Hermitian $A$).

## Complexity

- **Dense matrix.** The LU factorization with partial pivoting costs $2n^3/3$ flops (real arithmetic). Each step does two triangular solves ($2n^2$ flops) and one product $A x$ ($2n^2$ flops) for the residual. With $k$ steps the total is $2n^3/3 + 4kn^2 + O(kn)$ flops.
- **Hessenberg or tridiagonal matrix.** If $A$ is first reduced to [Hessenberg form](/hessenberg-reduction/) $H$, the factorization of $H - \sigma I$ costs $O(n^2)$ and each step $O(n^2)$. For a symmetric tridiagonal matrix both are $O(n)$, so $k$ steps cost $O(kn)$ flops; this is why bisection plus inverse iteration is cheap for a few eigenvectors.
- **Number of steps.** To reach a sine of $\varepsilon$ from a start with $C = O(1)$ takes about $\log(1/\varepsilon) / \log(1/r)$ steps. With a shift from a backward stable eigenvalue solver, one or two steps are typical; that count is observed, not proved, since it depends on the start vector.
- **Space.** $\Theta(n^2)$ for the factors of a dense matrix, $\Theta(n)$ for a tridiagonal one.

## Properties

- **Linear convergence with a tunable rate.** The rate $r$ goes to 0 as $\sigma \to \lambda_J$.
- **Finds interior eigenvalues.** Unlike power iteration, it reaches any eigenvalue, not only the largest in modulus.
- **One factorization.** The shift is fixed, so the matrix is factored once. [Rayleigh quotient iteration](/rayleigh-quotient-iteration/) changes the shift at each step and converges cubically for Hermitian matrices, but needs a new factorization each step.
- **Complex shifts for complex eigenvalues.** A real shift is equally far from $\lambda$ and $\bar\lambda$, so for a conjugate pair the real iteration does not converge; use complex arithmetic and a complex shift.

## Variants and improvements

- **Rayleigh quotient iteration.** Use $\sigma_k = \rho(x_k)$ as the shift of step $k + 1$.
- **Inverse subspace iteration.** Iterate on a block of $p$ vectors with orthonormalization to get the $p$ eigenvalues nearest $\sigma$, or a basis of an invariant subspace for a cluster.
- **Shift and invert in Krylov methods.** Running [Lanczos](/lanczos-algorithm/) or [Arnoldi](/arnoldi-iteration/) on $(A - \sigma I)^{-1}$ finds many eigenvalues near $\sigma$ at once; inverse iteration is the one-vector case.
- **Generalized problems.** For $A x = \lambda B x$, solve $(A - \sigma B) y = B x$ at each step.
- **Clusters and reorthogonalization.** When several computed eigenvalues are close, the vectors from inverse iteration may not be orthogonal; LAPACK's `xSTEIN` reorthogonalizes them against each other with Gram-Schmidt, and the [MRRR algorithm](/mrrr-algorithm/) avoids this cost with relatively robust representations.

## When to use it

Use it to get one or a few eigenvectors when good eigenvalue estimates are already known, especially for a tridiagonal or Hessenberg matrix where each step is cheap. Use it with a shift from a target region to find the eigenvalue of a large sparse matrix nearest that region, when a sparse factorization of $A - \sigma I$ is affordable. Do not use it to compute all eigenvectors of a matrix with tight clusters; use a method that returns an orthonormal set, such as the QR algorithm, [divide and conquer](/divide-and-conquer-eigensolver/) or MRRR.

## Pitfalls

- **A start vector without the wanted component.** If $x_0$ is orthogonal to the eigenvector (in the sense $P x_0 = 0$), the iteration converges to another eigenvector in exact arithmetic, and only rounding brings the wanted one back, slowly. Random start vectors avoid this with probability 1.
- **Two eigenvalues at the same distance.** If $|\lambda_J - \sigma| = |\lambda_K - \sigma|$ for $\lambda_J \neq \lambda_K$, then $r = 1$ and the iterates do not converge; they keep turning inside the span of the two eigenvectors. A real shift for a complex pair is a case of this.
- **Fear of the singular system.** Do not move $\sigma$ away from the eigenvalue to make $A - \sigma I$ well conditioned; that slows the method down. Only an exactly zero pivot needs a fix.
- **A stopping test on successive iterates.** $\|x_k - x_{k-1}\|$ can stay large when the eigenvector has a sign or phase that flips (for example when $\lambda_J - \sigma < 0$ the sign alternates). Test the residual.
- **Close eigenvalues.** The residual can be tiny while the vector is far from the true eigenvector, when another eigenvalue is close to $\lambda_J$; the error bound is the residual over the gap.
- **Defective eigenvalues.** For a Jordan block the convergence is only like $1/k$ for a fixed shift, since $(J - \sigma I)^{-k}$ has a term growing like $k$; with $\sigma$ very close to the eigenvalue the first step still gives a small residual.

## Implementations

## History

Ipsen's survey credits inverse iteration to Helmut Wielandt, who described it in 1944 in a report on the computation of eigenvalues by fractional iteration. Wilkinson analysed it in detail in the 1950s and 1960s, showed why the ill conditioning of $A - \sigma I$ does no harm, and made it the standard way to get eigenvectors of tridiagonal and Hessenberg matrices from computed eigenvalues (Wilkinson 1965, Chapter 9; Peters and Wilkinson 1979). It is the eigenvector part of the bisection and inverse iteration routines of EISPACK and LAPACK.

## References
