---
tag: ARVS59
kind: problem
slug: feature-detection
name: Feature detection
aliases:
- interest point detection
- keypoint detection
area: graphics-and-signals/image-processing
level: advanced
summary: Find a set of distinct points or regions of an image, each with a position and often a scale and an orientation, that can be found again in another image of the same scene.
model: real-ram
complexity:
  vars: {W: image width in pixels, H: image height in pixels}
  time: {worst: Ω(W H)}
prereqs: [digital-image]
see_also: [corner-detection, edge-detection, sift, harris-corner-detector, laplacian-of-gaussian, image-registration, non-maximum-suppression, hough-transform]
sources:
  - paper: doi:10.1023/A:1008199403446
    title: Cordelia Schmid, Roger Mohr and Christian Bauckhage, Evaluation of interest point detectors, International Journal of Computer Vision 37(2), 151-172, 2000
    locator: the whole paper (the repeatability rate and the information content as criteria for detectors)
  - paper: doi:10.1561/0600000017
    title: Tinne Tuytelaars and Krystian Mikolajczyk, Local invariant feature detectors, a survey, Foundations and Trends in Computer Graphics and Vision 3(3), 177-280, 2008
    locator: the whole survey (the properties of a good feature and the families of detectors)
  - paper: doi:10.1023/A:1008045108935
    title: Tony Lindeberg, Feature detection with automatic scale selection, International Journal of Computer Vision 30(2), 79-116, 1998
    locator: the whole paper (scale-normalized derivatives and the selection of scale at extrema over scale)
  - paper: doi:10.1007/s11263-005-3848-x
    title: Krystian Mikolajczyk, Tinne Tuytelaars, Cordelia Schmid, Andrew Zisserman, Jiri Matas, Frederik Schaffalitzky, Timor Kadir and Luc Van Gool, A comparison of affine region detectors, International Journal of Computer Vision 65(1-2), 43-72, 2005
    locator: the whole paper (affine covariant regions and their evaluation by overlap)
  - book: isbn:9783030343712
    title: Richard Szeliski, Computer Vision, Algorithms and Applications, second edition, Springer, 2022
    locator: Chapter 7, Feature detection and matching, Section 7.1 Points and patches
---

Feature detection is the problem of finding a set of local features in an image: points or small regions that stand out from their surroundings and that a program can find again in another image of the same scene. Each feature has a position, and many detectors also give it a scale, an orientation or an elliptic shape. The main requirement is *repeatability*: when the scene is seen from another place, at another zoom or in other light, the detector should return the same scene points. The problem has no single formal answer. Each detector fixes a response function and a rule, often the local extrema of a filtered image, and is then judged by measurements such as the repeatability rate of Schmid, Mohr and Bauckhage. Features are the first step of feature-based [image registration](/image-registration/), object recognition and 3D reconstruction. A second step, description and matching, compares the patches around the features.

## In plain words

Two photos of a street are taken from slightly different places. You want to find marks that you can point to in both: the corner of a window, the dot at the center of a sign, the tip of a roof. A good mark is easy to find again. A spot in the middle of a white wall is a poor mark, because every spot of the wall looks the same. A point on a long straight edge is also poor, because you can slide along the edge and not see a change. A corner or a small blob is good, because it looks different from every place near it. Feature detection asks a computer to pick such marks by itself. The marks must stay the same marks when the second photo is turned, zoomed, darker or a little blurred.

## Definition

The input is a gray [digital image](/digital-image/) $I$ with $W$ columns and $H$ rows and one channel of values, for example 0 to 255, used as they are stored with no gamma step. Pixel $(x, y)$ has its center at the integer point $(x, y)$, with $x$ to the right and $y$ down. Filters near the border use a stated border rule, most often the clamp rule, and many detectors drop features whose support leaves the image. A *feature* is a tuple $(x, y)$, or $(x, y, \sigma)$ with a scale, or $(x, y, \sigma, \theta)$ with an orientation, or a position with a $2 \times 2$ shape matrix. A *detector* is a map $D$ from images to finite sets of features.

Let $T$ be a transform of the plane from a class $G$, for example shifts, turns or changes of scale, and let $I' = I \circ T^{-1}$, so that a scene point at $x$ in $I$ is at $T(x)$ in $I'$. The detector is *covariant* with $G$ when

$$D(I \circ T^{-1}) = T(D(I)) \quad \text{for every } T \in G,$$

where $T$ acts on the scale and the shape of a feature as well as on its position. On real images this holds only up to noise and resampling, so it is measured. With a tolerance $\varepsilon$ in pixels and only the features whose points lie in the part of the scene seen in both images, the *repeatability rate* is

$$r = \frac{\big|\{f \in D(I) : \text{some } f' \in D(I') \text{ has } \lVert T(f) - f' \rVert \le \varepsilon\}\big|}{\min(|D(I)|, |D(I')|)}.$$

Other criteria are the accuracy of the position, the distinctiveness of the patch around each feature, the number of features and the cost. A detector is usually also asked to be insensitive to a change $aI + b$ of the brightness with $a > 0$.

## Variants

- **Corners.** Points where the gradient changes in two directions; see [corner detection](/corner-detection/).
- **Blobs.** Small regions brighter or darker than their surroundings, found as extrema of a second-derivative filter such as the [Laplacian of Gaussian](/laplacian-of-gaussian/), together with a scale.
- **Edges and lines.** Curves of sharp change, found by [edge detection](/edge-detection/), and straight lines and circles, found by the [Hough transform](/hough-transform/). Edges are features of a curve, not of a point.
- **Scale covariant features.** The detector searches over position and scale and returns the scale at which a normalized response is largest, as in [SIFT](/sift/).
- **Affine covariant regions.** The detector adapts an ellipse to the local structure, so that the region follows a change of viewpoint of a flat surface. Maximally stable extremal regions are another kind of region detector of this class.
- **Dense features.** Every pixel of a grid is used as a feature, with no detection. This is common when the patches are classified, not matched.
- **Learned detectors.** Detectors trained on data learn the response function itself; detectors based on convolutional neural networks are one such kind.

## Examples

**The scale of a blob.** Let $f(x) = e^{-\lvert x \rvert^2/(2s^2)}$ be a Gaussian blob of size $s$ in the plane, and let $L = G_\sigma \ast f$ be its blur by a Gaussian of standard deviation $\sigma$. Then $L(x) = \frac{s^2}{s^2 + \sigma^2} e^{-\lvert x \rvert^2 / (2(s^2 + \sigma^2))}$, and at the center the scale-normalized Laplacian is

$$\sigma^2 \lvert \nabla^2 L(0) \rvert = \frac{2 \sigma^2 s^2}{(s^2 + \sigma^2)^2}.$$

As a function of $u = \sigma^2$ this is $2s^2 u/(s^2 + u)^2$, whose derivative is zero exactly when $s^2 + u = 2u$. So the response is largest at $\sigma = s$, with the value $\frac{1}{2}$ for every $s$. If the image is enlarged by a factor $c$, the blob has size $cs$ and the selected scale is $c\sigma$. This is the covariance with scale that scale selection gives, and the factor $\sigma^2$ is what makes it work: without it the response falls as $\sigma$ grows and the largest value is always at the smallest scale.

**A repeatability rate.** A detector returns the points $(10, 10)$, $(20, 5)$, $(30, 30)$ and $(40, 12)$ in $I$. The second image is $I$ shifted by $(3, -2)$, and the detector returns $(13, 8)$, $(23, 3)$, $(43, 10.5)$ and $(50, 50)$ in it. Mapped by the shift, the first points become $(13, 8)$, $(23, 3)$, $(33, 28)$ and $(43, 10)$. With $\varepsilon = 1.5$ three of them have a partner, $(33, 28)$ has none, and $r = 3/\min(4, 4) = 0.75$.

**Where the marks are.** In a $5 \times 5$ window of a flat region all gradients are zero. On a straight edge they all point the same way, so the patch does not change when it slides along the edge. At a corner they point in two directions, and the patch changes for every direction of slide. The [corner detection](/corner-detection/) page turns this into a test on the eigenvalues of a $2 \times 2$ matrix.

## Known algorithms

| Detector | Features | Covariant with | Cost |
|---|---|---|---|
| [Harris corner detector](/harris-corner-detector/) | corners | shifts, turns | $O(WHr)$ for a window of radius $r$ |
| Shi and Tomasi | corners, by the smaller eigenvalue | shifts, turns | $O(WHr)$ |
| FAST (Rosten and Drummond, 2006) | corners, by a test on a circle of 16 pixels | shifts, turns in part | $O(WH)$ |
| [Laplacian of Gaussian](/laplacian-of-gaussian/) over scales | blobs with a scale | shifts, turns, scale | $O(WHr)$ per scale |
| [SIFT](/sift/) | extrema of a difference of Gaussians | shifts, turns, scale | $O(WH)$ for a fixed number of scales per octave |
| SURF (Bay and others, 2008) | extrema of a box-filter Hessian determinant | shifts, turns, scale | $O(WH)$ per scale with an [integral image](/integral-image/) |
| [Canny edge detector](/canny-edge-detector/) | edge pixels | shifts, turns | $O(WHr)$ |
| [Hough transform](/hough-transform/) | lines, circles | shifts, turns | depends on the parameter grid |

The costs are worst-case bounds for the stated parameters. Each detector also applies [non-maximum suppression](/non-maximum-suppression/) and a threshold, which decide how many features it returns. That number depends on the image and is not fixed by the method. The choice of a detector and of its thresholds is a heuristic matter, and published comparisons rank them differently for different scenes and transforms.

## Bounds

- **Reading the input.** A detector whose output can depend on any pixel must read all $WH$ of them, so $\Omega(WH)$ time is needed; the detectors above meet this bound up to the size of their filters.
- **Covariance from the response.** Let a detector return the local extrema of a response $F(I)$ over position. If $F(I \circ T^{-1}) = F(I) \circ T^{-1}$ for every $T$ in $G$, then a point $x$ is a local extremum of $F(I)$ exactly when $T(x)$ is one of $F(I \circ T^{-1})$, so the detector is covariant with $G$. Gradient-magnitude and eigenvalue responses satisfy this for shifts and turns of the continuous image. For scale they satisfy it only after each derivative of order $m$ is multiplied by $\sigma^m$, as in the blob example.
- **The grid breaks covariance.** On the pixel grid a turn by an angle that is not a multiple of $90°$, or a change of scale that is not a power of the sampling, needs resampling, so exact covariance holds only for shifts by whole pixels and turns by $90°$. Measured repeatability rates are below 1 for the other transforms.
- **The aperture problem.** At a point of a straight edge, the position along the edge is not fixed by the image near the point. A detector of points must therefore reject edge points, which is the reason for the tests on two eigenvalues in [corner detection](/corner-detection/) and on the ratio of curvatures in SIFT.

## Reductions

- **To filtering and non-maximum suppression.** Most detectors compute a response by [linear filtering](/linear-filtering/) and products of derivatives, and then keep the local maxima by [non-maximum suppression](/non-maximum-suppression/).
- **To eigenvalue problems.** Corner and blob tests are tests on the eigenvalues of a $2 \times 2$ symmetric matrix, of gradient products for corners and of second derivatives for blobs, which have a closed form; see [eigenvalue](/eigenvalue/).
- **Matching to nearest neighbour search.** After each feature gets a descriptor vector, matching two images is a [nearest neighbour search](/nearest-neighbor-search/) among the vectors, done exactly by a [k-d tree](/kd-tree-nearest-neighbor-search/) in low dimension or approximately by [approximate nearest neighbour search](/approximate-nearest-neighbor-search/).
- **As input to registration.** The matched features of two images are the point pairs of feature-based [image registration](/image-registration/).

## Applications

- Panoramas and the alignment of photos, through [image registration](/image-registration/).
- Structure from motion and visual odometry, where features tracked over many frames give the motion of the camera and the 3D points.
- Recognition of a known object or place by matching features against a database.
- Tracking of points in video, for example with the [Lucas-Kanade method](/lucas-kanade-method/) at corner points.
- Measurement in industry and medicine, where marks on a part or on tissue are found and followed.

## References
