---
tag: WEMPA3
kind: problem
slug: k-nearest-neighbor-search
name: k-nearest neighbor search
aliases:
- Nearest-neighbor search
- k-NN query
- k-NN search
- k-nearest-neighbor search
- kNN search
- post office problem
area: searching/similarity-search
level: intro
summary: Find the k stored points closest to a query point.
prereqs: [metric-space, euclidean-distance]
see_also: [nearest-neighbor-search, brute-force-nearest-neighbor-search, fixed-radius-near-neighbors, approximate-nearest-neighbor-search, kd-tree-nearest-neighbor-search, cover-tree, locality-sensitive-hashing, curse-of-dimensionality]
sources:
  - book: isbn:9780123694461
    title: Hanan Samet, Foundations of Multidimensional and Metric Data Structures, Morgan Kaufmann, 2006
    locator: Chapter 4, High-Dimensional Data, Sections 4.1 and 4.2 (best-first and depth-first k-nearest neighbor finding) and Section 4.5 (distance-based indexing)
  - paper: doi:10.1145/502807.502808
    title: Edgar Chávez, Gonzalo Navarro, Ricardo Baeza-Yates and José Luis Marroquín, Searching in metric spaces, ACM Computing Surveys 33(3), 2001
    locator: pages 273 to 321 (Section 2 defines the range query and the k nearest neighbor query in a metric space)
  - book: isbn:9783540779735
    title: Mark de Berg, Otfried Cheong, Marc van Kreveld and Mark Overmars, Computational Geometry, Algorithms and Applications, third edition, Springer, 2008
    locator: Chapter 7, Voronoi Diagrams (the post office problem, and the Voronoi diagram of n sites in the plane with O(n) size, built in O(n log n) time); Chapter 6, Point Location (O(log n) expected query time with O(n) space)
  - paper: doi:10.1016/j.tcs.2005.09.023
    title: Ryan Williams, A new algorithm for optimal 2-constraint satisfaction and its implications, Theoretical Computer Science 348(2-3), 2005
    locator: pages 357 to 365 (a fast algorithm for orthogonal vectors would give a faster algorithm for CNF-SAT, the base of the SETH lower bounds)
  - paper: doi:10.1145/800061.808735
    title: Michael Ben-Or, Lower bounds for algebraic computation trees, Proceedings of the 15th ACM Symposium on Theory of Computing (STOC), 1983
    locator: pages 80 to 86 (the Ω(n log n) bound for element distinctness, from the number of connected components)
  - book: isbn:9780201896855
    title: Donald E. Knuth, The Art of Computer Programming, Volume 3, second edition
    locator: Section 6.5, Retrieval on Secondary Keys (the post-office problem)
---

The k-nearest neighbor search problem asks, for a set $P$ of $n$ points in a [metric space](/metric-space/) and a query point $q$, for the $k$ points of $P$ at the least distance from $q$. A scan of all points solves it in $\Theta(n)$ distance evaluations, and this is optimal without preprocessing. With preprocessing, low dimensions allow logarithmic query time, but in high dimensions no known exact method is much faster than the scan, and under the Strong Exponential Time Hypothesis none can be. This gap, the [curse of dimensionality](/curse-of-dimensionality/), is why most large systems solve the [approximate](/approximate-nearest-neighbor-search/) version instead.

## In plain words

You have a large collection of things, and a way to say how far apart two things are. Someone shows you a new thing and asks for the few things in your collection that are most like it. These are its nearest neighbors.

Examples are the nearest shops to a house, the photos that look most like a given photo, or the songs that sound most like a song you like. The simple method compares the new thing with every thing in the collection. A good index lets you skip most of the collection. This works well when the things are described by a few numbers, and badly when they are described by hundreds of numbers.

## Definition

**Input.** A metric space $(M, \delta)$, a finite set $P \subseteq M$ of $n$ points, a query $q \in M$ and an integer $k \ge 1$. Often $M = \mathbb{R}^d$ and $\delta$ is the [Euclidean distance](/euclidean-distance/) or another $\ell_p$ distance.

**Output.** A set $S \subseteq P$ with $|S| = \min(k, n)$ such that

$$\delta(q, s) \le \delta(q, p) \quad \text{for each } s \in S \text{ and each } p \in P \setminus S.$$

The output is often given as a list sorted by distance. When several points have the same distance as the $k$-th nearest one, more than one set $S$ is correct, and a program must either break ties by a fixed rule (for example by index) or accept any correct set. The $k$-th smallest distance $r_k(q) = \max_{s \in S} \delta(q, s)$ is the same for every correct $S$.

**Two settings.** In the *offline* setting, $P$ and $q$ come together and the cost is the total time. In the *data structure* setting, $P$ is known first and is preprocessed into an index; then queries come one at a time, and the costs are the preprocessing time, the space and the query time. The page [nearest neighbor search](/nearest-neighbor-search/) treats the case $k = 1$.

## Variants

- **Nearest neighbor ($k = 1$).** Knuth called it the post-office problem: find the post office nearest to a house.
- **[Fixed-radius near neighbors](/fixed-radius-near-neighbors/)** (range query): report all points within distance $r$ of $q$. A $k$-NN query with answer $S$ is a range query with $r = r_k(q)$, but $r_k(q)$ is not known in advance.
- **Approximate.** Return points within a factor $c$ of the true distances. See [approximate nearest neighbor search](/approximate-nearest-neighbor-search/) and the [c-approximate nearest neighbor](/c-approximate-nearest-neighbor/) problem.
- **All k nearest neighbors.** Find the $k$ nearest neighbors of every point of $P$ among the others. The output is the [k-nearest neighbor graph](/k-nearest-neighbor-graph/); building it is [k-nearest neighbor graph construction](/k-nearest-neighbor-graph-construction/).
- **Reverse nearest neighbors.** Find the points that have $q$ among their own nearest neighbors. See [reverse nearest neighbor search](/reverse-nearest-neighbor-search/).
- **Similarity instead of distance.** With a similarity such as [cosine similarity](/cosine-similarity/) or the inner product, find the $k$ points of largest similarity. See [maximum inner product search](/maximum-inner-product-search/).
- **Dynamic.** Points are inserted and deleted between queries.

## Examples

Let $P = \{(1,1), (2,4), (4,2), (5,5), (6,1), (7,3), (3,6), (4,4)\}$ in the plane and $q = (4, 3)$. The squared Euclidean distances from $q$ are:

| point | (4,2) | (4,4) | (2,4) | (5,5) | (6,1) | (7,3) | (3,6) | (1,1) |
|---|---|---|---|---|---|---|---|---|
| squared $\ell_2$ distance | 1 | 1 | 5 | 5 | 8 | 9 | 10 | 13 |
| $\ell_1$ distance | 1 | 1 | 3 | 3 | 4 | 3 | 4 | 5 |

- For $k = 1$, both $\{(4,2)\}$ and $\{(4,4)\}$ are correct answers, and $r_1(q) = 1$.
- For $k = 2$, the only answer is $\{(4,2), (4,4)\}$.
- For $k = 3$, the answer is $\{(4,2), (4,4)\}$ with $(2,4)$ or with $(5,5)$, and $r_3(q) = \sqrt 5 \approx 2.2361$.
- For $k = 5$ under $\ell_2$, the answer is $\{(4,2), (4,4), (2,4), (5,5), (6,1)\}$. Under the $\ell_1$ distance, $(7,3)$ at distance 3 is nearer than $(6,1)$ at distance 4, so the answer changes. The metric is part of the problem.

## Known algorithms

- **[Brute-force nearest neighbor search](/brute-force-nearest-neighbor-search/)**: compute each distance and keep the $k$ smallest with a heap, in $O(n d + n \log k)$ time for points in $\mathbb{R}^d$. No preprocessing.
- **One dimension**: sort $P$, then [binary search](/binary-search/) for $q$ and expand left and right, in $O(\log n + k)$ time per query after $O(n \log n)$ preprocessing.
- **[k-d tree](/kd-tree/)** with [branch and bound](/kd-tree-nearest-neighbor-search/): $O(n)$ worst case per query, and logarithmic expected time for fixed $d$ and smooth distributions.
- **Metric trees** that use only the [triangle inequality](/triangle-inequality/): the [ball tree](/ball-tree/), the [vantage-point tree](/vantage-point-tree/), [GNAT](/gnat/), the [M-tree](/m-tree/), and for integer distances the [BK-tree](/bk-tree/). Their worst case is $\Theta(n)$ distance evaluations.
- **[Cover tree](/cover-tree/)**: exact nearest neighbor in $O(c^{12} \log n)$ time, where $c$ is the expansion constant of the data; see [intrinsic dimensionality](/intrinsic-dimensionality/).
- **Voronoi diagram** in the plane, for $k = 1$: $O(n \log n)$ preprocessing, $O(n)$ space and $O(\log n)$ query time with a point location structure.
- **Approximate indexes**: [locality-sensitive hashing](/locality-sensitive-hashing/), the [inverted file index](/inverted-file-index/), [HNSW](/hnsw/) and [DiskANN](/diskann/) answer the approximate variant.

## Bounds

**No preprocessing: $\Omega(n)$.** Let $P \subseteq \mathbb{R}^d$. An algorithm that does not read the coordinates of some point $p \in P$ cannot tell an input where $p$ is very far from $q$ from one where $p = q$ and $p$ is the unique nearest point, so it is wrong on one of them. So each exact algorithm reads all $n$ points on some input, and for $k \ge 1$ this matches the brute force. In a general metric space where the distance is a black box, the same argument counts distance evaluations.

**With preprocessing: $\Omega(\log n)$ per query.** Consider any algorithm that answers a query by a decision tree in which each test has at most three outcomes, such as the comparisons of the [comparison model](/comparison-model/) or the sign tests of the [algebraic decision tree](/algebraic-decision-tree/). For $k = 1$ and distinct points, the query $q = p$ has the unique answer $p$, so the tree has at least $n$ leaves and depth at least $\lceil \log_3 n \rceil$. A $k$-NN query must also write $k$ points, so it needs $\Omega(\log n + k)$ time. In one dimension and in the plane, the methods above meet this bound.

**High dimension and the SETH.** The *orthogonal vectors* problem gives two sets $A, B \subseteq \{0,1\}^d$ of $n$ vectors and asks whether some $a \in A$ and $b \in B$ have $a \cdot b = 0$. Williams showed that, under the [Strong Exponential Time Hypothesis](/strong-exponential-time-hypothesis/), for each $\varepsilon > 0$ there is a constant $c$ such that [orthogonal vectors](/orthogonal-vectors/) with $d = c \log n$ has no $O(n^{2 - \varepsilon})$ time algorithm. It reduces to nearest neighbor search in the [Hamming distance](/hamming-distance/) $H$. Split $A$ by the weight $|a| = w_1$ and $B$ by $|b| = w_2$, and replace each $b$ by its complement $\bar b$. Then $a \cdot \bar b = w_1 - a \cdot b$, so

$$H(a, \bar b) = |a| + |\bar b| - 2\, a \cdot \bar b = d - w_1 - w_2 + 2\, a \cdot b.$$

In the group $(w_1, w_2)$, the least distance from a query $a$ to the complemented set is $d - w_1 - w_2$ if and only if $a$ has an orthogonal partner. There are $(d+1)^2$ groups. So an index that answers $n$ exact nearest neighbor queries on $n$ points of $\{0,1\}^d$, preprocessing included, in total time $O(n^{2-\varepsilon})$ for $d = c \log n$ would solve orthogonal vectors in $O(d^2 n^{2-\varepsilon})$ time and refute the SETH.

## Reductions

- **Cosine to Euclidean.** For unit vectors, $\|\hat x - \hat q\|^2 = 2 - 2\cos(x, q)$, so $k$-NN by [cosine similarity](/cosine-similarity/) is $k$-NN by Euclidean distance after an $O(nd)$ normalization.
- **Closest pair to all nearest neighbors.** The [closest pair of points](/closest-pair-of-points/) is the shortest edge of the nearest neighbor graph, so it takes $n$ queries with $k = 1$ and an $O(n)$ scan.
- **Element distinctness to closest pair.** $n$ real numbers are distinct if and only if their closest pair has a positive distance. [Element distinctness](/element-distinctness/) needs $\Omega(n \log n)$ time in the algebraic decision tree model (Ben-Or), so the offline all-nearest-neighbors problem needs $\Omega(n \log n)$ time in this model, already in one dimension.
- **Inner product to nearest neighbor.** With [asymmetric transformations](/asymmetric-lsh/) of the data and the query, maximum inner product search becomes a nearest neighbor search in one more dimension.

## Applications

- The [k-nearest neighbors](/k-nearest-neighbors/) classifier and regression predict from the labels of the $k$ nearest training points.
- Retrieval of similar documents, images and products from embedding vectors, and retrieval for language models.
- Clustering and embedding methods such as [DBSCAN](/dbscan/), [t-SNE](/t-sne/) and [UMAP](/umap/), which start from the neighbors of each point.
- Spell checking and record linkage with the [edit distance](/edit-distance/) as the metric.
- Geographic queries such as the nearest hospital, with a [spatial index](/spatial-index/).

## References
