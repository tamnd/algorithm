---
tag: 0A4NQ0
kind: algorithm
slug: staircase-search
name: Staircase search
aliases:
- saddleback search
area: searching/sequential-and-binary-search
level: core
summary: Start at a corner and step left or down, discarding a row or column per comparison; O(m + n) comparisons.
solves: [sorted-matrix-search]
model: comparison-model
complexity:
  vars: {m: the number of rows, n: the number of columns}
  time: {worst: Θ(m + n), average: Θ(m + n), best: Θ(1)}
  space: {extra: Θ(1)}
properties: {deterministic: true, comparison: true, recursive: false, in_place: true}
prereqs: [sorted-matrix-search, loop-invariant]
see_also: [sorted-matrix-search, young-tableau, two-pointers, two-sum, sorted-matrix-selection, binary-search, adversary-argument]
sources:
  - paper: doi:10.1007/11783596_8
    title: Richard S. Bird, Improving saddleback search, a lesson in algorithm design, Mathematics of Program Construction (MPC 2006), LNCS 4014
    locator: pp. 82 to 89 (saddleback search, its m + n bound, and better methods for thin matrices)
  - paper: doi:10.1016/0196-6774(85)90020-3
    title: Nathan Linial and Michael Saks, Searching ordered structures, Journal of Algorithms 6(1) (1985)
    locator: pp. 86 to 103 (lower bounds for search in sorted matrices)
---

Staircase search, also called saddleback search, finds a key $x$ in an $m \times n$ matrix whose rows and columns are all non-decreasing. It starts at the top-right corner. When the cell there is larger than $x$, the whole rest of its column is larger too, so the walk steps left; when it is smaller, the whole rest of its row is smaller, so the walk steps down. Each read removes one row or one column, so the walk reads at most $m + n - 1$ cells, uses $\Theta(1)$ space and never goes back. For a square matrix no algorithm can read fewer cells in the worst case, as the lower bound on [search in a sorted matrix](/sorted-matrix-search/) shows. The same walk on the matrix of sums $a[i] + b[j]$ is the [two pointers](/two-pointers/) scan for [two sum](/two-sum/).

## In plain words

A grid of numbers grows to the right and grows downward. You stand in the top-right corner and look for one number.

If the number under your feet is too big, then every number below it is even bigger, so that whole column is useless. You step left. If the number is too small, then every number to its left is even smaller, so that whole row is useless. You step down.

Each look throws away a full row or a full column. You stop when you find the number or step off the grid. The walk looks like a staircase going down and to the left, and it is never longer than the number of rows plus the number of columns.

## The problem

The input is an $m \times n$ matrix $M$ with $M[i][j] \le M[i][j+1]$ and $M[i][j] \le M[i+1][j]$ for all indices in range, and a key $x$. The output is a pair $(i, j)$ with $M[i][j] = x$, or NIL when $x$ does not occur. This is [search in a row- and column-sorted matrix](/sorted-matrix-search/). The algorithm only compares $x$ with cells.

## The algorithm

```pseudo id=main
STAIRCASE-SEARCH(M, x)            ▷ M has m rows and n columns
L1  i ← 0, j ← n − 1               ▷ the top-right corner
L2  while i < m and j ≥ 0 do       ▷ x can only be in rows i .. m − 1 and columns 0 .. j
L3      if M[i][j] = x then return (i, j)
L4      if M[i][j] > x then j ← j − 1  ▷ column j from row i down is > x
L5      else i ← i + 1                 ▷ row i up to column j is < x
L6  return NIL
```

The comment on line L2 is the [loop invariant](/loop-invariant/). The live part of the matrix is always the rectangle of rows $i$ to $m - 1$ and columns $0$ to $j$, and its top-right corner is the cell read next. That corner is the largest cell of its row in the rectangle and the smallest cell of its column in the rectangle, which is why one comparison can drop a full line.

The walk can also start at the bottom-left corner $(m - 1, 0)$ and step up or right. The other two corners do not work: at the top-left corner both a step right and a step down make the cell larger, so a comparison does not tell which line to drop.

## Example

The matrix has $m = 4$ rows and $n = 5$ columns:

| | 0 | 1 | 2 | 3 | 4 |
|---|---|---|---|---|---|
| 0 | 1 | 4 | 7 | 11 | 15 |
| 1 | 2 | 5 | 8 | 12 | 19 |
| 2 | 3 | 6 | 9 | 16 | 22 |
| 3 | 10 | 13 | 14 | 17 | 24 |

Search for $x = 14$:

| step | $(i, j)$ | $M[i][j]$ | test | move |
|---|---|---|---|---|
| 1 | (0, 4) | 15 | $15 > 14$ | left |
| 2 | (0, 3) | 11 | $11 < 14$ | down |
| 3 | (1, 3) | 12 | $12 < 14$ | down |
| 4 | (2, 3) | 16 | $16 > 14$ | left |
| 5 | (2, 2) | 9 | $9 < 14$ | down |
| 6 | (3, 2) | 14 | equal | return (3, 2) |

A search for $x = 20$ reads 15, 19, 22, 16, 17 and leaves the matrix below row 3 after 5 reads: NIL. A search for $x = 0$ walks left along row 0 through 15, 11, 7, 4, 1 and leaves on the left: 5 reads, NIL.

## Correctness

The invariant is: every cell that holds $x$ lies in a row $\ge i$ and a column $\le j$. It holds at the start, since then it says nothing. When $M[i][j] > x$, every cell $M[k][j]$ with $k \ge i$ is at least $M[i][j]$ because column $j$ is sorted, so none is $x$, and dropping column $j$ keeps the invariant. When $M[i][j] < x$, every cell $M[i][k]$ with $k \le j$ is at most $M[i][j]$ because row $i$ is sorted, so dropping row $i$ keeps it. Each pass that does not return raises $i - j$ by one, from $-(n - 1)$ to at most $m$, so the loop stops. When it stops without a match, $i = m$ or $j < 0$, the rectangle is empty, and the invariant says that $x$ is nowhere: NIL is correct. The full proof is below.

## Complexity

Count the reads of cells; each read costs one or two comparisons with $x$.

- **Worst case.** Each pass without a return raises $i - j$ by one. The value starts at $-(n - 1)$, and the loop runs only while $i \le m - 1$ and $j \ge 0$, that is while $i - j \le m - 1$. So there are at most $(m - 1) + (n - 1) + 1 = m + n - 1$ passes. On the matrix $M[i][j] = 2(in + j)$, the key $x = 2(m-1)n - 1$, one less than the bottom-left cell, reaches it: the walk goes down the last column to row $m - 1$, then left along the last row and off the matrix. The tests of the implementation check that the worst case over all keys equals $m + n - 1$ on that matrix for several shapes. So the time is $\Theta(m + n)$.
- **Best case.** $x = M[0][n-1]$: one read, $\Theta(1)$.
- **Average case.** For a key at a uniform random cell of the matrix $M[i][j] = 2(in + j)$, the walk goes left until the column of the key, then down to its row, about $(m + n)/2$ reads on average: $\Theta(m + n)$.
- **Space.** Two indices: $\Theta(1)$.

For a square $n \times n$ matrix the bound $2n - 1$ is exactly optimal: the adversary on two anti-diagonals in [search in a sorted matrix](/sorted-matrix-search/) forces every algorithm to read $2n - 1$ cells. When $m \ll n$, a binary search in each row, $m \lceil \lg(n+1) \rceil$ comparisons, is already better, and divide and conquer reaches $O(m \log(2n/m))$.

## Properties

- **Which copy.** The walk drops a row only when that row has no $x$ in the live columns, and it drops a column only when it has no $x$ in the live rows. So the answer is in the smallest row that holds $x$, at the largest column of $x$ in that row.
- **Monotone path.** The path only moves left and down. It never reads a cell twice, and it reads at most one cell of each anti-diagonal $i - j$.
- **Comparison-based.** It uses only $=$ and $<$ on cells, so it works for strings and any total order.
- **On-demand cells.** It reads at most $m + n - 1$ cells, so the matrix can be a function $f(i, j)$ computed when needed, and need not be stored.

## Variants and improvements

- **Counting.** To count the cells with $M[i][j] \le x$, walk the same way without the equality test, and add $j + 1$ each time the walk steps down from row $i$. This takes $O(m + n)$ time and is the inner step of [selection in a sorted matrix](/sorted-matrix-selection/) by binary search on the value.
- **All occurrences.** Do not stop at a match; step left (or down) and go on. The walk lists, for each row, its largest-index copy of $x$, and the counts for $\le x$ and $< x$ give the number of all copies.
- **Two sum.** For sorted arrays $a$ and $b$, the matrix $a[i] + b[j]$ is sorted in both directions. The walk from $(0, n - 1)$ is the [two pointers](/two-pointers/) method for [two sum](/two-sum/), with $O(m + n)$ time and no matrix in memory.
- **Gallop instead of step.** Replace each step by an [exponential search](/exponential-search/) along the row or column. This keeps $O(m + n)$ in the worst case and helps when the path has long straight runs.
- **Thin matrices.** When $m \ll n$, binary search for the boundary in the middle row and recurse on the two parts that can still hold $x$. Bird shows that this gives $O(m \log(2n/m))$ comparisons, which matches the lower bound of Linial and Saks up to a constant factor.
- **[Young tableau](/young-tableau/).** The same walk searches a tableau whose empty cells hold $+\infty$.

## When to use it

Use staircase search when the matrix is sorted along both axes, $m$ and $n$ are of the same order, and simple code with no extra memory is wanted. It is also the right tool when the cells are values $f(i, j)$ of a function that grows in both arguments, such as all pairs with $a[i] + b[j] = t$ or all $(i, j)$ with $i^2 + j^2 = t$. When one side is much shorter, search each short-side line by binary search, or use divide and conquer. When the matrix is sorted in row-major order, treat it as one array of $mn$ items and use one [binary search](/binary-search/).

## Pitfalls

- **Starting at the wrong corner.** From the top-left or bottom-right corner a comparison does not tell which line to drop. Start at the top-right or the bottom-left.
- **Empty matrix.** With $m = 0$ there is no row 0, so $n$ cannot be read as the length of the first row. Set $n = 0$, and the loop does not run.
- **Unsigned column index.** The loop stops when $j$ drops to $-1$. With an unsigned $j$ the value wraps around and the test $j \ge 0$ is always true. Use a signed index, or keep $j$ as one past the column.
- **Order of the tests.** Test equality first, or test $M[i][j] > x$ before stepping down. Stepping down on $M[i][j] \le x$ without the equality test drops a row that holds $x$.
- **Rows sorted but columns not.** The walk needs both orders. With sorted rows only, use a binary search in each row.
- **Ragged rows.** The walk assumes a rectangle. With rows of different lengths, the column index can point past the end of a shorter row.

## Implementations

## History

The walk is a standard example in the literature on program derivation, where it is often credited to Gries, who called it saddleback search and derived it from its invariant. Bird revisited it in 2006 and showed that it is not the best method when one side of the matrix is much shorter than the other. Linial and Saks had given lower bounds for search in sorted matrices and other partial orders in 1985.

## References
