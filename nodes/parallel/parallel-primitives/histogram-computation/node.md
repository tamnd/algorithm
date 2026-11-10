---
tag: S4ZBZT
kind: problem
slug: histogram-computation
name: Histogram computation
aliases:
- counting occurrences
area: parallel/parallel-primitives
level: intro
summary: Count how many items of a sequence have each key. In parallel, private counts plus a reduce, shared atomic counters, and sort then segment trade work against span as the number of keys grows.
prereqs: [work-span-model, parallel-reduce]
see_also: [parallel-histogram, counting-sort, radix-sort, image-histogram, word-count, warp-aggregated-atomics, segmented-scan, fetch-and-add]
sources:
  - book: isbn:9780323912310
    title: David B. Kirk, Wen-mei W. Hwu and Izzat El Hajj, Programming Massively Parallel Processors, 4th edition, Morgan Kaufmann, 2022
    locator: Chapter 9, parallel histogram (atomic operations, contention and privatization)
  - book: isbn:9780262033848
    title: Thomas H. Cormen, Charles E. Leiserson, Ronald L. Rivest and Clifford Stein, Introduction to Algorithms, 3rd edition, MIT Press, 2009
    locator: Chapter 8, Section 8.2 (counting sort, whose first loop is a histogram) and Chapter 27, Section 27.1 (the work-span model)
---

Histogram computation asks, for a sequence of $n$ items with keys from $k$ possible values, how many items have each key. In sequence it is one loop that adds 1 to a counter for each item. In parallel the loop is hard, because all items write to only $k$ counters, and when $k$ is small or the keys are skewed, many tasks want the same counter at the same time. The methods differ in how they remove this contention: each block counts into its own counters, the counters are shared and updated by atomic operations, or the items are sorted so that equal keys sit together. Which method is best depends mostly on $k$ compared with $n$.

Notation on this page: $x[0 \ldots n-1]$ is the input, $k$ the number of bins, $H$ the output, $p$ the number of blocks or processors, and $c = \max_j H[j]$ the size of the largest bin. $W$ is the work and $S$ the span in the [work-span model](/work-span-model/). $\lg$ is $\log_2$.

## In plain words

A shop wants to know how many of each product it sold today. The sales list is long, and there are only a few products.

One clerk can go down the list and make a mark next to the right product for each sale. With many clerks, they all want to mark the same few lines at the same time.

There are three ways out. Each clerk can keep a private tally of their part of the list, and the tallies are added at the end. The clerks can take turns at the shared tally, which is fine if the products are many and the clerks rarely meet. Or the list can first be sorted by product, and then each run of equal products is simply counted.

## Definition

**Input.** An array $x[0 \ldots n-1]$ with each $x[i] \in \{0, \ldots, k-1\}$. When the items are values of another type, a bin function first maps each item to its bin.

**Output.** The array $H[0 \ldots k-1]$ with

$$H[j] = |\{ i : x[i] = j \}| \quad \text{for } 0 \le j < k.$$

The counts add up to $n$. The output has $k$ entries, so any method has work $\Omega(k)$ to write it, besides $\Omega(n)$ to read the input.

## Variants

- **Weighted histogram.** Each item has a weight, and $H[j]$ is the sum of the weights of the items with key $j$. Any associative and commutative operator can replace the sum, for example the maximum. With floating point weights the order of the additions changes the result, so a method with a fixed order of additions is deterministic and one with atomics is not.
- **Sparse keys.** The keys come from a large universe, and only the keys that occur must be listed, with their counts. A dense array of $k$ counters is then too large; sort the keys, or count into a hash table.
- **Cumulative histogram.** The output is the prefix sums of $H$, which give for each key the number of items with a smaller key. This is a histogram followed by an [all prefix sums](/all-prefix-sums/) over $k$ entries.
- **Many dimensions.** The key is a tuple, for example the colour channels of a pixel, and the bins form a grid that is stored as one array.

## Examples

Let $x = [2, 0, 1, 2, 2, 3, 0, 2, 1, 3]$ with $k = 4$. Then $H = [2, 2, 4, 2]$.

- **Private counts.** With four blocks $[2, 0, 1]$, $[2, 2, 3]$, $[0, 2, 1]$ and $[3]$, the private counts are $[1, 1, 1, 0]$, $[0, 0, 2, 1]$, $[1, 1, 1, 0]$ and $[0, 0, 0, 1]$. Their sum is $H$. The [parallel histogram](/parallel-histogram/) page works this case out with its exact work 50 and span 15.
- **Shared atomics.** Ten tasks each add 1 to $H[x[i]]$ with an atomic [fetch and add](/fetch-and-add/). The four additions to $H[2]$ must take turns, so they take at least 4 steps, even with ten processors.
- **Sort then segment.** Sorting gives $[0, 0, 1, 1, 2, 2, 2, 2, 3, 3]$. The runs start at the positions 0, 2, 4 and 8, so the counts are the differences $2, 2, 4$ and $10 - 8 = 2$.

**The trade-off with the number of blocks.** For $n = 10^6$ items and $k = 256$ bins, the privatized method of the [parallel histogram](/parallel-histogram/) page has these exact costs.

| blocks $p$ | work $W$ | span $S$ |
|---|---|---|
| 1 | 1000256 | 1000256 |
| 64 | 1048640 | 15941 |
| 976 | 1749056 | 1381 |
| 3906 | 3999296 | 633 |

Each step to more blocks cuts the span, but the work for the private arrays, $3pk$, grows until it is larger than the count of the items. For $k = 16$ bins, $p = 62500$ blocks give a span of 128 with a work below $4n$.

## Known algorithms

| method | work | span | page |
|---|---|---|---|
| sequential loop | $\Theta(n + k)$ | $\Theta(n + k)$ | [counting sort](/counting-sort/), first loop |
| private counts per block, then a tree of parallel adds | $n + 3pk - 2k$ | $O(n/p + k + \log p \log k)$ | [parallel histogram](/parallel-histogram/) |
| private counts per block, then one reduction per bin | $\Theta(n + pk)$ | $O(n/p + \log p + \log k)$ | [parallel histogram](/parallel-histogram/), variants |
| shared counters with atomic adds | $\Theta(n + k)$ | $\Omega(c)$, as each bin takes its additions in turn | [warp aggregated atomics](/warp-aggregated-atomics/) |
| sort, then count each run with a segmented scan | $\Theta(n \log n)$ | $O(\log^2 n)$ | [parallel merge sort](/parallel-merge-sort/), [segmented scan](/segmented-scan/) |
| one flag per item and bin, then $k$ reductions | $\Theta(nk)$ | $\Theta(\log n + \log k)$ | [parallel reduce](/parallel-reduce/) |

The third row sets the zeros of each block in parallel and sums each bin over the $p$ arrays by its own reduction. In the third row, the choice $p = \lceil n/k \rceil$ gives $O(n)$ work and a span of $O(k + \log n)$. For the atomic method, the span is small when the keys spread over many bins, since then $c$ is small, and it is $n$ when all keys are the same. Sort then segment does not depend on $k$ and lists only the keys that occur, so it suits sparse keys; the span uses a merge sort whose merges cut the output by co-ranking, as on the [merging sorted sequences](/merging-sorted-sequences/) page.

## Bounds

- **Work.** Each item must be read and each of the $k$ outputs written, so $W = \Omega(n + k)$. The sequential loop meets this bound.
- **Span.** Each $H[j]$ depends on all $n$ inputs, since a change to any item can change it. With tasks that fork into two, a value that depends on $n$ inputs needs span $\Omega(\log n)$.
- **Both at once.** For $k = O(\log n)$, private counts with $p = \lceil n / \lg n \rceil$ blocks and one reduction per bin give $O(n)$ work and $O(\log n)$ span, so both bounds are met. For the privatized methods in general, the work is at least $pk$ and the span at least $n/p$, so their product is at least $nk$, and linear work forces a span of $\Omega(k)$.

## Reductions

- **Histogram reduces to a reduce.** The histogram is a [parallel reduce](/parallel-reduce/) over the items, with the item $j$ mapped to the array with a 1 at place $j$, and arrays added entry by entry. This operator is associative and commutative, which is why the private counts may be added in any tree.
- **Histogram reduces to sorting.** After a sort, the run boundaries come from comparing each item with its neighbour, a parallel [compaction](/compaction/) keeps the boundaries, and the differences of their positions are the counts.
- **Counting sort reduces to histogram.** A histogram, an exclusive prefix sum over the $k$ counts, and a scatter of each item to its place give [counting sort](/counting-sort/). Each pass of a parallel [radix sort](/radix-sort/) runs this with $k$ equal to the radix.

## Applications

- The first step of [counting sort](/counting-sort/) and of each pass of [radix sort](/radix-sort/), and the bucket sizes in sample sort.
- [Image histograms](/image-histogram/) for contrast, equalization and thresholds, with 256 bins per channel.
- [Word count](/word-count/) and other counts by key in MapReduce, where the combiner plays the part of the private counts.
- Load balance and partitioning: counting the keys that go to each machine or bucket before the data moves.
- Statistics over large data: frequency tables, the bins of a distribution, and the counts of a join key.

## References
