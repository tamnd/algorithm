---
tag: 8WSAJV
kind: problem
slug: content-aware-resizing
name: Content-aware image resizing
aliases:
- retargeting
- image retargeting
area: graphics-and-signals/image-processing
level: advanced
summary: Change image dimensions while preserving salient content rather than scaling uniformly.
prereqs: [digital-image, image-resampling]
see_also: [seam-carving, image-warping, dp-on-dag, image-segmentation-graph-cuts, image-inpainting, super-resolution, poisson-image-editing]
sources:
  - paper: doi:10.1145/1276377.1276390
    title: Shai Avidan and Ariel Shamir, Seam carving for content-aware image resizing, ACM Transactions on Graphics 26(3), article 10, 2007 (SIGGRAPH 2007)
    locator: the comparison of seam carving with scaling and cropping, and the use of energy functions to mark important content
  - paper: doi:10.1145/1360612.1360615
    title: Michael Rubinstein, Ariel Shamir and Shai Avidan, Improved seam carving for video retargeting, ACM Transactions on Graphics 27(3), article 16, 2008 (SIGGRAPH 2008)
    locator: the section on forward energy, and the graph cut form for video
  - book: isbn:9783030343712
    title: Richard Szeliski, Computer Vision, Algorithms and Applications, second edition, Springer, 2022
    locator: Chapter 3, Image processing (image warping and resizing)
---

Content-aware image resizing, also called retargeting, is the problem of changing the width or height of an image, often its aspect ratio, so that the important content keeps its shape and size and the change is taken up by the parts that matter less. Uniform [resampling](/image-resampling/) changes every part of the image by the same factor, so a change of aspect ratio squeezes faces and buildings. Cropping keeps the scale but throws away whole regions, which can cut off content near the borders. Content-aware methods mark the important content with a measure such as the local gradient, a saliency map, faces found by a detector, or a mask drawn by the user, and then remove, shrink or deform the rest. The problem has no single objective: "important" and "looks natural" are judged by people, and methods are compared in user studies. [Seam carving](/seam-carving/) is the best-known method.

## In plain words

A wide photo must fit a tall phone screen, or a tall photo a wide banner. Stretching the photo makes people look too thin or too fat. Cutting off the sides can cut off a person standing at the edge. Content-aware resizing keeps the people, faces and buildings as they are, and takes the space from the sky, the grass or a plain wall instead. A computer decides what is important from how much the colors change, from faces it finds, or from marks that the user draws. The result fails when the whole photo is important, or when the computer guesses wrong about what matters.

## Definition

The input is an image $I$ of size $W \times H$, a target size $W' \times H'$, and optionally an importance map $S$ on the pixels. The output is an image $J$ of size $W' \times H'$. The goals, in no fixed balance, are:

- content with high importance appears in $J$ with little change in shape and scale;
- straight lines and object structure stay intact, without visible breaks or new edges;
- the overall layout of the scene, the order and position of objects, is kept;
- for video, the result changes smoothly from frame to frame.

The usual operators are: remove or insert pixels along paths (seams), deform the image by a warp that is nearly uniform scaling on important regions and absorbs the change elsewhere, crop to a window, and scale uniformly. Many methods combine several operators.

## Variants

- Reduction or enlargement of one dimension, or of both.
- Image or video retargeting; video adds consistency in time and a much larger search.
- Automatic importance from gradients and saliency, or importance from a user mask, which can also protect a region or force its removal.
- Object removal: the user marks an object, and the method shrinks the image through it until it is gone, then optionally enlarges the image back to its size.
- Retargeting of stereo pairs and of images with depth, where both views must change in a consistent way.

## Examples

Take an image of 4 equal rows, each $[10, 10, 200, 200, 10, 10, 10, 200, 200, 10, 10]$: two bright objects, 2 pixels wide, on a dark background. Make it 8 pixels wide in three ways:

| method | each row of the result |
|---|---|
| seam carving, 3 seams with central-difference gradient energy | $10, 200, 200, 10, 10, 200, 200, 10$ |
| linear resampling with antialiasing | $10.0, 111.8, 171.2, 16.6, 16.6, 171.2, 111.8, 10.0$ |
| crop to the first 8 columns | $10, 10, 200, 200, 10, 10, 10, 200$ |

Seam carving takes the 3 pixels from the flat background and keeps both objects 2 pixels wide with full contrast. Uniform scaling keeps the layout but blurs both objects and shrinks them by the factor $8/11$. Cropping keeps the first object exactly and cuts the second in half.

A failure of the energy. With central differences, a pixel on a line 1 pixel wide has the same value on its left and on its right, so its gradient energy is 0, as low as the flat background. For rows $[10, 10, 200, 10, 10, 10, 200, 10, 10]$, seam carving to width 6 removes one of the two lines completely and gives $[10, 10, 10, 200, 10, 10]$. The importance measure, not the resizing method, decided what was content.

## Known algorithms

- [Seam carving](/seam-carving/), by Avidan and Shamir: repeatedly remove the connected path of least energy from top to bottom, found by dynamic programming over a [directed acyclic graph](/dp-on-dag/); insert seams to enlarge.
- Seam carving with forward energy, by Rubinstein, Shamir and Avidan, which counts the energy of the new edges that a removal creates; for video, seams through space and time are found as [minimum cuts](/image-segmentation-graph-cuts/) in a graph.
- Warping methods: a mesh over the image is deformed by an [image warp](/image-warping/) chosen by least squares, so that important cells keep their shape and scale and less important cells stretch or shrink.
- Cropping methods: choose the window that contains the most importance, as in automatic thumbnails.
- Multi-operator methods: combine cropping, scaling and seam carving, choosing the mix by an image distance measure.
- Patch-based methods: build the result from patches of the input, so that each patch of the output resembles one of the input, with fast search as in PatchMatch.

## Bounds

- There is no objective function on which all agree, so there is no optimal method; methods are compared by user preference.
- If the important content covers more than the target size, every method must distort or drop some of it; content-aware methods then fall back to scaling or cropping.
- One seam costs $\Theta(WH)$ time by dynamic programming, and $k$ seams cost $\Theta(kWH)$ when the energy is computed again after each removal; the order of seams is greedy, so the sequence as a whole is not optimal.
- Minimum cuts for video seams are polynomial, but much slower than the dynamic program for images.

## Reductions

- One optimal seam is a shortest path in a [directed acyclic graph](/dp-on-dag/) with pixel weights.
- A seam through all frames of a video is a minimum $s$-$t$ cut in a graph whose edges force the cut to be connected and monotone, as in [graph-cut segmentation](/image-segmentation-graph-cuts/).
- Uniform scaling is [image resampling](/image-resampling/); a warp-based method ends with [image warping](/image-warping/).
- Object removal by seams is an alternative to [inpainting](/image-inpainting/) that changes the image size instead of inventing pixels.

## Applications

- Showing images and video on screens of different shapes, such as phones, tablets and wide monitors.
- Thumbnails and previews that keep the subject of the image.
- Web and print layouts where images must fit fixed boxes.
- Removing objects and people from photos.
- Changing the aspect ratio of film and video for television and phones.

## References
