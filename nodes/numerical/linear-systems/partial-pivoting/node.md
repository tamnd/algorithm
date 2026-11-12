---
tag: KKCX6A
kind: technique
slug: partial-pivoting
name: Partial pivoting
aliases:
- row pivoting
- partial pivoting strategy
- column-maximum pivoting
area: numerical/linear-systems
level: core
summary: Swap rows to place the largest pivot in the column to keep elimination stable.
prereqs: [gaussian-elimination, growth-factor, floating-point-model]
see_also: [lup-decomposition, lup-solve, complete-pivoting, growth-factor, diagonally-dominant-matrix, cholesky-decomposition, rank-revealing-factorization, sparse-linear-systems]
sources:
  - book: isbn:9780898715217
    title: Nicholas J. Higham, Accuracy and Stability of Numerical Algorithms, second edition, SIAM, 2002
    locator: Chapter 9, LU Factorization and Linear Equations (Section 9.1, pivoting strategies, including rook pivoting; Section 9.3, error analysis; Section 9.4, the growth factor; Section 9.5, diagonally dominant and banded matrices; Section 9.6, tridiagonal matrices); Chapter 11, symmetric indefinite matrices (pivoting for LDL^T)
  - book: isbn:9781421407944
    title: Gene H. Golub and Charles F. Van Loan, Matrix Computations, fourth edition, Johns Hopkins University Press, 2013
    locator: Section 3.4, Pivoting (partial, complete and rook pivoting, and the growth bounds); Section 3.5, Improving and estimating accuracy (scaling)
  - book: isbn:9780898713619
    title: Lloyd N. Trefethen and David Bau III, Numerical Linear Algebra, SIAM, 1997
    locator: Lecture 21, Pivoting; Lecture 22, Stability of Gaussian elimination
  - paper: doi:10.1145/321075.321076
    title: J. H. Wilkinson, Error analysis of direct methods of matrix inversion, Journal of the ACM 8(3), 1961
    locator: the backward error analysis of Gaussian elimination and the growth bounds for partial and complete pivoting
  - paper: doi:10.1137/0611023
    title: Lloyd N. Trefethen and Robert S. Schreiber, Average-case stability of Gaussian elimination, SIAM Journal on Matrix Analysis and Applications 11(3), 1990
    locator: the experiments on the growth factor of random matrices
  - paper: doi:10.1137/0914014
    title: Stephen J. Wright, A collection of problems for which Gaussian elimination with partial pivoting is unstable, SIAM Journal on Scientific Computing 14(1), 1993
    locator: the two-point boundary value problems with exponential growth
---

Partial pivoting is the rule that, before each step of [Gaussian elimination](/gaussian-elimination/), swaps rows so that the entry of largest magnitude in the current column, on or below the diagonal, becomes the pivot. Every multiplier then has magnitude at most one, and the [growth factor](/growth-factor/) is at most $2^{n-1}$. The same rule, applied to elimination on other structures, keeps them stable too. The cost is $n(n-1)/2$ comparisons for a dense matrix, which is nothing next to the $2n^3/3$ flops of the elimination. It is the default in LAPACK's `getrf` and in the [LUP decomposition](/lup-decomposition/).

## In plain words

Elimination subtracts multiples of one row from the rows below it. If the row in front has a tiny leading number, the multiples are huge, and adding huge numbers to normal ones wipes out their digits. Partial pivoting looks down the column first and moves the row with the biggest leading number to the front. Then no row is ever multiplied by more than one before it is subtracted, and the numbers stay about the size they started at in almost every case seen in practice. The rule is cheap: one scan down a column for each step.

## When it applies

The technique applies to an elimination that, at step $k$, divides by a pivot $a^{(k)}_{kk}$ and subtracts multiples of the pivot row from later rows, and where any of the rows still to be used could serve as the pivot row. Swapping rows only permutes the equations, so the solution set does not change.

**Notation.** $A \in \mathbb{R}^{n \times n}$, $A^{(k)}$ is the active matrix before step $k$, and $l_{ik} = a^{(k)}_{ik}/a^{(k)}_{kk}$ are the multipliers. The computed factors are $\hat L$, $\hat U$ with $P A \approx \hat L \hat U$. The unit roundoff is $u = 2^{-53}$ in binary64, $\gamma_n = n u/(1 - n u)$, and the growth factor is $\rho_n = \max_{i,j,k} |\hat a^{(k)}_{ij}| / \max_{i,j}|a_{ij}|$. The rest of the notation is on the page [linear system solving](/linear-system-solving/).

**What it buys (proved).** With partial pivoting, $|l_{ik}| \le 1$ for all $i, k$, and each step at most doubles the largest entry of the active matrix, so $\rho_n \le 2^{n-1}$. For each nonsingular $A$, and assuming $n u < 1$, the computed factors satisfy

$$\hat L \hat U = P A + \Delta A, \qquad |\Delta A| \le \gamma_n |\hat L|\,|\hat U|, \qquad \|\Delta A\|_\infty \le n^2 \gamma_n \rho_n \|A\|_\infty$$

(Higham, Section 9.3; the proof is on the page [LUP decomposition](/lup-decomposition/)). The solve with the factors adds a backward error of the same form, with $\gamma_{3n}$ in place of $\gamma_n$ ([LUP solve](/lup-solve/)). So the method is backward stable whenever $\rho_n$ is modest.

**What it does not buy.** The bound $2^{n-1}$ is attained, by Wilkinson's matrix, so partial pivoting is not backward stable for every matrix in the worst case. On random matrices the observed growth is small, roughly $n^{2/3}$ for Gaussian entries in the experiments of Trefethen and Schreiber (1990), and exponential growth in applications is rare (Wright 1993 gives some). This is an observation, not a theorem.

## The template

```pseudo id=main
PIVOTED-ELIMINATION(A, n)
L1  π ← (1, 2, ..., n)
L2  for k ← 1 to n - 1 do                                  ▷ hole: which steps eliminate
L3      p ← an index in CAND(k) maximizing |a_pk|           ▷ hole: the candidate rows CAND(k)
L4      if a_pk = 0 then report "singular at step k"; stop  ▷ hole: the singularity test
L5      if p ≠ k then swap rows p and k of A; swap π_p and π_k
L6      for i in TARGETS(k) do                              ▷ hole: the rows to update
L7          a_ik ← a_ik / a_kk                              ▷ multiplier, |a_ik| ≤ 1
L8          for j in COLS(k) do                             ▷ hole: the columns that change
L9              a_ij ← a_ij - a_ik · a_kj
L10 return A, π
```

The holes are the candidate set CAND$(k)$ (for dense LU, all rows $k, \ldots, n$), the rows TARGETS$(k)$ to update (the rows below $k$ with a nonzero in column $k$), the columns COLS$(k)$ (the columns $k+1, \ldots, n$ where the pivot row is nonzero), and the singularity test. Line L5 swaps whole rows, including the multipliers already stored, so that the final array holds $\hat L$ and $\hat U$ of $P A$.

**Why the multipliers are bounded.** At line L7, $|a_{ik}| \le |a_{kk}|$ for each $i$ in CAND$(k)$, because line L3 chose the maximum and line L5 moved it to row $k$. So $|l_{ik}| \le 1$ whenever TARGETS$(k) \subseteq$ CAND$(k)$. Line L9 then gives $|a^{(k+1)}_{ij}| \le |a^{(k)}_{ij}| + |a^{(k)}_{kj}| \le 2 \max |A^{(k)}|$, which yields $\rho_n \le 2^{n-1}$ by induction.

**Cost.** Line L3 makes $|$CAND$(k)| - 1$ comparisons, $n(n-1)/2$ in total for dense LU. Line L5 moves $2n$ numbers per swap if done eagerly; LAPACK delays the swaps of the trailing matrix to block updates, and many codes keep only $\pi$ and index through it. The flop count of lines L6 to L9 is that of the elimination without pivoting.

## Classic examples

**A tiny pivot.** For $A = \begin{pmatrix} \varepsilon & 1 \\ 1 & 1 \end{pmatrix}$ with $\varepsilon = 10^{-20}$ and $b = (1, 2)^T$, the exact solution is $x_1 = 1/(1 - \varepsilon)$, $x_2 = (1 - 2\varepsilon)/(1 - \varepsilon)$, both equal to $1$ to working precision. Without pivoting, binary64 gives $l_{21} = 10^{20}$, $\hat u_{22} = \mathrm{fl}(1 - 10^{20}) = -10^{20}$, $\hat x_2 = 1$ and $\hat x_1 = (1 - 1)/\varepsilon = 0$: a relative error of $1$ in $x_1$, although $\kappa_\infty(A) \approx 4$. With partial pivoting the rows are swapped, $l_{21} = 10^{-20}$, $\hat u_{22} = 1$, and $\hat x = (1, 1)$. The loss comes from $\|\,|\hat L|\,|\hat U|\,\| \approx 10^{20}$, not from $\kappa(A)$ (Trefethen and Bau, Lecture 21).

**Dense LU.** $\mathrm{CAND}(k) = \mathrm{TARGETS}(k) = \{k, \ldots, n\}$ and COLS$(k) = \{k+1, \ldots, n\}$ give the [LUP decomposition](/lup-decomposition/), $P A = L U$.

**Hessenberg matrices.** If $a_{ij} = 0$ for $i > j + 1$, only rows $k$ and $k+1$ are candidates and targets. Partial pivoting then costs $n - 1$ comparisons, and the growth factor is at most $n$ (Higham, Section 9.4). This is the elimination used in inverse iteration on a [Hessenberg](/hessenberg-reduction/) matrix.

**Tridiagonal and banded matrices.** With lower bandwidth $p$ and upper bandwidth $q$, CAND$(k)$ has $p + 1$ rows, and a swap can widen the upper bandwidth of $U$ to $p + q$ (Golub and Van Loan, Section 4.3). For a tridiagonal matrix the growth factor with partial pivoting is at most $2$ (Higham, Section 9.6). The [Thomas algorithm](/thomas-algorithm/) is the version without pivoting, safe for diagonally dominant matrices.

**When no pivoting is needed.** If $A$ is diagonally dominant by columns, elimination without pivoting never prefers another row, so partial pivoting makes no swaps, and $\rho_n \le 2$ (Higham, Section 9.5; see [diagonally dominant matrix](/diagonally-dominant-matrix/)). If $A$ is symmetric positive definite, elimination without pivoting is stable, with $\rho_n \le 1$ for the entries, and [Cholesky](/cholesky-decomposition/) is the right method.

**Exponential growth in practice.** Wright (1993) discretized two-point boundary value problems by multiple shooting and obtained matrices on which partial pivoting shows growth like $2^n$, so the computed solution is useless while QR or complete pivoting works.

## Variations

- **[Complete pivoting](/complete-pivoting/).** Search the whole active submatrix and swap rows and columns. Wilkinson proved the growth bound $\rho_n \le n^{1/2}(2 \cdot 3^{1/2} \cdots n^{1/(n-1)})^{1/2}$, which grows much slower than $2^{n-1}$, at the cost of about $n^3/3$ comparisons. It also reveals rank better (see [rank-revealing factorization](/rank-revealing-factorization/)).
- **Rook pivoting.** Search alternately in a column and a row until an entry is largest in both. It needs a few times the comparisons of partial pivoting on average, and its growth bound is subexponential, of the form $1.5\, n^{3/4 \log n}$ (Higham, Section 9.1, citing Foster).
- **Threshold pivoting.** In [sparse](/sparse-linear-systems/) LU, accept any candidate with $|a_{pk}| \ge \tau \max_i |a_{ik}|$ for a threshold such as $\tau = 0.1$, and among those choose the one that causes the least fill (Markowitz count). The multipliers satisfy $|l_{ik}| \le 1/\tau$, and the growth bound becomes $(1 + 1/\tau)^{n-1}$.
- **Scaled partial pivoting.** Choose $p$ to maximize $|a_{pk}|/s_p$, where $s_p$ is the largest entry of the original row $p$. This makes the choice invariant under row scaling. Golub and Van Loan, Section 3.5, discuss why no scaling rule is best in general.
- **Tournament pivoting.** Communication-avoiding LU picks the pivots of a block column by a reduction tree of small eliminations, so a parallel code does not need a global maximum per column. Its growth bound is weaker than that of partial pivoting, but the observed growth is similar.
- **Symmetric indefinite matrices.** Row swaps destroy symmetry, so $L D L^T$ factorizations use symmetric swaps and $2 \times 2$ pivots (Bunch-Kaufman and its relatives, Higham, Chapter 11).
- **Column pivoting in QR.** QR with column pivoting moves the column of largest remaining norm to the front. It does not control growth, which orthogonal transformations already prevent; it orders the columns to reveal the rank (see [QR decomposition](/qr-decomposition/)).

## Pitfalls

- **It depends on scaling.** Multiplying row $1$ of the tiny-pivot example by $10^{20}$ gives $\begin{pmatrix} 1 & 10^{20} \\ 1 & 1 \end{pmatrix}$, with $b = (10^{20}, 2)^T$ and the same solution. Now the two candidates tie at $1$, the first row is kept, and the computed solution is again $(0, 1)$. Partial pivoting protects against small pivots relative to the column, not against a badly scaled matrix.
- **Testing for singularity.** Line L4 tests for an exact zero. A pivot of size $u \|A\|$ is the usual sign of a numerically singular matrix, but partial pivoting is not a reliable rank test: there are matrices with no small pivot that are nearly singular. Use a [condition estimate](/hagers-condition-estimator/), the SVD or a [rank-revealing factorization](/rank-revealing-factorization/).
- **Small growth is not a small error.** Backward stability gives a small residual, and the forward error is then bounded by about $\kappa(A)$ times the backward error. On the [Hilbert matrix](/hilbert-matrix/) $H_{10}$ partial pivoting gives a backward error near $u$ and a forward error near $10^{-4}$, which is the best one can expect.
- **Swaps break structure.** In sparse matrices the pivot of largest magnitude can create much more [fill-in](/fill-in/) than another choice, and in banded matrices it widens the band. That is why threshold pivoting exists.
- **Ties.** The rule of line L3 must pick one of the tied rows in a fixed way (for example the first). Different tie rules give different but equally valid factorizations, which matters when comparing with a reference.
- **Pivot search is a synchronization point.** In parallel and out-of-core codes, the column maximum at each step is a global reduction, which can cost more than the flops of a narrow panel.

## Exercises

1. Show that for the $2 \times 2$ example without pivoting, $\|\,|\hat L|\,|\hat U|\,\|_\infty \approx 2 \cdot 10^{20}$ while $\|A\|_\infty = 2$, and use the bound $|\Delta A| \le \gamma_2 |\hat L||\hat U|$ to explain the result.
2. Prove that for Wilkinson's matrix ($a_{ii} = 1$, $a_{ij} = -1$ for $i > j$, $a_{in} = 1$, zero elsewhere), partial pivoting with the first-index tie rule makes no swaps and gives $u_{nn} = 2^{n-1}$.
3. Prove that if $A$ is upper Hessenberg, partial pivoting gives $\rho_n \le n$.
4. Prove that if $A^T$ is strictly diagonally dominant by rows, partial pivoting makes no swaps, and that each active matrix stays diagonally dominant by columns.
5. With threshold $\tau$, show that $|l_{ik}| \le 1/\tau$ and $\rho_n \le (1 + 1/\tau)^{n-1}$.
6. Give a $3 \times 3$ matrix where partial pivoting and scaled partial pivoting choose different first pivots, and compare the computed solutions in a low precision.

## References
