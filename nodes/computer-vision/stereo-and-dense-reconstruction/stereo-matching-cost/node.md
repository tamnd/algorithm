---
tag: RQ2T2Y
kind: concept
slug: stereo-matching-cost
name: Stereo matching cost
aliases:
- data cost
- pixel dissimilarity
area: computer-vision/stereo-and-dense-reconstruction
level: core
summary: A number that says how badly a left pixel matches a right pixel at a given disparity, such as an absolute difference, a census Hamming distance or mutual information.
prereqs: [disparity, stereo-matching]
see_also: [census-transform, normalized-cross-correlation, cost-volume, cost-aggregation, block-matching-stereo, semi-global-matching, hamming-distance, template-matching]
sources:
  - paper: doi:10.1023/A:1014573219977
    title: Daniel Scharstein and Richard Szeliski, A taxonomy and evaluation of dense two-frame stereo correspondence algorithms, International Journal of Computer Vision 47(1-3), 2002, 7-42
    locator: the part on matching cost computation (absolute and squared differences, truncated costs, sampling-insensitive costs, and normalized and non-parametric measures)
  - paper: doi:10.1109/34.677269
    title: Stan Birchfield and Carlo Tomasi, A pixel dissimilarity measure that is insensitive to image sampling, IEEE Transactions on Pattern Analysis and Machine Intelligence 20(4), 1998, 401-406
    locator: the whole paper (the dissimilarity from the linearly interpolated intensity range of the neighbors)
  - paper: doi:10.1007/BFb0028345
    title: Ramin Zabih and John Woodfill, Non-parametric local transforms for computing visual correspondence, Computer Vision, ECCV '94, Lecture Notes in Computer Science 801, Springer, 1994, 151-158
    locator: the rank and census transforms as matching costs
  - paper: "Heiko Hirschmüller and Daniel Scharstein, Evaluation of stereo matching costs on images with radiometric differences, IEEE Transactions on Pattern Analysis and Machine Intelligence 31(9), 2009"
    locator: the comparison of pixel, window and filter based costs under changes of exposure and light
  - paper: doi:10.1109/TPAMI.2007.1166
    title: Heiko Hirschmüller, Stereo processing by semiglobal matching and mutual information, IEEE Transactions on Pattern Analysis and Machine Intelligence 30(2), 2008, 328-341
    locator: the part on the pixelwise cost from mutual information
  - paper: "Jure Zbontar and Yann LeCun, Stereo matching by training a convolutional neural network to compare image patches, Journal of Machine Learning Research 17, 2016"
    locator: the learned matching cost and its use inside a classical stereo pipeline
  - book: isbn:9783030343712
    title: Richard Szeliski, Computer Vision, Algorithms and Applications, second edition, Springer, 2022
    locator: Chapter 12, Depth estimation (the matching costs of dense correspondence)
---

A stereo matching cost $C(p, d)$ is a number that says how badly the pixel $p = (u, v)$ of the left image matches the pixel $(u - d, v)$ of the right image of a rectified pair: small for a good match, large for a bad one. It is the first of the four steps of [stereo matching](/stereo-matching/) in the taxonomy of Scharstein and Szeliski (2002), and its values for all pixels and disparities fill the [cost volume](/cost-volume/). The choice of cost decides which differences between the two images the method ignores: noise, the position of the pixel grid, a change of gain or offset, or any change that keeps the order of intensities. This page compares the common costs. The [census transform](/census-transform/) page gives one of them as an algorithm with code.

## In plain words

To find the match of a pixel, a stereo program tries each possible shift and asks: how different do the two pixels look at this shift? The answer is the matching cost. The simplest answer subtracts the two brightness values. That fails when one camera makes everything a bit brighter, so other costs compare small patches after removing their mean, or after scaling them to the same contrast, or only compare which neighbors are darker. A cost that ignores more differences between the cameras also ignores some real differences between surfaces, so there is no single best cost.

## The idea

**Setting.** $I_L$ and $I_R$ are a rectified pair with the right camera to the right, so the true match of $(u, v)$ is $(u - d, v)$ for the true disparity $d \ge 0$. A cost is a function $C(p, d) \ge 0$. A pixel cost uses only the two pixels; a window cost uses a window $N(p)$ around each of them. Window costs already do some [aggregation](/cost-aggregation/); the line between the two steps is not sharp.

**Pixel costs.**

- **Absolute and squared difference.** $C_{AD} = |I_L(u, v) - I_R(u - d, v)|$ and $C_{SD} = C_{AD}^2$. For color, sum over the channels. The squared difference is the negative log likelihood of Gaussian noise, up to constants; the absolute difference is less hurt by single outliers.
- **Truncated costs.** $\min(C, T)$ for a threshold $T$. A wrong pixel, from an occlusion or a highlight, then adds at most $T$ to any sum, so it cannot dominate.
- **Birchfield and Tomasi (1998).** Let $I_R^{\pm} = \frac12 (I_R(x) + I_R(x \pm 1))$ be the values half a pixel to each side, and $I_{\min}$, $I_{\max}$ the least and the largest of $I_R^-$, $I_R(x)$, $I_R^+$. Then $\bar d(x_L, x_R) = \max(0, I_L(x_L) - I_{\max}, I_{\min} - I_L(x_L))$, the distance of the left value to the range of the right signal near $x_R$, and the cost is $\min(\bar d(x_L, x_R), \bar d(x_R, x_L))$ with the roles of the images swapped in the second term. It is zero when the two samples come from the same linear signal sampled at positions up to half a pixel apart, so it does not punish a disparity that is not an integer.
- **Gradient costs.** Compare the image gradients, for example of the [Sobel operator](/sobel-operator/), instead of the intensities. A gradient does not change when a constant is added to the image.
- **Mutual information.** Hirschmüller (2008) builds the joint histogram of the intensities of matched pixels, from a first disparity map, and sets the cost of a pair of intensities to minus their pointwise mutual information. It handles any fixed mapping of intensities between the cameras, even one that is not monotone, and it is computed per pixel.

**Window costs.**

- **SAD and SSD.** The sums of $C_{AD}$ and $C_{SD}$ over the window. [Block matching](/block-matching-stereo/) uses them.
- **Zero mean costs.** ZSAD and ZSSD subtract the mean of each window first. They are unchanged by an offset $I \mapsto I + \beta$.
- **Normalized cross-correlation.** [NCC](/normalized-cross-correlation/) of the two windows, usually with the cost $1 - \mathrm{NCC}$. It is unchanged by an affine change $I \mapsto \alpha I + \beta$ with $\alpha > 0$, on each window.
- **Rank and census.** Zabih and Woodfill (1994): the rank transform counts the neighbors darker than the center, and the [census transform](/census-transform/) writes one bit for each, compared with the [Hamming distance](/hamming-distance/). Both are unchanged by any strictly increasing change of the intensities on each window.
- **Learned costs.** Zbontar and LeCun (2016) trained a network to say whether two patches match and used its output as the cost, inside a classical pipeline. Most later learned methods build a [cost volume](/cost-volume/) of learned features.

**What each cost ignores.** The invariances are theorems about the formulas:

| cost | unchanged by |
|---|---|
| AD, SD, SAD, SSD | nothing but equal changes of both images |
| Birchfield-Tomasi | a shift of the sampling grid by up to half a pixel, on linear signals |
| gradient | an offset $I + \beta$ |
| ZSAD, ZSSD | an offset $I + \beta$ on each window |
| NCC | an affine change $\alpha I + \beta$, $\alpha > 0$, on each window |
| rank, census | any strictly increasing change, on each window |
| mutual information | any fixed one to one mapping of intensities over the image |

Which cost works best on real images is an empirical question. In the evaluation of Hirschmüller and Scharstein (2009), on images with changes of exposure and light, census was among the most robust costs overall, and the pixelwise costs were poor without a correction of the radiometry.

## Examples

**An offset and a gain.** Take the left window $(10, 20, 30)$ and the right window $(25, 45, 65)$, which is $2x + 5$ of the left one, so the two windows show the same surface under different camera settings.

| cost | value | why |
|---|---|---|
| SAD | 75 | $15 + 25 + 35$ |
| SSD | 2075 | $225 + 625 + 1225$ |
| ZSAD | 20 | means 20 and 45; $(-10, 0, 10)$ against $(-20, 0, 20)$ |
| $1 - \mathrm{NCC}$ | 0 | the windows are affinely related, so NCC $= 1$ |
| census at the center | 0 | in both windows the left neighbor is darker and the right one is brighter |

Only the last two costs see that this is a perfect match.

**Sampling.** A left row $(10, 50, 90)$ and a right row $(20, 80, 90)$ show an edge sampled at different positions. At the middle pixels, $C_{AD} = |50 - 80| = 30$. For Birchfield-Tomasi, the right values half a pixel to the sides are 50 and 85, so the right range is $[50, 85]$ and the left value 50 is in it: $\bar d(x_L, x_R) = 0$. The other term is $\bar d(x_R, x_L) = 80 - 70 = 10$, because the left range is $[30, 70]$. The cost is $\min(0, 10) = 0$: the two samples are consistent with one edge seen at a fractional shift.

**Truncation.** With $T = 20$, a window of nine pixels where eight match with $C_{AD} = 2$ and one is occluded with $C_{AD} = 200$ has the truncated sum $16 + 20 = 36$ instead of 216.

## Where it is used

- **Every dense stereo method.** [Block matching](/block-matching-stereo/), [adaptive support weights](/adaptive-support-weights/), [semi-global matching](/semi-global-matching/), [graph cut stereo](/graph-cut-stereo/) and [plane sweep stereo](/plane-sweep-stereo/) differ in what they do with the costs, but each starts with one of them. Census is the usual cost of semi-global matching in cars and robots.
- **Multi-view stereo.** [Multi-view stereo](/multi-view-stereo/) and [PatchMatch stereo](/patchmatch-stereo/) compare a patch of a reference image with several other images, mostly with NCC, because the views differ more in light and exposure than a stereo pair.
- **Other matching problems.** The same costs appear in [template matching](/template-matching/), [optical flow](/optical-flow/) and image registration, where the search is in two dimensions instead of along a row.

## References
