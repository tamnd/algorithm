---
tag: 5E6C9Y
kind: algorithm
slug: quick-shift
name: Quick shift
aliases:
- quick shift superpixels
area: computer-vision/segmentation-and-recognition
level: advanced
summary: Mode seeking that links each pixel to its nearest neighbor of higher density in joint space and color, which builds a tree whose cut gives superpixels.
solves: [image-segmentation]
model: real-ram
complexity:
  vars: {W: the image width in pixels, H: the image height in pixels, k: the number of pixels in the density window and the link window together}
  time: {worst: O(W H k), average: O(W H k), best: O(W H k)}
  space: {extra: O(W H)}
properties: {deterministic: true, iterative: false, hierarchical: true, mode_seeking: true}
history:
  year: 2008
  people: [Andrea Vedaldi, Stefano Soatto]
  note: Vedaldi and Soatto proposed quick shift at ECCV 2008 as a fast alternative to medoid shift and mean shift.
prereqs: [mean-shift, kernel-density-estimation, image-segmentation]
see_also: [mean-shift-segmentation, mean-shift, slic-superpixels, felzenszwalb-segmentation, watershed-segmentation, ultrametric-contour-map, kernel-density-estimation, single-linkage-clustering]
sources:
  - paper: doi:10.1007/978-3-540-88693-8_52
    title: Andrea Vedaldi and Stefano Soatto, Quick shift and kernel methods for mode seeking, ECCV 2008, LNCS 5305, 705-718
    locator: The sections on medoid shift and quick shift
  - url: https://www.vlfeat.org/api/quickshift.html
    title: VLFeat API documentation, Quick shift image segmentation
    locator: Overview and parameters (kernel size and maximum distance)
  - paper: doi:10.1109/34.1000236
    title: Dorin Comaniciu and Peter Meer, Mean shift, a robust approach toward feature space analysis, IEEE TPAMI 24(5), 603-619, 2002
    locator: Mean shift segmentation in the joint spatial and range domain
---

Quick shift groups the pixels of an image by the modes of a density. It estimates the density of each pixel in the joint space of position and color. Then it links each pixel to the nearest pixel that has a higher density, if that pixel is close enough. The links form a forest, and each tree is one segment, often used as a superpixel. Vedaldi and Soatto (2008) proposed it. [Mean shift](/mean-shift/) and [mean shift segmentation](/mean-shift-segmentation/) move each point uphill by many small gradient steps until it stops at a mode. Quick shift makes one jump per pixel, to a real pixel, and never iterates. It is not a gradient method, so the mean shift convergence results do not apply to it, and it does not need them.

## In plain words

Think of the image as a landscape. A pixel that has many similar pixels near it is high ground. A pixel that is unlike its neighbors is low ground. Each pixel looks around and points to the closest pixel that stands higher than itself. If no higher pixel is close enough, the pixel is a hilltop.

Follow the arrows from any pixel and you climb until you reach a hilltop. All pixels that end at the same hilltop form one segment. If you allow longer arrows, hilltops join, and you get fewer and larger segments. With no limit on the length, every pixel ends at the highest point, and you get one tree for the whole image.

## The problem

The input is an image of $W \times H$ pixels. A pixel $i$ is $(u_i, v_i)$, with $u$ the column and $v$ the row, and it has the gray value $I_i$ (for color, use three values). The output is a partition of the pixels into segments, with a root pixel for each segment. This is a form of [image segmentation](/image-segmentation/) into many small regions. Quick shift has three parameters:
- $\sigma$, the standard deviation of the Gaussian kernel of the density, in feature units;
- $\tau$, the largest length of a link, in feature units (VLFeat calls it the maximum distance);
- $\lambda$, the weight of color against position in the feature.

## The algorithm

The feature of pixel $i$ is $f_i = (u_i, v_i, \lambda I_i)$. The density is a [kernel density estimate](/kernel-density-estimation/) with a Gaussian kernel, without the normalizing constant. The sum runs over a square window of radius $\lceil 3 \sigma \rceil$, outside of which the kernel is below $e^{-4.5} \approx 0.011$. The key of pixel $i$ is the pair $(P_i, i)$, so two pixels with equal densities are ordered by their index $i = v_i W + u_i$.

```pseudo id=main
QUICK-SHIFT(I, sigma, tau, lambda)
L1  for each pixel i do f_i ← (u_i, v_i, lambda · I_i)
L2  for each pixel i do
L3      P_i ← sum of exp(-||f_i - f_j||^2 / (2 sigma^2)) over the pixels j with |u_j - u_i| ≤ ⌈3 sigma⌉ and |v_j - v_i| ≤ ⌈3 sigma⌉
L4  for each pixel i do
L5      parent_i ← i; d_i ← ∞
L6      for each pixel j with |u_j - u_i| ≤ ⌈tau⌉ and |v_j - v_i| ≤ ⌈tau⌉, in raster order do
L7          if (P_j, j) > (P_i, i) and ||f_i - f_j|| ≤ tau then
L8              if ||f_i - f_j|| < d_i then parent_i ← j; d_i ← ||f_i - f_j||
L9  for each pixel i do root_i ← the end of the walk i, parent_i, parent_(parent_i), ...
L10 return root, parent, d
```

The window of line L6 is large enough: a pixel within feature distance $\tau$ is within $\tau$ in $u$ and in $v$. With $\tau = \infty$ the window is the whole image.

## Example

Take one row of 7 pixels with the values $0, 1, 1, 0, 5, 6, 5$, and $\sigma = 1$, $\lambda = 1$, $\tau = 2$. The feature of pixel $i$ is $(i, 0, I_i)$, and the density window has radius 3. For pixel 1 the window holds pixels 0 to 4, at squared distances 2, 0, 1, 5 and 25, so
$$P_1 = e^{-1} + 1 + e^{-0.5} + e^{-2.5} + e^{-12.5} \approx 2.05650.$$

| pixel $i$ | 0 | 1 | 2 | 3 | 4 | 5 | 6 |
|---|---|---|---|---|---|---|---|
| $I_i$ | 0 | 1 | 1 | 0 | 5 | 6 | 5 |
| $P_i$ | 1.4611 | 2.05650 | 2.05654 | 1.4611 | 1.5033 | 1.7358 | 1.5032 |
| parent for $\tau = 2$ | 1 | 2 | 2 (root) | 2 | 5 | 5 (root) | 5 |
| link length | $\sqrt 2$ | 1 | none | $\sqrt 2$ | $\sqrt 2$ | none | $\sqrt 2$ |

Pixels 1 and 2 have nearly equal densities. Pixel 2 is a little higher, because its window reaches pixels 4 and 5 at squared distances 20 and 34. So pixel 1 links to pixel 2. Pixel 3 has two higher pixels at distance $\sqrt 2$ and $\sqrt 5$, and it takes pixel 2. The bright pixel 5 has no higher pixel within distance 2: pixel 2 is at distance $\sqrt{9 + 25} = \sqrt{34} \approx 5.83$. So there are two segments, $\{0, 1, 2, 3\}$ and $\{4, 5, 6\}$.

With $\tau = \infty$, pixel 5 links to pixel 2 with length $\sqrt{34}$, and the whole row is one tree. Cut the links longer than 2 in that tree, and the two segments come back. The test file checks all these numbers.

## Correctness

The full proof is in [proofs/correctness.md](proofs/correctness.md). The main steps:
- The window of line L6 holds every pixel within feature distance $\tau$, so the window search finds the nearest pixel with a larger key within $\tau$, with ties of distance broken by the smaller index.
- The key strictly increases along each link, and keys are distinct because indices are. So the links have no cycle, every walk reaches a root, and the segments are well defined.
- A pixel is a root exactly when no pixel within distance $\tau$ has a larger key, so roots are local maxima of the density at scale $\tau$.
- For $\tau' \le \tau$, the forest for $\tau'$ is the forest for $\tau$ with the links longer than $\tau'$ cut. So one run with a large $\tau$ gives the segmentations for all smaller values, and they are nested.

These are properties of the procedure. Whether the segments follow object boundaries depends on the image and on $\sigma$, $\tau$ and $\lambda$. That is a heuristic matter, measured on benchmarks.

## Complexity

Let $k = (2 \lceil 3 \sigma \rceil + 1)^2 + (2 \lceil \tau \rceil + 1)^2$, the number of pixels in the two windows. Lines L2 and L3 and lines L4 to L8 cost $O(k)$ per pixel, and line L9 costs $O(WH)$ in total if each pixel stores its root once found. The total is $O(W H k)$ time and $O(WH)$ extra space in the [real-RAM](/real-ram/) model, with an exponential and a square root at unit cost. The cost has no iteration count, unlike mean shift, where each pixel climbs for a number of steps that depends on the data.

Vedaldi and Soatto compare quick shift with medoid shift, which moves each point to the data point that maximizes a local criterion and needs $O(n^2)$ work for $n$ points with the Euclidean distance. On an image, the spatial windows make quick shift linear in the number of pixels for fixed $\sigma$ and $\tau$. With $\tau = \infty$ the link window is the whole image and the cost is $O((WH)^2)$.

## Properties

- **No iterations.** Each pixel computes its density and its parent once.
- **Hierarchy.** One forest for a large $\tau$ holds the segmentations for all smaller $\tau$. Cutting links never merges segments.
- **Modes are pixels.** Each root is a real pixel, a local maximum of the density. Mean shift modes are points of the feature space that need not be pixels.
- **No control of the number of segments.** The number of roots depends on the image and on $\sigma$ and $\tau$. [SLIC](/slic-superpixels/) asks for a target number of superpixels instead.
- **Segments need not be compact.** A segment follows the density, so it can be long and thin.

## Variants and improvements

- **Color images.** Use $f_i = (u_i, v_i, \lambda L_i, \lambda a_i, \lambda b_i)$ with a color space such as CIELAB. The proof does not change.
- **Other features.** Quick shift works on any set of points with a distance, not only on images. Then the link search needs a neighbor structure such as a [kd-tree](/kd-tree/) instead of a pixel window. Vedaldi and Soatto also give a kernel version, in which the distances come from a kernel matrix.
- **Medoid shift.** The method that quick shift replaces. Each point moves to the data point with the best local criterion, and the step repeats. It can split one mode into many pieces, which quick shift avoids by linking to any higher point.
- **GPU versions.** Each pixel computes its density and its parent alone, so the method is easy to run in parallel.

## When to use it

Use quick shift when you need superpixels or an over-segmentation as a first step, you can accept segments of irregular size and shape, and you want a method with no iterations and a simple hierarchy over $\tau$. Use [SLIC](/slic-superpixels/) when you need a set number of compact superpixels, and [Felzenszwalb-Huttenlocher segmentation](/felzenszwalb-segmentation/) when you need a fast graph-based method with one scale parameter. Use [mean shift segmentation](/mean-shift-segmentation/) when you want the modes in feature space rather than at pixels.

## Pitfalls

- **Ties.** On a flat region many pixels have equal or nearly equal densities. Without a strict tie rule a pixel may have no higher neighbor and become a root, and a flat region breaks into many segments. This page uses the key $(P_i, i)$. Other codes break ties in other ways, so results can differ between libraries.
- **Units.** $\sigma$ and $\tau$ act on the joint feature, so they mix pixels and gray levels. If the gray values are in $[0, 1]$ and the positions in pixels, the color hardly counts unless $\lambda$ is large.
- **Link window and cost.** A large $\tau$ makes the link window large, and the cost grows with $\tau^2$. VLFeat says that $\tau$ can be infinite, which gives one tree, but that small values are much faster.
- **Segments can be split in space.** A link can jump over pixels, up to distance $\tau$. So a segment is not always 4-connected. Run a connected component pass if the next step needs connected regions.
- **Border effects.** The density window is cut at the image border, so border pixels get lower densities and are rarely roots.
- **Floating point.** Two densities that are equal in exact arithmetic can differ in the last bit when they are summed in a different order. This changes the parent of a pixel. Compare densities with care in tests, or use symmetric sums.

## Implementations

The Python code in `impl/python/quick_shift.py` implements lines L1 to L10 for gray images, and a function that cuts the links longer than a given length. The tests compare the window search with a search over all pixels, check that keys increase along links, check that cutting the tree for $\tau = \infty$ gives the forest for each smaller $\tau$, check the example above, and check that adding a constant to the image changes nothing.

## History

Vedaldi and Soatto (2008) proposed quick shift together with a kernel form of medoid shift. Medoid shift (Sheikh, Khan and Kanade 2007) had replaced the mean shift step by a step to a data point. Quick shift kept the step to a data point and dropped the iteration. The VLFeat library made it a common superpixel method, and later superpixel papers, such as the SLIC paper, compare against it.

## References
