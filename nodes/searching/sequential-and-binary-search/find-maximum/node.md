---
tag: AQ5046
kind: problem
slug: find-maximum
name: Finding the maximum
aliases:
- Computing the maximum
area: searching/sequential-and-binary-search
level: intro
summary: Scans a list once, keeping the largest value seen so far, to find the maximum element in linear time.
model: comparison-model
complexity:
  vars: {n: the number of items}
  time: {worst: Θ(n)}
prereqs: [array, total-order, loop-invariant]
see_also: [max-finding-lower-bound, minimum-and-maximum-finding, hiring-problem, second-largest-lower-bound, tournament-method, selection-problem, peak-finding, unimodal-maximum]
sources:
  - book: isbn:9780201896831
    title: Donald E. Knuth, The Art of Computer Programming, Volume 1, third edition
    locator: Section 1.2.10, Algorithm M (find the maximum) and the analysis of the number of changes of the maximum
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Section 9.1, Minimum and maximum
  - book: isbn:9780201896855
    title: Donald E. Knuth, The Art of Computer Programming, Volume 3, second edition
    locator: Section 5.3.3, Minimum-comparison selection (the maximum, and the largest and second largest)
---

Finding the maximum asks, for a non-empty sequence of $n$ items from a [total order](/total-order/), for the largest item, or for an index where it occurs. The scan that keeps the largest item seen so far uses exactly $n - 1$ comparisons, and no algorithm in the [comparison model](/comparison-model/) can use fewer: each item other than the maximum must lose at least one comparison. So the problem has the exact cost $n - 1$, one of the few problems where the best algorithm and the lower bound meet exactly for every $n$. It is the simplest case of the [selection problem](/selection-problem/), and its cost of updates is the subject of the [hiring problem](/hiring-problem/).

## In plain words

You want the tallest person in a room. You call the first person to the front. Then each other person in turn stands next to the one at the front. If the new person is taller, they take the place at the front. After everyone has had a turn, the person at the front is the tallest.

Each comparison has a loser, and a loser can never be the tallest. To be sure who is tallest, you must know that every other person is shorter than someone. So every person except one must lose at least once, and each comparison makes only one loser. That is why you cannot do it with fewer comparisons than the number of people minus one.

## Definition

**Input.** A sequence $A[0 \ldots n-1]$ of $n \ge 1$ items from a set with a total order $\le$.

**Output.** An index $m$ with $A[m] \ge A[i]$ for each $i \in \{0, \ldots, n-1\}$, or the value $\max_i A[i]$ itself.

When the maximum occurs more than once, each of its indices is a correct output. The scan below returns the first one with a strict test "$>$", and the last one with "$\ge$". The input must be non-empty; for $n = 0$ the maximum is not defined, and a program must return an error or a chosen value such as $-\infty$.

The cost is the number of comparisons between items.

## Variants

- **Minimum.** The same problem for the order $\ge$.
- **[Minimum and maximum](/minimum-and-maximum-finding/) together.** Compare the items in pairs, then the smaller of each pair with the current minimum and the larger with the current maximum. This uses $\lceil 3n/2 \rceil - 2$ comparisons instead of $2n - 2$, and that is optimal ([max-min lower bound](/max-min-lower-bound/)).
- **Largest and second largest.** A [tournament](/tournament-method/) finds both with $n + \lceil \lg n \rceil - 2$ comparisons, which is optimal ([second-largest lower bound](/second-largest-lower-bound/)).
- **The $k$-th largest.** The general [selection problem](/selection-problem/), in $\Theta(n)$ time for each $k$.
- **Maximum by a key.** Find the item with the largest $f(A[i])$, the argmax. Compute each $f(A[i])$ once and compare the results.
- **Structured inputs.** When the sequence first rises and then falls, the maximum is found with $O(\log n)$ probes: see [maximum of a unimodal function](/unimodal-maximum/). A local maximum of any sequence is found the same way: see [peak finding](/peak-finding/).
- **Streams.** The items arrive one at a time and memory is small. The scan needs only one stored item, so it works as is.

## Examples

**One scan.** For $A = [5, 2, 8, 6, 9, 1, 10, 3, 7, 4]$, the scan compares the current maximum with $A[1], \ldots, A[9]$, which is 9 comparisons. The current maximum changes three times, from 5 to 8, to 9 and to 10, and the answer is 10 at index 6.

**Ties.** For $A = [4, 7, 7, 2]$ both 1 and 2 are correct indices. The strict scan returns 1.

**Counts for several $n$.** The table gives the exact worst-case number of comparisons of each variant, and the expected number of changes of the current maximum on a uniform random order of distinct items, $H_n - 1$:

| $n$ | maximum, $n - 1$ | changes, $H_n - 1$ | min and max, $\lceil 3n/2 \rceil - 2$ | max and second, $n + \lceil \lg n \rceil - 2$ |
|---|---|---|---|---|
| 10 | 9 | 1.929 | 13 | 12 |
| 100 | 99 | 4.187 | 148 | 105 |
| 1000 | 999 | 6.485 | 1498 | 1008 |

## Known algorithms

The scan, Algorithm M of Knuth Section 1.2.10, is:

```pseudo id=scan
FIND-MAXIMUM(A)                ▷ n ≥ 1
L1  m ← 0
L2  for i ← 1 to n − 1 do      ▷ A[m] is a maximum of A[0 .. i − 1]
L3      if A[i] > A[m] then m ← i
L4  return m
```

It does $n - 1$ comparisons on every input, keeps one index, and reads the items once in order. The comment on line L2 is its [loop invariant](/loop-invariant/): at the start it holds for $i = 1$, a pass keeps it because the new $A[m]$ is the larger of the old maximum and $A[i]$, and at the end $i = n$ gives a maximum of the whole array.

- **Tournament.** Compare the items in pairs, then the winners in pairs, and so on. It also uses $n - 1$ comparisons, because each comparison removes one candidate. Its depth is $\lceil \lg n \rceil$ rounds, so it runs in $O(\log n)$ time on $n/2$ processors, as a [parallel reduction](/parallel-reduction/).
- **Quantum search.** The [Dürr and Høyer algorithm](/durr-hoyer-minimum-finding/) finds the minimum, and so the maximum, with $O(\sqrt{n})$ queries with high probability.

## Bounds

**Upper bound.** $n - 1$ comparisons, by the scan or the tournament.

**Lower bound.** Each correct comparison algorithm uses at least $n - 1$ comparisons on each input of distinct items, not only in the worst case.

*Proof.* Run the algorithm on distinct items, and call an item a *loser* when it was the smaller item of some comparison. Assume that at the end some item $A[j]$ other than the output $A[m]$ is not a loser. Change the input by replacing $A[j]$ by a value larger than all items. Every comparison that involved $A[j]$ had $A[j]$ as the larger item, and it still has; no other comparison changes. So the algorithm makes the same comparisons and returns the same $m$, which is now wrong, since $A[j] > A[m]$. So all $n - 1$ items other than the output are losers. Each comparison makes at most one new loser, so at least $n - 1$ comparisons were made. $\blacksquare$

The page [max-finding lower bound](/max-finding-lower-bound/) gives this argument in the decision-tree form. The bound holds for randomized algorithms too, since the argument applies to each run.

**The cost of updates.** The scan always makes $n - 1$ comparisons, but the number of times line L3 changes $m$ depends on the order. It is $n - 1$ on an increasing sequence, 0 when the maximum comes first, and $H_n - 1 = \ln n + O(1)$ on average over the orders of distinct items. Knuth derives the mean and the variance of this count in Section 1.2.10; the [hiring problem](/hiring-problem/) gives the full distribution.

## Reductions

- **[Selection](/selection-problem/) with $k = n$ is this problem.** Algorithms for selection solve it, but with more comparisons.
- **Minimum reduces to maximum** by reversing the order, with no extra cost.
- **[Sorting](/sorting-problem/) solves it** as a by-product: the last item of the sorted order is the maximum. This costs $\Theta(n \log n)$, so it is the wrong method for this problem alone.
- **The [hiring problem](/hiring-problem/) is the cost analysis of the scan** when each change of the maximum is expensive.

## Applications

- Pick the best candidate by a score: the largest key of a list, the best move in a search, the most frequent element after counting.
- The selection step of [selection sort](/selection-sort/), which finds the maximum (or minimum) of the unsorted part $n - 1$ times.
- Normalize data by the largest value, or find the range $\max - \min$.
- A reduction in parallel code: each processor finds the maximum of its part, then the partial maxima are combined in a tree.

## References
