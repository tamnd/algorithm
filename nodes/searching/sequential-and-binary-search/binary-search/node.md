---
tag: 2B7QDX
kind: algorithm
slug: binary-search
name: Binary search
aliases: [half-interval search, logarithmic search, bisection search]
area: searching/sequential-and-binary-search
level: intro
summary: Find a key in a sorted array. Compare the key with the middle item, and keep only the half that can hold the key.
solves: [search-in-sorted-array]
model: comparison-model
complexity:
  vars: {n: the number of items in the array}
  time: {worst: Θ(log n), average: Θ(log n), best: Θ(1)}
  space: {extra: Θ(1)}
properties: {deterministic: true, comparison: true, recursive: false}
history:
  year: 1946
  people: [John Mauchly, Derrick Henry Lehmer]
  note: Mauchly described the method in the Moore School Lectures in 1946. Lehmer gave a version for any n in 1960.
prereqs: [search-in-sorted-array, loop-invariant, asymptotic-notation]
see_also: [lower-and-upper-bound-search, lower-bound-query, exponential-search, interpolation-search, branchless-binary-search, eytzinger-layout, search-lower-bound, binary-search-on-answer]
sources:
  - book: isbn:9780201896855
    title: Donald E. Knuth, The Art of Computer Programming, Volume 3, second edition
    locator: Section 6.2.1, Algorithm B
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Exercise 2.3-6
  - url: https://research.google/blog/extra-extra-read-all-about-it-nearly-all-binary-searches-and-mergesorts-are-broken/
    title: Joshua Bloch, Nearly all binary searches and mergesorts are broken (2006)
    note: the overflow of (lo + hi) / 2
  - book: isbn:9780201657883
    title: Jon Bentley, Programming Pearls, second edition
    locator: Column 4, Writing correct programs (binary search and its invariant)
---

Binary search finds a key in a sorted array of $n$ items with at most $\lfloor \lg n \rfloor + 1$ comparisons, so its time is $\Theta(\log n)$ in the worst case. It solves [search in a sorted array](/search-in-sorted-array/). Each comparison with the middle item removes half of the items that are left. No comparison algorithm can do better in the worst case, and the same loop is the base of the lower bound of a sorted range, of exponential search and of search on the answer.

## In plain words

You look for a word in a printed dictionary. You do not read each page. You open the book at the middle. If your word comes before the words on that page, you keep the first half. If it comes after, you keep the second half. You do the same step again on the half that you keep. Each step removes half of the pages, so you find the word after a small number of steps.

Binary search does this on a sorted array. It compares the key with the middle item. The result of the comparison tells which half can hold the key. The algorithm stops when it finds the key, or when no items are left.

## The problem

The input is an array $A[0 \ldots n-1]$ of $n$ items in non-decreasing order, and a key $x$. The output is an index $i$ with $A[i] = x$, or NIL when no item is equal to $x$. This is the problem [search in a sorted array](/search-in-sorted-array/). When the array has more than one copy of $x$, any index of a copy is a correct answer.

The algorithm only compares items. It does not do arithmetic on them. So it works for numbers, strings and any other type with a total order.

## The algorithm

The algorithm keeps a range of indices $[lo, hi)$. The key can only be at an index in this range. At the start, the range is the full array.

```pseudo id=main
BINARY-SEARCH(A, x)
L1  lo ← 0, hi ← n                    ▷ the range is A[lo .. hi − 1]
L2  while lo < hi do
L3      mid ← lo + ⌊(hi − lo) / 2⌋     ▷ no overflow, unlike ⌊(lo + hi) / 2⌋
L4      if A[mid] < x then
L5          lo ← mid + 1                ▷ x is not in A[lo .. mid]
L6      else if A[mid] > x then
L7          hi ← mid                    ▷ x is not in A[mid .. hi − 1]
L8      else return mid
L9  return NIL
```

Line L3 picks the middle of the range. Lines L4 to L8 compare $A[mid]$ with $x$. If $A[mid] < x$, then each item at an index of $mid$ or less is less than $x$, because the array is sorted. So line L5 removes these indices from the range. Line L7 does the same on the other side. Line L9 runs when the range is empty.

## Example

The array is $A = [2, 5, 8, 12, 16, 23, 38, 56, 72, 91]$, with $n = 10$. A search for $x = 23$ takes one step. The first middle item is $A[5] = 23$, so the algorithm returns 5.

A search for $x = 30$ takes four steps:

| step | lo | hi | mid | $A[mid]$ | result |
|---|---|---|---|---|---|
| 1 | 0 | 10 | 5 | 23 | $23 < 30$, so $lo \gets 6$ |
| 2 | 6 | 10 | 8 | 72 | $72 > 30$, so $hi \gets 8$ |
| 3 | 6 | 8 | 7 | 56 | $56 > 30$, so $hi \gets 7$ |
| 4 | 6 | 7 | 6 | 38 | $38 > 30$, so $hi \gets 6$ |

Now $lo = hi = 6$. The range is empty, so the algorithm returns NIL. The index 6 is the place where 30 can go to keep the array sorted.

## Correctness

The proof uses a [loop invariant](/loop-invariant/). Before each test of line L2, this statement is true:

> If $x$ is in $A$, then $x$ is in $A[lo \ldots hi-1]$.

At the start, the range is the full array, so the statement is true. Each step keeps it true, because lines L5 and L7 only remove indices that cannot hold $x$. Each step also makes the range smaller, because $lo \le mid < hi$. So the loop stops. When line L8 returns, $A[mid] = x$. When line L9 returns, the range is empty, and by the invariant $x$ is not in $A$. The full proof is below.

## Complexity

Let $k$ be the size $hi - lo$ of the range. One step that does not return makes the new size $\lfloor (k-1)/2 \rfloor$ or $\lceil (k-1)/2 \rceil$, and both are at most $\lfloor k/2 \rfloor$. So after $t$ steps the size is at most $\lfloor n / 2^t \rfloor$, which is 0 for $t = \lfloor \lg n \rfloor + 1$. So the loop runs at most $\lfloor \lg n \rfloor + 1$ times for $n \ge 1$, and 0 times for $n = 0$. Each step does one three-way comparison of $A[mid]$ with $x$ (two two-way tests in lines L4 and L6 at most), and a fixed number of other operations.

- **Worst case.** $\lfloor \lg n \rfloor + 1$ steps, so $\Theta(\log n)$ time. An absent key always takes $\lfloor \lg n \rfloor$ or $\lfloor \lg n \rfloor + 1$ steps.
- **Best case.** One step, $\Theta(1)$, when the key is the first middle item.
- **Average case.** For a key at a uniformly random index of an array of distinct items, the average number of steps is about $\lg n - 1$, and for an absent key about $\lg n$. So the average time is $\Theta(\log n)$. The exact averages of this loop are in the table.
- **Space.** $\Theta(1)$: three indices.

| $n$ | 10 | 100 | 1000 | $10^6$ |
|---|---|---|---|---|
| worst case, $\lfloor \lg n \rfloor + 1$ | 4 | 7 | 10 | 20 |
| average, key present | 2.9 | 5.8 | 8.987 | |
| average, key absent (each of the $n+1$ gaps) | 3.545 | 6.733 | 9.977 | |

In the [comparison model](/comparison-model/), each algorithm for this problem needs $\lceil \lg(n+1) \rceil$ three-way comparisons in the worst case. The argument uses a [decision tree](/search-decision-tree/): the tree must hold a comparison with each of the $n$ positions, and a binary tree with $n$ nodes has height at least $\lceil \lg(n+1) \rceil$. Because $\lfloor \lg n \rfloor + 1 = \lceil \lg(n+1) \rceil$, binary search is optimal in this model. The proof is on the page [lower bound for comparison-based search](/search-lower-bound/).

## Properties

- **Deterministic.** The same input gives the same steps and the same result.
- **Only comparisons.** The algorithm reads the items only through the comparisons of lines L4 and L6, so it works for each type with a total order.
- **In place.** The extra space is three indices. The array does not change.
- **Not stable in its result.** When the array has more than one copy of $x$, the index that it returns depends on $n$, not on the order of the copies. Use the lower bound variant below to get the first copy.

## Variants and improvements

- **Lower bound.** Return the first index $i$ with $A[i] \ge x$, or $n$. Remove line L8, change line L6 to "else $hi \gets mid$", and return $lo$ at line L9. Each step then does one two-way comparison, and the loop always runs $\lfloor \lg n \rfloor$ or $\lfloor \lg n \rfloor + 1$ times. The C++ function `std::lower_bound` and the Python function `bisect.bisect_left` do this. See [lower and upper bound search](/lower-and-upper-bound-search/) and the [lower bound query](/lower-bound-query/).
- **Upper bound.** Return the first index $i$ with $A[i] > x$: the same loop with the test $A[mid] \le x$. The number of copies of $x$ is the upper bound minus the lower bound. See the [upper bound query](/upper-bound-query/) and [first and last occurrence](/first-and-last-occurrence/).
- **Closed range.** Many texts keep $[lo, hi]$ with both ends in the range: start with $hi \gets n - 1$, loop while $lo \le hi$, and set $hi \gets mid - 1$ in line L7. This is also correct. The two styles must not be mixed.
- **Uniform and Fibonacci search.** [Uniform binary search](/uniform-binary-search/) keeps only the middle and a step from a precomputed table. [Fibonacci search](/fibonacci-search/) splits at Fibonacci numbers and uses only addition and subtraction.
- **Faster on real hardware.** [Branchless binary search](/branchless-binary-search/) replaces the branch by a conditional move. The [Eytzinger layout](/eytzinger-layout/) stores the array in the order of the implicit search tree, so the first probes share cache lines.
- **Search on the answer.** Use the same loop on any predicate that is false and then true over a range of integers. This finds the smallest value that satisfies the predicate. See [binary search on the answer](/binary-search-on-answer/).
- **[Exponential search](/exponential-search/).** When $n$ is not known, or the key is near the start, test the indices $1, 2, 4, 8, \ldots$ first. Then do a binary search in the last interval. The cost is $O(\log i)$ for a key at index $i$.
- **[Interpolation search](/interpolation-search/).** Guess the index from the values, as a person does with a phone book. On keys drawn uniformly at random the expected number of probes is $O(\log \log n)$, but the worst case is $\Theta(n)$.

## When to use it

Use binary search when the data is sorted and does not change often, and you search it many times. If the data changes often, a balanced search tree or a hash table is better. A hash table also answers a search in $O(1)$ expected time, but it cannot answer "which is the next larger item". If you search an array only once, a linear scan in $O(n)$ costs less than a sort in $O(n \log n)$ followed by a binary search.

## Pitfalls

- **Overflow.** The expression $\lfloor (lo + hi)/2 \rfloor$ can overflow a fixed-size integer when the array is very large. This bug was in the Java library for nine years. Use $lo + \lfloor (hi - lo)/2 \rfloor$, as line L3 does.
- **An infinite loop.** With a closed range $[lo, hi]$, the update "$lo \gets mid$" can keep the range the same size. Each update must remove $mid$, or the range must be half-open as here.
- **An off-by-one error.** Decide if $hi$ is in the range or not, and use the same rule in each line. With the half-open range of line L1, the test of line L2 must be $lo < hi$, not $lo \le hi$ (which reads $A[n]$ when $lo = hi = n$), and line L7 must be $hi \gets mid$, not $hi \gets mid - 1$ (which skips the index $mid - 1$).
- **A midpoint that rounds the wrong way.** With $mid = lo + \lceil (hi - lo)/2 \rceil$, the range $[lo, lo + 1)$ gives $mid = lo + 1 = hi$, outside the range. Line L3 rounds down so that $lo \le mid < hi$.
- **Unsorted input.** On an array that is not sorted, the result has no meaning. The algorithm does not detect this.

## Implementations

## History

John Mauchly described binary search in the Moore School Lectures in 1946. The first published version that works for each $n$, not only for $n = 2^k - 1$, is by Derrick Henry Lehmer in 1960. Knuth says that the idea is simple, but the details are hard. Jon Bentley reports in Programming Pearls that, given ample time, only about ten percent of the professional programmers in his courses wrote a correct binary search. In 2006 Joshua Bloch showed the overflow bug of the midpoint in the Java library.

## References
