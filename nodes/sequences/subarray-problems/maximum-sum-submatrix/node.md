---
tag: 6NRQ25
kind: problem
slug: maximum-sum-submatrix
name: Maximum sum submatrix
aliases:
- maximum sum rectangle
- two-dimensional maximum subarray
area: sequences/subarray-problems
level: core
summary: Find the axis-aligned rectangle of a 2D grid with the largest sum.
prereqs: [maximum-subarray-problem, two-dimensional-prefix-sums]
see_also: [bentley-column-sweep, kadane-algorithm, maximal-rectangle-binary-matrix, min-plus-matrix-multiplication, apsp-conjecture, k-maximum-subarray-problem, range-sum-query-2d, largest-empty-rectangle]
sources:
  - paper: doi:10.1145/358234.381162
    title: "Jon Bentley, Programming pearls: algorithm design techniques, Communications of the ACM 27(9) (1984), 865-873"
    locator: the two-dimensional problem of Grenander and its origin in pattern recognition
  - book: isbn:9780201657883
    title: Jon Bentley, Programming Pearls, second edition
    locator: Column 8, Algorithm Design Techniques, Section 8.1 (the problem and its origin) and the problems at the end of the column
  - paper: doi:10.4036/iis.2000.99
    title: "Hisao Tamaki and Takeshi Tokuyama, Algorithms for the Maximum Subarray Problem Based on Matrix Multiplication, Interdisciplinary Information Sciences 6(2) (2000), 99-104"
    locator: the reduction to distance matrix multiplication and the subcubic algorithm
  - paper: doi:10.1016/s1571-0661(04)00313-5
    title: "Tadao Takaoka, Efficient Algorithms for the Maximum Subarray Problem by Distance Matrix Multiplication, Electronic Notes in Theoretical Computer Science 61 (2002), 191-200"
    locator: the simpler divide-and-conquer algorithm with distance matrix multiplication
  - url: https://arxiv.org/abs/1602.05837
    title: "Arturs Backurs, Nishanth Dikkala and Christos Tzamos, Tight Hardness Results for Maximum Weight Rectangles, ICALP 2016"
    locator: the abstract and the conditional lower bounds for weighted points and for the maximum subarray problem on a grid
---

The maximum sum submatrix problem is the [maximum subarray problem](/maximum-subarray-problem/) in two dimensions. Given an $m \times n$ matrix of numbers that may be negative, find the block of consecutive rows and consecutive columns whose entries have the largest sum. Ulf Grenander posed it for pattern recognition, and it is the problem from which the one-dimensional version was taken. Unlike the linear case, it has no known linear-time algorithm. The standard method, the [Bentley column sweep](/bentley-column-sweep/), fixes a pair of rows and runs [Kadane's algorithm](/kadane-algorithm/) on the column sums, in $O(m^2 n)$ time. Matrix multiplication over the $(\min, +)$ semiring gives slightly faster algorithms, and a time of $O(n^{3 - \varepsilon})$ for $n \times n$ matrices would refute the [APSP conjecture](/apsp-conjecture/).

## In plain words

You have a grid of numbers, some positive and some negative, like a map of gains and losses. You want to draw one rectangle on the grid, along the grid lines, so that the numbers inside add up to as much as possible.

There are very many rectangles, so trying them all is slow. A better way picks a top row and a bottom row. For that band, add up each column between the two rows. Now the question is about one row of numbers: which run of columns has the largest total. That is the one-dimensional problem, which one pass solves. Do this for every pair of top and bottom rows and keep the best.

## Definition

**Input.** A matrix $M$ with $m$ rows and $n$ columns of real numbers, with $m, n \ge 1$. By symmetry, assume $m \le n$.

**Output.** Row indices $a \le b$ and column indices $e \le d$ that maximize
$$S(a, b, e, d) = \sum_{i=a}^{b} \sum_{j=e}^{d} M[i][j],$$
and the value $S^*$ of the maximum. As in one dimension, the empty rectangle, with sum $0$, may or may not be allowed.

**With prefix sums.** With the [two-dimensional prefix sums](/two-dimensional-prefix-sums/) $P$, each $S(a, b, e, d)$ is four lookups, $P[b+1][d+1] - P[a][d+1] - P[b+1][e] + P[a][e]$. So all $\Theta(m^2 n^2)$ rectangles can be checked in $\Theta(m^2 n^2)$ time.

**One band.** For fixed rows $a \le b$, let $C_{a,b}[j] = \sum_{i=a}^{b} M[i][j]$. The best rectangle with these rows is the maximum subarray of $C_{a,b}$, and $C_{a, b+1} = C_{a, b} + M[b+1]$, so the bands for one $a$ cost $O(n)$ each to build.

## Variants

- **Empty rectangle allowed.** The answer is $\max(0, S^*)$.
- **$k$ best rectangles.** The $k$ largest sums, or $k$ disjoint rectangles; see the [k-maximum subarray problem](/k-maximum-subarray-problem/).
- **Weighted points.** Given $n$ points in the plane with weights of any sign, find the axis-parallel rectangle of largest total weight. After compressing the coordinates it is a sparse $n \times n$ matrix, and it is solved in $O(n^2)$ time.
- **All-ones rectangle.** For a $0/1$ matrix and the largest rectangle of ones, see the [maximal rectangle in a binary matrix](/maximal-rectangle-binary-matrix/), which is linear in the size of the matrix.
- **Higher dimensions.** For a $d$-dimensional array, fixing a pair of bounds in each of $d - 1$ dimensions and running Kadane in the last takes $O(n^{2d - 1})$ time for side $n$.
- **Shape constraints.** Largest sum over rectangles of a fixed size, solved in $O(mn)$ with prefix sums, or over other shapes such as convex regions.

## Examples

**A small example.** For
$$M = \begin{pmatrix} 1 & 2 & -1 & -4 & -20 \\ -8 & -3 & 4 & 2 & 1 \\ 3 & 8 & 10 & 1 & 3 \\ -4 & -1 & 1 & 7 & -6 \end{pmatrix}$$
the best rectangle is rows $1..3$ and columns $1..3$, counted from $0$:
$$\begin{pmatrix} -3 & 4 & 2 \\ 8 & 10 & 1 \\ -1 & 1 & 7 \end{pmatrix},$$
with sum $29$. For the band of rows $1..3$ the column sums are $C = [-9, 4, 15, 10, -2]$, and the maximum subarray of $C$ is $4 + 15 + 10 = 29$.

**One row.** For $m = 1$ the problem is the plain maximum subarray problem.

**All negative.** If every entry is negative, the answer for a non-empty rectangle is the largest entry.

## Known algorithms

| method | time for $m \times n$, $m \le n$ | extra space | idea |
|---|---|---|---|
| all rectangles with 2D prefix sums | $\Theta(m^2 n^2)$ | $\Theta(mn)$ | four lookups per rectangle |
| [Bentley column sweep](/bentley-column-sweep/) | $\Theta(m^2 n)$ | $\Theta(n)$ | Kadane on the column sums of each band |
| Tamaki and Tokuyama (1998) | $O(n^3 \sqrt{\log \log n / \log n})$ for $m = n$ | $O(n^2)$ | divide and conquer, crossing case by distance matrix multiplication |
| Takaoka (2002) | $O(n^3 \sqrt{\log \log n / \log n})$ for $m = n$ | $O(n^2)$ | a simpler divide and conquer with the same product |

**Distance matrix multiplication.** Split the rows in half. The best rectangle lies in the top half, in the bottom half, or crosses the middle. For the crossing case, a rectangle on columns $e..d$ is the best part above the cut plus the best part below it, and both parts are differences of prefix sums. Taking the maximum over the column pairs is a product of two matrices over the $(\max, +)$ semiring, which is the [min-plus matrix multiplication](/min-plus-matrix-multiplication/) with the signs changed. The fastest products of this kind are slightly subcubic, and they give the bounds in the table.

## Bounds

**Lower bound from reading.** Every entry must be read, by the same [adversary argument](/adversary-argument/) as in one dimension, so $\Omega(mn)$ time is needed. No algorithm near this bound is known for $m = n$.

**Conditional lower bound.** Backurs, Dikkala and Tzamos (2016) showed that an $O(n^{3 - \varepsilon})$ algorithm for the maximum sum submatrix of an $n \times n$ matrix, for any $\varepsilon > 0$, would give a truly subcubic algorithm for all-pairs shortest paths, against the APSP conjecture. For $n$ weighted points in the plane they showed that the $O(n^2)$ time is tight under conjectures of the same kind. So the cubic algorithms are essentially the best possible unless those conjectures fail.

## Reductions

- **To one dimension.** Each band of rows is one maximum subarray problem on column sums; the $\binom{m+1}{2}$ bands give the column sweep.
- **To the $(\max, +)$ product.** The crossing case of the row split is a $(\max, +)$ matrix product, so faster products give faster algorithms for this problem.
- **From all-pairs shortest paths.** In the other direction, the reduction of Backurs, Dikkala and Tzamos turns a hard instance of a problem that is equivalent to all-pairs shortest paths under subcubic reductions into a maximum sum submatrix instance.
- **From weighted points.** Points with weights become a matrix after [coordinate compression](/coordinate-compression/), with zeros in the empty cells.

## Applications

- **Pattern recognition.** Grenander's motivation was the maximum likelihood estimate of the brightest rectangular region of a digital picture. After subtracting the mean brightness, the brightest region is the maximum sum submatrix.
- **Data mining.** In a table of counts over two ordered attributes, such as age and income, the rectangle with the largest total of a score, for example the excess of one class over another, is a range rule of the two attributes.
- **Images and maps.** The region of largest total value in a raster map, such as the richest block of a grid of resource estimates.

## References
