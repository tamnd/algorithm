---
tag: JT9XCG
kind: definition
slug: sampson-distance
name: Sampson distance
aliases:
- Sampson error
- first-order geometric error
area: computer-vision/multiple-view-geometry
level: advanced
summary: A first-order approximation of the geometric distance of a point to a variety, the algebraic residual divided by the norm of its gradient.
prereqs: [algebraic-and-geometric-error]
see_also: [reprojection-error, fundamental-matrix, essential-matrix, ransac, optimal-triangulation, homography-estimation, eight-point-algorithm, gauss-newton-algorithm]
sources:
  - paper: doi:10.1016/0146-664X(82)90101-0
    title: "Paul D. Sampson, Fitting conic sections to very scattered data: an iterative refinement of the Bookstein algorithm, Computer Graphics and Image Processing 18(1), 1982, 97-108"
    locator: the weighting of the algebraic residual of a conic by its gradient
  - book: isbn:9780521540513
    title: "Richard Hartley and Andrew Zisserman, Multiple View Geometry in Computer Vision, second edition, Cambridge University Press, 2004"
    locator: "Section 4.2.6, Sampson error (the derivation for a homography and the general form); Section 11.4, Geometric distance (the Sampson approximation for the fundamental matrix); Section 12.4, Sampson approximation (first-order geometric correction)"
---

The Sampson distance is a cheap estimate of the geometric distance of a measurement to the set of measurements that fit a model exactly. It linearizes the constraint at the measured point and returns the distance to the linearized set in closed form: for one scalar constraint, the algebraic residual divided by the norm of its gradient. For two-view matches it approximates the [reprojection error](/reprojection-error/) of a match without solving for the 3D point or for the corrected points. The page [algebraic and geometric error](/algebraic-and-geometric-error/) compares the two kinds of cost; this page defines the approximation that lies between them.

## Definition

Let a model with parameters $\mathbf{h}$ define, for a measurement vector $\mathbf{X} \in \mathbb{R}^N$, an algebraic residual $\boldsymbol{\epsilon} = C_{\mathbf{h}}(\mathbf{X}) \in \mathbb{R}^m$, with $m \le N$. The measurements that fit the model exactly form the variety $\mathcal{V} = \{\mathbf{X} : C_{\mathbf{h}}(\mathbf{X}) = \mathbf{0}\}$. The geometric distance of a measured $\mathbf{X}$ is the length of the shortest $\boldsymbol{\delta}$ with $\mathbf{X} + \boldsymbol{\delta} \in \mathcal{V}$.

Replace $C_{\mathbf{h}}$ by its first-order Taylor expansion at $\mathbf{X}$: $C_{\mathbf{h}}(\mathbf{X} + \boldsymbol{\delta}) \approx \boldsymbol{\epsilon} + J\boldsymbol{\delta}$, with $J$ the $m \times N$ Jacobian matrix of $C_{\mathbf{h}}$ at $\mathbf{X}$. If $J$ has full rank $m$, the shortest $\boldsymbol{\delta}$ with $J\boldsymbol{\delta} = -\boldsymbol{\epsilon}$ is

$$\boldsymbol{\delta}_S = -J^{\mathsf T}(J J^{\mathsf T})^{-1}\boldsymbol{\epsilon},$$

found with a [Lagrange multiplier](/lagrange-multiplier/) for the constraint. The **Sampson error** is its squared length, and the **Sampson distance** is its length:

$$\|\boldsymbol{\delta}_S\|^2 = \boldsymbol{\epsilon}^{\mathsf T}(J J^{\mathsf T})^{-1}\boldsymbol{\epsilon} .$$

For one scalar constraint ($m = 1$) this is $\epsilon^2 / \|\nabla C\|^2$.

**For the fundamental matrix.** A match $\mathbf{x} = (x, y, 1)^{\mathsf T}$, $\mathbf{x}' = (x', y', 1)^{\mathsf T}$ is a measurement $\mathbf{X} = (x, y, x', y') \in \mathbb{R}^4$, and the constraint is $\epsilon = \mathbf{x}'^{\mathsf T}F\mathbf{x}$. Its gradient with respect to $(x, y, x', y')$ is $((F^{\mathsf T}\mathbf{x}')_1, (F^{\mathsf T}\mathbf{x}')_2, (F\mathbf{x})_1, (F\mathbf{x})_2)$, so

$$d_S^2 = \frac{(\mathbf{x}'^{\mathsf T}F\mathbf{x})^2}{(F\mathbf{x})_1^2 + (F\mathbf{x})_2^2 + (F^{\mathsf T}\mathbf{x}')_1^2 + (F^{\mathsf T}\mathbf{x}')_2^2} .$$

The same formula holds for the [essential matrix](/essential-matrix/) in normalized image coordinates.

**For a homography.** The two DLT equations of a pair give $\boldsymbol{\epsilon} \in \mathbb{R}^2$, and $J$ is the $2 \times 4$ matrix of their derivatives with respect to $(x, y, x', y')$; the general formula applies with $m = 2$ (HZ Section 4.2.6).

**Properties.**

- It is 0 exactly when $\boldsymbol{\epsilon} = \mathbf{0}$, that is, when the measurement fits the model.
- It is exact when $C_{\mathbf{h}}$ is affine in $\mathbf{X}$, because then the linearization is the constraint itself. An example is the distance of a point to a line.
- Near the variety it differs from the geometric distance by a term of higher order in the distance.
- It does not change when $C_{\mathbf{h}}$ is multiplied by a nonzero constant, so the scale of $F$ or $H$ does not matter. Unlike the algebraic error, it does not depend on the choice of a Euclidean frame in the images.
- It needs $J J^{\mathsf T}$ to be invertible. For the fundamental matrix it fails at a match where $F\mathbf{x} = \mathbf{0}$ and $F^{\mathsf T}\mathbf{x}' = \mathbf{0}$, which means that both points are the epipoles.

## Examples and non-examples

- **A circle.** For $C(x, y) = x^2 + y^2 - 1$ and the point $(1.1, 0)$: $\epsilon = 0.21$, $\nabla C = (2.2, 0)$, so the Sampson distance is $0.21 / 2.2 \approx 0.0955$, against the true distance $0.1$. For the far point $(2, 0)$ it is $3 / 4 = 0.75$ against $1$: the approximation is good only near the curve. This is the setting of Sampson's 1982 paper on conic fitting.
- **A line.** For $C(x, y) = 3x + 4y - 5$ and the point $(3, 4)$: $\epsilon = 20$ and $\|\nabla C\| = 5$, so the Sampson distance is $4$, which is the exact distance from the point to the line.
- **A rectified stereo pair.** For a camera that moves along the $x$ axis, $F = \begin{pmatrix} 0 & 0 & 0 \\ 0 & 0 & -1 \\ 0 & 1 & 0 \end{pmatrix}$, and $\mathbf{x}'^{\mathsf T}F\mathbf{x} = y - y'$. Then $(F\mathbf{x})_{1,2} = (0, -1)$ and $(F^{\mathsf T}\mathbf{x}')_{1,2} = (0, 1)$, so $d_S^2 = (y - y')^2 / 2$. For $y = 10$ and $y' = 12$, $d_S^2 = 2$. This is exact: the best correction moves each point by 1 pixel toward the other, and $1^2 + 1^2 = 2$.
- **Non-example: the algebraic error.** $(\mathbf{x}'^{\mathsf T}F\mathbf{x})^2$ alone changes with the scale of $F$ and with the position of the match in the image.
- **Non-example: the symmetric epipolar distance.** The sum of the squared distances of $\mathbf{x}'$ to the epipolar line $F\mathbf{x}$ and of $\mathbf{x}$ to the line $F^{\mathsf T}\mathbf{x}'$ is $\epsilon^2 \left( \frac{1}{(F\mathbf{x})_1^2 + (F\mathbf{x})_2^2} + \frac{1}{(F^{\mathsf T}\mathbf{x}')_1^2 + (F^{\mathsf T}\mathbf{x}')_2^2} \right)$. It has the same numerator but another weight. In the stereo example it gives $4 + 4 = 8$, four times the Sampson value.

## Related definitions

- [Reprojection error](/reprojection-error/): the geometric distance that the Sampson distance approximates. For two views, the exact value needs [optimal triangulation](/optimal-triangulation/) of the match.
- [Algebraic and geometric error](/algebraic-and-geometric-error/): the Sampson distance is an algebraic residual with a weight that makes it a first-order geometric distance.
- [RANSAC](/ransac/): the Sampson distance is a common test for inliers of a fundamental or essential matrix, since it is cheap and is in pixels.
- [Homography estimation](/homography-estimation/) and the fundamental matrix: minimizing the sum of Sampson errors over the model parameters alone, with [Gauss-Newton](/gauss-newton-algorithm/) or Levenberg-Marquardt, gives results close to the Gold Standard method at a lower cost.
- Sampson correction: the vector $\boldsymbol{\delta}_S$ itself, added to the measured points, is a first-order correction of a match onto the variety (HZ Section 12.4).

## References
