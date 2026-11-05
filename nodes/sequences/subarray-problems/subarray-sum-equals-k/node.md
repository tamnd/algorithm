---
tag: 9GWMS6
kind: problem
slug: subarray-sum-equals-k
name: Subarray sum equals k
aliases:
- count subarrays with sum k
area: sequences/subarray-problems
level: core
summary: Count the subarrays whose elements sum to a given target k, where elements may be negative.
prereqs: [subarray, prefix-sums, hash-table]
see_also: [prefix-sum-hash-counting, longest-zero-sum-subarray, element-distinctness-lower-bound, sliding-window-positive-sum, fenwick-tree, counting-inversions, maximum-xor-subarray, range-sum-query]
sources:
  - url: https://leetcode.com/problems/subarray-sum-equals-k/
    title: LeetCode, problem 560, Subarray Sum Equals K
    locator: problem statement (count the subarrays with sum k, items may be negative)
  - url: https://leetcode.com/problems/subarray-sums-divisible-by-k/
    title: LeetCode, problem 974, Subarray Sums Divisible by K
    locator: problem statement
  - url: https://leetcode.com/problems/count-of-range-sum/
    title: LeetCode, problem 327, Count of Range Sum
    locator: problem statement (count the subarrays with sum in a range)
  - url: https://leetcode.com/problems/number-of-submatrices-that-sum-to-target/
    title: LeetCode, problem 1074, Number of Submatrices That Sum to Target
    locator: problem statement
  - url: https://cses.fi/book/book.pdf
    title: Antti Laaksonen, Competitive Programmer's Handbook
    locator: Chapter 9, Range queries, Section 9.1 Static array queries (a subarray sum as a difference of two prefix sums)
---

The subarray sum equals $k$ problem asks how many [subarrays](/subarray/) of an array have sum exactly $k$. The items may be negative, so a window cannot be grown and shrunk. With [prefix sums](/prefix-sums/) $P$, the subarray $A[i..j-1]$ has sum $P_j - P_i$, so the question is how many pairs $i < j$ have $P_i = P_j - k$. One pass that keeps a [hash table](/hash-table/) of how often each prefix sum has occurred answers it in $O(n)$ expected time, the [prefix sum hash counting](/prefix-sum-hash-counting/) algorithm. Deciding whether a zero-sum subarray exists is as hard as [element distinctness](/element-distinctness/), so without hashing $\Theta(n \log n)$ is the right bound for comparisons.

## In plain words

You have a list of numbers, some of them negative, and a target. You want to know how many stretches of neighbors add up to exactly the target.

Walk along the list and keep the running total. A stretch that ends here adds up to the target exactly when the running total at its start was the current total minus the target. So the number of good stretches that end here is the number of earlier points where the running total had that value.

Keep a tally of how often each running total has appeared. At each step, look up one value in the tally, add the count to the answer, and then record the current total.

## Definition

**Input.** An array $A[0..n-1]$ of integers or reals, which may be negative, and a target $k$.

**Output.** The number of pairs $(i, j)$ with $0 \le i \le j \le n - 1$ and $A[i] + \dots + A[j] = k$.

**With prefix sums.** Let $P_0 = 0$ and $P_m = A[0] + \dots + A[m-1]$ for $1 \le m \le n$. The subarray $A[i..j]$ has sum $P_{j+1} - P_i$. So the answer is
$$\#\{(a, b) : 0 \le a < b \le n,\ P_b - P_a = k\}.$$
For $k = 0$ this is the number of pairs of equal prefix sums: if the value $v$ occurs $c_v$ times among $P_0, \dots, P_n$, the answer is $\sum_v \binom{c_v}{2}$.

## Variants

- **Decide or find.** Report one subarray with sum $k$, or say there is none. The same pass stops at the first hit.
- **Longest or shortest.** The [longest zero-sum subarray](/longest-zero-sum-subarray/) keeps the first index of each prefix sum instead of a count; the shortest keeps the last.
- **Divisible by $k$.** Count the subarrays whose sum is a multiple of $k$: the prefix sums are compared modulo $k$, with a table of $k$ counters (LeetCode 974).
- **Sum in a range.** Count the subarrays with $L \le$ sum $\le U$ (LeetCode 327). Equality is no longer a hash lookup. Sort or compress the prefix sums and count with a [Fenwick tree](/fenwick-tree/) or with a merge step as in [counting inversions](/counting-inversions/), in $O(n \log n)$ time.
- **Non-negative items.** Then the prefix sums do not decrease, and the windows with sum $k$ can be counted with two pointers in $O(n)$ time and $O(1)$ space: for integers, the count of windows with sum at most $k$ minus the count with sum at most $k - 1$, each found by the [positive-sum sliding window](/sliding-window-positive-sum/).
- **XOR equals $k$.** With XOR in place of addition, $P_a \oplus P_b = k$ gives the same hash method; see the [maximum XOR subarray](/maximum-xor-subarray/) for the related optimization.
- **Two dimensions.** Count the submatrices with sum $k$ (LeetCode 1074): for each pair of rows, sum the columns between them and run the one-dimensional count, in $O(r^2 c)$ expected time for $r \le c$.

## Examples

**Small.** For $A = [1, 1, 1]$ and $k = 2$ the answer is $2$: $A[0..1]$ and $A[1..2]$.

**Negative items.** For $A = [3, 4, 7, 2, -3, 1, 4, 2]$ and $k = 7$, the prefix sums are $0, 3, 7, 14, 16, 13, 14, 18, 20$. The pairs with difference $7$ are $(0, 7)$, $(7, 14)$ twice and $(13, 20)$, so the answer is $4$: the subarrays $[3, 4]$, $[7]$, $[7, 2, -3, 1]$ and $[1, 4, 2]$. The prefix sum $14$ occurs twice, which is why $[7]$ and $[7, 2, -3, 1]$ both count.

**All zeros.** For $n$ zeros and $k = 0$ every one of the $n(n+1)/2$ subarrays counts, so the answer itself can be quadratic in $n$. A method that lists the subarrays one by one is too slow; the count must be added up in groups.

**No answer.** For $A = [1, 2, 3]$ and $k = 7$ the answer is $0$.

## Known algorithms

| method | time | extra space | items |
|---|---|---|---|
| all pairs with running sums | $\Theta(n^2)$ | $O(1)$ | any |
| [prefix sums and a hash table](/prefix-sum-hash-counting/) | $O(n)$ expected | $O(n)$ | any |
| sort the pairs $(P_a, a)$, then count by groups | $O(n \log n)$ | $O(n)$ | any, $k = 0$ |
| compressed prefix sums and a [Fenwick tree](/fenwick-tree/) or a [balanced search tree](/balanced-binary-search-tree/) | $O(n \log n)$ | $O(n)$ | any |
| two pointers | $O(n)$ | $O(1)$ | non-negative |

**Hash counting.** Scan $b = 0, 1, \dots, n$. Before recording $P_b$, add the count of $P_b - k$ seen so far to the answer. The order matters: it makes sure that only pairs $a < b$ are counted, which is what allows $k = 0$.

**Comparisons only.** Process the prefix sums in index order and keep them in a search tree, or compress them and use a Fenwick tree. For each $b$, look up how many earlier $P_a$ equal $P_b - k$. Each step costs $O(\log n)$, and the time is $O(n \log n)$ in the worst case with no hashing.

## Bounds

**Linear reading.** Every item must be read, since changing any one item changes some subarray sum, so $\Omega(n)$ time is needed.

**Comparison lower bound.** Deciding whether some subarray has sum $0$ needs $\Omega(n \log n)$ time in the algebraic decision tree model. The reduction is from element distinctness. Given reals $x_1, \dots, x_n$, let $m = \min_i x_i$ and $y_i = x_i - m + 1 \ge 1$, and set $A[0] = y_1$ and $A[i] = y_{i+1} - y_i$. The prefix sums are $0, y_1, \dots, y_n$, and $0$ differs from every $y_i$. So a zero-sum subarray exists exactly when two of the $x_i$ are equal. The [element distinctness lower bound](/element-distinctness-lower-bound/) gives $\Omega(n \log n)$, so the hash table, which is not an algebraic operation, is needed for linear time.

**Output size.** The count can be $\Theta(n^2)$, so it needs about $2 \log_2 n$ bits, which is still one word on the word RAM.

## Reductions

- **To pairs of prefix sums.** Counting subarrays with sum $k$ is counting pairs $a < b$ with $P_b - P_a = k$, as above.
- **From element distinctness.** As in the bounds, distinctness of $n$ numbers reduces to the existence of a zero-sum subarray in $O(n)$ time.
- **Longest to first occurrence.** The longest subarray with sum $k$ uses the same pairs, with the first index of each value in place of its count.
- **Two dimensions to one.** Summing the columns between two rows turns the submatrix count into one-dimensional counts, one per pair of rows.

## Applications

- **Balanced segments.** With $+1$ and $-1$ items, a zero-sum subarray is a segment with as many of each, for example as many $0$s as $1$s in a bit string, or as many opening as closing events.
- **Target totals in data.** Count the periods whose net change is exactly a given amount, such as days on which a balance returns to the same value.
- **Building block.** The hash pass appears inside problems on submatrices, on paths in trees, where the prefix sums run from the root, and on strings with given letter counts.

## References
