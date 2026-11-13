---
tag: DRVDD3
kind: algorithm
slug: rolling-ball-blend
name: Rolling-ball blend
aliases:
- rolling-ball fillet
- constant radius fillet
area: cad/solid-modeling
level: core
summary: Builds a blend as the envelope of a ball of fixed or varying radius that rolls while touching both surfaces, from the spine curve of the ball centres.
model: real-ram
complexity:
  vars: {m: the number of spine points, k: the number of points on each cross-section arc, i: the number of Newton iterations in one step}
  time: {worst: O(m (i + k))}
  space: {extra: O(m k)}
properties: {deterministic: true, recursive: false, exact: false}
history:
  year: 1989
  people: [Byoung K. Choi, Suk Y. Ju]
  note: Choi and Ju built constant-radius rolling-ball surfaces between parametric surfaces from the intersection curve of the two offset surfaces, the spine of the ball centers.
prereqs: [blending-surface, offset-surface, surface-surface-intersection, newton-method-for-systems]
see_also: [marching-surface-intersection, solid-offsetting, rossignac-requicha-offsetting, sweep-surface, trimmed-surface, parametric-continuity, signed-distance-function, frenet-frame]
sources:
  - paper: "Byoung K. Choi and Suk Y. Ju, Constant-radius blending in surface modelling, Computer-Aided Design 21(4), 213 to 220, 1989"
    locator: the whole paper (the spine as the intersection of offset surfaces, the contact points and the circular cross sections)
  - paper: "Janos Vida, Ralph R. Martin and Tamas Varady, A survey of blending methods that use parametric surfaces, Computer-Aided Design 26(5), 341 to 365, 1994"
    locator: the section on rolling-ball blends and their variable-radius forms, and the comparison with spine-based and trimline-based methods
  - paper: doi:10.1016/0167-8396(86)90017-8
    title: Jaroslaw R. Rossignac and Aristides A. G. Requicha, Offsetting operations in solid modelling, Computer Aided Geometric Design 3(2), 129 to 148, 1986
    locator: constant-radius rounding and filleting of solids as compositions of offsets, whose faces near an edge are rolling-ball surfaces
  - book: isbn:9783540424543
    title: Nicholas M. Patrikalakis and Takashi Maekawa, Shape Interrogation for Computer Aided Design and Manufacturing, Springer, 2002
    locator: Chapter 11, Offset curves and surfaces (the offset surfaces whose intersection is the spine), and Section 5.8, Surface/surface intersections
---

The rolling-ball blend of two surfaces $S_1$ and $S_2$ is the surface swept by a ball of radius $r$ that rolls along the edge between them while it touches both. Its [blending surface](/blending-surface/) is the envelope of the ball: at each position, the ball touches the envelope along a circle, and the part of that circle between the two contact points is a cross section of the blend. The ball center moves on the *spine*, which is the intersection of the two [offset surfaces](/offset-surface/) at distance $r$. So the algorithm traces the spine with [surface surface intersection](/surface-surface-intersection/), and then, for each center, drops the contact points onto the surfaces and draws the arc between them. Choi and Ju gave this construction for parametric surfaces in 1989. The result meets both surfaces with the same tangent plane ($G^1$), but in general not with the same curvature.

## In plain words

Push a ball into the inner corner between two walls, so that it touches both, and roll it along the corner. The ball sweeps out a rounded strip. That strip is the fillet.

The center of the ball always stays at the same distance from both walls. So it moves along the line where the two walls, moved out by the radius of the ball, cross each other. That line is called the spine.

To build the fillet, first follow the spine in small steps. At each step, find the two points where the ball touches the walls. They lie straight down from the center onto each wall. Then join them with the short arc of a circle around the center. The arcs, one after the other, form the fillet.

## The problem

The input is two surfaces $S_1$ and $S_2$, each with a signed distance function $\mathrm{sd}_i$ that is exact near the surface and whose gradient is the unit normal $n_i$, a radius $r > 0$, a side $s_i \in \{+1, -1\}$ for each surface, a start point $x_0$ near the spine, and a step length $h$. The ball must lie on side $s_i$ of $S_i$, so its center $c$ satisfies

$$\mathrm{sd}_1(c) = s_1 r, \qquad \mathrm{sd}_2(c) = s_2 r.$$

The output is a sequence of spine points $c_0, c_1, \ldots$ and, for each, the contact points $p_1 \in S_1$, $p_2 \in S_2$ and a sampled arc between them. For a fillet on a concave edge the ball lies outside the solid, so $s_i$ is the side of the outward normal; for a round on a convex edge it lies inside. The faces are oriented so that the outward normal of each face follows the right-hand rule with its loops, and the blend inherits the outward normals of $S_1$ and $S_2$ at its two trimlines.

## The algorithm

```pseudo id=main
ROLLING-BALL-BLEND(S1, S2, r, s1, s2, x0, h)
L1  c ← CORRECT(x0)                     ▷ Newton onto sd1 = s1 r and sd2 = s2 r
L2  spine ← [c]
L3  repeat
L4      t ← n1(c) × n2(c), as a unit vector that agrees in sign with the previous t
L5      c ← CORRECT(c + h t)
L6      append c to spine
L7  until c is back near spine[0] or the step budget is used up
L8  for each c in spine do
L9      p1 ← c − s1 r n1(c),  p2 ← c − s2 r n2(c)      ▷ the contact points
L10     A ← the shorter arc from p1 to p2 on the circle with center c and radius r
L11     record (c, p1, p2, A)
L12 return the records
```

CORRECT at lines L1 and L5 is the [Newton method for systems](/newton-method-for-systems/) on the two equations $F(x) = (\mathrm{sd}_1(x) - s_1 r, \mathrm{sd}_2(x) - s_2 r) = 0$, three unknowns and two equations. It takes the step of least length, $x \leftarrow x - J^\top (J J^\top)^{-1} F(x)$, where the rows of $J$ are $n_1(x)$ and $n_2(x)$. The step is undefined where $n_1 \parallel n_2$, which is where the spine has no tangent, and the implementation stops there with an error. Lines L3 to L7 are a [marching](/marching-surface-intersection/) trace of the intersection of the two offsets, with the step along $n_1 \times n_2$ that is the tangent of the spine.

Line L10 lies in the plane through $c$ normal to $t$, because both contact points do: $n_i \perp t$, so $p_i - c = -s_i r n_i$ is perpendicular to $t$. With $a = (p_1 - c)/r$, $b = (p_2 - c)/r$ and $\theta = \arccos(a \cdot b)$, the arc is $c + r \, (\sin((1 - \lambda)\theta) \, a + \sin(\lambda \theta) \, b) / \sin \theta$ for $0 \le \lambda \le 1$.

## Example

Take the floor $z = 0$ with the ball above it ($s_1 = +1$), a vertical shaft $x^2 + y^2 = 1$ with the ball outside it ($s_2 = +1$), and $r = 1/2$. This is the fillet at the foot of the shaft. Start at $x_0 = (1.8, 0, 0.7)$ with $h = 0.05$ and three points per arc.

| step | spine point $c$ | $p_1$ (floor) | arc midpoint | $p_2$ (shaft) |
|---|---|---|---|---|
| 0 | $(1.5, 0, 0.5)$ | $(1.5, 0, 0)$ | $(1.14645, 0, 0.14645)$ | $(1, 0, 0.5)$ |
| 1 | $(1.49917, 0.04997, 0.5)$ | $(1.49917, 0.04997, 0)$ | $(1.14581, 0.03819, 0.14645)$ | $(0.99944, 0.03331, 0.5)$ |
| 2 | $(1.49667, 0.09989, 0.5)$ | $(1.49667, 0.09989, 0)$ | $(1.14390, 0.07634, 0.14645)$ | $(0.99778, 0.06659, 0.5)$ |
| 47 | $(0.00706, 1.49998, 0.5)$ | $(0.00706, 1.49998, 0)$ | $(0.00540, 1.14643, 0.14645)$ | $(0.00471, 0.99999, 0.5)$ |
| 94 | $(-1.49993, 0.01413, 0.5)$ | $(-1.49993, 0.01413, 0)$ | $(-1.14640, 0.01080, 0.14645)$ | $(-0.99996, 0.00942, 0.5)$ |

At step 0, one Newton step moves $x_0$ to $(1.5, 0, 0.5)$: the offsets are the plane $z = 1/2$ and the cylinder of radius $3/2$, both linear in the direction of the step. The tangent is $n_1 \times n_2 = (0, 0, 1) \times (1, 0, 0) = (0, 1, 0)$. The spine closes after $188$ points, which matches the length $2\pi \cdot 3/2 \approx 9.42$ of the circle of radius $3/2$ at height $1/2$ divided by $h$. The arcs are quarter circles, and every arc point $x$ satisfies $(\sqrt{x_1^2 + x_2^2} - 3/2)^2 + (x_3 - 1/2)^2 = 1/4$: the blend is the inner lower quarter of a torus with axis radius $3/2$ and tube radius $1/2$.

## Correctness

Let $c(\sigma)$ be a regular parametrization of the exact spine, so that $\mathrm{sd}_i(c(\sigma)) = s_i r$ for all $\sigma$, and let $B(\sigma)$ be the sphere of radius $r$ around $c(\sigma)$. Differentiating gives $n_i(c) \cdot c' = 0$, so $c'$ is parallel to $n_1 \times n_2$, which justifies line L4. The envelope of the family $|x - c(\sigma)|^2 = r^2$ is found by also setting the derivative in $\sigma$ to zero: $(x - c(\sigma)) \cdot c'(\sigma) = 0$. So each sphere touches the envelope along the *characteristic circle*, its intersection with the plane through $c$ normal to $c'$. The contact point $p_i = c - s_i r n_i$ lies on $S_i$, because $\mathrm{sd}_i$ is a signed distance whose gradient is the unit normal, and it lies on the characteristic circle, because $|p_i - c| = r$ and $(p_i - c) \cdot c' = -s_i r \, n_i \cdot c' = 0$. At $p_i$ the normal of the envelope is $(p_i - c)/r = -s_i n_i$, parallel to the normal of $S_i$, so the join is $G^1$. The [full proof](proofs/correctness.md) states the conditions and also shows that the ball does not cut either surface near the contact.

What is proved is the geometry of exact spine points. The trace itself is numerical: each spine point satisfies the two equations within the Newton tolerance, and a step $h$ that is too long can jump to another branch of the spine, as for every marching method.

## Complexity

The costs are in the [real RAM](/real-ram/) with square roots, counted per spine point. Line L4 costs $O(1)$, CORRECT costs $O(1)$ per Newton iteration, which gives $O(i)$ per step with $i$ iterations, and lines L9 and L10 cost $O(k)$ for $k$ arc points. In all the time is $O(m(i + k))$ and the space $O(mk)$ for $m$ spine points. Near a regular spine point Newton converges quadratically, so $i$ is a small constant once $h$ is small. The number of spine points is the length of the spine divided by $h$.

## Properties

- **$G^1$, not $G^2$.** The blend has the tangent plane of each surface along the trimline. The normal curvature across the trimline jumps, for example from $0$ on a plane to $1/r$ on the blend.
- **Circular cross sections.** Each cross section is an arc of radius $r$ in the normal plane of the spine. The blend is a canal surface, the envelope of a one-parameter family of spheres.
- **Exact for simple pairs.** Two planes give a cylinder, a plane and a cylinder perpendicular to it give a torus, two parallel cylinders give a cylinder. CAD systems store these cases in closed form.
- **Rational only in special cases.** The spine is an intersection of offsets, which are not rational in general, so the blend of two NURBS surfaces is approximated.

## Variants and improvements

- **Variable radius.** The radius $r(\sigma)$ changes along the edge. The characteristic circle then lies in a plane that is no longer normal to the spine, given by $(x - c) \cdot c' + r r' = 0$, and the contact points come from offsets at varying distance.
- **Parametric surfaces.** For NURBS surfaces there is no exact distance function. Choi and Ju solve for a center $c$ and two parameter points $(u_1, v_1)$ and $(u_2, v_2)$ with $c = S_1(u_1, v_1) + s_1 r N_1 = S_2(u_2, v_2) + s_2 r N_2$, and march along the solution curve.
- **Spine-based and trimline-based blends.** Other cross sections, such as conics or Hermite cubics, give more control of the shape and can reach $G^2$; Vida, Martin and Várady compare the classes.
- **Solid offsetting.** Rounding and filleting a whole solid with one radius is $(S \downarrow r) \uparrow r$ or $(S \uparrow r) \downarrow r$ ([solid offsetting](/solid-offsetting/), [Rossignac and Requicha offsetting](/rossignac-requicha-offsetting/)). Near an edge, the faces of the result are rolling-ball surfaces.

## When to use it

Use the rolling-ball blend for constant or variable radius fillets and rounds on mechanical parts, where the radius is a design or manufacturing value: a ball-end cutter of radius $r$ leaves a rolling-ball fillet in a concave corner. Use a spine-based or trimline-based blend when the shape of the cross section matters more than a constant radius, for example for $G^2$ transitions on visible surfaces. For many edges at once on a whole solid, offsetting the solid gives all the fillets without a separate trace for each edge.

## Pitfalls

- **A radius larger than the space.** If the ball does not fit, for example a fillet of radius $r$ in a slot narrower than $2r$, the offsets do not meet where expected, and the spine runs into another face. The blend then intersects other faces of the solid and the operation must fail or be merged.
- **Parallel normals.** Where the two surfaces are tangent, $n_1 \times n_2 = 0$ and the spine has no tangent. The Newton step is undefined there. The implementation raises an error, and real systems end the blend before such points.
- **Concave surfaces.** On a surface whose radius of curvature on the ball side is smaller than $r$, the offset folds over, and the foot point at line L9 is not the nearest point. The ball then cuts the surface.
- **Branch jumps.** A long step at line L5 can land on another branch of the intersection of the offsets, for example the spine on the other side of the shaft. Keep $h$ small relative to the radius of curvature of the spine.
- **Corners.** Where three rounded edges meet, the three blends leave a hole at the vertex, which needs a separate vertex surface.

## Implementations

## History

Rossignac and Requicha's 1986 paper on offsetting obtained constant-radius rounding and filleting of whole solids as compositions of offsets. Choi and Ju published in 1989 the construction for parametric surfaces from the intersection of offset surfaces, and Vida, Martin and Várady's survey of 1994 put rolling-ball blends beside the spine-based and trimline-based methods.

## References
