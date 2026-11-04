---
tag: E9SF0P
kind: problem
slug: top-m-problem
name: Top M items of a large stream
aliases:
- TopM
area: data-structures/heaps
level: intro
summary: Finds the M largest items among N inputs arriving as a stream, using a priority queue of size M.
prereqs: [priority-queue, binary-heap, streaming-model]
see_also: [top-k-selection, selection-problem, heap-select, quickselect, partial-sorting, k-nearest-neighbors, sift-down-sink, tournament-tree]
sources:
  - book: isbn:9780321573513
    title: Robert Sedgewick and Kevin Wayne, Algorithms, fourth edition
    locator: Section 2.4 (Priority Queues), the client TopM and the table of costs for finding the M largest of N items
  - book: isbn:9780201896855
    title: Donald E. Knuth, The Art of Computer Programming, Volume 3, second edition
    locator: Section 5.3.3 (Minimum-comparison selection), the selection of the t largest items and the second largest
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Chapter 9 (Medians and Order Statistics), and Section 6.5 (Priority queues)
---

The top M problem asks for the $M$ largest items of a sequence of $N$ items that arrive one at a time, when $N$ is too large to store and $M$ is small. The standard solution keeps the $M$ largest items seen so far in a min-oriented [priority queue](/priority-queue/), so that the smallest of them is the one to compare with and to drop. With a [binary heap](/binary-heap/) this takes $O(N \log M)$ time and space for $M$ items, and on a random order the heap changes only about $M \ln(N/M)$ times. It is the client `TopM` of Sedgewick and Wayne and a [streaming](/streaming-model/) form of [top-k selection](/top-k-selection/).

## In plain words

A shop records millions of sales a day and wants the ten biggest ones. It cannot keep all the sales in memory. So it keeps a short list of the ten biggest sales so far. When a new sale comes in, it compares the sale with the smallest sale on the list. If the new sale is bigger, the smallest one leaves the list and the new one joins. Else the new sale is forgotten.

The list must give the smallest of its items fast, and take items in and out fast. A heap does both. Most sales are too small to enter the list once it is full, so most of the work is one comparison per sale.

## Definition

**Input.** A sequence $x_1, x_2, \ldots, x_N$ of items from a totally ordered set, read once from left to right, and an integer $M$ with $1 \le M \le N$. The value of $N$ need not be known in advance.

**Output.** A list $y_1 \ge y_2 \ge \cdots \ge y_M$ of $M$ items, taken from the input as a multiset, such that each input item not in the list is at most $y_M$. Formally, there are distinct indices $j_1, \ldots, j_M$ with $y_r = x_{j_r}$, and $x_i \le y_M$ for each $i \notin \{j_1, \ldots, j_M\}$. With equal keys the set of indices need not be unique, but the list of keys is.

**Resources.** The algorithm makes one pass over the input. Its memory holds $O(M)$ items, besides a constant number of counters, so it cannot store the whole input when $N \gg M$.

## Variants

- **Unordered output.** Return the $M$ items as a set. This removes the final sort, which costs $O(M \log M)$.
- **Smallest instead of largest.** Reverse the order. The $M$ nearest points to a query, in [k-nearest neighbors](/k-nearest-neighbors/), keep a max-oriented heap of the $M$ smallest distances.
- **Offline.** All $N$ items are in memory. This is the [top-k selection](/top-k-selection/) problem, and selection in $O(N)$ time becomes possible.
- **Only the $M$-th largest.** This is the [selection problem](/selection-problem/) with rank $N - M + 1$.
- **Sliding windows and deletions.** The top $M$ of the last $W$ items, or of a set with deletions, needs a structure that can delete, such as a balanced search tree.
- **Top $M$ by frequency.** The items repeat and the goal is the $M$ most frequent ones. That is a different problem, the heavy hitters, solved approximately by [Space-Saving](/space-saving/) or a [count-min sketch](/count-min-sketch/).

## Examples

**One stream.** Let $M = 3$ and the stream be $31, 4, 15, 92, 65, 35, 89, 79, 32, 38, 46, 26$. The heap holds the three largest items so far; its minimum is the first in each row.

| item | action | heap after (sorted) |
|---|---|---|
| 31 | insert | {31} |
| 4 | insert | {4, 31} |
| 15 | insert | {4, 15, 31} |
| 92 | 92 > 4: replace the minimum | {15, 31, 92} |
| 65 | 65 > 15: replace the minimum | {31, 65, 92} |
| 35 | 35 > 31: replace the minimum | {35, 65, 92} |
| 89 | 89 > 35: replace the minimum | {65, 89, 92} |
| 79 | 79 > 65: replace the minimum | {79, 89, 92} |
| 32, 38, 46, 26 | each is at most 79: skip | {79, 89, 92} |

The answer is $92, 89, 79$. The heap changed 8 times: 3 inserts and 5 replacements. The last four items each cost one comparison.

**Edge cases.** With $M = N$, the answer is the whole input in decreasing order, which is sorting. With $M = 1$, the heap is one cell and the algorithm is the scan for the maximum. With the stream $5, 5, 5, 5$ and $M = 2$, the answer is $5, 5$, and no replacement is needed after the first two items if the test is a strict "larger than the minimum".

**Counts on a random order.** If the $N$ keys are distinct and come in a uniformly random order, the expected number of replacements is $M(H_N - H_M)$, derived under Bounds. For $N = 10^6$ and $M = 10$ this is about 114.6; for $M = 1000$ it is about 6907. Both are far below $N$.

## Known algorithms

- **A heap of size $M$.** Keep a min-oriented binary heap of the $M$ largest items so far. For each new item after the first $M$, compare it with the minimum. If it is larger, replace the root by it and [sift it down](/sift-down/). At the end, extract the $M$ items, which come out in increasing order. Time $O(N \log M)$ in the worst case, space $O(M)$. Sedgewick and Wayne write it as "insert, then delete the minimum when the size is $M + 1$", which does the same with a heap of $M + 1$ items.
- **A buffer of $2M$ items.** Collect items in a buffer of size $2M$. When it is full, use [quickselect](/quickselect/) or [linear-time selection](/deterministic-linear-selection/) to find the $M$-th largest and drop the $M$ items below it. Each round handles $M$ new items in $O(M)$ time, so the total is $O(N)$, plus $O(M \log M)$ to sort the output, with space $O(M)$. The time is worst case with linear-time selection and expected with quickselect.
- **Sort everything.** Store all items and sort them. Time $O(N \log N)$ and space $O(N)$, which breaks the memory limit.
- **Offline selection.** With all items in memory, [quickselect](/quickselect/) finds the $M$-th largest in $O(N)$ expected time, and a scan collects the items above it. [Heap select](/heap-select/) builds a max-heap of all $N$ items in $O(N)$ and extracts $M$ times in $O(M \log N)$. A [partial sort](/partial-sorting/) gives the same output.

| method | time | memory | one pass |
|---|---|---|---|
| heap of size $M$ | $O(N \log M)$ worst | $O(M)$ | yes |
| buffer of $2M$ with selection | $O(N + M \log M)$ | $O(M)$ | yes |
| sort all | $O(N \log N)$ | $O(N)$ | no |
| quickselect, then sort the top | $O(N + M \log M)$ expected | $O(N)$ | no |
| heap select | $O(N + M \log N)$ | $O(N)$ | no |

## Bounds

**A lower bound of $N - M$ comparisons.** Assume distinct keys, in the [comparison model](/comparison-model/). Each item that is not in the output must be the smaller item in at least one comparison. If an item $y$ outside the output never was the smaller one, change its key to a value above all other keys. Each comparison of $y$ had $y$ as the larger item, so it gives the same result, and the other comparisons do not involve $y$. So the algorithm makes the same comparisons and gives the same output, but now $y$ is the largest item and the output, which does not contain $y$, is wrong. Each comparison has exactly one smaller item, so at least $N - M$ comparisons are needed.

**A lower bound for the sorted output.** The output is an ordered list of $M$ distinct positions, and each of the $N!/(N - M)!$ such lists is the right answer for some order of the keys. A comparison algorithm is a binary decision tree with one output at each leaf, so it has at least $N!/(N-M)!$ leaves, and its height is at least
$$\left\lceil \lg \frac{N!}{(N - M)!} \right\rceil = \left\lceil \sum_{i=0}^{M-1} \lg(N - i) \right\rceil.$$
For $N = 10^6$ this is 200 when $M = 10$, and 19931 when $M = 1000$. For fixed $M$ it is about $M \lg N$. So the comparisons needed are at least the larger of $N - M$ and this bound.

**Exact values for small $M$.** For $M = 1$ the answer is $N - 1$ comparisons. For the largest and the second largest, the minimum number of comparisons in the worst case is $N + \lceil \lg N \rceil - 2$, which a knockout [tournament](/tournament-tree/) reaches; Knuth, Section 5.3.3, gives the proof and the known results for larger $M$.

**Expected work of the heap method.** Let the keys be distinct and the order uniformly random. For $i > M$, item $i$ enters the heap exactly when it is among the $M$ largest of the first $i$ items. Each of the first $i$ items has the same chance to be in each rank among them, so this happens with probability $M/i$. By linearity of expectation, the expected number of replacements is
$$\sum_{i=M+1}^{N} \frac{M}{i} = M (H_N - H_M) \le M \ln(N/M),$$
because $1/i \le \int_{i-1}^{i} dx/x$ for each $i \ge 2$, so the sum of $1/i$ for $i = M+1$ to $N$ is at most $\int_M^N dx/x$. Each replacement costs $O(\log M)$, and each item costs one comparison with the minimum. So the expected time is $O(N + M \log M \log(N/M))$, which is $O(N)$ whenever $M \log M \log(N/M) = O(N)$.

**Memory.** A one-pass algorithm must store $M$ items. After the first $M$ items, which have distinct keys, the rest of the stream may consist of items smaller than all of them, and then each of the first $M$ items is in the output. So the algorithm must still hold all of them.

## Reductions

- **Sorting reduces to top $M$.** With $M = N$, the sorted output is the sorted input. So the problem with sorted output needs $\Omega(N \log N)$ comparisons when $M$ is a constant fraction of $N$, which matches the lower bound above.
- **Selection reduces to top $M$.** The $M$-th largest item is $y_M$, the last item of the output.
- **Top $M$ reduces to selection.** With all items in memory, find the $M$-th largest $t$ by a selection algorithm, collect the items larger than $t$, add copies of $t$ until there are $M$ items, and sort them. This costs one selection, one scan and $O(M \log M)$.

## Applications

- **Reports over logs and transactions.** The largest transactions of a day, the slowest requests of a server, or the top scores of a game, computed in one pass over data that is too large for memory. This is the example of Sedgewick and Wayne.
- **Nearest neighbors.** A brute-force $k$-nearest-neighbor search keeps the $k$ closest points so far in a max-heap of distances.
- **Search and recommendation.** A search engine scores many documents and returns the best few; see [top-k queries](/top-k-query/).
- **Beam search.** [Beam search](/beam-search/) keeps the best $M$ partial solutions at each step.

## References
