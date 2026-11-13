---
tag: YT936C
kind: algorithm
slug: mean-shift-segmentation
name: Mean shift segmentation
aliases:
- mean shift clustering of pixels
- Comaniciu-Meer segmentation
- mean shift filtering
area: graphics-and-signals/image-processing
level: advanced
summary: Move each pixel, as a point in joint position and color space, uphill to a mode of the pixel density, then group the pixels whose modes are close and merge small regions.
solves: [image-segmentation]
model: real-ram
complexity:
  vars: {N: the number of pixels, T: the largest number of mean shift steps for one pixel, W: the number of pixels in a spatial window of radius h_s}
  time: {worst: O(N T W + N^2), average: O(N T W + N^2), best: O(N W + N^2)}
  space: {extra: Θ(N)}
properties: {deterministic: true, finds_number_of_regions: true, edge_preserving_filter: true, needs_bandwidths: true, converges_for_flat_ball_kernel: true}
history:
  year: 2002
  people: [Dorin Comaniciu, Peter Meer]
  note: Fukunaga and Hostetler introduced the mean shift in 1975 and Cheng generalized it in 1995. Comaniciu and Meer applied it in the joint spatial and color domain for filtering and segmentation, in a 2002 paper in IEEE Transactions on Pattern Analysis and Machine Intelligence.
prereqs: [mean-shift, image-segmentation]
see_also: [bilateral-filter, slic-superpixels, felzenszwalb-segmentation, watershed-segmentation, k-means, color-spaces, gaussian-mixture-model, dbscan]
sources:
  - paper: doi:10.1109/34.1000236
    title: Dorin Comaniciu and Peter Meer, Mean shift, a robust approach toward feature space analysis, IEEE Transactions on Pattern Analysis and Machine Intelligence 24(5), 603 to 619, 2002
    locator: Section 2 (the mean shift vector and Theorem 1 on convergence for a kernel with a convex, monotonically decreasing profile), Section 4.1.1 (mean shift filtering), Section 4.2.1 (the four steps of the segmentation and the parameters (h_s, h_r, M))
  - paper: doi:10.1109/TIT.1975.1055330
    title: Keinosuke Fukunaga and Larry D. Hostetler, The estimation of the gradient of a density function, with applications in pattern recognition, IEEE Transactions on Information Theory 21(1), 32 to 40, 1975
    locator: the mean shift as a step along the estimated density gradient, and its use for clustering
  - paper: doi:10.1109/34.400568
    title: Yizong Cheng, Mean shift, mode seeking, and clustering, IEEE Transactions on Pattern Analysis and Machine Intelligence 17(8), 790 to 799, 1995
    locator: the mean shift with general kernels and weights, and its relation to gradient ascent and to k-means
  - book: isbn:9781848829343
    title: Richard Szeliski, Computer Vision, Algorithms and Applications, Springer, 2011
    locator: Section 5.3, mean shift and mode finding
---

Mean shift segmentation treats every pixel as a point in a joint space of position and color, and looks for the dense spots of this point cloud. From each pixel it runs the [mean shift](/mean-shift/) procedure: take the pixels in a window around the current point, move to their mean, and repeat until the point stops. The stop is a mode, a local peak of the density of pixels. Pixels whose modes are close end up in the same region. Because the window is limited in both position and color, a pixel never averages with pixels across a strong edge, so the method smooths flat areas and keeps edges. Comaniciu and Meer made this a standard tool in 2002, with two bandwidths, $h_s$ for position and $h_r$ for color, and a minimum region size $M$. The number of regions is not given: it comes out of the data and the bandwidths.

## In plain words

Picture every pixel as a dot, placed by where it is in the picture and by its color. Dots of one object sit close together, because they are near each other and look alike. Start at a dot, draw a small bubble around it, and move to the center of the dots inside. Draw the bubble again and move again. You climb toward the place where the dots are most crowded, and you stop when the center does not move. Do this for every dot. Dots that end at the same crowded place belong together. Small leftover bits are joined to a neighbor.

## The problem

The input is an image with $N$ pixels. Pixel $i$ is the point $x_i = (x_i^s, x_i^r)$, with position $x_i^s$ in the plane and color $x_i^r$ (one gray value, or a color vector, usually in a perceptual [color space](/color-spaces/) such as CIELUV or CIELAB). Two bandwidths $h_s, h_r > 0$ and a size $M \ge 0$ are given. The output is a partition of the pixels into connected regions. It is one way to solve the [image segmentation](/image-segmentation/) problem.

The kernel used here is flat on the unit ball of the scaled coordinates, so the window of a point $y$ is

$$W(y) = \left\{ j : \left\lVert \frac{x_j^s - y^s}{h_s} \right\rVert^2 + \left\lVert \frac{x_j^r - y^r}{h_r} \right\rVert^2 \le 1 \right\},$$

and a mean shift step is $y \gets \frac{1}{|W(y)|} \sum_{j \in W(y)} x_j$. This flat window is the shadow of the Epanechnikov kernel, so each step goes uphill on the Epanechnikov density estimate. Comaniciu and Meer write the joint kernel as a product of one kernel for position and one for color. With the Epanechnikov or normal profile, the joint ball and the product are close but not the same, and the difference matters for convergence (see the pitfalls).

## The algorithm

```pseudo id=main
MEAN-SHIFT-SEGMENTATION(I, h_s, h_r, M)
L1  for each pixel i do y ← x_i
L2      repeat
L3          W ← the pixels j with ‖(x_j^s − y^s)/h_s‖² + ‖(x_j^r − y^r)/h_r‖² ≤ 1
L4          y_old ← y;  y ← the mean of x_j over j ∈ W   until y = y_old
L5      z_i ← y   ▷ the mode; the filtered pixel is (x_i^s, y^r)
L6  join i and j when ‖z_i^s − z_j^s‖ < h_s and ‖z_i^r − z_j^r‖ < h_r;  the clusters are the connected components
L7  split each cluster into connected regions of the image
L8  while some region has fewer than M pixels: merge the smallest into the adjacent region of nearest mean color
L9  return the regions
```

Lines L1 to L5 are mean shift filtering. Replacing each pixel's color with the color of its mode, $z_i^r$, gives an image where flat areas are smooth and edges are sharp, an alternative to the [bilateral filter](/bilateral-filter/). Lines L6 and L7 are the step that Comaniciu and Meer describe as concatenating the basins of attraction of nearby convergence points. Line L8 is their optional last step, which removes regions with fewer than $M$ pixels. The paper does not fix the merge rule; the implementation merges the smallest region, the first in raster order on a tie, into the adjacent region whose mean color is nearest, and repeats. It uses exact fractions throughout, so "until $y = y_{\text{old}}$" is an exact test.

## Example

Take the $5 \times 3$ gray image with rows $(10, 12, 11, 50, 52)$, $(11, 13, 10, 51, 49)$ and $(12, 30, 12, 50, 51)$, with $h_s = 2$ and $h_r = 8$. The left three columns are dark, with one outlier of value 30, and the right two columns are bright.

Write a point as (column, row, value). The top left pixel starts at $(0, 0, 10)$. Its window holds the four pixels of the top left $2 \times 2$ block, because a pixel two steps away in position is already at scaled distance 1 before its color is counted. Their mean is the next point, $(1/2, 1/2, 23/2)$. The next steps go to $(6/7, 5/7, 79/7)$ and $(1, 7/8, 91/8)$, which is the mean of all 8 dark pixels and the mean of its own window, so the path stops. Every dark pixel reaches this mode, and every bright pixel reaches $(7/2, 1, 101/2)$, the mean of the 6 bright pixels. The outlier 30 has no other pixel within $h_r = 8$ in value, so its window holds only itself, and it is its own mode.

The result has three regions: the 8 dark pixels, the 6 bright pixels, and the single pixel 30. The filtered image has the value $91/8 = 11.375$ on the dark side, $101/2 = 50.5$ on the bright side, and 30 at the outlier. With $M = 2$, the outlier region is merged into the dark region, whose mean color is nearer. With $h_r = 25$ instead, the 30 is within the color bandwidth of the dark pixels, and all 9 pixels of the left side go to one mode, $121/9$.

## Correctness

The full proof is in [proofs/correctness.md](proofs/correctness.md). For the flat ball kernel, it shows that each step raises the Epanechnikov density estimate by at least $|W| \lVert \Delta \rVert^2$, where $\Delta$ is the step in scaled coordinates. After the first step every point is the mean of a subset of the pixels, and there are only finitely many such means, so the density cannot rise forever, and each path stops after finitely many steps at a point that is the mean of its own window. This is a finite version of Theorem 1 of Comaniciu and Meer, which proves convergence of the mean shift for kernels with a convex, monotonically decreasing profile. Line L6 gives the connected components of the "close modes" graph, and line L7 splits them into connected regions, so every region is connected, lies in one cluster, and two adjacent regions are in different clusters. Line L8 stops only when every region has at least $M$ pixels or one region is left. The tests check every claim on random gray and color images, compare each path with a direct computation that tests every pixel for the window, and check the grouping against a search over all pairs.

## Complexity

- A mean shift step only needs the pixels within $h_s$ in position, about $W = \pi h_s^2$ pixels, so it costs $O(W)$ with the image grid as the index.
- Each pixel takes at most $T$ steps, so the filtering costs $O(N T W)$. Comaniciu and Meer report about 3 steps per pixel on average for their example.
- The implementation groups the distinct modes by testing all pairs, $O(N^2)$ in the worst case, and the merging of small regions is also at most quadratic. A grid on the modes with cell size $h_s$ makes the grouping close to linear.

The extra space is $\Theta(N)$ for the modes and labels. The cost is high compared with [SLIC](/slic-superpixels/) or [Felzenszwalb segmentation](/felzenszwalb-segmentation/), which is why fast versions start one path for many pixels or stop a path when it enters a pixel that has already converged.

## Properties

- **The number of regions comes from the data.** Only the bandwidths are set, and they have a clear meaning: the smallest spatial size and the smallest color difference that count.
- **Edge preserving.** A window never reaches across a color step larger than $h_r$, so filtering does not blur edges.
- **Deterministic.** There is no random start: every pixel runs its own path.
- **Convergence depends on the kernel.** The flat joint ball, and every kernel with a convex, decreasing profile, gives paths that stop. A product of two flat windows can cycle.
- **Mode, not mean.** The color of a region is a local peak of the color density, which is robust to outliers inside the window.

## Variants and improvements

- **Kernel choice.** The normal kernel gives smoother paths but in general does not stop exactly, so a tolerance on the step length is used. The Epanechnikov kernel, whose shadow is the flat window, stops in finitely many steps.
- **Speed-ups.** Assign every pixel that a path passes close to the same mode (basin of attraction shortcut), run on a coarser grid, or quantize the color space.
- **Adaptive bandwidths.** Vary $h_s$ or $h_r$ with the local density of the data, at more cost.
- **Other clustering.** [k-means](/k-means/) needs the number of clusters; a [Gaussian mixture](/gaussian-mixture-model/) needs the number and shape; [DBSCAN](/dbscan/) finds dense groups with a radius and a count instead of modes.
- **Medoid shift and quick shift.** Move each point to a data point instead of a mean, which avoids the iteration in feature space and allows other distances.

## When to use it

Use mean shift segmentation when the number of regions is not known, the regions are roughly uniform in color, and an edge-preserving smoothing is useful as well, for example to simplify photos before further analysis or to make cartoon-like effects. Its two bandwidths are easy to explain to a user. Do not use it when speed matters on large images, where [SLIC](/slic-superpixels/) or [Felzenszwalb segmentation](/felzenszwalb-segmentation/) is much faster, or when the objects differ in texture rather than in color. For one foreground object, [GrabCut](/grabcut/) is the better tool.

## Pitfalls

- **Product windows can cycle.** In the $3 \times 2$ image with rows $(8, 4, 5)$ and $(9, 7, 9)$, with $h_s = 1$, $h_r = 3$ and the window $\lVert \Delta^s \rVert \le h_s$ and $\lVert \Delta^r \rVert \le h_r$ tested separately, the point $(1, 1, 7)$ moves to $(1, 3/4, 29/4)$, whose window holds only the pixel 7, and back. Use the joint ball, or cap the number of steps.
- **Floating-point stops.** With a normal kernel or with floats, a path never stops exactly. Stop when the step is below a small tolerance, and group the modes afterward.
- **Bandwidth in the wrong units.** $h_r$ is in color units of the chosen space. The same value in RGB and in CIELAB gives very different results.
- **Too small $h_s$.** If no other pixel is within $h_s$ in position, every pixel is its own mode and nothing is grouped. With $h_s = 1$ and 4-neighbors at distance exactly 1, only pixels of equal color join.
- **Slow on large images.** The naive cost is many times that of a linear method. Use the speed-ups or a smaller image.
- **Grouping is transitive.** Line L6 joins chains of close modes, so a slow color ramp can join modes that are far apart.

## Implementations

## History

Keinosuke Fukunaga and Larry Hostetler introduced the mean shift in 1975, as a step along the estimated gradient of a density, and used it for clustering. The idea was little used until Yizong Cheng generalized it in 1995 to other kernels and weights, and showed links to gradient ascent and to k-means. Dorin Comaniciu and Peter Meer, at Rutgers, developed it for computer vision in conference papers and then in their 2002 paper in IEEE Transactions on Pattern Analysis and Machine Intelligence, with a convergence theorem, edge-preserving filtering in the joint spatial and color domain, and the segmentation method described here. They also used it for real-time tracking.

## References
