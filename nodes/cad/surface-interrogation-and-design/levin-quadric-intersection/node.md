---
tag: NA927X
kind: algorithm
slug: levin-quadric-intersection
name: Levin's quadric intersection method
aliases:
- Levin pencil method
- quadric surface intersection
area: cad/surface-interrogation-and-design
level: advanced
summary: Intersects two quadrics by finding a ruled quadric in their pencil, parameterizing it, and solving a quadratic along each ruling, after Levin in 1976.
solves: [surface-surface-intersection]
model: real-ram
complexity:
  vars: {N: the number of sample values of the ruling parameter u}
  time: {worst: O(N)}
  space: {extra: O(N)}
properties: {deterministic: true, recursive: false, exact: false}
history:
  year: 1976
  people: [Joshua Levin]
  note: Levin intersected quadric patches for the display of solids by finding a member of the pencil of two quadrics with a parametrization linear in one parameter, so that the intersection reduces to one quadratic equation per ruling.
prereqs: [ruled-surface, spectral-theorem, implicit-surface]
see_also: [surface-surface-intersection, algebraic-surface-intersection, implicitization, jacobi-eigenvalue-algorithm, weyls-inequality, homogeneous-coordinates, curve-surface-intersection, tangential-surface-intersection]
sources:
  - paper: doi:10.1145/360349.360355
    title: Joshua Levin, A parametric algorithm for drawing pictures of solid objects composed of quadric surfaces, Communications of the ACM 19(10), 555 to 563, 1976
    locator: the whole paper (the pencil of two quadrics, a member with a parametrization linear in one parameter, and the quadratic equation along each line of it)
  - paper: "L. Dupont, D. Lazard, S. Lazard and S. Petitjean, Near-optimal parameterization of the intersection of quadrics: I. The generic algorithm, INRIA Research Report 5667, 2005"
    title: L. Dupont, D. Lazard, S. Lazard and S. Petitjean, Near-optimal parameterization of the intersection of quadrics, I, The generic algorithm, INRIA Research Report 5667, 2005
    locator: Section 3, Levin's pencil method (Theorem 3.1, the existence of a simple ruled quadric or the empty set in the pencil, the steps of the method, and the sources of numerical trouble)
---

Levin's method computes the intersection curve of two quadric surfaces $S = 0$ and $T = 0$. Every surface $\alpha S + \beta T = 0$ of their *pencil* passes through the curve, and the method picks a member $R$ that is ruled in a simple way: it has a parametrization $p(u) + v \, d(u)$ that is linear in $v$. On each line of $R$ the other quadric becomes a quadratic equation in $v$, so the curve is found by solving one quadratic per value of $u$, in closed form.

## In plain words

Two curved surfaces of the simplest kind, such as a sphere and a cylinder, cross along a curve. Mixing their equations in any proportion gives a new surface that still passes through that curve. Among these mixtures there is always one that is made of straight lines, like a sheet of paper that is bent but not stretched, or a saddle that can be built from straight sticks. The method finds that one.

Now walk along the straight lines of that surface, one by one. Each line meets the other surface in at most two points, and finding them is only a school quadratic equation. Collect the points for many lines and you have the whole curve, as a formula in the line number.

The only hard step is to find the right mixture, and that is a cubic equation.

## The problem

A *quadric* is a surface $Q(x) = x^T Q_u x + 2 q \cdot x + q_0 = 0$ in $\mathbb{R}^3$, stored as the symmetric $4 \times 4$ matrix $Q$ with upper left block $Q_u$, last column $(q, q_0)$, so that $Q(x) = X^T Q X$ for $X = (x, 1)$ in [homogeneous coordinates](/homogeneous-coordinates/). Spheres, ellipsoids, cylinders, cones, paraboloids, hyperboloids and pairs of planes are quadrics. The input is two quadrics $S$ and $T$ that are not multiples of each other, and a list $U$ of sample values. The output is a description of their real intersection curve: a member $R$ of the pencil, its sheets $p(u) + v \, d(u)$, and for each sample $u$ the points of the curve on the line of $u$, at most two per line, or the whole line when it lies in both quadrics. The intersection of two quadrics is a curve of degree at most $4$, so this is the closed form case of [surface surface intersection](/surface-surface-intersection/).

## The algorithm

The quadratic part $\alpha S_u + \beta T_u$ of a member is a symmetric $3 \times 3$ matrix. The method needs a member whose quadratic part is singular and not *semidefinite of rank 2*, that is, not with one zero eigenvalue and two of the same sign. Such a member is a plane, two planes, a hyperbolic or parabolic cylinder, a hyperbolic paraboloid, or empty, a *simple ruled quadric* in Levin's sense. The members with a singular quadratic part are the roots of the cubic $f(\alpha, \beta) = \det(\alpha S_u + \beta T_u)$.

```pseudo id=main
LEVIN(S, T, U)
L1  f ← the binary cubic det(α S_u + β T_u), from its values at four points
L2  C ← the real roots (α, β) of f on the unit circle, or, if f ≡ 0, a zero of the middle eigenvalue of α S_u + β T_u
L3  for each (α, β) ∈ C: R ← α S + β T
L4      G ← S if |β| ≥ |α| else T
L5      if R_u is singular and not semidefinite of rank 2: sheets ← the rulings p(u) + v d(u) of R = 0 from the principal axes of R_u, and stop
L6  for each sheet and each u ∈ U
L7      a ← dᵀ G_u d, b ← 2 d · (G_u p + g), c ← G(p); if a = b = c = 0, record the whole line
L8      for each real root v of a v² + b v + c = 0: output p(u) + v d(u)
L9  return R, its sheets, the points and the lines
```

Line L5 diagonalizes $R_u$ with the [Jacobi eigenvalue algorithm](/jacobi-eigenvalue-algorithm/), completes the squares, and reads the type of $R$ from the signs of the eigenvalues and the linear part. In the principal coordinates $P, Q, w$, a hyperbolic paraboloid is $P^2 - Q^2 + 2 \rho w + c' = 0$, and with $u = P - Q$, $v = P + Q$ it becomes $w = -(u v + c') / (2 \rho)$, linear in $v$. A hyperbolic cylinder $P^2 - Q^2 = k$ uses $P - Q = u$, $P + Q = k / u$ and the free axis $w = v$. A parabolic cylinder $\mu s^2 + 2 n z + c' = 0$ uses $s = u$ and its free axis as $v$. A plane uses two directions in it, with $v$ along a direction on which $G$ is not constant. Line L4 keeps the generator that, with $R$, still defines the same curve. The code also tries the zero of the middle eigenvalue after the roots of $f$, as a guard against rounding. The proof does not need it.

## Example

Intersect the sphere $S = x^2 + y^2 + z^2 - 4$ with the cylinder $T = (x - 1)^2 + y^2 - 1 = x^2 + y^2 - 2x$. The curve is Viviani's curve, a figure eight on the sphere. The quadratic parts are $S_u = I$ and $T_u = \mathrm{diag}(1, 1, 0)$, so

$$f(\alpha, \beta) = \det \mathrm{diag}(\alpha + \beta, \alpha + \beta, \alpha) = \alpha (\alpha + \beta)^2.$$

The root $(0, 1)$ is the cylinder $T$, whose quadratic part $\mathrm{diag}(1, 1, 0)$ is semidefinite of rank 2, so line L5 rejects it. The double root $(1, -1)$ gives

$$R = S - T = z^2 + 2x - 4,$$

with quadratic part $\mathrm{diag}(0, 0, 1)$ of rank 1, a parabolic cylinder. Its rulings are $p(u) = (2 - u^2/2, \, 0, \, u)$ and $d = (0, 1, 0)$: the line of $u$ is the line $z = u$, $x = 2 - u^2/2$ in the direction of $y$. Here $|\beta| \ge |\alpha|$, so $G = S$, and

$$S(p + v d) = v^2 + \left(2 - \tfrac{u^2}{2}\right)^2 + u^2 - 4 = v^2 - u^2 + \tfrac{u^4}{4},$$

so $a = 1$, $b = 0$, $c = u^4/4 - u^2$, and $v = \pm u \sqrt{1 - u^2/4}$, real for $|u| \le 2$. The whole curve is

$$x = 2 - \tfrac{u^2}{2}, \qquad y = \pm u \sqrt{1 - \tfrac{u^2}{4}}, \qquad z = u, \qquad -2 \le u \le 2.$$

| $u$ | $c$ | points |
|---|---|---|
| $0$ | $0$ | $(2, 0, 0)$, a double root, the crossing point of the figure eight |
| $\pm 1$ | $-\tfrac34$ | $(\tfrac32, \pm\tfrac{\sqrt3}{2}, \pm 1)$ |
| $\pm 2$ | $0$ | $(0, 0, \pm 2)$, a double root, the poles |
| $\lvert u \rvert > 2$ | $> 0$ | none |

Each point satisfies both equations: at $(\tfrac32, \tfrac{\sqrt3}{2}, 1)$, $\tfrac94 + \tfrac34 + 1 = 4$ and $\tfrac14 + \tfrac34 = 1$. The code finds the same member, scaled, and the same points; at the crossing point the two roots differ by about $10^{-6}$, the square root of the rounding error of $c$.

## Correctness

The [full proof](proofs/correctness.md) has three parts. First, a member as needed by line L5 always exists, which is Levin's theorem. Let $\lambda_2(\theta)$ be the middle eigenvalue of $\cos\theta \, S_u + \sin\theta \, T_u$. It is continuous in $\theta$, by [Weyl's inequality](/weyls-inequality/), and the member at $\theta + \pi$ is minus the member at $\theta$, so $\lambda_2(\pi) = -\lambda_2(0)$ and $\lambda_2$ has a zero $\theta^*$. There the eigenvalues are $\lambda_1 \le 0 \le \lambda_3$ with the middle one zero, so the quadratic part is singular and either indefinite or of rank at most 1. The point $\theta^*$ is a root of $f$, so line L3 meets it, and if $f \equiv 0$ line L2 computes $\theta^*$ directly.

Second, a member of this kind is one of the simple ruled quadrics or empty, by the [spectral theorem](/spectral-theorem/) and completing squares, and its sheets cover its zero set, with every point on the line of a parameter $u$ that is an affine function of the point. Third, a common zero of $S$ and $T$ is a common zero of $G$ and $R$ and conversely, because line L4 picks the generator whose partner has a coefficient at least $1/\sqrt2$ in $R$. And $G(p + v d)$ is exactly the quadratic of line L7. So for each sample $u$, the output is exactly the intersection on the line of $u$. An empty member means an empty intersection.

What is not proved is the effect of rounding on the roots of $f$ and on the rank decisions. The tests check, for the example, for disjoint spheres, for parallel cylinders where $f \equiv 0$, for one input of each member type, and for $60$ random pairs of quadrics through a common point, that every output point satisfies both quadrics to a relative residual of $10^{-9}$. They also check that more than $100$ points of the intersection, found independently by Newton steps, each lie on a sheet with a root of the quadratic at their $v$, and that for $300$ random pencils some real root of $f$ gives a simple ruled member.

## Complexity

All matrices have fixed size. Line L1 takes four $3 \times 3$ determinants, line L2 finds at most three roots of a cubic by bisection, or runs a bisection on $\theta$ with one $3 \times 3$ eigenvalue problem per step, and line L5 one Jacobi eigenvalue computation per candidate. This is $O(1)$ work for a fixed precision. Each sample $u$ costs $O(1)$ for the quadratic, so the total is $O(N)$ time for $N$ samples, and $O(N)$ space for the output.

The output is more than a set of points: the curve is $p(u) + v_\pm(u) \, d(u)$ with $v_\pm(u) = (-b \pm \sqrt{b^2 - 4ac}) / (2a)$, a closed form in $u$ that can be evaluated anywhere. The points where $b^2 - 4ac = 0$ split the $u$ axis into intervals on which the curve has a fixed number of branches.

## Properties

- **Closed form.** The curve is given by a formula with one square root of a function of $u$ of low degree, polynomial for a paraboloid or a parabolic cylinder, and no iteration on the curve itself.
- **Complete for each line.** Every intersection point on a sampled line is found, and an empty member proves that the intersection is empty.
- **Not rational.** The square root makes the parametrization irrational even when a rational one exists, for example when the curve is singular or splits into conics and lines.
- **Algebraic numbers.** The member comes from a root of a cubic and the sheets from square roots of eigenvalues. In exact arithmetic the numbers grow fast, and in floating point the classification of the member can be wrong near a type boundary.

## Variants and improvements

- **Elliptic cylinders.** An elliptic cylinder is also ruled, by lines parallel to its axis, and a parametrization of the ellipse gives a sheet linear in $v$. The method of this page does not use it, because the theorem does not need it.
- **Enhanced versions.** Wang, Goldman and Tu (2003) added a classification of the curve in the singular and reducible cases, where it can be given by rational functions.
- **Near optimal parametrizations.** Dupont, Lazard, Lazard and Petitjean work in projective space with exact arithmetic and find a member with the smallest possible number of square roots in its coefficients. In the generic case their parametrization has at most one square root more than needed.
- **Geometric special cases.** Many modelers intersect natural quadrics, such as planes, spheres, cylinders and cones, by special geometric formulas, which are faster and more stable for those cases.
- **General surfaces.** For surfaces of higher degree no member with a linear parametrization need exist. Then [algebraic surface intersection](/algebraic-surface-intersection/) or [implicitization](/implicitization/) followed by substitution are the analytic alternatives.

## When to use it

Use it for the intersection of two quadric faces in a solid modeler, where the inputs are often planes, spheres, cylinders and cones, and a closed form curve with all its branches is wanted. It also gives the number of branches over each interval of $u$, from the sign of $b^2 - 4ac$. For two natural quadrics in special position, prefer the geometric formulas, and for exact results with rational input, prefer the projective method of Dupont and others.

## Pitfalls

- **Wrong type near a boundary.** In floating point a member with a nearly zero eigenvalue can be classified as the wrong type, for example a nearly parabolic cylinder as a hyperbolic one, and then the sheets are wrong. Use a tolerance relative to the size of the matrix, and prefer members whose eigenvalues are well separated from zero.
- **Double roots.** At a tangency or a crossing point of the curve, $b^2 - 4ac$ is zero and rounding makes it slightly negative or positive. Clamp small negative values to zero, and expect the two branches to separate by about the square root of the rounding error.
- **The wrong partner.** If $R$ is almost a multiple of $S$ and the code uses $S$ as the partner, the two equations are almost the same, and the points are poorly fixed. Line L4 avoids this by taking the generator with the smaller coefficient in $R$.
- **Lines of the curve.** When the curve contains a line of a sheet, $a = b = c = 0$ for one value of $u$ only, and sampling misses it. A curve that contains a line is reducible, and the exact methods detect such cases from the multiple roots of $\det(\alpha S + \beta T)$.
- **The sampling in u.** Near the ends of a branch, where $b^2 - 4ac$ goes to zero, the points crowd in $u$ but spread in space, like $\sqrt{u - u_0}$. Refine the samples there, or use the ends as extra samples.

## Implementations

## History

Levin (1976) gave the pencil method as part of an algorithm to draw pictures of solids bounded by quadric patches, and extended it in 1979 into a method for the intersection of any two quadrics, with an analysis of the pencil. His method was for a long time the only general one. Later work studied its weak points: the classification by Wilf and Manor with the Segre characteristic, the enhancement of Wang, Goldman and Tu (2003) for singular and reducible curves, and the exact projective algorithm of Dupont, Lazard, Lazard and Petitjean, which gives near optimal parametrizations and removes the numerical trouble of the floating point method.

## References
