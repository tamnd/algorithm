---
tag: 6SRCHA
kind: problem
slug: search-in-sorted-array
name: Search in a sorted array
aliases: [sorted search, ordered search]
area: searching/sequential-and-binary-search
level: intro
summary: Given a sorted array and a key, find an index of the key, or report that the key is not in the array.
model: comparison-model
complexity:
  vars: {n: the number of items}
  time: {worst: Θ(log n)}
prereqs: [array, total-order, comparison-model]
see_also: [binary-search, lower-bound-query, upper-bound-query, search-in-unordered-array, search-lower-bound, exponential-search, interpolation-search, predecessor-problem]
sources:
  - book: isbn:9780201896855
    title: Donald E. Knuth, The Art of Computer Programming, Volume 3, second edition
    locator: Section 6.2.1, Searching an ordered table (Algorithm B, comparison trees, and the optimality of binary search)
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Exercise 2.3-6 (binary search)
  - book: isbn:9780321573513
    title: Robert Sedgewick and Kevin Wayne, Algorithms, fourth edition
    locator: Section 1.1 (binary search) and Section 3.1 (binary search in an ordered array, rank)
---

Search in a sorted array asks for an index of a key $x$ in an [array](/array/) whose items are in non-decreasing order, or for the answer that $x$ is not there. The order lets an algorithm skip most of the items: one comparison with an item tells on which side of it the key must be. [Binary search](/binary-search/) needs only $\lceil \lg(n+1) \rceil$ three-way comparisons in the worst case, and no algorithm in the [comparison model](/comparison-model/) needs fewer. The problem is a step of many other algorithms, such as a look-up in the index of a database or the insertion step of a sort.

## In plain words

You have a list of items in order, such as the words in a dictionary. You want to know if a word is in the list, and where. Because the list is in order, you do not need to look at each item. When you look at one word, you learn whether your word comes before it or after it, so you can forget the whole other side. A good method looks first at the middle, so each look throws away half of what is left. For a list of a million words, twenty looks are enough.

## Definition

**Input.** An array $A[0 \ldots n-1]$ of $n \ge 0$ items from a set with a [total order](/total-order/) $\le$, sorted so that $A[0] \le A[1] \le \cdots \le A[n-1]$, and a key $x$ from the same set.

**Output.** An index $i \in \{0, \ldots, n-1\}$ with $A[i] = x$, or NIL when no such index exists.

When $x$ occurs more than once, the indices of $x$ form a block $\{\ell, \ell+1, \ldots, u-1\}$, and each of them is a correct output. Here $\ell$ is the [lower bound](/lower-bound-query/) of $x$ and $u$ is the [upper bound](/upper-bound-query/):

$$ \ell = \min\{\, i : A[i] \ge x \,\}, \qquad u = \min\{\, i : A[i] > x \,\}, $$

with the convention that the minimum of an empty set is $n$. The key is present if and only if $\ell < u$, that is, $\ell < n$ and $A[\ell] = x$.

The cost is the number of comparisons between $x$ and items of $A$. A *three-way* comparison has the answers less, equal and greater. A *two-way* comparison answers one question such as "$x < A[i]$?".

## Variants

- **[Lower bound query](/lower-bound-query/).** Find $\ell$, the first index with $A[i] \ge x$. It is also the number of items less than $x$, and the place where $x$ can be inserted with the array still sorted.
- **[Upper bound query](/upper-bound-query/).** Find $u$, the first index with $A[i] > x$. The number of copies of $x$ is $u - \ell$.
- **[First and last occurrence](/first-and-last-occurrence/).** Find $\ell$ and $u - 1$ when $x$ is present.
- **Predecessor and successor.** Find the largest item less than $x$, which is $A[\ell - 1]$ when $\ell > 0$, or the smallest item greater than $x$, which is $A[u]$ when $u < n$. This is the [predecessor problem](/predecessor-problem/) on a static set.
- **[Unknown length](/unbounded-search/).** The array is very long, or its length is not known. The cost is measured in the position of the key.
- **Search with a known key distribution.** When the keys are numbers spread in a known way, the algorithm can guess the position from the value, as [interpolation search](/interpolation-search/) does.
- **Other sorted structures.** A [rotated sorted array](/rotated-sorted-array-search/), a [row- and column-sorted matrix](/sorted-matrix-search/), or a [unimodal](/unimodal-maximum/) sequence keep enough order for a search in sub-linear time.

## Examples

| $A$ | $x$ | correct outputs | $\ell$ | $u$ |
|---|---|---|---|---|
| 2 5 8 12 16 23 38 | 23 | 5 | 5 | 6 |
| 2 5 8 12 16 23 38 | 7 | NIL | 2 | 2 |
| 2 5 8 12 16 23 38 | 1 | NIL | 0 | 0 |
| 2 5 8 12 16 23 38 | 40 | NIL | 7 | 7 |
| 1 3 3 3 5 | 3 | 1, 2 or 3 | 1 | 4 |
| (empty) | 4 | NIL | 0 | 0 |

The second row shows that a failed search still has a useful result: $\ell = 2$ is the position where 7 goes, between 5 and 8.

## Known algorithms

- **[Binary search](/binary-search/).** Compare with the middle item and keep one half. At most $\lfloor \lg n \rfloor + 1 = \lceil \lg(n+1) \rceil$ three-way comparisons, $\Theta(\log n)$ time, $\Theta(1)$ space. This is optimal.
- **[Uniform binary search](/uniform-binary-search/) and [Fibonacci search](/fibonacci-search/).** The same number of steps up to a constant, with simpler index arithmetic.
- **[Branchless binary search](/branchless-binary-search/) and the [Eytzinger layout](/eytzinger-layout/).** The same comparisons, arranged to suit the branch predictor and the cache of a real processor.
- **[Exponential search](/exponential-search/).** Probe indices $1, 2, 4, \ldots$ and then do a binary search. It uses $O(\log i)$ comparisons for a key at index $i$, and it works when $n$ is not known.
- **[Jump search](/jump-search/).** Jump in blocks of about $\sqrt{n}$ items, then scan one block. $\Theta(\sqrt{n})$ comparisons; it suits media where a step back is costly.
- **[Interpolation search](/interpolation-search/).** Guess the position from the key value. $O(\log \log n)$ expected probes on keys drawn independently and uniformly, but $\Theta(n)$ in the worst case.
- **[Linear search](/linear-search/).** Ignore the order. $\Theta(n)$ comparisons; with the order it can stop at the first item greater than $x$.

## Bounds

**Upper bound.** Binary search makes at most $\lfloor \lg n \rfloor + 1$ three-way comparisons for $n \ge 1$. For a key in the array at a uniformly random index, the average is about $\lg n - 1$: for $n = 10$, 100 and 1000 the averages of the binary search on the [binary search](/binary-search/) page are 2.9, 5.8 and 8.987.

**Lower bound.** In the comparison model with three-way comparisons of $x$ with items, each correct deterministic algorithm makes at least $\lceil \lg(n+1) \rceil$ comparisons in the worst case. The algorithm is a [decision tree](/search-decision-tree/). For an input with distinct items it must be able to return each of the $n$ indices, and it can return index $i$ only after an "equal" answer to a comparison with $A[i]$. So the tree has at least $n$ comparison nodes, and a tree whose nodes have at most two non-leaf children and that has $n$ nodes has height at least $\lceil \lg(n+1) \rceil$. The full proof is on the page [lower bound for comparison-based search](/search-lower-bound/). Since $\lfloor \lg n \rfloor + 1 = \lceil \lg(n+1) \rceil$ for each $n \ge 1$, binary search meets the bound exactly.

| $n$ | 1 | 10 | 100 | 1000 | $10^6$ | $10^9$ |
|---|---|---|---|---|---|---|
| $\lceil \lg(n+1) \rceil$ | 1 | 4 | 7 | 10 | 20 | 30 |

**Other models.** Outside the comparison model the bound can fail. If the keys are numbers from a smooth distribution, interpolation search uses $O(\log \log n)$ probes on average ([expected time of interpolation search](/interpolation-search-expected-time/)). If the keys are $w$-bit integers on a [word RAM](/word-ram/) and the array may be preprocessed, structures for the predecessor problem answer faster than $\lg n$ for large $n$. If the array may be preprocessed into a [hash table](/hash-table/), membership takes $O(1)$ expected time, but the order queries $\ell$ and $u$ are lost.

## Reductions

- **Membership in a static set reduces to this problem.** Sort the set once in $O(n \log n)$. Then each test "is $x$ in the set" is a search in a sorted array, in $O(\log n)$.
- **This problem reduces to the lower bound query.** Compute $\ell$ and test $\ell < n$ and $A[\ell] = x$. This costs one more comparison.
- **Counting in a range reduces to two lower bound queries.** The number of items in $[a, b)$ is $\ell(b) - \ell(a)$.

## Applications

- Look up a key in a sorted table, such as a symbol table, a dictionary file, or the sorted run of an index on disk.
- Insert into a sorted array: the lower bound gives the place, as in the binary variant of [insertion sort](/insertion-sort/).
- Count the items in a range with two lower bound queries.
- Search on the answer: find the smallest value that satisfies a monotone test, as in [binary search on the answer](/binary-search-on-answer/).
- Debug by bisection: find the first version of a program that fails a test, when the versions are in order and the failure persists once it appears.

## References
