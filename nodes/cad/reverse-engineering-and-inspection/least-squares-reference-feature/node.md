---
tag: 5ETC50
kind: technique
slug: least-squares-reference-feature
name: Least-squares reference feature
aliases:
- Gaussian association
- Gaussian reference element
area: cad/reverse-engineering-and-inspection
level: core
summary: Fits the ideal feature that minimizes the sum of squared deviations, an option in standards beside the minimum zone. It is simpler, and its zone is never narrower than the minimum zone.
prereqs: [least-squares-approximation, rayleigh-quotient, form-error-evaluation]
see_also: [minimum-zone-flatness, minimum-zone-cylindricity, circle-fitting, geometric-primitive-fitting, principal-component-analysis, errors-in-variables-regression, datum-reference-frame, algebraic-distance-fitting]
sources:
  - paper: doi:10.1080/14786440109462720
    title: Karl Pearson, On lines and planes of closest fit to systems of points in space, The London, Edinburgh, and Dublin Philosophical Magazine and Journal of Science, Series 6, 2(11), 1901, 559 to 572
    locator: the line and the plane of least summed squared perpendicular distances through the centroid, along the principal axes of the ellipsoid of the data
  - paper: doi:10.6028/jres.103.043
    title: Craig M. Shakarji, Least-squares fitting algorithms of the NIST algorithm testing system, Journal of Research of the National Institute of Standards and Technology 103(6), 1998, 633 to 641
    locator: the orthogonal least-squares fits of lines, planes, circles, spheres, cylinders, cones and tori used to test coordinate measuring machine software
  - book: isbn:9781439835906
    title: Nikolai Chernov, Circular and Linear Regression, Fitting Circles and Lines by Least Squares, CRC Press, Monographs on Statistics and Applied Probability 117, 2010
    locator: Chapter 2 (fitting lines), Chapter 4 (geometric circle fits by Gauss-Newton and Levenberg-Marquardt) and Chapter 5 (algebraic circle fits used as starting points)
  - paper: doi:10.1109/TIM.1976.6312298
    title: István Kåsa, A circle fitting procedure and its error analysis, IEEE Transactions on Instrumentation and Measurement IM-25(1), 1976, 8 to 14
    locator: the linear circle fit used here as the start of the geometric circle fit
  - book: isbn:9780387303031
    title: Jorge Nocedal and Stephen J. Wright, Numerical Optimization, second edition, Springer, 2006
    locator: Chapter 10, nonlinear least squares (Gauss-Newton and Levenberg-Marquardt)
  - url: https://www.iso.org/standard/66777.html
    title: ISO 1101:2017, Geometrical product specifications (GPS), Geometrical tolerancing, Tolerances of form, orientation, location and run-out, fourth edition
    locator: the standard as a whole (form tolerance zones, against which the least-squares zone is an upper bound); no clause is quoted
---

A least-squares reference feature is the ideal line, plane, circle, sphere or cylinder that minimizes the sum of the squared orthogonal deviations of the measured points from it. In metrology this is the Gaussian association. Coordinate measuring machine software uses it to report the position, orientation and size of a feature, to set up datums, and to report a form error as the width of the zone between the largest and the smallest deviation from the fitted feature. That width is never smaller than the minimum zone form error, because the least-squares feature is one of the features over which the minimum zone is taken. The minimum zone is the definition of a form tolerance, the problem is [form error evaluation](/form-error-evaluation/), and its exact methods are [minimum zone flatness](/minimum-zone-flatness/) and [minimum zone cylindricity](/minimum-zone-cylindricity/). This page is the least-squares alternative and how to compute it.

## In plain words

We have points measured on a face that should be flat. We want one plane that represents the face. For any plane, each point is a little above or below it. Square those distances and add them up. The best plane makes that sum as small as possible. It passes through the center of mass of the points and lies along the directions in which the points spread most.

The plane is stable: moving one point a little moves the plane a little. It is also cheap to compute. Its disadvantage is that it does not give the thinnest pair of parallel planes around the points. If we put two planes parallel to it through the highest and lowest points, the gap is a correct but sometimes pessimistic flatness value. Lines and circles work the same way.

## When it applies

- A feature of known type is measured by many points, and a smooth, repeatable reference is wanted: the center of a bore, the axis of a shaft, the normal of a face, a datum plane.
- The noise in the points is random and of similar size in all directions. Then the least-squares feature is the maximum likelihood estimate of the ideal feature.
- A form value is wanted fast, and an upper bound is acceptable, or the drawing asks for the Gaussian association.

It does not apply when the tolerance must be checked against the minimum zone without a margin, and it is a poor choice when the data have outliers.

## The template

1. **Choose the feature and its deviation.** The parameters $\theta$ of the ideal feature and the signed orthogonal deviation $e_i(\theta)$ of each point: $u \cdot x_i - d$ for a plane with unit normal $u$, $\lvert x_i - c \rvert - r$ for a circle or a sphere, the distance to the axis minus $r$ for a cylinder.
2. **Minimize** $S(\theta) = \sum_i e_i(\theta)^2$.
3. **Report** the feature $\theta_{\mathrm{LS}}$, the root mean square deviation $\sqrt{S/n}$, and the least-squares zone, the region between the levels $\min_i e_i$ and $\max_i e_i$, of width $W_{\mathrm{LS}} = \max_i e_i(\theta_{\mathrm{LS}}) - \min_i e_i(\theta_{\mathrm{LS}})$.

**The zone is never narrower than the minimum zone.** For each $\theta$ the zone between the extreme deviations holds all points and has the shape of the tolerance zone, so its width is at least the minimum over $\theta$, which is the minimum zone form error $E$. In particular $W_{\mathrm{LS}} \ge E$. Equality holds when $\theta_{\mathrm{LS}}$ also minimizes the zone width, for example on noise-free points, where both are $0$.

**Plane: the smallest eigenvector.** Let $\bar x$ be the centroid and $C = \sum_i (x_i - \bar x)(x_i - \bar x)^{\mathsf T}$ the scatter matrix. For a fixed unit normal $u$, $S = \sum_i (u \cdot x_i - d)^2$ is a quadratic in $d$ with derivative $-2 \sum_i (u \cdot x_i - d)$, so the best offset is $d = u \cdot \bar x$: the plane passes through the centroid. Then $S(u) = \sum_i (u \cdot (x_i - \bar x))^2 = u^{\mathsf T} C u$. Over unit vectors this is the [Rayleigh quotient](/rayleigh-quotient/) of $C$, whose minimum is the smallest eigenvalue $\lambda_1$, attained at its eigenvector. So the least-squares plane passes through the centroid with the normal of the smallest eigenvector of $C$, and $S = \lambda_1$. This is Pearson's result of 1901, and it is the same computation as [principal component analysis](/principal-component-analysis/).

**Line: the largest eigenvector.** For a line through $\bar x$ with unit direction $u$, the squared distance of $x_i$ is $\lvert x_i - \bar x \rvert^2 - (u \cdot (x_i - \bar x))^2$. The first term does not depend on $u$, so the best $u$ maximizes $u^{\mathsf T} C u$ and is the largest eigenvector; the best line passes through the centroid by the same argument as for the plane, applied in the plane normal to $u$. In two dimensions the angle has the closed form $\tfrac12 \operatorname{atan2}(2 S_{xy}, S_{xx} - S_{yy})$.

**Circle, sphere and cylinder: iterate.** There is no closed form. The code starts from the linear fit of Kåsa, which minimizes the algebraic residuals of $x^2 + y^2 + D x + E y + G = 0$ by a $3 \times 3$ linear system, and improves it with Levenberg-Marquardt steps on the orthogonal residuals $\lvert x_i - c \rvert - r$, keeping a step only if it lowers $S$. At a minimum the derivative in $r$ gives $\sum_i e_i = 0$: the fitted radius is the mean distance from the center. The details and the bias of the algebraic start are on [circle fitting](/circle-fitting/) and [geometric primitive fitting](/geometric-primitive-fitting/).

## Classic examples

**Straightness.** The points $(0,0), (1,0), (2,0), (3,0), (4,1)$ have the centroid $(2, 0.2)$ and $S_{xx} = 10$, $S_{xy} = 2$, $S_{yy} = 0.8$. The least-squares line has slope about $0.208$, and the strip between the extreme deviations from it has the width $0.7754$. The minimum zone strip, through $(0,0)$ and $(4,1)$ and the parallel line through $(3,0)$, has the width $3/\sqrt{17} \approx 0.7276$. The least-squares value overstates straightness by about $7$ percent here.

**Flatness of a plate.** For a nearly flat plate the least-squares plane and the minimum zone planes are nearly parallel, and the least-squares zone is often close to the minimum zone. How close depends on the data; the tests on this page check only that it is never smaller.

**Datum planes and axes.** A primary datum plane is often taken as a least-squares plane of the datum face, or as a constrained fit of it, and an axis as the axis of a least-squares cylinder. The [datum reference frame](/datum-reference-frame/) page describes how datums are built from them.

**Center of a bore.** The least-squares circle of points on a hole gives the center used for position tolerances. Its zone gives a roundness upper bound, compared with the exact [minimum width annulus](/minimum-width-annulus/).

## Variations

- **Vertical regression** minimizes $\sum_i (z_i - a x_i - b y_i - c)^2$. It is a linear least-squares problem, but it is not invariant under rotation and is biased when $x$ and $y$ carry errors too; see [errors-in-variables regression](/errors-in-variables-regression/). For a tilted surface it gives a different plane from the orthogonal fit.
- **Minimum zone (Chebyshev) association** minimizes the largest deviation instead of the sum of squares, and gives the form error itself.
- **Minimum circumscribed and maximum inscribed features** fit the smallest circle or cylinder around the points, or the largest inside them, as for a shaft or a hole that must mate.
- **Weighted and robust fits** reduce the effect of outliers or of points with larger uncertainty.
- **Constrained fits** force parallel axes, equal radii or a fixed direction across several features; see [constrained primitive fitting](/constrained-primitive-fitting/).
- **Algebraic fits** such as the [algebraic distance fit](/algebraic-distance-fitting/) and the [Taubin fit](/taubin-fitting/) are faster and noniterative, but they do not minimize the orthogonal deviations and they are biased.

## Pitfalls

- **Reporting the zone width as the form error.** The least-squares zone width is an upper bound. A part can fail a tolerance by the least-squares value and pass it by the minimum zone. The converse cannot happen.
- **Reporting the RMS deviation as the form error.** The root mean square deviation is smaller than the zone width and is not a tolerance value.
- **Non-unique fits.** If the scatter matrix has a repeated smallest eigenvalue, every normal in its eigenspace is optimal. For the four vertices of a regular tetrahedron the scatter matrix is a multiple of the identity, so every plane through the centroid is a least-squares plane. Their zones range from $1$ to $2/\sqrt 3$ for a tetrahedron of edge $\sqrt 2$.
- **Short arcs.** A circle fitted to a short arc has a poorly determined radius and center, and the algebraic start is biased toward a smaller radius; see [circle fitting](/circle-fitting/).
- **Cancellation.** Compute the scatter matrix from centered coordinates, and compute a distance to a line from the perpendicular component, not as the difference of two large squares.
- **Outliers.** One wrong point moves the fit and widens the zone. Filter the data, or use a robust fit, before the evaluation.

## Exercises

1. Show that the least-squares line of points in the plane passes through the centroid, and derive the closed form of its angle from the $2 \times 2$ scatter matrix.
2. For the straightness example above, find the extreme deviations from the least-squares line and check the value $0.7754$.
3. Give four points in a plane whose least-squares line is not unique. What do the least-squares zones of the different optimal lines measure?
4. Prove that the least-squares radius of a circle with a fixed center is the mean distance of the points from the center.
5. Give a set of five points in the plane whose least-squares straightness equals its minimum zone straightness, though the points are not collinear. Then move one point so that the two values differ.

## References
