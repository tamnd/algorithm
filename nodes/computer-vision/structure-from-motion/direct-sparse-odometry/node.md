---
tag: YH2YPH
kind: algorithm
slug: direct-sparse-odometry
name: Direct sparse odometry
aliases:
- DSO
area: computer-vision/structure-from-motion
level: research
summary: "Track a camera by minimizing the photometric error of sparse high-gradient pixels, and optimize poses, inverse depths and affine brightness jointly over a window of keyframes."
solves: [visual-odometry]
model: real-ram
complexity:
  vars: {N: the number of frames, m: the number of points of the newest keyframe, n: the number of active points in the window, W: the number of keyframes in the window, L: the number of pyramid levels, k: the number of Gauss-Newton iterations, c: the number of candidate points, s: the number of steps of the depth search}
  time: {worst: O(N (L k m + c s + k n W^2 + k W^3)), average: O(N (L k m + c s + k n W^2 + k W^3)), best: O(N (L m + c s))}
  space: {extra: O(n W + W^2)}
properties: {deterministic: true, exact: false, online: true, iterative: true}
history:
  year: 2016
  people: [Jakob Engel, Vladlen Koltun, Daniel Cremers]
  note: "Engel, Koltun and Cremers put the preprint on arXiv in July 2016 (1607.02565); the journal paper is IEEE TPAMI 40(3), 2018."
prereqs: [direct-image-alignment, sliding-window-bundle-adjustment, photometric-error, visual-odometry]
see_also: [semi-direct-visual-odometry, nister-visual-odometry, keyframe-selection, scale-drift, schur-complement, huber-m-estimator, image-pyramid, gauss-newton-algorithm]
sources:
  - paper: doi:10.1109/TPAMI.2017.2658577
    title: "Jakob Engel, Vladlen Koltun and Daniel Cremers, Direct sparse odometry, IEEE Transactions on Pattern Analysis and Machine Intelligence 40(3), 2018, 611-625"
    locator: "Section 2 (the photometric model, the residual pattern, the weights and the windowed Gauss-Newton optimization with marginalization) and Section 3 (frame tracking, keyframe creation and marginalization, point selection and activation)"
  - paper: doi:10.1002/rob.20360
    title: "Gabe Sibley, Larry Matthies and Gaurav Sukhatme, Sliding window filters and their application to planetary landing, Journal of Field Robotics 27(5), 2010, 587-608"
    locator: "the sliding window filter, which removes old states from a window of states by marginalization with the Schur complement"
  - paper: doi:10.1023/B:VISI.0000011205.11775.fd
    title: "Simon Baker and Iain Matthews, Lucas-Kanade 20 years on: a unifying framework, International Journal of Computer Vision 56(3), 2004, 221-255"
    locator: "the Gauss-Newton image alignment that frame tracking uses"
---

Direct sparse odometry (DSO) is the [visual odometry](/visual-odometry/) method of Engel, Koltun and Cremers that works on pixel intensities instead of matched features. It uses a sparse set of pixels with a large gradient, and gives each pixel one inverse depth in the keyframe where it was first seen. The cost is the [photometric error](/photometric-error/) of small pixel patterns between keyframes, with an affine brightness change per frame. All poses, brightness terms and inverse depths of a small window of keyframes are optimized together by Gauss-Newton, and old keyframes leave the window by marginalization with the [Schur complement](/schur-complement/). New frames are tracked against the newest keyframe by [direct image alignment](/direct-image-alignment/). With one camera the result has an unknown scale, which the first depths fix.

## In plain words

A camera moves, and you want its path. You do not look for corners and match them. You pick pixels where the brightness changes fast, and you guess how far away each one is. If the guesses for the motion and the distances are right, each pixel has the same brightness in the next picture, up to a change of exposure. So you change the motion, the distances and two brightness numbers per picture until the brightness values agree as well as possible. You do this for a few recent key pictures at the same time. When a key picture gets old, you remove it, but you keep what it told you about the others as a summary.

## The problem

The input is a sequence of frames of a calibrated camera with pinhole intrinsics $(f_x, f_y, c_x, c_y)$, and the inverse depths of the points of the first frame (they fix the scale). A pose $T = (R, t)$ maps a world point into the camera, $X_c = R X + t$, and frame 0 is the world frame. The output is a pose and an affine brightness pair $(a, b)$ for each frame.

**Points and residuals.** A point $p$ lives in a host keyframe $i$ with an inverse depth $d_p$. For a pattern of 8 pixel offsets $o$ around $p$, each pattern pixel $q = p + o$ is moved into a target keyframe $j$ by

$$
q' = \Pi\big(R_{ji}\, \Pi^{-1}(q, d_p) + t_{ji}\big), \qquad (R_{ji}, t_{ji}) = T_j T_i^{-1},
$$

with $\Pi^{-1}(q, d) = \big((q_x - c_x)/(f_x d),\ (q_y - c_y)/(f_y d),\ 1/d\big)$. All 8 pixels share the same inverse depth. The residual is

$$
r_q = \big(I_j[q'] - b_j\big) - e^{a_j - a_i}\big(I_i[q] - b_i\big),
$$

and the energy of the window is

$$
E = \sum_{i} \sum_{p \in P_i} \sum_{j \ne i} \sum_{q} w_q\, \rho_k(r_q), \qquad w_q = \frac{c^2}{c^2 + |\nabla I_i(q)|^2},
$$

where $\rho_k$ is the Huber function with threshold $k$ (see [Huber M-estimator](/huber-m-estimator/)) and $w_q$ lowers the weight of pixels with a very large gradient. The paper also has the exposure times $t_i$ in the brightness factor and priors $\lambda_a a^2 + \lambda_b b^2$ on the affine terms; the code takes all exposure times as 1 and has no such priors.

## The algorithm

```pseudo id=main
DSO(frames F₀ … F_{N-1}, inverse depths of the points of F₀, window size W, threshold T_kf)
L1  keyframe 0 ← F₀ with pose (I, 0), a = b = 0, held fixed;  active points ← selected pixels of F₀ with their inverse depths, one depth held fixed
L2  for j ← 1 to N - 1 do
L3      (T_j, a_j, b_j) ← direct alignment of F_j against the newest keyframe, coarse to fine, from a constant motion guess
L4      for each candidate pixel of the newest keyframe do inverse depth ← search along the epipolar line in F_j, then Gauss-Newton on that depth
L5      if w_f f + w_ft f_t + w_a a ≤ T_kf then continue                     ▷ not a keyframe
L6      make the candidates with an inverse depth active points of the newest keyframe
L7      add F_j to the window as a keyframe with the pose and affine terms from L3
L8      build the Gauss-Newton system of E over all free poses, affine terms and inverse depths
L9      remove the inverse depths by the Schur complement, solve, back-substitute; keep the step only if E goes down; repeat up to the limit
L10     m ← the keyframe chosen by the marginalization rule, if any
L11     marginalize m and its points into the prior by the Schur complement; drop the residuals of other points in m
L12     select new candidate pixels in F_j
L13 return the poses and affine terms of all frames
```

**Tracking (L3).** For a new frame, the energy has only the residuals from the points of the newest keyframe into the new frame. The unknowns are the 6 pose parameters and $(a_j, b_j)$ of the new frame; the keyframe and the depths stay fixed. This is Gauss-Newton on an 8-parameter problem with the weights $w_q$ times the Huber weights, as in iteratively reweighted least squares. It runs from the coarsest level of an [image pyramid](/image-pyramid/) to the finest. The start is the last pose times the last motion (a constant velocity guess). The pose update is on the left: $R \leftarrow \exp([\omega]_\times) R$, $t \leftarrow \exp([\omega]_\times) t + v$.

**Candidates (L4, L6, L12).** Points are chosen by a gradient threshold per region: in each block the threshold is the median gradient of the block plus a constant $g_{th}$, and the strongest pixel above it is kept. Later passes use blocks of twice and four times the size and a lower threshold, so that some points are found in weak regions too. A candidate gets its inverse depth from a discrete search along the epipolar line in the new frame and a few Gauss-Newton steps on the depth alone.

**Keyframes (L5).** $f$ is the root mean square of the pixel shift of the points from the keyframe to the new frame, $f_t$ is the same shift with the rotation set to the identity, and $a = |a_j - a_i|$ measures the change in exposure. The paper uses this rule with weights that it chose; it is a heuristic (see [keyframe selection](/keyframe-selection/)).

**Window optimization (L8, L9).** Each residual depends on one inverse depth only, so the depth block of the Gauss-Newton matrix is diagonal. With the unknowns split into keyframe blocks $x_\alpha$ (8 per keyframe) and depths $x_\beta$,

$$
\begin{pmatrix} H_{\alpha\alpha} & H_{\alpha\beta} \\ H_{\beta\alpha} & H_{\beta\beta} \end{pmatrix} \begin{pmatrix} x_\alpha \\ x_\beta \end{pmatrix} = \begin{pmatrix} b_\alpha \\ b_\beta \end{pmatrix},
$$

the code solves $(H_{\alpha\alpha} - H_{\alpha\beta} H_{\beta\beta}^{-1} H_{\beta\alpha})\, x_\alpha = b_\alpha - H_{\alpha\beta} H_{\beta\beta}^{-1} b_\beta$ and then $x_\beta = H_{\beta\beta}^{-1}(b_\beta - H_{\beta\alpha} x_\alpha)$, the same structure as the [reduced camera system](/reduced-camera-system/) of bundle adjustment. A step is kept only if the energy goes down. The first keyframe (pose and affine terms) and one inverse depth are held fixed; they remove the 7 degrees of freedom of a similarity of the scene and the 2 of the brightness, see [gauge freedom](/gauge-freedom/).

**Marginalization (L10, L11).** The window keeps the two newest keyframes. A keyframe with less than 5 percent of its points visible in the newest frame leaves first. Otherwise, if the window is too large, the keyframe $i$ that maximizes $\sqrt{d(i, 1)} \sum_{j} (d(i, j) + \epsilon)^{-1}$ leaves, where $d$ is the distance between camera centers and keyframe 1 is the newest. This keeps keyframes spread out in space and close to the newest one; it is a heuristic. To remove keyframe $m$, the code drops the residuals of other points into $m$, builds the Gauss-Newton system, and takes the Schur complement over the block of $m$ and the depths of its points. The result $\hat H, \hat b$ is a quadratic prior $-\hat b^{\mathsf T} x + \frac{1}{2} x^{\mathsf T} \hat H x$ on the remaining keyframes, where $x$ is their change from the state at the time of marginalization.

**Differences from the paper.** The code leaves out the photometric calibration (response function and vignetting), the First Estimate Jacobians (the paper evaluates the Jacobians of variables connected to the prior at their linearization point, to keep the prior consistent), the outlier rules, the recovery after a tracking failure, the activation rule for candidates by their distance to other points, and the initialization from the first frames. A candidate is searched only in the frame just before the keyframe decision, not tracked over many frames. The 8 pattern offsets are this code's choice. The paper uses a window of 7 keyframes and about 2000 active points; the tests use 3 keyframes and about 50 points.

## Example

**One residual.** A pattern pixel has $I_i[q] = 100$ in its host, with $a_i = 0.1$, $b_i = 3$, and the target has $a_j = -0.2$, $b_j = 7$. The predicted target value is $7 + e^{-0.3}(100 - 3) = 7 + 0.740818 \cdot 97 = 78.859$. If the target image has $I_j[q'] = 80$, the residual is $r = 1.141$. With $|\nabla I_i(q)| = 30$ and $c = 50$, the weight is $2500 / 3400 = 0.7353$. With the Huber threshold $k = 9$ the residual is in the quadratic part, so its energy is $\frac{1}{2} \cdot 1.141^2 \cdot 0.7353 = 0.478$. A residual of 20 would cost $0.7353 \cdot 9 \cdot (20 - 4.5) = 102.6$ instead of $147.1$.

**Keyframe score.** Take a point at the principal point with inverse depth $0.2$ (depth 5), $f_x = 40$, and a new frame that moved $0.5$ sideways without rotation. The point moves $40 \cdot 0.5 / 5 = 4$ pixels, so $f = f_t = 4$. With $a_i = 0.1$ and $a_j = 0.4$, $a = 0.3$. With $w_f = 1$, $w_{ft} = 2$, $w_a = 10$ the score is $4 + 8 + 3 = 15$. For a pure rotation by $0.01$ radians about the vertical axis the shift is $40 \tan 0.01 = 0.4$ pixels for $f$ and 0 for $f_t$. The $f_t$ term grows only with translation, which is what makes new depths observable.

**A synthetic run.** The tests render a textured slanted plane at depth about 5 into $48 \times 36$ images with $f_x = f_y = 40$. The exact (analytic) images make every residual zero at the truth: from a start at the identity, tracking recovers a pose and $(a, b)$ within $10^{-6}$, and a window of three keyframes recovers poses and depths within $10^{-6}$ from a perturbed start, also after one keyframe is marginalized. On pixel grids, with 7 frames, 2 pyramid levels and a window of 3 keyframes, the largest rotation error was $0.49$ degrees and the largest position error $0.045$ on a path of length $0.75$. Bilinear sampling of the grid is not the true image, and a small rotation about the vertical axis looks like a sideways move, so the errors grow along the path. These numbers are one synthetic run, not a property of the method.

## Correctness

The full proof is in [proofs/correctness.md](proofs/correctness.md). It covers exact data: the images are exact images of the scene under the affine brightness model, and the pattern of each point lies on a plane parallel to its host image (so one inverse depth fits all 8 pixels). Under these assumptions it shows that the true state makes every residual zero and is a global minimizer of the tracking energy, of the window energy and of the window energy with the prior after any number of marginalizations; that the true state is a fixed point of every Gauss-Newton step; that the Schur steps solve the full linear system exactly; and that the window energy never goes up, because a step is kept only when it decreases the energy. It does not prove convergence from a far start. Gauss-Newton on the photometric error converges only locally, roughly within the range where the image is close to linear (the paper uses a rule of thumb of 1 to 2 pixels at the finest level), which is the reason for the pyramid and the constant motion guess.

## Complexity

All counts are in the [real RAM](/real-ram/). The pattern has 8 pixels, a constant.

- **Tracking.** One Gauss-Newton iteration at one level visits the $8m$ residuals of the newest keyframe, each with an $8 \times 8$ outer product, and solves an $8 \times 8$ system, so $O(m)$. With $L$ levels and at most $k$ iterations, $O(Lkm)$ per frame.
- **Candidates.** The depth search costs $O(s)$ per candidate, so $O(cs)$ per frame.
- **Window step.** A point has residuals into at most $W - 1$ keyframes, and each residual touches 17 unknowns, so building the system costs $O(nW)$. The Schur complement adds, for each point, an outer product of its column over at most $8W$ keyframe entries, so $O(nW^2)$. The reduced system is dense of size $8W$ and costs $O(W^3)$ to solve. One step costs $O(nW^2 + W^3)$; $k$ steps cost $O(k(nW^2 + W^3))$. This is a cost per iteration, not a convergence bound.
- **Marginalization.** The Schur complement over one keyframe and its points has the same form, $O(nW^2 + W^3)$ in a structured implementation. The code here stores the Gauss-Newton matrix densely and uses a dense solve for this step, which costs $O((n + W)^3)$; that is a simplification for clarity.
- **Space.** The structured form stores $O(nW)$ couplings between points and keyframes and the $O(W^2)$ reduced matrix and prior. The dense code uses $O((n + W)^2)$.

A frame that is not a keyframe costs only $O(Lkm + cs)$, and the window step runs once per keyframe.

## Properties

- **Deterministic.** There are no random samples. The result depends only on the input and the parameters.
- **Not exact.** Gauss-Newton converges only locally, and the result depends on the start, on the pyramid and on the image content.
- **Online.** Each frame costs a bounded amount of work for a fixed window and a fixed number of points.
- **Scale.** With one camera the scale is fixed by the first depths and carried by the window and the prior. It drifts over long paths; see [scale drift](/scale-drift/).
- **Photometric model.** The affine brightness terms absorb changes of exposure and gain. Without them, a change of exposure moves the energy minimum away from the true pose.
- **Sparse and direct.** It uses the intensities directly, with no descriptors, but only at sparse points, so the Gauss-Newton matrix has the same structure as in [bundle adjustment](/bundle-adjustment/).

## Variants and improvements

- **Photometric calibration.** The paper corrects the images with a known response function and vignetting map and uses the exposure times. Without them, more of the change has to go into $(a, b)$.
- **Stereo and inertial versions.** Later work by the same group adds a stereo camera (which gives metric scale) or an inertial sensor. These are separate systems.
- **Loop closure.** DSO is odometry and does not close loops. Systems built on it add a place recognition step and a pose graph; see [loop closure detection](/loop-closure-detection/).
- **Dense and semi-dense direct methods.** DTAM (Newcombe, Lovegrove and Davison, ICCV 2011) estimates a dense depth map; LSD-SLAM (Engel, Schöps and Cremers, ECCV 2014) uses all pixels with enough gradient and a pose graph. DSO is sparse, which makes the joint optimization of depths and poses affordable.
- **Semi-direct methods.** [Semi-direct visual odometry](/semi-direct-visual-odometry/) uses direct alignment only for tracking and refines the structure with reprojection errors.

## When to use it

Use DSO when the scene has little corner texture but many edges and smooth gradients, the camera has a global shutter, and you can calibrate the photometric response. Prefer a feature-based method such as [Nister visual odometry](/nister-visual-odometry/) or [ORB-SLAM](/orb-slam/) when the motion between frames is large, the exposure changes in ways the affine model does not fit, the camera has a rolling shutter, or you need relocalization and loop closure.

## Pitfalls

- **Large motion.** If the start of the tracking is more than a few pixels from the truth at the coarsest level, Gauss-Newton can converge to a wrong minimum. A higher frame rate or a better motion guess helps.
- **Gauge.** Without a fixed keyframe and a fixed scale, the Gauss-Newton matrix is singular. The code fixes the first keyframe and one depth; the prior keeps the gauge after that keyframe leaves.
- **Prior consistency.** If the Jacobians of the variables in the prior are later evaluated at a different point, the prior can gain information it does not have and the estimate becomes overconfident. The paper uses First Estimate Jacobians for this reason; the code does not.
- **Brightness gauge.** $(a, b)$ of one frame must be fixed, and a strong gain change with little contrast makes $a$ and $b$ nearly interchangeable.
- **Pattern depth.** All 8 pixels share one inverse depth. On a slanted surface close to the camera this is only an approximation.
- **Rolling shutter and motion blur.** The model assumes one pose per image. Both break that assumption.

## Implementations

## History

Direct methods track the camera by aligning image intensities, an idea that goes back to the work of Lucas and Kanade (1981) and was made into a theory for camera motion by Irani and Anandan (1999). DTAM (2011) and LSD-SLAM (2014) used dense and semi-dense depth maps. Engel, Koltun and Cremers published DSO as an arXiv preprint in July 2016 and in IEEE TPAMI in 2018. Its authors describe it as a fully direct model with a joint optimization of all parameters of a window of keyframes, including the affine brightness terms. Old keyframes leave by marginalization, in the manner of the sliding window filters of Sibley, Matthies and Sukhatme and the keyframe window of OKVIS (Leutenegger and others, 2015).

## References
