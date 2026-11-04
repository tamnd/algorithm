---
tag: F9MSTX
kind: problem
slug: partial-sorting
name: Partial sorting
aliases:
- k-smallest sorting
- partial sort
- top-k sorting
area: sorting/selection-and-order-statistics
level: core
summary: Place the k smallest elements in sorted order at the front of the array, leaving the rest unordered.
model: comparison-model
complexity:
  vars: {n: the number of items, k: the number of items to sort}
  time: {worst: Θ(n + k log k)}
prereqs: [top-k-selection, quicksort, quickselect]
see_also: [top-k-selection, largest-i-numbers-in-sorted-order, heap-select, quickselect-expected-linear, introsort, heapsort, median-of-medians, sorting-problem]
sources:
  - paper: "Conrado Martínez, Partial quicksort, Proceedings of the Sixth Workshop on Algorithm Engineering and Experiments and the First Workshop on Analytic Algorithmics and Combinatorics (ALENEX/ANALCO 2004)"
    locator: the algorithm partial quicksort and its exact expected number of comparisons
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Chapter 7, Quicksort, Chapter 9, Medians and Order Statistics, and the Chapter 9 problem "Largest i numbers in sorted order"
  - book: isbn:9780201896855
    title: Donald E. Knuth, The Art of Computer Programming, Volume 3, second edition
    locator: Section 5.3.3, Minimum-comparison selection (selecting and sorting the t smallest)
  - url: "https://en.cppreference.com/w/cpp/algorithm/partial_sort"
    locator: std::partial_sort, with about N log M comparisons for N items and M sorted places
---

Partial sorting rearranges an array of $n$ items so that its first $k$ places hold the $k$ smallest items in sorted order, and the other $n - k$ items follow in any order. It sits between [selection](/selection-problem/), which places one item, and [sorting](/sorting-problem/), which places all $n$: the right cost is $\Theta(n + k \log k)$ in the [comparison model](/comparison-model/). The common methods are a heap of $k$ candidates, as in C++'s `std::partial_sort`, in $O(n \log k)$ time, and partial quicksort, a [quicksort](/quicksort/) that does not recurse into parts beyond place $k$, in $O(n + k \log k)$ expected time.

## In plain words

You have a pile of job applications and you want the best twenty in order on top of the pile. The order of the others does not matter.

You could sort the whole pile, but most of that work orders applications that nobody will read. One better way is quicksort with a shortcut: split the pile around a guess, and only keep splitting the parts that hold some of the first twenty places. The parts that lie wholly beyond place twenty are left as they are.

Another way keeps the best twenty seen so far in a small heap, as you read the pile once, and sorts them at the end.

## Definition

**Input.** An array $A[0 \ldots n-1]$ of items with a [total order](/total-order/), and an integer $k$ with $0 \le k \le n$.

**Output.** A permutation of $A$ such that $A[0] \le A[1] \le \cdots \le A[k-1]$ and $A[k-1] \le A[j]$ for each $j \ge k$. So $A[r - 1]$ is the [order statistic](/order-statistic/) of rank $r$ for each $r \le k$, and $A[k \ldots n-1]$ holds the other items in any order.

**Cost.** Comparisons and time, in the worst case or in expectation, and extra space.

The problem is the in-place form of the sorted version of [top-k selection](/top-k-selection/). With $k = n$, or $k = n - 1$, it is sorting.

## Variants

- **Range sort.** Sort only the places $[l, r)$ of the sorted order: the items of ranks $l + 1$ to $r$ in order in $A[l \ldots r - 1]$. Select at $l$ and at $r$, then sort the middle: $O(n + (r - l)\log(r - l))$.
- **Incremental sorting.** $k$ is not known in advance; the caller reads the sorted items one at a time and may stop at any moment. A quicksort that keeps a stack of unsorted parts and sorts only the leftmost does this in $O(n + k \log k)$ expected time for the first $k$ items.
- **Copy out.** C++'s `std::partial_sort_copy` writes the $k$ smallest items, sorted, into a separate array and leaves the input as it is.
- **The largest $k$.** Reverse the order: [the largest $i$ numbers in sorted order](/largest-i-numbers-in-sorted-order/).

## Examples

**Small.** For $A = [31, 41, 59, 26, 53, 58, 97, 93, 23, 84]$ and $k = 3$, a correct output starts with $23, 26, 31$, followed by the other seven items in any order, for example $[23, 26, 31, 41, 53, 58, 59, 97, 93, 84]$ or $[23, 26, 31, 97, 93, 84, 59, 58, 53, 41]$.

**Partial quicksort on the small example.** With the last item of each range as pivot and the Lomuto partition:

1. Range $[0, 10)$, pivot $84$: after partition $A = [31, 41, 59, 26, 53, 58, 23, 84, 97, 93]$, pivot at place $7$. Since $7 \ge k - 1 = 2$, only the left part $[0, 7)$ holds sorted places. The part $[8, 10)$ is skipped.
2. Range $[0, 7)$, pivot $23$: $A[0 \ldots 6] = [23, 41, 59, 26, 53, 58, 31]$, pivot at place $0$. Recurse on $[1, 7)$, since place $0$ is before $k - 1$.
3. Range $[1, 7)$, pivot $31$: $A[1 \ldots 6] = [26, 31, 41, 53, 58, 59]$, pivot at place $2$. The left part $[1, 2)$ has one item. The right part $[3, 7)$ starts at place $3 \ge k$, so it is skipped.

The result begins $23, 26, 31$, after $9 + 6 + 5 = 20$ comparisons; a full quicksort with the same pivot rule continues into the skipped parts.

**Expected cost.** For random input of distinct items, partial quicksort makes $2083.7$ comparisons on average for $n = 1000$ and $k = 10$, and $3061.3$ for $k = 100$; quicksort of all $1000$ items makes $10985.9$.

## Known algorithms

**Sort.** Sort all of $A$: $\Theta(n \log n)$. It is the right choice only when $k$ is close to $n$.

**Heap of $k$ candidates.** Build a max-heap of $A[0 \ldots k-1]$, then for each later item smaller than the top, swap it into the heap and sift down; at the end, heapsort the heap. Time $O(n \log k)$ in the worst case, in place. This is the usual implementation of `std::partial_sort`, whose standard asks for about $n \log k$ comparisons. See [heap-based selection](/heap-select/).

**Heap of all items.** Build a min-heap of all $n$ items in $O(n)$ time and extract $k$ times: $O(n + k \log n)$, in place if the extracted items are moved to the end and the result is reversed.

**Select, then sort.** Run [quickselect](/quickselect/) for rank $k$, which leaves the $k$ smallest items in $A[0 \ldots k-1]$, then sort that part: $O(n + k \log k)$ expected time. With [median of medians](/median-of-medians/) for the selection and [heapsort](/heapsort/) for the sort, the same bound holds in the worst case.

**Partial quicksort.** Martínez (2004) studied the quicksort that, after each partition with the pivot at place $p$, always recurses on the left part, and recurses on the right part only if $p < k - 1$:

```pseudo id=main
PARTIAL-QUICKSORT(A, lo, hi, k)            ▷ sort the places of [lo, hi) that are below k
L1  if hi − lo ≤ 1 then return
L2  r ← a uniform random index in [lo, hi); swap A[r] and A[hi − 1]
L3  p ← PARTITION(A, lo, hi)               ▷ the pivot ends at place p
L4  PARTIAL-QUICKSORT(A, lo, p, k)
L5  if p < k − 1 then PARTIAL-QUICKSORT(A, p + 1, hi, k)
```

The call PARTIAL-QUICKSORT$(A, 0, n, k)$ solves the problem. For distinct items and a uniform random pivot, the expected number of comparisons is

$$ P_{n,k} = 2n + 2(n+1)H_n - 2(n+3-k)H_{n+1-k} - 6k + 6, $$

where $H_m$ is the $m$-th [harmonic number](/harmonic-series/). This is $2n + 2k \ln n + O(k + \log n)$, which is $O(n + k \log k)$ for each $k$: $k \ln n \le 2k \ln k$ when $k \ge \sqrt n$, and $k \ln n = o(n)$ when $k < \sqrt n$. For $k = 1$ it is $2n - 2H_n$, the cost of quickselect for the minimum, and for $k = n$ it is $2(n+1)H_n - 4n$, the cost of quicksort. Compared with quickselect followed by quicksort of the $k$ smallest, partial quicksort saves exactly $2k - 2H_k$ comparisons in expectation, because it does not partition the $k$ smallest items a second time.

| method | worst-case time | expected time | extra space |
|---|---|---|---|
| sort | $\Theta(n \log n)$ | $\Theta(n \log n)$ | depends on the sort |
| heap of $k$ candidates | $\Theta(n \log k)$ | $O(n + k \log k \log(n/k))$ | $O(1)$ |
| heap of all, $k$ extractions | $\Theta(n + k \log n)$ | the same | $O(1)$ |
| quickselect, then sort | $\Theta(n^2)$ | $\Theta(n + k \log k)$ | $O(\log k)$ |
| median of medians, then heapsort | $\Theta(n + k \log k)$ | the same | $O(\log n)$ |
| partial quicksort | $\Theta(n^2)$ | $\Theta(n + k \log k)$ | $O(\log n)$ expected |

## Bounds

The first $k$ places fix the order of the $k$ smallest items, which can be any of $k!$ orders, so a [decision tree](/decision-tree-model/) needs $\lg k! = \Omega(k \log k)$ comparisons; and each item must be read, so $\Omega(n)$ time. The bound $\Omega(n + k \log k)$ is met in the worst case by selection followed by a sort of $k$ items, so the problem takes $\Theta(n + k \log k)$ time. In comparisons, the selection part needs at least $n - k$ more by the [selection lower bound](/selection-lower-bound/), and the sort part $\lg k!$, so about $n + k \lg k$ comparisons are a lower bound up to lower-order terms.

## Reductions

- **To selection and sorting.** Select rank $k$, which also partitions, then sort $k$ items.
- **From sorting.** The case $k = n$ is sorting, so the $\Omega(n \log n)$ bound of the [comparison sort lower bound](/comparison-sort-lower-bound/) holds at that end.
- **To top-k selection.** Partial sorting is top-k selection with sorted output, kept in the input array.

## Applications

- **Paged results.** A database or search engine that shows the first page of results sorted by score needs only a partial sort; `ORDER BY ... LIMIT k` is executed this way.
- **Library routines.** C++ provides `std::partial_sort` and `std::nth_element`, and Python provides `heapq.nsmallest`, for this problem and its unsorted form.
- **Inside other algorithms.** A greedy algorithm that only uses its $k$ best candidates, such as beam search, partially sorts the candidates at each step.

## References
