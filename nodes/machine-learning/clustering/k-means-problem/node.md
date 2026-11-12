---
tag: 2GYFP1
kind: problem
slug: k-means-problem
name: k-means clustering problem
aliases:
- minimum sum-of-squares clustering
- sum-of-squares clustering
- k-means objective
area: machine-learning/clustering
level: core
summary: "Choose k centers in R^d that minimize the sum of squared Euclidean distances from each point to its nearest center."
prereqs: [clustering-problem, euclidean-distance]
see_also: [k-means, k-means-plus-plus, k-means-np-hardness, k-median-problem, k-center-problem, vector-quantization, kernel-k-means, ward-method]
sources:
  - paper: doi:10.1109/TIT.1982.1056489
    title: Stuart P. Lloyd, Least squares quantization in PCM, IEEE Transactions on Information Theory 28(2), 1982, pages 129 to 137
    locator: the quantization error as a sum of squares, and the two optimality conditions (nearest-center cells and centroid levels)
  - paper: doi:10.32614/RJ-2011-015
    title: Haizhou Wang and Mingzhou Song, Ckmeans.1d.dp, optimal k-means clustering in one dimension by dynamic programming, The R Journal 3(2), 2011, pages 29 to 33
    locator: the dynamic program for one dimension, its O(k n^2) time, and the comparison with the heuristic k-means
  - paper: doi:10.1007/s10994-009-5103-0
    title: Daniel Aloise, Amit Deshpande, Pierre Hansen and Preyas Popat, NP-hardness of Euclidean sum-of-squares clustering, Machine Learning 75(2), 2009, pages 245 to 248
    locator: the NP-hardness for two clusters in general dimension
  - paper: doi:10.1016/j.comgeo.2004.03.003
    title: Tapas Kanungo, David M. Mount, Nathan S. Netanyahu, Christine D. Piatko, Ruth Silverman and Angela Y. Wu, A local search approximation algorithm for k-means clustering, Computational Geometry 28(2-3), 2004
    locator: the swap local search and its (9 + epsilon) approximation ratio
  - paper: "Mary Inaba, Naoki Katoh and Hiroshi Imai, Applications of weighted Voronoi diagrams and randomization to variance-based k-clustering, Proceedings of the 10th ACM Symposium on Computational Geometry (SoCG), 1994"
    locator: the exact algorithm for fixed k and d by enumeration of the Voronoi partitions
  - book: isbn:9780387848570
    title: Trevor Hastie, Robert Tibshirani and Jerome Friedman, The Elements of Statistical Learning, second edition, Springer, 2009
    locator: Section 14.3.6 (K-means), with the within-cluster point scatter and its decomposition
  - book: isbn:9781107057135
    title: Shai Shalev-Shwartz and Shai Ben-David, Understanding Machine Learning, Cambridge University Press, 2014
    locator: Chapter 22, Section 22.2 (k-means and other cost minimization clusterings)
---

The k-means problem asks for $k$ centers in $\mathbb{R}^d$ that minimize the sum, over the data points, of the squared [Euclidean distance](/euclidean-distance/) to the nearest center. It is the most used objective of the [clustering problem](/clustering-problem/). For a fixed cluster the best center is the mean of its points, so the problem is the same as a search for the partition with the least within-cluster sum of squares. The problem is [NP-hard](/k-means-np-hardness/) in general, it has an exact dynamic program in one dimension, and the usual method for it is the heuristic [k-means algorithm](/k-means/), which is not the same thing as the problem.

## In plain words

You have many points, for example the positions of customers on a map. You may open a fixed number of shops. Each customer goes to the nearest shop and pays the square of the distance. You want to place the shops so that the total payment is as small as possible.

The square matters. It punishes a far customer much more than a near one, and it has a useful effect: once you know which customers go to a shop, the best place for that shop is the average position of those customers. So the hard part is not to place the shops. The hard part is to decide which customers belong together.

## Definition

**Data model.** The input is a finite list of points $x_1, \ldots, x_n \in \mathbb{R}^d$ with the Euclidean norm $\|\cdot\|$, and a number of clusters $k$ with $1 \le k \le n$. Here $n$ is the number of points, $d$ the dimension and $k$ the number of clusters. The value of $k$ is part of the input.

**Center form.** For a set $C \subset \mathbb{R}^d$ of at most $k$ centers, the cost is
$$\phi(C) = \sum_{i=1}^{n} \min_{c \in C} \|x_i - c\|^2 .$$
The task is to find $C$ with $|C| \le k$ that minimizes $\phi$. Write $\mathrm{OPT}_k$ for the minimum. It exists, because the minimum over $C$ is reached inside the bounded box that holds the points.

**Partition form.** For a partition of the points into clusters $P_1, \ldots, P_k$, let $\mu_j = \frac{1}{|P_j|}\sum_{x \in P_j} x$ be the centroid of a non-empty cluster, and let
$$\mathrm{SSE}(P_1, \ldots, P_k) = \sum_{j=1}^{k} \sum_{x \in P_j} \|x - \mu_j\|^2 ,$$
with the sum taken over the non-empty clusters. The task is to find the partition with the least SSE (the within-cluster sum of squares).

**The centroid identity.** For a finite non-empty set $S$ with mean $\mu$ and each $z \in \mathbb{R}^d$,
$$\sum_{x \in S} \|x - z\|^2 = \sum_{x \in S} \|x - \mu\|^2 + |S|\,\|\mu - z\|^2 .$$
*Proof.* Write $x - z = (x - \mu) + (\mu - z)$ and expand: $\|x - z\|^2 = \|x - \mu\|^2 + 2\langle x - \mu, \mu - z\rangle + \|\mu - z\|^2$. Sum over $x \in S$. The middle terms add to $2\langle \sum_{x \in S}(x - \mu), \mu - z\rangle = 0$, because $\sum_{x \in S} x = |S|\mu$. $\square$

So the mean is the unique best single center for a fixed cluster, and the extra cost of another center $z$ is exactly $|S|\,\|\mu - z\|^2$.

**The two forms have the same optimum.** Take centers $C$, give each point to a nearest center, and replace each center by the centroid of its points. By the identity, no cluster gets more expensive, so the best partition is at least as good as the best center set. In the other direction, a partition with its centroids as centers costs at most its SSE, because each point pays the distance to its nearest centroid, not to its own. If there are at least $k$ distinct points, an optimal partition uses exactly $k$ non-empty clusters, since a cluster with two distinct points can be split with no increase of cost.

**A pairwise form.** Apply the identity with $z = y$ for each $y \in S$ and add: $\sum_{x, y \in S}\|x - y\|^2 = 2|S| \sum_{x \in S}\|x - \mu\|^2$. So the cost of a cluster is
$$\sum_{x \in S}\|x - \mu\|^2 = \frac{1}{2|S|}\sum_{x \in S}\sum_{y \in S}\|x - y\|^2 ,$$
which needs only the distances. The [NP-hardness proof](/k-means-np-hardness/) and the analysis of [k-means++](/k-means-plus-plus-guarantee/) use this form.

## Variants

- **Weighted points.** Each point has a weight $w_i > 0$ and pays $w_i$ times its squared distance. The best center of a cluster is the weighted mean. [Coresets](/coreset/) and [kernel k-means](/kernel-k-means/) use this form.
- **Other powers and metrics.** With the distance itself instead of its square, the problem is the [k-median problem](/k-median-problem/). With the largest distance instead of the sum, it is the [k-center problem](/k-center-problem/). With centers that must be data points of a general [metric space](/metric-space/), the problem is solved in practice by [partitioning around medoids](/partitioning-around-medoids/).
- **Unknown k.** If $k$ is not given, $\mathrm{OPT}_k$ falls as $k$ grows and reaches 0 at the number of distinct points, so the objective alone cannot choose $k$. A rule is needed: the [elbow method](/elbow-method/), the [gap statistic](/gap-statistic/), or a split test as in [X-means](/x-means/) and [G-means](/g-means/).
- **Constraints.** Must-link and cannot-link pairs, or cluster sizes, give [constrained clustering](/constrained-clustering/).
- **Feature space.** Replace each point by its image under a feature map of a kernel. This is [kernel k-means](/kernel-k-means/).

## Examples

**One dimension.** Take the six numbers $1, 2, 4, 7, 8, 13$. The optimal costs are:

| $k$ | optimal clusters | $\mathrm{OPT}_k$ |
|---|---|---|
| 1 | {1, 2, 4, 7, 8, 13} | 593/6 ≈ 98.83 |
| 2 | {1, 2, 4}, {7, 8, 13} | 76/3 ≈ 25.33 |
| 3 | {1, 2, 4}, {7, 8}, {13} | 31/6 ≈ 5.17 |
| 4 | {1, 2}, {4}, {7, 8}, {13} | 1 |
| 5 | {1}, {2}, {4}, {7, 8}, {13} | 1/2 |
| 6 | each number alone | 0 |

For $k = 2$ the centroids are $7/3$ and $28/3$. The cluster {1, 2, 4} costs $(4/3)^2 + (1/3)^2 + (5/3)^2 = 14/3$, and {7, 8, 13} costs $62/3$. For $k = 5$ the clustering {1, 2}, {4}, {7}, {8}, {13} is also optimal, so an optimal partition need not be unique.

**Within and between.** Apply the identity to each cluster with $z$ equal to the overall mean $m$. The total sum of squares splits as $\sum_i \|x_i - m\|^2 = \mathrm{SSE} + \sum_j |P_j|\,\|\mu_j - m\|^2$. In the example with $k = 2$, $m = 35/6$, and $593/6 = 76/3 + 147/2$. So to minimize the within-cluster sum of squares is the same as to maximize the between-cluster sum of squares.

**The search space.** The number of partitions of $n$ points into exactly $k$ non-empty clusters is the [Stirling number of the second kind](/stirling-numbers-second-kind/) $S(n, k)$. It is 31 for $n = 6$, $k = 2$, and 90 for $n = 6$, $k = 3$, but $580{,}606{,}446$ for $n = 20$, $k = 3$. Exhaustive search is possible only for very small inputs.

## Known algorithms

- **Exhaustive search.** Try all $S(n, k)$ partitions and keep the one with the least SSE. This is the reference for tests on tiny inputs.
- **The dynamic program in one dimension.** For $d = 1$ there is an optimal partition whose clusters are intervals of the sorted points. *Proof.* Take an optimal partition and its centroids, and give each point to a nearest centroid, with ties to the leftmost. The cost does not rise, so the result is also optimal. On the line, the set of points nearest to a center $c_j$ among sorted centers is an interval, so each cluster is an interval. $\square$ Sort the points as $a_1 \le \cdots \le a_n$, and let $D[m][i]$ be the least cost of $a_1, \ldots, a_i$ in $m$ clusters. Then
$$D[0][0] = 0, \qquad D[m][i] = \min_{m-1 \le j < i} \big( D[m-1][j] + \mathrm{sse}(j+1, i) \big),$$
where $\mathrm{sse}(j+1, i)$ is the cost of $a_{j+1}, \ldots, a_i$ around their mean. With prefix sums of $a$ and $a^2$, $\mathrm{sse}(j+1, i) = \sum a^2 - (\sum a)^2/(i - j)$ is found in $O(1)$ time. The table has $k n$ entries with $O(n)$ choices each, so the time is $O(k n^2)$ and the space $O(k n)$. Wang and Song (2011) give this program as Ckmeans.1d.dp. The [SMAWK algorithm](/smawk-algorithm/) and the [Monge property](/monge-property/) of the cost lead to faster versions.
- **Fixed $k$ and $d$.** In an optimal partition, each cluster is the part of the points in a cell of the [Voronoi diagram](/voronoi-diagram/) of the centroids, so two clusters are separated by a hyperplane. Enumerating the partitions that hyperplanes can make gives a polynomial algorithm for each fixed $k$ and $d$, with an exponent that grows with $k d$ (Inaba, Katoh and Imai, 1994).
- **Lloyd's heuristic.** The [k-means algorithm](/k-means/) alternates the nearest-center assignment and the centroid update. It reaches a local optimum, which can be arbitrarily worse than $\mathrm{OPT}_k$. [Hartigan's method](/hartigan-wong-algorithm/) moves single points and has fewer local optima.
- **Approximation.** The [k-means++ seeding](/k-means-plus-plus/) gives an expected $8(\ln k + 2)$ approximation. A swap [local search](/local-search/) of Kanungo et al. (2004) gives a $(9 + \varepsilon)$ approximation in polynomial time.

## Bounds

- **Hardness.** The problem is NP-hard for $k = 2$ in general dimension, and for general $k$ in the plane. It is also hard to approximate within some constant $1 + \varepsilon$ when the dimension is part of the input. The exact statements and the proof are on the page [NP-hardness of k-means](/k-means-np-hardness/).
- **Easy cases.** It is solvable in polynomial time for $d = 1$ (the dynamic program above) and for fixed $k$ and $d$.
- **A spectral lower bound.** Let $K = X X^\top$ be the $n \times n$ Gram matrix with eigenvalues $\lambda_1 \ge \cdots \ge \lambda_n \ge 0$. For a partition, let $h_j \in \mathbb{R}^n$ be the indicator vector of $P_j$ divided by $\sqrt{|P_j|}$. These vectors are orthonormal, and $\mathrm{SSE} = \operatorname{tr}(K) - \sum_j h_j^\top K h_j$, because $h_j^\top K h_j = \|\sum_{x \in P_j} x\|^2 / |P_j|$. By the Ky Fan maximum principle, $\sum_j h_j^\top K h_j \le \lambda_1 + \cdots + \lambda_k$ for each set of $k$ orthonormal vectors. So $\mathrm{OPT}_k \ge \lambda_{k+1} + \cdots + \lambda_n$. This is the link between k-means and [principal component analysis](/principal-component-analysis/).

## Reductions

- **From densest cut.** A graph on $n$ vertices maps to $n$ points, one coordinate for each edge, so that the 2-means cost is a constant minus $n$ times the density of the cut. This proves the hardness for $k = 2$; see [NP-hardness of k-means](/k-means-np-hardness/).
- **To weighted kernel k-means.** With the pairwise form, the cost depends only on inner products. So the problem in a feature space is [kernel k-means](/kernel-k-means/), and weighted kernel k-means with a suitable kernel has the same objective as the [normalized cut](/normalized-cut/) of a graph, up to a constant.
- **Ward's method.** [Ward's method](/ward-method/) of [agglomerative clustering](/agglomerative-clustering/) merges, at each step, the two clusters whose union increases the SSE the least. It is a greedy method for the same objective.

## Applications

- **Vector quantization.** A codebook of $k$ vectors with the least mean squared error is an optimal $k$-means center set. Lloyd stated the problem for pulse code modulation; see [vector quantization](/vector-quantization/) and [color quantization](/color-quantization/).
- **Approximate nearest neighbor search.** [Product quantization](/product-quantization/) and the [inverted file index](/inverted-file-index/) store k-means centers of the data or of parts of the vectors.
- **Data analysis.** Segmentation of customers, images and documents, and the initialization of a [Gaussian mixture model](/gaussian-mixture-model/).

## References
