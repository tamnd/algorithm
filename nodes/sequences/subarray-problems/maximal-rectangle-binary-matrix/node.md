---
tag: 8H065B
kind: problem
slug: maximal-rectangle-binary-matrix
name: Maximal rectangle in a binary matrix
aliases:
- largest rectangle of ones in a binary matrix
area: sequences/subarray-problems
level: core
summary: Find the largest all-ones rectangle in a 0/1 matrix by reducing each row to a histogram.
prereqs: [largest-rectangle-in-histogram, histogram-stack-algorithm]
see_also: [maximum-sum-submatrix, two-dimensional-prefix-sums, largest-empty-rectangle, monotonic-stack, cartesian-tree, bentley-column-sweep, range-sum-query-2d, subarray]
sources:
  - url: https://www.drdobbs.com/database/the-maximal-rectangle-problem/184410529
    title: "David Vandevoorde, The Maximal Rectangle Problem, Dr. Dobb's Journal 23(4), April 1998"
    locator: the problem, the brute-force method, the row profile and the stack of open rectangles in linear time
  - url: https://leetcode.com/problems/maximal-rectangle/
    title: LeetCode, problem 85, Maximal Rectangle
    locator: problem statement and the 4 by 5 example with answer 6
  - url: https://leetcode.com/problems/maximal-square/
    title: LeetCode, problem 221, Maximal Square
    locator: problem statement
  - url: https://leetcode.com/problems/count-submatrices-with-all-ones/
    title: LeetCode, problem 1504, Count Submatrices With All Ones
    locator: problem statement
---

The maximal rectangle problem asks, for a matrix of $0$s and $1$s, for the largest axis-parallel rectangle that contains only $1$s. A rectangle is a block of consecutive rows and consecutive columns. The standard solution turns each row into a histogram: the height of column $j$ in row $i$ is the number of consecutive $1$s that end at row $i$ in that column. A rectangle of ones whose bottom row is $i$ is then a rectangle under the histogram of row $i$, so the answer is the best over the rows of the [largest rectangle in a histogram](/largest-rectangle-in-histogram/). With the [histogram stack algorithm](/histogram-stack-algorithm/) on each row, an $r \times c$ matrix takes $\Theta(rc)$ time, which is linear in its size and optimal.

## In plain words

You have a grid of cells, each one full or empty. You want the biggest rectangle made only of full cells.

Go through the grid one row at a time, from the top. For each column, count how many full cells stand in an unbroken column ending at the current row. An empty cell sets the count back to zero. These counts are like a bar chart that stands on the current row.

Any all-full rectangle whose bottom edge is on the current row fits under that bar chart, and the other way round. So find the largest rectangle under each row's bar chart, and keep the best over all rows.

## Definition

**Input.** A matrix $M$ with $r$ rows and $c$ columns, with $M[i][j] \in \{0, 1\}$.

**Output.** The largest area $(b - a + 1)(d - e + 1)$ over all row ranges $a..b$ and column ranges $e..d$ such that $M[i][j] = 1$ for all $a \le i \le b$ and $e \le j \le d$, or $0$ if $M$ has no $1$. Also a rectangle that reaches it.

**Row histograms.** Let
$$H_i[j] = \begin{cases} H_{i-1}[j] + 1 & \text{if } M[i][j] = 1, \\ 0 & \text{if } M[i][j] = 0, \end{cases}$$
with $H_{-1}[j] = 0$. A rectangle of ones with rows $a..b$ and columns $e..d$ has $H_b[j] \ge b - a + 1$ for $e \le j \le d$, so it lies under the histogram $H_b$. Conversely, a rectangle of height $t$ under $H_b$ on columns $e..d$ is a rectangle of ones with rows $b - t + 1..b$. So
$$\text{answer} = \max_{0 \le i \le r - 1} \text{LargestRectangle}(H_i).$$

## Variants

- **Largest square.** The largest all-ones square is found by the recurrence $Q[i][j] = 1 + \min(Q[i-1][j], Q[i][j-1], Q[i-1][j-1])$ for a cell with $M[i][j] = 1$, in $\Theta(rc)$ time (LeetCode 221).
- **Count the rectangles.** Count all submatrices of ones (LeetCode 1504). With the row histograms and a monotonic stack, the count of rectangles with their bottom-right corner at each cell is found in $O(1)$ amortized time, so $\Theta(rc)$ in total.
- **General weights.** If the cells hold numbers of any sign and the goal is the largest sum, the problem is the [maximum sum submatrix](/maximum-sum-submatrix/). It is much harder: the known algorithms take about cubic time.
- **Points instead of cells.** The [largest empty rectangle](/largest-empty-rectangle/) among $n$ points in a box is the continuous form, with zeros as points.
- **Zeros allowed.** A rectangle with at most $z$ zeros can be tested in $O(1)$ with [two-dimensional prefix sums](/two-dimensional-prefix-sums/) of the zeros, which gives an $O(r^2 c)$ method with a sliding window over columns for each pair of rows.

## Examples

**The standard example.** For
$$M = \begin{pmatrix} 1 & 0 & 1 & 0 & 0 \\ 1 & 0 & 1 & 1 & 1 \\ 1 & 1 & 1 & 1 & 1 \\ 1 & 0 & 0 & 1 & 0 \end{pmatrix}$$
the row histograms are $H_0 = [1, 0, 1, 0, 0]$, $H_1 = [2, 0, 2, 1, 1]$, $H_2 = [3, 1, 3, 2, 2]$ and $H_3 = [4, 0, 0, 3, 0]$. Their largest rectangles have areas $1$, $3$, $6$ and $4$. The answer is $6$: in $H_2$, height $2$ over columns $2..4$, which is the block of rows $1..2$ and columns $2..4$.

**A tall answer.** In the same matrix, column $0$ is all ones, an area of $4$, which $H_3$ finds. It is not the best, but it shows that the best rectangle of a row can be one column wide.

**No ones.** For a matrix of zeros, every histogram is zero and the answer is $0$.

## Known algorithms

| method | time | extra space | idea |
|---|---|---|---|
| all rectangles, checked with 2D prefix sums | $\Theta(r^2 c^2)$ | $\Theta(rc)$ | a rectangle is all ones when its sum is its area |
| all pairs of rows, runs of full columns | $\Theta(r^2 c)$ | $\Theta(c)$ | for rows $a..b$, the longest run of columns full in all of them |
| row histograms and the [histogram stack algorithm](/histogram-stack-algorithm/) | $\Theta(rc)$ | $\Theta(c)$ | one histogram problem per row |
| row histograms with left and right limits | $\Theta(rc)$ | $\Theta(c)$ | carry, per column, the height and the left and right ends of its widest rectangle from row to row |

**Left and right limits.** For each column $j$ of row $i$, keep $H_i[j]$ and the left and right ends of the widest run of columns with height at least $H_i[j]$ around $j$. These ends come from the previous row's ends and the current row's run of ones, in two scans of the row. The area at $j$ is $H_i[j]$ times the width. This avoids a stack but does the same work.

## Bounds

**Linear time is optimal.** Every cell must be read. If an algorithm does not read cell $(i, j)$ of a matrix of ones, that cell may be $0$, which changes the answer from $rc$ to a smaller value when $r, c \ge 2$. So $\Omega(rc)$ time is needed, and the histogram method reaches it.

**Memory.** The method keeps one row of heights and a stack of at most $c + 1$ indices, so $\Theta(c)$ extra space. Reading the matrix by columns instead uses $\Theta(r)$, so $\Theta(\min(r, c))$ is enough.

## Reductions

- **To histograms.** The maximal rectangle problem on $r \times c$ is $r$ instances of the largest rectangle in a histogram of $c$ bars, after an $O(rc)$ pass for the heights.
- **From histograms.** A histogram with heights at most $r$ is the matrix whose column $j$ has ones in its bottom $h_j$ rows. This costs $\Theta(rc)$ to build, so it shows the matrix problem is at least as hard as the histogram one only when the heights are small.
- **Largest square to rectangle.** The largest square is the largest $\min(\text{height}, \text{width})$ over the same histogram rectangles, but its own recurrence is simpler.

## Applications

- **Image analysis.** The largest uniform rectangle in a binary image, such as the largest block of background in a scanned page, which helps to find white space in page layout.
- **Grid maps.** The largest free rectangle in an occupancy grid for robots, or the largest free area in a floor plan.
- **Layout and packing.** The largest free rectangle on a chip, a sheet or a storage area, as a step in placing the next item.

## References
