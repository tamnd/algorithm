---
tag: EQBRS4
kind: problem
slug: minimum-and-maximum-finding
name: Finding the minimum and maximum
aliases:
- Minimum and maximum
area: sorting/selection-and-order-statistics
level: intro
summary: Finding the smallest and largest elements of a set, with n minus one comparisons for one and about three halves n for both.
model: comparison-model
complexity:
  vars: {n: the number of items}
  time: {worst: Θ(n)}
prereqs: [find-maximum, selection-problem, comparison-model]
see_also: [max-finding-lower-bound, max-min-lower-bound, tournament-minimum, tournament-method, second-largest-lower-bound, order-statistic, adversary-argument, hire-assistant]
sources:
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Chapter 9, Section 9.1, Minimum and maximum (MINIMUM with n - 1 comparisons, the pairs method with at most 3 floor(n/2) comparisons, and the exercise on the lower bound ceil(3n/2) - 2)
  - paper: doi:10.1145/361405.361423
    title: Ira Pohl, A sorting problem and its complexity, Communications of the ACM 15(6) (1972)
    locator: pages 462 to 464 (the bound ceil(3n/2) - 2 for the maximum and the minimum together)
  - book: isbn:9780201896855
    title: Donald E. Knuth, The Art of Computer Programming, Volume 3, second edition
    locator: Section 5.3.3, Minimum-comparison selection (the maximum, and the maximum and the minimum together)
  - book: isbn:9780201896831
    title: Donald E. Knuth, The Art of Computer Programming, Volume 1, third edition
    locator: Section 1.2.10, Algorithm M (find the maximum) and the analysis of the number of changes of the maximum
---

Finding the minimum and the maximum asks for the smallest item, the largest item, or both, among $n$ unsorted items. One of them needs exactly $n - 1$ comparisons in the [comparison model](/comparison-model/), and both together need exactly $\lceil 3n/2 \rceil - 2$, which a method that compares the items in pairs reaches. They are the [order statistics](/order-statistic/) of ranks $1$ and $n$, so this is the easiest case of the [selection problem](/selection-problem/), and the first place where a smart order of comparisons beats the obvious one.

## In plain words

To find the lightest of many parcels with a balance, you keep the lightest parcel so far and weigh it against each new parcel. Each weighing except the first knocks out one parcel, and every parcel except the winner must be knocked out once, so you need one weighing fewer than the number of parcels.

If you want both the lightest and the heaviest, the obvious way is to do the search twice. That costs almost two weighings per parcel. A better way takes the parcels two at a time. You weigh the two new parcels against each other first. Only the lighter one can be a new lightest, and only the heavier one can be a new heaviest. So each pair costs three weighings instead of four, and the total is about one and a half weighings per parcel.

## Definition

**Input.** A sequence $a_1, \ldots, a_n$ of $n \ge 1$ items with a [total order](/total-order/).

**Output.** One of these, by the variant:

- the minimum $\min_i a_i$, an item $a_j$ with $a_j \le a_i$ for each $i$;
- the maximum $\max_i a_i$, an item $a_j$ with $a_j \ge a_i$ for each $i$;
- both, as a pair $(a_j, a_l)$ of a minimum and a maximum.

Often the index is wanted, not the value. With repeated items there can be several correct indices; a common rule asks for the first one.

**Cost.** The number of comparisons between items, in the worst case over all inputs of size $n$.

## Variants

- **One extreme.** The minimum or the maximum alone, the problem of [finding the maximum](/find-maximum/).
- **Both extremes.** The minimum and the maximum together, the main case of this page.
- **The two smallest.** The minimum and the second smallest, which needs $n + \lceil \lg n \rceil - 2$ comparisons ([tournament method](/tournament-method/), [second largest lower bound](/second-largest-lower-bound/)).
- **Streams.** The items arrive one at a time and the answer must be known after each one. The scan below works, with $O(1)$ memory. The number of changes of the running maximum is the subject of the [hiring problem](/hiring-problem/).
- **Parallel.** On $p$ processors, a [parallel reduction](/parallel-reduction/) finds the minimum in $O(n/p + \log p)$ time.

## Examples

**One extreme.** For $A = [7, 2, 9, 4, 1, 8, 3, 6]$, a scan that keeps the smallest item so far compares $2 < 7$, then $9$, $4$, $1 < 2$, $8$, $3$ and $6$ with the current minimum: $7$ comparisons, and the minimum is $1$.

**Both, by pairs.** For the same $A$, with $n = 8$:

| step | items | comparisons | min | max |
|---|---|---|---|---|
| first pair | 7, 2 | $2 < 7$ | 2 | 7 |
| pair | 9, 4 | $4 < 9$, $4$ with $2$, $9$ with $7$ | 2 | 9 |
| pair | 1, 8 | $1 < 8$, $1$ with $2$, $8$ with $9$ | 1 | 9 |
| pair | 3, 6 | $3 < 6$, $3$ with $1$, $6$ with $9$ | 1 | 9 |

The total is $1 + 3 \cdot 3 = 10 = 3 \cdot 8/2 - 2$ comparisons. Two separate scans make $7 + 7 = 14$.

**Odd $n$.** For $A = [5, 3, 8]$, set both the minimum and the maximum to $5$, then handle the pair $(3, 8)$ with $3$ comparisons. The total is $3 = \lceil 9/2 \rceil - 2$.

## Known algorithms

**Scan for one extreme.** Keep the smallest item so far and compare it with each next item: $n - 1$ comparisons on each input, $O(1)$ extra space.

**Two scans.** Find the minimum and then the maximum: $2n - 2$ comparisons.

**Scan with "else".** For each next item, compare it with the minimum, and only if it is not a new minimum, with the maximum. In the worst case, for example an increasing input, this is still $2n - 2$. On a uniformly random order of distinct items, item $i \ge 2$ is a new minimum with probability $1/i$, because each of the first $i$ items is equally likely to be the smallest of them. So by [linearity of expectation](/linearity-of-expectation/) the expected count is $2(n-1) - (H_n - 1) = 2n - H_n - 1$, where $H_n$ is the [harmonic number](/harmonic-series/). This is still about $2n$.

**Pairs.** If $n$ is even, compare the first two items and set the minimum and the maximum from the result. If $n$ is odd, set both to the first item. Then for each next pair $(u, v)$: compare $u$ with $v$, compare the smaller with the minimum, and compare the larger with the maximum.

```pseudo id=main
MIN-MAX(A[1 .. n])                         ▷ n ≥ 1
L1  if n is odd then lo ← A[1], hi ← A[1], i ← 2
L2  else if A[1] ≤ A[2] then lo ← A[1], hi ← A[2], i ← 3
L3  else lo ← A[2], hi ← A[1], i ← 3
L4  while i < n do                         ▷ the pair A[i], A[i + 1]
L5      (s, b) ← (A[i], A[i + 1]) if A[i] ≤ A[i + 1], else (A[i + 1], A[i])
L6      if s < lo then lo ← s
L7      if b > hi then hi ← b
L8      i ← i + 2
L9  return (lo, hi)
```

The count is $3(n-1)/2$ for odd $n$ and $1 + 3(n-2)/2 = 3n/2 - 2$ for even $n$, which is $\lceil 3n/2 \rceil - 2$ in both cases. The item $s$ cannot be the maximum of the pair and $b$ cannot be the minimum, unless they are equal, and then either one serves. The [tournament method for the minimum](/tournament-minimum/) gives another way to the same count: play a knockout among the winners of the pairs and another among the losers.

## Bounds

**One extreme, exactly $n - 1$.** Each item other than the minimum must lose at least one comparison, else the algorithm cannot rule it out: if an item never lost, it could be the smallest. Each comparison has only one loser. So $n - 1$ comparisons are needed, and the scan uses $n - 1$. The full proof is the [max-finding lower bound](/max-finding-lower-bound/).

**Both extremes, exactly $\lceil 3n/2 \rceil - 2$.** At the end, each item except the minimum must have been larger in some comparison, and each item except the maximum must have been smaller in some comparison: $2n - 2$ units of information. An [adversary](/adversary-argument/) answers so that a comparison of two fresh items gives two units, and each other comparison gives at most one unit. At most $\lfloor n/2 \rfloor$ comparisons can involve two fresh items, so at least $\lfloor n/2 \rfloor + (2n - 2 - 2\lfloor n/2 \rfloor) = \lceil 3n/2 \rceil - 2$ comparisons are needed. Pohl (1972) proved this bound. The full proof is the [simultaneous maximum and minimum lower bound](/max-min-lower-bound/), and the pairs method shows that it is exact.

**Time.** All methods above take $\Theta(n)$ time, and every correct method must read each item, so $\Omega(n)$ is also a lower bound on time.

## Reductions

- **To selection.** The minimum is selection with $k = 1$ and the maximum with $k = n$. The general methods, such as [quickselect](/quickselect/), make more comparisons than the scan, so the special case is worth its own code.
- **Maximum from minimum.** Reverse the order: the maximum for $\le$ is the minimum for $\ge$, with the same number of comparisons.
- **Sorting.** A sort gives both extremes, but it costs $\Omega(n \log n)$ comparisons, far more than the $\lceil 3n/2 \rceil - 2$ that are needed.

## Applications

- **Ranges of keys.** [Counting sort](/counting-sort/) and [radix sort](/radix-sort/) need the smallest and the largest key to size their tables, and [bucket sort](/bucket-sort/) needs the range to map keys to buckets.
- **Bounding boxes.** The [axis-aligned bounding box](/axis-aligned-bounding-box/) of a set of points is the minimum and maximum of each coordinate.
- **Normalization.** Scaling data to the interval from 0 to 1 needs the minimum and maximum of the data.
- **Game trees.** The [minimax](/minimax/) rule takes the minimum or the maximum of the children at each node.

## References
