---
tag: 8TCN5X
kind: concept
slug: sorted-run
name: Sorted run
aliases:
- run
area: sorting/external-sorting
level: intro
summary: A maximal or fixed-size block of records already in sorted order, produced during run formation and merged later.
prereqs: [sorting-problem]
see_also: [external-merge-sort, replacement-selection, k-way-merge, natural-merge-sort, timsort, adaptive-sorting, eulerian-numbers, log-structured-merge-tree]
sources:
  - book: isbn:9780201896855
    title: Donald E. Knuth, The Art of Computer Programming, Volume 3, second edition
    locator: Section 5.1.3 (Runs), Section 5.2.4 (natural merge sort) and Section 5.4.1 (run formation by replacement selection)
  - paper: doi:10.1561/0400000014
    title: Jeffrey Scott Vitter, Algorithms and Data Structures for External Memory, Foundations and Trends in Theoretical Computer Science 2(4), 2008
    locator: Section 5.2, Sorting by Merging (run formation and merge passes)
  - paper: doi:10.1145/48529.48535
    title: Alok Aggarwal and Jeffrey Scott Vitter, The input/output complexity of sorting and related problems, Communications of the ACM 31(9), 1988, pages 1116 to 1127
    locator: the merge sort algorithm (runs of M items and merges of M/B runs)
---

A sorted run is a sequence of consecutive records that are in non-decreasing order. In a sort it is the unit of work: an [external merge sort](/external-merge-sort/) first makes runs, then merges them with a [k-way merge](/k-way-merge/), and the number of runs sets the number of merge passes. The runs of an input can be the maximal ascending pieces that it already has, pieces of a fixed size that are sorted in memory, or the longer runs of [replacement selection](/replacement-selection/).

## In plain words

A run is a part of a list that is already in order. A sort that merges works on runs: it merges two or more runs into one longer run, until one run holds all the items.

There are two ways to get runs. You can look at the list and cut it where an item is smaller than the item before it. Each piece is then a run. A list that is almost sorted has a few long runs, and a sort that uses them finishes fast. Or you can make runs yourself: take as many items as fit in memory, sort them, and write them out as one run. When the data is on disk, this second way is the first phase of the sort, and the merges are the second phase. Fewer runs means fewer merges, so methods that make long runs save time.

## The idea

Let $X = (x_1, \ldots, x_n)$ be a sequence over a totally ordered set. A *run* of $X$ is a segment $x_i, x_{i+1}, \ldots, x_j$ with $i \le j$ and $x_i \le x_{i+1} \le \cdots \le x_j$. A run is *maximal* when it cannot be extended: $i = 1$ or $x_{i-1} > x_i$, and $j = n$ or $x_j > x_{j+1}$.

**The count of maximal runs.** A *descent* of $X$ is a position $i$ with $x_i > x_{i+1}$. The maximal runs of a non-empty $X$ are the segments between the descents, so

$$\text{the number of maximal ascending runs} = 1 + \text{the number of descents}.$$

The number of permutations of $\{1, \ldots, n\}$ with exactly $r$ maximal ascending runs is the [Eulerian number](/eulerian-numbers/) $\left\langle {n \atop r-1} \right\rangle$. For a uniformly random permutation with $n \ge 2$, each of the $n - 1$ positions is a descent with probability $1/2$, because $x_i > x_{i+1}$ and $x_i < x_{i+1}$ have the same probability. By [linearity of expectation](/linearity-of-expectation/), the expected number of maximal runs is $1 + (n-1)/2 = (n+1)/2$, so the average run has a length of about 2. A random input has almost no order that a sort can use.

**Runs made by run formation.** An external sort does not wait for the input to have long runs. It makes them:

- *Load, sort, store.* Read $M$ items, sort them in memory, write them as one run. This gives $\lceil N/M \rceil$ runs of $M$ items, except the last.
- *Replacement selection.* Keep a heap of $M$ items. Output the smallest item that can still extend the current run, and read the next input item into its place. On random input the runs have an expected length of about $2M$; the proof is on the page [replacement selection run length](/replacement-selection-run-length/). On a sorted input there is one run.

**Why the count matters.** A merge of $k$ runs at a time reduces $r$ runs to $\lceil r/k \rceil$, so an external merge sort makes $\lceil \log_k r \rceil$ passes over the data. If run formation halves $r$, the number of passes drops by at most one. With $k = 2$, as in a sort with few tapes, it always drops by one. With a large $k$, as on disk, it drops only when $r$ is a little more than a power of $k$, for example when $k < r \le 2k$, where the sort then needs one pass instead of two.

**Descending runs.** A *strictly descending* run $x_i > x_{i+1} > \cdots > x_j$ can be reversed in place to give an ascending run. It must be strict: a reversal of equal items changes their order, and the sort is then not [stable](/stable-sort/). [Timsort](/timsort/) uses both kinds.

## Examples

Take $X = (3, 8, 9, 2, 5, 1, 4, 7, 6)$. The descents are at $9 > 2$, $5 > 1$ and $7 > 6$, so there are 4 maximal runs: $(3, 8, 9)$, $(2, 5)$, $(1, 4, 7)$ and $(6)$. The segment $(8, 9)$ is a run, but it is not maximal.

For $n = 4$, the Eulerian numbers are 1, 11, 11 and 1: of the 24 permutations, 1 has one run, 11 have two, 11 have three and 1 has four. The mean is $(1 + 22 + 33 + 4)/24 = 2.5 = (4+1)/2$.

The three kinds of runs differ much on the same input. Take the 12 items $(5, 1, 9, 3, 7, 2, 8, 6, 4, 10, 0, 11)$ and a memory of 3 items.

| method | the runs | runs |
|---|---|---|
| maximal ascending runs | (5) (1 9) (3 7) (2 8) (6) (4 10) (0 11) | 7 |
| load, sort, store | (1 5 9) (2 3 7) (4 6 8) (0 10 11) | 4 |
| replacement selection | (1 3 5 7 8 9) (2 4 6 10 11) (0) | 3 |

The first run of replacement selection has 6 items, two times the memory.

A non-example: in the list $(4, 1, 2, 3, 6)$, the items $(1, 2, 6)$ are in order, but they are not a run, because they are not consecutive. A run is always a segment. The maximal runs of this list are $(4)$ and $(1, 2, 3, 6)$.

## Where it is used

- **External merge sort.** The two phases are run formation and the merge of runs. See [external merge sort](/external-merge-sort/) and [replacement selection](/replacement-selection/).
- **Tape sorts.** [Balanced merge sort](/balanced-merge-sort/), [polyphase merge sort](/polyphase-merge-sort/) and [cascade merge sort](/cascade-merge-sort/) choose how many runs each tape gets. Polyphase and cascade add empty *dummy runs* to reach a good distribution.
- **Adaptive sorts.** The number of runs is a measure of presortedness. [Natural merge sort](/natural-merge-sort/) and [Timsort](/timsort/) take $O(n \log r)$ comparisons on an input with $r$ runs. See [adaptive sorting](/adaptive-sorting/).
- **Storage engines.** A [log-structured merge tree](/log-structured-merge-tree/) writes its buffer to disk as a sorted run and merges runs in the background.
- **Joins.** A [sort-merge join](/sort-merge-join/) can merge the runs of both inputs in the last pass of the sort and join at the same time.

## References
