---
tag: 59RAGT
kind: model
slug: kannala-brandt-fisheye-model
name: Kannala-Brandt fisheye model
aliases:
- generic fisheye camera model
- equidistant fisheye model
area: computer-vision/camera-models-and-calibration
level: advanced
summary: "Model a fisheye lens by the image radius as an odd polynomial of the angle between the ray and the optical axis, which covers fields of view of 180 degrees and more."
prereqs: [camera-intrinsic-matrix, brown-conrady-distortion-model]
see_also: [unified-omnidirectional-camera-model, division-distortion-model, pinhole-camera-model, camera-calibration, newton-raphson-method, visual-odometry, direct-sparse-odometry, generalized-camera-model]
sources:
  - paper: doi:10.1109/TPAMI.2006.153
    title: Juho Kannala and Sami S. Brandt, A generic camera model and calibration method for conventional, wide-angle, and fish-eye lenses, IEEE Transactions on Pattern Analysis and Machine Intelligence 28(8), 2006, 1335-1340
    locator: the radially symmetric model r(theta) as an odd polynomial, the extra asymmetric terms, and the calibration from a planar target
  - paper: doi:10.1109/3DV.2018.00069
    title: Vladyslav Usenko, Nikolaus Demmel and Daniel Cremers, The double sphere camera model, International Conference on 3D Vision, 2018, 552-560
    locator: the comparison of the Kannala-Brandt, unified, extended unified and double sphere models on fisheye data, including the cost of projection and unprojection
  - book: isbn:9783030343712
    title: Richard Szeliski, Computer Vision, Algorithms and Applications, second edition, Springer, 2022
    locator: Chapter 2, Image formation (the part on lens distortions and fisheye lenses)
---

The Kannala-Brandt model describes a fisheye lens, or any central lens with a wide field of view, by one function: the distance $r$ of the image point from the principal point as an odd polynomial of the angle $\theta$ between the incoming ray and the optical axis. A [pinhole camera](/pinhole-camera-model/) has $r = f \tan\theta$, which goes to infinity at 90 degrees, so no pinhole model with polynomial distortion, such as the [Brown-Conrady model](/brown-conrady-distortion-model/), can describe a field of view of 180 degrees. A polynomial in $\theta$ stays finite there. Kannala and Brandt (2006) showed that a few odd terms fit the common fisheye designs closely, and also normal lenses over a limited angle. With four coefficients it is the fisheye model of OpenCV, and many [visual odometry](/visual-odometry/) and SLAM systems use it for wide cameras.

## The machine

**Input.** A point of the world, the pose $(R, t)$, the coefficients $k_1, \ldots, k_n$, and the intrinsics $f_x, f_y, c_x, c_y$.

**Step 1: angle of the ray.** $X_c = R X_w + t = (X, Y, Z)$. Let $\rho = \sqrt{X^2 + Y^2}$ and $\theta = \operatorname{atan2}(\rho, Z)$. The point may have $Z \le 0$; only the direction counts, so the model is central, and $\theta$ runs from 0 to 180 degrees.

**Step 2: image radius.**
$$r(\theta) = k_1 \theta + k_2 \theta^3 + k_3 \theta^5 + k_4 \theta^7 + k_5 \theta^9 .$$
The polynomial is odd because the lens is symmetric about its axis. OpenCV writes the same thing as $\theta_d = \theta (1 + k_1 \theta^2 + k_2 \theta^4 + k_3 \theta^6 + k_4 \theta^8)$, with the first coefficient fixed at 1 and the scale moved into $f_x$ and $f_y$.

**Step 3: image point.** $x_d = r(\theta) \, X / \rho$ and $y_d = r(\theta) \, Y / \rho$ (and $(0, 0)$ if $\rho = 0$). Then $u = f_x x_d + c_x$ and $v = f_y y_d + c_y$.

**Lens distortion.** Lens distortion acts on normalized coordinates: project, distort, then apply $K$. Here the projection gives the angle $\theta$ and the azimuth instead of the point $(X / Z, Y / Z)$, which does not exist for $\theta \ge 90$ degrees, the polynomial $r(\theta)$ is the distortion, and $K$ comes last as in every other model on this list.

**Inverse.** Unprojection maps a pixel to a ray. Compute $(x_d, y_d)$ from $K^{-1}$, then $r = \lVert (x_d, y_d) \rVert$, then solve $r(\theta) = r$ for $\theta$ by the [Newton-Raphson method](/newton-raphson-method/) from the start $\theta_0 = r / k_1$, and return the direction $(\sin\theta \, x_d / r, \; \sin\theta \, y_d / r, \; \cos\theta)$. There is no closed form for more than one term.

**Extra terms.** The full model of Kannala and Brandt also has terms that depend on the azimuth, for lenses that are not exactly symmetric or not centered. Most software uses only the symmetric part.

## What it counts

The model predicts the pixel of each ray of a central camera, for rays up to the largest angle covered by the calibration data. Calibration fits the coefficients, $K$ and the target poses by minimizing the [reprojection error](/reprojection-error/), as for other models; Kannala and Brandt used a planar target. The cost of one projection is a few multiplications, an arctangent and a square root, all $\Theta(1)$ in the real-RAM model. The cost of unprojection is a few Newton steps.

**Classic projections.** Optical designers make fisheye lenses to follow one of a few projections. At $\theta = 60$ degrees with $f = 300$ pixels they give these radii (computed with a script):

| projection | formula | radius at 60 degrees |
|---|---|---|
| perspective | $f \tan\theta$ | 519.6 |
| equidistance | $f \theta$ | 314.16 |
| equisolid angle | $2 f \sin(\theta / 2)$ | 300.0 |
| stereographic | $2 f \tan(\theta / 2)$ | 346.4 |
| orthographic | $f \sin\theta$ | 259.8 |

The equidistance projection is the model with one term, $k_1 = f$. The others are fitted by the odd polynomial. A least squares fit of the equisolid angle projection over $[0, 90]$ degrees with $f = 300$ gave a largest error of 18.27, 0.178, $7.5 \cdot 10^{-4}$, $1.7 \cdot 10^{-6}$ and $2.5 \cdot 10^{-9}$ pixels for 1 to 5 odd terms. The perspective projection is harder because of its pole at 90 degrees: over $[0, 60]$ degrees, 2 to 5 terms gave 17.9, 2.95, 0.46 and 0.07 pixels. So the model also covers normal lenses, but only over a limited angle.

**Inverse example.** For $r(\theta) = \theta + 0.1 \theta^3 - 0.02 \theta^5$ and $r = 1.2$, Newton's method from $\theta_0 = 1.2$ reaches $\theta = 1.0992686$ (62.98 degrees) to 7 digits in 3 to 4 steps.

## Relation to other models

- **Pinhole with Brown-Conrady.** That model writes the radius as a polynomial in $\tan\theta$. It cannot reach 90 degrees, and its fit grows wild near the edge of a wide lens. The Kannala-Brandt model replaces $\tan\theta$ by $\theta$.
- **Unified and double sphere models.** The [unified model](/unified-omnidirectional-camera-model/) and its extensions have closed form unprojection, which is faster. Usenko, Demmel and Cremers (2018) compared these models on fisheye data sets by reprojection error and computation time, and proposed the double sphere model, which fits wide lenses well, is cheap to compute and has a closed form inverse. Their numbers are benchmark results for the lenses they tested; see the paper for the tables.
- **Division model.** The [division model](/division-distortion-model/) has one parameter and is algebraically simple, so it suits minimal solvers, but it fits strong fisheye lenses less well.
- **Generalized camera.** The model is central: all rays pass through one point. A [generalized camera](/generalized-camera-model/) drops this assumption, which some fisheye lenses violate slightly.

## Known results in the model

- **Field of view (theorem).** For an increasing $r(\theta)$ on $[0, \theta_{\max}]$, every ray up to $\theta_{\max}$ has exactly one image point, and $\theta_{\max}$ can be 90 degrees or more. A pinhole model with radial distortion cannot do this, because its input $\tan\theta$ is not defined at 90 degrees.
- **Unique inverse (theorem).** If $r'(\theta) > 0$ on the calibrated range, the inverse is unique on that range and Newton's method converges from a start close enough to the root. The polynomial must be checked for this: a fit can turn down beyond the data.
- **Approximation (heuristic and benchmark).** Odd polynomials with 4 or 5 terms approximate the classic fisheye projections to well below a pixel, as the fits above show. Real lenses deviate from the classic designs, so the fitted coefficients are not those of any closed formula.
- **Choice of terms.** More terms reduce the fit error on the calibration data but can make the polynomial non monotone outside the data. Four terms, as in OpenCV, is a common compromise, not a result of theory.
