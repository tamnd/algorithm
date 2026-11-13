---
tag: 7AQXHX
kind: problem
slug: contrast-enhancement
name: Contrast enhancement
aliases:
- contrast adjustment
- contrast improvement
area: graphics-and-signals/image-processing
level: intro
summary: Remap the gray levels of an image, globally or per region, so that detail differs more from its surround, while keeping the gray order and not boosting noise.
prereqs: [digital-image, image-histogram]
see_also: [contrast-stretching, histogram-equalization, clahe, gamma-correction, unsharp-masking, image-sharpening, image-noise, image-quality-assessment]
sources:
  - book: isbn:9780133356724
    title: Rafael C. Gonzalez and Richard E. Woods, Digital Image Processing, fourth edition, Pearson, 2018
    locator: Section 3.2, Some Basic Intensity Transformation Functions, page 136; Section 3.3, Histogram Processing, pages 147 to 175
  - paper: doi:10.1364/JOSAA.7.002032
    title: Eli Peli, Contrast in complex images, Journal of the Optical Society of America A 7(10), 1990
    locator: pages 2032 to 2040 (the Michelson and Weber definitions, and a local, band-limited contrast for complex images)
  - book: isbn:9783030343712
    title: Richard Szeliski, Computer Vision, Algorithms and Applications, second edition, Springer, 2022
    locator: Section 3.1, Point operators, and Section 3.1.4, Histogram equalization
---

Contrast enhancement is the problem of changing the values of an image so that the differences that carry detail become larger and easier to see. The common form asks for a monotone map $T$ of the gray levels, the same for every pixel, chosen from the image, often from its [histogram](/image-histogram/); local forms let the map depend on the position. There is no single objective: the methods trade a measure of contrast against keeping the gray order, using the output range well, not boosting noise, and avoiding unnatural results. The main methods are [contrast stretching](/contrast-stretching/), [histogram equalization](/histogram-equalization/), [CLAHE](/clahe/), the power law of [gamma correction](/gamma-correction/) and [unsharp masking](/unsharp-masking/).

## In plain words

A photo taken in fog, an X-ray, or a scan of faded paper can contain all the detail you need but show it as small steps between similar grays. Contrast enhancement makes those steps bigger. The simplest way is to give each gray a new gray from a fixed table: spread out the grays that are in use, or give more room to the grays that are common. A darker gray should stay darker than a lighter one, so the picture still looks like itself. Other ways adapt the table to each part of the image, or make edges stronger. Every way has a cost. Spreading out the grays also spreads out the noise, a too strong change makes halos and false contours, and a change that helps one region can hurt another.

## Definition

**The model.** The input is a gray [digital image](/digital-image/) $I$ of $W \times H$ pixels with integer values in $\{0, \ldots, L-1\}$, one channel, used as stored, so for 8-bit codes the values are gamma encoded. Point methods read no neighbors and need no border rule; local methods state their border rule and their pixel center convention.

**The global problem.** Given $I$, find a map $T : \{0, \ldots, L-1\} \to \{0, \ldots, L-1\}$ and output $O(x, y) = T(I(x, y))$, such that

- $T$ is nondecreasing, so that the gray order is kept, and
- a chosen contrast measure of $O$ is large, or the histogram of $O$ is close to a target.

**The local problem.** Find maps $T_{x,y}$ that depend on the position, each nondecreasing, and that change slowly with $(x, y)$ so that no seams appear.

**Measures of contrast.** Peli reviews the two classic definitions. For a periodic pattern with the extreme values $I_{\max}$ and $I_{\min}$, the Michelson contrast is $(I_{\max} - I_{\min})/(I_{\max} + I_{\min})$. For a small target of value $I$ on a uniform background $I_b$, the Weber contrast is $(I - I_b)/I_b$. A third common measure, the RMS contrast of an image scaled to $[0, 1]$, is the standard deviation of its values. These measures were made for simple patterns; for complex images, Peli defines a local contrast in each frequency band. No measure covers all uses, so each method fixes its own target: the full range for stretching, a flat histogram for equalization, and a bounded slope per region for CLAHE.

## Variants

- **Global point operations.** One table for all pixels: linear stretching, power and log curves, and histogram equalization or matching.
- **Local or adaptive operations.** The table depends on a region around each pixel: adaptive histogram equalization, [CLAHE](/clahe/), and local mean and variance methods.
- **Edge and detail boosting.** Add a high-pass part back to the image, as in [unsharp masking](/unsharp-masking/) and [image sharpening](/image-sharpening/). This raises local contrast at edges without a gray-level table.
- **Color images.** Enhance a brightness channel, such as $Y'$, $L^*$ or $V$ of a [color space](/color-spaces/), and keep the color channels, so that the hues stay.
- **High dynamic range.** Compress a range far larger than the display while keeping local contrast. This is tone mapping, a related problem with its own methods.
- **Enhancement for a task.** For a later step, such as [thresholding](/image-thresholding/) or [edge detection](/edge-detection/), the goal is the result of that step, not the look.

## Examples

- **A low-contrast patch.** The $3 \times 3$ image with the values $60, 70, \ldots, 140$, one pixel each, has a Michelson contrast of $80/200 = 0.4$ and an RMS contrast of about 0.101 on the scale $[0, 1]$ with 255 as 1. The min-max [contrast stretch](/contrast-stretching/) maps it to $0, 32, 64, 96, 128, 159, 191, 223, 255$, with a Michelson contrast of 1 and an RMS contrast of about 0.322.
- **A peak in the histogram.** If most pixels are in a few gray levels, as in a bright sky over a dark landscape, [histogram equalization](/histogram-equalization/) gives those levels most of the output range. A linear stretch cannot do this, because it keeps the spacing.
- **Two regions.** A scene with a dark half and a bright half needs a different curve in each half. One global table cannot improve both, and [CLAHE](/clahe/) uses a table per tile.
- **A flat image with noise.** On a nearly constant region, equalization spreads the few levels in use over the full range, and the noise becomes strong grain. The clip limit of CLAHE bounds this.
- **Not contrast enhancement.** Denoising, such as the [median filter](/median-filter/), lowers unwanted variation and does not try to enlarge differences in detail, although it is often run before an enhancement step.

## Known algorithms

| method | type | cost for $W \times H$ pixels, $L$ levels | what it targets |
|---|---|---|---|
| [contrast stretching](/contrast-stretching/) | global, linear between two quantiles | $\Theta(WH + L)$ | the full output range |
| [gamma correction](/gamma-correction/), power and log curves | global, fixed curve | $\Theta(WH + L)$ with a table | lift or darken the midtones |
| [histogram equalization](/histogram-equalization/) | global, from the cumulative histogram | $\Theta(WH + L)$ | a flat output histogram |
| [CLAHE](/clahe/) | local, a clipped table per tile, blended | $\Theta(WH + tL)$ for $t$ tiles | flat local histograms with a bounded slope |
| [unsharp masking](/unsharp-masking/) | local, linear filter | $\Theta(WH)$ per pass of a separable or box blur | stronger edges and fine detail |

All global methods follow the same pattern: one pass for the [image histogram](/image-histogram/), $\Theta(L)$ work for the table, and one pass to apply it.

## Bounds

- **Each pixel must be read.** Any method whose output depends on every pixel takes $\Omega(WH)$ time, so the global methods, at $\Theta(WH + L)$, are optimal up to a constant factor.
- **A table cannot split a level.** A point map sends equal inputs to equal outputs, so the output has at most as many distinct levels as the input. Equalization therefore cannot make the histogram of an image with one tall bin flat, and an image with 20 levels in use has at most 20 after any point map.
- **Monotone maps keep the order but can merge levels.** A nondecreasing $T$ can map two input levels to one output level, which loses detail. Linear stretching with ends inside the range is injective between its ends; equalization merges levels with small counts.

## Reductions

- **Histogram matching to the uniform target** is histogram equalization, and matching in general composes the equalization map of the input with the inverse of the equalization map of the target.
- **CLAHE with one tile and no clip** is global histogram equalization.
- **Color to gray.** Contrast enhancement of a color image reduces to the gray problem on a brightness channel, followed by the inverse color conversion.
- **Thresholding** is the limit of a piecewise linear stretch with both control points at the same input level, which maps the image to two levels.

## Applications

Contrast enhancement is used in medical imaging, where Pizer and coauthors studied adaptive equalization for the display of CT and other medical images, in remote sensing and astronomy for the display of data with a high bit depth, in photography for automatic levels and curves, in document scanning before thresholding, and as a preprocessing step in computer vision. In all of these, an enhanced image is for viewing or for a later step; measurements of intensity should use the original values. Measures from [image quality assessment](/image-quality-assessment/) compare an image with a reference, so they do not directly score enhancement, which has no reference.

## References
