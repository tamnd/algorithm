---
tag: 44KZ70
kind: algorithm
slug: levinson-durbin-algorithm
name: Levinson-Durbin algorithm
aliases: [Levinson recursion, Levinson algorithm, exact Levinson-Durbin recursion, Levinson-Trench-Zohar algorithm]
area: algebra/exact-linear-algebra
level: advanced
summary: Solves Toeplitz systems in quadratic time by recursively extending the solution order by order.
solves: [toeplitz-system-solving]
model: algebraic-computation-tree
complexity:
  vars: {n: the size of the Toeplitz matrix, b: the maximum binary length of an entry of an integer input}
  time: {worst: Θ(n^2)}
  space: {extra: Θ(n)}
  field_operations: {worst: 7n^2 + O(n)}
  bit_operations: {worst: O(n^4 (b + log n)^2)}
properties: {deterministic: true, in_place: false, recursive: false}
prereqs: [toeplitz-system-solving, linear-system-solving]
see_also: [levinson-durbin-recursion, berlekamp-massey, pade-approximation, lu-decomposition, cramers-rule, hadamard-bound, linear-prediction, half-gcd]
sources:
  - book: isbn:9781421407944
    title: Gene H. Golub and Charles F. Van Loan, Matrix Computations, fourth edition, Johns Hopkins University Press, 2013
    locator: Section 4.7, Classical Methods for Toeplitz Systems (Durbin's algorithm for the Yule-Walker equations, Levinson's algorithm for a general right-hand side, Trench's algorithm for the inverse, and the nonsymmetric case)
  - paper: "Norman Levinson, The Wiener RMS (root mean square) error criterion in filter design and prediction, Journal of Mathematics and Physics 25, 1947"
    locator: pp. 261 to 278 (the order-recursive solution of symmetric Toeplitz systems with O(n^2) operations)
  - paper: "James Durbin, The fitting of time-series models, Revue de l'Institut International de Statistique 28(3), 1960"
    locator: pp. 233 to 244 (the recursion for the Yule-Walker equations of autoregressive models)
  - paper: "William F. Trench, An algorithm for the inversion of finite Toeplitz matrices, Journal of the Society for Industrial and Applied Mathematics 12(3), 1964"
    locator: pp. 515 to 522 (the inverse of a Toeplitz matrix with nonzero leading minors in O(n^2) operations)
  - paper: "Shalhav Zohar, The solution of a Toeplitz set of linear equations, Journal of the ACM 21(2), 1974"
    locator: pp. 272 to 276 (the nonsymmetric recursion with forward and backward vectors)
  - paper: doi:10.1016/0196-6774(80)90013-9
    title: Richard P. Brent, Fred G. Gustavson and David Y. Y. Yun, Fast solution of Toeplitz systems of equations and computation of Pade approximants, Journal of Algorithms 1(3), 1980
    locator: pp. 259 to 295 (the superfast alternative with no condition on the leading minors)
---

The Levinson-Durbin algorithm solves a Toeplitz system $T x = c$, where $T_{ij} = t_{i - j}$ is constant along diagonals, in $O(n^2)$ field operations instead of the $O(n^3)$ of [Gaussian elimination](/gaussian-elimination/). It solves the leading $1 \times 1$, $2 \times 2$, $\ldots$ subsystems in turn and extends each solution to the next size with a few inner products, using a forward and a backward vector that solve $T_k f = e_1$ and $T_k g = e_k$. This page treats the exact, nonsymmetric version over any field, such as $\mathbb{Q}$ or $\mathbb{Z}/p\mathbb{Z}$. It needs every leading principal minor of $T$ to be nonzero, and it detects when one is zero. The floating-point version for symmetric positive definite matrices is the [numerical Levinson-Durbin recursion](/levinson-durbin-recursion/).

## In plain words

A Toeplitz table repeats the same numbers along each diagonal, so the top-left corner of size $k + 1$ contains the corner of size $k$, plus one new row and one new column made of numbers already known. The method solves the equations for the smallest corner first and then grows the solution one size at a time.

To grow it cheaply, the method keeps two helper solutions: one whose answer is a one at the top, and one whose answer is a one at the bottom. Because of the diagonal pattern, the helpers for the next size are simple mixtures of the current helpers, shifted by one place, and the real solution is corrected with the bottom helper. Each step costs a few sums of length $k$, so the whole run is quadratic.

## The problem

**Notation.** $K$ is a field given exactly. Indices start at $0$. $T = (t_{i - j})_{0 \le i, j < n}$ is an $n \times n$ Toeplitz matrix over $K$, given by $t_{-(n-1)}, \ldots, t_{n-1}$, and $c = (c_0, \ldots, c_{n-1})$. $T_k$ is the leading $k \times k$ submatrix, which is again Toeplitz, $\Delta_k = \det T_k$ with $\Delta_0 = 1$, and $e_1$, $e_k$ are the first and last unit vectors of $K^k$. For an integer input, $b$ is the maximum binary length of the $t_i$ and $c_i$. Costs are given in *field operations* (the algebraic computation tree model) and in *bit operations* over $\mathbb{Q}$ with schoolbook arithmetic.

**Input.** The entries $t_{-(n-1)}, \ldots, t_{n-1}$ and the vector $c$.

**Output.** The solution $x$ of $T x = c$, provided $\Delta_1, \ldots, \Delta_n$ are all nonzero (*strongly nonsingular* $T$); otherwise the report that some leading principal minor is zero.

## The algorithm

For a vector $f$ of length $k$, $(f, 0)$ and $(0, f)$ are the vectors of length $k + 1$ with a zero appended or prepended.

```pseudo id=main
LEVINSON(t, c)                         ▷ T = (t_{i−j}) is n × n over a field K
L1  if n = 0 then return ()
L2  if t_0 = 0 then fail "Δ_1 = 0"
L3  f ← (1/t_0); g ← (1/t_0); x ← (c_0/t_0)
L4  for k ← 1 to n − 1 do                ▷ here T_k f = e_1, T_k g = e_k, T_k x = c[0..k−1]
L5      ε_f ← Σ_{j<k} t_{k−j} f_j;  ε_g ← Σ_{j<k} t_{−1−j} g_j;  ε_x ← Σ_{j<k} t_{k−j} x_j
L6      d ← 1 − ε_f ε_g; if d = 0 then fail "Δ_{k+1} = 0"
L7      (f, g) ← ( ((f, 0) − ε_f (0, g)) / d,  ((0, g) − ε_g (f, 0)) / d )
L8      x ← (x, 0) + (c_k − ε_x) g
L9  return x
```

Line L5 computes what the new last row or new first row of $T_{k+1}$ gives on the padded vectors: $T_{k+1} (f, 0) = (e_1, \varepsilon_f)$, $T_{k+1} (0, g) = (\varepsilon_g, e_k)$, and $T_{k+1} (x, 0) = (c_0, \ldots, c_{k-1}, \varepsilon_x)$. Line L7 combines the two padded helpers so that the stray entries cancel; both new helpers use the old $f$ and $g$, so they are computed together. Line L8 adds the multiple of the new backward vector that fixes the last equation. The quantity $d$ equals $\Delta_{k-1} \Delta_{k+1} / \Delta_k^2$, so it is zero exactly when $\Delta_{k+1}$ is.

## Example

Solve over $\mathbb{Q}$, with $t_0 = 2$, $t_1 = 1$, $t_2 = 3$, $t_{-1} = -1$, $t_{-2} = 1$:

$$T = \begin{pmatrix} 2 & -1 & 1 \\ 1 & 2 & -1 \\ 3 & 1 & 2 \end{pmatrix}, \qquad c = \begin{pmatrix} 5 \\ -3 \\ 6 \end{pmatrix}.$$

The leading minors are $\Delta_1 = 2$, $\Delta_2 = 5$, $\Delta_3 = 10$.

| step | $\varepsilon_f$, $\varepsilon_g$, $\varepsilon_x$ | $d$ | $f$ | $g$ | $x$ |
|---|---|---|---|---|---|
| L3 | | | $(\tfrac12)$ | $(\tfrac12)$ | $(\tfrac52)$ |
| $k = 1$ | $\tfrac12$, $-\tfrac12$, $\tfrac52$ | $\tfrac54$ | $(\tfrac25, -\tfrac15)$ | $(\tfrac15, \tfrac25)$ | $(\tfrac75, -\tfrac{11}5)$ |
| $k = 2$ | $1$, $\tfrac15$, $2$ | $\tfrac45$ | $(\tfrac12, -\tfrac12, -\tfrac12)$ | $(-\tfrac1{10}, \tfrac3{10}, \tfrac12)$ | $(1, -1, 2)$ |

At $k = 1$, $c_1 - \varepsilon_x = -3 - \tfrac52 = -\tfrac{11}2$, and $x = (\tfrac52, 0) - \tfrac{11}2 (\tfrac15, \tfrac25)$. At $k = 2$, $c_2 - \varepsilon_x = 4$ and $x = (\tfrac75, -\tfrac{11}5, 0) + 4 g = (1, -1, 2)$, which satisfies $T x = c$. The values of $d$ agree with $\Delta_{k-1} \Delta_{k+1} / \Delta_k^2$: $1 \cdot 5 / 4$ and $2 \cdot 10 / 25$. The last entry of the final $g$ is $(T^{-1})_{2, 2} = \Delta_2 / \Delta_3 = \tfrac12$.

## Correctness

The invariant at the test of line L4 for a given $k$ is $T_k f = e_1$, $T_k g = e_k$ and $T_k x = (c_0, \ldots, c_{k-1})$. Line L3 makes it true for $k = 1$. If it holds for $k$, the identities after the pseudocode give

$$T_{k+1} \frac{(f, 0) - \varepsilon_f (0, g)}{d} = \frac{(1 - \varepsilon_f \varepsilon_g) e_1}{d} = e_1, \qquad T_{k+1} \frac{(0, g) - \varepsilon_g (f, 0)}{d} = e_{k+1},$$

and then $T_{k+1} ((x, 0) + (c_k - \varepsilon_x) g') = (c_0, \ldots, c_{k-1}, \varepsilon_x) + (c_k - \varepsilon_x) e_{k+1} = (c_0, \ldots, c_k)$. So the invariant holds for $k + 1$, and at the end $T x = c$. For the failure test, Cramer's rule gives $g_{k-1} = \Delta_{k-1} / \Delta_k$ for the last entry of the backward vector, and the last entry of the new backward vector is $g_{k-1} / d$, so $d = \Delta_{k-1} \Delta_{k+1} / \Delta_k^2$. Hence, while $\Delta_1, \ldots, \Delta_k \ne 0$, $d = 0$ exactly when $\Delta_{k+1} = 0$, and the algorithm fails exactly when some leading minor vanishes. The [full proof](proofs/correctness.md) gives the details.

## Complexity

**Field operations.** Step $k$ of the loop computes three inner products of length $k$ on line L5 ($3k$ multiplications), one product on line L6, $2k$ products by $\varepsilon_f$ and $\varepsilon_g$ and $2(k + 1)$ products by $1/d$ on line L7, and $k + 1$ products on line L8: $8k + 4$ multiplications, one division and about $6k$ additions. Summed over $k = 1, \ldots, n - 1$, this is $4 n^2 + O(n)$ multiplications, $n$ divisions and $3 n^2 + O(n)$ additions and subtractions, so $7 n^2 + O(n)$ field operations in the worst case, which happens whenever the algorithm does not fail. These counts are exact, and the bound $\Theta(n^2)$ is proved. For comparison, an LU decomposition of $T$ costs $\tfrac23 n^3 + O(n^2)$.

**Bit operations over $\mathbb{Q}$.** Let $T$ and $c$ have integer entries of binary length at most $b$. By Cramer's rule every entry of $f$, $g$ and $x$ after step $k$ is a quotient of two minors of order at most $k + 1$ of the matrix $(T \mid c)$, with denominator $\Delta_{k+1}$, and $\varepsilon_f$, $\varepsilon_g$, $\varepsilon_x$ and $d$ are quotients of minors in the same way. By the [Hadamard bound](/hadamard-bound/), each such minor has at most $n (b + \tfrac12 \log_2 n)$ binary digits. So each of the $O(n^2)$ field operations works on fractions of $O(n (b + \log n))$ digits and costs $O(n^2 (b + \log n)^2)$ bit operations with schoolbook multiplication and gcd, and the total is $O(n^4 (b + \log n)^2)$. This bound is proved. Without reducing the fractions, the numerators can grow much faster; a fraction-free variant keeps the numerators as minors, in the spirit of the [Bareiss algorithm](/bareiss-algorithm/).

**Over $\mathbb{Z}/p\mathbb{Z}$.** The same $7 n^2 + O(n)$ operations, each costing $O(\log^2 p)$ bit operations, with no growth of numbers.

**Space.** The vectors $f$, $g$ and $x$, so $\Theta(n)$ field elements beyond the $2n - 1$ input entries and $c$.

## Properties

- **Strong nonsingularity is required.** The algorithm fails on nonsingular matrices with a zero leading minor, such as $\begin{pmatrix} 0 & 1 \\ 1 & 0 \end{pmatrix}$.
- **By-products.** The final $f$ and $g$ are the first and last columns of $T^{-1}$, which by the Gohberg-Semencul formula determine all of $T^{-1}$. The quantities $d$ give all the leading minors: $\Delta_{k+1} = d \Delta_k^2 / \Delta_{k-1}$, so $\det T$ comes for free.
- **All sizes at once.** The solution of every leading subsystem $T_k x = c[0..k-1]$ appears on the way, which is what order-recursive model fitting uses.
- **Deterministic and exact.** Over $\mathbb{Q}$ or $\mathbb{Z}/p\mathbb{Z}$ the answer is exactly right whenever the algorithm does not fail.

## Variants and improvements

- **Symmetric matrices.** If $t_{-i} = t_i$, then $g$ is $f$ reversed, so the backward vector and $\varepsilon_g$ need not be computed. Durbin's form solves the Yule-Walker equations $T y = -(t_1, \ldots, t_n)$ with only the forward recursion, and its coefficients $\varepsilon_f$ are the reflection (partial correlation) coefficients.
- **Trench's algorithm.** Computes all of $T^{-1}$ in $O(n^2)$ from $f$ and $g$.
- **Look-ahead.** When $d = 0$ but $T$ is nonsingular, jump over the singular leading block to the next nonsingular leading minor; this handles every nonsingular $T$ at a cost that depends on the jumps.
- **Schur algorithm.** Computes the reflection coefficients and an LU factorization of $T$ in $O(n^2)$ without inner products, which parallelizes better.
- **Superfast algorithms.** Divide and conquer through the extended Euclidean algorithm and Pade approximation gives $O(n \log^2 n)$ field operations, with no condition on the leading minors (Brent, Gustavson and Yun, 1980); see [Toeplitz system solving](/toeplitz-system-solving/).
- **Hankel systems.** Reversing the rows turns a Hankel system into a Toeplitz one; the analogous recursion on Hankel matrices is closely related to [Berlekamp-Massey](/berlekamp-massey/).
- **Modular and fraction-free.** Over $\mathbb{Z}$, run the recursion modulo several primes and reconstruct with the [Chinese remainder theorem](/chinese-remainder-theorem/), or keep integer numerators and divide exactly.

## When to use it

Use it for exact Toeplitz systems of moderate size whose leading minors are nonzero, for example symmetric positive definite matrices from autocorrelations, or matrices over a large finite field after a random preconditioning. It is simple, needs $O(n)$ memory, and gives the leading minors and the first and last columns of the inverse along the way. For very large $n$, the superfast $O(n \log^2 n)$ methods win; for a matrix with zero leading minors use a look-ahead variant or the Euclidean approach; for a single small system, elimination is simpler.

## Pitfalls

- **Assuming nonsingular is enough.** $T$ can be nonsingular while $\Delta_k = 0$ for some $k < n$, and then line L6 fails. Over a small finite field this is common: for random $2 \times 2$ Toeplitz matrices over $\mathbb{F}_2$, $t_0 = 0$ half of the time.
- **Updating $f$ before $g$.** Line L7 must use the old $f$ in the new $g$ and the old $g$ in the new $f$; updating in place in sequence gives wrong vectors.
- **Mixing up $t_{k - j}$ and $t_{j - k}$.** $\varepsilon_f$ and $\varepsilon_x$ come from the new last row (indices $t_k, \ldots, t_1$), and $\varepsilon_g$ from the new first row (indices $t_{-1}, \ldots, t_{-k}$). Swapping them makes the recursion work on the wrong matrix, and the result does not solve $T x = c$.
- **Floating point for exact data.** Over $\mathbb{R}$ the recursion is only weakly stable even for positive definite matrices (Cybenko, 1980), and for indefinite matrices it can be unstable; exact arithmetic avoids this.

## Implementations

## History

Norman Levinson gave the recursion in 1947 for the symmetric Toeplitz systems of Wiener's filtering and prediction theory, and James Durbin gave the form for the Yule-Walker equations of autoregressive models in 1960. William Trench extended it to the inverse in 1964, and Shalhav Zohar treated the nonsymmetric case in detail in 1974. In 1980 Brent, Gustavson and Yun connected Toeplitz systems with Pade approximation and the Euclidean algorithm, which gave the first algorithms in $O(n \log^2 n)$ field operations.

## References
