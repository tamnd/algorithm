---
tag: ASHEE3
kind: algorithm
slug: prefix-sum-hash-counting
name: Prefix sum hash counting
aliases:
- prefix sum with hash map
area: sequences/subarray-problems
level: core
summary: Store prefix-sum frequencies in a hash table; each subarray sum equals a difference of two prefix sums.
solves: [subarray-sum-equals-k, longest-zero-sum-subarray]
model: word-ram
complexity:
  vars: {n: the number of items in the array}
  time: {worst: Θ(n^2), average: Θ(n) expected, best: Θ(n)}
  space: {extra: Θ(n)}
properties: {stable: false, in_place: true, adaptive: false, online: true, deterministic: false, comparison: false, recursive: false}
prereqs: [subarray-sum-equals-k, prefix-sums, hash-table, loop-invariant]
see_also: [longest-zero-sum-subarray, range-sum-query, sliding-window-positive-sum, fenwick-tree, element-distinctness, frequency-counter, coordinate-compression, maximum-xor-subarray]
sources:
  - url: https://leetcode.com/problems/subarray-sum-equals-k/
    title: LeetCode, problem 560, Subarray Sum Equals K
    locator: problem statement and examples
  - url: https://leetcode.com/problems/subarray-sums-divisible-by-k/
    title: LeetCode, problem 974, Subarray Sums Divisible by K
    locator: problem statement (the same count over residues)
  - url: https://cses.fi/book/book.pdf
    title: Antti Laaksonen, Competitive Programmer's Handbook
    locator: Chapter 9, Range queries, Section 9.1 Static array queries (a subarray sum as a difference of two prefix sums)
  - book: isbn:9780262033848
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, third edition
    locator: Chapter 11, Hash Tables, Sections 11.2 and 11.3.3 (chaining and universal hashing, expected O(1) time per operation)
---

Prefix sum hash counting counts the [subarrays](/subarray/) with sum exactly $k$ in one pass, in $O(n)$ expected time, for items of any sign. It walks along the array with the running prefix sum $p$ and keeps a [hash table](/hash-table/) $C$ that maps each prefix sum seen so far to the number of times it has occurred. A subarray that ends at the current item has sum $k$ exactly when the prefix sum before its start is $p - k$, so the number of such subarrays is $C[p - k]$. This solves [subarray sum equals k](/subarray-sum-equals-k/). With the first index of each prefix sum in place of its count, the same pass finds the [longest zero-sum subarray](/longest-zero-sum-subarray/).

## In plain words

Walk along the list and keep the running total. Also keep a tally book: for each running total you have seen, how many times you have seen it. Before you start, the running total is zero, so write down zero once.

At each number, first add it to the running total. Then ask the tally book how many times you have seen the running total minus the target. Each of those times marks the start of a stretch that ends here and adds up to the target, so add that count to the answer. Then write the new running total into the tally book.

Each step is one lookup and one update, so the whole walk is fast.

## The problem

**Input.** An array $A[0..n-1]$ of integers, which may be negative, and a target $k$.

**Output.** The number of pairs $(i, j)$ with $0 \le i \le j \le n - 1$ and $A[i] + \dots + A[j] = k$.

## The algorithm

```pseudo id=main
COUNT-SUM-K(A[0 .. n-1], k)
L1  C ← empty hash table; C[0] ← 1; p ← 0; count ← 0
L2  for j ← 0 to n − 1 do
L3      p ← p + A[j]
L4      count ← count + C[p − k]   (0 if absent)
L5      C[p] ← C[p] + 1   (from 0 if absent)
L6  return count
```

After line L3, $p$ is the [prefix sum](/prefix-sums/) $P_{j+1} = A[0] + \dots + A[j]$. The table holds the counts of $P_0, \dots, P_j$, so line L4 adds the number of starts $i$ with $P_i = P_{j+1} - k$, which is the number of subarrays $A[i..j]$ with sum $k$. Line L5 then adds $P_{j+1}$ to the table. The entry $C[0] = 1$ of line L1 stands for $P_0 = 0$, the empty prefix, so that subarrays that start at index $0$ are counted.

## Example

$A = [3, 4, 7, 2, -3, 1, 4, 2]$ and $k = 7$. The table shows each step; "lookup" is the key $p - k$ of line L4 and its count before line L5.

| $j$ | $A[j]$ | $p$ | lookup $p - 7$ | count found | $count$ | key added |
|---|---|---|---|---|---|---|
| 0 | 3 | 3 | $-4$ | 0 | 0 | 3 |
| 1 | 4 | 7 | 0 | 1 | 1 | 7 |
| 2 | 7 | 14 | 7 | 1 | 2 | 14 |
| 3 | 2 | 16 | 9 | 0 | 2 | 16 |
| 4 | $-3$ | 13 | 6 | 0 | 2 | 13 |
| 5 | 1 | 14 | 7 | 1 | 3 | 14 (now 2) |
| 6 | 4 | 18 | 11 | 0 | 3 | 18 |
| 7 | 2 | 20 | 13 | 1 | 4 | 20 |

The answer is $4$. The hits are $[3, 4]$ at $j = 1$ (start after $P_0 = 0$), $[7]$ at $j = 2$ (start after $P_2 = 7$), $[7, 2, -3, 1]$ at $j = 5$ (again after $P_2 = 7$), and $[1, 4, 2]$ at $j = 7$ (after $P_5 = 13$).

## Correctness

Write $P_0 = 0$ and $P_m = A[0] + \dots + A[m-1]$. The loop keeps this invariant at the start of each step $j$:

> **(H)** $p = P_j$; for every value $v$, $C[v]$ is the number of $m \le j$ with $P_m = v$ (absent means $0$); and $count$ is the number of subarrays $A[i..l]$ with $l < j$ and sum $k$.

*Base.* Line L1 makes $C$ hold one occurrence of $P_0 = 0$, with $p = 0$ and $count = 0$, and there is no subarray that ends before index $0$.

*Step.* Line L3 sets $p = P_{j+1}$. A subarray $A[i..j]$ has sum $P_{j+1} - P_i$, so it has sum $k$ exactly when $P_i = p - k$, for some $0 \le i \le j$. By (H) the number of such $i$ is $C[p - k]$, which line L4 adds. Line L5 records $P_{j+1}$, so (H) holds at the start of step $j + 1$. Each subarray is counted once, at the step of its last index.

At the end, $j = n$ and (H) says $count$ is the number of all subarrays with sum $k$. The order of lines L4 and L5 matters: looking up after recording would count the empty subarray $A[j+1..j]$ when $k = 0$. The [proof page](proofs/correctness.md) writes out the induction.

## Complexity

- **Time.** There are $n$ lookups and $n + 1$ insertions or increments. With chaining and a hash function chosen at random from a universal family, each takes $O(1)$ expected time, so the total is $\Theta(n)$ expected. For a fixed hash function, an adversary can choose items whose prefix sums all collide, and then each operation costs up to the table size, $\Theta(n^2)$ in total.
- **Space.** The table holds at most $n + 1$ distinct keys, $\Theta(n)$ in the worst case.
- **No hashing.** Replacing the table by a [balanced search tree](/balanced-binary-search-tree/), or by [coordinate compression](/coordinate-compression/) and an array of counters, gives $O(n \log n)$ worst-case time. By the reduction from [element distinctness](/element-distinctness/) on the problem page, comparisons alone cannot do better.

## Properties

- **Online.** Step $j$ uses only $A[0..j]$, and $count$ is the answer for the prefix read so far.
- **Las Vegas.** The answer is always right. Only the running time depends on the hash function.
- **Exact keys.** The method needs exact equality of prefix sums. With integers it is exact. With floating-point items, two sums that are equal in real arithmetic can differ in the last bit, so a hit can be missed.
- **Many targets.** The target appears only in the lookup key. For a new target the pass must run again, with $\Theta(n)$ expected time per target.

## Variants and improvements

- **Longest subarray with sum $k$.** Store the first index of each prefix sum, and do not overwrite it. At step $j$, if $p - k$ is present with first index $i$, the subarray $A[i..j]$ is a candidate of length $j - i + 1$. For $k = 0$ this is the [longest zero-sum subarray](/longest-zero-sum-subarray/).
- **Shortest subarray with sum $k$.** Store the last index instead, and overwrite it at each step.
- **Divisible by $k$.** Use $p \bmod k$ as the key, with a non-negative remainder, and look up the same key. An array of $k$ counters replaces the hash table, so the time is $O(n + k)$ worst case.
- **Zero counts in groups.** For $k = 0$, the answer is $\sum_v \binom{c_v}{2}$ over the final counts $c_v$, so the lookups can be done at the end.
- **XOR.** With $p \leftarrow p \oplus A[j]$ and the key $p \oplus k$, the pass counts the subarrays with XOR equal to $k$.
- **Non-negative items.** Two pointers count the windows with sum $k$ in $O(1)$ space; see the [positive-sum sliding window](/sliding-window-positive-sum/).
- **Sums in a range.** For $L \le$ sum $\le U$, keep the earlier prefix sums in a [Fenwick tree](/fenwick-tree/) over compressed values and count the range $[p - U, p - L]$, in $O(n \log n)$ time.

## When to use it

Use it to count, find, or measure subarrays with an exact sum when items can be negative. When all items are non-negative, two pointers use less memory. When the condition is an inequality, use a Fenwick tree or a sorted structure in place of the hash table. When the input may be chosen by an adversary, use a randomized hash function, or the sorted structure.

## Pitfalls

- **Forgetting $C[0] = 1$.** Without it, subarrays that start at index $0$ are missed. For $A = [7]$ and $k = 7$ the answer is $1$, from $P_1 - P_0$.
- **Updating before the lookup.** For $k = 0$ the lookup then finds the current prefix sum itself and counts an empty subarray at every step.
- **Using a set instead of counts.** A prefix sum can occur many times, as $14$ does in the example. A set of seen sums counts each start value once and misses subarrays.
- **Negative remainders.** In many languages $-3 \bmod 5$ is $-3$. For the divisible variant, normalize the remainder to $0..k-1$, or two equal residues will look different.
- **Two pointers on negative items.** Shrinking a window when its sum is above $k$ is wrong once items can be negative; this is why the hash table is needed.

## Implementations

## History

The identity that a subarray sum is a difference of two prefix sums is old, and the counting pass with a hash table has no known first paper. It became a standard technique of programming contests and interviews, and LeetCode problem 560 is its usual form.

## References
