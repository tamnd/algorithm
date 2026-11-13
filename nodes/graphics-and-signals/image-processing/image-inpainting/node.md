---
tag: AZ83B1
kind: problem
slug: image-inpainting
name: Image inpainting
aliases:
- image completion
- hole filling
area: graphics-and-signals/image-processing
level: advanced
summary: Fill in missing or masked regions of an image plausibly.
prereqs: [digital-image, poisson-equation]
see_also: [criminisi-inpainting, poisson-image-editing, heat-equation, fast-marching-method, total-variation-denoising, image-denoising, seam-carving, super-resolution]
sources:
  - paper: doi:10.1145/344779.344972
    title: Marcelo Bertalmio, Guillermo Sapiro, Vicent Caselles and Coloma Ballester, Image inpainting, Proceedings of SIGGRAPH 2000, pages 417-424
    locator: the term inpainting in image processing, and filling by transport of image smoothness along isophotes
  - paper: doi:10.1109/TIP.2004.833105
    title: Antonio Criminisi, Patrick Pérez and Kentaro Toyama, Region filling and object removal by exemplar-based image inpainting, IEEE Transactions on Image Processing 13(9):1200-1212, 2004
    locator: Section I (structure inpainting against texture synthesis) and Section III (the exemplar-based algorithm)
  - paper: doi:10.1109/ICCV.1999.790383
    title: Alexei A. Efros and Thomas K. Leung, Texture synthesis by non-parametric sampling, IEEE International Conference on Computer Vision, 1999, pages 1033-1038
    locator: synthesis of a pixel from similar neighborhoods in the known image, including hole filling
  - paper: doi:10.1145/1531326.1531330
    title: Connelly Barnes, Eli Shechtman, Adam Finkelstein and Dan B Goldman, PatchMatch, a randomized correspondence algorithm for structural image editing, ACM Transactions on Graphics 28(3), article 24, 2009
    locator: fast patch search and its use for image completion
---

Image inpainting is the problem of filling a region $\Omega$ of an image whose values are missing, damaged or unwanted, using the rest of the image, so that the result looks natural. Uses range from thin scratches and overlaid text, where the hole is a few pixels wide, to the removal of whole objects, where the hole is large and its content must be invented. The known pixels give no information about the values inside $\Omega$ by themselves, so the problem has no unique answer and no objective measure of success: every method uses a model of images. Diffusion methods continue the image smoothly from the border of the hole, which works for thin holes and smooth regions but blurs texture. Exemplar methods copy patches of real texture from other parts of the image, as [Criminisi exemplar-based inpainting](/criminisi-inpainting/) does, and learned methods fill holes with networks trained on many photos.

## In plain words

Part of a photo is missing: a scratch, a date stamp, or a person you want to remove. Inpainting paints the missing part so that nobody notices. For a thin scratch, it is enough to let the colors around the scratch flow in, like ink spreading on paper. For a big hole, flowing colors look like a smooth smear, because real photos have texture such as grass, bricks or waves. Then it works better to copy small pieces of texture from other parts of the same photo, and to make lines that enter the hole continue across it. There is never one right answer, because nobody knows what was really behind the person.

## Definition

The input is an image $f$ on a pixel grid and a mask that marks the target region $\Omega$; the values of $f$ on $\Omega$ are unknown or must be ignored. The output is an image $u$ with $u = f$ outside $\Omega$, and with values on $\Omega$ that are consistent with the rest of the image. "Consistent" is made precise only by a model, for example:

- smooth continuation: $u$ on $\Omega$ minimizes $\sum (u_p - u_q)^2$ over neighbor pairs, which gives the discrete Laplace equation $\Delta u = 0$ on $\Omega$ with $u = f$ on its border, the harmonic fill;
- bounded variation: $u$ on $\Omega$ minimizes the total variation, which allows sharp edges in the fill;
- texture: each patch of $u$ that overlaps $\Omega$ should be close to some patch of the known image;
- a probability model of images, either fitted to the image itself or learned from a data set, with $u$ a likely sample or its mode.

Inpainting has the same form as other inverse problems, $f = Mu + n$, with $M$ the operator that keeps the known pixels and drops the others; the null space of $M$ is every image that is zero outside $\Omega$.

## Variants

- Thin holes, such as scratches, cracks in old photos, and text or logos laid over an image.
- Object removal, with large holes and the need to fill both structure and texture.
- Image extension or outpainting, where the hole is outside the frame.
- Video inpainting, with time as a third dimension and with consistency between frames.
- Inpainting of depth maps, normal maps and other data on a grid.
- Guided inpainting, where the user draws lines that the fill must continue, or marks the source region.
- Error concealment, the filling of blocks lost in transmission of compressed images and video.

## Examples

A thin hole in one row: if the pixels between a known value 0 and a known value 50 are missing, the harmonic fill is the straight line between them, $0, 10, 20, 30, 40, 50$ for a gap of 4 pixels.

A measured case with structure. Take a $16 \times 12$ image with value 180 where $x + y < 14$ and value 60 elsewhere, a diagonal edge, and a hole of $6 \times 5$ pixels at $5 \le x \le 10$, $4 \le y \le 8$. Two fills of the 30 hole pixels:

| method | mean squared error on the hole | values in the hole |
|---|---|---|
| harmonic fill, by the Poisson solver of [Poisson image editing](/poisson-image-editing/) with zero guidance | 1334.36 | 30 different values from 66.57 to 173.43 |
| [Criminisi inpainting](/criminisi-inpainting/), patch radius 2 | 2880 | only 60 and 180; 6 pixels wrong |

The harmonic fill has the smaller error, but it replaces the sharp edge with a smooth ramp; the exemplar fill keeps the edge sharp and the two flat levels, but puts the edge in the wrong place in the lower rows. Neither is the true image, and the measure ranks them against the visual impression. That is the usual state of the problem: the error against the true image measures only one aspect of quality, and a real hole has no true image to compare with.

## Known algorithms

- Harmonic fill: solve the [Poisson equation](/poisson-equation/) $\Delta u = 0$ on $\Omega$ with Dirichlet values from the border, by Gauss-Seidel, conjugate gradients or multigrid. The [Poisson image editing](/poisson-image-editing/) solver with zero guidance does this. Running the [heat equation](/heat-equation/) to steady state gives the same fill.
- Transport and diffusion: Bertalmio, Sapiro, Caselles and Ballester move image smoothness into the hole along isophotes, the level lines of the image, with a partial differential equation. Telea's method fills the hole in the order of a [fast marching](/fast-marching-method/) front, with a weighted average of known pixels.
- Variational methods: total variation inpainting, and higher-order models that also continue curved edges.
- Texture synthesis: Efros and Leung grow the fill one pixel at a time by copying the center of a known neighborhood that matches the known part of the neighborhood of the pixel.
- Exemplar-based patch filling: [Criminisi exemplar-based inpainting](/criminisi-inpainting/) copies whole patches in an order given by a confidence term and an edge term. Global patch methods improve all patches of the fill together, with fast matching by PatchMatch.
- Learned methods: convolutional and other networks trained to fill random masks on large photo collections, which can invent content that appears nowhere in the image.

## Bounds

- The known pixels do not determine the hole: any values on $\Omega$ are consistent with the data, so there is no quality guarantee without a model, and no guarantee at all for content that the model cannot predict.
- The harmonic fill obeys the maximum principle: every filled value lies between the least and the largest value on the border of the hole, so it never invents new extremes and cannot continue a thin bright line through the middle of a wide hole.
- For the harmonic fill, a Gauss-Seidel sweep costs $\Theta(m)$ for $m$ hole pixels, but the number of sweeps grows with the square of the width of the hole; multigrid needs $O(m)$ work in total.
- Exemplar methods are limited by the search for the best patch, which is $O(WH)$ per query when done by brute force.

## Reductions

- The harmonic fill is the special case of [Poisson image editing](/poisson-image-editing/) with zero guidance field, and a [Dirichlet problem](/poisson-equation/) for the Laplace equation.
- With the masking operator $M$, inpainting is the deblurring problem $f = Ku + n$ with $K = M$; regularized methods for [deblurring](/image-deblurring/) and [denoising](/image-denoising/) carry over.
- Object removal in [seam carving](/seam-carving/) removes seams through an object instead of filling it, which changes the image size.
- Patch-based filling reduces to many nearest-neighbor searches over patches, the same search as [template matching](/template-matching/) and [non-local means](/non-local-means/).

## Applications

- Restoring old photos, films and paintings in digital form.
- Removing objects, people, wires and text from photos, as in the content-aware fill tools of photo editors.
- Hiding lost blocks in transmitted images and video.
- Filling holes in depth maps and in views warped to a new viewpoint.
- Removing logos, subtitles and time stamps from video.

## References
