---
tag: 82ZZ65
kind: algorithm
slug: gaussian-elimination
name: Gaussian elimination
aliases:
- LU-style elimination
- row reduction
- Gauss elimination
area: algebra/exact-linear-algebra
level: core
summary: Reduces a matrix to echelon form by row operations to solve systems and read off rank, nullspace and determinant.
model: algebraic-computation-tree
complexity:
  vars: {m: the number of rows, n: the number of columns, b: the maximum binary length of an entry of an integer input}
  time: {worst: "Θ(m n min(m, n))", best: Θ(m n)}
  space: {extra: Θ(1)}
  field_operations: {worst: 2n^3/3 + O(n^2)}
  bit_operations: {worst: O(n^5 (b + log n)^2)}
properties: {deterministic: true, in_place: true, recursive: false}
history:
  year: 1809
  people: [Carl Friedrich Gauss]
  note: The method is in Chapter 8 of the Chinese Nine Chapters on the Mathematical Art, about two thousand years old. Gauss used it in 1809 for least squares, and the name Gaussian elimination came much later.
prereqs: [echelon-form, linear-independence]
see_also: [gauss-jordan-elimination, determinant-gaussian-elimination, bareiss-algorithm, gaussian-elimination-modular, lu-decomposition, rank, pivot, hadamard-bound]
sources:
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Section 28.1, Solving systems of linear equations (LUP decomposition, forward and back substitution)
  - book: isbn:9781107039032
    title: Joachim von zur Gathen and Jurgen Gerhard, Modern Computer Algebra, third edition
    locator: Section 5.5, Modular determinant computation (Gaussian elimination over Q, the growth of the entries, and the bound by quotients of minors)
  - book: isbn:9783540556404
    title: Henri Cohen, A Course in Computational Algebraic Number Theory, Graduate Texts in Mathematics 138
    locator: Section 2.2.2, Gaussian elimination and solving linear systems
  - paper: "Jack Edmonds, Systems of distinct representatives and linear algebra, Journal of Research of the National Bureau of Standards 71B(4), 1967"
    locator: pp. 241 to 245 (the entries of the eliminated matrix are quotients of subdeterminants, so elimination over Q runs in polynomial time)
  - paper: doi:10.1016/j.hm.2010.06.003
    title: Joseph F. Grcar, How ordinary elimination became Gaussian elimination, Historia Mathematica 38(2), 2011
    locator: the whole paper (the Chinese source, Newton, Gauss, and the naming of the method)
---

Gaussian elimination brings a matrix over a field to [echelon form](/echelon-form/) by row operations: it picks a nonzero [pivot](/pivot/) in the next column, swaps it into place and subtracts multiples of its row to clear the entries below it. From the echelon form one reads off the [rank](/rank/), the pivot columns and the solutions of a linear system $Ax = b$, and the [determinant](/determinant/) of a square matrix. On an $n \times n$ matrix it uses $2n^3/3 + O(n^2)$ field operations. Over $\mathbb{Q}$ with reduced fractions, the entries stay small because each one is a quotient of two minors of the input, so the method also runs in polynomial time in the bit model.

Notation: $K$ is a field. $A$ is an $m \times n$ matrix over $K$; for a square matrix, $n$ is its size. For an integer matrix, $b$ is the maximum binary length of an entry, so $|a_{ij}| < 2^b$. $\omega$ is the [exponent of matrix multiplication](/matrix-multiplication-exponent/). Costs are given in two models: *field operations*, where each $+, -, \times, \div$ in $K$ costs $1$ (the algebraic model), and *bit operations* for inputs over $\mathbb{Z}$ or $\mathbb{Q}$, with schoolbook integer arithmetic.

## In plain words

Write each equation of a linear system as a row of numbers. Look at the first column. Find a row that has a nonzero number there and move it to the top. Now subtract the right multiple of the top row from each row below it, so that the first column becomes zero under the top row. Those rows no longer mention the first unknown. Repeat the same steps on the rows below the top row, with the next column. If a column has only zeros in the rows that are left, skip it. At the end the rows form a staircase. The last unknown with a step can be found from its row, then the one above it, and so on upward. The number of steps tells how many of the equations are really independent.

## The problem

**Input:** an $m \times n$ matrix $A$ over a field $K$, with $m, n \ge 0$.

**Output:** an [echelon form](/echelon-form/) $E = UA$ with $U$ invertible, the number $r$ of nonzero rows of $E$, and the list $P$ of pivot columns. Then $r = \operatorname{rank} A$.

For a linear system $Ax = b$, the same algorithm runs on the augmented matrix $[A \mid b]$, and back substitution gives a solution or shows that there is none.

## The algorithm

The pseudocode indexes rows and columns from $0$, like the implementation.

```pseudo id=main
GAUSSIAN-ELIMINATION(A)                     ▷ A has m rows and n columns, entries in a field K
L1  r ← 0, P ← empty list                    ▷ r = number of pivots found so far
L2  for j ← 0 to n − 1 do
L3      p ← the least i with r ≤ i < m and A[i, j] ≠ 0, or NONE
L4      if p = NONE then continue with the next j
L5      swap rows r and p of A
L6      for i ← r + 1 to m − 1 do
L7          f ← A[i, j] / A[r, j]
L8          for t ← j to n − 1 do A[i, t] ← A[i, t] − f · A[r, t]
L9      append j to P
L10     r ← r + 1
L11 return A, r, P
```

```pseudo id=solve
SOLVE(A, b)                                  ▷ A is m × n, b has m entries
S1  E, r, P ← GAUSSIAN-ELIMINATION([A | b])   ▷ the augmented matrix has n + 1 columns
S2  if r > 0 and P[r − 1] = n then return NO SOLUTION
S3  x ← the zero vector of length n            ▷ free variables stay 0
S4  for k ← r − 1 down to 0 do
S5      j ← P[k]
S6      x[j] ← (E[k, n] − Σ_{t = j+1}^{n−1} E[k, t] · x[t]) / E[k, j]
S7  return x
```

Rows $0, \dots, r-1$ are finished: they hold the pivots found so far. For column $j$, line L3 looks for a nonzero entry in the unfinished rows. If there is none, the column has no pivot and is skipped. Otherwise line L5 brings that row up to position $r$, and lines L6 to L8 clear column $j$ in every row below it. Line L8 starts at column $j$, because the pivot row is zero to the left of $j$. Over an exact field any nonzero pivot is correct. Line L3 takes the first one; numerical codes choose the largest in absolute value instead, which is a different concern.

In SOLVE, a pivot in the last column means a row $0 = c$ with $c \ne 0$, so the system has no solution. Otherwise back substitution goes up the staircase. Each variable that is not a pivot column is free, and SOLVE sets it to $0$, so it returns one solution; the full solution set is this vector plus the [nullspace](/nullspace/) of $A$.

## Example

Solve, over $\mathbb{Q}$,

$$
\begin{aligned} 2y + z &= 3 \\ x - y &= -1 \\ 2x + 3z &= -1. \end{aligned}
$$

The augmented matrix is $[A \mid b]$ with rows $(0, 2, 1, 3)$, $(1, -1, 0, -1)$ and $(2, 0, 3, -1)$. The first pivot position holds $0$, so a swap is needed.

| step | action | row 0 | row 1 | row 2 |
|---|---|---|---|---|
| start | | 0 2 1 3 | 1 −1 0 −1 | 2 0 3 −1 |
| $j = 0$ | L3 finds $p = 1$; L5 swaps rows 0 and 1 | 1 −1 0 −1 | 0 2 1 3 | 2 0 3 −1 |
| $j = 0$ | $i = 1$: $f = 0$; $i = 2$: $f = 2$ | 1 −1 0 −1 | 0 2 1 3 | 0 2 3 1 |
| $j = 1$ | $p = 1$, no swap; $i = 2$: $f = 1$ | 1 −1 0 −1 | 0 2 1 3 | 0 0 2 −2 |
| $j = 2$ | $p = 2$, nothing below | 1 −1 0 −1 | 0 2 1 3 | 0 0 2 −2 |
| $j = 3$ | no nonzero entry in rows $\ge 3$ | | | |

The result has $r = 3$ and $P = (0, 1, 2)$. The last pivot is not in column $3$, so the system has a solution. Back substitution gives $z = -2/2 = -1$, then $y = (3 - 1 \cdot (-1))/2 = 2$, then $x = (-1 - (-1) \cdot 2)/1 = 1$. Check: $2 \cdot 2 - 1 = 3$, $1 - 2 = -1$, and $2 - 3 = -1$.

## Correctness

The main loop keeps this invariant at the start of the iteration for column $j$: the working matrix is $U A$ for an invertible $U$; rows $0, \dots, r-1$ have leading columns $P_0 < \cdots < P_{r-1} < j$; and rows $r, \dots, m-1$ are zero in columns $0, \dots, j-1$. A column without a pivot keeps the invariant because it is already zero in the unfinished rows. A column with a pivot keeps it because a row swap and the addition of a multiple of one row to another are invertible, and line L7 chooses $f$ so that the new entry in column $j$ is zero. At the end ($j = n$) the unfinished rows are zero, which is the echelon form. For SOLVE, the row operations do not change the set of solutions, and back substitution makes each pivot equation true from the bottom up. The full proof is in [the correctness proof](proofs/correctness.md).

## Complexity

**Field operations.** The pivot with index $k$ (counting from $0$) is in some column $j \ge k$. Lines L6 to L8 then do one division and $n - j$ multiplications and subtractions for each of the $m - k - 1$ rows below it. For a square nonsingular matrix, $j = k$ for every $k$, and the totals are $\sum_{k=0}^{n-1} (n - k - 1) = n(n-1)/2$ divisions and

$$\sum_{k=0}^{n-1} (n - k - 1)(n - k) = \sum_{u=1}^{n} (u - 1) u = \frac{(n-1)n(n+1)}{3} = \frac{n^3 - n}{3}$$

multiplications, and as many subtractions. That is $2n^3/3 + O(n^2)$ field operations. For an $m \times n$ matrix with $r$ pivots, the work is at most $r \cdot m \cdot (n + 1)$ operations, plus $O(mn)$ zero tests in line L3. So the worst case is $\Theta(m n \min(m, n))$, reached when the rank is $\min(m, n)$, and the best case is $\Theta(mn)$, for example the zero matrix, where only the scans of line L3 run. Back substitution costs $O(nr)$ more. The algorithm works in place and needs $O(1)$ extra field elements, plus the list $P$.

**Bit operations over $\mathbb{Q}$.** Field operations are not unit cost on rational numbers, and naive elimination can make numbers grow fast. If fractions are not reduced, or if the code clears denominators by cross-multiplication, the lengths of the numbers can double at each step, which is exponential growth. With reduced fractions, the sizes stay polynomial. Assume no row swaps are needed (a swap only renames rows), and let $A_k$ be the leading $k \times k$ submatrix. After $k$ pivot steps, the entry in row $i > k$ and column $j > k$ is

$$a^{(k)}_{ij} = \frac{\det A_k^{(i, j)}}{\det A_k},$$

where $A_k^{(i, j)}$ is $A_k$ bordered by row $i$ and column $j$ of $A$. The reason: the row operations of the first $k$ steps do not change the determinant of the $(k+1) \times (k+1)$ submatrix in rows $1, \dots, k, i$ and columns $1, \dots, k, j$, and after them that submatrix is upper triangular with diagonal $a^{(0)}_{11}, \dots, a^{(k-1)}_{kk}, a^{(k)}_{ij}$, whose product of the first $k$ is $\det A_k$. This is the argument of Edmonds (1967); von zur Gathen and Gerhard give it in Section 5.5. For an integer matrix with $|a_{ij}| < 2^b$, the [Hadamard bound](/hadamard-bound/) gives $|\det A_k^{(i,j)}| \le (k+1)^{(k+1)/2} 2^{b(k+1)}$, so every reduced numerator and denominator has $O(n(b + \log n))$ binary digits. Each of the $O(n^3)$ field operations then costs $O(n^2 (b + \log n)^2)$ bit operations with schoolbook multiplication and gcd, which gives the proved bound $O(n^5 (b + \log n)^2)$. [Bareiss's fraction-free elimination](/bareiss-algorithm/) has the same bound with schoolbook arithmetic, but it needs no gcd and no fraction arithmetic, so it is faster by a constant factor in practice. The [modular approach](/gaussian-elimination-modular/) is faster still for large matrices.

**Faster in the algebraic model.** Block elimination reduces the triangular decomposition to [matrix multiplication](/matrix-multiplication-exponent/). Bunch and Hopcroft (1974) gave an LUP decomposition of a nonsingular matrix in $O(n^\omega)$ operations, and later work extends this to matrices of any rank and shape; see [LU decomposition](/lu-decomposition/).

## Properties

- **Exact.** Over an exact field the result is exact. Any nonzero pivot gives a correct echelon form.
- **In place.** The working matrix is overwritten. The multipliers $f$ can be stored in the zeroed entries, which gives the $L$ factor of an [LU decomposition](/lu-decomposition/).
- **Deterministic and not unique.** The echelon form depends on the choice of pivot rows, but the rank and the pivot columns do not.
- **Field only.** Line L7 divides. Over an integral domain such as $\mathbb{Z}$ the entries leave the ring; use [Bareiss](/bareiss-algorithm/) for fraction-free elimination, or work over the fraction field.

## Variants and improvements

- **[Gauss-Jordan elimination](/gauss-jordan-elimination/).** Also clear the entries above each pivot and scale the pivots to $1$. This gives the [reduced row echelon form](/reduced-row-echelon-form/) and the inverse of a matrix.
- **[Determinant by elimination](/determinant-gaussian-elimination/).** The determinant of a square matrix is the product of the pivots, times $-1$ for each row swap.
- **[Bareiss algorithm](/bareiss-algorithm/).** Fraction-free elimination over an integral domain, in which each division is exact.
- **[Modular elimination](/gaussian-elimination-modular/).** Work in $\mathbb{Z}/p\mathbb{Z}$ with machine words, and recover integer results by the Chinese remainder theorem.
- **[Bitset elimination](/bitset-gaussian-elimination/).** Over the field with two elements, pack each row into machine words and do a row operation with a few XOR instructions.
- **[Structured Gaussian elimination](/structured-gaussian-elimination/).** For large sparse systems, pick pivots that keep the matrix sparse.
- **[LU decomposition](/lu-decomposition/).** Record the multipliers to solve many systems with the same matrix.
- **Partial pivoting.** In floating point, choose the pivot of largest absolute value in the column, to bound the growth of rounding errors. This is a numerical issue; it does not change the exact result.

## When to use it

Use Gaussian elimination for a dense system or rank computation over a finite field, or over $\mathbb{Q}$ when the matrix is small. For integer matrices of moderate size, [Bareiss](/bareiss-algorithm/) avoids gcds and is usually faster; for large integer matrices, solve modulo primes, or use [Dixon's p-adic lifting](/dixon-p-adic-lifting/) for a system. For large sparse matrices over a finite field, the fill-in of elimination costs too much memory; use [Wiedemann's method](/wiedemann-algorithm/), the [block Wiedemann](/block-wiedemann-algorithm/) or the [block Lanczos](/block-lanczos-algorithm/) algorithm. For very large dense matrices over a field, block algorithms based on fast matrix multiplication are faster.

## Pitfalls

- **Assuming the pivot is on the diagonal.** Taking $A[r, j]$ as the pivot without line L3 divides by zero on the example above. Search the column, and swap (lines L3 to L5).
- **Moving to the next row when a column has no pivot.** If line L4 increments $r$ for an empty column, the rows go out of step with the columns, and a rank-deficient matrix gets a wrong echelon form. Only line L10 increments $r$.
- **Floating point in an exact problem.** A test such as $A[i, j] \ne 0$ in line L3 is unreliable with floats, so rank and solvability can come out wrong. Use exact rationals or a prime field.
- **Unreduced fractions.** Storing numerators and denominators without gcd reduction makes them grow exponentially. Reduce after each operation, or use fraction-free elimination.
- **Updating from column 0.** Line L8 can start at column $j$. Starting at $0$ is correct but wastes work; starting after $j$ leaves the cleared entry nonzero, which breaks the shape of the result unless the code sets it to zero itself.

## Implementations

## History

Elimination on a table of coefficients appears in Chapter 8 (fangcheng) of the Chinese Nine Chapters on the Mathematical Art, a text compiled about two thousand years ago. In Europe, Newton described elimination for algebra students, and Gauss used it in 1809 and later to solve the normal equations of least squares. The name Gaussian elimination, and the matrix form of the method, came in the twentieth century; Grcar (2011) traces this history. Edmonds (1967) showed that the method runs in polynomial time over the rationals, by the bound on the entries given above.

## References
