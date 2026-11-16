---
tag: MRH7EA
kind: definition
slug: interaction-matrix
name: Visual servoing interaction matrix
aliases:
- image Jacobian
area: robotics/grasping-and-manipulation
level: core
summary: The matrix that maps the camera twist to the velocity of image features, the core of visual servoing.
prereqs: [rigid-body-twist, pinhole-camera-model]
see_also: [image-based-visual-servoing, position-based-visual-servoing, geometric-jacobian, optical-flow, image-moments, pseudoinverse, camera-calibration, kinematic-singularity]
sources:
  - paper: doi:10.1109/70.143350
    title: Bernard Espiau, Francois Chaumette and Patrick Rives, A new approach to visual servoing in robotics, IEEE Transactions on Robotics and Automation 8(3), 1992
    locator: pages 313 to 326
  - paper: doi:10.1109/70.538972
    title: Seth Hutchinson, Gregory D. Hager and Peter I. Corke, A tutorial on visual servo control, IEEE Transactions on Robotics and Automation 12(5), 1996
    locator: pages 651 to 670 (the image Jacobian)
  - paper: doi:10.1109/MRA.2006.250573
    title: Francois Chaumette and Seth Hutchinson, Visual servo control, Part I, Basic approaches, IEEE Robotics and Automation Magazine 13(4), 2006
    locator: pages 82 to 90 (the interaction matrix of a point and of a 3D pose)
  - book: isbn:9781119523994
    title: Mark W. Spong, Seth Hutchinson and M. Vidyasagar, Robot Modeling and Control, second edition, Wiley, 2020
    locator: Chapter 11 (vision-based control)
  - book: isbn:9783319325507
    title: Bruno Siciliano and Oussama Khatib (editors), Springer Handbook of Robotics, second edition, Springer, 2016
    locator: Chapter 34 (Visual Servoing, by Francois Chaumette, Seth Hutchinson and Peter Corke)
---

The interaction matrix $L_s$ of a set of visual features $s$ is the matrix that gives the time derivative of the features from the velocity of the camera: $\dot s = L_s V$, where $V$ is the camera [twist](/rigid-body-twist/). It plays the role for a camera that the [geometric Jacobian](/geometric-jacobian/) plays for an arm, and Hutchinson, Hager and Corke called it the image Jacobian. Every visual servoing law is built on it: [image-based visual servoing](/image-based-visual-servoing/) inverts it to turn an image error into a camera velocity. For an image point it depends on the image coordinates and on the depth of the point, which a single image does not measure.

## Definition

Let a camera move with the twist $V = (\omega, v)$, angular part first, expressed in the camera frame, and let it observe a fixed scene. Let $s \in \mathbb{R}^m$ be a vector of features computed from the image, which depends only on the camera pose $T$ relative to the scene. The **interaction matrix** of $s$ is the $m \times 6$ matrix $L_s$ with

$$\dot s = L_s V$$

for every motion of the camera. It is the derivative of $s(T\exp([\xi]))$ with respect to $\xi$ at $\xi = 0$.

For a point with camera coordinates $(X, Y, Z)$, $Z > 0$, and normalized image coordinates $x = X/Z$, $y = Y/Z$ of a [pinhole camera](/pinhole-camera-model/) with unit focal length, the feature is $s = (x, y)$ and

$$L_s = \begin{bmatrix} xy & -(1 + x^2) & y & -1/Z & 0 & x/Z \\ 1 + y^2 & -xy & -x & 0 & -1/Z & y/Z \end{bmatrix}.$$

This follows from $\dot P = -v - \omega \times P$ for a point fixed in the scene and $\dot x = \dot X/Z - x\dot Z/Z$, $\dot y = \dot Y/Z - y\dot Z/Z$. For $k$ points the interaction matrix is the $2k \times 6$ stack of the point matrices. Chaumette and Hutchinson order the twist as $(v, \omega)$, so their matrix has the last three columns above first.

For features in pixels, the first row is multiplied by $f_x$ and the second by $f_y$, the focal lengths in pixels, and $x$, $y$ are computed from the pixel coordinates. So the matrix needs the intrinsic parameters from [camera calibration](/camera-calibration/) as well as the depths.

## Examples and non-examples

- **Point on the optical axis.** At $x = y = 0$ the matrix is $\begin{bmatrix} 0 & -1 & 0 & -1/Z & 0 & 0 \\ 1 & 0 & 0 & 0 & -1/Z & 0 \end{bmatrix}$. A rotation $\omega_y$ and a translation $v_x = Z\omega_y$ give the same image motion, so one point cannot tell a pan from a sideways shift.
- **Depth.** For the point $(x, y) = (0.1, 0.1)$ at $Z = 1$ m, a forward speed $v_z = 1$ m/s moves the image point at $(0.1, 0.1)$ per second, away from the center. At $Z = 2$ m the same speed moves it at half that rate. The rotation columns do not depend on $Z$.
- **Rank.** One point gives a matrix of rank 2. Three points in general position give rank 6, so the camera twist is determined by their image velocities. Three collinear points give a rank below 6, and three points in general position also lose rank at some camera poses.
- **A 3D point as the feature.** If the feature is the point $P$ itself in the camera frame, then $\dot P = [P]\omega - v$, so $L_P = \begin{bmatrix} [P] & -I \end{bmatrix}$, with $[P]$ the skew matrix of $P$. It does not depend on any unknown.
- **Pose as the feature.** For PBVS with the error $(t, \theta u)$ of the current camera in the desired camera frame, $\dot t = Rv$ and the derivative of $\theta u$ depends only on $\omega$, so the matrix has two nonzero $3 \times 3$ blocks; the law of [position-based visual servoing](/position-based-visual-servoing/) inverts it in closed form.
- **Not the robot Jacobian.** The interaction matrix maps the camera twist, not the joint speeds, to $\dot s$. For a camera on an arm, the map from joint speeds is $L_s\,{}^{c}X_{e}\,J(q)$, with the twist transform from the end effector to the camera; some authors call this product the feature Jacobian.
- **Not optical flow.** [Optical flow](/optical-flow/) is the image velocity measured from intensities. The interaction matrix predicts it for known features from the camera motion; the two agree only where the flow is measured correctly.

## Related definitions

- [Geometric Jacobian](/geometric-jacobian/): the corresponding map from joint speeds to the twist of the end effector.
- [Rigid-body twist](/rigid-body-twist/): the velocity that the interaction matrix takes as input.
- [Image moments](/image-moments/): features whose interaction matrices decouple some degrees of freedom, used in place of points.
- [Kinematic singularity](/kinematic-singularity/): the analogue of the poses where the interaction matrix loses rank.
- [Pseudoinverse](/pseudoinverse/): how IBVS inverts a matrix that is not square.

## References
