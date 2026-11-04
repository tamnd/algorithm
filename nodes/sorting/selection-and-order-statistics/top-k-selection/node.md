---
tag: WAHQ9F
kind: problem
slug: top-k-selection
name: Top-k selection
aliases:
- k smallest elements
- k largest elements
- partial selection
area: sorting/selection-and-order-statistics
level: intro
summary: Report the k smallest (or largest) elements, in any order or in sorted order.
model: comparison-model
complexity:
  vars: {n: the number of items, k: the number of items to report}
  time: {worst: Θ(n + k log k)}
prereqs: [selection-problem]
see_also: [heap-select, partial-sorting, largest-i-numbers-in-sorted-order, quickselect, top-k-query, top-m-problem, binary-heap, tournament-method]
sources:
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Chapter 9, Section 9.3 and the end-of-chapter problem "Largest i numbers in sorted order" (sort, heap and select-then-sort methods)
  - book: isbn:9780321573513
    title: Robert Sedgewick and Kevin Wayne, Algorithms, fourth edition
    locator: Section 2.4, Priority queues (the top-M client with a bounded priority queue) and Section 2.5, Applications (selection)
  - book: isbn:9780201896855
    title: Donald E. Knuth, The Art of Computer Programming, Volume 3, second edition
    locator: Section 5.3.3, Minimum-comparison selection (finding the t largest of n elements, in order or not)
  - paper: "Conrado Martínez, Partial quicksort, Proceedings of the Sixth Workshop on Algorithm Engineering and Experiments and the First Workshop on Analytic Algorithmics and Combinatorics (ALENEX/ANALCO 2004)"
    locator: the analysis of the expected cost of partial quicksort for the k smallest in sorted order
---

Top-k selection asks for the $k$ smallest items among $n$, either as a set in any order or in sorted order; the $k$ largest is the same problem with the order reversed. The unordered version takes $\Theta(n)$ time by [selection](/selection-problem/) followed by one partition pass. The sorted version takes $\Theta(n + k \log k)$ time in the [comparison model](/comparison-model/), and a [heap](/heap-select/) of $k$ candidates solves it in one pass over the input in $O(n \log k)$ time.

## In plain words

You have the scores of all runners in a race and you want the ten best. Sorting all scores works, but it also orders the slow runners, which nobody asked for.

One better way is to find the tenth best score first. Then one pass picks out every runner at least as fast, and only those ten need to be put in order.

Another way reads the scores one at a time and keeps a short list of the ten best seen so far, with the worst of them at hand. A new score that beats the worst on the list replaces it. Most scores are rejected with one look, so this is fast, and it needs room for only ten scores.

## Definition

**Input.** A sequence $a_1, \ldots, a_n$ of items with a [total order](/total-order/), and an integer $k$ with $1 \le k \le n$.

**Output, unordered.** A set of $k$ input positions $I$ such that $a_i \le a_j$ for each $i \in I$ and each $j \notin I$. When items repeat, the items equal to the [order statistic](/order-statistic/) $a_{(k)}$ may be split between $I$ and the rest in any way, so the set of positions is not unique, but the multiset of values $\{ a_i : i \in I \}$ is.

**Output, sorted.** The items $a_{(1)}, \ldots, a_{(k)}$ in this order.

**Cost.** Comparisons or time, in the worst case or in expectation. In the streaming version, also the extra space.

## Variants

- **Unordered or sorted.** The two outputs above. [Partial sorting](/partial-sorting/) is the sorted version done in place, and [the largest $i$ numbers in sorted order](/largest-i-numbers-in-sorted-order/) is the textbook form with the largest items.
- **Streaming.** The items arrive one at a time and memory is $O(k)$: only the heap method works, and the [top-M problem](/top-m-problem/) is this case.
- **Dynamic.** Items are inserted and deleted, and the $k$ smallest are asked from time to time. An [order-statistic tree](/order-statistic-tree/) answers each query in $O(k + \log n)$ time.
- **Multiple lists.** The $k$ best results from several sorted lists, as in a search engine or a database: the [top-k query](/top-k-query/), answered by a [k-way merge](/k-way-merge/) that stops after $k$ outputs.
- **Rank $k$ only.** Return $a_{(k)}$ and not the others: the [selection problem](/selection-problem/) itself.

## Examples

Let $A = [31, 41, 59, 26, 53, 58, 97, 93, 23, 84]$ with sorted order $23, 26, 31, 41, 53, 58, 59, 84, 93, 97$.

- For $k = 3$, the unordered output is the set $\{23, 26, 31\}$ and the sorted output is $23, 26, 31$.
- The $3$ largest are $97, 93, 84$ in decreasing order.
- **Select then filter.** The item of rank $3$ is $31$. One pass keeps the items that are at most $31$: $31$, $26$ and $23$, in input order. Sorting these three gives the sorted output.
- **Ties.** For $[5, 1, 5, 3, 5]$ and $k = 3$, the values are $1, 3, 5$, but any one of the three positions of $5$ is a correct choice for the third item.

## Known algorithms

| method | time | space | output |
|---|---|---|---|
| sort, then take $k$ | $O(n \log n)$ | depends on the sort | sorted |
| [select](/quickselect/), then partition | $O(n)$, expected or worst case by the selection method | $O(1)$ in place | unordered |
| select, partition, then sort the $k$ | $O(n + k \log k)$ | $O(1)$ in place | sorted |
| [heap of $k$ candidates](/heap-select/) | $O(n \log k)$ worst case | $O(k)$ | sorted after $k$ pops |
| build a heap of all items, pop $k$ | $O(n + k \log n)$ | $O(n)$ | sorted |
| [partial quicksort](/partial-sorting/) | $O(n + k \log k)$ expected | $O(\log n)$ stack | sorted |
| [tournament](/tournament-method/) | at most $n - 1 + (k - 1) \lceil \lg n \rceil$ comparisons | $O(n)$ | sorted |

**Heap of $k$ candidates.** Keep the $k$ smallest items seen so far in a max-heap. A new item that is less than the top replaces it and is sifted down. On a random order of distinct items, item $i > k$ enters the heap exactly when it is among the $k$ smallest of the first $i$ items, which has probability $k/i$. By [linearity of expectation](/linearity-of-expectation/), the expected number of replacements is $\sum_{i=k+1}^{n} k/i = k(H_n - H_k) \approx k \ln (n/k)$, so on random input most of the cost is one comparison per item, and the expected time is $O(n + k \log k \log (n/k))$.

**Which method to use.** For a one-off query on an array in memory, select then sort is the fastest in theory and in practice. For a stream, or when $n$ is unknown or the data does not fit in memory, the heap of $k$ candidates is the method of choice. For small $k$ and very large $n$, both make about $n$ comparisons.

## Bounds

**Unordered.** Each algorithm for the unordered output also gives $a_{(k)}$, the largest item of the output, after $k - 1$ more comparisons. So the [selection lower bound](/selection-lower-bound/) $n - 1 + \min(k - 1, n - k)$ applies up to $k - 1$, and the problem takes $\Theta(n)$ comparisons.

**Sorted.** An algorithm must read each item, so it needs $\Omega(n)$ time. The output also fixes the order of the $k$ smallest items, which can be in any of $k!$ orders, so a [decision tree](/decision-tree-model/) needs at least $\lg k! = \Omega(k \log k)$ comparisons. Together the bound is $\Omega(n + k \log k)$, and select, partition, then sort meets it. The finer counting bound $\lg (n!/(n-k)!)$, from the number of possible ordered outputs, is about $k \lg n$; it is $O(n + k \log k)$ for each $k$, since $k \lg n \le 2 k \lg k$ when $k \ge \sqrt{n}$ and $k \lg n \le \sqrt{n} \lg n$ otherwise.

**Space in a stream.** With items in a stream, $k$ items must be kept, since each of them may be in the answer.

## Reductions

- **To selection.** Find $x = a_{(k)}$, then keep the items less than $x$ and enough copies of $x$ to make $k$. Partition-based selection leaves the $k$ smallest in the first $k$ places of the array at no extra cost.
- **From selection.** The largest item of the unordered output is $a_{(k)}$.
- **To sorting.** Sorting gives the sorted output, but at $\Theta(n \log n)$ cost even for small $k$.

## Applications

- **Search and ranking.** A search engine returns the $k$ best documents by score, and a recommender the $k$ best items ([top-k query](/top-k-query/)).
- **Nearest neighbours.** The $k$ nearest neighbours of a query point are the $k$ smallest distances.
- **Monitoring.** The $k$ slowest requests or the $k$ largest files are kept by a heap of $k$ candidates over a log stream.
- **Pruning.** Beam search keeps the $k$ best partial solutions at each step.

## References
