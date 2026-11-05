---
tag: KGYZPT
kind: technique
slug: two-dimensional-difference-array
name: Two-dimensional difference array
aliases:
- 2D difference array
- 2D Imos method
area: sequences/prefix-sums-and-differences
level: intro
summary: Add a value to a rectangle with four point updates on a 2D difference grid, then recover the grid by 2D prefix sums.
prereqs: [difference-array, two-dimensional-prefix-sums]
see_also: [difference-array, two-dimensional-prefix-sums, range-update-point-query, range-sum-query-2d, two-dimensional-fenwick-tree, area-of-union-of-rectangles, inclusion-exclusion-principle]
sources:
  - url: https://imoz.jp/algorithms/imos_method.html
    title: Kentaro Imajo, Imos method (in Japanese), 2012
    locator: the two-dimensional method (weights at the four corners of each rectangle, then cumulative sums along each axis) and its extension to higher dimensions
  - url: https://cses.fi/book/book.pdf
    title: Antti Laaksonen, Competitive Programmer's Handbook
    locator: Chapter 9, Range queries, Section 9.1 Static array queries (two-dimensional prefix sums) and Section 9.4 Additional techniques (range updates with a difference array)
  - book: isbn:9780201558029
    title: Graham, Knuth and Patashnik, Concrete Mathematics, second edition
    locator: Section 2.6, Finite and infinite calculus (the difference operator as the inverse of summation)
---

A two-dimensional difference array lets a program add a constant $c$ to every cell of many axis-aligned rectangles of a grid $a[0 \ldots R-1][0 \ldots C-1]$ with four point updates per rectangle, and then rebuild the grid with one pass of [two-dimensional prefix sums](/two-dimensional-prefix-sums/). The cost is $\Theta(RC + m)$ for $m$ rectangles, against $\Theta(RCm)$ in the worst case for a loop over each rectangle. It is the grid form of the [difference array](/difference-array/), and it solves the batch form of the rectangle version of the [range update point query](/range-update-point-query/).

## In plain words

You must paint many rectangles on a grid, where painting adds a number to each covered cell, and at the end you want the total in every cell. Painting cell by cell is slow when the rectangles are big.

Instead, put four marks at the corners of each rectangle: a plus at its top-left corner, a minus just right of its top-right corner, a minus just below its bottom-left corner, and a plus diagonally past its bottom-right corner. Then sweep the marks with running totals, first along each row and then down each column. The running totals carry the plus mark into exactly the cells of the rectangle, and the three other marks cancel it everywhere else.

## When it applies

- **Many rectangle additions, then reads.** All updates come before the reads, or the reads come in a few batches.
- **The update adds a constant.** Each rectangle adds the same value to all its cells. Assignment, maximum and other operations that cannot be undone do not fit.
- **Coverage counts.** "How many rectangles cover each cell" is $+1$ per rectangle; the cells with a positive count form the union, and its area is the number of such cells. See [area of union of rectangles](/area-of-union-of-rectangles/) for the continuous version.
- **Signals that it does not apply.** Reads interleave with updates and both must be fast: store the difference grid in a [two-dimensional Fenwick tree](/two-dimensional-fenwick-tree/). The coordinates are large and sparse: compress them first, or sweep.

## The template

Rows and columns are 0-based and rectangles are half-open: $[x_1, x_2) \times [y_1, y_2)$ with $0 \le x_1 \le x_2 \le R$ and $0 \le y_1 \le y_2 \le C$. The difference grid $D$ has $R + 1$ rows and $C + 1$ columns, so that the corners with $x_2 = R$ or $y_2 = C$ have a cell.

```pseudo id=main
RECTANGLE-ADDS(R, C, updates)             ▷ updates: a list of (x1, y1, x2, y2, c)
L1  D ← an (R + 1) × (C + 1) grid of zeros
L2  for each (x1, y1, x2, y2, c) in updates do
L3      D[x1][y1] ← D[x1][y1] + c
L4      D[x1][y2] ← D[x1][y2] − c
L5      D[x2][y1] ← D[x2][y1] − c
L6      D[x2][y2] ← D[x2][y2] + c
L7  for x ← 0 to R − 1 do
L8      for y ← 0 to C − 1 do
L9          a[x][y] ← D[x][y] + a[x−1][y] + a[x][y−1] − a[x−1][y−1]   ▷ a terms with index −1 are 0
L10 return a
```

To start from a non-zero grid, add its original values to the result at the end, or first fill $D$ with the two-dimensional differences of the grid.

**Why it is correct.** Lines L7 to L9 compute the two-dimensional prefix sums $a[x][y] = \sum_{u \le x} \sum_{v \le y} D[u][v]$, by the recurrence proved on the page of [two-dimensional prefix sums](/two-dimensional-prefix-sums/). Prefix sums are linear, so it is enough to look at one update. Its four entries contribute to $a[x][y]$ the amount

$$c \cdot \big([x_1 \le x][y_1 \le y] - [x_1 \le x][y_2 \le y] - [x_2 \le x][y_1 \le y] + [x_2 \le x][y_2 \le y]\big),$$

where $[P]$ is 1 if $P$ is true and 0 if not. This factors as $c \cdot ([x_1 \le x] - [x_2 \le x]) \cdot ([y_1 \le y] - [y_2 \le y])$. Since $x_1 \le x_2$, the first factor is 1 exactly when $x_1 \le x < x_2$ and 0 otherwise, and the same holds for the second factor. So the update adds $c$ to the cells of its rectangle and nothing elsewhere.

**Cost.** Lines L2 to L6 take $\Theta(m)$ time, and lines L7 to L9 take $\Theta(RC)$. The total is $\Theta(RC + m)$ time and $(R+1)(C+1)$ words for $D$.

**A worked example.** On a grid with $R = 4$ and $C = 5$, apply $+2$ to $[0, 2) \times [1, 4)$, $+1$ to $[1, 4) \times [0, 3)$ and $-3$ to $[2, 3) \times [2, 5)$. The grid $D$ becomes, row by row: $[0, 2, 0, 0, -2, 0]$, $[1, 0, 0, -1, 0, 0]$, $[0, -2, -3, 0, 2, 3]$, $[0, 0, 3, 0, 0, -3]$, $[-1, 0, 0, 1, 0, 0]$. Its prefix sums give

$$a = \begin{pmatrix} 0 & 2 & 2 & 2 & 0 \\ 1 & 3 & 3 & 2 & 0 \\ 1 & 1 & -2 & -3 & -3 \\ 1 & 1 & 1 & 0 & 0 \end{pmatrix}.$$

The cell $(1, 1)$ lies in the first two rectangles and holds $2 + 1 = 3$. The cell $(2, 2)$ lies in the last two and holds $1 - 3 = -2$.

## Classic examples

From simple to hard:

- **Painting rectangles.** Count, for each cell, how many of $m$ rectangles cover it, and report the cells covered at least $k$ times, in $\Theta(RC + m)$.
- **Stamping and coverage on a board.** Decide whether a set of stamps of fixed size, placed at given positions, covers every free cell of a grid. The count of each cell comes from one difference grid.
- **Heat maps and density maps.** Each event adds weight to a box around its position; one pass builds the map.
- **Batch [range update point query](/range-update-point-query/) on a grid.** The template above; the online form keeps $D$ in a [two-dimensional Fenwick tree](/two-dimensional-fenwick-tree/).

## Variations

- **$d$ dimensions.** A box add sets $2^d$ entries, the corner with $k$ upper bounds getting $(-1)^k c$. Then $d$ passes of one-dimensional prefix sums, one along each axis, rebuild the array in $\Theta(dN)$ for $N$ cells.
- **Two passes.** Lines L7 to L9 can be replaced by prefix sums along each row, then along each column. The result is the same.
- **Online reads.** Keep $D$ in a two-dimensional Fenwick tree. An update is four point adds and a read is one two-dimensional prefix sum, each $O(\log R \log C)$.
- **Coordinate compression.** For rectangles with real or huge coordinates, sort the distinct $x$ and $y$ ends, work on the compressed grid of size at most $2m \times 2m$, and weight each compressed cell by its true area when an area is needed.
- **Other shapes.** Imajo's notes show that with other directions of cumulative sums, the same method adds constants to triangles and other polygons on triangular and hexagonal grids, and that higher-order differences add polynomial weights.

## Pitfalls

- **Grid of size $R \times C$.** The updates at $x_2 = R$ or $y_2 = C$ write outside an $R \times C$ grid. Allocate $(R+1) \times (C+1)$, or skip those writes with a test.
- **Inclusive rectangles.** For an inclusive rectangle $[x_1, x_2] \times [y_1, y_2]$, the three other corners are at $x_2 + 1$ and $y_2 + 1$. Using $x_2$ and $y_2$ leaves the last row and column of the rectangle unchanged.
- **Wrong corner signs.** The two corners on the diagonal of the rectangle get $+c$ and the other two get $-c$. A sign error leaves a stripe of $\pm c$ that runs to the edge of the grid.
- **Reading $D$ instead of $a$.** The values are only valid after the prefix-sum pass.
- **Overflow.** A cell covered by all $m$ rectangles holds $m$ times the largest $c$.

## Exercises

1. Give a grid of $R \times C$ cells and $m$ rectangles. Find the number of cells covered by an odd number of rectangles in $O(RC + m)$ time.
2. Prove that the two-pass method (rows, then columns) gives the same result as lines L7 to L9.
3. Write the $2^d$ updates for a box add in $d$ dimensions, and prove them correct with the factorization used above.
4. Each of $m$ updates adds $c$ to the cells of a rectangle whose distance from its center, in the maximum norm, is at most $r$. Explain why this is a rectangle add, and solve the batch problem.
5. Give a sequence of updates and reads for which rebuilding the grid after each update costs $\Theta(RCm)$, and explain how a two-dimensional Fenwick tree reduces it.

## References
