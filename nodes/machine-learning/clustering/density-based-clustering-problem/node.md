---
tag: HMGKQX
kind: problem
slug: density-based-clustering-problem
name: Density-based clustering problem
aliases:
- density-connected clustering
- high-density clustering
area: machine-learning/clustering
level: intro
summary: "Find clusters as regions of high density separated by regions of low density, with clusters of any shape and points in sparse regions left as noise."
prereqs: [clustering-problem, probability-density-function]
see_also: [dbscan, optics, hdbscan, mean-shift, denclue, density-peak-clustering, single-linkage-clustering, hierarchical-clustering-problem]
sources:
  - book: isbn:9780471356455
    title: John A. Hartigan, Clustering Algorithms, Wiley, 1975
    locator: the chapter on density clusters (high density clusters as connected parts of the level sets of a density, and the tree they form)
  - paper: doi:10.1080/01621459.1981.10477658
    title: "J. A. Hartigan, Consistency of single linkage for high-density clusters, Journal of the American Statistical Association 76(374), 1981"
    locator: the definition of consistency for the cluster tree, and the result that single linkage is consistent in one dimension but not in higher dimensions
  - paper: "Kamalika Chaudhuri and Sanjoy Dasgupta, Rates of convergence for the cluster tree, Advances in Neural Information Processing Systems 23 (NIPS 2010)"
    locator: robust single linkage and its consistency and rates for the cluster tree
  - paper: "Werner Stuetzle, Estimating the cluster tree of a density by analyzing the minimal spanning tree of a sample, Journal of Classification 20, 2003"
    locator: the cluster tree of a density and its estimate from the minimum spanning tree of a sample
  - paper: doi:10.1002/widm.30
    title: "Hans-Peter Kriegel, Peer Kröger, Jörg Sander and Arthur Zimek, Density-based clustering, WIREs Data Mining and Knowledge Discovery 1(3), 2011"
    locator: a survey of the density-based notion of a cluster and of DBSCAN, OPTICS, DENCLUE and related methods
---

The density-based clustering problem asks for the groups of a data set as the regions where the points are dense, separated by regions where they are sparse. A cluster can have any shape, its number is not given in advance, and points in sparse regions can stay outside every cluster as *noise*. The statistical form, due to Hartigan (1975), takes the clusters to be the connected parts of the level sets $\{x : f(x) \ge \lambda\}$ of the [density](/probability-density-function/) $f$ of the data, and these parts for all $\lambda$ form a tree, the *cluster tree*. Unlike the [k-means problem](/k-means-problem/), the task has no single objective function. Each algorithm fixes its own density estimate, its own level or levels, and its own rule for what a cluster is.

## In plain words

Think of the data as people standing in a field. Where many people stand close together, there is a crowd. A crowd can be round, long, or curved like a river. Between the crowds, only a few people stand here and there.

The task is to find the crowds. You do not say in advance how many crowds there are. A person who stands alone, far from any crowd, belongs to no crowd. That person is noise.

What counts as a crowd depends on how strict you are. With a strict rule, only the densest spots are crowds, and one big crowd may break into two. With a loose rule, nearby crowds join into one. So there is no single right answer, only answers at different levels of strictness.

## Definition

**The population form.** Let $f$ be a probability density on $\mathbb{R}^d$. For a level $\lambda > 0$, the *level set* is $L(\lambda) = \{x : f(x) \ge \lambda\}$. A **high density cluster at level $\lambda$** is a maximal connected subset of $L(\lambda)$ (Hartigan 1975). If $\lambda < \lambda'$, then $L(\lambda') \subseteq L(\lambda)$, so each cluster at level $\lambda'$ lies inside one cluster at level $\lambda$. Two clusters, at any levels, are therefore either nested or disjoint, and all of them together form a tree, the **cluster tree** of $f$. Points with $f(x) < \lambda$ are noise at level $\lambda$.

**The sample form.** The density is not known. The input is a finite set $D$ of $n$ points, taken from $f$, in $\mathbb{R}^d$ or in a [metric space](/metric-space/). The output is one of:

- a **flat clustering** at a level: disjoint clusters $C_1, \ldots, C_k \subseteq D$ and a noise set $D \setminus \bigcup_i C_i$, where $k$ is an output;
- a **hierarchy**: an estimate of the cluster tree, with the sample points attached to its nodes.

**A combinatorial form.** [DBSCAN](/dbscan/) gives a definition that uses no density function. With a radius $\varepsilon$ and a count $\mathit{MinPts}$, a point is a *core point* if at least $\mathit{MinPts}$ points lie within $\varepsilon$ of it. The count is a crude density estimate, and "core" means "in the level set". Clusters are the sets of points that are *density-connected* through chains of core points, and noise is the rest. The relation "density-connected" is what gave the problem its other name, density-connected clustering.

**No single objective.** The k-means problem asks to minimize one cost, and every k-means algorithm is judged by that cost. Density-based clustering has no such cost. The level $\lambda$, the density estimate (a count in a ball, a [k-nearest neighbor](/k-nearest-neighbor-search/) distance, a kernel sum), the notion of connection (a radius, a graph, a gradient flow) and the rule that picks clusters from the tree are all choices. Two methods can give different answers on the same data and both be correct for their own definition. The impossibility theorem of [Kleinberg](/kleinberg-impossibility-theorem/) shows that no clustering rule meets three natural axioms at once, so some choice of this kind cannot be avoided.

## Variants

- **One level.** Fix the level and return a flat clustering with noise. DBSCAN fixes it by $\varepsilon$ and $\mathit{MinPts}$, and [DENCLUE](/denclue/) by a threshold $\xi$ on a kernel density.
- **The whole cluster tree.** Return all levels at once. [OPTICS](/optics/) returns an ordering from which the DBSCAN clusters at every smaller radius can be read, and [HDBSCAN](/hdbscan/) returns the DBSCAN\* hierarchy.
- **A flat clustering chosen from the tree.** Select disjoint nodes of the tree by a score. HDBSCAN maximizes the total stability, a form of the excess of mass. This allows clusters of different densities, which no single level can give.
- **Mode clustering.** Take a cluster to be the set of points whose path of steepest ascent on the density ends at the same local maximum (mode). [Mean shift](/mean-shift/) and DENCLUE do this with a kernel density estimate. [Density peak clustering](/density-peak-clustering/) is a discrete form: each point follows its nearest point of higher density.
- **Partition or noise.** Some methods give every point a cluster (mean shift by default). Others leave sparse points as noise (DBSCAN, HDBSCAN).
- **Subspace clusters.** In high dimension, look for dense regions in subsets of the features, as in [CLIQUE](/clique-subspace-clustering/). See the [subspace clustering problem](/subspace-clustering-problem/).

## Examples

**Two levels on the line.** Take the points 0, 1, 2, 3, 10, 11, 12, 13 and 30, and count a point as dense if at least 3 points lie within distance $\varepsilon$ of it, the point itself counted.

| $\varepsilon$ | dense points | clusters | noise |
|---|---|---|---|
| 1 | 1, 2, 11, 12 | {0, 1, 2, 3}, {10, 11, 12, 13} | 30 |
| 7 | all but 30 | {0, 1, 2, 3, 10, 11, 12, 13} | 30 |
| 17 | all but 30 | all nine points | none |

At $\varepsilon = 1$ the points 0 and 3 are not dense, but each lies within 1 of a dense point, so they join its cluster as border points. At $\varepsilon = 17$ the point 30 has only 13 within reach, so it is not dense, but it joins as a border point of the dense point 13. A larger radius is a lower density level, so the clusters grow and join. The three rows are three cuts of one tree: the root holds all points, it has one child without the point 30, and that child splits into the two groups of four.

**Shapes that k-means cannot find.** Two rings around one center, a small one inside a large one, with points spread evenly on each. The density is high on the rings and low between them, so a density-based method finds the two rings as two clusters. [k-means](/k-means/) with $k = 2$ cuts both rings with a straight line, because its clusters are convex cells.

**Different densities.** One tight group of 50 points next to a wide group of 50 points. A radius small enough to keep the two groups apart makes most of the wide group noise. A radius large enough for the wide group merges them. No single level gives both, but the cluster tree holds both, and HDBSCAN can pick the tight group at a high level and the wide group at a low level.

## Known algorithms

| algorithm | output | density estimate | time with brute force distances |
|---|---|---|---|
| [DBSCAN](/dbscan/) (1996) | flat, with noise | count in an $\varepsilon$-ball | $\Theta(n^2 d)$ |
| [OPTICS](/optics/) (1999) | ordering for all $\varepsilon' \le \varepsilon$ | count in a ball, core distance | $O(n^2 d + n^2 \log n)$ |
| [HDBSCAN](/hdbscan/) (2013) | hierarchy and a flat selection | distance to the $m_{\mathrm{pts}}$-th nearest point | $O(n^2 (d + \log n))$ |
| [DENCLUE](/denclue/) (1998) | flat, with noise | kernel sum | heuristic, depends on the number of hill climbing steps |
| [Mean shift](/mean-shift/) (1975, 1995) | partition by modes | kernel density estimate | $O(n^2 d)$ for each iteration |
| [Density peak clustering](/density-peak-clustering/) (2014) | partition, optional halo | count in a ball or Gaussian kernel | $\Theta(n^2 d)$ |
| [Single linkage](/single-linkage-clustering/) | hierarchy | none (each point has the same weight) | $O(n^2 d)$ |

Robust single linkage (Chaudhuri and Dasgupta 2010) is single linkage on points that pass a $k$-nearest neighbor density test, and it is close to the hierarchy of HDBSCAN. A [Gaussian mixture model](/gaussian-mixture-model/) is a parametric alternative: it fits a density of a fixed form and gives clusters by components, not by level sets.

## Bounds

- **Exact DBSCAN.** With brute force range queries, DBSCAN costs $\Theta(n^2)$ distance computations. Gan and Tao (2015) show that exact DBSCAN in $\mathbb{R}^d$ for $d \ge 3$ needs $\Omega(n^{4/3})$ time, under the assumption that unit-spherical emptiness checking needs it. In the plane it takes $O(n \log n)$ time. Their $\rho$-approximate DBSCAN takes $O(n)$ expected time for fixed $d$ and $\rho$.
- **Consistency.** An estimate of the cluster tree is *Hartigan consistent* if, for any two disjoint clusters $A$ and $A'$ of $f$, with probability tending to 1 the smallest estimated clusters that hold the sample points of $A$ and of $A'$ are disjoint. Hartigan (1981) showed that single linkage has this property in one dimension and not in higher dimensions, because thin chains of points join separate clusters. Chaudhuri and Dasgupta (2010) showed that robust single linkage is consistent in any dimension and gave rates.
- **Dimension.** Nonparametric density estimates need a number of points that grows exponentially in $d$ for a fixed accuracy, so density-based methods work best in low dimension (see [curse of dimensionality](/curse-of-dimensionality/)).

## Reductions

- **To connected components.** With the core points fixed, the DBSCAN\* clusters are the [connected components](/connected-components/) of the graph that joins core points within $\varepsilon$.
- **To a minimum spanning tree.** The whole DBSCAN\* hierarchy is read from one [minimum spanning tree](/minimum-spanning-tree/) of the mutual reachability distances (HDBSCAN). With $\mathit{MinPts} = 2$, this is the single linkage hierarchy, which is read from a Euclidean minimum spanning tree.
- **To range searching.** DBSCAN reduces to $n$ [fixed-radius near neighbor](/fixed-radius-near-neighbors/) queries, so a [k-d tree](/kd-tree/) or an [R\*-tree](/r-star-tree/) speeds it up in low dimension.
- **To hill climbing.** Mode clustering is [hill climbing](/hill-climbing/) on the estimated density from each point. The mean shift step is a [fixed point iteration](/fixed-point-iteration/).

## Applications

- **Spatial databases.** DBSCAN was designed for geographic data, where clusters follow roads, rivers and coasts.
- **Outlier detection.** The noise points are candidate outliers, and HDBSCAN gives each point an outlier score.
- **Image segmentation.** Mean shift in the joint space of position and color segments images and tracks objects in video (see [image segmentation](/image-segmentation/)).
- **Science.** Astronomers find groups of galaxies by friends of friends linking, which is single linkage at a fixed radius. Biologists group cells and molecular states by density peaks.

## References
