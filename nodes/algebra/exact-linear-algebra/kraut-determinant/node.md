---
tag: VFMNY1
kind: algorithm
slug: kraut-determinant
name: Determinant by Kraut's method (LU decomposition)
aliases:
- Determinant of a matrix by Kraut method
- Crout's method for the determinant
- determinant by Crout LU decomposition
area: algebra/exact-linear-algebra
level: advanced
summary: Computes a matrix determinant by factoring it into lower and upper triangular matrices and multiplying the diagonal of the factors.
solves: [determinant-computation]
model: algebraic-computation-tree
complexity:
  vars: {n: the size of the matrix, b: the maximum binary length of an entry of an integer input}
  time: {worst: Θ(n^3), best: Θ(n)}
  space: {extra: Θ(1)}
  field_operations: {worst: 2n^3/3 - n^2/2 + 5n/6 - 1}
  bit_operations: {worst: O(n^5 (b + log n)^2)}
properties: {deterministic: true, in_place: true, recursive: false}
prereqs: [determinant, lu-decomposition]
see_also: [determinant-gaussian-elimination, bareiss-algorithm, determinant-computation, gaussian-elimination, lup-decomposition, multimodular-determinant, hadamard-bound, gaussian-elimination-modular]
sources:
  - url: "https://cp-algorithms.com/linear_algebra/determinant-kraut.html"
    title: cp-algorithms, Calculating the determinant using Kraut method in O(N^3)
    locator: the whole article (Crout's decomposition with row swaps, and the determinant as the product of the diagonal of L)
  - paper: "Prescott D. Crout, A short method for evaluating determinants and solving systems of linear equations with real or complex coefficients, Transactions of the American Institute of Electrical Engineers 60, 1941"
    locator: pp. 1235 to 1241 (the compact scheme that computes the factors by inner products)
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Section 28.1, Solving systems of linear equations (LU and LUP decomposition, and their cost)
  - book: isbn:9783540556404
    title: Henri Cohen, A Course in Computational Algebraic Number Theory, Graduate Texts in Mathematics 138
    locator: Section 2.2.3, Computing determinants (elimination over a field and the triangular factors)
  - book: isbn:9781107039032
    title: Joachim von zur Gathen and Jurgen Gerhard, Modern Computer Algebra, third edition
    locator: Section 5.5, Modular determinant computation (the size of the numbers in elimination over Q, and the modular alternative)
  - paper: doi:10.1016/j.hm.2010.06.003
    title: Joseph F. Grcar, How ordinary elimination became Gaussian elimination, Historia Mathematica 38(2), 2011
    locator: the sections on the compact schemes of Doolittle, Crout and Banachiewicz
---

Kraut's method, better known in English as Crout's method, computes the determinant by factoring the matrix as $PA = LU$, where $L$ is lower triangular, $U$ is upper triangular with ones on its diagonal, and $P$ is a row permutation. Then $\det A = \pm \prod_j L[j, j]$, with the sign of $P$. The factors are computed column by column: each entry of $L$ and each entry of $U$ is one inner product of a row of $L$ and a column of $U$ computed earlier. It does the same arithmetic as [Gaussian elimination](/determinant-gaussian-elimination/), $2n^3/3 + O(n^2)$ field operations, in a different order, and the diagonal of $L$ is exactly the list of Gaussian elimination pivots. The name "Kraut" comes from the Russian spelling of Crout, through the competitive programming literature.

Notation: $K$ is a field, $A$ is an $n \times n$ matrix over $K$, and $P$ is a permutation matrix. For an integer input, $b$ is the maximum binary length of an entry, so $|a_{ij}| < 2^b$, and $\omega$ is the exponent of matrix multiplication. Costs are given in field operations and in bit operations over $\mathbb{Q}$ with schoolbook arithmetic.

## In plain words

Any square table that can be inverted can be written, after reordering its rows, as the product of two simpler tables: one with zeros above its diagonal and one with zeros below it and ones on its diagonal. The determinant of such a simple table is the product of its diagonal. So the determinant of the original table is the product of the diagonal of the first factor, with a minus sign if the reordering was odd. Crout's method finds the two factors one column and one row at a time.

## The problem

Input: an $n \times n$ matrix $A$ over a field $K$. Output: $\det A$. On the way, if $A$ is nonsingular, the method gives a permutation $P$, a lower triangular $L$ and a unit upper triangular $U$ with $PA = LU$. This is the Crout form of the [LU decomposition](/lu-decomposition/); the Doolittle form puts the ones on the diagonal of $L$ instead.

## The algorithm

The pseudocode indexes rows and columns from $0$, like the implementation. It stores $L$ in the lower triangle of $A$, including the diagonal, and $U$ in the strict upper triangle; the ones of $U$ are not stored.

```pseudo id=main
KRAUT-DET(A)                                 ▷ A is n × n over a field K; overwritten by L and U
L1  s ← 1                                     ▷ sign of the row permutation
L2  for j ← 0 to n − 1 do
L3      for i ← j to n − 1 do A[i, j] ← A[i, j] − Σ_{k<j} A[i, k] · A[k, j]     ▷ column j of L
L4      p ← the least i with j ≤ i < n and A[i, j] ≠ 0, or NONE
L5      if p = NONE then return 0
L6      if p ≠ j then swap rows j and p of A; s ← −s
L7      for t ← j + 1 to n − 1 do A[j, t] ← (A[j, t] − Σ_{k<j} A[j, k] · A[k, t]) / A[j, j]   ▷ row j of U
L8  d ← s · A[0, 0]                           ▷ for n = 0 the product is empty and d = 1
L9  for j ← 1 to n − 1 do d ← d · A[j, j]
L10 return d
```

Line L3 computes the candidates for column $j$ of $L$ in all rows at or below $j$. These are the entries of column $j$ of the matrix that Gaussian elimination would have after $j$ steps, so a zero column means a singular matrix. Line L6 swaps whole rows, including the parts of $L$ already computed, which keeps $PA = LU$ consistent. Line L7 computes row $j$ of $U$ and divides by the pivot. Lines L3 and L7 read only finished entries: $A[i, k]$ with $k < j$ is in $L$, and $A[k, j]$ with $k < j$ is in $U$.

## Example

Take the matrix with rows $(0, 1, 2, 3)$, $(1, 0, 1, 2)$, $(2, 1, 0, 1)$, $(3, 2, 1, 0)$.

| $j$ | column $j$ of $L$ by L3 | swap | row $j$ of $U$ by L7 |
| --- | --- | --- | --- |
| 0 | $(0, 1, 2, 3)$ | rows 0 and 1, $s = -1$ | $U[0, 1..3] = (0, 1, 2)$ |
| 1 | rows 1 to 3: $(1, 1, 2)$ | none | $U[1, 2..3] = (2, 3)$ |
| 2 | rows 2, 3: $0 - 2 \cdot 1 - 1 \cdot 2 = -4$, $1 - 3 \cdot 1 - 2 \cdot 2 = -6$ | none | $U[2, 3] = (1 - 2 \cdot 2 - 1 \cdot 3)/(-4) = 3/2$ |
| 3 | row 3: $0 - 3 \cdot 2 - 2 \cdot 3 - (-6) \cdot \tfrac32 = -3$ | none | |

The factors are

$$
L = \begin{pmatrix} 1 & 0 & 0 & 0 \\ 0 & 1 & 0 & 0 \\ 2 & 1 & -4 & 0 \\ 3 & 2 & -6 & -3 \end{pmatrix}, \qquad U = \begin{pmatrix} 1 & 0 & 1 & 2 \\ 0 & 1 & 2 & 3 \\ 0 & 0 & 1 & 3/2 \\ 0 & 0 & 0 & 1 \end{pmatrix},
$$

and $LU$ is the input with rows $0$ and $1$ swapped. The determinant is $s \cdot 1 \cdot 1 \cdot (-4) \cdot (-3) = -12$. The diagonal $1, 1, -4, -3$ is the list of pivots that Gaussian elimination finds on the same matrix.

## Correctness

At the start of iteration $j$, let $S$ be the matrix of the entries $A'[i, t] - \sum_{k<j} L[i, k] U[k, t]$ for $i, t \ge j$, where $A'$ is the row-swapped input. The invariant is a block factorization: $A'$ is the product of $\begin{pmatrix} L_1 & 0 \\ L_2 & I \end{pmatrix}$ and $\begin{pmatrix} U_1 & U_2 \\ 0 & S \end{pmatrix}$, with the parts of $L$ and $U$ computed so far, so $\det A_0 = s \prod_{k<j} L[k, k] \det S$. Line L3 computes the first column of $S$. If it is zero, $\det S = 0$. Otherwise, after the swap, splitting off the first row and column of $S$ gives the next column of $L$, the next row of $U$, and a factor $L[j, j]$ of $\det S$. At the end $S$ is empty, so $\det A_0 = s \prod_k L[k, k]$. The [full proof](proofs/correctness.md) gives the details.

## Complexity

**Field operations.** In iteration $j$, line L3 does $j$ multiplications and $j$ subtractions for each of $n - j$ rows, and line L7 does $j$ of each plus one division for each of $n - j - 1$ columns. Lines L8 and L9 do $n - 1$ multiplications. The total is

$$
\sum_{j=0}^{n-1} \big( 2j(n - j) + (2j + 1)(n - j - 1) \big) + (n - 1) = \frac{2}{3} n^3 - \frac{1}{2} n^2 + \frac{5}{6} n - 1
$$

for a nonsingular matrix, which a counting run of the implementation confirms for $n = 3, 6, 10$ ($15$, $130$ and $624$ operations). This is the same leading term as Gaussian elimination; the two methods perform the same multiplications and subtractions, grouped differently. The best case is $\Theta(n)$, when the first column is zero.

**Bits over $\mathbb{Q}$.** Every partial sum on line L3 and line L7 is an entry of an intermediate matrix of Gaussian elimination with the same swaps, and every entry of $U$ is such an entry divided by a pivot. These numbers are quotients of minors of the input, so by the [Hadamard bound](/hadamard-bound/) their numerators and denominators have $O(n(b + \log n))$ bits when the fractions are kept in lowest terms. This gives the proved bound of $O(n^5 (b + \log n)^2)$ bit operations with schoolbook arithmetic, as for elimination. The sums must be computed in the order $k = 0, 1, \dots, j - 1$ for this argument.

**Faster.** With block recursion and fast multiplication, the LUP decomposition costs $O(n^\omega)$ field operations (Bunch and Hopcroft); see [LUP decomposition](/lup-decomposition/) and [determinant computation](/determinant-computation/).

**Space.** In place: $L$ and $U$ overwrite $A$, plus the sign and the permutation.

## Properties

- **The diagonal of $L$ is the list of pivots.** By the proof, $L[j, j]$ is the pivot of step $j$ of Gaussian elimination with the same swaps, and over $\mathbb{Q}$ it equals $d_{j+1}/d_j$, the quotient of two consecutive leading minors of the swapped matrix.
- **Uniqueness.** For a fixed permutation, the Crout factors of a matrix whose leading minors are all nonzero are unique: if $L U = L' U'$, then $L'^{-1} L = U' U^{-1}$ is both lower triangular and unit upper triangular, so it is $I$.
- **Inner-product form.** Each entry of the factors is one dot product of finished data. In floating point this allowed computing the products with extra precision on desk calculators and early computers, which was Crout's reason for the scheme. In exact arithmetic, the order of operations does not change the result.
- **Reuse.** Once $PA = LU$ is known, a system $Ax = b$ costs $2n^2 + O(n)$ more operations by forward and back substitution, and so does each further right-hand side.

## Variants and improvements

- **Doolittle's method.** The same scheme with ones on the diagonal of $L$ and the pivots on the diagonal of $U$; then $\det A = \pm \prod_j U[j, j]$.
- **LDU and Cholesky.** Writing $A = L D U$ with both triangular factors unit makes the pivots the diagonal of $D$. For a symmetric positive definite real matrix, $A = L L^T$ (Cholesky) needs half the work, and $\det A = \prod_j L[j, j]^2$.
- **Over $\mathbb{Z}/p\mathbb{Z}$.** The method runs unchanged with residues and modular inverses, as in [modular elimination](/gaussian-elimination-modular/); the implementation's tests run it modulo $2, 3, 5, 7$ and $101$.
- **Fraction-free LU.** Over $\mathbb{Z}$, the [Bareiss algorithm](/bareiss-algorithm/) gives integer triangular factors whose entries are minors, which avoids rational arithmetic.
- **Pivoting for size.** In floating point, line L4 should take the entry of largest absolute value (partial pivoting). In exact arithmetic, any nonzero entry is correct; choosing a small one keeps the numbers a little smaller in practice, but it does not change the proved bounds.

## When to use it

Use Crout's method when the LU factors are wanted as well as the determinant, for example to solve several systems with the same matrix, and the order of operations matters for the platform: the inner-product form suits code that accumulates dot products. For a determinant alone over a field, it is equivalent to [Gaussian elimination](/determinant-gaussian-elimination/). For integer matrices, prefer the [Bareiss algorithm](/bareiss-algorithm/) or the [multimodular method](/multimodular-determinant/), which avoid rational numbers.

## Pitfalls

- **Swapping only part of a row.** Line L6 must swap the whole row, including the entries of $L$ in the columns less than $j$. Swapping only the unfinished part breaks $PA = LU$ and gives wrong entries later.
- **Forgetting the sign.** Each swap flips the sign of the determinant. Counting swaps with $p = j$ as swaps also gives a wrong sign.
- **Testing the pivot before computing the column.** In Crout's order the candidate pivots are only known after line L3 has computed the whole column $j$ of $L$. Testing $A[j, j]$ of the input matrix is wrong.
- **Floating point in exact problems.** With doubles, a pivot that should be $0$ comes out as $10^{-17}$, and the method returns a tiny nonzero determinant for a singular matrix. Use fractions or residues for exact results.
- **Integer division.** In languages without rationals, `/` on integers truncates, and the entries of $U$ are fractions in general (the example has $3/2$).

## Implementations

## History

Compact schemes for triangular factorization grew out of the hand computations of geodesists and engineers. Myrick Doolittle described one in 1878 for least squares problems of the U.S. Coast and Geodetic Survey, and Prescott Crout published his inner-product scheme in 1941, for engineering problems with real or complex coefficients. Grcar traces this history. The name Kraut is the Russian transliteration of Crout, and the method is known under that name in the Russian and competitive programming literature.

## References
