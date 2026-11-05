---
tag: 00F99T
kind: algorithm
slug: circular-kadane-algorithm
name: Circular Kadane algorithm
aliases:
- circular maximum subarray algorithm
area: sequences/subarray-problems
level: core
summary: Answer is the larger of plain Kadane and the total sum minus the minimum subarray sum.
solves: [maximum-circular-subarray-sum]
model: word-ram
complexity:
  vars: {n: the number of items in the array}
  time: {worst: Θ(n), average: Θ(n), best: Θ(n)}
  space: {extra: Θ(1)}
properties: {stable: false, in_place: true, adaptive: false, online: true, deterministic: true, comparison: false, recursive: false}
history:
  year: 1977
  people: [Joseph B. Kadane]
  note: The circular form is folklore built on Kadane's scan of 1977, with no known first paper; it is the standard solution of LeetCode problem 918.
prereqs: [maximum-circular-subarray-sum, kadane-algorithm]
see_also: [maximum-subarray-problem, maximum-subarray-divide-and-conquer, monotonic-deque-prefix-sums, prefix-sums, kadane-max-product, segment-tree-maximum-subsegment-sum, online-algorithm, subarray]
sources:
  - url: https://leetcode.com/problems/maximum-sum-circular-subarray/
    title: LeetCode, problem 918, Maximum Sum Circular Subarray
    locator: problem statement and examples (including the case where every item is negative)
  - url: https://cp-algorithms.com/others/maximum_average_segment.html
    title: cp-algorithms, Search the subarray with the maximum/minimum sum
    locator: Algorithm 2 (the scan that drops a negative running sum) and the remark on the minimum subarray
  - paper: doi:10.1145/358234.381162
    title: "Jon Bentley, Programming pearls: algorithm design techniques, Communications of the ACM 27(9) (1984), 865-873"
    locator: the linear scan for the plain problem
---

The circular Kadane algorithm solves the [maximum circular subarray sum](/maximum-circular-subarray-sum/) problem in one pass, in $\Theta(n)$ time and $O(1)$ extra space. It runs [Kadane's algorithm](/kadane-algorithm/) twice at once: once for the largest plain subarray sum, and once, with max and min swapped, for the smallest. It also adds up the total $T$. A subarray that wraps around the end of the ring is the ring with one plain block taken out, so the best wrapping sum is $T$ minus the smallest plain sum. The answer is the larger of the two candidates, with one special case: if every item is negative, the second candidate is the empty subarray, and the answer is the plain maximum.

## In plain words

Walk once along the list and keep three things. The first is the best total of a stretch that does not wrap, found as in the plain problem. The second is the worst total of a stretch that does not wrap, found the same way with the roles of large and small swapped. The third is the total of the whole list.

A stretch that does wrap uses every number except one stretch in the middle. Its total is the whole total minus what it leaves out, so it is best when the left-out stretch is worst. At the end, compare the best plain total with the whole total minus the worst plain total, and keep the larger.

There is one trap. If all numbers are negative, the worst stretch is the whole list, and leaving it out leaves nothing. Then return the best plain total.

## The problem

**Input.** An array $A[0..n-1]$ of numbers with $n \ge 1$, read as a ring.

**Output.** The largest sum $C^*$ of a non-empty circular [subarray](/subarray/): either a plain subarray $A[i..j]$, or a wrapping one, $A[i..n-1]$ followed by $A[0..j]$ with $j < i$. No item is used twice.

## The algorithm

```pseudo id=main
CIRCULAR-KADANE(A[0 .. n-1])
L1  hi ← A[0]; best ← A[0]; lo ← A[0]; worst ← A[0]; T ← A[0]
L2  for j ← 1 to n − 1 do
L3      hi ← A[j] + max(hi, 0); best ← max(best, hi)
L4      lo ← A[j] + min(lo, 0); worst ← min(worst, lo)
L5      T ← T + A[j]
L6  if best < 0 then return best
L7  return max(best, T − worst)
```

Line L3 is Kadane's step: $hi$ is the largest sum of a subarray that ends at $j$, and $best$ the largest plain sum so far. Line L4 is the same step for the smallest sum, with $lo$ and $worst$. Line L5 keeps the total. Line L6 handles a ring of negative items, and line L7 compares the best plain sum with the best wrapping sum $T - worst$.

## Example

$A = [8, -4, 3, -5, 4]$. The table shows the values after line L5 of each step.

| $j$ | $A[j]$ | $hi$ | $best$ | $lo$ | $worst$ | $T$ |
|---|---|---|---|---|---|---|
| 0 | 8 | 8 | 8 | 8 | 8 | 8 |
| 1 | $-4$ | 4 | 8 | $-4$ | $-4$ | 4 |
| 2 | 3 | 7 | 8 | $-1$ | $-4$ | 7 |
| 3 | $-5$ | 2 | 8 | $-6$ | $-6$ | 2 |
| 4 | 4 | 6 | 8 | $-2$ | $-6$ | 6 |

At the end $best = 8$, from the plain subarray $[8]$, and $worst = -6$, from the block $A[1..3] = [-4, 3, -5]$. The best wrapping sum is $T - worst = 6 - (-6) = 12$, from $A[4]$ followed by $A[0]$, that is $[4, 8]$. Since $best \ge 0$, line L7 returns $\max(8, 12) = 12$.

## Correctness

Let $S^*_{\max}$ and $S^*_{\min}$ be the largest and the smallest sum of a non-empty plain subarray. By the correctness of [Kadane's algorithm](/kadane-algorithm/), line L3 ends with $best = S^*_{\max}$. Line L4 is Kadane's algorithm on $-A$ with the signs changed back, so it ends with $worst = S^*_{\min}$. Line L5 ends with $T$ equal to the total.

*Wrapping sums.* The wrapping subarray $A[i..n-1]\,A[0..j]$ with $j < i$ leaves out the plain block $A[j+1..i-1]$, so its sum is $T$ minus the sum of that block. As $(i, j)$ runs over all wrapping subarrays, the left-out block runs over all plain blocks, including the empty block when $j = i - 1$. So the best wrapping sum is $T - S^*_{\min}$, unless the best choice is the empty block, which leaves the whole ring, a plain subarray with sum $T \le S^*_{\max}$.

*The two cases.* If $best < 0$, every item is negative, since a non-negative item would be a subarray with sum at least $0$. Then the sum of any circular subarray is at most its largest item, because the other items are negative. So the answer is the largest item, which is $S^*_{\max}$, and line L6 returns it. If $best \ge 0$, then $\max(S^*_{\max}, T - S^*_{\min})$ is the best over all circular subarrays: if $S^*_{\min}$ is reached only by the whole ring, then $T - S^*_{\min} = 0 \le S^*_{\max}$ and it does no harm; otherwise $T - S^*_{\min}$ is the sum of a real wrapping subarray. The [proof page](proofs/correctness.md) writes this out.

## Complexity

- **Time.** The loop runs $n - 1$ times with $O(1)$ work, so $\Theta(n)$ on every input: at most $3(n - 1)$ additions and $4(n - 1)$ comparisons.
- **Space.** Five scalars, $\Theta(1)$ extra space. The array is only read.
- **Lower bound.** Every algorithm must read every item, see the [problem page](/maximum-circular-subarray-sum/).

## Properties

- **Online.** After step $j$, lines L6 and L7 applied to the current values give the answer for the ring $A[0..j]$. So the algorithm works on a stream with $O(1)$ memory, and the ring closes at the current item.
- **One pass.** The two scans and the total share one loop. They can also be three separate passes with the same cost.
- **Which arc.** To report the arc, track the start of $hi$ and of $lo$ as in Kadane's algorithm. If the wrapping case wins with the smallest block $A[a..b]$, the arc starts at $b + 1$ and has $n - (b - a + 1)$ items, taken modulo $n$.
- **Exact on integers.** All values are sums of items, so with integer items the only risk is overflow.

## Variants and improvements

- **Empty arc allowed.** Return $\max(0, best, T - worst)$ and drop line L6.
- **Prefix and suffix form.** Without the minimum, the best wrapping sum is the best suffix sum plus the best prefix sum that ends before the suffix, which one array of prefix maxima gives in $\Theta(n)$ time and $\Theta(n)$ space.
- **Length bound.** For an arc of at most $k$ items, the complement trick fails. Double the array and use the [prefix sums with a monotonic deque](/monotonic-deque-prefix-sums/).
- **Products.** The largest circular product does not reduce to a total divided by a smallest product, because zeros have no inverse. Run [Kadane for maximum product](/kadane-max-product/) on the doubled array with a length bound, or split the ring at its zeros.
- **Range queries.** For a changing ring, keep the four values of the [segment tree for maximum subsegment sum](/segment-tree-maximum-subsegment-sum/). Keep the same four values for minima as well. The root then gives the total, the best and the smallest subarray sum, and line L7 applies to them.

## When to use it

Use it whenever the data form a cycle and the best block may pass the end, for example values per hour of a day or per sector of a circle. It has the same cost as the plain scan. When the arc has a length bound, or the aggregate has no inverse, use doubling instead.

## Pitfalls

- **All negative items.** Without line L6, the ring $[-3, -2, -3]$ gives $\max(-2, -8 - (-8)) = 0$, the sum of the empty arc. The answer for a non-empty arc is $-2$.
- **Testing the wrong value.** Testing $T < 0$ instead of $best < 0$ is wrong: for $[5, -10]$, $T = -5$, but the answer is $5$.
- **Counting an item twice.** Running plain Kadane on the doubled array $A A$ without a length bound finds arcs longer than $n$. For $[5, -3, 5]$ it returns $14$, the sum of all six items of $[5, -3, 5, 5, -3, 5]$, and not $10$.
- **Overflow.** $T - worst$ can be up to about twice the largest absolute sum, so it can overflow where the other values do not.

## Implementations

## History

Kadane found the linear scan for the plain problem in 1977, and Bentley published it in 1984. The circular form, with the complement of the minimum subarray, has no known first paper. It is a standard exercise and the usual solution of LeetCode problem 918, where the all-negative special case is part of the tests.

## References
