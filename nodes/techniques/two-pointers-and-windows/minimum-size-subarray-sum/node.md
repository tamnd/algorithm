---
tag: F9DAMH
kind: problem
slug: minimum-size-subarray-sum
name: Minimum size subarray sum
aliases:
- minimum-length subarray with sum at least s
- shortest subarray with sum at least s
area: techniques/two-pointers-and-windows
level: intro
summary: Find the shortest contiguous subarray of positive numbers whose sum is at least a threshold.
prereqs: [sliding-window, prefix-sums, subarray]
see_also: [sliding-window, monotone-window-property, shortest-subarray-sum-at-least-k, sliding-window-positive-sum, prefix-sums, binary-search, monotonic-deque, subarray-sum-equals-k]
sources:
  - url: https://leetcode.com/problems/minimum-size-subarray-sum/
    title: LeetCode, problem 209, Minimum Size Subarray Sum
    locator: problem statement and follow-up (O(n log n) by binary search)
  - url: https://leetcode.com/problems/shortest-subarray-with-sum-at-least-k/
    title: LeetCode, problem 862, Shortest Subarray with Sum at Least K
    locator: problem statement (negative numbers allowed)
  - book: isbn:9780201657883
    title: Jon Bentley, Programming Pearls, second edition
    locator: Column 8, Algorithm design techniques (cumulative arrays and scanning algorithms for subarray sums)
---

The minimum size subarray sum problem gives an array of positive numbers and a threshold $s$, and asks for the length of the shortest contiguous subarray whose sum is at least $s$. A [sliding window](/sliding-window/) solves it in $\Theta(n)$ time and $O(1)$ extra space, because with positive numbers a window that reaches the sum stays good when it grows and a window that misses it stays bad when it shrinks. With negative numbers this fails, and the problem needs [prefix sums](/prefix-sums/) and a [monotonic deque](/monotonic-deque/), as in [shortest subarray with sum at least $k$](/shortest-subarray-sum-at-least-k/).

## In plain words

You have a row of positive numbers and a target. You want the shortest run of neighbors whose total reaches the target.

Use a window with a left and a right edge. Move the right edge one step at a time and add the new number. As soon as the total reaches the target, the window is a candidate: write down its length. Then try to make it shorter: drop numbers from the left while the total still reaches the target, writing down each length. When the total falls below the target, move the right edge again.

The window never needs to go back. Because all numbers are positive, a start that was dropped can only give longer answers later.

## Definition

**Input.** An array $A[0 \ldots n-1]$ of positive numbers and a number $s > 0$.

**Output.** The smallest length $j - i + 1$ over all pairs $i \le j$ with $A[i] + \cdots + A[j] \ge s$, or 0 if no such pair exists (the sum of the whole array is less than $s$).

The search version also returns a pair $(i, j)$ that attains the minimum.

## Variants

- **Non-negative numbers.** Zeros do not break the method; the proof below needs only $A[k] \ge 0$.
- **Negative numbers allowed.** The window method fails. Use the prefix sums $P[j] = A[0] + \cdots + A[j-1]$ and a deque of indices with increasing $P$: [shortest subarray with sum at least $k$](/shortest-subarray-sum-at-least-k/), $\Theta(n)$ time and $O(n)$ space.
- **Longest subarray with sum at most $s$.** The mirror problem for non-negative numbers: here a good window stays good when it shrinks, and the window finds the longest one. See the [positive-sum window](/sliding-window-positive-sum/).
- **Sum exactly $s$.** For positive numbers a window that shrinks while its sum is greater than $s$ finds every subarray with sum exactly $s$; with negatives use prefix sums and a hash table, as in [subarray sum equals $k$](/subarray-sum-equals-k/).
- **Many thresholds.** For many queries $s$ on one array, precompute for each length $L$ the maximum sum of a subarray of length $L$; it is non-decreasing in $L$ for non-negative numbers. The table takes $O(n^2)$ time to build, and then each query is a [binary search](/binary-search/) in $O(\log n)$ time.

## Examples

**Standard instance.** $A = [2, 3, 1, 2, 4, 3]$ and $s = 7$. The answer is 2, from $[4, 3]$. In the window method, $l$ is the left end and $t$ the window sum:

| $r$ | $A[r]$ | windows recorded | $l$ after | $t$ after | best |
| --- | --- | --- | --- | --- | --- |
| 0 | 2 | none | 0 | 2 | none |
| 1 | 3 | none | 0 | 5 | none |
| 2 | 1 | none | 0 | 6 | none |
| 3 | 2 | $[0, 3]$, sum 8 | 1 | 6 | 4 |
| 4 | 4 | $[1, 4]$, sum 10; $[2, 4]$, sum 7 | 3 | 6 | 3 |
| 5 | 3 | $[3, 5]$, sum 9; $[4, 5]$, sum 7 | 5 | 3 | 2 |

**One item is enough.** $A = [1, 4, 4]$ and $s = 4$ give 1.

**No answer.** $A = [1, 1, 1, 1, 1, 1, 1, 1]$ and $s = 11$ give 0, since the total is 8.

**Negative numbers break the window.** $A = [1, -3, 4]$ and $s = 4$. The answer is 1, from $[4]$. The window sum is $1$, then $-2$, then $2$, which never reaches 4, so the window method never shrinks and returns 0.

## Known algorithms

| algorithm | time | extra space | numbers |
| --- | --- | --- | --- |
| all pairs with running sums | $\Theta(n^2)$ | $O(1)$ | any |
| prefix sums and binary search | $\Theta(n \log n)$ | $\Theta(n)$ | non-negative |
| sliding window | $\Theta(n)$ | $O(1)$ | non-negative |
| prefix sums and a monotonic deque | $\Theta(n)$ | $\Theta(n)$ | any |

**Sliding window.** Set $l = 0$, $t = 0$ and $best = \infty$. For $r = 0, \ldots, n - 1$: add $A[r]$ to $t$; then, while $t \ge s$, set $best \leftarrow \min(best, r - l + 1)$, subtract $A[l]$ from $t$ and increase $l$. Return $best$, or 0 if it is still $\infty$.

For a start $i$, let $e(i)$ be the smallest $j \ge i$ with $A[i] + \cdots + A[j] \ge s$, or $\infty$ if there is none. The answer is $\min_i (e(i) - i + 1)$. With non-negative numbers, $e$ is non-decreasing: if $i < i'$ and $e(i') < \infty$, then $A[i] + \cdots + A[e(i')] \ge A[i'] + \cdots + A[e(i')] \ge s$, so $e(i) \le e(i')$. This is the [monotone window property](/monotone-window-property/). The loop keeps, at the start of each iteration $r$:

> **(M)** $t = A[l] + \cdots + A[r-1]$ and $t < s$; for every $i < l$, $e(i) \le r - 1$ and $best \le e(i) - i + 1$; and $best$ is the length of some valid window, or $\infty$.

*Why no shortest window is skipped.* The inner loop advances $l$ only when $t = A[l] + \cdots + A[r] \ge s$. At that moment $A[l] + \cdots + A[r-1] < s$: this sum is at most the sum of the window at the start of the iteration, which is less than $s$ by (M), because the numbers are non-negative and the current $l$ is at least the old one. So $e(l) = r$ exactly, and the recorded length $r - l + 1$ is the shortest valid window that starts at $l$. Each start $i$ is dropped only after its own shortest window is recorded. When the loop ends, the starts $i \ge l$ that were never dropped have $A[i] + \cdots + A[n-1] \le t < s$, so $e(i) = \infty$. So $best = \min_i (e(i) - i + 1)$.

*Cost.* $r$ moves $n$ times and $l$ moves at most $n$ times, so there are at most $2n$ additions and subtractions and $\Theta(n)$ time.

**Prefix sums and binary search.** With $P[0] = 0$ and $P[j] = A[0] + \cdots + A[j-1]$, the array $P$ is non-decreasing. For each $i$, binary search the least $j$ with $P[j] \ge P[i] + s$. The answer is the minimum of $j - i$.

**Monotonic deque, any signs.** For each end $j$, the best start is the largest $i < j$ with $P[i] \le P[j] - s$. Keep a deque of indices with increasing $P$; an index $i$ with $P[i] \ge P[j]$ can be removed from the back, since $j$ is a later and no worse start. See [shortest subarray with sum at least $k$](/shortest-subarray-sum-at-least-k/).

## Bounds

**Lower bound.** For $n \ge 2$ each algorithm must read all $n$ numbers on some input. Take $A = [1, 1, \ldots, 1]$ and $s = 2$, with answer 2. If $A[k]$ is not read, set $A[k] = 2$; then the answer is 1, and the algorithm cannot tell the two inputs apart. So the sliding window is optimal up to a constant factor.

**Upper bound.** $\Theta(n)$ time and $O(1)$ extra space for non-negative numbers; $\Theta(n)$ time and $\Theta(n)$ space for any signs.

## Reductions

- **To prefix sums.** The sum of $A[i \ldots j-1]$ is $P[j] - P[i]$, so the problem asks for the closest pair $i < j$ with $P[j] - P[i] \ge s$. For non-negative numbers $P$ is sorted, and the pair search becomes a two-pointer scan of $P$.
- **From fixed-length windows.** For each $L$, the best sum of a window of length $L$ can be found in $O(n)$ by a fixed window. Binary search over $L$ then solves the problem in $O(n \log n)$ for non-negative numbers, since a longer window has a best sum at least as large.

## Applications

- **Signal and log analysis.** The shortest time span in which a resource use, a count of events or a sum of transfers reaches a limit.
- **Teaching sliding windows.** It is the simplest window problem in which the left end moves by a rule, and the negative-number case shows where the rule needs the order of the data.

## References
