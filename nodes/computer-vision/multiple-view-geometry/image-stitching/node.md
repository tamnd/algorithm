---
tag: 5EXGW7
kind: problem
slug: image-stitching
name: Image stitching
aliases:
- panorama stitching
- image mosaicing
area: computer-vision/multiple-view-geometry
level: core
summary: Combine overlapping photographs into one seamless image by aligning them with homographies or rotations and blending the overlaps.
prereqs: [homography, homography-estimation, image-warping]
see_also: [multi-band-blending, feature-matching, ransac, bundle-adjustment, rotation-averaging, image-compositing, poisson-image-editing, sift]
sources:
  - paper: doi:10.1007/s11263-006-0002-3
    title: "Matthew Brown and David G. Lowe, Automatic panoramic image stitching using invariant features, International Journal of Computer Vision 74(1), 2007, 59-73"
    locator: "Section 2 (the camera model with a rotation and a focal length per image and Equation 1), Section 3 (image matching with RANSAC and probabilistic verification), Section 4 (bundle adjustment), Section 5 (panorama straightening), Section 6 (gain compensation), Section 7 (multi-band blending) and Algorithm 1"
  - paper: doi:10.1561/0600000009
    title: "Richard Szeliski, Image alignment and stitching: a tutorial, Foundations and Trends in Computer Graphics and Vision 2(1), 2006, 1-104"
    locator: the motion models, direct and feature-based alignment, global registration, compositing surfaces, seam selection and blending
  - book: isbn:9783030343712
    title: "Richard Szeliski, Computer Vision, Algorithms and Applications, second edition, Springer, 2022"
    locator: "Chapter 8, Image alignment and stitching"
  - book: isbn:9780521540513
    title: "Richard Hartley and Andrew Zisserman, Multiple View Geometry in Computer Vision, second edition, Cambridge University Press, 2004"
    locator: "Section 8.4, The importance of the camera centre (images from one center are related by homographies, synthetic rotations and mosaicing)"
---

Image stitching is the problem of combining overlapping photographs into one larger image, such as a panorama, so that the result looks like a single photo taken with a wider lens. The photos must be registered to each other, mapped onto a common surface, corrected for differences in exposure, and blended so that no seam shows. Registration is exact only when the camera turns about its optical center or the scene is a plane: then two photos are related by a [homography](/homography/), $H_{ij} = K_i R_i R_j^{\mathsf T} K_j^{-1}$ in the first case. This page is about the whole problem; [homography estimation](/homography-estimation/) is its registration step for one pair, and [multi-band blending](/multi-band-blending/) is one method for its last step.

## In plain words

You stand in one place and take several photos while you turn, each one overlapping the last. To make one wide picture, you must find how each photo sits relative to the others, bend each photo so that straight lines and shared objects line up, and paint them all onto one big canvas. Where two photos overlap, they never match perfectly: one may be a bit brighter, a person may have moved, and small alignment errors remain. So the last step hides the joins by mixing the photos gently across the overlap. If you walk between shots instead of turning in place, near and far objects shift by different amounts, and no amount of bending makes everything line up.

## Definition

**Input.** Images $I_1, \ldots, I_m$, often in no particular order, some of which overlap. The camera may change its focal length and exposure between shots.

**Output.** A composite image on a chosen projection surface, together with the transformation of each input image onto it. The usual surfaces are a plane (for a narrow field of view), a cylinder (for a horizontal panorama) and a sphere (for a full view). Each output pixel is a weighted combination of the input pixels that map to it.

**The geometric model.** In the model of Brown and Lowe each image $i$ has a rotation $R_i$ and a focal length $f_i$, with $K_i = \operatorname{diag}(f_i, f_i, 1)$ in coordinates centered at the image center. A pixel of image $j$ maps to image $i$ by

$$\tilde{\mathbf{u}}_i \sim H_{ij}\tilde{\mathbf{u}}_j, \qquad H_{ij} = K_i R_i R_j^{\mathsf T} K_j^{-1} .$$

This holds for every scene point when all photos share one camera center. If the scene is a plane, the photos are also related by homographies, but of the general form with 8 degrees of freedom. If the center moves and the scene has depth, there is parallax, and no single map aligns two photos.

**Ambiguity.** A common rotation of all cameras, $R_i \mapsto R_i R$, leaves every $H_{ij}$ unchanged. So the data fix the rotations only up to one global rotation, and the stitcher must choose it, for example so that the horizon is level.

**The parts of the problem.**

1. Pairwise registration: find which images overlap and estimate the transformation between each overlapping pair.
2. Global alignment: find all camera parameters at once, so that the errors do not add up around a loop.
3. Projection: choose the surface and the global rotation, and warp each image onto it.
4. Photometric correction: equalize exposure differences and vignetting.
5. Compositing: choose the seams or the blending weights, and blend.

## Variants

- **Pure translation.** Flatbed scans, microscope slides and some aerial strips need only a 2D translation per image.
- **Planar scene with a moving camera.** Documents, walls and satellite images of nearly flat ground use a general homography per image.
- **Rotating camera.** Hand-held panoramas use a rotation and a focal length per image, 4 parameters, instead of 8.
- **With parallax.** A camera that moves in a scene with depth breaks the model. Methods for this case use local warps that vary over the image, or they hide the misalignment with seams placed where the photos agree.
- **Video mosaics.** A sequence of frames from a moving camera, with a large number of images and small motions between them.
- **High dynamic range.** Photos with very different exposures, which need radiometric calibration before blending.

## Examples

- **How far a feature moves.** A camera with $f = 400$ pixels turns about its vertical axis by $\theta$ with $\tan\theta = 0.75$, about $36.9$ degrees. The pixel at the image center moves to $x = f\tan\theta = 300$ pixels in the first image's frame (see the example on the [homography](/homography/) page). On a cylinder of radius $f$, the same turn is a plain shift of $f\theta = 400 \cdot 0.6435 \approx 257.4$ pixels for every pixel, which is why cylindrical coordinates make a pan simple.
- **How many photos for a full circle.** With a horizontal field of view of 60 degrees and an overlap of 20 percent, each new photo adds 48 degrees, so a full circle needs $\lceil 360 / 48 \rceil = 8$ photos.
- **How many RANSAC trials.** Brown and Lowe draw samples of 4 matches and run 500 trials. If half of the matches are correct, one trial is all good with probability $1/16$, and the chance that all 500 trials fail is $(15/16)^{500} \approx 10^{-14}$.

## Known algorithms

- **Feature-based automatic stitching** (Brown and Lowe 2007). Extract [SIFT](/sift/) features, match them with a k-d tree, and for each image consider the $m = 6$ images with the most matches. For each candidate pair, estimate a homography with [RANSAC](/ransac/) on samples of 4 matches with the [DLT](/dlt-homography/), 500 trials, and accept the pair by a probabilistic test on the number of inliers. Then refine the rotations and focal lengths of all images by [bundle adjustment](/bundle-adjustment/) with a robust Huber cost, adding images one at a time. Straighten the panorama with the up vector, compensate the gain of each image in closed form, and blend with [multi-band blending](/multi-band-blending/). This also finds which images form panoramas, and it ignores images that belong to none.
- **Direct alignment.** Estimate each transformation by minimizing intensity differences, as in [direct image alignment](/direct-image-alignment/), from a coarse start. It works on scenes with little texture, where features fail, but it needs a good start.
- **Global alignment by rotation averaging.** Estimate the relative rotations of overlapping pairs, then solve for absolute rotations by [rotation averaging](/rotation-averaging/), and refine with bundle adjustment.
- **Compositing.** Feathering weights each pixel by its distance to the image border, computed with a [distance transform](/distance-transform/), and [alpha blending](/alpha-blending/) mixes the images. [Multi-band blending](/multi-band-blending/) mixes low frequencies over a wide region and high frequencies over a narrow one. Gradient domain methods, such as [Poisson image editing](/poisson-image-editing/), match gradients and solve for the pixels. Seams can be placed by a minimum cut (see the [max-flow min-cut theorem](/max-flow-min-cut-theorem/)) where the images agree, so that moving objects are not cut in half.

## Bounds

- **Model size.** A rotating camera has 3 rotation parameters and 1 focal length per image, $4m$ in all, less 3 for the global rotation. A general homography per image has $8(m - 1)$ free parameters relative to a reference image.
- **Minimal data.** A homography needs 4 matches per pair; a rotation with known focal lengths needs 2.
- **Matching cost.** With $N$ features in total, approximate nearest neighbor search with a k-d tree costs about $O(N \log N)$. Verifying a fixed number of candidates per image costs $O(m)$ RANSAC runs.
- **Bundle adjustment.** The normal equations have $4m$ unknowns. A dense factorization costs $O(m^3)$ per iteration; for panoramas $m$ is small, so this is cheap.
- **What no method can fix.** Under parallax, no global map aligns the photos. A seam can hide it, but the geometry of the result is then not that of any single camera.

## Reductions

- Pairwise registration reduces to [homography estimation](/homography-estimation/) with outliers, solved by [RANSAC](/ransac/) and the [DLT](/dlt-homography/).
- Global alignment is a [bundle adjustment](/bundle-adjustment/) problem with rotations and focal lengths as cameras and no 3D points, since all points are at infinity in the model of a turning camera.
- Seam selection reduces to a minimum cut in a graph of pixels, and blending to linear filtering of pyramids or to a Poisson equation.
- Exposure compensation reduces to a small linear least squares problem in one gain per image.

## Applications

- The panorama modes of phone cameras and of photo software.
- Street-level and 360 degree imagery, and virtual tours.
- Aerial and satellite mosaics of large areas, and maps from drone photos.
- Whole-slide imaging in microscopy and the scanning of large documents and paintings.
- Wide-field images in astronomy.

## References
