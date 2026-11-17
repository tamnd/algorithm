---
tag: KZZVS0
kind: algorithm
slug: shot-descriptor
name: SHOT descriptor
aliases:
- signature of histograms of orientations
area: computer-vision/point-clouds-and-registration
level: advanced
summary: A 3D descriptor that builds a repeatable local reference frame from the neighbor covariance and histograms normal angles in a spherical grid around it.
model: real-ram
complexity:
  vars: {n: the number of points, k: the number of neighbors within the radius}
  time: {worst: O(n^2), average: O(n (log n + k)), best: Ω(n k)}
  space: {extra: Θ(n + k)}
properties: {deterministic: true, exact: true, online: false, recursive: false, rigid_motion_invariant: true, needs_normals: true}
history:
  year: 2010
  people: [Federico Tombari, Samuele Salti, Luigi Di Stefano]
  note: "Tombari, Salti and Di Stefano proposed a unique and repeatable local reference frame from a distance weighted covariance with a sign rule, and the SHOT descriptor that histograms normal cosines in a spherical grid fixed to this frame."
prereqs: [point-cloud-normal-estimation, principal-component-analysis, nearest-neighbor-search]
see_also: [point-feature-histograms, spin-images, shape-context, histogram-of-oriented-gradients, sift, feature-matching, covariance-matrix, point-cloud-registration]
sources:
  - paper: doi:10.1007/978-3-642-15558-1_26
    title: "Federico Tombari, Samuele Salti and Luigi Di Stefano, Unique signatures of histograms for local surface description, European Conference on Computer Vision (ECCV) 2010, Lecture Notes in Computer Science 6313"
    locator: "The local reference frame from the weighted covariance with the sign disambiguation, the spherical grid of 32 volumes, the histograms of normal cosines, the quadrilinear interpolation and the normalization"
  - paper: doi:10.1016/j.cviu.2014.04.011
    title: "Samuele Salti, Federico Tombari and Luigi Di Stefano, SHOT: Unique signatures of histograms for surface and texture description, Computer Vision and Image Understanding 125, 2014"
    locator: "The journal version: the reference frame, the descriptor, its color extension, and the experiments on repeatability and matching"
---

The SHOT descriptor (signature of histograms of orientations) describes the shape of a point cloud around one point by 352 numbers, for matching points between scans or between a model and a scene. Tombari, Salti and Di Stefano (2010) built it in two steps. First, a local reference frame: three axes at the point, computed from the neighbors alone, so that the same surface patch gets the same axes in any scan. The axes are the eigenvectors of a distance weighted [covariance matrix](/covariance-matrix/) of the neighbors around the point, with a sign rule that makes each axis point to the side with more neighbors. Second, a grid: the sphere around the point is cut, in this frame, into 32 volumes, and each volume holds a histogram of the angles between the neighbors' normals and the frame's $z$ axis. The frame makes the descriptor invariant to rotations, and the grid keeps where on the patch each normal sits. SHOT is more discriminative than [FPFH](/point-feature-histograms/) and [spin images](/spin-images/) on many benchmarks, at the cost of a longer vector and a frame that can be unstable on symmetric patches.

## In plain words

To compare a patch of one scan with a patch of another, you first need a common way to hold them. SHOT finds three directions on each patch from its own shape: the direction in which the patch spreads most, the direction in which it spreads least, and a third one at right angles to both. Each direction gets its sign from the side that has more points. Two copies of the same patch, turned in any way, get the same three directions.

Then it cuts the ball around the point into 32 pieces, like the slices of an orange, cut again into an upper and a lower half and into an inner and an outer part. In each piece it counts how much the surface normals tilt away from the main direction. The 32 small counts, one after the other, are the description.

## The problem

The input is a cloud of points with unit normals, a feature point $p$ and a radius $R$. The output is a vector of 352 numbers with unit length, such that patches of the same shape give close vectors, patches of different shapes give distant ones, and a rotation and translation of the cloud do not change the vector. As for every local descriptor, there is no single correct output; the requirements are invariance, repeatability under noise and a change of sampling, and the power to tell shapes apart.

## The algorithm

```pseudo id=main
SHOT(P, N, p, R)
L1  Q ← the points q_i of P with 0 < ‖q_i - p‖ < R, and d_i ← ‖q_i - p‖
L2  M ← Σ_i (R - d_i)(q_i - p)(q_i - p)ᵀ / Σ_i (R - d_i)
L3  (x⁺, y⁺, z⁺) ← the unit eigenvectors of M for its largest, middle and smallest eigenvalue
L4  x ← ±x⁺, with the sign for which more of the q_i - p have a positive projection
L5  z ← ±z⁺ by the same rule; y ← z × x
L6  h ← 352 zeros
L7  for each q_i in Q do
L8      (a, b, c) ← ((q_i - p) · x, (q_i - p) · y, (q_i - p) · z)
L9      v ← the volume of (a, b, c): one of 8 azimuth sectors, 2 halves by the sign of c, and 2 shells split at R/2
L10     k ← the bin of n_i · z among 11 equal bins of [-1, 1]
L11     h[11 v + k] ← h[11 v + k] + 1
L12 return h / ‖h‖
```

Lines L1 to L5 build the local reference frame. Unlike the covariance of [normal estimation](/point-cloud-normal-estimation/), the matrix of line L2 is centered at the feature point $p$, not at the centroid, and each neighbor has the weight $R - d_i$, so that far points, which are the first to change with clutter, count less. The axis $z$ plays the part of the normal, and $x$ is the direction of largest spread. Lines L4 and L5 fix the signs: each axis points to the side that holds more of the neighbors. The code breaks a tie in the counts by the sign of the sum of the projections.

Lines L6 to L11 fill the signature. The volume of line L9 comes from the azimuth $\operatorname{atan2}(b, a)$, cut in sectors of 45°, the sign of the elevation $c$, and whether the distance is below $R/2$. Line L10 bins the cosine, not the angle: equal steps of the cosine are coarse near the axis and fine near the tangent plane, where small changes of the normal matter more. The original method then spreads each count over the neighboring bins and volumes by quadrilinear interpolation, which makes the descriptor less sensitive to points near cell borders; the code below bins each count in one cell. Line L12 makes the vector a unit vector, so that point density does not change it much.

## Example

Take $p = (0, 0, 0)$, $R = 2$ and five neighbors on the surface $z = 0.2x^2 + 0.1y^2$, with the surface normals. The weighted covariance of line L2 gives the frame, to four places:

| axis | vector |
|---|---|
| $x$ | $(0.8239, 0.5517, 0.1293)$ |
| $y$ | $(-0.5538, 0.8323, -0.0225)$ |
| $z$ | $(-0.1201, -0.0531, 0.9913)$ |

The $z$ axis is close to the surface normal $(0, 0, 1)$ at $p$, tilted a little because the neighbors are not spread evenly. Then each neighbor goes to its cell:

| neighbor | local $(a, b, c)$ | distance | azimuth | volume | $n_i \cdot z$ | bin | entry |
|---|---|---|---|---|---|---|---|
| $(1, 0, 0.2)$ | $(0.850, -0.558, 0.078)$ | 1.020 | 326.7° | 31 | 0.965 | 10 | 351 |
| $(-0.5, 0, 0.05)$ | $(-0.406, 0.276, 0.110)$ | 0.503 | 145.8° | 14 | 0.949 | 10 | 164 |
| $(0, 0.8, 0.064)$ | $(0.450, 0.664, 0.021)$ | 0.803 | 55.9° | 6 | 0.987 | 10 | 76 |
| $(0, -0.4, 0.016)$ | $(-0.219, -0.333, 0.037)$ | 0.400 | 236.7° | 22 | 0.984 | 10 | 252 |
| $(0.6, 0.6, 0.108)$ | $(0.839, 0.165, 0.003)$ | 0.855 | 11.1° | 2 | 0.992 | 10 | 32 |

For the first neighbor, the azimuth 326.7° is in sector 7, the elevation is positive, so the half is 1, and the distance 1.020 is above $R/2 = 1$, so the shell is 1: the volume is $(7 \cdot 2 + 1) \cdot 2 + 1 = 31$, and the entry is $11 \cdot 31 + 10 = 351$. All normals are within 20° of $z$, so every count falls in the last cosine bin. The five entries get 1 each, and line L12 scales them to $1 / \sqrt 5 \approx 0.447$.

## Correctness

The matrix of line L2 is symmetric and positive semidefinite, and a rigid motion $x \mapsto Q x + t$ turns it into $Q M Q^\top$. When its three eigenvalues are distinct, its eigenvectors are fixed up to sign and move with the cloud. The sign rule of lines L4 and L5 gives the same axis whichever sign the eigenvalue solver returns, as long as the neighbors are not balanced on the two sides of the axis. Then $(x, y, z)$ is an orthonormal right handed frame that depends only on the neighborhood and moves with it, so every neighbor has the same local coordinates and the same cosine after the motion, and the descriptor does not change, up to values that lie exactly on cell borders. Each neighbor adds to exactly one of the 352 entries. The full proof is below.

## Complexity

The model is the [real RAM](/real-ram/), with $n$ points in the cloud and $k$ neighbors within the radius.

- **One descriptor.** The neighbor search costs $\Theta(n)$ by brute force, or $O(\log n + k)$ on average with a [k-d tree](/kd-tree/) on well-spread points. Line L2 costs $\Theta(k)$, line L3 is a $3 \times 3$ eigenproblem, $O(1)$, and lines L7 to L11 cost $\Theta(k)$. Line L12 costs $O(352) = O(1)$.
- **All points.** $O(n^2)$ by brute force and $O(n (\log n + k))$ with a tree.
- **Space.** $\Theta(k)$ for the neighbors and $O(1)$ for one descriptor, plus the tree.

In practice SHOT is computed at a few thousand keypoints, not at every point.

## Properties

- **Rigid motion invariant.** As long as the frame is defined, a rotation and translation of the cloud leave the descriptor unchanged.
- **Unique frame, when it exists.** The frame has no free choice, unlike frames that fix only the normal and leave the rotation about it open.
- **Unstable on symmetric patches.** On a plane, a sphere or a cylinder two eigenvalues are equal or close, and the $x$ axis can turn freely; the descriptor is then not repeatable.
- **Not scale invariant.** The radius sets the size of the patch.
- **Long.** 352 values, against 33 for FPFH, which makes matching slower and memory larger.
- **Sensitive to normal signs.** Flipping a neighbor's normal moves its count to the mirror bin. Orient the normals first, or use the absolute cosine.

## Variants and improvements

- **Color SHOT.** The journal version adds a second signature of color differences in the same grid, for scans with color.
- **Interpolation.** The original spreads each count over the neighboring cosine bins, azimuth sectors, halves and shells, which the code here leaves out.
- **Better sign rules.** Later work fixes the signs of the axes with more robust rules, for example from the points nearest to the median projection, which helps on balanced neighborhoods.
- **Other frames.** The frame of line L2 to L5 is used by other descriptors too, such as rotational projection statistics; other frames use the normal and a single dominant direction.
- **Learned descriptors.** Networks trained on scans give more discriminative descriptors and are slower and depend on their training data.

## When to use it

Use SHOT for 3D keypoint matching in object recognition and in the coarse registration of scans, when the surfaces have enough detail to fix the frame. It needs normals and a radius large enough to see a distinctive part of the shape, but small enough to avoid clutter. For fast registration of clean scans, [FPFH](/point-feature-histograms/) is cheaper. For clouds of simple shapes such as planes and cylinders, a local descriptor has little to work with: detect the shapes instead.

## Pitfalls

- **Centroid in place of the point.** Line L2 is centered at $p$, not at the centroid of the neighbors. Using the centroid changes the frame and makes it depend more on the sampling.
- **Eigenvalue order.** Line L3 needs $x$ for the largest eigenvalue and $z$ for the smallest. Solvers return them in different orders; a mix-up gives a frame that is still orthonormal but not the SHOT frame.
- **Signs from the solver.** Skipping lines L4 and L5 leaves signs that change from one run to the next or between two scans. The descriptor then fails to match even on identical data.
- **Left-handed frame.** Setting $y$ by its eigenvector at line L5, in place of $z \times x$, gives a reflected frame for about half of the points. The descriptor then confuses a shape with its mirror image.
- **Balanced neighborhoods.** When the counts of line L4 are tied, the sign is decided by noise. On a symmetric patch this happens often; check the gap between the counts and drop keypoints with a small gap.
- **The point itself.** Line L1 excludes $p$, which has distance 0 and adds nothing to $M$, but it would add a count to the histograms.

## Implementations

## History

Local 3D descriptors before SHOT fell into two groups, as Tombari, Salti and Di Stefano (2010) put it: signatures, which describe the neighborhood in a local frame by its geometric measurements at positions in that frame, and histograms, which count measurements over the whole neighborhood. Signatures are discriminative but need a repeatable frame; histograms are robust but lose the positions. Most frames of the time fixed only the normal, as in [spin images](/spin-images/), or were not unique. Tombari, Salti and Di Stefano proposed a unique frame from a weighted covariance around the feature point with a sign rule for the axes, and a descriptor that is a signature of histograms: one histogram of normal cosines in each volume of a spherical grid. Salti, Tombari and Di Stefano (2014) extended it with color and analyzed the frame further. SHOT is part of the Point Cloud Library and is a common baseline for 3D local descriptors.

## References
