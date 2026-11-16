---
tag: ANM3SB
kind: definition
slug: detector-repeatability
name: Detector repeatability
aliases:
- repeatability score
area: computer-vision/local-features
level: core
summary: The fraction of features found in one image that are found again, at the corresponding place and shape, in a transformed image of the same scene.
prereqs: [invariant-local-features, homography]
see_also: [harris-affine-detector, harris-laplace-detector, maximally-stable-extremal-regions, difference-of-gaussians-detector, intersection-over-union, feature-matching, homography-estimation, image-registration]
sources:
  - paper: doi:10.1023/A:1008199403446
    title: Cordelia Schmid, Roger Mohr and Christian Bauckhage, Evaluation of interest point detectors, International Journal of Computer Vision 37(2), 151-172, 2000
    locator: the section on the repeatability criterion (repeated points within a tolerance, counted in the common part of the two images)
  - paper: doi:10.1023/B:VISI.0000027790.02288.f2
    title: Krystian Mikolajczyk and Cordelia Schmid, Scale and affine invariant interest point detectors, International Journal of Computer Vision 60(1), 63-86, 2004
    locator: Section 4.1 (the repeatability criterion with a location error below 1.5 pixels and a surface error below 0.4)
  - paper: doi:10.1007/s11263-005-3848-x
    title: Krystian Mikolajczyk, Tinne Tuytelaars, Cordelia Schmid, Andrew Zisserman, Jiri Matas, Frederik Schaffalitzky, Timor Kadir and Luc Van Gool, A comparison of affine region detectors, International Journal of Computer Vision 65(1-2), 43-72, 2005
    locator: the section on the evaluation criterion (the overlap error of elliptic regions, the threshold of 40 percent and the repeatability score)
  - paper: doi:10.1561/0600000017
    title: Tinne Tuytelaars and Krystian Mikolajczyk, Local invariant feature detectors, a survey, Foundations and Trends in Computer Graphics and Vision 3(3), 177-280, 2008
    locator: the part on the properties of good features and on the evaluation of detectors
---

The repeatability of a feature detector on a pair of images is the fraction of its features that it finds again, at the corresponding place and with the corresponding shape, when it runs on both images. The two images show the same scene, and the map between them is known, so the place where each feature should appear in the other image can be computed. Repeatability measures how well the detector is [covariant](/invariant-local-features/) in practice, with noise, sampling and the changes of light and view that real images have. It does not look at descriptors; the fraction of correct descriptor matches is a different number, the matching score.

## Definition

**Setting.** Let $I_1$ and $I_2$ be two images of a plane, or of any scene seen from one center of projection, so that a [homography](/homography/) $H$ maps the points of $I_1$ to the points of $I_2$. $H$ is known from a separate, accurate estimate. The *common part* is the set of points of $I_1$ whose image under $H$ is inside $I_2$, and the points of $I_2$ that come from it. Let $n_1$ and $n_2$ be the numbers of features that the detector finds in the common part of $I_1$ and of $I_2$.

**Repeated points.** For point features, a point $\mathbf x_1$ of $I_1$ is *repeated* with tolerance $\varepsilon$ if the detector found a point $\mathbf x_2$ in $I_2$ with $\lVert H(\mathbf x_1) - \mathbf x_2 \rVert \le \varepsilon$. Schmid, Mohr and Bauckhage define the repeatability rate as the number of repeated points divided by $\min(n_1, n_2)$.

**Overlap error.** For region features, each region is an ellipse $R_\mu = \{\mathbf x : (\mathbf x - \mathbf c)^\top \mu (\mathbf x - \mathbf c) \le 1\}$ with a center $\mathbf c$ and a positive definite matrix $\mu$. A region $R_b$ of $I_2$ is mapped into $I_1$ with the affine map $A$ that is the first-order part of $H^{-1}$ at its center, which gives the ellipse $\mu' = A^{-\top} \mu_b A^{-1}$ around $H^{-1}(\mathbf c_b)$. The overlap error of $R_a$ in $I_1$ and $R_b$ is

$$\varepsilon_O = 1 - \frac{\lvert R_a \cap R_{\mu'} \rvert}{\lvert R_a \cup R_{\mu'} \rvert},$$

one minus the [intersection over union](/intersection-over-union/) of the two ellipses. The regions *correspond* when $\varepsilon_O$ is below a threshold: $0.4$ in the comparison of Mikolajczyk and others (2005). Mikolajczyk and Schmid (2004) ask for a location error below $1.5$ pixels and a surface error, the same overlap error, below $0.4$.

**Repeatability score.** The repeatability score is the number of corresponding pairs divided by $\min(n_1, n_2)$. Here each feature is used in at most one pair, so the score is a number in $[0, 1]$, often given in percent. The *number of correspondences* is reported next to it, because a high score on few features means little.

## Examples and non-examples

**Example: a count.** In the common part the detector finds $n_1 = 5$ points in $I_1$ and $n_2 = 4$ points in $I_2$. Three points of $I_1$ have a point of $I_2$ within $\varepsilon$ after the map by $H$. The repeatability is $3 / \min(5, 4) = 75$ percent.

**Example: two circles with the same center.** A circle of radius $1$ and a circle of radius $r > 1$ with the same center have the overlap error $1 - 1/r^2$. For $r = 1.2$ it is $0.306$, so they correspond under the threshold $0.4$. For $r = 1.3$ it is $0.408$, so they do not. The threshold accepts a scale error up to the factor $\sqrt{1/0.6} = 1.29$.

**Example: two shifted circles.** Two circles of radius $1$ whose centers are $d$ apart overlap in the area $2\arccos(d/2) - (d/2)\sqrt{4 - d^2}$. The overlap error is $0.226$ for $d = 0.2$, $0.320$ for $d = 0.3$ and $0.404$ for $d = 0.4$. So a region passes the threshold of $0.4$ only if its center is off by less than about $0.4$ times its radius, and a small region needs a more precise position than a large one.

**Example: an exact transformation.** When $I_2$ is $I_1$ turned by 90 degrees, or shifted by whole pixels, the map is exact on the pixel grid. A detector that is exactly covariant with that map has repeatability 100 percent for every $\varepsilon \ge 0$, except near the image border, where a shifted image gives the detector different pixels.

**Non-example: descriptor matches.** The share of features whose nearest descriptor in the other image is the true correspondent is the matching score. It depends on the descriptor and on how many similar features the image holds, and it can be low when the repeatability is high.

**Non-example: a detector that marks everything.** A detector that returns every pixel of the image has repeatability $1$ under any shift for every $\varepsilon \ge \sqrt 2 / 2 \approx 0.71$ pixels, and is of no use. The score must be read together with the number of features and their density.

**Non-example: two views of a scene with depth.** If the scene is not a plane and the camera center moves, no homography maps one image to the other, and the place of a feature in the second image depends on its depth. The definition then needs the depth of each point or a dense ground truth.

## Related definitions

- **Matching score.** The ratio of correct descriptor matches to the smaller number of features; it measures the detector and the [descriptor](/feature-descriptor/) together.
- **Localization error.** The distance $\lVert H(\mathbf x_1) - \mathbf x_2 \rVert$ for one repeated point; repeatability counts the points where it is below $\varepsilon$.
- **[Intersection over union](/intersection-over-union/).** The overlap error is one minus the intersection over union of the two regions; detection benchmarks use the same ratio for boxes.
- **[Covariance](/invariant-local-features/).** A detector that is exactly covariant with the map between the images has repeatability $1$ when the image itself changes exactly by the map.
- **[Homography estimation](/homography-estimation/).** The ground truth map $H$ of a benchmark pair is an estimated homography, so its error enters the score.

## References
