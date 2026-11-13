---
tag: Z6JDBM
kind: problem
slug: template-matching
name: Template matching
aliases:
- pattern matching in images
area: graphics-and-signals/image-processing
level: intro
summary: Find the positions where a small template image best matches a larger image under a score such as the sum of squared differences or normalized cross-correlation.
model: word-ram
complexity:
  vars: {W: image width in pixels, H: image height in pixels, p: template width in pixels, q: template height in pixels}
  time: {worst: O(W H log(W H))}
prereqs: [digital-image]
see_also: [normalized-cross-correlation, phase-correlation, image-registration, cross-correlation, integral-image, bird-baker, gaussian-pyramid, feature-detection]
sources:
  - book: isbn:9780133356724
    title: Rafael C. Gonzalez and Richard E. Woods, Digital Image Processing, fourth edition, Pearson, 2018
    locator: Section 13.3, Pattern classification by prototype matching, the part on using correlation for 2-D prototype matching
  - book: isbn:9783030343712
    title: Richard Szeliski, Computer Vision, Algorithms and Applications, second edition, Springer, 2022
    locator: Chapter 9, Motion estimation (translational alignment and the error metrics for it)
  - paper: doi:10.1109/TC.1972.5008923
    title: Daniel I. Barnea and Harvey F. Silverman, A class of algorithms for fast digital image registration, IEEE Transactions on Computers C-21(2), 179-186, 1972
    locator: the whole paper (the sequential similarity detection algorithms, which stop a sum of absolute differences early)
  - paper: doi:10.1137/0207043
    title: Theodore P. Baker, A technique for extending rapid exact-match string matching to arrays of more than one dimension, SIAM Journal on Computing 7(4), 533-541, 1978
    locator: the whole paper (exact matching of an array pattern in linear time)
---

Template matching is the problem of finding where a small image, the template, appears in a larger image. The template is moved over every position of the image, a score compares it with the pixels under it, and the positions with the best scores are the answer. The common scores are the sum of squared differences, the sum of absolute differences, plain cross-correlation and [normalized cross-correlation](/normalized-cross-correlation/). The scores differ in what changes of the image they ignore. A direct computation costs $O(WHpq)$ for a $W \times H$ image and a $p \times q$ template, and the FFT brings the products to $O(WH \log(WH))$ for every score that is built from sums and one cross term. The problem only searches over shifts. When the object can also turn, change its size or look different from another view, the methods of [image registration](/image-registration/) and [feature detection](/feature-detection/) are needed.

## In plain words

You have a photo of a circuit board and a small picture of one chip. You want to know where the chip is on the board. Put the small picture on the top-left corner of the photo and compare the two, pixel by pixel. Write down how well they agree. Move the small picture one pixel to the right and compare again, and go on row by row until every place has a number. The place with the best number is the answer. How you compare matters. If you only add up the differences, a darker copy of the chip looks like a bad match. A better comparison first removes the brightness and the contrast of each part and then looks only at the pattern.

## Definition

The input is a [digital image](/digital-image/) $I$ with $W$ columns and $H$ rows and a template $T$ with $p$ columns and $q$ rows, $p \le W$ and $q \le H$. Both have one channel with integer values, for example 0 to 255, used as they are stored with no gamma step. Pixel $(x, y)$ is a point sample at the integer point $(x, y)$, with $x$ to the right and $y$ down. An offset $(u, v)$ is *valid* when the template placed with its top-left pixel at $(u, v)$ lies fully inside the image, that is $0 \le u \le W - p$ and $0 \le v \le H - q$. With valid offsets only, no border rule is needed. The window at $(u, v)$ is $I_{u,v}(i, j) = I(u + i, v + j)$ for $0 \le i < p$ and $0 \le j < q$.

A score $s(u, v)$ compares $I_{u,v}$ with $T$. The usual ones are

$$\mathrm{SSD}(u, v) = \sum_{i,j} \big(I_{u,v}(i, j) - T(i, j)\big)^2, \qquad \mathrm{SAD}(u, v) = \sum_{i,j} \big|I_{u,v}(i, j) - T(i, j)\big|,$$

$$\mathrm{CC}(u, v) = \sum_{i,j} I_{u,v}(i, j)\, T(i, j), \qquad \mathrm{NCC}(u, v) = \frac{\sum_{i,j} (I_{u,v} - \bar I_{u,v})(T - \bar T)}{\sqrt{\sum_{i,j} (I_{u,v} - \bar I_{u,v})^2 \sum_{i,j} (T - \bar T)^2}},$$

where the bars are the means over the $pq$ pixels. SSD and SAD are best when small, CC and NCC when large. The output is one of three things: the best offset, the $k$ best offsets, or all offsets whose score passes a threshold $\tau$. A *score map* is the table of $s(u, v)$ over all $(W - p + 1)(H - q + 1)$ valid offsets.

The problem is about shifts by whole pixels. Shifts by a fraction of a pixel, turns and changes of scale are variants below.

## Variants

- **Exact matching.** The score is 1 when the window equals the template and 0 otherwise. This is two-dimensional string matching, and it has exact linear-time algorithms.
- **Robust scores.** SAD gives less weight than SSD to a few very wrong pixels, for example where something covers the object. Truncated scores limit each term.
- **Photometric invariance.** NCC does not change when the window is replaced by $aI + b$ with $a > 0$. SSD changes under both. Zero-mean SSD, which subtracts the means first, ignores $b$ but not $a$.
- **Subpixel position.** A parabola through the best score and its two neighbours along each axis gives a position finer than the grid.
- **Several templates.** A set of templates for different views, sizes or turns of the object is searched, and the best over the set is kept. The cost grows with the size of the set.
- **Partial overlap.** Offsets where the template is only partly inside the image are allowed, with the score taken over the overlap. Then the score must be normalized by the size of the overlap.
- **Color.** The score adds the terms of all channels, or uses a vector form of NCC. The choice of the color space changes the result.
- **Detection of a class.** When the target is any face or any car and not one fixed picture, a single template is not enough, and the problem becomes a learned detection problem such as [face detection](/face-detection/).

## Examples

Take an image with $W = 5$ and $H = 2$ and a template with $p = q = 2$:

$$I = \begin{pmatrix} 0 & 1 & 3 & 1 & 5 \\ 0 & 2 & 4 & 3 & 7 \end{pmatrix}, \qquad T = \begin{pmatrix} 1 & 3 \\ 2 & 4 \end{pmatrix}.$$

There are four valid offsets, $u = 0, 1, 2, 3$ and $v = 0$. The window at $u = 1$ is equal to $T$, and the window at $u = 3$ is $2T - 1$, a copy with twice the contrast and a lower offset.

| $u$ | window (row by row) | SSD | SAD | CC | NCC |
|---|---|---|---|---|---|
| 0 | $0, 1, 0, 2$ | 13 | 7 | 11 | 0.944 |
| 1 | $1, 3, 2, 4$ | 0 | 0 | 30 | 1 |
| 2 | $3, 1, 4, 3$ | 13 | 7 | 26 | $-0.308$ |
| 3 | $1, 5, 3, 7$ | 14 | 6 | 50 | 1 |

SSD and SAD find the exact copy at $u = 1$. SSD ranks the brighter copy at $u = 3$ last of all, while SAD ranks it second. Plain CC picks $u = 3$ only because its pixels are large: CC grows with the brightness of the window, so it is a poor score unless the image has a constant brightness. NCC gives exactly 1 at both copies, because it ignores the change of contrast and offset; it cannot say which copy is the original. The window at $u = 0$ has an NCC of $0.944$ even though it is quite different in value, because its pattern rises in the same places as $T$.

## Known algorithms

| Method | Scores | Cost | Notes |
|---|---|---|---|
| Direct sliding window | any | $\Theta((W - p + 1)(H - q + 1)\, pq)$ | simple, best for small templates |
| FFT for the cross term, [integral images](/integral-image/) for the sums | SSD, CC, NCC | $O(WH \log(WH))$ | uses [convolution via the FFT](/convolution-via-fft/) |
| [Normalized cross-correlation](/normalized-cross-correlation/) | NCC | direct or FFT, as above | invariant to gain and offset |
| Sequential similarity detection (Barnea and Silverman, 1972) | SAD | $\Theta((W - p + 1)(H - q + 1)\, pq)$ in the worst case | stops a sum early when it passes a bound; the saving is observed, not guaranteed |
| Coarse to fine on a [Gaussian pyramid](/gaussian-pyramid/) | any | the direct work falls by a factor of about 16 per level | a heuristic: a thin detail can vanish at a coarse level and the true offset can be missed |
| [Bird-Baker algorithm](/bird-baker/) | exact match | $O(WH + pq)$ worst case | rows of the template are named, then columns are matched |
| Two-dimensional rolling hash, as in [Rabin-Karp](/rabin-karp/) | exact match | $O(WH + pq)$ expected | a hash collision needs a check |
| [Phase correlation](/phase-correlation/) | whole-image shift | $O(WH \log(WH))$ | for two images of the same size, not a small template |

The direct method is often the fastest in practice when $pq$ is small, for example a template of $8 \times 8$ pixels, because the FFT has a large constant and needs padding.

## Bounds

- **Reading the input.** Any exact algorithm for the best SSD, SAD or NCC offset must read every pixel of the template and every pixel that some valid window covers, since a change of one such pixel can change the answer. So $\Omega(WH + pq)$ time is needed in the worst case. The exact-match algorithms meet this bound.
- **The direct cost.** The direct method does $(W - p + 1)(H - q + 1)\, pq$ multiplications or differences. For a fixed image this product is largest when $p \approx W/2$ and $q \approx H/2$, where it is about $W^2 H^2 / 16$. The FFT method costs $O(WH \log(WH))$ for every template size.
- **No exact answer under noise.** With noise, the true position need not have the best score. Template matching returns the best score, and whether that is the right place depends on the noise and on how distinct the template is. A template with a repeated pattern, or a flat one, has several offsets with nearly the same score.

## Reductions

- **SSD to cross-correlation.** $\mathrm{SSD}(u, v) = \sum I_{u,v}^2 - 2\,\mathrm{CC}(u, v) + \sum T^2$. The first sum comes from an integral image of $I^2$ in $O(1)$ per offset, and the last does not depend on the offset, so the best SSD needs one [cross-correlation](/cross-correlation/) and two tables. The same holds for NCC with the tables of $I$ and $I^2$.
- **Cross-correlation to the FFT.** CC is a [discrete convolution](/discrete-convolution/) of $I$ with the template turned by $180°$. By the [convolution theorem](/convolution-theorem/) it is a product of transforms. Padding the template with zeros to the size $W \times H$ of the image is enough when only valid offsets are needed, because their sums do not wrap around.
- **SAD for a small range of values.** For integers in $0$ to $L - 1$, $|a - b|$ is the number of levels $t$ with $a > t \ge b$ or $b > t \ge a$. So SAD is a sum over $t$ of cross-correlations of the 0 or 1 images $[I > t]$ and $[T \le t]$ and the reverse pair. This gives $O(L\, WH \log(WH))$, which is useful only for a small $L$.
- **Exact matching to string matching.** Exact two-dimensional matching reduces to one-dimensional [string matching](/string-matching/) over the names of the template rows, which is the idea of the Bird-Baker algorithm.
- **As a step of other problems.** [Image registration](/image-registration/) by translation, the tracking of a patch from frame to frame, and the matching of patches around feature points all use template matching.

## Applications

- Finding a part, a mark or a printed symbol on a production line, where the object and the camera are fixed and only the position changes.
- Tracking a small patch from one video frame to the next, and block matching for motion estimation in video coding.
- Stereo matching, where a patch of the left image is searched along a line of the right image.
- Registration of images that differ by a translation, such as frames of a scanner or tiles of a microscope.
- Matching of patches around feature points found by [feature detection](/feature-detection/).

## References
