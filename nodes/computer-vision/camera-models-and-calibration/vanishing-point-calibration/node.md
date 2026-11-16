---
tag: QBYP5B
kind: algorithm
slug: vanishing-point-calibration
name: Calibration from vanishing points
aliases:
- orthogonal vanishing points calibration
area: computer-vision/camera-models-and-calibration
level: advanced
summary: "Get the focal length, the principal point and the rotation from the vanishing points of three orthogonal directions: the principal point is the orthocenter of their triangle."
solves: [camera-calibration]
model: real-ram
complexity:
  vars: {k: the number of polar iterations at line L9 (at most 60)}
  time: {worst: Θ(1), average: Θ(1), best: Θ(1)}
  space: {extra: Θ(1)}
properties: {deterministic: true, exact: true, online: false, recursive: false}
history:
  year: 1990
  people: [Bruno Caprile, Vincent Torre]
  note: Caprile and Torre showed that the principal point is the orthocenter of the triangle of three orthogonal vanishing points. Hartley and Zisserman later wrote the method as linear constraints on the image of the absolute conic.
prereqs: [vanishing-point-detection, image-of-the-absolute-conic, camera-intrinsic-matrix]
see_also: [camera-calibration, zhang-calibration-method, tsai-calibration-method, camera-matrix-decomposition, self-calibration, cholesky-decomposition, line-detection, camera-extrinsic-parameters]
sources:
  - paper: doi:10.1007/BF00127813
    title: Bruno Caprile and Vincent Torre, Using vanishing points for camera calibration, International Journal of Computer Vision 4(2), 1990, 127-139
    locator: the orthocenter property of the principal point, the focal length from two orthogonal vanishing points, and the rotation from the vanishing points
  - book: isbn:9780521540513
    title: Richard Hartley and Andrew Zisserman, Multiple View Geometry in Computer Vision, second edition, Cambridge University Press, 2004
    locator: Section 8.6, Vanishing points and vanishing lines; Section 8.8, Determining calibration K from a single view (the linear constraints on omega and the orthocenter result)
  - book: isbn:9783030343712
    title: Richard Szeliski, Computer Vision, Algorithms and Applications, second edition, Springer, 2022
    locator: Chapter 11, Structure from motion and SLAM (the part on geometric intrinsic calibration from vanishing points)
---

Calibration from vanishing points finds the focal length $f$, the principal point $c$ and the rotation $R$ of a camera from a single image that shows three mutually orthogonal sets of parallel lines, such as the edges of a building or a box. Each set of lines meets at a vanishing point $v_i \sim K r_i$, where $r_i$ is the direction of the lines in the camera frame. If the camera has zero skew and square pixels, the principal point is the orthocenter of the triangle $v_1 v_2 v_3$, and $f^2 = -(v_1 - c) \cdot (v_2 - c)$ (Caprile and Torre 1990, HZ Section 8.8). The method needs no calibration target and has a closed form. It is less accurate than [Zhang's method](/zhang-calibration-method/), which uses many points on several views of a plane, and unlike [Tsai's method](/tsai-calibration-method/) it needs no known 3D coordinates at all. The [camera calibration](/camera-calibration/) page states the problem; the [vanishing point detection](/vanishing-point-detection/) page covers how to find the three points.

## In plain words

Stand in front of a building and take a photo. The horizontal edges along the front wall seem to meet at one point far to the side. The edges along the side wall meet at another point, and the vertical edges meet at a third point far above or below. These three meeting points form a triangle.

The camera's center of view sits where the three heights of this triangle cross. The focal length follows from how far the points are from that center. Each meeting point also tells the direction of one set of edges, so you also get how the camera is turned. All this comes from one photo and a few lines, with no special pattern in the scene. The method assumes that the pixels are square and that the camera has no skew, which holds for nearly all modern cameras.

## The problem

**Input.** Three finite pixels $v_1, v_2, v_3$, the vanishing points of three mutually orthogonal scene directions. Coordinates follow the area: $u$ to the right, $v$ down, and the center of a pixel at integer coordinates.

**Model.** $K = \begin{pmatrix} f & 0 & c_x \\ 0 & f & c_y \\ 0 & 0 & 1 \end{pmatrix}$ with zero skew and square pixels. The world axes are the three directions, and $R = [r_1 \; r_2 \; r_3]$ holds them in the camera frame, so $v_i \sim K R e_i = K r_i$. Lens distortion must be removed first, because lens distortion acts on normalized coordinates (project, distort, then apply $K$) and bends the lines that define the $v_i$.

**Output.** $f$, $c$ and a rotation $R$ whose columns are $\pm r_i$. The sign of each column is not fixed by the image, because the directions $r_i$ and $-r_i$ have the same vanishing point. The translation is not part of the output: vanishing points are images of points at infinity, so they do not depend on where the camera is.

**The key fact.** $K^{-1} (v_i, 1)^{\mathsf T}$ is parallel to $r_i$, and with the form of $K$ above it equals $((v_i - c) / f, 1)$. So $r_i \cdot r_j = 0$ becomes
$$(v_i - c) \cdot (v_j - c) = -f^2 \qquad (i \ne j).$$
In the language of the [image of the absolute conic](/image-of-the-absolute-conic/) $\omega = (K K^{\mathsf T})^{-1}$, this is $v_i^{\mathsf T} \omega v_j = 0$. Subtract the equation for the pair $(1, 3)$ from the one for $(2, 3)$: $(v_1 - v_2) \cdot (v_3 - c) = 0$, so $c$ lies on the altitude of the triangle from $v_3$. In the same way, $c$ lies on the other two altitudes, so $c$ is the orthocenter.

## The algorithm

```pseudo id=main
VP-CALIBRATE(v_1, v_2, v_3)
L1  a_1 <- v_1 - v_2; b_1 <- a_1 . v_3
L2  a_2 <- v_2 - v_3; b_2 <- a_2 . v_1
L3  D <- det(a_1, a_2); if D = 0 then fail: the points are collinear
L4  c <- the solution p of a_1 . p = b_1 and a_2 . p = b_2, by Cramer's rule
L5  q <- -(v_1 - c) . (v_2 - c); if q <= 0 then fail: the triangle is not acute
L6  f <- sqrt(q); K <- [[f, 0, c_x], [0, f, c_y], [0, 0, 1]]
L7  for i <- 1 to 3: r_i <- K^-1 (v_i, 1) / ||K^-1 (v_i, 1)||
L8  R <- [r_1 r_2 r_3]; if det R < 0 then r_3 <- -r_3
L9  R <- nearest rotation to R, by the iteration X <- (X + X^-T) / 2
L10 return K, R
```

Lines L1 to L4 intersect two altitudes. The equation $a_1 \cdot p = b_1$ says $(v_1 - v_2) \cdot (p - v_3) = 0$, the altitude from $v_3$, and $a_2 \cdot p = b_2$ is the altitude from $v_1$. With $a_1 = (a_{1x}, a_{1y})$ and $a_2 = (a_{2x}, a_{2y})$,
$$D = a_{1x} a_{2y} - a_{1y} a_{2x}, \qquad c_x = \frac{b_1 a_{2y} - a_{1y} b_2}{D}, \qquad c_y = \frac{a_{1x} b_2 - a_{2x} b_1}{D}.$$
In floating point, line L3 rejects $|D|$ below a small multiple of $\lVert a_1 \rVert \lVert a_2 \rVert$. Line L5 uses the pair $(1, 2)$; at the orthocenter all three pairs give the same value, as the proof shows. Line L7 picks for each column the sign with a positive $Z$ component, because $K^{-1} (v_i, 1)$ has last entry 1. Line L8 makes the frame right handed. Line L9 is the Newton iteration for the orthogonal polar factor (Higham 1986); it does not change an exact rotation, and with noisy input it returns the nearest rotation in the Frobenius norm.

**The two point variant.** If the principal point is known, for example as the image center, two vanishing points of orthogonal directions suffice: $f = \sqrt{-(v_1 - c) \cdot (v_2 - c)}$.

## Example

Let the true camera have $f = 800$ and $c = (320, 240)$. The three scene directions have, in the camera frame, the directions $(2, 0, 1)$, $(-0.5, 1, 1)$ and $(-0.5, -1.25, 1)$, which are pairwise orthogonal. Their vanishing points are $v_i = (800 x_i / z_i + 320, 800 y_i / z_i + 240)$:
$$v_1 = (1920, 240), \qquad v_2 = (-80, 1040), \qquad v_3 = (-80, -760).$$

| line | values |
|---|---|
| L1 | $a_1 = (2000, -800)$, $b_1 = 2000 \cdot (-80) + (-800) \cdot (-760) = 448000$ |
| L2 | $a_2 = (0, 1800)$, $b_2 = 0 \cdot 1920 + 1800 \cdot 240 = 432000$ |
| L3 | $D = 2000 \cdot 1800 - (-800) \cdot 0 = 3600000$ |
| L4 | $c_x = (448000 \cdot 1800 + 800 \cdot 432000) / 3600000 = 320$, $c_y = 2000 \cdot 432000 / 3600000 = 240$ |
| L5 | $q = -(1600, 0) \cdot (-400, 800) = 640000$ |
| L6 | $f = 800$ |
| L7 | $r_1 = (2, 0, 1) / \sqrt 5 \approx (0.8944, 0, 0.4472)$, $r_2 = (-1/3, 2/3, 2/3)$, $r_3 \approx (-0.2981, -0.7454, 0.5963)$ |
| L8 | $r_1 \times r_2 = r_3$, so $\det R = 1$ and no column changes sign |
| L9 | $R$ is already a rotation and does not change |

The side $v_2 v_3$ is vertical, so the altitude from $v_1$ is the row $v = 240$, and indeed $c_y = 240$. The other two pairs give the same value: $(v_1 - c) \cdot (v_3 - c) = (1600, 0) \cdot (-400, -1000) = -640000$ and $(v_2 - c) \cdot (v_3 - c) = (-400, 800) \cdot (-400, -1000) = 160000 - 800000 = -640000$. The triangle is acute; for example, the angle at $v_1$ has $(v_2 - v_1) \cdot (v_3 - v_1) = 3200000 = f^2 + \lVert v_1 - c \rVert^2$.

As a check through the IAC, write $\omega \propto \begin{pmatrix} w_1 & 0 & w_2 \\ 0 & w_1 & w_3 \\ w_2 & w_3 & w_4 \end{pmatrix}$. Each pair gives $w_1 (x_i x_j + y_i y_j) + w_2 (x_i + x_j) + w_3 (y_i + y_j) + w_4 = 0$, here the rows $(96000, 1840, 1280, 1)$, $(-336000, 1840, -520, 1)$ and $(-784000, -160, 280, 1)$. The null vector is $(1, -320, -240, 800000)$, which gives $c = (320, 240)$ and $f^2 = 800000 - 320^2 - 240^2 = 640000$ again. A script with exact fractions confirmed every number in this section.

## Correctness

The full proof is in [proofs/correctness.md](proofs/correctness.md). In outline: orthogonality gives $(v_i - c) \cdot (v_j - c) = -f^2$ for each pair, and the difference of two of these equations is an altitude equation, so the true $c$ solves the system of line L4. The three vectors $(v_i, 1) \sim K r_i$ are independent, so the $v_i$ are not collinear, $D \ne 0$ and the solution is unique. Then line L5 gives $q = f^2 > 0$, and line L7 gives $\pm r_i$. Two more facts come from the same identity. The triangle of a real camera is always acute, because the angle at $v_i$ has $(v_j - v_i) \cdot (v_k - v_i) = f^2 + \lVert v_i - c \rVert^2 > 0$. And every input that the algorithm accepts is the exact set of vanishing points of the camera it returns; so a rejection at line L3 or L5 proves that no camera with zero skew and square pixels fits the input.

## Complexity

In the real-RAM model, lines L1 to L8 do a fixed number of arithmetic operations and three square roots: $\Theta(1)$ time and $\Theta(1)$ extra space. Line L9 runs at most a fixed number of iterations on a $3 \times 3$ matrix, so the total stays $\Theta(1)$. For an exact rotation it stops after one iteration. The real cost of calibration from vanishing points is in [vanishing point detection](/vanishing-point-detection/), which is linear or worse in the number of line segments.

## Properties

- **Closed form.** No start value and no iteration, apart from the final projection onto rotations.
- **Order free.** Any order of the three points gives the same $K$; only the order and the signs of the columns of $R$ change. The tests check all six orders.
- **Uses one image.** The method needs no motion and no known lengths. In return it needs strong assumptions: zero skew, square pixels and no distortion.
- **Invariant to scale of the scene and to translation.** Vanishing points do not depend on $t$ or on the size of the scene, so neither does the result.
- **Exact on exact data.** With exact vanishing points, the output is the true $K$ and $R$ up to the signs of the columns.

## Variants and improvements

- **Known principal point.** With $c$ assumed at the image center, two orthogonal vanishing points give $f$, as above. This is the common case when one direction (often the vertical) is nearly parallel to the image plane and its vanishing point is far away.
- **More than three points or images.** Each orthogonal pair gives one linear equation $v_i^{\mathsf T} \omega v_j = 0$ on the IAC. With more pairs, from several images or several boxes, stack the equations and solve them by least squares, then get $K$ from $\omega$ by the [Cholesky decomposition](/cholesky-decomposition/). Other linear constraints fit in the same system: zero skew, square pixels, and the images of circular points from [Zhang's method](/zhang-calibration-method/) (HZ Section 8.8).
- **Weaker camera models.** Without the square pixel assumption, $\omega$ has 4 unknowns up to scale. Three orthogonal vanishing points give only 3 equations, so one more constraint is needed, for example a vanishing line together with the vanishing point of its normal direction (HZ Section 8.8).
- **Refinement.** After the closed form, the line segments that support each vanishing point can be refitted jointly with $K$ and $R$, so that the three points are exactly orthogonal. This is a small [nonlinear least squares](/nonlinear-least-squares/) problem.
- **Manhattan world detection.** Detectors that assume three orthogonal directions estimate $K$ (or only $f$) and the three vanishing points together, so the orthogonality constraint helps the detection itself.

## When to use it

Use it when you have only one image, or images from a camera you cannot calibrate in advance, of a scene with clear orthogonal structure: buildings, rooms, roads with poles, boxes. It is also a good way to get a start value for [bundle adjustment](/bundle-adjustment/) or to check a calibration. Do not use it when you can print a pattern and take several photos; [Zhang's method](/zhang-calibration-method/) is much more accurate and also estimates distortion. Do not use it with a strong wide-angle lens unless the distortion is removed first.

## Pitfalls

- **A vanishing point far away.** If one direction is nearly parallel to the image plane, its vanishing point is far outside the image and its position is poorly determined. The orthocenter then moves a lot for small errors. In the limit, with one vanishing point at infinity, the principal point is only known to lie on the line through the other two, and $c$ must be assumed. Fall back to the two point variant.
- **Directions that are not orthogonal.** The method trusts that the three directions are at right angles. Real buildings have walls that are a few degrees off, and a wrong pairing of a line to a direction moves a vanishing point.
- **Distortion.** Radial distortion bends straight lines, so the line intersections do not meet at one point. Undistort the segments first, for example with the [Brown-Conrady model](/brown-conrady-distortion-model/).
- **Noise.** In the tests, Gaussian noise with sigma = 1 pixel on each vanishing point of a camera with $f = 800$ gave focal length errors up to about 3 pixels and principal point errors up to about 5 pixels over 40 random views. This is a measurement on synthetic data with nearby vanishing points, not a bound. Errors on real images are much larger, because a vanishing point from a few short segments can be off by many pixels.
- **Signs of the columns.** Each column of $R$ is known only up to sign. Fix the signs with extra knowledge, such as the vertical pointing up, before you use $R$.
- **A rejection is information.** A right or obtuse triangle, or a nonpositive $q$, means that the points cannot come from a camera with zero skew and square pixels. Usually one vanishing point is wrong. Do not take the absolute value of $q$.

## Implementations

## History

The orthocenter property of three orthogonal vanishing points was shown by Bruno Caprile and Vincent Torre in 1990, in a paper that also recovered the rotation of the camera from the same vanishing points. Hartley and Zisserman later described the same method with the [image of the absolute conic](/image-of-the-absolute-conic/): each orthogonal pair is a linear constraint on $\omega$, and other known properties of the camera add more linear constraints. Since then, the method has been a standard tool for single image metrology and for calibration in man-made scenes.

## References
