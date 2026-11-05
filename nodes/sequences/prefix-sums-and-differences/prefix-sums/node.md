---
tag: 37H2XG
kind: technique
slug: prefix-sums
name: Prefix sums
aliases:
- cumulative sums
- running sums
- summed-area table (1D)
area: sequences/prefix-sums-and-differences
level: intro
summary: Precompute P[i] = a[1]+...+a[i] in O(n) so any range sum a[l..r] is P[r]-P[l-1] in O(1).
prereqs: [array, asymptotic-notation]
see_also: [range-sum-query, difference-array, two-dimensional-prefix-sums, telescoping-sum, prefix-sum-hash-counting, fenwick-tree, all-prefix-sums, invertible-operation]
sources:
  - book: isbn:9780201657883
    title: Jon Bentley, Programming Pearls, second edition
    locator: Column 8, Algorithm Design Techniques, Section 8.2 (the cumulative array cumarr for the quadratic maximum subvector algorithm)
  - url: https://cses.fi/book/book.pdf
    title: Antti Laaksonen, Competitive Programmer's Handbook
    locator: Chapter 9, Range queries, Section 9.1 Static array queries (sum queries with a prefix sum array, and the two-dimensional form)
  - url: https://www.cs.cmu.edu/~guyb/papers/Ble93.pdf
    title: Guy E. Blelloch, Prefix Sums and Their Applications, Chapter 1 of John H. Reif (editor), Synthesis of Parallel Algorithms, Morgan Kaufmann, 1993
    locator: Section 1.1, Introduction (the all-prefix-sums operation for a binary associative operator, and its list of uses)
---

Prefix sums turn an [array](/array/) $a[0 \ldots n-1]$ into the array $P[0 \ldots n]$ with $P[i] = a[0] + \cdots + a[i-1]$, so that the sum of any range $a[l \ldots r-1]$ is the single difference $P[r] - P[l]$. The table costs $n$ additions and $n + 1$ words to build, and each range sum then costs one subtraction, $O(1)$ time, instead of $\Theta(r - l)$. The method works for every associative operation that has an inverse, such as addition, addition modulo $m$ and XOR, and it is the base of a large family of techniques on [subarrays](/subarray/): range sums, counting with a hash table, [difference arrays](/difference-array/) and their two-dimensional forms.

## In plain words

Write down a running total as you walk along a list of numbers: after each number, note the total so far. The total of any stretch of the list is then one subtraction. Take the running total at the end of the stretch, and take away the running total just before its start. Everything before the stretch cancels out.

So one walk over the list, with one addition per item, lets you answer any number of questions of the form "what is the total from here to there" with one subtraction each. The same trick works for any operation that you can undo, such as exclusive or. It does not work for the maximum, because a maximum cannot be taken away.

## When it applies

- **Many range queries on fixed data.** The array does not change, and the questions ask for the sum (or another invertible aggregate) of a contiguous range. This is the [range sum query](/range-sum-query/) problem.
- **A condition on a subarray sum.** A subarray sum $a[l] + \cdots + a[r-1]$ is $P[r] - P[l]$, so a question about subarrays becomes a question about *pairs* of prefix sums. "Sum equals $k$" becomes "$P[l] = P[r] - k$", which a hash table answers ([prefix sum hash counting](/prefix-sum-hash-counting/)). "Largest sum" becomes "largest $P[r]$ minus the smallest earlier $P[l]$", which is [Kadane's algorithm](/kadane-algorithm/).
- **Counts of a property in a range.** Map each item to 1 if it has the property and to 0 if not. The prefix sums of this 0/1 array count the items with the property in any range.
- **The operation has an inverse.** The operation $\oplus$ must be associative and each element must have an inverse, so that $P[l]^{-1} \oplus P[r]$ is the range aggregate. See [invertible operation](/invertible-operation/). For min, max and gcd, which have no inverse, use a [sparse table](/sparse-table/) or another [range minimum query](/range-minimum-query/) structure.
- **Signals that it does not apply.** The array changes between queries (use a [Fenwick tree](/fenwick-tree/)), or the query is not on a contiguous range.

## The template

The arrays are 0-based and the ranges are half-open: the range $[l, r)$ holds $a[l], \ldots, a[r-1]$.

```pseudo id=main
BUILD-PREFIX(a[0 .. n − 1])
L1  P[0] ← IDENTITY                       ▷ hole: 0 for +, 0 for XOR
L2  for i ← 1 to n do
L3      P[i] ← P[i − 1] ⊕ a[i − 1]        ▷ hole: the operation ⊕
L4  return P

RANGE(P, l, r)                            ▷ aggregate of a[l .. r − 1], for 0 ≤ l ≤ r ≤ n
L5  return INVERSE(P[l]) ⊕ P[r]           ▷ hole: P[r] − P[l] for +
```

For addition the holes are $0$, $+$ and $P[r] - P[l]$. For XOR they are $0$, $\oplus$ and $P[l] \oplus P[r]$, since each element is its own inverse.

**Why it is correct.** By induction on $i$, line L3 keeps $P[i] = a[0] \oplus \cdots \oplus a[i-1]$, with $P[0]$ the empty aggregate. For $l \le r$, associativity splits $P[r]$ as $P[l] \oplus (a[l] \oplus \cdots \oplus a[r-1])$. Apply $P[l]^{-1}$ on the left of both sides to get line L5. For addition, $P[r] - P[l] = \sum_{i=l}^{r-1} (P[i+1] - P[i]) = \sum_{i=l}^{r-1} a[i]$, which is a [telescoping sum](/telescoping-sum/). The operation need not be commutative, but then the inverse must go on the left, as in line L5.

**Cost.** BUILD-PREFIX does $n$ operations and stores $n + 1$ values: $\Theta(n)$ time and $\Theta(n)$ space. RANGE does one inverse and one operation: $O(1)$ time. So $q$ queries cost $\Theta(n + q)$ in total, against $\Theta(nq)$ in the worst case for summing each range directly. On a [word RAM](/word-ram/) with $w$-bit words and items of absolute value at most $M$, every prefix sum has absolute value at most $nM$, so it fits in a word when $nM < 2^{w-1}$.

**A worked example.** For $a = [3, 1, 4, 1, 5, 9, 2, 6]$ the table is $P = [0, 3, 4, 8, 9, 14, 23, 25, 31]$. The sum of $a[2 \ldots 5] = 4 + 1 + 5 + 9$ is $P[6] - P[2] = 23 - 4 = 19$, and the sum of the whole array is $P[8] - P[0] = 31$.

## Classic examples

From simple to hard:

- **[Range sum query](/range-sum-query/).** The direct use: $O(n)$ build, $O(1)$ per query.
- **Counting letters in a range.** For the string `abracadabra` and the letter `a`, the prefix counts are $[0, 1, 1, 1, 2, 2, 3, 3, 4, 4, 4, 5]$. The substring of positions 3 to 7, `acada`, holds $C[8] - C[3] = 4 - 1 = 3$ letters `a`. One table per letter of an alphabet of size $\sigma$ costs $\Theta(\sigma n)$ space.
- **[Maximum sum subarray of fixed length](/maximum-sum-subarray-of-fixed-length/).** The window sums are $P[i + k] - P[i]$.
- **[Subarray sum equals k](/subarray-sum-equals-k/).** Count pairs $l < r$ with $P[r] - P[l] = k$ by a hash table of the earlier prefix sums, in expected $O(n)$ time.
- **[Longest zero-sum subarray](/longest-zero-sum-subarray/).** Find the pair of equal prefix sums that are farthest apart.
- **[Maximum subarray problem](/maximum-subarray-problem/).** The answer is $\max_{l < r} (P[r] - P[l])$, the largest rise of the sequence $P$.
- **[Shortest subarray with sum at least K](/shortest-subarray-sum-at-least-k/).** With negative items, scan the prefix sums with a [monotonic deque](/monotonic-deque-prefix-sums/).
- **[Maximum XOR subarray](/maximum-xor-subarray/).** Prefix XORs turn the question into the largest XOR of two prefix values, which a trie answers.
- **[Two-dimensional prefix sums](/two-dimensional-prefix-sums/).** The same table for rectangles of a grid, with four terms per query.

## Variations

- **Prefix XOR, prefix sums modulo $m$.** Any group works. Modulo $m$, the range sum is $(P[r] - P[l]) \bmod m$, and "the range sum is divisible by $m$" means $P[r] \equiv P[l] \pmod m$.
- **Prefix products.** Products of nonzero numbers modulo a prime have inverses. With a zero item, the inverse fails; keep a separate prefix count of zeros.
- **Suffix sums.** $S[i] = a[i] + \cdots + a[n-1]$ is the mirror image, used when the scan runs from the right.
- **The inverse: differences.** The [difference array](/difference-array/) $d[i] = a[i] - a[i-1]$ undoes the prefix sum. Prefix sums and differences are the discrete forms of integration and differentiation; see the [discrete antiderivative](/discrete-antiderivative/).
- **Higher dimensions.** In $d$ dimensions, a box sum is a signed sum of $2^d$ table entries, by the [inclusion-exclusion principle](/inclusion-exclusion-principle/). See [two-dimensional prefix sums](/two-dimensional-prefix-sums/).
- **Prefix sums of prefix sums.** With $Q[i] = P[0] + \cdots + P[i-1]$, the sum of $P[l+1 \ldots r]$ and similar weighted range sums such as $\sum_{i} (i - l + 1)\,a[i]$ also come out in $O(1)$.
- **Updates.** When point updates mix with queries, the table needs $\Theta(n)$ time per update. A [Fenwick tree](/fenwick-tree/) or a [segment tree](/segment-tree/) gives $O(\log n)$ for both; this is the [partial sums problem](/partial-sums-problem/).
- **In parallel.** The prefix sums of $n$ items take $O(n)$ work and $O(\log n)$ span with a [parallel scan](/all-prefix-sums/), such as the [Blelloch scan](/blelloch-scan/).

## Pitfalls

- **Off by one.** With $P$ of length $n + 1$ and $P[0] = 0$, the sum of $a[l \ldots r]$ inclusive is $P[r + 1] - P[l]$. A table of length $n$ with $P[i] = a[0] + \cdots + a[i]$ needs a special case for $l = 0$. Choose one convention and use it everywhere.
- **Overflow.** The prefix sums grow up to $n$ times the largest item. Thirty-two-bit sums of $10^5$ items of size $10^9$ overflow; use 64-bit integers. In a language with wrapping integers, a range sum can still be correct modulo $2^w$ when the true range sum fits, since subtraction modulo $2^w$ undoes addition modulo $2^w$, but a comparison of two prefix sums is then wrong.
- **Floating-point cancellation.** For floats, $P[r] - P[l]$ subtracts two large, close numbers, and the error of the result is about the machine epsilon times $|P[r]|$, not times the range sum. Use [Kahan summation](/kahan-summation/) to build the table, keep integers when the data allows, or use a tree of partial sums.
- **Using it for min or max.** $\max(a[l \ldots r-1])$ cannot be found from prefix maxima, because the maximum has no inverse.
- **Stale tables.** After a change to $a$, every later prefix sum is wrong. Rebuild, or switch to a dynamic structure.

## Exercises

1. Given an array of $n$ integers and $q$ queries $(l, r)$, return the number of even items in each range in $O(n + q)$ time.
2. Show that the number of subarrays whose sum is divisible by $m$ is $\sum_{c=0}^{m-1} \binom{f_c}{2}$, where $f_c$ is the number of prefix sums $P[0], \ldots, P[n]$ that are congruent to $c$ modulo $m$.
3. Given $a$, compute $\sum_{0 \le l < r \le n} (P[r] - P[l])$, the sum of all subarray sums, in $O(n)$ time, and check the formula $\sum_{i} (i + 1)(n - i)\,a[i]$.
4. Prove that the operation in BUILD-PREFIX may be non-commutative, and find the correct order of the two factors in RANGE.
5. Give an array of 32-bit integers, each of absolute value at most $10^9$, for which a 32-bit prefix sum overflows but every range sum that a query asks for fits in 32 bits. Explain why wrapping arithmetic still returns the right range sums.

## References
