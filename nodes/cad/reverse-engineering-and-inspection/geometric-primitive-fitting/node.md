---
tag: 8FSGZT
kind: algorithm
slug: geometric-primitive-fitting
name: Least-squares fitting of spheres, cylinders, cones and tori
aliases:
- faithful primitive fitting
- Lukacs-Martin-Marshall fitting
area: cad/reverse-engineering-and-inspection
level: advanced
summary: Fits spheres, cylinders, cones and tori by minimizing the sum of squared orthogonal distances, with Levenberg-Marquardt steps from an algebraic start.
model: real-ram
complexity:
  vars: {m: the number of points, k: "the number of shape parameters (4 for a sphere, 5 for a cylinder, 6 for a cone, 7 for a torus)", s: the number of iterations}
  time: {worst: Θ(s (m k² + k³))}
  space: {extra: Θ(m k)}
properties: {deterministic: true, recursive: false, exact: false}
history:
  year: 1998
  people: [Gábor Lukács, Ralph R. Martin, A. David Marshall]
  note: They fitted spheres, cylinders, cones and tori by the geometric distance with parameterizations that stay valid as a surface tends to a simpler one, such as a sphere of growing radius tending to a plane.
prereqs: [algebraic-distance-fitting, gauss-newton-algorithm, levenberg-marquardt]
see_also: [taubin-fitting, constrained-primitive-fitting, efficient-ransac-shape-detection, primitive-segmentation, least-squares-reference-feature, circle-fitting, point-cloud-normal-estimation, errors-in-variables-regression]
sources:
  - paper: doi:10.1007/BFb0055697
    title: Gábor Lukács, Ralph Martin and Dave Marshall, Faithful least-squares fitting of spheres, cylinders, cones and tori for reliable segmentation, Computer Vision ECCV 98, Lecture Notes in Computer Science 1406, Springer, 1998, 671 to 686
    locator: the faithful parameterizations of the sphere, cylinder, cone and torus, the approximate distances that tend to the plane distance, the starting values and the Levenberg-Marquardt fit
  - paper: doi:10.6028/jres.103.043
    title: Craig M. Shakarji, Least-squares fitting algorithms of the NIST algorithm testing system, Journal of Research of the National Institute of Standards and Technology 103(6), 1998, 633 to 641
    locator: orthogonal distance fits of lines, planes, circles, spheres, cylinders, cones and tori for coordinate metrology, with their distance functions, parameterizations and the Levenberg-Marquardt method
  - book: isbn:9780387303031
    title: Jorge Nocedal and Stephen J. Wright, Numerical Optimization, second edition, Springer, 2006
    locator: Chapter 10, nonlinear least squares (the Gauss-Newton and Levenberg-Marquardt methods and their local convergence)
---

Geometric primitive fitting finds the sphere, cylinder, cone or torus that minimizes the sum of the squared orthogonal distances from a set of measured points to the surface. The orthogonal (geometric) distance is the length of the shortest segment from a point to the surface, so it is the error a measuring machine sees. It does not depend on how the surface is written, and the fit is invariant under rigid motions of the data. The price is that the problem is nonlinear in the shape parameters, so it is solved iteratively, by [Gauss-Newton](/gauss-newton-algorithm/) or [Levenberg-Marquardt](/levenberg-marquardt/) steps, from a starting value given by a linear [algebraic fit](/algebraic-distance-fitting/) or a [Taubin fit](/taubin-fitting/). For these four surfaces of revolution the distance has a closed form, which makes each step cheap. Lukács, Martin and Marshall (1998) added *faithful* parameterizations: the parameters stay finite and smooth when a cone tends to a cylinder or a sphere of growing radius tends to a plane, so one fit can decide between a primitive and its limit. In [reverse engineering](/reverse-engineering-of-geometric-models/) this step turns each segmented region of a scan into an exact surface of the CAD model, and in inspection it gives the least-squares reference features of a part.

## In plain words

A scanner measures many points on a part, say on a hole. We want the cylinder that the points came from: its axis, and its radius. For any guessed cylinder, each point has a distance to it, measured straight across to the surface. We look for the cylinder that makes the sum of the squared distances as small as possible.

There is no formula that gives this cylinder at once. So we start from a rough guess, found by a fast method that is a little biased, and improve it step by step. Each step looks at how the distances change when the cylinder moves, tilts or grows a little, and moves it the way that makes them smaller. Spheres, cones and doughnut shapes work the same way. A few steps are usually enough.

## The problem

The input is a set of points $x_1, \dots, x_m$ in $\mathbb{R}^3$, usually one region of a [primitive segmentation](/primitive-segmentation/), and a type of surface. The output is the parameters $\theta$ of a surface $S(\theta)$ of that type that minimize
$$ F(\theta) = \sum_{i=1}^{m} d(x_i, S(\theta))^2 , $$
the sum of squared orthogonal distances. This is the geometric distance; the [algebraic fit](/algebraic-distance-fitting/) minimizes the values of an implicit equation and the [Taubin fit](/taubin-fitting/) a first-order approximation of the distance, and both are biased under noise. With independent normal noise of equal size in all directions, the minimizer of $F$ is the maximum likelihood estimate of the surface.

With $w = x - p$, $h = w \cdot u$ and $\rho = \lvert w - h u \rvert$ for a point $p$ and a unit axis $u$, the signed distances are:

| surface | parameters | count | signed distance |
| --- | --- | --- | --- |
| sphere | center $c$, radius $r$ | $4$ | $\lvert x - c \rvert - r$ |
| cylinder | axis $(p, u)$, radius $r$ | $5$ | $\rho - r$ |
| cone | apex $p$, axis $u$, half angle $\alpha$ | $6$ | $\rho \cos \alpha - h \sin \alpha$ |
| torus | center $p$, axis $u$, radii $R > r$ | $7$ | $\sqrt{(\rho - R)^2 + h^2} - r$ |

The cone formula holds for points whose nearest point is not the apex. A line on the axis has four parameters (a point moving along the axis and the length of $u$ do not count), which gives the counts.

## The algorithm

```pseudo id=main
GEOMETRIC-FIT(x_1..x_m, type)
L1  θ ← start from an algebraic or Taubin fit; μ ← μ_0
L2  repeat
L3      r_i ← signed orthogonal distance from x_i to S(θ), for every i
L4      J ← Jacobian of r with respect to the local parameters of θ
L5      solve (Jᵀ J + μ I) Δ = −Jᵀ r
L6      θ' ← θ ⊕ Δ                            ▷ move along the local parameters
L7      if Σ r_i(θ')² < Σ r_i(θ)² then θ ← θ'; μ ← μ / 10
L8      else μ ← 10 μ
L9  until the gain of an accepted step or the step is below a tolerance
L10 return θ
```

**Line L1.** For a sphere the start is the linear algebraic fit of $\lvert x \rvert^2 + b \cdot x + e = 0$. For a cylinder the code tries axis directions spread over the half sphere, fits a circle to the points projected on the plane normal to each, and keeps the best; when the points have normals, as from [normal estimation](/point-cloud-normal-estimation/), the axis is the direction most nearly normal to all of them, the smallest eigenvector of $\sum_i n_i n_i^{\mathsf T}$. Cones and tori need starting values too; the paper of Lukács, Martin and Marshall gives methods for them, which this page does not reproduce, and the code fits spheres and cylinders only.

**Lines L4 and L6, the local parameters.** A cylinder has a point on its axis and a unit direction, six numbers for five degrees of freedom. The code steps in a frame $(u, e_1, e_2)$: two moves of the axis point normal to $u$, two tilts of $u$, and a change of $r$, then puts the axis point back at the projection of the centroid. The Jacobian row of point $i$ is $(-w_1/\rho, -w_2/\rho, -h w_1/\rho, -h w_2/\rho, -1)$ with $w_1 = w \cdot e_1$, $w_2 = w \cdot e_2$. This removes the freedom of sliding along the axis, which would make $J^{\mathsf T} J$ singular.

**Lines L5, L7 and L8.** For $\mu \to 0$ line L5 is a Gauss-Newton step, and for large $\mu$ it is a short step down the gradient. A step is kept only if it lowers the cost; otherwise $\mu$ grows and the next step is shorter. This is the Levenberg form with $\mu I$; Marquardt's form scales by the diagonal of $J^{\mathsf T} J$.

**Faithful parameters.** Writing a sphere by its center fails near a plane: the center runs off to infinity. Lukács, Martin and Marshall write it by its point $\rho n$ nearest the origin, the unit normal $n$ there and the curvature $\kappa = 1/r$. Then
$$ \tfrac{\kappa}{2} \bigl( \lvert x - c \rvert^2 - r^2 \bigr) = \tfrac{\kappa}{2} \lvert x - \rho n \rvert^2 - (x - \rho n) \cdot n = d + \tfrac{\kappa}{2} d^2 $$
for the signed distance $d$. The middle form is smooth at $\kappa = 0$, where it is the distance to the plane $x \cdot n = \rho$, and it equals the true distance up to the term $\kappa d^2 / 2$. The paper treats the cylinder, cone and torus in a similar way, with the plane, the cylinder and the sphere as limits.

## Example

**A spherical cap.** Forty points on a cap of half angle $30$ degrees of the unit sphere, with independent normal noise $\sigma = 0.01$ in each coordinate, $300$ samples, seed 2026. The algebraic fit, which is the start of line L1, has a median radius of $0.950$, and the geometric fit $1.002$. On a small cap the algebraic fit shrinks the sphere, as it shrinks a circle on a short arc, and the geometric fit removes most of that bias.

**A half cylinder without normals.** Sixty points on half of a cylinder of radius $2$ and height $3$ with axis $z$, noise $\sigma = 0.01$, $100$ samples, started from the direction search of line L1 with $400$ directions. The fitted radius had median $1.9998$ and ranged over $[1.9925, 2.0063]$, and the axis was off by a median of $0.15$ degrees and at most $0.41$ degrees.

**Noise-free data.** On points that lie exactly on a sphere, the start is already the sphere (Theorem 2 of the correctness file), and the loop leaves it unchanged. On points that lie exactly on a cylinder, the tests start from the direction search and reach the true cylinder to $10^{-8}$ on random cylinders with rational points; that is measured, not proved.

These numbers are measured on synthetic data.

## Correctness

The correctness file proves:

- **The distance formulas** of the table, by reducing each surface of revolution to its profile in the half plane through the axis and the point.
- **The Jacobians**, including the rows of the local cylinder parameterization.
- **Monotone descent.** $J^{\mathsf T} J + \mu I$ is positive definite for $\mu > 0$, and when the gradient $J^{\mathsf T} r$ is not zero, every large enough $\mu$ gives a step that lowers the cost. So the accepted costs strictly decrease, converge, and the loop stops.
- **Exact recovery of a sphere** from at least four noise-free points that are not coplanar: the algebraic start is the true sphere, where the gradient is zero.
- **The faithful sphere distance** identity above and its plane limit.

Not proved here: that the loop reaches the global minimum. The cost of a cylinder, cone or torus fit has local minima, and the result depends on the start. Near a minimizer with zero residuals and a Jacobian of full rank, Gauss-Newton converges quadratically; that is a standard result in Nocedal and Wright, Chapter 10. The statistical properties of the geometric fit (consistency, and a bias much smaller than that of algebraic fits) are studied for circles in Chernov's book, cited on the [algebraic fit](/algebraic-distance-fitting/) page.

## Complexity

One iteration computes $m$ distances and Jacobian rows in $\Theta(m k)$, forms $J^{\mathsf T} J$ in $\Theta(m k^2)$ and solves a $k \times k$ system in $\Theta(k^3)$, with $k \le 7$. With $s$ iterations the time is $\Theta(s (m k^2 + k^3))$ on the [real RAM](/real-ram/), linear in the number of points; from a good start, $s$ is usually below twenty. The extra space is $\Theta(m k)$ for $J$, or $\Theta(k^2)$ if $J^{\mathsf T} J$ and $J^{\mathsf T} r$ are accumulated row by row. The direction search for a cylinder start costs $\Theta(D m)$ for $D$ directions.

## Properties

- **Geometric.** It minimizes true orthogonal distances, as inspection standards require, and is invariant under rigid motions.
- **Local.** It converges to a local minimum near the start. A bad start, from a wrong segment or too few points, gives a wrong surface with a small cost.
- **Not exact in general.** It is an iterative numerical method; only the sphere on noise-free data has an exact answer from its start.
- **Degenerate cases are real.** A cylinder fitted to a nearly flat patch has a huge radius and a badly determined axis; a cone with a tiny angle is nearly a cylinder. Faithful parameters keep the fit well posed across these limits, and model selection must then decide which type to keep.

## Variants and improvements

- **Fit on the faithful approximate distance first.** Lukács, Martin and Marshall minimize the approximate distance of the identity above, which is cheaper and smooth across the limits, and use the result for the final geometric fit.
- **Orthogonal distance regression of general implicit surfaces.** For surfaces with no closed-form distance, each iteration also computes the foot points, as in the methods collected by Ahn and in [point projection onto a surface](/point-projection-onto-a-surface/).
- **Robust fits.** Replace the squares by a robust loss, or fit only to the inliers found by [RANSAC](/ransac/) and [efficient RANSAC shape detection](/efficient-ransac-shape-detection/).
- **Constraints.** Fitting several primitives together with parallel axes, equal radii or tangency is [constrained primitive fitting](/constrained-primitive-fitting/).
- **Metrology fits.** The NIST algorithm testing system described by Shakarji gives reference orthogonal fits of lines, planes, circles, spheres, cylinders, cones and tori used to test the software of coordinate measuring machines.

## When to use it

Use it as the final fit of every region in [reverse engineering](/reverse-engineering-of-geometric-models/) and for the [least-squares reference feature](/least-squares-reference-feature/) of a measured part, after a fast algebraic or Taubin fit has given the start. Use the algebraic or Taubin fit alone when speed matters more than the last bit of accuracy, for example inside the inner loop of RANSAC.

## Pitfalls

- **Gauge freedom.** Parameterizing a cylinder by a free axis point and a free direction vector makes $J^{\mathsf T} J$ singular; Gauss-Newton then fails or drifts along the axis. Use local parameters, or fix the axis point to the plane through the centroid normal to the axis.
- **Points on the axis.** The distance to a cylinder or a torus is not differentiable on the axis. Real data seldom lie there, but synthetic tests can.
- **Wrong sheet of a cone.** The cone formula is for the half cone of the apex; points behind the apex measure the distance to the apex. Check where the feet lie.
- **A start from too short a patch.** On a cylinder patch of a few degrees the axis direction is poorly determined; the direction search and the normals both become unreliable, and the fit may converge to a plane-like cylinder of huge radius.
- **Reporting the cost as a form error.** The root mean square distance is not the form error of a tolerance, which is a minimum zone value.

## Implementations

## History

Fitting circles and spheres by orthogonal distance is old in metrology and statistics; the algebraic fits of Kasa, Bookstein and Pratt were mainly used to find starting values. In 1998 Lukács, Martin and Marshall gave geometric fits of spheres, cylinders, cones and tori for the segmentation of range data in reverse engineering, with parameterizations that remain valid as one type degenerates into another and approximate distances for good starting values. The same year Shakarji described the orthogonal fits of the NIST algorithm testing system for coordinate measuring machines. Ahn's 2004 monograph treats orthogonal distance fitting of general curves and surfaces.

## References
