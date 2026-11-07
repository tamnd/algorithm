---
tag: 1X1DGA
kind: algorithm
slug: arnoldi-iteration
name: Arnoldi iteration
aliases:
- Arnoldi process
- Arnoldi method
area: numerical/eigenproblems
level: advanced
summary: Gram-Schmidt on the Krylov vectors b, Ab, A^2 b, ... of a general matrix. It gives an orthonormal basis Q_k and the Hessenberg H_k = Q_k* A Q_k, whose eigenvalues approximate outer eigenvalues of A.
solves: [nonsymmetric-eigenproblem]
model: floating-point-model
complexity:
  vars: {n: "the order of A", k: "the number of steps", z: "the cost of one product with A"}
  time: {worst: O(k^2 n + k z)}
  space: {worst: Θ(k n)}
  flops: {mgs: "2k^2 n", reorth: "4k^2 n"}
  matvecs: {worst: "k"}
properties: {deterministic: true, in_place: false, recursive: false, iterative: true}
history:
  year: 1951
  people: [Walter E. Arnoldi, Yousef Saad]
  note: Arnoldi proposed the process in 1951 as a way to reduce a matrix to Hessenberg form; Saad's 1980 paper made it an iterative method for a few eigenvalues of a large matrix.
prereqs: [krylov-subspace, gram-schmidt-process, rayleigh-ritz-method, hessenberg-reduction]
see_also: [lanczos-algorithm, implicitly-restarted-arnoldi, gmres, power-iteration, nonsymmetric-eigenproblem, pseudospectrum, subspace-iteration, eigenvalue-condition-number]
sources:
  - book: isbn:9780898713619
    title: Lloyd N. Trefethen and David Bau III, Numerical Linear Algebra, SIAM, 1997
    locator: Lecture 33, The Arnoldi Iteration, and Lecture 34, How Arnoldi Locates Eigenvalues (the polynomial minimization property)
  - book: isbn:9781611970722
    title: Yousef Saad, Numerical Methods for Large Eigenvalue Problems, revised edition, SIAM Classics in Applied Mathematics 66, 2011
    locator: Chapter 6, Krylov Subspace Methods (Arnoldi's method, its practical implementations and its convergence)
  - book: isbn:9781421407944
    title: Gene H. Golub and Charles F. Van Loan, Matrix Computations, fourth edition, Johns Hopkins University Press, 2013
    locator: Section 10.5, Large Sparse Unsymmetric Problems (the Arnoldi factorization and its relation to Hessenberg reduction)
  - book: isbn:9780898714715
    title: Zhaojun Bai, James Demmel, Jack Dongarra, Axel Ruhe and Henk van der Vorst (eds.), Templates for the Solution of Algebraic Eigenvalue Problems, SIAM, 2000
    locator: Chapter 7, Non-Hermitian Eigenvalue Problems (the Arnoldi method and its restarted forms)
  - paper: doi:10.1090/qam/42792
    title: W. E. Arnoldi, The principle of minimized iterations in the solution of the matrix eigenvalue problem, Quarterly of Applied Mathematics 9, 1951
    locator: pp. 17 to 29
  - paper: "Y. Saad, Variations on Arnoldi's method for computing eigenelements of large unsymmetric matrices, Linear Algebra and its Applications 34, 1980, pp. 269 to 295"
    title: Y. Saad, Variations on Arnoldi's method for computing eigenelements of large unsymmetric matrices
    locator: the Arnoldi method as an iterative projection method, and its convergence analysis
---

The Arnoldi iteration applies [Gram-Schmidt](/gram-schmidt-process/) orthogonalization to the [Krylov](/krylov-subspace/) vectors $b, Ab, A^2 b, \dots$ of a general square matrix $A$, one product with $A$ per step. After $k$ steps it gives an orthonormal basis $Q_k$ of $K_k(A, b)$ and a $k \times k$ upper Hessenberg matrix $H_k = Q_k^* A Q_k$. The eigenvalues of $H_k$, the Ritz values, approximate the outer eigenvalues of $A$, often well after $k \ll n$ steps. The cost is $k$ products with $A$ and about $2k^2 n$ flops of orthogonalization, so a restart is needed when $k$ grows.

## In plain words

Pick a starting vector and multiply it by the matrix again and again. The vectors you get span a growing space. Arnoldi builds a set of perpendicular unit vectors for that space, one new vector per product, by removing from each new product its parts along all earlier vectors.

The numbers removed form a small table. Its own special values approximate those of the big matrix, first the ones far out from the rest. The method only needs a way to multiply by the matrix, so it works for very large sparse matrices. Its weak point is that each step costs more than the previous one, because every earlier vector must be removed again.

## The problem

**Notation.** $A \in \mathbb{C}^{n \times n}$ with eigenvalues $\lambda_1, \dots, \lambda_n$, ordered $|\lambda_1| \ge \dots \ge |\lambda_n|$. $b \ne 0$ is the start vector and $K_k(A, b) = \operatorname{span}\{b, Ab, \dots, A^{k-1} b\}$. $Q_k = [q_1, \dots, q_k]$ has orthonormal columns. $\bar H_k$ is the $(k+1) \times k$ upper Hessenberg matrix of the coefficients $h_{ij}$, and $H_k$ is its first $k$ rows. A Ritz pair is $(\theta, Q_k y)$ with $H_k y = \theta y$ and $\|y\|_2 = 1$. $u$ is the unit roundoff.

Given a routine for $x \mapsto A x$, $b$ and $k$, compute $Q_{k+1}$ and $\bar H_k$ with the Arnoldi relation
$$A Q_k = Q_{k+1} \bar H_k = Q_k H_k + h_{k+1,k}\, q_{k+1} e_k^T,$$
and the Ritz pairs with their residual norms. This gives a few eigenvalues of the [nonsymmetric eigenproblem](/nonsymmetric-eigenproblem/), usually those of largest modulus or largest real part. Run to $k = n$ without breakdown, it is an orthogonal [Hessenberg reduction](/hessenberg-reduction/) $Q^* A Q = H$ with $Q e_1 = b / \|b\|_2$.

## The algorithm

```pseudo id=main
ARNOLDI(A, b, k)
L1  q₁ ← b / ‖b‖₂
L2  for j ← 1 to k do
L3      w ← A qⱼ
L4      for i ← 1 to j do                              ▷ modified Gram-Schmidt
L5          hᵢⱼ ← qᵢ* w;  w ← w − hᵢⱼ qᵢ
L6      (optional) repeat L4 and L5 once, adding to hᵢⱼ  ▷ reorthogonalization
L7      hⱼ₊₁,ⱼ ← ‖w‖₂
L8      if hⱼ₊₁,ⱼ ≤ tol then return Qⱼ, Hⱼ             ▷ K_j(A, b) is invariant
L9      qⱼ₊₁ ← w / hⱼ₊₁,ⱼ
L10 return Q_{k+1}, H̄_k
L11 compute H_k yᵢ = θᵢ yᵢ with ‖yᵢ‖₂ = 1
L12 xᵢ ← Q_k yᵢ
L13 return θᵢ, xᵢ and the residuals hₖ₊₁,ₖ |e_kᵀ yᵢ|
```

Lines L4 and L5 remove from $A q_j$ its components along every earlier $q_i$. This is modified Gram-Schmidt: each coefficient uses the current $w$, not the original $A q_j$, which is more stable in floating point. Line L6 is a second pass. It changes nothing in exact arithmetic and keeps the $q_j$ orthogonal to working accuracy in floating point. The implementation uses the tolerance $10\, n\, u \max_j \|A q_j\|_2$ in line L8. Lines L11 to L13 are the Rayleigh-Ritz step. The implementation computes the eigenvalues of the small Hessenberg matrix by a complex shifted [QR algorithm](/qr-algorithm/) and each $y_i$ by inverse iteration.

## Example

Let $A$ be the $100 \times 100$ upper bidiagonal matrix with diagonal $1, 2, \dots, 100$ and every superdiagonal entry 1, and $b = (1, \dots, 1)^T$. $A$ is not normal. Its eigenvalues are $1, \dots, 100$, all simple. With reorthogonalization, the largest Ritz value $\theta_1$ gives:

| $k$ | 5 | 10 | 20 | 30 | 40 |
|---|---|---|---|---|---|
| $\lambda_1 - \theta_1$ | 3.428396 | 0.452325 | 0.009806 | $1.60 \times 10^{-4}$ | $5.68 \times 10^{-7}$ |
| residual $h_{k+1,k} \lvert e_k^T y_1 \rvert$ | 6.1187 | 1.8069 | 0.11279 | 0.0032028 | $5.107 \times 10^{-5}$ |

The residual estimate of line L13 agrees with $\|A x_1 - \theta_1 x_1\|_2$ to all printed digits. For the diagonal matrix $\operatorname{diag}(1, \dots, 100)$, the [Lanczos example](/lanczos-algorithm/) gives errors 4.205216, 0.862128, 0.050398, $6.42 \times 10^{-4}$ and $7.15 \times 10^{-7}$ at the same $k$, so the nonnormal matrix behaves about the same here. The error of $\theta_1$ is not monotone in general, unlike the symmetric case. With a random start vector (seed 1, uniform entries in $[-1, 1]$), $\theta_1 = 100.12981$ at $k = 20$, which is outside the interval $[1, 100]$ that holds the spectrum.

**An invisible eigenvalue.** At $k = 40$ the next Ritz values are 97.999111 and 96.972734: no Ritz value is near 99. The left eigenvector of $\lambda = 99$ is $y = e_{99} - e_{100}$, so $y^* b = 0$. Then $b$ lies in the invariant subspace spanned by the other 99 eigenvectors, and in exact arithmetic no $K_k(A, b)$ contains any component along the eigenvector of 99. In floating point, rounding errors create such a component and later steps amplify it. In this run the Ritz values at $k = 60$ and $k = 80$ still miss 99, and at $k = 100$ they include it.

## Correctness

The full proof is in [proofs/correctness.md](proofs/correctness.md).

1. **Basis and relation.** If $h_{j+1,j} > 0$ for $j < k$, then $q_1, \dots, q_k$ are orthonormal, $\operatorname{span}\{q_1, \dots, q_j\} = K_j(A, b)$ for $j \le k$, $H_k = Q_k^* A Q_k$ is upper Hessenberg with positive subdiagonal, and the Arnoldi relation holds.
2. **Termination.** The loop runs at most $\min(k, n)$ times. In exact arithmetic $h_{m+1,m} = 0$ exactly when $K_m(A, b)$ is invariant, that is, when $m$ is the degree of the minimal polynomial of $b$ with respect to $A$. Then every eigenvalue of $H_m$ is an eigenvalue of $A$, and every Ritz pair is an exact eigenpair.
3. **Ritz residuals.** $\|A x_i - \theta_i x_i\|_2 = h_{k+1,k} |e_k^T y_i|$. So $(\theta_i, x_i)$ is an exact eigenpair of $A + E$ with $\|E\|_2$ equal to this number.
4. **Polynomial optimality.** The characteristic polynomial $p$ of $H_k$ minimizes $\|p(A) b\|_2$ over all monic polynomials of degree $k$. So the Ritz values are the roots of the polynomial that is smallest on $b$, which is why they move toward outer eigenvalues.
5. **Convergence.** For diagonalizable $A = V \Lambda V^{-1}$ with $b = \sum_j \alpha_j v_j$ and $\alpha_1 \ne 0$, the distance from the eigenvector $v_1$ to $K_k(A, b)$ is at most $\sum_{j \ne 1} (|\alpha_j| / |\alpha_1|) \min_{p} \max_{j \ne 1} |p(\lambda_j)|$, over polynomials $p$ of degree below $k$ with $p(\lambda_1) = 1$ and unit $v_j$ (Saad 2011, Chapter 6). If all other eigenvalues lie in a disc with center $c$ and radius $r < |\lambda_1 - c|$, the minimum is at most $(r / |\lambda_1 - c|)^{k-1}$.
6. **Floating point.** The computed quantities satisfy the Arnoldi relation with an error of order $u \|A\|$ times a low-degree polynomial in $n$ and $k$. With modified Gram-Schmidt alone, the loss of orthogonality of the $q_j$ grows with the condition number of the Krylov basis. With a second pass it stays near $u$ in practice and in the analysis of classical Gram-Schmidt run twice.

## Complexity

- **Products.** One product with $A$ per step, $k$ in total; this count is exact. At a cost $z$ each, about two flops per nonzero for a sparse matrix.
- **Orthogonalization.** Step $j$ has $j$ inner products and $j$ vector updates, $4 j n$ flops. The total is $2k^2 n + O(kn)$ flops for one pass and $4k^2 n + O(kn)$ with line L6. These counts are exact.
- **Storage.** $Q_{k+1}$ takes $(k+1) n$ numbers, and $\bar H_k$ takes $O(k^2)$. Unlike Lanczos, every $q_i$ is needed in line L5, so storage grows with $k$.
- **The small problem.** The eigenvalues of $H_k$ cost $O(k^3)$ flops by the Hessenberg QR algorithm, with an observed number of iterations per eigenvalue. Each Ritz vector $Q_k y_i$ costs $2kn$ flops.
- **Number of steps.** The bound in item 5 of Correctness is proved but often pessimistic. The number of steps to reach a tolerance depends on the spectrum, the eigenvector basis and $b$, and is observed. Because the cost per step grows linearly in $k$, practical codes stop at a fixed $k$ and restart.

## Properties

- **Hessenberg structure.** $H_k$ is upper Hessenberg because $A q_j \in K_{j+1}(A, b)$. Its subdiagonal is positive until breakdown, so $H_k$ is unreduced and each eigenvalue of $H_k$ has geometric multiplicity 1.
- **Symmetric case.** If $A$ is Hermitian, $H_k = Q_k^* A Q_k$ is Hermitian and Hessenberg, hence tridiagonal, and Arnoldi reduces in exact arithmetic to the [Lanczos algorithm](/lanczos-algorithm/).
- **One copy of each eigenvalue.** The Krylov space of one vector contains at most one direction from each eigenspace, so Arnoldi finds only one copy of a multiple eigenvalue (see the repeated-eigenvalue test of the implementation, which stops at $m = 4$ for a matrix of order 6 with a triple eigenvalue).
- **Numerical range.** Ritz values lie in the numerical range $\{x^* A x : \|x\|_2 = 1\}$, since $\theta_i = x_i^* A x_i$ for unit $x_i = Q_k y_i$. For a nonnormal $A$ this set can be much larger than the convex hull of the spectrum, which explains Ritz values outside it.
- **Shift invariance.** Arnoldi on $A - \sigma I$ gives the same $Q_k$ and $H_k - \sigma I$, since $K_k(A - \sigma I, b) = K_k(A, b)$.

## Variants and improvements

- **Restarting.** Explicit restarts begin again from a combination of wanted Ritz vectors. [Implicitly restarted Arnoldi](/implicitly-restarted-arnoldi/) (Sorensen 1992, ARPACK) applies shifted QR steps to $H_k$ to compress the factorization, and the Krylov-Schur method (Stewart 2001) does the same through a Schur form.
- **Shift and invert.** Run Arnoldi on $(A - \sigma I)^{-1}$ to find eigenvalues near $\sigma$, with one sparse factorization of $A - \sigma I$.
- **Linear systems.** [GMRES](/gmres/) uses the same relation and minimizes $\|\beta e_1 - \bar H_k y\|_2$; the full orthogonalization method solves $H_k y = \beta e_1$.
- **Block Arnoldi.** Start from several vectors to find multiple and clustered eigenvalues and to use matrix-block products.
- **Householder Arnoldi** (Walker 1988): build the basis with Householder reflections. Orthogonality is then near $u$ without a second pass, at about twice the flops.
- **Classical Gram-Schmidt run twice.** Same accuracy as line L6, but the two passes are matrix-vector products with $Q_j^*$ and $Q_j$, which run faster on parallel machines.
- **Refined and harmonic Ritz values.** Other extractions from the same space, better for interior eigenvalues (Jia 1997; Morgan 1991).

## When to use it

Use Arnoldi for a few eigenvalues of a large sparse or structured non-Hermitian matrix when only products $x \mapsto A x$ are cheap: stability analysis of large dynamical systems, Markov chains and [PageRank](/pagerank/)-type problems, and discretized convection-diffusion operators. Use it with restarts in practice. For a Hermitian matrix use [Lanczos](/lanczos-algorithm/) instead. For a dense matrix of moderate order use the [QR algorithm](/qr-algorithm/), which finds all eigenvalues in $O(n^3)$ flops. If the wanted eigenvalues are interior or clustered, combine Arnoldi with shift and invert, or use [subspace iteration](/subspace-iteration/) when a block method is wanted.

## Pitfalls

- **Classical Gram-Schmidt with one pass.** The $q_j$ then lose orthogonality fast, and $H_k$ is no longer a projection of $A$. Use modified Gram-Schmidt, a second pass, or Householder reflections.
- **Unbounded growth.** Memory and work per step grow with $k$. Without restarts a long run can cost more than a dense method.
- **A start vector with no component along the wanted eigenvector.** As in the example, the eigenvalue is then invisible in exact arithmetic, and it appears in floating point only after many steps. Use a random start vector.
- **Trusting converged-looking Ritz values of a nonnormal matrix.** A small residual $h_{k+1,k} |e_k^T y_i|$ means a small backward error. The forward error is that times the [eigenvalue condition number](/eigenvalue-condition-number/), which can be large. Ritz values can also sit in regions of the [pseudospectrum](/pseudospectrum/) far from any eigenvalue.
- **Exact breakdown tests.** $h_{j+1,j} = 0$ almost never happens in floating point. Use a relative tolerance; a small value means a found invariant subspace, which is good news.
- **Real matrices and complex Ritz values.** For real $A$ and $b$, $H_k$ is real and its complex Ritz values come in conjugate pairs. Restarted codes must keep both members of a pair together.

## Implementations

## History

Walter Arnoldi published the process in 1951, in the same "minimized iterations" framework as Lanczos's work of 1950, as a way to reduce a matrix to Hessenberg form and so to find its characteristic polynomial. With the arrival of Householder's method it was seen for many years as a less stable variant of a direct reduction. Yousef Saad (1980) showed that it is useful as an iterative method that stops early, and analyzed the convergence of the Ritz values. Restarting was the remaining problem, which Danny Sorensen's implicit restart (1992) and the ARPACK library solved in practice. Today Arnoldi with restarts is the standard method for a few eigenvalues of a large nonsymmetric matrix, and its relation is also the core of GMRES.

## References
