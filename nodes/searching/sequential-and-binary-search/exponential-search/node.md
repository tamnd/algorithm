---
tag: V34DA8
kind: algorithm
slug: exponential-search
name: Exponential search
aliases:
- doubling search
- galloping search
area: searching/sequential-and-binary-search
level: core
summary: Probe indices 1, 2, 4, and so on until the key is bracketed, then binary search; O(log i) for a key at position i.
solves: [search-in-sorted-array, unbounded-search]
model: comparison-model
complexity:
  vars: {n: the number of items in the array, i: the position of the key (its lower bound)}
  time: {worst: Θ(log i), best: Θ(1)}
  space: {extra: Θ(1)}
properties: {deterministic: true, comparison: true, recursive: false, in_place: true}
prereqs: [binary-search, lower-bound-query]
see_also: [unbounded-search, binary-search, jump-search, timsort, merging-sorted-lists, sorted-array-intersection, elias-gamma-coding, finger-search-tree]
sources:
  - paper: doi:10.1016/0020-0190(76)90071-5
    title: Jon Louis Bentley and Andrew Chi-Chih Yao, An almost optimal algorithm for unbounded searching, Information Processing Letters 5(3) (1976)
    locator: pp. 82 to 87 (algorithm B1, the doubling search, and the better algorithms B2 and Bk)
  - book: isbn:9780201896855
    title: Donald E. Knuth, The Art of Computer Programming, Volume 3, second edition
    locator: Section 6.2.1, Searching an ordered table
---

Exponential search finds a key $x$ in a sorted array by testing the items at the indices $0, 1, 3, 7, 15, \ldots$, that is $A[b - 1]$ for $b = 1, 2, 4, 8, \ldots$, until one of them is at least $x$, and then running a [binary search](/binary-search/) in the last interval it jumped over. If the first copy of $x$, or the place where $x$ would go, is at index $i$, it makes at most $2\lfloor \lg i \rfloor + 3$ comparisons. The cost depends on $i$, not on the length $n$, so the search is fast for keys near the start and works when the length is not known at all, as in the [unbounded search](/unbounded-search/) problem. Bentley and Yao gave it in 1976; under the name *galloping* it is a key step of [Timsort](/timsort/) and of adaptive merging.

## In plain words

You look for a word in a long sorted list, and you think it is near the top. You do not jump to the middle. You look at item 1, then item 2, then item 4, then item 8, and you double each time. When you see an item that is not before your word, you know the word is between that item and the one you looked at before.

That gap is no longer than the distance you have walked so far. You then search the gap by halving it. Both steps take about as many looks as the number of times you can halve the position of the word. A word near the top costs only a few looks, even in a list of a million items.

## The problem

The input is an array $A[0 \ldots n-1]$, $n \ge 0$, sorted so that $A[0] \le \cdots \le A[n-1]$, and a key $x$. The output is the smallest index $i$ with $A[i] = x$, or NIL when $x$ is not in $A$. This is [search in a sorted array](/search-in-sorted-array/). The algorithm uses only comparisons of $x$ with items. Let $\ell$ be the [lower bound](/lower-bound-query/) of $x$, the number of items less than $x$; the cost is measured in terms of $\ell$.

The algorithm reads $n$ only to stop at the end of the array. When the array has no end, as in [unbounded search](/unbounded-search/), the test $b \le n$ is always true and can be removed.

## The algorithm

```pseudo id=main
EXPONENTIAL-SEARCH(A, x)
L1  b ← 1
L2  while b ≤ n and A[b − 1] < x do       ▷ all of A[0 .. b − 1] is less than x
L3      b ← 2b
L4  lo ← ⌊b / 2⌋, hi ← min(b − 1, n)       ▷ the lower bound of x is in [lo, hi]
L5  while lo < hi do                       ▷ binary search for the lower bound
L6      mid ← lo + ⌊(hi − lo) / 2⌋
L7      if A[mid] < x then lo ← mid + 1
L8      else hi ← mid
L9  if lo < n and A[lo] = x then return lo
L10 return NIL
```

Lines L1 to L3 are the doubling phase. Each test reads $A[b - 1]$, the last item of the prefix of length $b$. When it is less than $x$, the whole prefix is less than $x$ because the array is sorted, and $b$ doubles. The phase stops at the first $b$ with $A[b - 1] \ge x$, or when $b$ passes $n$.

Line L4 sets the interval. The last test that passed was at $b/2$, so all items before $\lfloor b/2 \rfloor$ are less than $x$. The test that failed, or the end of the array, shows that the lower bound is at most $\min(b - 1, n)$. So the lower bound lies in $[lo, hi]$, an interval of $hi - lo \le b/2 - 1$ positions.

Lines L5 to L8 are the half-open [lower bound search](/lower-and-upper-bound-search/) on $[lo, hi)$, which returns $hi$ when all of $A[lo \ldots hi-1]$ is less than $x$. Line L9 tests whether the lower bound holds $x$.

## Example

The array has $n = 13$ items:

| index | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| $A$ | 2 | 5 | 8 | 12 | 16 | 23 | 38 | 56 | 72 | 91 | 99 | 104 | 120 |

Search for $x = 23$:

| step | line | $b$ or $[lo, hi)$ | test | result |
|---|---|---|---|---|
| 1 | L2 | $b = 1$ | $A[0] = 2 < 23$ | $b = 2$ |
| 2 | L2 | $b = 2$ | $A[1] = 5 < 23$ | $b = 4$ |
| 3 | L2 | $b = 4$ | $A[3] = 12 < 23$ | $b = 8$ |
| 4 | L2 | $b = 8$ | $A[7] = 56 < 23$ is false | stop |
| 5 | L7 | $[4, 7)$, $mid = 5$ | $A[5] = 23 < 23$ is false | $hi = 5$ |
| 6 | L7 | $[4, 5)$, $mid = 4$ | $A[4] = 16 < 23$ | $lo = 5$ |
| 7 | L9 | $lo = 5$ | $A[5] = 23$ | return 5 |

That is 7 comparisons, which is $2\lfloor \lg 5 \rfloor + 3$. A search for $x = 72$ passes the tests at $b = 1, 2, 4, 8$, stops because $b = 16 > n$, and searches $[8, 13)$ with 3 tests: 8 comparisons in all. A search for $x = 1$ fails the first test, gets $lo = hi = 0$, and makes one more test at line L9: 2 comparisons and the answer NIL.

## Correctness

Before each test of line L2, $b$ is a power of 2, $b \le 2n$ when $n \ge 1$, and $A[j] < x$ for each $j < \lfloor b/2 \rfloor$. A pass runs only when $A[b - 1] < x$, and then all of $A[0 \ldots b-1]$ is less than $x$, so the statement holds for $2b$. When the loop stops, either $b > n$, so the lower bound $\ell \le n = \min(b - 1, n)$, or $A[b - 1] \ge x$, so $\ell \le b - 1$. With the invariant, $lo \le \ell \le hi$ after line L4. The binary search keeps $lo \le \ell \le hi$ and stops with $lo = \ell$, and line L9 returns $\ell$ exactly when it holds $x$. The doubling stops once $b > n$, and the binary search shrinks $hi - lo$ in each step, so the algorithm stops. The full proof is below.

## Complexity

Count the comparisons of items, and let $\ell$ be the lower bound of $x$.

- **Doubling.** The test at $b$ passes exactly when $b \le \ell$. For $\ell \ge 1$ it passes for $b = 1, 2, \ldots, 2^k$ with $k = \lfloor \lg \ell \rfloor$, then fails at $b = 2^{k+1}$ or stops at the end. That is at most $\lfloor \lg \ell \rfloor + 2$ tests. For $\ell = 0$ it is one test.
- **Binary search.** The interval has $hi - lo \le 2^k - 1$ positions, so the search makes at most $k = \lfloor \lg \ell \rfloor$ tests (the [lower bound search](/lower-and-upper-bound-search/) makes at most $\lceil \lg(s + 1) \rceil$ tests on $s$ positions).
- **Final test.** One equality test.

So the total is at most $2\lfloor \lg \ell \rfloor + 3$ for $\ell \ge 1$, and 2 for $\ell = 0$. When the doubling does not reach the end, the bound is exact. The table gives the count on an array of $10^6$ distinct items for the key at index $i$:

| $i$ | 0 | 1 | 2 | 7 | 8 | 100 | 1000 | 999999 |
|---|---|---|---|---|---|---|---|---|
| comparisons | 2 | 3 | 5 | 7 | 9 | 15 | 21 | 40 |
| $2\lfloor \lg i \rfloor + 3$ | | 3 | 5 | 7 | 9 | 15 | 21 | 41 |

- **Worst case.** Since $\ell \le n$, at most $2\lfloor \lg n \rfloor + 3$ comparisons: $\Theta(\log n)$, about twice the cost of a plain binary search.
- **In terms of the position.** $\Theta(\log \ell)$ for $\ell \ge 1$. This is the point of the method: a key at index 100 costs 15 comparisons in an array of any length, against about 20 for binary search on $10^6$ items and 30 on $10^9$.
- **Best case.** $x \le A[0]$ costs 2 comparisons: $\Theta(1)$.
- **Space.** Four indices: $\Theta(1)$.

## Properties

- **Adaptive.** The cost grows with the position of the key, not with the length of the array.
- **Needs no length.** Only line L2 and line L4 read $n$, and only to stop at the end. On an unbounded sequence they can be dropped.
- **First occurrence.** The final phase finds the lower bound, so the result is the smallest index of $x$.
- **Comparison-based and in place.** It uses only $<$ and $=$ on items, and it does not change the array.

## Variants and improvements

- **Search from a finger.** Start the doubling at a known index $f$ and probe $f + 1, f + 2, f + 4, \ldots$ (or to the left). The cost is $O(\log d)$ for a key at distance $d$ from $f$. This is the search of a [finger search tree](/finger-search-tree/), and the galloping mode of [Timsort](/timsort/), which looks for the place of one run's head in the other run.
- **Adaptive merging and intersection.** To [merge](/merging-sorted-lists/) or [intersect](/sorted-array-intersection/) sorted lists of lengths $m \le n$, gallop in the long list from the last position for each item of the short one. The total is $O(m \log(n/m + 1))$, which is optimal for comparisons, and it is never much worse than the linear merge.
- **Faster unbounded search.** Bentley and Yao improve the doubling phase by searching for the exponent $k = \lfloor \lg \ell \rfloor$ itself with a doubling search (their algorithm B2). The cost becomes $\lg \ell + 2\lg \lg \ell + O(1)$, and repeating the idea gives $\lg \ell + \lg \lg \ell + \cdots + O(\lg^* \ell)$ comparisons, which is close to their lower bound. See [unbounded search](/unbounded-search/).
- **Codes for integers.** A search strategy for the unbounded problem gives a prefix code for the positive integers: write the result of each comparison as a bit. Doubling search matches the [Elias gamma code](/elias-gamma-coding/), which writes $N$ with $2\lfloor \lg N \rfloor + 1$ bits, and algorithm B2 matches the [Elias delta code](/elias-delta-coding/).
- **Other base.** Multiply $b$ by $c > 2$ instead of 2. The doubling takes fewer tests, $\log_c \ell$, but the final interval is $c - 1$ times longer. The base 2 is the best for this simple scheme.
- **Doubling then scan.** On a medium with costly steps back, the final interval can be scanned instead of halved; see [jump search](/jump-search/) for that trade.

## When to use it

Use exponential search when the key is likely to be near the start of the array, or near a known position, and when the length of the data is not known or is very large: a sorted stream, a sorted file read in blocks, a function $f(t)$ that is monotone in $t$ with no known upper end, or the merge of two runs of very different lengths. When the key can be anywhere in an array of known length, plain [binary search](/binary-search/) is better by about a factor of 2.

## Pitfalls

- **Testing $A[b]$ instead of $A[b - 1]$.** The test must read the last item of the prefix that is proved to be less than $x$. A version that tests $A[b]$ and sets $lo = b/2$ is also correct if it is written with care, but mixing the two forms gives an interval that misses the answer by one.
- **Starting the binary search at $b/2 + 1$ or ending at $b$.** The lower bound can be exactly $\lfloor b/2 \rfloor$, the first index not yet proved to be less than $x$, and it can be $\min(b - 1, n)$ when all of the interval is less than $x$. The half-open search on $[lo, hi)$ returns $hi$ in that case, so both ends are covered.
- **Reading past the end.** Line L2 tests $b \le n$ before it reads $A[b - 1]$, and line L4 cuts $hi$ to $n$.
- **Overflow of $b$.** On an array near the largest index of a fixed-size integer type, $2b$ can overflow. Stop the doubling when $b > n/2$, or use a wider type.
- **An empty array.** For $n = 0$ the loop does not run, $lo = hi = 0$, and line L9 must test $lo < n$ before it reads $A[0]$.

## Implementations

## History

Bentley and Yao described the doubling search, which they called algorithm B1, in 1976 as the first step of a family of algorithms for unbounded searching, and they proved that their best algorithm is within a small additive term of the optimum. The galloping form, used to merge runs of very different lengths, goes back to work on adaptive merging and set intersection, and Tim Peters made it part of the merge step of Timsort in 2002.

## References
