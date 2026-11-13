---
tag: 103JD1
kind: concept
slug: image-histogram
name: Image histogram
aliases:
- intensity histogram
- gray-level histogram
area: graphics-and-signals/image-processing
level: intro
summary: The count of pixels at each gray level of an image, and its cumulative form; one pass computes it, and contrast, thresholding and statistics methods read it.
prereqs: [digital-image]
see_also: [histogram-equalization, contrast-stretching, otsu-thresholding, counting-sort, quantile, shannon-entropy, histogram, sliding-window-median]
sources:
  - book: isbn:9780133356724
    title: Rafael C. Gonzalez and Richard E. Woods, Digital Image Processing, fourth edition, Pearson, 2018
    locator: Section 3.3, Histogram Processing, pages 147 to 175 (Histogram Equalization, page 148; Histogram Matching, page 156; Local Histogram Processing, page 173; Using Histogram Statistics, page 174)
  - book: isbn:9783030343712
    title: Richard Szeliski, Computer Vision, Algorithms and Applications, second edition, Springer, 2022
    locator: Section 3.1.4, Histogram equalization
---

The histogram of a gray image with $L$ levels is the array $h[0..L-1]$ in which $h[k]$ is the number of pixels with value $k$. It forgets where the pixels are and keeps only how many there are of each level, so it shows at a glance whether an image is dark, bright, low in contrast, or split into two populations. One pass over the $W \times H$ pixels builds it in $\Theta(WH + L)$ time, and its running sum, the cumulative histogram, gives the rank of every level. It is the input of [histogram equalization](/histogram-equalization/), [contrast stretching](/contrast-stretching/) and [Otsu thresholding](/otsu-thresholding/); this page covers the array and what can be read from it, and those pages cover the maps built from it. The database [histogram](/histogram/) of the same name summarizes a column with a few buckets for query planning.

## In plain words

Take every pixel of a gray image and drop it into one of 256 buckets, one for each shade from black to white. Then count how full each bucket is and draw the counts as bars. That bar chart is the histogram. A dark photo has tall bars on the left. A washed-out photo has all its bars bunched in the middle. A photo of black text on white paper has two tall groups, one for the ink and one for the paper. The chart does not say where in the picture each shade is, only how much of it there is. That is often enough to choose a good brightness curve, to find a cut between dark and light, or to compare two pictures. Counting is fast, because each pixel is looked at once.

## The idea

**The model.** The image is one channel of integer values in $\{0, \ldots, L-1\}$, usually $L = 256$, as stored, so for 8-bit codes the levels are gamma encoded (see [gamma correction](/gamma-correction/)). Pixel positions do not matter, and no neighbor is read, so there is no border rule. With $N = WH$:

$$h[k] = \#\{(x, y) : I(x, y) = k\}, \qquad p[k] = \frac{h[k]}{N}, \qquad c(k) = \sum_{j \le k} h[j].$$

$p$ is the normalized histogram, an estimate of the probability of each level, and $c$ is the cumulative histogram, with $c(L-1) = N$.

**Computing it.** One loop adds 1 to $h[I(x, y)]$ for each pixel, and a running sum gives $c$. This is the counting step of [counting sort](/counting-sort/), and the cumulative histogram is its [prefix sum](/prefix-sums/). The cost is $\Theta(WH + L)$ time and $\Theta(L)$ space. For float images or 16-bit data, values are grouped into $B$ bins of equal width first, and the choice of $B$ trades detail against noise in the counts.

**What it tells.** From $h$ alone, without the image:

- The mean is $\mu = \sum_k k\,p[k]$ and the variance is $\sigma^2 = \sum_k (k - \mu)^2 p[k]$; these are the histogram statistics that Gonzalez and Woods use for local enhancement.
- The rank of a level is $c(k)$, so the median and any [quantile](/quantile/) come from the first $k$ where $c(k)$ passes the target count.
- The [Shannon entropy](/shannon-entropy/) $-\sum_k p[k] \log_2 p[k]$ is the bits per pixel that an ideal coder would need if the pixels were independent.
- Two peaks with a valley between them suggest a threshold, which [Otsu's method](/otsu-thresholding/) chooses by maximizing the between-class variance.

**What it does not tell.** Many different images have the same histogram: any permutation of the pixels keeps it. So a histogram cannot see blur, noise patterns or structure, and a method built only on it treats every pixel of a level the same way. Local methods, such as [CLAHE](/clahe/), compute a histogram for each region to bring position back in.

**Color.** For color, one histogram per channel loses the joint distribution: an image with red and green pixels and one with yellow and black pixels can have the same R and G histograms. A joint histogram over the three channels, usually with coarse bins, keeps it. A joint histogram of two images, with $h[a][b]$ the count of positions with value $a$ in one and $b$ in the other, is the basis of mutual information in [image registration](/image-registration/).

## Examples

With $L = 8$, the $4 \times 3$ image with rows $(0, 1, 1, 2)$, $(1, 2, 2, 3)$ and $(2, 3, 7, 7)$ has this histogram:

| $k$ | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 |
|---|---|---|---|---|---|---|---|---|
| $h[k]$ | 1 | 3 | 4 | 2 | 0 | 0 | 0 | 2 |
| $c(k)$ | 1 | 4 | 8 | 10 | 10 | 10 | 10 | 12 |

The mean is $31/12 \approx 2.583$, the variance is $659/144 \approx 4.576$, and the entropy is about 2.189 bits per pixel. The lower median of the 12 values is the 6th smallest, the first $k$ with $c(k) \ge 6$, which is 2. The empty bins 4 to 6 show the gap between the main group and the two bright pixels.

- **A constant image.** All $N$ pixels are in one bin. The variance and the entropy are 0, and every contrast map built from the histogram either does nothing or must treat this case apart, as [contrast stretching](/contrast-stretching/) does.
- **The same histogram, different images.** A left-to-right ramp and a random shuffle of its pixels have the same histogram. Histogram methods give both the same map, although one is smooth and the other is noise.
- **After equalization.** [Histogram equalization](/histogram-equalization/) maps each level through $c$, so the output histogram is roughly flat; it cannot split one bin into several, so tall bins stay tall and some levels stay empty.

## Where it is used

Point operations for [contrast enhancement](/contrast-enhancement/) are built from it: [histogram equalization](/histogram-equalization/) maps through the cumulative histogram, [contrast stretching](/contrast-stretching/) reads two quantiles from it, and histogram matching maps one image so that its histogram follows another. [Image thresholding](/image-thresholding/) and [Otsu's method](/otsu-thresholding/) choose a cut from it. The running median filter keeps a histogram of the window and updates it as the window slides, which is a [sliding-window median](/sliding-window-median/) for small integer values. Camera software shows it to judge exposure, color reduction methods such as [median cut](/median-cut/) split color histograms, and content-based image retrieval compares color histograms between images.

## References
