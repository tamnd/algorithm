---
tag: HHFZR5
kind: algorithm
slug: monotonic-deque-prefix-sums
name: Monotonic deque over prefix sums
aliases:
- deque prefix sum algorithm
area: sequences/subarray-problems
level: advanced
summary: Keep an increasing deque of prefix sums to find, for each right end, the nearest valid left end in amortized O(1).
solves: [shortest-subarray-sum-at-least-k]
model: word-ram
complexity:
  vars: {n: the number of items in the array}
  time: {worst: Θ(n), average: Θ(n), best: Θ(n)}
  space: {extra: Θ(n)}
properties: {stable: false, in_place: false, adaptive: false, online: true, deterministic: true, comparison: true, recursive: false}
prereqs: [shortest-subarray-sum-at-least-k, prefix-sums, monotonic-deque]
see_also: [sliding-window-positive-sum, sliding-window-maximum, min-queue, maximum-density-segment, maximum-circular-subarray-sum, monotonic-stack, amortized-cost, maximum-sum-subarray-of-fixed-length]
sources:
  - url: https://leetcode.com/problems/shortest-subarray-with-sum-at-least-k/
    title: LeetCode, problem 862, Shortest Subarray with Sum at Least K
    locator: problem statement and examples
  - url: https://cp-algorithms.com/others/maximum_average_segment.html
    title: cp-algorithms, Search the subarray with the maximum/minimum sum
    locator: the section on length-constrained variants (the minimum of the prefix sums over the allowed starts)
  - paper: doi:10.1016/s0022-0000(02)00010-7
    title: "Yaw-Ling Lin, Tao Jiang and Kun-Mao Chao, Efficient algorithms for locating the length-constrained heaviest segments with applications to biomolecular sequence analysis, Journal of Computer and System Sciences 65(3) (2002), 570-586"
    locator: the linear-time algorithm for the heaviest segment with length between L and U
  - url: https://cses.fi/book/book.pdf
    title: Antti Laaksonen, Competitive Programmer's Handbook
    locator: Chapter 8, Amortized analysis, Section 8.3 Sliding window minimum
---

The monotonic deque over prefix sums solves the [shortest subarray with sum at least K](/shortest-subarray-sum-at-least-k/) in $\Theta(n)$ time when the items may be negative. It computes the [prefix sums](/prefix-sums/) $P[0..n]$ and scans the ends $j = 0, \dots, n$. A [deque](/monotonic-deque/) holds candidate starts $i < j$ whose prefix sums increase from front to back. At each end, starts at the front that already give a sum of at least $K$ are recorded and removed, because a later end only makes their subarray longer. Then starts at the back with a prefix sum not less than $P[j]$ are removed, because $j$ is a later start with a smaller or equal prefix sum. Each index enters and leaves the deque at most once.

## In plain words

Write down the running totals of the list. The total of a stretch is the running total at its end minus the running total before its start. So you want an end and a start close together, with a big gap between their running totals.

Walk along the running totals and keep a line of possible starts, with their totals going up from front to back.

At each new total, look at the front of the line. If the gap from the front total is big enough, you have a stretch. Note its length and remove that start, since later ends only give longer stretches from it.

Then look at the back of the line. A start with a total at least as high as the new one is never useful again, because the new one is later and lower. Remove it, then add the new total at the back.

## The problem

**Input.** An array $A[0..n-1]$ of numbers and a number $K$.

**Output.** The smallest length $j - i$ over $0 \le i < j \le n$ with $A[i] + \dots + A[j-1] \ge K$, and one such pair $(i, j)$, or $\infty$ if there is none.

## The algorithm

```pseudo id=main
SHORTEST-AT-LEAST(A[0 .. n-1], K)
L1  P[0] ← 0; for t ← 1 to n do P[t] ← P[t − 1] + A[t − 1]
L2  Q ← empty deque; best ← ∞; R ← none
L3  for j ← 0 to n do
L4      while Q is not empty and P[j] − P[front(Q)] ≥ K do
L5          i ← POP-FRONT(Q); if j − i < best then best ← j − i; R ← (i, j)
L6      while Q is not empty and P[back(Q)] ≥ P[j] do POP-BACK(Q)
L7      PUSH-BACK(Q, j)
L8  return (best, R)
```

Line L1 computes the prefix sums. Lines L4 and L5 take starts from the front while they give a sum of at least $K$ with the end $j$. Line L6 removes the starts that $j$ makes useless. Line L7 adds $j$ as a new start for later ends. After line L7, the prefix sums of the indices in $Q$ strictly increase from front to back.

## Example

$A = [84, -37, 32, 40, 95]$ and $K = 167$, so $P = [0, 84, 47, 79, 119, 214]$. The table shows each end $j$, the starts that leave at the front (L5) and at the back (L6), and the deque after line L7, as indices with their prefix sums.

| $j$ | $P[j]$ | front pops (L5) | back pops (L6) | $Q$ after L7 | $best$ |
|---|---|---|---|---|---|
| 0 | 0 | | | $0{:}0$ | $\infty$ |
| 1 | 84 | | | $0{:}0,\ 1{:}84$ | $\infty$ |
| 2 | 47 | | $1$ ($84 \ge 47$) | $0{:}0,\ 2{:}47$ | $\infty$ |
| 3 | 79 | | | $0{:}0,\ 2{:}47,\ 3{:}79$ | $\infty$ |
| 4 | 119 | | | $0{:}0,\ 2{:}47,\ 3{:}79,\ 4{:}119$ | $\infty$ |
| 5 | 214 | $0$ ($214 - 0$), $2$ ($214 - 47$) | | $3{:}79,\ 4{:}119,\ 5{:}214$ | $3$ |

At $j = 5$ the start $0$ gives the sum $214 \ge 167$ and length $5$, and the start $2$ gives $167$ and length $3$. The start $3$ gives $135 < 167$, so the front loop stops. The answer is $3$, the subarray $A[2..5) = [32, 40, 95]$. A plain sliding window stops at length $5$ on this input, because removing $84$ makes its sum fall below $K$.

## Correctness

Two facts drive the method. First, if $t > i$ and $P[t] \le P[i]$, then for every end $j > t$ the start $t$ gives a larger or equal sum and a shorter subarray than $i$, so $i$ is useless after $t$ arrives. This is why line L6 is safe, and why the deque has increasing prefix sums. Second, if the start $i$ gives a sum of at least $K$ with the end $j$, every later end gives a longer subarray from $i$, so $(i, j)$ is the best pair that starts at $i$. This is why line L5 is safe.

Take a shortest valid pair $(i^*, j^*)$. The start $i^*$ cannot leave at the front before step $j^*$, since that would give a shorter valid pair. It cannot leave at the back before step $j^*$, since the index that removed it would be a later start with a valid and shorter pair. So it is in $Q$ at step $j^*$. Every index before it in $Q$ has a smaller prefix sum, so the front loop pops them all and then pops $i^*$ with the pair $(i^*, j^*)$. The [proof page](proofs/correctness.md) gives the details.

## Complexity

- **Time.** Each of the $n + 1$ indices is pushed once in line L7 and popped at most once, at the front or at the back. Each loop test either pops an index or ends the loop, so the tests number at most $2(n + 1)$ beyond the pops. With line L1, the total is $\Theta(n)$ on every input. One end can pop many indices; the bound is [amortized](/amortized-cost/).
- **Space.** The array $P$ and the deque, $\Theta(n)$ extra space. The deque can hold all $n + 1$ indices, for example when the items are positive and $K$ is larger than their total.

## Properties

- **Online.** The prefix sum $P[j]$ depends only on $A[0..j-1]$, so the scan can compute it on the fly and report the best pair for the prefix read so far. The deque must store the prefix sums of its indices.
- **Deterministic and exact.** It uses only additions, subtractions and comparisons. With integers, all values are exact.
- **Earliest end.** The pair returned is a shortest one with the smallest end, because $best$ changes only on a strict improvement.
- **Positive items.** If all items are positive, $P$ increases, line L6 never pops, and the method is the same as the [sliding window with positive sums](/sliding-window-positive-sum/), with the deque as the window.

## Variants and improvements

- **Largest sum with a length between $L$ and $U$.** For each end $j$, the best start is the one with the smallest $P[i]$ over $j - U \le i \le j - L$. Add $j - L$ to the back of a deque of increasing prefix sums, drop starts below $j - U$ at the front, and read the minimum at the front. This is a [sliding window minimum](/sliding-window-maximum/) on $P$, in $\Theta(n)$ time (Lin, Jiang and Chao, 2002).
- **Circular arrays.** On the doubled array with $U = n$, the same deque gives the [maximum circular subarray sum](/maximum-circular-subarray-sum/).
- **Largest average with a minimum length.** A binary search on the average $\lambda$ tests whether some subarray of length at least $L$ has a sum of at least $0$ after subtracting $\lambda$ from each item. See the [maximum density segment](/maximum-density-segment/).
- **Binary search on a stack.** Keeping only the back pops gives a stack of increasing prefix sums. A [binary search](/binary-search/) in the stack finds the largest valid start for each end in $O(\log n)$ time, for $\Theta(n \log n)$ in total. This is simpler to adapt to other queries.
- **Dynamic programming.** The same deque speeds up the recurrences of the form $f(j) = \max_{j - U \le i < j} (f(i) + c(j))$, a standard [monotonic deque](/monotonic-deque/) optimization.

## When to use it

Use it when a subarray problem asks for a best start for each end under a condition on the prefix sums, and the items can be negative, so that a plain two pointers window does not work. If all items are positive, the sliding window is simpler and uses $O(1)$ space. If the condition is not monotone in this way, as for an exact sum, use [prefix sum hash counting](/prefix-sum-hash-counting/) instead.

## Pitfalls

- **Using a sliding window with negative items.** It returns wrong answers, as on the example, where it gives $5$ in place of $3$.
- **Forgetting the start $0$.** The deque must start with the index $0$ and $P[0] = 0$, or subarrays that start at the first item are missed. In the pseudocode this is the step $j = 0$.
- **The order of the two loops.** The front pops must come before the back pops and the push. Pushing $j$ first would let the front loop pair $j$ with itself, an empty subarray, when $K \le 0$.
- **Strict and non-strict tests.** Line L6 removes starts with $P[\text{back}] \ge P[j]$; using $>$ keeps equal prefix sums, which is still correct but wastes space. Line L5 must use $\ge K$ to match the problem.
- **Overflow.** Prefix sums of large integers can overflow a fixed-width word even when every subarray sum of interest fits.

## Implementations

## History

The deque that keeps a sliding minimum or maximum is programming folklore. Lin, Jiang and Chao (2002) gave linear-time algorithms for the heaviest segment with a length bound, motivated by biomolecular sequence analysis. The shortest subarray with sum at least $K$, with negative items, became a standard problem through LeetCode 862.

## References
