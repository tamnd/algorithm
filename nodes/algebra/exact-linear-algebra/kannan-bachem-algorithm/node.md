---
tag: XTZT1P
kind: algorithm
slug: kannan-bachem-algorithm
name: Kannan-Bachem algorithm
aliases:
- polynomial-time Hermite normal form
- Kannan-Bachem Hermite normal form algorithm
area: algebra/exact-linear-algebra
level: research
summary: First polynomial-time algorithm for the Hermite normal form, keeping numbers small by reducing a growing Hermite form after every step.
solves: [hermite-normal-form]
model: algebraic-computation-tree
complexity:
  vars: {m: the number of rows, n: the number of columns, r: the rank, b: the maximum binary length of an entry}
  time: {worst: O(m r^2 (n + m))}
  space: {extra: O((n + m) r)}
  ring_operations: {worst: O(m r^2 (n + m))}
  bit_operations: {worst: O(m r^8 (n + m) (b + log r)^2)}
properties: {deterministic: true, in_place: false, recursive: false}
prereqs: [hermite-normal-form, extended-euclidean-algorithm, unimodular-matrix, hadamard-bound]
see_also: [smith-normal-form, bareiss-algorithm, linear-diophantine-system, echelon-form, lattice-basis, lll-algorithm, dixon-p-adic-lifting, cramers-rule]
sources:
  - paper: doi:10.1137/0208040
    title: Ravindran Kannan and Achim Bachem, Polynomial algorithms for computing the Smith and Hermite normal forms of an integer matrix, SIAM Journal on Computing 8(4), 1979
    locator: pp. 499 to 507 (the Hermite form of the leading principal submatrices in turn, with off-diagonal reduction after each gcd step, and the polynomial bounds; the Smith form algorithm built on it)
  - book: isbn:9783540556404
    title: Henri Cohen, A Course in Computational Algebraic Number Theory, Graduate Texts in Mathematics 138
    locator: Section 2.4.2, The Hermite normal form (the growth of the naive algorithm, and the modular Algorithm 2.4.8 that avoids it)
  - paper: "Paul D. Domich, Ravindran Kannan and Leslie E. Trotter, Hermite normal form computation using modulo determinant arithmetic, Mathematics of Operations Research 12(1), 1987"
    locator: pp. 50 to 59 (the same elimination carried out modulo a multiple of the determinant)
  - paper: "Arne Storjohann, Algorithms for Matrix Canonical Forms, PhD thesis, ETH Zurich, 2000"
    locator: the chapter on the Hermite form of integer matrices (later algorithms with fast matrix multiplication and the history of the bounds)
  - paper: "Xin Gui Fang and George Havas, On the worst-case complexity of integer Gaussian elimination, ISSAC 1997"
    locator: pp. 28 to 31 (exponential growth of the numbers in a naive integer elimination)
---

The Kannan-Bachem algorithm computes the [Hermite normal form](/hermite-normal-form/) of an integer matrix with a proved polynomial bound on the size of every intermediate number. The naive method, which runs the Euclidean algorithm down each column, is correct, but its numbers can grow exponentially in the size of the matrix. Kannan and Bachem kept a part of the matrix in Hermite normal form at all times, enlarged it one row and column at a time, and reduced the entries above the pivots after every gcd step. Since that part is always a Hermite normal form, which is bounded by determinants, no number can grow far. This page presents the method in a row-insertion form that handles any shape and rank, and returns the unimodular transform as well.

Notation: $A$ is an $m \times n$ matrix over $\mathbb{Z}$ with rows $a_1, \dots, a_m$, of rank $r$. $B \ge 1$ bounds the absolute values of the entries and $b$ is their maximum binary length. $L(S)$ is the lattice spanned by the rows $S$, and $\operatorname{lead}(w)$ is the column of the first nonzero entry of a row $w$. The form is the row form $H = UA$ of the [Hermite normal form](/hermite-normal-form/) page, with $U$ [unimodular](/unimodular-matrix/). The algorithm uses only integer ring operations and exact integer division by pivots; bit costs assume schoolbook arithmetic, and $\omega$ is the exponent of matrix multiplication.

## In plain words

The goal is a staircase form of a table of whole numbers, using only row operations that can be undone with whole numbers. The simple way creates numbers that can grow far beyond what the answer needs. This method keeps a finished staircase for the rows seen so far. Each new row is merged into it with greatest common divisor steps, and then the rows are cleaned again so that every number above a step is smaller than that step. A finished staircase cannot hold huge numbers, so the numbers stay small.

## The problem

Input: an $m \times n$ integer matrix $A$. Output: the Hermite normal form $H$ of $A$ and a unimodular $U$ with $UA = H$. $H$ has $r$ nonzero rows in echelon form with positive pivots, every entry above a pivot lies in $[0, \text{pivot})$, and the zero rows come last. The cost of interest is the number of bit operations, which depends on how large the numbers become.

## The algorithm

The stored rows $h_1, \dots, h_s$ have pivot columns $c_1 < \cdots < c_s$. To get $U$, run the algorithm on the rows of $[A \mid I_m]$ with $\operatorname{lead}$ and the reductions looking only at the first $n$ columns; the rows set aside as zero give the last rows of $U$.

```pseudo id=main
KANNAN-BACHEM(A)                             ▷ A is m × n over Z
L1  H ← empty list of rows h_1, …, h_s with pivot columns c_1 < … < c_s
L2  for t ← 1 to m do
L3      w ← a_t
L4      for k ← 1 to s do
L5          if w = 0 or lead(w) < c_k then break
L6          if lead(w) = c_k then
L7              (g, x, y) ← XGCD(h_k[c_k], w[c_k])        ▷ g = x h_k[c_k] + y w[c_k] > 0
L8              (h_k, w) ← (x h_k + y w, (h_k[c_k]/g) w − (w[c_k]/g) h_k)
L9      if w ≠ 0 then
L10         make the leading entry of w positive; insert w into H before h_k
L11     for l ← s − 1 down to 1 do
L12         for k ← l + 1 to s do
L13             h_l ← h_l − ⌊h_l[c_k] / h_k[c_k]⌋ · h_k
L14 return H, followed by m − s zero rows
```

Line L8 is a $2 \times 2$ row operation with determinant $1$. It replaces the pivot $h_k[c_k]$ by $g = \gcd(h_k[c_k], w[c_k])$ and clears $w[c_k]$. Line L5 stops when $w$ starts before the next pivot column, which is then the place where $w$ becomes a new pivot row. Lines L11 to L13 reduce the stored rows from the bottom up, so that each row is reduced against rows that are already final. The XGCD is the [extended Euclidean algorithm](/extended-euclidean-algorithm/).

The original 1979 algorithm works on a nonsingular square matrix, permuted so that its leading principal minors are nonzero. Step $i$ takes the leading $i \times i$ block, already in Hermite form, adds the next row and column, clears the new column with gcd steps against the diagonal, and reduces the off-diagonal entries after each gcd step. The row-insertion form here has the same invariant, a growing Hermite form, but adds whole rows and needs no assumption on the minors.

## Example

Take $M$ with rows $(2, 1, 0)$, $(1, 3, 1)$, $(0, 1, 4)$.

| $t$ | gcd steps | stored rows after reduction |
| --- | --- | --- |
| 1 | none; $w = (2, 1, 0)$ is inserted | (2, 1, 0) |
| 2 | column 1: $\gcd(2, 1) = 1$ with $x = 0$, $y = 1$; $h_1 = (1, 3, 1)$, $w = 2(1, 3, 1) - (2, 1, 0) = (0, 5, 2)$ | (1, 3, 1), (0, 5, 2) |
| 3 | column 2: $\gcd(5, 1) = 1$ with $x = 0$, $y = 1$; $h_2 = (0, 1, 4)$, $w = 5(0, 1, 4) - (0, 5, 2) = (0, 0, 18)$ | (1, 0, 7), (0, 1, 4), (0, 0, 18) |

In step $2$ the reduction leaves $(1, 3, 1)$ alone, since $\lfloor 3/5 \rfloor = 0$. In step $3$, $w = (0, 1, 4)$ starts in column 2, after $c_1 = 1$, so the loop skips $h_1$. The reduction then takes $h_1 = (1, 3, 1)$ to $(1, 3, 1) - 3(0, 1, 4) = (1, 0, -11)$, and then to $(1, 0, -11) + (0, 0, 18) = (1, 0, 7)$, since $\lfloor -11/18 \rfloor = -1$. The result is the Hermite normal form $H = \begin{pmatrix} 1 & 0 & 7 \\ 0 & 1 & 4 \\ 0 & 0 & 18 \end{pmatrix}$, with $U = \begin{pmatrix} 1 & -1 & 2 \\ 0 & 0 & 1 \\ 1 & -2 & 5 \end{pmatrix}$ and $\det U = 1$. The product of the pivots is $18 = \det M$. The tests check this run.

## Correctness

The invariant is that, after row $t$ has been processed, the stored rows are in Hermite form and span $L(a_1, \dots, a_t)$. Line L8 has determinant $1$, so it keeps the lattice of the stored rows and $w$, and it keeps the leading columns of the stored rows, because $h_k$ and $w$ are both zero before $c_k$ when it runs. After it, $w$ is zero at $c_k$, so $w$ moves right past the pivot columns until it is zero or starts at a new column, where line L10 inserts it. The bottom-up reduction puts each entry above a pivot into $[0, \text{pivot})$ without disturbing the pivots or the entries reduced before. At the end, the stored rows are independent and in Hermite form, so there are $r$ of them and $H$ is the Hermite normal form of $A$; all row operations were unimodular, so $UA = H$ with $\det U = \pm 1$. The [full proof](proofs/correctness.md) also proves the size bound below.

## Complexity

**Operations.** Insertion $t$ runs at most $s \le r$ gcd steps of line L8 and at most $s(s-1)/2$ reductions of line L13, each on rows of length $n + m$ when $U$ is computed. The total is $O(m r^2 (n + m))$ integer operations, plus $O(m r)$ extended gcds. For a nonsingular $n \times n$ matrix this is $O(n^4)$.

**Sizes.** After each insertion the stored rows are the Hermite normal form of $a_1, \dots, a_t$. By the bound proved in the [full proof](proofs/correctness.md), every entry of the Hermite normal form of a rank-$r$ matrix is at most $r \cdot r^{r/2} B^r$, so it has $O(r(b + \log r))$ bits. Within one insertion, each step multiplies the largest entry of the changed row by at most $2S + 1$, where $S$ is that bound, so the numbers in $H$ have $O(r^3 (b + \log r))$ bits at worst. With schoolbook arithmetic this gives the proved, and crude, bound of $O(m r^8 (n + m) (b + \log r)^2)$ bit operations. The point of the 1979 paper was that such a polynomial bound exists at all.

**Observed.** On random $n \times n$ matrices with entries in $[-99, 99]$, the largest number in the first $n$ columns, measured after each gcd step, had $67$, $140$ and $229$ bits for $n = 10$, $20$, $30$, about the size of the final form ($67$, $140$ and $228$ bits). The naive column-by-column Euclidean elimination without reduction reached $671$, $19381$ and $34124$ bits on the same matrices. These are observations, not bounds.

**Better bounds.** Working modulo a multiple of the determinant (Domich, Kannan and Trotter 1987) keeps every number below the determinant and gives $O(n^3)$ operations on numbers of $O(n(b + \log n))$ bits for a nonsingular $n \times n$ matrix. Storjohann's algorithms bring the cost close to $n^\omega$ operations on such numbers; see the [Hermite normal form](/hermite-normal-form/) page.

**Space.** The stored rows take $O(r(n + m))$ numbers, and the zero rows set aside take $O((m - r) m)$ more for $U$.

## Properties

- **A Hermite form at all times.** After each row, the stored rows are the unique Hermite normal form of the rows seen so far. This is the invariant that bounds the numbers.
- **The transform comes for free.** Running on $[A \mid I_m]$ gives $U$. For a nonsingular square $A$, $U = H A^{-1}$ is unique and bounded by [Cramer's rule](/cramers-rule/). For a matrix with dependent rows, the kernel rows of $U$ are not reduced and the analysis does not bound them.
- **Rank and pivots.** The number of stored rows is the rank, and the pivot columns are the first independent columns. For a nonsingular square matrix, the product of the pivots is $|\det A|$.
- **Deterministic**, with integer operations and exact divisions only.

## Variants and improvements

- **The original form.** Kannan and Bachem handle a nonsingular square matrix by growing leading principal submatrices, with column operations, and reduce after every gcd step rather than after every row.
- **Smith normal form.** Alternating the Hermite form of $A$ and of $A^T$ converges to the [Smith normal form](/smith-normal-form/), and Kannan and Bachem bounded the number of rounds, which gave the first polynomial Smith form algorithm.
- **Modular arithmetic.** For a full-rank lattice $L$ with a known multiple $D$ of its determinant, $D \mathbb{Z}^n \subseteq L$, so all the work can be done modulo $D$, as in Cohen's Algorithm 2.4.8.
- **Lattice reduction.** A Hermite form is a valid but often skewed basis. To get short vectors, follow it with the [LLL algorithm](/lll-algorithm/).
- **Cheaper gcd choices.** The cofactors $x$ and $y$ of line L7 are not unique. Choosing small ones, or pivoting on the row with the smallest entry, reduces the growth in practice; Havas, Majewski and Matthews studied such heuristics for the transform.

## When to use it

Use the Kannan-Bachem method, or its row-insertion form here, for the Hermite normal form of small or medium integer matrices of any shape and rank, when a transform matrix is wanted and a simple method with a guaranteed polynomial bound is enough. For large nonsingular matrices, modular methods are faster. For a lattice basis with short vectors, use LLL instead.

## Pitfalls

- **No reduction.** Running the gcd steps without reducing the entries above the pivots gives a correct echelon form, but the numbers can explode, as the observed sizes above show. The reduction is the algorithm.
- **Reducing in the wrong order.** Reducing a row against a row that is not yet reduced gives the right form in the end, but loses the size bound. Go from the bottom up.
- **Floor division.** The reduction must use the floor, so that the result lies in $[0, \text{pivot})$. In C, `/` truncates toward zero and gives negative remainders for negative entries.
- **A gcd step on a row that starts earlier.** If $w$ starts before the pivot column $c_k$, combining it with $h_k$ puts nonzero entries in front of $h_k$'s pivot and breaks the echelon form. Line L5 inserts $w$ instead.
- **Signs.** The extended gcd can return a negative $g$ when an input is negative. Normalize so that the new pivot is positive.
- **Column versus row convention.** Cohen and many papers use columns, $AU = H$, with lower triangular $H$. Transpose before comparing results.

## Implementations

## History

Ravindran Kannan and Achim Bachem published the algorithm in 1979, as the first proof that the Hermite and Smith normal forms can be computed in polynomial time; the question came from integer programming, where these forms describe the integer solutions of linear equations. Before, the known methods, which go back to Hermite's reduction of 1851, were correct but had no bound on their intermediate numbers. Domich, Kannan and Trotter replaced the size argument by arithmetic modulo the determinant in 1987, and later work by Hafner and McCurley, Storjohann and others brought the cost close to that of matrix multiplication. Fang and Havas showed in 1997 that a naive integer elimination can indeed produce numbers of exponential size.

## References
