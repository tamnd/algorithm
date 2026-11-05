---
tag: B1PB10
kind: data-structure
slug: inverted-file-index
name: Inverted file index
aliases:
- IVF index
- inverted file
area: searching/similarity-search
level: core
summary: Partitions vectors into k-means cells and searches only the cells nearest the query.
implements: [similarity-index]
model: real-ram
complexity:
  vars: {n: the number of vectors, d: the dimension, m: the number of cells, t: the number of Lloyd rounds, s: the number of vectors in the probed lists, k: the number of neighbors asked for}
  time: {build: O(t n m d), insert: O(m d), search: O(m d + s d + s log k)}
  space: {total: O(n d + m d)}
history:
  year: 2003
  people: [Josef Sivic, Andrew Zisserman, Hervé Jégou, Matthijs Douze, Cordelia Schmid]
  note: Sivic and Zisserman indexed image descriptors by k-means cells with an inverted file in 2003; Jégou, Douze and Schmid made the inverted file with a coarse quantizer the standard index for approximate vector search in 2011.
prereqs: [k-means, approximate-nearest-neighbor-search]
see_also: [product-quantization, lloyds-algorithm, vector-quantization, inverted-index, voronoi-diagram, hnsw, brute-force-nearest-neighbor-search, k-nearest-neighbor-search]
sources:
  - paper: doi:10.1109/TPAMI.2010.57
    title: Hervé Jégou, Matthijs Douze and Cordelia Schmid, Product quantization for nearest neighbor search, IEEE Transactions on Pattern Analysis and Machine Intelligence 33(1), 2011
    locator: pages 117 to 128 (the inverted file with a coarse k-means quantizer, the probe of the w nearest cells, and the IVFADC index)
  - paper: doi:10.1109/ICCV.2003.1238663
    title: Josef Sivic and Andrew Zisserman, Video Google, a text retrieval approach to object matching in videos, Proceedings of the 9th IEEE International Conference on Computer Vision (ICCV), 2003
    locator: the visual vocabulary built by k-means on descriptors and the inverted file over visual words
  - paper: doi:10.1109/TBDATA.2019.2921572
    title: Jeff Johnson, Matthijs Douze and Hervé Jégou, Billion-scale similarity search with GPUs, IEEE Transactions on Big Data, 2019
    locator: the IVF index of the Faiss library, its nprobe parameter, and its use with product quantization
  - book: isbn:9780521865715
    title: Christopher D. Manning, Prabhakar Raghavan and Hinrich Schütze, Introduction to Information Retrieval, Cambridge University Press, 2008
    locator: Chapter 1 (the inverted index of text retrieval) and Chapter 16 (k-means)
---

An inverted file index (IVF) for vectors splits the space into $m$ cells with [k-means](/k-means/), one cell per centroid, and keeps for each cell the list of vectors whose nearest centroid it is. A query computes its distance to the $m$ centroids, picks the $n_{\text{probe}}$ nearest cells, and scans only their lists. With $n_{\text{probe}} = m$ the search is exact; with a small $n_{\text{probe}}$ it scans about $n_{\text{probe}} \cdot n/m$ vectors, at the risk of missing a neighbor that lies just across a cell border. It is the name of the [inverted index](/inverted-index/) of text retrieval applied to cells in place of words, and, combined with [product quantization](/product-quantization/), it is the main index of the Faiss library for [approximate nearest neighbor search](/approximate-nearest-neighbor-search/).

## In plain words

Group the stored points into a few hundred or thousand clusters, and remember the center of each cluster. For every cluster, keep a list of its points.

To answer a query, first find the cluster centers closest to the query. Then look only at the points in those few clusters, and keep the best ones. Looking at more clusters gives better answers but takes more time. Looking at all clusters gives the exact answer.

## The abstract type

An inverted file index implements a [similarity index](/similarity-index/) over vectors in $\mathbb{R}^d$ with the Euclidean distance: `build(P, m)`, `insert(x)`, `delete(x)`, and `search(q, k, nprobe)`, which returns $k$ stored vectors, nearest first, among those in the $n_{\text{probe}}$ cells whose centroids are nearest to $q$. For inner product or cosine similarity, the same structure works with that score in place of the distance.

## Representation

The index holds a list $C = (c_1, \dots, c_m)$ of centroids in $\mathbb{R}^d$, the stored vectors, and an inverted list $I_j$ of vector ids for each $j$.

**Invariant (V).** Each stored vector $x$ is in exactly one list $I_j$, where $c_j$ is a nearest centroid to $x$, with ties broken to the smallest index.

So $I_j$ holds the vectors of the [Voronoi](/voronoi-diagram/) cell of $c_j$. The centroids come from [Lloyd's algorithm](/lloyds-algorithm/) on $P$ or on a sample of it; (V) holds for any centroids, so the quality of the clustering affects only the speed and the recall, not the correctness of an exhaustive search.

## Operations

```pseudo id=main
IVF-BUILD(P, m)
L1  C ← m centroids from Lloyd's algorithm on P (or on a sample of P)
L2  for each x ∈ P do append x to I_j, where c_j is the nearest centroid to x

IVF-SEARCH(q, k, nprobe)
L3  J ← the nprobe indices j with the smallest ‖q − c_j‖
L4  H ← an empty max-heap that keeps the k pairs (‖q − x‖, x) of least distance
L5  for each j ∈ J and each x ∈ I_j do offer (‖q − x‖, x) to H
L6  return the pairs of H, nearest first
```

Line L1 is the training step; in practice it runs on a sample of a few times $m$ vectors per cell, with up to 20 or so rounds. Line L2 makes (V) true. Line L3 selects cells by their centroid, and lines L4 and L5 keep the $k$ best with a [binary heap](/binary-heap/), as in [top-k selection](/top-k-selection/). **Insert** appends $x$ to the list of its nearest centroid, in $O(md)$ time. **Delete** removes $x$ from its list. Neither changes the centroids, so after many updates the cells drift from the data, and the centroids are retrained.

**Exact search with a stopping rule.** Let $c_a$ be the nearest centroid to $q$. A vector $x$ of cell $j \ne a$ is at least as close to $c_j$ as to $c_a$, so it lies on the far side of the bisector of $c_a$ and $c_j$, and

$$\|q - x\| \ge \beta_j = \max\Big(0, \frac{\|q - c_j\|^2 - \|q - c_a\|^2}{2\|c_j - c_a\|}\Big).$$

```pseudo id=exact
IVF-SEARCH-EXACT(q, k)
L7  sort the cells by β_j, with β_a = 0 first
L8  for each cell j in this order: if H holds k pairs and β_j > the largest distance in H then stop
L9      offer (‖q − x‖, x) to H for each x ∈ I_j
L10 return the pairs of H, nearest first
```

This returns the exact $k$ nearest neighbors, and it often stops after a few cells in low dimension. In high dimension the bounds $\beta_j$ are small for most cells, and the rule scans almost everything.

## Example

Take the seven points $(0,1), (2,2), (1,0), (3,2), (5,5), (7,4), (6,6)$ in the plane with $m = 2$ and the centroids $c_1 = (1, 1)$ and $c_2 = (6, 5)$. By (V), $I_1 = \{(0,1), (2,2), (1,0), (3,2)\}$ and $I_2 = \{(5,5), (7,4), (6,6)\}$; for example $(3,2)$ is at squared distance 5 from $c_1$ and 18 from $c_2$.

Query $q = (4, 3)$ with $k = 1$. The squared distances to the centroids are 13 for $c_1$ and 8 for $c_2$.

| $n_{\text{probe}}$ | cells scanned | squared distances computed | answer |
|---|---|---|---|
| 1 | $I_2$ | 5, 10, 13 | $(5,5)$ at $\sqrt 5 \approx 2.24$ |
| 2 | $I_2, I_1$ | 5, 10, 13, 20, 5, 18, 2 | $(3,2)$ at $\sqrt 2 \approx 1.41$ |

With one probe the index misses the true neighbor $(3,2)$, which lies in the other cell, close to the border. The exact search computes $\beta_1 = (13 - 8)/(2\sqrt{41}) \approx 0.39$. After scanning $I_2$ the best distance is $2.24 > 0.39$, so it must scan $I_1$ and finds $(3,2)$.

## Correctness

**Exhaustive search is exact.** With $n_{\text{probe}} = m$, lines L3 to L5 offer every stored vector to $H$, by (V), and $H$ keeps the $k$ of least distance. So the answer is the exact $k$ nearest neighbors.

**Partial search returns true distances.** Every pair in the answer is a stored vector with its exact distance, and the answer is the $k$ best among the probed cells. Probing more cells offers a superset, so the $k$-th distance of the answer does not increase as $n_{\text{probe}}$ grows. There is no factor $c$: a missed neighbor can be arbitrarily closer than the returned one.

**The stopping rule is safe.** If line L8 stops at cell $j$, every later cell $j'$ has $\beta_{j'} \ge \beta_j$, which is above the current $k$-th distance, and every vector of cell $j'$ is at distance at least $\beta_{j'}$. So none of them would enter $H$. The proof of the bisector bound and of these claims is in `proofs/correctness.md`.

## Complexity

The model is the [real RAM](/real-ram/) with vectors of $d$ coordinates; one distance costs $O(d)$.

- **Build.** Each Lloyd round assigns $n$ vectors to $m$ centroids: $O(nmd)$, so $O(tnmd)$ for $t$ rounds, plus $O(nmd)$ for line L2. Training on a sample of size $n'$ costs $O(tn'md)$.
- **Search.** $O(md)$ for the centroid distances, $O(m \log m)$ or $O(m)$ to select the $n_{\text{probe}}$ nearest, and $O(sd + s \log k)$ for the $s$ vectors of the probed lists. If the cells are balanced, $s \approx n_{\text{probe}} \cdot n/m$, and the choice $m \approx \sqrt n$ balances the two terms at $O(\sqrt n \, d)$ for a constant $n_{\text{probe}}$. In the worst case all vectors are in one probed cell, and $s = n$.
- **Space.** $O(nd)$ for the vectors and $O(md)$ for the centroids; the lists add one id per vector.

| operation | time | case |
|---|---|---|
| build | $O(tnmd)$ | $t$ Lloyd rounds |
| insert | $O(md)$ | worst |
| search | $O(md + sd + s \log k)$ | $s$ vectors in the probed lists, $s \le n$ |
| search, exhaustive | $O(nd + md)$ | exact |
| space | $O(nd + md)$ | total |

## Variants

- **IVF with product quantization (IVFADC).** Jégou, Douze and Schmid store each vector as a short [product quantization](/product-quantization/) code of its residual $x - c_j$, so the lists fit in memory for billions of vectors, and distances are estimated from lookup tables.
- **IVF with flat lists.** The lists hold the full vectors, as above; the answer distances are exact.
- **Graph-based coarse search.** For large $m$, line L3 is itself an approximate search, often with an [HNSW](/hnsw/) index over the centroids.
- **Multi-assignment.** Storing border vectors in two cells raises recall at the cost of space.
- **Inner products.** For [maximum inner product search](/maximum-inner-product-search/), cells are chosen by the largest $q \cdot c_j$, which is not the same as the Euclidean rule unless the vectors are normalized.

## When to use it

Use an IVF index for large sets of dense vectors when memory is tight, when you want a simple tuning knob ($n_{\text{probe}}$), or with product quantization for very large sets. Build is cheap compared to graph indexes, and lists are easy to split across machines. For the best recall at a given speed in memory, graph indexes such as [HNSW](/hnsw/) usually do better. For small sets, a [brute-force scan](/brute-force-nearest-neighbor-search/) is simpler and exact.

## Pitfalls

- **Too few training vectors.** Lloyd's algorithm on fewer than a few dozen vectors per cell gives poor and unbalanced cells.
- **Unbalanced lists.** One huge cell makes every query that probes it slow; the time bound depends on $s$, not on $n/m$.
- **Stale centroids.** Inserts after training land in cells fit to old data; retrain when the data distribution shifts.
- **Mixing metrics.** Training with Euclidean k-means but searching by inner product on vectors of different norms gives cells that do not match the search.
- **Reading recall as a factor.** A recall of 0.9 says nothing about how far the missed neighbors are; measure both if the use needs it.

## Implementations

## History

The inverted file comes from text retrieval, where each word has a list of the documents that contain it. Sivic and Zisserman built a vocabulary of visual words with k-means on image descriptors in 2003 and used an inverted file over those words to search video frames. Jégou, Douze and Schmid in 2011 combined a coarse k-means quantizer with an inverted file and product quantization codes for the residuals, and Johnson, Douze and Jégou made it the base of the Faiss library on GPUs.

## References
