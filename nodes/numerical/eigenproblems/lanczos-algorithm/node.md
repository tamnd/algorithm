---
tag: GKZVXW
kind: algorithm
slug: lanczos-algorithm
name: Lanczos algorithm
aliases:
- Lanczos iteration
- symmetric Lanczos process
- Lanczos tridiagonalization
area: numerical/eigenproblems
level: core
summary: A three-term recurrence building an orthonormal basis of the Krylov space K_k(A,b) for a symmetric A and the tridiagonal T_k = Q_k* A Q_k, whose eigenvalues approximate the extreme eigenvalues of A.
solves: [symmetric-eigenproblem]
model: floating-point-model
complexity:
  vars: {n: "the order of A", k: "the number of steps", z: "the cost of one product with A"}
  time: {no_reorth: O(k n + k z), full_reorth: O(k^2 n + k z)}
  space: {no_reorth: Θ(n), full_reorth: Θ(k n)}
  flops: {no_reorth: "9k n", full_reorth: "4k^2 n"}
  matvecs: {worst: "k"}
properties: {deterministic: true, in_place: false, recursive: false, iterative: true}
history:
  year: 1950
  people: [Cornelius Lanczos, Christopher C. Paige, Beresford N. Parlett, Jane Cullum, Ralph A. Willoughby]
  note: Lanczos proposed the method in 1950 as a way to tridiagonalize; Paige's 1971 thesis showed why it works in floating point as an iterative method.
prereqs: [krylov-subspace, rayleigh-ritz-method, symmetric-eigenproblem]
see_also: [arnoldi-iteration, implicitly-restarted-arnoldi, conjugate-gradient-method, power-iteration, block-lanczos-algorithm, cauchy-interlacing-theorem, tridiagonal-eigenproblem, minres]
sources:
  - book: isbn:9781421407944
    title: Gene H. Golub and Charles F. Van Loan, Matrix Computations, fourth edition, Johns Hopkins University Press, 2013
    locator: Sections 10.1 (the Lanczos process and the Kaniel-Paige-Saad bound) and 10.3 (practical Lanczos procedures and reorthogonalization)
  - book: isbn:9780898713619
    title: Lloyd N. Trefethen and David Bau III, Numerical Linear Algebra, SIAM, 1997
    locator: Lecture 36, The Lanczos Iteration
  - book: isbn:9780898714029
    title: Beresford N. Parlett, The Symmetric Eigenvalue Problem, SIAM Classics in Applied Mathematics 20, 1998
    locator: Chapter 13, Lanczos Algorithms (the simple Lanczos algorithm, Paige's theorem, selective orthogonalization)
  - book: isbn:9781611970722
    title: Yousef Saad, Numerical Methods for Large Eigenvalue Problems, revised edition, SIAM Classics in Applied Mathematics 66, 2011
    locator: Chapter 6, Krylov Subspace Methods (Section 6.6 on the Hermitian Lanczos algorithm, Section 6.7 on convergence)
  - book: isbn:9780898714715
    title: Zhaojun Bai, James Demmel, Jack Dongarra, Axel Ruhe and Henk van der Vorst (eds.), Templates for the Solution of Algebraic Eigenvalue Problems, SIAM, 2000
    locator: Section 4.4, Lanczos Method
  - paper: doi:10.6028/jres.045.026
    title: Cornelius Lanczos, An iteration method for the solution of the eigenvalue problem of linear differential and integral operators, Journal of Research of the National Bureau of Standards 45(4), 1950
    locator: pp. 255 to 282
  - paper: "C. C. Paige, Accuracy and effectiveness of the Lanczos algorithm for the symmetric eigenproblem, Linear Algebra and its Applications 34, 1980, pp. 235 to 258"
    title: C. C. Paige, Accuracy and effectiveness of the Lanczos algorithm for the symmetric eigenproblem
    locator: the floating-point analysis and the link between loss of orthogonality and convergence
---

The Lanczos algorithm builds, for a Hermitian matrix $A$ and a start vector $b$, an orthonormal basis $q_1, \dots, q_k$ of the [Krylov space](/krylov-subspace/) $K_k(A, b)$ by a three-term recurrence, together with the real symmetric tridiagonal matrix $T_k = Q_k^* A Q_k$. The eigenvalues of $T_k$, the Ritz values, approximate the eigenvalues of $A$, the extreme ones first and fast. Each step needs one product $A q_j$ and $O(n)$ more work, so the method suits large sparse matrices that are accessed only through products. It is the [Arnoldi iteration](/arnoldi-iteration/) for a Hermitian matrix, where symmetry makes the Hessenberg matrix tridiagonal and the long recurrence short.

## In plain words

Start with a vector, multiply it by the matrix again and again, and look for the best answer among all combinations of the vectors you get. That set of combinations grows by one direction per product. The method keeps an orthonormal basis of it, and for a symmetric matrix each new basis vector needs only the two previous ones. So it can run with almost no memory.

In this basis the matrix becomes small and tridiagonal. The eigenvalues of the small matrix approximate the largest and smallest eigenvalues of the big one well after a number of steps far below its size. In floating point the basis slowly loses its orthogonality. Converged eigenvalues then come back as extra copies, unless the basis is orthogonalized again.

## The problem

**Notation.** $A = A^* \in \mathbb{C}^{n \times n}$ with eigenvalues $\lambda_1 \ge \dots \ge \lambda_n$ and orthonormal eigenvectors $v_i$. $b \ne 0$ is the start vector. $Q_k = [q_1, \dots, q_k]$, and $T_k$ has the diagonal $\alpha_1, \dots, \alpha_k$ and the off-diagonal $\beta_1, \dots, \beta_{k-1}$. The Ritz pairs are $(\theta_i, y_i = Q_k s_i)$ with $T_k s_i = \theta_i s_i$ and $\theta_1 \ge \dots \ge \theta_k$. $u$ is the unit roundoff.

Given a routine for $x \mapsto A x$, $b$ and $k$, compute $T_k$, $Q_k$ and the Ritz pairs with their residual norms. This gives some eigenvalues of the [symmetric eigenproblem](/symmetric-eigenproblem/) by the [Rayleigh-Ritz method](/rayleigh-ritz-method/) on $K_k(A, b)$.

## The algorithm

```pseudo id=main
LANCZOS(A, b, k)
L1  β₀ ← 0;  q₀ ← 0;  q₁ ← b / ‖b‖₂
L2  for j ← 1 to k do
L3      w ← A qⱼ − βⱼ₋₁ qⱼ₋₁
L4      αⱼ ← qⱼ* w;  w ← w − αⱼ qⱼ
L5      (optional) w ← w − Qⱼ (Qⱼ* w), twice          ▷ full reorthogonalization
L6      βⱼ ← ‖w‖₂;  if βⱼ = 0 then stop                ▷ K_j(A, b) is invariant
L7      qⱼ₊₁ ← w / βⱼ
L8  compute T_k sᵢ = θᵢ sᵢ;  return θᵢ, yᵢ = Q_k sᵢ and the residuals βₖ |e_kᵀ sᵢ|
```

Lines L3 and L4 subtract the components along $q_{j-1}$ and $q_j$; by symmetry $w$ is then orthogonal to all earlier $q_i$ in exact arithmetic. Line L5 enforces this in floating point. Without it the method needs only three vectors of length $n$, but $Q_k$ must then be kept or recomputed for the Ritz vectors. The residual of line L8 is computed from $T_k$ alone, without any product with $A$.

## Example

Let $A = \operatorname{diag}(1, 2, \dots, 100)$ and $b = (1, \dots, 1)^T$, so $\lambda_1 = 100$ and $\lambda_{100} = 1$. With full reorthogonalization, the error $\lambda_1 - \theta_1$ is:

| $k$ | 5 | 10 | 20 | 30 | 40 |
|---|---|---|---|---|---|
| $\lambda_1 - \theta_1$ | 4.205216 | 0.862128 | 0.050398 | $6.42 \times 10^{-4}$ | $7.15 \times 10^{-7}$ |
| bound of Theorem 4 | 5430 | 986 | 18.4 | 0.326 | 0.00577 |

The spectrum is symmetric about 50.5, so $\theta_k - 1$ is the same as $\lambda_1 - \theta_1$. Forty products give seven digits of both extreme eigenvalues of a matrix of order 100. The Chebyshev bound has $\gamma_1 = 1/98$ and $\tan^2\phi_1 = 99$. It is correct but pessimistic here, because it ignores the even spacing of the other eigenvalues. Power iteration converges at the rate $(99/100)^{2k}$, so after 40 products its error is still about 0.45 of the initial error.

Loss of orthogonality. Take $A = \operatorname{diag}(1, 2, \dots, 29, 60)$ and $b = (1, \dots, 1)^T$, without line L5. Then $T_{30}$ already has two eigenvalues within $10^{-8}$ of 60, $T_{60}$ has four and $T_{80}$ six. The largest value of $|q_1^T q_j|$ reaches 0.48. With line L5, $T_{30}$ has one such eigenvalue, as exact arithmetic predicts.

## Correctness

The full proof is in [proofs/correctness.md](proofs/correctness.md).

1. **Basis and projection.** In exact arithmetic $q_1, \dots, q_k$ are orthonormal and span $K_k(A, b)$, and $A Q_k = Q_k T_k + \beta_k q_{k+1} e_k^T$. Symmetry makes $w$ orthogonal to $q_1, \dots, q_{j-2}$ without explicit work.
2. **Termination.** The recurrence breaks down, $\beta_m = 0$, exactly at the number $m$ of distinct eigenvalues whose eigenspaces $b$ touches. Then $K_m$ is invariant and $T_m$ has exactly these eigenvalues, so at most $n$ steps are possible.
3. **Ritz residuals.** $\|A y_i - \theta_i y_i\|_2 = \beta_k |e_k^T s_i|$, and an eigenvalue of $A$ lies within this distance of $\theta_i$.
4. **Convergence.** $\theta_1^{(k)} = \max_{x \in K_k} \rho(x)$ increases with $k$, and the Kaniel-Paige-Saad bound gives $\lambda_1 - \theta_1^{(k)} \le (\lambda_1 - \lambda_n) (\tan\phi_1 / C_{k-1}(1 + 2\gamma_1))^2$ with $\gamma_1 = (\lambda_1 - \lambda_2)/(\lambda_2 - \lambda_n)$. The same holds for $\lambda_n$ from the other end. The interior Ritz values satisfy weaker bounds of the same kind.
5. **Floating point.** Paige proved that the computed recurrence holds up to $O(u\|A\|)$, and that the $q_j$ lose orthogonality only in the directions of converged Ritz vectors. The Ritz values are still accurate; the cost is extra copies of converged ones.

## Complexity

- **Products.** One product with $A$ per step, $k$ in total; at a cost $z$ each, which is about two flops per nonzero of a sparse matrix.
- **Without reorthogonalization.** About $9n$ more flops per step: two vector updates, one inner product, one norm and one scaling. Storage is three vectors if only eigenvalues are wanted.
- **With full reorthogonalization.** Two passes of classical Gram-Schmidt cost $8nj$ flops at step $j$, $4nk^2$ in total, and $Q_k$ takes $kn$ storage.
- **The small problem.** The eigenvalues of $T_k$ cost $O(k^2)$ by bisection or the tridiagonal QR algorithm, and the Ritz vectors $Q_k s_i$ cost $2nk$ flops each.
- **Number of steps.** The bound of Theorem 4 is proved. The number of steps to reach a tolerance in practice depends on the spectrum and is observed. Isolated extreme eigenvalues converge first, and clustered or interior eigenvalues need many more steps, or shift-and-invert.

## Properties

- **Krylov optimality.** Among all vectors of $K_k(A, b)$, the Ritz values are the [Rayleigh-Ritz](/rayleigh-ritz-method/) approximations, and the extreme ones are the best possible values of the [Rayleigh quotient](/rayleigh-quotient/) there.
- **Interlacing.** $T_k$ is a leading block of $T_{k+1}$, so the Ritz values of consecutive steps interlace ([Cauchy interlacing](/cauchy-interlacing-theorem/)). Each extreme Ritz value moves monotonically toward the extreme eigenvalue.
- **Short recurrence.** Only two previous vectors are needed, unlike Arnoldi; the memory and work per step stay constant.
- **Simple Ritz values.** In exact arithmetic $T_k$ is unreduced, so its eigenvalues are distinct. Lanczos therefore finds only one copy of a multiple eigenvalue, and block versions are needed to find its multiplicity.
- **Link with conjugate gradients.** For a positive definite $A$, the [conjugate gradient method](/conjugate-gradient-method/) is Lanczos with an implicit $LDL^T$ factorization of $T_k$, and [MINRES](/minres/) uses its QR factorization.

## Variants and improvements

- **Selective reorthogonalization** (Parlett and Scott, 1979): orthogonalize only against converged Ritz vectors, which by Paige's theorem are the only directions that need it.
- **Partial reorthogonalization** (Simon, 1984): estimate the loss of orthogonality by a recurrence and reorthogonalize only when it exceeds $\sqrt{u}$.
- **No reorthogonalization** (Cullum and Willoughby, 1985): run far past $n$ steps and identify the ghost copies by comparing $T_k$ with $T_k$ with its first row and column deleted.
- **Restarting.** [Implicitly restarted](/implicitly-restarted-arnoldi/) Lanczos (Sorensen; ARPACK) and thick restart (Wu and Simon, 2000) keep the memory bounded while filtering out unwanted directions.
- **Block Lanczos** ([block Lanczos](/block-lanczos-algorithm/)): start from several vectors to find multiple and clustered eigenvalues.
- **Shift-and-invert.** Apply Lanczos to $(A - \sigma I)^{-1}$ to find eigenvalues near $\sigma$; this needs one sparse factorization.
- **Nonsymmetric Lanczos.** Two biorthogonal sequences give a tridiagonal but non-symmetric $T_k$. This is the basis of the [biconjugate gradient method](/biconjugate-gradient/), and it can break down without an invariant subspace.

## When to use it

Use Lanczos for a few extreme eigenvalues of a large sparse or structured Hermitian matrix, for example the smallest eigenvalues of a graph Laplacian, a discretized differential operator or a Hamiltonian. Use shift-and-invert for interior eigenvalues. For dense matrices of moderate size, or when all eigenvalues are wanted, use [tridiagonalization](/tridiagonalization/) and a dense solver. For a non-Hermitian matrix use the [Arnoldi iteration](/arnoldi-iteration/).

## Pitfalls

- **Trusting $Q_k$ without reorthogonalization.** The $q_j$ can lose all orthogonality, and Ritz vectors computed from them are then not orthogonal. Ghost copies can also look like multiple eigenvalues.
- **A start vector orthogonal to the wanted eigenvector.** Then the eigenvalue is invisible in exact arithmetic. For the Toeplitz matrix $\operatorname{tridiag}(-1, 2, -1)$ of even order, $b = (1, \dots, 1)^T$ is orthogonal to the top eigenvector. Lanczos then stops after $n/2$ steps without it. Use a random start vector.
- **Testing $\beta_j$ against zero exactly.** Exact breakdown is rare in floating point; use a relative tolerance. A small $\beta_j$ is good news, an invariant subspace, not an error.
- **Stopping on the change in $\theta_i$.** Use the residual $\beta_k |e_k^T s_i|$ of line L8 instead; it is a computable bound.
- **Non-Hermitian $A$.** The three-term recurrence is then wrong, and the $q_j$ are not orthogonal even in exact arithmetic.

## Implementations

## History

Cornelius Lanczos published the method in 1950 as a way to reduce a matrix to tridiagonal form, the "method of minimized iterations", together with the nonsymmetric two-sided version. In floating point the vectors lost orthogonality, and Householder's method became the preferred finite reduction. In his 1971 thesis Christopher Paige showed that the loss of orthogonality comes with convergence, and that the method is a powerful iterative method when it runs for fewer steps than $n$. Kaniel (1966), Paige (1971) and Saad (1980) gave the convergence bounds. Parlett and Scott (1979), Simon (1984) and Cullum and Willoughby (1985) made it practical. Sorensen's implicit restart (1992) and the ARPACK code (Lehoucq, Sorensen and Yang, 1998) made it a standard tool for large problems.

## References
