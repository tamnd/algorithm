---
tag: 1HMDCT
kind: algorithm
slug: subspace-iteration
name: Subspace iteration
aliases:
- simultaneous iteration
- orthogonal iteration
- block power method
- Treppeniteration
area: numerical/eigenproblems
level: advanced
summary: Power iteration on a block of p vectors, orthonormalized each step and improved by a Rayleigh-Ritz step. The block turns to the dominant invariant subspace at the rate |λ_(p+1)/λ_p| per step.
solves: [symmetric-eigenproblem]
model: floating-point-model
complexity:
  vars: {n: "the order of A", p: "the block size", z: "the number of nonzeros of A", k: "the number of block steps"}
  time: {worst: O(k p z + k n p^2)}
  space: {extra: Θ(n p)}
  matvecs: {worst: "k p"}
  flops: {worst: "2 k p z + 10 k n p^2 + O(k p^3)"}
properties: {deterministic: true, in_place: false, recursive: false, iterative: true}
history:
  year: 1957
  people: [Friedrich L. Bauer, Heinz Rutishauser]
  note: Bauer introduced the Treppeniteration in 1957; Rutishauser added the Rayleigh-Ritz step and the practical program ritzit around 1969 to 1970.
prereqs: [power-iteration, qr-decomposition]
see_also: [rayleigh-ritz-method, qr-algorithm, lanczos-algorithm, arnoldi-iteration, krylov-subspace, deflation, symmetric-eigenproblem, principal-component-analysis]
sources:
  - book: isbn:9781421407944
    title: Gene H. Golub and Charles F. Van Loan, Matrix Computations, fourth edition, Johns Hopkins University Press, 2013
    locator: Section 7.3.2, Orthogonal Iteration; Section 8.2, Power Iterations (orthogonal iteration with Ritz acceleration for symmetric matrices)
  - book: isbn:9780898713619
    title: Lloyd N. Trefethen and David Bau III, Numerical Linear Algebra, SIAM, 1997
    locator: Lecture 28, QR Algorithm without Shifts (simultaneous iteration and its equivalence with the unshifted QR algorithm)
  - book: isbn:9780898713893
    title: James W. Demmel, Applied Numerical Linear Algebra, SIAM, 1997
    locator: Section 4.4.3, Orthogonal Iteration
  - book: isbn:9780898714029
    title: Beresford N. Parlett, The Symmetric Eigenvalue Problem, SIAM Classics in Applied Mathematics 20, 1998
    locator: Chapter 14, Subspace Iteration (the Rayleigh-Ritz variant, its convergence rates and Rutishauser's ritzit)
  - book: isbn:9781611970722
    title: Yousef Saad, Numerical Methods for Large Eigenvalue Problems, revised edition, SIAM Classics in Applied Mathematics 66, 2011
    locator: Chapter 5, Subspace Iteration (simple subspace iteration, subspace iteration with projection, the convergence theorem)
  - paper: "F. L. Bauer, Das Verfahren der Treppeniteration und verwandte Verfahren zur Lösung algebraischer Eigenwertprobleme, Zeitschrift für angewandte Mathematik und Physik 8, 1957"
    title: Das Verfahren der Treppeniteration und verwandte Verfahren zur Lösung algebraischer Eigenwertprobleme
    locator: ZAMP 8 (1957), pp. 214 to 235
  - paper: "H. Rutishauser, Simultaneous iteration method for symmetric matrices, Numerische Mathematik 16, 1970"
    title: Simultaneous iteration method for symmetric matrices
    locator: Numer. Math. 16 (1970), pp. 205 to 223
---

Subspace iteration computes the $p$ eigenvalues of largest modulus of a matrix $A$ and an orthonormal basis of the corresponding invariant subspace. It is [power iteration](/power-iteration/) applied to a block of $p$ vectors at once: multiply the block by $A$, orthonormalize it so that the columns do not all collapse onto the dominant eigenvector, and repeat. The span of the block after $k$ steps is $A^k \mathcal S_0$, and when $|\lambda_p| > |\lambda_{p+1}|$ it turns to the dominant invariant subspace, with the tangent of the largest angle shrinking by the factor $|\lambda_{p+1}/\lambda_p|$ per step. A [Rayleigh-Ritz](/rayleigh-ritz-method/) step on the block extracts the eigenvalue estimates, and for symmetric $A$ the $i$-th estimate converges at the faster rate $|\lambda_{p+1}/\lambda_i|^{2}$ per step. It needs only products with $A$ and $\Theta(np)$ memory, it is simple and robust, and it is the ancestor of the [QR algorithm](/qr-algorithm/), which is the same iteration with $p = n$.

## In plain words

Power iteration chases one direction: the one the matrix stretches most. To find several such directions at once, start with a handful of arrows, apply the matrix to all of them, and then straighten them out so they are at right angles to each other again. Without the straightening they would all fall onto the same strongest direction. With it, the first arrow follows the strongest direction, the second follows the strongest one left over, and so on. After each round a small side calculation reads off the stretching factors from the handful of arrows. The more the kept factors beat the first one left out, the faster the arrows settle.

## The problem

**Notation.** $A \in \mathbb R^{n \times n}$ symmetric, with real eigenvalues ordered **by modulus** on this page, $|\lambda_1| \ge |\lambda_2| \ge \dots \ge |\lambda_n|$, and orthonormal eigenvectors $v_i$. The block size is $p$, $V_p = [v_1, \dots, v_p]$, and $\mathcal V_p$ is its span, the dominant invariant subspace when $|\lambda_p| > |\lambda_{p+1}|$. The rate is the ratio $|\lambda_{p+1}/\lambda_p|$. For subspaces of equal dimension, $\theta(\mathcal S, \mathcal V_p)$ is the largest principal angle. $u$ is the unit roundoff, and $z$ the number of nonzeros of $A$, so a product $Av$ costs about $2z$ flops.

**Input.** $A$ (only products $Av$ are needed), $p$ with $1 \le p \le n$, a start block $X_0 \in \mathbb R^{n \times p}$ of rank $p$, a tolerance $\mathrm{tol}$ and a step limit $\mathrm{maxit}$.

**Output.** Ritz values $\theta_1, \dots, \theta_p$ ordered by decreasing modulus, orthonormal Ritz vectors $X = [x_1, \dots, x_p]$, and a flag. On CONVERGED every residual satisfies $\|A x_i - \theta_i x_i\|_2 \le \mathrm{tol} \cdot \max_j |\theta_j|$, so $(\Theta, X)$ is an exact block of eigenpairs of a symmetric $A + E$ with $\|E\|_2 \le \sqrt p \, \mathrm{tol} \, \|A\|_2$ (Lemma 3 of the proof).

## The algorithm

```pseudo id=main
SUBSPACE-ITERATION(A, X₀, p, tol, maxit)
L1  Q ← orthonormal basis of the columns of X₀            ▷ QR, n × p
L2  for k ← 1 to maxit do
L3      Z ← A Q                                           ▷ p matrix-vector products
L4      H ← Qᵀ Z                                          ▷ p × p, symmetric up to rounding
L5      (Θ, Y) ← eigen-decomposition H = Y Θ Yᵀ, |θ₁| ≥ … ≥ |θ_p|   ▷ Rayleigh-Ritz
L6      X ← Q Y;  W ← Z Y                                 ▷ Ritz vectors and W = A X
L7      R ← W − X Θ                                       ▷ Ritz residuals rᵢ = A xᵢ − θᵢ xᵢ
L8      if maxᵢ ‖rᵢ‖₂ ≤ tol · maxⱼ |θⱼ| then return (Θ, X, k, CONVERGED)
L9      if k = maxit then return (Θ, X, k, NOT-CONVERGED)
L10     Q ← orthonormal basis of the columns of W         ▷ span W = A · span Q
```

Line L10 is the power step: $W = AX$ and $X$ spans the same space as $Q$, so the new basis spans $A$ times the old subspace. Lines L4 to L7 are the [Rayleigh-Ritz method](/rayleigh-ritz-method/) on the current subspace; they do not change the subspace, only the basis inside it, but they give the eigenvalue estimates and make each column converge to its own eigenvector. The implementation solves the small problem of line L5 with the cyclic Jacobi method, orthonormalizes by modified Gram-Schmidt applied twice, and replaces a column that loses almost all of its norm (a rank-deficient block, as for a singular $A$) by a random vector.

## Example

Take the matrix of the [Rayleigh-Ritz](/rayleigh-ritz-method/) page,

$$A = \begin{pmatrix} 2 & 1 & 0 \\ 1 & 3 & 1 \\ 0 & 1 & 4 \end{pmatrix}, \qquad \lambda = 3 + \sqrt 3 = 4.732051, \; 3, \; 3 - \sqrt 3 = 1.267949,$$

with $p = 2$ and $X_0 = [e_1, e_2]$. The rate is $|\lambda_3/\lambda_2| = 0.422650$. Step $j$ below uses the basis of $A^j \mathcal S_0$:

| $j$ | $\tan\theta(A^j \mathcal S_0, \mathcal V_2)$ | $\theta_1$ | $\theta_2$ | $\lambda_2 - \theta_2$ |
|---|---|---|---|---|
| 0 | 4.625 | 3.618034 | 1.381966 | 1.618 |
| 1 | 1.528 | 4.095445 | 1.904555 | 1.095 |
| 2 | 0.5568 | 4.573847 | 2.653426 | 0.3466 |
| 3 | 0.2184 | 4.715678 | 2.928992 | 0.07101 |
| 4 | 0.08928 | 4.730788 | 2.986931 | 0.01307 |
| 5 | 0.03720 | 4.731959 | 2.997652 | 0.002348 |
| 6 | 0.01563 | 4.732044 | 2.999580 | 0.0004200 |
| 7 | 0.006592 | 4.732050 | 2.999925 | 0.00007503 |

Step 0 is exactly the Rayleigh-Ritz example, with Ritz values $(5 \pm \sqrt 5)/2$. The tangent obeys the bound $\tan\theta_j \le 0.422650^j \cdot 4.625$ of the Correctness section (at $j = 7$ the bound is $0.0111$), and its ratio settles at $0.4226$. The error of $\theta_2$ shrinks by $0.1787$ per step, which is $(\lambda_3/\lambda_2)^2 = 0.178633$, and the error of $\theta_1$ by $0.0718$, which is $(\lambda_3/\lambda_1)^2 = 0.071797$: the Ritz values converge at the squared rates. With $\mathrm{tol} = 10^{-12}$ the method stops at step 34 after 68 products, with residual norms $6.7 \times 10^{-16}$ and $2.1 \times 10^{-12}$ and Ritz vectors $(0.211325, 0.577350, 0.788675)$ and $(0.577350, 0.577350, -0.577350)$. These numbers come from the implementation and are checked by its tests.

## Correctness

The full proofs are in [proofs/correctness.md](proofs/correctness.md); the argument, in exact arithmetic:

- **The subspace.** If $X_0$ has rank $p$ and $\lambda_p \ne 0$, every block $A^k X_0$ has rank $p$, and the basis $Q_k$ at step $k + 1$ spans $A^k \operatorname{span}(X_0)$, because the Rayleigh-Ritz step only rotates the basis inside its span.
- **Galerkin and backward error.** $X^T X = I$ and $X^T R = 0$. Hence $E = -(R X^T + X R^T)$ is symmetric, $(A + E) X = X \Theta$, and $\|E\|_2 = \|R\|_2 \le \sqrt p \max_i \|r_i\|_2$. So line L8 returns an exact block of eigenpairs of a nearby symmetric matrix.
- **Convergence of the subspace (proved).** If $|\lambda_p| > |\lambda_{p+1}|$ and $V_p^T X_0$ is nonsingular, then $\tan\theta(A^k \mathcal S_0, \mathcal V_p) \le |\lambda_{p+1}/\lambda_p|^k \tan\theta(\mathcal S_0, \mathcal V_p)$. The proof writes the block in eigenvector coordinates as $\begin{pmatrix} I \\ F \end{pmatrix}$, where $\|F\|_2$ is the tangent, and observes that $A^k$ maps $F$ to $\Lambda_2^k F \Lambda_1^{-k}$.
- **Termination (proved).** The residual of the whole block is at most $2 \|A\|_2 \sin\theta_k$, while $\max_j |\theta_j| \ge |\lambda_p| \cos\theta_k - 3 \|A\|_2 \sin\theta_k$. So the test of line L8 holds after finitely many steps for every $\mathrm{tol} > 0$, and line L9 bounds the loop in any case.
- **Individual Ritz values (cited).** For symmetric $A$, $|\theta_i^{(k)} - \lambda_i| = O(|\lambda_{p+1}/\lambda_i|^{2k})$ and the angle between $x_i$ and $v_i$ is $O(|\lambda_{p+1}/\lambda_i|^{k})$ (Parlett Chapter 14; Saad 2011 Chapter 5). The tests measure these rates.

In floating point, each step is backward stable: modified Gram-Schmidt applied twice keeps $\|Q^T Q - I\|$ at a small multiple of $u$, and the tests observe Ritz vectors orthogonal to within $0.5 \, n u$.

## Complexity

**Products with $A$ (exact).** Each step makes $p$ products, so $k$ steps make $kp$. The number of steps to reach a tolerance $\mathrm{tol}$ is about $\log(\tan\theta_0 \, \|A\|_2 / (\mathrm{tol} \, |\lambda_p|)) / \log(|\lambda_p / \lambda_{p+1}|)$ by the two proved bounds; this is a worst-case bound up to constants, not a typical count.

**Flops per step (counted from the code, leading terms).** The products cost $2pz$ ($2n^2 p$ for a dense $A$). Forming $H$ costs $2np^2$, $X = QY$ and $W = ZY$ cost $2np^2$ each, and two passes of modified Gram-Schmidt cost $4np^2$, for $2pz + 10 np^2$, plus $O(p^3)$ per Jacobi sweep on $H$. When $p \ll n$ the products dominate.

**Space.** The blocks $Q$, $Z$, $X$, $W$ take $\Theta(np)$ extra memory.

## Properties

- **Iterative, deterministic for a fixed start.** The default start is a seeded random block.
- **Only products with $A$.** It works for sparse and implicit operators, and the $p$ products in line L3 can be done as one matrix-matrix product, which runs at a much higher rate than $p$ separate products.
- **One-sided for positive definite $A$.** By [Cauchy interlacing](/cauchy-interlacing-theorem/) each Ritz value satisfies $\theta_i \le \lambda_i$ when $A$ is positive definite, so the estimates approach from below.
- **Self-correcting.** Rounding errors in one step only perturb the subspace, and later steps correct the perturbation, as for power iteration.
- **Linear convergence.** The rate is fixed by the ratio of eigenvalues; there is no shift to speed it up as in the [QR algorithm](/qr-algorithm/).

## Variants and improvements

- **Guard vectors.** To get $s$ eigenpairs, iterate with $p > s$ vectors. The rate for the wanted pairs becomes $|\lambda_{p+1}/\lambda_s|$, which can be much smaller; $p = 2s$ or $s + 8$ are common choices.
- **Locking.** Freeze converged Ritz vectors and keep orthogonalizing against them, so that later steps work only on the unconverged columns.
- **Polynomial acceleration.** Replace $A$ by a Chebyshev polynomial in $A$ that is large on the wanted eigenvalues and small on an interval holding the rest (Rutishauser 1970; Saad 2011).
- **Shift and invert.** Iterating with $(A - \sigma I)^{-1}$ finds the eigenvalues nearest $\sigma$, as [inverse iteration](/inverse-iteration/) does for one vector; this was the standard method of structural engineering for the lowest vibration modes.
- **Nonsymmetric matrices.** Orthogonal iteration without the Rayleigh-Ritz step drives $Q^T A Q$ to block upper triangular form, the [Schur decomposition](/schur-decomposition/) of the dominant part; the Schur-Rayleigh-Ritz variant computes a small Schur form instead of an eigen-decomposition (Stewart 1976).
- **The QR algorithm.** With $p = n$ and $X_0 = I$, orthogonal iteration produces $A_k = Q_k^T A Q_k$, which are exactly the iterates of the unshifted [QR algorithm](/qr-algorithm/) (Trefethen and Bau, Lecture 28).
- **Krylov methods.** The [Lanczos algorithm](/lanczos-algorithm/) and [Arnoldi iteration](/arnoldi-iteration/) use the whole sequence $b, Ab, A^2 b, \dots$ rather than only the last block, and usually need far fewer products.

## When to use it

Use subspace iteration when a few dominant eigenpairs are wanted, products with blocks are cheap, and simplicity and robustness matter more than the number of products: for example when $A$ changes slowly and the previous basis is an excellent start, or in randomized SVD and [principal component analysis](/principal-component-analysis/), where a few power steps on a random block are enough. For a large gap it converges in a few steps. For small gaps, Krylov methods such as [Lanczos](/lanczos-algorithm/) converge much faster for the same number of products. For dense matrices of moderate size, the [symmetric QR algorithm](/symmetric-eigenproblem/) computes everything in $O(n^3)$ flops.

## Pitfalls

- **Equal moduli at the cut.** If $|\lambda_p| = |\lambda_{p+1}|$, as for $\operatorname{diag}(3, -3, 1)$ with $p = 1$, the subspace does not converge. Enlarge the block so that the cut falls in a gap; with $p = 2$ the same matrix converges at once to $\{3, -3\}$.
- **Order by modulus.** The method finds the eigenvalues largest in modulus, not the largest algebraically. For the largest algebraic eigenvalues, shift: iterate with $A + \sigma I$ for a $\sigma$ that makes them dominant.
- **Orthonormalize every step.** Without it, all columns converge to $v_1$ and the block becomes numerically rank one within $\log(1/u)/\log|\lambda_1/\lambda_2|$ steps.
- **Rank-deficient blocks.** If $A$ is singular, $AQ$ can lose rank; Gram-Schmidt must detect this and replace the lost columns, or it divides by a tiny norm.
- **Stopping on the Ritz values only.** Ritz values converge at the squared rate, so they look converged long before the vectors are; test the residuals, as line L8 does.
- **A start orthogonal to the target.** If $V_p^T X_0$ is singular, the exact iteration never finds part of $\mathcal V_p$; rounding errors usually rescue it, slowly. A random start avoids this with probability one.

## Implementations

## History

Friedrich L. Bauer introduced the Treppeniteration (staircase iteration) in 1957, iterating with a block and restoring triangular structure each step, and it is closely related to Rutishauser's LR algorithm and to the later QR algorithm. Heinz Rutishauser studied the symmetric case and in 1969 and 1970 published a careful version with the Rayleigh-Ritz step, Chebyshev acceleration and locking, the Handbook procedure ritzit. Clint and Jennings proposed a similar method in 1970, and it became the standard method for the lowest vibration modes in structural engineering. Stewart extended the convergence theory to nonsymmetric matrices in 1976.

## References
