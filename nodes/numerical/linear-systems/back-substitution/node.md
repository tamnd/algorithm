---
tag: 4HMP35
kind: algorithm
slug: back-substitution
name: Forward and back substitution
aliases:
- forward substitution
- back substitution
- backward substitution
- triangular solve
area: numerical/linear-systems
level: intro
summary: Solve a triangular system one unknown at a time, from the top or the bottom.
solves: [triangular-system-solving]
model: floating-point-model
complexity:
  vars: {n: "the order of the triangular matrix, at least 1"}
  time: {worst: Θ(n^2), best: Θ(n^2)}
  space: {extra: Θ(1)}
  flops: {worst: n^2}
properties: {deterministic: true, in_place: true, recursive: false}
prereqs: [linear-system-solving, floating-point-model]
see_also: [triangular-system-solving, lu-decomposition, lup-decomposition, cholesky-decomposition, gaussian-elimination, backward-error-analysis]
sources:
  - book: isbn:9780898715217
    title: Nicholas J. Higham, Accuracy and Stability of Numerical Algorithms, second edition, SIAM, 2002
    locator: Chapter 8, Triangular Systems (Lemma 8.4 for one row, Theorem 8.5, the backward error |ΔT| ≤ γ_n |T| for substitution in any order, and the forward error analysis of the same chapter, including triangular M-matrices); Lemma 3.1 for the γ_n bound
  - book: isbn:9780898713619
    title: Lloyd N. Trefethen and David Bau III, Numerical Linear Algebra, SIAM, 1997
    locator: Lecture 17, Stability of Back Substitution (Theorem 17.1)
  - book: isbn:9781421407944
    title: Gene H. Golub and Charles F. Van Loan, Matrix Computations, fourth edition, Johns Hopkins University Press, 2013
    locator: Section 3.1, Triangular Systems (row and column oriented versions, multiple right sides, the flop count)
  - paper: doi:10.1145/321075.321076
    title: J. H. Wilkinson, Error analysis of direct methods of matrix inversion, Journal of the ACM 8(3), 1961
    locator: pp. 281 to 330 (the backward error analysis of elimination and of the solution of triangular systems)
  - book: isbn:9780898716139
    title: Timothy A. Davis, Direct Methods for Sparse Linear Systems, SIAM, 2006
    locator: Chapter 3, Solving Triangular Systems (the sparse right side case by depth-first search)
---

Back substitution solves an upper triangular system $U x = b$ from the last unknown to the first, and forward substitution solves a lower triangular system $L y = b$ from the first unknown to the last. Each costs $n^2$ flops. They are the second half of each direct solver: after an [LU decomposition](/lu-decomposition/) $P A = L U$, the system $A x = b$ becomes $L y = P b$ and then $U x = y$. In [floating-point arithmetic](/floating-point-model/) both are backward stable in the strongest sense: the computed $\hat x$ solves $(U + \Delta U)\hat x = b$ with $|\Delta U| \le \gamma_n |U|$, entry by entry.

## In plain words

In a triangular system the last equation has only one unknown, so you get it with one division. The equation above it has two unknowns, but one of them is now known: move its part to the right side and divide again. Go on upwards, and each step uses the values found before it. That is back substitution. For a system where the first equation has one unknown, do the same from the top down; that is forward substitution.

The method fails only when a number on the diagonal is zero, and then the system has no unique answer. With rounding, the method gives the exact answer of a system whose numbers differ from yours by a few roundings each.

## The problem

**Notation.** As in [solving linear systems](/linear-system-solving/): $U = (u_{ij})$ is an $n \times n$ upper triangular real matrix ($u_{ij} = 0$ for $i > j$), $b \in \mathbb{R}^n$, $x$ is the exact solution, $\hat x$ the computed one, $u$ is the unit roundoff and $\gamma_n = n u / (1 - n u)$. $|U|$ is the matrix of the $|u_{ij}|$, and inequalities between matrices hold entry by entry.

Input: $U$ and $b$. Output: $x$ with $U x = b$, or the report that $U$ is singular. Since $\det U = \prod_i u_{ii}$, $U$ is nonsingular exactly when each $u_{ii} \neq 0$.

## The algorithm

Row $i$ of $U x = b$ reads $u_{ii} x_i + \sum_{j > i} u_{ij} x_j = b_i$, so $x_i = (b_i - \sum_{j > i} u_{ij} x_j)/u_{ii}$, and the sum uses only unknowns that are already known when $i$ runs from $n$ down to $1$.

```pseudo id=main
BACK-SUBSTITUTION(U, b)                    ▷ U upper triangular, n × n
L1  for i ← n downto 1 do
L2      if u_ii = 0 then return SINGULAR
L3      s ← b_i
L4      for j ← i + 1 to n do
L5          s ← s − u_ij · x_j
L6      x_i ← s / u_ii
L7  return x
```

Forward substitution for a lower triangular $L$ is the same with the loops turned around: $i$ runs from $1$ to $n$, and the inner loop runs over $j = 1, \ldots, i - 1$ with $l_{ij}$ in place of $u_{ij}$. If $L$ has a unit diagonal, as the $L$ of an LU decomposition has, line L6 has no division.

```pseudo id=forward
FORWARD-SUBSTITUTION(L, b)                 ▷ L lower triangular, n × n
F1  for i ← 1 to n do
F2      if l_ii = 0 then return SINGULAR
F3      s ← b_i
F4      for j ← 1 to i − 1 do
F5          s ← s − l_ij · x_j
F6      x_i ← s / l_ii
F7  return x
```

This is the *row-oriented* form: it reads $U$ by rows and computes one inner product per row. The *column-oriented* form (Golub and Van Loan, Section 3.1) computes $x_n$, subtracts $x_n$ times column $n$ from $b$, and goes on with the leading $(n-1) \times (n-1)$ block. Both do the same flops in a different order, and the error bound below holds for both.

## Example

Solve $U x = b$ with
$$U = \begin{pmatrix} 2 & 1 & -1 & 3 \\ 0 & 1 & 2 & -1 \\ 0 & 0 & 4 & 2 \\ 0 & 0 & 0 & 5 \end{pmatrix}, \qquad b = \begin{pmatrix} 0 \\ 3 \\ 14 \\ 5 \end{pmatrix}.$$

| $i$ | $s$ after line L5 | $x_i = s / u_{ii}$ |
|---|---|---|
| 4 | $5$ | $5 / 5 = 1$ |
| 3 | $14 - 2 \cdot 1 = 12$ | $12 / 4 = 3$ |
| 2 | $3 - 2 \cdot 3 - (-1) \cdot 1 = -2$ | $-2 / 1 = -2$ |
| 1 | $0 - 1 \cdot (-2) - (-1) \cdot 3 - 3 \cdot 1 = 2$ | $2 / 2 = 1$ |

So $x = (1, -2, 3, 1)^T$. All numbers here are small integers, so binary64 gives this answer with no rounding.

**An ill-conditioned matrix with an accurate answer.** Let $T$ be the $40 \times 40$ upper triangular matrix with $t_{ii} = 1$ and $t_{ij} = -1$ for $j > i$, and $b_i = 1/i$ rounded to binary64. Then $(T^{-1})_{ij} = 2^{j - i - 1}$ for $j > i$, so $\kappa_\infty(T) = 40 \cdot 2^{39} \approx 2.2 \times 10^{13}$, and $x_1 \approx 1.41 \times 10^{10}$. Back substitution in binary64 gives each $\hat x_i$ with relative error at most $4.1 \times 10^{-16}$, under $4u$. The normwise bound $\gamma_n \kappa_\infty(T)$ is about $0.1$ here and very pessimistic. Higham (Chapter 8) explains this: $T$ is an M-matrix and $b \ge 0$, so no cancellation happens and the componentwise forward error is small.

## Correctness

In exact arithmetic, a downward induction on $i$ shows that after the pass for index $i$, the values $x_i, \ldots, x_n$ equal the entries of the solution, because line L6 is row $i$ of $U x = b$ solved for $x_i$. In floating point, the computed $\hat x$ satisfies
$$(U + \Delta U)\hat x = b, \qquad |\Delta U| \le \gamma_n |U|$$
when $n u < 1$ (Higham, Theorem 8.5). The perturbation of row $i$ is at most $\gamma_{n - i + 1}$ relative to each entry, and $b$ is not perturbed. Both proofs are in [the proof](proofs/correctness.md).

**Forward error.** From the backward error, $\hat x - x = -U^{-1} \Delta U \hat x$. If $\gamma_n \kappa(U) < 1$ in a norm with $\| |U| \| = \|U\|$ (for example $\infty$, $1$ or Frobenius), then
$$\frac{\|x - \hat x\|}{\|x\|} \le \frac{\gamma_n \kappa(U)}{1 - \gamma_n \kappa(U)},$$
and with $\operatorname{cond}(U, x) = \| |U^{-1}| \, |U| \, |x| \|_\infty / \|x\|_\infty$ and $\operatorname{cond}(U) = \| |U^{-1}| \, |U| \|_\infty$ (the Skeel condition numbers), the sharper bound
$$\frac{\|x - \hat x\|_\infty}{\|x\|_\infty} \le \frac{\gamma_n \operatorname{cond}(U, x)}{1 - \gamma_n \operatorname{cond}(U)}$$
holds when $\gamma_n \operatorname{cond}(U) < 1$. It follows from $|\hat x - x| \le \gamma_n |U^{-1}| \, |U| \, |\hat x|$ and $|\hat x| \le |x| + |\hat x - x|$. Both are worst-case bounds. In practice triangular systems are often solved much more accurately than $\kappa(U) u$, as the example shows (Higham, Chapter 8, gives the explanation for several classes).

## Complexity

Row $i$ costs $n - i$ multiplications, $n - i$ subtractions and one division, so the total is $\sum_{i=1}^n (2(n - i) + 1) = n(n - 1) + n = n^2$ flops in each case, best and worst. With a unit diagonal it is $n^2 - n$ flops. The space is $\Theta(1)$ besides $x$, and $x$ can overwrite $b$ in place, since $b_i$ is read only at row $i$, before $x_i$ is written.

For $k$ right sides, $U X = B$ costs $k n^2$ flops. Each entry of $U$ is used once per right side, so a single solve does about one flop per word read from memory: it is limited by memory traffic, not by arithmetic. With many right sides, the blocked form uses matrix-matrix products and runs close to the peak speed. A solve with a band of width $p$ costs about $2 n p$ flops, and a sparse solve costs about $2 \cdot \text{nnz}(U)$ flops.

## Properties

- **Backward stable, componentwise.** The bound $|\Delta U| \le \gamma_n |U|$ is the strongest kind of backward error: each entry is perturbed relative to itself, zeros stay zero and $b$ is exact.
- **Order independent.** The bound holds for the row and the column form and for any order of the inner sums (Higham, Theorem 8.5).
- **Sequential.** Each $x_i$ depends on all later ones, so the critical path has length $\Theta(n)$. Parallel versions trade more flops for a shorter path.
- **No pivoting.** The pivots are given; a zero diagonal entry means a singular matrix.

## Variants and improvements

- **Forward substitution** for lower triangular systems, as above.
- **Unit triangular** systems from LU skip the divisions.
- **Transposed solves** $U^T y = c$ are forward substitutions that read $U$ by columns; LAPACK `xTRTRS` offers both.
- **Blocked triangular solve** (BLAS 3 `xTRSM`) splits $U$ into blocks: a small solve on the diagonal block, then a matrix product to update the rest.
- **Sparse triangular solve.** When $b$ is sparse too, only the unknowns reachable from the nonzeros of $b$ in the graph of $U$ are nonzero, and a depth-first search finds them first (Gilbert and Peierls; Davis, Chapter 3).
- **Band and tridiagonal** solves loop only over the band.

## When to use it

Use it each time a matrix is triangular or has been factored into triangles: after LU, [Cholesky](/cholesky-decomposition/) ($R^T R x = b$ is a forward and a back substitution) and QR ($R x = Q^T b$). Do not form a triangular inverse to apply it: $T^{-1} b$ costs the same $n^2$ flops per right side after $n^3/3$ flops for the inverse, and is less accurate.

## Pitfalls

- **Wrong loop direction.** Running line L1 upward ($i$ from $1$) on an upper triangular matrix uses $x_j$ for $j > i$ before they are computed. Back substitution goes from $n$ down to $1$; forward substitution goes up.
- **A test for zero is not a test for singularity.** Line L2 catches an exact zero. A tiny $u_{ii}$, for example $10^{-300}$, passes the test, and the result can overflow or be meaningless. Estimate $\kappa(U)$ (with [Hager's estimator](/hagers-condition-estimator/), or the LAPACK routine `xTRCON`) when the data can be nearly singular.
- **The normwise bound is not the observed error.** The forward error can be far smaller than $\kappa(U) u$ (the example has $\kappa_\infty \approx 10^{13}$ and full accuracy), or close to it. Do not use $\kappa(U) u$ as an estimate of the error of one solve.
- **Overwriting and order.** In the column form, $b$ is updated in place; reading an updated $b_j$ as if it were the original gives wrong answers.

## Implementations

## History

Substitution is the last step of elimination, and it is as old as elimination. The rounding error analysis of triangular systems is due to Wilkinson, in his 1961 paper on the error analysis of direct methods and in his 1963 book *Rounding Errors in Algebraic Processes*. Higham (Chapter 8) gives the modern form $|\Delta T| \le \gamma_n |T|$ and surveys the forward error results that explain why triangular systems are often solved more accurately than their condition number suggests.

## References
