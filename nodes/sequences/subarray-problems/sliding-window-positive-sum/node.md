---
tag: 7FDZS3
kind: algorithm
slug: sliding-window-positive-sum
name: Sliding window for positive sums
aliases:
- two-pointer sum window
area: sequences/subarray-problems
level: intro
summary: Grow the right end until the sum reaches s, then shrink the left end; runs in linear time because values are positive.
solves: [minimum-size-subarray-sum]
model: word-ram
complexity:
  vars: {n: the number of items in the array}
  time: {worst: Θ(n), average: Θ(n), best: Θ(n)}
  space: {extra: Θ(1)}
properties: {stable: false, in_place: true, adaptive: false, online: true, deterministic: true, comparison: false, recursive: false}
history:
  year: 2017
  people: [Antti Laaksonen]
  note: The window with two pointers over positive numbers is programming folklore with no known first paper; Laaksonen's handbook uses it as the first example of the two pointers method.
prereqs: [minimum-size-subarray-sum, sliding-window, two-pointers, loop-invariant]
see_also: [monotone-window-property, prefix-sums, binary-search, shortest-subarray-sum-at-least-k, monotonic-deque-prefix-sums, distinct-count-two-pointers, maximum-sum-subarray-of-fixed-length, subarray-sum-equals-k]
sources:
  - url: https://leetcode.com/problems/minimum-size-subarray-sum/
    title: LeetCode, problem 209, Minimum Size Subarray Sum
    locator: problem statement (positive numbers, a threshold, the shortest length or 0)
  - url: https://cses.fi/book/book.pdf
    title: Antti Laaksonen, Competitive Programmer's Handbook
    locator: Chapter 8, Amortized analysis, Section 8.1 Two pointers method (subarray sum over positive numbers)
  - url: https://leetcode.com/problems/subarray-product-less-than-k/
    title: LeetCode, problem 713, Subarray Product Less Than K
    locator: problem statement (counting windows with the same two pointers)
---

The sliding window for positive sums solves the [minimum size subarray sum](/minimum-size-subarray-sum/) problem in one pass, in $\Theta(n)$ time and $O(1)$ extra space. It keeps a window $A[l..r]$ and its sum $t$. The right end $r$ moves one step at a time and adds an item. While $t \ge s$, the window is recorded and the left end $l$ moves right. Both ends only move right, so there are at most $2n$ moves. The scan is correct only because no item is negative: then a window that reaches $s$ stays good when it grows, and a window that misses $s$ stays bad when it shrinks. This is the [monotone window property](/monotone-window-property/) that the general [sliding window](/sliding-window/) technique needs.

## In plain words

You have a row of positive numbers and a target. You want the shortest run of neighbors whose total is at least the target.

Keep a window with a left and a right edge, and keep its total. Move the right edge one step and add the new number. While the total is at least the target, write down the length if it is the shortest so far, then drop the leftmost number and move the left edge.

A left edge that you move past never comes back. That is safe: any longer window from that old left edge is longer than the one you wrote down, so it cannot be shorter. Each number goes in once and comes out at most once, so the work is linear.

## The problem

**Input.** An array $A[0..n-1]$ with $A[i] \ge 0$ for all $i$, and a number $s > 0$. The problem page asks for positive items; zero items do no harm here.

**Output.** The smallest length $r - l + 1$ over all pairs $l \le r$ with $A[l] + \dots + A[r] \ge s$, or $0$ if there is no such pair.

## The algorithm

```pseudo id=main
MIN-WINDOW(A[0 .. n-1], s)
L1  l ← 0; t ← 0; best ← ∞
L2  for r ← 0 to n − 1 do
L3      t ← t + A[r]
L4      while t ≥ s do
L5          best ← min(best, r − l + 1)
L6          t ← t − A[l]; l ← l + 1
L7  if best = ∞ then return 0
L8  return best
```

Line L3 grows the window at the right. The loop of lines L4 to L6 shrinks it at the left while it is still good, and line L5 records each good window that it sees. The value $t$ is always the sum of $A[l..r]$, so no sum is computed again.

## Example

$A = [2, 3, 1, 2, 4, 3]$ and $s = 7$. The table shows each step $r$, the windows that line L5 records, and the state after the inner loop.

| $r$ | $A[r]$ | windows recorded (start, length) | $l$ after | $t$ after | $best$ |
|---|---|---|---|---|---|
| 0 | 2 | none | 0 | 2 | $\infty$ |
| 1 | 3 | none | 0 | 5 | $\infty$ |
| 2 | 1 | none | 0 | 6 | $\infty$ |
| 3 | 2 | $(0, 4)$ | 1 | 6 | 4 |
| 4 | 4 | $(1, 4)$, $(2, 3)$ | 3 | 6 | 3 |
| 5 | 3 | $(3, 3)$, $(4, 2)$ | 5 | 3 | 2 |

The answer is $2$, from $A[4..5] = [4, 3]$. At step 4 the inner loop runs twice: $[3, 1, 2, 4]$ has sum $10$ and $[1, 2, 4]$ has sum $7$, and then $[2, 4]$ has sum $6 < 7$, so it stops. There are $6$ steps of the outer loop and $5$ steps of the inner loop in total.

## Correctness

For a start $i$, let $e(i)$ be the smallest $j \ge i$ with $A[i] + \dots + A[j] \ge s$, or $\infty$ if there is none. The answer is the smallest $e(i) - i + 1$, or $0$ if every $e(i)$ is $\infty$. With items that are not negative, $e$ does not decrease: if $i < i'$ and $e(i')$ is finite, the window $A[i..e(i')]$ contains $A[i'..e(i')]$, so its sum is at least $s$ and $e(i) \le e(i')$.

At the start of each step $r$ the loop keeps this invariant:

> **(W)** $t = A[l] + \dots + A[r-1]$ and $t < s$. Every start $i < l$ has $e(i) \le r - 1$ and $best \le e(i) - i + 1$. If $best$ is finite, it is the length of a window with sum at least $s$.

*Why the left end can move.* The inner loop moves $l$ only when $t = A[l] + \dots + A[r] \ge s$. At that moment the shorter window $A[l..r-1]$ has a sum less than $s$: it is part of the window from the start of step $r$, whose sum is less than $s$ by (W), and the items are not negative. So $e(l) = r$, and line L5 records exactly the shortest good window that starts at $l$. The start $l$ is dropped only after that.

*End.* After the last step, each start $i < l$ has its shortest window counted in $best$. Each start $i \ge l$ has $A[i] + \dots + A[n-1] \le t < s$, so $e(i) = \infty$. So $best$ is the smallest $e(i) - i + 1$, and lines L7 and L8 return the answer. The [proof page](proofs/correctness.md) writes out the induction and the termination of the inner loop.

## Complexity

- **Time.** Line L3 runs $n$ times. Each run of line L6 increases $l$, and $l \le r + 1 \le n$ at all times, so line L6 runs at most $n$ times in total. The total is at most $2n$ additions and subtractions and at most $2n$ comparisons in line L4, so $\Theta(n)$ on every input. This is an [aggregate](/aggregate-method/) count: one step of $r$ can cost $\Theta(n)$, but the [amortized cost](/amortized-cost/) per step is $O(1)$.
- **Space.** Four scalars, $\Theta(1)$ extra space. The array is only read.
- **Lower bound.** An item that is not read can be the one that reaches $s$, so every algorithm must read all $n$ items in the worst case.

## Properties

- **Online, with a buffer.** After step $r$, $best$ is the answer for the prefix $A[0..r]$. On a stream the algorithm must keep the items of the current window, because line L6 reads $A[l]$ again.
- **Exact on integers.** Every value of $t$ is a window sum, so with integer items there is no rounding. With floating-point items, the running sum $t$ collects rounding error over many additions and subtractions; recomputing it from time to time, or [Kahan summation](/kahan-summation/), keeps it close.
- **Which window.** Line L5 sees the good windows in order of their end. To return a shortest window, store $(l, r)$ in line L5 when $r - l + 1 < best$. This gives the shortest window with the earliest end.

## Variants and improvements

- **Count windows below a bound.** For the number of windows with sum less than $s$, shrink while $t \ge s$ and then add $r - l + 1$, the number of good windows that end at $r$. With products instead of sums and items at least $1$, this is LeetCode problem 713.
- **Longest window with sum at most $s$.** Shrink while $t > s$, then record $r - l + 1$. A window that is good stays good when it shrinks, so the same two pointers work.
- **Exact sum $s$.** With positive items, shrink while $t > s$ and report a window when $t = s$. With items of any sign, use [prefix sums and a hash table](/prefix-sum-hash-counting/), as in [subarray sum equals k](/subarray-sum-equals-k/).
- **Prefix sums and binary search.** The prefix sums $P$ do not decrease, so for each start a [binary search](/binary-search/) finds the least end. This costs $\Theta(n \log n)$ time and $\Theta(n)$ space, and it answers many thresholds $s$ on one array.
- **Negative items.** The window fails, see the pitfalls. The [monotonic deque over prefix sums](/monotonic-deque-prefix-sums/) solves [shortest subarray with sum at least $k$](/shortest-subarray-sum-at-least-k/) in $\Theta(n)$ time for items of any sign.
- **Other window measures.** The same scan with a table of counts instead of a sum gives the [two pointers for distinct counts](/distinct-count-two-pointers/).

## When to use it

Use it when the items are not negative and the question is about the shortest or longest run whose sum passes a bound, or the number of such runs. It needs one pass and no extra memory. For a fixed window length, the plain running sum of the [fixed-length window](/maximum-sum-subarray-of-fixed-length/) is simpler. When negative items can occur, use prefix sums with a monotonic deque instead.

## Pitfalls

- **Negative items.** For $A = [5, -10, 4, 4]$ and $s = 8$, the window $[5, -10, 4]$ has sum $-1$ and the scan never shrinks it. At $r = 3$ the window $[5, -10, 4, 4]$ has sum $3 < 8$, so the scan returns $0$, but $A[2..3] = [4, 4]$ has sum $8$. Check the sign of the items before you use the window.
- **A threshold that is not positive.** With $s \le 0$ the empty window also has $t \ge s$, so line L6 moves $l$ past $r$ and reads outside the window. Handle $s \le 0$ first: the answer is $1$ for a non-empty array if the problem asks for non-empty windows.
- **Using `if` instead of `while`.** Shrinking by only one item per step misses shorter windows. In the example, step 4 must record two windows.
- **Recording after the shrink.** Line L5 must run before line L6. If the length is recorded after an item is removed, the recorded window can have a sum less than $s$.
- **Returning $\infty$.** The sentinel must become $0$, or the agreed value for no answer, before it leaves the function.

## Implementations

## History

The window with two pointers over items that are not negative has no known first paper. It is part of the folklore of programming contests and interviews. Laaksonen's Competitive Programmer's Handbook uses it as the first example of the two pointers method, in the form that finds a window with an exact sum, and LeetCode problem 209 gives the shortest-window form with its $\Theta(n \log n)$ binary search follow-up.

## References
