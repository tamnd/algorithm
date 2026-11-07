---
tag: XY7DX3
kind: algorithm
slug: lup-solve
name: LUP-SOLVE
aliases:
- LU solve
- solving with an LU factorization
- forward and back substitution
area: numerical/linear-systems
level: core
summary: Solves a linear system given its LUP decomposition by forward substitution followed by back substitution.
solves: [linear-system-solving]
model: floating-point-model
complexity:
  vars: {n: "the order of A, at least 1"}
  time: {worst: Θ(n^2), best: Θ(n^2)}
  space: {extra: Θ(n)}
  flops: {worst: "2n^2 - n"}
properties: {deterministic: true, in_place: false, recursive: false}
prereqs: [lup-decomposition, triangular-system-solving]
see_also: [back-substitution, iterative-refinement, residual, hagers-condition-estimator, cholesky-decomposition, linear-system-solving, growth-factor, partial-pivoting]
sources:
  - book: isbn:9780898715217
    title: Nicholas J. Higham, Accuracy and Stability of Numerical Algorithms, second edition, SIAM, 2002
    locator: Chapter 9, LU Factorization and Linear Equations (Section 9.3, Theorem 9.4, the backward error of the solution; Section 9.4, the normwise bound with the growth factor); Chapter 8, Lemma 8.4 and Theorem 8.5 (substitution); Lemma 3.3 (the rules for combining the γ constants)
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Section 28.1, Solving systems of linear equations (the procedure LUP-SOLVE and its Θ(n^2) running time)
  - book: isbn:9781421407944
    title: Gene H. Golub and Charles F. Van Loan, Matrix Computations, fourth edition, Johns Hopkins University Press, 2013
    locator: Section 3.1, Triangular Systems; Section 3.4, Pivoting (solving with the factors of P A = L U); Section 3.5, Improving and Estimating Accuracy
  - book: isbn:9780898713619
    title: Lloyd N. Trefethen and David Bau III, Numerical Linear Algebra, SIAM, 1997
    locator: Lecture 21, Pivoting; Lecture 22, Stability of Gaussian Elimination (the backward stability of the solve, up to the growth factor)
---

LUP-SOLVE solves $A x = b$ when the factors of $P A = L U$ from the [LUP decomposition](/lup-decomposition/) are known. It permutes $b$, solves $L y = P b$ by forward substitution and $U x = y$ by back substitution, in $2n^2 - n$ flops. Since the factorization costs $2n^3/3$ flops and the solve only $2n^2$, one factorization serves many right sides. The computed solution is the exact solution of $(A + \Delta A)\hat x = b$ with $|\Delta A| \le \gamma_{3n} P^T |\hat L|\,|\hat U|$, which makes the whole method backward stable when the [growth factor](/growth-factor/) is modest.

## In plain words

After the factorization, the hard work is done. The swaps of the rows are recorded, so first you put the entries of the right side in the same order. Then the lower triangle gives a staircase of equations that you solve from the top, one unknown at a time. The upper triangle gives a second staircase that you solve from the bottom. The answer of the second staircase is the answer of the original system.

Each staircase costs about one multiplication and one subtraction for each entry of its triangle, so the solve is cheaper than the factorization by a factor of about the number of unknowns. The rounding errors of the two staircases are of the same size as those of the factorization, so they add almost nothing to its error.

## The problem

**Notation.** As in [solving linear systems](/linear-system-solving/): $A$ is $n \times n$ and nonsingular, $b \in \mathbb{R}^n$, $x$ the exact and $\hat x$ the computed solution, $u$ the unit roundoff, $\gamma_n = n u/(1 - n u)$. The input is the output of [LUP decomposition](/lup-decomposition/): an array that holds the unit lower triangular $L$ below its diagonal and the upper triangular $U$ on and above it, and a permutation $\pi$ such that row $i$ of $P A$ is row $\pi_i$ of $A$. Output: $x$ with $L U x = P b$, which is $A x = b$, or the report that $U$ is singular.

## The algorithm

```pseudo id=main
LUP-SOLVE(L, U, π, b)                      ▷ P A = L U, row i of P A is row π_i of A
L1  for i ← 1 to n do
L2      y_i ← b_{π_i} − Σ_{j=1}^{i−1} l_ij · y_j          ▷ L y = P b, no division: l_ii = 1
L3  for i ← n downto 1 do
L4      x_i ← (y_i − Σ_{j=i+1}^{n} u_ij · x_j) / u_ii       ▷ U x = y
L5  return x
```

Lines L1 and L2 are forward substitution with the unit lower triangular $L$, applied to the permuted right side; the permutation is applied while reading $b$, so no copy of $P b$ is made. Lines L3 and L4 are [back substitution](/back-substitution/) with $U$. An implementation tests $u_{ii} \ne 0$ before the division of line L4; after a successful LUP decomposition every $u_{ii}$ is nonzero.

## Example

Take the factors of $A = \begin{pmatrix} 2 & 1 & 1 \\ 4 & 3 & 3 \\ 8 & 7 & 9 \end{pmatrix}$ from the page [LUP decomposition](/lup-decomposition/): $\pi = (3, 1, 2)$, $L = \begin{pmatrix} 1 & 0 & 0 \\ \tfrac14 & 1 & 0 \\ \tfrac12 & \tfrac23 & 1 \end{pmatrix}$, $U = \begin{pmatrix} 8 & 7 & 9 \\ 0 & -\tfrac34 & -\tfrac54 \\ 0 & 0 & -\tfrac23 \end{pmatrix}$, and let $b = (4, 10, 24)^T$, so that $P b = (24, 4, 10)^T$.

| line | $i$ | computation | value |
|---|---|---|---|
| L2 | 1 | $b_3$ | $y_1 = 24$ |
| L2 | 2 | $b_1 - \tfrac14 \cdot 24$ | $y_2 = -2$ |
| L2 | 3 | $b_2 - \tfrac12 \cdot 24 - \tfrac23 \cdot (-2)$ | $y_3 = -\tfrac23$ |
| L4 | 3 | $(-\tfrac23)/(-\tfrac23)$ | $x_3 = 1$ |
| L4 | 2 | $(-2 - (-\tfrac54) \cdot 1)/(-\tfrac34)$ | $x_2 = 1$ |
| L4 | 1 | $(24 - 7 \cdot 1 - 9 \cdot 1)/8$ | $x_1 = 1$ |

So $x = (1, 1, 1)^T$, and indeed $A (1, 1, 1)^T = (4, 10, 24)^T$. In binary64 the computed factors hold rounded values of $\pm\tfrac23$, and the computed $\hat x$ is still exactly $(1, 1, 1)^T$ for this $b$.

## Correctness

**Exact arithmetic.** Lines L1 and L2 compute the unique $y$ with $L y = P b$, because row $i$ of $L y = P b$ reads $y_i + \sum_{j<i} l_{ij} y_j = b_{\pi_i}$, and $y_1, \ldots, y_{i-1}$ are known when $y_i$ is computed. Lines L3 and L4 compute the unique $x$ with $U x = y$ in the same way from the bottom. Then $P A x = L U x = L y = P b$, and $P$ is invertible, so $A x = b$.

**Backward error (proved).** Assume the [standard model](/floating-point-model/) and $3 n u < 1$, and let $\hat L$, $\hat U$ be the computed factors, with $\hat L \hat U = P A + \Delta A_1$, $|\Delta A_1| \le \gamma_n |\hat L|\,|\hat U|$. Then the computed $\hat x$ satisfies

$$(A + \Delta A)\hat x = b, \qquad |\Delta A| \le \gamma_{3n}\, P^T |\hat L|\,|\hat U|$$

(Higham, Theorem 9.4). The proof combines the bound of the factorization with the bound $|\Delta T| \le \gamma_n |T|$ for each substitution and the rule $3\gamma_n + \gamma_n^2 \le \gamma_{3n}$; it is in [the proof](proofs/correctness.md). With partial pivoting, the argument of the LUP page gives $\|\Delta A\|_\infty \le n^2 \gamma_{3n} \rho_n \|A\|_\infty$. So the normwise backward error $\eta(\hat x) = \|r\|_\infty/(\|A\|_\infty \|\hat x\|_\infty + \|b\|_\infty)$ of the [residual](/residual/) $r = b - A\hat x$ is at most $n^2 \gamma_{3n} \rho_n$, a worst-case bound. In practice $\eta(\hat x)$ is a small multiple of $u$: in 500 random systems of order 1 to 6 with entries uniform in $[-1, 1]$, generated by `random.Random(99)`, it never exceeded $4 n u$.

**Forward error.** If $\varepsilon \kappa(A) < 1$ for the backward error $\varepsilon$, then $\|x - \hat x\|/\|x\| \le 2\varepsilon\kappa(A)/(1 - \varepsilon\kappa(A))$ (Higham, Theorem 7.2). So the forward error of a backward stable solve is about $\kappa(A) u$, and it is large for an ill-conditioned $A$, as the [Hilbert matrix](/hilbert-matrix/) example on the page [residual](/residual/) shows.

## Complexity

Line L2 for row $i$ does $i - 1$ multiplications and $i - 1$ subtractions: $n(n-1)$ flops in all. Line L4 for row $i$ does $n - i$ multiplications, $n - i$ subtractions and one division: $n(n-1) + n$ flops. The total is $2n^2 - n$ flops, in each case. The extra space is the vectors $y$ and $x$, $\Theta(n)$; $y$ can overwrite $x$. For $k$ right sides, the cost is $k(2n^2 - n)$ flops, and the blocked form (`xGETRS` calls `xTRSM`) does it as matrix-matrix work. A solve reads each entry of the factors once, so for one right side it does about two flops for each word read from memory, and memory bandwidth, not the flop rate, limits its speed.

## Properties

- **One factorization, many solves.** The $2n^3/3$ flops of the factorization are paid once.
- **The same backward error as the factorization**, up to the constant: $\gamma_{3n}$ instead of $\gamma_n$.
- **Transposed systems.** $A^T x = b$ is solved with the same factors: $U^T z = b$, then $L^T w = z$, then $x = P^T w$. The condition estimator uses this.
- **Componentwise view.** The bound is in terms of $|\hat L|\,|\hat U|$, which can be much larger than $|A|$ when the growth is large; when $|\hat L|\,|\hat U| \approx |P A|$, the solve is componentwise backward stable.

## Variants and improvements

- **[Iterative refinement](/iterative-refinement/).** Compute $r = b - A\hat x$, solve $A d = r$ with the same factors, and set $\hat x \leftarrow \hat x + d$. With $r$ in working precision, one step usually makes the solve componentwise backward stable; with $r$ in higher precision, the forward error drops to about $u$ while $\kappa(A) u$ is well below $1$.
- **Condition estimation.** [Hager's estimator](/hagers-condition-estimator/) uses a few solves with $A$ and $A^T$ to estimate $\|A^{-1}\|_1$ in $O(n^2)$ flops.
- **Cholesky solve.** For $A = R^T R$ the same two substitutions apply, with $L = R^T$ and no permutation.
- **Sparse solve.** With sparse factors, each substitution costs time proportional to the nonzeros of the factor, or less when $b$ is sparse (Davis, Chapter 3).

## When to use it

Use LUP-SOLVE after each LUP decomposition: to solve one or many systems, to refine a solution, and to estimate a condition number. Do not compute $A^{-1}$ and multiply: that costs $2n^3$ flops instead of $2n^3/3$ for the factorization plus $2n^2$ for each solve, and its error bound for $\hat x$ is weaker. For a symmetric positive definite matrix, use the [Cholesky](/cholesky-decomposition/) solve instead, and for a least squares problem the QR solve.

## Pitfalls

- **Forgetting the permutation.** Line L2 reads $b_{\pi_i}$, not $b_i$. Solving $L y = b$ gives the solution of a system with permuted equations.
- **Applying $\pi$ the wrong way.** If the factorization stores the permutation as "row $i$ of $A$ goes to position $\pi_i$" (the inverse convention), line L2 must read $b$ through $\pi^{-1}$. The two conventions agree only for involutions, so a test with a single swap does not catch the mix-up; test with a 3-cycle, as in the example.
- **Dividing by $l_{ii}$.** $L$ is unit lower triangular, and its diagonal is not stored: the array holds $u_{ii}$ there. Dividing by the stored diagonal at line L2 uses $u_{ii}$ by mistake.
- **Trusting a tiny residual as an accurate answer.** A backward stable solve has a small residual even when $\hat x$ has no correct digits; estimate $\kappa(A)$ to judge the error.

## Implementations

## History

Solving with the triangular factors is as old as the factorization; the analysis of its rounding errors, with the backward error bound in terms of $|L|\,|U|$, is part of Wilkinson's work of the early 1960s, in the form given by Higham (Section 9.3). The name LUP-SOLVE is that of Cormen, Leiserson, Rivest and Stein.

## References
