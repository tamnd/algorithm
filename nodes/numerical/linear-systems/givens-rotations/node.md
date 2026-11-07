---
tag: 8EQDS2
kind: technique
slug: givens-rotations
name: Givens rotations
aliases:
- Givens transformation
- plane rotations
- Jacobi rotations
area: numerical/linear-systems
level: advanced
summary: Plane rotations that zero a single entry at a time, useful for sparse and structured matrices.
prereqs: [matrix-norms, backward-error-analysis, floating-point-model]
see_also: [householder-reflections, qr-decomposition, gmres, qr-algorithm, least-squares-problem, sparse-matrix, singular-value-decomposition, minres]
sources:
  - paper: doi:10.1137/0106004
    title: Wallace Givens, Computation of plane unitary rotations transforming a general matrix to triangular form, Journal of the Society for Industrial and Applied Mathematics 6(1), 1958
    locator: pp. 26 to 50 (triangularization by plane rotations)
  - book: isbn:9781421407944
    title: Gene H. Golub and Charles F. Van Loan, Matrix Computations, fourth edition, Johns Hopkins University Press, 2013
    locator: Section 5.1.8 to 5.1.13 (Givens rotations, Algorithm 5.1.3, applying and storing them, fast Givens); Section 5.2.5, Givens QR; Section 5.2.6, Hessenberg QR via Givens
  - book: isbn:9780898715217
    title: Nicholas J. Higham, Accuracy and Stability of Numerical Algorithms, second edition, SIAM, 2002
    locator: Chapter 19, Section 19.6, Givens rotations (error of one rotation and of disjoint rotation sequences; Givens QR)
  - paper: doi:10.1093/imamat/12.3.329
    title: W. Morven Gentleman, Least squares computations by Givens transformations without square roots, IMA Journal of Applied Mathematics 12(3), 1973
    locator: pp. 329 to 336 (square root free rotations)
  - paper: doi:10.1145/567806.567809
    title: David Bindel, James Demmel, William Kahan and Osni Marques, On computing Givens rotations reliably and efficiently, ACM Transactions on Mathematical Software 28(2), 2002
    locator: pp. 206 to 238 (scaling to avoid overflow, sign conventions, LAPACK dlartg)
  - paper: doi:10.1007/BF01462266
    title: G. W. Stewart, The economical storage of plane rotations, Numerische Mathematik 25(2), 1976
    locator: pp. 137 to 138 (one number per rotation)
---

A Givens rotation is the identity matrix with a $2 \times 2$ rotation $\begin{pmatrix} c & s \\ -s & c \end{pmatrix}$, $c^2 + s^2 = 1$, placed in rows and columns $i$ and $k$. Applied from the left, it mixes only rows $i$ and $k$, and with $c = a/r$, $s = b/r$, $r = \sqrt{a^2 + b^2}$ it sends the pair $(a, b)$ to $(r, 0)$. So one rotation zeros one chosen entry at a cost of $6$ flops per column touched. Dense QR by rotations costs $3 n^2 (m - n/3)$ flops, about $1.5$ times [Householder](/householder-reflections/) QR, but when only a few entries must be zeroed, as in Hessenberg, banded, sparse or updating problems, rotations do exactly the needed work. They are backward stable for the same reason as reflections: each is orthogonal, and the rounding error of one application is a relative perturbation of order $u$.

## In plain words

Turning a flat arrow in a plane can make it point straight along one axis without changing its length. A Givens rotation does this for two rows of a matrix at a time, chosen so that one entry turns into zero. Everything outside those two rows is left alone. To clear the bottom of a matrix you rotate pair after pair, one zero at a time. This costs more than a single big reflection on a full matrix, but when the matrix is mostly zeros already, only the few entries that need clearing are touched.

## When it applies

Use rotations when an orthogonal transformation must zero a few specific entries and leave the rest of the structure intact: an upper Hessenberg matrix (one subdiagonal), a banded or sparse matrix, a matrix with one appended row or column (updating a QR factorization), or a step of an iterative method that grows a small matrix one column at a time. They also parallelize well, since rotations in disjoint row pairs commute.

**Notation.** $A \in \mathbb{R}^{m \times n}$; $G(i, k, \theta)$ is the rotation in the $(i, k)$ plane, with $c = \cos\theta$ and $s = \sin\theta$; $G^T$ applied to rows $i, k$ replaces $(a_{ij}, a_{kj})$ by $(c\, a_{ij} + s\, a_{kj},\ -s\, a_{ij} + c\, a_{kj})$. The unit roundoff is $u = 2^{-53}$, and $\tilde\gamma_k = c' k u/(1 - c' k u)$ with a small constant $c'$, as in Higham.

## The template

```pseudo id=main
GIVENS(a, b)                                        ▷ returns c, s, r with [c s; −s c][a; b] = [r; 0]
L1  if b = 0 then return c = 1, s = 0, r = a
L2  if |b| > |a| then                               ▷ hole: the scaling that avoids overflow
L3      τ ← a / b; s ← sign(b) / sqrt(1 + τ²); c ← s · τ
L4  else
L5      τ ← b / a; c ← sign(a) / sqrt(1 + τ²); s ← c · τ
L6  r ← c · a + s · b
L7  return c, s, r
ROT(A, i, k, c, s, J)                               ▷ rows i and k, columns in J
L8  for j in J do                                   ▷ hole: the columns where row i or k is nonzero
L9      (a_ij, a_kj) ← (c · a_ij + s · a_kj, −s · a_ij + c · a_kj)
```

The holes are the scaling in GIVENS and the column set $J$. Dividing by the larger of $|a|$ and $|b|$ (lines L2 to L5) keeps $1 + \tau^2 \in [1, 2]$, so nothing overflows even when $a^2 + b^2$ would. This version always returns $r = \sqrt{a^2 + b^2} \ge 0$; conventions for the sign of $r$ differ between texts and libraries, and Bindel, Demmel, Kahan and Marques (2002) discuss the choice made in LAPACK's `dlartg`. Line L9 must use the old $a_{ij}$ in both parts.

**Correctness.** With $\rho = \sqrt{a^2 + b^2}$, the scaled formulas give $c = a/\rho$ and $s = b/\rho$ (for $|b| > |a|$, $|b| \sqrt{1 + \tau^2} = \rho$, so $s = b/\rho$ and $c = s\tau = a/\rho$; the other branch is symmetric), so $c^2 + s^2 = 1$, $-s a + c b = 0$ and $c a + s b = \rho$.

**Cost.** GIVENS: about $5$ flops, one square root and one division. ROT: $4$ multiplications and $2$ additions per column, $6 |J|$ flops.

**Error of one rotation (proved).** The computed $\hat c$, $\hat s$ satisfy $\hat c = c(1 + \theta_1)$, $\hat s = s(1 + \theta_2)$ with $|\theta_i| \le \tilde\gamma_1$, and applying them gives $\mathrm{fl}(\hat G^T x) = (G + \Delta G)^T x$ with $\|\Delta G\|_F \le \tilde\gamma_1$, where $G$ is the exact rotation (Higham, Section 19.6). A sequence of rotations that can be grouped into $t$ stages of rotations acting on disjoint row pairs gives a backward error with $t\, \tilde\gamma_1$ in place of $\tilde\gamma_1$ per column.

## Classic examples

**One pair.** For $(a, b) = (3, 4)$: $|b| > |a|$, $\tau = 3/4$, $s = 1/\sqrt{1 + 9/16} = 4/5$, $c = 3/5$, $r = 9/5 + 16/5 = 5$.

**Givens QR.** Zero the subdiagonal entries column by column, from the bottom up. For

$$A = \begin{pmatrix} 1 & 1 \\ 2 & 0 \\ 2 & 1 \end{pmatrix},$$

rotate rows $2, 3$ with $(a, b) = (2, 2)$, so $c = s = 1/\sqrt 2$; the rows become $(2\sqrt 2,\ 1/\sqrt 2)$ and $(0,\ 1/\sqrt 2)$. Rotate rows $1, 2$ with $(a, b) = (1, 2\sqrt2)$, so $c = 1/3$, $s = 2\sqrt 2/3$; the rows become $(3, 1)$ and $(0, -1/\sqrt 2)$. Rotate rows $2, 3$ with $(a, b) = (-1/\sqrt 2, 1/\sqrt 2)$, $r = 1$; row $2$ becomes $(0, 1)$ and row $3$ becomes $0$. So $R = \begin{pmatrix} 3 & 1 \\ 0 & 1 \end{pmatrix}$ and $R^T R = A^T A$. The [Householder](/householder-reflections/) factor of the same matrix is $\operatorname{diag}(-1, -1) R$: the two differ only in the signs of the rows. For dense $A$ there are $m n - n(n+1)/2$ rotations, and the cost is $3 n^2 (m - n/3)$ flops (Golub and Van Loan, Section 5.2.5). With the column-by-column order, the rotations can be scheduled in $m + n - 2$ stages of disjoint pairs, and the computed $\hat R$ satisfies $A + \Delta A = Q \hat R$ with $Q$ exactly orthogonal and $\|\Delta a_j\|_2 \le \tilde\gamma_{m + n - 2} \|a_j\|_2$ (Higham, Section 19.6, proved).

**Hessenberg QR.** An upper Hessenberg $H \in \mathbb{R}^{n \times n}$ needs only $n - 1$ rotations, one per subdiagonal entry, and $3 n^2$ flops in total, against $O(n^3)$ for dense QR (Golub and Van Loan, Section 5.2.6). This is the inner step of the [QR algorithm](/qr-algorithm/) on Hessenberg matrices.

**GMRES and MINRES.** In [GMRES](/gmres/) the Arnoldi process adds one column to an $(k+1) \times k$ Hessenberg matrix per step. Applying the $k - 1$ previous rotations to the new column and one new rotation to zero its last entry updates the QR factorization in $O(k)$ flops, and the last component of the rotated right side gives the residual norm $\|r_k\|_2$ at no extra cost. [MINRES](/minres/) does the same on a tridiagonal matrix with $O(1)$ work per step.

**Updating a factorization.** If $A = Q R$ and a row $w^T$ is appended, then $\begin{pmatrix} R \\ w^T \end{pmatrix}$ is upper triangular except for the last row, and $n$ rotations restore triangular form in $3 n^2$ flops instead of a new $O(m n^2)$ factorization. This is how recursive least squares and sliding window fits are computed stably (Golub and Van Loan, Section 6.5).

**Jacobi eigenvalue and SVD methods.** Two-sided rotations $G^T A G$ that zero an off-diagonal pair of a symmetric matrix give the Jacobi eigenvalue method; one-sided rotations of column pairs give the one-sided Jacobi SVD, which can compute small singular values to high relative accuracy.

## Variations

- **Fast Givens.** Gentleman (1973) and Hammarling (1974) keep $A$ in the form $D^{1/2} \tilde A$ and update $\tilde A$ with matrices of the form $\begin{pmatrix} 1 & \alpha \\ \beta & 1 \end{pmatrix}$, which removes the square roots and a third of the multiplications. Dense QR costs $2 n^2 (m - n/3)$ flops, like Householder, but the diagonal must be rescaled now and then to avoid overflow or underflow (Golub and Van Loan, Section 5.1.13).
- **Storing one number per rotation.** Stewart (1976) encodes $(c, s)$ as one number $\rho$ (for example $\rho = s$ if $|s| < |c|$, else $\operatorname{sign}(s)/c$), so $Q$ can be kept in the zeroed entries.
- **Complex rotations.** For complex data, $\begin{pmatrix} c & s \\ -\bar s & c \end{pmatrix}$ with real $c$ and complex $s$, $c^2 + |s|^2 = 1$.
- **Hyperbolic rotations.** $\begin{pmatrix} c & -s \\ -s & c \end{pmatrix}$ with $c^2 - s^2 = 1$ remove a row from a Cholesky factor (downdating). They are not orthogonal and can be unstable when $|s|$ is large.
- **Parallel orderings.** Sameh and Kuck's scheme zeros entries along anti-diagonals, giving $m + n - 2$ stages of independent rotations for Givens QR.

## Pitfalls

- **Overflow in $\sqrt{a^2 + b^2}$.** Squaring overflows for $|a| > 10^{154}$ and underflows below $10^{-154}$, even when $r$ is representable. Use the scaled form of lines L2 to L5 or `hypot`.
- **Using the updated $a_{ij}$.** Writing $a_{ij} \leftarrow c a_{ij} + s a_{kj}$ and then $a_{kj} \leftarrow -s a_{ij} + c a_{kj}$ uses the new $a_{ij}$ and gives a matrix that is not orthogonal. Keep a temporary.
- **Rotations on a dense matrix.** For a full column, $m - 1$ rotations cost $6 m$ flops per column touched, against $4 m$ for one reflector. Use Householder for dense blocks.
- **Fill in sparse problems.** A rotation of rows $i$ and $k$ gives both rows the union of their patterns. A poor row order in sparse QR creates much fill, which is why sparse QR codes order columns first (as for the [Cholesky factor](/cholesky-decomposition/) of $A^T A$) and then rotate rows in a matching order.
- **Inconsistent sign convention.** Different formulas give $r$ of different signs. Code that combines rotations from one source with formulas from another can mis-sign a factor; fix one convention.

## Exercises

1. Show that $G(i, k, \theta)$ is orthogonal and that it changes only rows $i$ and $k$ of $A$.
2. Prove that the scaled formulas of lines L2 to L5 never overflow if $a$ and $b$ are finite and not both zero.
3. Count the rotations and flops of Givens QR on a dense $m \times n$ matrix and show that the leading term is $3 m n^2 - n^3$.
4. Show that Givens QR of an upper Hessenberg matrix costs $3 n^2 + O(n)$ flops, and that $Q$ is again upper Hessenberg.
5. Give the order of rotations that zeros a dense $4 \times 3$ matrix in $m + n - 2 = 5$ stages of disjoint pairs.
6. In GMRES, show that after the $k$ rotations the last entry of the rotated right side $\beta Q_k^T e_1$ has absolute value $\|r_k\|_2$.

## References
