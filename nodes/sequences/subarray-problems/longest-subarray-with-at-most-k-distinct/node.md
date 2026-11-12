---
tag: 4D0T7F
kind: problem
slug: longest-subarray-with-at-most-k-distinct
name: Longest subarray with at most k distinct values
aliases:
- longest subarray with distinct elements
- longest window with at most k distinct
area: sequences/subarray-problems
level: intro
summary: Find the longest subarray containing at most k distinct values; k = 1 gives the longest run of equal values.
prereqs: [subarray, sliding-window, hash-table]
see_also: [distinct-count-two-pointers, longest-substring-with-k-distinct, monotone-window-property, coordinate-compression, element-distinctness, range-distinct-count-query, sliding-window-distinct-count, frequency-counter]
sources:
  - url: https://leetcode.com/problems/fruit-into-baskets/
    title: LeetCode, problem 904, Fruit Into Baskets
    locator: problem statement (the case k = 2 on an array of integers)
  - url: https://leetcode.com/problems/subarrays-with-k-different-integers/
    title: LeetCode, problem 992, Subarrays with K Different Integers
    locator: problem statement (counting the subarrays with exactly k distinct values)
  - url: https://cses.fi/book/book.pdf
    title: Antti Laaksonen, Competitive Programmer's Handbook
    locator: Chapter 8, Amortized analysis, Section 8.1 Two pointers method
---

The problem gives an array of values and an integer $k$, and asks for the longest [subarray](/subarray/) that contains at most $k$ distinct values. A [sliding window](/sliding-window/) with a count for each value in the window solves it in $O(n)$ expected time, by the [distinct count two pointers](/distinct-count-two-pointers/) algorithm. It is the array form of the [longest substring with at most $k$ distinct characters](/longest-substring-with-k-distinct/). On arrays the values come from a large or unknown universe, such as 64-bit integers, so the count table is a [hash table](/hash-table/) or an array over [compressed](/coordinate-compression/) values instead of an array indexed by the alphabet.

## In plain words

Walk along a row of fruit trees, each tree of some kind of fruit. You have two baskets, and each basket can hold only one kind of fruit. You want to pick from as many trees in a row as you can. The answer is the longest stretch of trees that has at most two kinds of fruit.

With $k$ baskets, the question is the same with $k$ kinds. If a stretch has at most $k$ kinds, every shorter stretch inside it also has at most $k$ kinds. This is what makes a single walk with two markers enough: the front marker adds trees, and the back marker drops trees from the start only when there are too many kinds.

## Definition

**Input.** An array $A[0..n-1]$ of values that can be compared for equality and hashed, and an integer $k \ge 0$.

**Output.** The largest length $j - i$ over $0 \le i \le j \le n$ such that the half-open subarray $A[i..j)$ has at most $k$ distinct values, and in the search version one such pair $(i, j)$. The empty subarray always qualifies, so the answer is $0$ when $k = 0$ or $n = 0$.

**Monotone property.** Let $D(i, j)$ be the number of distinct values in $A[i..j)$. If $i \le i' \le j' \le j$ then $D(i', j') \le D(i, j)$. So the property "at most $k$ distinct values" holds for every subarray of a subarray that has it. This is the [monotone window property](/monotone-window-property/), and it means that the smallest allowed start for each end never moves left as the end moves right.

## Variants

- **$k = 1$.** The longest run of equal values. One pass that counts the current run is enough.
- **$k = 2$.** "Fruit into baskets" (LeetCode 904), and the longest subarray that alternates between two values.
- **All values distinct.** A limit on the count of each value instead of on the number of values: the longest subarray with no repeated value. For strings this is the [longest substring without repeating characters](/longest-substring-without-repeating-characters/). It is not the case $k = 1$ of this problem.
- **Exactly $k$ distinct values.** If the array has at least $k$ distinct values, the longest subarray with exactly $k$ has the same length as the longest with at most $k$, because a longest window with fewer than $k$ that is not the whole array could grow.
- **Counting.** The number of subarrays with at most $k$ distinct values is $\sum_{j} (j - L(j))$, where $L(j)$ is the smallest allowed start for the end $j$. The number with exactly $k$ is the count for at most $k$ minus the count for at most $k - 1$ (LeetCode 992).
- **Queries.** For many ranges of a fixed array, the number of distinct values in each range is the [range distinct count query](/range-distinct-count-query/). On a stream with a fixed window, it is the [sliding window distinct count](/sliding-window-distinct-count/).

## Examples

**Two baskets.** $A = [1, 2, 3, 2, 2]$ and $k = 2$. The answer is $4$, from $[2, 3, 2, 2] = A[1..5)$. The whole array has three distinct values.

**A first window.** $A = [1, 2, 1, 2, 3, 3, 4, 1]$ and $k = 2$. The answer is $4$, from $[1, 2, 1, 2] = A[0..4)$. The windows $[2, 3, 3]$ and $[3, 3, 4]$ also have two values but are shorter.

**Large values.** $A = [10^9, -5, 10^9, 3, -5, -5, 3]$ and $k = 2$. The answer is $4$, from $[3, -5, -5, 3] = A[3..7)$. The values are too large for a direct table, so the counts go in a hash table, or the values are first mapped to $0, 1, 2$ by coordinate compression.

**Counts.** For $A = [1, 2, 1, 2, 3]$ and $k = 2$, there are $12$ subarrays with at most two distinct values and $5$ with at most one, so $7$ subarrays have exactly two.

**Edge cases.** $k = 0$ gives $0$. If $k$ is at least the number of distinct values in $A$, the answer is $n$.

## Known algorithms

| method | time | extra space | notes |
|---|---|---|---|
| all pairs, with a set per start | $\Theta(n^2)$ | $O(k)$ | for each start, extend until $k + 1$ values |
| [distinct count two pointers](/distinct-count-two-pointers/) with a hash table | $O(n)$ expected | $O(k)$ | the standard solution |
| two pointers after [coordinate compression](/coordinate-compression/) | $O(n \log n)$ worst case | $O(n)$ | sort once, then a plain count array |
| two pointers with a direct count array | $O(n + U)$ worst case | $O(U)$ | values in $\{0, \dots, U - 1\}$ |
| [binary search](/binary-search/) on the length with a fixed window | $O(n \log n)$ expected | $O(k)$ | test each length with one window pass |

The two pointers method keeps the counts of the values in the window and the number $d$ of values with a positive count. The right end adds one value per step. While $d > k$, the left end removes values. Each index enters and leaves the window once, so there are at most $2n$ count updates.

## Bounds

**Linear time with hashing.** Each item must be read, so $\Omega(n)$ time is needed. The two pointers method meets it in expectation with a hash table, and in the worst case when the values are small integers.

**Comparisons only.** If the values can only be compared, and not hashed, the problem with $k = n - 1$ answers whether all values are distinct: the answer is $n$ exactly when some value repeats. So it is at least as hard as [element distinctness](/element-distinctness/), which needs $\Omega(n \log n)$ comparisons in the algebraic decision tree model. Sorting for coordinate compression meets this bound.

## Reductions

- **To the monotone window template.** The property is closed under sub-intervals, so for each end the best start is found by a left pointer that only moves right.
- **Exactly $k$ by subtraction.** Counts for exactly $k$ come from two runs of the at-most version, with $k$ and $k - 1$.
- **From element distinctness.** With $k = n - 1$, as in the bounds.
- **From strings.** The [string version](/longest-substring-with-k-distinct/) is the case where the values are characters.

## Applications

- **Caching.** The longest stretch of a request sequence that touches at most $k$ distinct pages is the longest stretch that a cache of $k$ pages serves after each page is loaded once.
- **Sensor and log data.** The longest period in which a signal takes at most $k$ distinct levels, or a log shows at most $k$ distinct event types.
- **Teaching.** It is the standard example of a sliding window whose state is a count table with a counter of distinct keys.

## References
