---
tag: EAJ63H
kind: problem
slug: visual-odometry
name: Visual odometry
aliases:
- VO
- camera egomotion estimation
area: computer-vision/structure-from-motion
level: core
summary: Estimate the motion of a camera over time from the images it takes, frame by frame and without building a global map.
prereqs: [relative-pose-problem, perspective-n-point, bundle-adjustment]
see_also: [slam-problem, structure-from-motion-problem, nister-visual-odometry, direct-sparse-odometry, semi-direct-visual-odometry, scale-drift, dead-reckoning, loop-closure-detection]
sources:
  - paper: doi:10.1109/MRA.2011.943233
    title: "Davide Scaramuzza and Friedrich Fraundorfer, Visual odometry, Part I: the first 30 years and fundamentals, IEEE Robotics and Automation Magazine 18(4), 2011, 80-92"
    locator: "the problem statement, the history, and the feature-based motion estimation from 2D to 2D, 3D to 2D and 3D to 3D correspondences"
  - paper: doi:10.1109/MRA.2012.2182810
    title: "Friedrich Fraundorfer and Davide Scaramuzza, Visual odometry, Part II: matching, robustness, optimization, and applications, IEEE Robotics and Automation Magazine 19(2), 2012, 78-90"
    locator: "feature matching, outlier removal, windowed bundle adjustment and pose graph optimization for visual odometry"
  - paper: "David Nister, Oleg Naroditsky and James Bergen, Visual odometry, Proceedings of the IEEE Conference on Computer Vision and Pattern Recognition (CVPR), vol. 1, 2004, 652-659"
    locator: "the paper that gave the problem its name, with a real-time system for monocular and stereo cameras"
  - paper: doi:10.1002/rob.20103
    title: "David Nister, Oleg Naroditsky and James Bergen, Visual odometry for ground vehicle applications, Journal of Field Robotics 23(1), 2006, 3-20"
    locator: "the extended system and its evaluation on ground vehicles"
  - book: isbn:9783030343712
    title: "Richard Szeliski, Computer Vision: Algorithms and Applications, second edition, Springer, 2022"
    locator: "Chapter 11, Structure from motion and SLAM"
---

## In plain words

A camera moves through the world and takes pictures, one after the other. Visual odometry finds where the camera is at each picture, using only the pictures. It works like counting steps: from each picture to the next it measures a small motion, and it adds the motions up to get the path. It does not try to recognize a place it saw long ago. So small errors add up, and the path slowly drifts away from the truth. With one camera there is one more problem: pictures cannot tell a small scene close by from a large scene far away, so the path has an unknown scale.

## Definition

**Input.** A sequence of images $I_0, I_1, \ldots, I_{N-1}$ from one camera (monocular) or from a rigid set of cameras (for example a stereo pair), with known intrinsics. Images arrive one at a time.

**Output.** A pose $T_k = (R_k, t_k)$ for each image, with $R_k \in SO(3)$ and $X_c = R_k X + t_k$ for a world point $X$. The first camera fixes the world frame: $T_0 = (I, 0)$. For an online method, $T_k$ must be given when $I_k$ arrives, from $I_0, \ldots, I_k$ only.

**Composition.** Most methods estimate a relative motion $T_{k,k-1} = (R, t)$ from frame $k-1$ to frame $k$ and set $T_k = T_{k,k-1}\, T_{k-1}$, that is $R_k = R R_{k-1}$ and $t_k = R t_{k-1} + t$. The camera center is $C_k = -R_k^{\mathsf T} t_k$.

**What can be observed.** With a monocular camera, images determine the poses and the scene only up to a similarity of the world: for any rotation, translation and scale $s > 0$ applied to the whole scene and all camera centers, the images are the same. Fixing $T_0$ removes 6 of the 7 degrees of freedom, so the scale remains (see [gauge freedom](/gauge-freedom/)). The answer of a monocular method is a path up to one global scale, and in practice the scale drifts along the path (see [scale drift](/scale-drift/)). With a calibrated stereo pair, the known baseline fixes the scale.

**Quality.** The usual measures are the absolute trajectory error (the root mean square distance between estimated and true camera centers after the best alignment by a rigid motion, or by a similarity for monocular methods) and the relative pose error over a fixed distance or time. Both are measures, not part of the problem statement.

## Variants

- **Monocular, stereo or several cameras.** One camera gives the path up to scale; a stereo rig gives metric scale from its baseline.
- **Feature-based or direct.** Feature-based methods detect and match points and minimize a reprojection error. Direct methods minimize the [photometric error](/photometric-error/) of the pixel intensities (see [direct image alignment](/direct-image-alignment/)).
- **Frame to frame or with a local map.** The simplest form estimates each relative motion on its own. Most systems keep a local map of 3D points and [keyframes](/keyframe-selection/) and refine it with [sliding window bundle adjustment](/sliding-window-bundle-adjustment/).
- **Visual-inertial odometry.** An inertial sensor adds measurements of acceleration and angular rate, which make the scale and the direction of gravity observable.
- **Visual SLAM.** If the method also detects when it returns to a known place and corrects the whole path, it solves the [SLAM problem](/slam-problem/) instead. See [loop closure detection](/loop-closure-detection/).

## Examples

**Composition by hand.** Let the first motion be a pure translation: $T_{1,0} = (I, (-1, 0, 0))$, so camera 1 has its center at $C_1 = (1, 0, 0)$. Let the second motion be a rotation by $90$ degrees about the vertical axis with no translation in the frame of camera 1, $T_{2,1} = (R_y, 0)$. Then $R_2 = R_y$ and $t_2 = R_y (-1, 0, 0)$. The center is $C_2 = -R_y^{\mathsf T} R_y (-1, 0, 0) = (1, 0, 0)$: the camera turned on the spot, as it should.

**The scale cannot be seen.** A point at $X = (0, 0, 5)$ seen from $C_0 = (0, 0, 0)$ and $C_1 = (1, 0, 0)$ with $R = I$ projects to the normalized image points $(0, 0)$ and $(-1/5, 0)$. The point $(0, 0, 10)$ seen from $(0, 0, 0)$ and $(2, 0, 0)$ gives $(0, 0)$ and $(-2/10, 0) = (-1/5, 0)$, the same images. So two images cannot tell whether the camera moved 1 or 2 units.

**Drift.** Suppose each relative heading has an independent error of standard deviation $\sigma$ radians and each step has length $d$. After $n$ steps the heading error is a sum of $n$ errors, with standard deviation $\sigma \sqrt{n}$. The sideways position error after $n$ steps is approximately $d \sum_{k=1}^{n} \theta_k$, where $\theta_k$ is the heading error at step $k$. Its variance is $d^2 \sigma^2 \sum_{k=1}^{n} k^2 \approx d^2 \sigma^2 n^3 / 3$, so its standard deviation grows like $n^{3/2}$. With $\sigma = 0.001$, $d = 1$ and $n = 1000$, this is about $0.001 \cdot 1000^{1.5}/\sqrt{3} = 18$ units over a path of 1000 units. This is a result for this small-angle model, not for all methods.

## Known algorithms

- **Feature-based, from relative pose.** [Nister visual odometry](/nister-visual-odometry/) matches corners, finds the relative pose of the first frames with the [five-point algorithm](/five-point-algorithm/) in [preemptive RANSAC](/preemptive-ransac/), and then tracks the camera with [P3P](/p3p/) against triangulated points.
- **Direct and sparse.** [Direct sparse odometry](/direct-sparse-odometry/) optimizes poses, inverse depths and brightness terms of a window of keyframes with the photometric error.
- **Semi-direct.** [Semi-direct visual odometry](/semi-direct-visual-odometry/) aligns small patches directly for the motion and then refines features, pose and points by reprojection error.
- **SLAM systems used as odometry.** [ORB-SLAM](/orb-slam/) tracks ORB features against a local map with local bundle adjustment; without its loop closure it is a visual odometry method.
- **Building blocks.** [RANSAC](/ransac/) with a [relative pose](/relative-pose-problem/) or [perspective-n-point](/perspective-n-point/) solver gives each motion; [bundle adjustment](/bundle-adjustment/) refines a window of poses and points.

## Bounds

- **Minimal data (theorem).** A calibrated relative pose has 5 degrees of freedom (rotation and the direction of translation), and five point matches in general position give a finite number of solutions, at most 10 essential matrices. A calibrated absolute pose from 3D points has 6 degrees of freedom, and three points give at most 4 solutions. So the per-frame minimal solvers need 5 or 3 points.
- **Scale (theorem).** For a monocular camera with no other sensor, no method can recover the global scale, because a similarity of the whole scene gives the same images. For the same reason, the scale ratio between parts of the path is observable only through the points that the parts share.
- **Error growth (heuristic).** Without loop closure, the error of the path is not bounded: it grows with the length of the path. Under the independent heading error model of the examples, the position error grows like $n^{3/2}$ in the number of steps; real errors are not independent, and windowed optimization reduces the constant, not the growth.
- **Cost.** An online method must process each frame in bounded time, so it optimizes only a bounded window of recent frames and points. The cost per frame does not grow with the length of the path.

## Reductions

- **To relative and absolute pose.** Frame-to-frame odometry is a chain of [relative pose problems](/relative-pose-problem/) (2D to 2D), or of [perspective-n-point](/perspective-n-point/) problems against triangulated points (3D to 2D), or of 3D to 3D alignments for a stereo camera. Composing the results gives the path.
- **To structure from motion.** Offline, visual odometry is the [structure from motion problem](/structure-from-motion-problem/) for an ordered sequence, and [bundle adjustment](/bundle-adjustment/) over all frames solves it to the best accuracy. Visual odometry restricts this to a window, for bounded cost.
- **From SLAM.** Visual SLAM is visual odometry plus place recognition and a global correction of the path. Removing the loop closures of a SLAM system leaves an odometry method.

## Applications

- **Ground vehicles and planetary rovers.** Visual odometry was used on the Mars Exploration Rovers to measure motion where wheels slip, and it is used on cars and ground robots as a complement to wheel odometry (see [dead reckoning](/dead-reckoning/)).
- **Drones.** Small aerial vehicles use fast monocular or visual-inertial odometry for flight control.
- **Augmented and virtual reality.** Head-mounted displays and phones track the camera with visual-inertial odometry to place virtual objects in the scene.
- **Mapping.** The path from odometry is the start for [bundle adjustment](/bundle-adjustment/) and for pose graph optimization in larger mapping systems.

## References
