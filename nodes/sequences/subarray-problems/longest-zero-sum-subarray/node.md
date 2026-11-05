---
tag: 7Y1SQF
kind: problem
slug: longest-zero-sum-subarray
name: Longest zero-sum subarray
aliases:
- longest subarray with sum zero
area: sequences/subarray-problems
level: intro
summary: Find the longest subarray whose elements sum to zero, using first occurrences of prefix sums.
prereqs: [subarray, prefix-sums, hash-table]
see_also: [subarray-sum-equals-k, prefix-sum-hash-counting, maximum-subarray-problem, element-distinctness, coordinate-compression, range-sum-query, minimum-size-subarray-sum, longest-subarray-with-at-most-k-distinct]
sources:
  - url: https://cses.fi/book/book.pdf
    title: Antti Laaksonen, Competitive Programmer's Handbook
    locator: Chapter 9, Range queries, Section 9.1 Static array queries (a subarray sum as a difference of two prefix sums)
  - url: https://leetcode.com/problems/contiguous-array/
    title: LeetCode, problem 525, Contiguous Array
    locator: problem statement (the longest subarray with equally many 0s and 1s)
  - url: https://leetcode.com/problems/maximum-size-subarray-sum-equals-k/
    title: LeetCode, problem 325, Maximum Size Subarray Sum Equals k
    locator: problem statement (the longest subarray with a given sum)
---

The longest zero-sum subarray problem asks, for an array of integers that may be negative, for the longest [subarray](/subarray/) whose items add up to $0$. With [prefix sums](/prefix-sums/) $P$, a subarray $A[i..j)$ has sum $0$ exactly when $P_i = P_j$, so the problem is to find two equal prefix sums that are as far apart as possible. One pass that stores the first index of each prefix sum in a [hash table](/hash-table/) solves it in $O(n)$ expected time. The same pass, with a shift by the target, finds the longest subarray with any given sum.

## In plain words

Keep a running total as you walk along the list. If the running total at one point is the same as at an earlier point, then the numbers in between add up to nothing: whatever they added, they also took away.

So the question becomes: which running total comes back after the longest gap? Write down the first place where each running total appears. At each new point, look up the current total. If it was seen before, the stretch from its first place to here sums to zero. The first place gives the longest such stretch for this end, so it is the only one worth keeping.

## Definition

**Input.** An array $A[0..n-1]$ of integers, or of elements of any abelian group in which equality can be tested and hashed.

**Output.** The largest length $j - i$ over $0 \le i \le j \le n$ with $A[i] + \dots + A[j-1] = 0$, and in the search version a pair $(i, j)$ that reaches it. The empty subarray has sum $0$, so the answer is at least $0$; an answer of $0$ means no non-empty zero-sum subarray exists.

**Prefix form.** Let $P_0 = 0$ and $P_j = A[0] + \dots + A[j-1]$. Then the sum of $A[i..j)$ is $P_j - P_i$, and the problem is

$$\max \{\, j - i : 0 \le i \le j \le n,\ P_i = P_j \,\}.$$

For each value $v$ that occurs among $P_0, \dots, P_n$, the best pair uses its first and its last occurrence. So the answer is the largest gap between the first and the last index of one prefix value.

## Variants

- **Target sum $t$.** The longest subarray with sum $t$ needs $P_j - P_i = t$, so for each $j$ look up the first index of $P_j - t$ (LeetCode 325).
- **Equal numbers of two symbols.** Replace $0$ by $-1$ and keep $1$; a subarray has as many $0$s as $1$s exactly when its new sum is $0$ (LeetCode 525). With $c$ symbols, track the vector of count differences instead of one number.
- **Sum divisible by $m$.** Use $P_j \bmod m$ in place of $P_j$; the longest subarray with sum divisible by $m$ is the largest gap between equal residues.
- **Existence.** Is there any non-empty zero-sum subarray? Exactly when two prefix sums are equal, which is a question of [element distinctness](/element-distinctness/) on $P_0, \dots, P_n$.
- **Counting.** The number of zero-sum subarrays is $\sum_v \binom{c_v}{2}$, where $c_v$ is the number of indices with $P_i = v$. Counting for a general target is the [subarray sum equals k](/subarray-sum-equals-k/) problem, solved by [prefix sum hash counting](/prefix-sum-hash-counting/).
- **Shortest.** For the shortest non-empty zero-sum subarray, keep the *last* index of each prefix value instead of the first.
- **Positive items.** If all items are positive, no non-empty subarray has sum $0$, and for a positive target the [sliding window](/sliding-window-positive-sum/) needs only $O(1)$ extra space.

## Examples

**A standard instance.** $A = [15, -2, 2, -8, 1, 7, 10, 23]$. The prefix sums are

$$P = [0, 15, 13, 15, 7, 8, 15, 25, 48].$$

The value $15$ occurs at the indices $1$, $3$ and $6$. Its first and last occurrences give the subarray $A[1..6) = [-2, 2, -8, 1, 7]$ of length $5$, which is the answer. The pair $(1, 3)$ gives the shorter zero-sum subarray $[-2, 2]$.

**Equal zeros and ones.** For $B = [0, 1, 0, 0, 1, 1, 0]$, map $0 \mapsto -1$. The longest zero-sum subarray of $[-1, 1, -1, -1, 1, 1, -1]$ has length $6$, from $B[0..6) = [0, 1, 0, 0, 1, 1]$ with three of each.

**A target.** For $A = [1, -1, 5, -2, 3]$ and $t = 3$, the longest subarray with sum $3$ is $A[0..4) = [1, -1, 5, -2]$ of length $4$.

**No answer.** For $A = [1, 2, 3]$, the prefix sums $0, 1, 3, 6$ are distinct, so the answer is $0$.

## Known algorithms

| method | time | extra space | model |
|---|---|---|---|
| all pairs with running sums | $\Theta(n^2)$ | $O(1)$ | any |
| first occurrence of each prefix sum in a hash table | $O(n)$ expected | $O(n)$ | hashing |
| sort the pairs $(P_i, i)$, then scan each group of equal values | $O(n \log n)$ | $O(n)$ | comparisons |
| direct table of first occurrences | $O(n + R)$ | $O(R)$ | $P$ in a range of $R$ values |

**The hash pass.** Set $\mathit{first}[0] = 0$ and $\mathit{best} = 0$. For $j = 1, \dots, n$, compute $P_j$. If $P_j$ is in the table, set $\mathit{best} \leftarrow \max(\mathit{best}, j - \mathit{first}[P_j])$; otherwise store $\mathit{first}[P_j] = j$. Never overwrite a stored index. Each end $j$ is paired with the smallest $i$ that has $P_i = P_j$, which gives the longest zero-sum subarray ending at $j$, so the largest of these is the answer.

**The direct table.** If $|A[k]| \le M$ for all $k$, then every $P_j$ lies in $[-nM, nM]$, and an array of $2nM + 1$ entries replaces the hash table. For the $0$ and $1$ variant, $M = 1$ and the table has $2n + 1$ entries, so the worst-case time is $O(n)$ with no hashing.

## Bounds

**Linear expected time is optimal.** Every item must be read: changing an unread item changes some prefix sums and can create or destroy the answer.

**Comparison and algebraic models.** Deciding whether a non-empty zero-sum subarray exists is as hard as element distinctness. Given numbers $x_1, \dots, x_n$, shift them so that none is $0$, and set $A[0] = x_1$ and $A[k] = x_{k+1} - x_k$. Then the prefix sums are $0, x_1, \dots, x_n$, and a zero-sum subarray exists exactly when two of the $x$ are equal. So in the algebraic decision tree model the problem needs $\Omega(n \log n)$ time, and the sorting method is optimal there. The linear bound needs hashing or a direct table.

## Reductions

- **To equal prefix sums.** As in the definition, a zero-sum subarray is a pair of equal prefix sums, and the longest one is the widest such pair.
- **From element distinctness,** as in the bounds.
- **Target sum to zero sum.** The longest subarray with sum $t$ is the widest pair with $P_j - P_i = t$, which the same pass finds by looking up $P_j - t$.
- **Balanced symbols to zero sum.** Map the two symbols to $+1$ and $-1$.

## Applications

- **Balanced segments.** The longest stretch of a binary sequence with equally many of two outcomes, such as wins and losses, or the two bases of a DNA strand in a GC-skew analysis.
- **Ledgers.** The longest period after which an account returns to the same balance.
- **Building block.** First-occurrence tables of prefix sums appear in many array problems, for example the longest subarray with sum divisible by $m$ and the longest subarray in which two letters occur equally often.

## References
