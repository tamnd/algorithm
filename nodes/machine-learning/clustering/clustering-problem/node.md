---
tag: QZE4SH
kind: problem
slug: clustering-problem
name: Clustering problem
aliases:
- cluster analysis
area: machine-learning/clustering
level: intro
summary: Partition a set of points into groups so that points in the same group are similar.
prereqs: [euclidean-distance, metric-space]
see_also: [k-means-problem, k-median-problem, k-center-problem, hierarchical-clustering-problem, density-based-clustering-problem, correlation-clustering, hard-and-soft-clustering, kleinberg-impossibility-theorem]
sources:
  - paper: doi:10.1145/331499.331504
    title: Anil K. Jain, M. Narasimha Murty and Patrick J. Flynn, Data clustering, a review, ACM Computing Surveys 31(3), 1999, pages 264 to 323
    locator: the components of a clustering task (representation, proximity, grouping) and the taxonomy of partitional and hierarchical methods
  - paper: doi:10.1016/j.patrec.2009.09.011
    title: Anil K. Jain, Data clustering, 50 years beyond K-means, Pattern Recognition Letters 31(8), 2010, pages 651 to 666
    locator: the definition of clustering, the dependence on the objective and the representation, and the open problems
  - paper: doi:10.1016/0304-3975(85)90224-5
    title: Teofilo F. Gonzalez, Clustering to minimize the maximum intercluster distance, Theoretical Computer Science 38, 1985, pages 293 to 306
    locator: the k-center objective, the farthest point 2-approximation, and its NP-hardness
  - paper: "Jon Kleinberg, An impossibility theorem for clustering, Advances in Neural Information Processing Systems 15 (NIPS 2002), MIT Press, 2003"
    locator: the axioms of scale invariance, richness and consistency
  - book: isbn:9780321295354
    title: Jon Kleinberg and Éva Tardos, Algorithm Design, Addison-Wesley, 2006
    locator: Section 4.7 (clustering of maximum spacing, solved by Kruskal's algorithm)
  - book: isbn:9780387848570
    title: Trevor Hastie, Robert Tibshirani and Jerome Friedman, The Elements of Statistical Learning, second edition, Springer, 2009
    locator: Section 14.3 (cluster analysis), with proximity matrices, combinatorial algorithms, k-means, mixtures and hierarchical clustering
---

The clustering problem asks to divide a set of objects into groups, called clusters, so that objects in the same cluster are similar and objects in different clusters are not. It is the main task of unsupervised learning: there are no labels, only the objects and a way to compare them. The words "similar" and "group" have no single meaning, so clustering is a family of problems. Each member fixes an input (points with a distance, or a similarity graph) and an objective (for example [k-means](/k-means-problem/), [k-median](/k-median-problem/), [k-center](/k-center-problem/), linkage, density or a graph cut). Different objectives give different answers on the same data, and most of them are NP-hard to optimize.

## In plain words

You have a pile of things, for example customers, photos or genes, and you want to sort them into a few groups of similar things. Nobody tells you what the groups are. You only know how alike any two things are.

There are many ways to say what a good grouping is. You can ask for each group to be tight around a center. You can ask that no thing is far from the center of its group. You can ask that the groups are separated by wide empty gaps. You can ask that the groups are crowded regions with sparse space between them. Each choice is a different problem, and on the same data they can give different groups.

## Definition

**The input.** One of these:

- **Points with a distance.** A finite set $X = \{x_1, \ldots, x_n\}$ in a [metric space](/metric-space/) $(M, \mathrm{dist})$, or a dissimilarity matrix $D \in \mathbb{R}^{n \times n}$ with $D_{ij} = \mathrm{dist}(x_i, x_j)$. The most common case is $X \subset \mathbb{R}^d$ with the [Euclidean distance](/euclidean-distance/).
- **A similarity graph.** A graph $G = (V, E, w)$ with a weight $w_{ij} \ge 0$ on each edge that is large when $i$ and $j$ are similar. A common way to build it from points is the Gaussian weight $w_{ij} = \exp(-\|x_i - x_j\|^2 / (2\sigma^2))$ on the edges from each point to its nearest neighbors. In correlation clustering each edge is labeled "similar" or "dissimilar" instead.

Often a number $k$ of clusters is also given.

**The output.** A partition $\mathcal{C} = \{C_1, \ldots, C_k\}$ of $X$ into nonempty clusters. Some variants return more or less than a partition: a tree of nested partitions (hierarchical clustering), a membership weight for each point and cluster ([soft clustering](/hard-and-soft-clustering/)), or a partition of only part of the points, with the rest labeled as noise.

**The objective.** A cost to minimize or a quality to maximize. The main families, with $c(x)$ the center nearest to $x$ when the clusters have centers:

| family | objective | example method |
|---|---|---|
| [k-means](/k-means-problem/) | minimize $\sum_{x \in X} \|x - c(x)\|^2$ over $k$ centers in $\mathbb{R}^d$ | [k-means](/k-means/) |
| [k-median](/k-median-problem/) | minimize $\sum_{x \in X} \mathrm{dist}(x, c(x))$ over $k$ centers | [partitioning around medoids](/partitioning-around-medoids/) |
| [k-center](/k-center-problem/) | minimize $\max_{x \in X} \mathrm{dist}(x, c(x))$ over $k$ centers | the farthest point rule of Gonzalez |
| max spacing | maximize the least distance between points of different clusters | [single linkage](/single-linkage-clustering/) |
| [linkage](/hierarchical-clustering-problem/) | a tree built by merging the two closest clusters under a linkage rule | [agglomerative clustering](/agglomerative-clustering/), [Ward's method](/ward-method/) |
| [density](/density-based-clustering-problem/) | clusters are connected regions where the density is above a level, the rest is noise | [DBSCAN](/dbscan/), [mean shift](/mean-shift/) |
| graph cuts | minimize the weight of edges between clusters, divided by the cluster sizes or volumes | [spectral clustering](/spectral-clustering/), [normalized cut](/normalized-cut/) |
| [correlation](/correlation-clustering/) | minimize the number of "similar" edges cut plus "dissimilar" edges kept; $k$ is free | the [pivot algorithm](/pivot-algorithm/) |
| model based | maximize the likelihood of a mixture of distributions | the [Gaussian mixture model](/gaussian-mixture-model/) |

There is no single best objective. Kleinberg showed that no clustering function on distances can satisfy three natural axioms at once; see the [impossibility theorem](/kleinberg-impossibility-theorem/).

## Variants

- **Known or unknown $k$.** Center based objectives need $k$; otherwise the best cost is 0 with $n$ clusters. Methods such as [X-means](/x-means/), [G-means](/g-means/), the [elbow method](/elbow-method/) and the [gap statistic](/gap-statistic/) choose $k$. Density methods and correlation clustering find $k$ by themselves.
- **Hard or soft.** A hard clustering puts each point in one cluster; a soft clustering gives membership weights, as in [fuzzy c-means](/fuzzy-c-means/) and Gaussian mixtures. See [hard and soft clustering](/hard-and-soft-clustering/).
- **Flat or hierarchical.** A [hierarchical clustering](/hierarchical-clustering-problem/) returns a tree, a [dendrogram](/dendrogram/), from which a flat clustering is cut at any level. [Dasgupta's cost](/dasgupta-cost/) gives the tree an objective.
- **With outliers.** Some points may stay out of all clusters, as noise in DBSCAN or as $z$ excluded points in k-center with outliers.
- **With constraints.** [Constrained clustering](/constrained-clustering/) adds must-link and cannot-link pairs or limits on the cluster sizes.
- **Other structure.** [Subspace clustering](/subspace-clustering-problem/) looks for clusters in different subsets of the features, and [biclustering](/biclustering-problem/) clusters the rows and the columns of a matrix at once.
- **Restricted computation.** Streaming versions see the points once, with small memory, as in [BIRCH](/birch/) and [streaming k-median](/streaming-k-median/).

## Examples

Take the six numbers $0, 1, 2, 4, 5, 9$ on the line and $k = 2$. For each objective below, some optimal partition of points on a line cuts between two neighbors, so only five partitions need checks.

| objective | best partition | cost |
|---|---|---|
| k-means (sum of squares) | $\{0, 1, 2\}$, $\{4, 5, 9\}$ | $2 + 14 = 16$ |
| k-median (sum of distances) | $\{0, 1, 2\}$, $\{4, 5, 9\}$ | $2 + 5 = 7$ |
| k-center (largest radius, centers anywhere on the line) | $\{0, 1, 2, 4\}$, $\{5, 9\}$ | $\max(2, 2) = 2$ |
| max spacing (largest gap) | $\{0, 1, 2, 4, 5\}$, $\{9\}$ | gap $4$ |

The k-means and k-median objectives sum over all points, so they keep the tight group $0, 1, 2$ together and put the far point 9 with 4 and 5. The k-center objective looks only at the worst point, so it balances the two radii. The max spacing objective cuts the widest gap and leaves the point 9 alone. Three objectives give three answers, and each answer is right for its own objective.

## Known algorithms

- **Center based.** For k-means: the [k-means algorithm](/k-means/) of Lloyd, the [Hartigan-Wong algorithm](/hartigan-wong-algorithm/), [k-means++](/k-means-plus-plus/) seeding, [mini-batch k-means](/mini-batch-k-means/), [bisecting k-means](/bisecting-k-means/) and [kernel k-means](/kernel-k-means/). For k-median: [partitioning around medoids](/partitioning-around-medoids/) and local search. For k-center: the farthest point rule of Gonzalez, a 2-approximation.
- **Hierarchical.** [Agglomerative clustering](/agglomerative-clustering/) with single, complete, average or [Ward](/ward-method/) linkage, [divisive clustering](/divisive-clustering/) and [BIRCH](/birch/).
- **Density based.** [DBSCAN](/dbscan/), [OPTICS](/optics/), [HDBSCAN](/hdbscan/) and [mean shift](/mean-shift/).
- **Graph based.** [Spectral clustering](/spectral-clustering/) for normalized cuts, the [pivot algorithm](/pivot-algorithm/) for correlation clustering, and [affinity propagation](/affinity-propagation/).
- **Model based.** [Expectation maximization](/expectation-maximization/) for the [Gaussian mixture model](/gaussian-mixture-model/), and [fuzzy c-means](/fuzzy-c-means/).

## Bounds

- **k-means.** NP-hard in the plane for general $k$, and in general dimension already for $k = 2$; see [NP-hardness of k-means](/k-means-np-hardness/). In one dimension a dynamic program solves it exactly in polynomial time.
- **k-median and k-center.** Both are NP-hard in general metrics. For k-center, the farthest point rule gives a factor 2, and no factor $2 - \varepsilon$ is possible unless P = NP; see [k-center hardness](/k-center-hardness/).
- **Max spacing.** Solvable exactly in $O(m \log n)$ time on a graph with $m$ edges: stop Kruskal's algorithm when $k$ components remain; see [maximum spacing optimality](/maximum-spacing-optimality/).
- **Graph cuts and correlation clustering.** Minimum normalized cut and correlation clustering are NP-hard. Spectral methods solve a relaxation, and the pivot algorithm is a 3-approximation in expectation for correlation clustering on complete graphs.
- **No universal objective.** By the [impossibility theorem](/kleinberg-impossibility-theorem/) of Kleinberg, the choice of objective is a modeling decision, not something an algorithm can avoid.

## Reductions

- **k-median and facility location.** The k-median problem is the [facility location problem](/facility-location-problem/) with no opening costs and at most $k$ open facilities. Many approximation methods move between the two by a Lagrangian price on the facilities.
- **Max spacing and spanning trees.** The max spacing clustering is the set of components left by removing the $k - 1$ heaviest edges of a [minimum spanning tree](/minimum-spanning-tree/), which is the same as single linkage.
- **Graph cuts and k-means.** Weighted [kernel k-means](/kernel-k-means/) and minimum normalized cut have the same objective for a suitable kernel and weights, so either can solve the other.
- **k-means and quantization.** The k-means problem is the design of a [vector quantizer](/vector-quantization/) with $k$ code vectors and squared error.
- **Points to graphs.** Any input of points with a distance gives a similarity graph, by a kernel or by nearest neighbors, so graph methods apply to points too.

## Applications

- **Compression.** [Vector quantization](/vector-quantization/) and [color quantization](/color-quantization/) replace each point by the center of its cluster.
- **Images.** [Image segmentation](/image-segmentation/) clusters the pixels by color and position.
- **Networks.** [Community detection](/community-detection/) clusters the nodes of a graph.
- **Science and business.** Grouping genes by their expression profiles, documents by topic, and customers by their behavior.
- **Preprocessing.** Clusters serve as features, as a first step for nearest neighbor search, or to choose a small set of representative points.

## References
