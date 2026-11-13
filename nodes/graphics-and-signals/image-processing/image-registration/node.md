---
tag: QTGT5Y
kind: problem
slug: image-registration
name: Image registration
aliases:
- image alignment
area: graphics-and-signals/image-processing
level: advanced
summary: Find the geometric transform from a given class, such as shifts or affine maps, that best aligns a moving image with a reference image under a chosen measure of similarity.
model: real-ram
prereqs: [digital-image, template-matching]
see_also: [phase-correlation, normalized-cross-correlation, lucas-kanade-method, optical-flow, image-warping, sift, kabsch-algorithm, least-squares-problem]
sources:
  - paper: doi:10.1145/146370.146374
    title: Lisa Gottesfeld Brown, A survey of image registration techniques, ACM Computing Surveys 24(4), 325-376, 1992
    locator: the whole survey (the four parts of a registration method, the feature space, the search space, the search strategy and the similarity metric)
  - paper: doi:10.1016/S0262-8856(03)00137-9
    title: Barbara Zitová and Jan Flusser, Image registration methods, a survey, Image and Vision Computing 21(11), 977-1000, 2003
    locator: the whole survey (the steps of feature detection, feature matching, transform model estimation and resampling)
  - paper: "Bruce D. Lucas and Takeo Kanade, An iterative image registration technique with an application to stereo vision, Proceedings of the 7th International Joint Conference on Artificial Intelligence, Vancouver, 674-679, 1981"
    title: Bruce D. Lucas and Takeo Kanade, An iterative image registration technique with an application to stereo vision, IJCAI 1981
    locator: the whole paper (registration by a Newton-type step on the gradient of the image)
  - paper: doi:10.1109/83.506761
    title: B. Srinivasa Reddy and B. N. Chatterji, An FFT-based technique for translation, rotation, and scale-invariant image registration, IEEE Transactions on Image Processing 5(8), 1266-1271, 1996
    locator: the whole paper (rotation and scale as shifts in log-polar coordinates of the Fourier magnitude)
  - book: isbn:9783030343712
    title: Richard Szeliski, Computer Vision, Algorithms and Applications, second edition, Springer, 2022
    locator: Chapter 8, Image alignment and stitching, and Chapter 9, Motion estimation
---

Image registration is the problem of finding the geometric transform that maps one image onto another image of the same scene, so that the same point of the scene has the same coordinates in both. One image is the fixed *reference*, the other the *moving* image. The answer is a member of a chosen class of transforms, such as shifts, turns with shifts, affine maps or smooth deformation fields, together with a measure of how well the two images agree after the transform. Methods fall into two families. Area-based methods compare pixel values directly, for example by [phase correlation](/phase-correlation/) or [normalized cross-correlation](/normalized-cross-correlation/). Feature-based methods first find and match distinct points, for example with [SIFT](/sift/), and then fit the transform to the matched pairs. Registration is needed before two images can be compared, combined into one or used to measure a change.

## In plain words

You have two photos of the same scene. Maybe the camera moved a little, turned, or zoomed. You want to lay one photo on top of the other so that everything lines up: the corner of each building on the same corner, each tree on the same tree. Image registration finds how to move, turn, stretch or bend the second photo to make this happen. You can do it in two ways. You can slide the second photo around and look at how well all the pixels agree. Or you can pick out some clear marks, such as corners, find the same marks in both photos, and work out the move that brings the marks together.

## Definition

The input is a reference image $R$ and a moving image $M$, each a gray [digital image](/digital-image/) with $W$ columns and $H$ rows and one channel of integer values, for example 0 to 255, used as they are stored with no gamma step. Pixel $(x, y)$ has its center at the integer point $(x, y)$, with $x$ to the right and $y$ down. To evaluate $M$ at points between pixel centers, the image is extended to a function on the plane by an interpolation rule, for example [bilinear interpolation](/bilinear-interpolation/), and is undefined outside its rectangle. This is the border rule: points that map outside $M$ are left out of the measure.

A *transform class* $\mathcal{T}$ is a set of maps $T$ from the coordinates of $R$ to those of $M$ with a few real parameters. A *dissimilarity* $D$ compares $R$ and $M \circ T$ over the overlap $\Omega_T = \{x \in \text{grid of } R : T(x) \in \text{domain of } M\}$, for example the mean squared difference

$$D(T) = \frac{1}{|\Omega_T|} \sum_{x \in \Omega_T} \big(R(x) - M(T(x))\big)^2.$$

The *area-based* problem asks for $T^* = \arg\min_{T \in \mathcal{T}} D(T)$, often with a lower bound on $|\Omega_T|$. The *feature-based* problem has as input point lists $p_1, \ldots, p_m$ in $R$ and $q_1, \ldots, q_n$ in $M$ and asks for a $T$ and a set of pairs $(p_i, q_{j(i)})$ that agree, with $\lVert T(p_i) - q_{j(i)} \rVert$ small for as many pairs as possible. The usual classes, with their number of parameters, are:

| Class | Map | Parameters | Pairs in general position needed |
|---|---|---|---|
| Translation | $x + t$ | 2 | 1 |
| Rigid (Euclidean) | $Qx + t$, $Q$ a rotation | 3 | 2 |
| Similarity | $sQx + t$, $s > 0$ | 4 | 2 |
| Affine | $Ax + t$, $A$ invertible | 6 | 3, not on one line |
| Projective | $(Ax + t)/(c^{\mathsf T} x + 1)$ | 8 | 4, no three on one line |
| Deformable | $x + u(x)$ with a smooth field $u$ | many | not fixed |

This page is about the problem in general. [Template matching](/template-matching/) is the special case of a small template and shifts only, and [optical flow](/optical-flow/) is the case of a separate small motion at every pixel.

## Variants

- **Monomodal and multimodal.** Two photos of the same kind can be compared by their values. Images from different sensors, such as CT and MRI scans or visible and infrared images, have unrelated values for the same tissue or material. Then measures based on the joint histogram, such as mutual information, take the place of differences.
- **Global and local.** A global transform has a few parameters for the whole image. A local or deformable transform lets each part move on its own, as in medical images of soft tissue, with a smoothness term that keeps the field regular.
- **Pairwise and groupwise.** Groupwise registration aligns many images at once, for example all frames of a video or all scans of a study, to a common frame.
- **Subpixel accuracy.** Many uses need the transform to a fraction of a pixel. Area-based methods reach it by interpolation of the measure or by gradient steps.
- **Point sets.** When the input is two sets of points with no images, the problem is point set registration. Iterative closest point methods alternate between pairing each point with its nearest one and fitting the transform.
- **2D to 3D.** A 2D image is registered with a 3D model or volume, and the transform includes a camera projection.

## Examples

**An affine map from three pairs.** Let the points $(0, 0)$, $(1, 0)$ and $(0, 1)$ of $R$ match the points $(5, 2)$, $(5, 3)$ and $(4, 2)$ of $M$. An affine map $T(x) = Ax + t$ has $t = T(0, 0) = (5, 2)$. The first column of $A$ is $T(1, 0) - t = (0, 1)$, and the second column is $T(0, 1) - t = (-1, 0)$. So

$$T(x, y) = \begin{pmatrix} 0 & -1 \\ 1 & 0 \end{pmatrix} \begin{pmatrix} x \\ y \end{pmatrix} + \begin{pmatrix} 5 \\ 2 \end{pmatrix} = (5 - y,\; x + 2),$$

a turn by $90°$ followed by a shift. The matrix is a rotation, so the answer is also rigid. A fourth pair can check the answer: $T(2, 3) = (2, 4)$. If the three points of $R$ were on one line, the six equations would not fix $A$.

**The overlap must be normalized.** Take one image row $f = (3, 1, 4, 1, 5, 9, 2, 6, 5, 3)$ and a second row $g = (5, 1, 6, 8, 2, 7, 5, 4, 7, 7)$. The first eight values of $g$ are $f(x + 2)$ with an error of at most 1, and the last two are new content. Compare $f(x + d)$ with $g(x)$ over the overlap for each shift $d$ from $-8$ to $8$.

| $d$ | pixels in the overlap | sum of squared differences | mean |
|---|---|---|---|
| 2 | 8 | 5 | 0.625 |
| 5 | 5 | 27 | 5.4 |
| 8 | 2 | 4 | 2.0 |

The sum is smallest at $d = 8$, where only two pixels overlap and happen to agree. The mean is smallest at the true shift $d = 2$. Every other shift has a mean of at least $2$.

**A shift that cannot be found.** Let $R(x, y) = x$, a ramp that changes only along $x$. A shift $(0, t)$ along $y$ leaves the image the same, so every measure gives the same value for every $t$. Only the part of the shift along the gradient can be found. This is the *aperture problem*, and it is the reason why feature-based methods use corners and not points on straight edges.

## Known algorithms

| Method | Class | Cost | Notes |
|---|---|---|---|
| [Phase correlation](/phase-correlation/) | translation | $O(WH \log(WH))$ | exact for a circular integer shift; not changed by a gain and an offset of the brightness |
| Exhaustive search with [template matching](/template-matching/) scores | translation | one score map | global, so it cannot be caught in a local minimum |
| Log-polar Fourier method (Reddy and Chatterji, 1996) | similarity | a few FFTs | turns and scale become shifts of the Fourier magnitude |
| [Lucas-Kanade method](/lucas-kanade-method/) | any smooth class | $O(WH)$ per iteration for a fixed number of parameters | local: it needs a start near the answer, often on a [Gaussian pyramid](/gaussian-pyramid/) |
| Features, matching, robust fit | up to projective | detection plus matching plus fit | [SIFT](/sift/) or [Harris corners](/harris-corner-detector/), [nearest neighbour search](/kd-tree-nearest-neighbor-search/), then a fit that rejects wrong pairs, such as RANSAC |
| [Kabsch algorithm](/kabsch-algorithm/) | rigid, from known pairs | $O(m)$ for $m$ pairs in the plane | the least squares rotation and shift, from an SVD |
| [Linear least squares](/least-squares-problem/) | affine, from known pairs | $O(m)$ for $m$ pairs | six unknowns, two equations per pair |
| Deformable methods | deformable | depends on the model | a measure plus a smoothness term, solved by gradient steps on a grid of parameters |

After the transform is found, $M$ is resampled onto the grid of $R$ by [image warping](/image-warping/) with an interpolation rule. Learned methods based on convolutional neural networks can also predict a transform or a deformation field directly from the two images.

## Bounds

- **Minimal data.** A class with $k$ parameters needs at least $k$ independent equations. Each point pair gives two, so an affine map needs three pairs, and the three points must not lie on one line: if they do, $A$ times the direction across the line is not fixed. A projective map needs four pairs with no three on one line.
- **Not every transform can be seen.** If the image does not change along a direction, as in the ramp example, a shift along that direction is not determined by any measure. To first order, the shift of a window is determined exactly when the matrix of summed gradient products of [corner detection](/corner-detection/) has full rank. A flat image determines no transform.
- **Local minima.** The measure $D(T)$ is in general not convex in the parameters. A periodic texture gives one minimum per period. A local method finds the true answer only from a start in its capture range, which is about the size of the structures in the image at the current level of the pyramid. Global search on a grid of $K$ values per parameter costs $K^k$ evaluations for $k$ parameters, each of cost $O(WH)$.
- **Translation by whole pixels.** The best shift under the sum of squared differences over all $W H$ circular shifts costs $O(WH \log(WH))$ with the FFT, against $O(W^2 H^2)$ by direct evaluation.

## Reductions

- **Translation to correlation.** For shifts, the sum of squared differences reduces to a cross-correlation and box sums, as on the [template matching](/template-matching/) page, and phase correlation reads the shift from the peak of a normalized correlation.
- **Similarity to translation.** The magnitude of the Fourier transform does not change under a shift, and a turn of the image by an angle turns the magnitude by the same angle, while a scale by $s$ scales it by $1/s$ along the frequency axes. In log-polar coordinates of the magnitude they become shifts, so phase correlation finds them; a second phase correlation then finds the shift.
- **Feature-based to point fitting.** After the pairs are known, a rigid fit is the problem of the [Kabsch algorithm](/kabsch-algorithm/) and an affine fit is a [least squares problem](/least-squares-problem/). Finding the pairs is a [nearest neighbour search](/nearest-neighbor-search/) among descriptors.
- **Dense local registration is optical flow.** Registration with a separate shift for every pixel is the [optical flow](/optical-flow/) problem between the two images.
- **Gradient-based registration to least squares.** One step of the [Lucas-Kanade method](/lucas-kanade-method/) replaces $M(T(x))$ by its first-order Taylor form in the parameters, and the step is the solution of a linear least squares problem.

## Applications

- Building panoramas and mosaics from overlapping photos, and aligning satellite and aerial images with maps.
- Medical imaging: aligning scans of one patient taken at different times or with different devices, and aligning a patient scan with an atlas.
- Change detection, where two aligned images are subtracted to show what changed.
- Video stabilization, and the alignment of frames before denoising or [super-resolution](/super-resolution/).
- Microscopy and astronomy, where many exposures of one object are aligned and added.

## References
