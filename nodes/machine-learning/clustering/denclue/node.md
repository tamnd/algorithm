---
tag: HSSEG3
kind: algorithm
slug: denclue
name: DENCLUE
aliases:
- DENCLUE 2.0
area: machine-learning/clustering
level: advanced
summary: "Climb a Gaussian kernel density from each point to a density attractor; points with weak attractors are noise, and attractors joined by dense paths form one cluster."
solves: [density-based-clustering-problem]
model: real-ram
complexity:
  vars: {n: the number of points, d: the number of features, T: the largest number of steps of one climb, m: the number of attractor groups, s: the number of samples on a segment}
  time: {worst: "O(T n^2 d + m^2 s n d)", best: "Θ(n^2 d)"}
  space: {extra: "O(n d)"}
properties: {deterministic: true, online: false, exact: false, recursive: false}
history:
  year: 1998
  people: [Alexander Hinneburg, Daniel A. Keim, Hans-Henning Gabriel]
  note: Hinneburg and Keim presented DENCLUE at KDD 1998. Hinneburg and Gabriel gave DENCLUE 2.0, with a fixed point step, in 2007.
prereqs: [density-based-clustering-problem, hill-climbing, probability-density-function]
see_also: [mean-shift, dbscan, density-peak-clustering, optics, hdbscan, gradient-descent, fixed-point-iteration, grid-file]
sources:
  - paper: "Alexander Hinneburg and Daniel A. Keim, An efficient approach to clustering in large multimedia databases with noise, Proceedings of the Fourth International Conference on Knowledge Discovery and Data Mining (KDD-98), AAAI Press, 1998"
    locator: "pp. 58 to 65; the influence and density functions, the density attractors and the hill climbing, center-defined and arbitrary-shape clusters with the noise level ξ, the relation to DBSCAN and k-means, and the grid based implementation"
  - paper: doi:10.1007/978-3-540-74825-0_7
    title: "Alexander Hinneburg and Hans-Henning Gabriel, DENCLUE 2.0: fast clustering based on kernel density estimation, Advances in Intelligent Data Analysis VII (IDA 2007), Lecture Notes in Computer Science 4723, Springer, 2007"
    locator: the fixed point step for the Gaussian kernel, its link to expectation maximization, and the stopping rule on the relative gain in density
---

DENCLUE (DENsity-based CLUstEring) is a [density-based clustering](/density-based-clustering-problem/) method that models the data set by a sum of *influence functions*, one for each point, usually Gaussian, and so by a kernel estimate of the [density](/probability-density-function/). From each point it climbs the density by [hill climbing](/hill-climbing/) to a local top, its *density attractor*. Points whose attractor has a density below a noise level $\xi$ are outliers. Points with the same attractor form a *center-defined* cluster, and attractors joined by a path on which the density stays at least $\xi$ form one *arbitrary-shape* cluster. The original climb uses steps of a fixed length $\delta$ along the gradient. DENCLUE 2.0 uses a fixed point step that needs no step length. It is a heuristic: it has no guarantee to find all modes or the exact basins.

## In plain words

Put a small soft bump on top of each data point, and add the bumps up. Where many points are close, the bumps pile up into a hill. Where points are rare, the ground is low.

From each point, walk uphill in small steps until the next step would go down. The place where you stop is the top of your hill. Points that end at the same top form a group.

If a top is too low, the hill is just one or two lonely points, and those points are noise. Two tops count as one group if you can walk from one to the other without going below a certain height. That way a long ridge of high ground becomes one group, whatever its shape.

## The problem

The data model is clustering of points in $\mathbb{R}^d$ with the [Euclidean distance](/euclidean-distance/). The input is $n$ points $x_1, \ldots, x_n$, a smoothing parameter $\sigma > 0$ and a noise level $\xi \ge 0$. Hinneburg and Keim (1998) define:

- The **Gaussian influence function** of a point $y$ at $x$, $f_y(x) = \exp(-\lVert x - y \rVert^2 / (2\sigma^2))$.
- The **density function** $f(x) = \sum_{i=1}^n f_{x_i}(x)$, which is a kernel density estimate up to a constant factor. Its gradient is $\nabla f(x) = \sigma^{-2} \sum_i (x_i - x) f_{x_i}(x)$.
- A **density attractor** is a local maximum of $f$. A point is *density-attracted* to it if hill climbing from the point ends there.
- A **center-defined cluster** for an attractor $x^*$ with $f(x^*) \ge \xi$ is the set of points attracted to $x^*$. Points attracted to an attractor with $f(x^*) < \xi$ are **outliers**.
- An **arbitrary-shape cluster** for a set $X$ of attractors is the set of points attracted to them, where each attractor in $X$ has $f(x^*) \ge \xi$ and each two of them are joined by a path on which $f \ge \xi$.

The paper also allows other influence functions. With the *square wave* influence, $f_y(x) = 1$ if $\lVert x - y \rVert \le \sigma$ and $0$ otherwise, the density at $x$ is the number of points within $\sigma$, and arbitrary-shape clusters with $\xi = \mathit{MinPts}$ behave like the clusters of [DBSCAN](/dbscan/).

## The algorithm

```pseudo id=main
DENCLUE(D, σ, ξ, δ, merge distance, shape)
L1  for each point x_j of D do
L2      x ← x_j
L3      loop
L4          g ← Σ_i (x_i − x) exp(−‖x − x_i‖² / (2σ²))     ▷ σ² ∇f(x)
L5          if g = 0 then exit the loop
L6          x' ← x + δ g / ‖g‖
L7          if f(x') < f(x) then exit the loop
L8          x ← x'
L9      end[j] ← x
L10 group the ends: an end joins the first group whose representative is within the merge distance
L11 if shape = arbitrary then join two groups whose representatives have f ≥ ξ and
        the straight segment between them has f ≥ ξ at s + 1 sample points
L12 for each j: label[j] ← NOISE if f(end[j]) < ξ, else the joined group of end[j]
L13 return label
```

Lines L2 to L8 are the climb of DENCLUE 1.0: a step of length $\delta$ along the normalized gradient, stopped as soon as a step would lower the density. Line L10 is needed because climbs to one attractor stop at slightly different places, up to about $\delta$ apart. Line L11 tests the path condition on straight segments only, which is a sufficient test but not a necessary one.

**DENCLUE 2.0.** Hinneburg and Gabriel (2007) replace lines L4 to L8 by the step

$$x \leftarrow \frac{\sum_i f_{x_i}(x) \, x_i}{\sum_i f_{x_i}(x)},$$

and stop when the relative gain $(f(x') - f(x)) / f(x')$ is below a tolerance. For the Gaussian kernel this is the step of [mean shift](/mean-shift/), a [fixed point iteration](/fixed-point-iteration/) that never lowers the density and adapts its step length to the slope, so it needs no $\delta$ and converges much faster than the fixed step.

**Ties and order.** A step that leaves the density unchanged is accepted. Line L10 assigns an end to the first group in input order, so the numbering of the clusters follows the input order.

## Example

Take the points 0, 0.5, 1, 4, 4.5, 5 and 9 on the line, with $\sigma = 0.5$, $\delta = 0.05$ and $\xi = 1.2$. The density is $2.213$ at 0.5 and at 4.5, and $1.742$ at 0, 1, 4 and 5. Between the groups it falls to about $0.02$, and at 9 it is $1.000$, the influence of the point 9 alone.

The climb from 0 takes 10 steps of 0.05 and stops at 0.5, the top of the first hill, because the next step would go down. The climb from 0.5 stops at once. The climbs from 1, 4, 4.5 and 5 end at 0.5 or 4.5 in the same way. The point 9 is its own top, with density $1.000 < \xi$, so it is an outlier. The result is {0, 0.5, 1}, {4, 4.5, 5} and the noise point 9. The two attractors are not joined, because the segment between them passes density 0.02.

With $\sigma = 1.5$ the bumps are wider. The attractors move to 0.70, 4.35 and 8.70, with densities 3.01, 3.02 and 1.06. The point 9 is still noise. The density between 0.70 and 4.35 never falls below about 2.5, so the arbitrary-shape clusters join the first six points into one cluster, while the center-defined clusters keep two.

## Correctness

DENCLUE is a heuristic, and the claim is about what it guarantees, not about finding the true modes. The vector of line L4 is $\sigma^2$ times the gradient of $f$, so each step goes uphill in the steepest direction, and line L7 makes the density along each climb non-decreasing. Each climb ends at a point where one more step lowers the density, and in one dimension such a point lies within $\delta$ of a local maximum. A point is noise exactly when its own attractor has a density below $\xi$. The center-defined clusters are the groups of attractors, and the arbitrary-shape clusters are the components of the graph of groups joined by segments that stay at density $\xi$ or more at the sampled points. A segment of this kind is a path of the definition, so these clusters meet the definition, but a curved dense path is not found. The full proof is below.

## Complexity

The model is the [real RAM](/real-ram/), with $\exp$ at unit cost. Here $n$ is the number of points, $d$ the number of features, $T$ the largest number of steps of one climb, $m$ the number of groups of attractors, and $s$ the number of sample points on a segment.

- **Climbs.** Each step evaluates $g$ and $f$ over all points, $\Theta(n d)$. The climbs take $O(T n^2 d)$ time. With the fixed step, $T$ is at least the distance to the attractor divided by $\delta$, so a small $\delta$ is slow. DENCLUE 2.0 needs far fewer steps.
- **Joining attractors.** Line L11 makes $O(m^2)$ segment tests, each with $s + 1$ evaluations, $O(m^2 s n d)$ time.
- **The grid of the paper.** Hinneburg and Keim keep a [grid](/grid-file/) of hypercubes of side $2\sigma$, store only the populated cubes, and evaluate $f$ near $x$ with only the points in nearby cubes, since the Gaussian influence of far points is negligible. They also give every point close to the path of a climb the attractor of that climb, which saves most climbs.
- **Space.** $O(n d)$ for the ends of the climbs, besides the input.

## Properties

- **Not exact.** The result depends on $\sigma$, $\delta$, $\xi$ and the merge distance, and the climbs can stop near saddles or jump across valleys. No global guarantee is known.
- **Noise.** Points whose hills are low are outliers. The level $\xi$ is in the units of the density sum, so a point alone has density about 1 at its own position.
- **Arbitrary shapes.** Arbitrary-shape clusters follow ridges of high density, like the clusters of DBSCAN.
- **Generalization claims.** Hinneburg and Keim show that with suitable influence functions and parameters DENCLUE can mimic DBSCAN (square wave influence) and k-means type partitions (Gaussian influence with a $\sigma$ at which each cluster has one attractor).
- **Smooth density.** The sum of Gaussians is smooth and has a gradient everywhere, unlike the counts of DBSCAN.

## Variants and improvements

- **DENCLUE 2.0.** The fixed point step above, with an analysis that links it to [expectation maximization](/expectation-maximization/) and a stopping rule on the relative gain. It removes $\delta$ from the parameters.
- **Mean shift.** [Mean shift](/mean-shift/) uses the same step as DENCLUE 2.0 but has no noise level and no joining of attractors.
- **Other kernels.** The square wave kernel gives counts, as in DBSCAN. Kernels with bounded support let a spatial index find all the points that matter.
- **Hierarchy over $\xi$.** Raising $\xi$ splits arbitrary-shape clusters and turns more points into noise, which gives a tree of clusters as in [HDBSCAN](/hdbscan/).

## When to use it

Use DENCLUE when the data are low dimensional, when a smooth density model fits, and when you want both noise detection and clusters of any shape. It handles large data sets with the grid of the paper when $\sigma$ is small compared with the range of the data. Prefer DENCLUE 2.0 over the fixed step. Avoid it when the dimension is high, since density estimates and grids both fail there.

## Pitfalls

- **Units of $\xi$.** The density is a sum, not an average, so $\xi$ must grow with $n$ for the same meaning. Some write-ups normalize $f$ and then use a different $\xi$.
- **The step length.** A large $\delta$ jumps over narrow hills and stops far from the tops, so the merge distance must grow. A small $\delta$ makes the climbs slow.
- **Choosing $\sigma$.** It sets the smoothness. Too small gives one attractor for each point, too large merges all clusters. A common heuristic is to choose a value at which the number of attractors stays the same over a wide range of $\sigma$.
- **Path test.** The straight segment test misses curved dense paths. A curved cluster may need a finer chain of attractors or a test through data points.
- **Scaling.** One $\sigma$ for all features needs features on comparable scales.

## Implementations

## History

Alexander Hinneburg and Daniel Keim presented DENCLUE at the KDD conference in 1998, for large multimedia databases with much noise. They built on the idea of a density as a sum of influence functions, and showed that their framework covered DBSCAN and k-means type methods as special cases. In 2007 Hinneburg and Hans-Henning Gabriel presented DENCLUE 2.0, which replaced the fixed step climb by a fixed point iteration with a proof that it does not lower the density.

## References
