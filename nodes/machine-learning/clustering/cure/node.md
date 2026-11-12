---
tag: C6AZ80
kind: algorithm
slug: cure
name: CURE
aliases:
- clustering using representatives
- CURE clustering
area: machine-learning/clustering
level: advanced
summary: "Agglomerative clustering in which each cluster keeps c scattered points shrunk toward its mean, and the closest pair of clusters by these points merges; sampling makes it scale."
solves: [hierarchical-clustering-problem]
model: real-ram
complexity:
  vars: {n: the number of points that are clustered, k: the number of clusters, c: the number of representatives of a cluster, d: the number of features}
  time: {worst: "O(n^2 (log n + c^2 d))", best: "Θ(n^2 d)"}
  space: {extra: "Θ(n^2)"}
properties: {deterministic: true, online: false, exact: false, recursive: false}
history:
  year: 1998
  people: [Sudipto Guha, Rajeev Rastogi, Kyuseok Shim]
  note: Guha, Rastogi and Shim presented CURE at ACM SIGMOD 1998, as a hierarchical method for large databases that finds clusters of non-spherical shapes and is robust to outliers.
prereqs: [agglomerative-clustering, linkage-criterion, priority-queue]
see_also: [single-linkage-clustering, birch, k-means, dbscan, random-sampling, kd-tree, gonzalez-k-center, chernoff-bound]
sources:
  - paper: doi:10.1145/276304.276312
    title: "Sudipto Guha, Rajeev Rastogi and Kyuseok Shim, CURE: an efficient clustering algorithm for large databases, Proceedings of the 1998 ACM SIGMOD International Conference on Management of Data"
    locator: the scattered and shrunk representatives, the merge procedure with a heap and a k-d tree and its O(n^2 log n) bound, the Chernoff bound on the sample size, partitioning, the elimination of outliers, and the labeling of the data
---

CURE (Clustering Using REpresentatives) is a method of [agglomerative clustering](/agglomerative-clustering/) for large data sets. Each cluster keeps a fixed number $c$ of *well scattered* points of the cluster, moved toward the cluster mean by a fraction $\alpha$. The distance between two clusters is the smallest distance between their representatives, and CURE always merges the closest pair. The scattered points follow the shape of a cluster, so CURE finds long and non-spherical clusters that methods with one center miss. The shrinking pulls far points inward, so a few outliers do not join clusters. To handle large data, CURE clusters a [random sample](/random-sampling/), first in partitions, removes slowly growing clusters as outliers, and then gives each point the cluster of its nearest representative. It is a heuristic: it optimizes no stated objective.

## In plain words

Start with each point as its own group, and join the two closest groups again and again until the number of groups you want is left.

To measure how close two groups are, each group picks a few of its own points that lie far apart from each other, near its edges. These points are then pulled a little toward the middle of the group. Two groups are as close as their two nearest picked points.

Many picked points trace the shape of a group, so long or curved groups stay whole. The pull toward the middle keeps a lonely point at the edge from reaching out to another group.

For a large data set, you do all this on a random part of the data. At the end, each point joins the group whose picked point is nearest to it.

## The problem

CURE solves the [hierarchical clustering problem](/hierarchical-clustering-problem/) with a [linkage criterion](/linkage-criterion/) of its own. The input is $n$ points in $\mathbb{R}^d$ with the [Euclidean distance](/euclidean-distance/), a number of clusters $k$, a number of representatives $c \ge 1$ and a shrink factor $0 \le \alpha \le 1$. For a cluster $w$ with mean $\mu(w)$, the representatives are found in two steps:

1. Pick $\min(c, |w|)$ scattered points of $w$: first the point farthest from $\mu(w)$, then each time the point whose distance to the nearest point already picked is largest. This is the farthest point rule of [Gonzalez](/gonzalez-k-center/).
2. Move each picked point $p$ to $p + \alpha (\mu(w) - p)$.

Let $R(w)$ be the result. The distance between two clusters is

$$D(u, v) = \min_{a \in R(u),\, b \in R(v)} \lVert a - b \rVert.$$

With $\alpha = 0$ and $c$ at least the cluster sizes, $D$ is the distance of [single linkage](/single-linkage-clustering/). With $\alpha = 1$, every representative is the mean, and $D$ is the distance of centroid linkage. CURE lies between the two.

## The algorithm

```pseudo id=main
CURE(S, k, c, α)
L1  make a cluster {x} for each point x of S, with R({x}) = {x}
L2  put each pair of clusters (u, v) in a min heap with the key D(u, v)
L3  while more than k clusters are alive do
L4      pop the pair (u, v) with the smallest key; skip it if u or v is no longer alive
L5      w ← MERGE(u, v, c, α); u and v are no longer alive
L6      for each live cluster x: push (x, w) with the key D(x, w); w is alive
L7  return the live clusters

MERGE(u, v, c, α)
L8  w ← u ∪ v
L9  μ ← the mean of w
L10 P ← c points of w by the farthest point rule, starting at the point farthest from μ
L11 R(w) ← { p + α (μ − p) : p ∈ P }
L12 return w

LARGE-CURE(D, k, c, α, s, p, q)
L13 S ← a uniform random sample of s points of D
L14 split S into p parts; run lines L1 to L7 on each part until it has |part| / q clusters
L15 during the next run, when the number of clusters first falls below a threshold,
        remove the clusters with very few points as outliers
L16 run lines L2 to L7 on all partial clusters until k remain
L17 give each point of D the cluster of its nearest representative
```

**The heap.** A cluster never changes after it is made, so a key once computed stays correct. A pair whose cluster has merged is not removed from the heap: line L4 skips it when it comes to the top. This is lazy deletion. The paper uses a different structure: a heap of clusters keyed by the distance to the closest other cluster, and a [k-d tree](/kd-tree/) of all representatives to find the closest cluster of a new cluster. It uses less memory but needs more work to update the closest cluster of the others.

**Ties.** Equal keys go to the pair with the smaller cluster numbers, and the farthest point rule takes the earlier point in the list.

**Sampling and partitions.** Line L13 makes CURE independent of the size of $D$, apart from line L17. With $p$ parts, line L14 reduces each part of $s / p$ points to $s / (p q)$ clusters, so the expensive quadratic step runs on smaller inputs. Line L15 uses the observation of the paper that outliers grow slowly, since they are far from all other points. They stay in very small clusters while real clusters grow, so the paper removes such clusters at a point in the merging, and again near the end.

## Example

Take the seven points $(0,0), (1,0), (2,0), (3,0), (4,0)$, a horizontal bar, then $(7,0)$ to its right and $(2, 4.5)$ above its middle. Let $k = 2$, $c = 2$ and $\alpha = 0.5$.

The bar points are 1 apart, and the two other points are at least 3 from every point. So the first four merges build the bar. The bar has the mean $(2,0)$. Its farthest point from the mean is $(0,0)$, the first in the list among the two at distance 2, and the point farthest from $(0,0)$ is $(4,0)$. Shrinking them halfway to the mean gives the representatives $(1,0)$ and $(3,0)$.

Now three clusters are left:

| pair | CURE distance | centroid distance |
|---|---|---|
| bar and $(7,0)$ | $\lVert (3,0) - (7,0) \rVert = 4.00$ | $5.00$ |
| bar and $(2, 4.5)$ | $\lVert (1,0) - (2,4.5) \rVert = 4.61$ | $4.50$ |
| $(7,0)$ and $(2,4.5)$ | $6.73$ | $6.73$ |

CURE merges the bar with $(7,0)$, which continues the bar, and the result is $\{(0,0), \ldots, (4,0), (7,0)\}$ and $\{(2,4.5)\}$. With $\alpha = 1$ the representatives are the mean, which is centroid linkage, and the bar merges with the point above it instead, because the mean of a long bar is far from its ends. With $\alpha = 0$ CURE also joins $(7,0)$, at the distance 3.

## Correctness

CURE is a heuristic, so the claim is that it carries out the stated merge rule. A cluster never changes after it is made, so each key in the heap is the correct distance of its pair. At the start of each pass, every pair of live clusters is in the heap: line L2 puts in all first pairs, and line L6 puts in all pairs with the new cluster. The entries of merged clusters are skipped. So the first live pair that line L4 pops is a closest pair of live clusters under $D$, and each pass lowers the number of clusters by one until $k$ remain. With $\alpha = 0$ and $c \ge n$ the representatives are all points of a cluster, and CURE is single linkage. With $\alpha = 1$ it is centroid linkage. The paper also uses a Chernoff bound to choose a sample size that keeps a given fraction of each cluster with high probability. The full proof is below.

## Complexity

The model is the [real RAM](/real-ram/). Here $n$ is the number of points that are clustered, the sample size for LARGE-CURE.

- **Start.** Lines L1 and L2 compute $n(n-1)/2$ distances and build a heap of them in $\Theta(n^2 d)$ time.
- **Merges.** There are $n - k$ merges. A merge computes the mean and the scattered points of $w$ in $O(|w| c d)$ time, and the distance from $w$ to each live cluster in $O(c^2 d)$ time each. Each push and pop costs $O(\log n)$, and there are $O(n^2)$ of them. The total is $O(n^2 (\log n + c^2 d))$ time.
- **Space.** The heap of pairs holds $\Theta(n^2)$ entries. The heap of clusters and the k-d tree of the paper need $O(n c d)$ space. For that structure the paper states $O(n^2 \log n)$ worst case time, and $O(n^2)$ time when the dimension is low.
- **Large data.** With $p$ partitions, the first pass costs about $p \cdot (s/p)^2 = s^2 / p$ instead of $s^2$, up to the log and $c^2 d$ factors. Line L17 costs $O(|D| k c d)$ time and reads the data once.

## Properties

- **Not exact.** CURE optimizes no objective and has no guarantee of quality. The result depends on $c$, $\alpha$, the sample and the outlier rule.
- **Deterministic.** The plain algorithm with fixed tie rules is deterministic. LARGE-CURE is randomized through the sample.
- **Between two linkages.** It has single linkage and centroid linkage as limits. Single linkage follows shapes but chains through outliers, and centroid linkage resists outliers but prefers round clusters.
- **Shapes.** It finds clusters of non-spherical shape and of different sizes. It traces a shape only as well as $c$ shrunk points can, so it needs $c$ large enough.
- **Outliers.** The shrinking and the removal of small clusters make it robust to a moderate number of outliers.

## Variants and improvements

- **ROCK.** Guha, Rastogi and Shim gave ROCK in 1999 for categorical data. It merges clusters by the number of common neighbors (links) instead of distances.
- **CHAMELEON.** Karypis, Han and Kumar (1999) merge clusters of a sparse nearest neighbor graph by their relative connectivity and closeness, to adapt to clusters of different densities.
- **BIRCH.** [BIRCH](/birch/) also scales to large data, but with a tree of summaries of one center each, so it prefers round clusters.
- **Fewer representatives at labeling.** The labeling of line L17 can use a random subset of the representatives of each cluster, to save time on large data.

## When to use it

Use CURE when the clusters are elongated or of very different sizes, when the data set is large but a random sample shows its structure, and when the data contain some outliers. Use [k-means](/k-means/) for round clusters of similar size. Use [DBSCAN](/dbscan/) or a density method when the clusters have arbitrary, for example curved or nested, shapes, or when the number of clusters is not known.

## Pitfalls

- **Small clusters and the sample.** A small cluster may have few points in the sample, and then the outlier rule can remove it. The sample size must grow like $n / |u|$ for the smallest cluster $u$ that must be found.
- **The shrink factor.** A small $\alpha$ acts like single linkage and chains through outliers. A large $\alpha$ acts like centroid linkage and cuts long clusters.
- **Too few representatives.** A small $c$ cannot trace a long or curved cluster.
- **Partitions.** Too much partial clustering, a large $q$, can merge points of different clusters before they are seen together.
- **Memory.** The heap of all pairs needs quadratic memory. For many points, use the closest cluster heap of the paper or a smaller sample.
- **Scaling.** The Euclidean distance needs features on comparable scales.

## Implementations

## History

Sudipto Guha, Rajeev Rastogi and Kyuseok Shim presented CURE at ACM SIGMOD in 1998. At the time, most clustering methods for large databases, such as BIRCH, kept one center for each cluster and so preferred round clusters of similar size, while single linkage was too sensitive to outliers. CURE took a middle way with several shrunk representatives, and used random sampling, with a Chernoff bound on the sample size, and partitioning to make hierarchical clustering scale. A journal version appeared in Information Systems in 2001. The same authors gave ROCK for categorical data in 1999.

## References
