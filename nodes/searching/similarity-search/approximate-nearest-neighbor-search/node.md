---
tag: X8XS00
kind: problem
slug: approximate-nearest-neighbor-search
name: Approximate nearest neighbor search
aliases:
- ANN search
- ANNS
area: searching/similarity-search
level: core
summary: Find a point whose distance to the query is within a factor of the true nearest distance, trading exactness for speed.
prereqs: [k-nearest-neighbor-search, c-approximate-nearest-neighbor, curse-of-dimensionality]
see_also: [locality-sensitive-hashing, hnsw, inverted-file-index, product-quantization, diskann, johnson-lindenstrauss-lemma, kd-tree, maximum-inner-product-search]
sources:
  - paper: doi:10.1145/293347.293348
    title: Sunil Arya, David M. Mount, Nathan S. Netanyahu, Ruth Silverman and Angela Y. Wu, An optimal algorithm for approximate nearest neighbor searching in fixed dimensions, Journal of the ACM 45(6), 1998
    locator: pages 891 to 923 (the balanced box-decomposition tree, with O(dn) space, O(dn log n) preprocessing and O(c_{d,ε} log n) query time)
  - paper: doi:10.4086/toc.2012.v008a014
    title: Sariel Har-Peled, Piotr Indyk and Rajeev Motwani, Approximate nearest neighbor, towards removing the curse of dimensionality, Theory of Computing 8, 2012
    locator: Sections 2 and 3 (the reduction from c-approximate nearest neighbor to (c, r)-near neighbor, and locality-sensitive hashing)
  - paper: doi:10.1145/1327452.1327494
    title: Alexandr Andoni and Piotr Indyk, Near-optimal hashing algorithms for approximate nearest neighbor in high dimensions, Communications of the ACM 51(1), 2008
    locator: pages 117 to 122 (the exponent 1/c² + o(1) for the Euclidean distance and the survey of exponents)
  - paper: doi:10.1145/2578221
    title: Ryan O'Donnell, Yi Wu and Yuan Zhou, Optimal lower bounds for locality-sensitive hashing (except when q is tiny), ACM Transactions on Computation Theory 6(1), article 5, 2014
    locator: main theorem (every LSH family for the Hamming distance has ρ ≥ 1/c − o(1), which gives 1/c² − o(1) for the Euclidean distance)
  - paper: doi:10.1109/TBDATA.2019.2921572
    title: Jeff Johnson, Matthijs Douze and Hervé Jégou, Billion-scale similarity search with GPUs, IEEE Transactions on Big Data, 2019
    locator: the inverted file with product quantization, and the recall measure used to compare approximate methods
  - book: isbn:9780123694461
    title: Hanan Samet, Foundations of Multidimensional and Metric Data Structures, Morgan Kaufmann, 2006
    locator: Chapter 4, High-Dimensional Data (approximate nearest neighbor finding with trees, and dimension reduction)
---

Approximate nearest neighbor search (ANN search) asks, for a set $P$ of $n$ points and a query $q$, for a point of $P$ whose distance to $q$ is at most $c$ times the distance of the true nearest neighbor, for a fixed factor $c > 1$. It is the [k-nearest neighbor search](/k-nearest-neighbor-search/) problem with the answer relaxed to a [c-approximate nearest neighbor](/c-approximate-nearest-neighbor/). The relaxation escapes the [curse of dimensionality](/curse-of-dimensionality/): in $\mathbb{R}^d$, [locality-sensitive hashing](/locality-sensitive-hashing/) answers it with $O(d n^{\rho})$ query time for $\rho = 1/c^2 + o(1)$, while exact search in high dimension is believed to need almost $n$ distance evaluations. In practice the problem is often stated with recall, the fraction of the true $k$ nearest neighbors that a method returns.

## In plain words

You have many points and a query point, and you want the point closest to the query. Finding the exact closest point fast is very hard when the points have many coordinates. So you accept an answer that is close enough: a point whose distance to the query is not much larger than the best distance.

This small change makes very fast methods possible. They hash points so that close points meet, or they walk a graph that links each point to points near it, or they split the space into cells and look only in the cells near the query.

## Definition

Let $(M, \delta)$ be a metric space, $P \subseteq M$ a set of $n$ points, and $c \ge 1$ a factor (often written $c = 1 + \varepsilon$). For a query $q \in M$, let $\delta^*(q) = \min_{p \in P} \delta(q, p)$.

- **c-approximate nearest neighbor.** Preprocess $P$ so that for each query $q$ the answer is a point $p \in P$ with $\delta(q, p) \le c \cdot \delta^*(q)$.
- **Randomized version.** The preprocessing may use random bits, and for each fixed $q$ the answer must be correct with probability at least a fixed constant, usually $1/2$ or $2/3$, over those bits.
- **k-approximate version.** Return $k$ points $p_1, \dots, p_k$ with $\delta(q, p_i) \le c \cdot \delta_i^*(q)$, where $\delta_i^*(q)$ is the $i$-th smallest distance from $q$ to $P$.
- **Recall version.** Return a list $A$ of $k$ points. The recall is $|A \cap N_k(q)|/k$, where $N_k(q)$ is the set of the $k$ true nearest neighbors (ties broken by index). A method is measured by its average recall and its query time on a test set of queries; no factor is promised.

The cost of a solution has three parts: the preprocessing time, the space, and the query time. All bounds below are in the [real RAM](/real-ram/) with $O(1)$-time distance evaluation per coordinate.

## Variants

- **(c, r)-near neighbor.** A decision form with a fixed radius $r$: if some point is within $r$, return a point within $cr$. It is defined on the [c-approximate nearest neighbor](/c-approximate-nearest-neighbor/) page, and it is the form that [LSH](/locality-sensitive-hashing/) solves.
- **Fixed dimension against high dimension.** When $d$ is a constant, bounds may grow exponentially in $d$; when $d$ is part of the input, the goal is time polynomial in $d$ and sublinear in $n$.
- **Other distances and similarities.** Hamming, Jaccard, angular and inner-product versions, the last of which is [maximum inner product search](/maximum-inner-product-search/).
- **Dynamic.** Points are inserted and deleted between queries.
- **Batch.** All points are queries, as in [k-nearest neighbor graph construction](/k-nearest-neighbor-graph-construction/).
- **Fixed-radius approximate.** Report all points within $r$, and possibly some within $cr$; see [fixed-radius near neighbors](/fixed-radius-near-neighbors/).

## Examples

- **On a line.** Let $P = \{0, 3, 10\}$ and $q = 1$. The nearest neighbor is $0$ at distance 1. With $c = 2$, the valid answers are the points within distance 2, so only $0$; with $c = 3$, the point $3$ at distance 2 is also valid, and $10$ never is.
- **Recall.** Let the true 3 nearest neighbors of $q$ be $\{p_4, p_7, p_9\}$ and a method return $\{p_4, p_9, p_2\}$. The recall at 3 is $2/3$. If $\delta(q, p_2) \le c \cdot \delta(q, p_7)$, the list is still a valid $c$-approximate answer, so recall and the factor $c$ measure different things.
- **A typical use.** A text search system stores $10^8$ document vectors of dimension 768 and asks for the 10 vectors with the largest cosine similarity to the query vector. An index such as [HNSW](/hnsw/) answers in about a millisecond with recall above 0.95, against seconds for a scan.

## Known algorithms

| Method | Setting | Space | Query time | Guarantee |
|---|---|---|---|---|
| [Brute-force scan](/brute-force-nearest-neighbor-search/) | any metric | $O(n)$ | $O(n)$ distances | exact |
| BBD tree (Arya et al.) | $\mathbb{R}^d$, $\ell_p$, fixed $d$ | $O(dn)$ | $O(c_{d,\varepsilon} \log n)$, $c_{d,\varepsilon} \le d \lceil 1 + 6d/\varepsilon \rceil^d$ | $(1+\varepsilon)$, deterministic |
| [Bit-sampling LSH](/bit-sampling-lsh/) | Hamming | $O(n^{1+1/c} + nd)$ | $O(n^{1/c} (d + \log n))$ | $(c, r)$, success $> 0.29$ |
| [E2LSH](/e2lsh/) | $\ell_2$ | $O(n^{1+\rho} + nd)$ | $O(d n^{\rho} \log n)$, $\rho < 1/c$ | $(c, r)$, constant success |
| Andoni-Indyk LSH | $\ell_2$ | $n^{1+\rho + o(1)}$ | $d n^{\rho + o(1)}$, $\rho = 1/c^2$ | $(c, r)$, constant success |
| [Inverted file index](/inverted-file-index/) | $\ell_2$, inner product | $O(nd)$ | tuned by the number of probed cells | recall only |
| [Product quantization](/product-quantization/) | $\ell_2$ | $O(n m)$ bytes | $O(n m)$ table lookups | recall only |
| [HNSW](/hnsw/), [DiskANN](/diskann/) | any metric | $O(nM)$ links | about logarithmic in practice | recall only |

The BBD tree of Arya, Mount, Netanyahu, Silverman and Wu is a deterministic $(1+\varepsilon)$ method for fixed $d$, built in $O(dn \log n)$ time. Its query time is logarithmic in $n$ but exponential in $d$, so it helps only for small $d$, as do the [k-d tree](/kd-tree/) and the [cover tree](/cover-tree/). The LSH rows are polynomial in $d$; their exponent is the main measure of progress.

The last rows are the methods used in practice for $d$ in the hundreds. They have no worst-case factor, and they are compared by recall against queries per second on benchmark data. The Faiss library of Johnson, Douze and Jégou combines an inverted file with product quantization.

## Bounds

- **Dimension reduction.** By the [Johnson-Lindenstrauss lemma](/johnson-lindenstrauss-lemma/), a random linear map to $m = O(\varepsilon^{-2} \log n)$ dimensions keeps all distances among $n + 1$ points within a factor $1 \pm \varepsilon$ with high probability. So a $c$-approximate answer in the small space is a $c (1+\varepsilon)/(1-\varepsilon)$-approximate answer in the original space, for each fixed query with high probability.
- **LSH lower bound.** O'Donnell, Wu and Zhou proved that every LSH family for the Hamming distance has $\rho \ge 1/c - o(1)$, and, through the embedding of $\ell_2$ into Hamming, $\rho \ge 1/c^2 - o(1)$ for $\ell_2$. So bit sampling and the Andoni-Indyk family are optimal among data-independent hash families. This bound is about LSH only; it is not a lower bound for all data structures.
- **Exact search is hard.** For each $\varepsilon > 0$ there is a constant $c'$ such that no index answers $n$ exact nearest neighbor queries on $n$ points of $\{0,1\}^{c' \log n}$ under the Hamming distance in total time $O(n^{2-\varepsilon})$, preprocessing included, unless the [Strong Exponential Time Hypothesis](/strong-exponential-time-hypothesis/) fails (see [k-nearest neighbor search](/k-nearest-neighbor-search/)). The approximate problem with fixed $c > 1$ is not subject to this bound, which is why the relaxation matters.
- **Reading the answer.** Any method must compute at least one distance, so the query time is $\Omega(d)$ for points in $\mathbb{R}^d$.

## Reductions

- **c-ANN to (c, r)-near neighbor.** Build $(c, r_i)$ structures for radii $r_i = a(1+\varepsilon)^i$ and binary-search over $i$; the answer is $c(1+\varepsilon)$-approximate with $O(\log m)$ structure queries, where $m$ is the number of radii. The proof is on the [c-approximate nearest neighbor](/c-approximate-nearest-neighbor/) page. Har-Peled, Indyk and Motwani remove the dependence on the ratio of the largest to the smallest distance with more care.
- **MIPS to nearest neighbor.** After scaling all points to norm at most 1, the map $x \mapsto (x, \sqrt{1 - \|x\|^2})$ and $q \mapsto (q, 0)$ for a unit query turns the largest inner product into the smallest Euclidean distance; see [asymmetric LSH](/asymmetric-lsh/).
- **Cosine to Euclidean.** For unit vectors, $\|x - y\|^2 = 2 - 2\cos(x, y)$, so the largest [cosine similarity](/cosine-similarity/) is the smallest Euclidean distance after normalization.
- **Closest pair.** One approximate query for each of the $n$ points gives an approximate [closest pair of points](/closest-pair-of-points/).

## Applications

- **Retrieval for language models and search.** Text and images are mapped to vectors, and the nearest vectors to the query vector are the retrieved items.
- **Recommendation.** Users and items share a vector space, and the items with the largest inner product with a user vector are suggested.
- **Near-duplicate detection.** Web pages, images and code are found by near neighbors under Jaccard or Hamming distance, as with [MinHash](/minhash/) and [SimHash](/simhash/).
- **Machine learning.** [k-nearest neighbors](/k-nearest-neighbors/) classifiers, the neighbor graphs of [t-SNE](/t-sne/) and [UMAP](/umap/), and clustering such as [DBSCAN](/dbscan/) all need many neighbor queries.

## References
