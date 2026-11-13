---
tag: K4FZJP
kind: problem
slug: edge-detection
name: Edge detection
aliases:
- edge extraction
area: graphics-and-signals/image-processing
level: intro
summary: Find the pixels of an image where the intensity changes sharply, as local maxima of the gradient magnitude along the gradient or as zero crossings of a second derivative.
model: word-ram
complexity:
  vars: {W: image width in pixels, H: image height in pixels}
  time: {worst: Θ(W H)}
prereqs: [digital-image, linear-filtering]
see_also: [canny-edge-detector, sobel-operator, laplacian-of-gaussian, line-detection, corner-detection, image-segmentation, feature-detection, image-thresholding]
sources:
  - book: isbn:9780133356724
    title: Rafael C. Gonzalez and Richard E. Woods, Digital Image Processing, fourth edition, Pearson, 2018
    locator: Section 10.2, Point, Line, and Edge Detection (the subsections Edge Models, Basic Edge Detection, The Marr-Hildreth Edge Detector and The Canny Edge Detector)
  - paper: doi:10.1109/TPAMI.1986.4767851
    title: John Canny, A computational approach to edge detection, IEEE Transactions on Pattern Analysis and Machine Intelligence 8(6), 679 to 698, 1986
    locator: the statement of the three criteria (detection, localization, single response) and the trade off between detection and localization
  - paper: doi:10.1098/rspb.1980.0020
    title: David Marr and Ellen Hildreth, Theory of edge detection, Proceedings of the Royal Society of London B 207, 187 to 217, 1980
    locator: the definition of edges as zero crossings of the Laplacian of a Gaussian smoothed image
  - paper: "Vincent Torre and Tomaso A. Poggio, On edge detection, IEEE Transactions on Pattern Analysis and Machine Intelligence 8(2), 147 to 163, 1986"
    locator: edge detection as numerical differentiation, an ill posed problem that needs regularization by a smoothing filter
  - book: isbn:9783030343712
    title: Richard Szeliski, Computer Vision, Algorithms and Applications, second edition, Springer, 2022
    locator: Section 7.2, Edges and contours
---

Edge detection is the problem of finding the places in an image where the intensity changes sharply. Such places are often the boundaries of objects, of shadows or of changes in the surface, so an edge map is a compact summary of the shape content of an image. The problem has no single formal answer. The two common definitions are the local maxima of the gradient magnitude along the gradient direction, and the zero crossings of a second derivative, each after smoothing at a chosen scale. Algorithms for the problem range from $3 \times 3$ gradient masks such as the [Sobel operator](/sobel-operator/) to the full pipeline of [Canny's detector](/canny-edge-detector/).

## In plain words

Look at a photograph and draw a line wherever one region stops and another starts: the outline of a cup, the edge of a shadow, the border of a printed letter. Edge detection asks a computer to make that drawing. A computer sees only a grid of brightness values. So it looks for places where the brightness jumps between near pixels. The difficulty is that noise also makes small jumps, and real edges are often a little blurred. A good detector finds the real edges, puts each one at the right place, and marks it only one time.

## Definition

The input is a gray [digital image](/digital-image/) $I$ with $H$ rows and $W$ columns. Pixel $(x, y)$ is a point sample at integer coordinates, with $x$ to the right and $y$ downward. There is one channel with values from 0 to 255, which we treat as linear in the light intensity. A read outside the image returns the nearest border pixel (the clamp rule). The output is an edge map: a set of pixels, often with a direction and a strength for each one. A pixel with a direction and a strength is an *edgel*.

The usual definition has three parts. First, a smoothing at a scale $\sigma$ gives a smooth image $f = G_\sigma * I$, where $G_\sigma$ is a Gaussian, as in the [Gaussian filter](/gaussian-filter/). Second, a point $p$ is an edge point when $|\nabla f|$ has a local maximum at $p$ along the direction $n = \nabla f / |\nabla f|$. In terms of derivatives along $n$, this is $\partial^2 f / \partial n^2 = 0$ with $\partial^3 f / \partial n^3 < 0$. Third, the edge points with a gradient magnitude that is too small are removed. The definition of Marr and Hildreth replaces the second part by the zero crossings of the Laplacian $\nabla^2 f$. The two definitions agree on straight edges, and they differ where an edge curves.

Canny stated three criteria for a detector of step edges in noise. *Detection*: the detector should miss few real edges and mark few false ones. *Localization*: the marked points should be near the true edge. *Single response*: each real edge should give one response, not several.

This page is about the low level problem of marking edge points. [Line detection](/line-detection/) groups edge points into straight lines, [image segmentation](/image-segmentation/) divides the image into regions, and [corner detection](/corner-detection/) finds points where the gradient changes in two directions.

## Variants

- **Edge strength.** The output is the gradient magnitude at each pixel, with no decision. The [Sobel operator](/sobel-operator/), the [Prewitt operator](/prewitt-operator/), the [Scharr operator](/scharr-operator/) and the [Roberts cross operator](/roberts-cross-operator/) solve this variant.
- **Binary edge map.** The output marks edge pixels. A plain threshold of the gradient magnitude gives thick edges. [Non-maximum suppression](/non-maximum-suppression/) gives edges one pixel wide.
- **Subpixel edges.** The output gives each edge point with a position finer than the pixel grid, for example from a parabola fitted across the maximum.
- **Edge contours.** The output is a set of curves. [Hysteresis thresholding](/hysteresis-thresholding/) links strong and weak edge pixels, and contour following turns the pixels into ordered chains.
- **Scale.** The scale $\sigma$ of the smoothing decides which edges appear. Detectors at several scales report the edges of fine detail and of large structure.
- **Color and multi channel images.** The gradient of each channel can point in a different direction, so the detector needs a rule that combines them.
- **Boundary detection.** The output marks the boundaries of objects, not every change of intensity. Learned detectors solve this variant from training data.

## Examples

- A vertical step: $I(x, y) = 0$ for $x \le 7$ and $I(x, y) = 100$ for $x \ge 8$. The true edge is the line $x = 7.5$. A $3 \times 3$ gradient mask gives the same large response at columns 7 and 8. A thin edge map marks one of the two columns in each row.
- A ramp: the intensity rises by 10 per pixel over 10 columns. The gradient magnitude is constant over the ramp, so without smoothing the ramp is a plateau of the magnitude and has no single maximum. With enough smoothing, both definitions mark one edge at the middle of the ramp.
- A thin bright line, one pixel wide, on a dark background. This is a *line edge* or *roof edge*: the gradient definition marks two edges, one on each side, and a ridge detector marks one line.
- Noise: a flat image with Gaussian noise has many small local maxima of the gradient. A threshold or hysteresis removes them.

## Known algorithms

| Algorithm | Output | Cost | Notes |
|---|---|---|---|
| [Roberts cross operator](/roberts-cross-operator/) | strength and direction | $\Theta(W H)$ | $2 \times 2$ diagonal differences, no smoothing |
| [Prewitt operator](/prewitt-operator/) | strength and direction | $\Theta(W H)$ | $3 \times 3$, least squares plane |
| [Sobel operator](/sobel-operator/) | strength and direction | $\Theta(W H)$ | $3 \times 3$, smoothing $[1, 2, 1]$ |
| [Scharr operator](/scharr-operator/) | strength and direction | $\Theta(W H)$ | $3 \times 3$, accurate direction |
| [Laplacian of Gaussian](/laplacian-of-gaussian/) | zero crossings | $\Theta(W H r)$ | Marr and Hildreth, closed contours |
| [Canny edge detector](/canny-edge-detector/) | thin linked edges | $\Theta(W H r)$ | Gaussian gradient, suppression, hysteresis |

Here $r$ is the radius of the Gaussian kernel, about $3\sigma$ or $4\sigma$. Recursive filters bring the Gaussian steps to $\Theta(W H)$ for any $\sigma$. The parts of Canny's detector, [non-maximum suppression](/non-maximum-suppression/) and [hysteresis thresholding](/hysteresis-thresholding/), have their own pages, because other detectors use them too.

## Bounds

- **Reading the input.** In the worst case every pixel must be read: a single pixel that differs from its neighbors makes edges around it, so an algorithm that does not read some pixel can be wrong on some input. So $\Omega(W H)$ time is needed, and the $3 \times 3$ operators meet this bound.
- **Detection against localization.** For a step edge in white Gaussian noise and a filter of width $w$, Canny showed that the signal to noise ratio grows as $\sqrt{w}$ and the localization criterion falls as $1/\sqrt{w}$, so their product does not depend on $w$. A wider filter finds edges in more noise but places them less exactly. No choice of the scale improves both.
- **Ill posed differentiation.** Differentiation increases high frequency noise without a bound. Torre and Poggio showed that edge detection becomes well posed only with a smoothing filter, which fixes a scale.

## Reductions

- **To linear filtering.** The gradient step of every detector here is a [linear filter](/linear-filtering/), so it reduces to [discrete convolution](/discrete-convolution/), and for large kernels to [convolution via the FFT](/convolution-via-fft/).
- **To connected components.** Hysteresis thresholding is a search for the [connected components](/connected-components/) of the weak edge pixels that hold a strong one, done by a [flood fill](/flood-fill/).
- **From segmentation.** The boundaries of the regions of a [segmentation](/image-segmentation/) are edges. In the other direction, closed edge contours give regions by a flood fill of their inside.
- **As input to other problems.** [Line detection](/line-detection/) with the [Hough transform](/hough-transform/), contour fitting with [active contours](/active-contours/), and feature matching all start from an edge map or a gradient image.

## Applications

- Object outlines for [image segmentation](/image-segmentation/) and for shape measurement.
- Straight lines for document analysis, lane detection and the calibration of cameras, through [line detection](/line-detection/).
- Gradient features for [feature detection](/feature-detection/), such as [SIFT](/sift/) and the [Harris corner detector](/harris-corner-detector/).
- Edge maps for stereo matching, for [image sharpening](/image-sharpening/) and for the compression of drawings.
- Inspection of manufactured parts and measurement of cells and organs in medical images.

## References
