---
tag: S667TN
kind: algorithm
slug: bareiss-algorithm
name: Bareiss algorithm
aliases:
- Bareiss fraction-free elimination
- fraction-free Gaussian elimination
- Gauss-Bareiss method
- integer-preserving Gaussian elimination
area: algebra/exact-linear-algebra
level: advanced
summary: Fraction-free elimination over the integers in which every division is exact, keeping intermediate sizes polynomially bounded.
solves: [determinant-computation]
model: algebraic-computation-tree
complexity:
  vars: {n: the size of the matrix, b: the maximum binary length of an entry of an integer input}
  time: {worst: Θ(n^3), best: Θ(n)}
  space: {extra: Θ(1)}
  ring_operations: {worst: 4n^3/3 + O(n^2)}
  bit_operations: {worst: O(n^5 (b + log n)^2)}
properties: {deterministic: true, in_place: true, recursive: false}
prereqs: [determinant-gaussian-elimination, hadamard-bound]
see_also: [determinant-computation, gaussian-elimination, multimodular-determinant, kraut-determinant, cramers-rule, gaussian-elimination-modular, berkowitz-algorithm, smith-normal-form]
sources:
  - paper: doi:10.1090/S0025-5718-1968-0226829-0
    title: Erwin H. Bareiss, Sylvester's identity and multistep integer-preserving Gaussian elimination, Mathematics of Computation 22(103), 1968
    locator: pp. 565 to 578 (the one-step and two-step fraction-free methods, and the proof from Sylvester's identity that every division is exact)
  - book: isbn:9783540556404
    title: Henri Cohen, A Course in Computational Algebraic Number Theory, Graduate Texts in Mathematics 138
    locator: Section 2.2.3, Computing determinants (the Gauss-Bareiss method for matrices over Z and over integral domains)
  - book: isbn:9780792392590
    title: Keith O. Geddes, Stephen R. Czapor and George Labahn, Algorithms for Computer Algebra, Kluwer, 1992
    locator: Chapter 9, Solving systems of equations (fraction-free Gaussian elimination, single-step and multistep, over integral domains)
  - book: isbn:9781107039032
    title: Joachim von zur Gathen and Jurgen Gerhard, Modern Computer Algebra, third edition
    locator: Section 5.5, Modular determinant computation (the size of the numbers in elimination over Q, bounded through minors and Hadamard's inequality, and the modular alternative)
  - paper: "Jack Edmonds, Systems of distinct representatives and linear algebra, Journal of Research of the National Bureau of Standards 71B(4), 1967"
    locator: pp. 241 to 245 (the entries of Gaussian elimination over Q are quotients of minors, so the method runs in polynomial time)
---

The Bareiss algorithm computes the determinant of a matrix over the integers, or over any integral domain, with row operations that never leave the ring. Each step replaces an entry by $(a_{kk} a_{ij} - a_{ik} a_{kj}) / p$, where $p$ is the pivot of the previous step, and Sylvester's determinant identity shows that the division is always exact. The new entry is not just an integer: it is a minor of the input matrix. So every intermediate number is bounded by the [Hadamard bound](/hadamard-bound/) and has $O(n(b + \log n))$ bits, and the last entry is the determinant itself. The algorithm does twice the arithmetic of [Gaussian elimination](/determinant-gaussian-elimination/), but it needs no rational numbers and no gcds, which makes it the standard simple method for exact determinants of integer and polynomial matrices.

Notation: $R$ is an integral domain, for example $\mathbb{Z}$ or $K[x]$, with field of fractions $F$. $A$ is an $n \times n$ matrix over $R$, $d_k$ is its leading principal minor of order $k$ ($d_0 = 1$), and $\omega$ is the exponent of matrix multiplication. For an integer input, $b$ is the maximum binary length of an entry, so $|a_{ij}| < 2^b$. Costs are given in ring operations and in bit operations with schoolbook integer arithmetic.

## In plain words

Plain elimination subtracts a fraction of one row from another, so over whole numbers it creates fractions, and fractions are slow. The Bareiss method instead multiplies a row by the pivot and subtracts a whole multiple of the pivot row, which keeps whole numbers. Done alone, this makes the numbers grow very fast. The trick is that after each step every number can be divided exactly by the pivot of the step before. The numbers then stay about as large as the determinant, and the last number left is the determinant.

## The problem

Input: an $n \times n$ matrix $A$ over an integral domain $R$ in which exact division is computable: given $u$ and $v \ne 0$ with $v \mid u$, find $u/v$. Output: $\det A \in R$. Over $\mathbb{Z}$ the cost of interest is the number of bit operations, which depends on how large the intermediate numbers become.

## The algorithm

The pseudocode indexes rows and columns from $0$, like the implementation.

```pseudo id=main
BAREISS(A)                                   ▷ A is n × n over an integral domain R
L1  if n = 0 then return 1
L2  s ← 1, prev ← 1                            ▷ prev = previous pivot, d_k
L3  for k ← 0 to n − 2 do
L4      if A[k, k] = 0 then
L5          p ← the least i > k with A[i, k] ≠ 0, or NONE
L6          if p = NONE then return 0
L7          swap rows k and p; s ← −s
L8      for i ← k + 1 to n − 1 do
L9          for j ← k + 1 to n − 1 do
L10             A[i, j] ← (A[k, k] · A[i, j] − A[i, k] · A[k, j]) / prev   ▷ exact division in R
L11     prev ← A[k, k]
L12 return s · A[n − 1, n − 1]
```

Each iteration treats the $2 \times 2$ determinant of the pivot, the entry in its row, the entry in its column and the entry $A[i, j]$, and divides it by the previous pivot. Line L10 must compute the whole numerator first and divide afterwards: the two products alone are not divisible by $\mathit{prev}$ in general. A zero pivot is handled as in ordinary elimination, by a row swap that changes the sign. If the whole column below the pivot is zero, the determinant is $0$.

The result is the last diagonal entry, not the product of the diagonal. After step $k$, the diagonal entry $A[k, k]$ is the leading minor $d_{k+1}$ of the row-permuted input, so the diagonal holds $d_1, d_2, \dots, d_n$.

## Example

For $M$ with rows $(2, 1, 0)$, $(1, 3, 1)$, $(0, 1, 4)$: step $k = 0$ has $\mathit{prev} = 1$ and gives $A[1, 1] = 2 \cdot 3 - 1 \cdot 1 = 5$, $A[1, 2] = 2 \cdot 1 - 1 \cdot 0 = 2$, $A[2, 1] = 2 \cdot 1 - 0 \cdot 1 = 2$ and $A[2, 2] = 2 \cdot 4 - 0 \cdot 0 = 8$. Step $k = 1$ has $\mathit{prev} = 2$ and gives $A[2, 2] = (5 \cdot 8 - 2 \cdot 2)/2 = 36/2 = 18 = \det M$. The entry $5$ is the minor $\det \begin{pmatrix} 2 & 1 \\ 1 & 3 \end{pmatrix}$, as the theory says.

A matrix that needs a swap:

$$
A = \begin{pmatrix} 0 & 1 & 2 & 3 \\ 1 & 0 & 1 & 2 \\ 2 & 1 & 0 & 1 \\ 3 & 2 & 1 & 0 \end{pmatrix}.
$$

| $k$ | swap | prev | rows after the step |
| --- | --- | --- | --- |
| 0 | rows 0 and 1, $s = -1$ | 1 | (1 0 1 2), (0 1 2 3), (0 1 −2 −3), (0 2 −2 −6) |
| 1 | none | 1 | (1 0 1 2), (0 1 2 3), (0 0 −4 −6), (0 0 −6 −12) |
| 2 | none | 1 | (1 0 1 2), (0 1 2 3), (0 0 −4 −6), (0 0 0 12) |

In step $2$, $A[3, 3] = ((-4)(-12) - (-6)(-6))/1 = 12$. The result is $s \cdot 12 = -12$, the value of the Leibniz formula. The diagonal $1, 1, -4, 12$ is the list of leading minors of the swapped matrix, so the divisors $\mathit{prev}$ are $1, 1, -4$. The table shows the entries below the diagonal as $0$, as the implementation stores them; the pseudocode never reads them again.

## Correctness

Let $m_k(i, j)$ be the minor of the row-permuted input in the rows $0, \dots, k-1, i$ and the columns $0, \dots, k-1, j$. The invariant is that, before step $k$, every entry $A[i, j]$ with $i, j \ge k$ equals $m_k(i, j)$ and $\mathit{prev} = d_k \ne 0$. The key fact is the identity $d_k\, m_{k+1}(i, j) = m_k(k, k)\, m_k(i, j) - m_k(i, k)\, m_k(k, j)$, a case of Sylvester's identity. It follows from block elimination: after the first $k$ rows clear the first $k$ columns, each bordered minor is $d_k$ times an entry of the Schur complement. So line L10 produces $m_{k+1}(i, j)$, which is in $R$, and the division is exact because $R$ has no zero divisors. At the end $A[n-1, n-1] = d_n$, the determinant of the swapped matrix. If a column has no nonzero entry, the Schur complement has a zero column and the determinant is $0$. The [full proof](proofs/correctness.md) covers the swaps and the sign.

## Complexity

**Ring operations.** Step $k$ updates $(n - k - 1)^2$ entries with two multiplications, one subtraction and one exact division each. The total is $4 \sum_{t=1}^{n-1} t^2 = \tfrac{2}{3}(n-1)n(2n-1) = \tfrac43 n^3 + O(n^2)$ ring operations, of which about $n^3/3$ are divisions. Gaussian elimination over $F$ needs $\tfrac23 n^3 + O(n^2)$, so Bareiss does about twice as many operations, but on smaller numbers. The best case is $\Theta(n)$, when the first column is zero and line L6 returns at once.

**Bit operations over $\mathbb{Z}$.** Every stored number is a minor of order at most $n$ of the input, so by the Hadamard bound it has at most $n(b + \tfrac12 \log_2 n) + 1$ bits. A numerator on line L10 has at most twice as many bits. With schoolbook multiplication and division, each step of line L10 costs $O(n^2 (b + \log n)^2)$ bit operations, and the total is $O(n^5 (b + \log n)^2)$. With fast integer multiplication, $M(\ell)$ for $\ell$-bit numbers, the bound is $O(n^3 M(n(b + \log n)))$, which is $O(n^4 b)$ up to logarithmic factors. These bounds are proved. The same order holds for elimination over $\mathbb{Q}$ with reduced fractions, but there each operation also needs gcds. In a run of the implementation on this page with random $40 \times 40$ matrices of $21$-bit entries, Bareiss took about $0.05$ s and elimination with Python fractions about $0.5$ s; that factor is an observation, not a bound. The determinant there had $844$ bits, against the Hadamard estimate $n(b + \tfrac12 \log_2 n) \approx 906$.

**Space.** The algorithm works in place. The numbers have $O(n(b + \log n))$ bits each, so the matrix takes $O(n^3 (b + \log n))$ bits at most, against $n^2 b$ for the input.

**Better bounds.** The [multimodular determinant](/multimodular-determinant/) avoids large numbers altogether and costs about $n^4 b$ bit operations with schoolbook arithmetic, without the extra factor of $n$ from the number size per operation. Storjohann's algorithms reach about $n^\omega b$ up to logarithmic factors; see [determinant computation](/determinant-computation/).

## Properties

- **Every entry is a minor.** After step $k$, $A[i, j] = m_{k+1}(i, j)$ for $i, j > k$, the row $k$ holds $m_k(k, j)$, and the diagonal holds the leading minors $d_1, \dots, d_n$ of the swapped matrix. The implementation's tests check this against the Leibniz formula.
- **Exact division in any integral domain.** The proof uses only that $R$ has no zero divisors. Over $K[x]$ or $\mathbb{Z}[x_1, \dots, x_k]$ the divisions are exact polynomial divisions, and the degrees are bounded by the degrees of minors.
- **Division-free except for the exact divisions.** No inverses are ever computed, so the algorithm needs no field. Over a ring with zero divisors, such as $\mathbb{Z}/6\mathbb{Z}$, the quotient is not unique and the method does not apply; use the [Berkowitz algorithm](/berkowitz-algorithm/) there.
- **Deterministic and in place**, with the same pivoting as elimination over a field.

## Variants and improvements

- **Fraction-free echelon form.** Run the same update on an $m \times n$ matrix, skipping a column that has no pivot. The result is an echelon form with integer entries, the rank, and the pivot columns; the implementation's `fraction_free_echelon` does this. It is the integer counterpart of [Gaussian elimination](/gaussian-elimination/).
- **Solving systems.** On $[A \mid b]$, the last row ends with $\det A_{n-1}(b)$, the numerator of [Cramer's rule](/cramers-rule/) for $x_{n-1}$. A fraction-free back substitution then gives the integers $\det(A)\, x_i$ for every $i$.
- **Fraction-free Gauss-Jordan.** Clearing above the pivots too, with the same divisions, gives $\det(A)\, A^{-1} = \operatorname{adj}(A)$ on $[A \mid I]$ for a nonsingular $A$.
- **Multistep elimination.** Bareiss's paper also gives a two-step method that eliminates two columns at once, with a division by the pivot two steps back, which saves multiplications at the cost of a more complex update.
- **Fraction-free LU decomposition.** The same minors arranged as $PA = L D^{-1} U$ with integer $L$, $D$ and $U$ give a factorization that can be reused for several right sides.
- **Modular arithmetic instead.** For large $n$ or large $b$, compute the determinant modulo many primes by [modular elimination](/gaussian-elimination-modular/) and combine the results; this is the multimodular method.

## When to use it

Use Bareiss for an exact determinant, rank or solution of a small or medium integer matrix, or of a matrix with polynomial or symbolic entries, when a simple deterministic method is wanted. It is a common choice for matrices of polynomials, where modular methods need evaluation and interpolation as well. For large integer matrices, multimodular or p-adic methods are faster, and for matrices over a ring with zero divisors, use a division-free method.

## Pitfalls

- **The product of the diagonal.** In Bareiss, the diagonal holds the leading minors $d_1, \dots, d_n$. The determinant is the last of them, not their product.
- **Dividing too early.** Computing `A[k][k] * A[i][j] // prev - A[i][k] * A[k][j] // prev` divides the two products separately, which is not exact and gives wrong results. Divide the whole difference.
- **Floor division of negative numbers.** In Python, `//` is floor division, which is correct here only because the quotient is exact. In C, `/` truncates toward zero, which is also correct for exact quotients. A wrong result from an inexact division shows a bug elsewhere, so a debug build should check the remainder.
- **Fixed-width integers.** The numbers grow to about $n(b + \tfrac12 \log_2 n)$ bits and the numerators to twice that. With 64-bit integers, even a $10 \times 10$ matrix with entries below $100$ can overflow. Use big integers.
- **A zero pivot.** Skipping the swap when $A[k, k] = 0$ makes the next step divide by $0$. The swap must also flip the sign.
- **Rings with zero divisors.** Over $\mathbb{Z}/m\mathbb{Z}$ with composite $m$, or for floating-point numbers, the exact division is not defined or not exact. Bareiss is an algorithm for integral domains.

## Implementations

## History

Erwin Bareiss published the method in 1968, under the name of integer-preserving Gaussian elimination, and derived it from Sylvester's determinant identity; the paper also gives the two-step version. A year earlier, Jack Edmonds had shown that ordinary Gaussian elimination over $\mathbb{Q}$ runs in polynomial time, because its entries are quotients of minors. Cohen calls the method Gauss-Bareiss.

## References
