---
tag: BK37D0
kind: concept
slug: digital-image
name: Digital image
aliases:
- raster image
- pixel array
area: graphics-and-signals/image-processing
level: intro
summary: A W by H grid of pixels with C channels of quantized values, made by sampling and quantizing a continuous image, plus the conventions that give its values meaning.
prereqs: [pixel, sampling-theorem, scalar-quantization]
see_also: [frame-buffer, image-histogram, color-spaces, gamma-correction, image-noise, aliasing, linear-filtering, image-resampling]
sources:
  - book: isbn:9780133356724
    title: Rafael C. Gonzalez and Richard E. Woods, Digital Image Processing, fourth edition, Pearson, 2018
    locator: Section 2.4, Image Sampling and Quantization, from page 47 (Representing Digital Images, page 49; Spatial and Intensity Resolution, page 55)
  - book: isbn:9783030343712
    title: Richard Szeliski, Computer Vision, Algorithms and Applications, second edition, Springer, 2022
    locator: Section 2.3, The digital camera (sampling, aliasing and color)
---

A digital image is a finite grid of $W \times H$ [pixels](/pixel/), each holding $C$ channel values from a finite set, such as one 8-bit gray level or three 8-bit color codes. It comes from a continuous image in two steps: sampling on the grid, which sets the spatial resolution, and quantization of each sample to $2^b$ levels, which sets the intensity resolution. The array alone does not fix the meaning of the numbers; the image also needs a pixel center convention, a channel order, a value range, a statement of whether the values are linear in light or gamma encoded, and, for any operation that reads neighbors, a border rule. A [pixel](/pixel/) is one sample of this grid, and a [frame buffer](/frame-buffer/) is the memory that holds an image for display.

## In plain words

A camera or a scanner looks at a scene through a fine grid. For each cell of the grid it measures the light and writes down a whole number, for example from 0 for black to 255 for white. A color image writes down three numbers per cell, for red, green and blue. The list of all these numbers, row by row, is a digital image. Two choices decide how good it can be: how fine the grid is, and how many different numbers each cell may use. A coarse grid loses small details and can show false patterns. Too few numbers turn smooth shading into visible bands. Programs that work on images must also agree on small details, such as where each cell sits and what to do at the edge, or their results differ.

## The idea

**The model.** A digital image is a function

$$I : \{0, \ldots, W-1\} \times \{0, \ldots, H-1\} \to V^C,$$

where $x$ is the column, $y$ is the row, counted from the top in image files, and $V$ is the set of values of one channel. For a $b$-bit integer channel, $V = \{0, \ldots, 2^b - 1\}$, so $L = 2^b$ levels; for a float channel, $V$ is the floats in a nominal range such as $[0, 1]$. Following the [pixel](/pixel/) page, the sample $I(x, y)$ belongs to the point $(x + \tfrac12, y + \tfrac12)$ of the continuous plane. Pages in this area state when they use the index $(x, y)$ itself as the position, because the two conventions differ by half a pixel in resampling and in methods that interpolate between tiles, such as [CLAHE](/clahe/).

**Sampling.** The values come from a continuous image $f$, after the optics and the sensor have blurred it, sampled at the grid points. By the [sampling theorem](/sampling-theorem/), detail finer than two pixels per period cannot be represented, and if it reaches the sensor it shows up as [aliasing](/aliasing/), for example as moiré on fine fabric. Gonzalez and Woods measure the spatial resolution in samples, or line pairs, per unit distance.

**Quantization.** Each sample is then rounded to one of $L$ levels, a uniform [scalar quantization](/scalar-quantization/). If the rounding error is spread evenly over one step $\Delta$, its mean square is $\Delta^2/12$, so 8-bit codes carry an error of about $1/12$ of a code even before any processing. Too few levels show false contours in smooth gradients. The number of levels is the intensity resolution.

**Channels and their meaning.** One channel gives a gray image; three give a color image in some [color space](/color-spaces/), usually R, G and B in that order, but some libraries store B, G, R; a fourth channel is often the alpha used for [compositing](/alpha-blending/). 8-bit codes for display are almost always gamma encoded, so code 128 is not half the light of code 255 (see [gamma correction](/gamma-correction/)). Raw sensor data and float images for rendering are usually linear.

**Storage.** In the usual row-major, interleaved layout, channel $c$ of pixel $(x, y)$ is at index $(yW + x)C + c$. In a planar layout each channel is a separate $W \times H$ array, at index $cWH + yW + x$. Real buffers often pad each row to a row pitch $P \ge WC$ bytes, so the index becomes $yP + xC + c$.

**Borders.** A neighborhood operation, such as [linear filtering](/linear-filtering/) or a [median filter](/median-filter/), reads pixels outside the grid near the edge. A border rule defines them. For a row $a\,b\,c\,d$, the usual rules extend it to the left as follows:

| rule | values left of $a$ | notes |
|---|---|---|
| constant (zero) | $0\ 0\ \vert\ a\,b\,c\,d$ | darkens the border under blurring |
| replicate (clamp) | $a\ a\ \vert\ a\,b\,c\,d$ | the rule of [bilinear filtering](/bilinear-filtering/) with clamp to edge |
| reflect with the edge repeated | $b\ a\ \vert\ a\,b\,c\,d$ | mirror about the pixel edge |
| reflect without the edge | $c\ b\ \vert\ a\,b\,c\,d$ | mirror about the edge pixel center |
| wrap (periodic) | $c\ d\ \vert\ a\,b\,c\,d$ | what a discrete Fourier transform assumes |
| valid only | none | the output is smaller by the window size minus 1 |

Libraries use different names and different defaults for these rules, so a filter result near the border depends on the library.

## Examples

- **A tiny gray image.** The $4 \times 3$ image with rows $(0, 64, 128, 255)$, $(0, 64, 128, 255)$ and $(255, 255, 0, 0)$, with one 8-bit channel, is 12 bytes. $I(3, 0) = 255$ is white, and $I(2, 2) = 0$ is black.
- **A full HD color image.** $1920 \times 1080$ pixels with 3 channels of 8 bits take $1920 \cdot 1080 \cdot 3 = 6{,}220{,}800$ bytes with no row padding, about 5.9 MiB. The same image with 4 channels takes 8,294,400 bytes.
- **A binary image.** With $b = 1$, each pixel is 0 or 1. This is the output of [image thresholding](/image-thresholding/) and the input of [connected component labeling](/image-labeling/). Stored as one bit per pixel, it is a bitmap in the original sense of the word.
- **A 16-bit image.** Medical and scientific sensors often deliver 12 to 16 bits per sample. To show such an image on an 8-bit display, a program maps the range down, for example by [contrast stretching](/contrast-stretching/).
- **A float image.** High dynamic range images and rendering buffers store floats, often 16 or 32 bits per channel, in linear light, with values above 1.0 for light brighter than the nominal white.
- **Not a vector image.** A drawing stored as lines, curves and fills has no fixed grid. It becomes a digital image only when it is rasterized.

## Where it is used

Every method in this area takes and returns digital images. Point operations change each value alone, using the [image histogram](/image-histogram/), as in [histogram equalization](/histogram-equalization/), [contrast stretching](/contrast-stretching/) and [gamma correction](/gamma-correction/). Neighborhood operations, such as [linear filtering](/linear-filtering/), the [median filter](/median-filter/) and [edge detection](/edge-detection/), need the border rule above. Geometric operations, such as [image resampling](/image-resampling/), need the pixel center convention. Models of [image noise](/image-noise/) and measures such as [PSNR](/psnr/) and [SSIM](/structural-similarity-index/) assume a value range and a peak value. [Lossy image compression](/lossy-image-compression/) reduces the bits needed to store the array. In graphics, a [frame buffer](/frame-buffer/) holds the image that rasterization writes, and [texture mapping](/texture-mapping/) reads images as textures.

## References
