---
tag: M8JP0R
kind: problem
slug: median-finding
name: Median finding
aliases:
- median selection
area: sorting/selection-and-order-statistics
level: intro
summary: Compute the median of n elements; a special case of selection.
model: comparison-model
complexity:
  vars: {n: the number of items}
  time: {worst: Θ(n)}
prereqs: [median, selection-problem]
see_also: [median-of-medians, quickselect, floyd-rivest-select, selection-lower-bound, sliding-window-median, median-of-two-sorted-arrays, weighted-median, kd-tree]
sources:
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Chapter 9, Medians and Order Statistics (Sections 9.2 and 9.3, and the end-of-chapter problem "Alternative analysis of randomized selection")
  - paper: doi:10.1016/S0022-0000(73)80033-9
    title: Manuel Blum, Robert W. Floyd, Vaughan Pratt, Ronald L. Rivest and Robert E. Tarjan, Time bounds for selection, Journal of Computer and System Sciences 7(4) (1973)
    locator: pages 448 to 461 (linear worst-case selection, and lower bounds for the median)
  - paper: doi:10.1145/360680.360691
    title: Robert W. Floyd and Ronald L. Rivest, Expected time bounds for selection, Communications of the ACM 18(3) (1975)
    locator: pages 165 to 172 (the median with 1.5n + o(n) expected comparisons)
  - paper: "A. Schönhage, M. Paterson and N. Pippenger, Finding the median, Journal of Computer and System Sciences 13(2) (1976)"
    locator: pages 184 to 199 (the median with 3n + o(n) comparisons)
  - paper: doi:10.1137/S0097539795288611
    title: Dorit Dor and Uri Zwick, Selecting the median, SIAM Journal on Computing 28(5) (1999)
    locator: pages 1722 to 1758 (fewer than 2.95n comparisons)
  - paper: "Samuel W. Bent and John W. John, Finding the median requires 2n comparisons, Proceedings of the 17th Annual ACM Symposium on Theory of Computing (STOC 1985)"
    locator: the lower bound 2n - o(n) for the median
  - paper: "Dorit Dor and Uri Zwick, Median selection requires (2 + epsilon)n comparisons, SIAM Journal on Discrete Mathematics 14(3) (2001)"
    locator: pages 312 to 325 (the lower bound (2 + 2^-80)n)
  - paper: doi:10.1145/62044.62047
    title: Walter Cunto and J. Ian Munro, Average case selection, Journal of the ACM 36(2) (1989)
    locator: pages 270 to 279 (the average-case lower bound, 1.5n - O(1) for the median)
---

Median finding asks for the [median](/median/) of $n$ unsorted items: the item of rank $\lceil n/2 \rceil$, or for even $n$ also the upper median of rank $n/2 + 1$. It is the case $k = \lceil n/2 \rceil$ of the [selection problem](/selection-problem/) and the hardest one, so it is the case on which selection algorithms are measured. It takes $\Theta(n)$ time in the [comparison model](/comparison-model/), and the exact number of comparisons that are needed in the worst case is known only to lie between about $2n$ and $2.95n$.

## In plain words

You have a pile of exam papers and you want the middle score: half the class did at least as well, half at most as well. You could sort all the papers, but that is more work than the question needs.

The quick way is to guess a score, split the pile into "below" and "above", and count. If the "below" pile is too big, the middle score is in it, so you throw the other pile away and repeat. A random guess usually throws away a large part, so the work is a small multiple of the number of papers. With more care in the choice of the guess, this is true even for the worst pile.

## Definition

**Input.** A sequence $a_1, \ldots, a_n$ of $n \ge 1$ items with a [total order](/total-order/).

**Output.** The lower median $a_{(\lceil n/2 \rceil)}$, where $a_{(i)}$ is the [order statistic](/order-statistic/) of rank $i$. Some variants ask for the upper median $a_{(\lfloor n/2 \rfloor + 1)}$, or for both.

**Cost.** The number of comparisons between items, in the worst case or in expectation over the random choices of the algorithm.

## Variants

- **Statistical median.** For numbers and even $n$, return $\frac{1}{2}(a_{(n/2)} + a_{(n/2 + 1)})$. This is two selections, or one selection followed by a scan for the minimum of the upper half.
- **Approximate median.** Return an item whose rank is between $(1/2 - \varepsilon) n$ and $(1/2 + \varepsilon) n$. The median of a random sample of $O(\varepsilon^{-2} \log (1/\delta))$ items is such an item with probability at least $1 - \delta$, in time independent of $n$. The median of medians of groups of five is a deterministic answer with $\varepsilon$ about $1/5$.
- **Running median.** Items arrive one at a time, and the median of the items seen so far is asked after each one. Two heaps solve it in $O(\log n)$ time per item; see the example below.
- **Sliding window.** The median of each window of $w$ consecutive items: the [sliding window median](/sliding-window-median/), used by the [median filter](/median-filter/).
- **Structured input.** The median of the union of two sorted arrays takes $O(\log n)$ time ([median of two sorted arrays](/median-of-two-sorted-arrays/)).
- **Weighted.** Each item has a weight and the median splits the total weight: the [weighted median](/weighted-median/).

## Examples

**One array.** For $A = [31, 41, 59, 26, 53, 58, 97, 93, 23, 84]$, the sorted order is $23, 26, 31, 41, 53, 58, 59, 84, 93, 97$. The lower median is $53$ (rank 5), the upper median is $58$ (rank 6), and the statistical median is $55.5$.

**Odd count with repeats.** For $[5, 1, 5, 3, 5]$, the median is the item of rank 3 in $1, 3, 5, 5, 5$, which is $5$.

**Running median with two heaps.** Keep a max-heap `lo` of the smaller half and a min-heap `hi` of the larger half, with $|lo| = |hi|$ or $|lo| = |hi| + 1$. Put each new item into `lo` if it is at most the top of `lo`, else into `hi`, and move one top to the other heap if the sizes break the rule. The top of `lo` is the lower median. For the stream $5, 15, 1, 3, 8, 7, 9$:

| item | `lo` | `hi` | lower median |
|---|---|---|---|
| 5 | 5 | | 5 |
| 15 | 5 | 15 | 5 |
| 1 | 1, 5 | 15 | 5 |
| 3 | 1, 3 | 5, 15 | 3 |
| 8 | 1, 3, 5 | 8, 15 | 5 |
| 7 | 1, 3, 5 | 7, 8, 15 | 5 |
| 9 | 1, 3, 5, 7 | 8, 9, 15 | 7 |

When $3$ arrives, `lo` holds $1, 3, 5$ and `hi` holds $15$, so the top $5$ of `lo` moves to `hi`.

## Known algorithms

| algorithm | comparisons for the median | case |
|---|---|---|
| sort, then index | $n \lg n + O(n)$ | worst case, with merge sort |
| [quickselect](/quickselect/), random pivot | $2(1 + \ln 2) n + o(n) \approx 3.39n$ | expected |
| [median of medians](/median-of-medians/) (BFPRT) | at most $5.4305n$ for the refined method of the paper; the simple version with groups of five makes about $11.5n$ on random input of size $10^5$ | worst case |
| [introselect](/introselect/) | close to quickselect in practice | $O(n)$ worst case |
| [Floyd-Rivest selection](/floyd-rivest-select/) | $1.5n + o(n)$ | expected |
| Schönhage, Paterson and Pippenger (1976) | $3n + o(n)$ | worst case |
| Dor and Zwick (1999) | at most $2.95n$ | worst case |
| two heaps, online | $O(n \log n)$ | worst case, all prefixes |

The value $2(1 + \ln 2) n$ comes from the exact expected count of quickselect at $k = n/2$; for $n = 1000$ and $k = 500$ it is about $3336$ comparisons. The methods of Schönhage, Paterson and Pippenger and of Dor and Zwick are of theoretical interest: their constants are good but their lower-order terms and their bookkeeping make them slow in practice.

## Bounds

**Worst case.** The [selection lower bound](/selection-lower-bound/) $n - 1 + \min(k - 1, n - k)$ at $k = \lceil n/2 \rceil$ gives $\lceil 3n/2 \rceil - 2$ comparisons. Bent and John (1985) raised the lower bound for the median to $2n - o(n)$, and Dor and Zwick (2001) to $(2 + 2^{-80}) n - o(n)$. The best upper bound is below $2.95n$, so the constant is open between about $2$ and $2.95$.

**Expected and average case.** Floyd and Rivest (1975) find the median with $1.5n + o(n)$ comparisons in expectation. Cunto and Munro (1989) proved that each algorithm needs $1.5n - O(1)$ comparisons on average over random inputs, and so also in expectation for a randomized algorithm. Randomness thus helps: $1.5n$ against at least $2n$.

**Time.** Each algorithm must read each item, so $\Omega(n)$ time is needed, and median of medians gives $O(n)$.

## Reductions

- **Selection to the median.** Each rank $k$ reduces to a median of at most $2n$ items: pad the input with $|n - 2k + 1|$ copies of a value below all items (for $k < \lceil n/2 \rceil$) or above all items (for $k > \lceil n/2 \rceil$). So a median algorithm with $c n$ comparisons gives selection with at most $2cn$ comparisons.
- **The median to selection.** The median is selection with $k = \lceil n/2 \rceil$.
- **Median to sorting.** Sorting gives the median in $O(n \log n)$ time, but the median does not give a sort.

## Applications

- **Pivots.** A linear-time median gives [quicksort](/quicksort/) splits into halves at each level, so $O(n \log n)$ worst-case time. In practice an approximate median of a sample, such as the median of three items, is used ([pivot selection](/pivot-selection/)).
- **Space partitioning.** A [k-d tree](/kd-tree/) splits its points at the median of one coordinate at each node, so its depth is $\lceil \lg n \rceil$.
- **Robust statistics.** The median is not moved far by a few extreme values, unlike the mean.
- **Location on a line.** The point that minimizes the sum of distances to $n$ points on a line is a median, and with weights a [weighted median](/weighted-median-post-office-location/).
- **Prune and search.** Algorithms for linear programming in two dimensions take the median of $n/2$ slopes in each round and throw away a quarter of the constraints ([prune and search](/prune-and-search/)).

## References
