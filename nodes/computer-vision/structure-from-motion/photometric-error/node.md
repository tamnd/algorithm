---
tag: BZD8NJ
kind: definition
slug: photometric-error
name: Photometric error
aliases:
- photometric residual
area: computer-vision/structure-from-motion
level: advanced
summary: The difference in intensity between a pixel and its warp into another image under an estimated pose and depth, the cost of direct methods.
prereqs: [pinhole-camera-model, bilinear-interpolation]
see_also: [direct-image-alignment, lucas-kanade-method, optical-flow, normalized-cross-correlation, census-transform, huber-m-estimator, direct-sparse-odometry, semi-direct-visual-odometry]
sources:
  - paper: doi:10.1109/TPAMI.2017.2658577
    title: "Jakob Engel, Vladlen Koltun and Daniel Cremers, Direct sparse odometry, IEEE Transactions on Pattern Analysis and Machine Intelligence 40(3), 2018, 611-625"
    locator: "Section 2 (the photometric camera model and the photometric error of a point over a residual pattern, with affine brightness terms, exposure times, gradient weights and the Huber norm)"
  - paper: doi:10.1007/3-540-44480-7_18
    title: "Michal Irani and P. Anandan, About direct methods, Vision Algorithms: Theory and Practice, Lecture Notes in Computer Science 1883, Springer, 2000, 267-277"
    locator: "the case for estimating motion and structure directly from image intensities"
  - paper: doi:10.1023/B:VISI.0000011205.11775.fd
    title: "Simon Baker and Iain Matthews, Lucas-Kanade 20 years on: a unifying framework, International Journal of Computer Vision 56(3), 2004, 221-255"
    locator: "the sum of squared differences between a template and a warped image as the cost of image alignment"
  - book: isbn:9783030343712
    title: "Richard Szeliski, Computer Vision: Algorithms and Applications, second edition, Springer, 2022"
    locator: "Chapter 9, Motion estimation (error metrics for direct alignment, bias and gain, robust error metrics)"
---

## Definition

**Setting.** Two grayscale images $I_i$ (the host or reference) and $I_j$ (the target) come from a calibrated [pinhole camera](/pinhole-camera-model/) with intrinsics $(f_x, f_y, c_x, c_y)$. The relative pose from camera $i$ to camera $j$ is $(R, t)$, so a point $X$ in the frame of camera $i$ is $R X + t$ in the frame of camera $j$. A pixel $u$ of $I_i$ has a depth $z$, or an inverse depth $d = 1/z$.

**Warp.** The warp of $u$ into $I_j$ is

$$
w(u; R, t, d) = \Pi\big(R\, \Pi^{-1}(u, d) + t\big), \quad \Pi^{-1}(u, d) = \frac{1}{d}\Big(\frac{u_x - c_x}{f_x}, \frac{u_y - c_y}{f_y}, 1\Big), \quad \Pi(X) = \Big(f_x \frac{X_1}{X_3} + c_x,\ f_y \frac{X_2}{X_3} + c_y\Big).
$$

**Photometric residual.** Under the brightness constancy assumption (a scene point has the same intensity in both images), the photometric residual of $u$ is

$$
r(u) = I_j\big(w(u; R, t, d)\big) - I_i(u).
$$

The warped position is not an integer pixel in general, so $I_j$ is evaluated by [bilinear interpolation](/bilinear-interpolation/) or a higher order interpolation. With an affine brightness model, as in direct sparse odometry, the residual is

$$
r(u) = \big(I_j(w(u)) - b_j\big) - \frac{t_j e^{a_j}}{t_i e^{a_i}} \big(I_i(u) - b_i\big),
$$

where $t_i, t_j$ are the exposure times (1 if unknown) and $(a_i, b_i), (a_j, b_j)$ are a gain and an offset per image.

**Photometric error.** The photometric error of a set $S$ of pixels (a patch, a pattern of pixels around a point, or all pixels with enough gradient) is

$$
E = \sum_{u \in S} w_u\, \rho\big(r(u)\big),
$$

with a loss $\rho$ (the square $r^2$, or a robust function such as the [Huber function](/huber-m-estimator/)) and weights $w_u \ge 0$. With $\rho(r) = r^2$ and $w_u = 1$ this is the sum of squared differences (SSD) between the patch of $I_i$ and the warped patch of $I_j$. The photometric error is the cost that [direct image alignment](/direct-image-alignment/) minimizes over the pose, and in some methods also over the depths and the brightness terms.

## Examples and non-examples

**One residual by hand.** Let $f_x = f_y = 40$, $c_x = c_y = 20$, and let the pixel $u = (30, 20)$ of $I_i$ have depth $5$, so $d = 0.2$. Then $\Pi^{-1}(u, d) = 5 \cdot (10/40, 0, 1) = (1.25, 0, 5)$. With $R = I$ and $t = (-0.45, 0, 0)$, the point in camera $j$ is $(0.8, 0, 5)$, so $w(u) = (40 \cdot 0.8/5 + 20, 20) = (26.4, 20)$. If $I_j(26, 20) = 100$ and $I_j(27, 20) = 110$, bilinear interpolation gives $I_j(26.4, 20) = 104$. If $I_i(30, 20) = 103$, the residual is $r = 104 - 103 = 1$, and the squared error of this pixel is $1$.

**Brightness change.** Let $I_j(w(u)) = 2 I_i(u) + 5$ for every pixel, as when the gain doubles. The plain residual is $I_i(u) + 5$, which is not zero even at the true pose and depth. With $t_i = t_j = 1$, $a_i = b_i = 0$, $a_j = \ln 2$ and $b_j = 5$, the affine residual is $(2 I_i(u) + 5 - 5) - 2 I_i(u) = 0$ for every pixel.

**A patch.** For a $2 \times 2$ patch with host values $(10, 20, 30, 40)$ and warped target values $(11, 19, 33, 40)$, the residuals are $(1, -1, 3, 0)$ and the SSD is $1 + 1 + 9 + 0 = 11$. With the Huber function of threshold $2$, $\rho(r) = \frac{1}{2} r^2$ for $|r| \le 2$ and $2(|r| - 1)$ otherwise, the error is $0.5 + 0.5 + 4 + 0 = 5$.

**Non-examples.**
- The reprojection error $\Pi(R X + t) - u_j$ of a matched feature. It is a distance in pixels between two positions, and it needs a match $u_j$ found before; the photometric error compares intensities and needs no match.
- The difference $I_j(u) - I_i(u)$ at the same pixel, with no warp. This is a frame difference, used for change detection; it is the photometric residual only for zero motion.
- The zero-mean normalized cross-correlation of two patches. It is a similarity score, not a residual of one pixel, and it is invariant to gain and offset by construction. It is related (see [normalized cross-correlation](/normalized-cross-correlation/)), but it is not the error that Gauss-Newton direct methods minimize.
- The error of a [census transform](/census-transform/) match. It compares bit strings of local orderings, not intensities.

## Related definitions

- **Brightness constancy.** The assumption behind the plain residual. Its first order form, $\nabla I \cdot \dot u + I_t = 0$, is the constraint of [optical flow](/optical-flow/) and of the [Lucas-Kanade method](/lucas-kanade-method/).
- **Direct image alignment.** The minimization of the photometric error over the warp parameters; see [direct image alignment](/direct-image-alignment/).
- **Gradient weights.** Direct sparse odometry weights each residual by $c^2/(c^2 + |\nabla I_i(u)|^2)$, which lowers the weight of pixels with a very large gradient, where small errors of the warp give large residuals.
- **Photometric calibration.** The response function of the camera and the vignetting of the lens change the intensities before the residual is formed. A calibrated method removes them first, so that the affine model holds better.
- **Uses.** [Direct sparse odometry](/direct-sparse-odometry/) minimizes the photometric error of 8-pixel patterns over a window of keyframes; [semi-direct visual odometry](/semi-direct-visual-odometry/) uses it only to track the camera and then switches to the reprojection error.

## References
