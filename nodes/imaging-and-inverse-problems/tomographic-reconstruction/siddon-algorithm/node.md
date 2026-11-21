---
tag: 3SDE4K
kind: algorithm
slug: siddon-algorithm
name: Siddon's algorithm
aliases:
- Siddon ray tracing
area: imaging-and-inverse-problems/tomographic-reconstruction
level: core
summary: Compute the exact length of a ray in each pixel or voxel it crosses, by merging the sorted parameters of its crossings with the grid lines or planes.
model: real-ram
complexity:
  vars: {n: the side of the n x n image, a: the number of projection angles, d: the number of detector bins}
  time: {worst: "O(a d n)"}
  space: {extra: "O(n)"}
properties: {deterministic: true, in_place: false, recursive: false, iterative: false, linear: true}
history:
  year: 1985
  people: [Robert L. Siddon]
  note: Siddon computed the exact radiological path through a 3D CT array from the parametric crossings of the ray with the three sets of grid planes.
prereqs: [radon-transform, sparse-matrix]
see_also: [joseph-projector, distance-driven-projector, amanatides-woo-traversal, digital-differential-analyzer, kaczmarz-method, sart, sirt, x-ray-transform]
sources:
  - paper: doi:10.1118/1.595715
    title: Robert L. Siddon, Fast calculation of the exact radiological path for a three-dimensional CT array, Medical Physics 12(2), 1985
    locator: pp. 252 to 255 (the parametric form of the ray, the alpha sets of the x, y and z planes, their merge and the voxel index from the midpoint)
  - paper: "F. Jacobs, E. Sundermann, B. De Sutter, M. Christiaens and I. Lemahieu, A fast algorithm to calculate the exact radiological path through a pixel or voxel space, Journal of Computing and Information Technology 6(1), 1998, pages 89 to 94"
    locator: the incremental form that updates the next crossing and the voxel index without a merge (general locator)
  - book: isbn:9780898714944
    title: A. C. Kak and M. Slaney, Principles of Computerized Tomographic Imaging, SIAM Classics in Applied Mathematics 33, 2001
    locator: Chapter 7, algebraic reconstruction algorithms (the weights of the system matrix as intersection lengths of rays and pixels)
  - book: isbn:9781852336172
    title: Gabor T. Herman, Fundamentals of Computerized Tomography, Image Reconstruction from Projections, second edition, Springer, 2009
    locator: the discussion of the fast calculation of ray sums for a digitized picture (general locator; chapter not confirmed)
---

Siddon's algorithm computes, for one ray, the exact length of its path inside each pixel of a 2D grid or each voxel of a 3D grid. These lengths are the entries of one row of the system matrix $A$ in the discrete model $y = A x$ of transmission tomography, where $x$ holds the pixel values and $y_i$ approximates the line integral of the [X-ray transform](/x-ray-transform/) along ray $i$. The method writes the ray as $p(\alpha) = p_0 + \alpha(p_1 - p_0)$, lists the values of $\alpha$ where the ray meets each family of grid lines, merges these sorted lists, and reads off one pixel and one length between each two neighbors. It takes $O(n)$ time per ray on an $n \times n$ grid. It is the standard ray-driven projector for the iterative methods [SART](/sart/), [SIRT](/sirt/) and [ART](/kaczmarz-method/). [Joseph's projector](/joseph-projector/) and the [distance-driven projector](/distance-driven-projector/) are cheaper or smoother approximations of the same matrix.

## In plain words

Draw a straight line across a sheet of squared paper. The line passes through some squares, and it spends a different length in each one. Siddon's method finds these lengths with no guessing.

Walk along the line from its start. Each time the line crosses a vertical grid line or a horizontal grid line, write down how far along the line you are. The crossings with the vertical lines come in order, and so do the crossings with the horizontal lines. Merge the two ordered lists into one. Between two crossings that are next to each other, the line stays in one square. The distance between the two crossings is the length in that square, and the point halfway between them tells you which square it is.

## The problem

The image is $n \times n$ on the square $[-1, 1]^2$, with pixel size $h = 2/n$. Pixel $(i, j)$, in row $i$ from the top and column $j$ from the left, is the closed square $[-1 + jh, -1 + (j+1)h] \times [1 - (i+1)h, 1 - ih]$. Its center is $x_j = -1 + (2j+1)/n$, $y_i = 1 - (2i+1)/n$, so $y$ goes up. A ray is the segment from $p_0 = (x_0, y_0)$ to $p_1 = (x_1, y_1)$. The output is the list of pairs (pixel, length) for each pixel whose intersection with the segment has positive length, in the order in which the ray meets them. For a piecewise constant image $f = \sum_{i,j} x_{ij} \chi_{ij}$, the sum of length times value is the exact line integral of $f$ along the segment.

In parallel-beam geometry, ray $(k, b)$ is the line $x\cos\theta_k + y\sin\theta_k = s_b$ of the [Radon transform](/radon-transform/), with $\omega = (\cos\theta, \sin\theta)$ and $\omega^\perp = (-\sin\theta, \cos\theta)$. The code takes $p_0 = s_b\omega - 2\omega^\perp$ and $p_1 = s_b\omega + 2\omega^\perp$, a segment long enough to cross the whole square.

## The algorithm

```pseudo id=main
SIDDON(n, p0, p1)                       ▷ grid lines x = -1 + k h and y = -1 + k h, h = 2/n
L1  dx ← x1 - x0, dy ← y1 - y0, D ← sqrt(dx² + dy²)
L2  [α_min, α_max] ← [0, 1] ∩ {α : p(α) ∈ [-1, 1]²}     ▷ one interval per axis with dx or dy ≠ 0
L3  if α_min ≥ α_max then return the empty list
L4  Ax ← the α in (α_min, α_max) with x0 + α dx = -1 + k h for an integer k, increasing
L5  Ay ← the α in (α_min, α_max) with y0 + α dy = -1 + k h for an integer k, increasing
L6  S ← α_min, then MERGE(Ax, Ay), then α_max
L7  for each pair (α_prev, α_next) of neighbors in S with α_next > α_prev do
L8      (x_m, y_m) ← p((α_prev + α_next) / 2)
L9      j ← ⌊(x_m + 1)/h⌋, i ← ⌊(1 - y_m)/h⌋
L10     output (i, j, (α_next - α_prev) D)
```

Line L2 clips the segment to the square. For an axis with $dx \ne 0$, the ray is inside the slab $-1 \le x \le 1$ for $\alpha$ between $(-1 - x_0)/dx$ and $(1 - x_0)/dx$. If $dx = 0$, the ray is inside the slab for all $\alpha$ or for none. Lines L4 and L5 do not scan all $n + 1$ grid lines. They compute the first and last index $k$ of the lines that the clipped segment crosses, with a floor and a ceiling of $n(x + 1)/2$ at its two ends, and then step $k$ up for $dx > 0$ or down for $dx < 0$. So each list is already sorted, and line L6 is the merge step of [merge sort](/merge-sort/). Line L7 skips a pair with equal values: a ray through a grid corner meets a vertical and a horizontal line at the same $\alpha$. Line L9 finds the pixel from the midpoint, which is strictly inside one pixel. In 3D, line L5 has a third list for the $z$ planes, and the merge takes three lists.

To project an image, run SIDDON for each ray and sum length times pixel value. To back-project, run SIDDON for each ray again and add length times the ray value to each pixel. The two are exact transposes of each other, because they use the same weights.

## Example

Take $n = 4$, so $h = 1/2$, and the ray from $p_0 = (-1, -1/2)$ to $p_1 = (1, 1)$. Then $dx = 2$, $dy = 3/2$ and $D = 5/2$. The whole segment is in the square, so $\alpha_{\min} = 0$ and $\alpha_{\max} = 1$.

| step | values |
|---|---|
| $x$ lines $-1/2, 0, 1/2$ at $\alpha = (x + 1)/2$ | $A_x = 1/4, 1/2, 3/4$ |
| $y$ lines $0, 1/2$ at $\alpha = (y + 1/2)/(3/2)$ | $A_y = 1/3, 2/3$ |
| merged $S$ | $0, 1/4, 1/3, 1/2, 2/3, 3/4, 1$ |
| differences | $1/4, 1/12, 1/6, 1/6, 1/12, 1/4$ |
| lengths $= D \times$ difference | $5/8, 5/24, 5/12, 5/12, 5/24, 5/8$ |
| pixels $(i, j)$ from the midpoints | $(2,0), (2,1), (1,1), (1,2), (0,2), (0,3)$ |

The first midpoint is $\alpha = 1/8$, the point $(-0.75, -0.3125)$. It is in column $\lfloor 0.25 / 0.5 \rfloor = 0$ and row $\lfloor 1.3125/0.5 \rfloor = 2$. The lengths add up to $5/2 = D$, because the whole segment is inside the square. All values are exact rationals, and the test file checks them with `fractions.Fraction`.

The code below also projects a disk of radius $1/2$, sampled at the pixel centers of a $32 \times 32$ grid, along $8$ angles and $23$ bins. At the bins with $|s| < 0.35$, the projection differs from the analytic value $2\sqrt{1/4 - s^2}$ by at most $0.061$. That is less than one pixel width $2/n = 0.0625$, because the pixelated disk and the true disk differ by at most about one pixel along a chord. For the smooth image $e^{-16|x|^2}$, sampled at the pixel centers, the largest error against the exact projection $\sqrt{\pi/16}\,e^{-16 s^2}$ is $0.0115$ for $n = 16$, $0.0024$ for $n = 32$ and $0.00059$ for $n = 64$. These are measurements of this setup. The error falls by about 4 when $n$ doubles, as for a second order method.

## Correctness

The pieces between neighbors in $S$ partition the clipped segment. Inside one piece no $\alpha$ of a grid line occurs, so $x(\alpha)$ and $y(\alpha)$ each stay between two neighboring grid lines, and the open piece lies inside one pixel: the pixel of its midpoint. The length of the piece is $(\alpha_{\text{next}} - \alpha_{\text{prev}})D$, because $p$ is affine with speed $D$. A pixel cannot hold two pieces, because between them the ray crosses a grid line, and a pixel lies on one side of each grid line. So the output lists each pixel with positive intersection length once, with its exact length. The full proof, with the clipping of line L2 and the index ranges of lines L4 and L5, is in [proofs/correctness.md](proofs/correctness.md).

## Complexity

In the real-RAM model:

- Lines L1 to L3 take $O(1)$.
- The clipped segment crosses at most $n + 1$ vertical and $n + 1$ horizontal grid lines. Lines L4 and L5 compute their $\alpha$ values in $O(n)$ time, with no search.
- The merge of line L6 takes $O(n)$, and the loop of lines L7 to L10 runs at most $2n + 1$ times with $O(1)$ work each.

So one ray takes $O(n)$ time and $O(n)$ extra space, and a sinogram of $a$ angles and $d$ bins takes $O(a d n)$. The output of one ray has at most $2n - 1$ pixels, so the bound is tight up to a constant. In 3D, an $n \times n \times n$ grid gives $O(n)$ per ray in the same way, with three lists. Siddon's paper presents this as the gain over a method that tests every voxel against the ray, which costs $O(n^3)$ per ray in 3D.

## Properties

- **Exact.** The weights are the true intersection lengths of a line and the pixel squares. The forward projection of a piecewise constant image is its exact line integral. With rational endpoints and a rational length $D$ (a direction such as $(3, 4)$), the code returns exact rationals.
- **Matched pair.** The back projector uses the same weights, so it is the exact adjoint $A^T$ of the forward projector. Iterative methods that assume $A^T$, such as [SIRT](/sirt/) and the [Landweber iteration](/landweber-iteration/), need this.
- **Ray-driven.** The work is organized by rays. Each ray reads (forward) or writes (back projection) a thin set of pixels. On parallel hardware, the back projection has write conflicts, because two rays may update the same pixel.
- **Aliasing of thin rays.** A ray has zero width, while a detector bin has a finite width. When the bins are wider than the pixels, some pixels are crossed by no ray of a view, and the back projection of a smooth sinogram shows a moire pattern. The [distance-driven projector](/distance-driven-projector/) integrates over the bin width and avoids this.

## Variants and improvements

- **Incremental form (Jacobs et al. 1998).** Keep the next crossing $\alpha_x$ and $\alpha_y$ and the current index $(i, j)$. At each step take the smaller of the two, add its distance to the output, and step $j$ or $i$ by $\pm 1$. There is no merge list and no floor at each pixel. The same idea is the [Amanatides-Woo traversal](/amanatides-woo-traversal/) of computer graphics and the [digital differential analyzer](/digital-differential-analyzer/) of line drawing.
- **3D cone beam.** Each ray runs from the source to the center of a detector cell. The algorithm is the same with three plane families.
- **Several rays per bin.** Trace a few rays across the width of each detector bin and average them. This reduces the aliasing of thin rays at a proportional cost.
- **Integer coordinates.** With the grid lines at integers and rational endpoints, all $\alpha$ values are rational and the comparisons in the merge are exact. The test file uses this to check the code against a brute-force clip of the segment with each pixel.

## When to use it

Use Siddon's algorithm when the system matrix must hold the exact intersection lengths: for an exact model of a piecewise constant image, for a matched projector and back projector in [ART](/kaczmarz-method/), [SART](/sart/) and [SIRT](/sirt/), for dose calculations in radiotherapy, and for digitally reconstructed radiographs. Use [Joseph's projector](/joseph-projector/) when a smoother model of the image is better and a fixed cost per row is easier to vectorize. Use the [distance-driven projector](/distance-driven-projector/) when the detector bins are wide and the back projection must be free of moire patterns. [Filtered back-projection](/filtered-back-projection/) needs no system matrix at all.

## Pitfalls

- **Rounding at the grid lines.** In floating point, a crossing may land a tiny distance on the wrong side of a grid line. The floor in line L9 then picks a neighbor pixel for a piece of length near zero. This is harmless for the weights, but code that assumes each pixel appears once must merge such entries. Line L9 must also clamp $i$ and $j$ to $[0, n - 1]$.
- **Equal crossings.** A ray through a grid corner gives the same $\alpha$ in both lists. Without the test $\alpha_{\text{next}} > \alpha_{\text{prev}}$ of line L7, the code outputs a piece of length zero, and with rounding it may put it in a wrong pixel.
- **A ray on a grid line.** If $dx = 0$ and $x_0$ is a grid line, the ray runs along the border of two pixel columns. The intersection length is the full length for both. The code gives it to the column on the right, by the floor in line L9. Another convention is half to each. Pick one and keep it.
- **Sorting instead of merging.** Line L6 needs only a merge, because lines L4 and L5 give sorted lists. A general sort costs $O(n \log n)$ per ray.
- **Wrong row direction.** Row $i$ counts from the top while $y$ goes up. Line L9 uses $1 - y_m$, not $y_m + 1$. A wrong sign flips the image upside down.

## Implementations

The Python code traces rays in 2D with float or `fractions.Fraction` coordinates. It builds parallel-beam rays with the same bins as the pixel-driven projector of the shared helper, and it gives the forward projector, the back projector and the sparse matrix. The tests check the worked example exactly, compare 40 rational rays with a brute-force clip against each pixel, check the adjoint, and compare the projections of a disk and of a Gaussian with the analytic Radon transform.

## History

Robert Siddon published the method in Medical Physics in 1985 for three-dimensional CT arrays. Before, the exact path through a voxel array was found by testing the ray against each voxel or each plane in turn. Siddon's key step was to treat the voxels as the intersections of three families of equally spaced parallel planes, so that the crossings come from three arithmetic sequences. Jacobs, Sundermann, De Sutter, Christiaens and Lemahieu removed the merge and the index computation in 1998 with an incremental update, which is now often called the Siddon-Jacobs algorithm. The same traversal appeared in computer graphics in 1987 as the voxel traversal of Amanatides and Woo.

## References
