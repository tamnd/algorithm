---
tag: GDCGR7
kind: algorithm
slug: linear-search
name: Linear search
aliases:
- linear scan
- sequential search
area: searching/sequential-and-binary-search
level: intro
summary: Scan the array left to right until the key is found or the end is reached; O(n) comparisons.
solves: [search-in-unordered-array]
model: comparison-model
complexity:
  vars: {n: the number of items in the array}
  time: {worst: Θ(n), average: Θ(n), best: Θ(1)}
  space: {extra: Θ(1)}
properties: {deterministic: true, comparison: true, recursive: false, online: true, in_place: true}
prereqs: [search-in-unordered-array, loop-invariant, asymptotic-notation]
see_also: [sentinel-search, binary-search, jump-search, self-organizing-list-search, sequential-search-symbol-table, find-maximum, search-in-sorted-array, move-to-front-heuristic]
sources:
  - book: isbn:9780201896855
    title: Donald E. Knuth, The Art of Computer Programming, Volume 3, second edition
    locator: Section 6.1, Algorithm S (sequential search), Algorithm Q (with a sentinel) and Algorithm T (in an ordered table), with their analysis
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Section 2.1, exercises (linear search and its loop invariant) and Section 2.2, exercises (its average and worst case)
  - book: isbn:9780321573513
    title: Robert Sedgewick and Kevin Wayne, Algorithms, fourth edition
    locator: Section 3.1, SequentialSearchST
---

Linear search, also called sequential search, finds a key $x$ in an [array](/array/) by testing the items one by one from the left, and it returns the first index $i$ with $A[i] = x$, or NIL after the last item. It solves [search in an unordered array](/search-in-unordered-array/) with at most $n$ comparisons, and that is optimal: in the [comparison model](/comparison-model/) no algorithm can be sure that an item is absent from an unordered array with fewer than $n$ comparisons. It needs no order, no hash and no extra memory, so it is the method of choice for short lists and for data that is searched only once.

## In plain words

You look for a name in a stack of papers that are in no order. You take the first paper and read it. If it has the name, you stop. If not, you take the next one, and so on. If you reach the end of the stack, the name is not there.

The method finds the first paper with the name, because it looks at the papers in order. A name near the top is found fast. A name that is not there costs a look at every paper. Nothing about the order of the papers helps you skip any of them.

## The problem

The input is an array $A[0 \ldots n-1]$ of $n \ge 0$ items and a key $x$. The output is the smallest index $i$ with $A[i] = x$, or NIL when no item is equal to $x$. This is [search in an unordered array](/search-in-unordered-array/), with the convention that the first occurrence is returned. The algorithm uses only the equality test, so the items need no order.

## The algorithm

```pseudo id=main
LINEAR-SEARCH(A, x)
L1  for i ← 0 to n − 1 do             ▷ A[0 .. i − 1] holds no copy of x
L2      if A[i] = x then return i
L3  return NIL
```

Line L1 runs the index $i$ over the array from the left. Line L2 tests one item and stops at the first match. Line L3 runs only when the loop ends without a match, so then no item is equal to $x$.

Each pass of the loop does two tests: the end test $i \le n - 1$ of line L1 and the key test of line L2. The [sentinel](/sentinel-search/) version removes the end test by placing a copy of $x$ after the last item.

## Example

Search $A = [7, 3, 9, 3, 1, 8]$, with $n = 6$.

For $x = 3$:

| $i$ | $A[i]$ | $A[i] = 3$? | action |
|---|---|---|---|
| 0 | 7 | no | go on |
| 1 | 3 | yes | return 1 |

The search returns 1, the first of the two copies at indices 1 and 3. It makes 2 key tests.

For $x = 5$:

| $i$ | 0 | 1 | 2 | 3 | 4 | 5 |
|---|---|---|---|---|---|---|
| $A[i]$ | 7 | 3 | 9 | 3 | 1 | 8 |
| $A[i] = 5$? | no | no | no | no | no | no |

The loop ends after 6 key tests and returns NIL.

## Correctness

The proof uses a [loop invariant](/loop-invariant/) of line L1: before the pass with index $i$, no item of $A[0 \ldots i-1]$ is equal to $x$. It is true at the start because the range is empty. A pass that does not return has $A[i] \ne x$, so the invariant holds for $i + 1$. If line L2 returns $i$, then $A[i] = x$ and, by the invariant, $i$ is the smallest such index. If line L3 is reached, the invariant holds for $i = n$, so no item is equal to $x$. The loop runs at most $n$ passes, so it stops. The full proof is below.

## Complexity

Count the key tests of line L2. The work of one pass is a constant, so the time is $\Theta$ of this count, plus $\Theta(1)$.

- **Worst case.** When $x$ is absent, or only at the last index, the loop runs all $n$ passes: $n$ key tests and $\Theta(n)$ time.
- **Best case.** When $A[0] = x$, one key test: $\Theta(1)$.
- **Average case, successful.** If the items are distinct and $x$ is at each of the $n$ indices with probability $1/n$, a key at index $i$ costs $i + 1$ tests, so the average is $\frac1n \sum_{i=0}^{n-1} (i + 1) = \frac{n+1}{2}$. This is $\Theta(n)$.
- **Average case, mixed.** If $x$ is present with probability $q$, the average is $q \frac{n+1}{2} + (1 - q) n$. For $n = 100$ this is 50.5 for $q = 1$, 75.25 for $q = 1/2$ and 100 for $q = 0$.
- **Space.** The index $i$ only: $\Theta(1)$ extra space.

The worst case is optimal. Each comparison algorithm for search in an unordered array makes at least $n$ comparisons on some input where $x$ is absent; the proof is on the page [search in an unordered array](/search-in-unordered-array/).

If the probabilities are not uniform, the order of the items matters. With access probabilities $p_0, \ldots, p_{n-1}$, the expected cost of a successful search is $\sum_i (i+1) p_i$, which is smallest when the items are in order of non-increasing $p_i$. This is the starting point of [self-organizing lists](/self-organizing-list-search/).

## Properties

- **Online.** The algorithm reads the items once, in order. It works on a stream, a linked list or a file, where only the next item can be read.
- **No order needed.** It uses only the equality test, so it works for any type with an equality.
- **First occurrence.** It returns the smallest index of $x$. Scanning from the right returns the largest.
- **In place.** It does not change the array, and it uses one index.
- **Deterministic.** The same input gives the same tests.

## Variants and improvements

- **[Sentinel linear search](/sentinel-search/).** Store $x$ at $A[n]$, so the loop stops without the end test. It makes the same key tests and $n + 1$ fewer index tests in the worst case.
- **Search in an ordered table.** If $A$ is sorted, stop at the first $A[i] \ge x$. An absent key then costs on average about half the array, not all of it (Knuth, Algorithm T). [Binary search](/binary-search/) is much better in this case.
- **[Jump search](/jump-search/).** On a sorted array, test every $m$-th item first, then scan one block. With $m \approx \sqrt{n}$ this costs about $2\sqrt{n}$ tests.
- **Self-organizing lists.** After each successful search, move the item found to the front, or one place forward. Items that are asked for often then sit near the front. See [move-to-front](/move-to-front-heuristic/) and [search in a self-organizing list](/self-organizing-list-search/).
- **Search by a predicate.** Replace the test $A[i] = x$ by any test $P(A[i])$. This finds the first item with a property, for example the first negative number.
- **Find all occurrences.** Do not stop at a match, and collect each $i$. This always costs $n$ tests.

## When to use it

Use linear search when the array is short (up to a few dozen items, where the simple loop beats the overhead of other methods), when it is not sorted and is searched only a few times, when it changes after each search, or when the data can only be read in order. If the same array is searched many times, sort it once and use [binary search](/binary-search/), or build a [hash table](/hash-table/). Sorting costs $\Theta(n \log n)$, so it pays only after about $\log n$ searches.

## Pitfalls

- **An off-by-one end.** A loop "for $i \gets 0$ to $n$" in line L1 reads $A[n]$, which is outside the array. The last index is $n - 1$.
- **Returning too early.** Writing "else return NIL" inside the loop, after line L2, stops after the first item. Line L3 must come after the loop ends.
- **The value of NIL.** An implementation that returns $-1$ for NIL must not let the caller use it as an index. In Python, $A[-1]$ is the last item, so this mistake gives a wrong answer and no error.
- **Equality of floats.** A test $A[i] = x$ on floating-point values can fail for values that are equal in theory. Use a tolerance, or search for the closest item.

## Implementations

## History

Sequential search is older than computers: it is how a person searches an unsorted list. Knuth starts the chapter on searching with it, as Algorithm S of Section 6.1, and gives there the sentinel version (Algorithm Q), the version for an ordered table (Algorithm T), the average costs above, and the analysis of self-organizing files.

## References
