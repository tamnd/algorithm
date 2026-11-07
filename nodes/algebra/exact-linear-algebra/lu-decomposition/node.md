---
tag: EH2SQ6
kind: algorithm
slug: lu-decomposition
name: LU decomposition
aliases: [Crout factorization, Doolittle factorization, LU factorization, PLU decomposition, exact LU decomposition]
area: algebra/exact-linear-algebra
level: core
summary: Factors a matrix into a unit lower triangular and an upper triangular factor, reusable across many right-hand sides.
solves: [linear-system-solving, determinant-computation]
model: algebraic-computation-tree
complexity:
  vars: {m: the number of rows, n: the number of columns (the size when square), b: the maximum binary length of an entry of an integer input}
  time: {worst: "O(m n min(m, n))", best: Θ(m n)}
  space: {extra: Θ(m^2 + m n)}
  field_operations: {worst: 2n^3/3 + O(n^2)}
  bit_operations: {worst: O(n^5 (b + log n)^2)}
properties: {deterministic: true, in_place: false, recursive: false}
prereqs: [gaussian-elimination, pivot]
see_also: [lup-decomposition, determinant-gaussian-elimination, bareiss-algorithm, matrix-inversion, gaussian-elimination-modular, dixon-p-adic-lifting, hadamard-bound, schur-complement]
sources:
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Section 28.1, Solving systems of linear equations (LU and LUP decomposition, forward and back substitution)
  - book: isbn:9781421407944
    title: Gene H. Golub and Charles F. Van Loan, Matrix Computations, fourth edition, Johns Hopkins University Press, 2013
    locator: Section 3.2, The LU Factorization (existence through leading principal minors, the outer product form), and Section 3.4, Pivoting
  - book: isbn:9781107039032
    title: Joachim von zur Gathen and Jurgen Gerhard, Modern Computer Algebra, third edition, Cambridge University Press, 2013
    locator: Section 5.5, Modular determinant computation (the entries of elimination over Q are quotients of minors, bounded by Hadamard's inequality, and the modular alternative)
  - paper: doi:10.1090/S0025-5718-1974-0331751-8
    title: James R. Bunch and John E. Hopcroft, Triangular factorization and inversion by fast matrix multiplication, Mathematics of Computation 28(125), 1974
    locator: pp. 231 to 236 (LUP decomposition of a nonsingular matrix in O(n^ω) field operations)
  - paper: "Oscar H. Ibarra, Shlomo Moran and Roger Hui, A generalization of the fast LUP matrix decomposition algorithm and applications, Journal of Algorithms 3(1), 1982"
    locator: pp. 45 to 56 (the fast decomposition for matrices of any shape and rank)
  - paper: "Jack Edmonds, Systems of distinct representatives and linear algebra, Journal of Research of the National Bureau of Standards 71B(4), 1967"
    locator: pp. 241 to 245 (the entries of Gaussian elimination over Q are quotients of minors)
---

The LU decomposition writes a matrix $A$ over a field as $P A = L U$, where $P$ is a permutation matrix, $L$ is unit lower triangular and $U$ is upper triangular (in row echelon form when $A$ is singular or not square). It is [Gaussian elimination](/gaussian-elimination/) with its multipliers kept: after the factorization, each new right side $b$ of $A x = b$ costs only $O(n^2)$ field operations, and $\det A$ is the product of the diagonal of $U$ with the sign of $P$. This page treats the exact version over $\mathbb{Q}$ or a finite field; the floating-point version with partial pivoting is [LUP decomposition](/lup-decomposition/).

## In plain words

Elimination turns a system of equations into a triangle: the last equation has one unknown, the one above it two, and so on, and you solve them from the bottom up. To get there it subtracts multiples of one equation from the others. The LU decomposition writes down those multiples. The triangle is the factor called U, and the table of multiples is the factor called L.

Now a new system with the same left side but new numbers on the right is cheap. You replay the recorded subtractions on the new numbers, which is one pass down, and then solve the triangle, which is one pass up. You never redo the expensive elimination. If a needed pivot is zero, the method swaps two rows first and records the swap.

## The problem

**Notation.** $K$ is a field, given exactly (for example $\mathbb{Q}$ with fractions, or $\mathbb{Z}/p\mathbb{Z}$ for a prime $p$). $A$ is an $m \times n$ matrix over $K$; for a square matrix $n$ is its size. $\omega$ is the [exponent of matrix multiplication](/matrix-multiplication-exponent/). For an integer input, $b$ is the maximum binary length of an entry, so $|a_{ij}| < 2^b$. Costs are given in two models: *field operations*, where each $+, -, \times, \div$ in $K$ costs $1$ (the [algebraic computation tree](/algebraic-computation-tree/) model), and *bit operations* for inputs over $\mathbb{Z}$ or $\mathbb{Q}$, with schoolbook integer arithmetic.

**Input.** An $m \times n$ matrix $A$ over $K$.

**Output.** A permutation $\pi$ of the rows, a unit lower triangular $m \times m$ matrix $L$, and an $m \times n$ matrix $U$ in row echelon form, with $P A = L U$, where row $r$ of $P A$ is row $\pi(r)$ of $A$. For a square nonsingular $A$, the matrix $U$ is upper triangular with a nonzero diagonal, and LU-SOLVE returns the solution of $A x = b$.

## The algorithm

The pivot in each column is the first nonzero entry at or below the current row. In exact arithmetic any nonzero pivot is correct (see [pivot](/pivot/)); this rule makes the output unique.

```pseudo id=main
LU-DECOMPOSE(A)                            ▷ A is m × n over a field K
L1  U ← a copy of A, L ← I_m, π ← (1, 2, …, m), r ← 1
L2  for c ← 1 to n do
L3      if r > m then stop the loop
L4      i ← the least index ≥ r with U[i, c] ≠ 0; if there is none, go to the next c
L5      swap rows r and i of U, swap π[r] and π[i], swap L[r, 1 .. r − 1] and L[i, 1 .. r − 1]
L6      for i ← r + 1 to m do
L7          L[i, r] ← U[i, c] / U[r, c]
L8          for j ← c to n do U[i, j] ← U[i, j] − L[i, r] · U[r, j]
L9      r ← r + 1
L10 return π, L, U

LU-SOLVE(π, L, U, b)                       ▷ A is n × n and nonsingular
L11 for i ← 1 to n do y[i] ← b[π[i]] − Σ_{k < i} L[i, k] · y[k]
L12 for i ← n downto 1 do x[i] ← (y[i] − Σ_{k > i} U[i, k] · x[k]) / U[i, i]
L13 return x
```

The variable $r$ is the next pivot row, so after the loop $r - 1$ is the [rank](/rank/). Line L5 swaps the multipliers that are already stored in $L$ together with the rows of $U$, so that each stored multiplier stays with its row. Line L8 makes $U[i, c] = 0$ and updates the rest of row $i$. Line L11 is forward substitution with $L y = P b$, and line L12 is back substitution with $U x = y$. The determinant of a square $A$ is $\operatorname{sgn}(\pi) \prod_i U[i, i]$.

## Example

Factor over $\mathbb{Q}$

$$A = \begin{pmatrix} 2 & 1 & 1 & 0 \\ 4 & 2 & 3 & 1 \\ -2 & 0 & 1 & 3 \\ 6 & 3 & 5 & 4 \end{pmatrix}.$$

| step | pivot | action | rows of $U$ after the step |
|---|---|---|---|
| $c = 1$ | $U[1,1] = 2$ | $L[2,1] = 2$, $L[3,1] = -1$, $L[4,1] = 3$ | $(2,1,1,0)$, $(0,0,1,1)$, $(0,1,2,3)$, $(0,0,2,4)$ |
| $c = 2$ | $U[2,2] = 0$, so swap rows $2$ and $3$ | $\pi = (1,3,2,4)$; the multipliers $2$ and $-1$ swap; $L[3,2] = L[4,2] = 0$ | $(2,1,1,0)$, $(0,1,2,3)$, $(0,0,1,1)$, $(0,0,2,4)$ |
| $c = 3$ | $U[3,3] = 1$ | $L[4,3] = 2$ | $(2,1,1,0)$, $(0,1,2,3)$, $(0,0,1,1)$, $(0,0,0,2)$ |
| $c = 4$ | $U[4,4] = 2$ | no row below | unchanged |

The result is

$$L = \begin{pmatrix} 1 & 0 & 0 & 0 \\ -1 & 1 & 0 & 0 \\ 2 & 0 & 1 & 0 \\ 3 & 0 & 2 & 1 \end{pmatrix}, \qquad U = \begin{pmatrix} 2 & 1 & 1 & 0 \\ 0 & 1 & 2 & 3 \\ 0 & 0 & 1 & 1 \\ 0 & 0 & 0 & 2 \end{pmatrix},$$

with $\pi = (1, 3, 2, 4)$. One swap gives $\operatorname{sgn}(\pi) = -1$, so $\det A = -(2 \cdot 1 \cdot 1 \cdot 2) = -4$, which is also the Leibniz sum. For $b = (3, 8, 0, 13)^T$, line L11 gives $P b = (3, 0, 8, 13)$ and $y = (3, 3, 2, 0)$, and line L12 gives $x = (1, -1, 2, 0)^T$; indeed $A x = b$.

## Correctness

The invariant of the loop of line L2 is: $P A = L U$ for the current $\pi$, $L$ and $U$; rows $1$ to $r-1$ of $U$ are in echelon form with pivots in columns before $c$; and rows $r$ to $m$ of $U$ are zero in columns $1$ to $c - 1$, while row $i \ge r$ of $L$ has nonzero entries only in columns $1$ to $r - 1$ and on the diagonal. Line L5 multiplies both sides by the same transposition on the left, and lines L6 to L8 multiply by an elementary matrix whose inverse is recorded in column $r$ of $L$. At the end, $U$ is in echelon form, so $P A = L U$ is the claimed decomposition; LU-SOLVE then solves $L (U x) = P b$, which is equivalent to $A x = b$. The full proof is in [the correctness proof](proofs/correctness.md).

## Complexity

**Field operations.** For a square nonsingular $A$ step $c = k$ does $n - k$ divisions on line L7 and $(n - k)^2$ multiplications and subtractions on line L8 (the entry in column $c$ is set to $0$ directly). The total is $\sum_{t=1}^{n-1} t = \tfrac12 n(n-1)$ divisions and $\sum_{t=1}^{n-1} t^2 = \tfrac16 (n-1) n (2n - 1)$ multiplications and as many subtractions, so $\tfrac23 n^3 + O(n^2)$ field operations. For an $m \times n$ matrix of rank $r$ the count is $O(m n r)$, which is $O(m n \min(m, n))$; a zero matrix needs only the $\Theta(m n)$ tests of line L4. LU-SOLVE costs $n^2 + O(n)$ multiplications and as many additions. With fast matrix multiplication, a block version costs $O(n^\omega)$ field operations for a nonsingular $n \times n$ matrix (Bunch and Hopcroft, 1974) and $O(m n \min(m,n)^{\omega - 2})$ in general (the line of work begun by Ibarra, Moran and Hui, 1982). These bounds are proved.

**Size of the entries over $\mathbb{Q}$.** Let $A$ be an integer matrix, and assume for the statement that no swap happens (otherwise replace $A$ by $P A$). Let $\Delta_k$ be the leading $k \times k$ minor. After $k$ steps, the entry $(i, j)$ of $U$ for $i, j > k$ is

$$U^{(k)}_{ij} = \frac{\det A[\{1..k, i\}, \{1..k, j\}]}{\Delta_k},$$

and the multipliers are $L_{ik} = \det A[\{1..k-1, i\}, \{1..k\}] / \Delta_k$. Proof of the first formula: steps $1$ to $k$ add multiples of rows $1$ to $k$ to row $i$, which does not change the determinant of the submatrix in rows $\{1..k, i\}$ and columns $\{1..k, j\}$; after these steps that submatrix is block upper triangular with the diagonal blocks $U[1..k, 1..k]$ and $U^{(k)}_{ij}$, so its determinant is $\Delta_k \, U^{(k)}_{ij}$ by the [pivot](/pivot/) lemma $\Delta_k = \prod_{t \le k} U_{tt}$. The formula for $L_{ik}$ follows the same way from $L_{ik} = U^{(k-1)}_{ik} / U_{kk}$. So every number that the algorithm stores is a quotient of two minors of $A$ of order at most $n$, and by the [Hadamard bound](/hadamard-bound/) each minor has absolute value at most $n^{n/2} 2^{n b}$, so at most $n(b + \tfrac12 \log_2 n)$ binary digits. This is Edmonds' observation of 1967. Each field operation on such fractions, with the gcd that reduces the result, costs $O(n^2 (b + \log n)^2)$ bit operations with schoolbook arithmetic, so the whole factorization costs $O(n^5 (b + \log n)^2)$ bit operations. This bound is proved. It is the same order as for the [Bareiss algorithm](/bareiss-algorithm/), which avoids the gcds by keeping the numerators only. Better bit costs come from computing modulo primes; see [modular Gaussian elimination](/gaussian-elimination-modular/) and [Dixon lifting](/dixon-p-adic-lifting/).

**Over $\mathbb{Z}/p\mathbb{Z}$.** Each field operation costs $O(\log^2 p)$ bit operations with schoolbook arithmetic (an inverse by the extended Euclidean algorithm costs the same order), so the factorization costs $O(n^3 \log^2 p)$ bit operations. There is no growth of numbers.

**Space.** $L$ and $U$ take $m^2 + m n$ entries; an in-place version stores the multipliers of $L$ below the diagonal of $U$ and uses $m n$ entries plus the permutation.

## Properties

- **Unique for nonsingular matrices.** If $A$ is square and nonsingular and $P$ is fixed, $L$ and $U$ are unique: from $L_1 U_1 = L_2 U_2$ follows $L_2^{-1} L_1 = U_2 U_1^{-1}$, which is both unit lower and upper triangular, so it is $I$.
- **Exists without swaps exactly when the leading minors are nonzero.** A square $A$ has $A = L U$ with no permutation and nonzero pivots in steps $1$ to $n-1$ if and only if $\Delta_1, \ldots, \Delta_{n-1} \neq 0$; see [pivot](/pivot/).
- **Rank revealing.** The number of nonzero rows of $U$ is the rank, and the pivot columns are the column rank profile of $A$.
- **Deterministic.** The first-nonzero rule makes the output a function of $A$ alone.

## Variants and improvements

- **Doolittle and Crout.** Doolittle's form, used here, makes $L$ unit lower triangular. Crout's form makes $U$ unit upper triangular instead: $A = L' U'$ with $L' = L D$ and $U' = D^{-1} U$, where $D$ is the diagonal of $U$. The $LDU$ form keeps $D$ separate.
- **Fraction-free LU.** Over an integral domain, the Bareiss scheme gives a factorization with factors whose entries are minors of $A$, with no fractions; see the [Bareiss algorithm](/bareiss-algorithm/).
- **Block LU with fast multiplication.** Split $A$ into blocks, factor the top-left block recursively, form the [Schur complement](/schur-complement/) with one matrix product, and factor it recursively. With row swaps this is the Bunch-Hopcroft algorithm, in $O(n^\omega)$ field operations.
- **LU modulo primes.** For an integer matrix, factor modulo several primes and combine, or factor modulo one prime and lift the solution $p$-adically with [Dixon's method](/dixon-p-adic-lifting/).
- **Sparse LU.** Choose pivots to limit fill-in, as in Markowitz's rule; see [pivot](/pivot/) and [structured Gaussian elimination](/structured-gaussian-elimination/).
- **Floating point.** In floating point arithmetic the pivot is the largest entry in absolute value, for stability; see [LUP decomposition](/lup-decomposition/) and [partial pivoting](/partial-pivoting/).

## When to use it

Use the LU decomposition when the same matrix is used with many right sides, or when you need the determinant, the rank and solutions from one computation. For one exact solve over $\mathbb{Q}$ with large entries, [Dixon lifting](/dixon-p-adic-lifting/) is faster in bit operations, and for one determinant the [multimodular determinant](/multimodular-determinant/) is faster. For a sparse matrix over a finite field, the [Wiedemann algorithm](/wiedemann-algorithm/) avoids fill-in. To compute the inverse, LU plus $n$ solves costs $O(n^3)$ field operations, the same order as [Gauss-Jordan elimination](/gauss-jordan-elimination/).

## Pitfalls

- **Not swapping the stored multipliers.** If line L5 swaps the rows of $U$ but not the entries $L[r, 1..r-1]$ and $L[i, 1..r-1]$, then $L U$ is no longer $P A$. The worked example shows this: without that swap, the second and third rows of $L$ would be $(2, 1, 0, 0)$ and $(-1, 0, 1, 0)$, and $L U \neq P A$.
- **Assuming no zero pivot.** Elimination without line L5 fails on $\begin{pmatrix} 0 & 1 \\ 1 & 1 \end{pmatrix}$, which is nonsingular but has no LU factorization without a row swap.
- **Applying $b$ without the permutation.** Line L11 must read $b[\pi[i]]$, not $b[i]$; forward substitution solves $L y = P b$.
- **Floating point for exact problems.** A rank or a determinant of an integer matrix computed with floating point and a tolerance can be wrong; the exact versions over $\mathbb{Q}$ or $\mathbb{Z}/p\mathbb{Z}$ are always right.
- **Using LU-SOLVE on a singular matrix.** Line L12 divides by $U[i, i]$, which is $0$ for a singular square matrix. Use the echelon form and the [nullspace](/nullspace/) instead.

## Implementations

## History

The decomposition is Gaussian elimination with its multipliers recorded, as Golub and Van Loan present it. Edmonds (1967) proved that elimination over $\mathbb{Q}$ runs in polynomial time because its entries are quotients of minors. Bunch and Hopcroft (1974) reduced the decomposition to matrix multiplication.

## References
