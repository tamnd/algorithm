---
tag: 4X06MR
kind: algorithm
slug: multidimensional-scaling
name: Multidimensional scaling
aliases:
- MDS
- nonmetric multidimensional scaling
- Kruskal's nonmetric MDS
area: machine-learning/dimensionality-reduction
level: core
summary: "Place n points in a low dimension so that their distances fit given dissimilarities: in value (metric MDS) or only in rank order (Kruskal's nonmetric MDS)."
model: real-ram
complexity:
  vars: {n: the number of objects, k: the output dimension, t: the number of iterations}
  time: {worst: "O(t n^2 (k + log n))"}
  space: {extra: "O(n^2)"}
properties: {deterministic: true, exact: false, online: false, recursive: false}
history:
  year: 1964
  people: [Roger N. Shepard, Joseph B. Kruskal]
  note: Shepard (1962) fitted distances to the rank order of proximities. Kruskal (1964) defined the stress, used isotonic regression for the disparities and minimized the stress by steepest descent.
prereqs: [metric-space, gradient-descent]
see_also: [classical-mds, smacof, sammon-mapping, isomap, isotonic-regression, pool-adjacent-violators, embedding, t-sne]
sources:
  - paper: doi:10.1007/BF02289565
    title: Joseph B. Kruskal, Multidimensional scaling by optimizing goodness of fit to a nonmetric hypothesis, Psychometrika 29(1), 1964, pages 1 to 27
    locator: the definition of stress (stress-1), the monotone fit by disparities, the primary and secondary approaches to ties
  - paper: doi:10.1007/BF02289694
    title: Joseph B. Kruskal, Nonmetric multidimensional scaling, a numerical method, Psychometrika 29(2), 1964, pages 115 to 129
    locator: the up-and-down blocks algorithm for the monotone regression and the steepest descent on the stress with its gradient
  - paper: doi:10.1007/BF02288916
    title: Warren S. Torgerson, Multidimensional scaling, I. Theory and method, Psychometrika 17(4), 1952, pages 401 to 419
    locator: the classical metric method
  - paper: "Jan de Leeuw, Applications of convex analysis to multidimensional scaling, in J. R. Barra et al. (editors), Recent Developments in Statistics, North-Holland, 1977, pages 133 to 145"
    locator: the majorization of the stress
  - paper: "Roger N. Shepard, The analysis of proximities, multidimensional scaling with an unknown distance function, Parts I and II, Psychometrika 27(2) and 27(3), 1962"
    locator: the first nonmetric scaling procedure
  - book: isbn:9780387251509
    title: Ingwer Borg and Patrick J. F. Groenen, Modern Multidimensional Scaling, second edition, Springer, 2005
    locator: Chapter 3 (MDS models and measures of fit), Chapter 9 (Metric and nonmetric MDS) and Chapter 11 (fit measures)
  - book: isbn:9780387848570
    title: Trevor Hastie, Robert Tibshirani and Jerome Friedman, The Elements of Statistical Learning, second edition, Springer, 2009
    locator: Section 14.8 (Multidimensional scaling, least squares and Shepard-Kruskal nonmetric scaling)
---

Multidimensional scaling (MDS) is the family of methods that place $n$ objects as points in a space of low dimension $k$, so that the distances between the points fit given dissimilarities between the objects. *Metric* MDS fits the values of the dissimilarities, usually by minimizing the raw stress. *Nonmetric* MDS, due to Kruskal (1964), fits only their rank order, through monotone *disparities* found by [isotonic regression](/isotonic-regression/). This page states the criteria and gives Kruskal's alternating method, which never increases the stress but can stop at a local minimum. [Classical MDS](/classical-mds/), [SMACOF](/smacof/) and [Sammon mapping](/sammon-mapping/) are members of the family with their own pages.

## In plain words

People rate how different some objects are: colors, sounds, cities, words. You want a map in which objects that are rated as different lie far apart and objects rated as alike lie close together. Metric scaling takes the ratings as distances and moves the points until the map distances are as close as possible to the ratings. Often the ratings are only good for their order: one pair is more different than another, but the numbers mean little. Nonmetric scaling then asks only that the map distances be in the same order as the ratings. At each step it finds the closest list of numbers in that order, and moves the points a little toward those numbers. The fit never gets worse, but the result can depend on where the points start.

## The problem

The input is a symmetric $n \times n$ matrix of dissimilarities $\Delta = (\delta_{ij})$ with $\delta_{ii} = 0$, optional weights $w_{ij} \ge 0$, and the output dimension $k$. Here $n$ is the number of objects and $k$ the output dimension. The output is a configuration $X \in \mathbb{R}^{n \times k}$ with rows $x_i$ and distances $d_{ij}(X) = \|x_i - x_j\|$. The family has three main criteria.

- **Raw stress (metric MDS).** Minimize $\sigma_r(X) = \sum_{i < j} w_{ij}\,(d_{ij}(X) - \delta_{ij})^2$. [SMACOF](/smacof/) minimizes it by majorization. [Sammon mapping](/sammon-mapping/) uses the weights $w_{ij} = 1/\delta_{ij}$ with a normalization.
- **Strain (classical MDS).** Minimize $\|B - XX^\top\|_F$, where $B$ is the double-centered matrix of the squared dissimilarities. [Classical MDS](/classical-mds/) solves it exactly by an eigendecomposition.
- **Stress-1 (nonmetric MDS).** Minimize over $X$ and over the disparities $\hat d_{ij}$

$$S(X, \hat d) = \left(\frac{\sum_{i<j} (d_{ij}(X) - \hat d_{ij})^2}{\sum_{i<j} d_{ij}(X)^2}\right)^{1/2} \quad \text{subject to } \hat d_{ij} \le \hat d_{lm} \text{ whenever } \delta_{ij} < \delta_{lm}.$$

The denominator makes $S$ invariant under a change of scale of $X$. Without it, the trivial solution $X = 0$, $\hat d = 0$ would have zero stress. The constraint uses only the order of the $\delta_{ij}$. This is Kruskal's *primary approach* to ties: tied dissimilarities put no constraint on their disparities. The *secondary approach* asks that tied dissimilarities get equal disparities.

Kruskal gave a verbal scale for stress-1 (0.2 poor, 0.1 fair, 0.05 good, 0.025 excellent, 0 perfect). These labels are rules of thumb, not a statistical test, and the expected stress of random data grows with $n$ and falls with $k$.

## The algorithm

The algorithm alternates two minimizations of $S$. For a fixed $X$ it finds the best disparities by isotonic regression. For fixed disparities it takes a gradient step on $X$.

```pseudo id=main
KRUSKAL-MDS(Δ, X, T)
L1  for t ← 1 to T do
L2      d_ij ← ‖x_i − x_j‖ for each pair i < j
L3      sort the pairs by δ_ij, and break ties by d_ij       ▷ primary approach
L4      d̂ ← the isotonic regression of the d_ij in this order   ▷ pool adjacent violators
L5      S ← (Σ (d_ij − d̂_ij)² / Σ d_ij²)^(1/2)
L6      G ← the gradient of S(·, d̂) at X
L7      find a step α with S(X − αG, d̂) < S, halving α from a start value
L8      if no such α exists above a floor then return X
L9      X ← X − αG, then subtract the mean of the rows
L10 return X
```

Line L4 uses the [pool adjacent violators](/pool-adjacent-violators/) algorithm: walk along the sorted list, and whenever a value is smaller than the one before it, merge the two blocks into one block at their mean. Line L6 uses, with $S^* = \sum (d_{ij} - \hat d_{ij})^2$ and $T^* = \sum d_{ij}^2$,

$$\frac{\partial S}{\partial x_i} = \frac{S}{2}\left(\frac{1}{S^*}\sum_{j \ne i} \frac{2(d_{ij} - \hat d_{ij})}{d_{ij}}(x_i - x_j) - \frac{1}{T^*}\sum_{j \ne i} 2(x_i - x_j)\right),$$

where a pair with $d_{ij} = 0$ contributes nothing to the first sum. Kruskal (1964b) chose the step size by rules based on the angle between successive gradients. The implementation here uses a plain halving search, which is enough for the descent property. The scale of the step is tied to the size of $X$, because $S$ does not change when $X$ is scaled.

## Example

Take four objects with the six dissimilarities given only as ranks: the pair $(2,3)$ is the most alike (rank 1), then $(1,4)$, $(1,2)$, $(1,3)$, $(3,4)$ and $(2,4)$ (rank 6). Start from the points $x_1 = (0,0)$, $x_2 = (2,0)$, $x_3 = (2,1)$, $x_4 = (0,3)$.

| pair, in the order of δ | rank of δ | distance $d$ | disparity $\hat d$ |
|---|---|---|---|
| (2, 3) | 1 | 1 | 1 |
| (1, 4) | 2 | 3 | 2.4120 |
| (1, 2) | 3 | 2 | 2.4120 |
| (1, 3) | 4 | 2.2361 | 2.4120 |
| (3, 4) | 5 | 2.8284 | 2.8284 |
| (2, 4) | 6 | 3.6056 | 3.6056 |

The distance 3 of rank 2 is larger than the next ones, so pool adjacent violators merges ranks 2 to 4 into one block at their mean $(3 + 2 + \sqrt 5)/3 \approx 2.4120$. Then $S^* \approx 0.5465$ and $T^* = 1 + 9 + 4 + 5 + 8 + 13 = 40$, so $S = (0.5465/40)^{1/2} \approx 0.1169$. One gradient step brings the stress to $0.0060$, and the second step to $0$: the six distances become $1.090 < 2.473 < 2.646 < 2.651 < 2.743 < 3.571$, which is the order of the ranks. With four points and six ranks a perfect fit is easy, which is one face of the degeneracy noted under Pitfalls.

## Correctness

Kruskal's method is a local descent method, so its guarantee is about the stress, not about the optimum.

- **The disparities are optimal.** For a fixed $X$, the denominator $T^*$ does not depend on $\hat d$, so minimizing $S$ over $\hat d$ means minimizing $S^*$ over the monotone sequences. Lines L3 and L4 find this minimum for the primary approach. Sorting the tied pairs by their distances loses nothing, by a swap argument.
- **The stress never increases.** Line L7 accepts a step only if it lowers $S(\cdot, \hat d)$ for the current $\hat d$. Line L9 then centers $X$, which does not change any distance. In the next iteration, line L4 can only lower $S$ further. So the values of $S$ at line L5 form a non-increasing sequence, bounded below by 0, and they converge.
- **What is not guaranteed.** The limit can be a local minimum or a saddle point, and its value depends on the start. Nothing bounds the gap to the global minimum.

The full proof is in the proofs section below.

## Complexity

One iteration computes the $m = n(n-1)/2$ distances in $O(n^2 k)$ operations, sorts the pairs in $O(n^2 \log n)$, runs pool adjacent violators in $O(m) = O(n^2)$, and computes the gradient in $O(n^2 k)$. Each trial of the line search costs $O(n^2 k)$. So one iteration costs $O(n^2(k + \log n))$ operations, times the number of halvings, and the memory is $O(n^2)$ for the dissimilarities and the disparities. The sort can reuse the order of the last iteration, because only ties are reordered. The number of iterations $t$ has no general bound. It is set by a tolerance on the decrease of $S$ or by a limit, and in practice a few tens to a few hundreds of iterations are common.

## Properties

- **Invariance.** The stress does not change under a rotation, a reflection, a translation or a change of scale of $X$. The output is fixed only up to these maps.
- **Only the order counts.** Nonmetric MDS gives the same result for $\delta$ and for $f(\delta)$, for any strictly increasing $f$.
- **Local minima.** Stress functions in general have many local minima. Starting from the [classical MDS](/classical-mds/) solution and from several random starts is the usual remedy.
- **Not nested.** The best two-dimensional solution need not be a projection of the best three-dimensional one.
- **Shepard diagram.** A plot of $d_{ij}$ against $\delta_{ij}$, with the step function $\hat d$, shows how well the order is kept and is the standard diagnostic.

## Variants and improvements

- **Metric MDS by majorization.** [SMACOF](/smacof/) minimizes the raw stress with a step, the Guttman transform, that needs no line search and never increases the stress. Nonmetric SMACOF replaces the gradient step of line L9 by this transform and normalizes the disparities.
- **Sammon mapping.** [Sammon mapping](/sammon-mapping/) weights each squared error by $1/\delta_{ij}$, which keeps small distances.
- **Classical MDS.** [Classical MDS](/classical-mds/) changes the criterion to the strain and has a closed form.
- **Geodesic input.** [Isomap](/isomap/) feeds shortest path distances on a neighbor graph to classical MDS, which makes MDS a method of [manifold learning](/manifold-learning/).
- **Other fit criteria.** Stress-2 divides by $\sum (d_{ij} - \bar d)^2$ instead of $\sum d_{ij}^2$. Neighbor embeddings such as [t-SNE](/t-sne/) also place points from pairwise relations, but they fit probabilities of being neighbors, not distances.

## When to use it

Use MDS when the data are dissimilarities and not feature vectors: ratings of similarity, edit distances, correlations turned into distances, or travel times. Use the metric form when the values are meaningful up to a known transformation, and the nonmetric form when only their order is reliable. Use [classical MDS](/classical-mds/) when the dissimilarities are close to Euclidean distances and speed matters. For data on a curved manifold with many points, prefer [Isomap](/isomap/) or another method of [manifold learning](/manifold-learning/).

## Pitfalls

- **Degenerate nonmetric solutions.** With few objects, or with a few large dissimilarities that separate groups, nonmetric MDS can reach a stress near 0 with a useless map, for example clusters that collapse to points. Check the Shepard diagram, and compare with a metric solution.
- **Comparing stress values.** Stress-1, stress-2, raw stress and Sammon's stress are different numbers. A stress value is only meaningful with its definition, its tie approach, $n$ and $k$.
- **A single start.** One run can end in a poor local minimum. Use several starts, including the classical MDS solution.
- **Reading the axes.** Axes of an MDS map have no fixed meaning. Rotate the map for interpretation, or align two maps by the orthogonal Procrustes rotation, which comes from a [singular value decomposition](/singular-value-decomposition/), before you compare them.
- **Coincident points.** When $d_{ij} = 0$ the gradient of $d_{ij}$ is not defined. Leave that term out, as line L6 does, or move the points apart a little.

## Implementations

## History

Torgerson (1952) gave the classical metric method. Shepard (1962) produced the first nonmetric method, which only assumes that distance is a monotone function of dissimilarity. Kruskal (1964) made this precise: he defined the stress as a measure of fit, computed the disparities by monotone regression with his up-and-down blocks algorithm, and minimized the stress by steepest descent. De Leeuw (1977) introduced majorization for the stress, which led to [SMACOF](/smacof/).

## References
