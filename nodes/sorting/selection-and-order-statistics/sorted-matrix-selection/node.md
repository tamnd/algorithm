---
tag: P408WF
kind: problem
slug: sorted-matrix-selection
name: Selection in sorted matrices
aliases:
- k-th smallest in a row- and column-sorted matrix
area: sorting/selection-and-order-statistics
level: advanced
summary: Find the k-th smallest entry of a matrix whose rows and columns are sorted.
model: comparison-model
complexity:
  vars: {m: the number of rows, n: the number of columns, with m ≤ n}
  time: {worst: Θ(m log(2n/m))}
prereqs: [selection-problem, binary-search]
see_also: [sorted-matrix-search, staircase-search, young-tableau, median-of-two-sorted-arrays, binary-search-on-answer, parametric-search, k-way-merge, binary-heap]
sources:
  - paper: doi:10.1137/0213002
    title: Greg N. Frederickson and Donald B. Johnson, Generalized selection and ranking, sorted matrices, SIAM Journal on Computing 13(1) (1984)
    locator: pages 14 to 30 (selection in an m by n sorted matrix in O(m log(2n/m)) time, which is optimal)
  - paper: doi:10.1016/0022-0000(82)90048-4
    title: Greg N. Frederickson and Donald B. Johnson, The complexity of selection and ranking in X + Y and matrices with sorted columns, Journal of Computer and System Sciences 24(2) (1982)
    locator: pages 197 to 208 (selection in X + Y and in matrices with sorted columns)
  - paper: doi:10.1137/0207013
    title: Donald B. Johnson and Tetsuo Mizoguchi, Selecting the Kth element in X + Y and X1 + X2 + ... + Xm, SIAM Journal on Computing 7(2) (1978)
    locator: pages 147 to 153 (selection in X + Y in O(n log n) time)
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Chapter 6 problems, Young tableaus (a matrix with sorted rows and columns, and extracting its minimum)
---

Selection in a sorted matrix asks for the $k$-th smallest entry of an $m \times n$ matrix whose rows and whose columns are each in increasing order. The matrix has $mn$ entries, but the order structure means that far fewer must be looked at: Frederickson and Johnson (1984) showed that $O(m \log(2n/m))$ time suffices for $m \le n$, which is $O(n)$ for a square matrix, and that this is optimal. Simpler methods, a heap over the rows and a [binary search on the answer](/binary-search-on-answer/) with a staircase count, are what most programs use. The problem is the core of selection in sums $X + Y$ and of many optimization problems solved by [parametric search](/parametric-search/).

## In plain words

Picture a table of numbers where each row goes up from left to right and each column goes up from top to bottom. The smallest number is in the top left corner and the largest in the bottom right. You want, say, the 100th smallest number in the table.

Because of the order, you can count very quickly how many numbers are at most a given value: start in the bottom left corner and walk a staircase path toward the top right, moving right while the numbers are small enough and up when they are too big. With this count you can guess a value, see whether too few or too many numbers are below it, and adjust the guess, as in a binary search.

## Definition

**Input.** An $m \times n$ matrix $X$ with $X[i][j] \le X[i][j+1]$ and $X[i][j] \le X[i+1][j]$ for all valid $i$ and $j$, and a rank $k$ with $1 \le k \le mn$. By turning the matrix if needed, assume $m \le n$.

**Output.** The $k$-th entry of the sorted order of the $mn$ entries.

**Model.** The entries can be read in $O(1)$ time each, often because they are given by a formula, such as $X[i][j] = x_i + y_j$, and are never all written down. The cost is the number of entries read and compared.

## Variants

- **Ranking.** Given a value $t$, count the entries at most $t$. The staircase walk does it in $O(m + n)$ time.
- **Sums $X + Y$.** For sorted lists $x_1 \le \cdots \le x_m$ and $y_1 \le \cdots \le y_n$, the matrix $X[i][j] = x_i + y_j$ is sorted, so the $k$-th smallest pairwise sum is a sorted-matrix selection. Sorting the lists first costs $O(n \log n)$.
- **Columns sorted only.** If only the columns are sorted, the matrix is $n$ sorted lists, and selection is the problem of selecting in the union of sorted arrays, studied in the same 1982 paper of Frederickson and Johnson. With two columns it is the [median of two sorted arrays](/median-of-two-sorted-arrays/).
- **Search instead of selection.** Deciding whether a value occurs in the matrix is [search in a sorted matrix](/sorted-matrix-search/), done by the [staircase search](/staircase-search/) in $O(m + n)$ time.
- **Young tableaux.** A sorted matrix that may have empty cells is a [Young tableau](/young-tableau/), used as a priority queue in a CLRS problem.

## Examples

Take the sorted matrix

$$ X = \begin{pmatrix} 1 & 5 & 9 \\ 10 & 11 & 13 \\ 12 & 13 & 15 \end{pmatrix} $$

and $k = 8$. The sorted entries are $1, 5, 9, 10, 11, 12, 13, 13, 15$, so the answer is $13$.

**Counting by the staircase.** To count the entries at most $t = 12$, start at the bottom left, $X[3][1] = 12 \le 12$: the whole first column is at most $12$, so add $3$ and move right. $X[3][2] = 13 > 12$, so move up. $X[2][2] = 11 \le 12$: add $2$, the top two entries of column 2, and move right. $X[2][3] = 13 > 12$, so move up. $X[1][3] = 9 \le 12$: add $1$ and move right, past the end. The count is $6$. The same walk for $t = 13$ gives $3 + 3 + 2 = 8$. Since $6 < 8 \le 8$, the answer is the least entry above $12$ that has count at least $8$, which is $13$.

**By a heap.** Put the first entry of each row in a min-heap: $1, 10, 12$. Pop the minimum and push the next entry of its row, $k$ times. The pops are $1, 5, 9, 10, 11, 12, 13, 13$, and the eighth is $13$.

## Known algorithms

| method | time | notes |
|---|---|---|
| list all entries, then [quickselect](/quickselect/) | $O(mn)$ | ignores the order |
| heap of row heads, $k$ pops | $O(m + k \log m)$ | good for small $k$; like a [k-way merge](/k-way-merge/) |
| binary search on values with staircase counts | $O((m + n) \log R)$ | integer entries in a range of size $R$ |
| random entry as pivot, staircase partition | $O((m + n) \log(mn))$ expected | each round keeps a random part of the candidates |
| Frederickson and Johnson (1984) | $O(m \log(2n/m))$ | optimal; $O(n)$ for a square matrix |

**Binary search on the answer.** The count $c(t)$ of entries at most $t$ is nondecreasing in $t$, and the answer is the least entry $t$ with $c(t) \ge k$. For integer entries, a [binary search](/binary-search/) over $[X[1][1], X[m][n]]$ needs $O(\log R)$ counts of $O(m + n)$ each. For arbitrary entries, the search runs over the candidate entries instead: keep, for each row, the range of columns that can still hold the answer, pick a candidate pivot, count, and shrink the ranges.

**Frederickson and Johnson.** Their method works on a hierarchy of square submatrices. The corner entries of a submatrix bound all of its entries, so a pivot chosen from the corners lets whole submatrices that lie above or below the answer be discarded at once. Choosing the pivots as suitable medians of the corners removes a constant fraction of the remaining candidates in each round, and for $m \le n$ the total time is $O(m \log(2n/m))$.

## Bounds

- **Upper bound.** $O(m \log(2n/m))$ time, by Frederickson and Johnson; for $m = n$ this is $O(n)$, which is less than the $n^2$ entries.
- **Lower bound.** Frederickson and Johnson also proved a matching $\Omega(m \log(2n/m))$ lower bound in the comparison model: there are that many bits in the choice of which entries in each row lie below the answer. For a square matrix this is $\Omega(n)$.
- **Sums.** Selection in $X + Y$ takes $O(n)$ time once $x$ and $y$ are sorted, and $O(n \log n)$ in total; Johnson and Mizoguchi gave the first $O(n \log n)$ method in 1978.

## Reductions

- **From $X + Y$.** Selecting the $k$-th pairwise sum reduces to sorted-matrix selection after sorting $x$ and $y$.
- **To selection.** Listing all entries and running a linear-time selection solves the problem in $O(mn)$ time.
- **From optimization.** Many problems of the form "the least value $t$ for which a monotone test passes", where the candidate values are the entries of an implicit sorted matrix, such as distances $|p_i - q_j|$ between sorted points, are solved by selecting in that matrix and testing, the method of Frederickson and Johnson for location and partitioning problems on trees and paths.

## Applications

- **Location on trees and paths.** Frederickson and Johnson used sorted-matrix selection to solve the $p$-center problem on a tree and the partition of a path into parts of bounded weight, where the candidate values form sorted matrices.
- **The $k$-th smallest pair.** Finding the $k$-th smallest sum, difference or distance of pairs from two sorted lists, a common task in statistics, such as the Hodges-Lehmann estimator, which is a median of pairwise averages.
- **Programming contests.** The heap and the binary search with staircase counts are standard answers for the $k$-th smallest entry of a sorted matrix.

## References
