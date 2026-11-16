---
tag: 4ZTNE5
kind: technique
slug: direct-image-alignment
name: Direct image alignment
aliases:
- direct method
- direct visual odometry
area: computer-vision/structure-from-motion
level: advanced
summary: Estimate camera motion by minimizing photometric error over raw pixel intensities rather than reprojection error of matched features.
prereqs: [photometric-error, lucas-kanade-method, gauss-newton-algorithm]
see_also: [inverse-compositional-alignment, kanade-lucas-tomasi-tracker, image-pyramid, direct-sparse-odometry, semi-direct-visual-odometry, iteratively-reweighted-least-squares, image-registration, visual-odometry]
sources:
  - paper: doi:10.1007/3-540-44480-7_18
    title: "Michal Irani and P. Anandan, About direct methods, Vision Algorithms: Theory and Practice, Lecture Notes in Computer Science 1883, Springer, 2000, 267-277"
    locator: "the definition of direct methods, which recover motion and structure from the image intensities without matched features, and their comparison with feature-based methods"
  - paper: doi:10.1023/B:VISI.0000011205.11775.fd
    title: "Simon Baker and Iain Matthews, Lucas-Kanade 20 years on: a unifying framework, International Journal of Computer Vision 56(3), 2004, 221-255"
    locator: "the forward additive, forward compositional and inverse compositional Gauss-Newton algorithms for image alignment and their cost per iteration"
  - paper: doi:10.1109/TPAMI.2017.2658577
    title: "Jakob Engel, Vladlen Koltun and Daniel Cremers, Direct sparse odometry, IEEE Transactions on Pattern Analysis and Machine Intelligence 40(3), 2018, 611-625"
    locator: "Section 3 (frame tracking by direct alignment on an image pyramid with a constant motion model)"
  - paper: doi:10.1109/ICRA.2014.6906584
    title: "Christian Forster, Matia Pizzoli and Davide Scaramuzza, SVO: Fast semi-direct monocular visual odometry, IEEE International Conference on Robotics and Automation (ICRA), 2014, 15-22"
    locator: "the sparse model-based image alignment of small patches around known 3D points, with the inverse compositional update"
  - book: isbn:9783030343712
    title: "Richard Szeliski, Computer Vision: Algorithms and Applications, second edition, Springer, 2022"
    locator: "Chapter 9, Motion estimation (translational and parametric alignment, hierarchical estimation)"
---

## In plain words

Take two pictures from a moving camera, and suppose you know how far away each pixel of the first picture is. For a guess of the camera motion you can say where each of those pixels must land in the second picture. If the guess is right, the brightness there is the same as in the first picture. So you change the guess, a little at a time, until the brightness values agree as well as possible. No corners are detected and nothing is matched first: the intensities themselves are the measurements. This works when the guess is already close, so the search starts on small, blurred copies of the pictures, where a large motion looks small.

## When it applies

- The motion between the two images is small, a few pixels at the finest level, or a good prediction is available (for example from a constant velocity model). The method is local.
- The brightness of a scene point is nearly the same in both images, or follows a known model such as an affine gain and offset.
- The pixels used have enough gradient. Flat regions give no information about the motion, and edges give information only across the edge.
- The depth of the pixels in the reference image is known or is estimated at the same time. For a rotation only, or for a planar scene, a homography or a rotation replaces the depth.
- The camera has a global shutter, little motion blur and, best, a known photometric calibration.

## The template

```pseudo id=main
DIRECT-ALIGN(reference I_ref with depths, target I, start ξ₀, levels L)
L1  build image pyramids of I_ref and I                          ▷ see image pyramid
L2  ξ ← ξ₀
L3  for level ℓ ← L - 1 down to 0 do
L4      repeat
L5          for each selected pixel u: r_u ← I(w(u; ξ)) - I_ref(u), J_u ← ∂r_u/∂ξ   ▷ hole: forward or inverse compositional
L6          H ← Σ w_u J_uᵀ J_u,  g ← Σ w_u J_uᵀ r_u                   ▷ hole: weights and robust loss
L7          δ ← solve H δ = -g;  ξ ← ξ ⊕ δ;  undo and stop if the cost went up
L8      until the step is small or the iteration limit is reached
L9  return ξ
```

The warp is $w(u; \xi) = \Pi(\exp(\xi)\, \Pi^{-1}(u, d_u))$ for a camera motion $\xi$ with 6 parameters and a depth $d_u$ per pixel, as in the [photometric error](/photometric-error/). By the chain rule, the Jacobian of one residual is

$$
J_u = \nabla I\big(w(u)\big)\, \frac{\partial \Pi}{\partial X}\, \frac{\partial X}{\partial \xi},
$$

the image gradient times the derivative of the projection times the derivative of the 3D point. The holes are the parametrization of the update (line L5), the weights and the robust loss (line L6), and the choice of pixels.

**Cost and convergence.** One iteration with $n$ pixels and $p$ parameters costs $O(n p^2 + p^3)$; for a camera motion $p = 6$ and the cost is $O(n)$. The inverse compositional form computes $J_u$ and $H$ on the reference image once per level, which saves the $O(n p^2)$ outer products in each iteration but leaves the $O(n)$ evaluation of the residuals. Gauss-Newton converges only locally (a theorem for smooth costs with full rank $H$: near a minimum with zero residuals the convergence is quadratic; with small residuals it is linear, and with large residuals the full steps can fail to converge). How far from the minimum it still converges depends on the image, not on the method: the linearization of the image holds within about the scale of its blur. The authors of DSO give a rule of thumb of 1 to 2 pixels at the finest level. This is a heuristic, and it is the reason for the pyramid.

**Example by hand.** A 1D camera with $f = 40$ looks at a wall at depth $z = 5$, and the reference image is $I_{ref}(u) = 3u$. The camera moves sideways by $t^*$, so every point moves by $f t^*/z = 8 t^*$ pixels, and the target image is $I(u) = I_{ref}(u - 8 t^*)$. For a guess $t$, the warp is $w(u) = u + 8t$ and the residual is $r(t) = I(u + 8t) - I_{ref}(u) = 3 \cdot 8 (t - t^*) = 24(t - t^*)$ for every pixel. The Jacobian is $J = 3 \cdot 8 = 24$: the image gradient times the derivative $f/z$ of the warp. From $t = 0$ with $t^* = 0.05$, each residual is $-1.2$, and the Gauss-Newton step is $-(\sum J r)/(\sum J^2) = 1.2/24 = 0.05$. One step reaches $t^*$ because the image is linear. With a real image the step is exact only to first order, and the iteration repeats.

## Classic examples

- **Lucas-Kanade (1981).** A 2D translation of a patch, found by Gauss-Newton on the sum of squared differences. See [Lucas-Kanade method](/lucas-kanade-method/) and, for feature tracking over a sequence, the [Kanade-Lucas-Tomasi tracker](/kanade-lucas-tomasi-tracker/).
- **Inverse compositional alignment (Baker and Matthews, 2004).** The same cost with the roles of the images swapped in the update, so that the Jacobian and $H$ are fixed. See [inverse compositional alignment](/inverse-compositional-alignment/).
- **Direct methods for camera motion (Irani and Anandan).** The camera motion and the structure are found from the intensities, with a parametric model of the motion field, instead of from matched features.
- **Dense and semi-dense visual odometry.** DTAM (Newcombe, Lovegrove and Davison, ICCV 2011) aligns against a dense depth map; LSD-SLAM (Engel, Schöps and Cremers, ECCV 2014) aligns all pixels with enough gradient against semi-dense depth maps of keyframes.
- **Sparse direct tracking.** [Direct sparse odometry](/direct-sparse-odometry/) tracks each frame against the newest keyframe with 8-pixel patterns around sparse points, with affine brightness terms. [Semi-direct visual odometry](/semi-direct-visual-odometry/) aligns $4 \times 4$ patches around map points with the inverse compositional update, and then refines with features.

## Variations

- **Which pixels.** All pixels (dense), all pixels with enough gradient (semi-dense), or a sparse set of points with small patterns (sparse). Fewer pixels cost less; pixels with no gradient add nothing but cost and noise.
- **Update.** Forward additive, forward compositional or inverse compositional; for camera poses the update is made on the Lie group, for example $T \leftarrow \exp(\delta)\, T$.
- **Brightness model.** Constant brightness, an affine gain and offset per image, or a full photometric calibration with response, vignetting and exposure time.
- **Robust loss.** Huber, Tukey or Student-t weights, applied by [iteratively reweighted least squares](/iteratively-reweighted-least-squares/), reduce the effect of occlusions, reflections and moving objects.
- **Joint estimation.** Only the pose (tracking), or poses and depths together, as in the window optimization of direct sparse odometry.
- **Other costs.** Normalized cross-correlation, census or learned features replace intensities when the brightness changes a lot.

## Pitfalls

- **Large motion.** If the start is more than about the blur scale away at the coarsest level, Gauss-Newton converges to a wrong minimum, often without any sign of failure. Use a pyramid, a motion prior, and a check of the final cost.
- **Brightness changes.** Auto exposure, vignetting and the camera response break brightness constancy. Model them or calibrate them.
- **Interpolation.** The residual uses interpolated values, and the Jacobian uses interpolated gradients. Bilinear interpolation of a grid is not the true image, so the minimum is slightly biased; the effect is largest for small or sharp textures.
- **Rolling shutter and blur.** One pose per image is a wrong model for a rolling shutter camera in fast motion, and blur removes the gradient the method needs.
- **Weak directions.** A narrow field of view makes a small rotation look like a sideways translation. The error then moves between the two, and $H$ is badly conditioned.
- **Depth errors.** Wrong depths give wrong warps. In tracking they bias the pose; in joint estimation they must be optimized too.

## Exercises

1. In the example, let the reference image be $I_{ref}(u) = u^2/10$ near $u = 20$. Compute the first Gauss-Newton step from $t = 0$ for one pixel at $u = 20$ with $t^* = 0.05$, and explain why it is not exact. (Answer: the target is $I(u) = (u - 0.4)^2/10$, so $r = 19.6^2/10 - 40 = -1.584$ and $J = (2 \cdot 19.6/10) \cdot 8 = 31.36$, using the gradient of the target at the warped point. The step is $1.584/31.36 = 0.05051$. It overshoots $0.05$ slightly because the image is curved over the motion; the next step corrects most of the error.)
2. A pixel lies on a vertical edge: its gradient is $(g, 0)$. Show that its residual gives no information about a vertical image motion. Which camera motions does such a pixel not constrain?
3. Count the cost of one iteration of the forward additive and of the inverse compositional algorithm for $n$ pixels and $p = 6$ parameters, and say which part of the work the inverse compositional form saves.

## References
