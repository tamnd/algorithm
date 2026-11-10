---
tag: E0T4N3
kind: problem
slug: segmented-prefix-sums
name: Segmented prefix sums
aliases:
- segmented scan problem
- scan by key
area: parallel/parallel-primitives
level: core
summary: Prefix sums restarted at each segment boundary of a sequence.
prereqs: [all-prefix-sums]
see_also: [segmented-scan, compressed-sparse-row, sparse-matrix-vector-multiplication, parallel-quicksort, data-parallelism, scatter-and-gather, prefix-sums, histogram-computation]
sources:
  - url: https://www.cs.cmu.edu/~guyb/papers/Ble93.pdf
    title: Guy E. Blelloch, Prefix Sums and Their Applications, Technical Report CMU-CS-90-190, Carnegie Mellon University, 1990; also Chapter 1 of John H. Reif (editor), Synthesis of Parallel Algorithms, Morgan Kaufmann, 1993
    locator: Section 1.5, Segmented Scans, and Section 1.5.1, Example, Quicksort (seg-copy of the pivots and seg-split)
  - paper: doi:10.1109/12.42122
    title: Guy E. Blelloch, Scans as primitive parallel operations, IEEE Transactions on Computers 38(11), 1526 to 1538, 1989
    locator: Section II-C, Segments and Segmented Scans
  - paper: "Guy E. Blelloch, Michael A. Heroux and Marco Zagha, Segmented Operations for Sparse Matrix Computation on Vector Multiprocessors, Technical Report CMU-CS-93-173, Carnegie Mellon University, 1993"
    title: Segmented Operations for Sparse Matrix Computation on Vector Multiprocessors
    locator: the sparse matrix-vector product with a segmented sum over the rows
  - paper: "Shubhabrata Sengupta, Mark Harris, Yao Zhang and John D. Owens, Scan Primitives for GPU Computing, Graphics Hardware 2007, pages 97 to 106"
    title: Scan Primitives for GPU Computing
    locator: the segmented scan and its applications to quicksort and sparse matrix-vector products on the GPU
---

The segmented prefix sums problem asks for the running totals of each segment of an array, where the array is cut into contiguous segments and the total starts again from zero at each segment start. It is many independent [prefix sums](/all-prefix-sums/) problems packed into one flat array. The [segmented scan](/segmented-scan/) solves it, and the more general problem for any associative operator, with one ordinary scan on (flag, value) pairs, in $\Theta(n)$ work and $\Theta(\log n)$ span whatever the segments are. This lets a parallel program treat thousands of small sequences, such as the rows of a sparse matrix, as one large task.

## In plain words

A bank keeps all account entries in one long list, sorted by account, and wants a running balance inside each account. The balance must start again at the first entry of each account and must never carry over from the account before it.

Doing each account on its own is easy, but with millions of short accounts, setting up a separate job for each one costs more than the additions. The segmented prefix sums problem is the question of how to get all the running balances in one pass over the whole list, with the marks that show where each account starts.

## Definition

The input is an array $a_0, \ldots, a_{n-1}$ of numbers and a description of segments: contiguous ranges that cover $0, \ldots, n-1$ in order. Common descriptions are

- **head flags**: $f_i = 1$ when a segment starts at $i$, with $f_0 = 1$;
- **lengths**: $\ell_0, \ldots, \ell_{k-1}$ with $\sum_j \ell_j = n$;
- **offsets**: the start index of each segment, as in the row pointer array of [compressed sparse row](/compressed-sparse-row/) storage;
- **keys**: a key for each item, with equal keys adjacent, and a segment for each run of equal keys.

Let $s(i)$ be the start of the segment of $i$. The **inclusive** output is $y_i = a_{s(i)} + \cdots + a_i$, and the **exclusive** output is $y_i = a_{s(i)} + \cdots + a_{i-1}$, which is 0 at each segment start. Costs are counted in additions in the [work-span model](/work-span-model/).

**Relation to segmented scan.** This page is the problem for addition. The [segmented scan](/segmented-scan/) page gives the algorithm, which works for any [associative operator](/associative-operator/) with an identity: $\max$, $\min$, products, matrix products, or the "copy the first value" operator. The segmented scan with $+$ is the main algorithm for this problem.

## Variants

- **Segmented reduce.** Only the total of each segment, which is the inclusive value at the last item of the segment. With $k$ segments the output has $k$ items.
- **Backward.** Totals from each item to the end of its segment.
- **Other operators.** The segmented max, min, OR, or copy. Each is a segmented scan with the matching operator.
- **Empty segments.** With lengths or offsets, a segment may be empty; with flags it cannot. Empty segments matter for a segmented reduce, whose output must still have an entry for them.
- **Scan by key.** GPU libraries offer the problem with keys in place of flags: a new segment starts wherever the key changes.

## Examples

For $a = [3, 1, 7, 0, 4, 1, 6, 3]$ with segment lengths $[2, 3, 3]$, so flags $[1, 0, 1, 0, 0, 1, 0, 0]$:

| $i$ | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 |
|---|---|---|---|---|---|---|---|---|
| $a_i$ | 3 | 1 | 7 | 0 | 4 | 1 | 6 | 3 |
| inclusive | 3 | 4 | 7 | 7 | 11 | 1 | 7 | 10 |
| exclusive | 0 | 3 | 0 | 7 | 7 | 0 | 1 | 7 |

The segmented reduce gives $[4, 11, 10]$. With one segment the problem is the plain prefix sum $[3, 4, 11, 11, 15, 16, 22, 25]$. With every flag set, the inclusive output equals the input.

## Known algorithms

- **[Segmented scan](/segmented-scan/).** One scan with the operator $(f, x) \oplus_s (g, y) = (f \lor g,\ g\ ?\ y : x + y)$, which is associative. With a work-efficient scan this takes $\Theta(n)$ work and $\Theta(\log n)$ span for any segments.
- **One scan per segment.** Run a scan on each segment in parallel. The work is the same, but each segment costs a task, and long segments make the load uneven.
- **Subtract at the starts.** Because $+$ has an inverse, compute the plain exclusive prefix sums $P$, find the start $s(i)$ of each segment with a $\max$-scan of the values $i \cdot f_i$, and output $y_i = P_{i+1} - P_{s(i)}$ for the inclusive form. This uses two plain scans and a gather. With floating-point numbers it can lose accuracy, because it subtracts large totals.
- **Sequential.** One loop that resets the total at each flag, with $n$ additions and no extra space.

## Bounds

The work is at least $n - k$ additions for $k$ segments, since each item that is not a segment start needs one, and the segmented scan is within a constant factor of that. The span is at least $\lceil \lg \ell \rceil$ for the longest segment of length $\ell$, as for any prefix sum. An algorithm that works for every set of segments in one pass, such as the segmented scan, has span $\Theta(\log n)$, the bound for one segment of length $n$. On an EREW PRAM, the segmented scan runs in $O(\log n)$ time with $n / \lg n$ processors, the same as a plain scan.

## Reductions

- **To a plain scan.** The segmented problem with any associative operator reduces to one plain scan with the segmented operator; this is the content of the [segmented scan](/segmented-scan/) algorithm. So every scan algorithm and every scan circuit also solves the segmented problem.
- **From a plain scan.** A plain scan is the segmented problem with a single segment.
- **With inverses, to plain scans and a gather.** For $+$, as in the subtraction method above.
- **Descriptions.** Lengths turn into offsets with an exclusive $+$-scan, offsets into flags with a [scatter](/scatter-and-gather/) of 1s, and flags into offsets with a [pack](/parallel-pack/) of the flagged indices. Keys turn into flags by comparing each key with the one before it, which is a map.

## Applications

- **Sparse matrix-vector product.** In [compressed sparse row](/compressed-sparse-row/) form, the nonzeros of all rows are stored in one array. The product $y = Ax$ multiplies each nonzero $a_{ij}$ by $x_j$, which is a map with a gather, and then sums the products of each row, which is a segmented reduce with the rows as segments. Blelloch, Heroux and Zagha (1993) used this method on vector machines, and it balances the load even when the row lengths are very uneven. See [sparse matrix-vector multiplication](/sparse-matrix-vector-multiplication/).
- **Quicksort without recursion.** Blelloch's quicksort (Section 1.5.1) keeps all subarrays of one level of the recursion as segments of one array. In each round, a segmented copy gives each item the pivot of its segment, each item compares itself with its pivot, a segmented split puts the smaller items before the others inside each segment, using segmented $+$-scans of the flags to compute the positions, and new flags mark the new segments. All subproblems of a level are handled by a fixed number of segmented scans, however many there are. See [parallel quicksort](/parallel-quicksort/).
- **Nested data parallelism.** A nested sequence, such as a list of lists, is stored as one flat array of values and a segment descriptor. Every operation on the inner lists then becomes a segmented operation on the flat array. This flattening is how NESL runs nested [data-parallel](/data-parallelism/) programs on flat hardware.
- **Grouped totals.** Totals per group of sorted records, such as sales per customer, are a segmented reduce, or a reduce by key. If the records are not sorted, sort them by key first or use a [histogram](/histogram-computation/) method.
- **Graph algorithms.** The adjacency lists of all vertices are segments of one edge array, so a segmented reduce computes, for example, the minimum edge weight at every vertex at once.

## References
