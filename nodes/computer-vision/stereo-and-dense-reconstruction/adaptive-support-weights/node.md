---
tag: WDQMCM
kind: algorithm
slug: adaptive-support-weights
name: Adaptive support weights
aliases:
- Yoon-Kweon adaptive weights
area: computer-vision/stereo-and-dense-reconstruction
level: advanced
summary: Aggregate costs with weights that fall off with color difference and distance from the center pixel, like a bilateral filter on the cost volume.
solves: [stereo-matching]
model: real-ram
complexity:
  vars: {W: the image width in pixels, H: the image height in pixels, D: the number of disparities, r: the radius of the window}
  time: {worst: Θ(W H D r^2), average: Θ(W H D r^2), best: Θ(W H D r^2)}
  space: {extra: Θ(W H r^2)}
properties: {deterministic: true, exact: false, online: false, recursive: false}
history:
  year: 2005
  people: [Kuk-Jin Yoon, In So Kweon]
  note: Yoon and Kweon presented the method at CVPR 2005 and in the IEEE Transactions on Pattern Analysis and Machine Intelligence in 2006. It was the first local method to come close to global methods on the Middlebury benchmark, at a high cost per pixel.
prereqs: [block-matching-stereo, cost-aggregation, bilateral-filter]
see_also: [cost-volume, guided-filter, stereo-matching-cost, census-transform, left-right-consistency-check, semi-global-matching, stereo-matching, linear-filtering]
sources:
  - paper: doi:10.1109/TPAMI.2006.70
    title: Kuk-Jin Yoon and In So Kweon, Adaptive support-weight approach for correspondence search, IEEE Transactions on Pattern Analysis and Machine Intelligence 28(4), 2006, 650-656
    locator: the whole paper (the support weight from the color difference in CIELab and the distance, the combination of the weights of both windows, and winner-takes-all)
  - paper: "Kuk-Jin Yoon and In So Kweon, Locally adaptive support-weight approach for visual correspondence search, IEEE Conference on Computer Vision and Pattern Recognition, 2005, volume 2, 924-931"
    locator: the conference version of the method (the weight of Eq. 9 and the parameter setting of the Middlebury tests)
  - paper: doi:10.1007/978-3-642-15558-1_37
    title: Christian Richardt, Douglas Orr, Ian Davies, Antonio Criminisi and Neil A. Dodgson, Real-time spatiotemporal stereo matching using the dual-cross-bilateral grid, European Conference on Computer Vision, 2010
    locator: the description of adaptive support weights and its default parameter values
  - paper: doi:10.1109/TPAMI.2012.156
    title: Asmaa Hosni, Christoph Rhemann, Michael Bleyer, Carsten Rother and Margrit Gelautz, Fast cost-volume filtering for visual correspondence and beyond, IEEE Transactions on Pattern Analysis and Machine Intelligence 35(2), 2013, 504-511
    locator: edge-aware filtering of the cost volume with the guided filter, in time independent of the window size
  - paper: doi:10.1023/A:1014573219977
    title: Daniel Scharstein and Richard Szeliski, A taxonomy and evaluation of dense two-frame stereo correspondence algorithms, International Journal of Computer Vision 47(1-3), 2002, 7-42
    locator: the part on aggregation and the problems of square windows near depth edges
---

Adaptive support weights is a local stereo method that sums the matching costs of a window with a weight for each pixel of the window, where the weight is high for pixels close to the center in color and in position and low for the others. A pixel on the far side of a depth edge usually has another color, so it gets almost no weight, and the window behaves as if it followed the edge. Yoon and Kweon (2005, 2006) took the weight of a pixel as the product of its weight in the left window and the weight of its match in the right window, and chose disparities by winner-takes-all. It is [block matching](/block-matching-stereo/) with the box replaced by a [bilateral filter](/bilateral-filter/) of the [cost volume](/cost-volume/), and the weights must be computed for each window, so it costs $\Theta(W H D r^2)$ on the real RAM, not $\Theta(W H D)$.

## In plain words

Block matching adds up the differences over a whole square. If the square sits on the edge of a near object, half of it shows the background, and that half pulls the answer the wrong way. Adaptive support weights asks each pixel of the square how much it looks like the center pixel. A pixel of the same color and close by gets a weight near one; a pixel of a clearly different color gets a weight near zero. It does this in both images and multiplies the two weights. Then it averages the differences with these weights. The square now counts only the part that probably lies on the same surface as the center.

## The problem

**Input.** A rectified pair of color images $I_L$ and $I_R$ of $W \times H$ pixels, the right camera to the right of the left one, so the left pixel $(u, v)$ matches the right pixel $(u - d, v)$. A number of disparities $D$, a window radius $r$, two positive constants $\gamma_c$ and $\gamma_p$, and a truncation threshold $T$.

**Output.** For each left pixel $p = (u, v)$, the disparity $d^*(p) = \min \operatorname{arg\,min}_{0 \le d \le \min(D - 1, u)} E(p, d)$, with

$$E(p, d) = \frac{\sum_{q} w(p, q)\, w(\bar p_d, \bar q_d)\, e(q, \bar q_d)}{\sum_{q} w(p, q)\, w(\bar p_d, \bar q_d)}, \qquad w(p, q) = \exp\!\left(-\left(\frac{\Delta c_{pq}}{\gamma_c} + \frac{\Delta g_{pq}}{\gamma_p}\right)\right).$$

Here $q = p + o$ runs over the offsets $o$ of the $(2r + 1) \times (2r + 1)$ window such that $q$ is in the left image and $\bar q_d = q - (d, 0)$ is in the right image, and $\bar p_d = p - (d, 0)$. The color distance $\Delta c_{pq}$ is the Euclidean distance of the colors of $p$ and $q$ in CIELab, computed within one image, and $\Delta g_{pq} = \lVert o \rVert$ is the distance of the positions. The raw cost $e(q, \bar q) = \min\big(\sum_{c \in \{R, G, B\}} |I_{L,c}(q) - I_{R,c}(\bar q)|, T\big)$ is the truncated absolute difference. The outer $\min$ breaks ties toward the smallest disparity.

The parameters are tuned, not derived, and the sources give two settings. The conference paper (Yoon and Kweon 2005) reports a $33 \times 33$ window with $\gamma_c = 7$ and $\gamma_p = 36$, with $\gamma_p$ chosen by experiment. Richardt et al. (2010) give $35 \times 35$ ($r = 17$), $\gamma_c = 5$ and $\gamma_p = 17.5$ as the default values of the method, and later papers use these. The code uses the second setting as its defaults. The threshold $T = 40$ of the code is a choice of the code.

## The algorithm

```pseudo id=main
ASW(I_L, I_R, D, r, γc, γp, T)
L1  for each left pixel p = (u, v) do
L2      for d ← 0 to min(D - 1, u) do
L3          num ← 0;  den ← 0
L4          for each offset o of the window with q = p + o in I_L and q - (d, 0) in I_R do
L5              ω ← w(p, q) · w(p - (d, 0), q - (d, 0))         ▷ the left and the right weight
L6              num ← num + ω · e(q, q - (d, 0));  den ← den + ω
L7          E(d) ← num / den
L8      disp(p) ← the least d with the least E(d)
L9  return disp
```

Line L5 is the heart of the method. The left factor favors pixels like $p$ in the left image, and the right factor favors pixels like the candidate match in the right image. A pixel gets a large weight only if it looks like the center in both images, which is what is expected of a pixel on the same surface at the candidate disparity. Line L7 normalizes, so $E$ is a weighted mean of truncated costs. The weights $w(p, q)$ of a pixel do not depend on $d$, so the code computes them once per pixel and image and keeps them, $(2r + 1)^2$ numbers per pixel.

## Example

With $\gamma_c = 5$ and $\gamma_p = 17.5$, the weights of some neighbors $q$ of a red center $p$ with RGB color $(200, 30, 30)$ are:

| color of $q$ | distance $\lVert o \rVert$ | $\Delta c$ in CIELab | $w(p, q)$ |
|---|---|---|---|
| $(200, 30, 30)$ | 1 | 0 | 0.9445 |
| $(200, 30, 30)$ | 3 | 0 | 0.8425 |
| $(210, 40, 35)$ | 1 | 3.04 | 0.5138 |
| $(190, 60, 40)$ | 2 | 12.96 | 0.0668 |
| $(30, 30, 200)$ | 1 | 130.12 | $4.7 \cdot 10^{-12}$ |

The color term falls much faster than the distance term: a Lab difference of 13 already cuts the weight to under a tenth, while a distance of 3 pixels only cuts it to 0.84.

Now take a window of three pixels at one disparity. The center has raw cost 4 and joint weight $1 \cdot 1 = 1$. A neighbor on the same red surface has raw cost 6 and joint weight $0.9445^2 = 0.892$. A neighbor on a blue background has raw cost $T = 40$, because at this disparity its match is wrong, and joint weight below $10^{-20}$. Then

$$E = \frac{1 \cdot 4 + 0.892 \cdot 6 + 10^{-20} \cdot 40}{1 + 0.892 + 10^{-20}} \approx 4.94,$$

while the box mean is $(4 + 6 + 40) / 3 \approx 16.7$. The background pixel no longer decides the cost of the red center.

## Correctness

The full proof is in [proofs/correctness.md](proofs/correctness.md). It shows that the offset $o = (0, 0)$ is always in the sum of line L4, because $d \le u$, with joint weight $1$, so $\textit{den} \ge 1$ and line L7 never divides by zero. It shows that lines L3 to L7 compute $E(p, d)$ of the definition, that $E(p, d)$ is a weighted mean of truncated costs and so lies in $[0, T]$, that line L8 returns $d^*(p)$, and that for $\gamma_c, \gamma_p \to \infty$ all weights tend to 1 and $E$ tends to the box mean of [block matching](/block-matching-stereo/) with the truncated cost.

## Complexity

The model is the [real RAM](/real-ram/) with $\exp$ and the square root at unit cost.

- **Weights.** Each pixel of each image has $(2r + 1)^2$ weights, each from one color distance and one $\exp$: $\Theta(W H r^2)$ time and $\Theta(W H r^2)$ space for the stored weights. Without storing them, the time doubles and the space is $\Theta(W H)$.
- **Costs.** Lines L4 to L6 run $(2r + 1)^2$ times for each pixel and disparity, so the total is $\Theta(W H D r^2)$ time. For the usual $35 \times 35$ window, that is 1225 weighted terms per pixel and disparity, against the four additions and subtractions per pixel and disparity of a box filter with an integral image.
- **No shortcut by sums.** The weights change with the center pixel, so the window sum cannot be read from an integral image. That is the reason for the faster approximations below.

## Properties

- **Bilateral filter on the cost volume.** For a fixed $d$, line L6 is a joint [bilateral filter](/bilateral-filter/) of the cost slice, with the range kernel taken from the two images instead of from the costs (a theorem by the form of the sum). The left and right weights make it symmetric in the two images.
- **Weighted mean.** $E(p, d)$ is a convex combination of the raw costs, so it lies between the least and the largest raw cost in the window, and in $[0, T]$.
- **Edge preserving, by assumption.** The method assumes that pixels of similar color near each other lie on the same surface, and that a depth edge is also a color edge. This is a heuristic. Where a surface has strong texture or two surfaces have the same color, the weights help less.
- **No smoothness term.** Each pixel still decides by winner-takes-all. Large textureless areas of one color get large uniform supports, which helps, but there is no global constraint.

## Variants and improvements

- **Guided filter aggregation.** Hosni et al. (2013) filter each cost slice with the [guided filter](/guided-filter/), which is edge-aware like the bilateral weights but runs in $\Theta(W H)$ per slice for any radius, with box sums. The whole method is $\Theta(W H D)$.
- **Geodesic weights.** Replace the color distance by a geodesic distance in the image, so that a pixel of the same color behind an edge of another color is not counted.
- **Weights from the left image only.** Dropping the right factor halves the work. The result is close in many scenes but no longer symmetric.
- **Fast approximations.** Bilateral grids, as in Richardt et al. (2010), separable approximations, and tree filters bring the cost close to $\Theta(W H D)$.
- **With other costs.** The truncated absolute difference can be replaced by a [census](/census-transform/) cost or by gradients; the weights stay the same.

## When to use it

Use adaptive support weights as a reference local method, or when the scene has clear color edges at its depth edges and the image is small enough for the cost. For larger images and real time, use [guided filter aggregation](/cost-aggregation/), which gives similar edge behavior at $\Theta(W H D)$, or [semi-global matching](/semi-global-matching/), which adds a smoothness term. Use plain [block matching](/block-matching-stereo/) when speed matters more than edges.

## Pitfalls

- **Cost.** The usual window has 1225 pixels, each with an exponential, so the method does hundreds of times more arithmetic per cost than a box filter. Do not store all weights for large images without checking the memory: $(2r + 1)^2$ numbers per pixel per image.
- **Color space.** The color distance is defined in CIELab, which is closer to perceived differences than RGB. With 8-bit RGB distances, $\gamma_c = 5$ is far too small, and almost every weight is zero.
- **Gray images.** With one channel, many surfaces share a gray level, and the weights separate them much less well.
- **Truncation.** Without the threshold $T$, a single bad pixel with a large weight still dominates the mean. With a small $T$, the cost loses the power to tell a near miss from a far miss.
- **Occlusions.** Near the left side of a near object, some background pixels have no match at all. The weights do not fix this; a [left-right consistency check](/left-right-consistency-check/) is still needed.

## Implementations

## History

Yoon and Kweon presented the method at CVPR 2005 and in the IEEE Transactions on Pattern Analysis and Machine Intelligence in 2006, following earlier work on windows that adapt their shape or size, such as the adaptive windows of Kanade and Okutomi. Their method showed that a local method with carefully weighted support could compete with global methods on depth edges, at a high cost per pixel. Later work aimed at the same quality at the speed of a box filter, with bilateral grids, geodesic weights and, most widely, the guided filter of Hosni et al. (2013).

## References
