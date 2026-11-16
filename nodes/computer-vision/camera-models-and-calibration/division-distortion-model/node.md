---
tag: WW5HWP
kind: model
slug: division-distortion-model
name: Division model of radial distortion
aliases:
- Fitzgibbon division model
area: computer-vision/camera-models-and-calibration
level: advanced
summary: "Radial distortion as x_u = x_d / (1 + lambda r_d^2). The undistorted point is linear in lambda, so minimal problems with distortion stay polynomial."
prereqs: [camera-intrinsic-matrix, homogeneous-coordinates]
see_also: [brown-conrady-distortion-model, unified-omnidirectional-camera-model, fundamental-matrix, generalized-eigenvalue-problem, minimal-solver, groebner-basis, camera-calibration, eight-point-algorithm]
sources:
  - paper: doi:10.1109/CVPR.2001.990465
    title: Andrew W. Fitzgibbon, Simultaneous linear estimation of multiple view geometry and lens distortion, IEEE Conference on Computer Vision and Pattern Recognition, 2001, volume 1, 125-132
    locator: the division model, and the estimation of the fundamental matrix and lambda together as a quadratic eigenvalue problem
  - paper: doi:10.1109/TPAMI.2011.86
    title: Zuzana Kukelova and Tomas Pajdla, A minimal solution to radial distortion autocalibration, IEEE Transactions on Pattern Analysis and Machine Intelligence 33(12), 2011, 2410-2422
    locator: the minimal problem of the fundamental matrix with one division parameter, solved with a Groebner basis solver
  - book: isbn:9780521540513
    title: Richard Hartley and Andrew Zisserman, Multiple View Geometry in Computer Vision, second edition, Cambridge University Press, 2004
    locator: Section 7.4, Radial distortion (the general radial correction function that the division model is one case of)
---

The division model describes radial lens distortion with one parameter $\lambda$, and it writes the map in the direction from the distorted image point to the undistorted one: $x_u = x_d / (1 + \lambda r_d^2)$. Fitzgibbon (2001) proposed it because, in [homogeneous coordinates](/homogeneous-coordinates/), the undistorted point is then linear in $\lambda$, so the distortion can be estimated together with a [fundamental matrix](/fundamental-matrix/) or a homography by linear algebra. Lens distortion acts on normalized coordinates: project, distort, then apply $K$. One parameter is enough for many lenses with moderate distortion, and both directions of the map have closed forms. For lenses with strong distortion or a wide field of view, the [Brown-Conrady model](/brown-conrady-distortion-model/) with more terms or a fisheye model gives a better fit.

## The machine

**Input.** A point of the world, the pose $(R, t)$, the [intrinsic matrix](/camera-intrinsic-matrix/) $K$, and the parameter $\lambda$.

**Step 1: project.** $X_c = R X_w + t$, and the undistorted normalized point is $x_u = (X / Z, Y / Z)$, with $r_u = \lVert x_u \rVert$.

**Step 2: distort.** The model is defined by its inverse:
$$x_u = \frac{x_d}{1 + \lambda r_d^2}, \qquad r_d = \lVert x_d \rVert .$$
So $x_d$ lies on the same ray from the center as $x_u$, and its radius solves $\lambda r_u r_d^2 - r_d + r_u = 0$. For $r_u > 0$ the root that tends to $r_d = r_u$ as $\lambda \to 0$ is
$$r_d = \frac{1 - \sqrt{1 - 4 \lambda r_u^2}}{2 \lambda r_u},$$
and $x_d = (r_d / r_u) \, x_u$. With $\lambda < 0$ (barrel distortion) the root is real for all $r_u$. With $\lambda > 0$ it is real only for $r_u \le 1 / (2 \sqrt{\lambda})$.

**Step 3: apply K.** $(u, v, 1)^{\mathsf T} = K (x_d, 1)^{\mathsf T}$.

**Homogeneous form.** Multiply the inverse map by $1 + \lambda r_d^2$:
$$\tilde x_u \sim (x_d, \; y_d, \; 1 + \lambda r_d^2)^{\mathsf T} = (x_d, \; y_d, \; 1)^{\mathsf T} + \lambda \, (0, \; 0, \; r_d^2)^{\mathsf T}.$$
This is the main property of the model: the lifted point is affine in $\lambda$, with coefficients that are known from the measured image point.

**Units and center.** Many papers use pixel coordinates measured from a center of distortion, often the image center, instead of normalized coordinates. Then $\lambda$ has the unit of one over a squared pixel, and $\lambda_{\text{pixel}} = \lambda_{\text{normalized}} / f^2$ for square pixels with focal length $f$. Check the convention before you use a published value.

## What it counts

The model predicts where a ray meets the image, like the [pinhole model](/pinhole-camera-model/), with one extra number. Estimation fits $\lambda$ together with $K$ and the poses in [camera calibration](/camera-calibration/), or together with two view geometry when the camera is not calibrated. The usual cost is the [reprojection error](/reprojection-error/) in the distorted image.

**Worked example.** Let $\lambda = -0.2$ and the distorted normalized point $x_d = (0.5, 0.25)$. Then $r_d^2 = 0.3125$ and $1 + \lambda r_d^2 = 0.9375$, so $x_u = (0.5333, 0.2667)$, farther from the center than $x_d$, as barrel distortion requires. In the other direction, $r_u^2 = 0.35556$, $\sqrt{1 - 4 \lambda r_u^2} = \sqrt{1.28444} = 1.13333$, and $r_d = (1 - 1.13333) / (2 \cdot (-0.2) \cdot 0.59628) = 0.55902 = \sqrt{0.3125}$, which gives $x_d$ back.

**Lines become circles.** A line $a x_u + b y_u + c = 0$ of the undistorted image becomes, after substitution and multiplication by $1 + \lambda r_d^2$,
$$c \lambda (x_d^2 + y_d^2) + a x_d + b y_d + c = 0,$$
which is a circle (or a line through the center if $c = 0$). For $\lambda = -0.2$ the line $x_u = 0.5$ becomes $x_d^2 + y_d^2 + 10 x_d - 5 = 0$, the circle $(x_d + 5)^2 + y_d^2 = 30$. The points $(0.4772, 0)$ and $(0.4142, 0.8284)$ lie on it, and both map to $x_u = 0.5$. So the plumb line method for this model fits circles to the images of straight edges, and three points on an edge fix one circle.

## Relation to other models

- **Pinhole.** $\lambda = 0$.
- **Brown-Conrady.** The [Brown-Conrady model](/brown-conrady-distortion-model/) goes from undistorted to distorted with a polynomial; the division model goes from distorted to undistorted with a rational function. With one parameter each, they agree to first order in $r^2$ with $\lambda \approx -k_1$. Neither one contains the other. A division model with more terms, $1 + \lambda_1 r_d^2 + \lambda_2 r_d^4 + \ldots$ in the denominator, is also used, but it loses the linear structure in the parameters for the extra terms in most problems.
- **Para-catadioptric camera.** The [unified model](/unified-omnidirectional-camera-model/) with $\xi = 1$ lifts a normalized image point $(x, y)$ to the ray $(2x, 2y, 1 - x^2 - y^2)$. With $x' = 2x$, $y' = 2y$ and $\lambda = -1/4$, the division lifting gives $(x', y', 1 - (x'^2 + y'^2)/4) = (2x, 2y, 1 - x^2 - y^2)$, the same ray. So a parabolic mirror with an orthographic camera is a division model with a fixed $\lambda$ in suitable units (theorem, checked by direct substitution). This explains why lines map to circles in both models.
- **Two view geometry.** For [fundamental matrix](/fundamental-matrix/) estimation the epipolar constraint becomes $(p' + \lambda z')^{\mathsf T} F (p + \lambda z) = 0$ with $p = (x_d, y_d, 1)$ and $z = (0, 0, r_d^2)$. This is quadratic in $\lambda$ and linear in the entries of $F$.

## Known results in the model

- **Quadratic eigenvalue problem (theorem).** Fitzgibbon (2001) writes the epipolar constraints of a set of matches, with the same $\lambda$ in both images, as $(D_1 + \lambda D_2 + \lambda^2 D_3) f = 0$, where $f$ is the vector of the 9 entries of $F$ and each row of $D_1, D_2, D_3$ comes from one match. With 9 matches the matrices are square. This is a quadratic eigenvalue problem, and the standard linearization turns it into a [generalized eigenvalue problem](/generalized-eigenvalue-problem/) of twice the size. With more matches it is solved in the least squares sense. The same idea applies to homographies.
- **Minimal problem (theorem).** $F$ has 7 degrees of freedom and $\lambda$ adds 1, so 8 matches are minimal. Kukelova and Pajdla (2011) solve this case with the rank constraint $\det F = 0$ by a [Groebner basis](/groebner-basis/) [minimal solver](/minimal-solver/). Minimal solvers of this kind go inside [RANSAC](/ransac/), which then finds the distortion and the outliers together.
- **Lines to circles (theorem).** As shown above, every straight line of the scene maps to a circle or to a line through the center of distortion. Circle fitting to straight edges gives $\lambda$ and the center without a calibration target.
- **Monotonicity.** With $\lambda < 0$ the distortion map is defined and one to one for every undistorted radius, and $r_d < 1 / \sqrt{-\lambda}$. With $\lambda > 0$ it is defined only up to a radius, and the model cannot describe a ray beyond it.
- **Quality of fit (heuristic and benchmark).** One division parameter often fits a lens with moderate distortion about as well as one or two Brown-Conrady terms. This is an empirical observation that depends on the lens and the field of view, not a theorem.
