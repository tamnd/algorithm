---
tag: PQ8J25
kind: problem
slug: triangular-system-solving
name: Triangular system solving
aliases:
- solving Lx = b or Ux = b
- forward substitution
- triangular solve
- TRSV
area: numerical/linear-systems
level: intro
summary: Solve a system whose matrix is lower or upper triangular.
model: floating-point-model
complexity:
  vars: {n: "the order of T, at least 1"}
  time: {worst: Θ(n^2)}
  flops: {worst: n^2}
prereqs: [floating-point-model, matrix-norms]
see_also: [back-substitution, lup-solve, lup-decomposition, cholesky-decomposition, qr-decomposition, linear-system-solving, banded-matrix, condition-number]
sources:
  - book: isbn:9780898715217
    title: Nicholas J. Higham, Accuracy and Stability of Numerical Algorithms, second edition, SIAM, 2002
    locator: Chapter 8, Triangular Systems (Section 8.1, backward error analysis, Theorem 8.5, the bound |ΔT| ≤ γ_n |T| for substitution in any order; Section 8.2, forward error analysis, including triangular M-matrices; Section 8.3, bounds for the inverse; Section 8.4, a parallel fan-in algorithm)
  - book: isbn:9781421407944
    title: Gene H. Golub and Charles F. Van Loan, Matrix Computations, fourth edition, Johns Hopkins University Press, 2013
    locator: Section 3.1, Triangular Systems (row and column oriented forward and back substitution, multiple right sides, and the level-3 block form)
  - book: isbn:9780898713619
    title: Lloyd N. Trefethen and David Bau III, Numerical Linear Algebra, SIAM, 1997
    locator: Lecture 17, Stability of Back Substitution (the backward stability theorem and its proof)
  - book: isbn:9780898716139
    title: Timothy A. Davis, Direct Methods for Sparse Linear Systems, SIAM, 2006
    locator: Chapter 3, Solving Triangular Systems (dense and sparse right sides, and the reach of the right side in the graph of L)
---

A triangular system is a linear system $T x = b$ in which $T$ is lower triangular (all entries above the diagonal are zero) or upper triangular (all entries below are zero). It is solved by *substitution*, one unknown at a time, in exactly $n^2$ flops, and this solve is the last step of each direct method: [LU](/lup-decomposition/), [Cholesky](/cholesky-decomposition/) and [QR](/qr-decomposition/) all reduce $A x = b$ to one or two triangular systems. Substitution is backward stable in a strong, componentwise sense, and in practice it is often far more accurate than the [condition number](/condition-number/) of $T$ predicts.

## In plain words

In a triangular system the first equation has only one unknown, so you can solve it at once. The second equation has the first unknown and one new one; with the first already known, you solve for the new one. Each next equation adds one new unknown, and you go down the list until all are known. When the triangle points the other way, you start from the last equation and go up.

Each new value costs one division and a few multiplications and subtractions, so the work grows with the square of the number of unknowns. The method fails only when a diagonal entry is zero, which means the system has no unique answer. The rounding errors are tiny in a strong sense: each computed value is the exact answer for a matrix whose entries changed by a few roundings each.

## Definition

**Notation.** As in [solving linear systems](/linear-system-solving/): $T = (t_{ij})$ is an $n \times n$ real triangular matrix, $b \in \mathbb{R}^n$, $x$ is the exact solution, $\hat x$ the computed one, $|T|$ the matrix of the $|t_{ij}|$, $u$ the unit roundoff ($2^{-53}$ in binary64), and $\gamma_n = n u/(1 - n u)$. We write $L$ for a lower and $U$ for an upper triangular $T$.

**Input.** A triangular $T \in \mathbb{R}^{n \times n}$ and $b \in \mathbb{R}^n$ (or $B \in \mathbb{R}^{n \times k}$).

**Output.** $x$ with $T x = b$, or the report that $T$ is singular. Because $\det T = \prod_i t_{ii}$, the solution exists and is unique for each $b$ exactly when each $t_{ii} \ne 0$.

**Forward substitution** for $L x = b$:

$$x_i = \Bigl(b_i - \sum_{j=1}^{i-1} l_{ij} x_j\Bigr) \Big/ l_{ii}, \qquad i = 1, 2, \ldots, n,$$

and **back substitution** for $U x = b$ runs $i = n, n-1, \ldots, 1$ with the sum over $j > i$. The page [back substitution](/back-substitution/) gives the algorithm, its proof and its code.

**Backward error (proved).** Assume the [standard model](/floating-point-model/) and $n u < 1$. Substitution, with the inner sums done in any order, computes $\hat x$ with

$$(T + \Delta T)\hat x = b, \qquad |\Delta T| \le \gamma_n |T|$$

(Higham, Theorem 8.5). The perturbation is componentwise and only in $T$: each entry moves by at most $\gamma_n$ times its own size, and zero entries do not move. So the componentwise backward error $\omega(\hat x)$ of the [residual](/residual/) page is at most $\gamma_n$.

**Forward error.** From the backward bound, for $\gamma_n\, \mathrm{cond}(T) < 1$,

$$\frac{\|x - \hat x\|_\infty}{\|x\|_\infty} \le \frac{\gamma_n\, \mathrm{cond}(T, x)}{1 - \gamma_n\, \mathrm{cond}(T)}, \qquad \mathrm{cond}(T, x) = \frac{\|\,|T^{-1}|\,|T|\,|x|\,\|_\infty}{\|x\|_\infty},$$

with $\mathrm{cond}(T) = \|\,|T^{-1}|\,|T|\,\|_\infty \le \kappa_\infty(T)$ (Higham, Section 8.2, from the componentwise perturbation theory of Section 7.2). This bound is invariant under row scaling of $T$, unlike $\kappa_\infty(T)$.

## Variants

- **Lower or upper, unit or not.** A *unit* triangular matrix has $t_{ii} = 1$, and the divisions vanish; the $L$ of LU is unit lower triangular.
- **Row and column orientation.** The row form computes each $x_i$ as a dot product. The column form (*saxpy* form) subtracts $x_j$ times column $j$ from $b$ as soon as $x_j$ is known. Both do the same flops; the column form suits column-major storage (Golub and Van Loan, Section 3.1).
- **Many right sides.** $T X = B$ with $B \in \mathbb{R}^{n \times k}$ costs $n^2 k$ flops, and a blocked form does most of it as matrix products (BLAS level 3, `xTRSM`), which matters more than the flop count on cached machines.
- **Transposed systems.** $T^T x = b$ is again triangular, of the other kind; the Cholesky solve uses $R^T y = b$ and then $R x = y$.
- **Banded triangular.** If $t_{ij} = 0$ for $|i - j| > p$, the cost drops to about $2np$ flops; see [banded matrix](/banded-matrix/).
- **Sparse triangular.** For a sparse $L$ and a sparse $b$, the nonzero pattern of $x$ is the set of nodes reachable from the nonzeros of $b$ in the graph of $L$, and the solve costs time proportional to the flops, not to $n$ (Davis, Chapter 3).
- **Inverse.** $T^{-1}$ is triangular of the same kind and costs $n^3/3$ flops; it is rarely needed, because a solve is cheaper and more accurate.

## Examples

**A $3 \times 3$ forward substitution.** Let $L = \begin{pmatrix} 2 & 0 & 0 \\ 1 & 3 & 0 \\ -1 & 2 & 4 \end{pmatrix}$ and $b = (2, -5, 7)^T$.

| $i$ | $b_i - \sum_{j<i} l_{ij} x_j$ | $x_i$ |
|---|---|---|
| 1 | $2$ | $2/2 = 1$ |
| 2 | $-5 - 1 \cdot 1 = -6$ | $-6/3 = -2$ |
| 3 | $7 - (-1)(1) - 2(-2) = 12$ | $12/4 = 3$ |

So $x = (1, -2, 3)^T$, computed with no rounding because each value is a small integer.

**A singular triangle.** $U = \begin{pmatrix} 1 & 2 \\ 0 & 0 \end{pmatrix}$ has $\det U = 0$. Back substitution reaches $x_2 = b_2 / 0$, and the system has no solution if $b_2 \ne 0$ and infinitely many if $b_2 = 0$. A solver tests $t_{ii} = 0$ before it divides and reports the singularity.

**Ill conditioned, yet accurate.** Let $U_n$ be the upper triangular matrix with $1$ on the diagonal and $-1$ above it. Its inverse has entries $2^{j-i-1}$ above the diagonal, so $\|U_n\|_\infty = n$, $\|U_n^{-1}\|_\infty = 2^{n-1}$ and $\kappa_\infty(U_n) = n\, 2^{n-1}$; for $n = 60$ this is about $3.5 \times 10^{19}$, beyond $1/u$. Back substitution in binary64 on $U_{60} x = b$, with $b$ drawn uniformly from $[-1, 1]$ by `random.Random(1)`, gives a relative error $\|x - \hat x\|_\infty/\|x\|_\infty \approx 1.8 \times 10^{-16}$ against the exact rational solution. Here $U_n$ is a triangular M-matrix. For such a matrix and $b \ge 0$, Higham (Section 8.2) proves a componentwise forward error bound, $|x - \hat x| \le c_n u |x|$ with $c_n$ a low-degree polynomial in $n$, that does not depend on $\kappa$; this $b$ has entries of both signs, so the small error here is observed, not covered by that theorem. Higham (Chapter 8) also quotes Wilkinson's observation that triangular systems from pivoted factorizations are usually solved far more accurately than $\kappa(T) u$ suggests.

## Known algorithms

- [Back substitution](/back-substitution/) and forward substitution: $n^2$ flops, backward stable with $|\Delta T| \le \gamma_n |T|$.
- The solve phase of [LUP solve](/lup-solve/): one forward and one back substitution, $2n^2$ flops.
- The [Thomas algorithm](/thomas-algorithm/) ends with a bidiagonal back substitution in $3n$ flops.
- Parallel fan-in (Sameh and Brent): write $L = L_1 L_2 \cdots L_n$ with elementary factors and multiply the inverses $L_i^{-1}$ in a binary tree. The depth is $O(\log^2 n)$ with $O(n^3)$ processors, and the error bounds are weaker than those of substitution (Higham, Section 8.4).

## Bounds

- **Upper bound.** $n^2$ flops in the [floating-point model](/floating-point-model/) for a dense $T$: $n$ divisions, $n(n-1)/2$ multiplications and $n(n-1)/2$ subtractions. For $k$ right sides, $n^2 k$ flops.
- **Lower bound.** Each algorithm that is correct for each dense $T$ must read each of the $n(n+1)/2$ entries that can be nonzero, so $\Omega(n^2)$ operations are needed. Substitution is optimal up to the constant factor.
- **Multiple right sides.** With fast matrix multiplication, $T X = B$ for $k = n$ costs $O(n^\omega)$ by recursive blocking; this is used in exact arithmetic, not in floating point libraries.

## Reductions

- **From general systems.** $A x = b$ reduces to two triangular solves after $PA = LU$ ($2n^3/3$ flops), after $A = R^T R$ ($n^3/3$) or after $A = QR$ ($4n^3/3$ for Householder QR on a square matrix).
- **To matrix multiplication.** For many right sides, a block triangular solve reduces to half-size triangular solves and one matrix product, so the cost is that of matrix multiplication up to a constant factor.
- **Inversion and solving.** Computing $T^{-1}$ reduces to $n$ triangular solves with the columns of $I$.

## Applications

- The last step of each dense direct solver, and of the sparse direct solvers ([multifrontal method](/multifrontal-method/)).
- Applying a triangular preconditioner, such as an [incomplete Cholesky](/incomplete-cholesky-factorization/) or an [incomplete LU](/incomplete-lu-factorization/) factor, once in each iteration of a Krylov method.
- The [Gauss-Seidel method](/gauss-seidel-method/): each sweep solves a lower triangular system with the lower triangle of $A$.
- Least squares by [QR](/qr-decomposition/): $R x = Q^T b$.

## References
