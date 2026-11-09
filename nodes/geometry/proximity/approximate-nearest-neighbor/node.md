---
tag: Q7SN39
kind: problem
slug: approximate-nearest-neighbor
name: Approximate nearest neighbor search
aliases:
- ANN search
- (1+eps)-nearest neighbor
- epsilon-approximate nearest neighbor
area: geometry/proximity
level: advanced
summary: Find a point whose distance to the query is within a factor (1+eps) of the true nearest distance.
prereqs: [nearest-neighbor-search, kd-tree, euclidean-distance]
see_also: [approximate-nearest-neighbor-search, c-approximate-nearest-neighbor, kd-tree-nearest-neighbor-search, locality-sensitive-hashing, well-separated-pair-decomposition, curse-of-dimensionality, johnson-lindenstrauss-lemma, hnsw]
sources:
  - paper: doi:10.1145/293347.293348
    title: Sunil Arya, David M. Mount, Nathan S. Netanyahu, Ruth Silverman and Angela Y. Wu, An optimal algorithm for approximate nearest neighbor searching in fixed dimensions, Journal of the ACM 45(6), 1998, 891-923
    locator: the definition of (1 + epsilon)-approximate nearest neighbours, the balanced box-decomposition tree, and the bounds O(dn log n) preprocessing, O(dn) space and O(c log n) query time with c depending on d and epsilon
  - paper: "Piotr Indyk and Rajeev Motwani, Approximate nearest neighbors, towards removing the curse of dimensionality, Proceedings of the 30th Annual ACM Symposium on Theory of Computing, 1998, 604-613"
    locator: locality-sensitive hashing and the reduction from approximate nearest neighbour to approximate near neighbour
  - paper: "Alexandr Andoni and Piotr Indyk, Near-optimal hashing algorithms for approximate nearest neighbor in high dimensions, Communications of the ACM 51(1), 2008, 117-122"
    locator: the survey of locality-sensitive hashing for Euclidean space, with query exponent about 1/c^2
  - book: isbn:9780821849118
    title: Sariel Har-Peled, Geometric Approximation Algorithms, American Mathematical Society, 2011
    locator: the chapters on approximate nearest neighbour search in low dimension (quadtrees, approximate Voronoi diagrams) and high dimension (locality-sensitive hashing, dimension reduction)
---

Approximate nearest neighbor search preprocesses a set $P$ of $n$ points so that, for a query point $q$ and a fixed $\varepsilon > 0$, it returns a point $p \in P$ with
$$\|q - p\| \le (1 + \varepsilon) \, \|q - p^*\|,$$
where $p^*$ is a true nearest neighbour of $q$. Exact [nearest neighbor search](/nearest-neighbor-search/) is easy in the plane but suffers from the [curse of dimensionality](/curse-of-dimensionality/): in dimension $d$ the known exact structures need either space exponential in $d$ or query time close to $n$. Allowing the factor $1 + \varepsilon$ changes this. Arya, Mount, Netanyahu, Silverman and Wu (1998) answered queries in $O(c_{d,\varepsilon} \log n)$ time with a linear-size tree in fixed dimension, and Indyk and Motwani (1998) introduced [locality-sensitive hashing](/locality-sensitive-hashing/), with query time sublinear in $n$ and polynomial in $d$. This page states the problem and its geometric bounds; [approximate nearest neighbor search](/approximate-nearest-neighbor-search/) covers the high-dimensional practice.

## In plain words

You have a huge collection of points, such as songs described by many numbers, and want the one most similar to a new song. Finding the exact best match can mean looking at almost everything.

If you accept an answer that is nearly as close as the best one, for example at most 10 percent farther, the search can stop early. Regions of the collection that cannot contain anything much better are skipped, and the hunt ends as soon as the current candidate is good enough.

The trade is explicit: you choose the tolerance, and a smaller tolerance costs more time.

## Definition

**Input.** A set $P$ of $n$ points in $\mathbb{R}^d$ and a parameter $\varepsilon \ge 0$, given in advance. Then a sequence of query points $q$.

**Output.** For each query, a point $p \in P$ with $\|q - p\| \le (1 + \varepsilon) \min_{x \in P} \|q - x\|$. For $\varepsilon = 0$ this is exact nearest neighbour search. Any point that satisfies the inequality is correct, so the answer need not be unique.

**Cost model.** The usual measures are preprocessing time, space, and query time, as functions of $n$, $d$ and $\varepsilon$. In fixed dimension the analysis is on the [real RAM](/real-ram/), sometimes with the floor function for quadtree-style cells. For high dimension, $d$ is part of the input and polynomial dependence on $d$ is required; randomized structures there answer correctly with high probability.

**Exact check.** With rational $\varepsilon$ and integer coordinates, whether an answer is valid is decided without roots: compare $\|q - p\|^2$ with $(1 + \varepsilon)^2 \|q - p^*\|^2$ in exact arithmetic.

## Variants

- **Approximate near neighbour.** The decision version with a radius $r$ and a factor $c > 1$: if some point is within distance $r$ of $q$, return a point within distance $cr$; see [c-approximate nearest neighbor](/c-approximate-nearest-neighbor/). Indyk and Motwani reduce the optimization version to it with a logarithmic overhead.
- **k approximate nearest neighbours.** Return $k$ points, the $i$-th within a factor $1 + \varepsilon$ of the true $i$-th nearest distance.
- **Other distances.** Hamming, $L_1$, angular distance, and [maximum inner product search](/maximum-inner-product-search/), each with its own hashing schemes.
- **Batch version.** All queries at once, such as approximate [all nearest neighbors](/all-nearest-neighbors/), which the [well-separated pair decomposition](/well-separated-pair-decomposition/) handles.
- **Approximate Voronoi diagrams.** Trade space for time in fixed dimension: a subdivision into $O(n / \varepsilon^d)$ cells, up to logarithmic factors, each with a stored answer, gives $O(\log (n/\varepsilon))$ query time.

## Examples

For $P = \{(1,3), (1,11), (2,8), (5,1), (9,6), (11,1), (11,4)\}$ and $q = (7, 4)$, the squared distances are

| point | $(9,6)$ | $(5,1)$ | $(11,4)$ | $(11,1)$ | $(1,3)$ | $(2,8)$ | $(1,11)$ |
| --- | --- | --- | --- | --- | --- | --- | --- |
| $\|q - p\|^2$ | 8 | 13 | 16 | 25 | 37 | 41 | 85 |

The nearest neighbour is $(9,6)$ at squared distance 8. A point is a valid answer for $\varepsilon$ when its squared distance is at most $(1 + \varepsilon)^2 \cdot 8$:

| $\varepsilon$ | bound on $\|q - p\|^2$ | valid answers |
| --- | --- | --- |
| $1/4$ | $12.5$ | $(9,6)$ only |
| $1/2$ | $18$ | $(9,6)$, $(5,1)$, $(11,4)$ |
| $1$ | $32$ | also $(11,1)$ |

**How a tree uses the slack.** A [k-d tree search](/kd-tree-nearest-neighbor-search/) normally visits a cell when the cell's distance to $q$ is less than the best distance $r$ found so far. The approximate search visits it only when that distance is less than $r / (1 + \varepsilon)$. A skipped cell could only hold points at distance at least $r / (1 + \varepsilon)$, so the final answer is within the factor $1 + \varepsilon$, and far fewer cells are opened.

## Known algorithms

| method | preprocessing and space | query time | setting |
| --- | --- | --- | --- |
| linear scan | none | $O(dn)$ | exact, any $d$ |
| k-d tree with the $1 + \varepsilon$ pruning rule | $O(dn \log n)$, $O(dn)$ | no worst-case bound | practical in low $d$ |
| balanced box-decomposition tree (Arya et al., 1998) | $O(dn \log n)$, $O(dn)$ | $O(c_{d,\varepsilon} \log n)$, $c_{d,\varepsilon} = O(d (1 + 6d/\varepsilon)^d)$ | fixed $d$ |
| approximate Voronoi diagrams (Har-Peled; Arya, Malamatos and Mount) | about $n/\varepsilon^d$ cells | $O(\log (n/\varepsilon))$ | fixed $d$, space for speed |
| [locality-sensitive hashing](/locality-sensitive-hashing/) (Indyk and Motwani, 1998) | $O(n^{1 + \rho} + dn)$ | $O(d n^{\rho})$ | high $d$; $\rho = 1/c$ for Hamming, about $1/c^2$ for Euclidean (Andoni and Indyk) |
| [dimension reduction](/johnson-lindenstrauss-lemma/), then a low-dimensional method | random projection to $O(\log n / \varepsilon^2)$ dimensions | depends on the method | preserves all distances up to $1 \pm \varepsilon$ |
| graph-based search such as [HNSW](/hnsw/) | heuristic | no worst-case bound | the standard in practice for vector search |

Here $c = 1 + \varepsilon$ is the approximation factor.

## Bounds

- **Fixed dimension.** Arya et al. showed that the balanced box-decomposition tree is optimal in $n$: linear space and logarithmic query time, with a constant exponential in $d$ and polynomial in $1/\varepsilon$.
- **High dimension.** Locality-sensitive hashing gives query time $n^{\rho}$ with $\rho < 1$ and space polynomial in $n$, which no exact method achieves. For Euclidean space, $\rho$ about $1/c^2$ is the best possible for locality-sensitive hashing that does not depend on the data; data-dependent hashing (Andoni and Razenshteyn, 2015) improves it to about $1/(2c^2 - 1)$.
- **Exact search is believed hard in high dimension.** Exact [bichromatic closest pair](/bichromatic-closest-pair/) for 0/1 vectors of dimension growing faster than $\log n$ has no truly subquadratic algorithm under the [orthogonal vectors hypothesis](/orthogonal-vectors-hypothesis/). So no exact structure with preprocessing time $n^{2 - \delta}$ can answer queries in $n^{1 - \delta}$ time there, since building it on the blue points and querying with the $n$ red points would solve that problem.
- **Lower bounds in the cell-probe model.** Data-structure lower bounds for near neighbour search in high dimension are proved in the [cell-probe model](/cell-probe-model/), with tradeoffs between space and the number of probes.

## Reductions

- **Approximate nearest to approximate near neighbour.** Search over a range of radii with structures for the decision version; Indyk and Motwani, and later Har-Peled, Indyk and Motwani, do this with logarithmic overhead.
- **High to low dimension.** The [Johnson-Lindenstrauss lemma](/johnson-lindenstrauss-lemma/) maps $n$ points to $O(\log n / \varepsilon^2)$ dimensions while keeping all pairwise distances within $1 \pm \varepsilon$; the image of the query needs the same map.
- **Exact from approximate.** If all distances from $q$ differ by more than the factor $1 + \varepsilon$ from the minimum, the approximate answer is exact; in general it is not, and a final exact check of a few candidates is common in practice.
- **Batch problems reduce to it.** Approximate all nearest neighbours, approximate [bichromatic closest pair](/bichromatic-closest-pair/) and approximate [Euclidean minimum spanning trees](/euclidean-minimum-spanning-tree/) are solved with approximate queries.

## Applications

- **Similarity search.** Image, audio and text retrieval and recommendation map objects to vectors and look for close vectors; see [approximate nearest neighbor search](/approximate-nearest-neighbor-search/) and [product quantization](/product-quantization/).
- **Classification.** Nearest neighbour classifiers tolerate approximate neighbours with little loss of accuracy.
- **Geometric algorithms.** Approximate queries are a subroutine for approximate clustering, approximate minimum spanning trees and approximate diameter in fixed dimension.
- **Pattern recognition and databases.** Feature matching in computer vision and multimedia databases, where exact answers are not worth the cost.

## References
