---
tag: ZZBMD0
kind: technique
slug: complete-pivoting
name: Complete pivoting
aliases:
- full pivoting
- GECP
- total pivoting
area: numerical/linear-systems
level: advanced
summary: Swap both rows and columns to choose the largest entry as pivot.
prereqs: [gaussian-elimination, partial-pivoting, growth-factor]
see_also: [partial-pivoting, growth-factor, lup-decomposition, rank-revealing-factorization, gaussian-elimination, backward-error-analysis, condition-number, hagers-condition-estimator]
sources:
  - paper: doi:10.1145/321075.321076
    title: J. H. Wilkinson, Error analysis of direct methods of matrix inversion, Journal of the ACM 8(3), 1961
    locator: pp. 281 to 330 (the growth bound for complete pivoting via Hadamard's inequality)
  - book: isbn:9780898715217
    title: Nicholas J. Higham, Accuracy and Stability of Numerical Algorithms, second edition, SIAM, 2002
    locator: Section 9.1 (pivoting strategies); Section 9.4, the growth factor (Wilkinson's bound for complete pivoting, the conjecture rho_n <= n and its disproof)
  - book: isbn:9781421407944
    title: Gene H. Golub and Charles F. Van Loan, Matrix Computations, fourth edition, Johns Hopkins University Press, 2013
    locator: Section 3.4, Pivoting (complete pivoting, rook pivoting and their growth bounds)
  - paper: doi:10.1137/0612025
    title: Nick Gould, On growth in Gaussian elimination with complete pivoting, SIAM Journal on Matrix Analysis and Applications 12(2), 1991
    locator: pp. 354 to 361 (a 13 by 13 matrix with growth greater than 13 in floating point arithmetic)
  - paper: "Alan Edelman, The complete pivoting conjecture for Gaussian elimination is false, The Mathematica Journal 2(2), 1992"
    title: The complete pivoting conjecture for Gaussian elimination is false
    locator: pp. 58 to 61 (exact arithmetic confirmation of Gould's counterexample)
  - paper: "Colin W. Cryer, Pivot size in Gaussian elimination, Numerische Mathematik 12(4), 1968"
    title: Pivot size in Gaussian elimination
    locator: the conjecture that the growth of a Hadamard matrix is n, and small n cases
---

Complete pivoting chooses, at each step $k$ of [Gaussian elimination](/gaussian-elimination/), the entry of largest magnitude in the whole active submatrix $A^{(k)}_{k:n,\,k:n}$, and moves it to position $(k, k)$ by a row swap and a column swap. The result is $P A Q = L U$ with $|l_{ij}| \le 1$. Wilkinson (1961) proved that the [growth factor](/growth-factor/) is then at most $f(n) = n^{1/2} (2 \cdot 3^{1/2} \cdot 4^{1/3} \cdots n^{1/(n-1)})^{1/2}$, which grows like $n^{(\ln n)/4 + 1/2}$, much slower than the $2^{n-1}$ of [partial pivoting](/partial-pivoting/). So Gaussian elimination with complete pivoting (GECP) is backward stable for every matrix, with a backward error bounded by a modest polynomial times $f(n)$. The price is about $n^3/3$ comparisons, the same order as the $2n^3/3$ flops, and a search that touches the whole trailing matrix at every step, which is why LAPACK uses it only in small kernels such as `getc2`.

## In plain words

Partial pivoting looks down one column for the biggest number and puts it in front. Complete pivoting looks at every number that is still in play and picks the biggest one anywhere, then moves both its row and its column to the front. This makes it much harder for the numbers to blow up, and there is a proof that they can only grow slowly as the matrix gets bigger. The search is expensive, though: it looks at almost the whole matrix at every step, so in practice people use it only when they need the extra safety or want to see whether the matrix is close to having lower rank.

## When it applies

The technique applies to any elimination on a square or rectangular matrix where both the equations (rows) and the unknowns (columns) may be reordered. A column swap renames unknowns, so the solution must be permuted back at the end: if $P A Q = L U$, then $x = Q y$ where $L U y = P b$.

**Notation.** $A \in \mathbb{R}^{n \times n}$, $A^{(k)}$ is the active matrix before step $k$, $P$ and $Q$ are permutation matrices, and the computed factors are $\hat L, \hat U$. The unit roundoff is $u = 2^{-53}$, $\gamma_n = n u/(1 - n u)$, and the growth factor is $\rho_n = \max_{i,j,k} |\hat a^{(k)}_{ij}| / \max_{i,j} |a_{ij}|$. Other notation is on the page [linear system solving](/linear-system-solving/).

**What it buys.** The bounds below hold for every nonsingular $A$, assuming $n u < 1$.

- (Proved, Higham Theorem 9.3.) $\hat L \hat U = P A Q + \Delta A$ with $|\Delta A| \le \gamma_n |\hat L| |\hat U|$, and the solve adds $\gamma_{3n}$ in place of $\gamma_n$.
- (Proved, from the first item.) Since $|\hat l_{ij}| \le 1$ and $|\hat u_{ij}| \le \rho_n \max|a_{ij}|$, $\|\Delta A\|_\infty \le n^2 \gamma_{3n} \rho_n \|A\|_\infty$ for the solve.
- (Proved, Wilkinson 1961, in exact arithmetic.) $\rho_n \le f(n)$. The values are $f(10) \approx 19$, $f(20) \approx 72$, $f(50) \approx 570$, $f(100) \approx 3570$, $f(1000) \approx 8.7 \times 10^6$.
- (Observed.) On random matrices the growth is much smaller, roughly $n^{1/2}$, and no practical matrix with large growth under complete pivoting is known.

## The template

```pseudo id=main
COMPLETE-PIVOTED-ELIMINATION(A, n)
L1  π ← (1, ..., n); χ ← (1, ..., n)               ▷ row and column permutations
L2  for k ← 1 to n − 1 do
L3      (p, q) ← a pair in {k..n}² maximizing |a_pq|  ▷ hole: tie rule and the search region
L4      if a_pq = 0 then report "rank k − 1"; stop   ▷ hole: the rank or singularity test
L5      swap rows p and k of A; swap π_p and π_k
L6      swap columns q and k of A; swap χ_q and χ_k
L7      for i ← k + 1 to n do
L8          a_ik ← a_ik / a_kk                        ▷ |a_ik| ≤ 1
L9          for j ← k + 1 to n do
L10             a_ij ← a_ij − a_ik · a_kj
L11 return A, π, χ                                  ▷ P A Q = L U
```

The holes are the tie rule, the search region (all of the active matrix for complete pivoting; alternating row and column searches for rook pivoting) and the test at line L4. When line L4 fires, every remaining entry is exactly zero, so $A$ has rank exactly $k - 1$ in exact arithmetic. In floating point the test is replaced by $|a_{pq}| \le \tau$ for a tolerance such as $\tau = n u \|A\|$.

**Why the growth is bounded (proof sketch).** Let $p_k = |u_{kk}|$ be the pivots. By the choice at line L3, $p_k$ is the largest entry of $A^{(k)}$, and the entries of $A^{(k+1)}$ are the Schur complement of the leading block. Hadamard's inequality applied to the trailing $(n - k + 1) \times (n - k + 1)$ block, whose determinant is $\prod_{j \ge k} p_j$ and whose columns have norm at most $(n - k + 1)^{1/2} p_k$, gives $\prod_{j \ge k} p_j \le (n - k + 1)^{(n - k + 1)/2} p_k^{n - k + 1}$. Taking logarithms and combining these inequalities for all $k$ yields $p_n / p_1 \le f(n)$; Wilkinson (1961) gives the details, and Higham (Section 9.4) reproduces them.

**Cost.** Line L3 inspects $(n - k + 1)^2$ entries, $\sum_k (n - k + 1)^2 \approx n^3/3$ comparisons in total. The flops are those of elimination without pivoting, $2n^3/3$. Since the search reads the whole trailing matrix at each step, it costs as much memory traffic as an unblocked update, and it prevents the delayed updates of blocked LU.

## Classic examples

**A $2 \times 2$ matrix.** For $A = \begin{pmatrix} 1 & 2 \\ 3 & 4 \end{pmatrix}$, line L3 picks $(2, 2)$. After swapping both rows and both columns, $P A Q = \begin{pmatrix} 4 & 3 \\ 2 & 1 \end{pmatrix} = \begin{pmatrix} 1 & 0 \\ 1/2 & 1 \end{pmatrix} \begin{pmatrix} 4 & 3 \\ 0 & -1/2 \end{pmatrix}$. Partial pivoting would choose $3$.

**Wilkinson's matrix.** For $W_n$ with $w_{ii} = 1$, $w_{ij} = -1$ for $i > j$, $w_{in} = 1$, partial pivoting makes no swaps and gives $u_{nn} = 2^{n-1}$. Complete pivoting with the tie rule "smallest row, then smallest column" pivots on $(1, 1)$, after which the last column holds $2$s and becomes the next pivot column; computed in exact arithmetic, the growth factor is $2$ for $n = 4, 8, 16$, against $8, 128, 32768$ for partial pivoting.

**Hadamard matrices.** For a Hadamard matrix $H$ of order $n$ ($\pm 1$ entries, $H^T H = n I$) complete pivoting gives growth exactly $n$ in the cases checked, for example $4$ for the $4 \times 4$ Sylvester matrix. Cryer (1968) conjectured that this holds for all Hadamard matrices.

**Rank-revealing use.** On a matrix of exact rank $r$, complete pivoting stops with an exact zero active matrix after $r$ steps, and on nearby matrices the trailing entries are of the size of the perturbation in most cases (observed). This makes GECP a cheap first rank test, and LAPACK's `getc2` uses it inside the solvers for small Sylvester equations, where robustness matters more than speed.

## Variations

- **[Partial pivoting](/partial-pivoting/).** Search one column only: $n^2/2$ comparisons, growth up to $2^{n-1}$, and the default in practice.
- **Rook pivoting.** Search the column, then the row of the column maximum, and so on, until an entry is largest in both its row and column. The expected cost is a small multiple of partial pivoting's for random matrices, and Foster (1997) proved a growth bound of $1.5\, n^{(3/4)\ln n}$, of the same subexponential type as complete pivoting (Higham, Section 9.1; Golub and Van Loan, Section 3.4).
- **QR with column pivoting.** Choose the column of largest remaining 2-norm; there is no growth to control, but the choice orders the columns for a [rank-revealing factorization](/rank-revealing-factorization/).
- **Symmetric complete pivoting.** For symmetric positive semidefinite matrices, Cholesky with diagonal pivoting chooses the largest diagonal entry; this is complete pivoting restricted to symmetric swaps, and it reveals the rank of a semidefinite matrix.
- **Threshold complete pivoting.** In sparse codes, accept any entry within a factor $\tau$ of the largest in its row or column that minimizes the Markowitz count.

## Pitfalls

- **Forgetting the column permutation.** Solving $L U y = P b$ gives $y = Q^T x$, not $x$. Permute back with $x = Q y$.
- **The growth bound is not small for large $n$.** $f(1000) \approx 8.7 \times 10^6$, so the proved backward error bound for $n = 1000$ is far above $u$; the guarantee is better than partial pivoting's, but in practice both give errors near $u$.
- **The conjecture $\rho_n \le n$ is false.** Wilkinson and later Cryer conjectured it for real matrices. Gould (1991) found a $13 \times 13$ matrix with growth about $13.02$ in floating point, and Edelman (1992) confirmed in exact arithmetic that the growth exceeds $13$. Do not quote $n$ as a bound.
- **Small pivots are not the only sign of near-singularity.** The upper triangular matrix with $1$ on the diagonal and $-1$ above has all entries of size $1$, so complete pivoting (with ties kept in place) makes no swaps and every pivot is $1$, yet its smallest singular value is about $2^{-n}$ times its norm. Use a [condition estimate](/hagers-condition-estimator/) or the SVD to judge conditioning.
- **Speed.** The search costs $O(n^3)$ memory reads and blocks the use of level 3 BLAS. For large dense systems, partial pivoting with a growth check is the usual choice.

## Exercises

1. Show that complete pivoting with exact arithmetic stops at line L4 after exactly $\operatorname{rank}(A)$ steps.
2. Prove $f(2) = 2$ and show that it is attained by a $2 \times 2$ matrix.
3. Fill in the details of Wilkinson's argument: from Hadamard's inequality on the trailing blocks, derive $\ln(p_n/p_1) \le \tfrac12 \ln n + \tfrac12 \sum_{k=2}^{n} \tfrac{\ln k}{k - 1}$.
4. Verify that complete pivoting gives growth $2$ on Wilkinson's matrix $W_4$ with the tie rule of the classic example.
5. Show that GECP of the $4 \times 4$ Sylvester-Hadamard matrix gives pivots of magnitudes $1, 2, 2, 4$, so its growth factor is $4$.
6. Count the comparisons of rook pivoting on a matrix where each column maximum is also its row maximum, and compare with complete pivoting.

## References
