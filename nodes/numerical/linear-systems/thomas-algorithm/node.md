---
tag: V8X0CR
kind: algorithm
slug: thomas-algorithm
name: Thomas algorithm
aliases:
- TDMA
- tridiagonal matrix algorithm
- tridiagonal Gaussian elimination
- sweep method
area: numerical/linear-systems
level: core
summary: Gaussian elimination specialized to tridiagonal systems, in O(n) time.
solves: [tridiagonal-system-solving]
model: floating-point-model
complexity:
  vars: {n: "the order of the tridiagonal matrix, at least 1"}
  time: {worst: Θ(n), best: Θ(n)}
  space: {extra: Θ(n)}
  flops: {worst: "8n - 7"}
properties: {deterministic: true, in_place: true, recursive: false}
prereqs: [lu-decomposition, diagonally-dominant-matrix, banded-matrix]
see_also: [tridiagonal-system-solving, cyclic-reduction, partial-pivoting, sherman-morrison-formula, cholesky-decomposition, lup-decomposition, growth-factor, positive-definite-matrix]
sources:
  - book: isbn:9780898715217
    title: Nicholas J. Higham, Accuracy and Stability of Numerical Algorithms, second edition, SIAM, 2002
    locator: Section 9.6, Tridiagonal Matrices (the recurrences of LU without pivoting, the backward error bound with the constant f(u) = 4u + 3u^2 + u^3, and the classes of matrices for which |L||U| is bounded by a multiple of |A|)
  - book: isbn:9781421407944
    title: Gene H. Golub and Charles F. Van Loan, Matrix Computations, fourth edition, Johns Hopkins University Press, 2013
    locator: Section 4.3, Banded Systems (tridiagonal LU and the symmetric positive definite tridiagonal case)
  - book: isbn:9780898713893
    title: James W. Demmel, Applied Numerical Linear Algebra, SIAM, 1997
    locator: Section 2.7.3, Band matrices (tridiagonal Gaussian elimination and its cost)
  - book: isbn:9780898715347
    title: Yousef Saad, Iterative Methods for Sparse Linear Systems, second edition, SIAM, 2003
    locator: Section 2.2, Finite difference methods (the tridiagonal matrix of the one-dimensional model problem)
---

The Thomas algorithm solves a tridiagonal linear system $A x = d$ by Gaussian elimination without pivoting, written out for the three diagonals. A forward sweep eliminates the subdiagonal and a backward sweep substitutes, for $8n - 7$ flops and $O(n)$ storage, against $2n^3/3$ for dense elimination. Without pivoting it can break down or lose accuracy, but on the matrices where tridiagonal systems usually come from (diagonally dominant, symmetric positive definite, M-matrices) it is componentwise backward stable.

## In plain words

In a tridiagonal system each equation involves only an unknown and its two neighbors. Use the first equation to remove the first unknown from the second equation, then use the new second equation to remove the second unknown from the third, and so on down the line. The last equation then has one unknown and gives its value. Walking back up the line, each equation now has only one unknown left. Each step touches a handful of numbers, so the work grows only in proportion to the number of equations.

## The problem

Given $a_2, \ldots, a_n$ (subdiagonal), $b_1, \ldots, b_n$ (diagonal), $c_1, \ldots, c_{n-1}$ (superdiagonal) and $d \in \mathbb{R}^n$, solve

$$a_i x_{i-1} + b_i x_i + c_i x_{i+1} = d_i, \qquad i = 1, \ldots, n,$$

with $x_0 = x_{n+1} = 0$. The algorithm assumes that elimination without pivoting meets no zero pivot, which holds if every leading principal minor of $A$ is nonzero.

**Notation.** $A = L U$ with $L$ unit lower bidiagonal (subdiagonal $l_i$) and $U$ upper bidiagonal (diagonal $u_i$, superdiagonal $c_i$). Hats denote computed quantities. $u$ without an index is the unit roundoff $2^{-53}$; $\kappa_\infty(A) = \|A\|_\infty \|A^{-1}\|_\infty$. The rest of the notation is on the page [linear system solving](/linear-system-solving/).

## The algorithm

```pseudo id=main
THOMAS(a, b, c, d)                         ▷ a_i x_{i−1} + b_i x_i + c_i x_{i+1} = d_i
L1  u_1 ← b_1;  y_1 ← d_1
L2  for i ← 2 to n do
L3      l_i ← a_i / u_{i−1}                  ▷ stop if u_{i−1} = 0: a row swap would be needed
L4      u_i ← b_i − l_i · c_{i−1}             ▷ the pivot: the Schur complement of the leading block
L5      y_i ← d_i − l_i · y_{i−1}             ▷ forward substitution L y = d, merged with the factorization
L6  x_n ← y_n / u_n                          ▷ stop if u_n = 0: A is singular
L7  for i ← n − 1 downto 1 do x_i ← (y_i − c_i · x_{i+1}) / u_i
L8  return x
```

Lines L2 to L5 factor $A = L U$ and solve $L y = d$ in the same sweep. Lines L6 and L7 solve $U x = y$. If $d$ is not known in advance, store $l_i$ and $u_i$ and run line L5 and lines L6 to L7 later for each right side, at $5n - 4$ flops per solve. The common "modified coefficients" form divides each row by its pivot ($c'_i = c_i/u_i$, $d'_i = y_i/u_i$), which gives the same values in exact arithmetic.

## Example

The model problem $T_4 = \operatorname{tridiag}(-1, 2, -1)$ with $d = (1, 0, 0, 1)^T$ has the solution $x = (1, 1, 1, 1)^T$.

| $i$ | $l_i$ (L3) | $u_i$ (L4) | $y_i$ (L5) |
|---|---|---|---|
| 1 | | $2$ | $1$ |
| 2 | $-\tfrac12$ | $2 - \tfrac12 = \tfrac32$ | $0 + \tfrac12 \cdot 1 = \tfrac12$ |
| 3 | $-\tfrac23$ | $2 - \tfrac23 = \tfrac43$ | $0 + \tfrac23 \cdot \tfrac12 = \tfrac13$ |
| 4 | $-\tfrac34$ | $2 - \tfrac34 = \tfrac54$ | $1 + \tfrac34 \cdot \tfrac13 = \tfrac54$ |

Line L6 gives $x_4 = 1$, and line L7 gives $x_3 = (\tfrac13 + 1)/\tfrac43 = 1$, $x_2 = (\tfrac12 + 1)/\tfrac32 = 1$, $x_1 = (1 + 1)/2 = 1$. In general $u_i = (i+1)/i$ for this matrix, so the pivots stay between $1$ and $2$ and $\det T_n = n + 1$.

## Correctness

**Exact arithmetic.** By induction on $i$, $u_i$ is the $(1,1)$ entry of the [Schur complement](/schur-complement/) of the leading $(i-1) \times (i-1)$ block, and Gaussian elimination on a tridiagonal matrix creates no fill: eliminating $x_{i-1}$ from row $i$ changes only $b_i$ and $d_i$. So lines L2 to L5 are exactly Gaussian elimination without pivoting, and $A = L U$, $L y = d$. Lines L6 and L7 are back substitution with the bidiagonal $U$. The pivots are nonzero exactly when all leading principal minors are nonzero, since $u_1 \cdots u_i = \det A_{1:i,1:i}$. The details are in [the proof](proofs/correctness.md).

**Backward error (proved).** In the [standard model](/floating-point-model/), if no pivot is zero, the computed $\hat x$ satisfies

$$(A + \Delta A)\hat x = d, \qquad |\Delta A| \le f(u)\, |\hat L|\,|\hat U|, \qquad f(u) = 4u + 3u^2 + u^3$$

(Higham, Section 9.6). Each entry of $\hat L$ and $\hat U$ comes from one division or one multiply and subtract, so the constant does not grow with $n$. The tests check this inequality in exact rational arithmetic for every computed solution.

**When the bound is small (proved).** If $A$ is symmetric positive definite, diagonally dominant by rows or by columns, an M-matrix, or totally nonnegative, then $|\hat L|\,|\hat U|$ is bounded by a small constant times $|A|$ (Higham, Section 9.6), so the method is componentwise backward stable: $|\Delta A| \le c\, u\, |A|$ with a small $c$. The forward error is then at most about $c\, u\, \mathrm{cond}(A, \hat x)$ in Skeel's condition number, which is often much smaller than $u\,\kappa_\infty(A)$. For a general nonsingular tridiagonal matrix there is no such guarantee: a tiny pivot makes $|\hat L|\,|\hat U|$ huge (see Pitfalls).

## Complexity

Lines L3 to L5 cost one division, two multiplications and two subtractions per row, $5(n-1)$ flops; line L6 is one division; line L7 costs three flops per row, $3(n-1)$. The total is $8n - 7$ flops, in every case. With the factors stored, a further right side costs $5n - 4$. The algorithm reads each of the $4n$ input numbers once and writes $n$, so it does about $1.6$ flops per number moved; its speed is set by memory bandwidth, and each step depends on the previous one, so a single system cannot use vector units or several cores. Many independent systems (as in ADI methods or batched spline fitting) are vectorized across the systems instead. The extra storage is $\Theta(n)$ for $u$ and $y$, and both can overwrite $b$ and $d$.

## Properties

- **Linear time**, $8n - 7$ flops, no fill.
- **No pivoting**, so the factorization keeps the tridiagonal structure; breakdown is possible on matrices that need row swaps.
- **Componentwise backward stable** on diagonally dominant, symmetric positive definite, M-matrix and totally nonnegative tridiagonal matrices; the constant $f(u)$ does not depend on $n$.
- **Strictly sequential**: the recurrence in $u_i$ is a continued fraction and the dependency chain has length $n$.
- **Determinant for free**: $\det A = u_1 u_2 \cdots u_n$.

## Variants and improvements

- **With partial pivoting.** LAPACK `xGTSV` swaps rows when $|a_{i}| > |u_{i-1}|$; $U$ then gets a second superdiagonal and the cost rises slightly. The [growth factor](/growth-factor/) of tridiagonal partial pivoting is at most $2$ (see [tridiagonal system solving](/tridiagonal-system-solving/)).
- **Symmetric positive definite case.** Factor $A = L D L^T$ (LAPACK `xPTSV`), using only the diagonal and one off-diagonal, with no square roots.
- **Cyclic tridiagonal systems.** Periodic boundary conditions add corner entries $A_{1n}$ and $A_{n1}$. Writing $A = T' + u v^T$ with a modified tridiagonal $T'$, the [Sherman-Morrison formula](/sherman-morrison-formula/) solves it with two Thomas solves, about $17n$ flops; the implementation includes this.
- **Block tridiagonal systems.** The same recurrences with matrix blocks, $U_i = B_i - A_i U_{i-1}^{-1} C_{i-1}$, solve block tridiagonal systems from two-dimensional problems; stability then needs block diagonal dominance.
- **Parallel algorithms.** [Cyclic reduction](/cyclic-reduction/) and recursive doubling solve in $O(\log n)$ parallel steps with about twice the flops; partition methods and SPIKE split the matrix into blocks solved independently and couple them through a small reduced system.

## When to use it

Use it for tridiagonal systems that are diagonally dominant, symmetric positive definite or M-matrices: discretized second-order boundary value problems, implicit time steps for the heat equation, ADI sweeps, cubic spline interpolation and the inner solves of line relaxation. For a general tridiagonal matrix use the pivoted version, and for many systems on parallel hardware use cyclic reduction or a partition method.

## Pitfalls

- **Zero or tiny pivots.** $A = \begin{pmatrix} 0 & 1 \\ 1 & 0 \end{pmatrix}$ is perfectly conditioned but has $u_1 = 0$. For $A = \begin{pmatrix} 10^{-17} & 1 \\ 1 & 1 \end{pmatrix}$ and $d = (1, 2)^T$, the computed solution is $(0, 1)$ instead of about $(1, 1)$: $|\hat L|\,|\hat U|$ has entries near $10^{17}$, and the backward error bound, still valid, is useless.
- **Index conventions.** Codes differ on whether $a_1$ or $a_n$ is the unused entry, and an off-by-one shift of the subdiagonal silently solves a different system.
- **Testing for singularity.** A zero pivot means a zero leading minor, not a singular matrix; only $u_n = 0$ (with all earlier pivots nonzero) means $A$ is singular.
- **Overflow in long recurrences.** For non-dominant matrices the pivots can grow or decay geometrically, so $\det A$ computed as a product may overflow even when $x$ is fine.
- **Assuming that diagonal dominance holds after discretization.** Convection-dominated finite differences can lose dominance (for large cell Péclet numbers), and then the pivots may change sign or become small.

## Implementations

## History

The method appears in a 1949 report of L. H. Thomas at the Watson Scientific Computing Laboratory on elliptic difference equations, and it was used for the implicit sweeps of the alternating direction methods of Peaceman and Rachford (1955); in the Russian literature it is the "sweep method" (progonka). It is Gaussian elimination, and its error analysis is a special case of Wilkinson's; the sharp constant $f(u)$ and the classes of matrices for which it is componentwise stable are in Higham (Section 9.6).

## References
