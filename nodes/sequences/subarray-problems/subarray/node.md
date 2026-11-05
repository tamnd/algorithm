---
tag: HS3HAQ
kind: definition
slug: subarray
name: Subarray
aliases:
- contiguous subsequence
- contiguous segment
area: sequences/subarray-problems
level: intro
summary: A run of consecutive elements of an array, as opposed to a subsequence, which may skip elements.
prereqs: [array]
see_also: [subsequence, prefix-sums, sliding-window, maximum-subarray-problem, two-pointers, suffix]
sources:
  - book: isbn:9780262033848
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, third edition
    locator: Section 4.1, The maximum-subarray problem (the notation A[i..j] for a contiguous subarray)
  - url: https://cses.fi/book/book.pdf
    title: Antti Laaksonen, Competitive Programmer's Handbook
    locator: Chapter 2, Time complexity, Section 2.4 Maximum subarray sum
  - book: isbn:9780201657883
    title: Jon Bentley, Programming Pearls, second edition
    locator: Column 8, Section 8.1 (the maximum sum of a contiguous subvector)
---

A subarray of an array is a block of items that sit next to each other in the array, taken in their original order. It is fixed by a start index and an end index. Subarrays are the objects of the [maximum subarray problem](/maximum-subarray-problem/), of range queries, and of the [sliding window](/sliding-window/) and [two pointers](/two-pointers/) techniques. A [subsequence](/subsequence/) keeps the order too but may skip items, so every subarray is a subsequence and not the reverse.

## Definition

Let $A[0..n-1]$ be an [array](/array/) of length $n$. For integers $0 \le i \le j \le n - 1$, the *subarray* $A[i..j]$ is the array

$$A[i..j] = (A[i], A[i+1], \dots, A[j])$$

of length $j - i + 1$. Its *start* is $i$ and its *end* is $j$. Two subarrays are equal as positions when they have the same start and end, even if their items are equal as values.

**Half-open form.** Many algorithms use the range $A[i..j)$ with $0 \le i \le j \le n$, which holds the items with indices $i \le k < j$ and has length $j - i$. This form includes the *empty subarray*, $i = j$, and it fits [prefix sums](/prefix-sums/): the sum of $A[i..j)$ is $P_j - P_i$.

**Count.** An array of length $n$ has $\binom{n}{2} + n = n(n+1)/2$ non-empty subarrays, one for each pair $i \le j$. With the half-open form there are $n + 1$ empty ranges, one at each gap, which are all the same as values. For the subsequences the count is $2^n$, so problems on subarrays have a quadratic search space and problems on subsequences an exponential one.

**Special cases.** A *prefix* is a subarray with $i = 0$ and a *suffix* is a subarray with $j = n - 1$. A *window* of length $k$ is a subarray with $j - i + 1 = k$. In a *circular* array, a subarray may also wrap around: $A[i..n-1]$ followed by $A[0..j]$ for $0 \le j < i$.

## Examples and non-examples

Take $A = [3, 1, 4, 1, 5]$.

- $[1, 4, 1] = A[1..3]$ is a subarray of length $3$.
- $[3] = A[0..0]$ and $[5] = A[4..4]$ are subarrays of length $1$. $A[0..4]$, the whole array, is a subarray.
- $[1]$ occurs as the two different subarrays $A[1..1]$ and $A[3..3]$.
- $[3, 4, 5]$ is a subsequence but not a subarray, since it skips $A[1]$ and $A[3]$.
- $[4, 1, 3]$ is neither: its items appear in $A$, but not in this order.
- $[5, 3]$ is not a subarray of $A$ as a plain array. It is a subarray of $A$ read as a circular array, since it wraps from index $4$ to index $0$.
- $A$ has $5 \cdot 6 / 2 = 15$ non-empty subarrays.

## Related definitions

- **[Subsequence](/subsequence/).** Items $A[i_1], \dots, A[i_m]$ with $i_1 < \dots < i_m$. A subarray is a subsequence whose indices are consecutive.
- **Substring.** The same notion as a subarray, for strings. A substring is a contiguous block of characters; a subsequence of a string may skip characters.
- **Prefix and [suffix](/suffix/).** Subarrays that touch the start or the end.
- **Window.** A subarray of a fixed length, or the current range of a [sliding window](/sliding-window/) algorithm, whose two ends only move to the right.
- **Submatrix.** The two-dimensional analogue: a block of consecutive rows and consecutive columns, as in the [maximum sum submatrix](/maximum-sum-submatrix/) problem.
- **Segment or interval.** The set of indices $\{i, \dots, j\}$ of a subarray, used by range-query structures such as the segment tree.

## References
