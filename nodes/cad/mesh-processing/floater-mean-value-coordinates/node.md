---
tag: VWYQAM
kind: definition
slug: floater-mean-value-coordinates
name: Mean value coordinates
aliases:
- Floater mean value coordinates
area: cad/mesh-processing
level: advanced
summary: Floater's weights from the tangents of half angles that express a point as a convex combination of polygon vertices, used for shape preserving parameterization.
prereqs: [convex-combination, convex-polygon]
see_also: [tutte-embedding, mesh-parameterization, cotangent-laplacian, least-squares-conformal-maps, point-in-polygon, laplacian-matrix]
sources:
  - paper: doi:10.1016/S0167-8396(03)00002-5
    title: Michael S. Floater, Mean value coordinates, Computer Aided Geometric Design 20(1), 2003, 19 to 27
    locator: the definition from the mean value theorem for harmonic functions, the proof that the weights are positive and reproduce linear functions, and their use for parameterization
  - paper: doi:10.1145/1183287.1183295
    title: Kai Hormann and Michael S. Floater, Mean value coordinates for arbitrary planar polygons, ACM Transactions on Graphics 25(4), 2006, 1424 to 1441
    locator: the extension to points outside the kernel and to non-convex polygons with signed angles, where weights can be negative
  - paper: doi:10.1007/3-540-26808-1_9
    title: Michael S. Floater and Kai Hormann, Surface parameterization, a tutorial and survey, in Advances in Multiresolution for Geometric Modelling, Springer, 2005, 157 to 186
    locator: the comparison of uniform, harmonic, shape-preserving and mean value weights for barycentric mappings
---

Mean value coordinates are a way to write a point $v_0$ inside a star-shaped polygon $v_1, \ldots, v_d$ as a [convex combination](/convex-combination/) of the corners, $v_0 = \sum_i \lambda_i v_i$ with $\lambda_i > 0$ and $\sum_i \lambda_i = 1$. Michael Floater defined them in 2003 by a closed formula in the angles at $v_0$ and the distances to the corners. For a triangle they are the barycentric coordinates. For more corners there are many convex combinations that give $v_0$, and these are one choice that depends smoothly on the points and is always positive when $v_0$ sees every corner. Floater made them as weights for the [Tutte embedding](/tutte-embedding/) of a triangle mesh: they are positive, so the map has no flipped triangle, and they reproduce a planar mesh exactly. The name comes from the mean value property of harmonic functions, which the formula imitates.

## Definition

Let $v_1, \ldots, v_d$, $d \ge 3$, be the corners of a polygon in counterclockwise order, with indices taken mod $d$, and let $v_0$ be a point in the interior of its *kernel*, the set of points from which every corner and edge is visible. Write $r_i = \lVert v_i - v_0 \rVert > 0$, and let $\alpha_i \in (0, \pi)$ be the angle at $v_0$ in the triangle $(v_0, v_i, v_{i+1})$. The *mean value weights* and *mean value coordinates* of $v_0$ are

$$w_i = \frac{\tan(\alpha_{i-1}/2) + \tan(\alpha_i/2)}{r_i}, \qquad \lambda_i = \frac{w_i}{\sum_{j=1}^d w_j}.$$

With $d_i = v_i - v_0$, the half-angle tangent has a formula without trigonometric functions:

$$\tan\frac{\alpha_i}{2} = \frac{d_i \times d_{i+1}}{r_i r_{i+1} + d_i \cdot d_{i+1}},$$

where $d_i \times d_{i+1}$ is the [orientation test](/orientation-test/) value $d_{i,x} d_{i+1,y} - d_{i,y} d_{i+1,x}$. The numerator is positive because $v_0$ is in the kernel, and the denominator is positive because $\alpha_i < \pi$.

**Properties.** The coordinates are defined by a formula, with no system to solve.

1. *Positive*: $\alpha_i \in (0, \pi)$ gives $\tan(\alpha_i / 2) > 0$, so $w_i > 0$ and $\lambda_i > 0$.
2. *Partition of unity*: $\sum_i \lambda_i = 1$ by the definition.
3. *Linear reproduction*: $\sum_i \lambda_i v_i = v_0$, so $\sum_i \lambda_i f(v_i) = f(v_0)$ for every affine function $f$.
4. *Smooth*: the $\lambda_i$ are smooth functions of $v_0, \ldots, v_d$ in the set where they are defined, and they do not change under a similarity of the plane.

*Proof of 3.* Put $v_0 = 0$ and let $e(\theta) = (\cos \theta, \sin \theta)$. Let $e_i = d_i / r_i$ be the unit vector to $v_i$. The sector between $e_i$ and $e_{i+1}$ has angle $\alpha_i$, and the integral of $e(\theta)$ over it is $\tan(\alpha_i/2)\,(e_i + e_{i+1})$: after a rotation that puts $e_i$ at angle $0$, the integral is $(\sin \alpha_i, 1 - \cos \alpha_i)$, and $\tan(\alpha_i/2)(1 + \cos \alpha_i, \sin \alpha_i)$ is the same vector by the half-angle formulas. Because $v_0$ is in the kernel, the sectors cover the circle once, so their integrals add up to $\int_0^{2\pi} e(\theta)\, d\theta = 0$. Collect the terms of each $e_i$: it appears in sectors $i-1$ and $i$, so $\sum_i (\tan(\alpha_{i-1}/2) + \tan(\alpha_i/2))\, e_i = 0$, that is $\sum_i w_i d_i = 0$. Divide by $\sum_j w_j > 0$. $\square$

**On a surface.** For a vertex $v_0$ of a triangle mesh in 3D with neighbours $v_1, \ldots, v_d$ in the order of its 1-ring, Floater uses the same formula with the angles $\alpha_i$ of the 3D triangles at $v_0$. The weights are still positive. They do not depend on a flattening of the ring, and if the ring is planar they are the planar coordinates above.

## Examples and non-examples

**An exact example.** Take $v_0 = (0, 0)$ and the corners $(3, 4)$, $(-5, 12)$, $(-8, -15)$, $(7, -24)$, whose distances $5, 13, 17, 25$ are integers. Then every quantity is rational.

| $i$ | $d_i \times d_{i+1}$ | $d_i \cdot d_{i+1}$ | $\tan(\alpha_i/2)$ | $\alpha_i$ |
|---|---|---|---|---|
| 1 | $56$ | $33$ | $56/98 = 4/7$ | $59.49°$ |
| 2 | $171$ | $-140$ | $171/81 = 19/9$ | $129.31°$ |
| 3 | $297$ | $304$ | $297/729 = 11/27$ | $44.33°$ |
| 4 | $100$ | $-75$ | $100/50 = 2$ | $126.87°$ |

The angles add up to $360°$. The weights are $w = (18/35, 13/63, 4/27, 13/135)$, for example $w_1 = (2 + 4/7)/5$, and the coordinates are

$$\lambda = \left(\tfrac{81}{152}, \tfrac{65}{304}, \tfrac{35}{228}, \tfrac{91}{912}\right).$$

They are positive, they add up to 1, and $\sum_i \lambda_i d_i = (0, 0)$ exactly. Uniform weights $1/4$ give $\sum_i d_i / 4 = (-3/4, -23/4) \ne 0$, so uniform weights do not reproduce this planar star, and a Tutte map with them moves $v_0$.

**A triangle.** For $d = 3$ the coordinates are the barycentric coordinates, because three positive numbers with sum 1 and $\sum \lambda_i v_i = v_0$ are unique for a nondegenerate triangle.

**A point outside the kernel.** If $v_0$ is inside a non-convex polygon but does not see every corner, some triangle $(v_0, v_i, v_{i+1})$ is clockwise. With unsigned angles the weights stay positive, but the sectors no longer cover the circle once, and the proof of property 3 fails: the result is not $v_0$. Hormann and Floater (2006) use signed angles instead. Then the formula reproduces linear functions for every point that is not on the boundary, but some $\lambda_i$ can be negative, and the coordinates are no longer a convex combination.

**Cotangent weights are not always positive.** The discrete harmonic weights $\cot \alpha + \cot \beta$ of the [cotangent Laplacian](/cotangent-laplacian/) also reproduce linear functions, but a weight is negative when the two angles opposite an edge add up to more than $\pi$. Mean value weights are positive for every star in the kernel case, which is why they suit the Tutte embedding.

## Related definitions

- **Barycentric coordinates.** The case $d = 3$, and the model for all generalized barycentric coordinates: positive, a partition of unity, linear reproduction.
- **Wachspress coordinates.** Rational functions of $v_0$ for convex polygons, with weights from the areas of the triangles at the corners. They are not defined for non-convex polygons, where mean value coordinates still are.
- **Discrete harmonic coordinates.** The cotangent weights; they come from the minimum of the Dirichlet energy and can be negative.
- **Mean value coordinates in 3D.** Ju, Schaefer and Warren (2005) and Floater, Kós and Reimers (2005) gave the same idea for a point inside a closed triangle mesh, with an integral over the unit sphere. They are used to deform a shape with a cage.
- **Convex combination maps.** A [Tutte embedding](/tutte-embedding/) with any positive weights; mean value weights are the most common choice for [mesh parameterization](/mesh-parameterization/).

## References
