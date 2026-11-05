---
tag: 5NYQY1
kind: problem
slug: maximum-sum-subarray-of-fixed-length
name: Maximum sum subarray of fixed length
aliases:
- maximum average subarray of length k
- maximum sum window of size k
area: sequences/subarray-problems
level: intro
summary: Find the length-k window of an array with the largest sum.
prereqs: [subarray, sliding-window, prefix-sums]
see_also: [maximum-subarray-problem, maximum-density-segment, moving-average, monotonic-deque-prefix-sums, two-dimensional-prefix-sums, box-blur, sliding-window-maximum, kahan-summation]
sources:
  - url: https://leetcode.com/problems/maximum-average-subarray-i/
    title: LeetCode, problem 643, Maximum Average Subarray I
    locator: problem statement and example
  - url: https://leetcode.com/problems/maximum-sum-of-3-non-overlapping-subarrays/
    title: LeetCode, problem 689, Maximum Sum of 3 Non-Overlapping Subarrays
    locator: problem statement (three disjoint windows of length k)
  - url: https://cses.fi/book/book.pdf
    title: Antti Laaksonen, Competitive Programmer's Handbook
    locator: Chapter 8, Amortized analysis, Section 8.3 Sliding window minimum, and Chapter 9, Section 9.1 Static array queries
---

The problem gives an array of $n$ numbers and a length $k$, and asks for the window of $k$ consecutive items with the largest sum. There are only $n - k + 1$ such windows, and the sum of each one follows from the sum of the one before by adding the item that enters and subtracting the item that leaves. So one [sliding window](/sliding-window/) pass solves the problem in $\Theta(n)$ time and $O(1)$ extra space. Since all windows have the same length, the window with the largest sum is also the window with the largest average. Without the length limit the problem is the [maximum subarray problem](/maximum-subarray-problem/), and with a lower bound on the length and averages it becomes the [maximum density segment](/maximum-density-segment/) problem.

## In plain words

You have a list of daily sales and want the best week, that is, the best run of seven days in a row. Add up the first seven days. Then move the week forward by one day: add the new day and take away the day that dropped out. Each move costs two steps, however long the week is.

Keep the best total you have seen. When the week reaches the end of the list, that best total is the answer. Since every week has the same number of days, the week with the best total also has the best daily average.

## Definition

**Input.** An array $A[0..n-1]$ of numbers and an integer $k$ with $1 \le k \le n$.

**Output.** An index $l$ with $0 \le l \le n - k$ that maximizes the window sum

$$W(l) = A[l] + A[l+1] + \dots + A[l+k-1],$$

and the value $\max_l W(l)$. The average version returns $\max_l W(l)/k$.

**Recurrence.** $W(l + 1) = W(l) + A[l + k] - A[l]$. With [prefix sums](/prefix-sums/), $W(l) = P_{l+k} - P_l$.

## Variants

- **Average of length $k$.** Divide the best sum by $k$; the best window is the same (LeetCode 643).
- **Length at least $k$.** The best sum of a subarray with at least $k$ items is $\max_j \big(P_j - \min_{0 \le i \le j - k} P_i\big)$, which one pass with a running minimum computes in $O(n)$ time.
- **Length between $L$ and $U$.** The candidates $i$ for the end $j$ form the window $[j - U, j - L]$, and its minimum prefix sum comes from a [monotonic deque](/monotonic-deque-prefix-sums/), in $O(n)$ time.
- **Average with length at least $k$.** Here longer windows can have a larger average, so the fixed-length trick fails. This is the [maximum density segment](/maximum-density-segment/) problem.
- **Several disjoint windows.** Choose $m$ disjoint windows of length $k$ with the largest total (LeetCode 689 for $m = 3$). Compute all $W(l)$, then run a dynamic program over the positions in $O(nm)$ time.
- **Two dimensions.** The $a \times b$ block of a matrix with the largest sum. Each block sum is four lookups in a [two-dimensional prefix sum](/two-dimensional-prefix-sums/) table, so all blocks take $O(nm)$ time. This is the step behind a [box blur](/box-blur/).
- **Other aggregates.** The maximum or minimum of each window instead of the sum needs a deque, see the [sliding window maximum](/sliding-window-maximum/). The sums of all windows are a [moving average](/moving-average/) up to the factor $1/k$.

## Examples

**Averages.** $A = [1, 12, -5, -6, 50, 3]$ and $k = 4$. The window sums are $W(0) = 2$, $W(1) = 51$ and $W(2) = 42$. The best window is $A[1..4] = [12, -5, -6, 50]$, with sum $51$ and average $12.75$.

**A short trace.** $A = [2, 1, 5, 1, 3, 2]$ and $k = 3$.

| $l$ | enters | leaves | $W(l)$ | best |
|---|---|---|---|---|
| 0 | | | $2 + 1 + 5 = 8$ | 8 |
| 1 | $A[3] = 1$ | $A[0] = 2$ | $8 + 1 - 2 = 7$ | 8 |
| 2 | $A[4] = 3$ | $A[1] = 1$ | $7 + 3 - 1 = 9$ | 9 |
| 3 | $A[5] = 2$ | $A[2] = 5$ | $9 + 2 - 5 = 6$ | 9 |

The answer is $9$, from $A[2..4] = [5, 1, 3]$.

**Length at least $k$.** For the first array with $k = 4$, the best subarray with at least four items is the whole array, with sum $55$. This is larger than $51$, so the two problems differ.

**Edge cases.** If $k = n$ the only window is the whole array. If $k = 1$ the answer is the largest item.

## Known algorithms

| method | time | extra space | notes |
|---|---|---|---|
| sum each window separately | $\Theta(nk)$ | $O(1)$ | the direct method |
| rolling window sum | $\Theta(n)$ | $O(1)$ | one addition and one subtraction per step |
| prefix sums | $\Theta(n)$ | $O(n)$ | $W(l) = P_{l+k} - P_l$; also answers other lengths |

The rolling sum is the standard method. It is online: after reading $A[0..r]$ with $r \ge k - 1$ it knows the best window that ends at or before $r$.

**Floating point.** With floating-point items the rolling sum adds and subtracts $n$ times, and rounding errors can build up, so a window sum may drift from its true value. Recompute the sum from scratch every so many steps, use [Kahan summation](/kahan-summation/), or use the prefix sums in exact integer arithmetic when the items are integers.

## Bounds

**Linear time is optimal.** Every item lies in some window, so an algorithm that does not read $A[m]$ cannot tell an input with a huge value at $m$ from one with a very negative value there. So $\Omega(n)$ time is needed, and the rolling sum reaches it.

**Additions.** The rolling sum makes $k - 1$ additions for the first window and $2$ per later window, $k - 1 + 2(n - k)$ in all, and $n - k$ comparisons.

## Reductions

- **To prefix sums.** Each window sum is one difference of prefix sums.
- **Averages to sums.** For a fixed length, the order of the averages is the order of the sums.
- **Length at least $k$ to a minimum prefix.** As in the variants, a running minimum of $P_i$ over $i \le j - k$.
- **Two dimensions to one.** For a fixed block height $a$, sum each column over $a$ rows with a rolling sum, then run the one-dimensional problem with length $b$ on each band of rows.

## Applications

- **Signal smoothing.** The window sums divided by $k$ are the moving average of a signal or of a time series of prices.
- **Busiest periods.** The busiest hour of a server log or the best week of sales, as windows over counts per minute or per day.
- **Genomics.** Windows of fixed length with the most of some feature, such as GC content in windows of a DNA sequence.
- **Image processing.** Box filters, which average over fixed blocks, compute all block sums at once.

## References
