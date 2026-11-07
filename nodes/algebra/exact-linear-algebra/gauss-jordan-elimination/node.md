---
tag: NK577G
kind: algorithm
slug: gauss-jordan-elimination
name: Gauss-Jordan elimination
aliases:
- Gauss-Jordan reduction
- Gauss-Jordan method
area: algebra/exact-linear-algebra
level: core
summary: Gaussian elimination that continues to reduced row echelon form, giving the inverse or solution directly.
solves: [matrix-inversion]
model: algebraic-computation-tree
complexity:
  vars: {m: the number of rows, n: the number of columns, b: the maximum binary length of an entry of an integer input}
  time: {worst: "Θ(m n min(m, n))", best: Θ(m n)}
  space: {extra: Θ(1)}
  field_operations: {worst: n^3 + n^2/2 - n/2}
  bit_operations: {worst: O(n^5 (b + log n)^2)}
properties: {deterministic: true, in_place: true, recursive: false}
prereqs: [gaussian-elimination, echelon-form]
see_also: [reduced-row-echelon-form, matrix-inversion, lu-decomposition, nullspace-computation, bareiss-algorithm, gaussian-elimination-modular, bitset-gaussian-elimination, cramers-rule]
sources:
  - book: isbn:9780980232714
    title: Gilbert Strang, Introduction to Linear Algebra, fourth edition
    locator: Chapter 2, Section 2.5, Inverse matrices (computing the inverse by Gauss-Jordan elimination on [A I])
  - book: isbn:9783540556404
    title: Henri Cohen, A Course in Computational Algebraic Number Theory, Graduate Texts in Mathematics 138
    locator: Section 2.2.2, Gaussian elimination and solving linear systems (elimination over a field, the inverse of a square matrix)
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Section 28.2, Inverting matrices (the inverse from n solves, and its cost against matrix multiplication)
  - book: isbn:9781107039032
    title: Joachim von zur Gathen and Jurgen Gerhard, Modern Computer Algebra, third edition
    locator: Section 5.5, Modular determinant computation (the entries of elimination over Q as quotients of minors, and the Hadamard bound)
  - url: "https://cp-algorithms.com/linear_algebra/linear-system-gauss.html"
    title: cp-algorithms, Gauss method for solving system of linear equations
    locator: the whole article (reduction of every column above and below the pivot, and the free variables)
  - paper: doi:10.2307/2322413
    title: Steven C. Althoen and Renate McLaughlin, Gauss-Jordan reduction, a brief history, American Mathematical Monthly 94(2), 1987
    locator: pp. 130 to 142 (Wilhelm Jordan, B.-I. Clasen and the name of the method)
  - paper: doi:10.1016/j.hm.2010.06.003
    title: Joseph F. Grcar, How ordinary elimination became Gaussian elimination, Historia Mathematica 38(2), 2011
    locator: the sections on the geodesists and on Jordan
---

Gauss-Jordan elimination is [Gaussian elimination](/gaussian-elimination/) that does not stop at a staircase. At each pivot it divides the pivot row by the pivot and clears the pivot column above the pivot as well as below. The result is the [reduced row echelon form](/reduced-row-echelon-form/), which is unique, and from which the rank, a basis of the row space, the pivot columns and the solutions of a system can be read without back substitution. On the matrix $[A \mid I]$ it returns $[I \mid A^{-1}]$, the classical way to [invert a matrix](/matrix-inversion/) by hand. It costs about $n^3$ field operations on a square matrix, half as much again as Gaussian elimination.

Notation: $K$ is a field, $A$ is an $m \times n$ matrix over $K$, and $n$ is also the size of a square matrix. For costs over $\mathbb{Z}$ or $\mathbb{Q}$, $b$ is the maximum binary length of an entry of an integer input, so $|a_{ij}| < 2^b$, and $\omega$ is the exponent of matrix multiplication. Costs are given in field operations and in bit operations with schoolbook integer arithmetic.

## In plain words

Gaussian elimination makes zeros below each leading number, giving a staircase. Gauss-Jordan goes further. It scales each leading number to 1 and also makes zeros above it. When it is done, each leading 1 is alone in its column. For a system of equations, every equation then names one unknown and gives its value at once. If you write the identity matrix next to a square matrix and reduce both together, the identity turns into the inverse, provided the left side became the identity.

## The problem

Input: an $m \times n$ matrix $A$ over a field $K$. Output: the reduced row echelon form $E$ of $A$, its rank $r$ and its pivot columns $P = (p_0 < \dots < p_{r-1})$. The form $E$ is in [echelon form](/echelon-form/), each pivot is $1$, and each pivot is the only nonzero entry of its column. There is an invertible $T$ with $E = TA$, and $E$ depends only on the row space of $A$.

Two uses are built on it. INVERSE takes an $n \times n$ matrix $A$ and returns $A^{-1}$, or reports that $A$ is singular. SOLVE takes $A$ and $b \in K^m$ and returns one solution of $Ax = b$, or reports that there is none.

## The algorithm

The pseudocode indexes rows and columns from $0$, like the implementation.

```pseudo id=main
GAUSS-JORDAN(A)                              ▷ A has m rows and n columns, entries in a field K
L1  r ← 0, P ← empty list                    ▷ r = number of pivots found so far
L2  for j ← 0 to n − 1 do
L3      p ← the least i with r ≤ i < m and A[i, j] ≠ 0, or NONE
L4      if p = NONE then continue with the next j
L5      swap rows r and p of A
L6      c ← A[r, j]; for t ← j to n − 1 do A[r, t] ← A[r, t] / c
L7      for each i with 0 ≤ i < m and i ≠ r do
L8          f ← A[i, j]
L9          for t ← j to n − 1 do A[i, t] ← A[i, t] − f · A[r, t]
L10     append j to P; r ← r + 1
L11 return A, r, P
```

```pseudo id=inverse
INVERSE(A)                                   ▷ A is n × n
V1  E, r, P ← GAUSS-JORDAN([A | I])           ▷ the augmented matrix has 2n columns
V2  if P ≠ (0, 1, …, n − 1) then return SINGULAR
V3  return the columns n, …, 2n − 1 of E
```

```pseudo id=solve
SOLVE(A, b)                                  ▷ A is m × n, b has m entries
S1  E, r, P ← GAUSS-JORDAN([A | b])           ▷ the augmented matrix has n + 1 columns
S2  if r > 0 and P[r − 1] = n then return NO SOLUTION
S3  x ← the zero vector of length n            ▷ free variables stay 0
S4  for k ← 0 to r − 1 do x[P[k]] ← E[k, n]
S5  return x
```

The loop is the loop of Gaussian elimination with two changes. Line L6 scales the pivot row so that the pivot is $1$, and line L7 runs over every other row, above the pivot as well as below. Lines L6 and L9 start at column $j$, because the pivot row is zero to the left of $j$. Over an exact field any nonzero pivot is correct, and line L3 takes the first one.

INVERSE uses the identity matrix as a record of the row operations: if the operations multiply $A$ by $T$ on the left, they turn $I$ into $T$. When the left half becomes $I$, then $TA = I$ and $T = A^{-1}$. SOLVE needs no back substitution: in $E$, row $k$ contains the pivot variable $x_{P[k]}$ with coefficient $1$ and otherwise only free variables, which it sets to $0$.

## Example

Invert $A = \begin{pmatrix} 0 & 2 & 1 \\ 1 & 1 & 1 \\ 2 & 3 & 1 \end{pmatrix}$, with $\det A = 3$, by reducing $[A \mid I]$:

| step | action | row 0 | row 1 | row 2 |
| --- | --- | --- | --- | --- |
| start | | 0 2 1 \| 1 0 0 | 1 1 1 \| 0 1 0 | 2 3 1 \| 0 0 1 |
| $j = 0$ | L3 finds $p = 1$; L5 swaps rows 0 and 1; $c = 1$ | 1 1 1 \| 0 1 0 | 0 2 1 \| 1 0 0 | 2 3 1 \| 0 0 1 |
| $j = 0$ | row 1: $f = 0$; row 2: $f = 2$ | 1 1 1 \| 0 1 0 | 0 2 1 \| 1 0 0 | 0 1 −1 \| 0 −2 1 |
| $j = 1$ | $p = 1$; L6 divides row 1 by $c = 2$ | 1 1 1 \| 0 1 0 | 0 1 1/2 \| 1/2 0 0 | 0 1 −1 \| 0 −2 1 |
| $j = 1$ | row 0: $f = 1$; row 2: $f = 1$ | 1 0 1/2 \| −1/2 1 0 | 0 1 1/2 \| 1/2 0 0 | 0 0 −3/2 \| −1/2 −2 1 |
| $j = 2$ | $p = 2$; L6 divides row 2 by $c = −3/2$ | 1 0 1/2 \| −1/2 1 0 | 0 1 1/2 \| 1/2 0 0 | 0 0 1 \| 1/3 4/3 −2/3 |
| $j = 2$ | row 0: $f = 1/2$; row 1: $f = 1/2$ | 1 0 0 \| −2/3 1/3 1/3 | 0 1 0 \| 1/3 −2/3 1/3 | 0 0 1 \| 1/3 4/3 −2/3 |

The pivots are the columns $0, 1, 2$, so $A$ is invertible and

$$
A^{-1} = \frac{1}{3} \begin{pmatrix} -2 & 1 & 1 \\ 1 & -2 & 1 \\ 1 & 4 & -2 \end{pmatrix}.
$$

The common denominator is $3 = \det A$, as [Cramer's rule](/cramers-rule/) predicts: $A^{-1} = \operatorname{adj}(A)/\det A$. The pivots before scaling are $1$, $2$ and $-3/2$, and their product with the sign $-1$ of the one swap is $\det A = 3$. The columns $j = 3, 4, 5$ have no pivot, because the rows $r \ge 3$ do not exist.

On the singular matrix with rows $(0, 2, 4, 2)$, $(1, 1, 1, 0)$, $(2, 4, 6, 2)$, GAUSS-JORDAN returns rows $(1, 0, -1, -1)$, $(0, 1, 2, 1)$, $(0, 0, 0, 0)$, with $r = 2$ and $P = (0, 1)$.

## Correctness

The invariant at the start of iteration $j$ has three parts: the working matrix is $TA$ for an invertible $T$; the first $j$ columns are already in reduced row echelon form with pivots $P$; and the rows $r, \dots, m-1$ are zero in those columns. An iteration with a pivot makes column $j$ the unit vector $e_r$ and does not change the earlier columns, because the pivot row is zero there. At the end the whole matrix is in reduced row echelon form with the row space of $A$, and the uniqueness of that form makes it *the* reduced form of $A$. For INVERSE, the pivots in the first $n$ columns are the pivots of $A$, which are $0, \dots, n-1$ exactly when $A$ is invertible, and then the right half is $T = A^{-1}$. The [full proof](proofs/correctness.md) also covers SOLVE.

## Complexity

**Field operations.** When column $j$ has a pivot, line L6 costs $n - j$ divisions, and lines L7 to L9 cost $2(n - j)$ operations in each of the $m - 1$ other rows. The pivot of the $k$-th step is in a column $j \ge k$, so a matrix of rank $r$ costs at most $\sum_{k<r} (2m - 1)(n - k) \le 2mnr$ operations, and the loop of line L3 adds $O(mn)$ comparisons. With $r \le \min(m, n)$ this is $O(mn \min(m, n))$, and the bound is reached when the first $\min(m, n)$ columns have pivots. A zero matrix costs only the $\Theta(mn)$ tests of line L3.

For a nonsingular $n \times n$ matrix the exact count is $\sum_{j=0}^{n-1} (2n - 1)(n - j) = (2n - 1) n (n + 1)/2 = n^3 + n^2/2 - n/2$. Gaussian elimination with back substitution needs $2n^3/3 + O(n^2)$, so the full reduction costs $50\%$ more for one system. The reason is that clearing above the pivot works on full rows, while back substitution works on a triangle.

INVERSE on $[A \mid I]$, with $2n$ columns, costs $(2n - 1) n (3n + 1)/2 = 3n^3 - n^2/2 - n/2$ operations as written. A careful code skips the entries of the right half that are known to be zero: after $k$ steps, a row's right half has nonzero entries only in the $k + 1$ columns of the identity that the operations have touched. This brings the count to $2n^3 + O(n^2)$, the same as inversion by [LU decomposition](/lu-decomposition/). With fast matrix multiplication, inversion costs $O(n^\omega)$ field operations (Bunch and Hopcroft, and the reduction of inversion to multiplication in CLRS Section 28.2), but not by this loop.

**Bits over $\mathbb{Q}$.** Let $A$ have integer entries. After $k$ pivots, let $B$ be the $k \times k$ submatrix of the row-permuted input in the pivot rows and pivot columns. Then every entry of the working matrix is a quotient of two minors of $A$ of order at most $k + 1$, with the denominator $\det B$ (proved under Properties). By the [Hadamard bound](/hadamard-bound/), a minor of order $t$ has absolute value at most $t^{t/2} 2^{bt}$, so numerators and denominators have $O(n(b + \log n))$ bits. Python's `Fraction` keeps each number in lowest terms, so each field operation costs $O(n^2 (b + \log n)^2)$ bit operations with schoolbook multiplication and Euclid's gcd. The total is $O(n^5 (b + \log n)^2)$ bit operations, a proved bound. For INVERSE, a minor of $[A \mid I]$ is, up to sign, a minor of $A$ (expand along the identity columns), so the same bound holds. In practice the gcd computations dominate. The [Bareiss algorithm](/bareiss-algorithm/) avoids them by keeping the numerators as integers, and [modular elimination](/gaussian-elimination-modular/) avoids the large numbers entirely.

**Space.** The algorithm works in place, with $O(1)$ extra field elements besides the list $P$. INVERSE needs the $n \times 2n$ matrix.

## Properties

- **Quotients of minors.** After $k$ pivots with pivot columns $J$, let $P$ be the permutation of the row swaps so far, $B = (PA)[0..k-1, J]$ and $C = (PA)[k..m-1, J]$. The first $k$ rows of the working matrix $W$ are combinations of the first $k$ rows of $PA$, and each other row $i$ is row $i$ of $PA$ minus such a combination. So $W = \begin{pmatrix} T_1 & 0 \\ T_2 & I \end{pmatrix} PA$. The columns $J$ of $W$ are $e_0, \dots, e_{k-1}$, so $T_1 B = I$ and $T_2 B + C = 0$, that is $T_1 = B^{-1}$ and $T_2 = -CB^{-1}$. For a row $i < k$, $W[i, t]$ is entry $i$ of $B^{-1}$ times column $t$ of $PA$ restricted to the first $k$ rows, which by Cramer's rule is $\det B_i / \det B$, where $B_i$ is $B$ with column $i$ replaced by that column. For a row $i \ge k$, $W[i, t]$ is the Schur complement $(PA)[i, t] - C_i B^{-1} (PA)[0..k-1, t]$, which is the minor of $PA$ in rows $0..k-1, i$ and columns $J, t$, divided by $\det B$.
- **Unique output.** Unlike Gaussian elimination, whose staircase depends on the row operations, the output does not depend on the pivot choice or on the order of the rows.
- **Exact only.** In floating point, Gauss-Jordan has worse error bounds than LU with back substitution for solving a system, and numerical libraries do not use it for that purpose. Over exact fields this question does not arise.
- **No division by a pivot in the inner loop.** Because the pivot is scaled to $1$ on line L6, the multiplier on line L8 is just $A[i, j]$, so the inner loop has only multiplications and subtractions.

## Variants and improvements

- **Solving many systems.** $[A \mid B]$ with a matrix $B$ of right sides gives $[E \mid TB]$ in one pass, which is how INVERSE treats $B = I$.
- **Nullspace and image.** The reduced form gives a basis of the [nullspace](/nullspace/) directly: for each free column $t$, set $x_t = 1$, the other free variables to $0$, and $x_{P[k]} = -E[k, t]$. See [nullspace computation](/nullspace-computation/) and Cohen, Section 2.3.1.
- **Over $\mathbb{Z}/p\mathbb{Z}$.** The same loop, with inverses modulo $p$, is [Gaussian elimination modulo p](/gaussian-elimination-modular/). Over $\mathbb{F}_2$, rows packed into machine words give [bitset Gaussian elimination](/bitset-gaussian-elimination/).
- **Fraction-free form.** A Gauss-Jordan version of the [Bareiss algorithm](/bareiss-algorithm/) keeps integer entries and divides each update exactly by the previous pivot; it returns $\det A \cdot E$ for a nonsingular $A$ in place of $E$.
- **Fast reduced echelon form.** Over a field, the reduced row echelon form, the rank and the inverse can all be computed in $O(mnr^{\omega - 2})$ field operations by block recursive methods (Storjohann's thesis, Chapter 2).

## When to use it

Use Gauss-Jordan when the reduced form itself is the goal: to compare row spaces, to read the pivot columns, to get a nullspace basis, or to invert a small or medium matrix over an exact field. For a single system with a square matrix, Gaussian elimination with back substitution is cheaper. For integer or rational input of moderate size, use the [Bareiss algorithm](/bareiss-algorithm/), multimodular methods or [Dixon's p-adic lifting](/dixon-p-adic-lifting/), because rational arithmetic spends most of its time in gcds.

## Pitfalls

- **Testing invertibility by the shape.** INVERSE must check that the pivots are exactly the columns $0, \dots, n-1$. A pivot in the right half means that $A$ is singular, even though $[A \mid I]$ always has rank $n$.
- **Forgetting the rows above.** Clearing only below the pivot gives an echelon form but not the reduced one, and the right half of $[A \mid I]$ is then not $A^{-1}$.
- **Scaling after elimination.** If the row operations use the unscaled pivot row, the multiplier must be $A[i, j] / A[r, j]$; mixing the two conventions gives wrong rows.
- **Floating point.** Testing $A[i, j] \ne 0$ on floats is unreliable. The code on this page is for exact fields only.
- **Integer division.** In a language without exact rationals, `a / b` on integers truncates or gives a float. Use a rational type, or work modulo a prime.

## Implementations

## History

The method is named after Carl Friedrich Gauss and the German geodesist Wilhelm Jordan, who described it in his handbook of surveying in 1888, for the normal equations of least squares. The Belgian priest B.-I. Clasen published the same method independently in the same year. Althoen and McLaughlin traced the history, and in particular showed that the Jordan of the name is Wilhelm Jordan and not the mathematician Camille Jordan. Grcar describes how the elimination methods of the geodesists were named after Gauss.

## References
