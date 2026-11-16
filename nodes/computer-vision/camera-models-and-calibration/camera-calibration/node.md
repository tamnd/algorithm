---
tag: 97AGWE
kind: problem
slug: camera-calibration
name: Camera calibration
aliases:
- camera resectioning
- geometric camera calibration
area: computer-vision/camera-models-and-calibration
level: intro
summary: Estimate the intrinsic, extrinsic and distortion parameters of a camera from images of points whose 3D positions or structure are known.
prereqs: [camera-intrinsic-matrix, camera-extrinsic-parameters]
see_also: [dlt-camera-resectioning, zhang-calibration-method, tsai-calibration-method, stereo-camera-calibration, camera-matrix-decomposition, brown-conrady-distortion-model, self-calibration, bundle-adjustment]
sources:
  - book: isbn:9780521540513
    title: Richard Hartley and Andrew Zisserman, Multiple View Geometry in Computer Vision, second edition, Cambridge University Press, 2004
    locator: Chapter 6, Camera models; Chapter 7, Computation of the camera matrix P (the linear and gold standard methods, restricted cameras and radial distortion)
  - paper: doi:10.1109/34.888718
    title: Zhengyou Zhang, A flexible new technique for camera calibration, IEEE Transactions on Pattern Analysis and Machine Intelligence 22(11), 2000, 1330-1334
    locator: the whole paper (calibration from views of a plane, the closed form start and the maximum likelihood refinement)
  - paper: doi:10.1109/JRA.1987.1087109
    title: Roger Y. Tsai, A versatile camera calibration technique for high-accuracy 3D machine vision metrology using off-the-shelf TV cameras and lenses, IEEE Journal on Robotics and Automation 3(4), 1987, 323-344
    locator: the whole paper (the camera model with radial distortion and the two stage method)
  - paper: doi:10.1109/CVPR.1997.609468
    title: Janne Heikkila and Olli Silven, A four-step camera calibration procedure with implicit image correction, Proceedings of the IEEE Conference on Computer Vision and Pattern Recognition, 1997, 1106-1112
    locator: the whole paper (linear start, nonlinear fit with radial and tangential distortion)
  - paper: doi:10.1561/0600000023
    title: Peter Sturm, Srikumar Ramalingam, Jean-Philippe Tardif, Simone Gasparini and Joao Barreto, Camera models and fundamental concepts used in geometric computer vision, Foundations and Trends in Computer Graphics and Vision 6(1-2), 2011, 1-183
    locator: the overview of camera models and of calibration approaches
  - book: isbn:9783030343712
    title: Richard Szeliski, Computer Vision, Algorithms and Applications, second edition, Springer, 2022
    locator: Chapter 11, Structure from motion and SLAM (the part on geometric intrinsic calibration)
---

Camera calibration is the problem of finding the numbers that describe how a camera forms its image: the [intrinsic matrix](/camera-intrinsic-matrix/) $K$, the lens distortion, and, for each image, the pose given by the [extrinsic parameters](/camera-extrinsic-parameters/) $R$ and $t$. The input is images of a target whose 3D geometry is known, such as a box with marks, a flat checkerboard or a set of measured points. Among the close pages, this page states the problem and compares the methods. [DLT resectioning](/dlt-camera-resectioning/) estimates a general $3 \times 4$ matrix $P$ from a 3D target, with no distortion. [Camera matrix decomposition](/camera-matrix-decomposition/) splits such a $P$ into $K$, $R$ and $t$. [Zhang's method](/zhang-calibration-method/) uses several views of a plane. [Tsai's method](/tsai-calibration-method/) uses a constraint that radial distortion does not affect.

## In plain words

A camera turns 3D points into pixels by a fixed rule. The rule depends on the focal length, where the optical axis meets the sensor, how the lens bends straight lines, and where the camera stands. Calibration finds these numbers. You show the camera an object whose shape you know exactly, such as a printed checkerboard, and take some photos. You find the corners in each photo. Then you search for the numbers that make the rule send each known corner as close as possible to where it shows in the photo. After this, you can turn any pixel into a ray in 3D, remove the lens bending, and measure real sizes and distances.

## Definition

The usual camera model is a pinhole with distortion. A world point $X$ goes to camera coordinates $X_c = R X + t$, then to the normalized image point $x_n = (X_c / Z_c, Y_c / Z_c)$, then through a distortion map $x_d = D_k(x_n)$ with parameters $k$, and finally to the pixel
$$u = K \begin{pmatrix} x_d \\ 1 \end{pmatrix}, \qquad K = \begin{pmatrix} f_x & s & c_x \\ 0 & f_y & c_y \\ 0 & 0 & 1 \end{pmatrix}.$$
Write $\pi(K, k, R, t; X)$ for this map. The axes of the camera are $X$ to the right, $Y$ down and $Z$ forward, and the pixel center of the top left pixel is $(0, 0)$.

**Input.** $N$ images. In image $j$, the target points $X_{ij}$, with known 3D coordinates in the frame of the target, and their measured pixels $u_{ij}$, for $i = 1, \dots, n_j$.

**Output.** The intrinsics $K$, the distortion parameters $k$, and a pose $(R_j, t_j)$ for each image.

**Criterion.** Under independent Gaussian pixel noise with the same variance, the maximum likelihood estimate minimizes the total reprojection error
$$E = \sum_{j=1}^{N} \sum_{i=1}^{n_j} \big\| u_{ij} - \pi(K, k, R_j, t_j; X_{ij}) \big\|^2.$$
This is a [nonlinear least squares](/nonlinear-least-squares/) problem. All the methods below either minimize $E$ directly from a starting guess, or give such a starting guess in closed form.

## Variants

- **By target.** A 3D target with points not on one plane (the classic photogrammetry setup); a planar target, such as a checkerboard or a grid of ArUco or AprilTag marks; a 1D target, such as points on a stick moved about a fixed point; or no target at all, which is [self-calibration](/self-calibration/) from the images of a rigid scene. Calibration from the [vanishing points](/vanishing-point-calibration/) of three orthogonal directions is a special case with scene structure instead of a target.
- **By what is known.** Intrinsics only, with the poses as nuisance parameters; intrinsics and the pose of one chosen view; or only the pose, with $K$ known, which is the [perspective-n-point](/perspective-n-point/) problem.
- **By lens model.** A pure pinhole; a pinhole with the [Brown-Conrady](/brown-conrady-distortion-model/) radial and tangential distortion; a [fisheye model](/kannala-brandt-fisheye-model/) for wide lenses; or a [generalized camera](/generalized-camera-model/) that gives each pixel its own ray.
- **By number of cameras.** One camera, or several cameras with fixed relative poses, as in [stereo camera calibration](/stereo-camera-calibration/).
- **By the constraints on $K$.** General five parameter $K$; zero skew; square pixels ($f_x = f_y$); or a known principal point.

## Examples

**A direct check.** Take a camera with zero skew, square pixels, $f = 800$ unknown and principal point $(320, 240)$ known, and no distortion. A point at $(0.5, 0, 2)$ in camera coordinates shows at $u = 520$. Then $u - c_x = f \cdot 0.5 / 2$, so $f = 200 \cdot 4 = 800$. Real calibration does not know the camera coordinates of the point, so it must find the pose at the same time, and that makes the problem nonlinear.

**Counting for a checkerboard.** A board with $9 \times 6 = 54$ inner corners, seen in $N = 10$ images, gives $2 \cdot 54 \cdot 10 = 1080$ equations. The unknowns are 5 intrinsics, 2 radial distortion terms and 6 pose parameters per image, so $5 + 2 + 60 = 67$ unknowns. The problem is strongly overdetermined, which averages out the corner noise.

**Counting for a 3D target.** A general $3 \times 4$ camera matrix has 11 degrees of freedom, so 6 points in general position are enough for the linear method; see the worked example on [DLT resectioning](/dlt-camera-resectioning/).

## Known algorithms

| method | target | start | distortion | page |
|---|---|---|---|---|
| DLT, decomposition, then geometric fit | 3D, not coplanar | closed form, from $\ge 6$ points | added in the fit | [DLT resectioning](/dlt-camera-resectioning/), [decomposition](/camera-matrix-decomposition/) |
| Tsai (1987) | 3D, or planar with care | two linear stages | radial, one term | [Tsai's method](/tsai-calibration-method/) |
| Heikkila and Silven (1997) | 3D or planar | DLT | radial and tangential | none |
| Zhang (2000) | planar, $\ge 3$ views (2 with zero skew) | closed form from homographies | radial, in the fit | [Zhang's method](/zhang-calibration-method/) |
| vanishing points | scene with orthogonal directions | closed form | none | [vanishing point calibration](/vanishing-point-calibration/) |
| self-calibration | none, a rigid scene | from the Kruppa equations or the absolute quadric | in a bundle adjustment | [self-calibration](/self-calibration/) |

All of these end, when accuracy matters, with a [Levenberg-Marquardt](/levenberg-marquardt/) minimization of $E$ over all parameters, which is a [bundle adjustment](/bundle-adjustment/) with the 3D points held fixed. OpenCV's `calibrateCamera` and the MATLAB toolbox of Bouguet follow Zhang's start and this refinement.

## Bounds

- **Identifiability with a 3D target (theorem).** A finite camera matrix has 11 degrees of freedom and each point gives 2 equations, so at least 6 points are needed (5.5 in the count). If all points lie on one plane, $P$ is not determined: the DLT matrix has a null space of dimension at least 4. The full list of degenerate sets is in HZ section 22.1.
- **Identifiability with a plane (theorem, Zhang 2000).** Each view of a plane gives 2 linear equations on the 6 entries, up to scale, of $\omega = K^{-\mathsf T} K^{-1}$, the [image of the absolute conic](/image-of-the-absolute-conic/). So 3 views in general position fix a general $K$, and 2 views fix $K$ with zero skew. The two equations depend only on the orientation of the plane, so views of parallel planes, for example views that differ by a pure translation, give no new information.
- **Optimality (theorem).** Under independent, equal variance Gaussian pixel noise and exact target coordinates, minimizing $E$ is the maximum likelihood estimate. Linear methods minimize an algebraic error instead, and are not optimal.
- **Accuracy (heuristic).** The error of the parameters falls roughly as $1 / \sqrt{m}$ in the number $m$ of independent measurements, if the views are varied. Views that tilt the target strongly, and corners near the edges of the image, are what fix the principal point and the distortion; Zhang (2000) reports on synthetic data that tilts far from 0 degrees give better results than views facing the camera (a benchmark result).
- **Input size.** Every method reads all $2 \sum_j n_j$ measurements, so no method is faster than linear in the data.

## Reductions

- **3D target to linear algebra.** Calibration without distortion from a 3D target reduces to finding the null vector of a $2n \times 12$ matrix ([DLT resectioning](/dlt-camera-resectioning/)) and an RQ factorization ([decomposition](/camera-matrix-decomposition/)).
- **Planar target to homographies.** Each view of a plane at $Z = 0$ gives the homography $H = \lambda K [r_1 \; r_2 \; t]$ by the [DLT for homographies](/dlt-homography/). The constraints $r_1^{\mathsf T} r_2 = 0$ and $\|r_1\| = \|r_2\|$ are linear in $\omega$, and $K$ follows from $\omega$ by a [Cholesky factorization](/cholesky-decomposition/).
- **Known intrinsics to pose.** If $K$ and the distortion are known, the pose of each view is a [perspective-n-point](/perspective-n-point/) problem.
- **Refinement to nonlinear least squares.** The final step is a sparse nonlinear least squares problem, solved by [Levenberg-Marquardt](/levenberg-marquardt/).
- **Stereo to two calibrations.** A stereo rig is two calibrations that share the poses of the target, plus one fixed relative pose; see [stereo camera calibration](/stereo-camera-calibration/).

## Applications

- **Metric 3D reconstruction.** Triangulation, stereo depth and structure from motion need $K$ to turn pixels into rays with true angles.
- **Undistortion and rectification.** Removing lens distortion, and making the rows of two stereo images match for [stereo rectification](/stereo-rectification/).
- **Augmented reality.** Drawing virtual objects so that they line up with the real scene needs the true field of view and pose.
- **Robotics and measurement.** Visual servoing, the pose of parts on a conveyor, and photogrammetric measurement of sizes.
- **Multi-camera systems.** Rigs for motion capture, cars and 3D scanners are calibrated jointly so that all cameras share one frame.

## References
