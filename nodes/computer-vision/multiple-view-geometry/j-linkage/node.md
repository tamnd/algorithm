---
tag: ZDYX7K
kind: algorithm
slug: j-linkage
name: J-linkage
aliases:
- multi-model fitting by J-linkage
area: computer-vision/multiple-view-geometry
level: research
summary: "Fit several models at once: describe each point by the set of random hypotheses it supports, then cluster the points agglomeratively by the Jaccard distance."
solves: [robust-model-fitting]
model: real-ram
complexity:
  vars: {n: the number of data points, M: the number of random hypotheses}
  time: {worst: Θ(n^3 M), average: O(n^3 M), best: Θ(n^2 M)}
  space: {extra: Θ(n M)}
properties: {deterministic: false, exact: false, online: false, recursive: false}
history:
  year: 2008
  people: [Roberto Toldo, Andrea Fusiello]
  note: "Toldo and Fusiello presented J-linkage at ECCV 2008 as a way to fit an unknown number of models, such as lines, planes or homographies, without a first guess of how many there are."
prereqs: [ransac, agglomerative-clustering, jaccard-similarity]
see_also: [ransac, hough-transform, efficient-ransac-shape-detection, robust-model-fitting, agglomerative-clustering, jaccard-similarity, homography-estimation, line-detection]
sources:
  - paper: doi:10.1007/978-3-540-88682-2_41
    title: "Roberto Toldo and Andrea Fusiello, Robust multiple structures estimation with J-linkage, European Conference on Computer Vision (ECCV 2008), Lecture Notes in Computer Science 5302, 537-547"
    locator: "The sections on random sampling with locality, the preference set of a point, the Jaccard distance and the J-linkage clustering, and the experiments on lines, planes and homographies"
  - book: isbn:9783030343712
    title: "Richard Szeliski, Computer Vision: Algorithms and Applications, second edition, Springer, 2022"
    locator: "Chapter 8, the discussion of robust fitting and of fitting more than one model"
---

J-linkage is a method to fit several models to the same data at once, for example several lines in a set of points, several planes in a 3D scan or several homographies between two images of a scene with many flat parts. [RANSAC](/ransac/) finds one model, and running it again on the points that remain often fails, because the outliers of one model are the inliers of another. J-linkage does not look for the models one by one. It draws many random hypotheses, as RANSAC does, and then describes each point by its preference set, the set of hypotheses that pass close to it. Points on the same structure prefer the same hypotheses. The method then puts the points in clusters by [agglomerative clustering](/agglomerative-clustering/) with the Jaccard distance between preference sets, and fits one model to each large cluster. Toldo and Fusiello introduced it in 2008. The number of models is an output, not an input.

## In plain words

Imagine many random guesses of a line. Each point writes down the list of guesses that pass near it. Two points on the same true line have similar lists, because a guess near that line passes near both of them. A point that is noise has a short list that looks like no other list.

Now join points step by step. At each step, join the two groups whose lists are most alike. A group keeps only the guesses that every member has on its list. Stop when no two groups share a guess. Each big group is one structure, and a line fitted to it is one answer. Small groups are noise.

## The problem

The input is a set of points $D = \{x_1, \ldots, x_n\}$ that lie near an unknown number of models of one type, plus outliers. There is a minimal solver for samples of $s$ points, a residual $r(h, x)$, an inlier threshold $\varepsilon$, a number of hypotheses $M$, a locality scale $\sigma$ and a least cluster size $m_{\min}$. The output is a list of models, each with the points it explains. This is the multi-model form of [robust model fitting](/robust-model-fitting/). The code fits lines in the plane, with $s = 2$.

## The algorithm

```pseudo id=main
J-LINKAGE(D, M, ε, σ, m_min)                 ▷ n = |D|
L1  for j = 1, …, M do
L2      S ← one uniform point x_i, then s − 1 other points, each x with weight exp(−‖x − x_i‖²/σ²)
L3      h_j ← FIT-MINIMAL(S)
L4  P(x) ← {h_j : r(h_j, x) < ε} for each x in D          ▷ preference sets
L5  C ← {{x} : x ∈ D}, with P({x}) = P(x)
L6  loop
L7      (A, B) ← a pair of clusters in C of least d_J(P(A), P(B))
L8      if C has fewer than 2 clusters or d_J(P(A), P(B)) = 1 then exit the loop
L9      replace A and B in C by A ∪ B, with P(A ∪ B) = P(A) ∩ P(B)
L10 for each cluster A in C with |A| ≥ m_min do
L11     fit a model to A by least squares and output it with A
L12 return the models and the clusters
```

Here $d_J(P, Q) = (|P \cup Q| - |P \cap Q|)/|P \cup Q|$ is the Jaccard distance, one minus the [Jaccard similarity](/jaccard-similarity/). It is 1 exactly when the two sets have no hypothesis in common. Line L2 is the locality sampling of the paper: points of one structure are often near each other, so samples of nearby points are more likely to come from one structure. Line L9 keeps the hypotheses that all points of the new cluster prefer. The code stores each preference set as a bit mask of $M$ bits, so the union and the intersection are bit operations. It breaks ties at line L7 by the order of the clusters.

## Example

Take the 8 points $x_0 = (0,0)$, $x_1 = (1,0)$, $x_2 = (2,0)$, $x_3 = (3,0)$ on the line $y = 0$, $x_4 = (4,1)$, $x_5 = (4,2)$, $x_6 = (4,3)$ on the line $x = 4$, and the outlier $x_7 = (1,3)$. Take the 8 hypotheses through the pairs $(x_0, x_1)$, $(x_1, x_7)$, $(x_4, x_5)$, $(x_2, x_4)$, $(x_3, x_6)$, $(x_2, x_3)$, $(x_5, x_6)$ and $(x_0, x_7)$, called $h_1$ to $h_8$, and $\varepsilon = 0.1$. The preference sets are:

| point | $x_0$ | $x_1$ | $x_2$ | $x_3$ | $x_4$ | $x_5$ | $x_6$ | $x_7$ |
|---|---|---|---|---|---|---|---|---|
| $P$ | 1, 6, 8 | 1, 2, 6 | 1, 4, 6 | 1, 5, 6 | 3, 4, 7 | 3, 7 | 3, 5, 7 | 2, 8 |

The hypotheses $h_1$ and $h_6$ are both the line $y = 0$, and $h_3$ and $h_7$ are both $x = 4$. The merges are:

| step | merge | $d_J$ | new preference set |
|---|---|---|---|
| 1 | $\{x_4\}$ and $\{x_5\}$ | 1/3 | 3, 7 |
| 2 | $\{x_4, x_5\}$ and $\{x_6\}$ | 1/3 | 3, 7 |
| 3 | $\{x_0\}$ and $\{x_1\}$ | 1/2 | 1, 6 |
| 4 | $\{x_0, x_1\}$ and $\{x_2\}$ | 1/3 | 1, 6 |
| 5 | $\{x_0, x_1, x_2\}$ and $\{x_3\}$ | 1/3 | 1, 6 |

After step 5 the clusters have the preference sets $\{1, 6\}$, $\{3, 7\}$ and $\{2, 8\}$, which share no hypothesis, so every distance is 1 and the loop stops. With $m_{\min} = 3$, the method outputs the lines $y = 0$ and $x = 4$ and leaves $x_7$ as an outlier. The number of lines, 2, was not an input.

## Correctness

The clustering has four properties for any set of hypotheses (proofs below). The clusters form a partition of the points. The preference set of a cluster is the intersection of the preference sets of its points. Every cluster of two or more points has a hypothesis that all its points prefer, because two clusters merge only when their distance is below 1, which means that their sets meet. At the end, no two clusters share a hypothesis. The loop ends after at most $n - 1$ merges. Whether the clusters are the true structures depends on the hypotheses: a structure is found only if some hypotheses fit it, which the random sampling gives with high probability when $M$ is large enough. This last part is an empirical result.

## Complexity

Line L2 costs $O(s\,n)$ for the locality weights, so lines L1 to L3 cost $O(M n)$ for a fixed $s$. Line L4 computes $n M$ residuals, $\Theta(n M)$. The simple clustering of the code compares all pairs of clusters at each step, $O(n^2)$ pairs with $O(M)$ bit work each, and makes at most $n - 1$ merges, so it costs $O(n^3 M)$ in the worst case. If no pair merges, one pass of $\Theta(n^2 M)$ is enough. The extra space is $\Theta(n M)$ bits for the preference sets. A priority queue of pair distances lowers the time of the clustering, as for other forms of agglomerative clustering.

## Properties

- **The number of models is an output.** It is the number of clusters with at least $m_{\min}$ points.
- **Robust to outliers.** An outlier prefers few hypotheses, and these hypotheses are rarely shared by a structure, so it ends in a small cluster.
- **Randomized.** The hypotheses are random. The clustering itself is deterministic for a given set of hypotheses.
- **Two thresholds.** The method needs $\varepsilon$ and $m_{\min}$, but no number of models.

## Variants and improvements

- **T-linkage** (Magri and Fusiello, 2014) replaces the binary preference set by a vector of soft preferences in $[0, 1]$ and the Jaccard distance by the Tanimoto distance.
- **Sequential RANSAC** runs [RANSAC](/ransac/) again and again and removes the inliers of each model found. It is simpler but can fail when structures cross.
- **[Hough transform](/hough-transform/)** votes in a grid of model parameters and finds several models as peaks. It suits models with few parameters.
- **[Efficient RANSAC for shape detection](/efficient-ransac-shape-detection/)** finds several primitive shapes in point clouds with a RANSAC loop and local sampling.

## When to use it

Use J-linkage when the data contain several structures of the same model type and their number is not known, for example several planes in a scan of a building, several moving objects in two views or several lines in an image. Use it when the structures may cross or touch, where sequential RANSAC tends to fail. For one model, [RANSAC](/ransac/) and its variants are faster. For very large $n$, the cubic clustering of a simple implementation is slow, so use a priority queue or subsample the points.

## Pitfalls

- **Too few hypotheses.** A structure with no good hypothesis among the $M$ samples is lost. Raise $M$ for small structures or many outliers.
- **The locality scale $\sigma$.** If $\sigma$ is too small, samples come from tiny neighborhoods and give poor hypotheses. If it is too large, the sampling is uniform and most samples mix structures.
- **The threshold $\varepsilon$.** As in RANSAC, a too small $\varepsilon$ splits a structure into pieces, and a too large one merges close structures.
- **Points at crossings.** A point near two structures prefers the hypotheses of both, and it joins only one of the clusters.

## Implementations

The Python code fits lines in the plane. The function `locality_sample` draws the samples of line L2, `preference_sets` gives the bit masks of line L4 and `cluster` is the loop of lines L5 to L9, with an optional callback for each merge. The tests check the example, the invariants of the proof on random data and the recovery of two crossing lines with outliers.

## History

Toldo and Fusiello presented J-linkage at ECCV 2008. They combined three ideas: the random hypotheses of [RANSAC](/ransac/) (Fischler and Bolles, 1981), the description of a point by the models it agrees with, and agglomerative clustering with the Jaccard distance. Earlier methods for several models, such as sequential RANSAC and the [Hough transform](/hough-transform/), needed the number of models, a grid of parameters or a step that removes the points of each model found. Later methods, such as T-linkage, built on the idea of preference sets.

## References
