---
tag: C63QRR
kind: problem
slug: sorted-matrix-search
name: Search in a row- and column-sorted matrix
aliases:
- saddleback search problem
area: searching/sequential-and-binary-search
level: core
summary: Decide whether a key occurs in a matrix whose rows and columns are both sorted.
model: comparison-model
complexity:
  vars: {m: the number of rows, n: the number of columns, with m ≤ n}
  time: {worst: Θ(m log(2n/m))}
prereqs: [search-in-sorted-array, binary-search]
see_also: [staircase-search, young-tableau, sorted-matrix-selection, two-sum, adversary-argument, search-in-sorted-array, binary-search, dominance-counting]
sources:
  - paper: doi:10.1016/0196-6774(85)90020-3
    title: Nathan Linial and Michael Saks, Searching ordered structures, Journal of Algorithms 6(1) (1985)
    locator: pp. 86 to 103 (bounds for search in an m by n matrix with sorted rows and columns)
  - paper: doi:10.1007/11783596_8
    title: Richard S. Bird, Improving saddleback search, a lesson in algorithm design, Mathematics of Program Construction (MPC 2006), LNCS 4014
    locator: pp. 82 to 89 (saddleback search is not best when one side is much shorter than the other)
---

Search in a row- and column-sorted matrix asks whether a key $x$ occurs in an $m \times n$ matrix $M$ whose every row and every column is non-decreasing, and where. The order is only partial: $M[0][n-1]$ and $M[m-1][0]$ can be in any order, so the matrix is not one sorted list, and a single [binary search](/binary-search/) does not work. The [staircase search](/staircase-search/), also called saddleback search, walks from the top-right corner and drops one row or one column at each step, so it uses at most $m + n - 1$ reads. For a square matrix this is exactly optimal: an adversary with two anti-diagonals forces $2n - 1$ reads. When one side is much shorter, $m \ll n$, a divide-and-conquer method with binary searches is better, and $\Theta(m \log(2n/m))$ comparisons is the right order.

## In plain words

Think of a seating chart of a theater where the ticket numbers grow from left to right in each row and from front to back in each column. You want to know if ticket 57 is in the theater.

Stand at the front row, far right seat. If the number there is too big, the whole column behind you is too big too, so you step one seat left. If the number is too small, the whole row to your left is too small, so you step one row back. Each look throws away a full row or a full column. After at most the number of rows plus the number of columns, you find the ticket or walk out of the chart.

When the theater has only a few very long rows, you can do better by searching each row by halving.

## Definition

**Input.** An $m \times n$ matrix $M$ over a [total order](/total-order/), with
$$ M[i][j] \le M[i][j+1] \quad\text{and}\quad M[i][j] \le M[i+1][j] $$
for all indices in range, and a key $x$.

**Output.** A pair $(i, j)$ with $M[i][j] = x$, or NIL when no cell holds $x$.

The cost is the number of reads of cells, or the number of comparisons of $x$ with cells. When $x$ occurs more than once, any of its cells is a correct answer. By symmetry (transpose $M$) we can assume $m \le n$.

**The shape of the answer.** The cells with $M[i][j] < x$ form a staircase in the top-left corner: if a cell is less than $x$, so are all cells above it and to its left. The cells with $M[i][j] > x$ form a staircase in the bottom-right corner. The cells equal to $x$ lie in the band between the two.

## Variants

- **[Young tableau](/young-tableau/).** The same order, often with $+\infty$ in the empty cells. Search is this problem; insert and extract-min are heap-like operations on it.
- **Counting.** Count the cells with $M[i][j] \le x$. The staircase walk gives this in $O(m + n)$ time, by adding the column index plus one at each row where it moves down.
- **Selection.** Find the $k$-th smallest cell. This is [selection in a sorted matrix](/sorted-matrix-selection/), solved in $O(m \log(2n/m))$ time by Frederickson and Johnson.
- **Fully sorted matrix.** When each row starts after the previous row ends ($M[i][n-1] \le M[i+1][0]$), the matrix is one sorted list of $mn$ items in row-major order, and one binary search on the index $k = in + j$ uses $\lceil \lg(mn + 1) \rceil$ comparisons.
- **Higher dimensions.** A $d$-dimensional array sorted along every axis. The staircase idea gives $O(n^{d-1})$ for side $n$.

## Examples

The matrix used on many pages:

| | 0 | 1 | 2 | 3 | 4 |
|---|---|---|---|---|---|
| 0 | 1 | 4 | 7 | 11 | 15 |
| 1 | 2 | 5 | 8 | 12 | 19 |
| 2 | 3 | 6 | 9 | 16 | 22 |
| 3 | 10 | 13 | 14 | 17 | 24 |

Rows and columns are sorted, but the matrix is not sorted in row-major order: $M[0][4] = 15 > M[1][0] = 2$.

- **$x = 9$.** The staircase walk from $(0, 4)$ reads 15, 11, 7, 8, 9: $15 > 9$ left, $11 > 9$ left, $7 < 9$ down, $8 < 9$ down, $9 = 9$. It returns $(2, 2)$ after 5 reads.
- **$x = 20$.** It reads 15, 19, 22, 16, 17: down, down, left, down, down, and leaves the matrix after 5 reads. The answer is NIL.

**Worst cases.** The table gives the largest number of reads over all keys on the matrix $M[i][j] = 2(in + j)$, found by a script, for the staircase walk and for the divide-and-conquer method described below:

| $m \times n$ | $10 \times 10$ | $100 \times 100$ | $10 \times 1000$ | $10 \times 100000$ |
|---|---|---|---|---|
| staircase walk | 19 | 199 | 1009 | 100009 |
| divide and conquer | 21 | 81 | 60 | 102 |
| $m + n - 1$ | 19 | 199 | 1009 | 100009 |

On these inputs the staircase walk reaches $m + n - 1$, while divide and conquer grows only slowly with $n$ when $m$ is fixed.

## Known algorithms

- **[Staircase search](/staircase-search/).** Start at $(0, n-1)$. If $M[i][j] = x$, stop. If $M[i][j] > x$, every cell below it in column $j$ is also $> x$, so $j \gets j - 1$. If $M[i][j] < x$, every cell to its left in row $i$ is $< x$, so $i \gets i + 1$. Each read removes a row or a column, so it uses at most $m + n - 1$ reads, $\Theta(m + n)$ time and $\Theta(1)$ space. It is optimal for square matrices and good when $m$ and $n$ are close.
- **Binary search in each row.** Search each of the $m$ rows with a binary search: $m \lceil \lg(n+1) \rceil$ comparisons. This is better than the staircase when $m \lg n < m + n$, that is when $m$ is small.
- **Divide and conquer.** Take the middle row of the current submatrix and find, by binary search, the first column $c$ with $M[r][c] \ge x$. If $M[r][c] = x$, stop. Otherwise the cells above row $r$ from column $c$ on, and the cells below row $r$ before column $c$, are the only candidates, and the method recurses on these two parts (cutting along columns instead when the part is taller than wide). Bird analyses this method and shows that it uses $O(m \log(2n/m))$ comparisons, which is better than the staircase when $m \ll n$.
- **Quadrant elimination.** Compare $x$ with the center cell. If it is smaller, the bottom-right quadrant is out; if larger, the top-left quadrant is out. Three quadrants are left, which gives the recurrence $T(N) = 3T(N/4) + O(1)$ and $O(N^{\log_4 3}) = O(n^{1.59})$ for an $n \times n$ matrix. It is worse than the staircase and is shown here only as a trap.

## Bounds

**Upper bound.** $\min\bigl(m + n - 1,\ O(m \log(2n/m))\bigr)$ reads, by the staircase walk and by divide and conquer.

**Lower bound for square matrices.** Each correct algorithm reads at least $2n - 1$ cells of some $n \times n$ input, and at least $2m$ cells of some $m \times n$ input with $m < n$.

*Proof.* Call $d = i + j$ the anti-diagonal of cell $(i, j)$. Fix $x$, and take the *band* $B$ of cells on the two anti-diagonals $d = m - 1$ and $d = m$. For $m = n$ the band has $n + (n - 1) = 2n - 1$ cells, and for $m < n$ it has $m + m = 2m$ cells. Let $x = 2m - 1$ and build the default matrix $D$:
$$ D[i][j] = \begin{cases} 2(i + j) & \text{if } i + j \le m - 1, \\ 2(i + j) + 2 & \text{if } i + j \ge m. \end{cases} $$
A step right or down raises $d$ by 1 and the value by 2 or 4, so $D$ is sorted. No cell is $2m - 1$, so the answer on $D$ is NIL. For a band cell $c$, let $D_c$ be $D$ with $c$ set to $x = 2m - 1$. If $c$ is on $d = m - 1$, its old value was $2m - 2$, its neighbors above and to the left hold at most $2m - 4$, and its neighbors below and to the right hold $2m + 2$. If $c$ is on $d = m$, its old value was $2m + 2$, its neighbors above and to the left hold $2m - 2$, and those below and to the right hold $2m + 4$. In both cases $D_c$ is still sorted, and its only copy of $x$ is at $c$. Now run a correct algorithm on $D$. If it never reads $c$, then every read and every comparison it makes has the same result on $D_c$, so it gives the same answer NIL on $D_c$, which is wrong. So it reads every band cell. $\blacksquare$

For $m = n$ this lower bound is $2n - 1 = m + n - 1$, the cost of the staircase walk, so the walk is exactly optimal for square matrices. The argument is an [adversary argument](/adversary-argument/) in its simplest form.

**Lower bound for thin matrices.** Linial and Saks prove that, for $m \le n$, search needs a number of comparisons of the order $m \lg(n/m)$, which matches the divide-and-conquer bound up to a constant factor. So $\Theta(m \log(2n/m))$ is the complexity of the problem. For $m = 1$ it is $\Theta(\log n)$, a [search in a sorted array](/search-in-sorted-array/), and for $m = n$ it is $\Theta(n)$.

## Reductions

- **[Search in a sorted array](/search-in-sorted-array/) is the case $m = 1$.** So the $\lceil \lg(n+1) \rceil$ lower bound for sorted arrays is a lower bound here too.
- **[Two sum](/two-sum/) on sorted arrays reduces to it.** For sorted $a$ and $b$, the matrix $M[i][j] = a[i] + b[j]$ is sorted along rows and columns, and a pair with $a[i] + b[j] = t$ is a cell equal to $t$. The staircase walk on $M$, which starts at $(0, n-1)$, is the [two pointers](/two-pointers/) scan, and it never builds the matrix.
- **Monotone functions of two variables.** Finding all pairs $(i, j)$ with $f(i, j) = t$ for $f$ that grows in each argument (Bird's original setting) is this problem with $M[i][j] = f(i, j)$ computed on demand.
- **Counting cells $\le x$** is the [dominance counting](/dominance-counting/) idea on a grid, and it is the inner step of [selection in a sorted matrix](/sorted-matrix-selection/) by binary search on the value.

## Applications

- Search in a [Young tableau](/young-tableau/) used as a priority queue.
- Solve $f(i, j) = t$ for a monotone $f$ over a grid, such as finding all $(i, j)$ with $i^2 + 3j^2 = t$, without trying all pairs.
- The $k$-th smallest pair sum $a[i] + b[j]$ of two sorted lists, by counting with the staircase walk inside a binary search on the value.
- Tables sorted in two keys at once, such as a price table where cost rises with size and with distance.

## References
