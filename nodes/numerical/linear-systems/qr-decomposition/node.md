---
tag: H9XW97
kind: algorithm
slug: qr-decomposition
name: QR decomposition
aliases:
- QR factorization
- Householder QR
- thin QR factorization
area: numerical/linear-systems
level: core
summary: Factor A = QR with Q orthogonal and R upper triangular, the stable route to least squares.
solves: [least-squares-problem, linear-system-solving]
model: floating-point-model
complexity:
  vars: {m: "the number of rows of A", n: "the number of columns of A, with 1 <= n <= m"}
  time: {worst: Θ(m n^2), best: Θ(m n^2)}
  space: {extra: Θ(n)}
  flops: {worst: "2m n^2 - 2n^3/3"}
properties: {deterministic: true, in_place: true, recursive: false}
prereqs: [householder-reflections, least-squares-problem, matrix-norms]
see_also: [givens-rotations, gram-schmidt-process, normal-equations, rank-revealing-factorization, qr-algorithm, singular-value-decomposition, lup-decomposition, pseudoinverse]
sources:
  - book: isbn:9780898715217
    title: Nicholas J. Higham, Accuracy and Stability of Numerical Algorithms, second edition, SIAM, 2002
    locator: Chapter 19, QR Factorization (Section 19.1, Householder transformations; Section 19.3, error analysis of Householder computations and the backward error of the computed R and Q; Section 19.6, Givens rotations; Section 19.8, Gram-Schmidt orthogonalization); Chapter 20, The Least Squares Problem (Section 20.2, solution by QR factorization)
  - book: isbn:9781421407944
    title: Gene H. Golub and Charles F. Van Loan, Matrix Computations, fourth edition, Johns Hopkins University Press, 2013
    locator: Section 5.1, Householder and Givens Transformations; Section 5.2, The QR Factorization (Householder, block Householder, Givens and Gram-Schmidt versions and their flop counts); Section 5.3, The Full-Rank Least Squares Problem; Section 5.4, Other Orthogonal Factorizations (column pivoting)
  - book: isbn:9780898713619
    title: Lloyd N. Trefethen and David Bau III, Numerical Linear Algebra, SIAM, 1997
    locator: Lecture 7, QR Factorization; Lecture 8, Gram-Schmidt Orthogonalization; Lecture 10, Householder Triangularization; Lecture 11, Least Squares Problems; Lecture 16, Stability of Householder Triangularization
  - paper: doi:10.1145/320941.320947
    title: Alston S. Householder, Unitary triangularization of a nonsymmetric matrix, Journal of the ACM 5(4), 1958
    locator: the reflections I - 2 w w^T and their use to triangularize a matrix
  - paper: doi:10.1007/BF01436075
    title: Gene H. Golub, Numerical methods for solving linear least squares problems, Numerische Mathematik 7, 1965
    locator: Householder QR for least squares, with column pivoting
  - paper: doi:10.1007/BF01436084
    title: Peter Businger and Gene H. Golub, Linear least squares solutions by Householder transformations, Numerische Mathematik 7, 1965
    locator: the Algol procedure with column pivoting
---

A QR decomposition writes a matrix $A \in \mathbb{R}^{m \times n}$, $m \ge n$, as $A = Q R$ with $Q \in \mathbb{R}^{m \times m}$ orthogonal and $R \in \mathbb{R}^{m \times n}$ upper triangular; the *thin* form keeps the first $n$ columns of $Q$ and the top $n \times n$ block of $R$. Householder's method computes it by $n$ reflections in about $2 m n^2 - 2n^3/3$ flops. Orthogonal transformations do not magnify errors, so the computed $\hat R$ is the exact $R$ of a matrix within $O(m n u)$ of $A$, column by column. That makes Householder QR the standard backward stable way to solve [least squares problems](/least-squares-problem/), and a stable, if twice as expensive, alternative to LU for square systems.

## In plain words

Any set of independent columns can be replaced by a set of perpendicular unit columns that spans the same space, plus a triangular table that says how to rebuild each original column from the new ones. The new columns are the orthogonal factor, and the table is the triangular factor. Householder's method builds the table by reflecting the matrix in a mirror, one column at a time, so that everything below the diagonal of that column becomes zero. Mirrors keep lengths unchanged, so rounding errors are never magnified. With the factors in hand, the best fit to more equations than unknowns needs only one triangular solve.

## The problem

Given $A \in \mathbb{R}^{m \times n}$ with $m \ge n \ge 1$, find an orthogonal $Q$ (with $Q^T Q = I$) and an upper triangular $R$ with $A = Q R$. Such a factorization always exists. If $A$ has full column rank, the thin factors $Q_1 \in \mathbb{R}^{m \times n}$, $R_1 \in \mathbb{R}^{n \times n}$ are unique once the diagonal of $R_1$ is required to be positive, and $R_1^T R_1 = A^T A$ is then the Cholesky factorization of $A^T A$.

**Notation.** $\hat Q$, $\hat R$ are the computed factors, $a_j$ is column $j$ of $A$, $u = 2^{-53}$ is the unit roundoff of binary64, $\gamma_k = k u/(1 - k u)$, and $\tilde\gamma_k = c k u/(1 - c k u)$ for a small constant $c$, as in Higham. $\kappa_2(A) = \sigma_1/\sigma_n$. The general notation of this area is on the page [linear system solving](/linear-system-solving/).

**For least squares.** If $A = Q R$ and $Q^T b = (c_1, c_2)$ with $c_1 \in \mathbb{R}^n$, then $\|b - A x\|_2 = \|Q^T b - R x\|_2$, whose square is $\|c_1 - R_1 x\|_2^2 + \|c_2\|_2^2$. So $x = R_1^{-1} c_1$ and the residual norm is $\|c_2\|_2$.

## The algorithm

```pseudo id=main
HOUSEHOLDER-QR(A)                             ▷ A is m × n, m ≥ n; overwritten by R and the vectors
L1  for k ← 1 to n do
L2      α ← −sign(a_kk) · ‖a_{k:m,k}‖_2         ▷ sign(0) = +1; the sign avoids cancellation in L3
L3      v ← a_{k:m,k} − α e_1;  β ← 2/(v^T v)   ▷ H_k = I − β v v^T maps a_{k:m,k} to α e_1
L4      for j ← k+1 to n do a_{k:m,j} ← a_{k:m,j} − β v (v^T a_{k:m,j})
L5      a_kk ← α; store v below the diagonal and β
L6  return R (the upper triangle) and Q = H_1 H_2 ⋯ H_n in factored form
```

Line L2 chooses $\alpha$ with the sign opposite to $a_{kk}$, so the first entry of $v$ is $a_{kk} - \alpha = a_{kk} + \operatorname{sign}(a_{kk})\|a_{k:m,k}\|_2$, a sum of two numbers of the same sign, with no cancellation. If the column $a_{k:m,k}$ is zero, there is nothing to do: $H_k = I$, and $r_{kk} = 0$. Line L4 applies $H_k$ to the remaining columns without forming it, at $4(m - k + 1)$ flops per column. $Q$ is never formed unless asked for: $Q^T b$ is computed by applying $H_1, \ldots, H_n$ in turn to $b$, in $4 m n - 2n^2$ flops. The [Householder reflections](/householder-reflections/) page has the geometry of a single reflection.

## Example

Let

$$A = \begin{pmatrix} 3 & 0 \\ 4 & 5 \\ 0 & 4 \end{pmatrix}, \qquad b = \begin{pmatrix} 1 \\ 2 \\ 3 \end{pmatrix}.$$

**Step $k = 1$.** $\|a_1\|_2 = 5$ and $a_{11} = 3 > 0$, so $\alpha = -5$, $v = (8, 4, 0)^T$, $v^T v = 80$, $\beta = 1/40$. For the second column, $v^T a_2 = 20$, so $a_2 \leftarrow a_2 - \tfrac{20}{40} v = (-4, 3, 4)^T$. For $b$, $v^T b = 16$, so $b \leftarrow b - 0.4 v = (-2.2, 0.4, 3)^T$.

**Step $k = 2$.** The active part of column 2 is $(3, 4)^T$, of norm $5$, so $\alpha = -5$, $v = (8, 4)^T$, $\beta = 1/40$. For $b$, $v^T (0.4, 3)^T = 15.2$, so $(0.4, 3) \leftarrow (0.4, 3) - 0.38 \cdot (8, 4) = (-2.64, 1.48)$.

So $R_1 = \begin{pmatrix} -5 & -4 \\ 0 & -5 \end{pmatrix}$ and $Q^T b = (-2.2, -2.64, 1.48)^T$. Back substitution gives $x_2 = 0.528$ and $x_1 = (-2.2 + 4 \cdot 0.528)/(-5) = 0.0176$, that is $x = (11/625, 330/625)$, which matches the normal equations $\begin{pmatrix} 25 & 20 \\ 20 & 41 \end{pmatrix} x = \begin{pmatrix} 11 \\ 22 \end{pmatrix}$. The residual norm is $|c_2| = 1.48$, and indeed $\|b - A x\|_2^2 = 2.1904 = 1.48^2$. Binary64 reproduces $R_1$ exactly for this matrix.

## Correctness

**Exact arithmetic.** Each $H_k$ is symmetric and orthogonal, and it maps $a_{k:m,k}$ to $\alpha e_1$ because $\|a_{k:m,k}\|_2 = |\alpha|$. It acts only on rows $k, \ldots, m$, so it keeps the zeros created in columns $1, \ldots, k-1$. After step $n$, $H_n \cdots H_1 A = R$ is upper triangular, so $A = Q R$ with $Q = H_1 \cdots H_n$. The details are in [the proof](proofs/correctness.md).

**Backward error of the factorization (proved).** In the [standard model](/floating-point-model/), the computed $\hat R$ satisfies

$$A + \Delta A = Q \hat R, \qquad \|\Delta a_j\|_2 \le \tilde\gamma_{mn} \|a_j\|_2, \quad j = 1, \ldots, n,$$

for an exactly orthogonal $Q$, and the $Q$ formed from the computed vectors satisfies $\|\hat Q - Q\|_F \le \sqrt n\, \tilde\gamma_{mn}$ (Higham, Section 19.3). So $\hat Q$ is orthogonal to working accuracy, $\|\hat Q^T \hat Q - I\| = O(m n u)$, independently of $\kappa(A)$. This is the main difference from Gram-Schmidt.

**Least squares (proved).** The solution $\hat x$ computed by Householder QR is the exact least squares solution of $\min \|(b + \Delta b) - (A + \Delta A) x\|_2$ with $\|\Delta a_j\|_2 \le \tilde\gamma_{mn}\|a_j\|_2$ and $\|\Delta b\|_2 \le \tilde\gamma_{mn}\|b\|_2$ (Higham, Section 20.2). With the perturbation theory of least squares this gives a forward error of order $u\,(\kappa_2(A) + \kappa_2(A)^2 \|r\|_2/(\|A\|_2\|x\|_2))$, to first order. When the residual is small, this is about $u\,\kappa_2(A)$, the square root of the loss of the [normal equations](/normal-equations/).

**Observed constants.** In the tests, on 30 random Gaussian matrices with $m \le 12$, both $\|A - \hat Q \hat R\|_F/\|A\|_F$ and $\|\hat Q^T \hat Q - I\|_F$, measured in exact rational arithmetic, stay below $4 m n u$, and the largest ratios occur for the smallest matrices (observed).

## Complexity

Step $k$ computes a norm of length $m - k + 1$ and updates $n - k$ columns at $4(m - k + 1)$ flops each. Summing, $\sum_k 4(m - k + 1)(n - k) = 2 m n^2 - 2n^3/3 + O(m n)$ flops (Golub and Van Loan, Section 5.2). For a square matrix this is $4n^3/3$, twice the cost of the [LUP decomposition](/lup-decomposition/). Forming $Q$ explicitly costs about as much again, and is seldom needed. The factorization overwrites $A$; the extra storage is the $n$ scalars $\beta_k$ (or the first entries of the vectors), so $\Theta(n)$. The column-by-column form above does matrix-vector work and is limited by memory bandwidth; the blocked form, which aggregates $b$ reflectors as $I - V T V^T$ (the compact WY form), does most of its flops as matrix-matrix products.

## Properties

- **Backward stable**, column by column, with no growth factor: the bound does not depend on pivoting or on $A$.
- **Orthogonal factor accurate to working precision**, for every $A$.
- **Rank information only with pivoting.** Without column pivoting a small $|r_{kk}|$ signals near rank deficiency, but a near rank-deficient $A$ need not produce one; see [rank-revealing factorization](/rank-revealing-factorization/).
- **Invariant under column scaling** in exact arithmetic up to the scaling of $R$, and the columnwise bound makes it insensitive to bad column scaling in floating point too.
- **Uniqueness.** With full column rank and a positive diagonal, $R_1$ equals the Cholesky factor of $A^T A$, so all stable methods compute the same $R_1$ up to signs.

## Variants and improvements

- **[Givens rotations](/givens-rotations/).** Zero one entry at a time with plane rotations, at $3 m n^2 - n^3$ flops for a dense matrix. Better for sparse or structured matrices, such as Hessenberg ones ($O(n^2)$ flops), and for updating a QR factorization when a row is added.
- **[Gram-Schmidt](/gram-schmidt-process/).** Classical and modified Gram-Schmidt compute the thin $Q_1$ and $R_1$ directly in $2 m n^2$ flops. Modified Gram-Schmidt gives $\|\hat Q_1^T \hat Q_1 - I\|_2 = O(u\,\kappa_2(A))$, and classical Gram-Schmidt can lose orthogonality like $u\,\kappa_2(A)^2$ or worse (Higham, Section 19.8). Reorthogonalization ("twice is enough") restores orthogonality to working precision. MGS is still a backward stable way to solve least squares if $Q^T b$ is computed as an extra column.
- **Column pivoting.** At step $k$, swap the column of largest remaining norm into position $k$ (Businger and Golub, 1965). This gives $|r_{11}| \ge |r_{22}| \ge \cdots$ and usually reveals the numerical rank; strong rank-revealing versions guarantee it (see [rank-revealing factorization](/rank-revealing-factorization/)).
- **Blocked and tall-skinny QR.** The compact WY form gives level-3 performance, and TSQR factors a tall matrix by a reduction tree of small QRs, which minimizes communication in parallel.
- **Sparse QR.** The fill of $R$ is that of the Cholesky factor of $A^T A$; sparse QR orders the columns to reduce it and uses a multifrontal method (Davis, Chapter 5).
- **Complex matrices.** The same algorithm works with unitary reflections $I - \beta v v^*$.

## When to use it

Use Householder QR for dense least squares problems of full rank, especially when $\kappa_2(A)$ is too large for the [normal equations](/normal-equations/) or the residual is small. Use QR with column pivoting, or the [SVD](/singular-value-decomposition/), when $A$ may be rank deficient. For square systems, LU with partial pivoting is half the cost and almost always as accurate; QR is the choice when guaranteed backward stability without a growth factor is required. QR of a Hessenberg or tridiagonal matrix is the inner step of the [QR algorithm](/qr-algorithm/) for eigenvalues.

## Pitfalls

- **The wrong sign in line L2** makes $v_1 = a_{kk} - \|a_{k:m,k}\|_2$, which cancels when $a_{k:m,k}$ is nearly a positive multiple of $e_1$. Either choose the sign as above or use Parlett's formula $v_1 = -(\sum_{i>k} a_{ik}^2)/(a_{kk} + \|a_{k:m,k}\|_2)$.
- **Overflow in the norm.** Squaring entries near $10^{154}$ overflows; scale the column by its largest entry first, as the implementation does.
- **Forming $Q$ when it is not needed** costs $O(m^2 n)$ flops and $m^2$ storage for the full $Q$; apply the reflectors to $b$ instead.
- **Classical Gram-Schmidt for least squares.** Its $Q_1$ can be far from orthogonal, and solving with $Q_1^T b$ then gives large errors on ill-conditioned problems.
- **Assuming a small $r_{kk}$ will appear.** For Kahan's matrix, no $r_{kk}$ is small without pivoting although $A$ is nearly singular.

## Implementations

## History

Orthogonalization of vectors goes back to Laplace and to Schmidt's paper of 1907, and the name Gram-Schmidt honors Gram (1883) and Schmidt. Givens (1958) used plane rotations and Householder (1958) introduced the reflections that bear his name, both for eigenvalue problems. Golub (1965) showed how Householder QR solves least squares problems stably, and Businger and Golub (1965) published the program with column pivoting. The QR factorization is also the core of the [QR algorithm](/qr-algorithm/) of Francis and Kublanovskaya (1961). Wilkinson analyzed the rounding errors of Householder transformations in the 1960s; Higham (Chapter 19) gives the modern columnwise form.

## References
