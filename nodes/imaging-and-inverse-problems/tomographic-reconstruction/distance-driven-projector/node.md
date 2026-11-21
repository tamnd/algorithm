---
tag: MVREDC
kind: algorithm
slug: distance-driven-projector
name: Distance-driven projector
aliases:
- distance-driven projection
area: imaging-and-inverse-problems/tomographic-reconstruction
level: advanced
summary: A matched forward and back projector for CT that maps pixel borders and detector bin borders onto one axis and uses the lengths of their overlaps as weights.
model: real-ram
complexity:
  vars: {n: the side of the n x n image, a: the number of projection angles, d: the number of detector bins}
  time: {worst: "O(a n (n + d))"}
  space: {extra: "O(n + d)"}
properties: {deterministic: true, in_place: false, recursive: false, iterative: false, linear: true}
history:
  year: 2002
  people: [Bruno De Man, Samit Basu]
  note: De Man and Basu presented the method at the IEEE Nuclear Science Symposium and Medical Imaging Conference in 2002 and extended it to three dimensions in 2004.
prereqs: [radon-transform, sparse-matrix]
see_also: [siddon-algorithm, joseph-projector, back-projection-operator, sinogram, sart, sirt, filtered-back-projection, x-ray-transform]
sources:
  - paper: doi:10.1109/NSSMIC.2002.1239600
    title: Bruno De Man and Samit Basu, Distance-driven projection and backprojection, 2002 IEEE Nuclear Science Symposium Conference Record, vol. 3, 2002
    locator: pp. 1477 to 1480 (the 2D method, the comparison with pixel-driven and ray-driven projectors)
  - paper: doi:10.1088/0031-9155/49/11/024
    title: Bruno De Man and Samit Basu, Distance-driven projection and backprojection in three dimensions, Physics in Medicine and Biology 49(11), 2004
    locator: pp. 2463 to 2475 (the 3D form with the overlaps computed separately in the two detector directions; general locator)
  - book: isbn:9780898714944
    title: A. C. Kak and M. Slaney, Principles of Computerized Tomographic Imaging, SIAM Classics in Applied Mathematics 33, 2001
    locator: Chapter 7, algebraic reconstruction algorithms (the system matrix of the discrete model y = A x)
---

The distance-driven projector computes the system matrix $A$ of the discrete model $y = A x$ of transmission tomography, where $x$ holds the pixel values and $y$ the detector readings of a [sinogram](/sinogram/). For one view it takes each row of pixels (or each column, for a ray closer to horizontal), maps the borders of the pixels in that row and the borders of the detector bins onto one common axis, and uses the length of the overlap of each pixel and each bin as the weight. The back projector uses the same weights, so it is the exact transpose. One view costs $O(n(n + d))$ for an $n \times n$ image and $d$ bins. De Man and Basu designed it to remove the two known faults of the simpler projectors: the pixel-driven projector gives a high frequency ripple in the forward projection, and ray-driven projectors such as [Siddon's algorithm](/siddon-algorithm/) and [Joseph's projector](/joseph-projector/) give a similar artifact in the back projection when the bins are wide.

## In plain words

Look at one row of pixels from the direction of the rays. Each pixel casts a shadow on the detector line. The shadows of the pixels in one row lie side by side, with no gap and no overlap. The detector is cut into bins, also side by side. Put the two cuttings on the same line, like two rulers next to each other. Where the shadow of a pixel and a bin overlap, the pixel sends that share of itself to that bin.

The bin value is then the average over the bin of what the rays see. Because both sets of cells cover the line with no gap, each pixel gives all of its mass to the bins, and a constant image gives a flat projection with no ripple. The back projection runs the same overlaps in the other direction.

## The problem

The image is $n \times n$ on the square $[-1, 1]^2$, with $f[i][j]$ in row $i$ from the top and column $j$ from the left. The center of pixel $(i, j)$ is $x_j = -1 + (2j+1)/n$, $y_i = 1 - (2i+1)/n$, so $y$ goes up, and $h = 2/n$ is the pixel size. A view has the angle $\theta$, with $\omega = (\cos\theta, \sin\theta)$, and the detector coordinate of a point $(x, y)$ is $s = x\cos\theta + y\sin\theta$, as for the [Radon transform](/radon-transform/). Bin $b$ covers $[s_0 + b w, s_0 + (b+1) w]$ for $b = 0, \ldots, d - 1$. The code uses the bins of the shared pixel-driven projector: $d$ bins of width $w = 2\sqrt{2}/d$ on $[-\sqrt{2}, \sqrt{2}]$.

The image model is this. Suppose $|\cos\theta| \ge |\sin\theta|$. Then each row of pixels is collapsed onto its center line $y = y_i$, with the thickness $h$. A ray crosses the row along a path of length $\Delta = h/|\cos\theta|$, and it sees the value of the pixel where it meets the center line. The bin value is the average over the bin width of the sum of these row contributions. For $|\cos\theta| < |\sin\theta|$, swap the roles of rows and columns, with $\Delta = h/|\sin\theta|$. The task is to compute all bin values of all views, and the transpose of this linear map.

## The algorithm

```pseudo id=main
DD-VIEW(f, c, σ, s0, w, d)               ▷ c = cos θ, σ = sin θ; out has d zeros
L1  h ← 2/n
L2  if |c| ≥ |σ| then Δ ← h/|c|, the lines are rows else Δ ← h/|σ|, the lines are columns
L3  for k ← 0 to n - 1 do                 ▷ row k, or column k
L4      B ← the n + 1 pixel borders of line k mapped to s = x c + y σ, in increasing order
L5      D ← the bin borders s0, s0 + w, ..., s0 + d w
L6      p ← 0, q ← 0                      ▷ p: a pixel of line k, q: a bin
L7      while p < n and q < d do
L8          ℓ ← min(B[p+1], D[q+1]) - max(B[p], D[q])
L9          if ℓ > 0 then out[q] ← out[q] + (Δ ℓ / w) · f[pixel p of line k]
L10         if B[p+1] < D[q+1] then p ← p + 1 else q ← q + 1
L11 return out
```

For a row $k$ the borders are $x = -1 + jh$ at the height $y_k$, so $B$ holds $(-1 + jh)\cos\theta + y_k\sin\theta$ for $j = 0, \ldots, n$. These values are equally spaced, $h|\cos\theta|$ apart. If $\cos\theta < 0$ they decrease, and line L4 reverses them, which also reverses the order of the pixels. Lines L6 to L10 are the merge of two sorted lists, as in [merge sort](/merge-sort/): at each step the cell that ends first moves on. Line L8 is the overlap of pixel $p$ and bin $q$, and line L9 adds the share of the pixel. The factor $\Delta/w$ makes the weights of one pixel, times $w$, sum to $\Delta \cdot h|\cos\theta| = h^2$, the pixel area, when the detector covers its shadow.

The pairs (pixel, bin, weight) of line L9 are the nonzero entries of one view of the system matrix. The back projector runs the same loops and adds weight times the bin value to the pixel. It is the exact transpose.

## Example

Take $n = 2$, so $h = 1$, the image $f = [[1, 2], [3, 4]]$, $\cos\theta = 4/5$, $\sin\theta = 3/5$ and four bins of width $w = 1/2$ on $[-1, 1]$. Then $|c| \ge |\sigma|$, the lines are rows, and $\Delta = 5/4$.

| row | $y$ | borders $B$ | pixel and its shadow | overlaps with the bins | weights $\Delta\ell/w$ |
|---|---|---|---|---|---|
| 0 | $1/2$ | $-1/2, 3/10, 11/10$ | $(0,0)$: $[-1/2, 3/10]$ | bin 1: $1/2$, bin 2: $3/10$ | $5/4$, $3/4$ |
| | | | $(0,1)$: $[3/10, 11/10]$ | bin 2: $1/5$, bin 3: $1/2$ | $1/2$, $5/4$ |
| 1 | $-1/2$ | $-11/10, -3/10, 1/2$ | $(1,0)$: $[-11/10, -3/10]$ | bin 0: $1/2$, bin 1: $1/5$ | $5/4$, $1/2$ |
| | | | $(1,1)$: $[-3/10, 1/2]$ | bin 1: $3/10$, bin 2: $1/2$ | $3/4$, $5/4$ |

The bin values are $(5/4 \cdot 3, \; 5/4 + 3/2 + 3, \; 3/4 + 1 + 5, \; 5/4 \cdot 2) = (15/4, 23/4, 27/4, 5/2)$. The shadow of a pixel has the width $h|\cos\theta| = 4/5$. The detector ends at $s = \pm 1$, so it misses $1/10$, that is $1/8$, of the shadow of pixel $(0, 1)$ and $1/8$ of the shadow of pixel $(1, 0)$. So $w$ times the sum of the bins is $(1/2)(75/4) = 75/8 = 10 - 2/8 - 3/8$, the image mass minus the missed parts. The test file checks every weight, every bin value and this sum with `fractions.Fraction`.

The code also measures the projector on a $32 \times 32$ grid with $23$ bins. For a constant image of value 1, every bin that lies fully inside the part of the detector where each ray crosses all rows gets exactly $2/\max(|\cos\theta|, |\sin\theta|)$, within $4 \cdot 10^{-15}$, at the angles $0$, $0.3$, $1.2$ and $2.0$. The pixel-driven projector of the shared helper differs from the same value by up to $0.11$ percent on the same bins: that is its ripple. For a disk of radius $1/2$ sampled at the pixel centers, over 8 angles and the bins with $|s| < 0.35$, the largest difference from the bin average of $2\sqrt{1/4 - s^2}$ is $0.034$. For the image $e^{-16|x|^2}$ sampled at the pixel centers, the largest difference from the bin average of $\sqrt{\pi/16}\,e^{-16 s^2}$ is $0.018$ for $n = 16$, $0.0019$ for $n = 32$ and $0.00046$ for $n = 64$. These are measurements of this setup with the bin width fixed at $0.123$.

## Correctness

The proof has three parts, and the full form is in [proofs/correctness.md](proofs/correctness.md). First, the sweep of lines L6 to L10 visits every pair of a pixel and a bin whose intervals overlap with positive length, once each. Both lists are sorted and each is a partition of an interval. The loop keeps the invariant that all pairs $(p', q')$ with $p' < p$ or $q' < q$ that overlap have been visited, because a cell is dropped only when it ends before the other current cell, and then it cannot meet any later cell of the other list. Second, the weight of a pair is $\Delta\ell/w$, which is the integral over the bin, divided by $w$, of the row contribution $\Delta f$ for the rays that meet the center line inside the pixel. So the code computes the model of "The problem" exactly. Third, the back projector uses the same list of weights, so it is the transpose.

Two exact facts follow. If the detector covers the shadow of the whole image, $w\sum_q \text{out}[q] = h^2 \sum_{i,j} f[i][j]$, the integral of the pixel-square image. At $\theta = 0$, the rays are vertical and the collapse of a row onto its center line changes nothing, so each bin gets the exact average over its width of the line integrals of the pixel-square image.

The method is still an approximation of the [X-ray transform](/x-ray-transform/) of the pixel-square image at other angles, because it collapses each row to its center line. A ray that crosses a pixel near its corner sees the full $\Delta$ of that pixel, while its true path through the square is shorter.

## Complexity

In the real-RAM model:

- Lines L4 and L5 build two sorted lists of $n + 1$ and $d + 1$ numbers in $O(n + d)$ time.
- The loop of lines L7 to L10 moves $p$ or $q$ at each step, so it runs at most $n + d$ times with $O(1)$ work each.
- Line L3 repeats this for $n$ lines.

So one view costs $O(n(n + d))$ time and $O(n + d)$ extra space, and a sinogram of $a$ views costs $O(a n (n + d))$. In practice $d$ is about $n$, which gives $O(a n^2)$, the same order as the pixel-driven and the ray-driven projectors, which cost $O(a n^2)$ and $O(a d n)$. The number of nonzero weights per view is at most $n(n + d)$, because each step of the sweep gives at most one. A real code computes the bin borders once per view, not once per line. In 3D, De Man and Basu map the voxel borders and the detector cell borders onto a common plane and take the overlaps in the two directions separately, as the product of two 1D overlaps.

## Properties

- **Matched pair.** The back projector is the exact transpose of the forward projector. The test checks $|\langle A x, y\rangle - \langle x, A^T y\rangle| \le 10^{-10}\|A x\|\|y\|$.
- **No ripple.** A constant image gives a flat projection inside the image, because the shadows of the pixels in a row tile the detector line with no gap and no overlap. The pixel-driven projector splits each pixel between the two nearest bin centers, so its projection of a constant image ripples.
- **No moire pattern in the back projection.** Each bin spreads its value over all pixels whose shadows it overlaps, in proportion to the overlap. A ray-driven back projector with thin rays misses pixels when the bins are wider than the pixels.
- **Mass conservation.** Each pixel sends exactly its area, times its value, to the detector.
- **Direction dependent model.** The lines switch from rows to columns at $|\cos\theta| = |\sin\theta|$. At $\theta = \pi/4$ both models apply, and they give slightly different weights.
- **Positive weights.** All weights are nonnegative, which the convergence results of [SART](/sart/) and [SIRT](/sirt/) need for their row and column sums.

## Variants and improvements

- **Three dimensions (De Man and Basu 2004).** Map the voxel borders and the detector cell borders onto a plane through the center of the volume, and take the area of overlap as the product of the overlaps in the two directions. The cost per view stays proportional to the number of voxels plus the number of detector cells per line.
- **Fan beam and cone beam.** The rays of a view meet in a source point. The borders are mapped by a central projection from the source onto the common axis, not by the parallel map of line L4. The overlaps and the sweep are the same.
- **Branchless distance-driven projection.** For GPUs, later work replaces the sweep with a difference of integrals of the image: precompute the cumulative sums of each line, then each bin value is a difference of two interpolated cumulative sums. This removes the branch of line L10.
- **Separable footprints.** Long, Fessler and Balter in 2010 model the footprint of a voxel on the detector as a trapezoid instead of a rectangle. This is more accurate at oblique angles, at a higher cost.

## When to use it

Use the distance-driven projector as the forward and back projector of an iterative method, such as [SART](/sart/), [SIRT](/sirt/), MLEM or penalized least squares, when the detector bins are about as wide as the pixels or wider, and when the back projection must be free of high frequency artifacts. Use [Siddon's algorithm](/siddon-algorithm/) when the weights must be the exact path lengths, and [Joseph's projector](/joseph-projector/) for a smooth image model with a fixed cost per ray. [Filtered back-projection](/filtered-back-projection/) needs only a back projector, and the pixel-driven back projector with linear interpolation is the usual choice there.

## Pitfalls

- **Decreasing borders.** For $\cos\theta < 0$ (rows) or for the column case, the mapped borders come out in decreasing order. The merge needs increasing lists, so line L4 must reverse them and also reverse the pixel index.
- **Wrong normalization of the back projector.** Some codes divide the back projected overlaps by the pixel width instead of the bin width, so that a constant sinogram gives a flat image. That pair is not an exact transpose. Use the same weights in both directions when an iterative method assumes $A^T$.
- **Detector too short.** If the bins do not cover the shadow of the image, mass leaks out at the ends, as in the example. This is correct for the model, but a test of mass conservation must use a detector that covers the image.
- **Equal borders.** If a pixel border and a bin border coincide, line L8 gives $\ell = 0$ for one pair. Line L9 must skip it, or the matrix gets explicit zero entries.
- **Forgetting the factor $\Delta$.** Without $1/|\cos\theta|$ the projection of a constant image depends on the angle.

## Implementations

The Python code computes the weights of one view with float or `fractions.Fraction` input, the forward projector, the back projector and the sparse matrix, with the bins of the shared pixel-driven projector `imgkit.parallel_beam_matrix`. The tests check the worked example exactly, the exact mass conservation for random integer images at five rational angles, the flat projection of a constant image against the ripple of the pixel-driven projector, the adjoint, the matrix against the projector, and the projection of a disk against the analytic Radon transform averaged over each bin.

## History

Bruno De Man and Samit Basu presented the distance-driven method in 2002 at the IEEE Nuclear Science Symposium and Medical Imaging Conference. They argued that the pixel-driven projector is a poor forward projector and the ray-driven projector a poor back projector, and that the distance-driven method is good in both directions at a similar cost. Their 2004 paper in Physics in Medicine and Biology gave the 3D form for cone-beam and helical CT. Later work moved the method to GPUs, and Long, Fessler and Balter in 2010 refined its rectangular footprint into the separable footprint projector.

## References
