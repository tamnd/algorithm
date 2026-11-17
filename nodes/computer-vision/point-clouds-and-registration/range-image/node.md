---
tag: M707AA
kind: data-structure
slug: range-image
name: Range image
aliases:
- depth image
- 2.5D image
area: computer-vision/point-clouds-and-registration
level: intro
summary: An image whose pixels store the distance to the scene along each ray, which gives a point cloud with grid neighbors.
model: real-ram
complexity:
  vars: {W: image width in pixels, H: image height in pixels, n: the number of input points of a build}
  time: {build: Θ(n + W H), query: Θ(1)}
  space: {extra: Θ(W H)}
properties: {deterministic: true, static: false, exact: true}
history:
  year: 1988
  people: [Paul J. Besl]
  note: "Besl surveyed the active optical sensors that measure range images, by radar (time of flight), triangulation, moire, holographic interferometry, focusing and diffraction. Curless and Levoy (1996) merged many range images into one model, and cheap depth cameras from 2010 on made depth images a common input."
prereqs: [point-cloud, pinhole-camera-model, digital-image]
see_also: [z-buffer, depth-from-disparity, structured-light-scanning, tsdf-fusion, point-cloud-normal-estimation, camera-intrinsic-matrix, lidar-odometry-and-mapping, iterative-closest-point]
sources:
  - paper: doi:10.1007/BF01212277
    title: "Paul J. Besl, Active, optical range imaging sensors, Machine Vision and Applications 1(2), 1988, 127-152"
    locator: "The range image as the output of a sensor, and the survey of the measuring principles"
  - paper: doi:10.1145/237170.237269
    title: "Brian Curless and Marc Levoy, A volumetric method for building complex models from range images, SIGGRAPH 96, 303-312"
    locator: "Range images as the input of a model, merged into a cumulative weighted signed distance function"
  - book: isbn:9783030343712
    title: "Richard Szeliski, Computer Vision, Algorithms and Applications, second edition, Springer, 2022"
    locator: "Chapter 13, 3D reconstruction (range data and its merging)"
---

A range image is a 2D grid of numbers in which each cell holds the distance from a sensor to the first surface along one ray. It is a [digital image](/digital-image/) where the value of a [pixel](/pixel/) is a distance, not a brightness. Depth cameras, laser scanners and [stereo matching](/stereo-matching/) produce range images. Each valid cell gives one 3D point, so a range image is a [point cloud](/point-cloud/) whose points come with a grid: the four cells around a cell are its neighbors, often also on the surface. This makes neighbor search and normal estimation cost $O(1)$ per point, without a [k-d tree](/kd-tree/). The value is either the depth $Z$ along the optical axis, as in a *depth image*, or the Euclidean range $\|X\|$ to the sensor; the two differ by a known factor per pixel. The name 2.5D says that the image holds one surface per ray, the one seen from the sensor, not a full 3D model.

## In plain words

Take a photograph, but in each pixel write down how far away the thing in that pixel is, in meters, instead of its color. That is a range image. A blank pixel means the sensor saw nothing there, for example the sky or a black surface.

Because you know where the camera was and which way each pixel looks, you can turn every pixel back into a point in space: go out along the pixel's ray by the stored distance. The pixels next to each other in the grid are usually next to each other on the object too, so the grid already tells you the neighbors of each point. The exception is the edge of an object, where the next pixel jumps to the background far behind.

## The abstract type

A range image is a $W \times H$ grid of cells with a camera model. Each cell is empty or holds one depth. It supports:

- **BUILD$(P)$** makes the image of a point cloud $P$ seen by the camera: each cell gets the depth of the nearest point that projects into it.
- **BACK-PROJECT$(u, v)$** returns the 3D point of the cell $(u, v)$, or nothing if the cell is empty.
- **RANGE$(u, v)$** returns the distance $\|X\|$ of that point to the camera center.
- **NEIGHBORS$(u, v, \tau)$** returns the valid 4-neighbors of a cell whose depth differs from its depth by at most $\tau$.
- **NORMAL$(u, v, \tau)$** returns a unit surface normal at the cell from its neighbors, turned toward the camera.
- **TO-CLOUD** lists the points of all valid cells, row by row, an organized point cloud.

A cell can also be written directly, which is how a sensor fills the image.

## Representation

This page uses the [pinhole camera](/pinhole-camera-model/) with the conventions of the area: the camera frame has $X$ to the right, $Y$ down and $Z$ forward, along the optical axis. (The graphics page of the pinhole camera looks along $-w$ instead.) The [intrinsic matrix](/camera-intrinsic-matrix/) is $K = [[f_x, 0, c_x], [0, f_y, c_y], [0, 0, 1]]$, the pixel $(u, v)$ has column $u$ and row $v$, and the grid is stored as $\mathrm{img}[v][u]$. The center of pixel $(u, v)$ is the image point $(u, v)$, and its ray is

$$r(u, v) = (a, b, 1), \qquad a = \frac{u - c_x}{f_x}, \quad b = \frac{v - c_y}{f_y}.$$

A cell stores the depth $Z$. The point of the cell is $X = Z\, r(u, v)$, and its range is $\|X\| = Z \sqrt{1 + a^2 + b^2}$. A range image that stores $\|X\|$ converts to depth by dividing by the same factor, which depends only on the pixel. Empty cells hold a marker: here `None`, in files often 0 or NaN.

A lidar that spins about a vertical axis gives a different grid: one row per laser beam, one column per azimuth angle, and the range in each cell. The ray of a cell then comes from the two angles, not from $K$, but the rest of this page is the same.

## Operations

```pseudo id=main
BUILD(P, W, H, K)                        ▷ a z-buffer: keep the nearest point per pixel
L1  img ← a W × H grid of empty cells
L2  for each point X = (X₁, X₂, X₃) in P do
L3      if X₃ ≤ 0 then skip X              ▷ behind the camera
L4      u ← ⌊f_x X₁/X₃ + c_x + 1/2⌋, v ← ⌊f_y X₂/X₃ + c_y + 1/2⌋
L5      if (u, v) is outside the grid then skip X
L6      if img[v][u] is empty or X₃ < img[v][u] then
L7          img[v][u] ← X₃
L8  return img
```

BUILD is the [z-buffer](/z-buffer/) of computer graphics, applied to points. Line L4 rounds the projection to the nearest pixel center, so the pixel $(u, v)$ owns the square $[u - \tfrac12, u + \tfrac12) \times [v - \tfrac12, v + \tfrac12)$. Lines L6 and L7 keep the nearest point, the one the sensor would see.

```pseudo id=ops
BACK-PROJECT(img, u, v)
L9  Z ← img[v][u]; if Z is empty then return nothing
L10 return Z · ((u - c_x)/f_x, (v - c_y)/f_y, 1)

NEIGHBORS(img, u, v, τ)
L11 for each (u', v') in (u ± 1, v) and (u, v ± 1) do
L12     if (u', v') is outside the grid then skip it
L13     if img[v'][u'] is not empty and |img[v'][u'] - img[v][u]| ≤ τ then
L14         report (u', v')

NORMAL(img, u, v, τ)                     ▷ X is BACK-PROJECT(img, u, v)
L15 Δu ← right point - left point, Δv ← lower point - upper point   ▷ from NEIGHBORS; one-sided if a side is missing, give up if both are
L16 n ← Δu × Δv
L17 n ← n / ‖n‖
L18 if n · X > 0 then n ← -n            ▷ turn n toward the camera
L19 return n
```

The test at line L13 is what separates a range image from a plain image grid. Two adjacent cells on either side of the edge of an object hold depths that differ a lot, and their points are not neighbors on any surface. The threshold $\tau$ cuts these links. A good $\tau$ grows with the depth, because the gap between the points of two adjacent pixels on a slanted surface grows with $Z$.

Line L16 takes the cross product of two tangent directions, which gives a normal in $O(1)$ time per cell. For less noise, fit a plane to a larger window of cells as in [point cloud normal estimation](/point-cloud-normal-estimation/); the window is still found in $O(1)$ time per cell.

## Example

Use a $3 \times 2$ image with $f_x = f_y = 2$, $c_x = 1$, $c_y = 0.5$. BUILD gets five points.

| point | projection | pixel | result |
|---|---|---|---|
| $(0, -0.5, 2)$ | $(1, 0)$ | $(1, 0)$ | stored, $Z = 2$ |
| $(0, -1, 4)$ | $(1, 0)$ | $(1, 0)$ | hidden: $4 > 2$ |
| $(-1, 0.5, 2)$ | $(0, 1)$ | $(0, 1)$ | stored, $Z = 2$ |
| $(1, 0.25, 1)$ | $(3, 1)$ | $(3, 1)$ | outside the grid |
| $(0.2, 0, -1)$ | none | none | behind the camera |

The grid is then

| | $u = 0$ | $u = 1$ | $u = 2$ |
|---|---|---|---|
| $v = 0$ | empty | 2 | empty |
| $v = 1$ | 2 | empty | empty |

BACK-PROJECT of $(1, 0)$ uses the ray $(0, -0.25, 1)$ and returns $2 \cdot (0, -0.25, 1) = (0, -0.5, 2)$, the first point again. Its range is $2\sqrt{1 + 0.0625} = 2.0616$, a little more than its depth, because the pixel is off the optical axis. The second point is lost: a range image holds one surface per ray.

## Correctness

Line L4 gives the pixel $(u, v)$ exactly when the projection lies in the square of that pixel, by the definition of the floor. An induction over the points then shows that after BUILD each cell holds the least depth among the points with positive depth that project into its square. BACK-PROJECT returns the point of that depth on the ray through the pixel center; it projects back to $(u, v)$ with the same depth, so a cloud with one point on each pixel ray is rebuilt exactly. NORMAL returns the exact plane normal, turned toward the camera, whenever the neighbors it uses lie on one plane. The full proof is below.

## Complexity

The model is the [real RAM](/real-ram/) with the floor function.

| operation | time | notes |
|---|---|---|
| BUILD of $n$ points | $\Theta(n + WH)$ | $\Theta(WH)$ to clear the grid, $O(1)$ per point |
| BACK-PROJECT, RANGE | $\Theta(1)$ | one ray and one product |
| NEIGHBORS, NORMAL | $\Theta(1)$ | four cells |
| TO-CLOUD | $\Theta(WH)$ | one pass over the grid |
| space | $\Theta(WH)$ | one number per cell |

Compare an unorganized cloud of $n$ points, where each neighbor query needs a search structure, such as a [k-d tree](/kd-tree/) with an $O(n \log n)$ build and about $O(\log n)$ per query on well-spread points.

## Variants

- **Depth image and range image.** Depth cameras usually store $Z$, and scanners usually store $\|X\|$. Both are called range images. Check which one a file holds before back-projection.
- **Spherical range image.** A rotating lidar has one row per beam and one column per azimuth step. Many lidar methods, such as [LOAM](/lidar-odometry-and-mapping/), use this grid for fast neighbors along a scan line.
- **Disparity image.** Stereo gives a [disparity](/disparity/) $d$ per pixel, with $Z = f B / d$ for the baseline $B$. It is stored as an image and turned into depth by [depth from disparity](/depth-from-disparity/).
- **Multi-return and multi-layer images.** Some scanners record several returns per ray, from glass, leaves or rain. A layered depth image keeps several depths per pixel, which is no longer 2.5D.
- **Mesh from the grid.** Join each $2 \times 2$ block of valid cells into two triangles, and drop triangles across depth jumps. This gives a mesh of the visible surface in $\Theta(WH)$ time.
- **Fusion.** [TSDF fusion](/tsdf-fusion/) merges many depth images into one volume, following Curless and Levoy (1996).

## When to use it

Keep data as a range image as long as possible when it comes from one sensor position: neighbors, normals, edges and meshes are cheap on the grid, and it takes less space than a list of points. Use the grid to find depth edges, which are the jumps of line L13. Convert to an unorganized point cloud when you merge views from several positions, since the points of two views no longer share a grid. Do not use a single range image when you need the parts of the scene behind the first surface.

## Pitfalls

- **Depth where range is stored.** Using a range value as $Z$ at line L10 puts off-axis points too far away and bends planes into bowls. Divide a range by $\sqrt{1 + a^2 + b^2}$ first.
- **Pixel corner or pixel center.** Some programs put the pixel center at $(u + \tfrac12, v + \tfrac12)$. Mixing the conventions at lines L4 and L10 shifts every point by half a pixel. Use the same convention in both.
- **Zero as a depth.** Many files store 0 for an empty cell. Back-projecting it at line L10 gives points at the camera center, which spoil means and fits. Test for the marker first.
- **No jump test.** Leaving out the test $|Z' - Z| \le \tau$ at line L13 links the foreground to the background at every object edge. Normals there point sideways, and a mesh gets long, thin triangles across empty space.
- **A fixed jump threshold.** A $\tau$ that is right at 1 m cuts real surfaces at 10 m, because the spacing grows with $Z$. Scale $\tau$ with the depth, or test the angle between the ray and the line between the two points.

## Implementations

## History

Range images came with the first range sensors for robots and industrial inspection. Besl (1988) surveyed the active optical sensors that produce them and classified them by principle: radar, which measures the time of flight, triangulation, moire, holographic interferometry, focusing and diffraction. Curless and Levoy (1996) merged dozens of range images of one object into a single model with a cumulative signed distance function, the base of later depth fusion. Low-cost depth cameras, from structured light and then from time of flight, made depth images at video rate a common input of computer vision and robotics after 2010.

## References
