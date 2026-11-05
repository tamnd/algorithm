---
tag: VXFMJM
kind: algorithm
slug: brute-force-nearest-neighbor-search
name: Brute-force nearest neighbor search
aliases:
- linear scan
- exhaustive search for NN
area: searching/similarity-search
level: intro
summary: Compute the distance from the query to every point and keep the smallest; the baseline all indexes are measured against.
solves: [k-nearest-neighbor-search]
model: real-ram
complexity:
  vars: {n: the number of points, d: the dimension, k: the number of neighbors asked for}
  time: {worst: Θ(n d + n log k), best: Θ(n d + k log k)}
  space: {extra: Θ(k)}
properties: {stable: true, in_place: true, adaptive: false, online: true, deterministic: true, comparison: false, recursive: false}
prereqs: [k-nearest-neighbor-search, binary-heap, euclidean-distance]
see_also: [heap-select, top-k-selection, quickselect, kd-tree-nearest-neighbor-search, approximate-nearest-neighbor-search, curse-of-dimensionality, linear-search]
sources:
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Chapter 6, Heapsort, Section 6.5 Priority queues (the max-heap operations used to keep the k best), and Chapter 9, Medians and Order Statistics (selection in linear time)
  - book: isbn:9780123694461
    title: Hanan Samet, Foundations of Multidimensional and Metric Data Structures, Morgan Kaufmann, 2006
    locator: Chapter 4, High-Dimensional Data, Section 4.2 (k nearest neighbor finding with a max-priority queue of the k best candidates) and Section 4.4 (sequential scan as the baseline in high dimensions)
  - paper: doi:10.1109/TBDATA.2019.2921572
    title: Jeff Johnson, Matthijs Douze and Hervé Jégou, Billion-scale similarity search with GPUs, IEEE Transactions on Big Data 7(3), 2021
    locator: the sections on exact search (the squared distance decomposed into norms and one matrix product, followed by k-selection on the GPU)
---

Brute-force nearest neighbor search answers a [k-nearest neighbor](/k-nearest-neighbor-search/) query by computing the distance from the query to each of the $n$ stored points and keeping the $k$ smallest in a [max-heap](/binary-heap/). It takes $\Theta(nd + n \log k)$ time in the worst case for points in $\mathbb{R}^d$, needs no index and no preprocessing, and is exact for any distance. Each nearest neighbor index is judged by how much faster than this scan it is, and by the recall it reaches against the exact answer that the scan gives. In high dimensions the scan is often the fastest exact method.

## In plain words

To find the nearest shops to a house, measure the distance to every shop. Keep a short list of the best ones found so far, as long as the number of shops you want. When a new shop is closer than the worst shop on the list, drop that worst one and put the new shop on the list. At the end, sort the short list.

The list is kept so that its worst entry is always at the top, where you can see it at once. So each shop costs one measurement and, at most, a small update of the list.

## The problem

The input is a list $P[0 \ldots n-1]$ of points, a query point $q$, a distance $\delta$ and an integer $k \ge 1$. The output is the $\min(k, n)$ points of $P$ nearest to $q$, sorted by distance, as in [k-nearest neighbor search](/k-nearest-neighbor-search/). To make the answer unique, the algorithm orders the points by the pair $(\delta(q, P[i]), i)$ in lexicographic order: of two points at the same distance, the one with the smaller index comes first.

## The algorithm

$H$ is a max-heap of pairs $(\delta, i)$ in lexicographic order, so its top is the largest pair it holds.

```pseudo id=main
BRUTE-FORCE-KNN(P, q, k)
L1  H ← an empty max-heap of pairs (distance, index)
L2  for i ← 0 to n − 1 do
L3      δ ← dist(q, P[i])
L4      if |H| < k then INSERT(H, (δ, i))
L5      else if (δ, i) < TOP(H) then REPLACE-TOP(H, (δ, i))
L6  return the pairs of H in increasing order
```

Line L3 is the only place that looks at the points. Line L4 fills the heap with the first $k$ points. After that, line L5 compares each new pair with the worst pair kept so far, in $O(1)$ time, and only a better pair pays $O(\log k)$ for the heap update. Line L6 sorts the $\min(k, n)$ kept pairs, for example by extracting the maximum $k$ times and reversing.

For the Euclidean distance, line L3 can compute the squared distance $\sum_j (q_j - P[i]_j)^2$. The square root is increasing, so the order of the pairs, and so the answer, does not change.

## Example

Let $P = [(1,1), (2,4), (4,2), (5,5), (6,1), (7,3), (3,6), (4,4)]$, $q = (4, 3)$ and $k = 3$, with the squared Euclidean distance.

| $i$ | $P[i]$ | $\delta$ | line | $H$ after the step, sorted |
|---|---|---|---|---|
| 0 | (1,1) | 13 | L4 insert | (13, 0) |
| 1 | (2,4) | 5 | L4 insert | (5, 1), (13, 0) |
| 2 | (4,2) | 1 | L4 insert | (1, 2), (5, 1), (13, 0) |
| 3 | (5,5) | 5 | L5 replace (13, 0) | (1, 2), (5, 1), (5, 3) |
| 4 | (6,1) | 8 | L5 skip | (1, 2), (5, 1), (5, 3) |
| 5 | (7,3) | 9 | L5 skip | (1, 2), (5, 1), (5, 3) |
| 6 | (3,6) | 10 | L5 skip | (1, 2), (5, 1), (5, 3) |
| 7 | (4,4) | 1 | L5 replace (5, 3) | (1, 2), (1, 7), (5, 1) |

The output is $(4,2)$, $(4,4)$, $(2,4)$ at squared distances 1, 1 and 5. The point $(5,5)$ has the same distance as $(2,4)$, and the tie rule keeps $(2,4)$ because its index 1 is smaller than 3.

## Correctness

Write $\mathrm{best}_k(i)$ for the set of the $\min(k, i)$ smallest pairs among $(\delta(q, P[j]), j)$ for $j < i$. The pairs are distinct because the indices are, so this set is unique. The loop of line L2 keeps the invariant: at the start of iteration $i$, $H$ holds exactly $\mathrm{best}_k(i)$. A new pair joins the $k$ smallest exactly when there is room, or when it is smaller than the largest kept pair, and then that largest pair is the one to drop. At the end $i = n$, so line L6 returns the $\min(k, n)$ smallest pairs in order, which is a correct answer to the $k$-NN query, and the one with the smallest indices among ties. The full proof is in `proofs/correctness.md`.

## Complexity

The model is the [real RAM](/real-ram/): a distance in $\mathbb{R}^d$ costs $\Theta(d)$ operations, and a comparison of two pairs costs $O(1)$.

- **Distances.** Line L3 runs $n$ times: $\Theta(nd)$ time in each case. No exact algorithm without preprocessing can read fewer than all $n$ points, as shown on the [problem page](/k-nearest-neighbor-search/).
- **Heap.** Line L4 runs $\min(k, n)$ times and line L5 at most $n$ times, each in $O(\log k)$ time. The worst case is $\Theta(n \log k)$ when $n \ge 2k$: if the points come in order of decreasing distance, each of the last $n - k$ points replaces the top, and each REPLACE-TOP on a heap of size $k$ can cost $\Theta(\log k)$ sift steps. The best case for the heap is $\Theta(k \log k)$, when the first $k$ points are the answer and each later test of line L5 fails in $O(1)$.
- **Output.** Line L6 sorts $\min(k, n)$ pairs in $O(k \log k)$ time.
- **Total.** $\Theta(nd + n \log k)$ time in the worst case and $\Theta(nd + k \log k)$ in the best case, with $k \le n$. The extra space is $\Theta(k)$ for the heap.
- **Random order.** If the points come in uniformly random order with distinct distances, point $i$ (counting from 1) enters the heap with probability $\min(1, k/i)$, so the expected number of heap updates is $k + \sum_{i=k+1}^{n} k/i = k(1 + H_n - H_k) = O(k \log(n/k) + k)$, where $H_m$ is the $m$-th harmonic number.

For $k = 1$ the heap is one variable, and the time is $\Theta(nd)$.

## Properties

- **Exact.** It returns a correct answer for any distance function, metric or not.
- **Online.** It reads each point once, in order, so it works on a stream and on data on disk with one sequential pass.
- **Deterministic and tie-stable.** Ties are broken by the index, so the output is the same on each run.
- **No preprocessing.** Insertions and deletions of points cost nothing, since there is no index to update.

## Variants and improvements

- **Selection instead of a heap.** Store all $n$ distances and use [quickselect](/quickselect/) to find the $k$ smallest in $O(n)$ expected time, then sort them. This is $O(nd + k \log k)$ expected but needs $\Theta(n)$ space. See [top-k selection](/top-k-selection/) and [heap select](/heap-select/).
- **Matrix form.** For $m$ queries at once, use $\|x - q\|^2 = \|x\|^2 - 2\, x \cdot q + \|q\|^2$. The middle terms for all pairs are one matrix product of an $m \times d$ by a $d \times n$ matrix, which runs fast on vector units and GPUs.
- **Early abandoning.** Stop the sum of line L3 as soon as the partial squared distance exceeds the top of a full heap. The answer is the same, and many points cost far fewer than $d$ operations.
- **Pruning by a pivot.** With a metric, store $\delta(p, z)$ for a fixed point $z$. By the [triangle inequality](/triangle-inequality/), $\delta(q, p) \ge |\delta(q, z) - \delta(p, z)|$, so a point whose bound already exceeds the top of a full heap can be skipped. This is the idea of [pivot-based indexing](/pivot-based-indexing/).
- **Compressed vectors.** Scan short codes instead of the full vectors, as [product quantization](/product-quantization/) does, and rerank the best ones with the true distance.

## When to use it

Use the scan when $n$ is small (up to about $10^4$ to $10^5$ points for one query), when the dimension is high and an exact answer is needed, when the data changes often, or to measure the recall of an approximate index. For many queries in low dimension, a [k-d tree](/kd-tree/) or a [ball tree](/ball-tree/) is much faster. For large $n$ in high dimension where some error is allowed, use an [approximate](/approximate-nearest-neighbor-search/) index such as [HNSW](/hnsw/) or an [inverted file index](/inverted-file-index/).

## Pitfalls

- **A heap of all $n$ points.** Pushing every pair into a min-heap and popping $k$ times costs $\Theta(n \log n)$ for the pushes, or $\Theta(n)$ with a heap build, and $\Theta(n)$ space. Line L5 keeps only $k$ items.
- **The wrong kind of heap.** The heap of line L1 must be a max-heap, so that TOP is the worst kept pair. With a min-heap, line L5 compares with the best pair and drops good points.
- **Cancellation in the matrix form.** $\|x\|^2 - 2\, x \cdot q + \|q\|^2$ suffers from rounding when $x$ and $q$ are close and long, and can give a small negative value. Clamp it at 0, and recompute the final $k$ distances directly as in line L3.
- **$k$ larger than $n$.** Line L6 returns $\min(k, n)$ points. Code that assumes exactly $k$ results reads past the end.
- **Unfair ties.** If ties are broken by the order of a hash table or by a parallel race, two runs give different answers, and a recall measure against them is noisy. Compare pairs $(\delta, i)$ as line L5 does.

## Implementations

## References
