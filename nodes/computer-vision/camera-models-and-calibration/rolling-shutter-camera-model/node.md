---
tag: H7207T
kind: model
slug: rolling-shutter-camera-model
name: Rolling shutter camera model
aliases:
- rolling shutter projection
area: computer-vision/camera-models-and-calibration
level: advanced
summary: "A camera that exposes its rows one after another, so each row has its own pose, and moving scenes or cameras bend straight lines."
prereqs: [pinhole-camera-model, camera-extrinsic-parameters]
see_also: [generalized-camera-model, angular-velocity, b-spline, bundle-adjustment, visual-odometry, perspective-n-point, fixed-point-iteration, image-warping]
sources:
  - paper: arxiv:cs/0503076
    title: Marci Meingast, Christopher Geyer and Shankar Sastry, Geometric models of rolling-shutter cameras, Workshop on Omnidirectional Vision (OMNIVIS), 2005
    locator: the projection model with a row dependent pose, and the special cases of constant translation and rotation
  - paper: doi:10.1007/11744047_5
    title: Omar Ait-Aider, Nicolas Andreff, Jean-Marc Lavest and Philippe Martinet, Simultaneous object pose and velocity computation using a single view from a rolling shutter camera, European Conference on Computer Vision, 2006, 56-68
    locator: the estimation of the pose and the velocity of a known object from one rolling shutter image
---

Most CMOS image sensors do not expose all pixels at the same moment. They read the rows one after another, from top to bottom, and each row collects light over its own short time window. If the camera or the scene moves during the readout, each row sees the scene from a slightly different pose. The rolling shutter model adds this to the [pinhole camera](/pinhole-camera-model/): the pose is a function of time, and the time is a function of the row. A moving camera then bends straight lines, slants vertical edges, and makes spinning objects look warped. A camera that exposes all rows at once has a global shutter, and it is the special case where the row time is zero. Visual odometry, SLAM and [bundle adjustment](/bundle-adjustment/) on phone and drone cameras need the model when the camera moves fast.

## The machine

**Input.** A point $X_w$ of the world, the [intrinsic matrix](/camera-intrinsic-matrix/) $K$, the line delay $\tau$ (the time between the starts of two neighbor rows), the start time $t_0$ of the frame, and the camera trajectory $t \mapsto (R(t), T(t))$, the [extrinsic parameters](/camera-extrinsic-parameters/) as functions of time.

**Row time.** Row $v$ is exposed at time $t(v) = t_0 + \tau v$. A sensor with $H$ rows and a readout time $t_r$ has $\tau = t_r / H$.

**Projection.** The image point $(u, v)$ of $X_w$ is a solution of
$$\lambda \, (u, \; v, \; 1)^{\mathsf T} = K \big( R(t(v)) \, X_w + T(t(v)) \big), \qquad \lambda > 0 .$$
The row $v$ appears on both sides, so projection is an equation for $v$, not a formula. Write $v = g(v)$, where $g(v)$ is the row of the pinhole projection with the pose at time $t(v)$.

**Trajectory models.**
- Constant velocity in the frame: $R(t) = \exp([\omega]_\times (t - t_0)) R_0$ and $T(t) = T_0 + w \, (t - t_0)$, with the [angular velocity](/angular-velocity/) $\omega$ and the linear velocity $w$. This adds 6 unknowns per frame.
- Small rotation: replace the exponential by $I + [\omega]_\times (t - t_0)$. Then each coordinate of the camera point is affine in $v$, and $v \cdot Z_c(v) = c_y Z_c(v) + f_y Y_c(v)$ (with no skew) is a quadratic equation in $v$.
- Continuous trajectories: a [B-spline](/b-spline/) in the pose, used over many frames in continuous time SLAM and calibration.

**Solving for the row.** [Fixed point iteration](/fixed-point-iteration/) $v \leftarrow g(v)$, started at the global shutter row, converges when $\lvert g'(v) \rvert < 1$. Here $g'(v) = \tau \cdot \dot v$, where $\dot v$ is the vertical speed of the image point in rows per second, so the factor is the number of rows the point moves during one row time. For normal motion this is far below 1, and 2 or 3 steps are enough.

## What it counts

The model predicts where each point appears, given the trajectory over the frame, and it predicts the time of each measurement. Estimation fits the poses and the velocities, and sometimes $\tau$, by minimizing the [reprojection error](/reprojection-error/). Since each row has its own pose, a rolling shutter image is a [generalized camera](/generalized-camera-model/) image: the rays of different rows do not meet in one point when the camera translates.

**Worked example.** Let $f = 500$, $(c_x, c_y) = (320, 240)$, 480 rows read in 15 ms, so $\tau = 31.25$ microseconds. The camera moves sideways along its $x$ axis at 2 m/s, and a vertical pole stands 2 m in front of it, at $X = 0$ at time 0. At the time $\tau v$ of row $v$, the pole is at $X_c = -2 \tau v$ in the camera frame, so
$$u = 320 + 500 \cdot \frac{-2 \tau v}{2} = 320 - 0.015625 \, v .$$
The pole appears at $u = 320$ in row 0, 316.25 in row 240, and 312.52 in row 479. So the straight vertical pole is imaged as a line that leans by 7.5 pixels over the height of the frame. A global shutter camera would show it vertical at $u = 320$. In this example the point moves only horizontally, so $v$ does not depend on time and no iteration is needed.

## Relation to other models

- **Pinhole.** $\tau = 0$, or a camera at rest. Then every row has the same pose.
- **Generalized camera.** With a translating camera, the rows are rays from different centers, so the image is a [generalized camera](/generalized-camera-model/) image. Meingast, Geyer and Sastry (2005) studied this geometry for simple motions; for constant translation the rays meet two lines, a crossed slits camera.
- **Pure rotation.** If the camera only rotates (a hand held camera, a distant scene), row $v$ maps to the global shutter image by the homography $K R(t(v)) R(t_0)^{\mathsf T} K^{-1}$. Correction is then an [image warp](/image-warping/) with one homography per row, and it needs no depth.
- **Exposure time.** The model treats each row as exposed at one instant. Motion blur within a row comes from the exposure time, which is a different effect.

## Known results in the model

- **Pose and velocity from one view (theorem).** Ait-Aider et al. (2006) showed that one rolling shutter image of a known object gives both its pose and its velocity relative to the camera, because the rows sample the motion at different times. A global shutter image gives only the pose. The velocity is observable only if the motion changes the image during the readout.
- **Row equation (theorem).** Under constant velocity and the small rotation model, the row of a point is a root of a quadratic, as derived above; with translation only and no rotation it is linear. With the exact rotation it is a nonlinear equation, solved by iteration.
- **Bias without the model (heuristic and benchmark).** Pose estimation, [perspective-n-point](/perspective-n-point/) and bundle adjustment that assume a global shutter give biased results when a rolling shutter camera moves fast. The size of the bias depends on the speed and on $\tau$; published comparisons on phone and drone data show clear gains from the model in such cases.
- **Line delay.** $\tau$ is a property of the sensor and its mode, and is often not in the data sheet. It is calibrated with a known motion or a light that flashes at a known rate, or estimated together with the trajectory.
