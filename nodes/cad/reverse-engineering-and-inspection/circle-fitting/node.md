---
tag: 33N1KW
kind: problem
slug: circle-fitting
name: Circle fitting
aliases:
- least-squares circle fit
- Kasa fit
- Pratt fit
area: cad/reverse-engineering-and-inspection
level: core
summary: Fit a circle to measured points in a plane by least squares of the orthogonal distances, or of an algebraic residual. It is the base of hole and roundness measurement.
prereqs: [least-squares-approximation, algebraic-distance-fitting]
see_also: [taubin-fitting, geometric-primitive-fitting, least-squares-reference-feature, minimum-width-annulus, minimum-enclosing-circle, form-error-evaluation, gauss-newton-algorithm, ransac]
sources:
  - book: isbn:9781439835906
    title: Nikolai Chernov, Circular and Linear Regression, Fitting Circles and Lines by Least Squares, CRC Press, Monographs on Statistics and Applied Probability 117, 2010
    locator: Chapter 3 (theory of the geometric circle fit, nonexistence of a minimum, local minima), Chapter 4 (geometric fits by Gauss-Newton, Levenberg-Marquardt, Späth and Landau), Chapter 5 (algebraic fits of Kåsa, Pratt and Taubin), Chapters 6 and 7 (statistical analysis and bias)
  - paper: doi:10.1109/TIM.1976.6312298
    title: István Kåsa, A circle fitting procedure and its error analysis, IEEE Transactions on Instrumentation and Measurement IM-25(1), 1976, 8 to 14
    locator: the linear least-squares fit of x^2 + y^2 + D x + E y + G = 0 and its error analysis
  - paper: doi:10.1145/37402.37420
    title: Vaughan Pratt, Direct least-squares fitting of algebraic surfaces, Computer Graphics 21(4) (SIGGRAPH 87), 1987, 145 to 152
    locator: the algebraic fit of circles and spheres with the normalization B^2 + C^2 - 4AG = 1, which also allows lines and planes
  - paper: doi:10.1007/BF01934268
    title: Walter Gander, Gene H. Golub and Rolf Strebel, Least-squares fitting of circles and ellipses, BIT Numerical Mathematics 34(4), 1994, 558 to 578
    locator: algebraic and geometric circle fits, the Gauss-Newton method for the geometric fit, and examples where the algebraic fit is far from the geometric one
  - paper: doi:10.6028/jres.103.043
    title: Craig M. Shakarji, Least-squares fitting algorithms of the NIST algorithm testing system, Journal of Research of the National Institute of Standards and Technology 103(6), 1998, 633 to 641
    locator: the orthogonal least-squares circle and its use in testing coordinate measuring machine software
---

Circle fitting is the problem of finding the circle that best matches a set of points measured in a plane. The usual meaning of "best" is least squares of the orthogonal distances from the points to the circle, the geometric fit. Algebraic fits instead minimize the residuals of an equation of the circle, which is linear in the unknowns and has a closed form, but they are biased. In inspection, the least-squares circle of points measured in a section of a hole gives its center and diameter, and the zone about it gives an upper bound of roundness. This page states the problem and its known facts. The algebraic method with a fixed coefficient, the normalized algebraic methods and their bias are on [algebraic distance fitting](/algebraic-distance-fitting/), the first-order distance method is on [Taubin fitting](/taubin-fitting/), and the iterative geometric method is on [geometric primitive fitting](/geometric-primitive-fitting/). Roundness itself, the minimum zone, is the [minimum width annulus](/minimum-width-annulus/).

## In plain words

A machine touches a few points inside a drilled hole. We want the circle the points came from: its center, to check where the hole is, and its radius, to check its size. No circle passes through all points exactly, because of small errors. So for each candidate circle we measure how far each point is from it, square those gaps and add them. The best circle makes that sum smallest.

There is no formula for that circle. A shortcut uses a different measure of the gap that leads to a simple formula. The shortcut is exact when the points have no error, and it is good when the points go all the way around. When the points cover only a short arc, it tends to give a circle that is too small, so we use it as a first guess and then improve the circle step by step.

## Definition

The input is $n \ge 3$ points $x_i = (x_i, y_i)$ in the plane, not all on one line. A circle has a center $c = (a, b)$ and a radius $r > 0$.

**The geometric problem.** Minimize
$$ F(a, b, r) = \sum_{i=1}^{n} \bigl( \lvert x_i - c \rvert - r \bigr)^2 , $$
the sum of squared orthogonal distances. Under independent normal noise of equal variance in both coordinates, the minimizer is the maximum likelihood estimate of the circle.

**Algebraic problems.** Write the circle as $A(x^2 + y^2) + B x + C y + G = 0$. An algebraic fit minimizes $\sum_i (A(x_i^2 + y_i^2) + B x_i + C y_i + G)^2$ under a normalization of the coefficients. With $A = 1$ the problem is linear least squares in $B, C, G$, as in the method of Kåsa (1976). With the normalization $B^2 + C^2 - 4AG = 1$ of Pratt (1987), the fit is invariant under rigid motions and also allows lines ($A = 0$). Taubin's normalization uses the mean squared gradient. The algebraic residual is related to the orthogonal distance $\delta_i = \lvert x_i - c \rvert - r$ by the identity
$$ \lvert x_i - c \rvert^2 - r^2 = \delta_i (\delta_i + 2r), $$
so for small $\delta_i$ the method with $A = 1$ weighs the squared distance by about $4 r^2$, and a smaller circle has a smaller cost.

## Variants

- **Fixed center or fixed radius.** With the center fixed, the best radius is the mean of the distances $\lvert x_i - c \rvert$, since $F$ is a quadratic in $r$ with derivative $-2 \sum_i (\lvert x_i - c \rvert - r)$. With the radius fixed (a gauge pin of known size), only the center is fitted.
- **Circles in space.** Points measured on a circle in space are first fitted by a plane, the [least-squares reference feature](/least-squares-reference-feature/), then projected onto it and fitted by a circle.
- **Spheres and cylinders.** The same objectives in three dimensions; see [geometric primitive fitting](/geometric-primitive-fitting/).
- **Other references for round features.** The minimum zone (Chebyshev) circle pair is the [minimum width annulus](/minimum-width-annulus/); the minimum circumscribed circle, for a shaft, is the [minimum enclosing circle](/minimum-enclosing-circle/); the maximum inscribed circle, for a hole, is a largest empty circle with its center inside the hull of the points.
- **Robust fits.** With outliers, fit to the inliers found by [RANSAC](/ransac/) or minimize a robust loss.
- **Weighted fits.** When points have different uncertainties, weight each squared distance by the inverse variance.

## Examples

**Noise-free points.** Three or more points on one circle, not all equal, determine it. Every algebraic fit has the cost $0$ at the true circle and returns it, and the geometric fit has the cost $0$ there too. So all the methods agree on exact data.

**A short noisy arc.** Seven points every $10$ degrees on an arc of $60$ degrees of the unit circle, moved radially by $-0.02$ and $+0.02$ in turn. The linear algebraic method of Kåsa returns the radius $0.814$, and the geometric fit, started from it, $0.891$. The geometric cost of the geometric fit, $0.00244$, is below the cost $0.0028$ of the true circle: on a short arc the data cannot tell the radius well, and every least-squares fit can move far from the truth. The algebraic fit moves further toward a small circle. The tests of the [least-squares reference feature](/least-squares-reference-feature/) page check these values. A statistical study of this bias with many samples is on the [algebraic distance fitting](/algebraic-distance-fitting/) page.

**A full circle.** For points spread around the whole circle with small noise, the algebraic and geometric fits are close, since shrinking the circle then increases the residuals on all sides.

## Known algorithms

- **The linear method of Kåsa.** Least squares of $x^2 + y^2 + D x + E y + G$, a $3 \times 3$ linear system, $O(n)$ time. Invariant under rigid motions, exact on noise-free data, biased toward small circles on short arcs. On [algebraic distance fitting](/algebraic-distance-fitting/).
- **The normalized method of Pratt.** A generalized eigenvalue problem of size $4$, $O(n)$ time, includes lines. On [algebraic distance fitting](/algebraic-distance-fitting/).
- **Taubin's method.** The first-order approximation of the geometric distance, also a small generalized eigenvalue problem, with a much smaller bias. On [Taubin fitting](/taubin-fitting/).
- **The hyper method** of Al-Sharadqah and Chernov, a normalization that removes the leading term of the bias, in Chernov's book.
- **Geometric fits.** [Gauss-Newton](/gauss-newton-algorithm/) or Levenberg-Marquardt steps on the orthogonal residuals, started from an algebraic fit, $O(n)$ time per step; also the alternating methods of Späth and of Landau, which update the center with the radius fixed at the mean distance. On [geometric primitive fitting](/geometric-primitive-fitting/), with the details in Chernov's Chapter 4 and in Gander, Golub and Strebel.

## Bounds

- **Time.** All the algebraic fits take $\Theta(n)$ time and $O(1)$ extra space: accumulate the moments of the data, then solve a fixed-size system. Each geometric step is $\Theta(n)$ too.
- **Existence and uniqueness of the geometric fit.** The geometric cost need not have a minimum among circles: when the best fit is a line, circles of growing radius approach it. It can also have several local minima. Chernov's Chapter 3 studies both effects; with lines added as limit circles a minimum exists.
- **Bias.** Under small noise, the algebraic fit with $A = 1$ has a bias toward smaller radii that grows as the arc gets shorter; the Pratt and Taubin fits have smaller biases, and the geometric fit smaller still. The expansions in powers of the noise level are in Chernov's Chapters 6 and 7. The identity above explains the direction of the bias with $A = 1$.
- **Zone width.** For any fitted circle, the region between the extreme distances from its center is a ring that holds all points, so its width is never smaller than the roundness (the minimum width annulus).

## Reductions

- **The method with $A = 1$ is linear least squares** in three unknowns, so it reduces to a $3 \times 3$ system or a QR factorization of an $n \times 3$ matrix.
- **The normalized algebraic fits reduce to a generalized eigenvalue problem** of size $4$ on the matrix of moments.
- **The geometric fit is a nonlinear least-squares problem** in three unknowns. Eliminating $r$ by the mean distance leaves a problem in the center alone: minimize $n$ times the variance of the distances $\lvert x_i - c \rvert$.
- **Roundness is a different problem**, a minimax problem in the center, solved exactly through Voronoi diagrams on the [minimum width annulus](/minimum-width-annulus/) page.

## Applications

- **Holes and shafts on a measuring machine.** The center gives the position of a hole for location tolerances, and the radius its size; the [CAD-based inspection](/cad-based-inspection/) workflow uses the least-squares circle unless the drawing asks for another reference.
- **Roundness reference.** The zone about the least-squares center is the least-squares roundness value, an upper bound of the minimum zone value; see [form error evaluation](/form-error-evaluation/).
- **Reverse engineering.** Fillets, arcs and partial holes in scanned sections, often short arcs, where the start from an algebraic fit must be refined.
- **Other fields.** Circle fits are also used for the tracks of charged particles in a magnetic field and for arcs in images; Chernov's introduction surveys such uses.

## References
