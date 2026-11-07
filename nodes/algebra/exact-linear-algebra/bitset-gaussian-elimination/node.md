---
tag: KRD18F
kind: technique
slug: bitset-gaussian-elimination
name: Gaussian elimination with bitset optimization
aliases:
- Gauss improved implementation
- Gaussian elimination over GF(2) with bitsets
- word-packed Gaussian elimination
area: algebra/exact-linear-algebra
level: core
summary: Speeds up Gaussian elimination over the field of two elements by packing rows into machine words, cutting the cost by the word size.
prereqs: [gaussian-elimination-modular, bit-set, bitwise-operations]
see_also: [linear-system-modulo-2, xor-gaussian-elimination, xor-sat, four-russians-method, gauss-jordan-elimination, quadratic-sieve, word-ram, block-lanczos-algorithm]
sources:
  - url: "https://cp-algorithms.com/linear_algebra/linear-system-gauss.html"
    title: cp-algorithms, Gauss method for solving system of linear equations
    locator: the section on systems modulo 2, with rows stored as bitsets
  - book: isbn:9780387887562
    title: Gregory V. Bard, Algebraic Cryptanalysis, Springer, 2009
    locator: the chapters on dense linear algebra over GF(2) and the Method of Four Russians for inversion (M4RI)
  - paper: doi:10.1145/1644001.1644010
    title: Martin Albrecht, Gregory Bard and William Hart, Algorithm 898, Efficient multiplication of dense matrices over GF(2), ACM Transactions on Mathematical Software 37(1), 2010
    locator: the description of the M4RI library, its packed row format and its use of the Method of Four Russians
  - url: "https://github.com/malb/m4ri"
    title: The M4RI library for dense linear algebra over GF(2)
    locator: the library documentation (packed rows, M4RI elimination and PLE decomposition)
---

Over the field $\mathbb{F}_2 = \{0, 1\}$, an entry is one bit, adding two rows is a bitwise XOR, and the only nonzero pivot is $1$, so no row ever needs scaling. Bitset Gaussian elimination stores each row of an $m \times n$ matrix as $\lceil n/w \rceil$ machine words of $w$ bits and clears a column in a row with $\lceil n/w \rceil$ XOR instructions in place of $n$ separate bit operations. The field-operation count of [Gaussian elimination](/gaussian-elimination/) does not change, but on a [word RAM](/word-ram/) the running time drops from $O(mn \min(m, n))$ to $O(mn \min(m, n)/w + mn)$, a factor of $64$ on current machines, and the memory drops by the same factor. The technique solves [linear systems modulo 2](/linear-system-modulo-2/), computes ranks and nullspaces over $\mathbb{F}_2$, and runs inside SAT solvers and factoring programs.

Notation: $A$ is an $m \times n$ matrix over $\mathbb{F}_2$, $n$ is also the size of a square matrix, $w$ is the word size in bits, and $\oplus$ is bitwise XOR. Column $j$ of a row is bit $j$ of the row's bitset. In the tables, a row is written as a string of bits with column $0$ on the left.

## In plain words

Over the numbers 0 and 1 with arithmetic modulo 2, adding two rows of a matrix is the same as XOR of their bits. A computer word holds 64 bits and can XOR all of them in one step. So store each row as a sequence of words, one bit per entry, and add rows word by word. Elimination then does the usual steps, but each row step costs about one sixty-fourth of the plain cost. Nothing else changes: find a row with a 1 in the column, swap it up, and XOR it into every other row with a 1 there.

## When it applies

- **The field is $\mathbb{F}_2$.** The method needs a row update that is a word-wide logical operation. Over $\mathbb{F}_2$, $A[i, \cdot] \leftarrow A[i, \cdot] - f \cdot A[r, \cdot]$ with $f = 1$ is a XOR, and with $f = 0$ it is nothing. For $\mathbb{F}_3$ and other small fields, packed representations exist, but they need several logical operations per update; for a large prime, use [modular elimination](/gaussian-elimination-modular/) with one residue per word.
- **The matrix is dense.** When most rows have only a few ones, sparse methods such as [structured Gaussian elimination](/structured-gaussian-elimination/), [block Lanczos](/block-lanczos-algorithm/) or [block Wiedemann](/block-wiedemann-algorithm/) do better, because they never store the fill-in.
- **The cost model is the word RAM.** In the bit model a XOR of two $w$-bit words is still $w$ bit operations. The gain is parallelism inside a word, which real processors have and which the bit-operation count does not show.

## The template

The pseudocode indexes rows and columns from $0$. `row[i]` is a bitset of $n$ bits, and `BIT(x, j)` reads bit $j$. It computes the reduced row echelon form, which for an augmented matrix gives the solution directly.

```pseudo id=main
F2-ELIM(row, m, n)                           ▷ row[0..m−1] are bitsets of n bits
L1  r ← 0, P ← empty list
L2  for j ← 0 to n − 1 do
L3      q ← the least i with r ≤ i < m and BIT(row[i], j) = 1, or NONE
L4      if q = NONE then continue with the next j
L5      swap row[r] and row[q]
L6      for each i ≠ r with BIT(row[i], j) = 1 do
L7          row[i] ← row[i] ⊕ row[r]              ▷ ⌈n/w⌉ word XORs
L8      append j to P; r ← r + 1
L9  return row, r, P
```

There is no scaling step, because a nonzero pivot is $1$, and there is no multiplier, because $f = A[i, j]$ is $1$ for the rows that line L6 selects. To solve $Ax = b$, put $b$ in bit $n$ of each row and run the loop on the columns $0, \dots, n-1$. Row $k$ then reads $x_{P[k]} \oplus (\text{free variables}) = $ bit $n$, and the system has no solution exactly when some row is zero in the columns $0, \dots, n-1$ and has bit $n$ set. A consistent system of rank $r$ has $2^{n-r}$ solutions.

**Correctness.** The loop is [Gauss-Jordan elimination](/gauss-jordan-elimination/) over $\mathbb{F}_2$, where $c^{-1} = 1$ for the only nonzero $c$ and subtraction is XOR. Its correctness proof uses only field axioms.

**Cost.** Line L3 tests at most $m$ bits for each $j$, which is $O(mn)$ in total. For each of at most $\min(m, n)$ pivots, line L7 runs on at most $m - 1$ rows and costs $\lceil n/w \rceil$ word operations each. So the time is $O(mn \min(m, n)/w + mn)$ word operations and the space is $m \lceil n/w \rceil$ words. For a square $n \times n$ matrix this is $O(n^3/w)$. Since the pivot row is zero in the columns less than $j$, a code may start the XOR at word $\lfloor j/w \rfloor$; for a square matrix this brings the count to about $n^3/(2w)$ word XORs for the reduced form and $n^3/(3w)$ for the staircase form, but does not change the order. For $n = 10^4$, the matrix needs $12.5$ MB as bits, against $100$ MB with one byte per entry, and the elimination does about $n^3/w \approx 1.6 \cdot 10^{10}$ word XORs at most, in place of $10^{12}$ bit operations.

## Classic examples

**A system over $\mathbb{F}_2$.** Solve $x_0 + x_1 + x_3 = 1$, $x_1 + x_2 = 1$, $x_0 + x_2 + x_3 = 0$, $x_0 + x_1 + x_2 = 1$. The four rows of $[A \mid b]$, with bit $4$ for $b$, are the words `11011`, `01101`, `10110`, `11101` (column $0$ on the left).

| step | action | row 0 | row 1 | row 2 | row 3 |
| --- | --- | --- | --- | --- | --- |
| start | | 11011 | 01101 | 10110 | 11101 |
| $j = 0$ | pivot row 0; XOR it into rows 2 and 3 | 11011 | 01101 | 01101 | 00110 |
| $j = 1$ | pivot row 1; XOR it into rows 0 and 2 | 10110 | 01101 | 00000 | 00110 |
| $j = 2$ | pivot found in row 3; swap rows 2 and 3; XOR into rows 0 and 1 | 10000 | 01011 | 00110 | 00000 |
| $j = 3$ | no row $\ge 3$ has bit 3 | | | | |

The pivots are the columns $0, 1, 2$; column $3$ is free, and no row is `00001`, so the system is consistent. The rows read $x_0 = 0$, $x_1 + x_3 = 1$ and $x_2 + x_3 = 0$. With $x_3 = 0$ the solution is $(0, 1, 0, 0)$, and with $x_3 = 1$ it is $(0, 0, 1, 1)$, the $2^{4-3} = 2$ solutions that a search over all $16$ vectors also finds.

**The matrix step of factoring.** The [quadratic sieve](/quadratic-sieve/) and the [general number field sieve](/general-number-field-sieve/) collect relations whose exponent vectors modulo $2$ are the rows of a matrix over $\mathbb{F}_2$. A nonzero vector in the left nullspace picks a subset of relations whose product is a square. For small and medium factorizations, dense bitset elimination of this matrix is simple and fast; large ones use block Lanczos.

**XOR constraints.** SAT solvers with [XOR reasoning](/xor-gaussian-elimination/) keep the parity constraints as packed rows and run this elimination to detect conflicts and implied literals; see also [XOR-SAT](/xor-sat/).

**Maximum XOR of a subset.** A set of $k$-bit integers spans a subspace of $\mathbb{F}_2^k$. Eliminating the integers as rows, from the highest bit down, gives a basis in echelon form, and the greedy XOR of the basis rows that raise the current value gives the largest XOR of a subset. Each integer is one word, so each row step is one instruction.

**Rank of a code.** The dimension of a binary linear code is the rank of its generator matrix over $\mathbb{F}_2$, and a parity check matrix is a basis of the nullspace. Both come out of one elimination.

## Variations

- **Method of Four Russians (M4RI).** Take $k \approx \log_2 m$ pivot rows at a time, build a table of all $2^k$ XOR combinations of them in $O(2^k \cdot n/w)$ word operations, and then clear the $k$ columns in each other row with one table lookup and one row XOR, keyed by the $k$ bits of the row in those columns. This brings the cost to $O(n^3/(w \log n))$ for an $n \times n$ matrix. Bard named it the Method of Four Russians for inversion; it is the main elimination of the M4RI library. See the [Four Russians method](/four-russians-method/).
- **Fast matrix multiplication.** Block recursive PLE or LU decompositions reduce elimination to matrix multiplication over $\mathbb{F}_2$, which M4RI does with Strassen's algorithm and Four Russians tables at the leaves, in $O(n^{\omega}/w)$ word operations with $\omega = \log_2 7$ for Strassen.
- **Python and other languages with big integers.** A Python `int` is a bitset of any length, and `x ^ y` runs at C speed over the internal digits. A row update is one XOR of two integers, and `(x >> j) & 1` reads a bit. `std::bitset<N>` in C++ fixes the length at compile time.
- **Incremental basis.** For a stream of vectors, keep a basis indexed by the leading bit and reduce each new vector against it. This is the online form of the same loop and costs $O(n \cdot n/w)$ per vector.
- **Small fields other than $\mathbb{F}_2$.** Over $\mathbb{F}_3$ or $\mathbb{F}_4$, each entry takes two bit-planes, and a row update becomes a short sequence of AND, OR and XOR operations on the planes.

## Pitfalls

- **Bit order.** If column $0$ is the lowest bit, as on this page, then "the leading column" is the lowest set bit, not the highest. Mixing the two orders silently changes the echelon form and the pivot columns.
- **The right-hand side in the same word.** Keeping $b$ in bit $n$ is convenient, but the pivot search must stop at column $n - 1$, or the code may take a pivot in the right-hand side and miss the inconsistency.
- **Fixed-size bitsets.** `std::bitset<N>` with $N$ too small truncates the high columns without an error. A fixed $N$ larger than needed wastes the time of every XOR.
- **Sparse inputs.** A dense bitset XOR costs $n/w$ even when both rows have three ones, and the fill-in during elimination can make a sparse matrix dense. For the large sparse matrices of the number field sieve, dense elimination does not fit in memory.
- **Counting in the bit model.** The speedup is a factor $w$ in word operations only. A statement such as "elimination over $\mathbb{F}_2$ in $O(n^3/64)$ time" is a word-RAM statement with $w = 64$, not a smaller exponent.

## Exercises

1. Show that a consistent system over $\mathbb{F}_2$ of rank $r$ in $n$ unknowns has $2^{n-r}$ solutions. *Answer:* the solutions are one solution plus the nullspace, which has dimension $n - r$ and so $2^{n-r}$ elements.
2. How many 64-bit word XORs does F2-ELIM do at most on a $256 \times 256$ matrix if each XOR covers the whole row? *Answer:* at most $256$ pivots, $255$ other rows for each, and $4$ words for each row: $256 \cdot 255 \cdot 4 = 261120$.
3. Find the rank over $\mathbb{F}_2$ of the $3 \times 3$ matrix with rows `110`, `011`, `101`. *Answer:* $2$, since the third row is the XOR of the first two. Over $\mathbb{Q}$ the same matrix has determinant $2$ and rank $3$.

## References
