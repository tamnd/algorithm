---
tag: RNZB8E
kind: data-structure
slug: two-dimensional-fenwick-tree
name: Two-dimensional Fenwick tree
aliases:
- 2D Fenwick tree
- 2D BIT
area: data-structures/range-query-structures
level: advanced
summary: Fenwick tree nested over two dimensions for point updates and rectangle sums in O(log^2 n).
implements: [range-query-structure]
prereqs: [fenwick-tree, two-dimensional-range-sum-query, two-dimensional-prefix-sums]
see_also: [two-dimensional-segment-tree, range-sum-query-2d, inclusion-exclusion-principle, offline-orthogonal-range-counting, range-tree, coordinate-compression, range-update-range-query, dominance-counting]
sources:
  - paper: doi:10.1002/spe.4380240306
    title: "Peter M. Fenwick, A new data structure for cumulative frequency tables, Software: Practice and Experience 24(3) (1994), 327-336"
    locator: the binary indexed tree, the responsibility ranges given by the lowest set bit, and the update and prefix walks
  - url: https://cp-algorithms.com/data_structures/fenwick.html
    title: cp-algorithms, Fenwick Tree
    locator: section Finding sum in two-dimensional array
  - url: https://cses.fi/book/book.pdf
    title: Antti Laaksonen, Competitive Programmer's Handbook
    locator: Chapter 9, Section 9.2 (Binary indexed tree)
---

A two-dimensional Fenwick tree keeps an $n \times m$ matrix $M$ of numbers under point updates and answers the sum of any axis-aligned rectangle, both in $O(\log n \log m)$ time. It is a [Fenwick tree](/fenwick-tree/) over the rows whose items are Fenwick trees over the columns, all stored in one $(n + 1) \times (m + 1)$ table: the cell $F[i][j]$ holds the sum of $M$ over a block of $g(i)$ rows and $g(j)$ columns, where $g(x)$ is the lowest set bit of $x$. It solves the dynamic [two-dimensional range sum query](/two-dimensional-range-sum-query/), with each rectangle split into four corner sums by [inclusion and exclusion](/inclusion-exclusion-principle/), and it needs no more memory than the matrix itself.

## In plain words

Think of a grid of squares on a map, with a count in each square. One kind of request changes the count of one square, and another asks for the total of a rectangle of squares.

A one-dimensional Fenwick tree keeps, at each position, the total of a stretch that ends there, with lengths 1, 2, 4 and so on. Any start of the list is a few such stretches end to end, and a change touches only a few of them. The two-dimensional version does this in both directions. Each cell keeps the total of a block whose height and width are such powers of two. A corner of the map is a few rows of these blocks times a few columns of them. So each request touches only a few cells.

## The abstract type

The tree implements the [range query structure](/range-query-structure/) on a grid, for an abelian group such as the integers with $+$: `build(M)`, `add(r, c, δ)` for $M[r][c] \leftarrow M[r][c] + \delta$, and `query(r1, c1, r2, c2)` for the sum of the rectangle. The group must have inverses, because a rectangle is a signed sum of four corner sums, and it must be commutative, because the corner blocks are added in any order. For $\min$ or $\max$, use the [two-dimensional segment tree](/two-dimensional-segment-tree/).

## Representation

Indices inside the table are 1-based. For $x \ge 1$ let $g(x) = x \mathbin{\&} (-x)$, the lowest set bit of $x$, and let the *responsibility range* of $x$ be $R(x) = (x - g(x), x] = \{x - g(x) + 1, \ldots, x\}$. The table $F[0 \ldots n][0 \ldots m]$ has row 0 and column 0 unused.

**Invariant (F).** For all $1 \le i \le n$ and $1 \le j \le m$,

$$F[i][j] = \sum_{a \in R(i)} \sum_{b \in R(j)} M[a - 1][b - 1].$$

So $F[i][j]$ is the sum of a block of $g(i)$ rows and $g(j)$ columns whose bottom-right cell is $M[i - 1][j - 1]$. Row $i$ of $F$, read alone, is a one-dimensional Fenwick tree for the column sums of the rows $R(i)$.

Two facts about $R$ do all the work. They are proved in [the correctness proof](proofs/correctness.md).

- **Down chains.** For $x \ge 0$, the chain $x, x - g(x), \ldots$ down to 0 has ranges that split $\{1, \ldots, x\}$ into disjoint parts.
- **Up chains.** For $1 \le p \le N$, the indices $y \le N$ with $p \in R(y)$ are exactly the chain $p, p + g(p), \ldots$ while it stays at most $N$.

## Operations

```pseudo id=main
BUILD(M)                                                    ▷ M is n × m, 0-based
L1  for i ← 1 to n, j ← 1 to m do F[i][j] ← M[i − 1][j − 1]
L2  for i ← 1 to n do for j ← 1 to m do                     ▷ make each row a Fenwick tree
L3    if j + g(j) ≤ m then F[i][j + g(j)] ← F[i][j + g(j)] + F[i][j]
L4  for i ← 1 to n do                                       ▷ then combine whole rows
L5    if i + g(i) ≤ n then for j ← 1 to m do F[i + g(i)][j] ← F[i + g(i)][j] + F[i][j]

ADD(r, c, δ)                                                ▷ M[r][c] ← M[r][c] + δ
L6  i ← r + 1
L7  while i ≤ n do
L8    j ← c + 1
L9    while j ≤ m do
L10     F[i][j] ← F[i][j] + δ
L11     j ← j + g(j)
L12   i ← i + g(i)

PREFIX(r, c)                                                ▷ sum of M[0 .. r − 1][0 .. c − 1]
L13 s ← 0; i ← r
L14 while i > 0 do
L15   j ← c
L16   while j > 0 do
L17     s ← s + F[i][j]
L18     j ← j − g(j)
L19   i ← i − g(i)
L20 return s

QUERY(r1, c1, r2, c2)                                       ▷ sum of the rectangle
L21 return PREFIX(r2 + 1, c2 + 1) − PREFIX(r1, c2 + 1) − PREFIX(r2 + 1, c1) + PREFIX(r1, c1)
```

**Build** (lines L1 to L5) copies the matrix and then runs the linear-time build of a Fenwick tree twice. Lines L2 and L3 push each cell to its parent $j + g(j)$ in the same row, from left to right, which makes each row a Fenwick tree over the columns. Lines L4 and L5 push each whole row to its parent row $i + g(i)$, from top to bottom, which does the same over the rows. Each cell is pushed at most twice, so build costs $O(nm)$ time.

**Add** (lines L6 to L12) changes exactly the cells whose block holds the cell $(r, c)$. By the up-chain fact, these are the cells $(i, j)$ with $i$ on the up chain of $r + 1$ and $j$ on the up chain of $c + 1$.

**Prefix** (lines L13 to L20) adds the cells $(i, j)$ with $i$ on the down chain of $r$ and $j$ on the down chain of $c$. By the down-chain fact, their blocks split the corner rectangle $[0, r - 1] \times [0, c - 1]$ into disjoint parts.

**Query** (line L21) is [inclusion and exclusion](/inclusion-exclusion-principle/) over the four corners of the rectangle.

## Example

Let

$$M = \begin{pmatrix} 2 & 1 & 4 & 3 \\ 0 & 5 & 2 & 1 \\ 3 & 1 & 6 & 2 \\ 1 & 4 & 0 & 5 \end{pmatrix}.$$

BUILD gives the table below, with row 0 and column 0 left out. For example, $F[2][2]$ is the block of rows 1 and 2 and columns 1 and 2 (1-based), $2 + 1 + 0 + 5 = 8$; $F[4][4] = 40$ is the whole matrix; and $F[3][2]$ is the single row 3 with columns 1 and 2, $3 + 1 = 4$.

| $i$ | $g(i)$ | $F[i][1]$ | $F[i][2]$ | $F[i][3]$ | $F[i][4]$ |
|---|---|---|---|---|---|
| 1 | 1 | 2 | 3 | 4 | 10 |
| 2 | 2 | 2 | 8 | 6 | 18 |
| 3 | 1 | 3 | 4 | 6 | 12 |
| 4 | 4 | 6 | 17 | 12 | 40 |

Then run these operations.

| step | operation | cells used | result |
|---|---|---|---|
| 1 | PREFIX$(3, 4)$ | $i = 3, 2$ and $j = 4$: $F[3][4] + F[2][4] = 12 + 18$ | 30 |
| 2 | QUERY$(1, 1, 2, 3)$ | PREFIX$(3, 4) - $ PREFIX$(1, 4) - $ PREFIX$(3, 1) + $ PREFIX$(1, 1) = 30 - 10 - 5 + 2$ | 17 |
| 3 | ADD$(2, 1, 3)$ | $i = 3, 4$ and $j = 2, 4$: the cells $(3, 2)$, $(3, 4)$, $(4, 2)$, $(4, 4)$ get $+3$ | rows 3 and 4 become $3, 7, 6, 15$ and $6, 20, 12, 43$ |
| 4 | QUERY$(1, 1, 2, 3)$ | the same four prefixes, with PREFIX$(3, 4) = 15 + 18 = 33$ | 20 |

In step 3, the up chain of $r + 1 = 3$ is $3, 4$ and the up chain of $c + 1 = 2$ is $2, 4$, so four cells change. The rectangle of steps 2 and 4 holds the changed cell, so its sum grows by 3.

## Correctness

BUILD establishes (F), because each pass is the linear build of a one-dimensional Fenwick tree, and the row pass works on whole rows, which are added like vectors. ADD keeps (F), because it adds $\delta$ to exactly the cells whose block holds $(r + 1, c + 1)$ in 1-based form: a cell's block is $R(i) \times R(j)$, and it holds the cell exactly when $r + 1 \in R(i)$ and $c + 1 \in R(j)$, which by the up-chain fact means that $i$ and $j$ are on the two up chains. PREFIX returns the corner sum, because the blocks $R(i) \times R(j)$ over the two down chains are the products of two partitions, so they partition $\{1, \ldots, r\} \times \{1, \ldots, c\}$. QUERY is then correct by inclusion and exclusion. All loops end, because each step moves an index strictly up to a bound or strictly down to 0. The full proof is in [the correctness proof](proofs/correctness.md).

## Complexity

Each step of a down chain clears one set bit, so the down chain of $x$ has at most $\lfloor \lg x \rfloor + 1$ indices. Each step of an up chain raises $g$ at least by a factor of 2, so the up chain inside $\{1, \ldots, N\}$ has at most $\lfloor \lg N \rfloor + 1$ indices.

| operation | time | cells touched |
|---|---|---|
| build | $\Theta(nm)$ | each cell at most 3 times |
| add | $O(\log n \log m)$ | at most $(\lfloor \lg n \rfloor + 1)(\lfloor \lg m \rfloor + 1)$ |
| prefix | $O(\log n \log m)$ | at most $(\lfloor \lg n \rfloor + 1)(\lfloor \lg m \rfloor + 1)$ |
| query | $O(\log n \log m)$ | four prefixes |
| space | $(n + 1)(m + 1)$ numbers | |

The times are worst case. For $n = m = 1024$, an add touches at most $11 \cdot 11 = 121$ cells, against $2^{20}$ cells of the matrix. In $d$ dimensions the same nesting gives $O(\log^d n)$ per operation and $2^d$ corner sums per query.

## Variants

- **Rectangle add and point query.** Build the tree on the two-dimensional difference array. Adding $\delta$ to a rectangle is four ADD calls at its corners, and the value of one cell is a PREFIX.
- **Rectangle add and rectangle sum.** Keep four trees, over $d[i][j]$, $i \cdot d[i][j]$, $j \cdot d[i][j]$ and $ij \cdot d[i][j]$ of the difference array $d$. A corner sum is a fixed combination of four prefixes, as in the two-tree method for one dimension on the [range update range query](/range-update-range-query/) page.
- **Sparse coordinates, offline.** For $N$ points with large coordinates, [compress](/coordinate-compression/) the rows, and in each Fenwick row keep only the column values that can occur there, found in a first pass. The space becomes $O(N \log N)$ and each operation costs $O(\log^2 N)$ with binary searches.
- **Sparse coordinates, online.** Store the rows as hash maps from columns to values; only the touched cells exist, $O(q \log n \log m)$ of them after $q$ updates.
- **Other groups.** Any abelian group works, such as $\oplus$ for bitwise exclusive or, or sums modulo a prime.

## When to use it

Use it for point updates and rectangle sums on a grid that fits in memory, when the operation has an inverse. It is shorter and faster in practice than a [two-dimensional segment tree](/two-dimensional-segment-tree/), and it uses no extra space. For a static grid, [two-dimensional prefix sums](/two-dimensional-prefix-sums/) answer in $O(1)$. For $\min$ or $\max$, or for range updates that are not additions, use a two-dimensional segment tree. For many points in a huge coordinate range with all queries known in advance, an [offline sweep](/offline-orthogonal-range-counting/) with a one-dimensional Fenwick tree is simpler and uses $O(N)$ space.

## Pitfalls

- **0-based indices inside the table.** With $i = 0$, the update loop of line L12 never moves, since $g(0) = 0$, and the program hangs. Shift to 1-based indices once, at the entry of ADD and PREFIX.
- **Resetting the inner index.** Line L8 and line L15 must start $j$ again for each $i$. Writing the two loops with one shared $j$ skips columns from the second row on.
- **Off by one in the query.** The corner sums of line L21 use $r_2 + 1$ and $c_2 + 1$ for the far corner and $r_1$ and $c_1$ for the near one. Using $r_1 - 1$ in the 0-based form counts an extra row.
- **Building by $nm$ calls of ADD.** It works, but costs $O(nm \log n \log m)$ instead of $O(nm)$, which matters for large grids.
- **Overflow.** A cell holds the sum of up to $nm$ entries. In fixed-width arithmetic, choose a type that holds the total of the whole matrix.
- **No minimum.** The tree cannot answer rectangle minimums, even without updates, because the corner sums need subtraction.

## Implementations

The Python class `FenwickTree2D` follows the main block line by line, with the 1-based table hidden behind 0-based methods. It builds in $O(nm)$ time, and it has a `check_invariant` method that compares every cell with the sum of its block. The tests compare it with a brute-force sum on random matrices with random updates.

## History

Fenwick published the one-dimensional structure in 1994 as a table of cumulative frequencies for arithmetic coding, with the responsibility ranges given by the lowest set bit. Because the update and the prefix walk in each coordinate are independent, the structure extends to any number of dimensions by nesting the loops; this form is standard in programming texts such as cp-algorithms.

## References
