---
tag: 2EJRTP
kind: problem
slug: selection-problem
name: Selection problem
aliases:
- k-th smallest element problem
- order-statistic selection
area: sorting/selection-and-order-statistics
level: intro
summary: Find the element of rank k in an unordered collection of n elements.
model: comparison-model
complexity:
  vars: {n: the number of items}
  time: {worst: Θ(n)}
prereqs: [order-statistic, total-order, comparison-model]
see_also: [quickselect, median-of-medians, floyd-rivest-select, selection-lower-bound, median-finding, top-k-selection, multiple-selection, order-statistic-tree]
sources:
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Chapter 9, Medians and Order Statistics (the problem in the chapter introduction, Section 9.1 for the minimum and maximum, Sections 9.2 and 9.3 for selection in expected and worst-case linear time)
  - book: isbn:9780201896855
    title: Donald E. Knuth, The Art of Computer Programming, Volume 3, second edition
    locator: Section 5.3.3, Minimum-comparison selection (the numbers V_t(n), the tournament methods and the linear bounds)
  - paper: doi:10.1016/S0022-0000(73)80033-9
    title: Manuel Blum, Robert W. Floyd, Vaughan Pratt, Ronald L. Rivest and Robert E. Tarjan, Time bounds for selection, Journal of Computer and System Sciences 7(4) (1973)
    locator: pages 448 to 461 (the algorithm PICK with at most 5.4305n comparisons, and lower bounds)
  - paper: doi:10.1145/360680.360691
    title: Robert W. Floyd and Ronald L. Rivest, Expected time bounds for selection, Communications of the ACM 18(3) (1975)
    locator: pages 165 to 172 (n + min(k, n - k) + o(n) expected comparisons)
  - paper: doi:10.1145/62044.62047
    title: Walter Cunto and J. Ian Munro, Average case selection, Journal of the ACM 36(2) (1989)
    locator: pages 270 to 279 (the lower bound n + k - O(1) on the average number of comparisons, for k below n/2)
  - paper: doi:10.1137/S0097539795288611
    title: Dorit Dor and Uri Zwick, Selecting the median, SIAM Journal on Computing 28(5) (1999)
    locator: pages 1722 to 1758 (the median with fewer than 2.95n comparisons)
  - paper: "A. Schönhage, M. Paterson and N. Pippenger, Finding the median, Journal of Computer and System Sciences 13(2) (1976)"
    locator: pages 184 to 199 (the median with 3n + o(n) comparisons)
  - paper: "Dorit Dor and Uri Zwick, Median selection requires (2 + epsilon)n comparisons, SIAM Journal on Discrete Mathematics 14(3) (2001)"
    locator: pages 312 to 325 (the lower bound for the median)
---

The selection problem asks for the item of rank $k$, the $k$-th smallest, among $n$ items that are not sorted. Sorting solves it in $O(n \log n)$ time, but selection is easier: [quickselect](/quickselect/) takes expected linear time, and [median of medians](/median-of-medians/) takes $\Theta(n)$ time in the worst case in the [comparison model](/comparison-model/). The answer is the [order statistic](/order-statistic/) of rank $k$; the minimum, the maximum and the [median](/median/) are the special cases $k = 1$, $k = n$ and $k = \lceil n/2 \rceil$.

## In plain words

You have a list of numbers in no order, and you want the third smallest, or the middle one, or the hundredth largest. You could sort the list and read the answer at the right place. But sorting does more work than you need, because it puts every item in its place.

Selection asks only for one item. The smallest item needs one pass over the list. The middle item seems harder, but it too can be found in a number of steps that grows only in proportion to the length of the list. The trick is to split the list around a guess, as quicksort does, and then keep only the part that holds the answer.

## Definition

**Input.** A sequence $a_1, \ldots, a_n$ of $n \ge 1$ items with a [total order](/total-order/) $\le$ (or a total preorder given by a key), and an integer $k$ with $1 \le k \le n$.

**Output.** An item $x = a_j$ of the input such that

$$ \bigl|\{ i : a_i < x \}\bigr| \le k - 1 \quad \text{and} \quad \bigl|\{ i : a_i \le x \}\bigr| \ge k. $$

Equivalently, $x = b_k$ for every sorted order $b_1 \le b_2 \le \cdots \le b_n$ of the input. All sorted orders have the same $k$-th entry, so the value of $x$ is unique. When the items are distinct, $x$ is the unique item with exactly $k - 1$ items below it.

**Model.** In the comparison model, the algorithm learns about the items only by comparing two of them, and the cost is the number of comparisons. On a [word RAM](/word-ram/) with integer keys, the algorithm may also use the bits of the keys.

## Variants

- **Extreme ranks.** $k = 1$ or $k = n$ is [finding the minimum or the maximum](/minimum-and-maximum-finding/), with $n - 1$ comparisons. Small $k$, such as the second smallest, is the problem of [small order statistics](/small-order-statistics/).
- **Median.** $k = \lceil n/2 \rceil$ is [median finding](/median-finding/), the hardest rank for most methods.
- **The $k$ smallest.** Report the set of the $k$ smallest items, in any order or sorted: [top-k selection](/top-k-selection/), [partial sorting](/partial-sorting/) and [the largest $i$ numbers in sorted order](/largest-i-numbers-in-sorted-order/).
- **Many ranks.** Find the items of ranks $k_1 < \cdots < k_m$ together: [multiple selection](/multiple-selection/). The [quantiles](/quantile/) are the case of evenly spaced ranks.
- **Weighted.** Each item has a weight, and the answer splits the total weight in two halves: the [weighted median](/weighted-median/).
- **Structured input.** The items are the entries of a matrix with sorted rows and columns ([selection in sorted matrices](/sorted-matrix-selection/)), or the union of two sorted arrays ([median of two sorted arrays](/median-of-two-sorted-arrays/)). Then $o(n)$ time is possible.
- **Dynamic and range versions.** Insertions and deletions are mixed with rank queries: an [order-statistic tree](/order-statistic-tree/) answers each in $O(\log n)$ time. The query "the $k$-th smallest of $A[l \ldots r]$" is the [range $k$-th smallest query](/range-kth-smallest-query/).
- **Approximate.** Any item whose rank is within $\varepsilon n$ of $k$ is accepted. Sampling solves this in time independent of $n$, and stream sketches such as the [KLL sketch](/kll-sketch/) solve it in small space.

## Examples

Let $A = [31, 41, 59, 26, 53, 58, 97, 93, 23, 84]$, so $n = 10$. The sorted order is $23, 26, 31, 41, 53, 58, 59, 84, 93, 97$.

| $k$ | 1 | 3 | 5 | 6 | 10 |
|---|---|---|---|---|---|
| answer | 23 | 31 | 53 | 58 | 97 |

Rank 5 is the lower median and rank 6 is the upper median.

With repeated items, the rank of a value is a range. For $A = [5, 1, 5, 3, 5]$, the sorted order is $1, 3, 5, 5, 5$, so the answer is 1 for $k = 1$, 3 for $k = 2$, and 5 for $k = 3$, 4 and 5. The output condition holds for $x = 5$ and $k = 4$: two items are less than 5 and five items are at most 5.

**A non-answer.** For the first array and $k = 5$, the item 58 is wrong: five items are less than 58, and the condition allows at most $k - 1 = 4$.

## Known algorithms

| algorithm | time | model and case |
|---|---|---|
| sort, then index | $\Theta(n \log n)$ | comparisons, worst case |
| [quickselect](/quickselect/) | $\Theta(n)$ expected, $\Theta(n^2)$ worst | comparisons, random pivot |
| [median of medians](/median-of-medians/) | $\Theta(n)$ | comparisons, worst case |
| [introselect](/introselect/) | $\Theta(n)$ | comparisons, worst case, fast in practice |
| [Floyd-Rivest selection](/floyd-rivest-select/) | $n + \min(k, n-k) + o(n)$ comparisons expected | comparisons, random sample |
| [heap-based selection](/heap-select/) | $O(n \log k)$ | comparisons, worst case, one pass |
| [tournament method](/tournament-method/) | $n + \lceil \lg n \rceil - 2$ comparisons for $k = 2$ | comparisons, worst case |
| [radix select](/radix-select/) | $O(n \cdot w / r + 2^r w / r)$ | word RAM, $w$-bit keys, digits of $r$ bits |

## Bounds

**Upper bounds in the comparison model.** Blum, Floyd, Pratt, Rivest and Tarjan (1973) showed that each rank can be found with at most $5.4305n$ comparisons in the worst case. For the median, Schönhage, Paterson and Pippenger improved this to $3n + o(n)$ in 1976, and Dor and Zwick to fewer than $2.95n$ in 1999. With random choices, Floyd and Rivest (1975) find rank $k$ with $n + \min(k, n - k) + o(n)$ comparisons in expectation, so $1.5n + o(n)$ for the median.

**Lower bounds in the comparison model.** Each algorithm that finds rank $k$ of $n$ distinct items needs at least $n - 1 + \min(k - 1, n - k)$ comparisons in the worst case; the [selection lower bound](/selection-lower-bound/) page proves this by an adversary. For the median this is about $1.5n$. The best known lower bound for the median is $(2 + 2^{-80})n - o(n)$, by Dor and Zwick (2001). On average, and so also for the expected cost of a randomized algorithm, Cunto and Munro (1989) proved that $n + \min(k, n-k) - O(1)$ comparisons are needed, which matches Floyd and Rivest up to the lower-order term.

**Exact values for small ranks.** For $k = 1$ the answer is exactly $n - 1$ comparisons ([max-finding lower bound](/max-finding-lower-bound/)). For $k = 2$ it is exactly $n + \lceil \lg n \rceil - 2$ ([second largest lower bound](/second-largest-lower-bound/)).

## Reductions

- **Selection to sorting.** Sort, then return the $k$-th item: $O(n \log n)$. The reverse is false: by the [comparison sort lower bound](/comparison-sort-lower-bound/), sorting needs $\Omega(n \log n)$ comparisons, while selection needs only $\Theta(n)$.
- **Rank $k$ to the median.** To find rank $k < \lceil n/2 \rceil$ with a median routine, add $n - 2k + 1$ copies of a value below all items. The new list has $2n - 2k + 1$ items, its median has rank $n - k + 1$, and that is the item of rank $k$ of the old list. The case $k > \lceil n/2 \rceil$ is the mirror one. The cost is a median of at most $2n$ items, so the median is the hardest case up to a constant factor.
- **The $k$ smallest from rank $k$.** Once $x$ of rank $k$ is known, one pass that compares each item with $x$ gives the $k$ smallest items, in $O(n)$ time. Selection algorithms that [partition](/partition-around-pivot/) give this for free.
- **Pivot for quicksort.** A linear-time median gives [quicksort](/quicksort/) a perfect split at each step, so $O(n \log n)$ time in the worst case.

## Applications

- **Statistics.** The median, the quartiles and other [quantiles](/quantile/) are robust summaries of data, and each is a selection.
- **Divide and conquer on geometry.** A [k-d tree](/kd-tree/) splits its points at the median of one coordinate. Prune-and-search methods for linear programming in low dimension throw away a constant fraction of the constraints after each median.
- **Top results.** A search engine or a database that returns the best $k$ results needs the $k$ smallest scores, not a full sort ([top-k query](/top-k-query/)).
- **Signal and image processing.** A [median filter](/median-filter/) replaces each value by the median of its neighbours, which removes noise and keeps edges.
- **Location problems.** The point on a line that minimizes the total distance to given points is a median, and with weights it is the [weighted median](/weighted-median-post-office-location/).

## References
