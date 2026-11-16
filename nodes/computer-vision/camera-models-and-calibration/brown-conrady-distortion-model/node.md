---
tag: TS280K
kind: model
slug: brown-conrady-distortion-model
name: Brown-Conrady distortion model
aliases:
- radial and tangential distortion
- plumb bob model
area: computer-vision/camera-models-and-calibration
level: core
summary: "Lens distortion as even polynomials in the radius (radial terms k1, k2, k3) plus decentering terms p1, p2, applied to normalized image coordinates before K."
prereqs: [camera-intrinsic-matrix]
see_also: [division-distortion-model, kannala-brandt-fisheye-model, camera-calibration, zhang-calibration-method, tsai-calibration-method, newton-method-for-systems, fixed-point-iteration, image-warping]
sources:
  - paper: doi:10.1093/mnras/79.5.384
    title: A. E. Conrady, Decentred lens-systems, Monthly Notices of the Royal Astronomical Society 79(5), 1919, 384-390
    locator: the effect of a decentred lens element on the image, the origin of the tangential terms
  - paper: "Duane C. Brown, Decentering distortion of lenses, Photogrammetric Engineering 32(3), 1966, 444-462"
    title: Duane C. Brown, Decentering distortion of lenses, Photogrammetric Engineering 32(3), 1966, 444-462
    locator: the radial polynomial and the decentering terms of the model, derived from the Conrady analysis
  - paper: "Duane C. Brown, Close-range camera calibration, Photogrammetric Engineering 37(8), 1971, 855-866"
    title: Duane C. Brown, Close-range camera calibration, Photogrammetric Engineering 37(8), 1971, 855-866
    locator: the calibration of the distortion terms, including the plumb line method
  - book: isbn:9780521540513
    title: Richard Hartley and Andrew Zisserman, Multiple View Geometry in Computer Vision, second edition, Cambridge University Press, 2004
    locator: Section 7.4, Radial distortion (the radial model on normalized coordinates, its estimation, and correction by straight lines)
  - book: isbn:9783030343712
    title: Richard Szeliski, Computer Vision, Algorithms and Applications, second edition, Springer, 2022
    locator: Chapter 2, Image formation (the part on lens distortions)
---

The Brown-Conrady model describes how a real lens moves the image of a point away from where a [pinhole camera](/pinhole-camera-model/) would put it. It has two parts: a radial part, a polynomial in the squared distance from the optical axis, and a tangential or decentering part, which comes from lens elements that are not exactly centered. Lens distortion acts on normalized coordinates: project, distort, then apply $K$. In this form, with the parameters $(k_1, k_2, p_1, p_2, k_3)$, it is the default model of OpenCV and of most calibration tools, and it is what [Zhang's method](/zhang-calibration-method/) and the [camera calibration](/camera-calibration/) problem usually estimate. It suits normal and moderately wide lenses; fisheye lenses need the [Kannala-Brandt model](/kannala-brandt-fisheye-model/) or the [unified model](/unified-omnidirectional-camera-model/), and the [division model](/division-distortion-model/) is a one parameter alternative that is easier to invert.

## The machine

**Input.** A point $X_w$ of the world, the pose $(R, t)$, the [intrinsic matrix](/camera-intrinsic-matrix/) $K$, and the distortion parameters.

**Step 1: project.** $X_c = R X_w + t = (X, Y, Z)$ with $Z > 0$, and the normalized coordinates are $x = X / Z$, $y = Y / Z$. Let $r^2 = x^2 + y^2$.

**Step 2: distort.**
$$x_d = x \, (1 + k_1 r^2 + k_2 r^4 + k_3 r^6) + 2 p_1 x y + p_2 (r^2 + 2 x^2),$$
$$y_d = y \, (1 + k_1 r^2 + k_2 r^4 + k_3 r^6) + p_1 (r^2 + 2 y^2) + 2 p_2 x y.$$
The factor in parentheses is the radial part. It scales the point along the ray from the principal point. The terms with $p_1$ and $p_2$ are the decentering part; they also move the point at right angles to that ray.

**Step 3: apply K.** $u = f_x x_d + s \, y_d + c_x$ and $v = f_y y_d + c_y$.

**Parameters.**
- $k_1, k_2, k_3$: radial coefficients. With $k_1 < 0$ the image of a square bulges outward in the middle (barrel distortion, typical for wide lenses); with $k_1 > 0$ the corners stretch (pincushion, typical for telephoto lenses).
- $p_1, p_2$: decentering coefficients, usually small, of order $10^{-3}$.
- Extensions in OpenCV: the rational model multiplies by $(1 + k_1 r^2 + k_2 r^4 + k_3 r^6) / (1 + k_4 r^2 + k_5 r^4 + k_6 r^6)$, and the thin prism model adds $s_1 r^2 + s_2 r^4$ to $x_d$ and $s_3 r^2 + s_4 r^4$ to $y_d$. Tools differ in the order and the sign of $p_1$ and $p_2$, so check the convention before you copy values between tools.

**Domain.** The model is used where the radial map $r \mapsto r (1 + k_1 r^2 + k_2 r^4 + k_3 r^6)$ is increasing. Outside this range two rays map to the same pixel, and the fit has no meaning there. Since $r = \tan\theta$ for a ray at angle $\theta$ to the optical axis, the model can never reach $\theta = 90$ degrees.

**Inverse.** Undistortion maps a distorted point $(x_d, y_d)$, from $K^{-1} (u, v, 1)$, back to $(x, y)$. It has no closed form in general. Two methods are common:
- Fixed point iteration, as in OpenCV: start at $(x, y) = (x_d, y_d)$ and repeat $x \leftarrow (x_d - \delta_x(x, y)) / \rho(x, y)$ and $y \leftarrow (y_d - \delta_y(x, y)) / \rho(x, y)$, where $\rho$ is the radial factor and $\delta$ the decentering terms. This is [fixed point iteration](/fixed-point-iteration/). It converges when the distortion is mild, and it can fail near the edge of a strong wide lens.
- [Newton's method](/newton-method-for-systems/) on the $2 \times 2$ system, with the Jacobian of Step 2. It converges quadratically from a good start.

An undistorted image is made by the inverse warp: for each output pixel, apply the forward model to find where to read in the input, and interpolate (see [image warping](/image-warping/)). So making an undistorted image needs only the forward model.

## What it counts

The model predicts the pixel of each 3D point. Calibration chooses the parameters that minimize the sum of squared [reprojection errors](/reprojection-error/) over many points with known structure, usually by [Levenberg-Marquardt](/levenberg-marquardt/). The quantities to report are the RMS reprojection error in pixels and the spread of the parameters. The model is an empirical fit, not a law of optics: the polynomial has no physical meaning beyond the range of radii covered by the data, and higher terms can make it go wild outside that range. Brown (1971) also used the plumb line test: images of straight lines must be straight after undistortion, which needs no 3D target at all.

**Worked example.** Let $f_x = f_y = 800$, $s = 0$, $(c_x, c_y) = (320, 240)$, and $k_1 = -0.2$, $k_2 = 0.05$, $k_3 = 0$, $p_1 = 0.001$, $p_2 = -0.0005$. Take the normalized point $(x, y) = (0.4, 0.3)$, so $r^2 = 0.25$.
- Radial factor: $1 - 0.2 \cdot 0.25 + 0.05 \cdot 0.0625 = 0.953125$.
- Decentering: $\delta_x = 2 \cdot 0.001 \cdot 0.12 - 0.0005 \cdot (0.25 + 0.32) = -0.000045$ and $\delta_y = 0.001 \cdot (0.25 + 0.18) - 2 \cdot 0.0005 \cdot 0.12 = 0.00031$.
- Distorted: $x_d = 0.4 \cdot 0.953125 - 0.000045 = 0.381205$ and $y_d = 0.3 \cdot 0.953125 + 0.00031 = 0.2862475$.
- Pixels: the ideal pixel is $(640, 480)$, and the distorted pixel is $(624.964, 468.998)$, about 18.8 pixels closer to the principal point. This is barrel distortion.

Undistortion of $(0.381205, 0.2862475)$ by fixed point iteration gave errors (distance to $(0.4, 0.3)$) of $2.1 \cdot 10^{-3}$, $1.9 \cdot 10^{-4}$, $1.7 \cdot 10^{-5}$, $1.6 \cdot 10^{-6}$ after 1 to 4 steps, a linear rate with a factor of about 0.09. Newton's method gave $1.4 \cdot 10^{-4}$, $5.7 \cdot 10^{-9}$ and below $10^{-16}$ after 1 to 3 steps. A script computed these values.

## Relation to other models

- **Pinhole.** All parameters zero. The [pinhole model](/pinhole-camera-model/) and the [camera projection matrix](/camera-projection-matrix/) $P = K [R \mid t]$ describe Steps 1 and 3 only.
- **Tsai's model.** [Tsai's method](/tsai-calibration-method/) uses only the radial part, often only $k_1$, and the radial alignment constraint relies on this: radial distortion does not change the direction from the principal point.
- **Division model.** The [division model](/division-distortion-model/) writes the undistorted point as the distorted one divided by $1 + \lambda r_d^2$. It goes in the other direction, from distorted to undistorted, and with one parameter both directions have a closed form. With one parameter each, the two models agree to first order in $r^2$ with $\lambda \approx -k_1$, and they differ for wide lenses.
- **Fisheye models.** The [Kannala-Brandt model](/kannala-brandt-fisheye-model/) writes the image radius as an odd polynomial in the angle $\theta$, not in $\tan\theta$, so it can handle fields of view up to and beyond 180 degrees. The [unified model](/unified-omnidirectional-camera-model/) projects onto a sphere first. Mei and Rives add Brown-Conrady terms to the unified model.
- **Distortion in robotics and graphics.** The same polynomial is used to simulate lens effects in rendering, and as the default camera model of many SLAM systems for normal lenses.

## Known results in the model

- **Fold over.** With only $k_1 < 0$, the radial map $r \mapsto r + k_1 r^3$ has its maximum at $r^\ast = 1 / \sqrt{-3 k_1}$, with value $\tfrac{2}{3} r^\ast$. For $k_1 = -0.3$, $r^\ast \approx 1.0541$ (a ray at about 46.5 degrees from the axis) and the largest distorted radius is about $0.7027$. A distorted radius of $0.6$ then has two preimages, $0.7052$ and $1.3680$. Undistortion must pick the one below $r^\ast$, and a calibration with $k_1 = -0.3$ must not be used for rays beyond 46.5 degrees.
- **Degree of the inverse.** With radial terms only, undistortion is the root of a polynomial in $r$: degree 3 with $k_1$ alone (solvable by Cardano's formula), degree 5 with $k_2$, and degree 7 with $k_3$. With decentering terms, it is a $2 \times 2$ nonlinear system. In practice it is solved by iteration, not by a formula.
- **Straight lines.** A line through the principal point stays straight under the radial part, because radial distortion only moves points along rays from the principal point. Every other line bends. This is the basis of the plumb line method of Brown (1971).
- **Coupling with K.** The principal point and the decentering terms are strongly correlated in a fit: a small shift of $(c_x, c_y)$ looks like decentering distortion. So $p_1$ and $p_2$ are often fixed at 0 for good lenses.
- **Small distortion.** If the distortion is small, the inverse is close to the forward model with the opposite signs of $k_1$ and $p_i$, which is a common approximation for a first guess. This is an approximation, valid to first order only.
