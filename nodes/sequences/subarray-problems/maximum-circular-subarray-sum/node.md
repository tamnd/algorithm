---
tag: XEYJ19
kind: problem
slug: maximum-circular-subarray-sum
name: Maximum circular subarray sum
aliases:
- circular maximum subarray problem
area: sequences/subarray-problems
level: core
summary: Maximum subarray sum when the array is treated as circular, so a subarray may wrap around the end.
prereqs: [maximum-subarray-problem, subarray, prefix-sums]
see_also: [circular-kadane-algorithm, kadane-algorithm, maximum-subarray-divide-and-conquer, monotonic-deque-prefix-sums, maximum-sum-subarray-of-fixed-length, segment-tree-maximum-subsegment-sum, adversary-argument, maximum-product-subarray]
sources:
  - url: https://leetcode.com/problems/maximum-sum-circular-subarray/
    title: LeetCode, problem 918, Maximum Sum Circular Subarray
    locator: problem statement (a non-empty subarray of a circular array, each item used at most once)
  - url: https://cp-algorithms.com/others/maximum_average_segment.html
    title: cp-algorithms, Search the subarray with the maximum/minimum sum
    locator: Problem statement, Algorithm 1 (prefix sums with a running minimum) and the remark that the minimum subarray is found by changing the signs
  - paper: doi:10.1145/358234.381162
    title: "Jon Bentley, Programming pearls: algorithm design techniques, Communications of the ACM 27(9) (1984), 865-873"
    locator: the linear problem and its linear-time scan
---

The maximum circular subarray sum problem is the [maximum subarray problem](/maximum-subarray-problem/) on a ring. The array $A[0..n-1]$ is read as circular, so after $A[n-1]$ comes $A[0]$ again, and a [subarray](/subarray/) may wrap around the end. Each item may be used at most once. The key fact is that a wrapping subarray is the whole ring with one plain subarray taken out. So the best wrapping sum is the total minus the smallest plain subarray sum, and the problem reduces to two linear scans, the [circular Kadane algorithm](/circular-kadane-algorithm/), in $\Theta(n)$ time and $O(1)$ extra space.

## In plain words

Put the numbers around a circle, like the hours on a clock. You want one unbroken arc of the circle whose numbers have the largest total. The arc may pass the point where the list started, so the end of the list and its start can be in the same arc. No number can be counted twice, so the arc is at most the whole circle.

An arc that passes the starting point leaves out one stretch in the middle of the list. Making that arc as large as possible is the same as making the left-out stretch as small as possible. So the hard new case is the old problem turned upside down.

## Definition

**Input.** An array $A[0..n-1]$ of real numbers, with $n \ge 1$, read as a ring.

**Circular subarrays.** A *plain* subarray is $A[i..j]$ with $0 \le i \le j \le n - 1$. A *wrapping* subarray is $A[i..n-1]$ followed by $A[0..j]$, for $0 \le j < i \le n - 1$. Its sum is
$$W(i, j) = \sum_{k=i}^{n-1} A[k] + \sum_{k=0}^{j} A[k].$$
Each circular subarray has between $1$ and $n$ items, and no item appears twice.

**Output.** The largest sum $C^*$ of a non-empty circular subarray, and a subarray that reaches it.

**The complement form.** Let $T = A[0] + \dots + A[n-1]$. The items not in the wrapping subarray $(i, j)$ form the plain block $A[j+1..i-1]$, so $W(i, j) = T - S(j+1, i-1)$, where $S$ is the plain sum and an empty block has sum $0$. With $S^*_{\max}$ the largest and $S^*_{\min}$ the smallest sum of a non-empty plain subarray, this gives
$$C^* = \begin{cases} S^*_{\max} & \text{if } S^*_{\max} < 0, \\ \max(S^*_{\max},\ T - S^*_{\min}) & \text{otherwise.} \end{cases}$$
The first case covers rings where every item is negative. There the smallest block is the whole ring, and $T - S^*_{\min} = 0$ would be the sum of the empty subarray, which is not allowed. In the second case, if the smallest block is the whole ring, then $T - S^*_{\min} = 0 \le S^*_{\max}$, so the empty choice does no harm.

## Variants

- **Empty subarray allowed.** Then $C^* = \max(0, S^*_{\max}, T - S^*_{\min})$, with no special case.
- **Length at most $k$.** For an arc of at most $k$ items, double the array and take the best window of length at most $k$ with [prefix sums and a monotonic deque](/monotonic-deque-prefix-sums/). With $k = n$ this is a second linear algorithm for the plain circular problem.
- **Fixed length $k$.** The best arc of exactly $k$ items is a [fixed-length window](/maximum-sum-subarray-of-fixed-length/) on the array with its first $k - 1$ items appended.
- **Minimum circular subarray.** Change the signs of all items.
- **Other aggregates.** The largest circular product, or the best arc under a length bound and a sum bound, use the same doubling, but the complement trick needs an inverse operation, which products with zeros do not have.
- **Many queries.** For the best arc inside a range of a changing ring, keep the four values of the [segment tree for maximum subsegment sum](/segment-tree-maximum-subsegment-sum/) and join a suffix of the ring with a prefix.

## Examples

**A wrapping answer.** For $A = [5, -3, 5]$, the best plain subarray is the whole array with sum $7$. The total is $T = 7$ and the smallest plain subarray is $[-3]$, so the best wrapping sum is $7 - (-3) = 10$, from $A[2]$ followed by $A[0]$. So $C^* = 10$.

**A plain answer.** For $A = [1, -2, 3, -2]$, the best plain subarray is $[3]$ with sum $3$. The total is $0$ and the smallest plain subarray has sum $-2$, so the best wrapping sum is $2$. So $C^* = 3$.

**All negative.** For $A = [-3, -2, -3]$, the formula $T - S^*_{\min}$ gives $-8 - (-8) = 0$, the empty subarray. The correct answer is $C^* = -2$, the largest item.

**All non-negative.** If no item is negative, the whole ring is a best subarray, with sum $T$.

## Known algorithms

| method | time | extra space | idea |
|---|---|---|---|
| all start points, running sums | $\Theta(n^2)$ | $O(1)$ | for each start, grow the arc up to $n$ items |
| best suffix plus best prefix | $\Theta(n)$ | $\Theta(n)$ | $\max_{i} (\text{suffix sum from } i + \text{best prefix ending before } i)$ |
| doubling and a monotonic deque | $\Theta(n)$ | $\Theta(n)$ | best window of length at most $n$ in $A A$ |
| [circular Kadane](/circular-kadane-algorithm/) | $\Theta(n)$ | $O(1)$ | $\max(S^*_{\max}, T - S^*_{\min})$, two [Kadane](/kadane-algorithm/) scans |

**Best suffix plus best prefix.** A wrapping subarray is a non-empty suffix $A[i..n-1]$ joined to a non-empty prefix $A[0..j]$ with $j < i$. Compute $R[i] = \max_{j < i} (A[0] + \dots + A[j])$ from left to right, then scan the suffix sums from the right and take $\max_i (\text{suffix}(i) + R[i])$. This is the crossing step of the [divide-and-conquer algorithm](/maximum-subarray-divide-and-conquer/) with the cut at the end of the ring.

**Doubling.** Let $B = A A$, of length $2n$, with prefix sums $P$. Every circular subarray is a window $B[a..b]$ with $a \le n - 1$ and $b - a + 1 \le n$. For each end $b$, the best start minimizes $P_a$ over $b - n + 1 \le a \le b$, a sliding window minimum that a monotonic deque gives in $O(1)$ amortized time.

## Bounds

**Linear time is optimal.** The same [adversary argument](/adversary-argument/) as for the plain problem applies: if an algorithm does not read $A[k]$, setting $A[k]$ larger than the sum of the absolute values of all other items forces $A[k]$ into every best arc, and the algorithm cannot tell. So $\Omega(n)$ time is needed, and the circular Kadane algorithm reaches it with $O(1)$ extra space.

## Reductions

- **Circular to linear.** By the complement form, one maximum and one minimum plain subarray, plus the total, give the circular answer. The minimum is a maximum of the negated array.
- **Linear to circular.** Let $M$ be larger than $2 \sum_k |A[k]|$, and append the item $-M$ to $A$. Every wrapping subarray of the new ring contains its last item $-M$, and so does every plain subarray that ends there. Such a subarray has a sum less than $-\sum_k |A[k]|$, which is less than every item of $A$, so none of them can be best. The best circular subarray of the new ring is then the best plain subarray of $A$. So the two problems have the same complexity up to $O(n)$ extra work.
- **Circular to bounded length.** Doubling turns the ring into a plain array with a length bound $n$, as above.

## Applications

- **Cyclic time series.** Hourly or monthly values over a cycle, where the best period may pass midnight or the end of the year.
- **Angles and directions.** Values per sector of a circle, for example readings of a sensor that turns, where the best arc may cross the zero angle.
- **Circular sequences.** Scores along a circular DNA molecule, such as a bacterial chromosome or a plasmid, where a high-scoring segment may cross the point where the sequence was cut open.
- **Exercises.** It is a standard exercise on the complement trick and on the all-negative special case.

## References
