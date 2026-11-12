---
tag: 5AGNGC
kind: concept
slug: cluster-validity
name: Cluster validity
aliases:
- cluster validation
- clustering evaluation
area: machine-learning/clustering
level: intro
summary: "How to judge a clustering: external indices compare it with known classes, internal indices use only the data, and relative criteria compare clusterings, for example to choose k."
prereqs: [clustering-problem]
see_also: [adjusted-rand-index, normalized-mutual-information, silhouette-coefficient, calinski-harabasz-index, davies-bouldin-index, gap-statistic, kleinberg-impossibility-theorem, consensus-clustering]
sources:
  - book: isbn:9780130222787
    title: Anil K. Jain and Richard C. Dubes, Algorithms for Clustering Data, Prentice Hall, 1988
    locator: Chapter 4 (cluster validity), with external, internal and relative criteria
  - paper: doi:10.1023/A:1012801612483
    title: "Maria Halkidi, Yannis Batistakis and Michalis Vazirgiannis, On clustering validation techniques, Journal of Intelligent Information Systems 17(2-3), 2001, pages 107 to 145"
    locator: the survey of external, internal and relative validity criteria and of the indices for choosing k
  - paper: doi:10.1007/BF02294245
    title: "Glenn W. Milligan and Martha C. Cooper, An examination of procedures for determining the number of clusters in a data set, Psychometrika 50(2), 1985, pages 159 to 179"
    locator: the Monte Carlo comparison of 30 rules for choosing the number of clusters
  - book: isbn:9780521865715
    title: Christopher D. Manning, Prabhakar Raghavan and Hinrich Schütze, Introduction to Information Retrieval, Cambridge University Press, 2008
    locator: Section 16.3 (evaluation of clustering), with purity, NMI, the Rand index and the F measure on one example
---

Cluster validity is the evaluation of the result of a [clustering](/clustering-problem/) method. A method always returns some partition, even for data with no groups, so the question is whether the partition is good, and better than other partitions. There are three kinds of criteria. **External indices** compare the clustering with a known partition into classes: the [Rand index](/rand-index/), the [adjusted Rand index](/adjusted-rand-index/), [normalized mutual information](/normalized-mutual-information/) and [purity](/cluster-purity/). **Internal indices** use only the data and the clustering: the [silhouette coefficient](/silhouette-coefficient/), the [Calinski-Harabasz index](/calinski-harabasz-index/), the [Davies-Bouldin index](/davies-bouldin-index/) and the [Dunn index](/dunn-index/). **Relative criteria** compare clusterings from the same method with different parameters, mostly to choose the number of clusters $k$, as in the [elbow method](/elbow-method/) and the [gap statistic](/gap-statistic/). Each internal index has its own idea of a good cluster, so each favors particular cluster shapes.

## In plain words

After a computer has put your data into groups, you want to know if the groups are any good. There are three ways to ask.

If you already know the right groups for some of the data, you can compare. You check how often the computer agrees with the known answer. Some scores also subtract the agreement that a random guess would get.

If you know nothing, you can look at the groups themselves. Good groups are tight inside and far apart from each other. Each score measures tight and far apart in its own way, so each score likes some shapes of groups more than others.

To choose how many groups to make, you compare the results for different numbers of groups. More groups always look tighter, so a fair choice must correct for that.

## The idea

**Notation.** $X = \{x_1, \ldots, x_n\}$ is the data: $n$ points in $\mathbb{R}^d$, or $n$ objects with a dissimilarity. A clustering $\mathcal{C} = \{C_1, \ldots, C_k\}$ is a partition of $X$ into $k$ clusters. For external indices, a second partition $V$ into known classes is given.

**External indices** compare two [partitions](/set-partitions/) through their contingency table $n_{ij} = |C_i \cap V_j|$, and they need no distances.

| index | what it counts | range | chance corrected |
|---|---|---|---|
| [Rand index](/rand-index/) | share of pairs on which the partitions agree | $[0, 1]$ | no |
| [adjusted Rand index](/adjusted-rand-index/) | the Rand index minus its expected value, rescaled | at most 1, can be negative | yes, mean 0 |
| [normalized mutual information](/normalized-mutual-information/) | shared information over a mean of the entropies | $[0, 1]$ | no; the AMI is |
| [purity](/cluster-purity/) | share of objects in the majority class of their cluster | $[\text{largest class}/n, 1]$ | no |

The indices without chance correction give high values to random clusterings, and more so when there are many clusters. Purity is 1 for singleton clusters. So only chance-corrected indices compare clusterings with different $k$ in a fair way.

**Internal indices** score the clustering with the data alone. Each combines a measure of how compact the clusters are with a measure of how separated they are.

| index | compactness | separation | better | cost |
|---|---|---|---|---|
| [silhouette](/silhouette-coefficient/) | mean distance to own cluster, for each object | mean distance to the nearest other cluster | higher | $O(n^2 d)$ |
| [Calinski-Harabasz](/calinski-harabasz-index/) | within-cluster sum of squares | between-cluster sum of squares | higher | $O(nd)$ |
| [Davies-Bouldin](/davies-bouldin-index/) | mean distance to the centroid | distance between centroids | lower | $O(nd + k^2 d)$ |
| [Dunn](/dunn-index/) | largest diameter | smallest distance between clusters | higher | $O(n^2 d)$ |

**Internal indices favor particular shapes.** The Calinski-Harabasz and Davies-Bouldin indices use centroids, so they measure clusters as balls, like [k-means](/k-means-problem/). The silhouette uses means of distances, which also favors round and compact clusters. The Dunn index uses the smallest gap, like [single linkage](/single-linkage-clustering/), so it accepts long and curved clusters but is very sensitive to outliers. An index that measures the same thing as the objective of the method is partly circular: k-means minimizes the within-cluster sum of squares, and for a fixed $k$ the Calinski-Harabasz index is largest exactly for the clustering with the smallest such sum.

**Relative criteria** choose between clusterings, mostly between values of $k$. The internal indices above can do this (take the best value over $k$), but none is defined for $k = 1$. The [elbow method](/elbow-method/) looks for a bend in the within-cluster sum of squares against $k$, with no formal definition of the bend. The [gap statistic](/gap-statistic/) compares that curve with its value for uniform reference data, and it can answer $k = 1$. Other methods, such as [X-means](/x-means/), [G-means](/g-means/) and the [eigengap heuristic](/eigengap-heuristic/), build the choice of $k$ into the method. A further family checks stability: cluster many subsamples of the data and measure, with an external index, how much the results agree, as in [consensus clustering](/consensus-clustering/).

**No criterion is right for all data.** [Kleinberg's impossibility theorem](/kleinberg-impossibility-theorem/) shows that no clustering function has three natural properties at once, so different methods, and the indices that match them, make different trade-offs. In the comparison of Milligan and Cooper, the Calinski-Harabasz index chose $k$ best of 30 rules on their simulated data with well-separated clusters, but such a ranking depends on the kind of data.

## Examples

**One clustering, four external scores.** In the 17-object example of Manning, Raghavan and Schütze, three clusters are compared with three classes:

| purity | Rand index | NMI (arithmetic) | adjusted Rand index |
|---|---|---|---|
| $12/17 \approx 0.71$ | $92/136 \approx 0.68$ | 0.36 | $60/247 \approx 0.24$ |

The numbers are on different scales and cannot be compared with each other. A random clustering with the same sizes has a mean Rand index of about 0.57, so the Rand index of 0.68 is only a little above chance, which the adjusted Rand index of 0.24 shows directly.

**Four internal scores agree.** Take nine points in three triangles: $\{(0, 0), (2, 0), (1, 3)\}$, $\{(8, 0), (10, 0), (9, 3)\}$ and $\{(4, 8), (6, 8), (5, 11)\}$, with the Euclidean distance. Compare the three triangles with a clustering that merges the first two:

| clustering | silhouette | Calinski-Harabasz | Davies-Bouldin | Dunn |
|---|---|---|---|---|
| three triangles | 0.654 | 28 | 0.388 | 1.844 |
| first two merged | 0.440 | 7.47 | 0.732 | 0.583 |

All four prefer the three triangles. The clusters are round, compact and far apart, the case for which these indices were made.

**Four internal scores disagree.** Put 12 points evenly on a circle of radius 1 and 12 on a circle of radius 4, both centered at the origin. Compare the two rings with a cut into a left half and a right half:

| clustering | silhouette | Calinski-Harabasz | Davies-Bouldin | Dunn |
|---|---|---|---|---|
| two rings | 0.198 | 0 | $+\infty$ | 0.375 |
| left and right halves | 0.226 | 9.65 | 1.34 | 0.067 |

The two rings have the same centroid, so the centroid indices give them the worst possible value, and the silhouette also prefers the halves. Only the Dunn index, which looks at the gap between clusters, prefers the rings. Which answer is right depends on what the user means by a cluster, and no index can decide that.

## Where it is used

- Comparing clustering methods on data sets with known classes, in research papers and benchmarks, usually with the adjusted Rand index or NMI.
- Choosing $k$ or other parameters of a method, such as the parameters of [DBSCAN](/dbscan/) or the number of components of a [Gaussian mixture model](/gaussian-mixture-model/), with internal indices or the gap statistic.
- Checking the clusters of a single run in data analysis, for example with a silhouette plot of each cluster.
- Measuring the agreement of the members of a cluster ensemble in [consensus clustering](/consensus-clustering/).

## References
