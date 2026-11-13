---
tag: 6RG5Y2
kind: concept
slug: image-pyramid
name: Image pyramid
aliases:
- multiresolution pyramid
area: graphics-and-signals/image-processing
level: advanced
summary: A sequence of copies of an image, each one low-pass filtered and subsampled from the one before, so that each level shows the image at half the resolution.
prereqs: [digital-image, linear-filtering, aliasing]
see_also: [gaussian-pyramid, laplacian-pyramid, mipmap, discrete-wavelet-transform, gaussian-filter, image-resampling, optical-flow, image-registration]
sources:
  - paper: doi:10.1109/TCOM.1983.1095851
    title: Peter J. Burt and Edward H. Adelson, The Laplacian pyramid as a compact image code, IEEE Transactions on Communications 31(4), 1983, 532 to 540
    locator: pages 532 to 534 (the pyramid as a sequence of low-pass copies, the REDUCE step and the generating kernel)
  - paper: doi:10.1145/245.247
    title: Peter J. Burt and Edward H. Adelson, A multiresolution spline with application to image mosaics, ACM Transactions on Graphics 2(4), 1983, 217 to 236
    locator: the whole paper (the band-pass decomposition and the blend of two images band by band)
  - book: isbn:9783030343712
    title: Richard Szeliski, Computer Vision, Algorithms and Applications, second edition, Springer, 2022
    locator: Chapter 3, Section 3.5, Pyramids and wavelets
  - paper: "Edward H. Adelson, Charles H. Anderson, James R. Bergen, Peter J. Burt and Joan M. Ogden, Pyramid methods in image processing, RCA Engineer 29(6), 1984, 33 to 41"
    locator: the survey of Gaussian and Laplacian pyramids and their uses (coarse-to-fine search, blending, coding)
---

An image pyramid is a sequence of copies of a [digital image](/digital-image/): level 0 is the image itself, and each next level is made from the one before by a [low-pass filter](/linear-filtering/) and a subsampling, most often by 2 along each axis. The filter removes the detail that the coarser grid cannot hold, so the small copies do not show [aliasing](/aliasing/). Programs use the stack to search for a pattern or a motion first at a coarse level, where the search is short, and then refine the answer level by level. The two main kinds are the low-pass [Gaussian pyramid](/gaussian-pyramid/) and the band-pass [Laplacian pyramid](/laplacian-pyramid/).

## In plain words

Take a photo and make a copy that is half as wide and half as high. Then make a copy of the copy, and go on until one pixel is left. Stack the copies with the largest at the bottom, and the stack looks like a pyramid. Each copy shows the same scene with less detail. Before you shrink, you blur a little, because if you only drop every second pixel, thin stripes can turn into false patterns. The stack is useful because a large object or a large motion in the full photo is small in a small copy. A program can find it cheaply in the small copy, then use that answer as a starting guess in the next larger copy, and so on up to full size. The whole stack takes only about one third more memory than the photo.

## The idea

Let $G_0 = I$ be an image of $W \times H$ samples. A pyramid with a reduction factor of 2 is the sequence

$$
G_{l+1} = \downarrow_2 \big( h * G_l \big), \qquad l = 0, 1, \ldots, N - 1,
$$

where $h$ is a low-pass [convolution](/discrete-convolution/) kernel and $\downarrow_2$ keeps the samples at even row and column indices. Sample $(x, y)$ of level $l$ sits on sample $(2^l x, 2^l y)$ of level 0, so one step of the coarse grid covers $2^l$ steps of the fine grid. Level $l$ has about $W/2^l \times H/2^l$ samples. The stack ends at a $1 \times 1$ level, or earlier when the coarsest useful scale is reached.

Four ideas make the stack work.

- **Filter, then subsample.** Dropping every second sample folds frequencies above the new Nyquist limit onto lower ones (see the [sampling theorem](/sampling-theorem/)). The kernel $h$ attenuates them first. Burt and Adelson use a separable 5-tap kernel, with a [Gaussian filter](/gaussian-filter/) as the usual choice, and this gives the Gaussian pyramid.
- **Small total size.** Level $l$ has about $4^{-l}$ of the samples of level 0, so the whole stack has about $1 + 1/4 + 1/16 + \cdots = 4/3$ times as many samples as the image. The exact count depends on how odd sizes round. It is on the [Gaussian pyramid](/gaussian-pyramid/) page.
- **Coarse to fine.** A displacement of $d$ pixels at level 0 is $d/2^l$ pixels at level $l$. A method that works only for small displacements, such as a local [optical flow](/optical-flow/) solver, can run at the top level, double its answer, and correct it at each finer level.
- **Low-pass or band-pass.** A Gaussian pyramid keeps the coarse content of the image at each level. A Laplacian pyramid keeps the difference between a level and the upsampled next level, which is one band of spatial frequencies. The band-pass form allows the image to be rebuilt exactly, and it allows operations per frequency band, such as the blend of two images in the multiresolution spline.

A pyramid is overcomplete: it stores more numbers than the image. A [discrete wavelet transform](/discrete-wavelet-transform/) is the critically sampled relative: it splits each level into a coarse part and detail parts with the same total count as the image, through a [filter bank](/filter-bank/) with [perfect reconstruction](/perfect-reconstruction/).

The [mipmap](/mipmap/) of rasterization is the same halving chain built for another job. It prefilters a texture, often with a $2 \times 2$ box, so that a renderer can read a texel of the right size at draw time. An image pyramid in image analysis is built from a camera image and uses a wider smoothing kernel, and its levels feed search, matching and blending.

## Examples

**Why the blur matters.** Take the row $0, 16, 0, 16, 0, 16, 0, 16$, a pattern of period 2. Keeping the even samples without a blur gives $0, 0, 0, 0$: the stripes have turned into a flat dark row with the wrong mean. With the binomial kernel $\frac{1}{16}(1, 4, 6, 4, 1)$ and a mirror border, each even sample becomes $(4 \cdot 16 + 4 \cdot 16)/16 = 8$, so the reduced row is $8, 8, 8, 8$. The pattern is too fine for the coarse grid, and the filtered level shows its mean gray, which is the right answer at that scale.

**Level sizes.** A $640 \times 480$ image with sizes rounded up at each halving has 11 levels: $640 \times 480$, $320 \times 240$, $160 \times 120$, $80 \times 60$, $40 \times 30$, $20 \times 15$, $10 \times 8$, $5 \times 4$, $3 \times 2$, $2 \times 1$ and $1 \times 1$. Together they hold 409609 samples, against 307200 in the image.

**Coarse-to-fine search.** A camera moves 40 pixels between two frames. A local motion estimator that can only find shifts of about one or two pixels fails at level 0. At level 3 the shift is $40/8 = 5$ pixels, and at level 5 it is $40/32 = 1.25$ pixels, within reach. The program estimates the shift at level 5, doubles it as the start at level 4, corrects it there, and goes on down to level 0.

**A non-example.** Shrinking an image once for a thumbnail is [image resampling](/image-resampling/), not a pyramid. A pyramid keeps all the levels and the fixed relation between their grids.

## Where it is used

- **Motion and registration.** The iterative [Lucas-Kanade method](/lucas-kanade-method/) and many [optical flow](/optical-flow/) and [image registration](/image-registration/) methods run coarse to fine, so that large motions become small at the top level.
- **Matching.** [Template matching](/template-matching/) can test every position at a coarse level and only the neighbors of the best ones at the finer levels.
- **Features at many scales.** Detectors such as [SIFT](/sift/) and multiscale forms of the [Harris corner detector](/harris-corner-detector/) search for features in a stack of blurred and subsampled images.
- **Blending.** Burt and Adelson blend two images by mixing their Laplacian levels with a mask that is smooth at coarse levels and sharp at fine levels, a form of [image compositing](/image-compositing/) without a visible seam.
- **Coding.** The Laplacian levels are mostly near zero, so they quantize and compress well. This is the use in the title of the 1983 paper of Burt and Adelson on the Laplacian pyramid.
- **Texture lookup.** The [mipmap](/mipmap/) uses the same chain to filter textures at render time.

## References
