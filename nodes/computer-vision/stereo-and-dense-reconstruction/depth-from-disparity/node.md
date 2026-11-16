---
tag: V59KRG
kind: concept
slug: depth-from-disparity
name: Depth from disparity
aliases:
- stereo depth equation
area: computer-vision/stereo-and-dense-reconstruction
level: intro
summary: For a rectified pair with focal length f and baseline b, a point with disparity d has depth Z = f b / d, so depth error grows as the square of depth.
prereqs: [disparity, camera-intrinsic-matrix]
see_also: [stereo-rectification, point-triangulation, subpixel-disparity-refinement, stereo-matching, point-cloud, depth-map-fusion, structured-light-scanning, range-image]
sources:
  - book: isbn:9783030343712
    title: Richard Szeliski, Computer Vision, Algorithms and Applications, second edition, Springer, 2022
    locator: Chapter 12, Depth estimation (the relation between disparity and depth in a rectified pair)
  - paper: doi:10.1023/A:1014573219977
    title: Daniel Scharstein and Richard Szeliski, A taxonomy and evaluation of dense two-frame stereo correspondence algorithms, International Journal of Computer Vision 47(1-3), 2002, 7-42
    locator: the part that relates disparity to inverse depth
  - book: isbn:9780521540513
    title: Richard Hartley and Andrew Zisserman, Multiple View Geometry in Computer Vision, second edition, Cambridge University Press, 2004
    locator: Chapter 12, Structure computation (triangulation of a point from two views, of which the rectified case is the simplest)
---

In a rectified stereo pair with focal length $f$ in pixels and baseline $b$, a point with [disparity](/disparity/) $d$ has depth $Z = f b / d$, and its other two coordinates follow from its pixel. This is [triangulation](/point-triangulation/) in the simplest geometry, where the two rays lie in one plane with the baseline and meet at a point that two similar triangles give. The same formula shows the main limit of stereo: an error of $\delta d$ pixels in disparity gives an error of about $Z^2 \delta d / (f b)$ in depth, which grows as the square of the distance.

## In plain words

Hold a finger close to your eyes and close one eye, then the other. The finger jumps a lot against the background. A far tree hardly jumps at all. The jump is the disparity, and it is large for near things and small for far things. With two cameras a known distance apart, the size of the jump gives the distance exactly: half the jump means twice the distance. But far things jump so little that a small error in measuring the jump gives a large error in the distance. So stereo measures near things well and far things poorly, and a wider gap between the cameras helps.

## The idea

**The formula.** Put the first camera at the origin and the second at $(b, 0, 0)$, both with intrinsic matrix $K$ with $f_x = f_y = f$, principal point $(c_x, c_y)$ and the same rotation, as after [rectification](/stereo-rectification/). A point $(X, Y, Z)$ has pixels

$$u_1 = f \frac{X}{Z} + c_x, \qquad u_2 = f \frac{X - b}{Z} + c_x, \qquad v = f \frac{Y}{Z} + c_y .$$

So $d = u_1 - u_2 = f b / Z$, and

$$Z = \frac{f b}{d}, \qquad X = \frac{(u_1 - c_x) Z}{f} = \frac{(u_1 - c_x) b}{d}, \qquad Y = \frac{(v - c_y) b}{d} .$$

The units of $Z$ are the units of $b$. The pixel size cancels, because $f$ and $d$ are both in pixels. In homogeneous form, $(X, Y, Z, W)^{\mathsf T} = Q (u_1, v, d, 1)^{\mathsf T}$ with

$$Q = \begin{pmatrix} 1 & 0 & 0 & -c_x \\ 0 & 1 & 0 & -c_y \\ 0 & 0 & 0 & f \\ 0 & 0 & 1/b & 0 \end{pmatrix}$$

and the point is $(X/W, Y/W, Z/W)$. OpenCV calls this matrix the reprojection matrix; with $f_x \ne f_y$, the second row gets the factor $f_x / f_y$. If the rectified cameras have different principal points $c_{x1}$ and $c_{x2}$, replace $d$ by $d - (c_{x1} - c_{x2})$ first.

**The error.** Differentiate $Z = f b / d$:

$$\frac{\partial Z}{\partial d} = -\frac{f b}{d^2} = -\frac{Z^2}{f b}, \qquad |\delta Z| \approx \frac{Z^2}{f b} |\delta d| , \qquad \frac{|\delta Z|}{Z} \approx \frac{Z}{f b} |\delta d| .$$

So the absolute depth error grows as $Z^2$, and the relative error grows as $Z$. This is a theorem to first order in $\delta d$. The size of $\delta d$ is an empirical fact about the matcher: a good [subpixel refinement](/subpixel-disparity-refinement/) gets to a few tenths of a pixel on textured surfaces, and much worse on textureless ones.

**Depth layers.** A matcher that returns whole disparities can only give the depths $Z_k = f b / k$, $k = 1, 2, \ldots$ The gap between two layers is $Z_k - Z_{k+1} = f b / (k(k+1)) \approx Z^2 / (f b)$, the same law. Near points are in thin layers and far points in thick ones.

**The range.** A search over $0 \le d < D$ cannot find points nearer than $Z_{\min} = f b / (D - 1)$. The far limit is set by the smallest disparity the matcher can tell from zero.

**The bias.** The map $d \mapsto f b / d$ is convex for $d > 0$. So if the measured disparity is the true one plus zero mean noise of variance $\sigma^2$, the mean of the computed depth is larger than the true depth (Jensen's inequality), by about $Z \sigma^2 / d^2$ to second order. For small disparities, averaging depths is worse than averaging disparities and then converting.

**The baseline.** A larger $b$ or a larger $f$ gives a larger disparity for the same depth and so a smaller depth error. The price is a larger disparity range to search, more occlusion, and a larger change of view between the images, which makes matching harder. Okutomi and Kanade (1993) used several baselines at once to get both.

## Examples

**Check value.** $f = 500$, $b = 0.1$ m, $d = 20$ gives $Z = 500 \cdot 0.1 / 20 = 2.5$ m. With $(c_x, c_y) = (320, 240)$ and the pixel $(u_1, v) = (420, 290)$, the point is $X = 100 \cdot 0.1 / 20 = 0.5$ m, $Y = 50 \cdot 0.1 / 20 = 0.25$ m.

**Error against depth.** With $f = 500$, $b = 0.1$ m and a disparity error of $0.25$ pixel:

| $Z$ (m) | $d$ (pixels) | $\lvert \delta Z \rvert \approx Z^2 \cdot 0.25 / 50$ (m) | relative error |
|---|---|---|---|
| 1 | 50 | 0.005 | 0.5% |
| 2.5 | 20 | 0.031 | 1.25% |
| 5 | 10 | 0.125 | 2.5% |
| 10 | 5 | 0.5 | 5% |
| 25 | 2 | 3.1 | 12.5% |

At 25 m the disparity is 2 pixels, and a quarter pixel of error is already an eighth of it.

**Depth layers.** With the same rig, whole disparities 20 and 19 give 2.5 m and 2.632 m, a gap of 13 cm. Disparities 5 and 4 give 10 m and 12.5 m, a gap of 2.5 m.

## Where it is used

- **Stereo cameras.** Robots, cars and drones turn each disparity map from [stereo matching](/stereo-matching/) into a depth map and a [point cloud](/point-cloud/) with this formula. The $Z^2$ law sets the useful range of a camera pair for a given baseline.
- **Structured light.** A projector and a camera form a rectified pair in the same way, and [structured light scanning](/structured-light-scanning/) uses the same formula with the projector in place of the second camera.
- **Fusion.** [Depth map fusion](/depth-map-fusion/) and [TSDF fusion](/tsdf-fusion/) weight each depth by its expected error, which grows with $Z^2$.
- **General triangulation.** For cameras that are not rectified, the rays do not meet in general, and [point triangulation](/point-triangulation/) finds the best point by least squares. The rectified formula is its special case.

## References
