---
tag: GTC8AH
kind: algorithm
slug: lidar-odometry-and-mapping
name: Lidar odometry and mapping
aliases:
- LOAM
area: robotics/localization-and-slam
level: research
summary: Zhang and Singh's lidar odometry and mapping, which matches edge and planar feature points at a high rate for odometry and at a low rate against the map.
solves: [slam-problem]
model: real-ram
complexity:
  vars: {n: the number of points of one scan, k: the half width of the smoothness window, f: the number of feature points of one scan, g: the number of Gauss-Newton iterations, m: the number of map points}
  time: {feature_extraction: O(n k + n log n), odometry_step: O(g f + n), mapping_step: O(g n)}
  space: {map: O(m)}
properties: {deterministic: true, exact: false, online: true, toy_code: true}
history:
  year: 2014
  people: [Ji Zhang, Sanjiv Singh]
  note: Zhang and Singh split lidar SLAM into a fast, coarse odometry and a slow, fine mapping step, both built on the matching of edge and planar feature points.
prereqs: [point-to-plane-icp, slam-problem]
see_also: [iterative-closest-point, normal-distributions-transform, correlative-scan-matching, range-image, iteratively-reweighted-least-squares, levenberg-marquardt, orb-slam, pose-graph-optimization]
sources:
  - paper: doi:10.15607/RSS.2014.X.007
    title: "Ji Zhang and Sanjiv Singh, LOAM: Lidar Odometry and Mapping in Real-time, Robotics: Science and Systems X, 2014"
    locator: "the smoothness value c, the choice of edge and planar points per subregion, the point-to-edge and point-to-plane distances, the bisquare weights and Levenberg-Marquardt, the odometry at 10 Hz and the mapping at 1 Hz"
  - paper: doi:10.1007/s10514-016-9548-2
    title: "Ji Zhang and Sanjiv Singh, Low-drift and real-time lidar odometry and mapping, Autonomous Robots 41(2), 2017, pages 401 to 416"
    locator: "the journal version, with the removal of motion distortion within a sweep, the map matching with the eigenvalues of the covariance of nearby map points, and the tests on the KITTI odometry benchmark"
---

Lidar odometry and mapping, LOAM, estimates the motion of a lidar and builds a map of point features at the same time. It splits the work between two algorithms that run at different rates. The odometry runs at the rate of the scans, 10 Hz in the paper. It matches a few feature points of the new scan to the previous scan and finds the motion between them. It is fast, but its errors add up. The mapping runs at a lower rate, 1 Hz in the paper. It matches many more feature points to the map, which is built from all earlier scans, and corrects the pose. Both algorithms use the same features. An edge point lies on a sharp edge of the scene, and a planar point lies on a flat surface. Edge points are matched to edge lines and planar points to planes, and the motion is found by nonlinear least squares with robust weights.

The code on this page is a toy. It works in the plane with a 2D scanner, its scans have no motion distortion, and it keeps only the feature extraction, the scan to scan odometry and the scan to map step. In the plane a surface is a line and an edge is a corner, so a flat point is matched to a line and a sharp point to a point.

## In plain words

A laser scanner spins and measures the distance to everything around it. To know how it moved, compare two scans. Most points on a flat wall look alike, so the method picks only two kinds of points: points on sharp corners and points on smooth flat parts. It asks how the new scan must move so that its corner points fall on the old corners and its flat points fall on the old walls. This guess is quick and is made for every scan, but small errors pile up. Less often, the method compares the new scan with the whole map made so far, which has many more points, and corrects the position. Then it adds the new points to the map.

## The problem

The input is a stream of lidar scans. Each scan is a list of points in the frame of the sensor, in the order of the beams. The output, after each scan, is the pose of the sensor relative to the first scan, and a map of feature points in that frame. The method must run in real time on one computer, and it has no other sensor. LOAM has no loop closure, so it is an odometry and mapping method, not a full solution of the [SLAM problem](/slam-problem/). The drift that the map does not remove stays.

In the toy, the poses are planar, $(t_x, t_y, \theta)$, and a scan has 360 beams over a full turn.

## The algorithm

```pseudo id=main
PROCESS-SCAN(points X_1 .. X_n in beam order)
L1  for each point i: c_i ← ‖Σ_{j ∈ S_i} (X_i - X_j)‖ / (|S_i| ‖X_i‖), with S_i the k beams on each side of i
L2  in each sector, take the points with the largest c as sharp and the smallest c as flat; skip points next to a range jump and points next to a chosen point
L3  if this is the first scan then add the features to the map M and return the pose 0
L4  motion T ← the last motion; repeat Gauss-Newton on T:
L5      for each flat point p: find the nearest flat point a of the last scan and a second one b next to it on the scan line; r ← the distance from T(p) to the line ab
L6      for each sharp point p: find the nearest sharp point a of the last scan; r ← T(p) - a
L7      weight each match by the bisquare of its distance; solve the weighted normal equations for the step and update T
L8  until the step is small
L9  pose ← pose ⊕ T; every m-th scan, refine pose by the same loop against M, with a line fitted to the nearest map points for each flat point
L10 every m-th scan, add the features at the refined pose to M, on a voxel grid
```

**The smoothness value (line L1).** The value $c_i$ is the distance from $X_i$ to the mean of its $2k$ neighbors on the scan line, divided by the range of $X_i$. It is near 0 on an evenly sampled flat surface and large at a corner. Because it is divided by the range, it does not change when the scene is scaled about the sensor, so one threshold works at all ranges.

**The choice of features (line L2).** LOAM splits each scan line into four subregions and takes at most two edge points and four planar points from each, so the features spread over the scene. It also rejects two kinds of unreliable points: points on a surface nearly parallel to the beam, and points at the edge of an occluded region, where the range jumps. A point that looks sharp only because the object behind it is far away is not a real edge, and it moves when the sensor moves. The toy uses six sectors, at most two sharp and eight flat points per sector, and rejects every point within $k + 1$ beams of a range jump of more than 10 percent.

**Odometry (lines L4 to L8).** The motion between two scans starts from the last motion, a constant velocity guess. In 3D, LOAM matches an edge point to the line through two edge points of the last sweep on nearby scan lines, and a planar point to the plane through three planar points. The residual is the distance to that line or plane. The matches are found again at each iteration. Each match gets a bisquare weight $(1 - (d/\tau)^2)^2$, which is zero for far matches, and LOAM takes Levenberg-Marquardt steps. The toy takes plain Gauss-Newton steps. LOAM also removes the motion distortion: a spinning lidar takes a sweep over a time interval, and each point is moved by the part of the motion that happened before it was measured, by linear interpolation of the pose in time.

**Mapping (lines L9 and L10).** The mapping step starts from the odometry pose and matches the features to the map. For each feature point, it takes the nearby map points and computes their covariance. For an edge, one eigenvalue must be much larger than the others, and its eigenvector is the direction of the line. For a plane, one eigenvalue must be much smaller, and its eigenvector is the normal. Then it solves the same robust least squares problem. LOAM keeps the map in a cube around the sensor and thins it with a voxel grid. The published pose is the last mapped pose combined with the odometry since then, so it comes out at the high rate.

## Example

**The smoothness value by hand.** Take $k = 5$ and eleven points: $(3, -0.5), (3, -0.4), \dots, (3, 0)$ on one wall and $(2.9, 0), (2.8, 0), \dots, (2.5, 0)$ on another, with $X_i = (3, 0)$ at the corner. The five differences along the first wall are $(0, 0.1), \dots, (0, 0.5)$, with sum $(0, 1.5)$. Along the second wall they sum to $(1.5, 0)$. So $c_i = \|(1.5, 1.5)\| / (10 \cdot 3) = 2.121 / 30 = 0.071$, above the edge threshold 0.05 of the toy. For eleven equally spaced points on one line, the differences cancel in pairs, and $c_i = 0$.

**A run of the toy.** The room is L-shaped, 12 m by 9 m, with two square pillars of side 0.8 m. The sensor drives on a circle of radius 1.8 m around one pillar, with 24 scans per lap, and takes 30 scans, a lap and a quarter. Each scan has 360 beams with range noise of standard deviation 0.03 m. The seed is 1. The first scan gives 8 sharp points, 33 flat points and 137 less flat points, which the mapping uses. Without noise, the same scan gives 3 sharp points, at room and pillar corners, and 251 less flat points, so the noise both adds false sharp points and moves points above the flat threshold. The mapping runs at every fifth scan.

| scan | odometry error (m) | mapped error (m) |
|---|---|---|
| 5 | 0.025 | 0.004 |
| 10 | 0.022 | 0.004 |
| 15 | 0.017 | 0.007 |
| 20 | 0.043 | 0.019 |
| 25 | 0.083 | 0.020 |
| 29 | 0.088 | 0.015 |

The largest position error is 0.090 m with odometry alone and 0.039 m with mapping. In the last quarter lap the sensor sees again the walls of the first scans, and the mapping pulls the pose back to the old map, while the odometry error keeps growing. At the end the map has 28 sharp and 522 flat points. On the seeds 1 to 6, the largest odometry error was 0.045 to 0.102 m and the largest mapped error was 0.022 to 0.058 m, between 0.37 and 0.61 times as large. These are measurements of a toy on simulated scans.

**Exact motion without noise.** With noise-free scans and flat points only, the odometry finds the motion $(0.2, 0.05, 0.04)$ to within $10^{-6}$ from the start $(0, 0, 0)$, because at the true motion every flat point lies on the wall of its match.

## Correctness

LOAM has no proof of accuracy. It is judged by measured drift, for example on the KITTI odometry benchmark. The [correctness proof](proofs/correctness.md) covers the toy. It shows that the smoothness value is the distance to the mean of the neighbors divided by the range, so it does not change under scaling and rotation about the sensor and is zero on evenly spaced collinear points; that the residuals are the distances to lines and points and the Jacobians are their derivatives; that on noise-free scans the true motion is a zero of the flat cost; that each step minimizes the weighted linearized cost; that the line fit uses the eigenvector of the larger eigenvalue and gives the least squares line; that the grid search returns exactly the points within the radius; and that the mapping never changes the odometry. It also says what is not proved: convergence from a far start, the bias of sharp points from the beam spacing, and any bound on the drift.

The tests check the smoothness value on a line and a corner with its invariance, the features of a scan of the room against the true corners and walls, the Jacobians against finite differences, the grid against brute force, the line fit, the exact recovery of two motions without noise, and the drift with and without mapping on two seeds.

## Complexity

Let $n$ be the number of points of a scan, $k$ the half width of the window, $f$ the number of feature points, $g$ the number of Gauss-Newton iterations and $m$ the number of map points.

- The smoothness values cost $O(n k)$, and sorting each sector costs $O(n \log n)$ in total.
- An odometry iteration finds one or two neighbors for each of the $f$ features. With a grid or a k-d tree over the points of the last scan and a bounded density of points, this costs $O(f)$ expected time per iteration, plus $O(n)$ to build the search structure once per scan.
- A mapping iteration matches all $O(n)$ less sharp and less flat points of the scan, with a small fixed number of map neighbors each. LOAM bounds the cost by keeping only the map in a cube around the sensor, so $m$ does not grow with the length of the run in the matching step.
- The map takes $O(m)$ space.

## Properties

- **Two rates.** The odometry gives a pose at every scan. The mapping corrects it at a lower rate, and the published pose combines the two.
- **Features, not all points.** Matching a few hundred features instead of all points makes each iteration cheap, compared with [ICP](/iterative-closest-point/) on whole scans.
- **Point-to-line and point-to-plane residuals.** As in [point-to-plane ICP](/point-to-plane-icp/), a point may slide along its surface without cost, which avoids wrong pairings of points between two samplings of the same surface.
- **Robust weights.** The bisquare weights make the estimate an [iteratively reweighted least squares](/iteratively-reweighted-least-squares/) fit that ignores far matches.
- **No loop closure.** Drift is reduced but never removed. A revisit helps only when the map near it is still accurate.

## Variants and improvements

- **V-LOAM.** Zhang and Singh added a camera, with visual odometry at a high rate and lidar odometry for refinement.
- **LeGO-LOAM.** Shan and Englot segmented the ground, used it for some degrees of freedom, and added loop closure with a pose graph.
- **LIO-SAM and other lidar-inertial methods.** An inertial sensor removes the motion distortion and gives the motion guess, and a factor graph with [iSAM2](/isam2/)-style smoothing joins lidar, inertial and loop factors.
- **A-LOAM and F-LOAM.** A-LOAM is a shorter open implementation of the same scheme. F-LOAM drops the scan to scan step and matches every scan to the map.
- **Other registration.** [NDT](/normal-distributions-transform/) and [correlative scan matching](/correlative-scan-matching/) match whole scans to a map without features. They are slower or coarser per scan, but they need no corners or flat surfaces.

## When to use it

Use LOAM or one of its successors for real-time lidar odometry and local mapping with a spinning lidar, in scenes with enough edges and surfaces, such as buildings and streets. Add an inertial sensor when the motion is fast, and add [loop closure detection](/loop-closure-detection/) with [pose graph optimization](/pose-graph-optimization/) when the robot returns to old places over long runs. In long corridors, tunnels and open fields, the features do not fix all degrees of freedom, and the estimate slides. Use the toy only to study the feature extraction and the two rates.

## Pitfalls

- **Degenerate scenes.** In a long corridor all flat points constrain only the motion across it, and the normal equations are nearly singular along it. A check on the eigenvalues of the normal matrix finds this.
- **Occlusion edges.** A point at the border of a near object in front of a far wall looks sharp but is not a fixed point of the scene. The range jump test removes it.
- **Motion distortion.** A sweep that is treated as one instant bends straight walls when the sensor moves fast.
- **Bad motion guess.** The matches are found from the guess. A sudden change of motion, with no inertial sensor, can make most matches wrong.
- **Beam spacing at corners.** The beam nearest a corner hits a wall up to one beam spacing away from it, so sharp point matches carry an error that grows with the range.

## Implementations

## History

Lidar scan matching for mobile robots goes back to the ICP of Besl and McKay (1992) and the work of Lu and Milios (1997) on 2D scans. Biber and Straßer (2003) gave NDT. Zhang and Singh (2014) presented LOAM at RSS. Their key ideas were the split into a fast odometry and a slow mapping step and the use of edge and planar feature points with point-to-line and point-to-plane distances. The journal version (2017) added detail and tests on the KITTI odometry benchmark, where LOAM was among the most accurate methods for years. LeGO-LOAM (2018) and LIO-SAM (2020) built on it, and its feature scheme is still the base of many lidar odometry systems.

## References
