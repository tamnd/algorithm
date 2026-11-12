---
tag: 8RTBTG
kind: algorithm
slug: kernel-k-means
name: Kernel k-means
aliases:
- kernelized k-means
- weighted kernel k-means
area: machine-learning/clustering
level: advanced
summary: "K-means carried out in the feature space of a kernel, using only the kernel matrix; its weighted form is equivalent to normalized cut."
solves: [k-means-problem]
model: real-ram
complexity:
  vars: {n: the number of points, k: the number of clusters, t: the number of iterations}
  time: {worst: "O(n^2 t)"}
  space: {extra: "O(n^2)"}
properties: {deterministic: true, exact: false, online: false, recursive: false}
history:
  year: 1998
  people: [Bernhard Schölkopf, Alexander Smola, Klaus-Robert Müller, Mark Girolami, Inderjit S. Dhillon, Yuqiang Guan, Brian Kulis]
  note: Schölkopf, Smola and Müller noted that k-means can use a kernel (1998); Girolami (2002) studied it as a clustering method; Dhillon, Guan and Kulis (2004) linked its weighted form to graph cuts.
prereqs: [k-means, kernel-trick]
see_also: [kernel-trick, spectral-clustering, normalized-cut, k-means, mercer-theorem, kernel-pca, laplacian-matrix, eigengap-heuristic]
sources:
  - paper: doi:10.1145/1014052.1014118
    title: Inderjit S. Dhillon, Yuqiang Guan and Brian Kulis, Kernel k-means, spectral clustering and normalized cuts, Proceedings of the 10th ACM SIGKDD International Conference on Knowledge Discovery and Data Mining, 2004, pages 551 to 556
    locator: Section 2 (weighted kernel k-means, Algorithm 1), Section 3 (the trace form and the spectral relaxation), Section 4 (the equivalence with normalized cut and the choice of the diagonal shift)
  - paper: "Mark Girolami, Mercer kernel-based clustering in feature space, IEEE Transactions on Neural Networks 13(3), 2002, pages 780 to 784"
    locator: the distance to a cluster mean in feature space written with the kernel matrix
  - paper: "Bernhard Schölkopf, Alexander Smola and Klaus-Robert Müller, Nonlinear component analysis as a kernel eigenvalue problem, Neural Computation 10(5), 1998, pages 1299 to 1319"
    locator: the remark that k-means can be done in feature space with kernels
  - book: isbn:9780521813976
    title: John Shawe-Taylor and Nello Cristianini, Kernel Methods for Pattern Analysis, Cambridge University Press, 2004
    locator: Chapter 8 (clustering in feature space, the kernel form of the k-means objective)
---

Kernel k-means runs [Lloyd's k-means algorithm](/k-means/) in the feature space of a kernel $\kappa(x, y) = \langle \varphi(x), \varphi(y) \rangle$, without computing the feature map $\varphi$. The squared distance from $\varphi(x_i)$ to the mean of a cluster needs only the entries of the kernel matrix $K_{ij} = \kappa(x_i, x_j)$, by the [kernel trick](/kernel-trick/). So the method can find clusters that are not separated by hyperplanes in the input space, such as a ring around a disk. With weights on the points, its objective equals the [normalized cut](/normalized-cut/) of a graph plus a constant, for a suitable kernel, which links it to [spectral clustering](/spectral-clustering/) (Dhillon, Guan and Kulis, 2004). Like plain k-means it is a heuristic that stops at a local optimum.

## In plain words

Plain k-means can only draw straight borders between groups. Some groups are not like that: for example, an inner disk of points with a ring of points around it. A kernel is a way to measure how similar two points are, and each kernel acts as if the points lived in a new space with many more features. In that space, the ring and the disk can be far apart.

Kernel k-means does the usual k-means steps in the new space. It never builds the new features. It only needs the similarity of each pair of points, stored in a table. From the table it can find how far a point is from the average of a group in the new space, and it moves each point to the nearest group. When the table is a valid kernel, each step lowers the total squared distance, so the method stops.

## The problem

The input is a set of $n$ objects $x_1, \ldots, x_n$ (points in $\mathbb{R}^d$ or any other objects), a kernel $\kappa$ with kernel matrix $K$, positive weights $w_1, \ldots, w_n$ (all 1 for the plain method), the number of clusters $k$, and initial labels. The kernel is positive semidefinite, so by [Mercer's theorem](/mercer-theorem/) there is a feature map $\varphi$ into a Hilbert space with $K_{ij} = \langle \varphi(x_i), \varphi(x_j) \rangle$. The goal is a partition $P_1, \ldots, P_k$ with a small weighted k-means cost in feature space,
$$J = \sum_{c=1}^{k} \sum_{i \in P_c} w_i \|\varphi(x_i) - m_c\|^2, \qquad m_c = \frac{\sum_{j \in P_c} w_j \varphi(x_j)}{\sum_{j \in P_c} w_j} .$$
This is the [k-means problem](/k-means-problem/) in feature space; the method gives a local optimum, not the minimum.

## The algorithm

Expand the square. With $W_c = \sum_{j \in P_c} w_j$,
$$\|\varphi(x_i) - m_c\|^2 = K_{ii} - \frac{2}{W_c}\sum_{j \in P_c} w_j K_{ij} + \frac{1}{W_c^2}\sum_{j, l \in P_c} w_j w_l K_{jl} .$$
Every term is an entry of $K$.

```pseudo id=main
KERNEL-KMEANS(K, w, k, a_1..a_n)
L1  repeat
L2      for each non-empty cluster c: S_c ← Σ_{j,l ∈ P_c} w_j w_l K_jl / W_c²
L3      for i ← 1 to n do
L4          for each non-empty c: D(i, c) ← K_ii − (2 / W_c) Σ_{j ∈ P_c} w_j K_ij + S_c
L5          b_i ← a cluster c that minimizes D(i, c), with b_i = a_i if a_i is one of them
L6      if b = a then return a
L7      a ← b
```

Line L2 computes the term that does not depend on the point. Line L4 is the distance to the weighted mean in feature space. Line L5 uses the same tie rule as plain k-means, so a point at equal distance keeps its cluster. The means $m_c$ are never formed; they are only implicit in the labels.

## Example

Take the seven numbers $-4, -3, -1, 0, 1, 3, 4$ and $k = 2$. The natural groups are the inner points $\{-1, 0, 1\}$ and the outer points $\{-4, -3, 3, 4\}$, and no single cut point on the line separates them. Use the kernel $\kappa(x, y) = (xy)^2$, whose feature map is $\varphi(x) = x^2$.

Start from the split left and right, $\{-4, -3, -1\}$ and $\{0, 1, 3, 4\}$, which is a fixed point of plain k-means. In feature space the values are $\{16, 9, 1\}$ with mean $26/3$, and $\{0, 1, 9, 16\}$ with mean $13/2$.

| point | $\varphi(x)$ | distance² to $26/3$ | distance² to $13/2$ | new cluster |
|---|---|---|---|---|
| −4 | 16 | 484/9 | 361/4 | 1 |
| −3 | 9 | 1/9 | 25/4 | 1 |
| −1 | 1 | 529/9 | 121/4 | 2 |
| 0 | 0 | 676/9 | 169/4 | 2 |
| 1 | 1 | 529/9 | 121/4 | 2 |
| 3 | 9 | 1/9 | 25/4 | 1 |
| 4 | 16 | 484/9 | 361/4 | 1 |

The new clusters are the outer points, with feature mean $25/2$, and the inner points, with feature mean $2/3$. The next pass changes nothing. The cost is $4 \cdot (7/2)^2 + 2/3 = 49 + 2/3$, and it is the best split in feature space. The method used only the numbers $K_{ij} = (x_i x_j)^2$.

## Correctness

When $K$ is positive semidefinite, kernel k-means is Lloyd's algorithm on the vectors $\varphi(x_i)$, with weights. So:

- **Each pass lowers $J$.** Line L5 moves each point to a nearest weighted mean, which does not raise $J$ for the old means. Recomputing the means for the new labels does not raise $J$, because the weighted mean minimizes $\sum_{i \in P} w_i \|\varphi(x_i) - z\|^2$ over $z$. A change of a label lowers $J$ strictly, by the tie rule.
- **Termination.** $J$ is a function of the labels, there are finitely many labelings, and $J$ falls strictly in each pass that changes a label. So the loop stops.
- **Fixed point.** At the end each point is at a nearest weighted mean in feature space.

The proofs are in the proofs section below. If $K$ is not positive semidefinite, no feature map exists, the "distances" can be negative, and the method can cycle; Dhillon, Guan and Kulis add $\sigma$ times the inverse weight matrix to $K$ to make it positive semidefinite, which changes $J$ only by a constant.

## Complexity

**Time.** Building $K$ costs $n^2$ kernel evaluations, for example $O(n^2 d)$ for points in $\mathbb{R}^d$. In one pass, line L2 costs $O(n^2)$ in total over the clusters, and lines L3 and L4 cost $O(n^2)$, because each row of $K$ is summed once by cluster. A pass costs $O(n^2)$, against $O(nkd)$ for plain k-means. The number of passes $t$ is as for Lloyd's algorithm.

**Space.** The kernel matrix takes $O(n^2)$ memory, which limits the method to tens of thousands of points. Low rank approximations of $K$ (for example the Nyström method) or sampling reduce both costs.

## Properties

- **Nonlinear borders.** The clusters are separated by hyperplanes in feature space, which can be curved surfaces in the input space.
- **Any data type.** The objects need not be vectors; strings, graphs and sets work with a suitable kernel.
- **Deterministic.** For fixed initial labels the result is fixed. The initial labels can come from random seeds or from [k-means++](/k-means-plus-plus/) in feature space.
- **Means are implicit.** There are no centers to report in the input space; a new point is assigned by the same kernel sums.
- **Equivalent to graph cuts.** With degrees as weights and $K = \sigma D^{-1} + D^{-1} A D^{-1}$ for a graph with adjacency matrix $A$ and degree matrix $D$, the objective is $J = \text{const} + \mathrm{NCut}$; see below.

## Variants and improvements

- **Weighted kernel k-means and graph cuts.** Dhillon, Guan and Kulis show that for a graph with adjacency $A$ and degrees $d_i$, the weights $w_i = d_i$ and the kernel $K = \sigma D^{-1} + D^{-1}AD^{-1}$ give
$$J = n\sigma + \sum_i \frac{A_{ii}}{d_i} - k\sigma - k + \mathrm{NCut}(P_1, \ldots, P_k),$$
where $\mathrm{NCut} = \sum_c \mathrm{links}(P_c, V \setminus P_c) / \mathrm{deg}(P_c)$. So each pass of kernel k-means does not raise the [normalized cut](/normalized-cut/), and the method optimizes it without eigenvectors. Other choices of $w$ and $K$ give ratio association, ratio cut and the Kernighan-Lin objective.
- **Spectral relaxation.** Write $J = \mathrm{tr}(K) - \mathrm{tr}(Y^\top K Y)$ with $Y$ the normalized indicator matrix of the clusters ($Y_{ic} = 1/\sqrt{|P_c|}$ for $i \in P_c$). Relaxing $Y$ to any matrix with orthonormal columns gives the top $k$ eigenvectors of $K$, which is the basis of [spectral clustering](/spectral-clustering/) and links to [kernel PCA](/kernel-pca/). The two methods are often combined: spectral clustering to start, kernel k-means to refine.
- **Single point moves.** [Hartigan's method](/hartigan-wong-algorithm/) works in feature space with the same kernel sums.
- **Large data.** Approximate kernel k-means restricts the means to the span of a random sample of points, which cuts the memory to $O(nm)$ for a sample of size $m$.

## When to use it

Use it when the clusters are not convex in the input space but a known kernel, such as a Gaussian kernel, makes them compact, and when $n$ is small enough to store $K$. Use it also to refine the output of spectral clustering or to minimize a normalized cut on a large sparse graph without eigenvectors. For convex clusters plain [k-means](/k-means/) is much cheaper, and for clusters of arbitrary shape and unknown number [DBSCAN](/dbscan/) is often simpler.

## Pitfalls

- **Kernel not positive semidefinite.** A similarity matrix that is not positive semidefinite has no feature map; the objective can rise and the method can cycle. Add a multiple of the identity (or of $D^{-1}$ in the weighted case) to $K$.
- **Bandwidth.** The result of a Gaussian kernel depends strongly on its width. A width too small makes each point its own cluster in feature space; a width too large gives plain k-means.
- **Quadratic memory.** The full kernel matrix does not fit for large $n$. Use a low rank approximation or sampling.
- **Initialization.** As for plain k-means, a poor start gives a poor local optimum. Use several starts, or start from spectral clustering.
- **Empty clusters.** A cluster can lose all its points and stays empty. Reseed it if exactly $k$ clusters are needed.

## Implementations

## History

Schölkopf, Smola and Müller remarked in 1998, in their paper on kernel PCA, that k-means can be carried out in feature space. Girolami (2002) developed kernel k-means as a clustering method and used the eigenvalues of the kernel matrix to choose $k$. Dhillon, Guan and Kulis (2004) introduced the weighted form and proved that it is equivalent to normalized cut and other graph cut objectives, so that the same local search can optimize them.

## References
