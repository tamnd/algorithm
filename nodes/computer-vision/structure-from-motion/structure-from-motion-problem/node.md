---
tag: FS0JBE
kind: problem
slug: structure-from-motion-problem
name: Structure from motion
aliases:
- structure and motion recovery
area: computer-vision/structure-from-motion
level: core
summary: Recover the 3D points of a scene and the poses of the cameras that saw them from feature matches across a set of images.
prereqs: [camera-projection-matrix, epipolar-geometry, feature-track]
see_also: [incremental-structure-from-motion, global-structure-from-motion, bundle-adjustment, tomasi-kanade-factorization, sturm-triggs-factorization, view-graph, multi-view-stereo, visual-odometry]
sources:
  - book: isbn:9780521540513
    title: "Richard Hartley and Andrew Zisserman, Multiple View Geometry in Computer Vision, second edition, Cambridge University Press, 2004"
    locator: "Chapter 10, 3D reconstruction of cameras and structure (the reconstruction ambiguities and the projective reconstruction theorem) and Chapter 18, N-view computational methods"
  - book: isbn:9783030343712
    title: "Richard Szeliski, Computer Vision, Algorithms and Applications, second edition, Springer, 2022"
    locator: "Chapter 11, Structure from motion and SLAM"
  - paper: doi:10.1017/S096249291700006X
    title: "Onur Özyeşil, Vladislav Voroninski, Ronen Basri and Amit Singer, A survey of structure from motion, Acta Numerica 26, 2017, 305-364"
    locator: "the whole survey (the problem statement, the ambiguities, the incremental and global pipelines, rotation and location estimation)"
  - paper: doi:10.1145/1141911.1141964
    title: "Noah Snavely, Steven M. Seitz and Richard Szeliski, Photo tourism: exploring photo collections in 3D, ACM Transactions on Graphics 25(3), 2006, 835-846"
    locator: "the reconstruction section (structure from motion on unordered Internet photo collections)"
  - paper: doi:10.1109/CVPR.2016.445
    title: "Johannes L. Schönberger and Jan-Michael Frahm, Structure-from-motion revisited, IEEE Conference on Computer Vision and Pattern Recognition (CVPR 2016), 4104-4113"
    locator: "the review of the problem and of the incremental pipeline"
---

Structure from motion (SfM) is the problem of recovering the 3D positions of scene points (the structure) and the poses, and sometimes the calibrations, of the cameras that took a set of images (the motion), from the image positions of the points alone. The data are [feature tracks](/feature-track/): for each scene point, the pixels where it appears in the images that see it. The cameras follow the pinhole model with the [camera projection matrix](/camera-projection-matrix/) $P_i = K_i [R_i \mid t_i]$, so the problem is to invert the projection equations for many cameras and points at once. A solution is fixed only up to a change of the world frame: a similarity for calibrated cameras and a projective map for uncalibrated ones. The usual final answer is the one that minimizes the total [reprojection error](/reprojection-error/), which is the [bundle adjustment](/bundle-adjustment/) problem, but that cost is not convex, so practical methods first build a good start. [Incremental structure from motion](/incremental-structure-from-motion/) adds one camera at a time, [global structure from motion](/global-structure-from-motion/) solves for all rotations and then all positions, and the factorization methods of [Tomasi and Kanade](/tomasi-kanade-factorization/) and [Sturm and Triggs](/sturm-triggs-factorization/) solve the case where every point is seen in every image by one singular value decomposition.

## In plain words

You walk around a building and take many photos. In each photo, a program finds small distinctive spots and works out which spots in different photos show the same piece of the building. Structure from motion takes only these spot positions and answers two questions together: where was the camera, and which way did it point, for each photo, and where is each piece of the building in 3D? The answers depend on each other. If you knew the cameras, you could find each point by crossing the viewing rays. If you knew the points, you could find each camera from what it sees. The photos alone cannot tell the size of the building, or where the world starts, so the answer is only fixed up to a move, a turn and a change of scale.

## Definition

**Input.**
- $N$ images. For each image $i$, an intrinsic matrix $K_i$ if the camera is calibrated, or nothing if it is not.
- $n$ tracks. Track $j$ is a set of observations $(i, x_{ij})$: the scene point $j$ appears at the pixel $x_{ij}$ in image $i$. There are $m$ observations in all. Some observations can be wrong matches (outliers).

The camera frame has $X$ to the right, $Y$ down and $Z$ forward. A world point $X$ maps to the camera frame by $X_c = R_i X + t_i$ with $R_i \in SO(3)$, to the pixel $\pi(K_i X_c)$, where $\pi(a, b, c) = (a / c, b / c)$, and it is visible only if its depth $Z_c$ is positive. The center of camera $i$ is $C_i = -R_i^{\mathsf T} t_i$.

**Output.** Camera parameters $(K_i, R_i, t_i)$ for as many images as possible and a point $X_j \in \mathbb{R}^3$ for as many tracks as possible, such that the inlier observations satisfy $\pi(K_i (R_i X_j + t_i)) \approx x_{ij}$ with positive depth, and a list of the observations judged to be outliers.

**Cost.** With independent Gaussian pixel noise of equal variance, the maximum likelihood answer minimizes
$$F = \sum_{(i, j)} \big\| \pi(K_i (R_i X_j + t_i)) - x_{ij} \big\|^2$$
over all inlier observations. This is bundle adjustment. A structure from motion method is judged by whether it finds the right inlier set and a start in the basin of the global minimum of $F$.

**Ambiguity.** If $(R_i, t_i, X_j)$ is a solution, so is the transformed scene $X_j' = s Q X_j + d$ with the cameras $R_i' = R_i Q^{\mathsf T}$, $t_i' = s t_i - R_i' d$, for any rotation $Q$, scale $s > 0$ and shift $d$, since $R_i' X_j' + t_i' = s (R_i X_j + t_i)$ and $\pi$ ignores the factor $s$. So calibrated SfM has a 7-parameter family of equal answers (theorem). For uncalibrated cameras the family is the 15-parameter group of projective maps of space: $P_i H^{-1}$ and $H X_j$ give the same images for any invertible $4 \times 4$ matrix $H$ (theorem). The [projective reconstruction theorem](/projective-reconstruction-theorem/) states that, for two views in general position, this is the only ambiguity. The outputs are compared only after one fixes the [gauge](/gauge-freedom/), for example $R_0 = I$, $t_0 = 0$ and one distance set to 1.

## Variants

- **Calibrated or uncalibrated.** With known $K_i$, the result is metric up to a similarity. With unknown $K_i$, the direct result is projective, and [self-calibration](/self-calibration/) or a [stratified reconstruction](/stratified-reconstruction/) upgrades it to a metric one.
- **Affine cameras.** When the scene depth is small compared with the distance, the [affine camera model](/affine-camera-model/) applies, the projection becomes linear, and the [Tomasi-Kanade factorization](/tomasi-kanade-factorization/) solves the problem in closed form if all points are seen in all images.
- **Ordered or unordered images.** A video gives images in time order with small motion between frames, which is the setting of [visual odometry](/visual-odometry/) and SLAM. An Internet photo collection has no order, so the pairs that overlap must first be found, for example by [image retrieval](/image-retrieval/), and stored in a [view graph](/view-graph/).
- **Full or missing data.** In the full data case, every point is seen in every image, and the measurement matrix is complete. Real data has a sparse pattern of visibility, which rules out the plain factorization methods.
- **Other features.** Lines, planes, or known objects can replace points, and other sensors (GPS, an inertial unit) can add constraints on the cameras.
- **Rolling shutter and moving objects.** A rolling shutter gives each image row its own pose, and a non-rigid scene breaks the model; both need extended models.

## Examples

- **Two calibrated views.** The [essential matrix](/essential-matrix/) from five or more matches gives the relative pose $(R, t)$ with $\|t\| = 1$; the [five-point algorithm](/five-point-algorithm/) gives at most 10 solutions for 5 matches (theorem). [Triangulation](/point-triangulation/) then gives the points. The size of the scene stays unknown, which is the scale part of the gauge.
- **A small synthetic scene.** The reference test of [incremental structure from motion](/incremental-structure-from-motion/) has 5 cameras at a distance of about 5 from 40 points in a cube of side 2, 160 observations with 0.5 pixel noise and 5% of the observations replaced by random pixels. The pipeline registers all 5 cameras, keeps 36 points and 138 observations, and its points agree with the truth to 0.034 after a similarity alignment (a benchmark result on this scene).
- **Pure rotation.** If all images are taken from one center, the images are related by [homographies](/homography/), the rays of a point never cross at a finite angle, and no depth can be recovered. This is a degenerate input, not a hard instance.
- **A counting argument.** Each observation gives 2 equations, and a calibrated scene has $6N + 3n - 7$ free parameters after the gauge. So $2m \ge 6N + 3n - 7$ is necessary for a finite set of solutions in general position (a counting argument). Ullman (1979) showed that 3 orthographic views of 4 non-coplanar points fix the structure up to a mirror reflection (theorem).

## Known algorithms

- [Incremental structure from motion](/incremental-structure-from-motion/): start from a good pair, then add images one at a time by [PnP](/perspective-n-point/), [triangulate](/point-triangulation/) new points and run bundle adjustment after each step. It is the method of Bundler (Snavely, Seitz and Szeliski 2006) and COLMAP (Schönberger and Frahm 2016).
- [Global structure from motion](/global-structure-from-motion/): estimate the relative poses of all overlapping pairs, solve [rotation averaging](/rotation-averaging/) and then [translation averaging](/translation-averaging/) for all cameras at once, triangulate, and run bundle adjustment once.
- [Tomasi-Kanade factorization](/tomasi-kanade-factorization/): affine cameras and full data, by a rank 3 SVD and a metric upgrade.
- [Sturm-Triggs factorization](/sturm-triggs-factorization/): perspective cameras and full data, by projective depths from [fundamental matrices](/fundamental-matrix/) and a rank 4 SVD.
- [Bundle adjustment](/bundle-adjustment/), for example by [sparse bundle adjustment](/sparse-bundle-adjustment/), refines the result of any of these methods.
- Hierarchical methods split the images into clusters, reconstruct each cluster and merge the parts by similarity transforms; they sit between the incremental and the global methods.

## Bounds

- **Minimal problems.** Two calibrated views need 5 point matches and give at most 10 relative poses (theorem). Two uncalibrated views need 7 matches and give 1 or 3 fundamental matrices (theorem). These are the sample sizes of [RANSAC](/ransac/) in SfM pipelines.
- **No global optimality in general.** The bundle adjustment cost is not convex, and no known algorithm finds its global minimum for general inputs in polynomial time. The practical methods are heuristics with a local refinement at the end.
- **Convex subproblems.** With known rotations and calibrations, each observation gives the constraint $\tilde x_{ij} \times (R_i X_j + t_i) = 0$ for the normalized point $\tilde x_{ij} = K_i^{-1} (x_{ij}, 1)$, and these constraints are linear in all $X_j$ and $t_i$ (theorem). Kahl and Hartley showed that the same problem with the maximum reprojection error as the cost is quasi-convex and can be solved to global optimality by bisection with second order cone programs (theorem).
- **Critical configurations.** Some scenes and camera paths admit more than one reconstruction that is not related by the gauge, for example points and centers on certain quadric surfaces; see [critical configurations](/critical-configurations/).
- **Data size.** A reconstruction reads all $m$ observations, so any method costs $\Omega(m)$. Incremental methods with a full bundle adjustment after each image cost much more, which is why large systems run global or partial bundle adjustments.

## Reductions

- **To bundle adjustment.** Given a start inside the basin of the global minimum and the right inlier set, SfM reduces to [bundle adjustment](/bundle-adjustment/), a [nonlinear least squares](/nonlinear-least-squares/) problem.
- **To averaging problems.** The global approach splits SfM into [rotation averaging](/rotation-averaging/) over the [view graph](/view-graph/), [translation averaging](/translation-averaging/) with the rotations fixed, and triangulation with all cameras fixed. Each of these is a smaller problem.
- **To PnP and triangulation.** With all points known, each camera is a [perspective-n-point](/perspective-n-point/) problem. With all cameras known, each point is a [triangulation](/point-triangulation/) problem. Incremental SfM alternates these two, and bundle adjustment couples them.
- **To pose graph optimization.** In SLAM, the relative poses between keyframes form a [pose graph](/pose-graph/), and [pose graph optimization](/pose-graph-optimization/) solves the same synchronization problem on camera poses without the points.
- **From the affine case to low rank approximation.** Under the affine camera model with full data, SfM is the best rank 3 approximation of the centered measurement matrix (theorem), which the [singular value decomposition](/singular-value-decomposition/) solves.

## Applications

- 3D models of buildings, cities and cultural heritage sites from photo collections, as in Photo Tourism.
- Aerial photogrammetry and mapping from drone or aircraft images.
- Camera tracking for visual effects in film (match moving) and for augmented reality.
- Robot and vehicle localization, where the sequential form is visual odometry and visual SLAM.
- The camera poses that [multi-view stereo](/multi-view-stereo/) needs to compute dense depth maps and surface meshes.

## References
