---
tag: G92RVJ
kind: problem
slug: largest-i-numbers-in-sorted-order
name: Largest i numbers in sorted order
area: sorting/selection-and-order-statistics
level: core
summary: Listing the i largest elements of an array in sorted order, compared across sorting, heap and selection based approaches.
model: comparison-model
complexity:
  vars: {n: the number of items, i: the number of items to report}
  time: {worst: Θ(n + i log i)}
prereqs: [top-k-selection, binary-heap, selection-problem]
see_also: [top-k-selection, partial-sorting, heap-select, quickselect, median-of-medians, heapsort, top-m-problem, tournament-method]
sources:
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Chapter 9, end-of-chapter problem "Largest i numbers in sorted order" (the three methods sort, max-priority queue and order-statistic algorithm), and Chapter 6, Heapsort (BUILD-MAX-HEAP and HEAP-EXTRACT-MAX)
  - book: isbn:9780201896855
    title: Donald E. Knuth, The Art of Computer Programming, Volume 3, second edition
    locator: Section 5.3.3, Minimum-comparison selection (selecting the t largest in order)
  - book: isbn:9780321573513
    title: Robert Sedgewick and Kevin Wayne, Algorithms, fourth edition
    locator: Section 2.4, Priority queues (TopM), and Section 2.5, Applications (selection)
---

Given $n$ numbers, the problem asks for the $i$ largest of them, listed from the largest down. It is the CLRS end-of-chapter problem that compares three methods: sort everything in $O(n \log n)$ time; build a max-heap and extract the maximum $i$ times, in $O(n + i \log n)$; or [select](/selection-problem/) the $i$-th largest, partition around it, and sort only the $i$ winners, in $O(n + i \log i)$. The last is optimal in the [comparison model](/comparison-model/), and the comparison shows how much of a sort a problem really needs.

## In plain words

A teacher wants the ten best marks of a large school, best first. Sorting the whole school puts every pupil in order, which is far more than asked.

A heap is a way to arrange the marks so that the best one is always on top and can be taken off quickly. Building it costs a little more than one look at each mark, and each of the ten removals is cheap.

The third way first finds the tenth best mark, with a method that costs a few looks per pupil. Everyone at or above that mark is a winner. Only those ten need to be sorted, which is very little work.

## Definition

**Input.** An array $A$ of $n$ items with a [total order](/total-order/), and an integer $i$ with $1 \le i \le n$.

**Output.** The items $a_{(n)}, a_{(n-1)}, \ldots, a_{(n-i+1)}$, in this order, where $a_{(r)}$ is the [order statistic](/order-statistic/) of rank $r$.

**Cost.** The worst-case running time, or the number of comparisons, as a function of both $n$ and $i$.

It is the sorted version of [top-k selection](/top-k-selection/) with $k = i$ and the order reversed. For the smallest items, reverse the order.

## Variants

- **Unordered.** Report the $i$ largest in any order: one selection and one partition, $\Theta(n)$ time.
- **In place.** Leave the $i$ largest sorted at the end of $A$ and the rest in any order: [partial sorting](/partial-sorting/).
- **Stream.** The items arrive one at a time and memory is $O(i)$: the [heap of $i$ candidates](/heap-select/), $O(n \log i)$ time, which is the [top-M problem](/top-m-problem/).
- **Incremental.** $i$ is not known in advance, and the caller asks for the next largest item until it stops. The max-heap method supports this directly, and so does an incremental quicksort that sorts only the part being read.

## Examples

**Small.** For $A = [31, 41, 59, 26, 53, 58, 97, 93, 23, 84]$ and $i = 3$, the answer is $97, 93, 84$.

- *Sort.* Sorting gives $23, 26, \ldots, 97$, and the last three in reverse are the answer.
- *Max-heap.* BUILD-MAX-HEAP gives a heap with $97$ at the root. EXTRACT-MAX returns $97$, then $93$, then $84$.
- *Select and sort.* The $3$rd largest is $a_{(8)} = 84$. One pass keeps $97$, $93$ and $84$, and sorting these three in decreasing order gives the answer.

**Measured cost.** For $n = 10^5$ distinct random integers and $i = 100$, the four methods made these numbers of comparisons:

| method | comparisons | per item |
|---|---|---|
| sort all (Python's built-in sort) | $1531879$ | $15.3$ |
| build a heap, extract $100$ times | $166547$ | $1.67$ |
| [quickselect](/quickselect/), then sort $100$ items (mean of 10 runs) | $212146$ | $2.12$ |
| [heap of $100$ candidates](/heap-select/) | $108420$ | $1.08$ |

For small $i$ and random input, the three methods that avoid a full sort are all within a small factor of $n$. The heap of candidates wins here because on random input it rejects almost every item with one comparison.

## Known algorithms

**(a) Sort, then list.** Sort $A$ with a comparison sort such as [merge sort](/merge-sort/) or [heapsort](/heapsort/), then output the last $i$ items in reverse. Time $\Theta(n \log n)$ in the worst case, for each $i$.

**(b) Max-priority queue.** Build a max-heap of all $n$ items with BUILD-MAX-HEAP, in $O(n)$ time, then call EXTRACT-MAX $i$ times, each in $O(\log n)$ time. Total $O(n + i \log n)$. It needs no knowledge of $i$ in advance: the items come out one by one.

**(c) Select, partition, sort.** Find the item $x$ of rank $n - i + 1$, the $i$-th largest, with a worst-case linear selection such as [median of medians](/median-of-medians/). Partition $A$ around $x$, so that the $i$ largest items are in one part, in $O(n)$ time. Sort these $i$ items in $O(i \log i)$ time. Total $O(n + i \log i)$ in the worst case; with [quickselect](/quickselect/) instead, the same in expectation.

**(d) Heap of $i$ candidates.** Read the items once and keep the $i$ largest so far in a min-heap: $O(n \log i)$ time and $O(i)$ space. It is not one of the three methods of the CLRS problem, but it is the right one for a stream.

| method | worst-case time | extra space | streaming |
|---|---|---|---|
| (a) sort | $\Theta(n \log n)$ | $O(1)$ to $O(n)$ | no |
| (b) max-heap and $i$ extractions | $\Theta(n + i \log n)$ | $O(1)$ in place | no |
| (c) select, partition, sort | $\Theta(n + i \log i)$ | $O(1)$ to $O(\log n)$ | no |
| (d) heap of $i$ candidates | $\Theta(n \log i)$ | $\Theta(i)$ | yes |

**Comparing (b) and (c).** Method (c) is never worse than (b) by more than a constant factor, since $i \log i \le i \log n$. In fact the gap is at most a factor of about $2$: since $\log i \ge \frac{1}{2}\log n$ when $i \ge \sqrt n$, and $i \log n \le \sqrt n \log n = o(n)$ when $i < \sqrt n$, the ratio of the bounds of (b) and (c) is at most $2$ for large $n$, for each $i$. So both are asymptotically optimal; (c) has the cleaner bound, (b) the simpler code and the incremental output.

## Bounds

The output determines the order of the $i$ largest items, which can be any of $i!$ orders, so a [decision tree](/decision-tree-model/) needs at least $\lg i! = \Omega(i \log i)$ comparisons. Each item must be read, so $\Omega(n)$ time is needed. So the problem takes $\Theta(n + i \log i)$ time in the worst case, and method (c) is optimal. The counting bound $\lg (n!/(n-i)!) \approx i \lg n$ for the number of possible ordered outputs is not larger in order, by the argument above.

## Reductions

- **To selection and sorting.** Method (c): one selection of rank $n - i + 1$, one partition, and one sort of $i$ items.
- **To a priority queue.** Method (b): $n$ insertions, or one linear build, and $i$ extractions.
- **From sorting.** With $i = n$ the problem is sorting, which needs $\Omega(n \log n)$ comparisons, the case $i = n$ of the bound.

## Applications

- **Leaderboards and reports.** The ten largest sales, the hundred most active users, or the slowest requests of a day, best first.
- **Search engines.** The best $i$ results by score, shown in order ([top-k query](/top-k-query/)).
- **Teaching.** The problem is a standard exercise in matching the work of an algorithm to the output that is asked for.

## References
