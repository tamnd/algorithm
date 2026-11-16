---
tag: WSAQZX
kind: algorithm
slug: zhang-calibration-method
name: Zhang's calibration method
aliases:
- planar camera calibration
- Zhang's method
area: computer-vision/camera-models-and-calibration
level: core
summary: Calibrate a camera from several views of a planar pattern, getting K in closed form from the homographies and refining all parameters with Levenberg-Marquardt.
solves: [camera-calibration]
model: floating-point-model
complexity:
  vars: {n: the number of points on the pattern, N: the number of views, T: the number of Levenberg-Marquardt iterations}
  time: {worst: O(n N + T n N^3), average: O(n N + T n N^3), best: O(n N + T n N^3)}
  space: {extra: O(n N^2)}
properties: {deterministic: true, exact: false, online: false, recursive: false}
history:
  year: 2000
  people: [Zhengyou Zhang]
  note: Zhang published the method as a Microsoft Research report in 1998 and in IEEE PAMI in 2000. It needs only a printed pattern on a flat surface, and it became the standard way to calibrate a camera in OpenCV and in the MATLAB toolbox of Bouguet.
prereqs: [camera-calibration, camera-intrinsic-matrix, singular-value-decomposition]
see_also: [homography, dlt-homography, image-of-the-absolute-conic, levenberg-marquardt, brown-conrady-distortion-model, tsai-calibration-method, dlt-camera-resectioning, stereo-camera-calibration]
sources:
  - paper: doi:10.1109/34.888718
    title: Zhengyou Zhang, A flexible new technique for camera calibration, IEEE Transactions on Pattern Analysis and Machine Intelligence 22(11), 2000, 1330-1334
    locator: the basic constraints on the homography, the closed form solution for B and K, the maximum likelihood refinement, and the treatment of radial distortion
  - book: isbn:9780521540513
    title: Richard Hartley and Andrew Zisserman, Multiple View Geometry in Computer Vision, second edition, Cambridge University Press, 2004
    locator: Section 8.5, Camera calibration and the image of the absolute conic (calibration from the images of the circular points of planes); Section 4.4 on data normalization for the homography DLT
  - book: isbn:9783030343712
    title: Richard Szeliski, Computer Vision, Algorithms and Applications, second edition, Springer, 2022
    locator: Chapter 11, Structure from motion and SLAM (the part on geometric intrinsic calibration with planar patterns)
---

Zhang's method calibrates a camera from $N \ge 3$ photos of a flat pattern, such as a printed checkerboard, taken from different angles. Each photo gives a [homography](/homography/) $H_j \sim K [r_1 \; r_2 \; t]$ from the plane to the image. Because $r_1$ and $r_2$ are orthonormal, each $H_j$ gives two linear equations on the symmetric matrix $B = K^{-\mathsf T} K^{-1}$. An SVD solves for $B$, a closed form gives $K$, and $K^{-1} H_j$ gives each pose. A [Levenberg-Marquardt](/levenberg-marquardt/) fit of the reprojection error over all parameters, with radial distortion, then gives the final answer. Among the close pages, [camera calibration](/camera-calibration/) states the problem; [DLT resectioning](/dlt-camera-resectioning/) needs a 3D target, not a plane, and estimates a general $P$; [camera matrix decomposition](/camera-matrix-decomposition/) splits such a $P$; and [Tsai's method](/tsai-calibration-method/) uses the radial alignment constraint, which needs a known principal point.

## In plain words

Print a checkerboard and glue it to a flat board. Take ten or so photos of it, tilted in different ways. In each photo the board looks like a squashed square. How it is squashed depends both on how the board is tilted and on the camera's focal length and center. One tilt alone cannot separate the two. But the true corners of the board are at right angles and the squares are equal, and every tilted view must agree with that. Each photo gives two such conditions on the camera. Three photos are enough to solve for the camera in one step. Then a search adjusts all the numbers together, with the lens bending, until the predicted corners land on the found corners.

## The problem

**Input.** Model points $m_i = (X_i, Y_i)$, $i = 1, \dots, n$, on the plane $Z = 0$ of the pattern frame, with $n \ge 4$ and no three on one line; and their pixels $u_{ij}$ in views $j = 1, \dots, N$. Either $N \ge 3$, or $N \ge 2$ with zero skew.

**Output.** $K$, the radial distortion $(k_1, k_2)$, and the pose $(R_j, t_j)$ of each view. The model is: $X_c = R_j (X_i, Y_i, 0)^{\mathsf T} + t_j$, $(x, y) = (X_c / Z_c, Y_c / Z_c)$, $x_d = x (1 + k_1 r^2 + k_2 r^4)$ and $y_d = y (1 + k_1 r^2 + k_2 r^4)$ with $r^2 = x^2 + y^2$, and $u = K (x_d, y_d, 1)^{\mathsf T}$.

**Goal.** Minimize the reprojection error $\sum_{j} \sum_{i} \| u_{ij} - \pi(K, k_1, k_2, R_j, t_j; m_i) \|^2$, which is the maximum likelihood estimate under Gaussian pixel noise.

## The algorithm

For a point on $Z = 0$, $K [r_1 \; r_2 \; r_3 \; t] (X, Y, 0, 1)^{\mathsf T} = K [r_1 \; r_2 \; t] (X, Y, 1)^{\mathsf T}$, so the view is the homography $H = [h_1 \; h_2 \; h_3] = \lambda K [r_1 \; r_2 \; t]$. Then $K^{-1} h_1$ and $K^{-1} h_2$ are orthogonal and of equal length, which gives
$$h_1^{\mathsf T} B h_2 = 0, \qquad h_1^{\mathsf T} B h_1 - h_2^{\mathsf T} B h_2 = 0, \qquad B = K^{-\mathsf T} K^{-1}.$$
With $b = (B_{11}, B_{12}, B_{22}, B_{13}, B_{23}, B_{33})$ and the columns $h_i = (h_{i1}, h_{i2}, h_{i3})$, one has $h_i^{\mathsf T} B h_j = v_{ij}^{\mathsf T} b$ with
$$v_{ij} = (h_{i1} h_{j1},\; h_{i1} h_{j2} + h_{i2} h_{j1},\; h_{i2} h_{j2},\; h_{i3} h_{j1} + h_{i1} h_{j3},\; h_{i3} h_{j2} + h_{i2} h_{j3},\; h_{i3} h_{j3}).$$
So each view adds the rows $v_{12}^{\mathsf T}$ and $(v_{11} - v_{22})^{\mathsf T}$ to a matrix $V$ with $V b = 0$. The matrix $B$ is the [image of the absolute conic](/image-of-the-absolute-conic/) $\omega$, and the two equations say that the images of the two circular points of the plane lie on it.

```pseudo id=main
ZHANG-CALIBRATE(m_1..m_n, u_ij for views j = 1..N)
L1  for j <- 1 to N: H_j <- normalized DLT homography from the m_i to the u_ij
L2  for j <- 1 to N: add the rows v_12(H_j)^T and (v_11(H_j) - v_22(H_j))^T to V
L3  if the skew is known to be 0 then add the row (0, 1, 0, 0, 0, 0) to V
L4  b <- unit right singular vector of V for the smallest singular value
L5  K_0 <- closed form intrinsics from b
L6  for j <- 1 to N: (R_j, t_j) <- pose from K_0^-1 H_j, then the nearest rotation
L7  (k_1, k_2) <- linear least squares with K_0 and the poses fixed
L8  minimize the reprojection error over K, k_1, k_2, R_j, t_j by Levenberg-Marquardt
L9  return K, k_1, k_2, (R_j, t_j) for j = 1..N
```

Line L1 is the [DLT for homographies](/dlt-homography/) with the normalization of Hartley. Line L4 needs at least 5 rows; with fewer, the code raises an error. Line L5 is the closed form of Zhang (2000). With $\lambda$ the unknown scale of $b$,
$$v_0 = \frac{B_{12} B_{13} - B_{11} B_{23}}{B_{11} B_{22} - B_{12}^2}, \quad \lambda = B_{33} - \frac{B_{13}^2 + v_0 (B_{12} B_{13} - B_{11} B_{23})}{B_{11}}, \quad \alpha = \sqrt{\lambda / B_{11}},$$
$$\beta = \sqrt{\frac{\lambda B_{11}}{B_{11} B_{22} - B_{12}^2}}, \quad \gamma = -\frac{B_{12} \alpha^2 \beta}{\lambda}, \quad u_0 = \frac{\gamma v_0}{\beta} - \frac{B_{13} \alpha^2}{\lambda},$$
and $K_0 = \begin{pmatrix} \alpha & \gamma & u_0 \\ 0 & \beta & v_0 \\ 0 & 0 & 1 \end{pmatrix}$. The sign of $b$ does not matter. Line L6 sets $r_1 = \mu K_0^{-1} h_1$, $r_2 = \mu K_0^{-1} h_2$, $r_3 = r_1 \times r_2$ and $t = \mu K_0^{-1} h_3$, with $\mu = \pm 1 / \|K_0^{-1} h_1\|$ and the sign that puts the plane in front of the camera ($t_z > 0$). With noise, $[r_1 \; r_2 \; r_3]$ is not exactly a rotation, so it is replaced by the nearest rotation $U V^{\mathsf T}$ from its SVD. Line L7 uses the fact that, with $(u, v)$ the ideal pixel and $(\breve u, \breve v)$ the distorted one, $\breve u - u = (u - c_x)(k_1 r^2 + k_2 r^4)$, and the same for $v$; these are two linear equations in $(k_1, k_2)$ per point. Line L8 fits all $7 + 6N$ parameters, with each rotation as a rotation vector.

## Example

**The closed form on exact numbers.** Take $K = \begin{pmatrix} 2 & 1 & 3 \\ 0 & 4 & 2 \\ 0 & 0 & 1 \end{pmatrix}$. Then $K^{-1} = \begin{pmatrix} 1/2 & -1/8 & -5/4 \\ 0 & 1/4 & -1/2 \\ 0 & 0 & 1 \end{pmatrix}$, and $B = K^{-\mathsf T} K^{-1}$ gives
$$b = \left(\tfrac{1}{4}, -\tfrac{1}{16}, \tfrac{5}{64}, -\tfrac{5}{8}, \tfrac{1}{32}, \tfrac{45}{16}\right).$$
Line L5: $B_{11} B_{22} - B_{12}^2 = 1/64$ and $B_{12} B_{13} - B_{11} B_{23} = 1/32$, so $v_0 = 2$; $\lambda = 45/16 - (25/64 + 2/32) \cdot 4 = 1$; $\alpha = \sqrt{4} = 2$; $\beta = \sqrt{16} = 4$; $\gamma = (1/16) \cdot 4 \cdot 4 = 1$; $u_0 = 1 \cdot 2 / 4 + (5/8) \cdot 4 = 3$. This is $K$. With $-3 b$ in place of $b$, $\lambda$ becomes $-3$ and the same $K$ comes out.

**A full run.** The reference tests use $K$ with $f_x = 800$, $f_y = 780$, skew $1.5$ and principal point $(320, 240)$, radial distortion $k_1 = -0.25$, $k_2 = 0.08$, a $6 \times 5$ grid of unit spacing, and 4 views tilted by up to about 0.5 radians at a depth of 12.

| step | result |
|---|---|
| L1 to L5, exact pixels | $K_0 = \begin{pmatrix} 810.42 & 1.46 & 320.51 \\ 0 & 790.95 & 240.97 \end{pmatrix}$, off by about 1.3% because the closed form ignores distortion |
| L7 | a first $(k_1, k_2)$ with $K_0$ fixed |
| L8 | the cost falls from 17.02 to $3.3 \cdot 10^{-25}$ in 7 accepted steps |
| L9 | $K$, $k_1$, $k_2$ and all poses equal to the true values with a relative error below $10^{-6}$ |

Without distortion, 3 views give $K$ to 12 digits from line L5 alone. With pixel noise of $\sigma = 0.2$ on 5 views, zero skew and the same distortion, one run (seed 7) gave $f_x = 798.24$, $f_y = 778.00$, principal point $(317.96, 238.69)$, $k_1 = -0.2472$, $k_2 = 0.0167$ and an RMS reprojection error of 0.19 pixel. The focal lengths are good to 0.3%, but $k_2$ is far from 0.08: with 30 points per view, the $r^4$ term is weakly determined.

## Correctness

With exact data and no distortion, each $H_j$ is $\lambda_j K [r_1 \; r_2 \; t]$, so the true $b$ satisfies $V b = 0$. If $V$ has rank 5, which holds for 3 views in general position, line L4 returns a multiple of the true $b$. The closed form of line L5 recovers $K$ from any nonzero multiple $\mu K^{-\mathsf T} K^{-1}$: one checks that the expression for $\lambda$ equals $\mu$, and then each formula gives the matching entry of $K$. Line L6 then gives the exact poses. Line L8 accepts only steps that lower the cost, so the cost never increases; it converges to a local minimum, which is the global one when the start is close, as the closed form makes it in practice. The full proof is in the proof file below.

## Complexity

The time is $O(n N)$ for lines L1 to L7: each homography is an SVD of a $2n \times 9$ matrix, and $V$ has $2N$ (or $2N + 1$) rows and 6 columns. Each Levenberg-Marquardt iteration in the reference code forms the Jacobian by forward differences, which costs $O(n N)$ model evaluations because a pose parameter affects only its own view, then forms the dense normal matrix of size $7 + 6N$ in $O(n N \cdot N^2)$ and solves it in $O(N^3)$. So $T$ iterations cost $O(T n N^3)$, and the extra space is the dense Jacobian, $O(n N^2)$. The Jacobian is block sparse: with a Schur complement on the pose blocks, as in [bundle adjustment](/bundle-adjustment/), each iteration costs $O(n N)$. With $N = 10$ to 30 views, the dense form is fast enough. The method is not exact: with noise, it returns a local minimum of a nonlinear cost.

## Properties

- **Needs only a plane.** A printed pattern is cheap and easy to make accurate, unlike a 3D target.
- **No starting guess.** Lines L1 to L7 give a start from the data alone.
- **Maximum likelihood at the end.** The final fit minimizes the reprojection error, so under Gaussian noise it is the maximum likelihood estimate, if Levenberg-Marquardt finds the global minimum.
- **Degenerate motions.** Views of parallel planes give the same two equations, because the equations depend only on the orientation of the plane through its circular points. So pure translations of the pattern add nothing; the tests check that three translated views leave $V$ with rank 2.
- **Deterministic.** The same input gives the same output; there is no random sampling.

## Variants and improvements

- **Zero skew.** Add the row $(0, 1, 0, 0, 0, 0)$ (line L3), which needs only 2 views, and keep the skew fixed at 0 in line L8. Most modern cameras have zero skew.
- **More distortion terms.** Add a third radial term and the two tangential terms of the [Brown-Conrady model](/brown-conrady-distortion-model/), as OpenCV does, only in line L8. For wide lenses, use a [fisheye model](/kannala-brandt-fisheye-model/).
- **Sparse refinement.** Exploit the block structure of the Jacobian, as in bundle adjustment, for many views.
- **Better corners.** Subpixel corner detection, and patterns with coded marks, such as ChArUco or AprilTag grids, which allow partial views of the board.
- **Several cameras.** Calibrate each camera, then fit the fixed relative pose, as in [stereo camera calibration](/stereo-camera-calibration/).
- **Known principal point.** Fix $c_x$ and $c_y$ in the closed form, so that one view is enough for the focal lengths; this is weaker in accuracy.

## When to use it

Use Zhang's method to calibrate a camera in the lab or in the field, when you can move a flat pattern in front of it. It is the default for most cameras with a normal field of view. Use [DLT resectioning](/dlt-camera-resectioning/) if you have a precise 3D target. Use [self-calibration](/self-calibration/) if no target is available. For lenses wider than about 120 degrees, use a fisheye model in the refinement, because the pinhole start can be far off.

## Pitfalls

- **Too little tilt.** Views that face the camera, or views that only translate, make $V$ nearly rank deficient, and the principal point and focal length become unstable. Tilt the board clearly about both axes.
- **Corners only near the center.** The distortion is fitted from the corners near the edges of the image. Cover the whole image across all views.
- **Assuming the closed form is the answer.** With distortion, $K_0$ is biased, about 1% in the example. Always run line L8.
- **A pattern that is not flat or not to scale.** Measure the printed square size; a warped board biases the result, and a wrong square size scales all the translations.
- **Ambiguous board orientation.** A symmetric board can be detected rotated by 180 degrees in some views, so the point order changes. Use a board with an odd and an even number of corners, or coded marks.
- **Reporting only the RMS error.** A low RMS on the data used for the fit can hide a poorly determined $k_2$ or principal point. Check the parameter spread over subsets of the views.

## Implementations

## History

Zhengyou Zhang described the method in a Microsoft Research technical report in 1998 and published it in IEEE Transactions on Pattern Analysis and Machine Intelligence in 2000. The method replaced the 3D targets of earlier photogrammetric methods with a pattern that anyone can print, and the closed form start removed the need for a guess. The calibration functions of OpenCV and the MATLAB camera calibration toolbox of Jean-Yves Bouguet follow its scheme of a closed form start and a full nonlinear fit with distortion.

## References
