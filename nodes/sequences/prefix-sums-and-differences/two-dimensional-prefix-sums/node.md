---
tag: 5VFF8X
kind: technique
slug: two-dimensional-prefix-sums
name: Two-dimensional prefix sums
aliases:
- 2D prefix sums
- grid prefix sums
area: sequences/prefix-sums-and-differences
level: intro
summary: Precompute the sum of each top-left rectangle, then get any rectangle sum with inclusion-exclusion in O(1).
prereqs: [prefix-sums, inclusion-exclusion-principle]
see_also: [range-sum-query-2d, two-dimensional-difference-array, integral-image, two-dimensional-range-sum-query, maximum-sum-submatrix, two-dimensional-fenwick-tree, box-blur, prefix-sums]
sources:
  - paper: doi:10.1145/800031.808600
    title: "Franklin C. Crow, Summed-area tables for texture mapping, Proceedings of SIGGRAPH 1984, Computer Graphics 18(3), 207-212"
    locator: the summed-area table and the sum over a rectangle from four table entries
  - paper: doi:10.1109/CVPR.2001.990517
    title: "Paul Viola and Michael Jones, Rapid object detection using a boosted cascade of simple features, Proceedings of the IEEE Conference on Computer Vision and Pattern Recognition (CVPR 2001), volume 1, 511-518"
    locator: Section 2.1, Integral Image (one pass with a cumulative row sum, and any rectangle sum from four array references)
  - url: https://cses.fi/book/book.pdf
    title: Antti Laaksonen, Competitive Programmer's Handbook
    locator: Chapter 9, Range queries, Section 9.1 Static array queries (the two-dimensional generalization of prefix sums)
  - paper: "Rainer Lienhart and Jochen Maydt, An extended set of Haar-like features for rapid object detection, Proceedings of the IEEE International Conference on Image Processing (ICIP 2002)"
    locator: the rotated summed area table for features turned by 45 degrees
---

Two-dimensional prefix sums turn a grid $a[0 \ldots R-1][0 \ldots C-1]$ into the table $S$ with $S[i][j] = \sum_{x < i} \sum_{y < j} a[x][y]$, the sum of the top-left rectangle of $i$ rows and $j$ columns. The table costs $\Theta(RC)$ time to build, and then the sum of any axis-aligned rectangle is a signed sum of four table entries, by the [inclusion-exclusion principle](/inclusion-exclusion-principle/), in $O(1)$ time. It is the grid form of [prefix sums](/prefix-sums/), it solves the static [two-dimensional range sum query](/range-sum-query-2d/), and in graphics and vision it is called the summed-area table or the [integral image](/integral-image/).

## In plain words

Picture a spreadsheet of numbers. In a second sheet, let each cell hold the total of everything above it and to its left, the cell itself included. Now the total of any block of cells takes four lookups. Start with the total of the big block that reaches from the top-left corner to the bottom-right corner of your block. Remove the strip above your block, and remove the strip to its left. The small corner region above and to the left was removed twice, so add it back once.

The second sheet itself is easy to fill row by row: each cell is its own number, plus the cell above, plus the cell to the left, minus the cell up and to the left, which the two neighbors both counted.

## When it applies

- **Many rectangle sums on a fixed grid.** Images, height maps, game boards and density maps where the data does not change between queries.
- **Counts of a property in a rectangle.** Use a 0/1 grid of the property: the number of obstacles, of ones, of pixels above a threshold.
- **Sliding a fixed-size box.** All $k \times k$ box sums of an image, for a [box blur](/box-blur/) or a local mean, cost $O(1)$ each, whatever $k$ is.
- **A rectangle condition in a search.** In the [maximum sum submatrix](/maximum-sum-submatrix/) or "largest square with sum at most $s$", the table makes each candidate rectangle cost $O(1)$ to evaluate.
- **Signals that it does not apply.** The grid changes between queries (use a [two-dimensional Fenwick tree](/two-dimensional-fenwick-tree/)), or the operation has no inverse, such as the maximum (use a two-dimensional sparse table).

## The template

Rows and columns are 0-based. The table $S$ has $R + 1$ rows and $C + 1$ columns, with a border of zeros in row 0 and column 0. A query names the rows $r_1 \le x < r_2$ and the columns $c_1 \le y < c_2$, half-open.

```pseudo id=main
BUILD-2D(a[0 .. R − 1][0 .. C − 1])
L1  S[i][0] ← 0 for 0 ≤ i ≤ R; S[0][j] ← 0 for 0 ≤ j ≤ C
L2  for i ← 1 to R do
L3      for j ← 1 to C do
L4          S[i][j] ← a[i−1][j−1] + S[i−1][j] + S[i][j−1] − S[i−1][j−1]
L5  return S

RECT(S, r1, c1, r2, c2)                    ▷ sum of a[x][y] for r1 ≤ x < r2, c1 ≤ y < c2
L6  return S[r2][c2] − S[r1][c2] − S[r2][c1] + S[r1][c1]
```

**Why it is correct.** Write $T(i, j)$ for the set of cells $\{(x, y) : x < i,\ y < j\}$, so $S[i][j]$ is the sum over $T(i, j)$. For line L6, with $r_1 \le r_2$ and $c_1 \le c_2$, the query rectangle is $T(r_2, c_2)$ minus the union of $T(r_1, c_2)$ and $T(r_2, c_1)$. These two sets meet in $T(r_1, c_1)$, and both lie inside $T(r_2, c_2)$. So by inclusion-exclusion the sum over the union is $S[r_1][c_2] + S[r_2][c_1] - S[r_1][c_1]$, and subtracting it from $S[r_2][c_2]$ gives line L6. Line L4 is the same identity for the rectangle of the single cell $(i-1, j-1)$: $a[i-1][j-1] = S[i][j] - S[i-1][j] - S[i][j-1] + S[i-1][j-1]$. Rows are filled in order and each row from left to right, so the three table entries that line L4 reads are already correct, by induction on $(i, j)$ in this order.

**Cost.** BUILD-2D does $3$ additions or subtractions per cell: $\Theta(RC)$ time and $(R+1)(C+1)$ words. RECT does $3$ operations: $O(1)$. On a [word RAM](/word-ram/), every entry has absolute value at most $RC \cdot M$ when all items have absolute value at most $M$; for an 8-bit image of $4096 \times 4096$ pixels this is below $2^{32}$, but only just: $4096^2 \cdot 255 < 2^{32}$.

**A worked example.** For the grid

$$a = \begin{pmatrix} 3 & 0 & 1 & 4 & 2 \\ 5 & 6 & 3 & 2 & 1 \\ 1 & 2 & 0 & 1 & 5 \\ 4 & 1 & 0 & 1 & 7 \end{pmatrix}$$

the rows of $S$ after the zero row are $[0, 3, 3, 4, 8, 10]$, $[0, 8, 14, 18, 24, 27]$, $[0, 9, 17, 21, 28, 36]$ and $[0, 13, 22, 26, 34, 49]$. The rectangle of rows 1 to 2 and columns 1 to 3, inclusive, is $r_1 = 1$, $r_2 = 3$, $c_1 = 1$, $c_2 = 4$. Its sum is $S[3][4] - S[1][4] - S[3][1] + S[1][1] = 28 - 8 - 9 + 3 = 14$, which is $6 + 3 + 2 + 2 + 0 + 1$. The whole grid sums to $S[4][5] = 49$.

## Classic examples

From simple to hard:

- **[Two-dimensional range sum query](/range-sum-query-2d/).** The direct use: $\Theta(RC)$ build, $O(1)$ per query.
- **Box filters.** The mean of every $k \times k$ window of an image in $O(1)$ per pixel, used for [box blur](/box-blur/) and local thresholds.
- **Haar-like features in face detection.** Viola and Jones compute the differences of adjacent rectangle sums from the integral image in a few lookups each, which made real-time [face detection](/face-detection/) possible in 2001.
- **Texture mapping.** Crow's summed-area table gives the average color of a texture over the rectangle that a pixel covers, for filtered [texture mapping](/texture-mapping/).
- **[Maximum sum submatrix](/maximum-sum-submatrix/).** Column prefix sums let [Bentley's sweep](/bentley-column-sweep/) collapse each pair of rows into one array in $O(C)$ time.
- **[Two-dimensional difference array](/two-dimensional-difference-array/).** The inverse operation: four point updates add a constant to a rectangle, and BUILD-2D rebuilds the grid.

## Variations

- **Two passes instead of four terms.** Take the prefix sums of each row, then the prefix sums of each column of the result. This also gives $S$, and it extends to any number of dimensions.
- **$d$ dimensions.** A box sum is a signed sum of $2^d$ table entries, with the sign $(-1)^k$ for an entry that uses the lower bound in $k$ coordinates. Building with $d$ one-dimensional passes costs $\Theta(dN)$ for $N$ cells, against $\Theta(2^d N)$ for the direct $2^d$-term recurrence.
- **Other groups.** XOR and sums modulo $m$ work with the same signs (for XOR all signs are $\oplus$).
- **Rotated rectangles.** Tables of sums over 45-degree triangles give the sums of rectangles rotated by 45 degrees in $O(1)$; Lienhart and Maydt used them to extend the Haar features.
- **Squared values.** A second table of $a[x][y]^2$ gives the variance of any rectangle in $O(1)$, used for contrast normalization.
- **Updates.** With point updates between queries, use a [two-dimensional Fenwick tree](/two-dimensional-fenwick-tree/) with $O(\log R \log C)$ per operation.

## Pitfalls

- **Missing border.** Without the zero row and column, line L4 and line L6 need special cases for $i = 0$, $j = 0$, $r_1 = 0$ or $c_1 = 0$, and these cases are where the bugs hide.
- **Inclusive corners.** For an inclusive query $[x_1, x_2] \times [y_1, y_2]$, the arguments are $r_1 = x_1$, $r_2 = x_2 + 1$, $c_1 = y_1$, $c_2 = y_2 + 1$. Using $x_2$ instead of $x_2 + 1$ drops the last row.
- **A wrong sign.** The corner term $S[r_1][c_1]$ is added, not subtracted, because it was subtracted twice.
- **Overflow.** The entries grow with the area of the grid. An integral image of a large 8-bit image needs 32-bit or 64-bit entries, as the cost analysis shows; Crow notes that the table needs more bits per entry than the image.
- **Floating-point images.** For floating-point data, the four-term difference cancels large, close numbers, and the error grows with the size of the image, not of the rectangle. Subtract the mean of the image first, or use integer data.

## Exercises

1. Prove that the two-pass method (rows, then columns) gives the same table as BUILD-2D.
2. Given a 0/1 grid with $R$ rows and $C$ columns, find the side of the largest square of all ones in $O(RC \log \min(R, C))$ time with a table and a binary search on the side, and then in $O(RC)$ time without the table.
3. State and prove the $2^d$-term query formula for $d$ dimensions by induction on $d$.
4. Count the rectangles of a grid of integers whose sum is exactly $k$, in $O(R^2 C)$ expected time.
5. Show that $4096 \times 4096$ is the largest square size $n \times n$, with $n$ a power of two, for which an integral image of 8-bit pixels fits in unsigned 32-bit integers.

## References
