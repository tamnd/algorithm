---
tag: E7GXER
kind: technique
slug: difference-array
name: Difference array
aliases:
- Imos method
- delta array
- difference sequence
area: sequences/prefix-sums-and-differences
level: intro
summary: Store d[i]=a[i]-a[i-1]; a range add becomes two point updates, and one prefix-sum pass recovers the array.
prereqs: [prefix-sums]
see_also: [range-update-point-query, two-dimensional-difference-array, prefix-sums, telescoping-sum, finite-differences, fenwick-tree, range-update-range-query, sweep-line-technique]
sources:
  - url: https://cses.fi/book/book.pdf
    title: Antti Laaksonen, Competitive Programmer's Handbook
    locator: Chapter 9, Range queries, Section 9.4 Additional techniques (range updates with a difference array and a binary indexed tree)
  - url: https://imoz.jp/algorithms/imos_method.html
    title: Kentaro Imajo, Imos method (in Japanese), 2012
    locator: the one-dimensional method, the two-dimensional method, and the higher-order method for piecewise polynomial updates
  - book: isbn:9780201558029
    title: Graham, Knuth and Patashnik, Concrete Mathematics, second edition
    locator: Section 2.6, Finite and infinite calculus (the difference operator and the fundamental theorem of finite calculus)
---

A difference array stores, for an [array](/array/) $a[0 \ldots n-1]$, the array $d$ with $d[0] = a[0]$ and $d[i] = a[i] - a[i-1]$ for $1 \le i < n$, so that $a$ is the array of [prefix sums](/prefix-sums/) of $d$. Adding a constant $c$ to every item of a range $a[l \ldots r-1]$ changes only two entries of $d$: $d[l]$ grows by $c$ and $d[r]$ drops by $c$. So $m$ range additions cost $O(m)$ time, and one prefix-sum pass of $\Theta(n)$ time rebuilds $a$. It solves the offline form of the [range update point query](/range-update-point-query/) problem, and in competitive programming it is often called the Imos method.

## In plain words

Instead of the values of a list, keep the steps between neighbors: how much each value goes up or down from the one before it. You can rebuild the values by walking from the left and adding up the steps.

Now suppose you must add five to every value in a long stretch. Inside the stretch, each value goes up by five and so does its left neighbor, so the steps between them do not change. Only two steps change: the step into the stretch goes up by five, and the step out of the stretch goes down by five. So a change to a whole stretch costs two small edits. After all the changes, one walk with a running total gives the final values.

## When it applies

- **Many range updates, few reads.** All the additions come first, and the reads come after them. This is the offline form of [range update point query](/range-update-point-query/).
- **The update is "add $c$ to a range".** Addition has an inverse, which the second point update needs. A range *assignment* or a range *maximum* is not of this form.
- **Coverage counts.** "How many of these intervals cover point $x$" is a range add of $+1$ per interval, then a prefix sum. The maximum of the result is the maximum overlap of the intervals.
- **Signals that it does not apply.** Reads mix with updates and both must be fast: keep $d$ in a [Fenwick tree](/fenwick-tree/), so a read is a prefix sum of $d$ in $O(\log n)$. The coordinates are huge and sparse: sort the $2m$ events instead, which is a [sweep](/sweep-line-technique/).

## The template

The ranges are half-open. The array $d$ has length $n + 1$, so that $d[r]$ exists for $r = n$; the entry $d[n]$ is never read back.

```pseudo id=main
RANGE-ADDS(a[0 .. n − 1], updates)        ▷ updates: a list of (l, r, c) with 0 ≤ l ≤ r ≤ n
L1  d[0] ← a[0]; d[n] ← 0
L2  for i ← 1 to n − 1 do d[i] ← a[i] − a[i − 1]
L3  for each (l, r, c) in updates do
L4      d[l] ← d[l] + c                    ▷ the step into the range
L5      d[r] ← d[r] − c                    ▷ the step out of the range
L6  s ← 0
L7  for i ← 0 to n − 1 do
L8      s ← s + d[i]; a[i] ← s             ▷ prefix sums rebuild a
L9  return a
```

When $a$ starts as all zeros, lines L1 and L2 just set $d$ to zeros.

**Why it is correct.** Write $D(i) = d[0] + \cdots + d[i]$. Before line L3, $D(i) = a[0] + \sum_{j=1}^{i} (a[j] - a[j-1]) = a[i]$, a [telescoping sum](/telescoping-sum/). One update $(l, r, c)$ adds $c$ to $D(i)$ exactly when $l \le i$, and subtracts $c$ exactly when $r \le i$. So $D(i)$ grows by $c$ when $l \le i < r$ and does not change otherwise, which is the effect of adding $c$ to $a[l \ldots r-1]$. The updates add up, so after all of them $D(i)$ is the final value of $a[i]$, and lines L6 to L8 write $a[i] = D(i)$.

**Cost.** Lines L1 and L2 take $\Theta(n)$, lines L3 to L5 take $\Theta(m)$ for $m$ updates, and lines L6 to L8 take $\Theta(n)$. The total is $\Theta(n + m)$, against $\Theta(nm)$ in the worst case when each update loops over its range. The extra space is the $n + 1$ entries of $d$.

**A worked example.** Start with $n = 8$ zeros and apply $+3$ to $[1, 4)$, $+2$ to $[2, 6)$ and $+1$ to $[5, 8)$. Then $d = [0, 3, 2, 0, -3, 1, -2, 0, -1]$, where the last entry is $d[8]$. Its prefix sums are $a = [0, 3, 5, 5, 2, 3, 1, 1]$. Position 2 lies in the first two ranges, so it holds $3 + 2 = 5$, and position 5 lies in the last two, so it holds $2 + 1 = 3$.

## Classic examples

From simple to hard:

- **[Range update point query](/range-update-point-query/), offline.** The template above, in $\Theta(n + m)$ time.
- **Maximum overlap of intervals.** Add $+1$ on each interval and take the maximum prefix sum; this is the number of rooms that the [interval partitioning](/interval-partitioning/) problem needs.
- **Flight bookings and car pooling.** Each booking adds seats to a range of stops. A trip is feasible if no stop exceeds the capacity.
- **[Two-dimensional difference array](/two-dimensional-difference-array/).** A rectangle add is four point updates, and a two-dimensional prefix sum rebuilds the grid.
- **[Range update range query](/range-update-range-query/).** Keep $d$ and the array $i \cdot d[i]$ in two [Fenwick trees](/fenwick-tree/). Then $\sum_{j<i} a[j] = i \sum_{j<i} d[j] - \sum_{j<i} j\,d[j]$, so both range adds and range sums cost $O(\log n)$.

## Variations

- **Online point reads.** Store $d$ in a [Fenwick tree](/fenwick-tree/). A range add is two point updates and a read of $a[i]$ is one prefix sum, both $O(\log n)$.
- **Higher order: adding a polynomial.** To add $1, 2, \ldots, m$ to $a[l \ldots l+m-1]$, work on the second difference $e$, whose two prefix-sum passes give $a$. The update is $e[l] \mathrel{+}= 1$, $e[l+m] \mathrel{-}= m + 1$ and $e[l+m+1] \mathrel{+}= m$. For $n = 8$, $l = 2$ and $m = 4$, the two passes give $[0, 0, 1, 2, 3, 4, 0, 0]$. A polynomial of degree $k$ needs the $(k+1)$-th difference and $k + 2$ point updates; see [finite differences](/finite-differences/).
- **Higher dimensions.** In $d$ dimensions a box add is $2^d$ point updates with signs, and $d$ passes of prefix sums, one per axis, rebuild the grid.
- **Sparse coordinates.** With coordinates up to $10^9$, keep the $2m$ events $(l, +c)$ and $(r, -c)$, sort them, and take the running sum in order. This costs $O(m \log m)$ and is independent of $n$; see [coordinate compression](/coordinate-compression/).
- **Other groups.** XOR works the same way, and the two point updates are both $\oplus c$. Multiplication by nonzero numbers modulo a prime works with $d[l] \cdot c$ and $d[r] \cdot c^{-1}$.

## Pitfalls

- **No room for $d[r]$.** With $r = n$, line L5 writes $d[n]$. An array $d$ of length $n$ needs an `if r < n` test; the length $n + 1$ removes it.
- **Inclusive ranges.** For an inclusive range $[l, r]$, the second update goes to $d[r + 1]$, not to $d[r]$. Writing it to $d[r]$ leaves the last item unchanged.
- **Reading $d$ instead of $a$.** The values of $a$ are only valid after the prefix-sum pass. A read between updates must take a prefix sum of $d$.
- **Mixing updates and reads.** Rebuilding $a$ after each update costs $\Theta(n)$ per update. Use a Fenwick tree when the two kinds of operation interleave.
- **Overflow.** A position covered by $m$ updates of size $c$ holds up to $mc$, and $d$ can hold partial sums of either sign. Use 64-bit integers.

## Exercises

1. Given $m$ closed intervals with integer ends in $[0, n)$, find the largest number of intervals that share a point, in $O(n + m)$ time.
2. Show that RANGE-ADDS stays correct when $a$ is not all zeros at the start, and that lines L1 and L2 can be skipped by adding the original $a[i]$ in line L8.
3. Derive the three point updates of the second difference that add $1, 2, \ldots, m$ to a range, and prove that they are correct with two prefix-sum passes.
4. Given $m$ updates "add $c$ to every position $i$ with $l \le i < r$ and $i \equiv l \pmod k$", apply all of them in $O(n + m)$ time for a fixed $k$.
5. Prove that the prefix sum of a difference array and the difference of a prefix-sum array both return the original array.

## References
