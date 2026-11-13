---
tag: 4HSCV2
kind: algorithm
slug: guided-filter
name: Guided filter
aliases:
- guided image filtering
area: graphics-and-signals/image-processing
level: advanced
summary: An edge-preserving filter that transfers structure from a guidance image using local linear models.
solves: [image-smoothing]
model: real-ram
complexity:
  vars: {W: image width in pixels, H: image height in pixels, r: window radius}
  time: {worst: Θ(W H)}
  space: {extra: Θ(W H)}
properties: {deterministic: true, linear_in_input: true, edge_preserving: true, in_place: false}
history:
  year: 2010
  people: [Kaiming He, Jian Sun, Xiaoou Tang]
  note: He, Sun and Tang introduced the guided filter at ECCV 2010 and gave the full version in IEEE TPAMI in 2013. Its cost of O(1) per pixel for any window radius comes from box filters.
prereqs: [integral-image, ridge-regression]
see_also: [bilateral-filter, box-blur, image-smoothing, image-denoising, non-local-means, unsharp-masking, linear-regression, anisotropic-diffusion]
sources:
  - paper: doi:10.1007/978-3-642-15549-9_1
    title: Kaiming He, Jian Sun and Xiaoou Tang, Guided image filtering, European Conference on Computer Vision (ECCV), 2010
    locator: the definition of the filter by local linear models and its box filter algorithm
  - paper: doi:10.1109/TPAMI.2012.213
    title: Kaiming He, Jian Sun and Xiaoou Tang, Guided image filtering, IEEE Transactions on Pattern Analysis and Machine Intelligence 35(6), 2013
    locator: Algorithm 1 (the guided filter by box filters) and the explicit filter kernel
  - book: isbn:9783030343712
    title: Richard Szeliski, Computer Vision, Algorithms and Applications, second edition, Springer, 2022
    locator: Section 3.3.1, Non-linear filtering (guided image filtering)
---

The guided filter smooths an input image $p$ while it follows the edges of a guidance image $I$, which may be $p$ itself. In each window $w_k$ of radius $r$ it fits a linear model $q = a_k I + b_k$ to $p$ by least squares, with a penalty $\varepsilon a_k^2$ that keeps $a_k$ small, and the output at a pixel is the mean of the fits of all windows that hold it. Where the guide has an edge, its local variance is much larger than $\varepsilon$, $a_k$ is near 1 and the edge passes to the output; where the guide is flat, $a_k$ is near 0 and the output is a local mean. All the sums are box means, so with an [integral image](/integral-image/) or running sums the cost is $\Theta(WH)$ for any radius. He, Sun and Tang introduced it in 2010 as a fast alternative to the [bilateral filter](/bilateral-filter/) without its gradient reversal.

## In plain words

Look at a small square of the guide picture. Inside it, try to write the input picture as the guide made brighter or darker by some factor, plus a constant. If the square holds a strong edge of the guide, the best factor is large, and the output copies the edge. If the square is almost flat, the best factor is close to zero, and the output is just the average of the input there.

Every pixel lies in many squares. Each square gives its own guess for the pixel, and the output is the average of these guesses. One setting says how strong an edge must be to be kept. Another sets the size of the squares.

## The problem

The input is a guidance image $I$ and a filtering input $p$ of the same size, $W$ columns and $H$ rows, a radius $r \ge 0$ and a regularization $\varepsilon > 0$, in the square of the units of $I$. For a pixel $k$, the window $w_k$ is the set of pixels $i$ of the image with $|i_x - k_x| \le r$ and $|i_y - k_y| \le r$, and $n_k = |w_k|$. The border rule is the cut window: pixels outside the image do not exist, and every mean divides by the count of the pixels in the cut window. For each $k$, the coefficients $(a_k, b_k)$ minimize

$$E_k(a, b) = \sum_{i \in w_k} \left( (a I_i + b - p_i)^2 + \varepsilon a^2 \right),$$

and the output is $q_i = \frac{1}{n_i} \sum_{k \in w_i} (a_k I_i + b_k)$, the mean over the windows that hold $i$, because $i \in w_k$ exactly when $k \in w_i$.

## The algorithm

Write $\mathrm{mean}(X)$ for the box mean of an image $X$ over the cut windows, computed in $O(WH)$ by an integral image, and $I \cdot p$ for the pixelwise product.

```pseudo id=main
GUIDED-FILTER(I, p, r, ε)
L1  μ ← mean(I);  p̄ ← mean(p);  c_II ← mean(I·I);  c_Ip ← mean(I·p)
L2  for each pixel k do  var_k ← c_II[k] − μ[k]²;  cov_k ← c_Ip[k] − μ[k] p̄[k]
L3      a_k ← cov_k / (var_k + ε);  b_k ← p̄[k] − a_k μ[k]
L4  ā ← mean(a);  b̄ ← mean(b)
L5  return q with q_i = ā[i] I_i + b̄[i]
```

Line L1 computes four box means: the means of $I$ and $p$ and of their products. Line L2 turns them into the variance of $I$ and the covariance of $I$ and $p$ in each window. Line L3 is the closed form of the regularized least squares fit, a one-variable [ridge regression](/ridge-regression/): the slope is the covariance over the variance plus $\varepsilon$, and the line goes through the means. Line L4 averages the coefficients over the windows that hold each pixel, and line L5 applies the averaged model to the guide. For a color guide, line L3 solves a $3 \times 3$ linear system per window with the covariance matrix of the three channels plus $\varepsilon$ times the identity.

## Example

Take the one-row image $f = (10, 12, 10, 50, 48, 50)$ as both guide and input, $I = p = f$, with $r = 1$ and $\varepsilon = 100$. The image has one row, so each window holds up to three pixels and only two at the ends.

| $x$ | 0 | 1 | 2 | 3 | 4 | 5 |
|---|---|---|---|---|---|---|
| $f$ | 10 | 12 | 10 | 50 | 48 | 50 |
| $\mu$ (line L1) | 11 | 10.667 | 24 | 36 | 49.333 | 49 |
| $\mathrm{var}$ (line L2) | 1 | 0.889 | 338.667 | 338.667 | 0.889 | 1 |
| $a$ (line L3) | 0.0099 | 0.0088 | 0.772 | 0.772 | 0.0088 | 0.0099 |
| $b$ (line L3) | 10.891 | 10.573 | 5.471 | 8.207 | 48.899 | 48.515 |
| $\bar a$ (line L4) | 0.0094 | 0.2636 | 0.5176 | 0.5176 | 0.2636 | 0.0094 |
| $\bar b$ (line L4) | 10.732 | 8.978 | 8.083 | 20.859 | 35.207 | 48.707 |
| $q$, $\varepsilon = 100$ (line L5) | 10.825 | 12.141 | 13.260 | 46.740 | 47.859 | 49.175 |
| $q$, $\varepsilon = 1$ | 10.426 | 11.610 | 10.157 | 49.843 | 48.390 | 49.574 |
| $q$, $\varepsilon = 10^4$ | 10.833 | 15.091 | 23.119 | 36.881 | 44.909 | 49.167 |

In the flat windows the variance is about 1, far below $\varepsilon = 100$, so $a \approx 0.01$ and the fit is the local mean. The windows across the step have a variance of 339, so $a = 0.77$ and the edge is mostly kept. With $\varepsilon = 1$ the step is kept almost fully, and with $\varepsilon = 10^4$, far above every variance, the filter is close to a double box blur. For example $q_1 = 0.2636 \cdot 12 + 8.978 = 12.141$.

## Correctness

Setting the two partial derivatives of $E_k$ to zero gives $b = \bar p_k - a \mu_k$ and $a(\mathrm{var}_k + \varepsilon) = \mathrm{cov}_k$, which is line L3, and $E_k$ is strictly convex because $\varepsilon > 0$, so this is its unique minimum. The box means of line L4 average exactly over the windows that hold each pixel, because the window relation is symmetric. The full proof is below.

## Complexity

- **Time.** Each box mean costs $\Theta(WH)$ with an integral image or with running sums, whatever $r$ is. The algorithm uses six of them, at lines L1 and L4, and $O(1)$ more work per pixel, so the time is $\Theta(WH)$. The bilateral filter costs $\Theta(WHr^2)$ when evaluated directly.
- **Space.** A constant number of images of size $W \times H$, $\Theta(WH)$.
- **Color guide.** With a guide of $c$ channels, line L1 needs $O(c^2)$ box means and line L3 solves a $c \times c$ system per pixel, so the time is $\Theta(WH c^3)$, still independent of $r$.

## Properties

- **Linear in the input.** For a fixed guide, $q$ is a linear function of $p$: $q_i = \sum_j K_{ij}(I)\, p_j$ with a kernel that depends on $I$ and whose weights sum to 1. With the full windows of the interior, $K_{ij} = \frac{1}{n^2} \sum_{k : i, j \in w_k} \left(1 + \frac{(I_i - \mu_k)(I_j - \mu_k)}{\mathrm{var}_k + \varepsilon}\right)$. It is not linear in the guide.
- **Edges of the guide.** Near a pixel $i$, $q \approx \bar a_i I + \bar b_i$, so the output has the edges of the guide, scaled by $\bar a$. An edge of the guide with a local variance much larger than $\varepsilon$ passes with $a \approx 1$ when $I = p$.
- **Constants.** If $p$ is constant, $\mathrm{cov} = 0$, so $a = 0$, $b = p$ and $q = p$, whatever the guide is.
- **No gradient reversal.** Unlike the bilateral filter, the guided filter keeps the sign of the gradients of the guide, so detail boosting with it does not make reversed halos.
- **Halos at some edges.** The model is linear in each window, so near an edge whose two sides do not follow one line in $I$, the output is blurred a little, by the box of radius $r$.

## Variants and improvements

- **Fast guided filter.** He and Sun (2015) compute $a$ and $b$ on images subsampled by a factor $s$ and upsample them before line L5, which cuts the time to about $\Theta(WH/s^2)$ for the expensive part, with little visible change.
- **Weighted and gradient domain guided filters.** Li, Zheng, Zhu, Yao and Wu (2015) let $\varepsilon$ depend on an edge measure of the guide, and Kou, Chen, Wen and Li (2015) add a first order edge term, to reduce the halos.
- **Joint filtering.** With a different guide, for example a flash photo guiding a dark photo, or a color image guiding a depth map or a coarse matte, the filter transfers the structure of the guide to the input.
- **Color guide.** A color guide with the $3 \times 3$ covariance of line L3 keeps edges between regions of equal gray value but different color.
- **Detail enhancement.** Use $q$ as a base layer and boost $p - q$, as in [unsharp masking](/unsharp-masking/) with an edge aware blur.

## When to use it

Use the guided filter for fast edge aware smoothing, for base and detail decomposition, and for joint filtering: refining a transmission map in haze removal, a matte from a rough trimap, a depth map or a stereo cost volume by a color image. It is the usual choice when the radius is large, because its cost does not grow with $r$. Use the [bilateral filter](/bilateral-filter/) when the radius is small and a filter that is not linear in the input is wanted, and [non-local means](/non-local-means/) for strong noise.

## Pitfalls

- **The units of ε.** For an image stored in $[0, 1]$, $\varepsilon = 0.01$ keeps edges with a local standard deviation above about $0.1$; the same $\varepsilon$ for an image stored in $[0, 255]$ keeps almost everything. At line L3, scale $\varepsilon$ with the square of the range of $I$.
- **Wrong border normalization.** Dividing every box sum by $(2r+1)^2$ in line L1 and line L4 makes the means too small near the border, which darkens the border. Divide by the count of the pixels in the cut window, $n_k$.
- **Skipping the second mean.** Writing $q_i \leftarrow a_i I_i + b_i$ at line L5 uses one window per pixel and gives blocky, noisy output. The output is $\bar a_i I_i + \bar b_i$, the mean over all windows that hold $i$.
- **Cancellation in the variance.** At line L2, $c_{II} - \mu^2$ subtracts two large numbers; in single precision for values near 255 it can be negative or very wrong. Use double precision, or subtract a constant from $I$ first.
- **ε = 0.** With $\varepsilon = 0$, line L3 divides by zero in every flat window. Keep $\varepsilon > 0$.

## Implementations

## History

He, Sun and Tang presented the guided filter at ECCV 2010 and gave the full version, with Algorithm 1 in terms of box filters and the explicit kernel, in IEEE TPAMI in 2013. In their work on haze removal the same group had used a soft matting step to refine transmission maps, and the guided filter replaced it with a much faster local method. He and Sun (2015) later gave the fast guided filter with subsampling. The filter is part of common image processing libraries and is a standard step in haze removal, matting and depth refinement.

## References
