---
tag: FJGF9W
kind: algorithm
slug: optimal-triangulation
name: Hartley-Sturm optimal triangulation
aliases:
- polynomial triangulation
- optimal two-view triangulation
area: computer-vision/multiple-view-geometry
level: advanced
summary: "Find the two-view triangulation of least reprojection error exactly, by reducing it to the roots of a degree 6 polynomial over the pencil of epipolar lines."
solves: [point-triangulation]
model: real-ram
complexity:
  vars: {d: "the degree of the polynomial, always 6"}
  time: {worst: Θ(1), average: Θ(1), best: Θ(1)}
  space: {extra: Θ(1)}
properties: {deterministic: true, exact: true, online: false, recursive: false}
history:
  year: 1997
  people: [Richard Hartley, Peter Sturm]
  note: Hartley and Sturm reduced the two-view triangulation of least reprojection error to the real roots of a polynomial of degree 6 and showed that the method is projective invariant.
prereqs: [point-triangulation, fundamental-matrix, reprojection-error, polynomial-root-finding]
see_also: [linear-triangulation, midpoint-triangulation, sampson-distance, maximum-likelihood-estimation, bundle-adjustment, companion-matrix-method, algebraic-and-geometric-error, five-point-algorithm]
sources:
  - paper: doi:10.1006/cviu.1997.0547
    title: "Richard I. Hartley and Peter Sturm, Triangulation, Computer Vision and Image Understanding 68(2), 1997, 146-157"
    locator: the polynomial method, its projective invariance and the comparison with linear and midpoint methods
  - book: isbn:9780521540513
    title: "Richard Hartley and Andrew Zisserman, Multiple View Geometry in Computer Vision, second edition, Cambridge University Press, 2004"
    locator: "Sections 12.3 to 12.5, Algorithm 12.1"
  - paper: doi:10.1109/CVPR.2010.5539785
    title: "Peter Lindstrom, Triangulation Made Easy, IEEE Conference on Computer Vision and Pattern Recognition (CVPR), 2010, 1554-1561"
    locator: the fast iterative alternative to the polynomial method
  - book: isbn:9783030343712
    title: "Richard Szeliski, Computer Vision, Algorithms and Applications, second edition, Springer, 2022"
    locator: "Section 11.2.4, Triangulation"
---

Optimal triangulation finds the 3D point whose two projections are closest to the measured image points, in the sense of the sum of the squared image distances: the [reprojection error](/reprojection-error/). Under independent Gaussian noise on the image points this is the [maximum likelihood estimate](/maximum-likelihood-estimation/). The method of Hartley and Sturm does not search over 3D points. It looks for the corrected image points $\hat{\mathbf{x}}_1$, $\hat{\mathbf{x}}_2$ that satisfy the epipolar constraint $\hat{\mathbf{x}}_2^{\mathsf T}F\hat{\mathbf{x}}_1 = 0$ of the [fundamental matrix](/fundamental-matrix/) and are closest to the measured points. Each such pair lies on a pair of matching epipolar lines, and these lines form a family with one parameter $t$. After a Euclidean change of each image frame, the cost is a simple rational function of $t$, and its stationary points are the real roots of a polynomial of degree 6. The best root gives the corrected points, which back-project to rays that meet, so any [linear triangulation](/linear-triangulation/) gives the point exactly. The result depends only on $F$ and the image points, so the method is projective invariant.

## In plain words

Each photo shows the point a little off from where it should be, so the two lines of sight do not quite meet. The method asks: what is the smallest shift of the two dots that makes the lines meet? It does not try 3D points. Instead it looks at the pairs of lines in the two photos on which matching dots must lie. These pairs can be described with one number. For each value of that number, the needed shift is easy to write down. The best value is found by solving one equation, and the shifted dots give the point directly.

## The problem

**Input.** A fundamental matrix $F$ of rank 2, or two camera matrices $P_1$, $P_2$ from which $F = [\mathbf{e}_2]_\times P_2P_1^+$ is formed, and two measured points $\mathbf{x}_1$, $\mathbf{x}_2$ in Euclidean image coordinates (pixels with square pixels and no skew, or normalized coordinates).

**Output.** The pair $(\hat{\mathbf{x}}_1, \hat{\mathbf{x}}_2)$ with $\hat{\mathbf{x}}_2^{\mathsf T}F\hat{\mathbf{x}}_1 = 0$ that minimizes $d(\mathbf{x}_1, \hat{\mathbf{x}}_1)^2 + d(\mathbf{x}_2, \hat{\mathbf{x}}_2)^2$, and the 3D point $\hat{\mathbf{X}}$ that projects to them.

## The algorithm

Lines L1 to L3 move $\mathbf{x}_1$ and $\mathbf{x}_2$ to the origin of their images and turn each image about the origin so that the epipoles lie on the $x$ axis, at $(1, 0, f)$ and $(1, 0, f')$. Then $F$ has the form
$$F = \begin{pmatrix} ff'd & -f'c & -f'd \\ -fb & a & b \\ -fd & c & d \end{pmatrix}.$$
The epipolar line in image 1 through $(0, t)$ is $\mathbf{l}_1(t) = (tf, 1, -t)$, and the matching line in image 2 is $\mathbf{l}_2(t) = (-f'(ct + d), at + b, ct + d)$. The cost of the best pair on these two lines is the sum of the squared distances from the origin to them:
$$s(t) = \frac{t^2}{1 + f^2t^2} + \frac{(ct + d)^2}{(at + b)^2 + f'^2(ct + d)^2}.$$

```pseudo id=main
OPTIMAL-TRIANGULATION(F, x_1, x_2)
L1  T_1, T_2 <- translations that move x_1, x_2 to the origin; F <- T_2^-T F T_1^-1
L2  e_1, e_2 <- right and left null vectors of F, scaled so that e_x^2 + e_y^2 = 1
L3  R_1, R_2 <- rotations with R_1 e_1 = (1, 0, f), R_2 e_2 = (1, 0, f'); F <- R_2 F R_1^T
L4  f, f' <- third entries of e_1, e_2; a, b, c, d <- F_22, F_23, F_32, F_33
L5  g(t) <- t ((a t + b)^2 + f'^2 (c t + d)^2)^2 - (a d - b c)(1 + f^2 t^2)^2 (a t + b)(c t + d)
L6  t_min <- the real root of g, or t = infinity, with the least s(t)
L7  l_1 <- (t f, 1, -t); l_2 <- (-f'(c t + d), a t + b, c t + d), at t = t_min
L8  x^_1, x^_2 <- the points of l_1, l_2 closest to the origin
L9  x^_i <- T_i^-1 R_i^T x^_i
L10 X <- the linear triangulation of x^_1, x^_2
```

The point of the line $(\lambda, \mu, \nu)$ closest to the origin is $(-\lambda\nu, -\mu\nu, \lambda^2 + \mu^2)$. At $t = \infty$ the lines are $(f, 0, -1)$ and $(-f'c, a, c)$, and $s(\infty) = 1/f^2 + c^2/(a^2 + f'^2c^2)$.

## Example

Take $P_1 = [I \mid \mathbf{0}]$ and $P_2 = [R_y(-0.3) \mid (-1, 0, 0.2)^{\mathsf T}]$, in normalized coordinates. The point $(1, 2, 4)$ has the images $(0.25, 0.5)$ and $(-0.2842, 0.4633)$. Move the second one by $(0.01, 0.02)$ to $(-0.2742, 0.4833)$.

| line | value |
|---|---|
| L2 to L4 | $f = -0.4649$, $f' = -0.2105$, $a = -0.0927$, $b = 1.0228$, $c = -0.9739$, $d = 0.0194$ |
| L5 | $g(t) = -0.0042t^6 + 0.0489t^5 - 0.0591t^4 + 0.5716t^3 - 0.4987t^2 + 2.0865t - 0.0197$ |
| L6 | real roots $0.009456$ and $11.419$, with $s = 1.880 \times 10^{-4}$ and $27.03$; $s(\infty) = 23.36$; so $t_{\min} = 0.009456$ |
| L9 | $\hat{\mathbf{x}}_1 = (0.2478, 0.5092)$, $\hat{\mathbf{x}}_2 = (-0.2732, 0.4734)$ |
| L10 | $\hat{\mathbf{X}} = (1.0543, 2.1667, 4.2553)$, reprojection error $1.880 \times 10^{-4}$ |

On the same data, linear triangulation gives $(1.0540, 2.1704, 4.2563)$ with the larger reprojection error $1.891 \times 10^{-4}$. In the simpler case $P_2 = [I \mid (-1, 0, 0)^{\mathsf T}]$, with the images $(0.25, 0.5)$ and $(0, 0.52)$, the epipolar lines are horizontal, the polynomial has degree 1, and the method moves both points to the height $0.51$. The result is $(1, 2.04, 4)$, with reprojection error $2 \times 10^{-4}$.

## Correctness

Translations and rotations of the images keep distances and transform $F$ in a matching way, so the normal form above loses nothing. Every corrected point $\hat{\mathbf{x}}_1$ other than the epipole lies on one line $\mathbf{l}_1(t)$ of the pencil, and its epipolar line in image 2 is $\mathbf{l}_2(t)$. So the least cost for a given $t$ is the sum of the squared distances from the origin to the two lines, $s(t)$, and pairs that contain an epipole are never better. On the projective line of $t$ the function $s$ reaches its minimum, either at $t = \infty$ or where $s'(t) = 0$. Clearing denominators in $s'(t) = 0$ gives exactly $g(t) = 0$. So line L6 finds the optimal $t$, and the feet of the perpendiculars are the optimal pair. The corrected points satisfy the epipolar constraint, so their rays meet, and the point where they meet has a reprojection error equal to the optimal cost. The full proof is in the proof file of this page.

## Complexity

All steps work on objects of fixed size: $3 \times 3$ matrices, a polynomial of degree 6 and at most 7 candidate values of $t$. So the method takes $\Theta(1)$ time and space per point. In practice it is several times slower than linear triangulation, mostly because of the root finding.

## Properties

- **Optimal.** It gives the global minimum of the two-view reprojection error, not a local one; it is the maximum likelihood estimate under independent isotropic Gaussian image noise.
- **Projective invariant.** It uses only $F$ and the image points. A projective change of the world frame gives the same corrected points and the transformed 3D point.
- **Exact on exact data.** If the measured points already satisfy the epipolar constraint, the cost is 0, they are not moved, and the point is exact.
- **Two views only.** The pencil argument needs one pair of epipolar lines. For three or more views the problem has many more stationary points, and other methods are used.
- **Euclidean images.** The cost is a distance in each image, so the image coordinates must have square pixels and no skew, or be normalized.

## Variants and improvements

- **Iterative correction.** Lindstrom (2010) finds the same optimal pair with a short iteration that needs no polynomial roots; in practice two steps are enough, and the result is much faster to compute.
- **First-order correction.** One step of correction along the gradient of the epipolar constraint gives the pair that minimizes the [Sampson distance](/sampson-distance/), a first-order approximation of the optimal cost.
- **Triangulation in more views.** For three or more views, local minimization of the reprojection error from a linear start, or a full [bundle adjustment](/bundle-adjustment/), is the usual approach.
- **Calibrated cameras.** With an essential matrix, for example from the [five-point algorithm](/five-point-algorithm/), the same method works on normalized image points, and the cost is then measured in normalized units instead of pixels.

## When to use it

Use it when two views must give the best possible point under image noise, for example to evaluate other methods, to triangulate in a projective reconstruction where Euclidean methods do not apply, or to initialize a reconstruction with as little bias as possible. When speed matters and many points must be triangulated, linear triangulation followed by a few Gauss-Newton steps, or the iterative correction of Lindstrom, gives almost the same result.

## Pitfalls

- **Non-Euclidean image frames.** Running the method on pixel coordinates with skew, or on coordinates after a projective normalization, minimizes the wrong distance.
- **Points near the epipole.** The rotation of line L3 is not defined when a measured point is at the epipole, and it is badly conditioned near it.
- **Root finding.** Two real roots can be close or form a double root; take the real parts of nearly real complex roots as candidates, and do not forget the candidate $t = \infty$.
- **Back-transformation.** The corrected points must be mapped back with the inverses of both the rotation and the translation, in that order.
- **Points behind a camera.** The method minimizes an image distance and can return a point behind a camera. Check [cheirality](/cheirality/) if the cameras are known in a Euclidean frame.

## Implementations

## History

Hartley and Sturm (1997) studied the triangulation of a point from two views with known cameras. They showed that the linear and midpoint methods are not projective invariant, reduced the minimization of the reprojection error to the real roots of a polynomial of degree 6, and showed in experiments that the optimal method is more accurate than the others. Hartley and Zisserman present the method as Algorithm 12.1 of their book. Lindstrom (2010) gave a fast iterative method that reaches the same optimum in a few steps.

## References
