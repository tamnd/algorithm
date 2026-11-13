---
tag: 9B4AGD
kind: problem
slug: image-thresholding
name: Image thresholding
aliases:
- binarization
- gray-level thresholding
area: graphics-and-signals/image-processing
level: intro
summary: Turn a gray image into a binary image by comparing each pixel with a threshold, global or local, chosen by a criterion on the histogram or on a neighborhood.
prereqs: [image-histogram, digital-image]
see_also: [otsu-thresholding, hysteresis-thresholding, image-histogram, image-segmentation, image-labeling, integral-image, mathematical-morphology, k-means]
sources:
  - paper: doi:10.1117/1.1631315
    title: Mehmet Sezgin and Bülent Sankur, Survey over image thresholding techniques and quantitative performance evaluation, Journal of Electronic Imaging 13(1), 2004
    locator: the whole survey (the six groups of methods by the information they use, the uniform notation, and the local methods of Niblack and Sauvola)
  - paper: doi:10.1109/TSMC.1979.4310076
    title: Nobuyuki Otsu, A threshold selection method from gray-level histograms, IEEE Transactions on Systems, Man and Cybernetics 9(1), 62 to 66, 1979
    locator: the between-class variance criterion
  - paper: doi:10.1016/0031-3203(86)90030-0
    title: Josef Kittler and John Illingworth, Minimum error thresholding, Pattern Recognition 19(1), 41 to 47, 1986
    locator: the criterion from a two-Gaussian fit of the histogram
  - paper: doi:10.1016/S0031-3203(99)00055-2
    title: Jaakko Sauvola and Matti Pietikäinen, Adaptive document image binarization, Pattern Recognition 33(2), 225 to 236, 2000
    locator: the local threshold from the window mean and standard deviation
  - book: isbn:9780133356724
    title: Rafael C. Gonzalez and Richard E. Woods, Digital Image Processing, fourth edition, Pearson, 2018
    locator: Chapter 10, Image segmentation, Section 10.3, Thresholding
---

Image thresholding is the problem of turning a gray image into a binary image: each pixel becomes 1 (foreground) or 0 (background) by comparing its value with a threshold. The comparison itself is trivial. The problem is to choose the threshold so that the 1 pixels are the objects of interest, such as the ink on a page or the cells on a slide. A global method chooses one threshold for the whole image, usually from the [histogram](/image-histogram/); a local or adaptive method chooses a threshold for each pixel from a window around it. Thresholding is the simplest form of [image segmentation](/image-segmentation/), with two classes and a decision that depends on the value of the pixel (and its window) only. Its output is the usual input of [image labeling](/image-labeling/) and of [morphology](/mathematical-morphology/).

## In plain words

A gray photo has many shades. Many tasks want only two: ink or paper, cell or glass, part or table. Thresholding draws a line between the shades: everything darker than the line becomes black, everything lighter becomes white (or the other way round). The hard part is where to draw the line. One way looks at how many pixels have each shade, finds two piles of shades, and cuts in the valley between them. Another way draws a different line for each small area, which helps when one side of the page is in shadow. A bad line joins letters, breaks them apart, or fills the shadow with black.

## Definition

The input is a gray [digital image](/digital-image/) $I$ of $W \times H$ pixels with integer values in $\{0, \ldots, L-1\}$ (often $L = 256$) or real values in $[0, 1]$. Values may be gamma encoded or linear; a method sees only the numbers, and the two encodings give different results.

- **Global thresholding.** Choose one $t$, and output $B(p) = 1$ if $I(p) > t$ and $B(p) = 0$ otherwise. For integer values, only the $D - 1$ thresholds between the $D$ distinct values that occur give different nontrivial outputs, so the choice is one of at most $L - 1$ options. A method is a rule that picks $t$, usually from the histogram $h_0, \ldots, h_{L-1}$ alone.
- **Local (adaptive) thresholding.** Choose a threshold surface $t(p)$, usually from the pixels in a window $N(p)$ of size $k \times k$ centered at $p$, and output $B(p) = [I(p) > t(p)]$. The method must also fix a border rule for windows that leave the image (clamp, mirror or a smaller window).
- **Multilevel thresholding.** Choose $t_1 < \cdots < t_{M-1}$ and output the class index of each pixel. This gives $M$ classes.

The cost model is the word RAM, and the costs are in terms of $N = WH$, $L$ and $k$. Any method must read every pixel, so $\Omega(N)$ is a lower bound for every variant.

The criterion is the real content of the problem. It cannot be derived from the image alone, because "object" is a property of the task, not of the values. So each method states a model: two clusters of values, two Gaussian populations, a valley in the histogram, the most information, or a background that changes slowly.

## Variants

- **By the information used.** Sezgin and Sankur sort the methods into six groups: histogram shape (peaks and valleys, for example the triangle method), clustering (Otsu, iterative isodata, minimum error), entropy (maximize the information of the two classes), object attributes (match moments or edges), spatial methods (use a co-occurrence or 2D histogram) and local methods.
- **Inverted output.** Dark objects on a light background use $B(p) = [I(p) \le t]$. This changes nothing in the choice of $t$.
- **Band thresholding.** $B(p) = [t_1 < I(p) \le t_2]$ selects a range, for example one tissue type in a CT slice.
- **Hysteresis.** Two thresholds and connectivity: pixels above the high threshold are kept, and pixels above the low threshold are kept if they connect to a kept pixel. See [hysteresis thresholding](/hysteresis-thresholding/).
- **Color and multichannel.** Threshold each channel or a distance to a reference color, after a change of [color space](/color-spaces/). This is a classification problem in a few dimensions, and it is usually treated as segmentation.

## Examples

**Two clear groups.** Take the $6 \times 3$ image with rows $(0, 1, 1, 2, 6, 7)$, $(1, 1, 2, 2, 6, 6)$ and $(1, 0, 2, 5, 6, 7)$, with $L = 8$. Its histogram is $(2, 5, 4, 0, 0, 1, 4, 2)$. There are six distinct values, so five nontrivial global binarizations. The thresholds $t = 2, 3, 4$ give the same one, because levels 3 and 4 are empty, and [Otsu's method](/otsu-thresholding/) picks it: the eleven pixels with values 0 to 2 become 0 and the seven pixels with values 5 to 7 become 1. The pixel of value 5 is the only doubtful one. A method that cuts at the deepest valley of a smoothed histogram can put it on either side, depending on the smoothing.

**A ramp defeats every global threshold.** Take one row of eight pixels, $(40, 30, 80, 70, 120, 110, 160, 150)$, where the paper brightens from left to right and each odd pixel is a dark mark 10 levels below the paper next to it. The marks are 30, 70, 110 and 150, and the paper is 40, 80, 120 and 160. A global threshold that makes the mark 150 dark needs $t \ge 150$, and one that keeps the paper 40 light needs $t < 40$, so no global $t$ works. Otsu's method returns $t = 80$ and makes the left half dark and the right half light. A local threshold equal to the mean of the pixel and its two neighbors, with the border clamped, gives thresholds of about $36.7, 50, 60, 90, 100, 130, 140, 153.3$ and the output $(1, 0, 1, 0, 1, 0, 1, 0)$, which is exactly paper and marks.

**A window that holds only background.** The same local mean rule, applied to a window of plain paper, splits the paper noise in half and makes a speckle of false marks. Local methods guard against this. Niblack's rule uses $t(p) = m(p) + \kappa\, s(p)$ with the window mean $m$, the window standard deviation $s$ and a negative $\kappa$. Sauvola and Pietikäinen use $t(p) = m(p)\,(1 + \kappa(s(p)/R - 1))$ with $R$ the largest possible standard deviation (128 for 8-bit data) and $\kappa$ around 0.5. Where $s$ is small, the threshold falls below the mean and the paper stays white.

## Known algorithms

- [Otsu's thresholding](/otsu-thresholding/): maximize the between-class variance of the histogram, which is the global optimum of 2-means on the gray values, in $\Theta(N + L)$ time. It also extends to several thresholds.
- Iterative selection (Ridler and Calvard, isodata): repeat $t \leftarrow (\mu_0 + \mu_1)/2$, which is Lloyd's [k-means](/k-means/) iteration with two clusters. It can stop at a fixed point that is not the best split.
- Minimum error thresholding (Kittler and Illingworth): fit two Gaussians with their own means and variances to the two sides of each candidate threshold, and choose the threshold of least error. It is $\Theta(N + L)$ with cumulative moments up to the second order.
- Entropy methods (Kapur, Sahoo and Wong, and others): maximize the sum of the entropies of the two class histograms. Also $\Theta(N + L)$ with cumulative sums.
- Histogram shape methods: smooth the histogram and cut at the deepest valley between the two largest peaks, or use the triangle method for one peak with a long tail. They need a smoothing parameter.
- Local methods (Niblack, Sauvola and many variants): mean and standard deviation in a $k \times k$ window. With an [integral image](/integral-image/) of the values and of their squares, every window mean and variance costs $O(1)$, so the whole image costs $O(N)$ for any $k$.
- [Hysteresis thresholding](/hysteresis-thresholding/): two thresholds plus a connectivity pass, $O(N)$.

## Bounds

Every method must read each pixel, so $\Omega(N)$ time is necessary. Global methods whose criterion is a function of the cumulative moments $\sum_{i \le t} i^r h_i$ for a fixed set of $r$ (Otsu, minimum error, the entropy methods with a cumulative entropy sum) reach $\Theta(N + L)$: $\Theta(N)$ for the histogram and $\Theta(L)$ for the scan. Multilevel Otsu with $M$ classes costs $O(N + M L^2)$ by dynamic programming, against $\Theta(L^{M-1})$ candidate tuples for a direct search. Local methods with a window statistic that an integral image gives (sum, sum of squares) cost $O(N)$ time and $O(N)$ extra space for any window size; a direct window scan costs $O(N k^2)$. Local methods with an order statistic, such as a local median, need a [sliding-window median](/sliding-window-median/) structure instead.

There is no general correctness bound, because the true foreground is not a function of the image. A criterion can only be correct relative to its model. For example, if the two classes are Gaussian with known parameters, the Bayes threshold minimizes the expected number of misclassified pixels.

## Reductions

- **To clustering.** Global two-class thresholding with a squared error criterion is 2-means clustering of the pixel values. In one dimension an optimal clustering is always a split at a threshold, so the 1D problem is solved exactly, which [k-means](/k-means/) in higher dimensions is not.
- **To segmentation.** Thresholding is image segmentation with two labels where each decision depends on one value or one window. Methods such as [region growing](/region-growing/), [watershed](/watershed-segmentation/) or [graph cuts](/image-segmentation-graph-cuts/) add spatial coherence. A graph cut with the two class models as data terms and a smoothness term is a thresholding that is penalized for isolated pixels.
- **From thresholding to labeling.** The binary output becomes a set of objects by [connected component labeling](/connected-component-labeling/), which solves the [image labeling](/image-labeling/) problem.

## Applications

- Document binarization before character recognition, where local methods handle shadows and stains.
- Counting cells, colonies or particles in microscopy, after a global or local threshold and labeling.
- Industrial inspection with backlit parts, where the histogram has two clear peaks and a global threshold is reliable.
- Masks for later steps: morphology, [distance transforms](/distance-transform/), [skeletons](/image-skeletonization/) and shape [moments](/image-moments/) all start from a binary image.
- Medical images, where band thresholds select a tissue by its value range, for example bone in CT.

## References
