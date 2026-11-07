---
tag: 4WHW5Y
kind: algorithm
slug: cholesky-decomposition
name: Cholesky decomposition
aliases:
- Cholesky factorization
- Cholesky factorisation
- square root method
area: numerical/linear-systems
level: core
summary: Factor a symmetric positive definite A as LL^T, about half the work of LU.
solves: [linear-system-solving]
model: floating-point-model
complexity:
  vars: {n: "the order of A, at least 1"}
  time: {worst: Θ(n^3), best: Θ(n^3)}
  space: {extra: Θ(n^2)}
  flops: {worst: "n^3/3 + n^2/2 - 5n/6"}
  square_roots: {worst: n}
properties: {deterministic: true, in_place: false, recursive: false}
prereqs: [positive-definite-matrix, back-substitution, linear-system-solving]
see_also: [lu-decomposition, lup-decomposition, incomplete-cholesky-factorization, elimination-tree, fill-reducing-ordering, conjugate-gradient-method, schur-complement, hilbert-matrix]
sources:
  - book: isbn:9780898715217
    title: Nicholas J. Higham, Accuracy and Stability of Numerical Algorithms, second edition, SIAM, 2002
    locator: Chapter 10, Cholesky Factorization (Theorem 10.1, existence and uniqueness; Theorem 10.3, the backward error of the factorization; Theorem 10.4, the backward error of the solve; Section 10.1 also gives the condition for the factorization to run to completion and the history)
  - book: isbn:9781421407944
    title: Gene H. Golub and Charles F. Van Loan, Matrix Computations, fourth edition, Johns Hopkins University Press, 2013
    locator: Section 4.2, Positive Definite Systems (the Cholesky factorization, its outer and inner product forms, the flop count, and the stability discussion)
  - book: isbn:9780898713619
    title: Lloyd N. Trefethen and David Bau III, Numerical Linear Algebra, SIAM, 1997
    locator: Lecture 23, Cholesky Factorization (existence and uniqueness, the operation count, and backward stability)
  - paper: doi:10.1007/BF03031308
    title: Commandant Benoit, Note sur une methode de resolution des equations normales provenant de l'application de la methode des moindres carres a un systeme d'equations lineaires en nombre inferieur a celui des inconnues (Procede du Commandant Cholesky), Bulletin geodesique 2, 1924
    locator: pp. 67 to 77 (the first publication of Cholesky's method)
---

The Cholesky decomposition writes a [symmetric positive definite](/positive-definite-matrix/) matrix $A$ as $A = R^T R$, where $R$ is upper triangular with a positive diagonal (equivalently $A = L L^T$ with $L = R^T$). It costs $n^3/3$ flops, half of [LU](/lup-decomposition/), and needs no pivoting: the entries of $R$ satisfy $|r_{ij}| \le \sqrt{a_{jj}}$, so they cannot grow, and the method is backward stable for each symmetric positive definite $A$. With $R$, the system $A x = b$ is solved by one forward and one [back substitution](/back-substitution/). The factorization exists exactly when $A$ is positive definite, so the algorithm is also the standard test of positive definiteness.

## In plain words

A positive number has a square root. A symmetric positive definite matrix has something like a square root too: a triangular matrix that, multiplied by its own mirror image, gives the matrix back. The method finds it column by column. Each new diagonal entry is the square root of what is left of the matching diagonal entry of the matrix after the earlier columns are used, and the entries to its right are found by one division each.

If the number under a square root is ever zero or negative, the matrix was not positive definite, and the method stops and says so. Because the entries of the triangle can never be larger than the square roots of the diagonal of the matrix, rounding errors cannot be amplified by large intermediate numbers, so no row swaps are needed.

## The problem

**Notation.** As in [solving linear systems](/linear-system-solving/): $A = (a_{ij})$ is an $n \times n$ real symmetric matrix, $u$ is the unit roundoff, $\gamma_n = n u / (1 - n u)$, and $|R|$ is the matrix of the $|r_{ij}|$. $A$ is *positive definite* if $z^T A z > 0$ for each nonzero $z \in \mathbb{R}^n$.

Input: a symmetric $A$. Output: the upper triangular $R$ with $r_{jj} > 0$ and $R^T R = A$, or the report that $A$ is not positive definite. To solve $A x = b$, then solve $R^T y = b$ and $R x = y$.

**Theorem (existence and uniqueness).** A symmetric $A$ has a factorization $A = R^T R$ with $R$ upper triangular and $r_{jj} > 0$ if and only if $A$ is positive definite, and then $R$ is unique (Higham, Theorem 10.1).

## The algorithm

Compare entry $(j, i)$, $i \ge j$, of $A = R^T R$: $a_{ji} = \sum_{k=1}^{j} r_{kj} r_{ki}$. For $i = j$ this gives $r_{jj}$, and for $i > j$ it gives $r_{ji}$, from the entries of the earlier rows of $R$.

```pseudo id=main
CHOLESKY(A)                                ▷ A symmetric, n × n; only a_ji with i ≥ j is read
L1  for j ← 1 to n do
L2      s ← a_jj − Σ_{k=1}^{j−1} r_kj²
L3      if s ≤ 0 then return NOT-POSITIVE-DEFINITE
L4      r_jj ← √s
L5      for i ← j + 1 to n do
L6          r_ji ← (a_ji − Σ_{k=1}^{j−1} r_kj · r_ki) / r_jj
L7  return R
```

```pseudo id=solve
CHOLESKY-SOLVE(R, b)
S1  y ← FORWARD-SUBSTITUTION(R^T, b)
S2  x ← BACK-SUBSTITUTION(R, y)
S3  return x
```

Row $j$ of $R$ is computed from rows $1, \ldots, j - 1$. Line L2 is the diagonal entry of the [Schur complement](/schur-complement/) that elimination would have left, and line L6 is the rest of row $j$ of that complement divided by its pivot. This is the *up-looking* or inner product form. The *right-looking* (outer product) form computes row $j$ and then subtracts $r_j^T r_j$ from the trailing block at once; it does the same flops in a different order.

## Example

Let
$$A = \begin{pmatrix} 4 & 12 & -16 \\ 12 & 37 & -43 \\ -16 & -43 & 98 \end{pmatrix}, \qquad b = \begin{pmatrix} 0 \\ 6 \\ 39 \end{pmatrix}.$$

| $j$ | $s$ (line L2) | $r_{jj}$ | rest of row $j$ (line L6) |
|---|---|---|---|
| 1 | $4$ | $2$ | $r_{12} = 12/2 = 6$, $r_{13} = -16/2 = -8$ |
| 2 | $37 - 6^2 = 1$ | $1$ | $r_{23} = (-43 - 6 \cdot (-8))/1 = 5$ |
| 3 | $98 - (-8)^2 - 5^2 = 9$ | $3$ | none |

So $R = \begin{pmatrix} 2 & 6 & -8 \\ 0 & 1 & 5 \\ 0 & 0 & 3 \end{pmatrix}$. The forward substitution $R^T y = b$ gives $y = (0, 6, 3)^T$, and the back substitution $R x = y$ gives $x = (1, 1, 1)^T$. All values are small integers, so binary64 computes them with no rounding.

**An indefinite matrix.** For $A = \begin{pmatrix} 1 & 2 \\ 2 & 3 \end{pmatrix}$, line L2 gives $s = 1$, then $r_{12} = 2$, and at $j = 2$, $s = 3 - 4 = -1$, so the algorithm reports that $A$ is not positive definite. Indeed $\det A = -1 < 0$.

**Near the limit.** On the binary64 [Hilbert matrix](/hilbert-matrix/) $\mathrm{fl}(H_n)$, this algorithm runs to completion for $n \le 13$ and stops at $n = 14$, where $\kappa_2(H_{14}) \approx 1.9 \times 10^{19} > 1/u$.

## Correctness

The exact algorithm computes the unique factor when $A$ is positive definite, and returns NOT-POSITIVE-DEFINITE otherwise. The proof keeps an invariant on the rows of $R$ computed so far, and shows that the value $s$ of line L2 at step $j$ equals $\det A_j / \det(R_{j-1})^2$, where $A_j$ is the leading $j \times j$ block of $A$. So $s > 0$ at each step exactly when each leading block has a positive determinant, which holds when $A$ is positive definite. The full proof is in [the proof](proofs/correctness.md).

**Backward error (proved).** Assume the [standard model](/floating-point-model/) and $(n + 1) u < 1$. If the algorithm runs to completion on a symmetric $A$, the computed $\hat R$ satisfies
$$\hat R^T \hat R = A + \Delta A, \qquad |\Delta A| \le \gamma_{n+1} |\hat R^T| \, |\hat R|$$
(Higham, Theorem 10.3), and the computed solution satisfies $(A + \Delta A')\hat x = b$ with $|\Delta A'| \le \gamma_{3n+1} |\hat R^T| \, |\hat R|$ (Higham, Theorem 10.4). By the Cauchy-Schwarz inequality, $(|\hat R^T| |\hat R|)_{ij} \le \|\hat r_{:,i}\|_2 \|\hat r_{:,j}\|_2$, and $\|\hat r_{:,j}\|_2^2 = a_{jj} + \Delta a_{jj} \le a_{jj}/(1 - \gamma_{n+1})$. So the bound is a small multiple of $u \max_j a_{jj}$, with no growth factor: Cholesky is backward stable for each symmetric positive definite matrix. In the 2-norm this gives $\|\Delta A'\|_2 \le c\, n^2 u \|A\|_2$ for a modest constant $c$, and the forward error satisfies $\|x - \hat x\|_2 / \|x\|_2 \lesssim c\, n^2 u \, \kappa_2(A)$ to first order.

**Running to completion.** In floating point the algorithm can fail on a positive definite matrix when $\kappa_2(A) u$ is close to $1$, as the Hilbert example shows. Demmel proved that it succeeds when the scaled matrix $H = D^{-1} A D^{-1}$, $D = \operatorname{diag}(a_{jj})^{1/2}$, satisfies $\lambda_{\min}(H) > n \gamma_{n+1}/(1 - \gamma_{n+1})$ (Higham, Section 10.1). So a failure in floating point means that $A$ is not positive definite or is within a few roundings of a matrix that is not.

## Complexity

Row $j$ costs $2(j - 1)$ flops at line L2, one square root, and $2(j - 1) + 1$ flops for each of the $n - j$ entries at line L6. With $k = j - 1$,
$$\sum_{k=0}^{n-1} \bigl(2 k (n - k) + (n - 1 - k)\bigr) = \frac{n^3 - n}{3} + \frac{n^2 - n}{2} = \frac{n^3}{3} + \frac{n^2}{2} - \frac{5n}{6}$$
flops and $n$ square roots, in each case. The solve adds $2n^2$ flops. The storage is the upper triangle, $n(n+1)/2$ numbers, and $R$ can overwrite the upper triangle of $A$. For a [banded](/banded-matrix/) $A$ of half-bandwidth $p$, $R$ has the same band and the cost is about $n p^2$ flops. For a sparse $A$, the cost depends on the [fill-in](/fill-in/) of $R$, which a [fill-reducing ordering](/fill-reducing-ordering/) reduces. Dense Cholesky in LAPACK (`xPOTRF`) is blocked so that most flops are matrix-matrix products, because memory traffic, not the flop count, limits the unblocked form.

## Properties

- **No pivoting, no growth.** $\sum_k r_{kj}^2 = a_{jj}$ gives $|r_{kj}| \le \sqrt{a_{jj}}$ in exact arithmetic.
- **Backward stable** for each symmetric positive definite $A$, with the bound above.
- **A test of definiteness.** The exact algorithm completes exactly when $A$ is positive definite; this is the cheapest standard test.
- **Determinant.** $\det A = \prod_j r_{jj}^2$, and $\log \det A = 2 \sum_j \log r_{jj}$ without overflow.
- **Symmetric storage.** Only one triangle of $A$ is read.

## Variants and improvements

- **$L D L^T$ factorization.** $A = L D L^T$ with unit lower triangular $L$ and diagonal $D$ avoids square roots; it also exists for some indefinite matrices, but without pivoting it is not stable for them.
- **Symmetric indefinite matrices.** Use $L D L^T$ with $1 \times 1$ and $2 \times 2$ pivots (Bunch and Kaufman, Higham Chapter 11), not plain Cholesky.
- **Pivoted Cholesky.** Pick the largest remaining diagonal entry at each step. For a positive semidefinite $A$ of rank $k$ it stops after $k$ steps and gives a factorization of $P^T A P$ that reveals the rank.
- **Band, sparse and supernodal Cholesky.** Organized by the [elimination tree](/elimination-tree/), with an ordering chosen to reduce fill.
- **Incomplete Cholesky.** Drop entries outside a pattern to get a [preconditioner](/incomplete-cholesky-factorization/) for the [conjugate gradient method](/conjugate-gradient-method/).
- **Modified Cholesky.** Optimization codes add a diagonal shift when a pivot is too small, to get a positive definite matrix near $A$.

## When to use it

Use Cholesky for each symmetric positive definite system that fits in memory as a dense or sparse factor: normal equations, covariance matrices, finite element stiffness matrices, Newton steps of convex optimization. It is about twice as fast as LU and needs half the storage. For least squares, prefer QR to Cholesky on $A^T A$, because $\kappa_2(A^T A) = \kappa_2(A)^2$. For very large sparse problems where the factor does not fit, use the conjugate gradient method with a preconditioner.

## Pitfalls

- **Testing $s < 0$ instead of $s \le 0$ at line L3.** With $s = 0$, line L4 gives $r_{jj} = 0$ and line L6 divides by zero. The test is $s \le 0$; in floating point a tiny positive $s$ also signals a near-singular matrix.
- **Reading the wrong triangle.** Line L6 uses $a_{ji}$ with $i > j$. Code that reads $a_{ij}$ on an input whose lower triangle is not set (as LAPACK allows) uses garbage. Read one triangle consistently.
- **Using Cholesky on an indefinite matrix with a shift and no note.** A failure means the matrix is not (numerically) positive definite. Adding a multiple of $I$ makes it succeed, but then the solution is of another system.
- **Forming $A^T A$ for least squares.** It squares the condition number, so a problem with $\kappa_2(A) = 10^8$ loses all digits in binary64. Use a QR factorization.

## Implementations

## History

André-Louis Cholesky, an officer of the French army, developed the method for the least squares problems of geodesy. He died in 1918, and Commandant Benoit published the method in 1924 in the *Bulletin géodésique*, with Cholesky's name. Higham (Section 10.1 and its notes) gives the history and the later error analysis by Wilkinson and Demmel.

## References
