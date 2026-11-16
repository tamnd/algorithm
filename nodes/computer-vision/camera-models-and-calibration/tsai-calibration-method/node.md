---
tag: 0E3W2B
kind: algorithm
slug: tsai-calibration-method
name: Tsai's calibration method
aliases:
- Tsai two-stage calibration
- radial alignment constraint calibration
area: computer-vision/camera-models-and-calibration
level: advanced
summary: Calibrate in two stages, first the rotation, T_x, T_y and the x scale factor by the radial alignment constraint, which radial distortion does not affect, then f, T_z and the distortion.
solves: [camera-calibration]
model: floating-point-model
complexity:
  vars: {n: the number of world to image point pairs, T: the number of Levenberg-Marquardt iterations}
  time: {worst: O(T n), average: O(T n), best: O(n)}
  space: {extra: O(n)}
properties: {deterministic: true, exact: false, online: false, recursive: false}
history:
  year: 1987
  people: [Roger Y. Tsai]
  note: Tsai presented the method at CVPR in 1986 and in the IEEE Journal of Robotics and Automation in 1987. It was among the first methods to model lens distortion with a linear start that needs no guess, and it was widely used in machine vision metrology.
prereqs: [camera-calibration, camera-extrinsic-parameters, least-squares-problem]
see_also: [zhang-calibration-method, dlt-camera-resectioning, brown-conrady-distortion-model, division-distortion-model, levenberg-marquardt, camera-intrinsic-matrix, singular-value-decomposition, perspective-n-point]
sources:
  - paper: doi:10.1109/JRA.1987.1087109
    title: Roger Y. Tsai, A versatile camera calibration technique for high-accuracy 3D machine vision metrology using off-the-shelf TV cameras and lenses, IEEE Journal on Robotics and Automation 3(4), 1987, 323-344
    locator: the camera model with radial distortion, the radial alignment constraint, the two stage method for coplanar and for non-coplanar points, and the sign rule for T_y
  - paper: doi:10.1109/CVPR.1997.609468
    title: Janne Heikkila and Olli Silven, A four-step camera calibration procedure with implicit image correction, Proceedings of the IEEE Conference on Computer Vision and Pattern Recognition, 1997, 1106-1112
    locator: the discussion of earlier methods, including the two stage method, and a full nonlinear fit as an alternative
  - book: isbn:9780521540513
    title: Richard Hartley and Andrew Zisserman, Multiple View Geometry in Computer Vision, second edition, Cambridge University Press, 2004
    locator: Section 7.4, Radial distortion (the radial distortion model and its estimation together with the camera)
---

Tsai's method calibrates a camera from one image of known 3D points, with a model that includes radial lens distortion. Its key idea is the radial alignment constraint: radial distortion moves a point only along the line from the principal point, so the direction of each image point from the principal point does not depend on the distortion, the focal length or the depth $T_z$. The first stage uses this to get the rotation, $T_x$, $T_y$ and the scale factor $s_x$ of the x axis from a linear system. The second stage gets $f$ and $T_z$ from another linear system, then fits $f$, $T_z$ and the distortion coefficient $\kappa_1$ by nonlinear least squares. Among the close pages, [camera calibration](/camera-calibration/) states the problem; [DLT resectioning](/dlt-camera-resectioning/) also uses a 3D target, but has no distortion and does not need the principal point; [camera matrix decomposition](/camera-matrix-decomposition/) splits a $3 \times 4$ matrix; and [Zhang's method](/zhang-calibration-method/) uses several views of a plane.

## In plain words

A lens bends straight lines, but it bends them in a simple way: each point moves straight toward or away from the center of the image. So the direction of a point from the center stays correct, even if its distance is wrong. Tsai's method uses only those directions first. From them it finds how the camera is turned and how it is shifted sideways and up or down, with simple equations. The distances from the center, which the lens has changed, are used only after that, to find the focal length, how far away the camera is, and how strong the lens bending is. Splitting the work this way means that the hard nonlinear part has only three unknowns.

## The problem

**Input.** World points $X_i \in \mathbb{R}^3$, $i = 1, \dots, n$, with $n \ge 7$ and not all on one plane; their pixels $(u_i, v_i)$; and the principal point $(c_x, c_y)$, which is known (Tsai takes the center of the image).

**Camera model.** With $(x_c, y_c, z_c) = R X + T$ and $T = (T_x, T_y, T_z)$, in units of pixels along the y axis:
$$X_u = f \frac{x_c}{z_c}, \quad Y_u = f \frac{y_c}{z_c}, \quad X_u = X_d (1 + \kappa_1 r_d^2), \quad Y_u = Y_d (1 + \kappa_1 r_d^2), \quad r_d^2 = X_d^2 + Y_d^2,$$
$$u = c_x + s_x X_d, \qquad v = c_y + Y_d.$$
So the focal lengths are $f$ along y and $s_x f$ along x, and the skew is 0. As in Tsai's paper, the distortion maps the distorted point $(X_d, Y_d)$ to the undistorted one. This is the opposite direction from the [Brown-Conrady model](/brown-conrady-distortion-model/) used by OpenCV, so a $\kappa_1$ from this model is not a $k_1$ of OpenCV.

**Output.** $R$, $T$, $f$, $s_x$ and $\kappa_1$.

## The algorithm

Write $x'_i = u_i - c_x = s_x X_{d,i}$ and $y'_i = v_i - c_y = Y_{d,i}$. The distortion factor $1 + \kappa_1 r_d^2$ is the same for $X_d$ and $Y_d$, so $X_d / Y_d = x_c / y_c$; this is the radial alignment constraint. With $r_1, r_2, r_3$ the rows of $R$, it reads $x'_i (r_2 \cdot X_i + T_y) = s_x\, y'_i (r_1 \cdot X_i + T_x)$. Dividing by $T_y$ gives one linear equation per point in seven unknowns:
$$\begin{pmatrix} y'_i X_i^{\mathsf T} & y'_i & -x'_i X_i^{\mathsf T} \end{pmatrix} a = x'_i, \qquad a = \Big(\frac{s_x r_1}{T_y}, \frac{s_x T_x}{T_y}, \frac{r_2}{T_y}\Big).$$
Neither $f$, nor $T_z$, nor $\kappa_1$ appears.

```pseudo id=main
TSAI-CALIBRATE(X_1..X_n, (u_i, v_i), c_x, c_y)
L1  x'_i <- u_i - c_x ; y'_i <- v_i - c_y
L2  a <- least squares solution of the n equations (y'_i X_i, y'_i, -x'_i X_i) . a = x'_i
L3  |T_y| <- 1 / |(a_5, a_6, a_7)| ; s_x <- |T_y| |(a_1, a_2, a_3)|
L4  T_y <- |T_y| ; r_1 <- T_y (a_1, a_2, a_3) / s_x ; r_2 <- T_y (a_5, a_6, a_7) ; T_x <- T_y a_4 / s_x
L5  if, at the point farthest from the center, x_c or y_c has the other sign than x' or y' then negate T_y, T_x, r_1, r_2
L6  r_3 <- r_1 × r_2 ; R <- nearest rotation to the matrix with rows r_1, r_2, r_3
L7  (f, T_z) <- least squares on f y_i - y'_i T_z = y'_i w_i, with y_i = r_2 . X_i + T_y and w_i = r_3 . X_i
L8  (f, T_z, kappa_1) <- Levenberg-Marquardt on the y residuals, from (f, T_z, 0)
L9  return R, (T_x, T_y, T_z), f, s_x, kappa_1
```

Lines L3 and L4 use $\|r_2\| = \|r_1\| = 1$: the last three entries of $a$ are $r_2 / T_y$, so their norm is $1 / |T_y|$, and the first three are $s_x r_1 / T_y$, so their norm is $s_x / |T_y|$. Line L5 fixes the sign of $T_y$: with $f > 0$, $s_x > 0$ and $1 + \kappa_1 r_d^2 > 0$, a point and its image lie on the same side of the center, so $x_c$ has the sign of $x'$ and $y_c$ the sign of $y'$. A point far from the center makes this test robust to noise. Line L7 ignores the distortion and uses only the y coordinate, so that $s_x$ does not enter; from $Y_d (w_i + T_z) = f y_i$ it is linear in $(f, T_z)$. Line L8 minimizes $\sum_i (Y_{d,i} (1 + \kappa_1 r_{d,i}^2) - f y_i / (w_i + T_z))^2$, which has only three unknowns.

## Example

The reference tests use $f = 800$, $s_x = 1.02$, $\kappa_1 = 8 \cdot 10^{-7}$, principal point $(320, 240)$, the rotation $R_0 = R_x(0.3) R_y(-0.2) R_z(0.1)$, $T = (0.2, 0.6, 5)$, and 40 random points in the cube $[-1, 1]^3$. The farthest image point is $258.9$ pixels from the center, where the distortion moves it by $\kappa_1 r_d^3 \approx 13.9$ pixels.

| step | result |
|---|---|
| L2 to L6 | $T_x = 0.2$, $T_y = 0.6$, $s_x = 1.02$ to 15 digits, and $\|R - R_0\|_F = 4 \cdot 10^{-16}$, although the pixels are distorted |
| L7 | $f = 788.55$ and $T_z = 5.0845$: the distortion biases the linear stage by 1.4% |
| L8 | the cost falls from 111.6 to $9.8 \cdot 10^{-26}$ in 8 accepted steps |
| L9 | $f = 800$, $T_z = 5$, $\kappa_1 = 8 \cdot 10^{-7}$, to at least 13 digits |

With pixel noise of $\sigma = 0.1$ on 60 points, over 5 random scenes, the relative error of $f$ was between 0.02% and 0.15%, and that of $\kappa_1$ between 0.13% and 0.9%.

## Correctness

With exact data, the radial alignment constraint holds for the true parameters whatever $f$, $T_z$ and $\kappa_1$ are, so the true $a$ solves the system of line L2. If the $n \times 7$ matrix has full rank, which needs points not on one plane and $T_y \ne 0$, the least squares solution is that $a$, and lines L3 and L4 recover $|T_y|$, $s_x$, $r_1$, $r_2$ and $T_x$ up to the common sign of $T_y$. Line L5 picks the right sign, and line L6 gives $R$ exactly. Without distortion, line L7 gives $f$ and $T_z$ exactly. Line L8 accepts only steps that lower the cost. The full proof is in the proof file below.

## Complexity

Lines L1 and L4 to L6 are $O(n)$ or $O(1)$. Line L2 is a least squares problem with $n$ rows and 7 columns, which costs $O(n)$ by an SVD or by the normal equations. Line L7 is $O(n)$. Each Levenberg-Marquardt iteration in line L8 computes $n$ residuals and an $n \times 3$ analytic Jacobian, then solves a $3 \times 3$ system, so it costs $O(n)$, and $T$ iterations cost $O(T n)$. The extra space is $O(n)$ for the two linear systems and the Jacobian. The best case, $O(n)$, is when the refinement stops after a constant number of steps, or is skipped.

## Properties

- **Distortion does not affect stage one.** The rotation, $T_x$, $T_y$ and $s_x$ are exact on exact data for any $\kappa_1$, as the tests check.
- **Small nonlinear part.** Only three parameters go into the nonlinear fit, so it is fast and has a good start.
- **Needs the principal point.** The constraint is about directions from the principal point, so an error in $(c_x, c_y)$ biases every parameter. Tsai uses the center of the image.
- **Not maximum likelihood.** Stage one fixes the rotation and $T_x$, $T_y$ before the distortion is known, and the final fit uses only the y residuals. So the result is not the minimizer of the full reprojection error.
- **One image.** A single image of a 3D target is enough.

## Variants and improvements

- **Coplanar points.** For points on the plane $Z = 0$, Tsai's paper gives a version with 5 unknowns in stage one. It needs $s_x$ to be known, since it cannot be separated from the other parameters for a plane.
- **Full refinement.** Use the result as the start of a [Levenberg-Marquardt](/levenberg-marquardt/) fit of all parameters, including the principal point and more distortion terms, on the full reprojection error. Heikkila and Silven (1997) follow this scheme with a DLT start and radial and tangential distortion.
- **Several images.** Use several images of the target, sharing the intrinsics, which helps to fix the principal point.
- **Other distortion models.** The first stage holds for any purely radial distortion about the principal point, including the [division model](/division-distortion-model/) and higher order terms.

## When to use it

Use Tsai's method when you have a precise 3D target, or a plane moved by a known amount, and a lens with clear radial distortion, and you want a start that needs no guess. Today, most users take [Zhang's method](/zhang-calibration-method/) with a flat pattern, which also estimates the principal point. Tsai's radial alignment constraint is still useful whenever a method must not depend on an unknown radial distortion, for example to get a pose from a camera with an unknown lens.

## Pitfalls

- **$T_y$ near zero.** The equations of line L2 divide by $T_y$, so they fail when the origin of the world frame lies near the plane $y_c = 0$ of the camera. Move the world origin, for example to a corner of the target that is not near the middle row of the image.
- **Coplanar points in the general form.** The $n \times 7$ system is rank deficient for coplanar points; the code raises an error. Use the coplanar variant with known $s_x$.
- **Points near the center.** Near the principal point, the direction of a point is poorly measured, and the sign test of line L5 can fail. Use points spread over the image, and the farthest point for the sign.
- **Wrong principal point.** An offset of a few pixels in $(c_x, c_y)$ breaks the constraint and biases the rotation. Do not use this method on cropped images or on cameras whose principal point is far from the center.
- **Mixing distortion conventions.** Tsai's $\kappa_1$ maps distorted to undistorted points. Using it as the $k_1$ of a model that maps undistorted to distorted points gives the wrong correction.
- **A negative $f$.** If the linear stage gives $f \le 0$, the sign of $T_y$ or the axis conventions are wrong; the code raises an error rather than return a mirrored camera.

## Implementations

## History

Roger Tsai presented the two stage method at the IEEE Conference on Computer Vision and Pattern Recognition in 1986, and the full paper appeared in the IEEE Journal on Robotics and Automation in 1987. It was aimed at 3D measurement with standard TV cameras and lenses, and it handled radial distortion with a linear start, which earlier methods either ignored or fitted by a nonlinear search from a guess. It was widely used in machine vision until plane based methods such as Zhang's (2000) became common.

## References
