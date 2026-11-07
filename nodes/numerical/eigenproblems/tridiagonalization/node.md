---
tag: 9W3V78
kind: algorithm
slug: tridiagonalization
name: Householder tridiagonalization
aliases:
- reduction to tridiagonal form
- Householder reduction to tridiagonal form
- symmetric tridiagonal reduction
area: numerical/eigenproblems
level: core
summary: An orthogonal similarity A = Q T Q^T of a symmetric matrix to tridiagonal form by n - 2 Householder reflectors and symmetric rank-2 updates, in 4n^3/3 flops.
solves: [symmetric-eigenproblem]
model: floating-point-model
complexity:
  vars: {n: "the order of A"}
  time: {worst: Θ(n^3)}
  space: {extra: Θ(n)}
  flops: {worst: "4n^3/3 + O(n^2)", with_q: "8n^3/3 + O(n^2)"}
properties: {deterministic: true, in_place: true, recursive: false, iterative: false}
history:
  year: 1958
  people: [Alston S. Householder, J. H. Wilkinson, Wallace Givens]
  note: Givens reduced symmetric matrices to tridiagonal form by rotations in 1954; Householder's reflectors of 1958 halved the work, and Wilkinson analysed the method and made it the standard in 1960.
prereqs: [householder-reflections, symmetric-eigenproblem, similarity-transformation]
see_also: [tridiagonal-eigenproblem, hessenberg-reduction, lanczos-algorithm, qr-algorithm, givens-rotations, divide-and-conquer-eigensolver, mrrr-algorithm, jacobi-eigenvalue-algorithm]
sources:
  - book: isbn:9781421407944
    title: Gene H. Golub and Charles F. Van Loan, Matrix Computations, fourth edition, Johns Hopkins University Press, 2013
    locator: Section 8.3.1 (Householder tridiagonalization, Algorithm 8.3.1, the 4n^3/3 flop count, the accumulation of Q and the backward error)
  - book: isbn:9780898713619
    title: Lloyd N. Trefethen and David Bau III, Numerical Linear Algebra, SIAM, 1997
    locator: Lecture 26 (reduction to Hessenberg or tridiagonal form, operation counts and stability)
  - book: isbn:9780898713893
    title: James W. Demmel, Applied Numerical Linear Algebra, SIAM, 1997
    locator: Section 4.4.7 (reduction to Hessenberg and tridiagonal form), Section 5.3 (the cost of the reduction compared with the tridiagonal solvers)
  - book: "J. H. Wilkinson, The Algebraic Eigenvalue Problem, Oxford University Press, 1965"
    title: J. H. Wilkinson, The Algebraic Eigenvalue Problem
    locator: Chapter 3 (error analysis of Householder transformations), Chapter 5 (Givens' and Householder's methods for symmetric matrices)
  - paper: "Alston S. Householder, Unitary triangularization of a nonsymmetric matrix, Journal of the ACM 5, 1958"
    title: Unitary triangularization of a nonsymmetric matrix
    locator: J. ACM 5(4) (1958), pp. 339 to 342
  - paper: "J. H. Wilkinson, Householder's method for the solution of the algebraic eigenproblem, The Computer Journal 3, 1960"
    title: Householder's method for the solution of the algebraic eigenproblem
    locator: Comput. J. 3(1) (1960), pp. 23 to 27
  - paper: "J. J. Dongarra, S. J. Hammarling and D. C. Sorensen, Block reduction of matrices to condensed forms for eigenvalue computations, Journal of Computational and Applied Mathematics 27, 1989"
    title: Block reduction of matrices to condensed forms for eigenvalue computations
    locator: J. Comput. Appl. Math. 27 (1989), pp. 215 to 227
---

Householder tridiagonalization computes an orthogonal $Q$ and a symmetric tridiagonal $T$ with $A = Q T Q^T$ for a real symmetric $A$. It applies $n - 2$ Householder reflectors as similarities; reflector $k$ zeros column $k$ below the subdiagonal, and by symmetry row $k$ to the right of the superdiagonal. Because each reflector is applied from both sides, the update of the trailing block can be written as a symmetric rank-2 change, which computes only one triangle and brings the cost to $4n^3/3$ flops, half that of the [Hessenberg reduction](/hessenberg-reduction/) of a general matrix. The result is backward stable: the computed $T$ is exactly similar to $A + E$ with $\|E\|_2 = O(n u)\|A\|_2$. It is the first phase of every dense [symmetric eigensolver](/symmetric-eigenproblem/), whose second phase solves the [tridiagonal eigenproblem](/tridiagonal-eigenproblem/).

## In plain words

A symmetric table full of numbers is slow to work with directly. This method cleans it up column by column. At each step it picks a mirror that folds the part of the current column below the diagonal onto a single entry, and applies that mirror on both sides so the answers do not change. When it is done, only the main diagonal and its two neighbours are left. The mirrors are kept, so the directions found for the thin table can later be turned back into directions for the original one.

## The problem

**Notation.** $A \in \mathbb R^{n \times n}$ symmetric with eigenvalues $\lambda_1 \ge \dots \ge \lambda_n$. $T$ is symmetric tridiagonal with diagonal $d_1, \dots, d_n$ and off-diagonal $e_1, \dots, e_{n-1}$. $P_k = I - \beta_k v_k v_k^T$ is a Householder reflector acting on rows and columns $k + 1$ to $n$, with $\beta_k = 2 / v_k^T v_k$, or $\beta_k = 0$ and $P_k = I$. Indices in the pseudocode are 1-based, and $A[i..j, k..l]$ is a submatrix. $u$ is the unit roundoff.

Given $A$, return $d$, $e$ and, if asked, $Q$ orthogonal with $A = Q T Q^T$ and $Q e_1 = e_1$. For a complex Hermitian $A$ the same algorithm with complex reflectors gives a Hermitian tridiagonal $T$, which a diagonal unitary scaling makes real.

## The algorithm

```pseudo id=main
TRIDIAGONALIZE(A)                                ▷ reads and overwrites the lower triangle of A
L1  Q ← I_n
L2  for k ← 1 to n − 2 do
L3      x ← A[k+1 .. n, k]
L4      (v_k, β_k, α) ← HOUSE(x)                  ▷ (I − β_k v_k v_kᵀ) x = α e₁, β_k = 0 if x is a multiple of e₁
L5      p ← β_k A[k+1 .. n, k+1 .. n] v_k          ▷ symmetric matrix-vector product
L6      w ← p − (β_k pᵀ v_k / 2) v_k
L7      A[k+1 .. n, k+1 .. n] ← A[k+1 .. n, k+1 .. n] − v_k wᵀ − w v_kᵀ   ▷ lower triangle only
L8      A[k+1, k] ← α;  A[k+2 .. n, k] ← 0
L9  for k ← n − 2 downto 1 do                    ▷ backward accumulation, if Q is wanted
L10     Q[k+1 .. n, k+1 .. n] ← Q[k+1 .. n, k+1 .. n] − β_k v_k (v_kᵀ Q[k+1 .. n, k+1 .. n])
L11 return d = diag(A), e = subdiagonal of A, Q
```

HOUSE uses $\alpha = -\operatorname{sign}(x_1) \|x\|_2$ and $v = x - \alpha e_1$, so $v_1 = x_1 + \operatorname{sign}(x_1)\|x\|_2$ has no cancellation; if $\|x_{2..m}\|_2 = 0$ it returns $\beta = 0$ and $\alpha = x_1$. Lines L5 to L7 compute $P_k A_{22} P_k$ for the trailing block $A_{22}$ without forming $P_k$: expanding the product gives $A_{22} - v p^T - p v^T + \beta (v^T p) v v^T$, and that is $A_{22} - v w^T - w v^T$. In the implementation the reflectors are kept in a list; LAPACK `xSYTRD` stores them in the zeroed part of $A$ and keeps $Q$ in factored form unless it is asked for (`xORGTR`).

## Example

Take the symmetric matrix

$$A = \begin{pmatrix} 4 & 1 & -2 & 2 \\ 1 & 2 & 0 & 1 \\ -2 & 0 & 3 & -2 \\ 2 & 1 & -2 & -1 \end{pmatrix}.$$

**Step $k = 1$.** $x = (1, -2, 2)^T$ has norm $3$, so $\alpha = -3$, $v_1 = (4, -2, 2)^T$ and $\beta_1 = 2/24 = 1/12$. The update gives

$$P_1 A P_1 = \begin{pmatrix} 4 & -3 & 0 & 0 \\ -3 & 10/3 & 1 & 4/3 \\ 0 & 1 & 5/3 & -4/3 \\ 0 & 4/3 & -4/3 & -1 \end{pmatrix}.$$

**Step $k = 2$.** $x = (1, 4/3)^T$ has norm $5/3$, so $\alpha = -5/3$, $v_2 = (8/3, 4/3)^T$ and $\beta_2 = 9/40$. The result is

$$T = \begin{pmatrix} 4 & -3 & 0 & 0 \\ -3 & 10/3 & -5/3 & 0 \\ 0 & -5/3 & -33/25 & 68/75 \\ 0 & 0 & 68/75 & 149/75 \end{pmatrix}.$$

Every number here was checked in exact rational arithmetic, and the floating-point implementation reproduces it to within $10^{-14}$. As checks, the trace is $4 + 10/3 - 33/25 + 149/75 = 8$, which is the trace of $A$, and the Frobenius norms agree. The second column of $Q$ is $(0, -1/3, 2/3, -2/3)^T$, the first column of $P_1$ restricted to the trailing rows, and $Q e_1 = e_1$.

## Correctness

The proof is in [proofs/correctness.md](proofs/correctness.md). By induction on $k$, after the $k$-th pass of the loop the stored matrix equals $P_k \cdots P_1 A P_1 \cdots P_k$, its first $k$ columns are zero below the subdiagonal, and by symmetry its first $k$ rows are zero beyond the superdiagonal. The step keeps the earlier columns because $P_k$ acts only on rows and columns $k + 1$ to $n$, where those columns already have zeros except in row $k + 1$ of column $k$, which is the one entry the reflector folds the column onto. So after $n - 2$ passes the matrix is tridiagonal and equals $Q^T A Q$ with $Q = P_1 \cdots P_{n-2}$; lines L9 and L10 form this product from the right end, which never touches the first $k$ rows and columns at step $k$. The algorithm terminates because both loops are counted.

## Complexity

Exact counts of the leading terms, with $m = n - k$ the size of the trailing block at step $k$:

- **Reduction.** Line L5 is a symmetric matrix-vector product, $2m^2$ flops. Line L7 updates $m(m+1)/2$ entries at 4 flops each, another $2m^2$. So step $k$ costs $4m^2 + O(m)$, and $\sum_m 4m^2 = 4n^3/3 + O(n^2)$ flops (GVL Section 8.3.1). Without the symmetry, applying $P_k$ from both sides costs $8m^2$ per step, $8n^3/3$ in total.
- **Forming $Q$.** Step $k$ of the backward accumulation applies $P_k$ to an $m \times m$ block in $4m^2$ flops, so $4n^3/3$ more, $8n^3/3$ in all. Forward accumulation would act on $n \times m$ blocks and cost twice as much.
- **Applying $Q$ to eigenvectors.** $Q V_T$ for all $n$ eigenvectors costs $2n^3$ flops with the reflectors in factored form.
- **Space.** In place in the lower triangle of $A$, plus $O(n)$ for $p$ and $w$; $Q$ needs $n^2$ more.

The implementation tallies these counts; for $n = 64$ the ratios to $4n^3/3$ are $1.011$ for the reduction and $0.977$ for the accumulation, which approach 1 as $n$ grows. The Level 2 operations of lines L5 and L7 make this form memory bound; the blocked version below moves half the flops into matrix-matrix products.

## Properties

- **Backward stable.** The computed $\hat T$ satisfies $\hat T = \tilde Q^T (A + E) \tilde Q$ for an exactly orthogonal $\tilde Q$, with $\|E\|_F \le c \, n \, u \, \|A\|_F$ for a modest constant $c$, and the computed $\hat Q$ satisfies $\|\hat Q - \tilde Q\|_F = O(n u)$ (Wilkinson 1965 Chapter 3; GVL Section 8.3.1). By [Weyl's inequality](/weyls-inequality/), the eigenvalues of $\hat T$ are within $c n u \|A\|_F$ of those of $A$. On 3 random matrices for each $n$ from 4 to 64, the observed $\|A - \hat Q \hat T \hat Q^T\|_F / \|A\|_F$ stayed below $6u$, and $\|\hat Q^T \hat Q - I\|_F$ below $0.7 n u$.
- **Direct, not iterative.** A fixed number of operations, with no convergence question.
- **Deterministic and in place.**
- **First column of $Q$ is $e_1$.** By the implicit Q theorem, $T$ is determined by $A$ and $Q e_1$ up to the signs of the $e_i$, as long as $T$ is unreduced; the [Lanczos algorithm](/lanczos-algorithm/) started from $e_1$ produces the same $T$, up to the signs of the off-diagonal, in exact arithmetic.
- **Preserves structure.** If $A$ is already tridiagonal, every $\beta_k$ is zero and $T = A$, $Q = I$ exactly. A zero in $e$ can occur only when the trailing part of a column is exactly zero.

## Variants and improvements

- **Givens rotations.** Givens' 1954 method zeros one entry at a time with plane rotations, about twice the flops of Householder's method, but it suits banded matrices and parallel orderings.
- **Blocked reduction.** The `xSYTRD` algorithm of LAPACK accumulates $b$ reflectors in the form $A_{22} - V W^T - W V^T$ (Dongarra, Hammarling and Sorensen 1989), so half the flops become Level 3 products; the other half, the symmetric products of line L5, remain Level 2.
- **Two-stage reduction.** First reduce to a band of width $b$ with Level 3 operations, then reduce the band to tridiagonal form by bulge chasing in $O(n^2 b)$ flops (Bischof, Lang and Sun's SBR toolbox; used in PLASMA, MAGMA and ELPA). This is faster on modern machines, but forming $Q$ costs more.
- **Banded input.** Schwarz's and Kaufman's band reductions chase bulges with rotations and keep the bandwidth, in $O(n^2 b)$ flops.
- **Lanczos.** For large sparse $A$, the [Lanczos algorithm](/lanczos-algorithm/) builds the same $T$ one row at a time from matrix-vector products, but in floating point its vectors lose orthogonality.
- **Hermitian matrices.** Complex reflectors give a Hermitian tridiagonal matrix, and a diagonal unitary similarity makes the off-diagonal real and nonnegative.

## When to use it

Use it as the first step for every dense symmetric or Hermitian eigenproblem, whatever the tridiagonal solver ([QR](/qr-algorithm/), [divide and conquer](/divide-and-conquer-eigensolver/), [MRRR](/mrrr-algorithm/), [bisection](/bisection-eigenvalue-algorithm/)). The reduction is usually the dominant cost when only eigenvalues are wanted. Do not use it for large sparse matrices, because the reflectors fill in the matrix; use [Lanczos](/lanczos-algorithm/) instead. When high relative accuracy of tiny eigenvalues of a graded positive definite matrix matters, [Jacobi's method](/jacobi-eigenvalue-algorithm/) on the original matrix can be more accurate, because the reduction only guarantees errors relative to $\|A\|$.

## Pitfalls

- **The sign in HOUSE.** Taking $\alpha = +\operatorname{sign}(x_1)\|x\|_2$ makes $v_1 = x_1 - \alpha$ suffer cancellation when $x$ is close to a multiple of $e_1$, and the reflector loses orthogonality.
- **Overflow in the norm.** Summing squares overflows for entries near $10^{154}$ in double precision; library codes scale or use a careful norm.
- **Reading both triangles.** If the input is only nearly symmetric, a code that reads one triangle reduces a different matrix from one that reads the other. The implementation reads only the lower triangle.
- **Forming $Q$ forward.** Accumulating $Q = P_1 P_2 \cdots$ from the left end doubles the cost of forming $Q$.
- **Expecting relative accuracy.** The backward error is relative to $\|A\|$, so eigenvalues much smaller than $\|A\|$ can lose all their correct digits; a graded matrix can lose them even when its entries determine them well.
- **Not reducing the Hermitian off-diagonal to real numbers.** Real tridiagonal solvers need the diagonal unitary scaling, or they silently drop the imaginary parts.

## Implementations

## History

Wallace Givens reduced symmetric matrices to tridiagonal form by plane rotations in a 1954 Oak Ridge report, and combined it with Sturm sequence bisection. Alston Householder introduced elementary reflectors for unitary triangularization in 1958, and J. H. Wilkinson showed in 1960 that they reduce a symmetric matrix to tridiagonal form with half the multiplications of Givens' method, gave the rank-2 form of the update and proved the backward error bounds, collected in his 1965 book. The method became the reduction of EISPACK (`TRED2`) and of LAPACK (`xSYTRD`); the blocked form is due to Dongarra, Hammarling and Sorensen (1989), and two-stage band reduction became standard on multicore machines after 2010.

## References
