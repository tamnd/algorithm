---
tag: 0FYNC4
kind: problem
slug: first-and-last-occurrence
name: First and last occurrence of a key
aliases:
- key range in a sorted array
area: searching/sequential-and-binary-search
level: intro
summary: Find the first and last index of a key that occurs repeatedly in a sorted array, using two binary searches.
model: comparison-model
complexity:
  vars: {n: the number of items in the array}
  time: {worst: Θ(log n)}
prereqs: [lower-and-upper-bound-search]
see_also: [lower-bound-query, upper-bound-query, binary-search, search-in-sorted-array, exponential-search, linear-search]
sources:
  - book: isbn:9780201657883
    title: Jon Bentley, Programming Pearls, second edition
    locator: Column 9, Section 9.3 (a binary search for the first occurrence of a value)
  - book: isbn:9780321573513
    title: Robert Sedgewick and Kevin Wayne, Algorithms, fourth edition
    locator: Section 3.1, binary search in an ordered array (rank and range queries)
  - url: https://en.cppreference.com/w/cpp/algorithm/equal_range
    title: cppreference.com, std::equal_range
---

The first and last occurrence problem asks, for a sorted array $A[0 \ldots n-1]$ and a key $x$, for the smallest and the largest index $i$ with $A[i] = x$, or for the answer that $x$ does not occur. Because the copies of $x$ in a sorted array form one block, the first index is the [lower bound](/lower-bound-query/) $\ell$ and the last index is the [upper bound](/upper-bound-query/) $u$ minus one. Two [boundary searches](/lower-and-upper-bound-search/) answer it with at most $2\lceil \lg(n+1) \rceil$ comparisons, and no comparison algorithm can use fewer than about $2 \lg n - 1$. The block also gives the number of copies, $u - \ell$, in $O(\log n)$ time, however many copies there are.

## In plain words

A sorted list of exam scores has many students with the same score. You want the first and the last place in the list where a score appears, for example to count how many students got exactly 70, or to print all of them.

A plain binary search finds some copy of the score, but you do not know which one. Walking left and right from it to the ends of the block can take a long time when the block is big. Instead you do two searches that never stop early: one for the place where the block starts, and one for the place just after it ends. Each takes a few steps, even for a block of a million copies.

## Definition

**Input.** An array $A[0 \ldots n-1]$, $n \ge 0$, from a [total order](/total-order/), with $A[0] \le \cdots \le A[n-1]$, and a key $x$.

**Output.** The pair

$$ (f, l) = \bigl(\min\{\, i : A[i] = x \,\},\ \max\{\, i : A[i] = x \,\}\bigr) $$

when $x$ occurs in $A$, and NIL otherwise. Many libraries return $(-1, -1)$ for NIL.

**The block.** Let $\ell = |\{i : A[i] < x\}|$ and $u = |\{i : A[i] \le x\}|$ be the lower and upper bounds. Since $A$ is sorted, $A[i] < x$ exactly for $i < \ell$ and $A[i] \le x$ exactly for $i < u$, so $\{i : A[i] = x\} = \{\ell, \ldots, u - 1\}$. Hence $x$ occurs if and only if $\ell < u$, and then

$$ f = \ell, \qquad l = u - 1, \qquad \text{the number of copies is } u - \ell. $$

## Variants

- **Count only.** Return $u - \ell$. This is 0 when $x$ is absent, so it needs no special case.
- **Equal range.** Return the half-open range $[\ell, u)$, as `std::equal_range` does in C++. An empty range means that $x$ is absent, and its position is where $x$ would go.
- **Range of keys.** Return the indices of all items in $[a, b]$: the block is $[\ell(a), u(b))$.
- **Unsorted array.** The first occurrence needs a scan from the left and the last a scan from the right, $\Theta(n)$ comparisons in the worst case; see [search in an unordered array](/search-in-unordered-array/).

## Examples

The array is $A = [2, 4, 4, 4, 4, 7, 9, 9, 12]$, with $n = 9$.

| $x$ | 4 | 9 | 12 | 2 | 5 | 1 | 13 |
|---|---|---|---|---|---|---|---|
| $\ell$ | 1 | 6 | 8 | 0 | 5 | 0 | 9 |
| $u$ | 5 | 8 | 9 | 1 | 5 | 0 | 9 |
| $(f, l)$ | (1, 4) | (6, 7) | (8, 8) | (0, 0) | NIL | NIL | NIL |
| copies | 4 | 2 | 1 | 1 | 0 | 0 | 0 |

For $x = 12$ the last copy is the last item, so $u = n$. For $x = 5$ the key is absent and $\ell = u = 5$, the index of the 7.

## Known algorithms

- **Two boundary searches.** Compute $\ell$ with the lower bound loop and $u$ with the upper bound loop of [lower and upper bound search](/lower-and-upper-bound-search/). Each makes at most $\lceil \lg(n+1) \rceil$ two-way comparisons, so the total is at most $2\lceil \lg(n+1) \rceil$, and the space is $\Theta(1)$. The second search can start at $lo = \ell$, since $u \ge \ell$, and it can stop at once when $\ell = n$ or $A[\ell] \ne x$.
- **Lower bound, then gallop.** Find $\ell$, then find $u$ by [exponential search](/exponential-search/) from $\ell$. This costs $\lceil \lg(n+1) \rceil + O(\log k)$ for $k$ copies, which is better when the blocks are short.
- **Find one copy, then walk.** A [binary search](/binary-search/) finds some copy, then two scans walk to the ends of the block. This costs $O(\log n + k)$, which is $\Theta(n)$ when most items are copies of $x$. It is correct, but it is the slow method.

## Bounds

**Upper bound.** $2\lceil \lg(n+1) \rceil$ two-way comparisons, by two boundary searches.

**Lower bound.** Each deterministic algorithm that uses two-way comparisons makes at least $\lceil \lg(n(n+1)/2 + 1) \rceil$ comparisons on some input.

*Proof.* For each pair $0 \le f \le l \le n - 1$ there is an input with that answer: put copies of $x$ at the indices $f$ to $l$, distinct values less than $x$ before them, and distinct values greater than $x$ after them. One more input has $x$ absent. So there are $n(n+1)/2 + 1$ inputs with different answers. For a fixed $n$ the algorithm is a decision tree with two answers at each comparison, and these inputs must reach leaves with different outputs. A binary tree of height $h$ has at most $2^h$ leaves, so $2^h \ge n(n+1)/2 + 1$. $\blacksquare$

Since $\lg(n(n+1)/2) \ge 2\lg n - 1$, the lower bound is about $2 \lg n - 1$, and two searches are optimal up to a small additive term.

| $n$ | 1 | 8 | 1000 | $10^6$ |
|---|---|---|---|---|
| lower bound $\lceil \lg(n(n+1)/2 + 1) \rceil$ | 1 | 6 | 19 | 39 |
| two searches, $2\lceil \lg(n+1) \rceil$ | 2 | 8 | 20 | 40 |

## Reductions

- **It reduces to two lower bound queries** for integer keys: $f = \ell(A, x)$ and $l = \ell(A, x+1) - 1$. For other keys, use one lower and one upper bound query.
- **The [lower bound query](/lower-bound-query/) reduces to it** only for keys that are present. For an absent key, the problem says only NIL, so the equal-range form, which also returns the position, is the more useful output.
- **[Search in a sorted array](/search-in-sorted-array/) reduces to it.** Return $f$ when the answer is not NIL.

## Applications

- Count the copies of a value in a sorted list, for example the number of log lines with a given minute, in $O(\log n)$ time.
- Report all records with a given key from a table sorted by that key, such as all rows of a sorted file with the same customer number.
- Find the range of suffixes that start with a pattern in a [suffix array](/suffix-array/), as in [suffix array search](/suffix-array-search/): the suffixes with a given prefix form one block of the sorted order.
- Group the items of a sorted array into runs of equal keys, jumping from one run to the next with an upper bound query.

## References
