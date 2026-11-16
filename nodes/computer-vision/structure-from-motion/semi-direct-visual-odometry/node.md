---
tag: BR51JE
kind: algorithm
slug: semi-direct-visual-odometry
name: Semi-direct visual odometry
aliases:
- SVO
area: computer-vision/structure-from-motion
level: research
summary: "Track a camera by direct alignment of small patches around sparse map points, then refine the 2D features, the pose and the points by reprojection error."
solves: [visual-odometry]
model: real-ram
complexity:
  vars: {N: the number of frames, m: the number of visible map points, W: the number of keyframes, L: the number of pyramid levels, k: the number of Gauss-Newton iterations, c: the number of seeds, s: the number of steps of the epipolar search, P: the number of pixels of an image}
  time: {worst: O(N (L k m + k m W + c (s + k) + P)), average: O(N (L k m + k m W + c (s + k) + P)), best: O(N (L m + m W + c s + P))}
  space: {extra: O(N P + m W + c)}
properties: {deterministic: true, exact: false, online: true, iterative: true}
history:
  year: 2014
  people: [Christian Forster, Matia Pizzoli, Davide Scaramuzza]
  note: "Forster, Pizzoli and Scaramuzza presented SVO at ICRA 2014; an extended version for several cameras followed in IEEE Transactions on Robotics in 2017."
prereqs: [direct-image-alignment, visual-odometry, bundle-adjustment]
see_also: [direct-sparse-odometry, nister-visual-odometry, inverse-compositional-alignment, keyframe-selection, fast-corner-detector, shi-tomasi-corner-detector, homography-estimation, scale-drift]
sources:
  - paper: doi:10.1109/ICRA.2014.6906584
    title: "Christian Forster, Matia Pizzoli and Davide Scaramuzza, SVO: Fast semi-direct monocular visual odometry, IEEE International Conference on Robotics and Automation (ICRA), 2014, 15-22"
    locator: "the motion estimation (sparse model-based image alignment, feature alignment, pose and structure refinement) and the mapping with the depth filter"
  - paper: doi:10.1109/TRO.2016.2623335
    title: "Christian Forster, Zichao Zhang, Michael Gassner, Manuel Werlberger and Davide Scaramuzza, SVO: Semidirect visual odometry for monocular and multicamera systems, IEEE Transactions on Robotics 33(2), 2017, 249-265"
    locator: "the extended system for several cameras and other camera models"
  - paper: doi:10.1016/j.imavis.2011.01.006
    title: "George Vogiatzis and Carlos Hernandez, Video-based, real-time multi-view stereo, Image and Vision Computing 29(7), 2011, 434-441"
    locator: "the Gaussian times Beta depth filter and its moment-matching update"
  - paper: doi:10.1023/B:VISI.0000011205.11775.fd
    title: "Simon Baker and Iain Matthews, Lucas-Kanade 20 years on: a unifying framework, International Journal of Computer Vision 56(3), 2004, 221-255"
    locator: "the inverse compositional algorithm used by the sparse image alignment"
---

Semi-direct visual odometry (SVO) is the [visual odometry](/visual-odometry/) method of Forster, Pizzoli and Scaramuzza that mixes a direct step and a feature step. The direct step finds the motion of a new frame by aligning small patches around projected map points with the [photometric error](/photometric-error/), so it needs no feature matching. The feature step then moves each projected point a little in the image so that its patch matches a keyframe, and the pose and the points are refined with the reprojection error, as in [bundle adjustment](/bundle-adjustment/). New points come from a probabilistic depth filter on pixels of the keyframes. With one camera the scale is unknown and is fixed by the first depths.

## In plain words

A camera moves, and you have a small set of 3D points that you already know. For a new picture, you first guess the motion by moving the old picture's small squares around the points until they look like the new picture. That gives a good pose quickly. Then, for each point, you take its square from a keyframe that saw it from a similar angle, and you slide it a little in the new picture until it fits best. These new 2D positions are more precise than the projections, so you fix the pose and the points with them. New points start as guesses of distance with a large uncertainty. Each new picture narrows the guess, and when the guess is narrow enough the point joins the map.

## The problem

The input is a sequence of frames of a calibrated pinhole camera with intrinsics $(f_x, f_y, c_x, c_y)$, and the depths of some pixels of the first frame (the original system gets them from a homography between the first frames; here the caller gives them). A pose $T = (R, t)$ maps a world point into the camera, $X_c = R X + t$, and frame 0 is the world frame. The output is a pose for each frame and a sparse map of 3D points.

**Sparse image alignment.** Let $k-1$ be the previous frame with pose $T_{k-1}$. A map point $X$ projects to $u$ in it with depth $z$. The relative pose $T_{k,k-1}$ minimizes

$$
E(T_{k,k-1}) = \sum_{\text{points}} \sum_{o \in P_4} \Big(I_k\big(\Pi(T_{k,k-1}\, \Pi^{-1}(u + o, z))\big) - I_{k-1}(u + o)\Big)^2,
$$

where $P_4$ is the set of 16 offsets of a $4 \times 4$ patch and all pixels of a patch take the depth of its point.

**Feature alignment.** For a point seen in keyframe $r$ at $u_r$, the new 2D position $u'$ and an intensity offset $\beta$ minimize $\sum_{o \in P_8} \big(I_k(u' + A o) - I_r(u_r + o) - \beta\big)^2$ over an $8 \times 8$ patch, where $A$ is the $2 \times 2$ affine warp of the patch from keyframe $r$ to frame $k$.

**Depth filter.** A seed is a pixel of a keyframe with an unknown inverse depth $Z$ and an unknown inlier ratio $\pi$. A measurement $x$ with variance $\tau^2$ follows $\pi\, N(x \mid Z, \tau^2) + (1 - \pi)\, U(x)$, where $U$ is uniform over the range of inverse depths. The posterior is approximated by $N(Z \mid \mu, \sigma^2)\, \mathrm{Beta}(\pi \mid a, b)$, as in Vogiatzis and Hernandez.

## The algorithm

```pseudo id=main
SVO(frames F₀ … F_{N-1}, depths of selected pixels of F₀)
L1  keyframe 0 ← F₀ with pose (I, 0);  map ← the selected pixels of F₀ back-projected with their depths
L2  for k ← 1 to N - 1 do
L3      T_k ← sparse image alignment of 4 x 4 patches against F_{k-1}, inverse compositional, coarse to fine, then composed with T_{k-1}
L4      for each visible map point do u' ← feature alignment of an affinely warped 8 x 8 patch from the keyframe with the closest viewing direction
L5      T_k ← motion-only bundle adjustment on the reprojection errors of the positions u'
L6      for each aligned point do X ← structure-only bundle adjustment over its keyframe observations and u'
L7      for each seed do search along the epipolar line in F_k, update the depth filter, and move the seed to the map if σ is small
L8      if the distance from F_k to every keyframe > 0.12 x the mean scene depth then
L9          add F_k as a keyframe, drop the farthest keyframe if there are too many, and start new seeds in empty cells
L10 return T₀ … T_{N-1}
```

**Sparse image alignment (L3).** The unknown is the relative pose from the previous frame. The inverse compositional form of Baker and Matthews (see [inverse compositional alignment](/inverse-compositional-alignment/)) moves the reference point instead of the current one: the residual is $I_k(\Pi(T\, \exp(\xi)\, X)) - I_{k-1}(u)$, linearized at $\xi = 0$ on the reference side. Each patch pixel gives a Jacobian row $J = \nabla I_{k-1}(u)\, \frac{\partial \Pi}{\partial X}\, [\,-[X]_\times \mid I\,]$ of size $1 \times 6$, so a $4 \times 4$ patch gives a $16 \times 6$ block. These rows and $H = \sum J^{\mathsf T} J$ depend only on the reference image, so they are computed once per pyramid level. Each iteration solves $H \xi = \sum J^{\mathsf T} r$ and updates $T \leftarrow T \exp(\xi)^{-1}$. It runs from the coarsest level of an [image pyramid](/image-pyramid/) to a fine level, from the identity. The paper uses 5 levels and stops at level 3, because the next step refines each feature at full resolution anyway. The code keeps a step only if the mean squared residual goes down.

**Feature alignment (L4).** For each map point that projects into the frame, the code takes the keyframe that saw it from the closest viewing direction. The warp $A$ is the derivative of the exact warp from that keyframe to the new frame for a patch on a plane parallel to the keyframe image at the depth of the point. Gauss-Newton on $(u', \beta)$ then aligns the warped $8 \times 8$ patch with the new frame, a 2D [Lucas-Kanade](/lucas-kanade-method/) step. The new positions do not have to agree with one pose: the paper calls this a relaxation and notes that it breaks the epipolar constraints on purpose. The reprojection error that remains is what the next two steps reduce.

**Pose and structure refinement (L5, L6).** Motion-only bundle adjustment is Gauss-Newton on the 6 pose parameters with the reprojection errors $\Pi(R X + t) - u'$ and a left update $R \leftarrow \exp([\omega]_\times) R$, $t \leftarrow \exp([\omega]_\times) t + v$. Structure-only bundle adjustment is Gauss-Newton on each point alone, with all its observations. Both keep a step only if the cost goes down.

**Depth filter (L7).** For each seed, the code searches the inverse depths in $\mu \pm 2\sigma$ along the epipolar line, with the zero-mean sum of squared differences of an $8 \times 8$ patch. It refines the best position by feature alignment and triangulates the depth along the ray of the seed. The variance $\tau^2$ is the change of the inverse depth when the matched position moves by one pixel (a parameter) along the epipolar line. The update is the moment matching of Vogiatzis and Hernandez:

$$
C_1 \propto \frac{a}{a + b}\, N(x \mid \mu, \sigma^2 + \tau^2), \quad C_2 \propto \frac{b}{a + b}\, U(x), \quad C_1 + C_2 = 1,
$$

$$
s^2 = \Big(\frac{1}{\sigma^2} + \frac{1}{\tau^2}\Big)^{-1}, \quad m = s^2\Big(\frac{\mu}{\sigma^2} + \frac{x}{\tau^2}\Big), \quad \mu' = C_1 m + C_2 \mu, \quad \sigma'^2 = C_1 (s^2 + m^2) + C_2 (\sigma^2 + \mu^2) - \mu'^2,
$$

and $a', b'$ are chosen so that $\mathrm{Beta}(a', b')$ has the first two moments $f$ and $e$ of $\pi$ under the posterior: $a' = (e - f)/(f - e/f)$, $b' = a'(1 - f)/f$. A seed whose $\sigma$ is below a fraction of the range becomes a map point.

**Keyframes (L8, L9).** A frame becomes a keyframe when its camera center is farther than 12 percent of the mean scene depth from the centers of all keyframes. If there are too many keyframes, the one farthest from the new keyframe is removed. New seeds are placed in the cells of a grid that hold no point: in each cell, the pixel with the highest [Shi-Tomasi](/shi-tomasi-corner-detector/) score. The paper uses cells of $30 \times 30$ pixels and takes the [FAST](/fast-corner-detector/) corner with the highest Shi-Tomasi score in each cell. These rules are heuristics; see [keyframe selection](/keyframe-selection/).

**Differences from the paper.** The code leaves out the homography bootstrap, the FAST detector, the robust weights in the refinement steps, the separate mapping thread, edgelet features and the recovery after a tracking failure. The sparse alignment has no brightness offset. The parameters of the tests (cells of 8 pixels, a smaller convergence threshold, a smaller keyframe distance) fit $48 \times 36$ images and are not the paper's values.

## Example

**One depth filter update.** A seed has $\mu = 0.3$, an inverse depth range of $0.5$, so $\sigma^2 = 0.5^2/36 = 0.006944$, and $a = b = 10$. A measurement $x = 0.25$ arrives with $\tau = 0.02$. Then $\sigma^2 + \tau^2 = 0.007344$, and $N(0.25 \mid 0.3, 0.007344) = e^{-0.1702}/(0.08570 \cdot 2.5066) = 3.927$. So $C_1 \propto 0.5 \cdot 3.927 = 1.963$ and $C_2 \propto 0.5/0.5 = 1$, which give $C_1 = 0.6626$ and $C_2 = 0.3374$. The Gaussian part has $s^2 = 1/(144 + 2500) = 0.0003782$ and $m = 0.0003782 \cdot (43.2 + 625) = 0.2527$. The new mean is $\mu' = 0.6626 \cdot 0.2527 + 0.3374 \cdot 0.3 = 0.2687$, and the new standard deviation is $0.0556$ (it was $0.0833$). The inlier ratio $a/(a + b)$ goes from $0.5$ to $0.508$: the measurement is likely, but the prior is wide, so it is not certainly an inlier.

**Keyframe rule.** With a mean scene depth of 5, the threshold is $0.12 \cdot 5 = 0.6$. A frame at $(0.5, 0, 0)$ with keyframes at the origin and at $(1, 0, 0)$ is $0.5$ from both, so it is not a keyframe. A frame at $(0.5, 0.7, 0)$ is $0.86$ from both, so it is.

**One pixel in inverse depth.** For a sideways move of length $|t|$ and focal length $f$, a point at inverse depth $x$ moves $f |t| x$ pixels. So one pixel of error is $1/(f |t|)$ in inverse depth. With $f = 40$ and $|t| = 0.354$ this is $0.0707$: short baselines give poor depth, which is why a seed needs many frames.

**A synthetic run.** The tests render a textured slanted plane at depth about 5 into $48 \times 36$ pixel grids with $f_x = f_y = 40$, for 8 frames along a path of length $0.88$. The pipeline starts with 23 map points, makes keyframes 0, 2, 4 and 6, and turns 5 seeds into map points. The largest rotation error was $0.15$ degrees and the largest position error $0.011$. On exact (analytic) images, the sparse alignment recovers a relative pose within $10^{-6}$ and the feature alignment recovers a position within $10^{-6}$. These numbers are one synthetic run, not a property of the method.

## Correctness

The full proof is in [proofs/correctness.md](proofs/correctness.md). For exact images of a scene with known map points, it shows that the true relative pose makes every residual of the sparse alignment zero, so it is a global minimizer and a fixed point; that the true position is a fixed point of the feature alignment when the warp is exact; that the true pose and points are global minimizers and fixed points of the two refinement steps; and that every one of these steps never increases its cost, because a step is kept only when the cost goes down. It also proves that the depth filter update matches the mean and variance of $Z$ and the first two moments of $\pi$ under the exact one-step posterior (this is a theorem about the update, not about convergence of the filter), and that the triangulation along the ray is exact for noise-free bearings. Convergence from a far start is not proved: the direct alignment works only within a few pixels at the coarsest level.

## Complexity

All counts are in the [real RAM](/real-ram/). Patch sizes are constants.

- **Sparse alignment.** The setup of one level costs $O(m)$, and one iteration costs $O(m)$ for the residuals and a $6 \times 6$ solve. With $L$ levels and $k$ iterations, $O(Lkm)$ per frame. The inverse compositional form saves the recomputation of $J$ and $H$ in each iteration, not an order of growth.
- **Feature alignment.** Choosing the keyframe costs $O(W)$ per point and the alignment $O(k)$, so $O(m(W + k))$.
- **Refinement.** Motion-only bundle adjustment costs $O(km)$. Structure-only bundle adjustment costs $O(kW)$ per point, so $O(kmW)$.
- **Seeds.** One epipolar search costs $O(s)$ and the refinement $O(k)$, so $O(c(s + k))$.
- **Images.** Building the pyramid costs $O(P)$ per frame, and the Shi-Tomasi scores $O(P)$ per keyframe.

The cost per frame is $O(Lkm + kmW + c(s + k) + P)$. These are costs per iteration times an iteration limit, not a convergence bound. The code keeps all pyramids, which takes $O(NP)$ space; a real system keeps only those of the keyframes and the last frame.

## Properties

- **Deterministic.** There are no random samples.
- **Not exact.** All Gauss-Newton steps converge only locally, and the result depends on the start and the image content.
- **Online.** Each frame costs a bounded amount of work for a bounded map.
- **Fast.** The direct step uses few pixels and needs no descriptors or matching. The ICRA 2014 paper reports more than 300 frames per second on a laptop; this is a benchmark result for that implementation and hardware.
- **Scale.** With one camera the scale comes from the first depths and drifts over long paths; see [scale drift](/scale-drift/).
- **Outlier handling.** The depth filter models outliers with the inlier ratio $\pi$, so a seed that gets many bad measurements gets a low $a/(a + b)$ and can be dropped.

## Variants and improvements

- **Several cameras and other models.** The 2017 journal version handles several cameras, fisheye and catadioptric cameras, and adds edgelets for scenes with few corners.
- **Inertial data.** Later systems add an inertial sensor for metric scale and robustness.
- **Fully direct methods.** [Direct sparse odometry](/direct-sparse-odometry/) keeps the photometric error also in the window optimization and models brightness changes.
- **Feature-based methods.** [Nister visual odometry](/nister-visual-odometry/) and [ORB-SLAM](/orb-slam/) match features with descriptors and use [RANSAC](/ransac/); they tolerate larger motion between frames.

## When to use it

Use SVO when the frame rate is high, the motion between frames is small, the computer is small (an onboard computer of a drone was the original target), and the scene has texture. Prefer a feature-based method when the motion between frames is large or the brightness changes a lot, and a method with loop closure, such as [ORB-SLAM](/orb-slam/), when the camera returns to places it saw before.

## Pitfalls

- **Large motion.** The sparse alignment starts from the identity. If a frame moves by more than a few pixels at the coarsest level, it can converge to a wrong pose.
- **Brightness change.** The sparse alignment assumes constant brightness. A change of exposure biases the pose; the feature alignment has an offset $\beta$, but the first step does not in the basic form.
- **Seeds on edges.** On an edge parallel to the epipolar line, the search finds many equal minima. The filter then gets bad measurements and must reject them through $\pi$.
- **Depth of a patch.** All pixels of a patch take one depth, and the affine warp assumes a plane parallel to the keyframe image. On slanted surfaces close to the camera these are approximations.
- **Keyframe rule.** A fixed fraction of the mean depth gives few keyframes for a camera that only rotates, and new seeds then have no baseline.
- **Bootstrap.** The homography bootstrap assumes a mostly planar view of the first frames; see [homography estimation](/homography-estimation/).

## Implementations

## History

Feature-based visual odometry, such as the system of Nister, Naroditsky and Bergen (2004), matched corners and estimated the motion from the matches. Direct methods, such as DTAM (2011), aligned image intensities and were slow on small computers. Forster, Pizzoli and Scaramuzza combined the two at ICRA 2014: a direct sparse alignment for the motion, a feature step for precision, and the depth filter of Vogiatzis and Hernandez (2011) for new points, with the tracking and mapping split into two threads as in PTAM. The extended version of Forster, Zhang, Gassner, Werlberger and Scaramuzza in IEEE Transactions on Robotics (2017) added several cameras, other camera models and edgelets.

## References
