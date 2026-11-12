---
tag: AN3FSZ
kind: algorithm
slug: mean-shift
name: Mean shift
aliases:
- mean shift clustering
- mean shift mode seeking
area: machine-learning/clustering
level: advanced
summary: "Move each point to the kernel weighted mean of the data around it, again and again, until it stops at a mode of the density; points at one mode form a cluster."
solves: [density-based-clustering-problem]
model: real-ram
complexity:
  vars: {n: the number of points, d: the number of features, T: the largest number of steps of one walk}
  time: {worst: "O(T n^2 d)", best: "Θ(n^2 d)"}
  space: {extra: "O(n d)"}
properties: {deterministic: true, online: false, exact: false, recursive: false}
history:
  year: 1975
  people: [Keinosuke Fukunaga, Larry Hostetler, Yizong Cheng, Dorin Comaniciu, Peter Meer]
  note: Fukunaga and Hostetler introduced the mean shift in 1975. Cheng (1995) generalized it and linked it to clustering, and Comaniciu and Meer (2002) made it a standard tool in computer vision.
prereqs: [density-based-clustering-problem, probability-density-function, hill-climbing]
see_also: [denclue, density-peak-clustering, dbscan, k-means, gaussian-mixture-model, expectation-maximization, image-segmentation, fixed-point-iteration]
sources:
  - paper: doi:10.1109/TIT.1975.1055330
    title: "Keinosuke Fukunaga and Larry D. Hostetler, The estimation of the gradient of a density function, with applications in pattern recognition, IEEE Transactions on Information Theory 21(1), 1975"
    locator: the estimate of the density gradient by a kernel, the mean shift, and its use for clustering
  - paper: doi:10.1109/34.400568
    title: "Yizong Cheng, Mean shift, mode seeking, and clustering, IEEE Transactions on Pattern Analysis and Machine Intelligence 17(8), 1995"
    locator: the general kernel and weight form, the mean shift as gradient ascent with an adaptive step, blurring mean shift, and the link to k-means
  - paper: doi:10.1109/34.1000236
    title: "Dorin Comaniciu and Peter Meer, Mean shift: a robust approach toward feature space analysis, IEEE Transactions on Pattern Analysis and Machine Intelligence 24(5), 2002"
    locator: Section 2 (the mean shift vector as the normalized density gradient, Theorem 1 on the convergence and on the monotone density), and the applications to filtering and segmentation
  - paper: "Xiangru Li, Zhanyi Hu and Fuchao Wu, A note on the convergence of the mean shift, Pattern Recognition 40(6), 2007"
    locator: the gap in the proof that the whole sequence of mean shift points converges
---

Mean shift is a mode seeking method for [density-based clustering](/density-based-clustering-problem/). From each data point it repeats one step: move to the mean of the data, weighted by a kernel centered at the current position. The move is a step uphill on a kernel estimate of the [density](/probability-density-function/), and with the Gaussian kernel the step equals $h^2 \nabla f / f$, so it is long in sparse regions and short near a peak. Each walk stops at a local maximum (a *mode*), and the points whose walks end at one mode form a cluster. The only parameter is the bandwidth $h$. The number of clusters is an output. Each step costs $\Theta(n d)$ for each walk in the [real RAM](/real-ram/) model.

## In plain words

Put a light on each data point and look at the points around it. Nearby points count a lot, far ones count little. Find the center of mass of what you see, and move there. Look again, and move again.

Each move goes toward the place where the points are most crowded. The moves get shorter as you get close to the most crowded spot, and then you stop there.

Do this from every data point. The points that end at the same crowded spot form one group. How far you look, the bandwidth, decides how many crowded spots there are: look far and the spots blur into one, look near and every small bump is a spot.

## The problem

The data model is clustering of points in $\mathbb{R}^d$ with the [Euclidean distance](/euclidean-distance/). The input is $n$ points $x_1, \ldots, x_n$ and a bandwidth $h > 0$. With the Gaussian kernel, the kernel density estimate is

$$\hat f(y) = \frac{1}{n (2 \pi h^2)^{d/2}} \sum_{i=1}^n \exp\!\Big(-\frac{\lVert y - x_i \rVert^2}{2 h^2}\Big).$$

A *mode* is a local maximum of $\hat f$. The *basin of attraction* of a mode is the set of starting points whose path of steepest ascent ends there. The goal is the partition of the data into the basins of the modes. The **mean shift vector** at $y$ is

$$m(y) = \frac{\sum_i w_i x_i}{\sum_i w_i} - y, \qquad w_i = \exp\!\Big(-\frac{\lVert y - x_i \rVert^2}{2 h^2}\Big).$$

For the Gaussian kernel, $m(y) = h^2 \nabla \hat f(y) / \hat f(y)$ (Comaniciu and Meer 2002, Section 2). For a general kernel with profile $k$, the weights use $g = -k'$ and the vector is proportional to the gradient of the estimate with the profile $k$, divided by the estimate with the profile $g$.

## The algorithm

```pseudo id=main
MEAN-SHIFT(D, h, τ, δ)
L1  for each point x_j of D do
L2      y ← x_j
L3      repeat
L4          w_i ← exp(−‖y − x_i‖² / (2h²)) for each point x_i of D
L5          y' ← Σ w_i x_i / Σ w_i
L6          s ← ‖y' − y‖; y ← y'
L7      until s < τ
L8      mode[j] ← y
L9  centers ← empty list
L10 for each j, in input order do
L11     if some center c has ‖mode[j] − c‖ < δ then label[j] ← the first such c
L12     else append mode[j] to centers; label[j] ← its index
L13 return label, centers
```

Lines L4 to L6 are one mean shift step, a [fixed point iteration](/fixed-point-iteration/) of the map $y \mapsto y + m(y)$, whose fixed points are the stationary points of $\hat f$. Line L7 stops a walk when the step is shorter than $\tau$; a cap on the number of steps is a common safeguard. Lines L9 to L12 merge the end points that lie closer than $\delta$, since walks to one mode stop at slightly different places. A common choice is $\delta = h/2$.

**Ties.** A point exactly at a local minimum or a saddle of $\hat f$ has $m = 0$ and does not move, so it forms its own mode. Line L11 gives an end point the first center within $\delta$ in input order, so the cluster numbers follow the input order.

## Example

Take the points 1, 2, 3, 7 and 8 on the line, with $h = 1$. At $y = 1$ the weights are $1$, $e^{-1/2} \approx 0.6065$, $e^{-2} \approx 0.1353$, and $e^{-18}$ and $e^{-24.5}$ for 7 and 8, which are almost 0. The weighted mean is $2.6191 / 1.7419 \approx 1.5036$. The walk from 1 continues:

| step | 0 | 1 | 2 | 3 | 4 | ... | end |
|---|---|---|---|---|---|---|---|
| $y$ | 1 | 1.5036 | 1.7349 | 1.8558 | 1.9211 | ... | 2.0000 |
| $\hat f(y)$, up to a constant | 0.3484 | 0.4183 | | | | ... | 0.4426 |

The density rises at every step, and the steps get shorter: 0.50, 0.23, 0.12, 0.07. The walk from 3 is the mirror image and also ends at 2. The walk from 2 stays at 2. The walks from 7 and 8 end at 7.4999, slightly left of the middle 7.5, because the point 3 pulls with a tiny weight. With $\delta = 0.5$ the result is two clusters, {1, 2, 3} with the mode 2 and {7, 8} with the mode 7.5. With $h = 4$ the two groups blur into one bump, and all points end at one mode.

## Correctness

The claim is that each step raises the density estimate, that each walk stops, and that it stops where the gradient is small. With the Gaussian profile $k(t) = e^{-t/2}$ and $g = -k'$, the mean shift vector equals $h^2 \nabla \hat f / \hat f$, by a direct computation. The profile is convex, so $k(s) \ge k(t) - g(t)(s - t)$. Adding this over the data points gives $\hat f(y') - \hat f(y) \ge (G / h^2) \lVert y' - y \rVert^2$, where $G$ is the sum of the weights $g$; this is Theorem 1 of Comaniciu and Meer. The new point is a convex combination of the data, so the walk stays in the convex hull, $G$ stays bounded below, and the sum of the squared steps is finite. So the steps tend to 0, and the stop test is met. The full proof is below.

The Comaniciu and Meer proof that the whole sequence converges to one point has a gap (Li, Hu and Wu 2007). The algorithm above does not need that statement, because it stops on the length of the step.

## Complexity

The model is the [real RAM](/real-ram/), with $\exp$ at unit cost. Here $n$ is the number of points, $d$ the number of features and $T$ the largest number of steps of one walk.

- **Time.** One step computes $n$ weights, $\Theta(n d)$. There are $n$ walks, so the time is $O(T n^2 d)$, and at least $\Theta(n^2 d)$ since each walk takes at least one step.
- **The number of steps.** The convergence near a mode is linear: the error shrinks by a factor below 1 at each step, and the factor is close to 1 when the mode is flat. Carreira-Perpiñán (2007) shows that Gaussian mean shift is an [expectation maximization](/expectation-maximization/) algorithm, which explains the linear rate.
- **Space.** The walks are independent, so the extra space is $O(n d)$ for the end points, besides the input.
- **Speed-ups.** Kernels with bounded support (for example the Epanechnikov kernel) need only the points within $h$, which a [k-d tree](/kd-tree/) or a grid finds. Starting walks from a grid of bins, or from a sample, cuts the number of walks.

## Properties

- **Not exact.** The method finds an approximate stationary point for each walk. It has no global guarantee: the clusters depend on $h$, and the walks can stop near a saddle.
- **Monotone density.** With a convex and decreasing profile, such as the Gaussian or the Epanechnikov profile, the density estimate never decreases along a walk.
- **No number of clusters.** The number of clusters equals the number of modes reached, which $h$ controls.
- **Every point gets a cluster.** There is no noise. A point in a sparse region forms a cluster of its own or walks to a far mode.
- **Translation and rotation invariant**, since only distances enter.
- **Link to k-means.** Cheng (1995) generalizes mean shift so that some clustering methods of the [k-means](/k-means/) type become special cases of it.

## Variants and improvements

- **Blurring mean shift.** Move all data points at once and use the moved points as the new data in the next step (Fukunaga and Hostetler 1975, Cheng 1995). It converges in fewer steps, but the data collapse to points in the end, so it needs a stopping rule.
- **Other kernels.** With the Epanechnikov kernel the weights $g$ are those of the flat kernel, so each step moves to the plain mean of the points within the window. The walk then reaches a fixed point in finitely many steps.
- **Adaptive bandwidth.** A bandwidth for each point, for example from the distance to its $k$-th nearest neighbor, adapts to the local density.
- **Joint spatial and range domain.** Comaniciu and Meer use the vector of pixel position and color, with one bandwidth for each part, for edge preserving filtering and [image segmentation](/image-segmentation/).
- **Tracking.** Comaniciu, Ramesh and Meer (2000) run mean shift on a similarity surface to track objects in video.
- **[DENCLUE](/denclue/).** Uses the same hill climbing on a kernel density, with a noise threshold.

## When to use it

Use mean shift in low dimension when the clusters are the bumps of a smooth density, the number of clusters is unknown, and one bandwidth fits all clusters. It is common for images, where the feature space has three to five dimensions. Avoid it when $n$ is large without an index, when the dimension is high, or when you need a noise label.

## Pitfalls

- **The bandwidth.** It decides everything: too small gives one cluster for each point, too large gives one cluster in all. Rules of thumb from density estimation, such as Silverman's rule, aim at a good density estimate, which is not the same as a good clustering.
- **A loose stop test.** With a large $\tau$, walks stop early, far from the mode, and the merge step must then use a larger $\delta$, which can join different modes.
- **Unscaled features.** One bandwidth for all features needs features on comparable scales.
- **Slow convergence.** Walks near a flat mode take many steps. Cap the number of steps.
- **Trusting the convergence proof.** The claim that the sequence of points converges was not fully proved in the 2002 paper. Monotone density and the stopping of the algorithm are proved.

## Implementations

## History

Keinosuke Fukunaga and Larry Hostetler introduced the mean shift in 1975, as an estimate of the gradient of a density for pattern recognition, and used it to cluster data. The idea was little used until Yizong Cheng in 1995 generalized the kernel and the weights, explained the method as gradient ascent with an adaptive step, and related it to k-means. Dorin Comaniciu and Peter Meer made it a main tool of computer vision around 2000, for filtering, segmentation and tracking, and their 2002 paper is the standard reference. Li, Hu and Wu in 2007 found a gap in its convergence proof, which later work closed for special cases.

## References
