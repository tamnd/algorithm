---
tag: 2E4BQ0
kind: concept
slug: photo-consistency
name: Photo-consistency
aliases:
- photometric consistency
area: computer-vision/stereo-and-dense-reconstruction
level: core
summary: A 3D point is photo-consistent when the images that see it agree in color around its projections, the test on which multi-view stereo rests.
prereqs: [pinhole-camera-model, lambertian-reflectance, normalized-cross-correlation]
see_also: [multi-view-stereo, stereo-matching-cost, plane-sweep-stereo, patch-based-multi-view-stereo, space-carving, voxel-coloring, census-transform, helmholtz-reciprocity]
sources:
  - paper: doi:10.1109/CVPR.2006.19
    title: Steven M. Seitz, Brian Curless, James Diebel, Daniel Scharstein and Richard Szeliski, A comparison and evaluation of multi-view stereo reconstruction algorithms, IEEE Conference on Computer Vision and Pattern Recognition 2006
    locator: Section 2 (photo-consistency measures in scene space and in image space, and the visibility models)
  - paper: doi:10.1561/0600000052
    title: "Yasutaka Furukawa and Carlos Hernández, Multi-view stereo: a tutorial, Foundations and Trends in Computer Graphics and Vision 9(1-2), pages 1 to 148, 2015"
    locator: the chapter on multi-view photo-consistency (the measures and how they are combined over many views)
  - book: isbn:9783030343712
    title: Richard Szeliski, Computer Vision, Algorithms and Applications, second edition, Springer, 2022
    locator: Chapter 12, Depth estimation (matching costs and multi-view stereo)
---

Photo-consistency is the test that a 3D point, or a small piece of surface, could really be part of the scene: the images that see it must record about the same color around the places where it projects. It is the data term of almost every [multi-view stereo](/multi-view-stereo/) method. A point on the true surface passes the test, and a point in front of or behind the surface usually fails it, because each camera then sees a different part of the scene. The two-view form of the same idea, a cost per pixel and disparity, is the [stereo matching cost](/stereo-matching-cost/); this page is about the test in 3D over any number of calibrated views.

## In plain words

Imagine three people who look at the same spot from different places and each say what color they see. If the spot is on a real object, they all say "dark red". If the spot is just empty air in front of the object, each of them looks through it to a different part of the background and they disagree. Photo-consistency is a number for how well the views agree. A method that rebuilds a scene keeps the points where the views agree and throws away the others.

## The idea

**The point test.** Let $X$ be a point and let $V(X)$ be the set of images that see it. Each image $i$ projects $X$ to the pixel $\pi_i(X)$. If the surface is Lambertian ([Lambertian reflectance](/lambertian-reflectance/)), it sends the same light in all directions, so

$$I_i(\pi_i(X)) \approx I_j(\pi_j(X)) \quad \text{for all } i, j \in V(X).$$

Voxel coloring and space carving use the spread of these values, for example their variance, and call $X$ consistent when the spread is below a threshold.

**The patch test.** One pixel value has noise and does not tell much. Most methods test a small piece of surface instead: a planar patch with a center and a normal. They lay a grid of points on the patch, project the grid into each image, and compare the sampled windows. Because the patch is a plane, the map from one image to another over the patch is a [homography](/homography/), so the windows are correctly warped even when the surface is slanted.

**The measure.** For two windows $a$ and $b$ of $n$ samples each, the common measures are:

- the sum of squared differences $\sum_k (a_k - b_k)^2$ and the sum of absolute differences $\sum_k |a_k - b_k|$, which are simple and fast but change with exposure;
- the [normalized cross-correlation](/normalized-cross-correlation/) $\mathrm{NCC}(a, b) = \sum_k (a_k - \bar a)(b_k - \bar b) / \sqrt{\sum_k (a_k - \bar a)^2 \sum_k (b_k - \bar b)^2}$, which does not change when $b$ is replaced by $\alpha b + \beta$ with $\alpha > 0$, so it ignores gain and offset between cameras;
- the [census transform](/census-transform/) and other rank measures, which compare only the order of the values.

**Many views.** With $N$ images, the measure is computed between a reference image and each other image, and the results are combined. A plain mean is hurt by images where $X$ is hidden or where there is a highlight. Robust choices use the best $k$ of the scores, cut each score at a limit, or keep only the images whose score passes a threshold, as [PMVS](/patch-based-multi-view-stereo/) does with its set $V^*(p)$.

**Scene space and image space.** Seitz et al. (2006) separate two families. A scene space measure projects a point or patch into the images and compares the values, as above. An image space measure renders the current shape into each view, with the colors of the other views, and compares the rendered image with the real one. Neural scene models such as the [neural radiance field](/neural-radiance-field/) use an image space form: they fit the scene so that rendered pixels match the photos.

**Visibility.** The test needs $V(X)$, but which images see $X$ depends on the shape that is being computed. Seitz et al. name three answers: geometric (use the current shape to compute occlusion exactly), quasi-geometric (use an approximate shape, for example the [visual hull](/visual-hull/), or only nearby cameras) and outlier-based (treat a hidden view as an outlier and use a robust measure).

**Where the test fails.** The test is only as good as its assumptions.

- *No texture.* On a uniform wall every depth gives the same colors, so every depth passes. Kutulakos and Seitz (2000) showed that the set of shapes that pass a monotone test has a largest member, the photo hull, which can be much larger than the true scene.
- *Repeated texture.* A wrong depth can line up one period of a pattern with the next. More views at other baselines remove most such cases.
- *Specular and transparent surfaces.* The Lambertian assumption fails. [Helmholtz reciprocity](/helmholtz-reciprocity/) gives a test that does not need it, with special lighting.
- *Large windows.* A window on a curved surface or across a depth edge mixes surfaces. Patches with normals help on slanted surfaces, not at edges.

## Examples

**Variance of a point.** Three images see a candidate point and record 100, 102 and 98. The mean is 100 and the variance is $(0 + 4 + 4) / 3 \approx 2.67$, so the point passes a variance threshold of, say, 25. At a wrong depth the same pixel rays meet the scene at different places, and the images record 100, 140 and 60: the variance is $(0 + 1600 + 1600) / 3 \approx 1067$, and the point fails.

**NCC ignores gain and offset.** The window $a = (10, 20, 30)$ in one image and $b = (25, 45, 65)$ in a brighter image show the same surface, since $b = 2a + 5$. The deviations from the means are $(-10, 0, 10)$ and $(-20, 0, 20)$, so $\mathrm{NCC} = 400 / \sqrt{200 \cdot 800} = 1$. The sum of squared differences is $15^2 + 25^2 + 35^2 = 2075$, which looks like a bad match. For the reversed window $b = (30, 20, 10)$ the NCC is $-1$.

**A plane sweep score.** In [plane sweep stereo](/plane-sweep-stereo/), each plane gives a depth for each pixel, and the score of that pixel and plane is a photo-consistency measure between the reference window and the warped windows of the other images. The depth with the best score wins.

## Where it is used

- [Plane sweep stereo](/plane-sweep-stereo/) and [PatchMatch stereo](/patchmatch-stereo/): the cost of a depth or of a slanted plane at a pixel.
- [Patch-based multi-view stereo](/patch-based-multi-view-stereo/): the score $g^*$ of a patch, one minus the mean NCC.
- [Space carving](/space-carving/) and [voxel coloring](/voxel-coloring/): the test that decides whether a voxel stays.
- [Depth map fusion](/depth-map-fusion/): checks that a depth from one view agrees with the images of the other views.
- [Neural radiance fields](/neural-radiance-field/) and [3D Gaussian splatting](/gaussian-splatting/): the photometric loss between rendered and real pixels, which is an image space form of the same test.

## References
