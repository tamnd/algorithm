---
tag: 8EPB4B
kind: algorithm
slug: kadane-max-product
name: Max-product scan with minimum tracking
aliases:
- Kadane-style maximum product algorithm
area: sequences/subarray-problems
level: core
summary: Single pass that keeps both the running maximum and running minimum product at each position.
solves: [maximum-product-subarray]
model: word-ram
complexity:
  vars: {n: the number of items in the array}
  time: {worst: Θ(n), average: Θ(n), best: Θ(n)}
  space: {extra: Θ(1)}
properties: {stable: false, in_place: true, adaptive: false, online: true, deterministic: true, comparison: false, recursive: false}
prereqs: [maximum-product-subarray, kadane-algorithm, loop-invariant]
see_also: [maximum-subarray-problem, circular-kadane-algorithm, optimal-substructure, sliding-window-positive-sum, online-algorithm, maximum-circular-subarray-sum, prefix-sums, subarray]
sources:
  - url: https://leetcode.com/problems/maximum-product-subarray/
    title: LeetCode, problem 152, Maximum Product Subarray
    locator: problem statement and examples
  - url: https://leetcode.com/problems/maximum-length-of-subarray-with-positive-product/
    title: LeetCode, problem 1567, Maximum Length of Subarray With Positive Product
    locator: problem statement (the same two-state scan, for lengths)
  - paper: doi:10.1145/358234.381162
    title: "Jon Bentley, Programming pearls: algorithm design techniques, Communications of the ACM 27(9) (1984), 865-873"
    locator: the linear scan for sums that this algorithm extends
---

The max-product scan with minimum tracking solves the [maximum product subarray](/maximum-product-subarray/) problem in one pass, in $\Theta(n)$ time and $O(1)$ extra space. It is [Kadane's algorithm](/kadane-algorithm/) with two states instead of one. At each position $j$ it keeps $hi$, the largest product of a subarray that ends at $j$, and $lo$, the smallest. A negative item maps large products to small ones and small to large, so before such an item the two states are swapped. Then each state is either the item alone or the item times the old state. The answer is the largest $hi$ seen.

## In plain words

Walk along the list once. Carry two numbers: the largest and the smallest product of a stretch that ends at the current place.

When the next number is positive, the largest product grows from the old largest, and the smallest from the old smallest. When the next number is negative, it is the other way round: the old smallest, which may be very negative, gives the new largest. So swap the two before you multiply. In both cases, also try to start a new stretch at the next number alone, which is what a zero forces.

Keep a note of the largest product you have seen. That is the answer.

## The problem

**Input.** An array $A[0..n-1]$ of numbers with $n \ge 1$.

**Output.** The largest product $\Pi^* = \max_{i \le j} A[i] \cdots A[j]$ of a non-empty [subarray](/subarray/).

## The algorithm

```pseudo id=main
MAX-PRODUCT(A[0 .. n-1])
L1  hi ← A[0]; lo ← A[0]; best ← A[0]
L2  for j ← 1 to n − 1 do
L3      if A[j] < 0 then swap hi and lo
L4      hi ← max(A[j], hi · A[j])
L5      lo ← min(A[j], lo · A[j])
L6      best ← max(best, hi)
L7  return best
```

Line L3 swaps the states before a negative item, so that line L4 multiplies the item by the old smallest product. Lines L4 and L5 each choose between starting again at $A[j]$ and extending. Line L6 keeps the running answer.

The recurrence behind the loop, with $E^{+}(j)$ and $E^{-}(j)$ the largest and the smallest product of a subarray ending at $j$, is
$$E^{+}(j) = \max\bigl(A[j],\ A[j] E^{+}(j-1),\ A[j] E^{-}(j-1)\bigr), \qquad E^{-}(j) = \min\bigl(A[j],\ A[j] E^{+}(j-1),\ A[j] E^{-}(j-1)\bigr).$$
The swap picks the right one of the two products, so lines L4 and L5 need only two choices each.

## Example

$A = [2, 3, -2, 4, -1]$. The table shows the values after line L6 of each step.

| $j$ | $A[j]$ | swap | $hi$ | $lo$ | $best$ |
|---|---|---|---|---|---|
| 0 | 2 | | 2 | 2 | 2 |
| 1 | 3 | no | 6 | 3 | 6 |
| 2 | $-2$ | yes | $-2$ | $-12$ | 6 |
| 3 | 4 | no | 4 | $-48$ | 6 |
| 4 | $-1$ | yes | 48 | $-4$ | 48 |

At step 2 the swap gives $hi = 3$ and $lo = 6$ before the update, so $hi = \max(-2, -6) = -2$ and $lo = \min(-2, -12) = -12$. The small product $-12$ is kept, and at step 4 the negative item turns $lo = -48$ into $hi = 48$. The answer is $48$, the whole array. A scan that kept only the largest product would return $6$.

## Correctness

The loop keeps this invariant at the end of each step $j$:

> **(P)** $hi = E^{+}(j)$, $lo = E^{-}(j)$, and $best$ is the largest product of a subarray of $A[0..j]$.

*Base.* After line L1, the only subarray of $A[0..0]$ has product $A[0]$.

*Step.* Every subarray that ends at $j \ge 1$ is $A[j..j]$ or a subarray ending at $j - 1$ extended by $A[j]$. The products of the second kind are $x \cdot A[j]$ for products $x$ of subarrays ending at $j - 1$, and those $x$ lie between $E^{-}(j-1)$ and $E^{+}(j-1)$, both of which occur. The map $x \mapsto x \cdot A[j]$ does not decrease when $A[j] \ge 0$ and does not increase when $A[j] < 0$. So the largest product of the second kind is $E^{+}(j-1) A[j]$ in the first case and $E^{-}(j-1) A[j]$ in the second, and the smallest is the other one. After the swap of line L3, lines L4 and L5 compute exactly these. A subarray of $A[0..j]$ either ends at $j$ or lies in $A[0..j-1]$, so line L6 keeps the last part of (P).

At the end (P) with $j = n - 1$ gives the answer. The [proof page](proofs/correctness.md) writes out the induction.

## Complexity

- **Time.** The loop runs $n - 1$ times, with at most two multiplications and three comparisons each, so $\Theta(n)$ on every input, as long as a product fits in a word.
- **Space.** Three scalars, $\Theta(1)$ extra space.
- **Size of the numbers.** With $b$-bit integer items, $hi$ and $lo$ can have up to $n b$ bits. With exact big integers, the time is the cost of the multiplications. With floating-point items, the values can overflow to infinity or fall to zero; keeping $\log |hi|$ and the sign avoids that.

## Properties

- **Online.** After step $j$, $best$ is the answer for $A[0..j]$, with $O(1)$ memory.
- **Two-state dynamic program.** It is a dynamic program with [optimal substructure](/optimal-substructure/) only once the state holds both extremes. One extreme alone is not enough.
- **Zeros.** At $A[j] = 0$ both $hi$ and $lo$ become $0$, which restarts the scan. Lines L4 and L5 handle it with no extra test.
- **Which subarray.** To report the subarray, keep a start index for each state, swap the starts with the states in line L3, and set a start to $j$ when its state is reset to $A[j]$.

## Variants and improvements

- **Without the swap.** Compute both products first: $p = hi \cdot A[j]$ and $q = lo \cdot A[j]$, then $hi \leftarrow \max(A[j], p, q)$ and $lo \leftarrow \min(A[j], p, q)$. This needs two temporaries and three-way choices but no test on the sign.
- **Integer items.** If every non-zero item has $|A[k]| \ge 1$, the best of all prefix products and all suffix products, each restarted after a zero, is the answer. This needs no minimum, but it fails for items between $-1$ and $1$.
- **Positive items.** With no zero and no negative item, $lo$ is not needed, and the scan is Kadane's algorithm on the logarithms.
- **Lengths.** Keeping the longest length of a subarray with a positive product and with a negative product, in the same two-state way, solves LeetCode problem 1567.
- **Circular arrays.** Run the scan on the doubled array with a length bound $n$; the complement trick of the [circular Kadane algorithm](/circular-kadane-algorithm/) fails for products.

## When to use it

Use it for the largest product of a contiguous run when items can be negative or zero, or for any running aggregate where a sign change swaps the best and the worst. When all items are positive, Kadane's algorithm on logarithms is enough and avoids overflow.

## Pitfalls

- **Swapping after the update.** The swap must come before lines L4 and L5. Updating $hi$ first and then using the new $hi$ to compute $lo$ uses a value from step $j$ in place of one from step $j - 1$.
- **Starting with $best = 0$ or $1$.** For $A = [-3]$ the answer is $-3$. Start from $A[0]$.
- **Keeping only the maximum.** For $[-2, 3, -4]$, a scan with $hi$ alone returns $3$, but the answer is $24$.
- **Overflow.** In LeetCode 152 the answer fits in $32$ bits, but the intermediate $lo$ need not. Use a wider type, or exact integers.

## Implementations

## History

The two-state scan has no known first paper. It extends the linear scan that Kadane found in 1977 for sums, and it is the usual solution of LeetCode problem 152, which made it a standard interview exercise.

## References
