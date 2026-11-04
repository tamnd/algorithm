---
tag: AQN873
kind: algorithm
slug: introselect
name: Introselect
aliases:
- introspective selection
area: sorting/selection-and-order-statistics
level: advanced
summary: Quickselect that switches to median of medians when partitioning degrades, giving worst-case linear time.
solves: [selection-problem, median-finding]
model: comparison-model
complexity:
  vars: {n: the number of items}
  time: {worst: Θ(n), expected: Θ(n), best: Θ(n)}
  space: {extra: Θ(n)}
properties: {stable: false, in_place: false, adaptive: false, online: false, deterministic: true, comparison: true, recursive: false}
history:
  year: 1997
  people: [David R. Musser]
  note: Musser introduced introspective sorting and selection in 1997, which run quicksort or quickselect and switch to a method with a worst-case guarantee when the recursion goes badly.
prereqs: [quickselect, median-of-medians]
see_also: [introsort, quickselect, median-of-medians, deterministic-linear-selection, pivot-selection, dutch-national-flag, floyd-rivest-select, heap-select]
sources:
  - paper: "David R. Musser, Introspective sorting and selection algorithms, Software: Practice and Experience 27(8) (1997)"
    locator: pages 983 to 993 (introsort, introselect, and median-of-3 killer sequences)
  - paper: doi:10.1016/S0022-0000(73)80033-9
    title: Manuel Blum, Robert W. Floyd, Vaughan Pratt, Ronald L. Rivest and Robert E. Tarjan, Time bounds for selection, Journal of Computer and System Sciences 7(4) (1973)
    locator: pages 448 to 461 (the linear-time fallback)
  - paper: "M. Douglas McIlroy, A killer adversary for quicksort, Software: Practice and Experience 29(4) (1999)"
    locator: pages 341 to 344 (an adversary that makes any quicksort-like method quadratic)
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Chapter 9, Sections 9.2 and 9.3 (randomized selection and selection in worst-case linear time)
---

Introselect is [quickselect](/quickselect/) with a safety net. It picks each pivot cheaply, here as the median of three items, and watches how fast the range of candidates shrinks; if the partitions stop cutting the range down, it finishes the job with [median of medians](/median-of-medians/), which takes linear time on every input. On typical inputs it runs as fast as quickselect, since the fallback is rarely used or used only on a small range, and on every input it takes $\Theta(n)$ time. David Musser introduced it in 1997 as the selection twin of [introsort](/introsort/).

## In plain words

Quickselect guesses a splitting item, divides the items around it, and keeps only the side that holds the answer. Usually each guess throws away a good part of the items. But a bad run of guesses, or an input built on purpose to fool the guessing rule, can make each step throw away only one or two items, and then the work grows like the square of the input size.

Introselect keeps an eye on the progress. If two steps in a row each keep most of the items, it stops guessing and switches to a slower method whose splitting item is always good. That method is never fooled, so the total work stays proportional to the number of items.

## The problem

Given $n \ge 1$ items with a [total order](/total-order/) and a rank $k$ with $1 \le k \le n$, return the item of rank $k$, the $k$-th entry of the sorted order: the [selection problem](/selection-problem/). The aim is the speed of quickselect on typical inputs together with a linear bound in the worst case.

## The algorithm

$B$ is a copy of the input with 0-based indices, $t = k - 1$ is the target position, and $[lo, hi)$ is the range that must contain position $t$ of the sorted order. A step is *bad* when it keeps more than $3/4$ of the range. MOM-SELECT is [median of medians](/median-of-medians/) and returns the item of a given rank of a list.

```pseudo id=main
INTROSELECT(A[0 .. n−1], k)                ▷ 1 ≤ k ≤ n
L1  B ← a copy of A; lo ← 0; hi ← n; t ← k − 1; bad ← 0
L2  while hi − lo > 1 do
L3      if bad ≥ 2 then return MOM-SELECT(B[lo .. hi−1], t − lo + 1)
L4      x ← the median of B[lo], B[⌊(lo + hi − 1)/2⌋], B[hi − 1]
L5      (p, q) ← PARTITION3(B, lo, hi, x)  ▷ B[lo..p−1] < x, B[p..q−1] = x, B[q..hi−1] > x
L6      if p ≤ t < q then return x
L7      old ← hi − lo
L8      if t < p then hi ← p else lo ← q
L9      if 4(hi − lo) > 3 · old then bad ← bad + 1 else bad ← 0
L10 return B[lo]
```

PARTITION3 is the three-way [Dutch national flag](/dutch-national-flag/) partition of the [partition template](/partition-around-pivot/). Line L4 chooses the pivot among three items of the range, so the pivot is an item of the range and the part equal to it is not empty. Line L6 stops when the target lies among the copies of the pivot. Line L8 keeps the part that holds the target, as in quickselect, and line L9 counts the bad steps in a row. Line L3 is the switch: after two bad steps in a row, the rest of the range goes to median of medians.

## Example

For $A = [31, 41, 59, 26, 53, 58, 97, 93, 23, 84]$ and $k = 5$, so $t = 4$:

| step | range | median of three | parts | kept range | bad |
|---|---|---|---|---|---|
| 1 | $[0, 10)$ | of $31, 53, 84$: $53$ | $4$ below, $1$ equal, $5$ above | $t = 4 = p$: return $53$ | |

The answer $53$ is found in one step. With $k = 1$, the first step also uses the pivot $53$ and keeps the $4$ smaller items, a good step since $4 \cdot 4 \le 3 \cdot 10$; the partition left them as $[31, 41, 23, 26]$, the median of $31$, $41$ and $26$ is $31$, and the next step keeps $[26, 23]$, also good. The last step uses the pivot $26$ and keeps $[23]$, which line L10 returns.

**An input that defeats the median of three.** McIlroy's adversary chooses the values of the items while the algorithm runs, so that each pivot is close to an end of the range. Against plain median-of-three quickselect with three-way partition, for the median of $n = 8000$ items it forced $3000.75n$ comparisons, which is quadratic. Against introselect it forced $13.7n$, since after two bad steps the range goes to median of medians.

## Correctness

At each test of line L2, the items of $B[0 \ldots lo-1]$ are at most each item of $B[lo \ldots hi-1]$, which are at most each item of $B[hi \ldots n-1]$, and $lo \le t < hi$. This is the invariant of [quickselect](/quickselect/), and the three-way partition keeps it: the kept part is the part of the range that holds position $t$ of the sorted order. So the item of rank $t - lo + 1$ of the range is the answer, which is what line L3 asks of median of medians, which is correct by its own proof; line L6 returns a pivot copy that lies at position $t$; and line L10 returns the only item of a range of size one. Each step that does not return removes at least the copies of the pivot, so the loop stops. The full proof is in the proof file below.

## Complexity

Let $s_0 = n$ and let $s_1, s_2, \ldots$ be the sizes of the range after each step. A step on a range of size $s$ costs $O(s)$: three comparisons for the pivot and at most $2s$ in the partition.

- **Worst case, $\Theta(n)$.** A bad step can be followed only by a good step or by the switch, since two bad steps in a row trigger line L3. A good step keeps at most $3/4$ of its range. So among any two steps in a row at least one is good, and $s_{i+2} \le \tfrac{3}{4} s_i$. The sum of the sizes is then at most $(s_0 + s_1) \cdot (1 + \tfrac{3}{4} + \tfrac{9}{16} + \cdots) \le 8n$. The call to median of medians, if any, is on a range of at most $n$ items and costs $O(n)$. So the total is $O(n)$, and reading the input costs $\Omega(n)$.
- **Measured.** On random lists of $10^5$ distinct items, finding the median made $4.9n$ comparisons on average over $20$ runs, against $4.3n$ for the same loop with the switch turned off. The three-way partition makes two comparisons for each item that is not below the pivot, which is why both counts are above the $2.75n$ of median-of-three quickselect with a two-way partition. Against McIlroy's adversary the counts were $13.4n$ for $n = 2000$ and $13.7n$ for $n = 8000$.
- **Space.** This version copies the input and the fallback builds lists, so $\Theta(n)$ extra space. An in-place version partitions $A$ itself and uses an in-place median of medians, with $O(1)$ extra space besides the recursion of the fallback.

## Properties

- **Deterministic.** The pivot rule and the switch use no randomness, so each input has a fixed cost, and the bound holds for every input.
- **Not stable.** Partitioning changes the order of equal items.
- **Comparison based.** It uses only comparisons between items.
- **Not recursive in its main loop.** The loop is iterative; only the fallback recurses.

## Variants and improvements

- **Other switch rules.** Musser's rule bounds the total work: switch when the sum of the sizes of the ranges partitioned so far passes a constant times $n$, or when the depth passes a constant times $\lg n$. Any rule that forces a constant-factor shrink every few steps gives linear time. A rule based only on depth, with a fallback that is not linear, gives $O(n \log n)$.
- **Other fallbacks.** Some libraries switch to [heap-based selection](/heap-select/) instead, which is simpler but gives $O(n \log n)$ in the worst case, not $O(n)$. The C++ function `std::nth_element` in several standard libraries works this way.
- **Random pivots.** With a random pivot, quickselect is already fast in expectation, and the switch only protects against bad luck; with a median of three the switch also protects against crafted inputs.
- **Better samples.** The pivot can be the median of a larger sample, or chosen as in [Floyd-Rivest selection](/floyd-rivest-select/), to cut the average number of comparisons, with the same fallback for safety.

## When to use it

Use it as the default selection routine of a library: when the input may come from an adversary, as in a server that sorts or ranks user data, or when a worst-case bound is required but the speed of quickselect is wanted. If only the expected time matters and the pivot is random, plain quickselect is simpler. If comparisons are expensive and the input is large, Floyd-Rivest selection makes fewer comparisons on average.

## Pitfalls

- **A switch that never fires.** A rule that resets too easily, for example after any step that removes at least one item, does not stop the quadratic case. The rule must demand a constant-factor shrink.
- **A two-way partition with many equal items.** If all items are equal, a two-way partition puts them all on one side and each step removes one item. The three-way partition removes all copies of the pivot at once.
- **The wrong rank in the fallback.** The fallback works on the range $[lo, hi)$, so the rank it needs is $t - lo + 1$, not $k$.
- **Calling a heap fallback linear.** Implementations that fall back to a heap have an $O(n \log n)$ worst case.

## Implementations

## History

David Musser described introsort and introselect in "Introspective sorting and selection algorithms" in Software: Practice and Experience in 1997. He showed median-of-3 killer inputs that make median-of-three quicksort and quickselect quadratic, and proposed to monitor the recursion and switch to a method with a worst-case bound: heapsort for sorting, and a linear-time selection, such as the one of Blum, Floyd, Pratt, Rivest and Tarjan (1973), for selection. McIlroy's adversary of 1999 showed that any quicksort-like method that picks pivots by a fixed rule can be forced into quadratic time, which is the case that the switch handles.

## References
