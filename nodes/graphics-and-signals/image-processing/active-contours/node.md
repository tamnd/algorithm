---
tag: JHEZE1
kind: algorithm
slug: active-contours
name: Active contours
aliases:
- snakes
area: graphics-and-signals/image-processing
level: advanced
summary: Deform a closed curve to a nearby object boundary by minimizing an energy of smoothness plus image edge strength. The semi-implicit step of Kass, Witkin and Terzopoulos solves a linear system.
solves: [image-segmentation]
model: real-ram
complexity:
  vars: {n: number of contour points, K: number of iterations}
  time: {worst: Θ(n³ + K n²), best: Θ(n³ + K n²)}
  space: {extra: Θ(n²)}
properties: {deterministic: true, exact: false, linear: false, in_place: false}
history:
  year: 1988
  people: [Michael Kass, Andrew Witkin, Demetri Terzopoulos]
  note: Kass, Witkin and Terzopoulos introduced snakes in 1988 in the first volume of the International Journal of Computer Vision, as curves that minimize an internal energy plus an image energy.
prereqs: [edge-detection, gaussian-filter, gradient-descent]
see_also: [level-set-method, proximal-gradient-method, cholesky-decomposition, backward-euler-method, b-spline, watershed-segmentation, image-segmentation-graph-cuts, canny-edge-detector]
sources:
  - paper: doi:10.1007/BF00133570
    title: Michael Kass, Andrew Witkin and Demetri Terzopoulos, Snakes, active contour models, International Journal of Computer Vision 1(4), 321 to 331, 1988
    locator: the energy of a snake (internal, image and constraint terms), the image forces from lines, edges and terminations, and the semi-implicit numerical scheme with the pentadiagonal matrix
  - book: isbn:9780133356724
    title: Rafael C. Gonzalez and Richard E. Woods, Digital Image Processing, fourth edition, Pearson, 2018
    locator: Section 11.2, Active Contours, Snakes (the energy, the iterative solution, and the external forces)
  - paper: "Amir A. Amini, Terry E. Weymouth and Ramesh C. Jain, Using dynamic programming for solving variational problems in vision, IEEE Transactions on Pattern Analysis and Machine Intelligence 12(9), 855 to 867, 1990"
    locator: the minimization of the snake energy over a discrete window of positions by dynamic programming
  - paper: "Chenyang Xu and Jerry L. Prince, Snakes, shapes, and gradient vector flow, IEEE Transactions on Image Processing 7(3), 359 to 369, 1998"
    locator: the gradient vector flow field as an external force with a large capture range
  - book: isbn:9783030343712
    title: Richard Szeliski, Computer Vision, Algorithms and Applications, second edition, Springer, 2022
    locator: Section 7.3, Contour tracking (snakes and scissors)
---

An active contour, or snake, is a closed curve that moves in an image to lock onto the boundary of an object. Its shape is the result of a minimization. The energy has an internal part, which is small when the curve is short and smooth, and an image part, which is small where the image has strong edges. The user, or another method, places the first curve near the object, and each step moves all the points of the curve at once to a curve of lower energy. Michael Kass, Andrew Witkin and Demetri Terzopoulos introduced the method in 1988, with a semi-implicit step that solves a linear system. The energy is not convex, so the result depends on the start: a snake finds a boundary near where it begins, not the best boundary in the image. It is a method of [image segmentation](/image-segmentation/) for one object.

## In plain words

Think of a rubber band that you put around an object in a picture. The band pulls itself tight and tries to stay smooth. The edges of the object pull on the band, because the picture is made to look like a valley along each edge. The band slides down into the valley and stops there, where the pull of the edges and the pull of the rubber balance. Each step of the method moves every point of the band a little. The band is never worse after a step than before it. But if you start the band far from the object, it can stop on some other edge, or shrink to nothing.

## The problem

The input is an image $I$ with $H$ rows and $W$ columns, and a closed curve of $n$ points $v_0, \ldots, v_{n-1}$, with $v_i = (x_i, y_i)$ and the point after $v_{n-1}$ being $v_0$. Pixel $(i, j)$ is a point sample at the integer point $(i, j)$, with $x$ to the right and $y$ downward. The points of the curve have real coordinates. The image enters through a potential $P(x, y)$ that is low on edges. Here $P = -w f$, where $f$ is a smooth function of an edge strength image $S$, and $w > 0$ is a weight. The output is a curve that is a local minimum of the energy

$$E(v) = \sum_{i=0}^{n-1} \left( \frac{\alpha}{2} |v_{i+1} - v_i|^2 + \frac{\beta}{2} |v_{i+1} - 2 v_i + v_{i-1}|^2 + P(v_i) \right),$$

with $\alpha \ge 0$ for the tension and $\beta \ge 0$ for the stiffness. The first two terms are the internal energy, a discrete form of $\int \tfrac{1}{2}(\alpha |v'|^2 + \beta |v''|^2)\, ds$. The last is the image energy.

**The edge strength and the potential.** The implementation takes $S = |\nabla (G_\sigma * I)|^2$ by central differences of the image smoothed with a [Gaussian filter](/gaussian-filter/), scaled to a maximum of 1. The potential is $P(x, y) = -w \sum_{i, j} S_{ij}\, b(x - i)\, b(y - j)$, where $b$ is the cubic [B-spline](/b-spline/) basis function. So $P$ has two continuous derivatives everywhere, and the gradient of $P$ can be read at any real point.

## The algorithm

The internal energy is a quadratic form. Let $L$ be the $n \times n$ circulant matrix with the row $(-1, 2, -1)$, the Laplacian of the cycle. Then the internal energy is $\tfrac{1}{2} x^T A x + \tfrac{1}{2} y^T A y$ with $A = \alpha L + \beta L^2$, the circulant matrix with the row $(\beta, -\alpha - 4\beta, 2\alpha + 6\beta, -\alpha - 4\beta, \beta)$. A step of size $1/\gamma$ is explicit in the image force and implicit in the internal force:

$$(A + \gamma I)\, x^{\text{new}} = \gamma x - P_x(v), \qquad (A + \gamma I)\, y^{\text{new}} = \gamma y - P_y(v).$$

The matrix $A + \gamma I$ does not change, so it is factored once.

```pseudo id=main
SNAKE(v, P, α, β, γ, K)                     ▷ v has n ≥ 3 points, γ > 0
L1  A ← α L + β L²
L2  C ← the Cholesky factor of A + γ I      ▷ C Cᵀ = A + γ I
L3  repeat K times
L4      (P_x(v_i), P_y(v_i)) for each point v_i
L5      x ← the solution of C Cᵀ x = γ x − P_x
L6      y ← the solution of C Cᵀ y = γ y − P_y
L7  return v = (x, y)
```

Line L2 is the [Cholesky decomposition](/cholesky-decomposition/) of a symmetric positive definite matrix, and lines L5 and L6 are a forward and a back substitution each. The step is a [backward Euler](/backward-euler-method/) step for the internal force and a forward step for the image force. In the terms of optimization it is a [proximal gradient](/proximal-gradient-method/) step, which is why it decreases the energy.

## Example

**No image energy.** Let $P = 0$, and let $v$ be a circle of radius 5 with $n = 24$ points, with $\alpha = 0.4$, $\beta = 0.2$ and $\gamma = 1$. A circle is an eigenvector of every circulant matrix: $L$ multiplies it by $\mu = 2 - 2\cos(2\pi/24) \approx 0.0681$. So one step scales the circle about its center by $\gamma / (\gamma + \alpha\mu + \beta\mu^2) \approx 0.9726$, and the new radius is about 4.863. Without an image, a snake shrinks.

**A disk.** Take a $33 \times 33$ image with the value 200 inside the disk of radius 8 about $(16, 16)$ and 20 outside. The edge strength $S$ with $\sigma = 2$ is largest at about 8 pixels from the center. Start with a circle of radius 13 with $n = 40$ points, and take $w = 1$, $\alpha = \beta = 0.05$ and $\gamma = 3.5$. The energy is 4.142 at the start, 3.769 after 50 steps, 3.03 after 100 steps and $-35.4$ after 300 steps. Far from the edge, the image force is small and the snake only shrinks slowly. Near the edge it falls into the valley of $P$. After 300 steps all 40 points are at a radius between 7.56 and 7.65. The energy decreases at every step.

**The start matters.** In an image with two disks of radius 6 at $x = 12$ and $x = 36$, a start of radius 10 around either disk finds that disk, and a start of radius 22 around both finds one curve that wraps both disks.

## Correctness

The energy is not convex, so the method does not find a global minimum, and the [proof](proofs/correctness.md) shows the property that it does have. Let the gradient of $P$ be Lipschitz with a constant $\Lambda$ (see the [Lipschitz condition](/lipschitz-condition/)). Then each step from $v$ to $v'$ satisfies

$$E(v') \le E(v) - \left(\gamma - \frac{\Lambda}{2}\right) |v' - v|^2.$$

So for $\gamma > \Lambda / 2$ the energy decreases at every step, strictly unless the curve has stopped. For the spline potential, $\Lambda \le 6.25\, w \max S$, because the sums $\sum_i |b''(t - i)|$ and $\sum_i |b'(t - i)|$ are at most 4 and $1.5$ for every $t$. The energy is bounded below, so the decreases add up to a finite total, $|v' - v| \to 0$, and every limit point of the curve is a stationary point of $E$. The tests check the inequality at every step on the disk and on a smooth analytic potential.

## Complexity

Filling $A$ from the 5 known entries per row costs $\Theta(n^2)$ for a dense matrix. The implementation multiplies $L$ by itself, which costs $\Theta(n^3)$, the same order as the dense Cholesky factorization, which also costs $\Theta(n^3)$ once. Each iteration does $n$ reads of the potential, 16 values of $S$ each, and two dense solves of $\Theta(n^2)$. So $K$ iterations cost $\Theta(n^3 + K n^2)$ in the worst case and in the best case, with $\Theta(n^2)$ space for the factor. The matrix is pentadiagonal with two corner blocks, so a [banded](/banded-matrix/) solver with a low rank correction for the corners, the Woodbury form of the [Sherman-Morrison formula](/sherman-morrison-formula/), makes each step $\Theta(n)$. The dense form is simpler to check and is enough for a few hundred points. The number of iterations depends on the distance from the start to the edge and on $\gamma$, and has no bound in terms of $n$.

## Properties

- **Monotone energy.** With $\gamma > \Lambda / 2$, every step decreases $E$.
- **Local.** The result is a local minimum near the start. The capture range is about the width of the valley of $P$, a few times $\sigma$.
- **Shrinks without an image.** With $P = 0$ the curve shrinks toward its centroid, and the centroid does not move, because the circulant matrix keeps the mean of the points.
- **Smooth and closed.** The curve stays closed, and the stiffness $\beta$ keeps it from having sharp corners. Real corners of objects are rounded.
- **Points slide.** The tension pulls the points to equal spacing along the curve, but nothing keeps them on the same part of the object.
- **Fixed topology.** One snake is one closed curve. It cannot split into two curves or merge with another.

## Variants and improvements

- **Balloon force.** Laurent Cohen added in 1991 a force along the normal that inflates or deflates the curve, so that it can expand to an edge from inside and pass weak edges.
- **Gradient vector flow.** Chenyang Xu and Jerry Prince in 1998 replaced the image force by a smooth field that diffuses the edge gradients into the flat regions. It has a much larger capture range and can pull a curve into concave parts of a boundary.
- **Dynamic programming.** Amini, Weymouth and Jain in 1990 let each point move only to one of the positions of a small window, and found the best choice for all points by [dynamic programming](/dag-dynamic-programming/), as in the [Viterbi algorithm](/viterbi-algorithm/). This allows hard constraints and gives the best curve in the window, at a cost of $\Theta(n m^3)$ per pass for $m$ positions on an open curve, or $\Theta(n m^2)$ when the energy has only the terms of next points.
- **Greedy snakes.** Williams and Shah in 1992 moved each point in turn to the best position of its $3 \times 3$ window, a [greedy](/greedy-algorithm/) method that is fast and simple but has no guarantee of decrease for the whole curve.
- **Geometric active contours.** A curve written as the zero level of a function, with the [level set method](/level-set-method/), can split and merge. The geodesic active contours of Caselles, Kimmel and Sapiro in 1997 use this form with an energy close to that of snakes.
- **Region energies.** The method of Chan and Vese in 2001 uses the means of the image inside and outside the curve in place of the edges. It can find objects without sharp edges.

## When to use it

Use an active contour when you have a good first guess of one object boundary, for example from a user, from the previous frame of a video or from a coarse segmentation, and you want a smooth closed curve that follows the edge with subpixel precision. It is useful in medical images, in the tracking of moving outlines and in interactive tools. If you have no first guess, or the number of objects is unknown, use [watershed segmentation](/watershed-segmentation/), [graph cuts](/image-segmentation-graph-cuts/) or a level set method. If you only need the edge pixels, use the [Canny edge detector](/canny-edge-detector/).

## Pitfalls

- **Too large a step.** With $\gamma \le \Lambda / 2$, the explicit part of the step can overshoot, and the energy can rise and the curve oscillate across the edge. Scale $\gamma$ with the weight $w$ and the maximum of $S$.
- **An image force that is not smooth.** A bilinear interpolation of $S$ has a gradient that jumps at pixel boundaries, so it is not Lipschitz and the guarantee of decrease fails. Use a smooth interpolation, such as the cubic B-spline here, or check the energy and reduce the step.
- **A start far from the edge.** Where $S$ is near 0, the image force is near 0, and the snake only shrinks. It can shrink past a weak edge or to a point. Smooth more, use a balloon force, or start closer.
- **Too much tension.** A large $\alpha$ makes the curve cut through concave parts of the boundary and shrink off the edge.
- **Few points.** With too few points, the curve cannot follow the boundary. With too many, the cost of the dense solve grows as $n^2$ per step. Resample the curve to keep the spacing near one pixel.
- **Weak edges and noise.** A snake stops at any strong edge in its way, including noise and texture.

## Implementations

## History

Michael Kass, Andrew Witkin and Demetri Terzopoulos presented snakes at the first International Conference on Computer Vision in 1987, and published "Snakes: active contour models" in the first volume of the International Journal of Computer Vision in 1988. They described a snake as an energy minimizing spline guided by external constraint forces and influenced by image forces that pull it toward features such as lines and edges, and they gave the semi-implicit scheme with the pentadiagonal matrix. The method started the field of deformable models. Amini and others in 1990 and Williams and Shah in 1992 gave discrete minimizations, Cohen in 1991 the balloon, and Xu and Prince in 1998 gradient vector flow. The level set methods of the 1990s and the Chan-Vese model of 2001 removed the fixed topology.

## References
