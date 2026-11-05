---
tag: B4PWT1
kind: algorithm
slug: bentley-column-sweep
name: Bentley's maximum sum submatrix algorithm
aliases:
- Kadane in two dimensions
- column-pair sweep with Kadane
area: sequences/subarray-problems
level: core
summary: Fix a pair of rows, compress columns into a 1D array, then run Kadane; runs in O(n^3) for an n by n grid.
solves: [maximum-sum-submatrix]
model: word-ram
complexity:
  vars: {m: the number of rows, n: the number of columns, with m at most n}
  time: {worst: Θ(m^2 n), average: Θ(m^2 n), best: Θ(m^2 n)}
  space: {extra: Θ(n)}
properties: {stable: false, in_place: true, adaptive: false, online: false, deterministic: true, comparison: false, recursive: false}
history:
  year: 1984
  people: [Jon Bentley, Ulf Grenander]
  note: Bentley's Programming Pearls column of 1984 gave cubic time as the best known for Grenander's two-dimensional problem, reached by running the one-dimensional scan on the column sums of each band of rows.
prereqs: [maximum-sum-submatrix, kadane-algorithm]
see_also: [maximum-subarray-problem, two-dimensional-prefix-sums, maximal-rectangle-binary-matrix, min-plus-matrix-multiplication, apsp-conjecture, maximum-subarray-divide-and-conquer, k-maximum-subarray-problem, range-sum-query-2d]
sources:
  - paper: doi:10.1145/358234.381162
    title: "Jon Bentley, Programming pearls: algorithm design techniques, Communications of the ACM 27(9) (1984), 865-873"
    locator: the two-dimensional problem and the cubic bound
  - book: isbn:9780201657883
    title: Jon Bentley, Programming Pearls, second edition
    locator: Column 8, Algorithm Design Techniques, the problems at the end of the column (the two-dimensional problem)
  - paper: doi:10.1016/s1571-0661(04)00313-5
    title: "Tadao Takaoka, Efficient Algorithms for the Maximum Subarray Problem by Distance Matrix Multiplication, Electronic Notes in Theoretical Computer Science 61 (2002), 191-200"
    locator: the cubic algorithm by reduction to one dimension, as the baseline for the subcubic algorithms
  - url: https://arxiv.org/abs/1602.05837
    title: "Arturs Backurs, Nishanth Dikkala and Christos Tzamos, Tight Hardness Results for Maximum Weight Rectangles, ICALP 2016"
    locator: the conditional lower bound for the maximum subarray problem on a grid
---

The column sweep solves the [maximum sum submatrix](/maximum-sum-submatrix/) problem by reducing it to the one-dimensional [maximum subarray problem](/maximum-subarray-problem/). For each pair of rows $a \le b$, it adds up each column between them into one array $C$, so that a rectangle with rows $a..b$ and columns $e..d$ has sum $C[e] + \dots + C[d]$. Then [Kadane's algorithm](/kadane-algorithm/) finds the best columns for that band in $O(n)$ time. Moving $b$ down by one row updates $C$ in $O(n)$ time, so the whole sweep takes $\Theta(m^2 n)$ time for an $m \times n$ matrix with $m \le n$, or $\Theta(n^3)$ for a square one. Under the [APSP conjecture](/apsp-conjecture/) no algorithm is faster by a polynomial factor.

## In plain words

Pick a top row. Start a running list of column totals, one per column, all zero. Now move a bottom row down from the top row, one row at a time. Each time, add the new row into the column totals. The list now holds, for each column, the total of the band between the top and the bottom row.

A rectangle in this band is a run of columns, and its total is the total of that run in the list. So the best rectangle for the band is the best run in the list, which one pass of Kadane's scan finds. Keep the best rectangle seen.

When the bottom row reaches the last row, move the top row down by one and start the list again.

## The problem

**Input.** A matrix $M[0..m-1][0..n-1]$ of numbers with $m, n \ge 1$. If $m > n$, transpose it first, or swap the roles of rows and columns.

**Output.** The largest sum of a non-empty rectangle of consecutive rows and columns, and its rows $a..b$ and columns $e..d$.

## The algorithm

```pseudo id=main
COLUMN-SWEEP(M[0 .. m-1][0 .. n-1])
L1  best ← −∞
L2  for a ← 0 to m − 1 do
L3      C[0 .. n-1] ← 0
L4      for b ← a to m − 1 do
L5          for j ← 0 to n − 1 do C[j] ← C[j] + M[b][j]
L6          (s, e, d) ← KADANE(C)
L7          if s > best then best ← s; R ← (a, b, e, d)
L8  return (best, R)
```

Line L3 starts a new top row $a$ with zero column sums. Line L5 adds row $b$, so that $C[j]$ is the sum of column $j$ over rows $a..b$. Line L6 runs Kadane's algorithm on $C$ and returns the best sum with its columns. Line L7 keeps the best rectangle.

## Example

$$M = \begin{pmatrix} 1 & 2 & -1 & -4 & -20 \\ -8 & -3 & 4 & 2 & 1 \\ 3 & 8 & 10 & 1 & 3 \\ -4 & -1 & 1 & 7 & -6 \end{pmatrix}$$

The table lists every band $(a, b)$, the column sums $C$ after line L5, the result of Kadane on $C$, and $best$ after line L7.

| $a$ | $b$ | $C$ | Kadane: sum, columns | $best$ |
|---|---|---|---|---|
| 0 | 0 | $[1, 2, -1, -4, -20]$ | 3, $0..1$ | 3 |
| 0 | 1 | $[-7, -1, 3, -2, -19]$ | 3, $2..2$ | 3 |
| 0 | 2 | $[-4, 7, 13, -1, -16]$ | 20, $1..2$ | 20 |
| 0 | 3 | $[-8, 6, 14, 6, -22]$ | 26, $1..3$ | 26 |
| 1 | 1 | $[-8, -3, 4, 2, 1]$ | 7, $2..4$ | 26 |
| 1 | 2 | $[-5, 5, 14, 3, 4]$ | 26, $1..4$ | 26 |
| 1 | 3 | $[-9, 4, 15, 10, -2]$ | 29, $1..3$ | 29 |
| 2 | 2 | $[3, 8, 10, 1, 3]$ | 25, $0..4$ | 29 |
| 2 | 3 | $[-1, 7, 11, 8, -3]$ | 26, $1..3$ | 29 |
| 3 | 3 | $[-4, -1, 1, 7, -6]$ | 8, $2..3$ | 29 |

The answer is $29$, the rectangle with rows $1..3$ and columns $1..3$. There are $\binom{5}{2} = 10$ bands, each with one update of $C$ and one Kadane pass of $5$ items.

## Correctness

Every rectangle has a top row $a$ and a bottom row $b \ge a$, and the loops of lines L2 and L4 visit every such pair once. For a fixed band, line L5 keeps the invariant
$$C[j] = \sum_{i=a}^{b} M[i][j] \quad \text{for all } j,$$
since line L3 starts with zeros and each step $b$ adds row $b$. A rectangle with rows $a..b$ and columns $e..d$ has sum
$$\sum_{i=a}^{b} \sum_{j=e}^{d} M[i][j] = \sum_{j=e}^{d} C[j],$$
so the best rectangle in the band is the maximum subarray of $C$, which Kadane's algorithm returns in line L6. Line L7 keeps the best over all bands, which is the best over all rectangles. The [proof page](proofs/correctness.md) gives the details.

## Complexity

- **Time.** There are $m(m+1)/2$ bands. Each costs $n$ additions in line L5 and one Kadane pass of $\Theta(n)$ in line L6. So the time is $\Theta(m^2 n)$ on every input, and $\Theta(n^3)$ for $m = n$. Choosing the smaller side for the rows matters: for $m \le n$, $m^2 n \le m n^2$.
- **Space.** The array $C$ and $O(1)$ scalars, $\Theta(n)$ extra space.
- **Lower bound.** Under the APSP conjecture, no algorithm takes $O(n^{3 - \varepsilon})$ time on $n \times n$ matrices (Backurs, Dikkala and Tzamos, 2016). The known subcubic algorithms gain only a factor of about $\sqrt{\log n / \log \log n}$.

## Properties

- **Exact.** With integer entries, all values are exact sums. The column sums need a word large enough for $m \max |M|$, and the answer for $mn \max |M|$.
- **Not online.** Each top row needs all rows below it, so the matrix must be stored.
- **Simple to parallelize.** The $m$ top rows are independent, and so are the bands for one top row once their column sums are known.
- **Prefix-sum form.** With column prefix sums $Q[i][j] = M[0][j] + \dots + M[i-1][j]$, the band sums are $C[j] = Q[b+1][j] - Q[a][j]$, so the bands can be visited in any order. This is the form with [two-dimensional prefix sums](/two-dimensional-prefix-sums/) used in one dimension.

## Variants and improvements

- **Empty rectangle allowed.** Start with $best = 0$ and use the empty-allowed form of Kadane.
- **Non-square matrices.** Put the shorter side on the rows, so the cost is $\Theta(\min(m, n)^2 \max(m, n))$.
- **Subcubic.** Splitting the rows in half and solving the crossing case with a $(\max, +)$ matrix product gives $O(n^3 \sqrt{\log \log n / \log n})$ time (Tamaki and Tokuyama, Takaoka). See [min-plus matrix multiplication](/min-plus-matrix-multiplication/).
- **$k$ best rectangles.** Replacing Kadane by an algorithm for the $k$ best subarrays of $C$ gives the [k-maximum subarray problem](/k-maximum-subarray-problem/) in two dimensions.
- **Rectangles with a length bound.** If the width of the rectangle must be at most $w$ columns, replace Kadane by the [monotonic deque over prefix sums](/monotonic-deque-prefix-sums/) for bounded length.
- **Higher dimensions.** In $d$ dimensions, fix a pair of bounds in $d - 1$ of them and run Kadane on the last, for $O(n^{2d - 1})$ time on an array of side $n$.

## When to use it

Use it for the largest-sum rectangle in a matrix of moderate size, up to a few thousand on the short side. It is simple, has no large constants, and uses little memory. The subcubic methods are of theoretical interest; their gain is too small to matter in practice. For a $0/1$ matrix and the largest rectangle of ones, use the linear [maximal rectangle](/maximal-rectangle-binary-matrix/) method instead.

## Pitfalls

- **Wrong orientation.** On a $10 \times 10^4$ matrix, bands of rows cost $10^2 \cdot 10^4 = 10^6$, but bands of columns cost $10^8 \cdot 10 = 10^9$. Put the short side on the rows.
- **Not resetting $C$.** Line L3 must zero $C$ for each new top row; otherwise the band sums include rows above $a$.
- **All negative entries.** Kadane with the empty subarray allowed returns $0$, which is wrong for a non-empty rectangle. Use the non-empty form, as in line L6.
- **Recomputing band sums.** Summing the rows $a..b$ again for each band costs $\Theta(m^3 n)$ in total. Update $C$ by one row at a time, or use column prefix sums.

## Implementations

## History

Ulf Grenander posed the two-dimensional problem at Brown University, as the maximum likelihood estimate of a pattern in a digitized picture. The one-dimensional problem was its simplification, and Kadane's linear scan followed in 1977. Bentley's Programming Pearls column of 1984 told the story and gave cubic time as the best known for the two-dimensional problem, which the reduction to column sums reaches. Tamaki and Tokuyama (1998) and Takaoka (2002) found slightly subcubic algorithms, and Backurs, Dikkala and Tzamos (2016) showed that a polynomially faster one would refute the APSP conjecture.

## References
