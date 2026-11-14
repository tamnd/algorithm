---
tag: TB95X2
kind: algorithm
slug: simplicial-approximation
name: Simplicial approximation
aliases:
- Director-Hachtel design centering
area: eda/power-reliability-and-manufacturability
level: advanced
summary: Director and Hachtel's design centering. A polytope built from boundary points approximates the feasible region, and the design moves to the center of its largest inscribed ball.
model: word-ram
complexity:
  vars: {K: the number of rounds, m: "the number of boundary points, at most 4 + K in the plane", s: the number of circuit evaluations per line search}
  time: {worst: "O(K (m log m + s))"}
  space: {extra: "O(m)"}
properties: {deterministic: true, exact: false, recursive: false, online: false}
history:
  year: 1977
  people: [Stephen W. Director, Gary D. Hachtel]
  note: Director and Hachtel proposed in IEEE Transactions on Circuits and Systems in 1977 to approximate a convex acceptable region by the convex hull of boundary points found by line searches, to center the design in the largest hypersphere inscribed in that polytope by linear programming, and to refine the polytope at the faces that touch the sphere.
prereqs: [design-centering, convex-hull, linear-programming-problem]
see_also: [andrew-monotone-chain, megiddo-fixed-dimension-lp, lp-duality, complementary-slackness, supporting-hyperplane, convex-set, monte-carlo-integration, bisection-method]
sources:
  - paper: doi:10.1109/TCS.1977.1084353
    title: Stephen W. Director and Gary D. Hachtel, The simplicial approximation approach to design centering, IEEE Transactions on Circuits and Systems CAS-24(7), 363 to 372, July 1977
    locator: the method (boundary points by line searches, the convex hull, the inscribed hypersphere by a linear program, expansion from the largest face that touches the sphere) and its assumption that the region is convex; the section numbers were not checked
  - paper: "Stephen W. Director, Gary D. Hachtel and Luis M. Vidigal, Computationally efficient yield estimation procedures based on simplicial approximation, IEEE Transactions on Circuits and Systems 25(3), 121 to 130, March 1978"
    title: Stephen W. Director, Gary D. Hachtel and Luis M. Vidigal, Computationally efficient yield estimation procedures based on simplicial approximation, IEEE Transactions on Circuits and Systems 25(3), 121 to 130, 1978
    locator: yield estimation from the polytope of the method
  - paper: "John W. Bandler and Shao Hua Chen, Circuit optimization: the state of the art, IEEE Transactions on Microwave Theory and Techniques 36(2), 424 to 443, February 1988"
    title: John W. Bandler and Shao Hua Chen, Circuit optimization, the state of the art, IEEE Transactions on Microwave Theory and Techniques 36(2), 424 to 443, February 1988
    locator: Section V.B, the simplicial approach, which gives a lower bound on the yield that increases monotonically and is limited by its convexity assumption
  - paper: "Vishal Goyal and Marianthi G. Ierapetritou, Determination of operability limits using simplicial approximation, AIChE Journal 48(12), December 2002"
    title: Vishal Goyal and Marianthi G. Ierapetritou, Determination of operability limits using simplicial approximation, AIChE Journal 48(12), 2002
    locator: a step-by-step restatement of the method and its use outside circuit design (the page range was not confirmed)
---

Simplicial approximation is a method for [design centering](/design-centering/) that Director and Hachtel published in 1977. The acceptable region $R$ of the circuit parameters, the set where every specification holds, is known only through circuit simulation. The method assumes that $R$ is convex. It finds points on the boundary of $R$ by line searches, takes their [convex hull](/convex-hull/) as an inner approximation of $R$, and puts the nominal design at the center of the largest ball inscribed in that polytope, which is a [linear program](/linear-programming-problem/). It then adds a boundary point near a face that touches the ball and repeats. The ball is a hypersphere in the parameter space as scaled. If the parameters are first scaled by their spreads, the ball is an ellipsoid in the original units. This page proves what the method guarantees on a convex region, shows a region where the polytope stops growing, and shows a nonconvex region where the method fails.

## In plain words

A circuit works for some parameter settings and fails for others. The settings that work form a region, and its edge is costly to find, since each test is a simulation. The goal is to put the design deep inside the region, so that manufacturing errors do not push it out.

The method walks from a working design in a few directions until the circuit fails, and keeps the points where it crossed the edge. Joining these points gives a shape with flat sides that lies inside the region, if the region has no dents. Inside the shape it finds the largest round ball, and the center of that ball is the new design.

Then it looks at the flat sides that touch the ball, walks outward from the middle of the largest one to find a new edge point, and grows the shape. The ball can only grow.

## The problem

The input is a point $x_0$ inside $R \subset \mathbb{R}^n$ and a line search oracle: for $x \in R$ and a direction $d$, $\mathrm{exit}(x, d)$ is the last point of the ray $x + td$, $t \ge 0$, that lies in $R$. In practice the oracle is a [bisection](/bisection-method/) on $t$ with one circuit simulation per step. The output is a center $c$ and a radius $r$ with $B(c, r) \subseteq R$, as large as the method can certify. The parameters are assumed to be scaled so that a ball is the right shape for the tolerances: with a covariance $\Sigma$ of the process spreads, the scaled parameters are $\Sigma^{-1/2} x$, and a ball there is the ellipsoid $\{x : (x - c)^T \Sigma^{-1} (x - c) \le r^2\}$ in the original units.

The key subproblem is the largest ball in a polytope $P = \{x : n_f \cdot x \le b_f\}$ with unit normals $n_f$. A ball $B(c, r)$ lies in the half-space of face $f$ if and only if $n_f \cdot c + r \le b_f$, because the farthest point of the ball along $n_f$ is $c + r n_f$. So the largest ball is the linear program

$$ \max\ r \quad\text{subject to}\quad n_f \cdot c + r \le b_f \quad\text{for every face } f, $$

in the $n + 1$ variables $(c, r)$. Its center is often called a Chebyshev center of $P$. A face is *tangent* when its constraint is tight at the optimum, that is when it touches the ball.

## The algorithm

```pseudo id=main
SIMPLICIAL-APPROXIMATION(exit, x0, K)
L1  S ← {exit(x0, +e_j), exit(x0, −e_j) : j = 1, …, n}      ▷ 2n line searches
L2  repeat at most K times
L3      P ← the convex hull of S, as faces n_f · x ≤ b_f with unit normals
L4      (c, r) ← argmax r subject to n_f · c + r ≤ b_f for every face f
L5      T ← the faces of P with n_f · c + r = b_f            ▷ tangent faces
L6      sort T by decreasing size (in the plane, edge length)
L7      for each face f of T that is not marked: q ← the center of the largest ball inside f
L8          y ← exit(q, n_f)                                 ▷ search outward along the normal
L9          if y ≠ q then S ← S ∪ {y}; go to the next round
L10         else mark f                                      ▷ f lies on a supporting hyperplane of R
L11     if no point was added then stop                       ▷ every tangent face supports R
L12 return c, r
```

In the plane, a face is an edge, and the center of the largest ball inside it is its midpoint. The implementation works in the plane. It builds the hull with [Andrew's monotone chain](/andrew-monotone-chain/) and solves the three-variable linear program of line L4 with the [simplex method](/simplex-method/) under Bland's rule, starting from the basis of slack variables around the centroid of the hull vertices.

## Example

The region is the triangle $x \ge 0$, $y \ge 0$, $x + y \le 6$. Its largest inscribed disc has radius $6 - 3\sqrt{2} \approx 1.7574$ and center $(1.7574, 1.7574)$. The start is $x_0 = (1, 4)$, and the four line searches of L1 return $(2, 4)$, $(1, 5)$, $(0, 4)$ and $(1, 0)$. The last column gives the area of the hull divided by the area 18 of the triangle.

| round | new point | center $c$ | radius $r$ | step of lines L5 to L10 | area ratio |
|---|---|---|---|---|---|
| 0 | the four of L1 | (1, 3.723) | 0.903 | all 4 edges touch; the longest, (0, 4) to (1, 0), has midpoint (0.5, 2), and the search finds (0, 1.875) | 0.278 |
| 1 | (0, 1.875) | (0.937, 3.612) | 0.937 | longest tangent edge (1, 0) to (2, 4), midpoint (1.5, 2), new point (4.833, 1.167) | 0.337 |
| 2 | (4.833, 1.167) | (1.798, 1.926) | 1.610 | the longest tangent edge lies on $x + y = 6$, so the search returns its midpoint and the edge is marked; the next, (1, 0) to (4.833, 1.167), gives (3.094, 0) | 0.730 |
| 3 | (3.094, 0) | (1.995, 1.659) | 1.659 | the longest unmarked tangent edge, (0, 1.875) to (1, 0), gives (0, 0.671) | 0.798 |
| 4 | (0, 0.671) | (1.757, 1.757) | 1.757 | the four tangent edges lie on the sides of the triangle: stop | 0.832 |

The method stops with the exact inscribed disc after eight line searches that found a point and four that did not. The hull covers only 83 percent of the triangle at the stop. The method needs the boundary only where the ball touches it.

On regions with a curved boundary the method does not stop, and the measured behavior depends on the shape. The table gives the area ratio $|P_k| / |R|$ and the radius $r_k$ for a unit disc started at $(0.3, -0.2)$ and for the ellipse $x^2/4 + y^2 \le 1$ started at $(0.5, 0.3)$, whose largest inscribed disc has radius 1. The "longest edge" rule refines the longest edge of the whole hull in place of the longest tangent edge.

| region and rule | round 0 | round 5 | round 10 | round 20 | round 40 | round 59 |
|---|---|---|---|---|---|---|
| disc, tangent rule: area | 0.595 | 0.906 | 0.965 | 0.987 | 0.996 | 0.998 |
| disc, tangent rule: $r_k$ | 0.666 | 0.904 | 0.966 | 0.987 | 0.995 | 0.998 |
| ellipse, tangent rule: area | 0.588 | 0.872 | 0.880 | 0.880 | 0.880 | 0.880 |
| ellipse, tangent rule: $r_k$ | 0.846 | 0.967 | 0.998 | 1.000 | 1.000 | 1.000 |
| ellipse, longest edge: area | 0.588 | 0.906 | 0.956 | 0.982 | 0.995 | 0.998 |

On the ellipse the tangent rule finds the right radius by round 20 and then keeps refining near the two points $(0, \pm 1)$ where the ball touches, so the polytope never covers more than 88 percent of the region. This is correct for centering, but it means the polytope is not a good model of the whole region.

## Correctness

The [full proof](proofs/correctness.md) shows four facts for a compact convex region with a nonempty interior, and one failure for a nonconvex region.

**The ball is a linear program.** As shown above, $B(c, r) \subseteq P$ if and only if $n_f \cdot c + r \le b_f$ for all faces.

**Inclusion, nesting and monotone radius.** The points of $S$ lie in $R$ and $R$ is convex, so each hull $P_k$ lies in $R$, and so does each ball. Points are only added, so $P_k \subseteq P_{k+1}$, the old ball is feasible in the next round, and $r_0 \le r_1 \le \cdots \le r(R)$, where $r(R)$ is the radius of the largest ball in $R$.

**The stop test is sound.** If the outward search from the midpoint of a face, or from any point in its relative interior, does not move, then the hyperplane of that face supports $R$. Otherwise a point of $R$ beyond the face and the face itself would span points of $R$ just outside the midpoint.

**A fixed point is optimal.** Suppose every tangent face supports $R$. By [LP duality](/lp-duality/) and [complementary slackness](/complementary-slackness/), there are weights $\lambda_f \ge 0$ on the tangent faces with $\sum \lambda_f n_f = 0$, $\sum \lambda_f = 1$ and $\sum \lambda_f b_f = r$. Any ball $B(c', r')$ in $R$ satisfies $n_f \cdot c' + r' \le b_f$ for these faces, and the weighted sum gives $r' \le r$. So when the method stops at line L11, its ball is a largest ball in $R$.

**What is not guaranteed.** The rule does not make the polytope converge to $R$, as the ellipse shows. This page does not prove that $r_k$ tends to $r(R)$ when the method runs forever; the disc and ellipse runs only measure it. Director and Hachtel discuss convergence for convex regions in their paper, and the reader should take the exact statement from there.

**Nonconvex regions.** For the L-shaped region $[0,4] \times [0,2] \cup [0,2] \times [0,4]$ started at $(1, 1)$, the first hull is the quadrilateral with corners $(0, 1)$, $(1, 0)$, $(4, 1)$ and $(1, 4)$. It contains $(2.4, 2.4)$, which is not in $R$, and its inscribed disc, with center $(1.573, 1.573)$ and radius 1.311, contains $(2.5, 2.5)$, which is not in $R$ either. The run ends with a radius of 1.464, while no disc in $R$ has a radius above $2\sqrt{2}/(1 + \sqrt{2}) \approx 1.172$.

## Complexity

In the plane, round $k$ has $m \le 4 + k$ boundary points. The hull costs $O(m \log m)$, the three-variable program costs $O(m)$ with [Megiddo's method](/megiddo-fixed-dimension-lp/) for fixed dimension, and a round runs at most one successful line search plus one search for each newly marked face. Each face is marked at most once, so $K$ rounds cost $O(K(m \log m + s))$ arithmetic and circuit evaluations, where $s$ is the number of simulations per line search. In practice the simulations dominate: a bisection to a relative accuracy of $10^{-3}$ takes about 10 of them. The implementation uses the simplex method, which is fast on these small programs but has no such worst-case bound.

In $n$ dimensions the hull of $m$ points can have on the order of $m^{\lfloor n/2 \rfloor}$ faces, by the upper bound theorem for polytopes, and the program has one constraint per face. This is why the method is practical only for a few parameters, often fewer than ten.

## Properties

- **Inner approximation.** For a convex region every polytope and every ball lie inside $R$, so the center is always a working design and $r_k$ is a certified margin.
- **Monotone.** The radius never decreases, and the polytope only grows. With a distribution of the parameters, the probability of the polytope around the nominal point is a lower bound on the yield, and it grows from round to round, as Bandler and Chen note.
- **Exact at a fixed point.** When all tangent faces support $R$ the ball is a largest ball in $R$. On polygons and polytopes this stop can happen after finitely many rounds, as on the triangle.
- **Local refinement.** Only the boundary near the ball is explored, which saves simulations but leaves the rest of the region unknown.
- **Needs convexity.** Every guarantee above rests on the convexity of $R$.

## Variants and improvements

- **Scaling and ellipsoids.** Scaling by the process covariance before the method turns the ball into an ellipsoid of equal probability density under a normal law. A worst-case tolerance box needs a different body and a different program.
- **Refining the whole boundary.** Choosing the longest face overall, as in the ellipse table, makes the polytope fill the region, at the cost of searches far from the ball. Such a polytope is better for yield estimation.
- **Yield estimation.** Director, Hachtel and Vidigal (1978) estimate the yield from the polytope, by integrating the parameter density over it, which is cheap since membership in a polytope needs no simulation.
- **Other centering methods.** The design centering page lists the gravity method, statistical [Monte Carlo](/monte-carlo-integration/) methods and worst-case distance methods, which do not need a convex region.
- **Operability analysis.** Goyal and Ierapetritou (2002) used the same steps to map the feasible operating region of chemical processes.

## When to use it

Use it when the acceptable region is known or expected to be convex, the number of parameters is small, and each simulation is expensive enough that a few dozen line searches are the budget. It gives a centered design with a certified margin. Do not use it when the region may be nonconvex, for example when several specifications pull in different directions, or for more than a handful of parameters. In those cases a statistical method or a worst-case distance method is safer.

## Pitfalls

- **Nonconvex regions.** The polytope can contain failing designs, and the reported margin can be larger than any margin in $R$, as in the L-shaped example. Nothing in the method warns about this; a check of the center and of a few points of the ball by simulation catches the worst cases.
- **Unscaled parameters.** A ball in raw units treats a resistor in ohms and a width in micrometers as equal. Scale by the spreads first.
- **Inexact line searches.** A bisection that stops early returns a point slightly inside or outside $R$. A point outside breaks the inclusion. Bias the search to return the last feasible point.
- **Ties and degenerate faces.** Several faces can touch the ball, and several can have the same size. A fixed tie rule keeps runs reproducible.
- **Using the polytope as the region.** The polytope is accurate only near the ball. A yield computed from it is a lower bound, and it can be far below the true yield, as on the ellipse.
- **Starting point.** $x_0$ must be strictly inside $R$; otherwise the first hull can be flat and the program has no ball.

## Implementations

## History

Director and Hachtel published simplicial approximation in 1977, at a time when design centering by Monte Carlo methods needed thousands of simulations. Their idea was to replace the unknown region by a polytope that is cheap to work with, and to spend simulations only on line searches. Director, Hachtel and Vidigal (1978) used the same polytope to estimate the yield. Later surveys, such as that of Bandler and Chen (1988), list the method among the first geometric centering methods and note that its convexity assumption limits its use. The method was later applied to the operability of chemical processes by Goyal and Ierapetritou (2002).

## References
