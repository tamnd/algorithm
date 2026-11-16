---
tag: B0Z8Z4
kind: algorithm
slug: independent-contact-regions
name: Independent contact regions
aliases:
- Nguyen's independent regions
area: robotics/grasping-and-manipulation
level: advanced
summary: Computes segments on two edges of a polygon such that any choice of one finger contact in each segment gives a force-closure grasp, with the smaller segment as long as possible.
model: real-ram
complexity:
  vars: {n: "the number of edges of the polygon, when every pair of edges is tried"}
  time: {worst: O(n^2)}
  space: {extra: O(1)}
properties: {deterministic: true, exact: true, optimal: true}
history:
  year: 1988
  people: [Van-Duc Nguyen]
  note: Nguyen gave the two-finger force-closure condition in the plane and introduced independent regions of contact, so that a grasp stays in force closure when the fingers miss their target points.
prereqs: [force-closure, friction-cone, linear-programming-problem]
see_also: [force-closure-test, antipodal-grasp, grasp-synthesis, polyhedral-friction-cone, two-phase-simplex-method, bland-rule, grasp-quality-measures, fixture-planning]
sources:
  - paper: doi:10.1177/027836498800700301
    title: Van-Duc Nguyen, Constructing force-closure grasps, The International Journal of Robotics Research 7(3), 3-16, 1988
    locator: the whole paper (the force-closure condition for two fingers with friction in the plane, and independent regions of contact on the edges of a polygon)
  - paper: doi:10.1177/027836499701600102
    title: Jean Ponce, Steve Sullivan, Attawith Sudsang, Jean-Daniel Boissonnat and Jean-Pierre Merlet, On computing four-finger equilibrium and force-closure grasps of polyhedral objects, The International Journal of Robotics Research 16(1), 11-35, 1997
    locator: the whole paper (independent regions for four fingers on the faces of a polyhedron, by linear constraints)
  - paper: doi:10.1287/moor.2.2.103
    title: Robert G. Bland, New finite pivoting rules for the simplex method, Mathematics of Operations Research 2(2), 1977
    locator: pages 103 to 107 (the smallest index rule and the proof that it does not cycle)
---

Independent contact regions are segments on the edges of an object, one for each finger, chosen so that the grasp is in [force closure](/force-closure/) for every choice of one contact point in each segment. A finger then does not need to hit an exact point: any point in its segment works, whatever the other fingers do inside their own segments. This page computes the regions for two fingers with friction on two edges of a convex polygon. It writes Nguyen's two-finger condition as a small linear program and solves it in exact arithmetic, so the smaller region is as long as possible.

## In plain words

Pinch a flat part between two fingers. The pinch holds when the line between the two fingers is steep enough against each edge, so that friction can stop the fingers from sliding off. A robot never puts its fingers exactly where it planned. So it is better to plan two short pieces of edge, one for each finger, such that every pair of points from the two pieces makes a good pinch. Then small errors do not matter. The method checks the four pairs of end points of the two pieces. If those four pairs are good, every pair in between is good too. It then stretches the pieces as far as these checks allow, so that the shorter piece is as long as possible.

## The problem

The input is a convex polygon with vertices in counterclockwise order, two different edges $i$ and $j$, and a friction coefficient $\mu > 0$. Edge $e$ starts at $A_e$, has the direction $D_e$ (the vector to its end point) and the inward normal $n_e$, which is $D_e$ turned by 90 degrees counterclockwise. A finger on edge $e$ touches the point $A_e + t D_e$ with the parameter $t \in [0, 1]$. The fingers are [point contacts with friction](/grasp-contact-models/). In the plane the [friction cone](/friction-cone/) $C_e$ has exactly two edges, $n_e + \mu D_e$ and $n_e - \mu D_e$, so there is no linearization error.

Nguyen (1988) showed that two contacts $p_1$ on edge $i$ and $p_2$ on edge $j$ form a force-closure grasp if and only if the vector $d = p_2 - p_1$ lies strictly inside $C_i$ and $-d$ lies strictly inside $C_j$. In words, the segment between the fingers lies inside both friction cones. This is the [antipodal grasp](/antipodal-grasp/) condition.

The output is two parameter intervals $(s_1, u_1)$ on edge $i$ and $(s_2, u_2)$ on edge $j$ such that every $t_1 \in (s_1, u_1)$ and every $t_2 \in (s_2, u_2)$ satisfy Nguyen's condition, with the smaller width $\min(u_1 - s_1, u_2 - s_2)$ as large as possible. The widths are fractions of the edge lengths, which keeps every number rational. If no pair of points on the two edges gives force closure, the output is NONE.

## The algorithm

Write $d(t_1, t_2) = (A_j - A_i) + t_2 D_j - t_1 D_i$. This is affine in the parameters. A vector $v$ is in the cone with edges $g_0, g_1$, ordered so that $\operatorname{cross}(g_0, g_1) > 0$, if and only if $\operatorname{cross}(g_0, v) \ge 0$ and $\operatorname{cross}(v, g_1) \ge 0$, where $\operatorname{cross}(a, b) = a_x b_y - a_y b_x$. So each cone condition at one pair of parameters is two linear inequalities.

```pseudo id=main
INDEPENDENT-REGIONS(polygon, i, j, μ)
L1  for e in (i, j): A_e, D_e ← the start and the direction of edge e; n_e ← D_e turned by +90 degrees
L2  for e in (i, j): g_e0, g_e1 ← n_e + μ D_e and n_e - μ D_e, ordered so that cross(g_e0, g_e1) > 0
L3  d(t_1, t_2) ← (A_j - A_i) + t_2 D_j - t_1 D_i              ▷ affine in t_1, t_2
L4  for each corner (t_1, t_2) in {s_1, u_1} × {s_2, u_2} do
L5      add cross(g_i0, d) ≥ 0 and cross(d, g_i1) ≥ 0          ▷ d in the cone at p_1
L6      add cross(g_j0, -d) ≥ 0 and cross(-d, g_j1) ≥ 0        ▷ -d in the cone at p_2
L7  add 0 ≤ s_1, u_1 ≤ 1, 0 ≤ s_2, u_2 ≤ 1, u_1 - s_1 ≥ z, u_2 - s_2 ≥ z
L8  (z*, s_1, u_1, s_2, u_2) ← maximize z subject to these constraints   ▷ two-phase simplex, Bland's rule
L9  if the program is infeasible or z* = 0 then return NONE
L10 return the open intervals (s_1, u_1) on edge i and (s_2, u_2) on edge j
```

The program has five variables and twenty constraints: sixteen from lines L4 to L6 and four from line L7. The solver is the [two-phase simplex method](/two-phase-simplex-method/) in rational arithmetic, with [Bland's rule](/bland-rule/) so that it cannot cycle. To find the best pair of edges of an $n$-gon, run it on each of the $n(n-1)/2$ pairs and keep the largest $z^*$.

## Example

Take the square with vertices $(0, 0)$, $(2, 0)$, $(2, 2)$, $(0, 2)$ and $\mu = 1/2$. Edge 1 is the right side, from $(2, 0)$ up to $(2, 2)$, with $D_1 = (0, 2)$ and $n_1 = (-2, 0)$. Edge 3 is the left side, from $(0, 2)$ down to $(0, 0)$, with $D_3 = (0, -2)$ and $n_3 = (2, 0)$. The cone edges are $(-2, \pm 1)$ at the right side and $(2, \pm 1)$ at the left side. A finger at height $y_1$ on the right and a finger at height $y_3$ on the left give $d = (-2,\ y_3 - y_1)$, and both cone conditions say $\lvert y_3 - y_1 \rvert \le 1$.

The linear program returns $z^* = 1/2$ with $(s_1, u_1) = (1/2, 1)$ and $(s_2, u_2) = (0, 1/2)$. In heights, both regions are $1 < y < 2$, the upper halves of both sides. The four corner pairs are:

| $y_1$ | $y_3$ | $\lvert y_3 - y_1 \rvert$ | On the boundary of the cones |
|---|---|---|---|
| 1 | 1 | 0 | no |
| 1 | 2 | 1 | yes |
| 2 | 1 | 1 | yes |
| 2 | 2 | 0 | no |

Two corner pairs are on the boundary, so the closed segments are not regions, but the open ones are: two heights strictly between 1 and 2 differ by less than 1. No pair of regions does better. If the two height intervals have lengths $L_1$ and $L_3$, some pair of their points differs by at least $(L_1 + L_3)/2$, so $\min(L_1, L_3) \le 1$, which is half of the side. Any two equal height intervals of length 1 are also optimal; the solver returns one of them.

On the adjacent sides of the same square, with the bottom edge $i = 0$ and the right edge $j = 1$, the answer depends on $\mu$. With $\mu = 1$ the closed conditions hold only on the segment where $y = 2 - x$, which has no interior, so $z^* = 0$ and the algorithm returns NONE: no two-finger grasp on these two edges is in force closure. With $\mu = 2$ it returns $z^* = 1/2$, with the regions $0 < x < 1$ on the bottom and $1 < y < 2$ on the right. For the triangle with vertices $(0, 0)$, $(4, 0)$ and $(1, 3)$, the best pair of edges is the bottom and the right edge, with $z^* = 2/7$ for $\mu = 1$, and no pair of edges works for $\mu = 1/4$.

## Correctness

The full proof is in proofs/correctness.md. Lemma 1 proves Nguyen's condition from the force-closure characterization on the [force-closure test](/force-closure-test/) page, using that the polygon is convex. Lemma 2 writes each closed cone as two cross product inequalities. Lemma 3 shows that four corner pairs suffice: the parameter rectangle is the convex hull of its corners, $d$ is affine, and the closed cones are convex. Lemma 4 shows that when $z > 0$ the open rectangle maps into the open cones; the key step is that $d$ can move both ways along the edge direction, which is never parallel to a cone edge. The theorem then gives three facts: the returned open intervals are independent regions, no pair of regions has a larger smaller width, and NONE is returned exactly when no pair of contacts works.

## Complexity

For one pair of edges the program has a fixed size, five variables and twenty constraints. Bland's rule never repeats a basis, so the number of pivots is bounded by a constant, and the work is $O(1)$ arithmetic operations on rationals whose size depends only on the input coordinates and $\mu$. Over all pairs of edges of an $n$-gon this is $O(n^2)$ time and $O(1)$ extra space besides the best answer. The cost model is the real RAM; the implementation uses exact rationals. Its run time in Python is about 30 ms per pair of edges on a laptop (a measurement, not a bound).

## Properties

- **Exact.** All numbers are rational, so the test $z^* > 0$ in line L9 is exact. Boundary cases, such as a segment on the edge of the friction cone, get the right answer.
- **Optimal for its objective.** The smaller relative width is the largest possible over all pairs of intervals on the two edges. A different objective, such as the sum of the widths or the widths in length units, gives other regions.
- **Robustness margin.** Each finger may land anywhere in its region, independently of the other finger. This is a guarantee about positioning errors along the edge, not about errors in $\mu$ or in the shape.
- **Not unique.** When several pairs of intervals reach $z^*$, the solver returns one optimal vertex of the program.

## Variants and improvements

- **Nguyen's construction.** Nguyen (1988) builds the regions geometrically, from the friction cones on the edges. The linear program here uses the same condition and gives the regions with the largest smaller width.
- **More fingers and three dimensions.** Ponce, Sullivan, Sudsang, Boissonnat and Merlet (1997) compute regions for four fingers on the faces of a polyhedron. The conditions are again linear in the contact positions, which is why linear programs appear there too.
- **Other objectives.** Maximize the sum of the widths, weight the edges by their lengths, or require the regions to be centered on a planned grasp. Each is a different linear objective over the same constraints.
- **Curved objects.** On a smooth boundary the cone directions change along the region, so the constraints are no longer linear. One approach samples the boundary and grows the regions around a good grasp, checking each new sample.

## When to use it

Use it when a planner picks a grasp on a flat part with two fingers and the hand cannot reach the planned points exactly. The regions tell the controller how much error is safe on each finger. Use the plain [force-closure test](/force-closure-test/) when the contacts are fixed and only a yes or no answer is needed. Use a [grasp quality measure](/grasp-quality-measures/) when you must rank closed grasps by the forces they can resist, not by the positioning error they allow.

## Pitfalls

- **Closed versus open regions.** The optimal closed segments can touch the boundary of a friction cone at their end points, as in the example. Only the open segments are regions.
- **Nonconvex polygons.** Nguyen's condition in Lemma 1 uses convexity. On a nonconvex part, the segment between the fingers can leave the part, and the condition must be checked against the true contact normals and the reachability of the points.
- **Normal direction.** The inward normal of a counterclockwise polygon is the edge direction turned by +90 degrees. A clockwise polygon flips every normal and turns every push into a pull.
- **Uncertain friction.** The regions hold for the given $\mu$. Use a lower bound of the true friction coefficient, because a smaller $\mu$ gives smaller regions.
- **Floating point.** A float solver with a tolerance can report $z^* > 0$ for a pair of edges where only boundary grasps exist, such as the adjacent sides with $\mu = 1$ in the example.

## Implementations

## History

Nguyen (1988) gave the force-closure condition for two fingers with friction in the plane and introduced independent regions of contact for the fingertips, so that a planned grasp stays in force closure under positioning errors. Ponce and his coauthors (1997) extended the computation to four fingers on polyhedra. Later work computes regions for more fingers, for three-dimensional objects given as meshes, and for hands whose fingers cannot reach every point.

## References
