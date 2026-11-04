---
tag: 0YXEH5
kind: algorithm
slug: heap-select
name: Heap-based selection
aliases:
- bounded heap top-k
area: sorting/selection-and-order-statistics
level: intro
summary: Keep a heap of at most k candidates to find the k smallest elements in O(n log k) time.
solves: [top-k-selection, selection-problem]
model: comparison-model
complexity:
  vars: {n: the number of items, k: the number of items to report}
  time: {worst: Θ(n log k), best: Θ(n + k log k)}
  space: {extra: Θ(k)}
properties: {stable: false, in_place: false, adaptive: false, online: true, deterministic: true, comparison: true, recursive: false}
history:
  year: 1964
  people: [J. W. J. Williams]
  note: Williams introduced the binary heap with Heapsort in 1964; keeping a bounded heap of the best k candidates is a direct use of it that is standard in textbooks.
prereqs: [binary-heap, top-k-selection]
see_also: [top-m-problem, quickselect, partial-sorting, heapsort, sift-down, priority-queue, largest-i-numbers-in-sorted-order, tournament-method]
sources:
  - book: isbn:9780321573513
    title: Robert Sedgewick and Kevin Wayne, Algorithms, fourth edition
    locator: Section 2.4, Priority queues (the client TopM, which keeps the M largest items of a stream in a priority queue of size M + 1)
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Chapter 6, Heapsort (MAX-HEAPIFY, BUILD-MAX-HEAP and HEAPSORT), and the Chapter 9 problem "Largest i numbers in sorted order"
  - paper: doi:10.1145/512274.3734138
    title: J. W. J. Williams, Algorithm 232, Heapsort, Communications of the ACM 7(6) (1964)
    locator: pages 347 to 348
  - book: isbn:9780201896855
    title: Donald E. Knuth, The Art of Computer Programming, Volume 3, second edition
    locator: Section 5.2.3, Sorting by selection (heaps), and Section 5.3.3, Minimum-comparison selection
---

Heap-based selection finds the $k$ smallest of $n$ items by reading the items once and keeping the $k$ smallest seen so far in a max-heap of size $k$. A new item is compared with the top of the heap, the largest candidate, and replaces it only if it is smaller. The method takes $O(n \log k)$ time in the worst case and $O(k)$ extra space, it works on a stream whose length is not known in advance, and at the end a [heapsort](/heapsort/) of the heap gives the $k$ smallest in sorted order. It solves [top-k selection](/top-k-selection/), and the largest item of its output is the item of rank $k$.

## In plain words

You want the ten cheapest flights from a long list that arrives one flight at a time. You keep a short list of the ten cheapest so far, and you always know which of them is the most expensive.

For each new flight you ask one question: is it cheaper than the most expensive flight on my list? Most of the time the answer is no, and you go on. If the answer is yes, the new flight takes the place of that one, and you find the new most expensive flight on your list.

A heap is a way to keep the short list so that this last step is fast: it takes a few steps even if the list is long. At the end you sort the short list.

## The problem

The input is a sequence $a_0, \ldots, a_{n-1}$ of items with a [total order](/total-order/), read once from left to right, and an integer $k \ge 0$. The output is the $\min(k, n)$ smallest items in increasing order: $a_{(1)}, \ldots, a_{(\min(k,n))}$, where $a_{(i)}$ is the [order statistic](/order-statistic/) of rank $i$. This is the sorted form of [top-k selection](/top-k-selection/). For the $k$ largest items, reverse the order and keep a min-heap.

## The algorithm

$H[0 \ldots m-1]$ is a binary max-heap in an array: the children of index $i$ are $2i + 1$ and $2i + 2$, and each item is at least the items of its children. SIFT-DOWN is the usual [sift-down](/sift-down/) step of a [binary heap](/binary-heap/).

```pseudo id=main
HEAP-SELECT(a, k)                          ▷ return the k smallest items, sorted
L1  H ← the first min(k, n) items of a; m ← |H|
L2  for i ← ⌊m/2⌋ − 1 downto 0 do SIFT-DOWN(H, i, m)   ▷ build a max-heap
L3  for each next item x of a do
L4      if x < H[0] then                   ▷ H[0] is the largest candidate
L5          H[0] ← x
L6          SIFT-DOWN(H, 0, m)
L7  for j ← m − 1 downto 1 do             ▷ heapsort the candidates
L8      swap H[0] and H[j]
L9      SIFT-DOWN(H, 0, j)
L10 return H

SIFT-DOWN(H, i, m)                         ▷ the subtrees below i are max-heaps
L11 loop
L12     c ← 2i + 1
L13     if c ≥ m then return
L14     if c + 1 < m and H[c] < H[c + 1] then c ← c + 1
L15     if not H[i] < H[c] then return
L16     swap H[i] and H[c]; i ← c
```

Lines L1 and L2 put the first $k$ items in a heap with the bottom-up method, in $O(k)$ time. Line L4 is the filter: an item that is not less than the largest candidate cannot be among the $k$ smallest, since the $k$ candidates are all at most it. An item that passes takes the place of the largest candidate, and line L6 restores the heap order. After the last item, lines L7 to L9 are the second phase of heapsort: each step moves the largest remaining candidate to the end of the heap area. So $H$ ends in increasing order.

## Example

Let $a = [31, 41, 59, 26, 53, 58, 97, 93, 23, 84]$ and $k = 3$.

Line L2 turns $[31, 41, 59]$ into the max-heap $[59, 41, 31]$ with 2 comparisons. Then:

| item | test of L4 | heap after the step | comparisons |
|---|---|---|---|
| 26 | $26 < 59$, replace | [41, 26, 31] | 3 |
| 53 | $53 \ge 41$, skip | [41, 26, 31] | 1 |
| 58 | skip | [41, 26, 31] | 1 |
| 97 | skip | [41, 26, 31] | 1 |
| 93 | skip | [41, 26, 31] | 1 |
| 23 | $23 < 41$, replace | [31, 26, 23] | 3 |
| 84 | $84 \ge 31$, skip | [31, 26, 23] | 1 |

When $26$ enters, it is placed at the root, and SIFT-DOWN compares the children $41$ and $31$, then $26$ with $41$, and swaps them. Lines L7 to L9 sort $[31, 26, 23]$ into $[23, 26, 31]$ with 1 comparison. The run makes $2 + 11 + 1 = 14$ comparisons. The top of the heap before the sort, $31$, is the item of rank $3$.

## Correctness

After line L2, and after each pass of the loop of line L3, this [loop invariant](/loop-invariant/) holds: $H[0 \ldots m-1]$ is a max-heap, and as a multiset it is a set of $m$ smallest items of the prefix read so far. When a new item $x$ is read, either $x \ge H[0]$, and then each candidate is at most $x$, so the candidates are still $m$ smallest items of the longer prefix; or $x < H[0]$, and then $H[0]$ has at least $m$ items of the prefix at most it, counting $x$, so it can be dropped for $x$. SIFT-DOWN restores the heap order. At the end of the input the heap holds $m$ smallest items of the whole input, and the heapsort phase puts them in order. The full proof, with the proof of SIFT-DOWN, is in the proof file below.

## Complexity

Let $m = \min(k, n)$. A SIFT-DOWN on a heap of $m$ items makes at most $2 \lfloor \lg m \rfloor$ comparisons.

- **Worst case, $\Theta(n \log k)$.** Building the heap costs $O(k)$. Each of the $n - k$ later items costs one comparison in line L4, and at most $O(\log k)$ more if it enters the heap. The final sort costs $O(k \log k)$. So the total is $O(n \log k)$. A decreasing input makes each item enter the heap and sink to a leaf: for $n = 10^5$ and $k = 100$ the method makes about $12.5n$ comparisons, close to $2 n \lg k \approx 13.3n$.
- **Best case, $\Theta(n + k \log k)$.** On an increasing input no item after the first $k$ enters the heap, so the loop costs $n - k$ comparisons. For $n = 10^5$ and $k = 100$ the method makes $100981$ comparisons: $99900$ in the loop and the rest in the build and the sort.
- **Random order, $n + O(k \log k \log(n/k))$.** For distinct items in a uniformly random order, item $i > k$ (counted from 1) enters the heap exactly when it is among the $k$ smallest of the first $i$ items, which has probability $k/i$. By [linearity of expectation](/linearity-of-expectation/) the expected number of replacements is
$$ \sum_{i=k+1}^{n} \frac{k}{i} = k (H_n - H_k) \approx k \ln \frac{n}{k}, $$
where $H_m$ is the $m$-th [harmonic number](/harmonic-series/). For $n = 10^5$ and $k = 100$ this is $690.3$, and $20$ random inputs averaged $685.9$ replacements and $1.08n$ comparisons.
- **Space, $\Theta(k)$.** The heap holds $k$ items. The input is read once and need not be stored.

## Properties

- **Online.** It reads each item once, in order, and at each moment the heap holds the $k$ smallest items so far. So it works on a stream, and it can report the current $k$-th smallest at any time as $H[0]$.
- **Not in place.** It uses $\Theta(k)$ memory outside the input. If the input is an array that may be changed, the heap can live in $a[0 \ldots k-1]$.
- **Not stable.** Equal items can leave the heap in any order. To break ties by position, compare pairs $(a_i, i)$.
- **Deterministic and comparison based.** It uses only comparisons between items.

## Variants and improvements

- **The $k$ largest.** Use a min-heap and the test $x > H[0]$. This is the TopM client of Sedgewick and Wayne, which keeps the $M$ largest transactions of a stream ([top-M problem](/top-m-problem/)).
- **Rank $k$ only.** Skip the sort of lines L7 to L9 and return $H[0]$. This is [selection](/selection-problem/) in $O(n \log k)$ time, useful when $k$ is small or the input is a stream.
- **Heap of all items.** Build a min-heap of all $n$ items in $O(n)$ time and pop $k$ times: $O(n + k \log n)$ time, but $\Theta(n)$ space and no streaming. CLRS lists it as one answer to "the largest $i$ numbers in sorted order".
- **Replace in one step.** Python's `heapq.heapreplace` and `heapq.nsmallest` implement lines L5 and L6 and this whole method.
- **Partition instead.** On an array in memory, [quickselect](/quickselect/) followed by a sort of the first $k$ items takes $O(n + k \log k)$ expected time, which is better for large $k$; see [partial sorting](/partial-sorting/).

## When to use it

Use it when the items come from a stream or a file too large for memory, when $n$ is not known in advance, or when the $k$ smallest so far must be known at each moment. It is also a good choice when $k$ is much smaller than $n$, since on most inputs nearly all items are rejected with one comparison. For an array in memory and large $k$, selection by partition followed by a sort of $k$ items is faster.

## Pitfalls

- **A min-heap for the $k$ smallest.** The filter needs the largest candidate at the top, so the $k$ smallest need a max-heap and the $k$ largest a min-heap. With the wrong heap, the method throws away the wrong item.
- **Pushing before popping.** Pushing $x$ and then popping the top makes the heap grow to $k + 1$ items for a moment; this is correct, as in TopM, but it costs a sift-up and a sift-down for each item. Testing $x < H[0]$ first is cheaper.
- **Fewer than $k$ items.** If $n < k$, the heap never fills. The loop of line L3 must not run before the heap is full, and the result has $n$ items.
- **Ties at the boundary.** With the strict test $x < H[0]$, an item equal to the largest candidate is skipped. The values of the output are still correct, but which copies are kept depends on the input order.

## Implementations

## History

J. W. J. Williams introduced the binary heap with Heapsort, Algorithm 232 in the Communications of the ACM, in June 1964, and Floyd gave the linear-time bottom-up construction the same year. A bounded heap of the best $k$ candidates is a direct use of the structure; textbooks present it as the standard method for the $k$ largest items of a stream, for example the TopM client of Sedgewick and Wayne.

## References
