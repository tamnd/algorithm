---
tag: MQ38PN
kind: algorithm
slug: iso-scallop-toolpath
name: Iso-scallop toolpath
aliases:
- constant scallop toolpath
area: cad/cam-and-additive-manufacturing
level: advanced
summary: Places each pass so the scallop height to the last pass is constant, as in Suresh and Yang, which shortens the path for a given finish.
solves: [toolpath-planning]
model: real-ram
complexity:
  vars: {N: number of passes, B: bisection and doubling steps per pass, G: golden-section steps per height}
  time: {worst: "O(N B G)"}
  space: {extra: "O(1)"}
properties: {deterministic: true, recursive: false, exact: false}
history:
  year: 1994
  people: [Krishnan Suresh, Daniel C. H. Yang]
  note: Suresh and Yang placed each pass of a ball end mill on a free-form surface so that the scallop height to the last pass is constant. Lin and Koren gave an efficient version in 1996.
prereqs: [scallop-height, iso-parametric-toolpath, bisection-method]
see_also: [iso-planar-toolpath, cutter-location-data, golden-section-search, offset-surface, surface-curvature, gouge-detection, fermat-spiral-toolpath, newton-raphson-method]
sources:
  - book: isbn:978-0-412-78020-2
    title: Byoung K. Choi and Robert B. Jerard, Sculptured Surface Machining, Theory and Applications, Kluwer Academic Publishers, 1998
    locator: chapter 6, introduction to tool-path generation methods, the part on constant scallop (iso-scallop) machining
  - title: Krishnan Suresh and Daniel C. H. Yang, Constant scallop-height machining of free-form surfaces, ASME Journal of Engineering for Industry 116(2), 253-259, 1994
    locator: the placement of each pass from the last one so that the scallop height between them is constant
  - paper: doi:10.1115/1.2803642
    title: Rong-Shine Lin and Yoram Koren, Efficient tool-path planning for machining free-form surfaces, ASME Journal of Engineering for Industry 118(1), 20-28, 1996
    locator: the path interval from the target scallop height and the local curvature, and the generation of the next pass from the last one
---

An iso-scallop toolpath finishes a surface with a ball end mill by placing each pass next to the last one so that the ridge left between them, the [scallop height](/scallop-height/), is exactly the allowed value $h$. Where the surface is concave across the passes, the ridges are lower for a given step, so the passes spread out; where it is convex, they move closer. Compared with a path that uses one fixed step chosen for the worst place, this gives the same finish with fewer passes. This is a manufacturing method of mechanical CAD: placement and routing here mean where a cutter goes and how it moves, not the placement and routing of a circuit. The code places the passes on a profile surface $z = f(x)$, where the scallop between two passes is a two-dimensional problem, and it checks the result against the closed form for a cylinder.

## In plain words

A round tool leaves a small ridge between two neighbouring passes. The finish is as good as the highest ridge, so a careful planner looks at the worst place on the part and uses the step that keeps the ridge small enough there. On the rest of the part this step is smaller than needed, and the tool runs more passes than it has to.

An iso-scallop path does not use one step. After each pass, it asks how far it can move the tool before the ridge gets too high, and it moves exactly that far. On a hollow, the tool can move farther. On a bump, it must move less.

The answer to that question is found by trial: try a step, measure the ridge, and halve the gap between a step that is too small and a step that is too large until the two agree.

## The problem

The input is a surface, a ball end mill of radius $r$ and a target scallop height $h$. The output is a set of passes whose neighbouring pairs leave a scallop of height $h$, with the boundary as the first and the last pass.

On a translational surface $z = f(x)$ the passes run along $y$, and the cross-section is a profile $p(t) = (t, f(t))$ with unit normal $n(t)$. The ball that touches the profile at $p(t)$ has its center at $c(t) = p(t) + r\,n(t)$, which is the [cutter location](/cutter-location-data/) of the pass. Between two passes the tool leaves a ridge whose top, the cusp, is the meeting point of the two tool circles on the side of the surface. The scallop height $H(t, t')$ is the distance from the cusp to the profile.

For small steps the step $w$ along the surface that gives height $h$ is about
$$
w \approx \sqrt{\frac{8 h r \rho}{\rho + r}}
$$
where $\rho$ is the radius of curvature of the surface across the passes, positive on a convex part and negative on a concave part, and $\rho = \infty$ on a plane gives $\sqrt{8rh}$. This is the formula of the [scallop height](/scallop-height/) page.

## The algorithm

```pseudo id=main
ISO-SCALLOP(profile on [a, b], r, h)
L1  t ← a; passes ← [a]
L2  while SCALLOP(t, b) > h do
L3      double a trial step from t until SCALLOP(t, t + step) > h, or the step reaches b
L4      bisect between the last good step and the first bad one, 60 times; t' ← the good end
L5      append t' to passes; t ← t'
L6  append b and return passes

SCALLOP(t0, t1)
L7  c0 ← p(t0) + r n(t0); c1 ← p(t1) + r n(t1)
L8  q ← the meeting point of the circles of radius r around c0 and c1 on the side of the surface
L9  return the distance from q to the profile between t0 and t1, by golden-section search
```

Line L4 keeps the end whose height is at most $h$, so every pair of passes stays within the target even if the height does not grow with the step. Line L9 is a [golden-section search](/golden-section-search/), and line L4 is the [bisection method](/bisection-method/). On a general surface the same step is taken at many points along the last pass, and the new contact points are joined into the next pass.

## Example

Take a ball end mill with $r = 5$ and the target $h = 0.05$. The table gives the step between passes on three surfaces, measured along the surface.

| surface | step from the closed form | small-step formula |
|---|---|---|
| plane | $2\sqrt{r^2 - (r - h)^2} = 1.4107$ | $\sqrt{8rh} = 1.4142$ |
| convex cylinder, $R = 20$ | $R\theta = 20 \times 0.063011 = 1.2602$ | $1.2649$ |
| concave cylinder, $R = 20$ | $R\theta = 20 \times 0.081553 = 1.6311$ | $1.6330$ |

A path with one fixed step for a part that has all three regions must use 1.2602 everywhere, which is about 29 percent more passes on the concave region than an iso-scallop path. On the sine profile $z = 3\sin(x/4)$ for $0 \le x \le 30$, with $r = 2$ and $h = 0.02$, the code places 62 passes, with steps in $x$ from 0.446 to 0.713. A fixed step of 0.446 in $x$ needs 69 passes. These counts are measured, not proved.

## Correctness

**Theorem.** If ISO-SCALLOP returns $a = t_0 < \dots < t_N = b$, every neighbouring pair has a computed scallop height of at most $h$. For each pair before the last, a pass at most $(b - a)2^{-60}$ farther would have a height above $h$. If short steps always have a height at most $h$, the method stops.

The doubling and the bisection keep two facts: the lower end has height at most $h$, and the upper end has height above $h$. The new pass is the lower end, and the gap between the ends is at most $(b - a)2^{-60}$ after 60 steps. On a convex or concave cylinder the cusp lies on the bisecting line by symmetry, and the law of cosines gives the closed-form angle $\theta$ with $\cos(\theta/2) = ((R \pm r)^2 + (R \pm h)^2 - r^2)/(2(R \pm r)(R \pm h))$. The full proof is in the proof file.

**What is measured.** The theorem is about the computed height. The tests compare the passes on planes and on convex and concave cylinders with the closed forms, within $10^{-9}$. They compare the cusp distance on a sine profile with a brute force that shoots the normal ray from each sample point of the profile to the first of the two tool circles, within $10^{-4}$ of $h$. The pass counts against a fixed step are measured.

## Complexity

Each call of SCALLOP takes $G = 80$ golden-section steps. Each pass takes $O(\log((b - a)/w_0))$ doubling steps and 60 bisection steps, with $w_0 = \sqrt{8rh}/2$ the first trial. With $B$ the number of these steps per pass, the time is $O(NBG)$ for $N$ passes, and the space is $O(1)$ apart from the output. On a general surface each pass is a curve, and the cost per pass grows with the number of points on it.

## Properties

- **Constant finish.** Every pair of passes leaves the same scallop height, so no part of the surface is finished better than needed.
- **Fewer passes.** The path is shorter than an iso-parametric or iso-planar path for the same worst scallop. The saving depends on how much the curvature varies.
- **Pass after pass.** Each pass depends on the last one, so errors add up along the passes, and the passes cannot be computed in parallel.
- **Not exact.** The method finds roots and minima numerically; it does not use exact arithmetic.

## Variants and improvements

- **Curvature formula in place of the search.** Lin and Koren (1996) compute the step from the target height and the local curvature, with the small-step formula, which is fast but only first order.
- **Points along the pass.** On a free-form surface, the next pass is made of the new contact points found at many points of the last one. Where the passes converge or diverge, points must be added or removed, and loops in the new pass must be cut off.
- **Other tools.** For a flat or bull-nose end mill the scallop depends on the tool axis, and the same placement works with the tool profile in place of the circle.
- **Spirals.** Iso-scallop passes can be joined into a spiral, as in the [Fermat spiral](/fermat-spiral-toolpath/) paths of additive manufacturing.

## When to use it

Use an iso-scallop path for the finishing of free-form surfaces whose curvature varies, where a fixed step would waste many passes, and where the finish must be even. For a roughing pass, or for a surface of almost constant curvature, a simpler [iso-planar](/iso-planar-toolpath/) or [iso-parametric](/iso-parametric-toolpath/) path is enough.

## Pitfalls

- **Self-intersecting passes.** On a free-form surface the next pass can fold over itself where the last pass is strongly curved. The loops must be detected and cut.
- **Gouging.** A ball whose radius exceeds the radius of a concave region cannot touch it without cutting the part, and the contact model fails. See [gouge detection](/gouge-detection/).
- **Height not monotone.** The scallop height need not grow with the step on a wavy surface. A search that assumes it does can skip a high ridge; the bisection here keeps a good end, but it can return a step that is not the largest good one.
- **Error build-up.** Each pass is placed from the last one, so a small error in the first pass carries to all later passes.

## Implementations

## History

Suresh and Yang (1994) placed each pass on a free-form surface so that the scallop height to the last pass is constant. Lin and Koren (1996) made the method efficient with a curvature-based step and a direct construction of the next pass. Choi and Jerard (1998) compare iso-scallop machining with the iso-parametric and iso-planar methods.

## References
