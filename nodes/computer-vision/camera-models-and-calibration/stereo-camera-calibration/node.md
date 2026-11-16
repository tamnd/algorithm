---
tag: EMSXKE
kind: problem
slug: stereo-camera-calibration
name: Stereo camera calibration
aliases:
- stereo rig calibration
area: computer-vision/camera-models-and-calibration
level: core
summary: Estimate the intrinsics of two cameras and the rigid motion between them from shared views of a pattern, as needed for rectification and metric depth.
prereqs: [camera-calibration, camera-extrinsic-parameters, zhang-calibration-method]
see_also: [stereo-rectification, depth-from-disparity, essential-matrix, epipolar-geometry, relative-pose-problem, bundle-adjustment, rotation-averaging, point-triangulation]
sources:
  - book: isbn:9780521540513
    title: Richard Hartley and Andrew Zisserman, Multiple View Geometry in Computer Vision, second edition, Cambridge University Press, 2004
    locator: Section 9.6, The essential matrix (the relative pose of two calibrated cameras and its scale ambiguity); Section 11.12, Image rectification
  - paper: doi:10.1109/34.888718
    title: Zhengyou Zhang, A flexible new technique for camera calibration, IEEE Transactions on Pattern Analysis and Machine Intelligence 22(11), 2000, 1330-1334
    locator: the calibration of each camera from views of a plane, which gives the poses that the stereo calibration combines
  - book: isbn:9783030343712
    title: Richard Szeliski, Computer Vision, Algorithms and Applications, second edition, Springer, 2022
    locator: Chapter 12, Depth estimation (rectification and the relation of disparity to depth)
---

Stereo camera calibration finds the intrinsics and distortion of two cameras on a rigid rig, and the fixed rotation $R$ and translation $t$ that take points from the frame of the first camera to the frame of the second. The input is pairs of images of a calibration pattern, taken by both cameras at the same moment. The result is what [stereo rectification](/stereo-rectification/) needs to align the image rows, and what [depth from disparity](/depth-from-disparity/) needs to turn a disparity into a metric depth: the baseline $\|t\|$ gives the scale. It differs from single [camera calibration](/camera-calibration/) by the shared relative pose, which ties the two cameras together, and from the [relative pose problem](/relative-pose-problem/) by the known pattern, which fixes the scale of $t$.

## In plain words

Two cameras are bolted side by side, like two eyes. To measure depth, you need to know each camera's own numbers, and exactly where the second camera sits relative to the first, including the distance between them. You hold a checkerboard in front of both cameras and take photos with both at once, several times, in different positions. Each photo pair tells you where the board was for each camera. Since the cameras do not move relative to each other, the step from one camera to the other must be the same in every pair. You find that one step, then adjust all the numbers together so that the board corners land where they show in all the photos.

## Definition

Use the conventions of the [extrinsic parameters](/camera-extrinsic-parameters/) page: a point $X$ in the frame of the pattern has camera coordinates $X_{c} = R_j X + t_j$ in view $j$. For a rigid rig, the poses of the two cameras in view $j$ satisfy
$$R_{2j} = R\, R_{1j}, \qquad t_{2j} = R\, t_{1j} + t,$$
where $(R, t)$ is the fixed pose of camera 2 relative to camera 1: $X_{c2} = R X_{c1} + t$. If the two poses of one view are known, then
$$R = R_{2j} R_{1j}^{\mathsf T}, \qquad t = t_{2j} - R\, t_{1j}.$$
The center of camera 2 in the frame of camera 1 is $-R^{\mathsf T} t$, and the baseline is $\|t\|$.

**Input.** $N$ pairs of images of a pattern with known model points $m_i$; in view $j$, the pixels $u^{(1)}_{ij}$ in camera 1 and $u^{(2)}_{ij}$ in camera 2.

**Output.** $K_1$, $K_2$, the distortion of each camera, $(R, t)$, and the pose $(R_{1j}, t_{1j})$ of the pattern in camera 1 for each view.

**Criterion.** The maximum likelihood estimate under Gaussian pixel noise minimizes
$$\sum_{j} \sum_{i} \Big( \big\| u^{(1)}_{ij} - \pi_1(R_{1j}, t_{1j}; m_i) \big\|^2 + \big\| u^{(2)}_{ij} - \pi_2(R R_{1j}, R t_{1j} + t; m_i) \big\|^2 \Big),$$
where $\pi_c$ is the projection of camera $c$ with its intrinsics and distortion. The poses of camera 2 are not free: they are fixed by the poses of camera 1 and $(R, t)$, which is what makes this more than two separate calibrations.

## Variants

- **Fixed intrinsics.** Each camera is calibrated alone first, for example with [Zhang's method](/zhang-calibration-method/), and the stereo step fits only $(R, t)$ and the pattern poses. This is common when each camera can see the pattern alone more easily.
- **Joint fit.** All intrinsics, distortions, $(R, t)$ and the poses are fitted together, which uses the stereo views to improve the intrinsics too.
- **Without a pattern.** With known intrinsics and matched points of any scene, the relative pose comes from the [essential matrix](/essential-matrix/), but only up to the scale of $t$. A known length in the scene, or a known baseline, then fixes the scale.
- **Multi-camera rigs.** Three or more cameras with fixed relative poses. Pairwise poses are combined in a graph, for example by [rotation averaging](/rotation-averaging/), and refined jointly.
- **Different sensors.** A color camera with an infrared or depth camera; the model is the same, but the pattern must be visible to both.
- **Online recalibration.** Small corrections to $(R, t)$ during use, from the [epipolar geometry](/epipolar-geometry/) of natural image matches, to follow changes in the rig due to heat or shock.

## Examples

**Two cameras side by side.** In one view, camera 1 sees the pattern with $R_{11} = I$ and $t_{11} = (0, 0, 5)$, and camera 2 with $R_{21} = I$ and $t_{21} = (-0.1, 0, 5)$. Then
$$R = I \, I^{\mathsf T} = I, \qquad t = (-0.1, 0, 5) - (0, 0, 5) = (-0.1, 0, 0).$$
Camera 2 is $0.1$ units to the right of camera 1 ($-R^{\mathsf T} t = (0.1, 0, 0)$), and the baseline is $b = 0.1$. The essential matrix $E = [t]_\times R$ has the rows $(0, 0, 0)$, $(0, 0, 0.1)$ and $(0, -0.1, 0)$. For normalized image points $(x_1, y_1, 1)$ and $(x_2, y_2, 1)$, the epipolar constraint $x_2^{\mathsf T} E x_1 = 0.1 (y_2 - y_1) = 0$ says that matching points lie on the same row: this rig is already rectified.

**Depth.** With the same rig, $f = 500$ pixels for both cameras and a disparity of $d = 20$ pixels, the depth is $Z = f b / d = 500 \cdot 0.1 / 20 = 2.5$ units. A 1% error in the calibrated baseline gives a 1% error in every depth.

**A count.** With 15 views of a board with 54 corners seen by both cameras, there are $2 \cdot 2 \cdot 54 \cdot 15 = 3240$ equations. With zero skew and 2 radial distortion terms per camera, the unknowns are $2 \cdot (4 + 2) = 12$ intrinsic terms, 6 for $(R, t)$ and $6 \cdot 15 = 90$ for the poses, so 108 in total.

## Known algorithms

- **Calibrate each camera, compose, refine.** Calibrate each camera with [Zhang's method](/zhang-calibration-method/), compute $(R, t)$ from each view by the formulas above, take a robust mean over the views (the median of $t$ and a [rotation average](/rotation-averaging/) of $R$), and then minimize the criterion with [Levenberg-Marquardt](/levenberg-marquardt/). This is the scheme of the stereo functions of OpenCV and of the MATLAB toolbox of Bouguet.
- **Joint bundle adjustment.** For many cameras, a [bundle adjustment](/bundle-adjustment/) with the pattern points held fixed and the rig poses shared over all views.
- **Essential matrix and a scale.** Without a pattern: estimate the [essential matrix](/essential-matrix/) from matched points with known intrinsics, decompose it into $R$ and the direction of $t$, and fix the length of $t$ from one known distance.

## Bounds

- **Scale (theorem).** From image matches alone, with known intrinsics, $t$ is determined only up to a positive scale: scaling the scene and $t$ by the same factor leaves all images the same (HZ section 9.6). A pattern of known size removes this ambiguity.
- **One view is enough in principle (theorem).** If both cameras are calibrated and both see the pattern in one view, the two poses of that view, and so $(R, t)$, are determined. More views only reduce the effect of noise.
- **Depth sensitivity (theorem, to first order).** From $Z = f b / d$, an error $\delta d$ in disparity gives $\delta Z \approx Z^2 \delta d / (f b)$, and a relative error in $b$ or $f$ gives the same relative error in $Z$. So calibration errors matter most for far points and short baselines.
- **Vertical alignment (heuristic).** After rectification, a vertical error of more than a fraction of a pixel between matching points makes many [stereo matching](/stereo-matching/) methods, which search along one row, lose matches. The mean vertical error of rectified pattern corners is a practical check of the calibration.

## Reductions

- **To single camera calibration.** With fixed intrinsics, stereo calibration is two [camera calibrations](/camera-calibration/) plus the composition $R = R_{2j} R_{1j}^{\mathsf T}$, $t = t_{2j} - R t_{1j}$, then a small nonlinear fit.
- **To bundle adjustment.** The joint fit is a [bundle adjustment](/bundle-adjustment/) with known 3D points (the pattern) and a shared rig pose.
- **To the relative pose problem.** Without a pattern, it is the [relative pose problem](/relative-pose-problem/) for calibrated cameras, plus a scale.
- **Rectification uses it.** [Stereo rectification](/stereo-rectification/) takes $K_1$, $K_2$, the distortions, $R$ and $t$ as input, and gives the two rotations that make the epipolar lines horizontal.

## Applications

- **Depth cameras and 3D scanning.** Passive and active stereo sensors need $(R, t)$ to compute metric depth by [triangulation](/point-triangulation/).
- **Robots and cars.** Stereo heads for obstacle detection and mapping, where the baseline sets the range of useful depth.
- **Headsets.** VR and AR headsets with several tracking cameras.
- **Motion capture and photogrammetry.** Multi-camera rigs calibrated with a wand or a board, so that all cameras share one frame.

## References
