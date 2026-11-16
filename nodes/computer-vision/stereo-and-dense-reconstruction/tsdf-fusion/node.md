---
tag: AYN2F8
kind: algorithm
slug: tsdf-fusion
name: TSDF fusion
aliases:
- Curless-Levoy volumetric fusion
- truncated signed distance fusion
- KinectFusion volumetric integration
area: computer-vision/stereo-and-dense-reconstruction
level: advanced
summary: "Fuse many depth images into a voxel grid by a weighted running average of truncated signed distances to the surface, then extract the zero level set as the fused surface."
solves: [surface-reconstruction]
model: real-ram
complexity:
  vars: {N: the number of depth images, n: the number of voxels along each side of the grid}
  time: {worst: Θ(N n^3), average: Θ(N n^3), best: Θ(N n^3)}
  space: {extra: Θ(n^3)}
properties: {deterministic: true, exact: false, online: true, recursive: false}
history:
  year: 1996
  people: [Brian Curless, Marc Levoy]
  note: "Curless and Levoy fused range scans by averaging weighted signed distances on a grid. Newcombe et al. (KinectFusion, 2011) ran the same update in real time on a GPU for a moving depth camera."
prereqs: [signed-distance-function, pinhole-camera-model, range-image]
see_also: [depth-map-fusion, marching-cubes, isosurface-extraction, point-to-plane-icp, ray-casting, occupancy-grid-mapping, space-carving, poisson-surface-reconstruction]
sources:
  - paper: doi:10.1145/237170.237269
    title: "Brian Curless and Marc Levoy, A volumetric method for building complex models from range images, SIGGRAPH 1996, pages 303 to 312"
    locator: "the cumulative signed distance and weight functions and their incremental update, the ramp that limits the distance near the surface, hole filling with the unseen, empty and near-surface states, and Appendix A (the isosurface as a least squares minimizer)"
  - paper: doi:10.1109/ISMAR.2011.6092378
    title: "Richard A. Newcombe, Shahram Izadi, Otmar Hilliges, David Molyneaux, David Kim, Andrew J. Davison, Pushmeet Kohli, Jamie Shotton, Steve Hodges and Andrew Fitzgibbon, KinectFusion: Real-time dense surface mapping and tracking, IEEE International Symposium on Mixed and Augmented Reality 2011, pages 127 to 136"
    locator: "the surface reconstruction update (the projective truncated signed distance and the weighted running average), surface prediction by ray casting, and tracking by ICP against the predicted surface"
  - paper: doi:10.1561/0600000052
    title: "Yasutaka Furukawa and Carlos Hernández, Multi-view stereo: a tutorial, Foundations and Trends in Computer Graphics and Vision 9(1-2), pages 1 to 148, 2015"
    locator: the discussion of volumetric fusion of depth maps
  - book: isbn:9783030343712
    title: "Richard Szeliski, Computer Vision, Algorithms and Applications, second edition, Springer, 2022"
    locator: "Section 13.2.1, Range data merging, and Section 13.5, Volumetric representations"
---

TSDF fusion builds one surface from many depth images, for example scans from a laser scanner or frames from a depth camera. It cuts space into a grid of small cubes, called voxels. For each depth image and each voxel, it computes how far the voxel is in front of or behind the measured surface along the line of sight, cuts this signed distance off at a small band $\mu$ (the truncation), and adds it to a weighted running average stored in the voxel. The surface is where the averaged distance is zero, and [marching cubes](/marching-cubes/) turns it into a mesh. Averaging removes much of the noise of single scans, and the grid can grow one image at a time. [Depth map fusion](/depth-map-fusion/) is the general technique of merging depth maps; TSDF fusion is its volumetric algorithm, by Curless and Levoy (1996), which KinectFusion made real time.

## In plain words

Imagine a room filled with a grid of tiny boxes. Each time a depth camera takes a picture, every box near the measured surface writes down a number: positive if it is in front of the surface, negative if it is behind, and larger the farther it is, up to a small limit. Each box keeps the average of all the numbers it got, giving more weight to readings it trusts more. Boxes far in front of every surface say plus one, and boxes far behind it say nothing, because no camera saw them. The surface lies where the averages change from positive to negative. One noisy picture gives a rough surface, but many pictures average out to a smooth one.

## The problem

**Input.**

- Depth images $Z_1, \dots, Z_N$. $Z_i[v][u]$ is the depth of the surface at pixel $(u, v)$ in camera $i$, or empty where the sensor gave no reading.
- The cameras $(K_i, R_i, t_i)$ with $X_c = R_i X + t_i$ (see [pinhole camera model](/pinhole-camera-model/)), all in one world frame.
- A grid of $n \times n \times n$ voxels of size $h$, a truncation distance $\mu$ of a few voxels, and a weight $w_i > 0$ per image or per pixel.

**Output.** For each voxel, a value $D \in [-1, 1]$ and a weight $W \ge 0$. $D$ is the weighted mean of the truncated distances divided by $\mu$, and $W = 0$ marks a voxel that no image has seen. The surface is the zero level set of $D$ over the seen voxels. In the sense of a [signed distance function](/signed-distance-function/), $D$ is positive outside the object, toward the cameras.

## The algorithm

```pseudo id=main
TSDF-INTEGRATE(D, W, Z, (K, R, t), μ, w)
L1  for each voxel x with center X do
L2      X_c ← R X + t; if Z_c ≤ 0 then skip x
L3      (u, v) ← the pixel nearest to the projection of X_c; if it is outside the image or Z[v][u] is empty then skip x
L4      η ← Z[v][u] - Z_c                       ▷ signed distance along the line of sight
L5      if η < -μ then skip x                     ▷ far behind the surface: not seen
L6      f ← min(1, η / μ)
L7      D[x] ← (W[x] D[x] + w f) / (W[x] + w); W[x] ← W[x] + w
```

Call TSDF-INTEGRATE once per depth image. To extract the surface, find the pairs of neighboring seen voxels where $D$ changes sign and place a point between them by linear interpolation. The code does this along one axis; [marching cubes](/marching-cubes/) does it on all edges of each cube and links the points into triangles.

**Line L4, the distance.** $\eta$ is the difference of depths along the line of sight, as in KinectFusion. It is zero exactly on the measured surface, but on a slanted surface it is larger than the true distance to the surface by the factor $1 / \cos \theta$, where $\theta$ is the angle between the line of sight and the normal.

**Lines L5 and L6, the truncation.** In front of the surface, the distance is cut off at 1, which marks free space. Behind the surface, the camera saw nothing, so voxels more than $\mu$ behind it get no reading. This keeps a thin object from being wiped out by readings from the other side.

**Line L7, the update.** This is the running form of the weighted mean, so the images can come one at a time and in any order. Curless and Levoy set the weight from the angle between the line of sight and the surface normal and lower it near the edges of a scan, where range data are less reliable.

## Example

**One line of sight.** A camera at the origin looks along the $z$ axis, and four voxels on the axis have centers at $z = 1.975, 2.000, 2.025, 2.050$. Three depth images read the depth on the axis as $2.00$, $2.03$ and $1.98$, with weights 1, 2 and 1. The truncation is $\mu = 0.05$.

| voxel $z$ | $f_1$ | $f_2$ | $f_3$ | $D$ | $W$ |
|---|---|---|---|---|---|
| 1.975 | 0.5 | 1 (cut off from 1.1) | 0.1 | 0.65 | 4 |
| 2.000 | 0 | 0.6 | -0.4 | 0.2 | 4 |
| 2.025 | -0.5 | 0.1 | -0.9 | -0.3 | 4 |
| 2.050 | -1 | -0.4 | none ($\eta = -0.07$) | -0.6 | 3 |

The sign changes between $z = 2.000$ and $z = 2.025$. Linear interpolation gives $2.000 + 0.025 \cdot 0.2 / 0.5 = 2.010$, which is the weighted mean $(2.00 + 2 \cdot 2.03 + 1.98) / 4 = 2.01$ of the readings.

**A noisy sphere.** The test file renders a sphere of radius 1 at a distance of 3 from eight cameras near the origin, with $32 \times 32$ depth images and Gaussian noise of standard deviation $0.02$ on every depth. On a grid of $24 \times 24 \times 14$ voxels of size $0.1$ with $\mu = 0.15$, the surface points near the center of the view from one image are on average $0.0125$ from the true sphere. After fusing all eight images, the mean error is $0.0050$.

## Correctness

The full proof is in [proofs/correctness.md](proofs/correctness.md).

1. **Running mean.** By induction over the images, line L7 keeps $W = \sum w_i$ and $D = \sum w_i f_i / \sum w_i$ over the images that gave the voxel a reading. So the result does not depend on the order of the images.
2. **Least squares.** Along a line of sight on which every reading lies within $\mu$ of two neighboring voxels, $D$ is linear in the depth: $D(z) = (\bar z - z) / \mu$ with $\bar z = \sum w_i z_i / \sum w_i$. Linear interpolation therefore puts the surface at $\bar z$, which is the minimizer of $\sum w_i (z - z_i)^2$.

This is a theorem only inside the truncation band and along a common line of sight. Curless and Levoy show in an appendix that the zero set still minimizes a weighted sum of squared distances when the lines of sight are nearly parallel and the weights change slowly. Outside these conditions, the method is a well-tested heuristic.

## Complexity

The model is the real RAM. Each image visits every voxel once, with constant work per voxel, so integration takes $\Theta(n^3)$ per image and $\Theta(N n^3)$ for all images, in every case. Extraction takes $\Theta(n^3)$. The grid stores $D$ and $W$ for each voxel, $\Theta(n^3)$, and the images can be dropped after integration. An implementation that updates only the voxels in the band near each measured surface, as sparse grids do, spends time in proportion to the area of the surface times $\mu / h$ instead of the volume.

## Properties

- **Online.** Each image is used once and can be dropped. The cost of one update does not depend on how many images came before.
- **Order independent.** The fused grid is the same for any order of the images, up to rounding.
- **Least squares surface.** Under the conditions above, the zero set is the weighted mean of the readings.
- **Any topology.** The zero set can have any number of parts and holes, and needs no initial shape.
- **Fixed resolution.** The grid limits the detail to about the voxel size $h$ and needs $\Theta(n^3)$ memory, even though the surface fills only a thin layer.

## Variants and improvements

- **Hole filling.** Curless and Levoy also mark voxels as unseen, empty or near the surface. They then put a surface between unseen and empty voxels, which closes the holes of the model in a way that is consistent with the scans.
- **Real-time fusion.** KinectFusion runs line L7 for every voxel on a GPU at camera frame rate. It finds the pose of each new frame by [point-to-plane ICP](/point-to-plane-icp/) against a surface that it predicts by [ray casting](/ray-casting/) the grid, and caps the weight so that the model can follow slow changes in the scene.
- **Sparse grids.** Voxel hashing and [octrees](/octree/) store only the blocks of voxels near the surface, which makes large scenes fit in memory.
- **Occupancy instead of distance.** An [occupancy grid](/occupancy-grid-mapping/) stores a probability of being occupied per cell. It is the robotics counterpart and has no subvoxel surface.
- **Other surfaces from depth.** [Poisson surface reconstruction](/poisson-surface-reconstruction/) fits an indicator function to oriented points instead of averaging distances on a grid.

## When to use it

Use TSDF fusion when you have many depth images with known poses, from a range scanner, a depth camera, or [multi-view stereo](/multi-view-stereo/), and you want a closed, smooth mesh at a resolution that fits in memory. It is simple, runs well on a GPU, and handles new images as they come. For a few depth maps with many outliers, use a voting form of [depth map fusion](/depth-map-fusion/) first, since one far outlier with a high weight moves the averaged surface. For thin structures thinner than the band $\mu$, and for very large scenes, use a sparse grid or a point-based method.

## Pitfalls

- **Thin objects.** Readings from the back of a thin object reach the front voxels through the band behind the surface and pull the surface back. Keep $\mu$ smaller than the thickness of the thinnest part you want to keep.
- **Too small a band.** If $\mu$ is less than the noise or than about two voxels, neighboring voxels do not both get readings, and the surface breaks into holes.
- **Projective distance.** On slanted surfaces $\eta$ is larger than the true distance, so the band is wider than $\mu$ and readings from different directions are scaled differently. Weighting by the angle to the normal reduces the effect.
- **Pose errors.** The fusion assumes exact poses. A small error in one pose blurs or doubles the surface. KinectFusion tracks each frame against the model to keep poses consistent.
- **Sign convention.** Here $D > 0$ in front of the surface. Some code uses the opposite sign. Mixing the two puts the mesh normals inside out.
- **Nearest pixel.** Rounding the projection to the nearest pixel, as the code does, gives staircase artifacts at depth edges. Bilinear interpolation of the depth helps on smooth surfaces but blurs edges.

## Implementations

## History

Curless and Levoy (1996) introduced the weighted average of signed distances on a grid to merge range scans from a laser scanner into one model. They showed that the zero set is a least squares surface, added hole filling with the unseen and empty states, and used marching cubes for the mesh. Newcombe, Izadi and co-authors (2011) used the same update in KinectFusion, which tracked a moving depth camera and fused its frames on a GPU in real time. Later systems made the grid sparse, with voxel hashing or octrees, to scale to rooms and buildings.

## References
