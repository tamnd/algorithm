---
tag: MG89TJ
kind: algorithm
slug: uniform-binary-search
name: Uniform binary search
aliases:
- Shar's method
area: searching/sequential-and-binary-search
level: advanced
summary: Binary search driven by a precomputed table of offsets rather than per-step bound updates; suits repeated searches in a fixed array.
solves: [search-in-sorted-array]
model: comparison-model
complexity:
  vars: {n: the number of items in the array}
  time: {worst: Θ(log n), average: Θ(log n), best: Θ(log n)}
  space: {extra: Θ(1)}
properties: {deterministic: true, comparison: true, recursive: false, in_place: true}
prereqs: [binary-search, lower-and-upper-bound-search]
see_also: [binary-search, lower-and-upper-bound-search, branchless-binary-search, eytzinger-layout, fibonacci-search, sorted-search-lower-bound, search-in-sorted-array]
sources:
  - book: isbn:9780201896855
    title: Donald E. Knuth, The Art of Computer Programming, Volume 3, second edition
    locator: Section 6.2.1, Algorithm U (uniform binary search), Algorithm C (with a table of offsets) and the method of Shar
  - book: isbn:9780201657883
    title: Jon Bentley, Programming Pearls, second edition
    locator: Column 9, Code tuning (a binary search for n = 1000 with fixed power-of-two steps, unrolled)
---

Uniform binary search is a [binary search](/binary-search/) that keeps one position and a step size instead of two bounds. The step sizes do not depend on the data: they come from a fixed table that depends only on $n$, so they can be computed once and reused for every search in the same array, or written into unrolled code. The form on this page, Shar's method, uses one first step of $n - p$, where $p$ is the largest power of 2 with $p \le n$, and then the steps $p/2, p/4, \ldots, 1$. Every search makes exactly $\lfloor \lg n \rfloor + 1 = \lceil \lg(n+1) \rceil$ two-way comparisons, which is the [lower bound](/sorted-search-lower-bound/) for search in a sorted array, plus one equality test, and returns the first index of the key. Knuth's three-way Algorithm U and its table form, Algorithm C, are covered under the variants.

## In plain words

In a normal binary search you keep two marks and look in the middle between them. Each time, you work out the new middle.

In a uniform binary search you keep one mark and a step length. You look one step ahead of the mark. If what you see is still too small, you move the mark there. Then you halve the step and look again. The steps are always the same list, such as 512, 256, 128 and so on down to 1, whatever you search for. Only the choice "move or stay" depends on the key.

Because the list of steps is fixed, a program can store it once, or even write each step into the code, with no loop at all.

## The problem

The input is an array $A[0 \ldots n-1]$, $n \ge 0$, with $A[0] \le \cdots \le A[n-1]$, and a key $x$. The output is the smallest index $i$ with $A[i] = x$, or NIL when $x$ is not in $A$. This is [search in a sorted array](/search-in-sorted-array/). The algorithm uses only comparisons of $x$ with items.

In the reasoning below, $A[-1]$ is read as $-\infty$ and $A[n]$ as $+\infty$. The algorithm never reads these two cells.

## The algorithm

```pseudo id=main
UNIFORM-BINARY-SEARCH(A, x)
L1  if n = 0 then return NIL
L2  p ← 2^⌊lg n⌋                       ▷ the largest power of 2 with p ≤ n
L3  b ← −1                              ▷ A[b] < x, with A[−1] = −∞
L4  if A[p − 1] < x then b ← n − p      ▷ the first step
L5  s ← p                               ▷ invariant: A[b] < x ≤ A[b + s], with A[n] = +∞
L6  while s > 1 do
L7      s ← s / 2
L8      if A[b + s] < x then b ← b + s
L9  if b + 1 < n and A[b + 1] = x then return b + 1
L10 return NIL
```

The comment on line L5 is the [loop invariant](/loop-invariant/): the boundary between the items $< x$ and the items $\ge x$ lies after $b$ and at most at $b + s$. Line L4 sets it up with a window of size $p$. If $A[p - 1] \ge x$, the window is $(-1, p - 1]$. If $A[p - 1] < x$, the window $(n - p, n]$ is the last $p$ positions, and it is safe since $n - p \le p - 1$, so $A[n - p] \le A[p - 1] < x$. Lines L6 to L8 halve the window. At the end $s = 1$, so $b + 1$ is the [lower bound](/lower-bound-query/) of $x$, and line L9 tests it, as in [lower and upper bound search](/lower-and-upper-bound-search/).

The step sizes are $n - p$ or $0$ for the first step, and then $p/2, \ldots, 1$. They depend only on $n$. That is what "uniform" means here.

## Example

The array has $n = 10$ items, so $p = 8$:

| index | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 |
|---|---|---|---|---|---|---|---|---|---|---|
| $A$ | 2 | 4 | 6 | 8 | 10 | 12 | 14 | 16 | 18 | 20 |

Search for $x = 14$ and for $x = 19$:

| line | $s$ | $x = 14$: test | $b$ | $x = 19$: test | $b$ |
|---|---|---|---|---|---|
| L4 | 8 | $A[7] = 16 < 14$ is false | $-1$ | $A[7] = 16 < 19$ | $10 - 8 = 2$ |
| L8 | 4 | $A[3] = 8 < 14$ | 3 | $A[6] = 14 < 19$ | 6 |
| L8 | 2 | $A[5] = 12 < 14$ | 5 | $A[8] = 18 < 19$ | 8 |
| L8 | 1 | $A[6] = 14 < 14$ is false | 5 | $A[9] = 20 < 19$ is false | 8 |
| L9 | | $A[6] = 14$ | return 6 | $A[9] = 20 \ne 19$ | NIL |

Both searches make $\lfloor \lg 10 \rfloor + 1 = 4$ order comparisons and one equality test. So does every other search in this array.

## Correctness

Before each test of line L6, $-1 \le b$, $b + s \le n$, $s$ is a power of 2, and $A[b] < x \le A[b + s]$, with the two virtual cells. At the start, if $A[p - 1] \ge x$ then $b = -1$ and $b + s = p - 1$. Otherwise $b = n - p$, $b + s = n$, and $A[b] \le A[p - 1] < x$ because $n < 2p$ gives $b \le p - 1$. A pass halves $s$ and reads $A[b + s]$ with the new $s$; this index lies in $[b + 1, b + 2s - 1] \subseteq [0, n - 1]$, so it is a real cell. If $A[b + s] < x$, the new $b$ is $b + s$ and the upper side keeps $A[b + 2s]$; otherwise $b$ stays and $x \le A[b + s]$. So the invariant holds. At the end $s = 1$, so all items before $b + 1$ are $< x$ and all from $b + 1$ on are $\ge x$: $b + 1$ is the lower bound $\ell$, and line L9 returns the first copy of $x$ or NIL. The full proof is below.

## Complexity

- **Exact count.** Line L4 makes one order comparison and the loop makes $\lg p = \lfloor \lg n \rfloor$, so every search with $n \ge 1$ makes exactly $\lfloor \lg n \rfloor + 1$ order comparisons, plus at most one equality test. Since $\lfloor \lg n \rfloor + 1 = \lceil \lg(n+1) \rceil$, this is the worst-case lower bound for two-way comparisons.
- **Worst, average and best case.** All equal $\lceil \lg(n+1) \rceil$, so the time is $\Theta(\log n)$ in all three cases. A plain lower bound loop takes $\lfloor \lg(n+1) \rfloor$ or $\lceil \lg(n+1) \rceil$ steps; over the $n + 1$ outcomes on distinct keys its average is 3.55 for $n = 10$, 6.73 for $n = 100$ and 9.98 for $n = 1000$, against 4, 7 and 10 here. So the uniform form spends less than one extra comparison on average.
- **Space.** Two indices and the step: $\Theta(1)$. The table form needs $\lfloor \lg n \rfloor + 2$ stored offsets.

| $n$ | 10 | 100 | 1000 | $10^6$ |
|---|---|---|---|---|
| $p$ | 8 | 64 | 512 | 524288 |
| first step $n - p$ | 2 | 36 | 488 | 475712 |
| order comparisons, every search | 4 | 7 | 10 | 20 |

## Properties

- **Data-independent steps.** The sequence of step sizes depends only on $n$, and the number of loop passes is the same for every key. This makes the loop easy to unroll and the time the same for every input, which matters for [branchless](/branchless-binary-search/) and constant-time code.
- **First occurrence.** It computes the lower bound, so it returns the smallest index of $x$.
- **Two-way.** It uses only $<$ in the loop and one $=$ at the end.
- **In place.** It does not change the array.

## Variants and improvements

- **Knuth's Algorithm U, three-way.** Keep a position $i$ and a count $m$. Start with $i = \lceil n/2 \rceil$ and $m = \lfloor n/2 \rfloor$ in a 1-based array. Compare $x$ with $A[i]$: on equality stop; otherwise, if $m = 0$ fail, else move $i$ left or right by $\lceil m/2 \rceil$ and set $m \gets \lfloor m/2 \rfloor$. It stops early on a match, so it returns some copy of $x$, not the first.
- **Knuth's Algorithm C, the table.** Algorithm U with the step sizes stored in a table $\delta_j = \lfloor (n + 2^{j-1}) / 2^j \rfloor$ for $j = 1, \ldots, \lfloor \lg n \rfloor + 2$. The search starts at $i = \delta_1$ and moves by $\delta_2, \delta_3, \ldots$ until the next entry is 0. For $n = 10$ the table is $5, 3, 1, 1, 0$, and for $n = 16$ it is $8, 4, 2, 1, 1, 0$. Checked by a script for every $n < 400$: the method finds every key with at most $\lfloor \lg n \rfloor + 1$ three-way comparisons, but for even $n$ the walk can step to position 0, before the first item. That position must act as $-\infty$, either as a stored sentinel or as a test in the code, as in the implementation of this page.
- **Unrolled code.** For a fixed $n$, write the steps as straight-line code: one test for the first step, then one test for each of $p/2, \ldots, 1$. Bentley tunes a search for $n = 1000$ this way, with $p = 512$ and the first step 488.
- **[Branchless binary search](/branchless-binary-search/).** The same idea with a conditional move in place of the branch of line L8.
- **[Eytzinger layout](/eytzinger-layout/).** Store the array in the order of the probes, so that the probes of the first levels are close in memory.
- **[Fibonacci search](/fibonacci-search/).** A search whose steps are Fibonacci numbers instead of powers of 2, also from a fixed table.

## When to use it

Use the uniform form when many searches run on arrays of one fixed size, so that the table or the unrolled code can be built once, or when the search must take the same number of steps for every key. It is also a clean way to write a lower bound search with one index instead of two. For a single search in a general program, the plain [lower bound loop](/lower-and-upper-bound-search/) is just as fast and more familiar.

## Pitfalls

- **First step $b \gets n - p - 1$.** With this first step the window after line L4 is $(n - p - 1, n - 1]$, which misses the answer $n$ when all items are $< x$, for example $n = p$ and $x$ larger than all items. The first step is $n - p$, and the window is $(n - p, n]$.
- **Reading the virtual cells.** The invariant uses $A[-1]$ and $A[n]$, but the loop never reads them: the index $b + s$ of line L8 lies between $b + 1$ and $b + 2s - 1$. Code that tests $A[b + 2s]$ or starts with $b = 0$ breaks this.
- **Position 0 in Algorithm C.** In Knuth's three-way table method the walk can reach position 0 for even $n$. Without a sentinel $-\infty$ there, a language with negative indices, such as Python, reads the last item instead, and other languages read memory before the array.
- **$p$ by floating point.** Compute $p = 2^{\lfloor \lg n \rfloor}$ with integer operations, such as `1 << (n.bit_length() - 1)`, not with a floating-point logarithm, which can round at exact powers of 2.
- **Empty array.** For $n = 0$ there is no $p$; line L1 returns at once.

## Implementations

## History

Knuth presents the uniform binary search as Algorithm U in Section 6.2.1, with the table form as Algorithm C and the variant with power-of-two steps that he credits to L. E. Shar. Bentley uses the power-of-two form in Programming Pearls as an example of code tuning, unrolled for an array of 1000 items.

## References
