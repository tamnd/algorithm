---
tag: SG9MK0
kind: concept
slug: hubness
name: Hubness
aliases:
- hub phenomenon
- k-occurrence skewness
- hub points
area: searching/similarity-search
level: research
summary: In high dimensions a few points appear as nearest neighbors of many queries while others almost never do.
prereqs: [k-nearest-neighbor-search, curse-of-dimensionality, k-nearest-neighbor-graph]
see_also: [intrinsic-dimensionality, reverse-nearest-neighbor, k-nearest-neighbor-graph-construction, cosine-similarity, hnsw, approximate-nearest-neighbor-search, t-sne, umap]
sources:
  - url: https://www.jmlr.org/papers/v11/radovanovic10a.html
    title: Miloš Radovanović, Alexandros Nanopoulos and Mirjana Ivanović, Hubs in space, popular nearest neighbors in high-dimensional data, Journal of Machine Learning Research 11, 2010
    locator: pages 2487 to 2531 (the k-occurrence N_k, its skewness as a measure of hubness, its growth with the intrinsic dimension, and the fact that hubs lie near the data mean)
  - url: https://www.jmlr.org/papers/v13/schnitzer12a.html
    title: Dominik Schnitzer, Arthur Flexer, Markus Schedl and Gerhard Widmer, Local and global scaling reduce hubs in space, Journal of Machine Learning Research 13, 2012
    locator: pages 2871 to 2902 (local scaling and mutual proximity, which rescale distances to make neighbor relations more symmetric and reduce hubness)
  - paper: doi:10.1145/502807.502808
    title: Edgar Chávez, Gonzalo Navarro, Ricardo Baeza-Yates and José Luis Marroquín, Searching in metric spaces, ACM Computing Surveys 33(3), 2001
    locator: pages 273 to 321 (Section 7, the concentration of the distance histogram in high intrinsic dimension)
---

Hubness is the tendency of high-dimensional data to contain a few points, the hubs, that appear in the $k$-nearest neighbor lists of very many other points, while many other points, the anti-hubs, appear in almost no list. It is measured by the distribution of the $k$-occurrence $N_k(x)$, the in-degree of $x$ in the [k-nearest neighbor graph](/k-nearest-neighbor-graph/): its mean is always exactly $k$, and Radovanović, Nanopoulos and Ivanović showed that its skewness grows with the [intrinsic dimension](/intrinsic-dimensionality/) of the data. Hubness is a side of the [curse of dimensionality](/curse-of-dimensionality/), and it affects classification, retrieval and graph-based [nearest neighbor search](/approximate-nearest-neighbor-search/).

## In plain words

Let every point vote for its 10 closest points. In two dimensions, each point gets about 10 votes, a few more or a few less. In a hundred dimensions, the votes become very unequal: some points get 50 or 90 votes, and many points get none at all.

The popular points are the ones close to the center of the data. In high dimensions all distances are nearly equal, so a small advantage, like being a bit closer to the center, decides almost every vote. A search or a classifier that trusts the votes then gives too much weight to the hubs, and the points with no votes are never found.

## The idea

Let $P$ be a set of $n$ points with a distance $\delta$, and let $N(i)$ be the $k$ nearest neighbors of $p_i$ in $P \setminus \{p_i\}$. The **$k$-occurrence** of $x \in P$ is

$$N_k(x) = |\{i : x \in N(i)\}|,$$

the number of points that have $x$ among their $k$ nearest neighbors, which is the number of [reverse nearest neighbors](/reverse-nearest-neighbor/) of $x$ within $P$.

**The mean is fixed.** Each of the $n$ points lists exactly $k$ others (for $k \le n - 1$), so $\sum_x N_k(x) = nk$ and the mean of $N_k$ is exactly $k$, for every data set and every dimension. Hubness is therefore a property of the shape of the distribution, not of its mean.

**Measure.** The usual measure is the skewness

$$S_{N_k} = \frac{\frac1n \sum_x (N_k(x) - k)^3}{\Big(\frac1n \sum_x (N_k(x) - k)^2\Big)^{3/2}}.$$

A value near 0 means a symmetric distribution; a large positive value means a long right tail of hubs. Other measures count the anti-hubs, the points with $N_k(x) = 0$, or the share of all list entries taken by the most frequent points.

**Why it happens.** Radovanović, Nanopoulos and Ivanović explain hubness by the concentration of distances. In high dimension the distances from a point to the others have a mean that grows with the dimension and a spread that stays about constant, so the relative differences shrink. A point closer to the data mean has a slightly smaller expected distance to every other point, and with concentrated distances this small shift is enough to place it in many lists. They found that the skewness depends on the intrinsic dimension of the data, not on the number of coordinates, and that hubs are points with small distance to the data mean or to the center of their cluster.

## Examples

**A small exact case.** The six points $0, 1, 3, 6, 10, 11$ on a line with $k = 1$ have nearest neighbors $1, 0, 1, 2, 5, 4$ (the tie for 3 goes to the smaller index), so

$$N_1(0) = 1,\ N_1(1) = 2,\ N_1(3) = 1,\ N_1(6) = 0,\ N_1(10) = 1,\ N_1(11) = 1,$$

with sum 6 and mean 1. Point 6 is an anti-hub: it is not the nearest neighbor of any point.

**Uniform random points.** For $n = 500$ points drawn uniformly from $[0, 1]^d$ with the Euclidean distance and $k = 10$ (one random sample with a fixed seed):

| $d$ | skewness $S_{N_{10}}$ | largest $N_{10}$ | points with $N_{10} = 0$ | correlation of $N_{10}$ with the distance to the center |
|---|---|---|---|---|
| 2 | −0.06 | 18 | 0 | −0.08 |
| 10 | 0.93 | 37 | 0 | −0.88 |
| 50 | 2.13 | 64 | 11 | −0.85 |
| 100 | 2.86 | 90 | 29 | −0.85 |

In two dimensions the distribution is symmetric around 10. From $d = 10$ on, it is skewed: at $d = 100$ one point is in 90 lists, 9 times the mean, and 29 points are in none. The strong negative correlation shows that the hubs are the points near the center $(0.5, \dots, 0.5)$.

**Data on a low-dimensional surface.** Points on a curve or a plane embedded in $\mathbb{R}^{100}$ show the low skewness of their intrinsic dimension, not of 100: hubness follows the intrinsic dimension.

## Where it is used

- **Nearest neighbor classification.** A hub with a wrong label spreads its error to every point that lists it. Weighting votes by how often a point is a "good" or "bad" neighbor, or reducing hubness first, improves $k$-NN classifiers in high dimension.
- **Retrieval and recommendation.** Hub items are returned for many unrelated queries, and anti-hub items are never returned. Rescaling the distances, as in the next item, is the usual fix.
- **Hubness reduction.** Local scaling divides $\delta(x, y)$ by a function of the distances from $x$ and $y$ to their own $k$-th neighbors; mutual proximity replaces $\delta(x, y)$ by the probability that $y$ is closer to $x$ than a random point is, and that $x$ is closer to $y$, which makes the neighbor relation more symmetric. Schnitzer, Flexer, Schedl and Widmer showed that both reduce hubness.
- **Graph indexes.** In the graphs of [HNSW](/hnsw/) and similar indexes, hubs have high in-degree, so searches pass through them often and they are good entry points; anti-hubs have few incoming edges and are hard to reach, which lowers recall for queries whose answer is an anti-hub. Index builders add reverse edges to keep such points reachable.
- **Clustering and embedding.** Methods that start from a [k-nearest neighbor graph](/k-nearest-neighbor-graph-construction/), such as [t-SNE](/t-sne/) and [UMAP](/umap/), inherit its skewed degrees; symmetrization of the graph partly compensates.
- **Diagnosing data.** The skewness of $N_k$ is a cheap test of whether distance-based methods will behave well on a data set, and a rough indicator of its intrinsic dimension.

## References
