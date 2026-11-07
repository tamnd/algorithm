---
tag: H2T7HQ
kind: algorithm
slug: hessenberg-reduction
name: Hessenberg reduction
aliases:
- reduction to upper Hessenberg form
- Householder reduction to Hessenberg form
area: numerical/eigenproblems
level: core
summary: A unitary similarity A = Q H Q* to upper Hessenberg form by n − 2 Householder reflectors, in 10n^3/3 flops. It is the standard first step of the QR algorithm.
solves: [eigenvalue-problem]
model: floating-point-model
complexity:
  vars: {n: "the order of A"}
  time: {worst: Θ(n^3)}
  space: {extra: Θ(n)}
  flops: {worst: "10n^3/3 + O(n^2)", with_q: "14n^3/3 + O(n^2)"}
properties: {deterministic: true, in_place: true, recursive: false, iterative: false}
history:
  year: 1958
  people: [Alston S. Householder, Karl Hessenberg, J. H. Wilkinson]
  note: Householder introduced reflectors for triangularization in 1958; Wilkinson used them for the reduction to Hessenberg and tridiagonal form.
prereqs: [householder-reflections, eigenvalue, similarity-transformation]
see_also: [qr-algorithm, francis-double-shift-qr, tridiagonalization, schur-decomposition, matrix-balancing, givens-rotations, qr-decomposition, arnoldi-iteration]
sources:
  - book: isbn:9781421407944
    title: Gene H. Golub and Charles F. Van Loan, Matrix Computations, fourth edition, Johns Hopkins University Press, 2013
    locator: Section 7.4.3 (Householder reduction to Hessenberg form, Algorithm 7.4.2, the flop count and the backward error) and Section 7.4.5 (the implicit Q theorem)
  - book: isbn:9780898713619
    title: Lloyd N. Trefethen and David Bau III, Numerical Linear Algebra, SIAM, 1997
    locator: Lecture 26, Reduction to Hessenberg or Tridiagonal Form (Algorithm 26.1, the operation count and the backward stability theorem)
  - book: isbn:9780898715217
    title: Nicholas J. Higham, Accuracy and Stability of Numerical Algorithms, second edition, SIAM, 2002
    locator: Chapter 19, QR Factorization (error analysis of Householder transformations)
  - paper: doi:10.1145/320941.320947
    title: Alston S. Householder, Unitary triangularization of a nonsymmetric matrix, Journal of the ACM 5(4), 1958
    locator: pp. 339 to 342
  - book: "J. H. Wilkinson, The Algebraic Eigenvalue Problem, Oxford University Press, 1965"
    title: J. H. Wilkinson, The Algebraic Eigenvalue Problem
    locator: Chapter 6, Reduction of a general matrix to condensed form
---

Hessenberg reduction computes a unitary similarity $A = Q H Q^*$ of a square matrix $A$ with $H$ upper Hessenberg, that is, $h_{ij} = 0$ for $i > j + 1$. It applies $n - 2$ [Householder reflectors](/householder-reflections/), each on both sides, at a cost of $10n^3/3$ flops for a real matrix. The reduction is finite and backward stable, and it keeps the eigenvalues. It is the first phase of the [QR algorithm](/qr-algorithm/): a QR step on a Hessenberg matrix costs $O(n^2)$ instead of $O(n^3)$, and the Hessenberg form is kept by the step. For a Hermitian matrix the result is tridiagonal ([tridiagonalization](/tridiagonalization/)).

## In plain words

Eigenvalue methods work best on a matrix with many zeros. You cannot make every entry below the diagonal zero in a fixed number of steps, because then you could read off the eigenvalues, and no finite method can do that for large matrices. One diagonal below the main diagonal must stay. All entries further down can be cleared.

The method clears one column at a time. A reflection, a mirror that maps a vector onto a coordinate axis, clears the entries of a column below the first entry under the diagonal. The same mirror must then be applied from the other side, so that the eigenvalues stay the same. The second application does not touch the columns that were already cleared. Mirrors do not magnify rounding errors, so the result is exact for a matrix very close to the input.

## The problem

**Notation.** $A \in \mathbb{C}^{n \times n}$; $H$ is upper Hessenberg; $Q$ is unitary; $P = I - \beta v v^*$ is a Householder reflector with $\beta = 2 / v^* v$. Indices in the pseudocode are 1-based. $u$ is the unit roundoff.

Given $A$, return $H$ upper Hessenberg and, if asked, $Q$ unitary with $A = Q H Q^*$ and $Q e_1 = e_1$.

## The algorithm

```pseudo id=main
HESSENBERG(A)                                   ▷ overwrites A with H
L1  for k ← 1 to n − 2 do
L2      (v, β) ← HOUSE(A[k+1 .. n, k])           ▷ (I − β v v*) x = α e₁
L3      A[k+1 .. n, k .. n] ← A[k+1 .. n, k .. n] − β v (v* A[k+1 .. n, k .. n])
L4      A[1 .. n, k+1 .. n] ← A[1 .. n, k+1 .. n] − β (A[1 .. n, k+1 .. n] v) v*
L5      A[k+2 .. n, k] ← 0                       ▷ exact zeros, not rounded ones
L6      if Q is wanted then Q[1 .. n, k+1 .. n] ← Q[1 .. n, k+1 .. n] − β (Q[1 .. n, k+1 .. n] v) v*
L7  return H = A and Q

HOUSE(x)                                        ▷ x has length m
L8  σ ← ‖x[2 .. m]‖₂;  if σ = 0 then return (e₁, 0)
L9  φ ← x₁ / |x₁| (φ ← 1 if x₁ = 0);  α ← −φ ‖x‖₂
L10 v ← x;  v₁ ← x₁ − α;  return (v, 2 / (v* v))
```

The sign in line L9 makes $|v_1| = |x_1| + \|x\|_2$, with no cancellation; the other sign can make $v_1$ tiny and $v$ inaccurate. The left product of line L3 touches only rows $k + 1$ to $n$, and starts at column $k$ because the earlier columns are zero there. The right product of line L4 touches only columns $k + 1$ to $n$, so it does not refill column $k$. The matrix $Q$ is kept in factored form by most codes (the vectors $v$ are stored in the zeroed part of $A$), and formed only when the Schur vectors are needed.

## Example

Take
$$A = \begin{pmatrix} 4 & 1 & 2 & 3 \\ 2 & 3 & 1 & 1 \\ 1 & 2 & 5 & 1 \\ 3 & 1 & 1 & 2 \end{pmatrix}.$$
Step 1 reduces $x = (2, 1, 3)^T$, with $\|x\|_2 = \sqrt{14} \approx 3.741657$. Then $\alpha = -3.741657$, $v = (5.741657, 1, 3)^T$ and $\beta = 0.046548$, and the reflector maps $x$ to $(-3.741657, 0, 0)^T$. Step 2 clears the entry in row 4 of column 2. The result, to six decimals, is
$$H = \begin{pmatrix} 4 & -3.474396 & -0.711158 & 1.192822 \\ -3.741657 & 4.214286 & 1.907205 & 0.416886 \\ 0 & 2.335398 & 4.001804 & -0.076753 \\ 0 & 0 & -0.878537 & 1.783910 \end{pmatrix}.$$
The first row and column of $Q$ are $e_1^T$ and $e_1$, so $h_{11} = a_{11} = 4$. The trace is 14 in both matrices. The largest entry of $Q H Q^T - A$ is $7.1 \times 10^{-15}$, and the subdiagonal entries are all nonzero, so $H$ is unreduced.

## Correctness

The full proof is in [proofs/correctness.md](proofs/correctness.md).

1. **The reflector.** HOUSE returns $v$ and $\beta$ with $I - \beta v v^*$ unitary, Hermitian, and mapping $x$ to $\alpha e_1$ with $|\alpha| = \|x\|_2$.
2. **Invariant.** After step $k$, the matrix equals $Q_k^* A Q_k$ with $Q_k = P_1 \cdots P_k$ unitary, and columns 1 to $k$ have zeros below the subdiagonal. The left product creates the zeros of column $k$ and maps the earlier zero parts to zero; the right product mixes only columns $k + 1$ to $n$.
3. **Result.** After $n - 2$ steps $H$ is Hessenberg and $A = Q H Q^*$. Since $Q$ is unitary, $H$ has the eigenvalues of $A$; since every $P_k$ fixes $e_1$, $Q e_1 = e_1$. A Hermitian $A$ gives a Hermitian Hessenberg, hence tridiagonal, $H$.
4. **Uniqueness (implicit Q theorem).** If $Q^* A Q = H$ and $\tilde Q^* A \tilde Q = \tilde H$ are both Hessenberg, $Q e_1 = \tilde Q e_1$, and $H$ is unreduced (no zero subdiagonal entry), then $\tilde Q = Q D$ with $D$ diagonal and unitary, and $\tilde H = D^* H D$ (Golub and Van Loan, Section 7.4.5). The implicitly shifted QR step rests on this fact.

**Backward stability.** The computed $\hat H$ is $Q^*(A + E)Q$ for an exactly unitary $Q$ with $\|E\|_F \le c n^2 u \|A\|_F$, and the computed $\hat Q$ is within $O(n^2 u)$ of $Q$ (Golub and Van Loan, Section 7.4.3; Trefethen and Bau, Lecture 26). The constant is modest and in practice the error grows more like $n u$. This is a normwise statement: the eigenvalues of $\hat H$ are those of $A + E$, and their accuracy then depends on the [condition](/eigenvalue-condition-number/) of the eigenvalues, not on the reduction.

## Complexity

- **Flops.** Step $k$ with $m = n - k$ costs $4m(m+1)$ flops for the left product and $4nm$ for the right product. The sum over the steps is $\frac{4n^3}{3} + 2n^3 = \frac{10n^3}{3} + O(n^2)$ flops for real $A$. This count is exact up to the lower-order term.
- **With Q.** Accumulating $Q$ backward, $P_1(P_2(\cdots P_{n-2}))$, works on shrinking blocks and costs $4n^3/3$ more, for $14n^3/3$ in total. The forward product of line L6 is simpler and costs $2n^3$.
- **Hermitian input.** Exploiting symmetry, the reduction to tridiagonal form costs $4n^3/3$ flops, or $8n^3/3$ with $Q$.
- **Space.** The reduction works in place; the reflector vectors fit in the zeroed part of $A$, with $O(n)$ extra space for the $\beta$ values and one work vector.
- **Comparison.** A QR step on a full matrix costs $O(n^3)$, on a Hessenberg matrix $O(n^2)$ (about $10n^2$ flops for a Francis double step), so the one-time reduction pays for itself after a few steps.

## Properties

- **Finite and direct.** Exactly $n - 2$ steps, with no iteration and no convergence test.
- **Backward stable,** with a unitary transformation that does not change the condition of the eigenvalues.
- **Keeps the first column of $Q$ as $e_1$.** Other first columns give other Hessenberg forms; by the implicit Q theorem, the first column fixes the form up to signs. The [Arnoldi iteration](/arnoldi-iteration/) builds the same $H$ column by column with $Q e_1 = b / \|b\|$.
- **Not unique without that normalization,** and not continuous at matrices whose Hessenberg form is reduced.

## Variants and improvements

- **Blocked reduction.** Dongarra, Sorensen and Hammarling (1989) grouped the reflectors so that half of the work is done as matrix-matrix products; LAPACK `xGEHRD` uses this form, and later work moved more of the work into level-3 operations.
- **Givens rotations.** Zeroing one entry at a time with [Givens rotations](/givens-rotations/) costs about twice as many flops for a dense matrix but suits matrices with structure.
- **Gaussian similarity transforms.** Elementary stabilized transformations with pivoting, as in EISPACK `ELMHES`, cost $5n^3/3$ flops, half the Householder count, but are not unitary and have a weaker error bound (Wilkinson 1965, Chapter 6).
- **Balancing first.** A diagonal similarity that equalizes row and column norms ([matrix balancing](/matrix-balancing/)) is usually applied before the reduction; it can make the computed eigenvalues much more accurate.
- **Hermitian and banded cases.** [Tridiagonalization](/tridiagonalization/) for Hermitian matrices, and band reduction in two stages (full to band, then band to tridiagonal) for better use of the memory hierarchy.

## When to use it

Use it before every dense QR iteration for a nonsymmetric matrix, and before inverse iteration or Hessenberg-based linear solves with many shifts (for example frequency response computations $(A - \sigma I)^{-1} b$ for many $\sigma$). Do not use it on large sparse matrices: the reflectors fill in the matrix, and Krylov methods are the right tool there.

## Pitfalls

- **The wrong sign in HOUSE.** $v_1 = x_1 + \operatorname{sign}(x_1)\|x\|$ in the real case, never the difference; the difference cancels when $x$ is nearly a multiple of $e_1$.
- **Only one side.** Applying $P_k$ only on the left gives a QR-type factorization, not a similarity; the eigenvalues change.
- **Leaving rounded junk below the subdiagonal.** Store exact zeros (line L5); later codes assume them.
- **Starting the right product at column $k$.** That would refill column $k$; the right product starts at column $k + 1$.
- **Expecting a triangular result.** No finite sequence of similarities gives a triangular matrix in general; that is the job of the iterative QR algorithm.
- **Overflow in $\|x\|_2$.** Compute norms with scaling or `hypot` when the entries can be near the overflow threshold.

## Implementations

## History

Karl Hessenberg described the form that bears his name in a 1940 report on the computation of eigenvalues. Alston Householder introduced the reflectors $I - 2 w w^*$ for unitary triangularization in 1958. Wilkinson then used them, and Givens rotations, to reduce a general matrix to Hessenberg form and a symmetric one to tridiagonal form, and he gave the error analysis in his 1965 book (Chapter 6). Together with the QR algorithm of Francis and Kublanovskaya (1961), this two-phase scheme became the standard dense eigenvalue method of EISPACK and LAPACK.

## References
