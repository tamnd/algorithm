---
tag: BEM639
kind: problem
slug: subspace-clustering-problem
name: Subspace clustering problem
aliases:
- projected clustering
- subspace clustering
- clustering in subspaces of high-dimensional data
area: machine-learning/clustering
level: advanced
summary: "Find clusters that each live in their own subspace of a high-dimensional space: a subset of the attributes (axis-parallel) or any affine subspace (arbitrarily oriented)."
prereqs: [clustering-problem, curse-of-dimensionality]
see_also: [clique-subspace-clustering, biclustering-problem, principal-component-analysis, feature-selection, dbscan, density-based-clustering-problem, k-means-problem, correlation-clustering]
sources:
  - paper: doi:10.1145/1497577.1497578
    title: "Hans-Peter Kriegel, Peer Kröger and Arthur Zimek, Clustering high-dimensional data: a survey on subspace clustering, pattern-based clustering, and correlation clustering, ACM Transactions on Knowledge Discovery from Data 3(1), 2009, article 1"
    locator: "the problems of high-dimensional data (local feature relevance and local feature correlation), the 2^d - 1 axis-parallel subspaces, the split into axis-parallel (projected, soft projected, subspace and hybrid), pattern-based and arbitrarily oriented (correlation) clustering, with the algorithms in each class"
  - paper: doi:10.1145/276304.276314
    title: "Rakesh Agrawal, Johannes Gehrke, Dimitrios Gunopulos and Prabhakar Raghavan, Automatic subspace clustering of high dimensional data for data mining applications, Proceedings of ACM SIGMOD 1998, pages 94 to 105"
    locator: "the problem of finding all dense clusters in all subspaces, the downward closure of density, and the CLIQUE algorithm"
  - paper: "Charu C. Aggarwal, Cecilia Procopiuc, Joel L. Wolf, Philip S. Yu and Jong Soo Park, Fast algorithms for projected clustering, Proceedings of ACM SIGMOD 1999, pages 61 to 72"
    locator: "the projected clustering problem (k disjoint clusters, each with its own set of attributes) and the PROCLUS algorithm"
  - paper: "Charu C. Aggarwal and Philip S. Yu, Finding generalized projected clusters in high dimensional spaces, Proceedings of ACM SIGMOD 2000, pages 70 to 81"
    locator: "clusters in arbitrarily oriented subspaces and the ORCLUS algorithm"
  - paper: "Lance Parsons, Ehtesham Haque and Huan Liu, Subspace clustering for high dimensional data: a review, ACM SIGKDD Explorations 6(1), 2004, pages 90 to 105"
    locator: "the bottom-up (grid, downward closure) and top-down (iterative attribute weighting) families of subspace clustering methods"
---

The subspace clustering problem asks for clusters in high-dimensional data when each cluster shows up only in its own subspace. In $d$ dimensions, a group of points can be tight in some attributes and spread out in the others, and a different group can be tight in other attributes. Clustering in the full space misses both, and one global reduction of the dimension, such as [principal component analysis](/principal-component-analysis/), cannot fit both. In the *axis-parallel* form, a subspace is a non-empty subset of the attributes, so there are $2^d - 1$ subspaces to consider. In the *arbitrarily oriented* form, a subspace is any affine subspace, and the clusters are sets of points near a line, a plane or a higher-dimensional flat. Kriegel, Kröger and Zimek (2009) survey the problem and split it into these two forms and a third, pattern-based form, which is [biclustering](/biclustering-problem/). The search space is exponential in $d$, and the number of clusters that a method reports can be exponential too.

## In plain words

Think of customers described by fifty numbers: age, income, how often they buy shoes, how often they buy books, and so on. One group of customers is alike in age and shoe buying, but differs in everything else. Another group is alike in income and books only.

If you measure distance with all fifty numbers, the differences in the other numbers hide both groups. If you drop some numbers for everyone, you may drop the very numbers that one of the groups needs.

Subspace clustering looks for each group together with the numbers in which that group is tight. The hard part is that there are so many sets of numbers to try: with fifty numbers, more than a million billion.

## Definition

Let $D \subseteq \mathbb{R}^d$ be a set of $N$ points with attributes $A = \{1, \ldots, d\}$. For $\emptyset \ne S \subseteq A$, let $\pi_S$ be the projection onto the attributes in $S$.

**Axis-parallel subspace clusters.** Fix a cluster criterion for point sets in any space, for example "dense", "a connected component of points within distance $\varepsilon$ that has at least $\mathit{minPts}$ points", or "small variance". A *subspace cluster* is a pair $(C, S)$ with $C \subseteq D$ and $\emptyset \ne S \subseteq A$ such that $\pi_S(C)$ is a cluster of $\pi_S(D)$ by that criterion. There are $2^d - 1$ choices of $S$.

**Arbitrarily oriented subspace clusters.** A *correlation cluster* of dimension $\lambda < d$ is a pair $(C, V)$ with $V$ an affine subspace of dimension $\lambda$ such that the points of $C$ lie close to $V$ (for example, the $d - \lambda$ smallest eigenvalues of the covariance matrix of $C$ are small) and $C$ is a cluster by the criterion in $V$.

**The problem.** Given $D$ and the criterion, find the set of subspace clusters $(C_1, S_1), \ldots, (C_k, S_k)$ in one of these forms:

- *subspace clustering* in the narrow sense: all clusters in all subspaces, often only the maximal ones, and a point may lie in several clusters with different subspaces;
- *projected clustering*: a partition of $D$ (maybe with an outlier set) into $k$ clusters, each with its own subspace $S_i$, that optimizes an objective;
- *soft projected clustering*: each cluster gets a weight per attribute instead of a subset;
- *correlation clustering* in the sense of Kriegel and others: clusters with arbitrarily oriented subspaces.

## Variants

- **Axis-parallel against arbitrarily oriented.** Axis-parallel clusters keep the meaning of the attributes ("these customers agree on age and shoes"), and the search runs over subsets of attributes. Arbitrarily oriented clusters also catch linear dependencies between attributes ("income is about twice the spending"), at the cost of a search over all orientations, usually done by local PCA.
- **Bottom-up and top-down.** Bottom-up methods start from one-dimensional dense regions and combine them, using a monotonicity property ([CLIQUE](/clique-subspace-clustering/), ENCLUS, MAFIA, SUBCLU). Top-down methods start from a full-dimensional clustering and refine the attribute set of each cluster (PROCLUS, ORCLUS, PreDeCon) (Parsons, Haque and Liu 2004).
- **Hybrid.** Methods such as DiSH and FIRES report overlapping clusters but not all of them, to control the size of the output.
- **Pattern-based.** If rows are objects and columns are attributes, a cluster that follows a pattern in some attributes is a bicluster; see the [biclustering problem](/biclustering-problem/).

## Examples

**Clusters hidden in the full space.** Ten points in $d = 3$:

| point | $x_1$ | $x_2$ | $x_3$ |
|---|---|---|---|
| $a_1, a_2, a_3, a_4$ | 1, 1, 2, 2 | 1, 2, 1, 2 | 0, 4, 8, 12 |
| $b_1, b_2, b_3, b_4$ | 0, 5, 10, 14 | 8, 8, 9, 9 | 8, 9, 8, 9 |
| $n_1, n_2$ | 7, 12 | 5, 4 | 3, 14 |

Use the criterion "a connected component, with at least 3 points, of the graph that links two points when they differ by at most 1 in each attribute of $S$". A script over all $2^3 - 1 = 7$ subspaces finds:

| $S$ | clusters |
|---|---|
| $\{1, 2, 3\}$ | none |
| $\{1, 2\}$ | $\{a_1, a_2, a_3, a_4\}$ |
| $\{2, 3\}$ | $\{b_1, b_2, b_3, b_4\}$ |
| $\{1, 3\}$ | none |
| $\{1\}$ | $\{a_1, a_2, a_3, a_4, b_1\}$ |
| $\{2\}$ | $\{a_1, \ldots, a_4\}$ and $\{b_1, \ldots, b_4\}$ |
| $\{3\}$ | $\{a_3, b_1, b_2, b_3, b_4\}$ |

The full space has no cluster at all. The two true clusters appear in their own two-dimensional subspaces, and they also project to clusters in each one-dimensional subspace of those, as the downward closure says. But some of the one-dimensional clusters pick up extra points ($b_1$ in $\{1\}$ and $a_3$ in $\{3\}$), so a lower-dimensional view is not a substitute for the right subspace.

**An arbitrarily oriented cluster.** The ten points $(t, 2t \pm 0.5)$, $t = 0, \ldots, 9$, with the sign alternating, spread over $[0, 9]$ in $x_1$ and over $[-0.5, 18.5]$ in $x_2$, so no axis-parallel subspace makes them tight. Their covariance matrix has the eigenvalues $42.45$ and $0.047$: the points lie near a line, a correlation cluster of dimension 1.

**How many subspaces.** $2^d - 1$ is 7 for $d = 3$, 1023 for $d = 10$, 1,048,575 for $d = 20$ and about $1.13 \times 10^{15}$ for $d = 50$.

**Why the full space fails.** For 500 uniform random points in $[0, 1]^d$ and a random query (seed 7), the ratio $(\max - \min)/\min$ of the distances from the query is $304.6$ for $d = 2$, $1.92$ for $d = 10$, $0.36$ for $d = 100$ and $0.105$ for $d = 1000$. Distances concentrate as $d$ grows (Beyer and others 1999; see the [curse of dimensionality](/curse-of-dimensionality/)), so "near" and "far" lose meaning when most attributes are noise for a given cluster.

## Known algorithms

- **CLIQUE** (Agrawal, Gehrke, Gunopulos and Raghavan 1998). A grid with $\xi$ intervals per attribute and a density threshold $\tau$; dense units are found bottom-up like frequent itemsets, using downward closure, and clusters are connected dense units, described as DNF expressions. See [CLIQUE](/clique-subspace-clustering/).
- **ENCLUS** (Cheng, Fu and Zhang 1999) ranks subspaces by the entropy of the grid. **MAFIA** (Goil, Nagesh and Choudhary 1999) uses adaptive grids. **SUBCLU** (Kailing, Kriegel and Kröger 2004) uses [DBSCAN](/dbscan/) in each subspace, bottom-up.
- **PROCLUS** (Aggarwal and others 1999). A $k$-medoid method: each medoid picks the attributes with the smallest average spread of its neighborhood, and points are assigned by a distance averaged over those attributes.
- **DOC** (Procopiuc and others 2002). A Monte Carlo method for one projected cluster at a time, an axis-parallel box of width $w$.
- **ORCLUS** (Aggarwal and Yu 2000). Projected clustering in arbitrarily oriented subspaces, using the eigenvectors of each cluster with the smallest eigenvalues.
- **4C, COPAC, ERiC, CASH** (Kriegel's group). Density-based and Hough-transform methods for correlation clusters.

## Bounds

- **Search space.** $2^d - 1$ axis-parallel subspaces; for each, the number of candidate point sets is $2^N$. Arbitrary orientations form a continuum.
- **Output size.** With a density criterion that is downward closed, a cluster in a subspace of dimension $k$ projects to a cluster in each of the $2^k - 1$ non-empty subsets of its attributes. So reporting all clusters in all subspaces can produce output exponential in $k$, and methods report only maximal subspaces or filter the redundant ones.
- **Hardness.** When every cluster must use all $d$ attributes, the problem becomes ordinary clustering. So projected versions of NP-hard objectives, such as the [k-means problem](/k-means-problem/) with a per-cluster attribute set, are NP-hard. The single best dense box in a subset of attributes is related to the hard biclique problems of [biclustering](/biclustering-problem/).
- **Grid methods.** With $\xi$ intervals per attribute, a single $k$-dimensional subspace has $\xi^k$ grid units. Bottom-up search with downward closure only looks at candidates whose projections are all dense, so it is fast when dense regions have low dimension, and exponential in the largest dimension of a dense unit in the worst case.

## Reductions

- **To frequent itemsets.** For a grid, a dense unit in $S$ is an itemset of (attribute, interval) items that occurs in at least $\tau N$ points. Downward closure is the Apriori property, and bottom-up subspace search is level-wise itemset mining.
- **From ordinary clustering.** Taking $S = A$ for all clusters gives full-dimensional clustering, so subspace clustering contains it.
- **To biclustering.** With the points as rows and the attributes as columns, an axis-parallel subspace cluster with a pattern criterion is a bicluster; Kriegel, Kröger and Zimek call that view pattern-based clustering.
- **A name clash.** "Correlation clustering" here means arbitrarily oriented subspace clustering. It is not the [correlation clustering](/correlation-clustering/) of Bansal, Blum and Chawla, which partitions items from $+$ and $-$ pair labels.

## Applications

- **Gene expression and biology.** Groups of genes or samples that agree on a subset of conditions.
- **Customer and sensor data.** Segments that are defined by a few of many recorded attributes.
- **Text and images.** Bag-of-words or feature vectors with thousands of dimensions, where each topic or object class uses a few of them.
- **Data exploration.** The interpretable output of axis-parallel methods (a cluster with the attributes that define it) is useful in its own right.

## References
