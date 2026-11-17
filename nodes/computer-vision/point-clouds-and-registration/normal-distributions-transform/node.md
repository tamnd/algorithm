---
tag: 2WB2RV
kind: algorithm
slug: normal-distributions-transform
name: Normal distributions transform
aliases:
- NDT
- NDT registration
area: computer-vision/point-clouds-and-registration
level: advanced
summary: "Model the reference cloud as a Gaussian per voxel and align the other cloud by Newton steps that maximize the likelihood of its points."
solves: [point-cloud-registration]
model: real-ram
complexity:
  vars: {n: the number of points in the reference scan, m: the number of points in the current scan, N: the number of Newton iterations}
  time: {worst: O(n + N m), average: O(n + N m), best: Θ(n + m)}
  space: {extra: Θ(n)}
properties: {deterministic: true, exact: false, online: false, recursive: false}
history:
  year: 2003
  people: [Peter Biber, Wolfgang Straßer]
  note: "Biber and Straßer introduced NDT for 2D laser scans at IROS 2003. Magnusson, Lilienthal and Duckett extended it to 3D scans in 2007."
prereqs: [point-cloud-registration, newton-method-for-systems, covariance-matrix]
see_also: [iterative-closest-point, generalized-icp, correlative-scan-matching, lidar-odometry-and-mapping, gaussian-mixture-model, coherent-point-drift, levenberg-marquardt, voxel-grid-downsampling]
sources:
  - paper: doi:10.1109/IROS.2003.1249285
    title: "Peter Biber and Wolfgang Straßer, The normal distributions transform: a new approach to laser scan matching, Proceedings of the IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS 2003), vol. 3, 2743-2748"
    locator: "The normal distribution of each cell with at least 3 points, the four overlapping grids, the score as a sum of exponentials, and the Newton steps on the 2D pose with a positive definite Hessian"
  - paper: doi:10.1002/rob.20204
    title: "Martin Magnusson, Achim Lilienthal and Tom Duckett, Scan registration for autonomous mining vehicles using 3D-NDT, Journal of Field Robotics 24(10), 2007, 803-827"
    locator: "NDT for 3D scans and its comparison with ICP"
---

The normal distributions transform (NDT) aligns a laser scan to a reference scan, or a [point cloud](/point-cloud/) to a map. It does not match points to points. It cuts the space of the reference scan into a grid of square cells, and in each cell with enough points it stores the mean and the [covariance](/covariance-matrix/) of those points: a normal distribution that describes the local shape, for example a thin ellipse along a wall. The pose of the current scan is then scored by how well its points fit these distributions, and the score is improved by [Newton steps](/newton-method-for-systems/) with an exact gradient and Hessian. The method needs no nearest neighbour search, and the cost of one step is linear in the number of scan points.

## In plain words

Cut the floor plan of the first scan into squares. In each square, look at the points that fall in it, and replace them by a soft blob: a centre, and an oval that is long along the wall and thin across it.

Now lay the second scan over the squares. Each point gets a high mark if it sits near the centre of the blob of its square, and a higher mark if it is off the centre only along the long side of the oval. Add all the marks. Then turn and move the second scan a little, in the direction that raises the total most quickly, and repeat until the total stops rising.

The blobs are smooth, so the best direction is easy to find. And a point needs only the blob of its own square, so no search for the closest point is needed.

## The problem

**Input.** A reference scan with $n$ points in $\mathbb{R}^2$, a current scan with $m$ points $x_1, \ldots, x_m$, a cell size, and a start pose $p_0$.

**Output.** A pose $p = (t_x, t_y, \phi)$, which maps a point $x$ to $x' = R(\phi)\,x + t$, such that the moved scan lies on the reference scan. NDT finds a local minimum of the cost below near $p_0$. This is local [point cloud registration](/point-cloud-registration/), like [ICP](/iterative-closest-point/).

## The algorithm

**The grids.** Cut the plane into square cells. For a cell whose reference points are $y_1, \ldots, y_k$ with $k \ge 3$, compute

$$q = \frac{1}{k} \sum_{j} y_j, \qquad \Sigma = \frac{1}{k} \sum_j (y_j - q)(y_j - q)^\top .$$

Cells with fewer points get no distribution. Biber and Straßer use four grids: one plain, one shifted by half a cell in $x$, one in $y$, and one in both. So each point lies in four cells, and the effect of the cell boundaries is smaller.

**The cost.** For a pose $p$, each scan point $x'$ and each grid with a distribution $(q, \Sigma)$ in the cell of $x'$ give the term $\exp\bigl(-\frac{1}{2}(x' - q)^\top \Sigma^{-1} (x' - q)\bigr)$. The score is the sum of all terms, and NDT minimizes the cost $f(p)$, which is minus the score. Let $u = x' - q$, $A = \Sigma^{-1}$, $e = \exp(-\frac{1}{2} u^\top A u)$ and $J_i = \partial x' / \partial p_i$. Each term adds $e\, u^\top A J_i$ to the gradient $g$ and

$$e \bigl( -(u^\top A J_i)(u^\top A J_k) + J_i^\top A J_k + u^\top A\, \partial J_i / \partial p_k \bigr)$$

to the Hessian $H$. $J_1 = (1, 0)$ and $J_2 = (0, 1)$ are constant; only $J_3 = \partial x' / \partial \phi$ has a derivative.

```pseudo id=main
NDT(reference, scan, cell, p₀)
L1  build the four grids: for each cell with ≥ 3 points, the mean q and Σ⁻¹
L2  p ← p₀ ;  repeat
L3      f, g, H ← the cost of the scan at p, its gradient and its Hessian
L4      λ ← 0 ;  while H + λI is not positive definite:  increase λ ;  Δp ← -(H + λI)⁻¹ g
L5      t ← 1 ;  while f(p + t Δp) ≥ f and few halvings so far:  t ← t / 2
L6      if no step lowered f: stop ;  p ← p + t Δp
L7      if the decrease is tiny: stop
L8  return p
```

Line L1 groups the reference points by cell with a [hash table](/hash-table/). The reference code raises the smaller eigenvalue of $\Sigma$ to at least 0.001 times the larger one, so that the points of a straight wall do not give a singular matrix. Line L3 finds the cell of each moved point by its key in each grid, in constant time. Line L4 makes $H$ [positive definite](/positive-definite-matrix/), as the paper asks; the reference code adds $\lambda I$ and tests with a [Cholesky factorization](/cholesky-decomposition/). Line L5 halves the step, as in a [backtracking line search](/backtracking-line-search/), until the cost drops. The cell size, the eigenvalue floor and the step halving are choices of the reference code, not of the paper.

## Example

**One cell.** A cell of side 1 holds the points $(0.2, 0.4)$, $(0.8, 0.4)$, $(0.2, 0.6)$ and $(0.8, 0.6)$. The mean is $q = (0.5, 0.5)$, and $\Sigma$ is diagonal with $0.09$ in $x$ and $0.01$ in $y$, so $A = \operatorname{diag}(11.1, 100)$. The points spread more along $x$, like a wall. A scan point at $(0.7, 0.5)$, off the mean by $0.2$ along the wall, gets $\exp(-\frac{1}{2} \cdot 0.04 \cdot 11.1) = 0.80$. A point at $(0.5, 0.7)$, off by the same $0.2$ across the wall, gets $\exp(-\frac{1}{2} \cdot 0.04 \cdot 100) = 0.14$. So the cost pulls points onto the wall far more than along it.

**A registration.** The reference scan has 600 points on the walls of an L-shaped room of $10 \times 8$ with a slanted box, and noise of standard deviation 0.02. The current scan has 300 other points of the same walls, seen from the pose $(0.4, -0.3, 8°)$. With cells of side 1, the four grids hold 67, 55, 55 and 39 distributions. From the start pose $(0, 0, 0°)$ the reference code takes 17 accepted steps:

| Step | $t_x$ | $t_y$ | $\phi$ | $f$ |
|---:|---:|---:|---:|---:|
| 0 | 0 | 0 | 0° | -55.99 |
| 3 | -0.016 | -0.017 | 0.80° | -64.90 |
| 6 | 0.052 | -0.084 | 1.87° | -87.05 |
| 7 | 0.244 | -0.225 | 5.23° | -127.26 |
| 9 | 0.346 | -0.280 | 7.74° | -352.00 |
| 12 | 0.391 | -0.283 | 7.82° | -456.18 |
| 17 | 0.392 | -0.288 | 7.89° | -461.98 |

The first steps are small, because at the start few scan points lie near a wall of the same direction. Once the walls begin to overlap, the cost drops fast. The final pose is within 0.012 of the true shift and 0.11° of the true turn. The cost cannot go below $-4 \cdot 300 = -1200$; it stays far above that because a cell of side 1 at a corner or at the box does not fit one ellipse well.

## Correctness

NDT is a local method, and what can be proved is that it is a sound descent method. Each term of $f$ lies in $[-1, 0)$, so $-4m \le f \le 0$. Line L5 accepts a step only if $f$ drops, so the costs of the accepted poses strictly decrease and converge. Where no moved point lies on a cell boundary, every point keeps its cells near $p$, so $f$ is smooth there, and the formulas above give its exact gradient and Hessian. Because $H + \lambda I$ is positive definite, $g^\top \Delta p < 0$ when $g \ne 0$, so a short enough step lowers $f$. The full proof is in [proofs/correctness.md](proofs/correctness.md).

This does not mean that NDT finds the right pose. $f$ has many local minima and jumps where points cross cell boundaries. With the reference code and cells of side 1, a turn of 8 degrees is recovered, but for some random scans a turn of 12 degrees with a shift of 0.5 is not; a first run with cells of side 2 fixes such cases.

## Complexity

The model is the [real RAM](/real-ram/), with a hash table that answers a lookup in expected constant time. Line L1 groups the $n$ reference points and computes each mean and covariance in one pass, in $\Theta(n)$ time; the grids hold at most $4n/3$ distributions, so the extra space is $\Theta(n)$. Line L3 visits each of the $m$ scan points with 4 lookups, in $\Theta(m)$ time. Line L4 works on a $3 \times 3$ matrix. Line L5 evaluates $f$ a bounded number of times, each in $\Theta(m)$. So $N$ iterations take $O(n + N m)$ time, and one iteration that stops at once takes $\Theta(n + m)$. The number $N$ depends on the data and the start pose; in the example it is 17.

ICP needs a nearest neighbour query for each point in each iteration, $O(\log n)$ time with a [k-d tree](/kd-tree/) on spread out points. NDT replaces it with a cell lookup, at the price of a coarser model of the surface.

## Properties

- **Local.** It converges to a minimum near the start pose. The basin is about the size of a cell.
- **No correspondences.** Each point is scored against a distribution, not matched to a point, so there is no nearest neighbour search.
- **Smooth within cells.** The cost has exact first and second derivatives where the cells do not change, so Newton steps work well.
- **Deterministic.** The same input gives the same pose.
- **Compact map.** The reference scan is stored as one mean and one matrix per cell, which is often much smaller than the points.
- **Probabilistic view.** The score is close to the log likelihood of the scan under a mixture of normal distributions, one per cell, as in [maximum likelihood estimation](/maximum-likelihood-estimation/).

## Variants and improvements

- **3D NDT.** Magnusson, Lilienthal and Duckett (2007) use cubic cells in 3D and a 6D pose, with the same Newton scheme. It is common in lidar localization against a prior map.
- **Coarse to fine.** Run NDT with large cells first, then with smaller cells from the result. The large cells give a wide basin, and the small cells give an accurate pose.
- **Robust score.** Later forms mix each normal distribution with a uniform part, so that points with no good cell weigh less.
- **Other cell structures.** An [octree](/octree/) or cells of adaptive size fit the cells to the density of the points.
- **Distribution to distribution.** Both scans are turned into normal distributions, and the cost compares the distributions instead of points with distributions.
- **Other optimizers.** A [Levenberg-Marquardt](/levenberg-marquardt/) step, or a line search with other conditions, replaces the plain Newton step.

## When to use it

Use NDT to register lidar scans, or a scan to a stored map, when a fair start pose is known, for example from odometry, and the scenes have walls, ground and other smooth surfaces. It is fast and needs no correspondences, so it suits real-time localization in [SLAM](/slam-problem/) and [lidar odometry](/lidar-odometry-and-mapping/). When the start pose is poor, start with large cells, or use a global method such as [correlative scan matching](/correlative-scan-matching/) first. When the surfaces are fine or the scans are sparse, [ICP](/iterative-closest-point/) or [generalized ICP](/generalized-icp/) may be more accurate.

## Pitfalls

- **Cell size.** Cells much smaller than the motion give a small basin. Cells much larger than the detail of the scene give poor distributions, for example one ellipse over a corner. The right size depends on the scene and the sensor.
- **Singular covariance.** The points of a straight wall lie on a line, so $\Sigma$ is singular and $\Sigma^{-1}$ does not exist. Raise the small eigenvalues, or skip the cell.
- **Too few points.** A cell with 1 or 2 points has no useful covariance. The paper skips cells with fewer than 3 points; with sparse scans, many cells are skipped.
- **Hessian not positive definite.** Far from a minimum the Hessian of the score can be indefinite, and a plain Newton step can go uphill. Make it positive definite, or use a line search.
- **Jumps at cell boundaries.** A point that crosses a boundary changes its cell, so the cost jumps. The four shifted grids reduce this; a line search that tests the true cost is still needed.
- **Repeated structure.** A long corridor looks the same along its length, so the cost is nearly flat along it, and the pose drifts.

## Implementations

## History

Biber and Straßer presented NDT at IROS 2003 as a way to match 2D laser scans without explicit correspondences between points. Their method uses the cells with at least 3 points, four overlapping grids, and Newton steps. Magnusson, Lilienthal and Duckett extended NDT to 3D scans for autonomous mining vehicles in 2007, and Magnusson's 2009 thesis developed the 3D method further. NDT is now a standard tool for lidar localization against a prior map.

## References
