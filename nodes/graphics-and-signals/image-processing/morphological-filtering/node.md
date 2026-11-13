---
tag: KAHKFQ
kind: problem
slug: morphological-filtering
name: Morphological filtering
aliases:
- morphological image operations
area: graphics-and-signals/image-processing
level: advanced
summary: Remove or extract the bright and dark structures of a binary or gray image by their shape and size, with increasing and idempotent operators built from erosion and dilation.
prereqs: [morphological-opening, morphological-closing, structuring-element]
see_also: [mathematical-morphology, median-filter, sliding-window-maximum, watershed-segmentation, distance-transform, image-skeletonization, hit-or-miss-transform, image-smoothing]
sources:
  - book: isbn:9783540429883
    title: Pierre Soille, Morphological Image Analysis, Principles and Applications, second edition, Springer, 2003
    locator: Chapter 4, Opening and Closing (top-hats and granulometries); Chapter 6, Geodesic Transformations (reconstruction); Chapter 8, Filtering (morphological filters and alternating sequential filters)
  - book: isbn:9780126372403
    title: Jean Serra, Image Analysis and Mathematical Morphology, Academic Press, 1982
    locator: the chapters on openings, closings and size distributions (general locator)
  - paper: doi:10.1109/83.217222
    title: Luc Vincent, Morphological grayscale reconstruction in image analysis, applications and efficient algorithms, IEEE Transactions on Image Processing 2(2), 176 to 201, 1993
    locator: the definition of reconstruction by dilation and the queue based algorithms (general locator)
  - paper: doi:10.1016/0167-8655(92)90069-C
    title: Marcel van Herk, A fast algorithm for local minimum and maximum filters on rectangular and octagonal kernels, Pattern Recognition Letters 13(7), 517 to 521, 1992
    locator: the block prefix and suffix maxima that cost a constant number of comparisons per pixel
  - paper: doi:10.1109/34.211471
    title: Joseph Gil and Michael Werman, Computing 2-D min, median, and max filters, IEEE Transactions on Pattern Analysis and Machine Intelligence 15(5), 504 to 507, 1993
    locator: the min and max filters with a constant number of comparisons per pixel (general locator)
---

Morphological filtering removes or extracts parts of an image by their shape and size, not by their frequency. A small bright spot, a thin dark crack or a narrow peak is a structure into which a given structuring element does not fit, and an operator built from [erosion](/morphological-erosion/) and [dilation](/morphological-dilation/) can remove it while leaving larger structures exactly as they were. In the strict sense, a morphological filter is an operator that is increasing and idempotent: it keeps the order of images, and applying it twice changes nothing more. The [opening](/morphological-opening/) and the [closing](/morphological-closing/) are the basic filters, and compositions of them, reconstructions and their differences with the image give the rest of the toolbox: alternating sequential filters, top-hats, gradients and size distributions. For flat structuring elements, all of them reduce to moving minima and maxima.

## In plain words

Imagine a picture as a landscape, with bright pixels as high ground. Take a flat disc of a chosen size and push it up from below against the landscape, everywhere it can go. Peaks too narrow for the disc are cut off, and the rest of the landscape keeps its shape. That is an opening. Pressing the disc down from above fills pits and cracks too narrow for it. That is a closing.

Doing one after the other cleans both bright and dark specks of a given size. Subtracting the opened picture from the original keeps only the small bright things, such as text on an uneven background. Opening with larger and larger discs and measuring what is lost each time tells you how many things of each size the picture has.

## Definition

**Images and order.** An image is a function $f$ from a rectangle $D$ of pixels to a set of values with an order, such as $\{0, 1\}$ for binary images or $\{0, \dots, 255\}$ for gray images. For two images, $f \le g$ means $f(p) \le g(p)$ at every pixel.

**Morphological filter.** An operator $\psi$ on images is a morphological filter if it is

- **increasing:** $f \le g$ implies $\psi(f) \le \psi(g)$, and
- **idempotent:** $\psi(\psi(f)) = \psi(f)$.

It is an **opening** if it is also anti-extensive, $\psi(f) \le f$, and a **closing** if it is extensive, $\psi(f) \ge f$. The [opening](/morphological-opening/) $\gamma_B = \delta_B \varepsilon_B$ and the [closing](/morphological-closing/) $\varphi_B = \varepsilon_B \delta_B$ by a [structuring element](/structuring-element/) $B$ are the main examples; a supremum of openings is again an opening, and an infimum of closings is a closing.

**The problem.** Given an image and a description of what to remove or keep, by size, shape, orientation or contrast, build an operator from erosions, dilations, suprema, infima and differences that does it, in time close to linear in the number of pixels. Operators that are not filters in the strict sense, such as the top-hats and the gradient, are part of the same problem because they are built from the same parts.

## Variants

- **Alternating filters.** $\gamma\varphi$, $\varphi\gamma$, $\gamma\varphi\gamma$ and $\varphi\gamma\varphi$ for an opening $\gamma$ and a closing $\varphi$. Each is a morphological filter; $\gamma\varphi$ and $\varphi\gamma$ differ in which of bright and dark noise wins where they touch.
- **Alternating sequential filters.** $\gamma_n\varphi_n \cdots \gamma_2\varphi_2\,\gamma_1\varphi_1$, with structuring elements of growing size $1, 2, \dots, n$. Removing the small structures first keeps a large element from merging them with large ones; this is the usual way to denoise with morphology.
- **Filters by reconstruction.** The opening by reconstruction rebuilds, from the eroded image used as a marker, every bright structure that was not removed completely, by repeated geodesic dilation under $f$ until stability. Structures are kept or removed whole, and their outlines are never changed. For binary images, it keeps exactly the connected components that contain a pixel of the marker.
- **Area and attribute filters.** The area opening removes the bright connected components of each threshold set that have fewer than $\lambda$ pixels, whatever their shape. Other attributes, such as height, length or contrast, give other connected filters.
- **Top-hats.** The white top-hat $f - \gamma_B(f)$ keeps the bright structures that $B$ does not fit, and the black top-hat $\varphi_B(f) - f$ keeps the dark ones. They correct uneven background and find small objects.
- **Gradients.** $\delta_B(f) - \varepsilon_B(f)$, the morphological gradient, is large on edges; its two halves $\delta_B(f) - f$ and $f - \varepsilon_B(f)$ are the external and internal gradients.
- **Granulometry.** The family $\gamma_{nB}$, $n = 0, 1, 2, \dots$, sieves the image by size. The sums $\sum_p \gamma_{nB}(f)(p)$ decrease with $n$, and their drops, the pattern spectrum, count how much of the image has each size.
- **Binary or gray, flat or not.** All of the above work on binary images, on gray images with flat structuring elements, and with non-flat elements that add a height function.

## Examples

A gray row $f$ with a narrow peak (7), a narrow pit (0) and a plateau of width 3 (5), filtered with the flat segment of 3 pixels centered at the origin, ignoring the pixels outside the row:

| signal | values |
|---|---|
| $f$ | 2 2 7 2 2 2 0 2 2 5 5 5 2 2 |
| opening $\gamma(f)$ | 2 2 **2** 2 2 2 0 2 2 5 5 5 2 2 |
| closing $\varphi(f)$ | 2 2 7 2 2 2 **2** 2 2 5 5 5 2 2 |
| $\gamma\varphi(f)$ and $\varphi\gamma(f)$ | 2 2 2 2 2 2 2 2 2 5 5 5 2 2 |
| white top-hat $f - \gamma(f)$ | 0 0 5 0 0 0 0 0 0 0 0 0 0 0 |
| black top-hat $\varphi(f) - f$ | 0 0 0 0 0 0 2 0 0 0 0 0 0 0 |
| gradient $\delta(f) - \varepsilon(f)$ | 0 5 5 5 0 2 2 2 3 3 0 3 3 0 |

The opening removes the peak and keeps the plateau, which the segment fits, with its edges unchanged. The closing fills the pit. A linear smoothing filter would instead spread both the peak and the edges of the plateau. The top-hats find exactly the two removed structures with their contrast.

For the granulometry by segments of width 1, 3, 5 and 7, the sums of the openings are 40, 35, 26 and 26. The pattern spectrum has a drop of 5 at width 3, the peak, and a drop of 9 at width 5, the plateau, and nothing more: the row has one structure narrower than 3 and one of width 3 to 4.

## Known algorithms

| task | method | time for $N$ pixels | notes |
|---|---|---|---|
| flat erosion or dilation by a segment of length $k$ | van Herk (1992), Gil and Werman (1993) | $O(N)$, about 3 comparisons per pixel, for any $k$ | block prefix and suffix extremes; see [sliding window maximum](/sliding-window-maximum/) |
| flat erosion or dilation by a rectangle | the segment method on rows, then columns | $O(N)$ | the rectangle is the dilation of two segments |
| erosion or dilation by a digital disk, binary | threshold a [distance transform](/distance-transform/) | $\Theta(N)$ for any radius | exact with the Euclidean transform |
| erosion or dilation by an octagon or polygon | a cascade of segments in several directions | $O(N)$ per direction | the polygon is a Minkowski sum of segments |
| any flat structuring element | direct scan | $O(N \lvert B\rvert)$ | the brute force reference |
| reconstruction by dilation | the hybrid raster and queue algorithm of Vincent (1993) | close to linear in practice | two raster scans, then a FIFO queue |
| binary reconstruction | [flood fill](/flood-fill/) from the marker, or [connected component labeling](/connected-component-labeling/) | $O(N)$ | keep the components that meet the marker |
| area opening | union-find on the pixels sorted by value, or a max-tree | $O(N \log N)$ with sorting, less with a bucket sort | a connected filter |
| alternating sequential filter of size $n$ | $2n$ openings and closings | $O(nN)$ with the segment method | |

## Bounds

- **Linear time.** Every output pixel depends on the input, so $\Omega(N)$ is needed. For segments, rectangles, polygons and disks the methods above reach it, independent of the size of the structuring element.
- **Per element cost.** For a general flat element of $|B|$ pixels, the direct scan costs $\Theta(N|B|)$. Faster methods decompose $B$ into a Minkowski sum or a union of simple elements; not every element decomposes.
- **Idempotence saves work.** Applying an opening, a closing or an alternating filter a second time changes nothing, so a pipeline never needs to repeat one to reach a stable result.

## Reductions

- **To moving minima and maxima.** Flat gray erosion by a segment is a moving minimum, and dilation a moving maximum, so every filter above with flat line or rectangle elements reduces to the [sliding window maximum](/sliding-window-maximum/), applied along rows and columns.
- **Binary to gray.** Any composition of flat erosions, dilations, openings and closings commutes with thresholding: the threshold of $\psi(f)$ at level $t$ is the binary $\psi$ applied to the threshold of $f$ at $t$. So the gray filter is the stack of the binary filters of all threshold sets. The top-hats and the gradient are differences and do not commute in this way.
- **Disk operators to distance transforms.** Binary erosion, dilation, opening and closing by a digital disk reduce to thresholds of [distance transforms](/distance-transform/) of the image and of the result.
- **Binary reconstruction to connected components.** The binary opening by reconstruction is a selection of [connected components](/connected-components/), and the area opening is a selection by size.
- **Segmentation.** The morphological gradient followed by a [watershed](/watershed-segmentation/) is the standard morphological segmentation; filtering the gradient first by an alternating or reconstruction filter controls oversegmentation.

## Applications

- **Noise removal.** Opening and closing remove salt and pepper noise of a known size and keep edges sharp, an alternative to the [median filter](/median-filter/) when the noise is impulsive and the objects have a known minimum size.
- **Uneven illumination.** The white top-hat with an element larger than the objects removes a slowly varying background, for example before thresholding text or cells.
- **Size and shape measurement.** Granulometries give size distributions of grains, pores, particles and cells, without segmenting each object.
- **Industrial inspection.** Closings fill small gaps and openings find thin defects such as scratches, with line elements of a chosen direction.
- **Preprocessing.** Cleaning masks before [connected component labeling](/connected-component-labeling/), smoothing outlines before [skeletonization](/image-skeletonization/), and finding features with the [hit-or-miss transform](/hit-or-miss-transform/).

## References
