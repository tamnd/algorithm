---
tag: VSCW79
kind: algorithm
slug: block-matching-stereo
name: Block matching stereo
aliases:
- window-based stereo
- SAD block matching
area: computer-vision/stereo-and-dense-reconstruction
level: intro
summary: Give each pixel the disparity whose window in the other image has the least sum of absolute or squared differences.
solves: [stereo-matching]
model: word-ram
complexity:
  vars: {W: the image width in pixels, H: the image height in pixels, D: the number of disparities}
  time: {worst: Θ(W H D), average: Θ(W H D), best: Θ(W H D)}
  space: {extra: Θ(W H)}
properties: {deterministic: true, exact: true, online: false, recursive: false}
history:
  year: 2002
  people: [Daniel Scharstein, Richard Szeliski]
  note: Correlation of windows along epipolar lines is the oldest form of computer stereo. Scharstein and Szeliski (2002) placed it in their taxonomy as a matching cost, box aggregation and winner-takes-all, and measured it on a common benchmark.
prereqs: [stereo-matching, disparity, integral-image]
see_also: [stereo-matching-cost, cost-aggregation, cost-volume, census-transform, adaptive-support-weights, left-right-consistency-check, subpixel-disparity-refinement, template-matching]
sources:
  - paper: doi:10.1023/A:1014573219977
    title: Daniel Scharstein and Richard Szeliski, A taxonomy and evaluation of dense two-frame stereo correspondence algorithms, International Journal of Computer Vision 47(1-3), 2002, 7-42
    locator: the parts on matching costs (absolute and squared differences), aggregation with a square window, winner-takes-all, and the results of these local methods on the benchmark
  - book: isbn:9783030343712
    title: Richard Szeliski, Computer Vision, Algorithms and Applications, second edition, Springer, 2022
    locator: Chapter 12, Depth estimation (local methods and the sum of squared or absolute differences over a window)
  - paper: doi:10.1109/TPAMI.2012.156
    title: Asmaa Hosni, Christoph Rhemann, Michael Bleyer, Carsten Rother and Margrit Gelautz, Fast cost-volume filtering for visual correspondence and beyond, IEEE Transactions on Pattern Analysis and Machine Intelligence 35(2), 2013, 504-511
    locator: the cost volume, filter and winner-takes-all pipeline, of which the box filter is the simplest case
---

Block matching stereo gives each pixel of the left image the [disparity](/disparity/) $d$ for which the square window around it best matches the window around column $u - d$ in the right image, measured by the sum of absolute differences (SAD) or of squared differences (SSD). It is the simplest local method for [stereo matching](/stereo-matching/): a pixel [matching cost](/stereo-matching-cost/), a box [aggregation](/cost-aggregation/) of the cost, and winner-takes-all over the disparities. With an [integral image](/integral-image/) or running sums the window sums cost $O(1)$ each, so the whole method takes $\Theta(W H D)$ time on the word RAM, independent of the window size. It differs from [template matching](/template-matching/), which searches one template over a whole image in two dimensions; here every pixel has its own window and the search is along one row.

## In plain words

Take a small square around a pixel of the left image, say 7 by 7 pixels. Slide the same square along the same row of the right image, one pixel at a time, and at each place add up how different the two squares are. The place with the smallest total is the match, and the number of pixels slid is the disparity. Do this for every pixel. A larger square sees more texture and makes fewer wild mistakes, but it blurs the edges of objects. A smaller square keeps the edges but gets confused where the image is plain.

## The problem

**Input.** A rectified pair of grayscale images $L$ and $R$ of $W \times H$ pixels with integer values of $b$ bits, the right camera to the right of the left one. A window radius $r \ge 0$ and a number of disparities $D \ge 1$. Pixel $(u, v)$ is in column $u$ and row $v$; in code it is `img[v][u]`.

**Output.** For each left pixel $p = (u, v)$ the disparity

$$d^*(p) = \min \operatorname*{arg\,min}_{0 \le d < D} S_d(p), \qquad S_d(u, v) = \sum_{|i| \le r} \sum_{|j| \le r} e_d(\bar u + i, \bar v + j),$$

with the pixel cost $e_d(u, v) = |L(u, v) - R(\max(u - d, 0), v)|$ for SAD, or its square for SSD, and with positions outside the image clamped to the nearest border pixel (written with bars). The outer $\min$ breaks ties toward the smallest disparity. The definitions at the border are choices of the code; other programs leave a frame of $r$ pixels, and the first $D - 1$ columns, without a value.

## The algorithm

```pseudo id=main
BLOCK-MATCH(L, R, D, r)
L1  for each pixel p do best[p] ← ∞; disp[p] ← 0
L2  for d ← 0 to D - 1 do
L3      e(u, v) ← |L(u, v) - R(max(u - d, 0), v)| for every pixel      ▷ or the square
L4      S ← the integral image of e, padded by r on each side by copying the border
L5      for each pixel p = (u, v) do
L6          c ← S[v + k][u + k] - S[v][u + k] - S[v + k][u] + S[v][u]   ▷ k = 2r + 1
L7          if c < best[p] then best[p] ← c; disp[p] ← d
L8  return disp
```

The loop over disparities is outside, so only one image of pixel costs and one integral image are alive at a time, together with the best cost and disparity of each pixel. Line L4 builds the integral image $S[y][x]$, the sum of the padded cost image over the rows before $y$ and the columns before $x$. Line L6 reads the window sum with four lookups, the identity of the [integral image](/integral-image/) page. Line L7 keeps the smallest cost so far, and the strict test keeps the first, smallest disparity on ties. The same loop with running sums along rows and columns, or with a [box blur](/box-blur/) of $e$, gives the same sums.

## Example

Take three equal rows, so the window of $r = 1$ only sums each column three times. The left row is $(10, 10, 50, 90, 10, 10)$ and the right row $(10, 50, 90, 10, 10, 10)$, the left row shifted by one, and $D = 3$. The window costs $S_d$ at the middle row are:

| $u$ | 0 | 1 | 2 | 3 | 4 | 5 |
|---|---|---|---|---|---|---|
| $S_0$ | 120 | 240 | 480 | 360 | 240 | 0 |
| $S_1$ | 0 | 0 | 0 | 0 | 0 | 0 |
| $S_2$ | 0 | 120 | 240 | 480 | 360 | 240 |
| $d^*$ | 1 | 1 | 1 | 1 | 1 | 0 |

At $u = 3$, the pixel alone gives the costs $80, 0, 40$, and the window gives $360, 0, 480$: the texture at columns 2 to 4 makes the minimum clear. At $u = 5$, the window covers columns 4 and 5 (column 6 is clamped to 5), which are all 10 in both images at $d = 0$ and $d = 1$. The tie goes to $d = 0$, which is wrong. At $u = 0$ the costs at $d = 1$ and $d = 2$ both use column 0 of the right image, by the border rule, and are both 0; the tie goes to $d = 1$, which is right by luck. These are the two classic failures: no texture, and the left border, where the true match is outside the right image.

## Correctness

The full proof is in [proofs/correctness.md](proofs/correctness.md). It has two parts. First, line L6 returns $S_d(p)$: the padded image at row $y$ and column $x$ is $e$ at the clamped position $(\bar x - r, \bar y - r)$, so the window of $p$ in the original image is the block of rows $v$ to $v + 2r$ and columns $u$ to $u + 2r$ of the padded image, and the four lookups give the sum of that block. Second, the loop of line L2 keeps the invariant that after the disparities $0, \ldots, d - 1$, $\textit{best}[p]$ is the least of $S_0(p), \ldots, S_{d-1}(p)$ and $\textit{disp}[p]$ is the least disparity that reaches it. At the end this is $d^*(p)$.

## Complexity

The model is the [word RAM](/word-ram/). An SAD window sum is at most $(2r + 1)^2 (2^b - 1)$, and an SSD sum at most $(2r + 1)^2 (2^b - 1)^2$, and an integral image entry at most $(W + 2r)(H + 2r)$ times the largest pixel cost. With 8-bit pixels and images of a few million pixels these fit a 64-bit word.

- **Time.** For each of the $D$ disparities, lines L3, L4 and L5 to L7 take $\Theta(W H)$ time for $r$ less than $W$ and $H$, so the total is $\Theta(W H D)$. The window size does not appear, which is the point of the integral image.
- **Space.** One cost image, one integral image of $(W + 2r + 1)(H + 2r + 1)$ words, and two arrays of $W H$ entries: $\Theta(W H)$ extra space. A program that stores the full [cost volume](/cost-volume/) needs $\Theta(W H D)$ instead.
- **Brute force.** Summing each window directly takes $\Theta(W H D r^2)$ time. The code has it as the reference for the tests.

## Properties

- **Box support.** Every pixel of the window counts the same. This assumes that all pixels of the window have the same disparity, which is false near depth edges (a heuristic assumption).
- **Foreground fattening.** Near a depth edge, the window of a background pixel contains part of the near object, which has strong texture and a larger disparity. The near object then wins, and the disparity map shows the object larger than it is, by up to $r$ pixels. This is a known failure of box windows, measured in the benchmark of Scharstein and Szeliski.
- **No smoothness.** Each pixel decides alone. Neighbors agree only because their windows overlap.
- **SAD or SSD.** SSD is the maximum likelihood cost for Gaussian noise; SAD is less hurt by single outliers. Neither tolerates a change of brightness between the cameras, for which the [census transform](/census-transform/) or [normalized cross-correlation](/normalized-cross-correlation/) is better.

## Variants and improvements

- **Other costs.** Replace the pixel cost of line L3 by the [census](/census-transform/) Hamming distance, the Birchfield-Tomasi cost, or a truncated difference. The rest of the method is unchanged.
- **Zero mean and normalized windows.** Subtract the window mean (ZSAD, ZSSD) or use [normalized cross-correlation](/normalized-cross-correlation/), to cancel an offset or a gain between the cameras.
- **Weighted windows.** Weight the pixels of the window by their similarity to the center, as in [adaptive support weights](/adaptive-support-weights/) or the guided filter of Hosni et al. (2013). This reduces foreground fattening at a higher cost per pixel or with a more complex filter.
- **Shiftable and multiple windows.** Take the best of several windows that contain the pixel but are not centered on it, so a pixel near an edge can use a window that stays on its own side.
- **Adaptive window size.** Kanade and Okutomi (1994) chose the window size per pixel from the local texture and disparity variation.
- **Post-processing.** A [left-right consistency check](/left-right-consistency-check/), a test on the texture of the window, a uniqueness test on the ratio of the best and second best costs, [subpixel refinement](/subpixel-disparity-refinement/) and a [median filter](/median-filter/) of the map. OpenCV's StereoBM is block matching with such tests.

## When to use it

Use block matching when speed and simplicity matter more than quality: on small processors, as a first estimate for a slower method, or on images with rich texture. It runs in real time with SIMD instructions because every step is integer adds. Use [semi-global matching](/semi-global-matching/) when the scene has large textureless areas or many depth edges, and an edge-aware aggregation when you want a local method that keeps edges.

## Pitfalls

- **Window size.** No single size works everywhere: small windows fail in flat areas, large ones fatten objects. Choose it for the data, and say so; typical sizes are 5 by 5 to 21 by 21.
- **Left border.** For $u < d$ the true match is outside the right image. Mark the first $D - 1$ columns invalid, or at least do not trust them.
- **Ties and flat areas.** In a flat area all costs are equal, and the tie rule picks the answer. Report such pixels as invalid by a texture test.
- **Overflow.** SSD sums of 8-bit images over large windows exceed 16 and 32 bits quickly. Check the bound in the complexity section for your word size.
- **Unrectified input.** The method assumes that matches lie in the same row. A rectification error of one pixel already hurts, so check the vertical offset of known matches.

## Implementations

## History

Matching windows along epipolar lines by correlation is the oldest computer stereo method and was used in photogrammetry before computer vision. Kanade and Okutomi (1994) adapted the window to the image. Scharstein and Szeliski (2002) described local methods as a matching cost, aggregation and winner-takes-all, and evaluated SAD and SSD with square windows on the Middlebury benchmark, where they showed the trade-off between window size and edge errors. Hosni et al. (2013) showed that replacing the box filter by an edge-aware filter on the cost volume gives a local method that keeps edges much better than the box, at the same $\Theta(W H D)$ cost.

## References
