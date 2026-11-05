---
tag: TAES1Q
kind: concept
slug: intrinsic-dimensionality
name: Intrinsic dimensionality
aliases:
- doubling dimension
- expansion constant
area: searching/similarity-search
level: advanced
summary: The effective dimension of data, which governs the cost of nearest neighbor search even when the ambient dimension is high.
prereqs: [metric-space, curse-of-dimensionality]
see_also: [cover-tree, hubness, k-nearest-neighbor-search, ball-tree, gnat, johnson-lindenstrauss-lemma, metric-space-indexing, umap]
sources:
  - paper: doi:10.1145/509907.510013
    title: David R. Karger and Matthias Ruhl, Finding nearest neighbors in growth-restricted metrics, Proceedings of the 34th ACM Symposium on Theory of Computing (STOC), 2002
    locator: pages 741 to 750 (the expansion constant c with |B(p, 2r)| ≤ c |B(p, r)|, and a nearest neighbor structure whose bounds depend on c)
  - paper: doi:10.1109/SFCS.2003.1238226
    title: Anupam Gupta, Robert Krauthgamer and James R. Lee, Bounded geometries, fractals, and low-distortion embeddings, Proceedings of the 44th IEEE Symposium on Foundations of Computer Science (FOCS), 2003
    locator: pages 534 to 543 (the doubling dimension, and the fact that a bounded expansion constant implies a bounded doubling dimension but not the reverse)
  - paper: doi:10.1145/1143844.1143857
    title: Alina Beygelzimer, Sham Kakade and John Langford, Cover trees for nearest neighbor, Proceedings of the 23rd International Conference on Machine Learning (ICML), 2006
    locator: the bounds of the cover tree in terms of the expansion constant c
  - paper: doi:10.1145/502807.502808
    title: Edgar Chávez, Gonzalo Navarro, Ricardo Baeza-Yates and José Luis Marroquín, Searching in metric spaces, ACM Computing Surveys 33(3), 2001
    locator: pages 273 to 321 (Section 7, the intrinsic dimensionality of a metric space measured from the histogram of distances, ρ = μ²/(2σ²))
---

The intrinsic dimensionality of a data set is a number that measures how many independent directions the data really use, as opposed to the number of coordinates, the ambient dimension. Points on a curve in $\mathbb{R}^{1000}$ have intrinsic dimension about 1, and the cost of exact [nearest neighbor search](/k-nearest-neighbor-search/) with trees depends on this number, not on 1000. Two precise forms are used in the analysis of [metric space](/metric-space/) indexes: the expansion constant of Karger and Ruhl, which bounds how fast the number of points in a ball grows when the radius doubles, and the doubling dimension, which bounds how many half-size balls cover a ball. The [cover tree](/cover-tree/) and other indexes have query bounds of the form $2^{O(\dim)} \log n$, which escape the [curse of dimensionality](/curse-of-dimensionality/) exactly when the intrinsic dimension is small.

## In plain words

A data set can have many numbers per item but still be simple. Photos of one face turning in front of a camera may have a million pixels each, yet only a couple of things change from photo to photo. Such data lie on a thin surface inside the big space.

The intrinsic dimension says how thick the data really are. One way to measure it: double the radius of a ball around a data point and count how many more points fall inside. In a flat sheet, the count grows about four times; along a line, about two times; in a full cloud of $D$ directions, about $2^D$ times. Search methods that use only distances are fast when this growth is slow.

## The idea

Let $S$ be a finite set of points in a metric space $(M, \delta)$, and write $B(p, r) = \{x \in S : \delta(p, x) \le r\}$ for a ball, counted inside $S$.

**Expansion constant (Karger and Ruhl).** The expansion constant of $S$ is the least $c \ge 1$ such that

$$|B(p, 2r)| \le c \cdot |B(p, r)| \quad \text{for all } p \in S \text{ and } r > 0.$$

The KR dimension is $\log_2 c$. In $\mathbb{R}^D$ the volume of a ball grows by $2^D$ when the radius doubles, so a uniformly dense set has $c \approx 2^D$.

**Doubling dimension.** The doubling constant $\lambda$ of $S$ is the least number such that every ball $B(p, 2r)$ can be covered by $\lambda$ balls $B(y, r)$ with centers $y \in S$. The doubling dimension is $\log_2 \lambda$. Euclidean space $\mathbb{R}^D$ has doubling dimension $\Theta(D)$, and every subset has doubling dimension at most that of the whole space, up to a factor of 2 from the restriction of centers to the subset.

**The two compared.** A small expansion constant implies a small doubling dimension: $\lambda \le c^4$, so the doubling dimension is at most $4 \log_2 c$.

*Proof.* Fix $p$ and $r$, and let $N$ be a maximal subset of $B(p, 2r)$ whose points are pairwise more than $r$ apart. By maximality, the balls $B(y, r)$ for $y \in N$ cover $B(p, 2r)$. The balls $B(y, r/2)$ for $y \in N$ are disjoint and lie in $B(p, 5r/2)$. Let $y^* \in N$ minimize $|B(y, r/2)|$. Then $|N| \cdot |B(y^*, r/2)| \le |B(p, 5r/2)| \le |B(y^*, 9r/2)|$, since $\delta(p, y^*) \le 2r$. Doubling the radius four times from $r/2$ reaches $8r \ge 9r/2$, so $|B(y^*, 9r/2)| \le c^4 |B(y^*, r/2)|$. Hence $|N| \le c^4$. $\square$

The converse fails: a small doubling dimension allows a huge expansion constant. On the line, take the point 0 and $n - 1$ points in $[2, 2.001]$. Then $|B(0, 1)| = 1$ and $|B(0, 2)| = n$, so $c \ge n$, while every subset of the line has doubling constant at most 4. The expansion constant is sensitive to sudden jumps in density; the doubling dimension sees only the geometry.

**Other measures.** Chávez, Navarro, Baeza-Yates and Marroquín define the intrinsic dimensionality of a metric space from the histogram of distances as $\mu^2/(2\sigma^2)$, where $\mu$ and $\sigma^2$ are the mean and variance of the distance between two random points; a concentrated histogram, as in high dimension, gives a large value and makes pivot-based pruning useless. Statistical estimators fit the growth rate of the number of neighbors within $r$, as the correlation dimension does, or use the distances to the $k$ nearest neighbors.

## Examples

- **A grid.** The points of $\{1, \dots, m\}^D$ with the $\ell_\infty$ distance have $|B(p, r)| = (2r + 1)^D$ for interior points and integer $r$, so the ratio for doubling is about $2^D$: $c \approx 2^D$, and the KR dimension is about $D$.
- **A curve in high dimension.** Points spaced evenly along a line segment embedded in $\mathbb{R}^{1000}$ have $c \le 4$ for radii above the spacing; the ambient dimension plays no role.
- **The regular simplex.** $n$ points at pairwise distance 1. For $r < 1$, $B(p, r) = \{p\}$, and for $r \ge 1$ it is all of $S$. So $c = n$ and $\lambda = n$: the intrinsic dimension is $\log_2 n$, the largest possible, and no distance-based index can beat a scan, since every point is equally near every query point at distance 1.
- **Random points in high dimension.** For $n$ uniform points in $[0, 1]^D$ with $D$ large, distances concentrate near their mean, the histogram measure is large, and the data behave like the simplex at the scale of interest.

## Where it is used

- **Bounds for metric indexes.** The [cover tree](/cover-tree/) uses $O(n)$ space and answers a nearest neighbor query in $O(c^{12} \log n)$ time, where $c$ is the expansion constant of $S \cup \{q\}$; Karger and Ruhl gave the first structure with bounds in terms of $c$. Bounds in terms of the doubling dimension, of the form $2^{O(\dim)} \log \Delta$ with $\Delta$ the ratio of the largest to the smallest distance, are known for navigating nets.
- **Choosing an index.** Trees such as the [ball tree](/ball-tree/), [GNAT](/gnat/) and the [k-d tree](/kd-tree/) are fast when the intrinsic dimension is low, even if the ambient dimension is high. When it is high, approximate methods such as [HNSW](/hnsw/) or [LSH](/locality-sensitive-hashing/) are the practical choice.
- **Hubness.** High intrinsic dimension, not ambient dimension, drives [hubness](/hubness/), the skew of how often points appear in the neighbor lists of others.
- **Dimension reduction.** The [Johnson-Lindenstrauss lemma](/johnson-lindenstrauss-lemma/) reduces the ambient dimension to $O(\log n/\varepsilon^2)$ for any data; manifold methods such as [UMAP](/umap/) aim at the intrinsic dimension, which may be much smaller.

## References
