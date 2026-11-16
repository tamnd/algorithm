---
tag: A4GWRN
kind: algorithm
slug: image-based-visual-servoing
name: Image-based visual servoing
aliases:
- IBVS
area: robotics/grasping-and-manipulation
level: core
summary: Moves the camera with a velocity from the pseudoinverse of the interaction matrix times the image feature error.
model: real-ram
complexity:
  vars: {k: "the number of point features; the bounds are for one control step"}
  time: {per_step: O(k)}
  space: {extra: O(k)}
properties: {deterministic: true, online: true, exact: false}
history:
  year: 1992
  people: [Bernard Espiau, Francois Chaumette, Patrick Rives]
  note: Espiau, Chaumette and Rives gave the task-function form with the interaction matrix; earlier work by Weiss and Sanderson in the 1980s had named image-based control.
prereqs: [interaction-matrix, pseudoinverse]
see_also: [position-based-visual-servoing, pinhole-camera-model, camera-calibration, perspective-n-point, resolved-rate-motion-control, rigid-body-twist, lyapunov-stability, gauss-newton-algorithm]
sources:
  - paper: doi:10.1109/70.143350
    title: Bernard Espiau, Francois Chaumette and Patrick Rives, A new approach to visual servoing in robotics, IEEE Transactions on Robotics and Automation 8(3), 1992
    locator: pages 313 to 326
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
    locator: Chapter 11 (vision-based control), Section 11.5 (image-based control laws)
  - book: isbn:9783319325507
    title: Bruno Siciliano and Oussama Khatib (editors), Springer Handbook of Robotics, second edition, Springer, 2016
    locator: Chapter 34 (Visual Servoing, by Francois Chaumette, Seth Hutchinson and Peter Corke)
---

Image-based visual servoing (IBVS) moves a camera so that features in its image, such as the image points of a few target corners, reach their positions in a reference image taken at the goal. The controller works directly on the image error $e = s - s^*$. It computes the camera velocity $V = -\lambda L^+ e$, where $L$ is the [interaction matrix](/interaction-matrix/) that maps camera velocity to feature velocity and $L^+$ is its [pseudoinverse](/pseudoinverse/). The method does not need a 3D model of the target or an estimate of its pose, and it is robust to errors in the camera calibration. It needs the depths of the points, or an estimate of them, and its camera path in 3D space is not controlled, so it can make large or useless motions.

## In plain words

You hold a camera and look at a target. You also have a photo taken from the place where you want to be. You compare the two images: each corner of the target should move from where it is now to where it is in the photo. The interaction matrix tells you how the corners move in the image when you move the camera. So you choose the camera motion that moves the corners straight toward their places, at a speed proportional to how far they still have to go.

Because you only look at the image, the camera can take odd paths. If the target is turned half a turn, the straight image paths all pass through the center, and the only motion that does that is to back away from the target.

## The problem

A calibrated camera is moved by a robot that accepts a camera twist $V = (\omega, v) \in \mathbb{R}^6$, angular part first, in the camera frame. It sees $k \ge 3$ points of a fixed target, with normalized image coordinates $s = (x_1, y_1, \dots, x_k, y_k)$ and depths $Z_i > 0$. The desired features $s^*$ are those seen at the goal pose. Find $V$ at each step so that $e = s - s^* \to 0$, which for enough points in general position means that the camera reaches the goal pose.

## The algorithm

Each control step reads the features and the depths, and returns a twist.

```pseudo id=main
IBVS-STEP(s, Z, s*, λ)
L1  e ← s - s*
L2  L ← stack over i of [[x_i y_i, -(1 + x_i²), y_i, -1/Z_i, 0, x_i/Z_i], [1 + y_i², -x_i y_i, -x_i, 0, -1/Z_i, y_i/Z_i]]
L3  L⁺ ← (Lᵀ L)⁻¹ Lᵀ
L4  V ← -λ L⁺ e
L5  return V
```

The robot applies $V$ for one sample time, the camera takes a new image, and the step repeats. Line L2 uses the current features and depths. Two other choices are common: the matrix $L^*$ at the goal, with the goal depths, which is constant and needs no depth estimate during the motion, and the mean $(L + L^*)/2$. The columns are ordered as $(\omega, v)$ here; Chaumette and Hutchinson order them as $(v, \omega)$. With exactly three points, $L$ is square and line L3 is the plain inverse.

## Example

Four points form a square of side 0.2 m, centered on the optical axis at a depth of 1 m in the goal pose, so $s^* = (\pm 0.1, \pm 0.1)$. The camera starts at the goal position, but rotated by $\pi/2$ about its optical axis. Each point now appears where its neighbor should be: the first point is seen at $(-0.1, 0.1)$ but should be at $(-0.1, -0.1)$, so its error is $(0, 0.2)$. With $Z = 1$, line L2 gives its two rows as $(-0.01, -1.01, 0.1, -1, 0, -0.1)$ and $(1.01, 0.01, 0.1, 0, -1, 0.1)$. With $\lambda = 1$, lines L3 and L4 give

$$V = (0, 0, -1, 0, 0, -1),$$

a rotation about the optical axis and a translation backward along it. As a check, the two rows times $V$ give $(0, -0.2)$, which is $-e$ for this point.

Applying each twist for 10 ms gives:

| time (s) | $\lVert e\rVert$ | angle left (rad) | distance moved back (m) |
|---|---|---|---|
| 0 | 0.400 | 1.571 | 0 |
| 0.5 | 0.243 | 0.995 | 0.387 |
| 1 | 0.147 | 0.524 | 0.371 |
| 2 | 0.054 | 0.153 | 0.143 |
| 5 | 0.0026 | 0.0066 | 0.0066 |

The camera moves back up to 0.419 m at $t = 0.69$ s and then returns. With the constant matrix $L^*$ instead, it first moves forward, up to 0.330 m toward the target, which is worse if the target is close. In both cases the error shrinks by about $e^{-\lambda t}$.

## Correctness

Under the law, $\dot e = LV = -\lambda L L^+ e$. The matrix $LL^+$ is the orthogonal projection onto the range of $L$, so $\frac{d}{dt}\tfrac12\lVert e\rVert^2 = -\lambda\lVert LL^+ e\rVert^2 \le 0$: the image error never grows. With three points the projection is the identity and $e$ decays exactly like $e^{-\lambda t}$. With more points the error can stop at $e \ne 0$ with $L^T e = 0$, a local minimum. Near the goal, the linearized loop in pose coordinates is $\dot\xi = -\lambda\xi$, so the goal is locally exponentially stable. For a rotation by $\theta$ about the optical axis with the target plane parallel to the image, the first twist is $\omega_z = -\lambda\sin\theta$ and $v_z = -\lambda Z(1 - \cos\theta)$. At $\theta = \pi$ the camera only moves back, and its depth becomes infinite in finite time. The proofs are in the proof file.

## Complexity

In the [real-RAM](/real-ram/) model, with $k$ points, line L2 builds a $2k \times 6$ matrix in $O(k)$ time. Line L3 forms $L^T L$ in $O(36 \cdot 2k)$ operations and inverts a $6 \times 6$ matrix in constant time, and line L4 is $O(k)$. So one step takes $O(k)$ time and $O(k)$ memory. In practice the image processing that finds and tracks the features costs far more than the control law.

## Properties

- **Image error decreases.** With exact depths, $\lVert e\rVert$ is nonincreasing along the continuous-time loop, and the features move on nearly straight lines in the image, which helps to keep them in view.
- **No pose estimate.** The law uses the features directly. Calibration errors change $L$ and so the path, but if the reference image was taken with the same camera, the loop still stops where the image equals the reference image.
- **Uncontrolled camera path.** The path in 3D space can be far from a straight line, and large rotations about the optical axis cause a retreat or an advance.
- **Local minima and singularities.** With four or more points, the loop can stop at a pose where $L^T e = 0$ but $e \ne 0$. $L$ loses rank for three collinear points, and for three points there are configurations where it is singular.
- **Local stability only.** The convergence results hold near the goal; global convergence is not guaranteed.

## Variants and improvements

- **Constant matrix $L^*$.** Compute $L$ once at the goal. It needs no depth estimate, but its region of convergence is smaller and it can drive the camera toward the target.
- **Mean matrix.** Use $(L + L^*)/2$, as proposed by Malis. For a rotation about the optical axis it gives a pure rotation, but it is singular at a half turn, and for the square of the example also at a quarter turn.
- **Depth estimation.** Estimate $Z_i$ online from the known camera motion, or use a constant guess such as $Z^*$.
- **Other features.** Use lines, image moments or cylindrical coordinates of points instead of Cartesian points; image moments decouple the rotation about the optical axis.
- **Hybrid and switching schemes.** 2.5D visual servoing (Malis, Chaumette and Boudet) controls the rotation from a partial pose estimate and the rest from the image; other schemes switch between IBVS and [PBVS](/position-based-visual-servoing/).
- **Eye-to-hand.** The camera is fixed and watches the end effector; the same law applies with the robot Jacobian between the twist and the joints.

## When to use it

Use it when the goal is given by a reference image rather than a pose, when the camera calibration or the target model is uncertain, and when the motion from the start to the goal is moderate: positioning a gripper above a part, docking, or tracking a moving target. For large rotations, or when the camera path in space must be controlled, use [position-based visual servoing](/position-based-visual-servoing/) or a hybrid scheme.

## Pitfalls

- **Depths.** The translation columns of $L$ scale with $1/Z_i$. A wrong depth changes the gain and the direction of the motion; a negative or zero depth estimate breaks the law.
- **Half turn about the optical axis.** The camera retreats to infinity. Plan a rotation first or use another feature set.
- **Features leave the image.** The law does not keep features in view. Add a constraint or a secondary task in the null space of $L$.
- **Too few or degenerate features.** Three points in general position give a square $L$ but several poses with the same image; four points avoid this but bring local minima. Collinear points make $L$ singular.
- **Gain and delay.** The image is slow and delayed; a large $\lambda$ with a slow camera makes the loop oscillate. Saturate the twist.

## Implementations

## History

Weiss, Sanderson and Neuman studied image-based control of robots in the 1980s. In 1992, Espiau, Chaumette and Rives wrote IBVS as the regulation of a task function with the interaction matrix, the form used today. Hutchinson, Hager and Corke wrote the 1996 tutorial that classified the methods into image-based and position-based. In 1998, Chaumette described the stability problems of both schemes, including the local minima of IBVS and the retreat for a rotation about the optical axis, and in 2006 Chaumette and Hutchinson wrote a two-part tutorial that is now the standard reference.

## References
