---
tag: KQ2JBB
kind: algorithm
slug: determinant-gaussian-elimination
name: Determinant by Gaussian elimination
aliases:
- Determinant of a matrix by Gauss
- determinant by row reduction
area: algebra/exact-linear-algebra
level: core
summary: Reduces a matrix to triangular form by row operations and multiplies the diagonal entries, tracking sign changes from row swaps.
solves: [determinant-computation]
model: algebraic-computation-tree
complexity:
  vars: {n: the size of the matrix, b: the maximum binary length of an entry of an integer input}
  time: {worst: Θ(n^3), best: Θ(n)}
  space: {extra: Θ(1)}
  field_operations: {worst: 2n^3/3 + O(n^2)}
  bit_operations: {worst: O(n^5 (b + log n)^2)}
properties: {deterministic: true, in_place: true, recursive: false}
prereqs: [determinant, gaussian-elimination]
see_also: [bareiss-algorithm, kraut-determinant, multimodular-determinant, determinant-computation, hadamard-bound, lu-decomposition, laplace-expansion, gaussian-elimination-modular]
sources:
  - book: isbn:9783540556404
    title: Henri Cohen, A Course in Computational Algebraic Number Theory, Graduate Texts in Mathematics 138
    locator: Section 2.2.3, Computing determinants (determinant by elimination over a field, and the Gauss-Bareiss method over Z)
  - book: isbn:9781107039032
    title: Joachim von zur Gathen and Jurgen Gerhard, Modern Computer Algebra, third edition
    locator: Section 5.5, Modular determinant computation (elimination over Q, the size of the intermediate entries, and the modular alternative)
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Section 28.1, Solving systems of linear equations (LUP decomposition; the determinant is the product of the diagonal of U up to the sign of P)
  - url: "https://cp-algorithms.com/linear_algebra/determinant-gauss.html"
    title: cp-algorithms, Calculating the determinant of a matrix by Gauss
    locator: the whole article (the method with row swaps and its O(n^3) cost)
  - paper: doi:10.1016/0304-3975(83)90110-X
    title: Walter Baur and Volker Strassen, The complexity of partial derivatives, Theoretical Computer Science 22(3), 1983
    locator: the derivative theorem and its corollary that inversion costs at most a constant times the determinant
  - paper: "Jack Edmonds, Systems of distinct representatives and linear algebra, Journal of Research of the National Bureau of Standards 71B(4), 1967"
    locator: pp. 241 to 245
  - paper: "Prescott D. Crout, A short method for evaluating determinants and solving systems of linear equations with real or complex coefficients, Transactions of the American Institute of Electrical Engineers 60, 1941"
---

To compute the [determinant](/determinant/) of a square matrix over a field, run [Gaussian elimination](/gaussian-elimination/) to upper triangular form and multiply the pivots, with one sign change for each row swap. Adding a multiple of a row to another row does not change the determinant, a swap negates it, and the determinant of a triangular matrix is the product of its diagonal. So the method needs $2n^3/3 + O(n^2)$ field operations, against the $n!$ terms of the Leibniz formula. It is the standard exact method over finite fields, and over $\mathbb{Q}$ for small matrices.

Notation: $K$ is a field, $A$ is an $n \times n$ matrix over $K$, and for an integer matrix $b$ is the maximum binary length of an entry. Costs are counted in field operations (each $+, -, \times, \div$ in $K$ costs $1$) and, for $\mathbb{Q}$, in bit operations with schoolbook integer arithmetic.

## In plain words

The determinant of a triangular table of numbers is just the product of the numbers on its diagonal. So turn the table into a triangular one, and keep track of how the determinant changes. Subtracting a multiple of one row from another row does not change it at all. Swapping two rows flips its sign. So go down the columns as in Gaussian elimination. If the current diagonal place holds zero, swap in a lower row that has a nonzero number there, and flip the sign. If no lower row has one, the determinant is zero. Multiply the diagonal numbers as you go.

## The problem

**Input:** an $n \times n$ matrix $A$ over a field $K$, with $n \ge 0$.

**Output:** $\det A \in K$. This is the [determinant computation](/determinant-computation/) problem over a field.

## The algorithm

Indices start at $0$.

```pseudo id=main
DET-ELIM(A)                                 ▷ A is n × n over a field K
L1  d ← 1
L2  for k ← 0 to n − 1 do
L3      p ← the least i with k ≤ i < n and A[i, k] ≠ 0, or NONE
L4      if p = NONE then return 0           ▷ column k is zero from row k down
L5      if p ≠ k then swap rows k and p of A; d ← −d
L6      d ← d · A[k, k]
L7      for i ← k + 1 to n − 1 do
L8          f ← A[i, k] / A[k, k]
L9          for t ← k + 1 to n − 1 do A[i, t] ← A[i, t] − f · A[k, t]
L10 return d
```

Line L9 skips column $k$: those entries would become $0$, and the algorithm never reads them again. The variable $d$ holds the signed product of the pivots found so far. The test of line L4 is a proof of singularity: if the trailing part of column $k$ is zero, the matrix has rank less than $n$.

## Example

Take, over $\mathbb{Q}$,

$$
A = \begin{pmatrix} 0 & 1 & 2 & 3 \\ 1 & 0 & 1 & 2 \\ 2 & 1 & 0 & 1 \\ 3 & 2 & 1 & 0 \end{pmatrix}.
$$

| $k$ | pivot row $p$ | swap | pivot $A[k, k]$ | $d$ after L6 | multipliers $f$ | trailing rows after L9 |
|---|---|---|---|---|---|---|
| 0 | 1 | yes, $d \to -1$ | 1 | $-1$ | 0, 2, 3 | (1 2 3), (1 −2 −3), (2 −2 −6) |
| 1 | 1 | no | 1 | $-1$ | 1, 2 | (−4 −6), (−6 −12) |
| 2 | 2 | no | $-4$ | $4$ | $3/2$ | (−3) |
| 3 | 3 | no | $-3$ | $-12$ | | |

So $\det A = -12$, which agrees with the Leibniz formula. In step $k = 2$ the multiplier is $3/2$ and the new entry is $-12 - \tfrac32 \cdot (-6) = -3$, so fractions appear in the middle of the computation even though the answer is an integer.

## Correctness

Let $S_k$ be the trailing submatrix in rows and columns $k, \dots, n-1$. The invariant at the start of iteration $k$ is $\det A_0 = d \cdot \det S_k$. A swap negates both $d$ and $\det S_k$, the row additions of lines L8 and L9 do not change $\det S_k$, and after them the first column of $S_k$ is $(A[k, k], 0, \dots, 0)^T$, so $\det S_k = A[k, k] \cdot \det S_{k+1}$. At $k = n$ the empty matrix has determinant $1$, so $d = \det A_0$. If line L4 fires, $S_k$ has a zero column and $\det A_0 = 0$. The full proof is in [the correctness proof](proofs/correctness.md).

## Complexity

**Field operations.** Iteration $k$ does one multiplication in line L6, $n - 1 - k$ divisions in line L8, and $(n - 1 - k)^2$ multiplications and as many subtractions in line L9. Summing over $k$ with $u = n - 1 - k$:

$$
\sum_{u=0}^{n-1} \left(1 + u + 2u^2\right) = n + \frac{n(n-1)}{2} + \frac{(n-1)n(2n-1)}{3} = \frac{2n^3}{3} - \frac{n^2}{2} + \frac{5n}{6}.
$$

This is the worst case, reached for each nonsingular matrix. The best case is $\Theta(n)$: a matrix whose first column is zero stops at line L4 after $n$ zero tests. The space is $O(1)$ field elements beyond the matrix, which is overwritten.

**Bit operations over $\mathbb{Q}$.** If the input has integer entries with $|a_{ij}| < 2^b$, the pivot of step $k$ is the quotient $\det A_{k+1}/\det A_k$ of two leading principal minors of the row-permuted input, and each other entry is a quotient of two minors as well, as shown on the [Gaussian elimination](/gaussian-elimination/) page. By the [Hadamard bound](/hadamard-bound/), minors of order $t$ have absolute value at most $t^{t/2} 2^{bt}$, so with fractions in lowest terms each numerator and denominator has $O(n(b + \log n))$ binary digits. The $O(n^3)$ operations then cost $O(n^5 (b + \log n)^2)$ bit operations with schoolbook multiplication and gcd. This is a proved bound. In practice the gcd computations take most of the time. Over $\mathbb{Z}$ the [Bareiss algorithm](/bareiss-algorithm/) avoids fractions and the [multimodular determinant](/multimodular-determinant/) avoids large numbers in the elimination altogether.

**Lower and faster bounds.** In the algebraic model the determinant is as hard as matrix multiplication: it costs $O(n^\omega)$ field operations by a fast LU decomposition, and Baur and Strassen (1983) showed that a program for $\det A$ gives one for $A^{-1}$ with at most a constant factor more operations. See [determinant computation](/determinant-computation/).

## Properties

- **Field only.** Line L8 divides. Over $\mathbb{Z}$ it works with rational numbers; over a ring that is not a domain, such as $\mathbb{Z}/12\mathbb{Z}$, the division can fail even when the determinant exists.
- **Exact.** Any nonzero pivot is correct. No pivoting rule for accuracy is needed in exact arithmetic.
- **In place.** The upper triangle of the working matrix ends up holding $U$ of an LUP decomposition.
- **Early exit.** A singular matrix is often found before the last column.

## Variants and improvements

- **[Bareiss algorithm](/bareiss-algorithm/).** Fraction-free elimination over an integral domain: each division is exact, and the last pivot is the determinant.
- **[Kraut's method](/kraut-determinant/).** Compute an LU decomposition column by column (the Crout order) and multiply the diagonal of the factor.
- **Modular determinant.** Over $\mathbb{Z}$, compute the determinant modulo many word-size primes with this algorithm in $\mathbb{Z}/p\mathbb{Z}$ ([modular elimination](/gaussian-elimination-modular/)), and combine the residues by the Chinese remainder theorem, with the Hadamard bound to decide how many primes are needed. See [multimodular determinant](/multimodular-determinant/).
- **Division-free methods.** Over a commutative ring without division, use the [Berkowitz algorithm](/berkowitz-algorithm/), which gives the whole characteristic polynomial in $O(n^4)$ ring operations.
- **Determinant modulo a composite number.** Over $\mathbb{Z}/m\mathbb{Z}$ with $m$ composite, replace the division by Euclidean steps between two rows. Each swap still negates the result, and the cost grows by a factor $O(\log m)$.

## When to use it

Use this method over a finite field, or over $\mathbb{Q}$ when the matrix is small or its entries are fractions anyway. For integer matrices of moderate size, [Bareiss](/bareiss-algorithm/) is simpler and faster; for large integer matrices, the multimodular method is the standard choice. Never use [Laplace expansion](/laplace-expansion/) beyond $n = 4$ or so: it costs $\Theta(n!)$ operations. In floating point the same algorithm with partial pivoting is the standard numerical method, but its result can lose all relative accuracy for an ill-conditioned matrix, and it cannot decide whether an integer matrix is singular.

## Pitfalls

- **Forgetting the sign of a swap.** If line L5 swaps without negating $d$, the result is wrong in sign for half of the permutations. Each swap negates $d$.
- **Swapping with the wrong row.** Line L3 must search only rows $i \ge k$. Swapping with a row above $k$ destroys the triangular part.
- **Dividing the row instead of subtracting.** Scaling a row by $1/A[k, k]$ multiplies the determinant by $1/A[k, k]$. If the code normalizes pivots to $1$ (as in Gauss-Jordan), it must multiply $d$ by each pivot before the scaling.
- **Integer division.** In a language with integer types, writing $f$ as an integer quotient in line L8 gives wrong answers. Use rationals, a prime field, or the fraction-free [Bareiss](/bareiss-algorithm/) update.
- **Floating point zero tests.** The test $A[i, k] \ne 0$ in line L3 with floats can take a rounding error as a pivot, so a singular matrix gets a tiny nonzero determinant.

## Implementations

## History

The rules for row operations on determinants were known in the nineteenth century, and elimination became the standard way to evaluate determinants once matrices were large enough that expansion by minors was impractical. Crout (1941) described a compact organization of the same computation for desk calculators, which is the [Kraut method](/kraut-determinant/). Edmonds (1967) proved that elimination over $\mathbb{Q}$ runs in polynomial time, through the bound on the intermediate entries.

## References
