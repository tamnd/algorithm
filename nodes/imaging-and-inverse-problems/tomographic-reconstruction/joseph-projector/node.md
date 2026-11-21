---
tag: YFWYC3
kind: algorithm
slug: joseph-projector
name: Joseph's projector
aliases:
- Joseph's method
area: imaging-and-inverse-problems/tomographic-reconstruction
level: advanced
summary: Approximate a line integral through an image by linear interpolation between the two nearest pixel centers on each row or column the ray crosses.
model: real-ram
complexity:
  vars: {n: the side of the n x n image, a: the number of projection angles, d: the number of detector bins}
  time: {worst: "O(a d n)"}
  space: {extra: "O(1)"}
properties: {deterministic: true, in_place: false, recursive: false, iterative: false, linear: true}
history:
  year: 1982
  people: [Peter M. Joseph]
  note: Joseph proposed to reproject rays through a pixel image by stepping row by row and interpolating linearly between the two nearest pixels in each row.
prereqs: [radon-transform, bilinear-interpolation]
see_also: [siddon-algorithm, distance-driven-projector, back-projection-operator, sart, sirt, filtered-back-projection, x-ray-transform, sinogram]
sources:
  - paper: doi:10.1109/TMI.1982.4307572
    title: Peter M. Joseph, An improved algorithm for reprojecting rays through pixel images, IEEE Transactions on Medical Imaging 1(3), 1982
    locator: pp. 192 to 196 (the method as a whole; section numbers not confirmed)
  - paper: doi:10.1088/0031-9155/49/11/024
    title: Bruno De Man and Samit Basu, Distance-driven projection and backprojection in three dimensions, Physics in Medicine and Biology 49(11), 2004
    locator: pp. 2463 to 2475 (the comparison of pixel-driven, ray-driven and distance-driven projectors; general locator)
---

Joseph's projector computes an approximate line integral of an image along a ray, for the discrete model $y = A x$ of transmission tomography. It treats the image as a set of samples at the pixel centers, not as squares. The ray crosses each row of pixel centers at one point. There the method interpolates linearly between the two nearest samples in the row, and it adds the result times the length of the ray between two rows. If the ray is closer to horizontal, it steps column by column instead. Each ray costs $O(n)$ on an $n \times n$ image, with exactly two weights per row. The error is $O(h^2)$ for smooth images, with $h = 2/n$ the pixel size. The weights form a sparse matrix, and the back projector with the same weights is its exact transpose. Compare [Siddon's algorithm](/siddon-algorithm/), which gives the exact lengths of the ray in pixel squares, and the [distance-driven projector](/distance-driven-projector/), which integrates over the width of each detector bin.

## In plain words

Think of the image as a grid of measured values, one at the center of each pixel. A ray crosses the image. Pick the direction in which the ray changes slowly: if the ray is closer to vertical, walk down the rows; if it is closer to horizontal, walk across the columns.

At each row, the ray passes between two pixel centers. Estimate the value at the crossing point by a straight-line blend of the two neighbor values: the closer neighbor counts more. Multiply this estimate by the length of the ray between two rows, and add it to the total. When you reach the last row, the total is the projection. Each row gives exactly two weights, so the work is the same for every ray.

## The problem

The image is $n \times n$ on the square $[-1, 1]^2$, with $f[i][j]$ in row $i$ from the top and column $j$ from the left. The center of pixel $(i, j)$ is $x_j = -1 + (2j+1)/n$, $y_i = 1 - (2i+1)/n$, so $y$ goes up, and $h = 2/n$. A ray is the line $x\cos\theta + y\sin\theta = s$ of the [Radon transform](/radon-transform/). Its direction is $\omega^\perp = (-\sin\theta, \cos\theta)$. The task is to approximate $\mathcal{R}f(\theta, s) = \int f(s\omega + t\omega^\perp)\,dt$ from the samples $f[i][j]$, for all rays of a sinogram, and to give the transpose of this map for back projection.

## The algorithm

```pseudo id=main
JOSEPH(f, θ, s)                          ▷ c = cos θ, σ = sin θ, values outside the image are 0
L1  h ← 2/n, p ← 0
L2  if |c| ≥ |σ| then                     ▷ the ray is closer to vertical: step along rows
L3      Δ ← h / |c|
L4      for i ← 0 to n - 1 do
L5          x ← (s - y_i σ) / c, u ← ((x + 1) n - 1) / 2       ▷ u = j at the center x_j
L6          j ← ⌊u⌋, t ← u - j
L7          p ← p + Δ ((1 - t) f[i][j] + t f[i][j+1])
L8  else Δ ← h / |σ|                      ▷ the ray is closer to horizontal: step along columns
L9      for j ← 0 to n - 1 do y ← (s - x_j c) / σ, v ← ((1 - y) n - 1) / 2, i ← ⌊v⌋, t ← v - i
L10         p ← p + Δ ((1 - t) f[i][j] + t f[i+1][j])
L11 return p
```

Line L3 is the length of the ray between two neighboring rows of centers. Along the ray, $y$ changes at the rate $\cos\theta$, so a step of $h$ in $y$ is a step of $h/|\cos\theta|$ along the ray. Line L5 solves the equation of the ray for $x$ at the height $y_i$ and turns $x$ into a fractional column index. Line L7 is linear interpolation in the row. An index outside the image adds nothing. Lines L8 to L10 are the same with rows and columns exchanged.

The pairs (pixel, weight) of lines L7 and L10 are the nonzero entries of one row of the system matrix. The back projector runs the same loops and adds weight times the ray value to each pixel. It is the exact transpose of the forward projector.

## Example

Take $n = 4$, so $h = 1/2$, the centers $x_j \in \{-3/4, -1/4, 1/4, 3/4\}$ and $y_i \in \{3/4, 1/4, -1/4, -3/4\}$. Take $\cos\theta = 4/5$, $\sin\theta = 3/5$ and $s = 0$. Then $|c| \ge |\sigma|$, the code steps along rows, and $\Delta = (1/2)/(4/5) = 5/8$. The ray is $x = -3y/4$. Let the image be $f[i][j] = 4i + j + 1$.

| row $i$ | $y_i$ | $x$ | $u$ | $j$, $t$ | weights $\Delta(1-t)$, $\Delta t$ | interpolated value |
|---|---|---|---|---|---|---|
| 0 | $3/4$ | $-9/16$ | $3/8$ | $0$, $3/8$ | $25/64$, $15/64$ | $1 + 3/8 = 11/8$ |
| 1 | $1/4$ | $-3/16$ | $9/8$ | $1$, $1/8$ | $35/64$, $5/64$ | $6 + 1/8 = 49/8$ |
| 2 | $-1/4$ | $3/16$ | $15/8$ | $1$, $7/8$ | $5/64$, $35/64$ | $10 + 7/8 = 87/8$ |
| 3 | $-3/4$ | $9/16$ | $21/8$ | $2$, $5/8$ | $15/64$, $25/64$ | $15 + 5/8 = 125/8$ |

The interpolated values add up to $272/8 = 34$, and $p = (5/8) \cdot 34 = 85/4$. The weights in each row add up to $\Delta = 5/8$, and the eight weights add up to $5/2$, the length of the ray between $y = -1$ and $y = 1$. The test file checks all these values with `fractions.Fraction`.

The code below also measures accuracy on a $32 \times 32$ grid with 23 bins. For a constant image of value 1, it returns exactly 2 at $\theta = 0$ for every bin with $|s| < 1 - 1/n$, and exactly $2\sqrt{2}$ at $\theta = \pi/4$, $s = 0$. For a disk of radius $1/2$, sampled at the pixel centers, the largest error against $2\sqrt{1/4 - s^2}$ over 8 angles and the bins with $|s| < 0.35$ is $0.061$, less than one pixel width. For the smooth image $e^{-16|x|^2}$, the largest error against $\sqrt{\pi/16}\,e^{-16s^2}$ is $0.0162$ for $n = 16$, $0.0041$ for $n = 32$ and $0.0010$ for $n = 64$. These are measurements of this setup. The error falls by 4 when $n$ doubles, as the proof predicts.

## Correctness

Joseph's method is an approximation, so correctness here has two parts. First, the code computes the sum $\Delta\sum_i \phi_i(x(y_i))$, where $\phi_i$ is the linear interpolant of row $i$ with zero values outside the image. Lines L5 and L6 place the crossing point between the two centers $x_j$ and $x_{j+1}$ and give its fraction $t$, and line L3 is the length of the ray per row. Second, this sum approximates the line integral to second order. Write the line integral as $\frac{1}{|c|}\int_{-1}^{1} f(x(y), y)\,dy$. The sum over the rows is the midpoint rule for this integral, with error at most $h^2 M/3$ when the second partial derivatives of $f$ are bounded by $M$. Linear interpolation in each row adds at most $h^2 M/8$ per row, or $h^2 M/4$ in total. Since $|c| \ge 1/\sqrt{2}$, the total error is at most $(7\sqrt{2}/12)\,h^2 M$ for an image that vanishes near the border. The back projector uses the same weights, so it is the exact transpose. The full proof is in [proofs/correctness.md](proofs/correctness.md).

## Complexity

One ray visits $n$ rows (or columns) with $O(1)$ work each, so it costs $O(n)$ time and $O(1)$ extra space. A sinogram of $a$ angles and $d$ bins costs $O(a d n)$, and the back projection costs the same. The matrix has exactly $2n$ nonzero entries per row, fewer at the border, so it takes $O(a d n)$ memory if it is stored. The cost per ray does not depend on the angle or the offset, which makes the loops easy to vectorize. On a GPU, line L7 is one hardware texture fetch with linear filtering. In 3D, the method steps through the slices along the main direction and interpolates bilinearly in each slice, at $O(n)$ per ray on an $n \times n \times n$ volume.

## Properties

- **Linear and matched.** The projection is a linear map of the image, and the back projector with the same weights is its exact adjoint.
- **Smooth image model.** The method integrates the row-wise linear interpolant of the samples, not the pixel squares. For smooth images it is second order accurate. For an image with jumps, such as a disk, the error near a jump is of the order of one pixel, as for any discrete model.
- **Exact on the grid.** A ray through the centers of one column ($\theta = 0$, $s = x_j$) gives exactly $h$ times the column sum. A constant image gives exactly $2/|\cos\theta|$ for the rays that meet every row inside the outer centers.
- **Direction dependent model.** The interpolation runs along rows for some angles and along columns for others. At $\theta = \pi/4$ the method switches from one model to the other, so the weights of a ray change abruptly there. For a smooth image both models are second order, and the jump in the projection is small.
- **Ray-driven.** Like Siddon's algorithm, it samples the image along a ray of zero width. When the detector bins are wider than the pixels, the back projection of a smooth sinogram can show a moire pattern of high frequency.

## Variants and improvements

- **3D and cone beam.** Step through the slices perpendicular to the main axis of the ray and interpolate bilinearly in each slice. This is the common form in cone-beam iterative reconstruction.
- **Hardware interpolation.** On GPUs, the interpolation of line L7 or its 3D form uses the texture units. The forward projector is then very fast, but the back projector needs a separate kernel, and the two are often not exact transposes. Many codes accept this unmatched pair.
- **Siddon's algorithm.** The [exact intersection lengths](/siddon-algorithm/) model the image as pixel squares. They give a different matrix with a varying number of entries per row.
- **Distance-driven projection.** The [distance-driven projector](/distance-driven-projector/) maps the pixel borders and the bin borders onto one axis and uses their overlaps. It has no moire pattern in the back projection.
- **Pixel-driven projection.** The pixel-driven projector loops over pixels and splits each one between the two nearest bins. It is the natural back projector of [filtered back-projection](/filtered-back-projection/), but as a forward projector it has a ripple in the projections.

## When to use it

Use Joseph's projector as the forward and back projector of an iterative method such as [SART](/sart/) or [SIRT](/sirt/) when the image is smooth on the scale of a pixel and the detector bins are about as wide as a pixel. It costs the same for every ray, it vectorizes well, and it gives a smaller error than the pixel-square model on smooth images. Use [Siddon's algorithm](/siddon-algorithm/) when the model must be the exact path length in pixel squares, for example for dose calculation. Use the [distance-driven projector](/distance-driven-projector/) when the bins are much wider than the pixels or when the back projection must be free of artifacts.

## Pitfalls

- **Forgetting the factor $1/|\cos\theta|$.** Without line L3 the projection of a constant image depends on the angle. Test a constant image at $\theta = 0$ and $\theta = \pi/4$: the central values must be $2$ and $2\sqrt{2}$.
- **Wrong half-pixel offset.** The interpolation must use the pixel centers, so $u = j$ at $x = x_j$, which needs the $-1$ in line L5. An index measured from the pixel edge shifts the whole projection by half a pixel.
- **The border.** Near the edge of the image, one of the two neighbors is outside. It must count as zero, not be clamped to the edge value, or the projection of an image with nonzero border values grows outside the image.
- **Unmatched back projector.** A back projector that interpolates in the sinogram (pixel-driven) is not the transpose of Joseph's forward projector. An iterative method that assumes $A^T$, such as the [Landweber iteration](/landweber-iteration/), can then diverge or converge to a different point.
- **Choice of axis.** The test $|\cos\theta| \ge |\sin\theta|$ must select the axis along which the ray moves slowly. With the opposite choice, $\Delta$ can become very large near $\theta = \pi/2$ and the interpolation steps over many pixels.

## Implementations

The Python code computes the weights of one ray with float or `fractions.Fraction` input, the forward projector, the back projector and the sparse matrix, with the bins of the shared pixel-driven projector. The tests check the worked example exactly, axis-aligned rays, the adjoint, the matrix, a constant image, a disk, and the second order error on a Gaussian.

## History

Peter M. Joseph published the method in IEEE Transactions on Medical Imaging in 1982, in the first volume of the journal, as an improved way to reproject rays through pixel images. Its fixed cost per ray and its smooth image model made it a standard forward projector in iterative CT reconstruction. In 2002 and 2004, De Man and Basu compared ray-driven and pixel-driven projectors with their distance-driven projector, which removes the artifacts that thin rays give in the back projection.

## References
