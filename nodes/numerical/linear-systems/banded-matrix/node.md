---
tag: HE5FHC
kind: data-structure
slug: banded-matrix
name: Banded matrix
aliases:
- band storage
- band matrix
- general band storage
area: numerical/linear-systems
level: core
summary: Matrix stored only within a fixed band around the diagonal.
model: floating-point-model
complexity:
  vars: {n: "the order of A", p: "the lower bandwidth", q: "the upper bandwidth"}
  time: {worst: "Θ(n p q + n)"}
  space: {extra: "Θ(n (p + q + 1))"}
  flops: {worst: "n p (2q + 1)"}
  matvec: {worst: "2n (p + q + 1)"}
properties: {persistent: false, concurrent: false, external: false}
prereqs: [lup-decomposition, partial-pivoting, sparse-matrix]
see_also: [thomas-algorithm, tridiagonal-system-solving, cholesky-decomposition, bandwidth-reduction, cuthill-mckee, diagonally-dominant-matrix, cyclic-reduction, growth-factor]
sources:
  - book: isbn:9781421407944
    title: Gene H. Golub and Charles F. Van Loan, Matrix Computations, fourth edition, Johns Hopkins University Press, 2013
    locator: Section 1.2, Structure and Efficiency (band storage and band matrix-vector products); Section 4.3, Banded Systems (Algorithm 4.3.1, band Gaussian elimination; Section 4.3.3, band elimination with pivoting; Section 4.3.6, band Cholesky)
  - book: isbn:9780898715217
    title: Nicholas J. Higham, Accuracy and Stability of Numerical Algorithms, second edition, SIAM, 2002
    locator: Section 9.5, Diagonally Dominant and Banded Matrices (the growth factor bound of Bohte for band matrices with partial pivoting)
  - book: isbn:9780898713893
    title: James W. Demmel, Applied Numerical Linear Algebra, SIAM, 1997
    locator: Section 2.7.3, Band Matrices (the fill pattern with and without pivoting)
  - book: "Edward Anderson et al., LAPACK Users' Guide, third edition, SIAM, 1999"
    locator: Section 5.3.3, Band Storage (the layout AB(ku+1+i-j, j) and the extra kl rows for xGBTRF)
  - paper: "Zvonimir Bohte, Bounds for rounding errors in the Gaussian elimination for band systems, IMA Journal of Applied Mathematics 16(2), 1975"
    locator: pp. 133 to 142 (growth factor at most 2^(2p-1) - (p-1) 2^(p-2) with partial pivoting when p = q)
---

A **banded matrix** with lower bandwidth $p$ and upper bandwidth $q$ has $a_{ij} = 0$ whenever $i - j > p$ or $j - i > q$. **Band storage** keeps only the $p + q + 1$ diagonals that may be nonzero, in an array of $(p + q + 1) \times n$ numbers instead of $n^2$. Gaussian elimination without pivoting keeps all fill inside the band and costs about $2 n p q$ flops instead of $2n^3/3$. With partial pivoting the upper bandwidth grows to at most $p + q$, so the storage needs $p$ extra diagonals and the cost stays linear in $n$. Banded matrices come from finite differences in one dimension, from splines, and from sparse matrices after a [bandwidth-reducing ordering](/bandwidth-reduction/).

## In plain words

Many matrices have all their nonzero numbers on a narrow strip around the main diagonal, for example when each unknown is linked only to its near neighbors on a line. Storing the whole square wastes memory on zeros. Band storage keeps each of the few diagonals of the strip as one row of a short, wide table.

The point is that solving a system does not leave the strip, so the work grows with the length of the strip times its width squared, not with the cube of the size. Swapping rows for safety widens the strip on one side by a fixed amount, so the extra cost is bounded.

## The abstract type

An $n \times n$ matrix $A$ with fixed bandwidths $(p, q)$, with operations:

- `get(i, j)` and `set(i, j, v)`: read and write an entry; writing a nonzero outside the band is an error.
- `matvec(x)`: return $A x$.
- `lu()`: factor $A = L U$ without pivoting, with $L$ unit lower triangular of lower bandwidth $p$ and $U$ upper triangular of upper bandwidth $q$; fail on a zero pivot.
- `lu_pivoted()`: factor $P A = L U$ with partial pivoting, where $U$ has upper bandwidth at most $p + q$ and each column of $L$ has at most $p$ multipliers; fail only if $A$ is singular.
- `solve(b)` on a factorization: return $x$ with $A x = b$.

Notation as in [solving linear systems](/linear-system-solving/): $u = 2^{-53}$, $\gamma_m = m u/(1 - m u)$, $\rho_n$ the [growth factor](/growth-factor/), $|M|$ the matrix of absolute values, inequalities between matrices entrywise.

## Representation

Entry $a_{ij}$ of the band is stored in `ab[q + i - j][j]` (0-based), so row $d$ of `ab` holds one diagonal: $d = q$ the main diagonal, $d < q$ the superdiagonals and $d > q$ the subdiagonals. Each column $j$ of `ab` holds column $j$ of $A$, which makes column operations contiguous. For $n = 5$, $p = 1$, $q = 2$ the layout is
$$\begin{pmatrix} \ast & \ast & a_{13} & a_{24} & a_{35} \\ \ast & a_{12} & a_{23} & a_{34} & a_{45} \\ a_{11} & a_{22} & a_{33} & a_{44} & a_{55} \\ a_{21} & a_{32} & a_{43} & a_{54} & \ast \end{pmatrix}$$
with 1-based matrix indices; the slots marked $\ast$ correspond to no entry and hold zero. This is the LAPACK general band layout `AB(ku+1+i-j, j)` with $kl = p$, $ku = q$. For the pivoted factorization the array is allocated with upper bandwidth $p + q$, which is the same as LAPACK's $kl$ extra rows on top. The **invariant** is that `ab` has $p + q + 1$ rows of length $n$ and the $\ast$ slots are zero.

## Operations

The main operation is band LU without pivoting (Golub and Van Loan, Algorithm 4.3.1). Row $k$ of $U$ reaches only column $k + q$, and column $k$ of $L$ reaches only row $k + p$, so the update touches a $p \times q$ block.

```pseudo id=main
BandLU(A, n, p, q)                          ▷ overwrites the band of A with L and U
L1  for k ← 1 to n do
L2      if a_kk = 0 then fail (zero pivot)
L3      for i ← k + 1 to min(k + p, n) do
L4          a_ik ← a_ik / a_kk                   ▷ multiplier l_ik
L5      for j ← k + 1 to min(k + q, n) do
L6          for i ← k + 1 to min(k + p, n) do
L7              a_ij ← a_ij − a_ik a_kj
L8  return (L, U) in the band of A
```

The product $y = A x$ visits only the stored entries.

```pseudo id=matvec
BandMatvec(A, x)
M1  for i ← 1 to n do
M2      for j ← max(1, i − p) to min(n, i + q) do
M3          y_i ← y_i + a_ij x_j
```

A solve is a forward pass with the multipliers and a banded [back substitution](/back-substitution/). With pivoting, step $k$ first swaps $y_k$ with $y_{\pi_k}$ (LINPACK style: the multipliers are not permuted afterwards), and the back substitution uses upper bandwidth $p + q$.

```pseudo id=solve
BandSolve(L, U, b)                          ▷ y ← b
S1  for k ← 1 to n do                        ▷ with pivoting: first swap y_k and y_π(k)
S2      for i ← k + 1 to min(k + p, n) do y_i ← y_i − l_ik y_k
S3  for i ← n down to 1 do
S4      x_i ← (y_i − Σ_{j=i+1}^{min(i+q, n)} u_ij x_j) / u_ii
```

`lu_pivoted` runs BandLU with two changes: at step $k$ it picks $r \in \{k, \ldots, \min(k + p, n)\}$ with the largest $|a_{rk}|$ and swaps rows $k$ and $r$ in columns $k$ to $\min(k + p + q, n)$, and the loop in line L5 runs to $\min(k + p + q, n)$. Row $r \le k + p$ reached column $r + q \le k + p + q$, which is why $p$ extra superdiagonals suffice.

## Example

The second difference matrix $T_4 = \operatorname{tridiag}(-1, 2, -1)$ has $p = q = 1$ and band storage
$$\texttt{ab} = \begin{pmatrix} 0 & -1 & -1 & -1 \\ 2 & 2 & 2 & 2 \\ -1 & -1 & -1 & 0 \end{pmatrix}.$$
BandLU computes $l_{21} = -1/2$, $u_{22} = 2 - 1/2 = 3/2$, $l_{32} = -2/3$, $u_{33} = 4/3$, $l_{43} = -3/4$, $u_{44} = 5/4$, so $\det T_4 = 2 \cdot \tfrac32 \cdot \tfrac43 \cdot \tfrac54 = 5$. The superdiagonal of $U$ is the superdiagonal of $T_4$, and no entry outside the band is ever touched. Solving with $b = (1, 1, 1, 1)$ gives $x = (2, 3, 3, 2)$.

Pivoting widens the band. For $A = \begin{pmatrix} 1 & 1 & 0 \\ 4 & 1 & 1 \\ 0 & 4 & 1 \end{pmatrix}$ ($p = q = 1$), step 1 swaps rows 1 and 2, so the new row 1 is $(4, 1, 1)$, with an entry two places right of the diagonal. Step 2 swaps rows 2 and 3 again. The result is $\pi = (2, 3, 3)$ and $U = \begin{pmatrix} 4 & 1 & 1 \\ 0 & 4 & 1 \\ 0 & 0 & -7/16 \end{pmatrix}$, of upper bandwidth $2 = p + q$. With $b = (1, 2, 3)$ the solve gives $x = (2/7, 5/7, 1/7)$.

## Correctness

The proofs are in `proofs/correctness.md` and `proofs/complexity.md`.

1. **No fill outside the band (exact arithmetic).** BandLU performs exactly the operations of Gaussian elimination without pivoting that involve nonzero entries: the multipliers $a_{ik}$ with $i > k + p$ and the entries $a_{kj}$ with $j > k + q$ are zero at step $k$ and stay zero. So it returns the same $L$ and $U$ as dense elimination, with $L$ of lower bandwidth $p$ and $U$ of upper bandwidth $q$.
2. **Pivoting.** With partial pivoting, every row ever used as a pivot row at step $k$ has its last nonzero in a column at most $k + p + q$, so $U$ has upper bandwidth at most $p + q$, and the multipliers of step $k$ occupy rows $k + 1$ to $k + p$.
3. **Backward error (proved).** In the [floating point model](/floating-point-model/), if BandLU runs to completion, the computed factors satisfy
$$\hat L \hat U = A + \Delta A, \qquad |\Delta A| \le \gamma_{w} |\hat L| |\hat U|, \qquad w = \min(p, q) + 1,$$
because each entry of $\hat L \hat U$ is an inner product with at most $\min(p, q)$ terms besides the diagonal one. This is the band version of Higham, Theorem 9.3, with $\gamma_n$ replaced by $\gamma_w$. The two banded triangular solves are backward stable with constants $\gamma_{p+1}$ and $\gamma_{q+1}$ (Higham, Theorem 8.5, with the inner products shortened in the same way), so the computed solution satisfies $(A + \Delta A) \hat x = b$ with $|\Delta A| \le \gamma_{w + p + q + 2} |\hat L| |\hat U|$.
4. **When no pivoting is safe.** For [diagonally dominant](/diagonally-dominant-matrix/) and for [symmetric positive definite](/positive-definite-matrix/) band matrices, $|\hat L| |\hat U|$ is bounded by a modest multiple of $|A|$ (growth factor at most 2 for diagonal dominance), so BandLU is backward stable. For general band matrices, use `lu_pivoted`.
5. **Growth with pivoting (cited).** Bohte (1975) showed that partial pivoting on a band matrix with $p = q$ has $\rho_n \le 2^{2p - 1} - (p - 1) 2^{p - 2}$, independent of $n$; for tridiagonal matrices this is $2$ (Higham, Section 9.5). The tests confirm $\rho_n \le 2$ on random tridiagonal matrices. When $q > p$ the bound depends on $q$ too: $p = 1$ with $q = n - 1$ is a Hessenberg matrix, for which $\rho_n \le n$.

## Complexity

| operation | flops | storage touched |
|---|---|---|
| `get`, `set` | none | $O(1)$ |
| `matvec` | at most $2n(p + q + 1)$ | every stored entry once |
| `lu` (no pivoting) | $\sum_k (m_k + 2 m_k s_k)$ with $m_k = \min(p, n - k)$, $s_k = \min(q, n - k)$; at most $n p (2q + 1)$, about $2npq$ when $n \gg p, q$ | the band, $(p + q + 1) n$ numbers |
| `lu_pivoted` | at most $n p (2(p + q) + 1)$ | $(2p + q + 1) n$ numbers |
| `solve` | about $2n(p + q)$, or $2n(2p + q)$ with pivoting | the factors once |

Dense LU costs $2n^3/3$ flops, so for $T_n$ ($p = q = 1$) band storage turns $n^3$ work into about $3n$ flops: this is the [Thomas algorithm](/thomas-algorithm/). For small $p$ and $q$ all band operations do $O(1)$ flops per entry loaded, so they are bound by memory bandwidth and do not reach the peak flop rate. LAPACK's blocked `xGBTRF` helps only once $p$ and $q$ are in the tens. For a band [Cholesky decomposition](/cholesky-decomposition/) of a symmetric positive definite matrix ($p = q$), only $p + 1$ diagonals are stored and the cost is about $n p^2$ flops plus $n$ square roots.

## Variants

- **Symmetric band storage.** Keep only the main diagonal and the $p$ superdiagonals; band Cholesky (LAPACK `xPBTRF`) works in place.
- **Tridiagonal storage.** Three vectors; the [Thomas algorithm](/thomas-algorithm/) and [tridiagonal system solving](/tridiagonal-system-solving/), or [cyclic reduction](/cyclic-reduction/) for parallel machines.
- **Variable band (skyline, profile, envelope) storage.** For each row, store from the first nonzero to the diagonal. Fill in Cholesky stays inside this envelope, which is often much smaller than a constant band. It is the target of [Cuthill-McKee](/cuthill-mckee/) orderings.
- **Block banded storage.** Block tridiagonal matrices from 2D grids, with dense or banded blocks.
- **Diagonal (DIA) format.** For sparse matrices with a few far-off diagonals, store only the occupied diagonals with their offsets. It is good for matvecs on regular grids, but not for factorization, which fills the space between them.

## When to use it

Use band storage when the nonzeros really lie in a narrow band, either naturally (one-dimensional problems, splines, ODE boundary value problems, implicit time steps on a line) or after a [bandwidth reduction](/bandwidth-reduction/) ordering. For two-dimensional grids with $N$ unknowns the best band is about $\sqrt N$ wide, so banded LU costs $O(N^2)$ flops; [nested dissection](/nested-dissection/) with a general [sparse](/sparse-matrix/) solver costs $O(N^{3/2})$ and wins for large grids. For three-dimensional grids banded methods are rarely competitive.

## Pitfalls

- **Forgetting the room for pivoting.** With partial pivoting the upper bandwidth becomes $p + q$; allocating only $p + q + 1$ diagonals overwrites data. LAPACK's `xGBTRF` requires $2 kl + ku + 1$ rows.
- **Skipping pivoting for general band matrices.** No pivoting is safe for diagonally dominant and positive definite matrices only; on others a tiny pivot can give an arbitrarily large $|\hat L| |\hat U|$.
- **Index confusion.** The 1-based LAPACK formula `AB(ku+1+i-j, j)` becomes `ab[q+i-j][j]` with 0-based indices; mixing the two shifts all diagonals by one.
- **Wide bands.** When $p q$ is comparable to $n^2$, band storage saves nothing and dense LU with blocking is faster.
- **Assuming the band survives inversion.** $A^{-1}$ of a band matrix is in general full; use the factors.

## Implementations

## History

Band elimination appears in the early literature on finite difference methods, and its error analysis was given by Wilkinson in the 1960s; the growth bound for band matrices with pivoting is due to Bohte (1975). The storage scheme with diagonals as rows was standardized by LINPACK (1979, routines `xGBFA` and `xGBSL`) and kept by LAPACK (1992, `xGBTRF`, `xGBTRS`, `xPBTRF`). Profile and envelope schemes developed alongside the [Cuthill-McKee](/cuthill-mckee/) ordering (1969) and the George and Liu book on sparse positive definite systems (1981).

## References
