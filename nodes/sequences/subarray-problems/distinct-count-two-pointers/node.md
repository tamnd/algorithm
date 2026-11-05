---
tag: 9MW95T
kind: algorithm
slug: distinct-count-two-pointers
name: Two pointers with distinct counts
aliases:
- sliding window with frequency map
area: sequences/subarray-problems
level: core
summary: Advance the right pointer, shrink the left pointer while the distinct count exceeds k, and track the best length.
solves: [longest-subarray-with-at-most-k-distinct]
model: word-ram
complexity:
  vars: {n: the number of items in the array, k: the bound on the number of distinct values}
  time: {worst: Θ(n^2), average: Θ(n) expected, best: Θ(n)}
  space: {extra: "Θ(min(n, k))"}
properties: {stable: false, in_place: true, adaptive: false, online: true, deterministic: false, comparison: false, recursive: false}
prereqs: [longest-subarray-with-at-most-k-distinct, sliding-window, two-pointers, hash-table]
see_also: [monotone-window-property, frequency-counter, longest-substring-with-k-distinct, sliding-window-distinct-count, coordinate-compression, sliding-window-positive-sum, longest-substring-without-repeating-characters, range-distinct-count-query]
sources:
  - url: https://leetcode.com/problems/fruit-into-baskets/
    title: LeetCode, problem 904, Fruit Into Baskets
    locator: problem statement (the case k = 2)
  - url: https://leetcode.com/problems/subarrays-with-k-different-integers/
    title: LeetCode, problem 992, Subarrays with K Different Integers
    locator: problem statement (counting with exactly k distinct values, by two runs of the at-most count)
  - url: https://cses.fi/book/book.pdf
    title: Antti Laaksonen, Competitive Programmer's Handbook
    locator: Chapter 8, Amortized analysis, Section 8.1 Two pointers method (the amortized bound on the pointer moves)
  - book: isbn:9780262033848
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, third edition
    locator: Chapter 11, Hash Tables, Sections 11.2 and 11.3.3 (expected O(1) time per operation)
---

Two pointers with distinct counts finds the longest [subarray](/subarray/) with at most $k$ distinct values in one pass, in $O(n)$ expected time. It keeps a [sliding window](/sliding-window/) $A[i..j]$, a [hash table](/hash-table/) that maps each value in the window to its count, and the number $d$ of values with a positive count. The right pointer $j$ adds one item per step. While $d > k$, the left pointer $i$ removes items from the front. Then the window is the longest valid one that ends at $j$, and its length is a candidate for the answer. This solves [longest subarray with at most k distinct values](/longest-subarray-with-at-most-k-distinct/), and with a small change it counts the subarrays with at most $k$ or exactly $k$ distinct values.

## In plain words

Keep a window over the list, with a tally of how many times each value is in it. Also keep the number of different values in the tally.

Move the front edge on by one item and add it to the tally. If the item is new to the window, the number of different values goes up by one.

If there are now too many different values, move the back edge on, one item at a time, and take each item out of the tally. When the tally of a value reaches zero, that value has left the window. Stop when the number of different values is allowed again.

Now the window is the longest allowed one that ends at the front edge. Compare its length with the best so far. Each item comes in once and goes out at most once.

## The problem

**Input.** An array $A[0..n-1]$ of values that can be tested for equality and hashed, and an integer $k \ge 0$.

**Output.** The largest length $j - i$ over $0 \le i \le j \le n$ such that $A[i..j)$ has at most $k$ distinct values, and a start $i$ of one such subarray.

## The algorithm

```pseudo id=main
DISTINCT-WINDOW(A[0 .. n-1], k)
L1  cnt ← empty hash table; d ← 0; i ← 0; best ← 0; start ← 0
L2  for j ← 0 to n − 1 do
L3      if A[j] ∉ cnt then cnt[A[j]] ← 0; d ← d + 1
L4      cnt[A[j]] ← cnt[A[j]] + 1
L5      while d > k do
L6          cnt[A[i]] ← cnt[A[i]] − 1; if cnt[A[i]] = 0 then delete A[i] from cnt; d ← d − 1
L7          i ← i + 1
L8      if j + 1 − i > best then best ← j + 1 − i; start ← i
L9  return (best, start)
```

Lines L3 and L4 add $A[j]$ to the window. Lines L5 to L7 remove items from the front until at most $k$ values remain. Line L6 deletes a value whose count falls to zero, so the table holds exactly the $d$ values of the window. Line L8 records the window $A[i..j]$ if it is the longest so far.

## Example

$A = [1, 2, 1, 2, 3, 3, 4, 1]$ and $k = 2$. The table shows the state after line L7 for each $j$, and $best$ after line L8.

| $j$ | $A[j]$ | removed by L5 to L7 | $i$ | window | counts | $d$ | $best$ |
|---|---|---|---|---|---|---|---|
| 0 | 1 | | 0 | $[1]$ | 1:1 | 1 | 1 |
| 1 | 2 | | 0 | $[1, 2]$ | 1:1, 2:1 | 2 | 2 |
| 2 | 1 | | 0 | $[1, 2, 1]$ | 1:2, 2:1 | 2 | 3 |
| 3 | 2 | | 0 | $[1, 2, 1, 2]$ | 1:2, 2:2 | 2 | 4 |
| 4 | 3 | 1, 2, 1 | 3 | $[2, 3]$ | 2:1, 3:1 | 2 | 4 |
| 5 | 3 | | 3 | $[2, 3, 3]$ | 2:1, 3:2 | 2 | 4 |
| 6 | 4 | 2 | 4 | $[3, 3, 4]$ | 3:2, 4:1 | 2 | 4 |
| 7 | 1 | 3, 3 | 6 | $[4, 1]$ | 4:1, 1:1 | 2 | 4 |

The answer is $4$ with start $0$, the subarray $[1, 2, 1, 2]$. At $j = 4$ the value $3$ makes $d = 3$, and the left pointer must pass three items before the value $1$ leaves the window. In total the left pointer moves $6$ times and the right pointer $8$ times.

## Correctness

Let $D(i, j)$ be the number of distinct values in $A[i..j)$, and for each $j$ let $L(j)$ be the smallest $i \le j$ with $D(i, j) \le k$. Because $D(i, j)$ can only fall when $i$ grows and only rise when $j$ grows, $L$ never decreases. The key invariant is that after line L7 in the step for $j$,
$$i = L(j + 1), \qquad d = D(i, j + 1),$$
and the table holds the count of each value in $A[i..j]$. By the invariant, $A[i..j]$ is the longest valid subarray that ends at $j$, so line L8 tests the best candidate for each end, and $best$ is the maximum over all ends. The empty subarray, with length $0$, is the starting value. The [proof page](proofs/correctness.md) gives the details.

## Complexity

- **Time.** The right pointer moves $n$ times and the left pointer at most $n$ times in total, since $i \le j + 1$ and $i$ never decreases. So there are at most $2n$ table updates. With a hash table each costs $O(1)$ expected time, for $O(n)$ expected time in total. With adversarial collisions a table operation can cost $\Theta(n)$, for $\Theta(n^2)$ in the worst case. With a direct count array over values in $\{0, \dots, U - 1\}$, the time is $O(n + U)$ in the worst case.
- **Space.** The table holds at most $k + 1$ keys at any time, and at most $n$, so the extra space is $O(\min(n, k))$. This needs the deletes in line L6.

## Properties

- **Online.** Each item is read once, and after item $j$ the answer for the prefix $A[0..j]$ is known. But the left pointer reads items again, so the window must be stored or the stream read twice.
- **Randomized cost.** The result does not depend on the hash function, but the running time does.
- **Equality only.** The method needs equality tests and hashing, not an order on the values.
- **Amortized, not per step.** One step of the right pointer can move the left pointer many times, as at $j = 4$ in the example. Only the total is linear.

## Variants and improvements

- **Counting.** Adding $j + 1 - i$ in line L8, in place of the maximum, counts the subarrays with at most $k$ distinct values. The count with exactly $k$ is the count with at most $k$ minus the count with at most $k - 1$ (LeetCode 992).
- **Direct count array.** For small integer values, or after [coordinate compression](/coordinate-compression/), an array replaces the hash table and the time is worst-case linear.
- **No repeated value.** Changing the test in line L5 to "the count of $A[j]$ is more than $1$" gives the longest subarray with all values distinct, as in the [longest substring without repeating characters](/longest-substring-without-repeating-characters/). A table of the last index of each value lets the left pointer jump in one step.
- **Strings.** For characters, the table is an array of size $\sigma$, as in the [longest substring with k distinct characters](/longest-substring-with-k-distinct/).
- **Fixed window length.** For the number of distinct values in each window of a fixed length, the left and right pointers move together. See [sliding window distinct count](/sliding-window-distinct-count/).
- **General template.** The same loop works for any window property that is closed under sub-intervals and has an $O(1)$ update. See the [monotone window property](/monotone-window-property/) and [sliding window with positive sums](/sliding-window-positive-sum/).

## When to use it

Use it for the longest or the count of subarrays under a bound on the number of distinct values, when the values can be hashed. It needs one pass and little memory. If the values are small integers, use a count array. If the input is under attack, use a salted hash or sort the values first. For many range queries on a fixed array, use a [range distinct count query](/range-distinct-count-query/) structure instead.

## Pitfalls

- **Not deleting zero counts.** If a value with count $0$ stays in the table, then the table size is not the number of distinct values. Code that uses the table size as $d$ then gives wrong answers, and the table grows to $O(n)$.
- **Using `if` in place of `while`.** One new value can need many removals, as at $j = 4$ in the example. A single removal leaves an invalid window.
- **$k = 0$.** The loop of line L5 then empties the window at each step, and the answer is $0$. Code that assumes a non-empty window fails here.
- **Exactly $k$ by one pass.** The windows with exactly $k$ distinct values do not have the monotone property, so one window pass does not count them. Use the subtraction of two at-most counts.
- **Off by one in the length.** The window $A[i..j]$ is closed, with length $j - i + 1$.

## Implementations

## History

The two pointers method with a count table is programming folklore with no known first paper. It became a standard exercise in contest programming and interview problems, such as LeetCode 904 (Fruit Into Baskets) and LeetCode 992 (Subarrays with K Different Integers). The amortized argument that bounds the pointer moves is the one that Laaksonen's handbook gives for the two pointers method.

## References
