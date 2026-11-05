---
tag: 2QRZFX
kind: problem
slug: kth-smallest-pair-distance
name: Kth smallest pair distance
aliases:
- k-th smallest distance among pairs
- kth smallest pairwise difference
area: searching/search-on-answers
level: advanced
summary: Find the k-th smallest of the n(n-1)/2 pairwise distances without enumerating all pairs.
model: algebraic-decision-tree
complexity:
  vars: {n: the number of values}
  time: {worst: Θ(n log n)}
prereqs: [binary-search-on-answer, two-pointers, selection-problem]
see_also: [binary-search-on-answer, sorted-matrix-selection, maximin-placement, selection-problem, element-distinctness, two-pointers, parametric-search, order-statistic]
sources:
  - url: https://leetcode.com/problems/find-k-th-smallest-pair-distance/
    title: LeetCode 719, Find K-th Smallest Pair Distance
  - paper: doi:10.1137/0213002
    title: "Greg N. Frederickson and Donald B. Johnson, Generalized selection and ranking: sorted matrices, SIAM Journal on Computing 13(1) (1984), 14-30"
    note: selection in a matrix with sorted rows and columns in linear time in the number of rows
  - paper: doi:10.1145/299917.299918
    title: "Pankaj K. Agarwal and Micha Sharir, Efficient algorithms for geometric optimization, ACM Computing Surveys 30(4) (1998), 412-458"
    note: distance selection and slope selection as applications of parametric search
---

The k-th smallest pair distance problem asks, for $n$ numbers, for the $k$-th smallest of the $n(n-1)/2$ distances $|a_i - a_j|$ between two of them. Listing all distances takes $\Theta(n^2)$ time, but the number of distances at most $d$ can be counted with [two pointers](/two-pointers/) in $O(n)$ time on the sorted values, and it is non-decreasing in $d$, so [binary search on the answer](/binary-search-on-answer/) finds the $k$-th distance in $O(n \log n + n \log U)$ time for integers with range $U$. The distances also form a matrix with sorted rows and columns, and [sorted-matrix selection](/sorted-matrix-selection/) gives an exact $O(n \log n)$ algorithm, which is optimal. It is the simplest instance of selection in a large set that is given implicitly.

## In plain words

You have a list of numbers. Take every pair of them and write down how far apart the two numbers are. You want the fifth smallest of these distances, or the thousandth. With many numbers there are far too many pairs to write down.

Instead, guess a distance and count how many pairs are at most that far apart. Counting is fast: sort the numbers, and for each number walk a second finger forward to the first number that is close enough; the finger never moves back. If the count reaches $k$, the answer is at most your guess; if not, it is larger. So you can halve the range of guesses until one is left.

## Definition

**Input.** Real numbers $a_1, \ldots, a_n$ with $n \ge 2$, not necessarily distinct, and an integer $k$ with $1 \le k \le n(n-1)/2$.

**Output.** The $k$-th smallest element $D_{(k)}$ of the multiset $D = \{\, |a_i - a_j| : 1 \le i < j \le n \,\}$, counted with multiplicity.

**The counting function.** Let $c(d) = |\{(i, j) : i < j,\ |a_i - a_j| \le d\}|$. It is non-decreasing in $d$, and

$$c(d) \ge k \iff D_{(k)} \le d.$$

*Proof.* If $D_{(k)} \le d$, the $k$ smallest distances are all at most $d$, so $c(d) \ge k$. If $D_{(k)} > d$, at most $k - 1$ distances are below $D_{(k)}$, so $c(d) \le k - 1$. $\square$ So the predicate $c(d) \ge k$ is a [monotone predicate](/monotone-predicate/), and $D_{(k)}$ is the smallest $d$ where it holds. Since $D_{(k)}$ is itself a distance, the smallest such $d$ is attained.

## Variants

- **The k-th largest distance.** The $k$-th largest is $D_{(N - k + 1)}$ with $N = n(n-1)/2$.
- **Sums instead of differences.** The $k$-th smallest $x_i + y_j$ over two sorted arrays, selection in $X + Y$, has the same structure: the sums form a sorted matrix.
- **Subarray sums.** The $k$-th smallest sum of a contiguous subarray is the $k$-th smallest difference $P_j - P_i$ of [prefix sums](/prefix-sums/). The prefix sums are not sorted when items are negative, so the count of differences at most $d$ needs a merge-sort or Fenwick-tree count of pairs, in $O(n \log n)$ per test, like [counting inversions](/counting-inversions/).
- **Fractions.** The $k$-th smallest fraction $a_i / a_j$ of a sorted array of positive numbers is found by a real binary search with a two-pointer count of the fractions at most $t$.
- **Points in the plane.** The $k$-th smallest of the Euclidean distances between $n$ points, distance selection, has no sorted structure, and is a standard application of [parametric search](/parametric-search/); the best algorithms take more than $n \log n$ but less than quadratic time (Agarwal and Sharir).
- **Slope selection.** The $k$-th smallest slope of the lines through pairs of $n$ points in the plane is related; it can be counted by inversions, and it is solvable in $O(n \log n)$ time.

## Examples

**A small array.** Let $a = (1, 6, 1, 3, 10)$ and $k = 5$. Sorted: $1, 1, 3, 6, 10$. The ten distances, sorted, are $0, 2, 2, 3, 4, 5, 5, 7, 9, 9$, so $D_{(5)} = 4$. The two-pointer count for $d = 4$ keeps, for each $j$, the first $i$ with $a_j - a_i \le 4$:

| j | $a_j$ | first i | pairs ending at j |
|---|---|---|---|
| 1 | 1 | 1 | 0 |
| 2 | 1 | 1 | 1 |
| 3 | 3 | 1 | 2 |
| 4 | 6 | 3 | 1 |
| 5 | 10 | 4 | 1 |

So $c(4) = 5 \ge 5$. The smallest-feasible search on $[0, 9]$ tests $d = 4$ ($c = 5$, yes), $d = 2$ ($c = 3$, no), $d = 3$ ($c = 4$, no), and returns $4$.

**The smallest distance.** For $k = 1$, $D_{(1)}$ is the smallest gap between sorted neighbours, found in $O(n)$ after sorting. For $a = (1, 3, 1)$ it is $0$.

**The largest distance.** For $k = n(n-1)/2$, $D_{(k)} = \max a - \min a$, found in $O(n)$ without sorting.

## Known algorithms

**Brute force.** List the $n(n-1)/2$ distances and select the $k$-th with [quickselect](/quickselect/): $\Theta(n^2)$ expected time and $\Theta(n^2)$ space.

**A heap of pairs.** On the sorted values, the distances $a_j - a_i$ for a fixed $i$ increase with $j$. Put $(i, i+1)$ for each $i$ into a [priority queue](/priority-queue/), pop the smallest $k$ times, and after popping $(i, j)$ push $(i, j + 1)$. This takes $O((n + k) \log n)$ time and is good for small $k$.

**Binary search with a two-pointer count.** Sort the values. For a threshold $d$, move $j$ from left to right and keep the smallest $i$ with $a_j - a_i \le d$; since $a_j$ grows, $i$ never moves back, so the count $c(d) = \sum_j (j - i)$ takes $O(n)$ time. For integers, a smallest-feasible search over $[0, \max a - \min a]$ gives $O(n \log n + n \log U)$ time. This is the usual solution of LeetCode 719.

**Exact selection in a sorted matrix.** With the values sorted, the $n \times n$ matrix $M[i][j] = a_j - a_i$ has non-decreasing rows and non-increasing columns. Its $n^2$ entries are the $n(n-1)/2$ values $-D$ (below the diagonal, all $\le 0$), $n$ zeros on the diagonal, and the $n(n-1)/2$ values of $D$ (above the diagonal, all $\ge 0$). So in the sorted order of all entries, the entry of rank $n(n-1)/2 + n + k$ is $D_{(k)}$. Frederickson and Johnson select an entry of given rank in such a matrix in $O(n)$ time, so the total is $O(n \log n)$ for the sort and $O(n)$ for the selection, for any real input.

## Bounds

- **Upper bound.** $O(n \log n)$, by sorting and sorted-matrix selection.
- **Lower bound.** $\Omega(n \log n)$ in the [algebraic decision tree](/algebraic-decision-tree/) model, already for $k = 1$. *Proof.* $D_{(1)} = 0$ holds exactly when two values are equal. So an algorithm for the problem decides [element distinctness](/element-distinctness/) with $O(1)$ more operations, and element distinctness needs $\Omega(n \log n)$ operations in this model. $\square$
- **Sorted input.** If the values are given sorted, the selection takes $\Theta(n)$ time: the upper bound by Frederickson and Johnson, the lower bound because each value must be read.

## Reductions

- **To a monotone count.** The problem reduces to $O(\log U)$ counts, or to a binary search on the rank in the sorted matrix with $O(\log n)$ counts. This is the [optimization-to-decision reduction](/optimization-to-decision-reduction/) for a selection.
- **To sorted-matrix selection.** As above, in $O(1)$ extra work after sorting.
- **From element distinctness.** The case $k = 1$, as in the lower bound.

## Applications

- **Robust statistics.** Scale estimators such as the median of all pairwise distances, or the Rousseeuw-Croux estimator $Q_n$, which is an order statistic of the pairwise distances, are computed by this selection instead of listing the $\Theta(n^2)$ distances.
- **Thresholds for near pairs.** Choosing a distance threshold that admits a given number of near pairs, for example in clustering or in the detection of near-duplicates.
- **A building block.** The search over pairwise differences appears inside other problems whose optimum is a difference, such as [maximin placement](/maximin-placement/).

## References
