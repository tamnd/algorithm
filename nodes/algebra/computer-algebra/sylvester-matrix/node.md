---
tag: NEATH6
kind: data-structure
slug: sylvester-matrix
name: Sylvester matrix
aliases: [Sylvester's matrix, Sylvester resultant matrix, eliminant matrix]
area: algebra/computer-algebra
level: core
summary: Matrix of coefficients of two polynomials whose determinant is their resultant.
model: blum-shub-smale-machine
complexity:
  vars: {m: the formal degree of f, n: the formal degree of g}
  time: {worst: O((m+n)^3)}
  space: {extra: O((m+n)^2)}
prereqs: [polynomial, determinant, bareiss-algorithm]
see_also: [resultant, subresultant, subresultant-prs, subresultant-gcd, discriminant, polynomial-extended-euclidean-algorithm, hadamard-bound, toeplitz-system-solving]
sources:
  - book: isbn:9781107039032
    title: Joachim von zur Gathen and Jürgen Gerhard, Modern Computer Algebra, third edition, Cambridge University Press, 2013
    locator: Section 6.3, The resultant (the Sylvester matrix as the matrix of the map (s, t) to s f + t g, and the gcd criterion); Chapter 11 for the fast Euclidean algorithm and fast resultants
  - book: isbn:9780792392590
    title: Keith O. Geddes, Stephen R. Czapor and George Labahn, Algorithms for Computer Algebra, Kluwer, 1992
    locator: Chapter 7, Polynomial GCD Computation (the Sylvester matrix, resultants and subresultants)
  - book: isbn:9783540330981
    title: Saugata Basu, Richard Pollack and Marie-Françoise Roy, Algorithms in Real Algebraic Geometry, second edition, Springer, 2006
    locator: Chapter 4, Algebra (the Sylvester matrix, resultants and subresultants)
  - paper: doi:10.1080/14786444008649995
    title: J. J. Sylvester, A method of determining by mere inspection the derivatives from two equations of any degree, Philosophical Magazine 16, 1840
    locator: pp. 132 to 135
  - paper: doi:10.1090/S0025-5718-1968-0226829-0
    title: Erwin H. Bareiss, Sylvester's identity and multistep integer-preserving Gaussian elimination, Mathematics of Computation 22, 1968
    locator: pp. 565 to 578
---

The Sylvester matrix of two polynomials $f$ and $g$ of formal degrees $m$ and $n$ is the $(m + n) \times (m + n)$ matrix whose rows are the coefficient vectors of $x^{n-1} f, \ldots, x f, f$ and $x^{m-1} g, \ldots, x g, g$. It is the matrix of the linear map $(s, t) \mapsto s f + t g$ on multipliers of degree below $n$ and $m$. Its determinant is the [resultant](/resultant/) of $f$ and $g$, its rank tells the degree of $\gcd(f, g)$, and its submatrices give the [subresultants](/subresultant/). The matrix is fully set by $m + n + 2$ coefficients, so a good representation stores only those and computes each entry when it is needed.

## In plain words

Take two polynomials in one variable. Write the numbers of the first one in a row, then write the same row again shifted one place to the right, and do this as many times as the degree of the second polynomial. Then do the same with the second polynomial, as many times as the degree of the first. Fill the empty places with zeros. The result is a square table of numbers.

This table answers questions about the two polynomials with plain linear algebra. Its determinant is zero exactly when the two polynomials have a common factor. The number of independent rows tells how large that common factor is. And multiplying the table by a row of numbers is the same as forming a combination of the two polynomials. Because the table is only shifted copies of two short lists, there is no need to store it in full.

## The abstract type

The structure is a read-only matrix with the Sylvester pattern. $R$ is a commutative ring, an integral domain with exact division when determinants are computed (such as $\mathbb{Z}$, $\mathbb{Q}$, $\mathbb{Z}/p\mathbb{Z}$ or $K[y]$). The operations are

- `entry(r, c)`: the entry in row $r$ and column $c$;
- `combine(s, t)`: the row vector $(s, t)$ times the matrix, that is the coefficients of $s f + t g$;
- `determinant()`: $\det \operatorname{Syl}(f, g) = \operatorname{Res}_{m,n}(f, g)$;
- `rank()`: the rank over the field of fractions of $R$;
- `to_dense()`: the full matrix.

Costs are counted in ring operations of $R$, in the model of the [Blum-Shub-Smale machine](/blum-shub-smale-machine/). Over $\mathbb{Z}$ the bit cost also depends on the size of the numbers, which is discussed under Complexity.

## Representation

Let $f = a_m x^m + \cdots + a_0$ and $g = b_n x^n + \cdots + b_0$ in $R[x]$, given with formal degrees $m, n \ge 0$. The leading coefficients $a_m$ and $b_n$ may be zero; then $m$ and $n$ are only upper bounds for the degrees. The structure stores the two lists $(a_m, \ldots, a_0)$ and $(b_n, \ldots, b_0)$, which is $m + n + 2$ ring elements.

The matrix $\operatorname{Syl}(f, g)$ has $N = m + n$ rows and columns, indexed from 0. Column $c$ stands for the monomial $x^{N - 1 - c}$.

- Row $i$, for $0 \le i < n$, holds the coefficients of $x^{n - 1 - i} f$: the entry in column $c$ is $a_{m - (c - i)}$ when $0 \le c - i \le m$, and $0$ otherwise.
- Row $n + j$, for $0 \le j < m$, holds the coefficients of $x^{m - 1 - j} g$: the entry in column $c$ is $b_{n - (c - j)}$ when $0 \le c - j \le n$, and $0$ otherwise.

**Invariant.** Each row of the first block is the list $(a_m, \ldots, a_0)$ shifted to start at the diagonal, and each row of the second block is $(b_n, \ldots, b_0)$ shifted to start at column $j$. All the other entries are zero. This is the convention of the [resultant](/resultant/) page; some books use the transpose, which has the same determinant.

The matrix is a pair of stacked Toeplitz blocks: in each block, the entry depends only on $c$ minus the row number. Such a matrix has displacement rank at most 2, which is what fast structured solvers use.

## Operations

### Determinant

The main operation is the determinant by [Bareiss elimination](/bareiss-algorithm/), which uses only exact divisions in $R$.

```pseudo id=main
DET(f, g)                    ▷ N = m + n; the result is Res_(m,n)(f, g)
L1  if N = 0 then return 1
L2  A ← the dense matrix of ENTRY(r, c)
L3  sign ← 1; prev ← 1
L4  for k ← 0 to N - 2 do
L5      p ← the first row r ≥ k with A[r][k] ≠ 0
L6      if there is no such row then return 0
L7      if p ≠ k then swap the rows k and p; sign ← -sign
L8      for i ← k + 1 to N - 1 do
L9          for j ← k + 1 to N - 1 do A[i][j] ← (A[i][j] A[k][k] - A[i][k] A[k][j]) / prev   ▷ exact
L10     prev ← A[k][k]
L11 return sign · A[N - 1][N - 1]
```

After step $k$, each entry $A[i][j]$ with $i, j > k$ is a $(k + 2) \times (k + 2)$ minor of the row-permuted matrix, so the division on line L9 is exact in $R$. When $N = 0$, that is $m = n = 0$, the matrix is empty and its determinant is 1 by convention. This gives $\operatorname{Res}(a_0, b_0) = 1$.

### Entry

```pseudo id=entry
ENTRY(r, c)
E1  if r or c is outside 0 .. N - 1 then error
E2  if r < n then                     ▷ a row of x^(n-1-r) f
E3      k ← c - r; return a_(m-k) if 0 ≤ k ≤ m, else 0
E4  k ← c - (r - n); return b_(n-k) if 0 ≤ k ≤ n, else 0
```

### Combination

```pseudo id=combine
COMBINE(s, t)              ▷ s = (s_0 .. s_(n-1)) and t = (t_0 .. t_(m-1)), highest degree first
C1  check |s| = n and |t| = m
C2  out ← N zeros
C3  for each i and k: out[i + k] ← out[i + k] + s_i a_(m-k)
C4  for each j and k: out[j + k] ← out[j + k] + t_j b_(n-k)
C5  return out                        ▷ the coefficients of s f + t g, highest degree first
```

The product of the row vector $(s, t)$ with $\operatorname{Syl}(f, g)$ is $\sum_i s_i \cdot (\text{row } i) + \sum_j t_j \cdot (\text{row } n + j)$, and row $i$ is $x^{n-1-i} f$. So the product is the coefficient vector of $s f + t g$ with $s = \sum_i s_i x^{n-1-i}$ and $t = \sum_j t_j x^{m-1-j}$. COMBINE computes it as two polynomial products, in $O(mn)$ operations, without forming the matrix.

### Rank

`rank()` runs the same fraction-free elimination, but it moves to the next column when a column has no pivot, and it counts the pivots.

## Example

Let $f = x^2 - 3x + 2 = (x - 1)(x - 2)$ and $g = x^2 + 1$, so $m = n = 2$ and

$$\operatorname{Syl}(f, g) = \begin{pmatrix} 1 & -3 & 2 & 0 \\ 0 & 1 & -3 & 2 \\ 1 & 0 & 1 & 0 \\ 0 & 1 & 0 & 1 \end{pmatrix}.$$

The rows are $x f$, $f$, $x g$ and $g$. DET needs no row swap here.

| step $k$ | pivot $A[k][k]$ | rows after the step | prev |
|---|---|---|---|
| start | | $(1, -3, 2, 0)$, $(0, 1, -3, 2)$, $(1, 0, 1, 0)$, $(0, 1, 0, 1)$ | 1 |
| 0 | 1 | $(1, -3, 2, 0)$, $(0, 1, -3, 2)$, $(0, 3, -1, 0)$, $(0, 1, 0, 1)$ | 1 |
| 1 | 1 | $(1, -3, 2, 0)$, $(0, 1, -3, 2)$, $(0, 0, 8, -6)$, $(0, 0, 3, -1)$ | 1 |
| 2 | 8 | $(1, -3, 2, 0)$, $(0, 1, -3, 2)$, $(0, 0, 8, -6)$, $(0, 0, 0, 10)$ | 8 |

The last step computes $A[3][3] = (-1 \cdot 8 - 3 \cdot (-6)) / 1 = 10$, so $\operatorname{Res}(f, g) = 10$. This agrees with the product formula $\operatorname{Res}(f, g) = g(1) \, g(2) = 2 \cdot 5 = 10$ for monic $f$. The rank is 4, so $\gcd(f, g) = 1$.

For $g = x^2 + x - 2 = (x - 1)(x + 2)$ instead, the determinant is 0 and the rank is 3, because the gcd $x - 1$ has degree 1. And COMBINE with $s = x$ and $t = 1 - x$ gives $(0, -2, 1, 1)$, the coefficients of $x f + (1 - x)(x^2 + 1) = -2x^2 + x + 1$.

## Correctness

ENTRY follows the definition of the rows. COMBINE is correct because row $i$ of the matrix is the coefficient vector of $x^{n-1-i} f$ and row $n + j$ is that of $x^{m-1-j} g$, so a row combination is a polynomial combination. DET is correct because Bareiss elimination keeps every working entry equal to a minor of the row-permuted matrix, and the last one is the full determinant. The rank satisfies

$$\operatorname{rank} \operatorname{Syl}(f, g) = m + n - \deg \gcd(f, g)$$

over the field of fractions $F$ of $R$, when $a_m \ne 0$ or $b_n \ne 0$. In particular $\operatorname{Res}(f, g) = 0$ exactly when $f$ and $g$ have a common factor of positive degree. The proof is in the proof file below.

## Complexity

| operation | ring operations | extra space |
|---|---|---|
| store $f$ and $g$ | | $O(m + n)$ |
| `entry` | $O(1)$ | $O(1)$ |
| `combine` | $O(mn)$ | $O(m + n)$ |
| `to_dense` | $O((m + n)^2)$ | $O((m + n)^2)$ |
| `determinant`, `rank` | $O((m + n)^3)$ | $O((m + n)^2)$ |

These bounds are proved for the methods shown. Over $\mathbb{Z}$, every number that Bareiss stores is a minor of $\operatorname{Syl}(f, g)$. By the [Hadamard bound](/hadamard-bound/), each minor has absolute value at most $\|f\|_2^{\,n} \|g\|_2^{\,m}$, so each number has $O(n \log \|f\|_2 + m \log \|g\|_2)$ digits, and the total bit cost is polynomial in the size of the input.

Elimination on the matrix is not the fastest way to get the resultant. Over a field $K$, the [Euclidean algorithm](/polynomial-extended-euclidean-algorithm/) gives $\operatorname{Res}(f, g)$ in $O(mn)$ field operations, and the half-gcd method in $O(M(d) \log d)$ for $d = \max(m, n)$ (von zur Gathen and Gerhard, Chapter 11). Over $\mathbb{Z}$, the [subresultant PRS](/subresultant-prs/) and modular methods are used. The dense matrix is still the clearest definition, and the right tool for small sizes, for a symbolic entry $R = K[y_1, \ldots]$, and for proofs.

## Variants

- **Subresultant matrices.** For $k < \min(m, n)$, keep the first $n - k$ rows of the $f$ block and the first $m - k$ rows of the $g$ block, and drop the last $k$ columns, which are zero in these rows. The determinant of the first $m + n - 2k$ columns is the $k$-th principal subresultant coefficient, and replacing the last of these columns by each later column gives the coefficients of the $k$-th subresultant. See [subresultant](/subresultant/).
- **Bézout matrix.** A $\max(m, n) \times \max(m, n)$ matrix built from $(f(x) g(y) - f(y) g(x)) / (x - y)$. Its determinant equals the resultant up to sign and a power of a leading coefficient, and its size is half that of the Sylvester matrix when $m = n$.
- **Transposed convention.** Many texts write the coefficient vectors as columns. The determinant does not change.
- **Multivariate elimination.** For $f, g \in K[y][x]$, the Sylvester matrix with respect to $x$ has entries in $K[y]$, and its determinant is a polynomial in $y$ that vanishes at the $y$-coordinates of the common zeros. This is the basis of elimination and of the projection step in cylindrical algebraic decomposition.
- **Structured solvers.** The two Toeplitz blocks give displacement rank 2, so linear systems with $\operatorname{Syl}(f, g)$ can be solved by the fast methods for [Toeplitz systems](/toeplitz-system-solving/).
- **The discriminant.** $\operatorname{Syl}(f, f')$ with formal degrees $m$ and $m - 1$ gives the [discriminant](/discriminant/), after division by the leading coefficient and a sign.

## When to use it

Use the Sylvester matrix to define and prove facts about resultants and subresultants, and to compute them for small degrees or with polynomial entries, where a determinant with exact division is simple and safe. Use COMBINE when an algorithm needs the map $(s, t) \mapsto s f + t g$, for example to find Bézout cofactors by linear algebra. For large univariate inputs over a field, compute the resultant by the Euclidean algorithm or the half-gcd method, not by elimination on the matrix.

## Pitfalls

- **Formal degree versus degree.** If both $a_m = 0$ and $b_n = 0$, the first column is zero and the determinant is 0, whether or not $f$ and $g$ have a common factor. When the coefficients are specialized, for example $y \mapsto y_0$, the gcd criterion holds only where a leading coefficient stays nonzero.
- **Sign.** $\operatorname{Res}(g, f) = (-1)^{mn} \operatorname{Res}(f, g)$, because swapping the blocks permutes the rows. Mixing the two orders changes the sign.
- **Division that is not exact.** Bareiss divides by the previous pivot. Over $\mathbb{Z}$ this is exact only if the rows are updated in the order shown; a different update rule, or a floating-point pivot, gives wrong or rounded values.
- **Empty matrix.** For $m = n = 0$ the matrix is $0 \times 0$, and its determinant is 1, not 0. With $m = 0$ and $n > 0$ the matrix is $a_0 I_n$ and the determinant is $a_0^n$.
- **Storing the full matrix.** The dense form uses $(m + n)^2$ entries for $m + n + 2$ numbers of input. Form it only when an elimination needs it.

## Implementations

## History

Sylvester described the matrix in 1840 as a way to eliminate $x$ from two equations "by mere inspection". Resultants of this kind were studied by Euler and Bézout in the eighteenth century, and Bézout's form of the resultant matrix is the other classical construction. Collins, and Brown and Traub, used determinants of submatrices of the Sylvester matrix to define subresultants and to control coefficient growth in polynomial gcd algorithms around 1967 to 1971. Bareiss published his integer-preserving elimination, based on Sylvester's determinant identity, in 1968.

## References
