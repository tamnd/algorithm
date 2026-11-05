---
tag: T2VJT6
kind: technique
slug: lower-and-upper-bound-search
name: Lower bound and upper bound search
aliases:
- Lower bound and upper bound
area: searching/sequential-and-binary-search
level: intro
summary: Binary search variants that find the first element not less than a value or the first element greater than a value.
prereqs: [binary-search, lower-bound-query, upper-bound-query, loop-invariant]
see_also: [first-and-last-occurrence, binary-search-on-answer, branchless-binary-search, rotated-sorted-array-minimum, peak-finding, binary-search-on-real-numbers, search-in-sorted-array, eytzinger-layout]
sources:
  - book: isbn:9780201657883
    title: Jon Bentley, Programming Pearls, second edition
    locator: Column 4 (writing a binary search from its invariant) and Column 9, Section 9.3 (a binary search that finds the first occurrence)
  - book: isbn:9780201896855
    title: Donald E. Knuth, The Art of Computer Programming, Volume 3, second edition
    locator: Section 6.2.1, Searching an ordered table
  - book: isbn:9780321573513
    title: Robert Sedgewick and Kevin Wayne, Algorithms, fourth edition
    locator: Section 3.1, binary search in an ordered array (rank)
  - url: https://docs.python.org/3/library/bisect.html
    title: Python Software Foundation, bisect, Array bisection algorithm
---

Lower and upper bound search is the form of [binary search](/binary-search/) that does not look for a key but for a *boundary*: the first index of a range at which a monotone test becomes true. With the test $A[i] \ge x$ on a sorted array it answers the [lower bound query](/lower-bound-query/), and with the test $A[i] > x$ the [upper bound query](/upper-bound-query/). One loop of five lines, with the half-open range $[lo, hi)$ and the [loop invariant](/loop-invariant/) "false to the left of $lo$, true from $hi$ on", solves both with at most $\lceil \lg(n+1) \rceil$ tests, and the same loop finds the first bad version, the smallest feasible capacity or the minimum of a rotated array.

## In plain words

Think of a row of lamps where all the lamps that are off come first and all the lamps that are on come after them. You want the first lamp that is on. You check the lamp in the middle. If it is on, the first lit lamp is this one or one to its left. If it is off, the first lit lamp is to its right. Each check halves the part of the row where the answer can be.

You keep two marks: everything before the left mark is known to be off, and everything from the right mark on is known to be on. When the two marks meet, they point at the answer. If all lamps are off, the marks meet just past the end of the row.

## When it applies

- The question has the form "the first index (or value) at which something becomes true", or "the last one at which it is still false".
- There is a test $P(i)$ on the integers of a range $[lo, hi)$ that is **monotone**: once it is true, it stays true. In symbols, $i \le j$ and $P(i)$ imply $P(j)$.
- Each test costs about the same, and much less than testing all of the range.
- Typical signals: a sorted array and a key; "how many items are less than"; "where to insert"; "the smallest $t$ such that the job fits in time $t$"; a sequence that is all of one kind and then all of another kind.

The test need not be a comparison with a key. It can be any computation, as long as it is monotone on the range.

## The template

```pseudo id=main
FIRST-TRUE(lo, hi, P)               ▷ P is false on [lo, k) and true on [k, hi) for some k
L1  while lo < hi do
L2      mid ← lo + ⌊(hi − lo) / 2⌋     ▷ lo ≤ mid < hi
L3      if P(mid) then hi ← mid       ▷ the boundary k is at mid or to its left
L4      else lo ← mid + 1             ▷ the boundary k is to the right of mid
L5  return lo                        ▷ lo = hi = k; it equals the old hi when P is never true
```

The holes are the range $[lo, hi)$ and the test $P$. The two queries on a sorted array $A[0 \ldots n-1]$ are:

- LOWER-BOUND$(A, x)$ = FIRST-TRUE$(0, n, i \mapsto A[i] \ge x)$, written in code as "if not $A[mid] < x$".
- UPPER-BOUND$(A, x)$ = FIRST-TRUE$(0, n, i \mapsto A[i] > x)$, written in code as "if $x < A[mid]$".

So the two searches differ in one character: the lower bound moves $lo$ past items that are $< x$, and the upper bound moves $lo$ past items that are $\le x$.

**Why it is correct.** Let $lo_0, hi_0$ be the first values and $k$ the boundary. Before each test of line L1 this invariant holds:

$$ lo_0 \le lo \le k \le hi \le hi_0, $$

so $P$ is false at each index of $[lo_0, lo)$ and true at each index of $[hi, hi_0)$. At the start it holds because $lo_0 \le k \le hi_0$. In a step, line L2 gives $lo \le mid < hi$. If $P(mid)$ is true then $mid \ge k$, since $P$ is false below $k$, so the new $hi = mid$ still has $k \le hi$. If $P(mid)$ is false then $mid < k$, so the new $lo = mid + 1 \le k$. The other inequalities hold because $lo \le mid < hi$. When the loop stops, $lo \ge hi$, and the invariant gives $lo = k = hi$. So line L5 returns the boundary.

**Why it stops, and how fast.** Let $s = hi - lo \ge 1$. Line L3 makes the new size $\lfloor s/2 \rfloor$ and line L4 makes it $s - \lfloor s/2 \rfloor - 1 = \lceil s/2 \rceil - 1$. Both are at most $\lfloor s/2 \rfloor$, which is less than $s$, so the size drops by at least 1 in each step and the loop stops. After $t$ steps the size is at most $\lfloor s_0/2^t \rfloor$, so the loop runs at most $\lfloor \lg s_0 \rfloor + 1 = \lceil \lg(s_0 + 1) \rceil$ times. Both new sizes are also at least $\lceil s/2 \rceil - 1$, so $s' + 1 \ge \lfloor (s+1)/2 \rfloor$; by induction on $s$ the loop runs at least $\lfloor \lg(s_0 + 1) \rfloor$ times. So the number of tests of $P$ is $\lfloor \lg(s_0+1) \rfloor$ or $\lceil \lg(s_0+1) \rceil$ on each input, and exactly $\lg(s_0 + 1)$ when $s_0 + 1$ is a power of 2.

**A trace.** On $A = [1, 3, 3, 3, 5, 8, 8, 13]$ and $x = 3$:

| step | lower bound: $lo, hi, mid, A[mid]$ | $A[mid] \ge 3$ | upper bound: $lo, hi, mid, A[mid]$ | $A[mid] > 3$ |
|---|---|---|---|---|
| 1 | 0, 8, 4, 5 | true | 0, 8, 4, 5 | true |
| 2 | 0, 4, 2, 3 | true | 0, 4, 2, 3 | false |
| 3 | 0, 2, 1, 3 | true | 3, 4, 3, 3 | false |
| 4 | 0, 1, 0, 1 | false | | |
| result | $lo = 1$ | | $lo = 4$ | |

The lower bound is 1 and the upper bound is 4, so the three copies of 3 are at indices 1, 2 and 3. Here $n + 1 = 9$ is not a power of 2, and the two searches take 4 and 3 steps, which are $\lceil \lg 9 \rceil$ and $\lfloor \lg 9 \rfloor$.

## Classic examples

- **[Lower bound query](/lower-bound-query/) and [upper bound query](/upper-bound-query/).** The two direct uses, with $P(i) = A[i] \ge x$ and $P(i) = A[i] > x$.
- **[Search in a sorted array](/search-in-sorted-array/).** Compute the lower bound $\ell$ and test $\ell < n$ and $A[\ell] = x$. This is the "deferred equality test" form of binary search: one two-way test per step and one equality test at the end.
- **[First and last occurrence](/first-and-last-occurrence/).** The first copy is at the lower bound and the last copy at the upper bound minus one.
- **[Minimum of a rotated sorted array](/rotated-sorted-array-minimum/).** With distinct values, the test $P(i) = A[i] \le A[n-1]$ is false on the left part and true on the right part, and its boundary is the minimum.
- **[Peak finding](/peak-finding/).** The test $P(i) = A[i] > A[i+1]$ is not monotone in general, but the same loop keeps an invariant that a peak lies in the range.
- **[Binary search on the answer](/binary-search-on-answer/).** The range is a range of candidate answers, such as capacities or times, and $P(t)$ is "a solution with value $t$ exists". The test is monotone, so the smallest feasible value is the boundary.
- **[Median of two sorted arrays](/median-of-two-sorted-arrays/).** The first cut of the shorter array whose left part is too large is found with the same loop.

## Variations

- **Last false.** The last index where $P$ is false is FIRST-TRUE$(lo, hi, P) - 1$. This gives "the largest item less than $x$" and "the last copy of $x$".
- **Closed range.** Keep $[lo, hi]$ with $hi = n - 1$, loop while $lo \le hi$, and keep the answer in a separate variable that is set when $P(mid)$ is true. This is correct, but it has three places for an off-by-one error instead of one.
- **First and count.** Keep the start $f$ and the size $c$ of the range. While $c > 0$: let $h = \lfloor c/2 \rfloor$; if $P(f + h)$ is false, set $f \gets f + h + 1$ and $c \gets c - h - 1$, else set $c \gets h$. Return $f$. This is the form of `std::lower_bound` in the common C++ libraries, and the base of the [branchless binary search](/branchless-binary-search/).
- **Real numbers.** On a real interval, halve until the length is below a tolerance. See [binary search on real numbers](/binary-search-on-real-numbers/) and the [bisection method](/bisection-method/).
- **Unbounded range.** When $hi$ is not known, double a step until $P$ becomes true, then use the template on the last interval. This is [exponential search](/exponential-search/).
- **Other layouts.** The same boundary search on an array in breadth-first order is the [Eytzinger layout](/eytzinger-layout/).

## Pitfalls

- **An infinite loop with $lo \gets mid$.** If line L4 sets $lo \gets mid$ instead of $mid + 1$, then for $hi = lo + 1$ the midpoint is $mid = lo$ and the range never shrinks. In a "last true" search, which does set $lo \gets mid$, the midpoint must round up: $mid = lo + \lceil (hi - lo)/2 \rceil$.
- **$hi \gets mid - 1$.** With the half-open range, line L3 must keep $mid$ in the range, since $mid$ may be the answer. Setting $hi \gets mid - 1$ loses it.
- **Starting with $hi = n - 1$.** The answer can be $n$ (all items less than $x$). With the half-open template, $hi$ starts at $n$. Line L2 never reads index $n$, because $mid < hi$.
- **Reading $A[\ell]$ without a test.** The result can be $n$, which is not an index. Test $\ell < n$ first.
- **A test that is not monotone.** If $P$ is true, then false, then true again, the loop returns some boundary, not the first true index. The test must be monotone on the whole range, which for a lower bound means that $A$ must be sorted.
- **Swapping $<$ and $\le$.** The lower bound moves past items $< x$; the upper bound moves past items $\le x$. Using the wrong one gives the other boundary, and the difference shows only on arrays with copies of $x$.
- **Overflow.** Use $lo + \lfloor (hi - lo)/2 \rfloor$, not $\lfloor (lo + hi)/2 \rfloor$, in languages with fixed-size integers.

## Exercises

1. Write the integer square root $\lfloor \sqrt{m} \rfloor$ as FIRST-TRUE$(0, m + 1, t \mapsto t^2 > m) - 1$, and check it for $m = 0, 1, 2, 3, 4, 99, 100$.
2. A sorted array holds 0 and 1 values, all 0 first. Count the 1 values with one call of the template.
3. Given sorted arrays of start times and end times of $n$ intervals, count the intervals that contain a point $p$ with two calls, using that an interval $[s, e)$ contains $p$ when $s \le p$ and $e > p$.
4. Show that LOWER-BOUND and UPPER-BOUND make the same sequence of tests until the first $mid$ with $A[mid] = x$, and use this to write EQUAL-RANGE with fewer tests than two separate searches.

## References
