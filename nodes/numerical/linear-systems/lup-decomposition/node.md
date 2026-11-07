---
tag: 3B5H9A
kind: algorithm
slug: lup-decomposition
name: LUP decomposition
aliases:
- LU factorization with partial pivoting
- Gaussian elimination with partial pivoting
- GEPP
- PA = LU
- LUP-DECOMPOSITION
area: numerical/linear-systems
level: core
summary: Factors a square matrix into a lower triangular, an upper triangular and a permutation matrix, using Gaussian elimination with pivoting.
solves: [linear-system-solving]
model: floating-point-model
complexity:
  vars: {n: "the order of A, at least 1"}
  time: {worst: Θ(n^3), best: Θ(n^3)}
  space: {extra: Θ(n)}
  flops: {worst: "2n^3/3 - n^2/2 - n/6"}
  comparisons: {worst: n(n-1)/2}
properties: {deterministic: true, in_place: true, recursive: false}
prereqs: [lu-decomposition, triangular-system-solving, matrix-norms, floating-point-model]
see_also: [lup-solve, partial-pivoting, growth-factor, complete-pivoting, cholesky-decomposition, qr-decomposition, iterative-refinement, hagers-condition-estimator]
sources:
  - book: isbn:9780898715217
    title: Nicholas J. Higham, Accuracy and Stability of Numerical Algorithms, second edition, SIAM, 2002
    locator: Chapter 9, LU Factorization and Linear Equations (Section 9.1, pivoting strategies; Section 9.2, existence of the LU factorization; Section 9.3, error analysis, Theorem 9.3 for the factors; Section 9.4, the growth factor, the bound 2^(n-1) and its attainment; Section 9.13, historical perspective)
  - book: isbn:9781421407944
    title: Gene H. Golub and Charles F. Van Loan, Matrix Computations, fourth edition, Johns Hopkins University Press, 2013
    locator: Section 3.2, The LU Factorization; Section 3.3, Roundoff Error in Gaussian Elimination; Section 3.4, Pivoting (partial pivoting, the growth bound, and the blocked form)
  - book: isbn:9780898713619
    title: Lloyd N. Trefethen and David Bau III, Numerical Linear Algebra, SIAM, 1997
    locator: Lecture 20, Gaussian Elimination; Lecture 21, Pivoting (the 4 by 4 example and the operation count); Lecture 22, Stability of Gaussian Elimination (the growth factor and the worst-case matrix)
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Section 28.1, Solving systems of linear equations (the procedures LUP-DECOMPOSITION and LUP-SOLVE)
  - paper: doi:10.1145/321075.321076
    title: J. H. Wilkinson, Error analysis of direct methods of matrix inversion, Journal of the ACM 8(3), 1961
    locator: pp. 281 to 330 (the backward error analysis of elimination and the bound 2^(n-1) on the growth with partial pivoting)
  - paper: doi:10.1137/0611023
    title: Lloyd N. Trefethen and Robert S. Schreiber, Average-case stability of Gaussian elimination, SIAM Journal on Matrix Analysis and Applications 11(3), 1990
    locator: pp. 335 to 360 (experiments on the growth factor of random matrices)
  - paper: doi:10.1137/0914014
    title: Stephen J. Wright, A collection of problems for which Gaussian elimination with partial pivoting is unstable, SIAM Journal on Scientific Computing 14(1), 1993
    locator: pp. 231 to 238 (practical matrices with exponential growth)
---

The LUP decomposition of a square matrix $A$ is a factorization $P A = L U$, where $P$ is a permutation matrix, $L$ is unit lower triangular with entries $|l_{ij}| \le 1$, and $U$ is upper triangular. It is computed by Gaussian elimination with [partial pivoting](/partial-pivoting/): at each step, the row with the largest entry in the pivot column is swapped into the pivot position. It costs $2n^3/3$ flops, exists for each nonsingular $A$, and is the standard dense solver of LAPACK (`xGETRF`). With the factors, each system $A x = b$ costs $2n^2$ more flops by [LUP solve](/lup-solve/). In floating point it is backward stable unless the [growth factor](/growth-factor/) is large, which is possible in theory and very rare in practice.

## In plain words

Gaussian elimination clears the numbers below the diagonal, one column at a time, by subtracting a multiple of a pivot row from each row below it. The multiples form the lower triangle, and what is left forms the upper triangle. If a pivot is zero the method cannot divide; if it is tiny, the multiples are huge, and rounding errors in the huge numbers wipe out the small data.

Partial pivoting fixes both problems with one rule: before clearing a column, look down that column and swap the row with the largest entry into the pivot position. Then each multiple is at most one in size. The record of the swaps is the permutation. If the whole column below the diagonal is zero, the matrix is singular and the method says so.

## The problem

**Notation.** As in [solving linear systems](/linear-system-solving/): $A = (a_{ij})$ is an $n \times n$ real matrix, $|A|$ the matrix of the $|a_{ij}|$, $u$ the unit roundoff ($2^{-53}$ in binary64), $\gamma_n = n u / (1 - n u)$, and $a^{(k)}_{ij}$ the entries after $k - 1$ steps of elimination. The growth factor is

$$\rho_n = \frac{\max_{i,j,k} |\hat a^{(k)}_{ij}|}{\max_{i,j} |a_{ij}|},$$

computed from the floating-point entries $\hat a^{(k)}_{ij}$.

Input: $A \in \mathbb{R}^{n \times n}$. Output: a permutation $\pi$ of $\{1, \ldots, n\}$, the unit lower triangular $L$ and the upper triangular $U$ with $P A = L U$, where row $k$ of $P A$ is row $\pi_k$ of $A$; or the report that $A$ is singular. The exact-arithmetic facts about LU (existence without pivoting when the leading minors are nonzero, uniqueness, the determinant) are on the page [LU decomposition](/lu-decomposition/). This page is about the pivoted algorithm and its behavior in floating point.

## The algorithm

The array $A$ is overwritten: after the call, $u_{ij} = a_{ij}$ for $j \ge i$ and $l_{ij} = a_{ij}$ for $j < i$. Line L5 swaps whole rows, the multipliers stored in the first $k - 1$ columns included.

```pseudo id=main
LUP-DECOMPOSITION(A)                       ▷ A is n × n, overwritten by L and U
L1  π ← (1, 2, …, n)
L2  for k ← 1 to n do
L3      p ← the first i in k..n with |a_ik| = max_{k ≤ i' ≤ n} |a_i'k|
L4      if a_pk = 0 then return SINGULAR
L5      exchange π_k ↔ π_p and rows k ↔ p of A
L6      for i ← k + 1 to n do
L7          a_ik ← a_ik / a_kk                       ▷ the multiplier l_ik, |l_ik| ≤ 1
L8          for j ← k + 1 to n do
L9              a_ij ← a_ij − a_ik · a_kj            ▷ the Schur complement update
L10 return (A, π)
```

Line L3 is the pivot search, and it is the only difference from elimination without pivoting. Lines L6 to L9 subtract $l_{ik}$ times row $k$ from row $i$, for each row below the pivot; the block $a_{k+1:n, k+1:n}$ that they leave is the [Schur complement](/schur-complement/) of the leading $k \times k$ block of $P A$. In the last pass, $k = n$, the loops of lines L6 and L8 are empty, and lines L3 and L4 only test the last pivot $u_{nn}$.

## Example

Let $A = \begin{pmatrix} 2 & 1 & 1 \\ 4 & 3 & 3 \\ 8 & 7 & 9 \end{pmatrix}$ (the example of Trefethen and Bau, Lecture 21, cut to $3 \times 3$). The table shows the array after each pass; the multipliers are left of the bar.

| $k$ | pivot (line L3) | $\pi$ | array after the pass |
|---|---|---|---|
| start | | $(1, 2, 3)$ | $\begin{pmatrix} 2 & 1 & 1 \\ 4 & 3 & 3 \\ 8 & 7 & 9 \end{pmatrix}$ |
| 1 | $8$ in row 3 | $(3, 2, 1)$ | $\begin{pmatrix} 8 & 7 & 9 \\ \tfrac12 \mid & -\tfrac12 & -\tfrac32 \\ \tfrac14 \mid & -\tfrac34 & -\tfrac54 \end{pmatrix}$ |
| 2 | $-\tfrac34$ in row 3 | $(3, 1, 2)$ | $\begin{pmatrix} 8 & 7 & 9 \\ \tfrac14 & -\tfrac34 & -\tfrac54 \\ \tfrac12 & \tfrac23 \mid & -\tfrac23 \end{pmatrix}$ |
| 3 | $-\tfrac23$ in row 3 | $(3, 1, 2)$ | no change |

So
$$P A = \begin{pmatrix} 8 & 7 & 9 \\ 2 & 1 & 1 \\ 4 & 3 & 3 \end{pmatrix} = \begin{pmatrix} 1 & 0 & 0 \\ \tfrac14 & 1 & 0 \\ \tfrac12 & \tfrac23 & 1 \end{pmatrix} \begin{pmatrix} 8 & 7 & 9 \\ 0 & -\tfrac34 & -\tfrac54 \\ 0 & 0 & -\tfrac23 \end{pmatrix}.$$

At $k = 2$, the swap of rows 2 and 3 also swaps their multipliers $\tfrac12$ and $\tfrac14$; without it, $L$ would be wrong. Each $|l_{ij}| \le 1$, and $\det A = \det P \cdot \prod u_{ii} = (+1) \cdot 8 \cdot (-\tfrac34)(-\tfrac23) = 4$, because $\pi = (3, 1, 2)$ is an even permutation. In binary64 every value is exact except $\tfrac23$ and $-\tfrac23$, which are rounded.

**A singular matrix, in floating point.** For $A = \begin{pmatrix} 1 & 2 & 3 \\ 4 & 5 & 6 \\ 7 & 8 & 9 \end{pmatrix}$, which is singular, binary64 elimination with partial pivoting gives $\hat u_{33} = 2^{-53} \approx 1.11 \times 10^{-16}$, not $0$, because the multipliers $\tfrac17$ and $\tfrac47$ are rounded. Line L4 does not fire, and the factors are those of a nonsingular matrix within a few units of roundoff of $A$. For $A = \begin{pmatrix} 1 & 2 \\ 2 & 4 \end{pmatrix}$ the multiplier is $\tfrac12$, the elimination is exact, and line L4 reports SINGULAR at $k = 2$.

## Correctness

**Exact arithmetic.** If line L4 never returns, then $P A = L U$ with $P$ the permutation matrix of $\pi$, $L$ unit lower triangular with $|l_{ij}| \le 1$, and $U$ upper triangular with nonzero diagonal. Line L4 returns SINGULAR exactly when $A$ is singular. The proof keeps the invariant that, after pass $k$, $P^{(k)} A = L^{(k)} S^{(k)}$, where $L^{(k)}$ holds the multipliers of the first $k$ columns and $S^{(k)}$ is the first $k$ rows of $U$ on top of the Schur complement. The row swap of line L5 keeps the invariant only because it swaps the stored multipliers too. The nonsingular Schur complement has a nonzero column, so the pivot is nonzero, and a zero pivot column makes the complement, and so $A$, singular. The full proof is in [the proof](proofs/correctness.md).

**Backward error of the factors (proved).** Assume the [standard model](/floating-point-model/) and $n u < 1$. If the algorithm runs to completion, the computed factors satisfy

$$\hat L \hat U = P A + \Delta A, \qquad |\Delta A| \le \gamma_n |\hat L|\,|\hat U|,$$

where $P$ is the permutation that the algorithm chose (Higham, Theorem 9.3, applied to $P A$). Each entry $\hat u_{ij}$ or $\hat l_{ij}$ is the result of one recurrence $a_{ij} - \sum_k l_{ik} u_{kj}$, so the bound follows from the error of an inner product of length at most $n$.

**In the $\infty$-norm.** Partial pivoting gives $|\hat l_{ij}| \le 1$, so $\|\,|\hat L|\,\|_\infty \le n$. Each $|\hat u_{ij}|$ is an entry $|\hat a^{(i)}_{ij}|$, so $\|\,|\hat U|\,\|_\infty \le n \rho_n \max_{ij}|a_{ij}| \le n \rho_n \|A\|_\infty$. Hence

$$\|\Delta A\|_\infty \le n^2 \gamma_n \rho_n \|A\|_\infty.$$

This is a proved, worst-case bound. It makes the factorization backward stable when $\rho_n$ is modest. The growth factor is bounded by $\rho_n \le 2^{n-1}$, because each pass at most doubles the largest entry: $|a^{(k+1)}_{ij}| \le |a^{(k)}_{ij}| + |l_{ik}|\,|a^{(k)}_{kj}| \le 2 \max |a^{(k)}|$. The bound is attained (see Complexity). On random matrices $\rho_n$ is small, a fact that is observed and not proved.

## Complexity

**Flops.** Pass $k$ does $n - k$ divisions at line L7 and $(n - k)^2$ multiplications and as many subtractions at line L9. With $m = n - k$,

$$\sum_{m=1}^{n-1} (m + 2 m^2) = \frac{n(n-1)}{2} + \frac{(n-1)n(2n-1)}{3} = \frac{2n^3}{3} - \frac{n^2}{2} - \frac{n}{6}$$

flops, in each case: the count does not depend on the data. For $n = 2$ this gives $3$ flops: one division, one multiplication and one subtraction. Line L3 makes $n - k$ comparisons in pass $k$, $n(n-1)/2$ in total, which is a lower-order term. The extra space is the vector $\pi$; the factors overwrite $A$.

**Memory traffic.** The form above is *right-looking*: pass $k$ reads and writes the whole trailing block, so it reads about $n^3/3$ words and writes as many for $2n^3/3$ flops, about one flop for each word moved, and its speed is bound by memory bandwidth, not by the flop rate. LAPACK's `xGETRF` factors a panel of $b$ columns with this algorithm and updates the rest with one matrix product, so most flops become matrix-matrix products with $O(n^3/b)$ words of traffic. Recursive LU, which splits the columns in halves, has the same effect with no block size. The pivot search of line L3 needs a whole column, which is the reason that pivoting limits parallel LU.

**Worst-case growth.** Wilkinson's matrix with $a_{ii} = 1$, $a_{ij} = -1$ for $i > j$, $a_{in} = 1$ and zeros elsewhere needs no swaps under the tie rule of line L3, and its last column doubles at each pass, so $\rho_n = 2^{n-1}$; for $n = 5$ the last column becomes $(1, 2, 4, 8, 16)$, and $\rho_5 = 16$. Wright (1993) gives practical problems, from the solution of two-point boundary value problems by multiple shooting, with exponential growth.

**Observed growth.** For 5 matrices with independent standard normal entries generated by `random.Random(5)`, binary64 elimination gave $\rho_n$ between $1.2$ and $3.2$ for $n = 10$, between $3.0$ and $4.0$ for $n = 50$, and between $4.4$ and $4.9$ for $n = 100$. Trefethen and Schreiber (1990) measured the same slow growth on large samples.

## Properties

- **Exists for each nonsingular $A$**, unlike LU without pivoting, which needs nonzero leading minors.
- **Bounded multipliers**: $|l_{ij}| \le 1$.
- **Not unique when there are ties** in line L3; the tie rule (first index) makes the output deterministic.
- **Backward stable in practice**, with the proved bound above that involves $\rho_n$. It is not backward stable for every matrix in the worst case.
- **In place**: $L$ and $U$ overwrite $A$, and $P$ is stored as a vector of $n$ indices.
- **Determinant**: $\det A = \operatorname{sign}(\pi) \prod_i u_{ii}$, in $n$ more multiplications.
- **Band structure**: if $A$ has lower bandwidth $p$ and upper bandwidth $q$, then $U$ has upper bandwidth at most $p + q$, and each column of $L$ has at most $p$ nonzeros below the diagonal (Golub and Van Loan, Section 4.3).

## Variants and improvements

- **No pivoting.** Correct and stable for [diagonally dominant](/diagonally-dominant-matrix/) by columns and for [positive definite](/positive-definite-matrix/) matrices, where partial pivoting chooses no swap anyway.
- **[Complete pivoting](/complete-pivoting/).** Search the whole trailing block for the pivot. The growth is much smaller in the worst case (Wilkinson's bound grows like $n^{(1/4)\log n}$), at the cost of $n^3/3$ comparisons.
- **Rook pivoting.** Search alternately along a row and a column until an entry is largest in both; the cost is usually close to that of partial pivoting, and the worst-case growth is smaller.
- **Blocked and recursive LU.** The same arithmetic in another order, for memory traffic; see Complexity.
- **Tournament pivoting (CALU).** Choose $b$ pivots for a panel by a reduction tree, which cuts communication in parallel LU; the pivots differ from those of partial pivoting.
- **Threshold pivoting for sparse matrices.** Accept any pivot with $|a_{pk}| \ge \tau \max_i |a_{ik}|$, $0 < \tau \le 1$, to choose among candidates the one that makes less [fill-in](/fill-in/).
- **[Cholesky](/cholesky-decomposition/)** for symmetric positive definite $A$, at half the cost.

## When to use it

Use LUP to solve a dense nonsymmetric system of moderate size, to solve many systems with the same matrix, and to compute a determinant. It costs half as much as [Householder QR](/qr-decomposition/) ($4n^3/3$ flops for a square matrix), whose stability does not depend on a growth factor. Prefer QR when guaranteed stability matters more than a factor of two, or when the matrix is nearly rank deficient. Prefer Cholesky for symmetric positive definite matrices, and a sparse factorization or an iterative method when $A$ is large and sparse. Follow LUP with an estimate of $\kappa(A)$ by [Hager's estimator](/hagers-condition-estimator/), and with [iterative refinement](/iterative-refinement/) when a smaller forward error is needed.

## Pitfalls

- **Swapping only the active part of the rows.** If line L5 swaps only columns $k$ to $n$, the multipliers stored in columns $1$ to $k-1$ stay in the wrong rows, and $L U \ne P A$. Swap whole rows, as in the example at $k = 2$.
- **Testing $a_{pk} = 0$ as the test of singularity.** In floating point a singular matrix rarely gives an exact zero pivot, as the $3 \times 3$ example shows. Line L4 only avoids a division by zero. Decide near-singularity by an estimate of $\kappa(A)$ or by the size of $u_{nn}$ relative to $\|A\|$.
- **Taking the pivot of largest value, not of largest modulus.** Line L3 compares $|a_{ik}|$. Comparing $a_{ik}$ picks a large positive entry over a larger negative one and loses the bound $|l_{ij}| \le 1$.
- **Assuming that partial pivoting makes every problem safe.** It bounds the multipliers, not the growth; Wilkinson's matrix of order 60 has $\rho_{60} = 2^{59}$, and the result has no correct digits.
- **Forming $A^{-1}$ to solve.** $A^{-1} b$ costs $2n^3$ flops instead of $2n^3/3 + 2n^2$, and its error bound is weaker; use the factors.

## Implementations

## History

Elimination is much older than computers; see [Gaussian elimination](/gaussian-elimination/). The analysis of elimination in floating point, with the growth factor and the bound $2^{n-1}$ for partial pivoting, is due to Wilkinson (1961). The name LUP decomposition and the procedure names LUP-DECOMPOSITION and LUP-SOLVE are those of Cormen, Leiserson, Rivest and Stein.

## References
