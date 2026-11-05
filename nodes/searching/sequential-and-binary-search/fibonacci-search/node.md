---
tag: 8R17S9
kind: algorithm
slug: fibonacci-search
name: Fibonacci search
aliases:
- Fibonacci search technique
area: searching/sequential-and-binary-search
level: core
summary: Divide-and-conquer search that splits the array at Fibonacci numbers, using only addition and subtraction for index arithmetic.
solves: [search-in-sorted-array]
model: comparison-model
complexity:
  vars: {n: the number of items in the array}
  time: {worst: Θ(log n), average: Θ(log n), best: Θ(log n)}
  space: {extra: Θ(1)}
properties: {deterministic: true, comparison: true, recursive: false, in_place: true}
prereqs: [binary-search, fibonacci-numbers]
see_also: [binary-search, uniform-binary-search, fibonacci-search-unimodal, golden-section-search, fibonacci-numbers, zeckendorf-theorem, lower-and-upper-bound-search, search-in-sorted-array]
sources:
  - paper: doi:10.1145/367487.367496
    title: David E. Ferguson, Fibonaccian searching, Communications of the ACM 3(12) (1960)
    locator: p. 648
  - book: isbn:9780201896855
    title: Donald E. Knuth, The Art of Computer Programming, Volume 3, second edition
    locator: Section 6.2.1, Algorithm F (Fibonaccian search) and the Fibonaccian tree
  - paper: doi:10.1007/BF01933527
    title: K. J. Overholt, Efficiency of the Fibonacci search method, BIT Numerical Mathematics 13(1) (1973)
    locator: the mean and the maximum search length compared with binary search
---

Fibonacci search is a form of [binary search](/binary-search/) that splits the range at a [Fibonacci number](/fibonacci-numbers/) instead of at the middle. A range of $F_k - 1$ positions is cut into parts of $F_{k-1} - 1$ and $F_{k-2} - 1$ positions, about $62\%$ and $38\%$ of the range, so that both parts again have the size of a Fibonacci number minus one. The index of the next probe is then found with one addition or subtraction, with no division and no shift. It makes at most about $\log_\varphi n \approx 1.44 \lg n$ comparisons, where $\varphi = (1 + \sqrt{5})/2$, and on average about 4 percent more than binary search. Ferguson described it in 1960, and Knuth gives it as Algorithm F.

## In plain words

Binary search cuts the list in two equal halves. Fibonacci search cuts it in two parts of unequal size, one part a bit larger than the other. The sizes come from the Fibonacci numbers 1, 2, 3, 5, 8, 13, 21, in which each number is the sum of the two before it.

A list of 12 items is treated as 13 positions minus one. It is cut into 8 and 5. The part of 8 is then cut into 5 and 3, the part of 5 into 3 and 2, and so on. Because the next cut is always the previous number in the row, you get it by a subtraction. Older computers had no fast division, so this was faster than halving. The cost is a few more looks than binary search.

## The problem

The input is an array $A[0 \ldots n-1]$, $n \ge 0$, sorted so that $A[0] \le \cdots \le A[n-1]$, and a key $x$. The output is the smallest index $i$ with $A[i] = x$, or NIL when $x$ is not in $A$. This is [search in a sorted array](/search-in-sorted-array/), with the first occurrence as the answer. The algorithm uses only comparisons of $x$ with items, and only additions and subtractions on indices.

The Fibonacci numbers are $F_0 = 0$, $F_1 = 1$ and $F_k = F_{k-1} + F_{k-2}$.

## The algorithm

The search looks for the [lower bound](/lower-bound-query/) $\ell$ of $x$, the number of items less than $x$. It keeps a start $lo$ and two consecutive Fibonacci numbers $f = F_k$ and $g = F_{k-1}$, and the range is the $f - 1$ positions from $lo$. Positions at index $n$ or more are treated as $+\infty$, so the range can extend past the end of the array.

```pseudo id=main
FIBONACCI-SEARCH(A, x)
L1  g ← 0, f ← 1                         ▷ g = F(k − 1), f = F(k)
L2  while f − 1 < n do (g, f) ← (f, f + g)  ▷ the smallest F(k) with F(k) − 1 ≥ n
L3  lo ← 0                               ▷ the lower bound of x is in [lo, lo + f − 1]
L4  while f > 1 do
L5      mid ← lo + g − 1                 ▷ the left part has g − 1 positions
L6      if mid < n and A[mid] < x then
L7          lo ← mid + 1, (f, g) ← (f − g, 2g − f)   ▷ keep the right part, F(k − 2) − 1 positions
L8      else (f, g) ← (g, f − g)                       ▷ keep the left part, F(k − 1) − 1 positions
L9  if lo < n and A[lo] = x then return lo
L10 return NIL
```

Line L2 finds the size. Lines L5 to L8 are one step. The probe $mid$ is the position just after the left part of $g - 1 = F_{k-1} - 1$ positions. If $A[mid] < x$, the lower bound is past $mid$, and the right part has $F_k - 1 - F_{k-1} = F_{k-2} - 1$ positions; the new pair is $(F_{k-2}, F_{k-3})$, and $F_{k-3} = 2F_{k-1} - F_k$. Otherwise the lower bound is at most $mid$, and the new range is the left part, of $F_{k-1} - 1$ positions, with the pair $(F_{k-1}, F_{k-2})$. A probe at $mid \ge n$ needs no comparison, since the item there counts as $+\infty$.

## Example

The array has $n = 12$ items, so line L2 stops at $f = F_7 = 13$, $g = F_6 = 8$:

| index | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| $A$ | 3 | 8 | 11 | 15 | 19 | 23 | 27 | 31 | 35 | 40 | 44 | 50 |

Search for $x = 40$:

| step | $lo$ | $f$ | $g$ | $mid$ | test | result |
|---|---|---|---|---|---|---|
| 1 | 0 | 13 | 8 | 7 | $A[7] = 31 < 40$ | right: $lo = 8$, $(f, g) = (5, 3)$ |
| 2 | 8 | 5 | 3 | 10 | $A[10] = 44 < 40$ is false | left: $(f, g) = (3, 2)$ |
| 3 | 8 | 3 | 2 | 9 | $A[9] = 40 < 40$ is false | left: $(f, g) = (2, 1)$ |
| 4 | 8 | 2 | 1 | 8 | $A[8] = 35 < 40$ | right: $lo = 9$, $(f, g) = (1, 0)$ |
| 5 | 9 | | | | $A[9] = 40$ | return 9 |

That is 4 steps and the final equality test, 5 comparisons. A search for $x = 12$ goes left at $A[7]$, left at $A[4] = 19$, right at $A[2] = 11$, and left at $A[3] = 15$, ends with $lo = 3$, and finds $A[3] = 15 \ne 12$: also 5 comparisons, and the answer NIL.

## Correctness

Let $\ell$ be the lower bound of $x$. Before each test of line L4, $f = F_k$ and $g = F_{k-1}$ for some $k \ge 1$, and $lo \le \ell \le lo + f - 1$, where items at index $n$ or more count as $+\infty$. At the start $lo = 0$ and $f - 1 \ge n \ge \ell$. In a step, if $mid < n$ and $A[mid] < x$, then $\ell > mid$, and the new range $[mid + 1, lo + f - 1]$ has $F_{k-2} - 1$ positions. Otherwise $A[mid] \ge x$ (or $mid \ge n$, where the item counts as $+\infty$), so $\ell \le mid = lo + F_{k-1} - 1$, which is the end of the new range. Each step lowers $k$ by 1 or 2, and the loop stops when $f = 1$, that is, when the range is the one position $lo$. Then $lo = \ell$, and line L9 returns it when it holds $x$. The full proof is below.

## Complexity

Count the comparisons of items. Let $F_K$ be the smallest Fibonacci number with $F_K \ge n + 1$.

- **Worst case.** Each step lowers $k$ by at least 1, from $K$ to at most 2, so there are at most $K - 2$ steps and $K - 1$ comparisons with the final test. Since $F_{K-1} \le n$ and $F_{K-1} \ge \varphi^{K-3}$, this is $K - 2 \le \log_\varphi n + 1 \approx 1.44 \lg n + 1$. The worst case is a key that goes left at each step, which takes exactly $K - 2$ steps.
- **Average case.** A step that goes right costs one comparison and removes two levels, so the average is less than the worst case. When $n + 1$ is a Fibonacci number, the average is about 4 percent more than that of binary search.
- **Best case.** A search that goes right at each step takes about $K/2$ steps, so even the best case is $\Theta(\log n)$ for this two-way version. Only the final test can be avoided.
- **Space.** Four integers: $\Theta(1)$.

The table counts the comparisons of the loop alone (without line L9), on the array $[0, 2, \ldots, 2n - 2]$, over the $2n + 1$ keys $-1, 0, 1, \ldots, 2n - 1$. Each $n$ here has $n + 1$ a Fibonacci number. The binary search is the half-open lower bound search.

| $n$ | 20 | 143 | 986 | 10945 |
|---|---|---|---|---|
| Fibonacci, worst | 6 | 10 | 14 | 19 |
| binary, worst | 5 | 8 | 10 | 14 |
| Fibonacci, average | 4.610 | 7.474 | 10.361 | 13.978 |
| binary, average | 4.488 | 7.223 | 9.963 | 13.503 |
| ratio of averages | 1.027 | 1.035 | 1.040 | 1.035 |

For other $n$ the range is padded up to $F_K - 1$ positions, and the probes past the end cost nothing but the cuts no longer fit the array: for $n = 1000$, with $F_K = 1597$, the worst case is 15 and the average 11.28, against 10 and 9.98.

## Properties

- **No division.** The next probe is found with additions and subtractions only. This mattered on machines without a fast divide or shift.
- **Unequal cuts.** The left part is about $1/\varphi \approx 0.618$ of the range. The probes move by smaller steps as the search goes on, which can help on memory where nearby reads are cheaper.
- **First occurrence.** It finds the lower bound, so the result is the smallest index of $x$.
- **Comparison-based and in place.** It uses only $<$ and $=$ on items, and it does not change the array.

## Variants and improvements

- **Three-way form.** Knuth's Algorithm F compares $x$ with $A[mid]$ for $<$, $=$ and $>$ and stops at once on a match. Its search tree is the Fibonacci tree of order $k$. It is the form in which the 4 percent figure was first derived.
- **[Uniform binary search](/uniform-binary-search/).** Another way to avoid the division of the midpoint: precompute a table of the step sizes, so each step is one addition.
- **[Fibonacci search for a unimodal function](/fibonacci-search-unimodal/).** A different method with the same name, by Kiefer: it finds the maximum of a unimodal function, and there the Fibonacci cuts are optimal, since one of the two probes is reused in the next step. Its limit is [golden section search](/golden-section-search/).

## When to use it

Today Fibonacci search is mainly of historical and teaching value. On a modern processor a shift is as cheap as an addition, so the midpoint of binary search costs nothing extra, and binary search makes fewer comparisons. Fibonacci search can still be a good choice when division or shift is expensive, on very simple hardware, or when an access far from the last probe costs more than one close to it, because its later steps are short.

## Pitfalls

- **Wrong pair after a right move.** After the probe at $lo + F_{k-1} - 1$, the right part has $F_{k-2} - 1$ positions, not $F_{k-1} - 1$. The new pair is $(F_{k-2}, F_{k-3}) = (f - g, 2g - f)$.
- **Reading past the end.** The padded range can extend past $n - 1$. Line L6 tests $mid < n$ before it reads $A[mid]$.
- **Stopping with $f = 2$.** The range of $F_3 - 1 = 1$ position still needs a step, because the answer can be $lo$ or $lo + 1$. The loop runs while $f > 1$.
- **Starting with the wrong size.** Line L2 must reach $F_k - 1 \ge n$, not $F_k \ge n$; with $F_k = n$ the last position $n$, the answer for a key larger than all items, is outside the range.
- **Confusing the two Fibonacci searches.** The search in a sorted array and the search for the maximum of a unimodal function are different algorithms.

## Implementations

## History

Ferguson described Fibonaccian searching for sorted tables in Communications of the ACM in 1960. Kiefer had used the Fibonacci numbers in 1953 for the search of the maximum of a unimodal function, a different problem. Knuth analyzes the method as Algorithm F in Section 6.2.1, with its Fibonacci tree, and Overholt compared its mean and maximum cost with binary search in 1973.

## References
