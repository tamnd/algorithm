---
tag: 4PZFVQ
kind: definition
slug: cluster-purity
name: Cluster purity
aliases:
- purity of a clustering
area: machine-learning/clustering
level: intro
summary: The share of objects that are in the majority class of their cluster. It is 1 for singleton clusters, so it cannot compare clusterings with different numbers of clusters.
prereqs: [clustering-problem, confusion-matrix]
see_also: [rand-index, adjusted-rand-index, normalized-mutual-information, cluster-validity]
sources:
  - book: isbn:9780521865715
    title: Christopher D. Manning, Prabhakar Raghavan and Hinrich Schütze, Introduction to Information Retrieval, Cambridge University Press, 2008
    locator: Section 16.3 (evaluation of clustering), the definition of purity and the 17-point example of Figure 16.4 with purity about 0.71
  - paper: doi:10.1007/s10791-008-9066-8
    title: "Enrique Amigó, Julio Gonzalo, Javier Artiles and Felisa Verdejo, A comparison of extrinsic clustering evaluation metrics based on formal constraints, Information Retrieval 12(4), 2009, pages 461 to 486"
    locator: purity and inverse purity in the family of set-matching metrics, and the formal constraints that they fail
---

Cluster purity measures how much each cluster is made of one known class. For each cluster, take the class with the most objects in it, and count those objects. Purity is the sum of these counts divided by the number $n$ of objects. It is an external [cluster validity](/cluster-validity/) index: it needs the true classes. It is easy to compute and to explain, but it has a serious fault: if each object is its own cluster, purity is 1. So it can only compare clusterings that have the same number of clusters.

## Definition

**Setting.** $X$ is a set of $n$ objects. $\Omega = \{\omega_1, \ldots, \omega_k\}$ is a clustering of $X$ into $k$ clusters, and $\mathcal{C} = \{c_1, \ldots, c_J\}$ is the partition of $X$ into known classes. No distance is used. Let $n_{ij} = |\omega_i \cap c_j|$ be the contingency table, which is the [confusion matrix](/confusion-matrix/) of clusters against classes.

**Purity.**

$$\mathrm{purity}(\Omega, \mathcal{C}) = \frac{1}{n} \sum_{i=1}^{k} \max_{j} |\omega_i \cap c_j| = \frac{1}{n} \sum_{i=1}^{k} \max_j n_{ij}.$$

The class $\arg\max_j n_{ij}$ is the majority class of cluster $\omega_i$. If each cluster is labeled with its majority class, purity is the accuracy of these labels. Two clusters can have the same majority class: purity does not need a one-to-one match of clusters and classes. Ties do not change the value.

**Cost.** One pass over the labels builds the nonzero cells of the table in $O(n)$ time with a hash map. The maxima then take time proportional to the number of nonzero cells. The implementation returns an exact fraction.

**Properties.**

- **Range.** $\max_j |c_j| / n \le \mathrm{purity} \le 1$. For the lower bound, let $c_{j^*}$ be the largest class. Then $\sum_i \max_j n_{ij} \ge \sum_i n_{i j^*} = |c_{j^*}|$. One cluster with all objects reaches the lower bound.
- **Splitting never lowers purity.** If a cluster $\omega$ is split into $\omega'$ and $\omega''$, then $\max_j |\omega \cap c_j| \le \max_j |\omega' \cap c_j| + \max_j |\omega'' \cap c_j|$, because the class that wins in $\omega$ has at most the maximum count in each part. So refining a clustering can only increase purity.
- **Singletons.** With $k = n$ clusters of one object each, every cluster is pure, and purity is 1. By the previous property, purity favors clusterings with more clusters. It is not a criterion for choosing $k$.
- **Not symmetric.** $\mathrm{purity}(\Omega, \mathcal{C})$ and $\mathrm{purity}(\mathcal{C}, \Omega)$ are different in general. The second is called the inverse purity. It is 1 when each class lies in one cluster, so it rewards large clusters. Some reports combine both into one score, in the same way as precision and recall.
- **No chance correction.** Random clusters already get at least the share of the largest class.

## Examples and non-examples

**The example of Manning, Raghavan and Schütze.** 17 objects in three classes x, o and d, and three clusters:

| | x | o | d | majority | count |
|---|---|---|---|---|---|
| cluster 1 | 5 | 1 | 0 | x | 5 |
| cluster 2 | 1 | 4 | 1 | o | 4 |
| cluster 3 | 2 | 0 | 3 | d | 3 |

$$\mathrm{purity} = \frac{5 + 4 + 3}{17} = \frac{12}{17} \approx 0.71.$$

The largest class, x, has 8 objects, so one cluster with all 17 objects has purity $8/17 \approx 0.47$, and 17 singleton clusters have purity 1. The value 0.71 is between these two extremes, and it is only useful against other clusterings with three clusters.

**Not symmetric.** Four objects, one cluster $\{0, 1, 2, 3\}$, and classes $\{0, 1\}$ and $\{2, 3\}$. The purity of the clustering is $2/4 = 1/2$. The other way, each class lies inside the single cluster, so the purity of the classes with respect to the clustering is 1.

**Two clusters, one majority.** Clusters $\{0, 1, 2\}$ and $\{3, 4, 5\}$ with classes a, a, b and a, a, b. Both clusters have the majority class a, and purity is $(2 + 2)/6 = 2/3$. A one-to-one match would assign class b to one of the clusters and give a lower accuracy, $(2 + 1)/6 = 1/2$.

**Non-examples.**

- Purity is not the [Rand index](/rand-index/). The Rand index counts agreeing pairs and is symmetric. Purity counts objects and is not symmetric.
- Purity is not the accuracy after an optimal one-to-one match of clusters and classes. That accuracy needs an assignment problem, and it does not reach 1 with singletons when there are fewer classes than objects.
- Purity is not a measure of compactness. It does not use distances. A cluster can be pure and spread out.

## Related definitions

- [Rand index](/rand-index/) and [adjusted Rand index](/adjusted-rand-index/): external indices over pairs; the adjusted form is corrected for chance.
- [Normalized mutual information](/normalized-mutual-information/): an external index from information theory. Its value for singleton clusters is less than 1, so it penalizes the many small clusters that purity rewards, but only in part.
- [Confusion matrix](/confusion-matrix/): the table from which purity is read.
- [Cluster validity](/cluster-validity/) gives the overview of external and internal indices.

## References
