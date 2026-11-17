---
tag: RBGT7A
kind: algorithm
slug: statistical-outlier-removal
name: Statistical outlier removal
aliases:
- statistical outlier filter
area: computer-vision/point-clouds-and-registration
level: core
summary: Remove points whose mean distance to their k nearest neighbors is more than a few standard deviations above the mean of that distance over the cloud.
model: real-ram
complexity:
  vars: {n: the number of points, k: the number of neighbors per point}
  time: {worst: O(n^2), average: O(n (log n + k log k)), best: Θ(n k)}
  space: {extra: Θ(n)}
properties: {deterministic: true, exact: true, online: false, recursive: false, rigid_motion_invariant: true, scale_invariant: true, heuristic: true}
history:
  year: 2008
  people: [Radu Bogdan Rusu, Zoltan Csaba Marton, Nico Blodow, Mihai Dolha, Michael Beetz]
  note: "Rusu and his coauthors removed the sparse outliers of laser scans by the statistics of the mean distance from each point to its k nearest neighbors, in their work on object maps of kitchens. The filter became the StatisticalOutlierRemoval class of the Point Cloud Library."
prereqs: [point-cloud, nearest-neighbor-search, sample-variance]
see_also: [kd-tree, k-nearest-neighbors, median-absolute-deviation, chebyshev-inequality, dbscan, voxel-grid-downsampling, point-cloud-normal-estimation, breakdown-point]
sources:
  - paper: doi:10.1016/j.robot.2008.08.005
    title: "Radu Bogdan Rusu, Zoltan Csaba Marton, Nico Blodow, Mihai Dolha and Michael Beetz, Towards 3D point cloud based object maps for household environments, Robotics and Autonomous Systems 56(11), 2008, 927-941"
    locator: "The removal of sparse outliers by the mean and the standard deviation of the mean distances to the k nearest neighbors"
  - paper: doi:10.1109/ICRA.2011.5980567
    title: "Radu Bogdan Rusu and Steve Cousins, 3D is here: Point Cloud Library (PCL), IEEE International Conference on Robotics and Automation (ICRA), 2011"
    locator: "The library and its filtering module"
---

Statistical outlier removal is a filter that deletes isolated points from a set of points in space. Laser scanners and depth cameras produce a few points that float in empty space, from reflections, from edges where the beam hits two surfaces, or from noise in the sensor. Such points are far from their neighbors. The filter measures, for each point, the mean distance $d_i$ to its $k$ nearest neighbors. It then takes the mean $\mu$ and the standard deviation $\sigma$ of these values over the whole cloud, and keeps a point only if $d_i \le \mu + \alpha \sigma$, for a user choice of $\alpha$ such as 1 or 2. It is a rule of thumb, not a statistical test: it assumes that most points lie on dense surfaces, so that a large mean neighbor distance means an outlier. With a [k-d tree](/kd-tree/) for the neighbor search, it costs $O(n (\log n + k \log k))$ time on well-spread points in 3D.

## In plain words

Points on a real surface have close neighbors. A stray point in the air does not. So, for each point, find its few nearest neighbors and take the average distance to them. This gives one number per point, a measure of how lonely the point is.

Look at all these numbers together. Most of them are about the same, because most points sit on surfaces sampled at about the same spacing. Compute their average and their spread. A point whose number is much larger than the average, by more than a chosen number of spreads, is thrown away. The rest are kept.

## The problem

The input is a finite list $P$ of $n$ points in $\mathbb{R}^3$, a number of neighbors $k$ with $1 \le k \le n - 1$, and a multiplier $\alpha \ge 0$. The output is the sub-list of the points whose mean distance to their $k$ nearest neighbors is at most $\mu + \alpha \sigma$, where $\mu$ and $\sigma$ are the mean and the standard deviation of these mean distances over all $n$ points.

The real aim, to remove the points that are not samples of a surface, has no exact definition. The rule above is one practical stand-in for it.

## The algorithm

```pseudo id=main
SOR(P, k, α)
L1  for i ← 1 to n do
L2      N ← the k nearest neighbors of p_i in P, without p_i
L3      d_i ← (1/k) Σ_{q ∈ N} ‖p_i - q‖
L4  μ ← (1/n) Σ_i d_i
L5  σ ← sqrt( (1/(n - 1)) Σ_i (d_i - μ)² )
L6  T ← μ + α σ
L7  return the points p_i with d_i ≤ T, in input order
```

Line L2 is the expensive step. Build a [k-d tree](/kd-tree/) on $P$ once and query it with $k + 1$ neighbors, since the nearest point to $p_i$ in $P$ is $p_i$ itself. Line L3 averages the distances, not the squared distances. Line L5 uses the [sample variance](/sample-variance/) with the divisor $n - 1$; with many points, the divisor $n$ gives the same result in practice. Lines L4 and L5 can run in one pass with [Welford's method](/welford-algorithm/).

The rule has two parameters. A larger $k$ makes $d_i$ smoother, but it also raises $d_i$ for points at the border of a surface, which have neighbors on one side only. A smaller $\alpha$ removes more points.

## Example

Take the nine points of a $3 \times 3$ grid with spacing 1 in the plane $z = 0$, at $(x, y, 0)$ for $x, y \in \{0, 1, 2\}$, and one outlier at $(4, 4, 0)$. Use $k = 2$.

| point | two nearest distances | $d_i$ |
|---|---|---|
| each grid point | 1 and 1 | 1 |
| $(4, 4, 0)$ | $\sqrt{8} = 2.828$ and $\sqrt{13} = 3.606$ | 3.217 |

Every grid point has two neighbors at distance 1. The outlier is nearest to $(2, 2, 0)$, then to $(2, 1, 0)$ and $(1, 2, 0)$, which tie. The mean is $\mu = (9 \cdot 1 + 3.217)/10 = 1.2217$, and the sample standard deviation is $\sigma = 0.7011$.

- With $\alpha = 1$, the threshold is $T = 1.9228$. The outlier has $d = 3.217 > T$, so it is removed, and the nine grid points stay.
- With $\alpha = 3$, the threshold is $T = 3.3249$, and the outlier stays. The outlier itself raised $\sigma$ from 0 to 0.70, enough to hide it at this setting. This is the masking effect of the mean and the standard deviation, which the variant with the median below avoids.

## Correctness

The mean of the $k$ smallest distances is the same for every way to break ties among equal distances, so line L3 is well defined. Lines L4 to L7 then compute $\mu$, $\sigma$ and the threshold by their definitions and keep exactly the points with $d_i \le \mu + \alpha\sigma$. The values $d_i$ depend only on the distances between points, so the kept set does not change under a rigid motion, a uniform scaling or a reordering of the cloud.

The one guarantee on the result is a bound on the number of removed points. For $\alpha > 0$, the one-sided [Chebyshev inequality](/chebyshev-inequality/) of Cantelli shows that at most $n / (1 + \alpha^2)$ points are removed, whatever the cloud: at most half for $\alpha = 1$. There is no guarantee that the removed points are outliers, or that all outliers are removed. The full proof is below.

## Complexity

The model is the [real RAM](/real-ram/), with $n$ points and $k$ neighbors per point.

- **Brute force.** Line L2 scans all other points, $\Theta(n)$ per point with a selection of the $k$ smallest. The total is $\Theta(n^2)$ for a fixed $k$.
- **With a k-d tree.** Building the tree costs $O(n \log n)$. In 3D, on points that are spread out without large clusters of equal coordinates, a query for $k$ neighbors visits $O(\log n + k)$ nodes on average, and keeping the $k$ best in a heap costs $O(\log k)$ per update. The total is then $O(n (\log n + k \log k))$. This is an average case bound for well-spread data in low dimension, not a worst case bound.
- **Lines L4 to L7.** $\Theta(n)$.
- **Space.** $\Theta(n)$ for the tree and the values $d_i$.

## Properties

- **A heuristic.** The rule assumes that the $d_i$ of the surface points form one tight group. It has no model of the sensor and no false alarm rate.
- **Global threshold.** One threshold serves the whole cloud. Where the density falls with the distance to the sensor, far surfaces have large $d_i$ and can be removed as a whole, while dense clusters of outliers near the sensor are kept.
- **Not robust.** The mean and the standard deviation have a [breakdown point](/breakdown-point/) of zero, so a few far outliers raise $\mu$ and $\sigma$ and hide themselves, as in the example.
- **Invariant.** The result does not depend on the order of the points, on a rigid motion or on a uniform scaling of the cloud.
- **Bounded removal.** At most $n / (1 + \alpha^2)$ points are removed for $\alpha > 0$.

## Variants and improvements

- **Median and MAD.** Replace $\mu$ by the [median](/median/) of the $d_i$ and $\sigma$ by a scaled [median absolute deviation](/median-absolute-deviation/). These have a breakdown point of one half, so a group of outliers cannot hide itself.
- **Radius outlier removal.** Count the neighbors within a fixed radius $r$ of each point, and remove the points with fewer than a set count. This needs one radius search per point and no global statistics, but the radius depends on the density.
- **Repeat.** Run the filter again on the output. Each pass removes outliers that the previous $\sigma$ hid, but it also eats into the borders of surfaces.
- **Local density ratios.** Compare $d_i$ with the $d_j$ of the neighbors of $p_i$, not with the global mean. This adapts to the fall of density with range. The local outlier factor of Breunig, Kriegel, Ng and Sander (2000) is a method of this kind.
- **Clusters.** Group the points with [DBSCAN](/dbscan/) or by [connected components](/connected-components/) of a radius graph, and remove the small clusters. This also removes small groups of outliers that are dense inside.
- **Downsample first.** A [voxel grid](/voxel-grid-downsampling/) before the filter makes the density more even, so the global threshold fits better.

## When to use it

Use statistical outlier removal on raw scans before [normal estimation](/point-cloud-normal-estimation/), registration and surface reconstruction, where isolated points spoil the local fits. It works best on clouds of roughly even density with sparse, scattered outliers. On clouds whose density changes a lot with the distance to the sensor, downsample first or use a local variant. Do not use it to remove dense groups of false points, such as the ghost points of a mirror or the mixed points along a depth edge: those have close neighbors.

## Pitfalls

- **The point is its own neighbor.** A k-d tree query for the $k$ nearest points of $p_i$ in $P$ returns $p_i$ first, at distance zero. Using these $k$ points at line L2 makes $d_i$ too small for every point. Query $k + 1$ points and drop the first, or exclude the point by its index.
- **Duplicates.** Several identical points have neighbors at distance zero, so their $d_i$ is small and they are always kept. Remove exact duplicates first if they come from the sensor.
- **The wrong side of the threshold.** The rule at line L7 keeps points with small $d_i$. The two-sided form $|d_i - \mu| \le \alpha\sigma$ also removes the points with very close neighbors, which are the densest and best samples.
- **Large $k$ at borders.** With a large $k$, line L3 reaches far past the border of a small surface, so a thin object or the edge of a table can be removed as outliers. Keep $k$ small compared with the number of points on the smallest object you need, often 10 to 50.
- **Units of $\alpha$.** The threshold at line L6 is in standard deviations of $d_i$, not in meters. The same $\alpha$ removes more or fewer points on another cloud. If you need a distance in meters, use a radius filter.

## Implementations

## History

Rusu, Marton, Blodow, Dolha and Beetz (2008) built maps of kitchens from laser scans for a household robot. To remove the sparse outliers of the scans, they computed the mean distance of each point to its $k$ nearest neighbors, modeled these distances by their mean and standard deviation, and trimmed the points that fell outside an interval set by these two values. The method became the StatisticalOutlierRemoval filter of the Point Cloud Library (Rusu and Cousins, 2011), which keeps the points below the threshold $\mu + \alpha\sigma$ and is the form most programs use.

## References
