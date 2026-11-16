---
tag: K15KYC
kind: algorithm
slug: incremental-structure-from-motion
name: Incremental structure from motion
aliases:
- sequential structure from motion
area: computer-vision/structure-from-motion
level: core
summary: Start from a good image pair, then add one image at a time by PnP, triangulate its new points and bundle adjust, rejecting outliers as it goes.
solves: [structure-from-motion-problem]
model: real-ram
complexity:
  vars: {N: "the number of images", n: "the number of tracks", m: "the number of observations"}
  time: {total: "O(N^2 m + N^4)"}
  space: {extra: "O(N^2 + m)"}
properties: {deterministic: false, iterative: true, local: true, recursive: false, monotone: false}
history:
  year: 2006
  people: [Noah Snavely, Steven M. Seitz, Richard Szeliski, Johannes L. Schönberger, Jan-Michael Frahm]
  note: Sequential reconstruction from image sequences goes back to the 1990s. Photo Tourism (2006) applied it to unordered Internet photo collections, and COLMAP (Schönberger and Frahm, 2016) is the standard modern form.
prereqs: [structure-from-motion-problem, perspective-n-point, point-triangulation, bundle-adjustment, ransac]
see_also: [global-structure-from-motion, essential-matrix-decomposition, five-point-algorithm, sparse-bundle-adjustment, reduced-camera-system, scale-drift, view-graph, feature-track]
sources:
  - paper: doi:10.1145/1141911.1141964
    title: "Noah Snavely, Steven M. Seitz and Richard Szeliski, Photo tourism: exploring photo collections in 3D, ACM Transactions on Graphics 25(3), 2006, 835-846"
    locator: "the structure from motion section (the initial pair, the addition of one camera at a time, the bundle adjustment after each addition)"
  - paper: doi:10.1109/CVPR.2016.445
    title: "Johannes L. Schönberger and Jan-Michael Frahm, Structure-from-motion revisited, IEEE Conference on Computer Vision and Pattern Recognition (CVPR 2016), 4104-4113"
    locator: "the whole paper (the initialization, the next best view selection, robust triangulation, bundle adjustment and filtering)"
  - book: isbn:9780521540513
    title: "Richard Hartley and Andrew Zisserman, Multiple View Geometry in Computer Vision, second edition, Cambridge University Press, 2004"
    locator: "Chapter 7 (camera resectioning by the DLT), Chapter 9 (the essential matrix and its four decompositions), Chapter 12 (triangulation) and Chapter 18 (N-view methods)"
  - paper: doi:10.1007/3-540-44480-7_21
    title: "Bill Triggs, Philip F. McLauchlan, Richard I. Hartley and Andrew W. Fitzgibbon, Bundle adjustment, a modern synthesis, Vision Algorithms: Theory and Practice, Lecture Notes in Computer Science 1883, Springer, 2000, 298-372"
    locator: "the sections on the sparse normal equations and the Schur complement"
  - book: isbn:9783030343712
    title: "Richard Szeliski, Computer Vision, Algorithms and Applications, second edition, Springer, 2022"
    locator: "Chapter 11, Structure from motion and SLAM (the section on multi-frame structure from motion)"
---

Incremental structure from motion is the most used way to solve the [structure from motion problem](/structure-from-motion-problem/) for calibrated cameras. It builds the reconstruction one image at a time. It starts from one image pair with many matches, finds the relative pose of the pair from the essential matrix, and [triangulates](/point-triangulation/) the common tracks. Then it repeats three steps: it picks the next image that sees many points that are already in 3D, finds its pose by [PnP](/perspective-n-point/) inside [RANSAC](/ransac/), triangulates the tracks that the new image makes visible in two images, and runs [bundle adjustment](/bundle-adjustment/) to refine all cameras and points together. After each bundle adjustment it drops the observations with a large reprojection error. Each step is a small, well understood problem with a robust solver, and the repeated bundle adjustment stops the errors from piling up, which makes the method accurate and reliable. The cost is that the bundle adjustments become expensive for many images, and a bad early decision can spoil the rest.

## In plain words

Think of a jigsaw puzzle that you build from one corner. First you find two photos that overlap a lot and work out how the second camera stood compared with the first. From these two views you place the first set of points in 3D. Next you look for the photo that sees the most of the points you have already placed. From those points you can work out where that camera stood. Now the new photo lets you place more points. Then you adjust everything a little, so that all the points and cameras agree as well as possible, and you throw away the matches that still do not fit. You repeat this until no photo can be added.

## The problem

**Input.** An intrinsic matrix $K$ shared by all images (the method extends to one $K_i$ per image), and the [feature tracks](/feature-track/) of $N$ images: track $j$ lists the pixel $u_{ij}$ of one scene point in each image $i$ that sees it. A threshold $\tau$ on the reprojection error in pixels, and a random seed.

**Output.** A pose $(R_i, t_i)$ with $X_c = R_i X + t_i$ for each image that could be registered, a point $X_j$ for each track that could be triangulated, and the set of kept observations. After each run of line L9, every kept observation has a reprojection error of at most $\tau$, and every kept point has at least two kept observations. The first image $a$ has $R_a = I$ and $t_a = 0$, and the second image $b$ starts with $\|t_b\| = 1$, so the result is fixed up to this similarity.

**Coordinates.** The code works in normalized image coordinates $x_{ij} = K^{-1} u_{ij}$, so a reprojection error $e$ in these coordinates is about $f e$ pixels for the focal length $f$.

## The algorithm

```pseudo id=main
INCREMENTAL-SFM(K, tracks, τ)
L1  (a, b) <- the image pair with the most common tracks
L2  (R_b, t_b), inliers <- RANSAC on the eight-point essential matrix with the Sampson error, then the decomposition with the most points in front; R_a <- I, t_a <- 0
L3  triangulate each inlier track from a and b, keep it if both errors are below τ
L4  bundle adjust all cameras and points with camera a fixed
L5  while some unregistered image sees at least 6 triangulated points
L6      c <- the unregistered image that sees the most triangulated points
L7      (R_c, t_c), inliers <- RANSAC on the six-point DLT pose, each fit refined by Gauss-Newton; add the inlier observations
L8      triangulate each new track seen by c and at least one other registered image; keep the views with error below τ, refit once, keep it if 2 views remain
L9      bundle adjust with camera a fixed; drop observations with error above τ and points with fewer than 2 observations
L10 return the cameras, the points and the kept observations
```

Line L1 uses the number of common tracks. Real systems also ask for a wide baseline, for example many inliers to the essential matrix but few to a homography, because a pair with a short baseline gives poorly conditioned depths. Line L2 uses the [eight-point algorithm](/eight-point-algorithm/) on normalized points, with [Hartley normalization](/hartley-normalization/); the [five-point algorithm](/five-point-algorithm/) is the usual choice in practice. The decomposition picks, among the four candidates of the [essential matrix decomposition](/essential-matrix-decomposition/), the one that puts the most points in front of both cameras, the [cheirality](/cheirality/) test. Line L7 is a [DLT resection](/dlt-camera-resectioning/) on 6 points, with its $3 \times 3$ block projected to the nearest rotation. Calibrated minimal solvers such as [P3P](/p3p/) need fewer samples. Line L8 is linear triangulation. Lines L4 and L9 run [Levenberg-Marquardt](/levenberg-marquardt/) on the reprojection error and eliminate the points with the [Schur complement](/schur-complement/), so the solve is on the [reduced camera system](/reduced-camera-system/).

## Example

The reference test uses 5 cameras with $f = 800$ px that look at a cube of 40 points from a distance of 5 units, each turned by up to 0.5 rad. Each point is seen by each camera with probability 0.8. Gaussian noise of 0.5 px is added, and 5% of the observations are replaced by random pixels. With $\tau = 3$ px:

- There are 160 observations. Line L1 picks the pair $(0, 3)$ with 29 common tracks, and line L2 keeps 25 of them as inliers.
- The loop registers the images in the order 2, 1, 4. Image 2 sees 20 triangulated points, and PnP keeps 16. Image 1 sees 25 and keeps 25. Image 4 sees 25 and keeps 24.
- The result has 5 cameras, 36 points and 138 kept observations. The largest reprojection error is 1.30 px and the root mean square error is 0.52 px. After the best similarity to the truth, the largest point error is 0.033 units, in a scene of size 2.

On the same scene without noise or outliers, all 40 points are recovered to $10^{-6}$ after the similarity, as the correctness section predicts. These are benchmark results of the reference test.

## Correctness

On exact data in general position, the method recovers every registered camera and every triangulated point exactly, up to the similarity fixed by the first pair (theorem). The reasons are: the eight-point method gives the exact essential matrix from 8 or more generic points, exactly one of its four decompositions puts the points in front of both cameras, linear triangulation from exact poses is exact, the DLT gives the exact pose from 6 or more points in general position, and bundle adjustment cannot move a solution with zero cost. The proof below gives the induction over the registration order. Each bundle adjustment never raises its cost, because Levenberg-Marquardt accepts only steps that lower it (theorem). With noise and outliers there is no guarantee: RANSAC finds an all-inlier sample only with high probability, bundle adjustment finds only a local minimum, and the order of the images matters (heuristic). The filter after each bundle adjustment makes sure that every kept point has at least two observations, each with an error of at most $\tau$ (theorem).

## Complexity

In the real RAM model, the RANSAC loops have a fixed cap on the number of samples, and each sample costs $O(n)$, so lines L2 and L7 cost $O(n)$ per image. Line L8 scans the tracks, $O(m)$ per image. Line L6 counts the seen points, $O(m)$ per image. The bundle adjustment dominates. With $N'$ registered cameras, one Levenberg-Marquardt iteration builds the reduced camera system in $O(m N')$ time, because a point seen by $d$ cameras adds $d^2$ blocks and $\sum d^2 \le N' m$, and solves it densely in $O(N'^3)$. With a fixed cap on the iterations, the bundle adjustments over all $N$ additions cost $O(\sum_{N'} (m N' + N'^3)) = O(N^2 m + N^4)$. The space is $O(N^2)$ for the reduced system plus $O(m)$ for the data. This quadratic and quartic growth is why large systems run the full bundle adjustment only after the model has grown by some fraction, and use local bundle adjustment in between.

## Properties

- **Randomized.** RANSAC samples at random, so the result depends on the seed; the reference code fixes it.
- **Local.** Bundle adjustment finds a local minimum near the start that the earlier steps give.
- **Order dependent.** Different first pairs or image orders can give different results, and an early wrong registration can spoil the rest.
- **Drift.** In long sequences without loops, small errors in the poses add up, as in [scale drift](/scale-drift/) of visual odometry.
- **Accurate.** With repeated bundle adjustment and outlier filtering, it is among the most accurate SfM methods on benchmarks (benchmark result).

## Variants and improvements

- **Next best view.** COLMAP scores the candidate images by the number and the spread of their visible points over the image, not only by the count, to register well conditioned images first.
- **Local bundle adjustment.** After each addition, adjust only the new camera and its neighbors; run the global adjustment after the model grows by a fixed fraction.
- **Robust triangulation.** COLMAP triangulates with RANSAC over the pairs of views of a track and merges and completes tracks after each step.
- **Minimal solvers.** Use the five-point method for the first pair and P3P for registration, both with a [local optimization in RANSAC](/lo-ransac/).
- **Hierarchical SfM.** Split the images into clusters, reconstruct each one incrementally and merge the partial models.
- **Uncalibrated images.** Add focal lengths and distortion to the bundle adjustment, with an initial focal length from the image metadata.

## When to use it

Use it for unordered photo collections when accuracy matters more than speed, up to tens of thousands of images. It handles outliers well because each step is robust and each new image is checked against a model that is already reliable. For very large collections, or when a fast first result is needed, use [global structure from motion](/global-structure-from-motion/), which solves for all cameras at once. For video in real time, use [visual odometry](/visual-odometry/) or SLAM with [keyframe selection](/keyframe-selection/).

## Pitfalls

- **A short baseline in the first pair.** The depths of the first points are then very uncertain, and the whole reconstruction can fail. Ask for a minimum triangulation angle.
- **Planar scenes.** The eight-point method fails when all points lie on one plane, and so does the six-point DLT for PnP. The five-point method and P3P still work for planar points, and a [homography](/homography/) can start the reconstruction.
- **Repetitive structures.** Symmetric buildings give wrong matches that agree with each other, which RANSAC cannot reject, and the result can fold onto itself.
- **The gauge.** Fixing one camera leaves the global scale free. Levenberg-Marquardt copes because of its damping, but a solver without damping needs a scale constraint as well.
- **Points behind the camera.** Check the depth sign in every reprojection error, or the bundle adjustment can move points through the camera.

## Implementations

## History

Sequential reconstruction from image sequences, which adds one view at a time to a projective or metric model, was developed in the 1990s, for example by Beardsley, Zisserman and Murray and by Pollefeys and colleagues. Snavely, Seitz and Szeliski (2006) applied the incremental scheme to unordered photo collections from the Internet in Photo Tourism and its software Bundler, with a bundle adjustment after each new camera. Schönberger and Frahm (2016) revisited each step, with a new next best view score, robust triangulation and iterative filtering, in COLMAP, which became the standard open tool.

## References
