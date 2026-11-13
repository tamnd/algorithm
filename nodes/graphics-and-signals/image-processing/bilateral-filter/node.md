---
tag: 1PRAE4
kind: algorithm
slug: bilateral-filter
name: Bilateral filter
aliases:
- edge-preserving smoothing
area: graphics-and-signals/image-processing
level: advanced
summary: Weight neighbors by both spatial distance and intensity similarity to preserve edges.
solves: [image-smoothing]
model: real-ram
complexity:
  vars: {W: image width in pixels, H: image height in pixels, R: window radius}
  time: {worst: Θ(W H R²)}
  space: {extra: Θ(W H)}
properties: {deterministic: true, linear: false, edge_preserving: true, in_place: false}
history:
  year: 1998
  people: [Carlo Tomasi, Roberto Manduchi]
  note: Tomasi and Manduchi named the bilateral filter and gave it for gray and color images. Aurich and Weule (1995) and Smith and Brady (SUSAN, 1997) had used similar weights before.
prereqs: [gaussian-filter, linear-filtering]
see_also: [guided-filter, non-local-means, anisotropic-diffusion, image-smoothing, image-denoising, median-filter, total-variation-denoising, mean-shift]
sources:
  - paper: doi:10.1109/ICCV.1998.710815
    title: Carlo Tomasi and Roberto Manduchi, Bilateral filtering for gray and color images, Proceedings of the Sixth International Conference on Computer Vision (ICCV), 1998
    locator: the definition of the bilateral filter and its Gaussian case
  - paper: doi:10.1561/0600000020
    title: Sylvain Paris, Pierre Kornprobst, Jack Tumblin and Frédo Durand, Bilateral filtering, theory and applications, Foundations and Trends in Computer Graphics and Vision 4(1), 2009
    locator: the definition, the parameters and the fast algorithms
  - book: isbn:9783030343712
    title: Richard Szeliski, Computer Vision, Algorithms and Applications, second edition, Springer, 2022
    locator: Section 3.3.1, Non-linear filtering (bilateral filtering)
---

The bilateral filter smooths an image while it keeps strong edges. Like a [Gaussian filter](/gaussian-filter/), it replaces each pixel $p$ by a weighted mean of the pixels $q$ in a window around it. But the weight of $q$ is the product of two factors: a spatial weight $w_s(q - p)$ that falls with the distance from $p$, and a range weight $w_r(f(q) - f(p))$ that falls with the difference in value. Across an edge the range weight is nearly 0, so the pixels on the other side do not take part, and the edge is not blurred. The weights depend on the image, so the filter is not linear, and direct evaluation costs $\Theta(WHR^2)$ for a window of radius $R$. Tomasi and Manduchi introduced it in 1998; it is used for denoising, for detail and base layer separation in tone mapping, and as a building block of many photo tools.

## In plain words

A plain blur replaces each pixel by the average of its neighbors, and so it also mixes the two sides of every edge. The bilateral filter asks each neighbor two questions. Is it close? Does it look alike? A neighbor counts much only when the answer to both is yes. Near the middle of a flat region all neighbors look alike, and the filter acts like a blur that removes noise. At an edge, the neighbors on the other side look very different, so they count almost nothing, and the edge stays sharp.

Two settings control it. One is how far the neighborhood reaches. The other is how different a neighbor may look before it stops counting.

## The problem

The input is a gray image $f$ with $W$ columns and $H$ rows, a spatial weight $w_s$, a range weight $w_r$ and a window radius $R$. The usual weights are Gaussians, $w_s(u, v) = e^{-(u^2 + v^2)/(2\sigma_s^2)}$ and $w_r(d) = e^{-d^2/(2\sigma_r^2)}$, and a common radius is $R = \lceil 2\sigma_s \rceil$. Both weights must be positive at 0. The output at each pixel $p$ is

$$g(p) = \frac{\sum_{q \in N(p)} w_s(q - p)\, w_r(f(q) - f(p))\, f(q)}{\sum_{q \in N(p)} w_s(q - p)\, w_r(f(q) - f(p))},$$

where $N(p)$ is the set of pixels $q$ of the image with $|q_x - p_x| \le R$ and $|q_y - p_y| \le R$. The border rule is the cut window: pixels outside the image do not take part, and the division renormalizes the weights that remain. Extending the image by clamping instead would count the edge pixel several times.

## The algorithm

The loops run offset by offset, so the spatial weight of each offset is computed only once.

```pseudo id=main
BILATERAL(f, w_s, w_r, R)
L1  for each offset o = (u, v) with |u| ≤ R and |v| ≤ R do
L2      s ← w_s(u, v)
L3      for each pixel p such that q = p + o is inside the image do
L4          w ← s · w_r(f[q] − f[p])
L5          num[p] ← num[p] + w · f[q];  den[p] ← den[p] + w
L6  for each pixel p do g[p] ← num[p] / den[p]
L7  return g
```

The arrays `num` and `den` start at 0. Line L1 runs over the $(2R+1)^2$ offsets of the window, and line L2 computes the spatial weight of the offset. Line L3 visits every pixel $p$ whose neighbor $q = p + o$ lies in the image, which is the cut window of the border rule. Line L4 multiplies in the range weight, which depends on the two values and makes the filter nonlinear. Line L5 adds the weighted value and the weight. After all offsets, `num[p]` and `den[p]` hold the two sums of the definition, and line L6 divides. The offset $o = (0, 0)$ adds $w_s(0)\, w_r(0) > 0$ to every `den[p]`, so the division is safe. For a color image, $f[q] - f[p]$ is a color difference and $w_r$ uses its length, so that all channels get the same weights.

## Example

Take the one-row image $f = (10, 12, 10, 50, 48, 50)$, a noisy step, with $\sigma_s = 1$, $\sigma_r = 10$ and $R = 1$. The image has one row, so the vertical offsets find no pixel and the window is the three pixels $x - 1, x, x + 1$. The spatial weights are $1$ for the center and $e^{-1/2} = 0.6065$ for the two neighbors. The trace for the pixel $x = 2$:

| offset $u$ | $q$ | $f(q)$ | $w_s$ (line L2) | $w_r$ | $w$ (line L4) | $w\,f(q)$ (line L5) |
|---|---|---|---|---|---|---|
| $-1$ | 1 | 12 | 0.6065 | $e^{-0.02} = 0.9802$ | 0.5945 | 7.1343 |
| $0$ | 2 | 10 | 1 | 1 | 1 | 10 |
| $+1$ | 3 | 50 | 0.6065 | $e^{-8} = 0.000335$ | 0.000203 | 0.0102 |
| sums | | | | | 1.5947 | 17.1444 |

Line L6 gives $g(2) = 17.1444 / 1.5947 = 10.7507$. The pixel 50 across the edge has a weight of only 0.0002, so it hardly changes the result. The whole row:

| $x$ | 0 | 1 | 2 | 3 | 4 | 5 |
|---|---|---|---|---|---|---|
| $f$ | 10 | 12 | 10 | 50 | 48 | 50 |
| bilateral, $\sigma_r = 10$ | 10.7457 | 10.9136 | 10.7507 | 49.2493 | 49.0864 | 49.2543 |
| Gaussian only, $\sigma_r = \infty$ | 10.755 | 10.904 | 21.511 | 38.489 | 49.096 | 49.245 |

The noise of size 2 is reduced on both sides, and the step of 40 stays a step. With $w_r \equiv 1$ the filter is the Gaussian with the cut window, and it turns the step into the ramp $10.9, 21.5, 38.5, 49.1$.

## Correctness

Each pair $(p, q)$ with $q$ in $N(p)$ is met exactly once, at the offset $o = q - p$ of line L1 and the pixel $p$ of line L3, and it adds its term to both sums. No other pair is met. So after the loops `num[p]` and `den[p]` are the numerator and the denominator of the definition, and $\mathrm{den}[p] \ge w_s(0)\,w_r(0) > 0$. As a mean with nonnegative weights, $g(p)$ lies between the least and the largest value of $f$ in $N(p)$. The full proof is below.

## Complexity

- **Time.** Line L1 runs $(2R+1)^2$ times, and lines L3 to L5 cost $O(WH)$ for each offset, so the time is $\Theta(WHR^2)$, with one evaluation of $w_r$ per pair. With $R = \lceil 2\sigma_s \rceil$ this is $\Theta(WH\sigma_s^2)$.
- **Space.** The two arrays `num` and `den`, $\Theta(WH)$. The per-pixel loop order needs only $O(1)$ extra space, at the price of recomputing $w_s$.
- **No separation.** The range weight couples the two axes, so the filter does not factor into a row pass and a column pass. Running it row by row and then column by column is a common approximation, not the same filter.

## Properties

- **Not linear.** The filter of $f_1 + f_2$ is in general not the sum of the filters, and the filter of $c f$ for $c \ne 1$ differs from $c$ times the filter of $f$, because $w_r$ sees the scaled differences.
- **Range.** The output at $p$ lies between the least and the largest value in its window, so no new extremes and no overshoot appear.
- **Edges.** A step much larger than $\sigma_r$ is kept, while variations much smaller than $\sigma_r$ are smoothed as by a Gaussian of $\sigma_s$.
- **Limits.** As $\sigma_r \to \infty$ it becomes a Gaussian blur with the cut window. As $\sigma_r \to 0$ only the pixels with the same value as $p$ keep a weight, so the output tends to the input image.
- **Equivariance.** It commutes with adding a constant to the image, and with reflections and right-angle turns of the image when $w_s$ is radial.
- **Staircase and gradient reversal.** On a smooth ramp it tends to form flat steps, and near a sharp edge it can reverse the sign of small gradients, which shows as halos after detail boosting.

## Variants and improvements

- **Joint (cross) bilateral filter.** Take the range weight from a second guide image, for example a flash photo, and average the values of the first. The [guided filter](/guided-filter/) gives a similar result in $O(WH)$ time and without gradient reversal.
- **Fast approximations.** Durand and Dorsey (2002) interpolated between linear filters for a few range values. Paris and Durand (2006) and the bilateral grid of Chen, Paris and Durand (2007) downsample the space of position and value and filter there with linear filters. Porikli (2008) and Yang, Tan and Ahuja (2009) gave methods whose cost does not grow with $R$.
- **Iterated filter.** Applying the filter several times gives stronger, cartoon-like smoothing; it is close to a step of [anisotropic diffusion](/anisotropic-diffusion/) with a robust conductance.
- **Patch based weights.** Comparing small patches in place of single values gives [non-local means](/non-local-means/), which is more robust to noise.
- **Robust statistics view.** The filter is one step of a weighted least squares estimate of the local value with the robust weight $w_r$, which links it to [mean shift](/mean-shift/).

## When to use it

Use the bilateral filter to remove small noise or texture while keeping strong edges, and to split an image into a smooth base layer and a detail layer for tone mapping or detail editing. Keep $R$ small, or use a fast approximation, because the direct cost grows with $R^2$. Use [non-local means](/non-local-means/) for stronger noise, the [guided filter](/guided-filter/) when speed and the absence of gradient reversal matter, and the [median filter](/median-filter/) for salt-and-pepper noise, which the bilateral filter keeps because an outlier finds no similar neighbors.

## Pitfalls

- **Missing normalization.** Writing $g[p] \leftarrow \mathrm{num}[p]$ at line L6, with weights normalized once for the full window, gives wrong values near edges and near the border. The weights depend on $p$, so line L6 must divide by `den[p]`, the sum of the weights actually used.
- **The range of the values.** Using $\sigma_r = 10$ for an image stored in $[0, 1]$ makes $w_r \approx 1$ everywhere, and the filter is a plain blur. Give $\sigma_r$ in the units of the stored values.
- **Updating in place.** Writing the result back into $f$ while later pixels still read it at line L4 makes the output depend on the visiting order. Keep $f$ unchanged until line L7.
- **The range weight of the absolute value.** Writing $w_r(f[q])$ at line L4 weights bright pixels more and does not preserve edges. The argument is the difference $f[q] - f[p]$.
- **Color per channel.** Filtering R, G and B with three independent range weights gives different weights per channel and color fringes at edges. Use one weight from the color difference, preferably in a perceptual space such as CIELAB, as Tomasi and Manduchi did.

## Implementations

## History

Tomasi and Manduchi (1998) gave the filter its name and its standard form, for gray and color images, with the range weight computed in CIELAB for color. Related weights appeared before: Aurich and Weule (1995) in nonlinear Gaussian filters, and Smith and Brady (1997) in the SUSAN method for edges, corners and noise reduction. Durand and Dorsey (2002) made it a standard tool in computational photography by using it to split images into base and detail layers for tone mapping, and the survey of Paris, Kornprobst, Tumblin and Durand (2009) collects its theory and its fast algorithms.

## References
