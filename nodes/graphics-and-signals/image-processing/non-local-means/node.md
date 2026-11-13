---
tag: S75JEX
kind: algorithm
slug: non-local-means
name: Non-local means
aliases:
- NL-means
area: graphics-and-signals/image-processing
level: advanced
summary: Average the pixels of a search window, each weighted by how similar the patch around it is to the patch around the pixel being denoised.
solves: [image-denoising]
model: real-ram
complexity:
  vars: {W: image width in pixels, H: image height in pixels, S: search window radius, P: patch radius}
  time: {worst: Θ(W H S²), direct: Θ(W H S² P²)}
  space: {extra: Θ(W H)}
properties: {deterministic: true, linear: false, patch_based: true, in_place: false}
history:
  year: 2005
  people: [Antoni Buades, Bartomeu Coll, Jean-Michel Morel]
  note: Buades, Coll and Morel introduced non-local means at CVPR 2005 and compared it with earlier denoising methods through their method noise in a review of the same year.
prereqs: [bilateral-filter, integral-image]
see_also: [image-denoising, bilateral-filter, guided-filter, anisotropic-diffusion, total-variation-denoising, wiener-filter, k-nearest-neighbors, image-smoothing]
sources:
  - paper: doi:10.1109/CVPR.2005.38
    title: Antoni Buades, Bartomeu Coll and Jean-Michel Morel, A non-local algorithm for image denoising, IEEE Conference on Computer Vision and Pattern Recognition (CVPR), 2005
    locator: the definition of the NL-means weights, and the 21 by 21 search window and 7 by 7 patches used in the experiments
  - paper: doi:10.1137/040616024
    title: Antoni Buades, Bartomeu Coll and Jean-Michel Morel, A review of image denoising algorithms, with a new one, Multiscale Modeling and Simulation 4(2), 2005
    locator: the method noise and the NL-means algorithm
  - paper: doi:10.5201/ipol.2011.bcm_nlm
    title: Antoni Buades, Bartomeu Coll and Jean-Michel Morel, Non-local means denoising, Image Processing On Line 1, 2011
    locator: the pixelwise and patchwise implementations and their parameters
  - paper: doi:10.1109/ISBI.2008.4541250
    title: Jérôme Darbon, Alexandre Cunha, Tony F. Chan, Stanley Osher and Grant J. Jensen, Fast nonlocal filtering applied to electron cryomicroscopy, IEEE International Symposium on Biomedical Imaging (ISBI), 2008
    locator: the computation of all patch distances of one offset by an integral image
---

Non-local means (NL-means) removes noise by averaging pixels that have similar surroundings. For a pixel $p$, it compares the small patch around $p$ with the patch around every pixel $q$ of a search window, and gives $q$ the weight $w = e^{-d/h^2}$, where $d$ is the mean squared difference of the two patches. The output is the weighted mean of the values $f(q)$. A [bilateral filter](/bilateral-filter/) compares single values, which noise disturbs; a patch of $(2P+1)^2$ values is a much more reliable measure, and pixels on the same edge or in the same texture find each other even when they are not close. Buades, Coll and Morel introduced it in 2005. The direct cost is $\Theta(WHS^2P^2)$ for a search radius $S$ and a patch radius $P$, and the [integral image](/integral-image/) of the squared differences of each offset brings it to $\Theta(WHS^2)$.

## In plain words

To clean one pixel, look at the small square of pixels around it. Then look at many other pixels nearby, each with its own small square. If a square looks like the square of our pixel, its center pixel probably shows the same thing, only with different noise. Such pixels count much. Pixels whose squares look different count almost nothing.

The cleaned pixel is the weighted average of all these pixels. Noise is random, so averaging many similar pixels makes it cancel out. Edges and texture repeat, so they find good matches and stay sharp. The name says that the matches need not be next to the pixel.

## The problem

The input is a gray image $f$ with $W$ columns and $H$ rows, a search radius $S$, a patch radius $P$ and a filtering parameter $h > 0$ in the units of $f$. The patch distance of two pixels is

$$d(p, q) = \frac{1}{(2P+1)^2} \sum_{|t_x|, |t_y| \le P} \left( \tilde f(p + t) - \tilde f(q + t) \right)^2,$$

and the output is

$$g(p) = \frac{\sum_{q \in N(p)} e^{-d(p, q)/h^2}\, f(q)}{\sum_{q \in N(p)} e^{-d(p, q)/h^2}},$$

where $N(p)$ is the set of pixels $q$ of the image with $|q_x - p_x| \le S$ and $|q_y - p_y| \le S$. There are two border rules: the search window is cut at the image border, and a patch pixel outside the image takes the value of the nearest edge pixel, $\tilde f$ being the clamp extension of $f$. The original paper weighted the patch differences by a Gaussian; this page uses the uniform weights of the Image Processing On Line version.

## The algorithm

For one offset $o = q - p$, the squared differences $D(x) = (\tilde f(x) - \tilde f(x + o))^2$ do not depend on $p$, so one table of their prefix sums gives the distance of every patch pair with this offset in $O(1)$.

```pseudo id=main
NL-MEANS(f, S, P, h)
L1  for each offset o with |o_x| ≤ S and |o_y| ≤ S do
L2      D(x) ← (f̃(x) − f̃(x + o))² for each x of the image grown by P on every side
L3      T ← the integral image of D
L4      for each pixel p such that q = p + o is inside the image do
L5          d ← RECT-SUM(T, the patch of radius P around p) / (2P+1)²
L6          w ← exp(−d / h²)
L7          num[p] ← num[p] + w · f[q];  den[p] ← den[p] + w
L8  return g with g[p] = num[p] / den[p]
```

The arrays `num` and `den` start at 0. Line L1 runs over the $(2S+1)^2$ offsets of the search window. Line L2 computes the squared differences between the image and its copy shifted by $o$, over the image grown by $P$ pixels on every side, so that every patch lies inside the table; the values outside the image come from the clamp rule. Line L3 builds the [integral image](/integral-image/) of $D$ with a running row sum. Line L4 visits the pixels whose partner $q$ lies in the image, the cut search window, and line L5 reads the patch distance with one rectangle sum. Line L6 turns the distance into a weight, and line L7 adds the weighted value. After all offsets, line L8 divides. The offset $o = 0$ gives $d = 0$ and $w = 1$ at every pixel, so every denominator is at least 1.

## Example

Take the one-row image $f = (10, 12, 10, 50, 48, 50)$ with $S = 2$, $P = 1$ and $h = 10$. On a one-row image the rows of every patch are clamp copies of the image row, so $d$ is the mean of three squared differences. The trace for the pixel $p = 2$, whose patch is $(12, 10, 50)$:

| offset | $q$ | patch of $q$ | $d$ (line L5) | $w$ (line L6) | $w\,f(q)$ (line L7) |
|---|---|---|---|---|---|
| $-2$ | 0 | $(10, 10, 12)$ | 482.67 | 0.008013 | 0.0801 |
| $-1$ | 1 | $(10, 12, 10)$ | 536 | 0.004701 | 0.0564 |
| $0$ | 2 | $(12, 10, 50)$ | 0 | 1 | 10 |
| $+1$ | 3 | $(10, 50, 48)$ | 536 | 0.004701 | 0.2351 |
| $+2$ | 4 | $(50, 48, 50)$ | 962.67 | 0.000066 | 0.0032 |
| sums | | | | 1.017481 | 10.3748 |

Line L8 gives $g(2) = 10.3748 / 1.0175 = 10.1965$. The whole row:

| $x$ | 0 | 1 | 2 | 3 | 4 | 5 |
|---|---|---|---|---|---|---|
| $f$ | 10 | 12 | 10 | 50 | 48 | 50 |
| NL-means, $P = 1$ | 10.98268 | 11.01222 | 10.19651 | 49.80349 | 48.98778 | 49.01732 |
| $P = 0$, single values | 10.64901 | 10.68457 | 10.64902 | 49.35098 | 49.31543 | 49.35099 |

The edge is kept exactly: no pixel on one side takes weight from the other side. But the patch of $p = 2$ holds the edge, so no other patch in this short row is like it, and $p$ keeps most of its own weight. This shows the main weakness of the plain weights: the pixel itself always has the weight 1, the largest possible, and with few good matches it dominates.

## Correctness

For each offset the table $T$ holds the prefix sums of $D$, so line L5 returns the mean of $D$ over the patch of $p$, which is $d(p, p + o)$ by the definition of $D$. Each pair $(p, q)$ with $q$ in the cut search window is met once, at the offset $q - p$, so `num[p]` and `den[p]` are the two sums of the definition. The output at $p$ is a convex combination of the values in its search window. The full proof is below.

## Complexity

- **Time.** Each offset costs $\Theta((W + 2P)(H + 2P))$ for lines L2 and L3 and $O(WH)$ for lines L4 to L7, and there are $(2S+1)^2$ offsets. When $P$ is at most $W$ and $H$, the time is $\Theta(WHS^2)$, independent of the patch size. Direct evaluation of each patch distance costs $\Theta(P^2)$, for $\Theta(WHS^2P^2)$ in total.
- **Space.** The table $T$ of one offset and the arrays `num` and `den`, $\Theta(WH)$.
- **The full image as window.** With $N(p)$ the whole image, as the name suggests, the cost is $\Theta((WH)^2)$, which is why every practical version uses a search window. The paper used a $21 \times 21$ window and $7 \times 7$ patches.

## Properties

- **Not linear.** The weights depend on the image.
- **Range.** Each output value lies between the least and the largest value in the search window of its pixel.
- **Constants and shifts.** A constant image is kept, and adding a constant to the image adds it to the output, because the distances only see differences.
- **Consistency.** Buades, Coll and Morel showed that, for a stationary random field and a growing image, the weighted mean tends to the conditional expectation of the value of a pixel given its noisy neighborhood.
- **Method noise.** The difference $f - g$ is the method noise of Buades, Coll and Morel; for NL-means on natural images it looks much more like white noise than that of Gaussian, anisotropic or total variation filters, which means less structure is removed.
- **Self weight.** The center pixel always has $d = 0$ and the weight 1, the largest possible weight.

## Variants and improvements

- **Noise aware distance.** With Gaussian noise of standard deviation $\sigma$, the expected distance of two patches of the same clean content is $2\sigma^2$. The Image Processing On Line version uses $\max(d - 2\sigma^2, 0)$ in line L6 and gives $h$ and the sizes as functions of $\sigma$.
- **Center weight.** Replacing the self weight 1 by the largest weight of the other pixels of the window removes the dominance seen in the example.
- **Patchwise aggregation.** Denoise whole patches and average the overlapping estimates, which gives a smoother result for the same cost.
- **Fast versions.** Besides the per-offset integral images of Darbon et al. (2008), patch distances can be computed by the [FFT](/convolution-via-fft/), and similar patches can be found by reduced patch features or by search trees, as in [k-nearest neighbors](/k-nearest-neighbors/).
- **Block matching and 3D filtering.** BM3D (Dabov, Foi, Katkovnik and Egiazarian, 2007) groups similar patches and filters each group jointly in a transform domain; it is a stronger successor.
- **Other data.** The same weights are used for video, with the search window extended over time, for 3D medical images, and for regularization in inverse problems through nonlocal graph operators.

## When to use it

Use NL-means to remove Gaussian-like noise from photographs, scans and medical images when edges and repeated texture must be kept. Choose the patch size by the noise level and $h$ near the noise standard deviation times a constant; the paper suggests about $10\sigma$ for its weighted distance. Use the [bilateral filter](/bilateral-filter/) or the [guided filter](/guided-filter/) when speed matters more than quality, the [median filter](/median-filter/) for impulse noise, and a learned denoiser or BM3D when the best quality is needed.

## Pitfalls

- **The search over the whole image.** Taking $N(p)$ as the whole image at line L1 makes the cost $\Theta((WH)^2)$; a $512 \times 512$ image needs about $7 \cdot 10^{10}$ weights. Use a search window of radius $S$ of about 10.
- **Self weight dominance.** With the plain weights of line L6, the center pixel has $w = 1$ while good matches have less, so a pixel with few matches is barely denoised, as at $p = 2$ in the example. Give the center the largest weight of the others, or subtract the noise term $2\sigma^2$ from $d$.
- **Units of h.** With $d$ a mean of squared differences, $h$ is in the units of the values. Using $h = 10$ for an image stored in $[0, 1]$ gives $w \approx 1$ for every $q$, and line L6 makes a plain box mean. Scale $h$ with the noise and the value range.
- **Sum in place of mean.** Writing $d \leftarrow \mathrm{RECT}\text{-}\mathrm{SUM}(\ldots)$ at line L5 without the division by $(2P+1)^2$ makes $h$ depend on the patch size. Divide by the patch area, or scale $h^2$ by it.
- **Updating in place.** Writing $g$ into $f$ during the loops makes later distances use denoised values. Keep $f$ unchanged until line L8.

## Implementations

## History

Buades, Coll and Morel presented non-local means at CVPR 2005 and, in a review published the same year in Multiscale Modeling and Simulation, compared it with Gaussian smoothing, [anisotropic diffusion](/anisotropic-diffusion/), [total variation](/total-variation-denoising/), neighborhood filters and Wiener filters through their method noise. The idea of comparing neighborhoods comes from texture synthesis by Efros and Leung (1999). Fast versions with integral images (Darbon et al., 2008) and many others followed, and the Image Processing On Line paper of 2011 gave a reference implementation. NL-means led to the patch-based methods such as BM3D that dominated image denoising until learned methods.

## References
