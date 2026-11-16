---
tag: CP9B6Z
kind: algorithm
slug: position-based-visual-servoing
name: Position-based visual servoing
aliases:
- PBVS
area: robotics/grasping-and-manipulation
level: core
summary: Estimates the target pose from the image and controls the camera by the pose error in Cartesian space.
model: real-ram
complexity:
  vars: {k: "the number of image features used by the pose estimator; the bounds are for one control step after the pose estimate"}
  time: {per_step: O(1)}
  space: {extra: O(1)}
properties: {deterministic: true, online: true, exact: false}
history:
  year: 1996
  people: [Seth Hutchinson, Gregory D. Hager, Peter I. Corke]
  note: Position-based control appeared in the 1980s work of Weiss and Sanderson; the 1996 tutorial of Hutchinson, Hager and Corke set it beside image-based control as one of the two basic schemes.
prereqs: [perspective-n-point, so3-logarithm-map, rigid-body-twist]
see_also: [image-based-visual-servoing, interaction-matrix, camera-calibration, axis-angle-representation, se3-exponential-map, resolved-rate-motion-control, homography, lyapunov-stability]
sources:
  - paper: doi:10.1109/70.538972
    title: Seth Hutchinson, Gregory D. Hager and Peter I. Corke, A tutorial on visual servo control, IEEE Transactions on Robotics and Automation 12(5), 1996
    locator: pages 651 to 670
  - paper: doi:10.1109/MRA.2006.250573
    title: Francois Chaumette and Seth Hutchinson, Visual servo control, Part I, Basic approaches, IEEE Robotics and Automation Magazine 13(4), 2006
    locator: pages 82 to 90
  - paper: doi:10.1007/BFb0109663
    title: Francois Chaumette, Potential problems of stability and convergence in image-based and position-based visual servoing, in The Confluence of Vision and Control, Lecture Notes in Control and Information Sciences 237, Springer, 1998
    locator: pages 66 to 78
  - book: isbn:9781119523994
    title: Mark W. Spong, Seth Hutchinson and M. Vidyasagar, Robot Modeling and Control, second edition, Wiley, 2020
    locator: Chapter 11 (vision-based control)
  - book: isbn:9783319325507
    title: Bruno Siciliano and Oussama Khatib (editors), Springer Handbook of Robotics, second edition, Springer, 2016
    locator: Chapter 34 (Visual Servoing, by Francois Chaumette, Seth Hutchinson and Peter Corke)
---

Position-based visual servoing (PBVS) uses the camera as a pose sensor. At each step it estimates the pose of the target in the camera frame from the image, for example by [perspective-n-point](/perspective-n-point/) with a calibrated camera and a model of the target. From this estimate and the desired pose of the target in the camera frame, it computes the pose of the current camera in the desired camera frame, and it drives this pose error to zero with a Cartesian control law. With the error written as a translation $t$ and an axis-angle rotation $\theta u$, the law $v = -\lambda R^T t$, $\omega = -\lambda\theta u$ moves the camera center on a straight line and turns it about a fixed axis. The quality of the result depends on the pose estimate: errors in the calibration or in the target model move the final pose.

## In plain words

Instead of looking at how the target moves in the image, you first work out where the target is in 3D, relative to the camera. You know where it should be when you reach the goal. The difference tells you how far, and in which direction, the camera must move and turn. You move and turn the camera a fixed fraction of that difference per second, so you approach the goal smoothly along a straight line and turn about one fixed axis.

The image is used only to find the target pose. If that pose is wrong, you stop at the wrong place and never notice, because you trust the estimate.

## The problem

A calibrated camera on a robot accepts a twist $V = (\omega, v)$, angular part first, in the camera frame. A pose estimator returns $\hat T_{ct}$, the pose of the target in the current camera frame. The task gives $T_{c^*t}$, the pose of the target in the desired camera frame. Find $V$ at each step so that the camera reaches the desired pose, that is, $E = T_{c^*t}T_{ct}^{-1} \to I$.

## The algorithm

Each control step takes the pose estimate and returns a twist.

```pseudo id=main
PBVS-STEP(T̂_ct, T_c*t, λ)
L1  E ← T_c*t T̂_ct⁻¹                ▷ the current camera in the desired camera frame
L2  (R, t) ← rotation and translation of E
L3  θu ← log(R)
L4  v ← -λ Rᵀ t
L5  ω ← -λ θu
L6  return V = (ω, v)
```

Line L3 is the [SO(3) logarithm](/so3-logarithm-map/), which returns the [axis-angle](/axis-angle-representation/) vector with $\theta \in [0, \pi]$. Line L4 expresses the translation error in the current camera frame, because the twist is a camera-frame velocity. The pose estimate comes from outside the step, usually from PnP on the same image features that IBVS would use.

## Example

The target is 1 m in front of the desired camera, so $T_{c^*t}$ is a pure translation by $(0, 0, 1)$. The camera starts rotated by $\pi/2$ about its optical axis and displaced by $t = (0.2, 0.1, -0.3)$ m in the desired camera frame. Then $R^T t = (0.1, -0.2, -0.3)$, and with $\lambda = 1$ lines L4 and L5 give

$$V = (0, 0, -\pi/2,\ -0.1, 0.2, 0.3).$$

Applying each twist for 10 ms gives:

| time (s) | camera center in the desired frame (m) | angle left (rad) |
|---|---|---|
| 0 | (0.200, 0.100, -0.300) | 1.571 |
| 0.5 | (0.121, 0.061, -0.182) | 0.950 |
| 1 | (0.073, 0.037, -0.110) | 0.575 |
| 2 | (0.027, 0.014, -0.040) | 0.211 |
| 3 | (0.010, 0.005, -0.015) | 0.077 |

The angle shrinks exactly by the factor $0.99^{100 t}$, close to $e^{-t}$, and the center shrinks by almost the same factor, so it stays within 0.5 mm of the line toward the goal. For the same quarter turn without the displacement, the camera only rotates, while [IBVS](/image-based-visual-servoing/) first moves 0.42 m back.

Now let the estimator be biased: it reports the target turned by 0.02 rad about the camera $y$ axis and shifted by 1 cm. The loop converges as before, but to a camera pose 1 cm away from the goal and tilted by 0.02 rad about $y$: the final error is the bias itself, moved to the desired camera frame. The image at the end does not match the reference image, and the controller cannot see this.

## Correctness

The error pose obeys $\dot E = E[V]$, so $\dot t = Rv = -\lambda t$ and $\dot R = R[\omega]$. Hence $t(\tau) = e^{-\lambda\tau}t(0)$, and the rotation keeps its axis while $\theta(\tau) = e^{-\lambda\tau}\theta(0)$. With an exact estimate the goal is reached from every start with $\theta < \pi$, with no local minima. With sampling and a held twist, the angle is exactly $(1 - \lambda h)^k\theta_0$ and the translation leaves the straight line by $O(h)$. If the estimator returns $T_{ct}B$ with a fixed error $B$, the same argument applies to the estimated error, so the true target pose $T_{ct}$ converges to $T_{c^*t}B^{-1}$, not to $T_{c^*t}$. The proofs are in the proof file.

## Complexity

In the [real-RAM](/real-ram/) model, one step of lines L1 to L6 is a fixed number of $4 \times 4$ products, one inverse and one logarithm: $O(1)$ time and memory. The pose estimate dominates the cost: PnP on $k$ points costs $O(k)$ for a linear method, times the number of iterations for an iterative refinement.

## Properties

- **Straight camera path.** With an exact estimate, the camera center moves on a straight line and the rotation keeps a fixed axis, so the 3D motion is the shortest and most predictable one.
- **Global convergence in pose.** No local minima and no singularities in the law itself, unlike IBVS. A half turn about the optical axis is a pure rotation.
- **Needs a model and a calibration.** The pose estimate needs the intrinsic parameters, a 3D model of the target and, for an arm, the hand-eye transform. Errors in any of these move the final pose.
- **Image not controlled.** The features follow whatever paths the 3D motion gives them, and they can leave the field of view.
- **Noise sensitivity.** Pose estimates from a small or distant target are noisy, especially in depth and in rotations about axes in the image plane, and the noise goes straight into the control.

## Variants and improvements

- **Other error choices.** Use the pose of the target in the camera frame as the feature. Then the origin of the target frame moves on a straight line in the image, which helps to keep it in view, but the camera path is no longer straight.
- **Pose from a homography.** For a planar target, a [homography](/homography/) between the current and the reference image gives the rotation and the scaled translation without a full 3D model.
- **2.5D visual servoing.** Control the rotation from a partial pose estimate and the translation from image coordinates and a depth ratio, which keeps one point in view and needs no 3D model.
- **Filtering.** Run a Kalman filter on the pose estimate to reduce noise and to bridge frames where the estimator fails.
- **Switching with IBVS.** Use PBVS far from the goal and IBVS near it, or switch when features approach the image border.

## When to use it

Use it when a calibrated camera and a model of the target are available, when the motion is large, and when the camera path in space matters, for example to avoid obstacles or the workspace limits. For final precision with an uncertain calibration, finish with [IBVS](/image-based-visual-servoing/), which stops where the image equals the reference image.

## Pitfalls

- **Biased pose estimates.** A small error in the calibration or the model gives a fixed error in the final pose, which no gain removes.
- **Losing the target.** If the target leaves the image, the estimator fails and the loop has no input. Watch the projected features and limit the rotation.
- **Rotation near pi.** The logarithm is not unique at $\theta = \pi$ and changes axis there; noise can make the axis jump between two choices.
- **Frame of the translation.** The translation error is in the desired frame; using it without $R^T$ as a camera-frame velocity gives a curved path or divergence for large rotations.
- **Depth noise.** Monocular pose estimates are weakest along the optical axis; do not use a high gain on $v_z$ with a small target.

## Implementations

## History

Weiss and Sanderson used the terms position-based and image-based for the two ways to close a visual loop in the 1980s. The 1996 tutorial of Hutchinson, Hager and Corke presented PBVS and IBVS side by side. In 1998, Chaumette compared their stability problems: PBVS has no local minima in the law but depends on the pose estimate and does not control the image. In 1999, Malis, Chaumette and Boudet proposed 2.5D visual servoing, which combines both. The 2006 tutorial of Chaumette and Hutchinson gives the law with the error $(t, \theta u)$ used here.

## References
