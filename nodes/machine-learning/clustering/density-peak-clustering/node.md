---
tag: E4EF5R
kind: algorithm
slug: density-peak-clustering
name: Density peak clustering
aliases:
- clustering by fast search and find of density peaks
- DPC
area: machine-learning/clustering
level: advanced
summary: "Rank points by local density, give each its distance delta to the nearest denser point, take dense points with large delta as centers, and assign the rest in density order."
solves: [density-based-clustering-problem]
model: real-ram
complexity:
  vars: {n: the number of points, d: the number of features}
  time: {worst: "Θ(n^2 d)", best: "Θ(n^2 d)"}
  space: {extra: Θ(n)}
properties: {deterministic: true, online: false, exact: true, recursive: false}
history:
  year: 2014
  people: [Alex Rodriguez, Alessandro Laio]
  note: Rodriguez and Laio published the method in Science in 2014.
prereqs: [density-based-clustering-problem, nearest-neighbor-search]
see_also: [mean-shift, dbscan, hdbscan, denclue, k-means, affinity-propagation, single-linkage-clustering, minimum-spanning-tree]
sources:
  - paper: doi:10.1126/science.1242072
    title: "Alex Rodriguez and Alessandro Laio, Clustering by fast search and find of density peaks, Science 344(6191), 2014"
    locator: the definitions of the local density and of delta, the decision graph, the assignment of the remaining points, the cluster halo, and the choice of the cutoff distance
---

Density peak clustering is a method for [density-based clustering](/density-based-clustering-problem/) that rests on one observation: a cluster center is a point that is denser than its neighbors and far from any denser point. For each point it computes a local density $\rho$ and the distance $\delta$ to its nearest point of higher density. The user picks the centers on a plot of $\delta$ against $\rho$, the *decision graph*, where they stand out at the top right. Every other point then joins the cluster of its nearest denser point, in one pass in order of decreasing density. With all distances computed directly, it takes $\Theta(n^2 d)$ time in the [real RAM](/real-ram/) model.

## In plain words

For each point, count its close neighbors. That count is how crowded the point is.

Then, for each point, find the nearest point that is more crowded than it. Write down how far away it is.

The center of a group is crowded, and the nearest more crowded point is far away, in another group. An ordinary point in a group has a more crowded point right next to it. So the centers are easy to see: plot crowd count against that distance, and the centers are the few points that are high on both.

Each other point then follows the arrow to its nearest more crowded point. Following the arrows always ends at a center, and the point joins that center's group.

## The problem

The data model is clustering of points with a distance $d(i, j)$, for example the [Euclidean distance](/euclidean-distance/) in $\mathbb{R}^d$. The input is the $n$ points and a cutoff distance $d_c > 0$. Rodriguez and Laio (2014) define:

- The **local density** with the cutoff kernel, $\rho_i = |\{j \ne i : d(i, j) < d_c\}|$, or with the Gaussian kernel, $\rho_i = \sum_{j \ne i} \exp(-(d(i, j)/d_c)^2)$.
- The **distance to higher density**, $\delta_i = \min_{j : \rho_j > \rho_i} d(i, j)$. For the point of highest density, $\delta_i = \max_j d(i, j)$.
- The **decision graph** is the plot of the points $(\rho_i, \delta_i)$. Centers have a large $\rho$ and an anomalously large $\delta$. Points with a large $\delta$ and a small $\rho$ are outliers: isolated points far from anything.
- A **cluster** is the set of points whose chain of nearest denser points first reaches a given center.

The number of clusters is the number of centers chosen. It is not an input of the computation of $\rho$ and $\delta$.

**Tie rule.** The paper does not say what happens when two points have the same density, which is common with the cutoff kernel, since its values are integers. Here the points are ranked by $\rho$ from high to low, and equal $\rho$ by index from low to high, and "higher density" means "earlier in this ranking". Then every point except the first has a nearest denser point, and the first point is always a center. Among denser points at the same distance, the earliest in the ranking is the nearest one.

## The algorithm

```pseudo id=main
DENSITY-PEAKS(D, d_c, centers rule)
L1  ρ_i ← |{j ≠ i : d(i, j) < d_c}| for each point i
L2  q_1, ..., q_n ← the points sorted by ρ descending, ties by index ascending
L3  δ(q_1) ← max over j of d(q_1, j); nn(q_1) ← none
L4  for r ← 2 to n do
L5      δ(q_r) ← min over s < r of d(q_r, q_s); nn(q_r) ← the first q_s at that distance
L6  Z ← the centers chosen on the decision graph (ρ, δ), with q_1 always in Z
L7  for r ← 1 to n do
L8      if q_r ∈ Z then label(q_r) ← a new cluster
L9      else label(q_r) ← label(nn(q_r))
    ▷ optional halo
L10 ρ_b(c) ← the largest ρ_i over points i of c within d_c of a point of another cluster
L11 halo(i) ← ρ_i ≤ ρ_b(label(i))
L12 return label, halo
```

Line L6 is where the user acts. The paper picks the centers by eye on the decision graph. Two automatic rules are common: all points with $\rho > \rho_{\min}$ and $\delta > \delta_{\min}$, or the $k$ points with the largest $\gamma_i = \rho_i \delta_i$, a rule the paper also suggests. Line L9 always finds a label, because $\mathrm{nn}(q_r)$ comes earlier in the order and was labeled in an earlier pass of the loop.

## Example

Take the points 0, 1, 2, 3, 4, 10, 11, 12 and 20 on the line, with $d_c = 1.5$ and the cutoff kernel.

| point | 0 | 1 | 2 | 3 | 4 | 10 | 11 | 12 | 20 |
|---|---|---|---|---|---|---|---|---|---|
| $\rho$ | 1 | 2 | 2 | 2 | 1 | 1 | 2 | 1 | 0 |
| rank | 5 | 1 | 2 | 3 | 6 | 7 | 4 | 8 | 9 |
| nearest denser point | 1 | none | 1 | 2 | 3 | 11 | 3 | 11 | 12 |
| $\delta$ | 1 | 19 | 1 | 1 | 1 | 1 | 8 | 1 | 8 |

The points 1, 2, 3 and 11 all have $\rho = 2$, and the tie rule ranks them by index. So the point 1 is first, its $\delta$ is the distance to the farthest point, 19, and the point 2 has the point 1 as its nearest denser point, not the point 3. The point 11 is the densest point of its group, and its nearest denser point is 3, at distance 8.

On the decision graph, three points have a large $\delta$: the point 1 at $(2, 19)$, the point 11 at $(2, 8)$ and the point 20 at $(0, 8)$. The point 20 has density 0, so it is an outlier, not a center. With $\rho_{\min} = 0.5$ and $\delta_{\min} = 4$, the centers are 1 and 11. The pass in rank order labels 1 as cluster 0, then 2 and 3 through their arrows, then 11 as cluster 1, then the rest. The result is {0, 1, 2, 3, 4} and {10, 11, 12, 20}. The point 20 joins the second cluster through the point 12, because the method gives every point a cluster; the halo is the way to mark such points.

The rule "$k = 3$ largest $\gamma$" shows a weak point. The values of $\gamma$ are 38 for the point 1, 16 for the point 11, and 2 for the points 2 and 3. The tie rule picks the point 2, and the first group splits into {0, 1} and {2, 3, 4}.

## Correctness

The claim is that the labels are the clusters of the definition: each point gets the label of the first center on its chain of nearest denser points, and these clusters partition the data. Line L5 scans exactly the points before $q_r$ in the ranking, which are the denser points, so $\delta$ and the nearest denser point match the definition. Each arrow goes to an earlier point in the ranking, so following arrows from any point ends, and it can end only at a center, since the first point is a center and every other point has an arrow. The pass of lines L7 to L9 visits each point after the point its arrow leads to, so by induction it copies the label of the first center on the chain. The full proof is below.

## Complexity

The model is the [real RAM](/real-ram/). Here $n$ is the number of points and $d$ the number of features.

- **Densities.** Line L1 needs all pairs of distances, $\Theta(n^2 d)$ time. A [fixed-radius near neighbor](/fixed-radius-near-neighbors/) structure makes it faster when the neighborhoods are small, in low dimension.
- **Delta.** Lines L4 and L5 compare each point with all denser points, $\Theta(n^2 d)$ in total. The sort of line L2 is $O(n \log n)$.
- **Assignment.** Lines L7 to L9 are one pass, $\Theta(n)$.
- **Space.** Computing distances again when needed keeps the extra space at $\Theta(n)$. Many implementations store the distance matrix, which costs $\Theta(n^2)$.

## Properties

- **Deterministic and exact.** With a fixed tie rule and a fixed choice of centers, the output is a function of the input. Nothing is iterated or approximated.
- **Not order independent under ties.** With the cutoff kernel, ties in $\rho$ are common, and the tie rule decides who is denser, which can move points between clusters. With the Gaussian kernel, ties are rare and the partition does not depend on the input order.
- **Non-convex clusters.** Arrows follow the data, so a cluster can be curved, as long as each part of it has a denser neighbor nearby.
- **Every point gets a cluster.** Noise is not left out unless the halo is used.
- **A tree.** The arrows form a spanning tree of the data rooted at the densest point. Removing the arrows out of the centers splits it into the clusters.
- **Link to mean shift.** Following the nearest denser point is a discrete form of climbing the density, as in [mean shift](/mean-shift/). The point reached is a data point, and no iteration is needed.

## Variants and improvements

- **Gaussian density.** The smooth kernel avoids ties, and it gives a less noisy $\rho$ when there are few points.
- **Choosing $d_c$.** The paper suggests choosing $d_c$ so that the average number of neighbors is about 1 to 2 percent of the number of points.
- **k-nearest neighbor densities.** Later variants define $\rho$ from the distances to the $k$ nearest neighbors, which adapts to clusters of different densities.
- **Automatic center selection.** Rules on $\gamma = \rho \delta$, or a fit of the tail of the $\gamma$ values, replace the choice by eye.
- **Faster delta.** For large data, $\delta$ can be computed with a spatial index, or approximately with grids or locality sensitive hashing.

## When to use it

Use density peak clustering when the clusters have clear density peaks, the shapes may be non-convex, and you want to see the structure on a two dimensional plot before you choose the number of clusters. It is quick to implement and has one pass of assignment. Avoid it when a cluster has several peaks of similar height, since each can become a center, or when the data are too large for quadratic time without an index.

## Pitfalls

- **Ties in the cutoff density.** Without a stated tie rule, two implementations give different results on the same data. State the rule, or use the Gaussian kernel.
- **The densest point is a center.** It has no denser point, so it must be a center. A rule that does not include it leaves its chain without an end.
- **Ranking by $\gamma$ alone.** Large $\gamma$ can come from a dense point with a small $\delta$, as in the example. Look at the decision graph.
- **Outliers.** A point with a large $\delta$ and a small $\rho$ is an outlier, not a center. Use a lower bound on $\rho$.
- **One error spreads.** If one point gets a wrong label, all points whose chains pass through it get the same wrong label.
- **The halo is not noise removal.** It marks the low density part of each cluster near the others. Isolated outliers far from other clusters are not in any border region and stay in the core.

## Implementations

## History

Alex Rodriguez and Alessandro Laio, at SISSA in Trieste, published the method in Science in 2014. They showed it on synthetic point sets with clusters of many shapes and on a set of face images. The paper was widely cited and led to many variants with other densities, automatic center choice and faster computation of $\delta$.

## References
