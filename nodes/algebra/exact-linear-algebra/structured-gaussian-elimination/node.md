---
tag: FPBFNE
kind: algorithm
slug: structured-gaussian-elimination
name: Structured Gaussian elimination
aliases: [structured elimination, LaMacchia-Odlyzko elimination, intelligent Gaussian elimination, sparse matrix filtering]
area: algebra/exact-linear-algebra
level: research
summary: Eliminates sparse columns and rows first to shrink a large sparse system before dense solving, used in integer factorization.
solves: [linear-system-solving]
model: algebraic-computation-tree
complexity:
  vars: {m: the number of rows, n: the number of columns, w: the number of nonzero entries, h: the number of heavy columns at the end, b: the maximum binary length of an entry of an integer input}
  time: {worst: "O(m + n + w (h + 1) + m h min(m, h))"}
  space: {extra: O(w + m h)}
  field_operations: {worst: "O(w (h + 1) + m h min(m, h))"}
  bit_operations: {worst: "O((w (h + 1) + m h min(m, h)) n^2 (b + log n)^2)"}
properties: {deterministic: true, in_place: false, recursive: false}
prereqs: [gaussian-elimination, sparse-matrix, pivot]
see_also: [wiedemann-algorithm, block-lanczos-algorithm, block-wiedemann-algorithm, linear-system-modulo-2, fill-in, minimum-degree-ordering, index-calculus, quadratic-sieve]
sources:
  - paper: doi:10.1007/3-540-38424-3_8
    title: Brian A. LaMacchia and Andrew M. Odlyzko, Solving large sparse linear systems over finite fields, Advances in Cryptology, CRYPTO '90, Lecture Notes in Computer Science 537, Springer, 1991
    locator: pp. 109 to 133 (structured Gaussian elimination with heavy and light columns, and its comparison with Lanczos, conjugate gradient and Wiedemann on discrete logarithm systems)
  - paper: "Andrew M. Odlyzko, Discrete logarithms in finite fields and their cryptographic significance, Advances in Cryptology, EUROCRYPT '84, Lecture Notes in Computer Science 209, Springer, 1985"
    locator: pp. 224 to 314 (the sparse systems of index calculus, and the first proposal to pivot on sparse columns and keep the fill-in in a few dense columns)
  - paper: "Carl Pomerance and J. W. Smith, Reduction of huge, sparse matrices over finite fields via created catastrophes, Experimental Mathematics 1(2), 1992"
    locator: pp. 89 to 94 (declaring heavy columns until the light part collapses, and its use for factoring matrices)
  - paper: "Stefania Cavallar, Strategies in filtering in the number field sieve, Algorithmic Number Theory, ANTS-IV, Lecture Notes in Computer Science 1838, Springer, 2000"
    locator: pp. 209 to 231 (removing singletons and excess rows and merging, the filtering stage before block Lanczos or block Wiedemann)
  - paper: doi:10.1007/BF01459082
    title: John D. Dixon, Exact solution of linear equations using p-adic expansions, Numerische Mathematik 40, 1982
    locator: pp. 137 to 141 (the exact solution of the remaining dense system over Q)
---

Structured Gaussian elimination shrinks a large sparse linear system before it is solved. It pivots on the sparse part of the matrix with rules that never create fill-in outside a small set of *heavy* columns, and it grows that set only when it has to. What remains is a system in the heavy unknowns alone, often a small fraction of the original, which is solved by ordinary dense [Gaussian elimination](/gaussian-elimination/); the other unknowns then follow by back-substitution. It was designed by Odlyzko, LaMacchia and Pomerance for the sparse systems of [index calculus](/index-calculus/) and of factoring algorithms such as the [quadratic sieve](/quadratic-sieve/), where a few columns (small primes) are dense and most columns (large primes) have only a handful of entries. This page treats exact arithmetic over a field, usually $\mathbb{F}_p$ or $\mathbb{F}_2$.

## In plain words

Plain elimination on a huge sparse table is a bad idea: subtracting one row from another fills empty places with numbers, and soon the table is full and too large to store.

The structured method splits the unknowns into light ones, which appear in few equations, and heavy ones. It looks for an equation that mentions only one light unknown; that equation expresses this unknown through heavy ones, so it can be used to remove the unknown from every other equation, and new numbers appear only in the heavy columns. An unknown that appears in a single equation is even easier: put that equation aside for the end. When no such step is possible, the busiest light unknown is declared heavy. At the end only a small dense system in the heavy unknowns is left; solve it, then recover the rest one by one.

## The problem

**Notation.** $K$ is a field given exactly, such as $\mathbb{F}_p$ or $\mathbb{Q}$. $A$ is an $m \times n$ matrix over $K$ stored sparsely, with $w$ nonzero entries, and $c \in K^m$. During the algorithm, the columns are split into *light* columns $L$, *heavy* columns $H$, and columns already eliminated; the rows into *active* rows and pivot rows set aside. The *weight* of a column is its number of nonzero entries in active rows. $h$ is the size of $H$ at the end. Costs are given in *field operations* (the algebraic computation tree model) and in *bit operations* over $\mathbb{Q}$ with schoolbook arithmetic, where $b$ bounds the binary length of the entries of an integer $A$ and $c$; over $\mathbb{F}_p$ each operation costs $O(\log^2 p)$.

**Input.** The sparse matrix $A$ and the vector $c$.

**Output.** One solution $x$ of $A x = c$, with free unknowns set to $0$, or the report that the system is inconsistent.

## The algorithm

```pseudo id=main
STRUCTURED-GE(A, c)                       ▷ A is m × n sparse over a field K
L1  H ← ∅; L ← all columns; all rows active; P ← empty list of pivots
L2  while L ≠ ∅ do
L3      if a column j ∈ L has weight 0 then remove j from L; x_j ← 0                     ▷ free unknown
L4      else if a column j ∈ L has weight 1, in row r, then append (r, j) to P; set row r aside; remove j from L
L5      else if an active row r has exactly one entry in L, in column j, then
            append (r, j) to P; set row r aside; remove j from L
            for each active row i with a_ij ≠ 0: (row i, c_i) ← (row i, c_i) − (a_ij / a_rj)(row r, c_r)
L6      else move the column of L with the largest weight to H
L7  solve the active rows, which now involve only columns of H, by dense elimination; if inconsistent return "inconsistent"
L8  for (r, j) in P, last to first: x_j ← (c_r − Σ_{k ≠ j} a_rk x_k) / a_rj
L9  return x
```

The key point is line L5: row $r$ has no light entry other than $j$, and it has no entry in an eliminated column (those have been cleared from all active rows), so it lives in column $j$ and the heavy columns. Subtracting multiples of it clears column $j$ and changes only heavy entries: the light part of the matrix never fills in. Line L4 needs no subtraction at all, because column $j$ has no other entry; row $r$ is kept to compute $x_j$ at the end, after the other unknowns of that row are known. Line L6 is the only place where a choice of strategy enters; moving the heaviest column to $H$ lowers the light count of as many rows as possible, and new rows with one light entry appear. Line L8 runs through the pivots backwards: each pivot row mentions, besides $x_j$, only heavy unknowns and unknowns pivoted later, which are already known.

## Example

Over $\mathbb{Q}$, take five equations in five unknowns:

$$\begin{aligned} R_0: \; & x_0 + x_1 = 3, & R_1: \; & x_1 + x_2 + x_4 = 10, & R_2: \; & x_2 + x_3 = 7, \\ R_3: \; & x_0 + x_3 + x_4 = 10, & R_4: \; & x_2 + x_4 = 8. \end{aligned}$$

All column weights are $2$ or $3$ and every row has at least two light entries, so nothing applies until line L6.

| step | rule | action | effect |
|---|---|---|---|
| 1 | L6 | $x_2$ (weight 3, first of the heaviest) becomes heavy | $R_2$ and $R_4$ now have one light entry |
| 2 | L5 | pivot $(R_2, x_3)$ | $R_3 \leftarrow R_3 - R_2$: $x_0 - x_2 + x_4 = 3$ |
| 3 | L5 | pivot $(R_4, x_4)$ | $R_1 \leftarrow R_1 - R_4$: $x_1 = 2$; $R_3 \leftarrow R_3 - R_4$: $x_0 - 2 x_2 = -5$ |
| 4 | L5 | pivot $(R_1, x_1)$ | $R_0 \leftarrow R_0 - R_1$: $x_0 = 1$ |
| 5 | L5 | pivot $(R_0, x_0)$ | $R_3 \leftarrow R_3 - R_0$: $-2 x_2 = -6$ |
| 6 | L7 | dense system $-2 x_2 = -6$ | $x_2 = 3$ |
| 7 | L8 | back-substitution | $x_0 = 1$, $x_1 = 2$, $x_4 = 8 - 3 = 5$, $x_3 = 7 - 3 = 4$ |

Every new entry created in steps 2 to 5 lies in the heavy column $x_2$, and the dense part is a $1 \times 1$ system. The solution $(1, 2, 3, 4, 5)$ satisfies all five equations.

## Correctness

Every change to the active rows on line L5 adds a multiple of another row to a row, which is invertible, so the system of active rows together with the pivot rows set aside has the same solutions as $A x = c$. When the loop ends, every column is heavy, eliminated or free, and no active row has an entry outside $H$. A solution of the dense system on line L7 gives the heavy unknowns; the free unknowns are $0$ and appear in no active row; and line L8 makes each pivot row hold, using only unknowns that are already known. So the result satisfies all the transformed equations and hence $A x = c$. If the dense system is inconsistent, so is the original. The loop ends because each pass removes a column from $L$. The [full proof](proofs/correctness.md) gives the details.

## Complexity

**Field operations.** In line L5, column $j$ is light, and light columns never gain entries, so the rows touched by the pivot are original nonzeros of column $j$; each is updated in at most $h + 1$ places. Summed over all pivots this is at most $w (h + 1)$ multiplications and as many subtractions. Line L8 costs one operation per entry of a pivot row, which is $O(w + n h)$ and so $O(w (h + 1))$, since there are at most $w$ pivots: every pivoted column has an entry. The dense system has at most $m$ rows and $h$ columns, and elimination costs $O(m h \min(m, h))$. So the total is $O(w (h + 1) + m h \min(m, h))$ field operations; this is proved.

**Bookkeeping.** With a counter of active entries per column and of light entries per row, queues of columns of weight $0$ or $1$ and of rows with one light entry, and a bucket array of light columns by weight (weights of light columns only decrease, so the pointer to the heaviest bucket moves one way), the choices on lines L3 to L6 cost $O(m + n + w)$ in total. The reference implementation simply scans, which is quadratic but fine for tests.

**Bit operations over $\mathbb{Q}$.** The algorithm is Gaussian elimination with a particular pivot order, so by Sylvester's identity every entry of an active row after some pivots is a quotient of two minors of $(A \mid c)$ of order at most $\min(m, n) + 1$, and by the [Hadamard bound](/hadamard-bound/) these have $O(n (b + \log n))$ binary digits. Each operation then costs $O(n^2 (b + \log n)^2)$ with schoolbook arithmetic and reduced fractions, which gives the bound in the front matter; this is proved. Over $\mathbb{F}_p$ there is no growth and the bit cost is $O((w (h + 1) + m h \min(m, h)) \log^2 p)$. In practice the reduction is run modulo $p$ or $2$, and over $\mathbb{Q}$ the dense part is better solved by [Dixon lifting](/dixon-p-adic-lifting/).

**The size of $h$.** In the worst case $h$ is close to $n$: for a dense matrix every row has many light entries, and line L6 moves columns to $H$ until only one light entry per row is left, so the algorithm degenerates into dense elimination. No useful general upper bound on $h$ is known; its value is an observation. The tests use $310$ random equations with $10$ entries in $300$ unknowns, column $j$ chosen with probability about $1/(j + 1)$, as for a factor base of primes; there the dense part has $39$ unknowns. With $500$ unknowns it has $54$ unknowns for $10$ entries per row and $117$ for $15$. LaMacchia and Odlyzko reported large reductions on real discrete logarithm systems, leaving dense parts small enough to be solved in memory.

**Space.** The sparse rows, which only grow in the heavy columns: $O(w + m h)$.

## Properties

- **Exact and deterministic.** With a fixed tie-breaking rule, the same input gives the same pivots and the same answer.
- **Fill-in is confined.** New nonzeros appear only in heavy columns, which are stored densely in the final step.
- **A front end.** It does not solve the system by itself; it reduces it to a dense system on $h$ unknowns, or, when stopped early, to a smaller sparse system for an iterative method.
- **Works for any shape.** Overdetermined, underdetermined, singular or inconsistent systems are all handled; the dense step decides consistency.

## Variants and improvements

- **Excess rows.** Factoring and discrete logarithm matrices have more rows than needed. Deleting the heaviest rows, or rows containing many light entries, keeps the system determined while making more columns singletons; LaMacchia and Odlyzko interleave this with the steps above.
- **Created catastrophes.** Pomerance and Smith (1992) declare columns heavy in larger batches, which after a while makes the light part collapse all at once, with a remaining dense part of predictable size.
- **Filtering and merging.** In the number field sieve, the matrix is first filtered (singletons and cliques removed, duplicate relations deleted), and then light columns of weight $2$ or $3$ are merged by adding rows in the way that creates the least fill (Cavallar, 2000). The result is passed to [block Lanczos](/block-lanczos-algorithm/) or [block Wiedemann](/block-wiedemann-algorithm/) rather than to dense elimination.
- **Over $\mathbb{F}_2$.** Factoring needs vectors of the left kernel of a matrix over $\mathbb{F}_2$. The same rules apply with rows as bit vectors and the dense part handled by [bitset elimination](/bitset-gaussian-elimination/) or the table lookup methods for [linear systems modulo 2](/linear-system-modulo-2/).
- **Markowitz-type orderings.** Numerical sparse solvers choose pivots by the Markowitz cost $(r_i - 1)(c_j - 1)$ or by a [minimum degree ordering](/minimum-degree-ordering/) to limit [fill-in](/fill-in/). Structured elimination is cruder: it allows fill-in only in chosen columns, which suits exact arithmetic over finite fields where stability does not matter.
- **Hybrid with iterative methods.** Stop the reduction when further steps would make the matrix too dense, and solve the rest with [Wiedemann's method](/wiedemann-algorithm/), whose cost is proportional to the number of nonzeros times the dimension.

## When to use it

Use it as the first stage for very large sparse systems over finite fields with a skewed column distribution: the linear algebra of index calculus, of the quadratic and number field sieves, and of other relation-collection methods. It is also a good exact solver on its own when the matrix is close to triangular after permutation, since then $h$ stays small. For a matrix with no structure, $h$ approaches $n$, and either dense elimination or an iterative black box method is better.

## Pitfalls

- **Pivoting with rows that have several light entries.** Using such a row to eliminate creates fill-in in light columns, which destroys sparsity quickly; only line L5 rows are safe.
- **Forgetting the right-hand side.** Every row operation of line L5 must also be applied to $c$, and the pivot rows set aside must keep their right-hand side for line L8.
- **Back-substituting in the wrong order.** Rows set aside by line L4 can contain light unknowns pivoted later, so line L8 must run from the last pivot to the first.
- **Declaring too few heavy columns.** Moving one column at a time is slow on huge matrices; production code moves a batch and recomputes weights.
- **Expecting a guaranteed reduction.** The final $h$ depends on the matrix; there is no worst-case guarantee better than $h \le n$.

## Implementations

## History

Andrew Odlyzko suggested in his 1984 survey on discrete logarithms that the index calculus systems could be reduced by pivoting on sparse columns and keeping the fill in a few dense columns. Brian LaMacchia and Odlyzko developed the method and measured it against Lanczos, conjugate gradient and Wiedemann on discrete logarithm systems at CRYPTO 1990, and Carl Pomerance and J. W. Smith described the variant with created catastrophes in 1992. With the number field sieve, its rules became the filtering stage before block Lanczos and block Wiedemann, studied in detail by Stefania Cavallar (2000).

## References
