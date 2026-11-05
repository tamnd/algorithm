---
tag: M8BX35
kind: problem
slug: shortest-subarray-sum-at-least-k
name: Shortest subarray with sum at least K
aliases:
- shortest subarray with sum at least K with negatives
area: sequences/subarray-problems
level: advanced
summary: Shortest subarray with sum at least K when elements may be negative, so the sliding window does not apply.
prereqs: [subarray, prefix-sums, minimum-size-subarray-sum]
see_also: [monotonic-deque-prefix-sums, sliding-window-positive-sum, monotonic-deque, maximum-density-segment, next-greater-element, binary-search, fenwick-tree, maximum-sum-subarray-of-fixed-length]
sources:
  - url: https://leetcode.com/problems/shortest-subarray-with-sum-at-least-k/
    title: LeetCode, problem 862, Shortest Subarray with Sum at Least K
    locator: problem statement and examples (items may be negative)
  - url: https://leetcode.com/problems/minimum-size-subarray-sum/
    title: LeetCode, problem 209, Minimum Size Subarray Sum
    locator: problem statement (the case of positive items)
  - url: https://cp-algorithms.com/others/maximum_average_segment.html
    title: cp-algorithms, Search the subarray with the maximum/minimum sum
    locator: the section on length-constrained variants (a subarray sum as a difference of prefix sums, with a minimum over the allowed starts)
  - paper: doi:10.1016/s0022-0000(02)00010-7
    title: "Yaw-Ling Lin, Tao Jiang and Kun-Mao Chao, Efficient algorithms for locating the length-constrained heaviest segments with applications to biomolecular sequence analysis, Journal of Computer and System Sciences 65(3) (2002), 570-586"
    locator: the related problem of the heaviest segment with a bound on its length
---

The problem gives an array of numbers of any sign and a target $K$, and asks for the shortest non-empty [subarray](/subarray/) whose sum is at least $K$. With [prefix sums](/prefix-sums/) $P$, the subarray $A[i..j)$ has sum $P[j] - P[i]$, so for each end $j$ the task is to find the largest $i < j$ with $P[i] \le P[j] - K$. When all items are positive, $P$ is increasing and a plain [sliding window](/sliding-window-positive-sum/) solves it, as in [minimum size subarray sum](/minimum-size-subarray-sum/). With negative items $P$ goes up and down, the window loses its monotone property, and the standard solution is the [monotonic deque over prefix sums](/monotonic-deque-prefix-sums/), in $\Theta(n)$ time.

## In plain words

You have a list of daily gains and losses, and you want the shortest run of days with a total gain of at least some target.

If every day is a gain, a simple method works: grow a window at the front, and drop days at the back while the total stays at the target. But with losses this fails. Dropping a loss at the back makes the total go up, so a window that is too small can grow into a good one by dropping days, not adding them.

The fix is to look at running totals. A run of days has total gain equal to the running total at its end minus the running total before its start. So for each end day, you want the latest start whose running total is low enough.

## Definition

**Input.** An array $A[0..n-1]$ of numbers and a number $K$.

**Output.** The smallest length $j - i$ over $0 \le i < j \le n$ such that $A[i] + \dots + A[j-1] \ge K$, and one such pair $(i, j)$. If there is no such subarray, report that, for example as $-1$ or $\infty$.

**Prefix form.** With $P[0] = 0$ and $P[t] = A[0] + \dots + A[t-1]$, the output is the smallest $j - i$ over $i < j$ with $P[j] - P[i] \ge K$. For a fixed $j$ the best $i$ is the largest $i < j$ with $P[i] \le P[j] - K$.

**Why the window fails.** For the property "sum at least $K$", a window that has it can lose it when it grows, and a window without it can gain it when it shrinks at the back. So the two pointers argument of the [monotone window property](/monotone-window-property/) does not hold.

## Variants

- **Positive items.** The [minimum size subarray sum](/minimum-size-subarray-sum/) problem, solved by a [sliding window](/sliding-window-positive-sum/) in $\Theta(n)$ time and $O(1)$ space.
- **Sum at most $K$.** Negate the items and $K$.
- **Longest subarray with sum at least $K$.** For each end $j$, the best start is the smallest $i$ with $P[i] \le P[j] - K$. Only the prefix minima are useful starts, and two pointers over the prefix minima from the left and the suffix maxima from the right solve it in $\Theta(n)$ time.
- **Length bounds with the largest sum.** The largest sum of a subarray of length between $L$ and $U$ uses a minimum over a sliding range of starts, with a [monotonic deque](/monotonic-deque/), in $\Theta(n)$ time (Lin, Jiang and Chao, 2002).
- **Largest average with a minimum length.** The [maximum density segment](/maximum-density-segment/) problem, which reduces to this kind of test by a binary search on the average.
- **Counting.** The number of subarrays with sum at least $K$ is a count of pairs $i < j$ with $P[i] \le P[j] - K$, an inversion-type count solved with a [Fenwick tree](/fenwick-tree/) after compression in $O(n \log n)$ time.

## Examples

**The window fails.** $A = [84, -37, 32, 40, 95]$ and $K = 167$. The prefix sums are $P = [0, 84, 47, 79, 119, 214]$. A sliding window first reaches a sum of at least $167$ with the whole array, sum $214$, length $5$. It then drops $84$, the sum becomes $130 < 167$, and it stops. But dropping $-37$ as well gives $[32, 40, 95]$ with sum $167$, so the answer is $3$, from $P[5] - P[2] = 214 - 47$.

**A single item.** $A = [2, -3, 4, -1, 3, -5, 6]$ and $K = 6$. The answer is $1$, the item $6$.

**Small example.** $A = [2, -1, 2]$ and $K = 3$. Only the whole array works, so the answer is $3$.

**No answer.** $A = [1, 2]$ and $K = 4$. The total is $3$, and there is no subarray with sum at least $4$.

## Known algorithms

| method | time | extra space | notes |
|---|---|---|---|
| all pairs with running sums | $\Theta(n^2)$ | $O(1)$ | for each start, extend to the right |
| increasing stack of prefix sums with [binary search](/binary-search/) | $\Theta(n \log n)$ | $O(n)$ | for each $j$, search the stack for the largest $i$ with $P[i] \le P[j] - K$ |
| [monotonic deque over prefix sums](/monotonic-deque-prefix-sums/) | $\Theta(n)$ | $O(n)$ | the standard solution |
| [sliding window](/sliding-window-positive-sum/) | $\Theta(n)$ | $O(1)$ | correct only for positive items |

The deque method keeps start indices with increasing prefix sums. A start $i$ with $P[i] \ge P[j]$ for a later $j$ is useless, because $j$ is a later start with a smaller prefix sum, so it leaves at the back. A start that already gives a valid subarray for the current end leaves at the front, because a later end can only make that subarray longer. Each index enters and leaves once.

## Bounds

**Linear time.** Each item must be read, so $\Omega(n)$ time is needed in the worst case, and the deque method meets it. The deque can hold $n + 1$ indices, for example when $A$ is all positive and $K$ is larger than the total.

**Values.** The method uses additions, subtractions and comparisons of prefix sums. With integers, the prefix sums need about $\log_2(n \max |A|)$ bits.

## Reductions

- **To prefix sums.** The problem is a query on pairs of prefix sums, $\min \{ j - i : i < j,\ P[i] \le P[j] - K \}$.
- **Shortest to nearest.** For each $j$, the best start is the nearest index to the left with a prefix sum at most $P[j] - K$. With $K = 0$ and strict inequality, this is close to the [next greater element](/next-greater-element/) problem on $P$ read from the right.
- **Positive case.** If all items are positive, $P$ is increasing, the deque never drops from the back, and the deque method becomes the sliding window.

## Applications

- **Contest and interview problems.** It is the standard example of a problem that looks like a sliding window but needs a monotonic deque.
- **Time series.** The shortest period with a total change of at least $K$ in a series of gains and losses, such as prices, scores or energy use.
- **Sequence analysis.** Short segments of a scored biological sequence with a total score above a threshold, as in the length-constrained segment problems.
- **Subroutine.** The test step in a binary search on the answer, such as in the maximum density segment problem.

## References
