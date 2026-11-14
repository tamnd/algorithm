---
tag: G3VS8H
kind: definition
slug: scallop-height
name: Scallop height
aliases:
- cusp height of machining
area: cad/cam-and-additive-manufacturing
level: core
summary: The height of the ridges that a ball or round tool leaves between two neighbouring passes, which sets the step over for a given surface finish.
prereqs: [cutter-location-data, surface-curvature]
see_also: [iso-scallop-toolpath, iso-parametric-toolpath, iso-planar-toolpath, direction-parallel-toolpath, staircase-effect, fundamental-forms, z-map-model, toolpath-planning]
sources:
  - book: isbn:978-0-412-78020-2
    title: Byoung K. Choi and Robert B. Jerard, Sculptured Surface Machining, Theory and Applications, Kluwer Academic Publishers, 1998
    locator: chapter 5, fundamentals of tool-path generation, the parts on the path interval and the scallop height of ball and round tools
  - paper: doi:10.1115/1.2803642
    title: Rong-Shine Lin and Yoram Koren, Efficient tool-path planning for machining free-form surfaces, ASME Journal of Engineering for Industry 118(1), 20-28, 1996
    locator: the path interval of a ball end mill from the allowed scallop height and the normal curvature of the surface across the passes
  - title: Krishnan Suresh and Daniel C. H. Yang, Constant scallop-height machining of free-form surfaces, ASME Journal of Engineering for Industry 116(2), 253-259, 1994
    locator: the scallop height between two passes of a ball end mill on a free-form surface
---

The scallop height is the height of the ridge of material that a round tool leaves between two neighbouring passes. A ball end mill cuts a groove with a round bottom along each pass. Two grooves side by side leave a ridge between them, the scallop or cusp, and its height, measured from the design surface along the normal, sets the roughness of the finished surface. The larger the step-over between passes, the higher the scallops, so the allowed scallop height fixes the step-over and with it the length of a finishing path. This is a term of mechanical manufacturing, not of electronic design. The same word, cusp height, is used for the steps of the layers of additive manufacturing, which is the [staircase effect](/staircase-effect/) and has a different formula.

## Definition

Take two neighbouring passes of a tool over a surface, and a cross-section across the passes. In this plane the surface is a curve, and the tool at each pass is a shape that touches the curve at the contact point of the pass. The tool removes all material on its side of this shape. The *cusp* is the point where the two tool shapes meet on the side of the surface, which is the top of the material left between them. The **scallop height** $h$ is the distance from the cusp to the surface. The **step-over** or path interval $w$ is the distance between the two contact points along the surface.

**Ball end mill on a plane.** The tool cross-section is a circle of radius $r$ whose center is $r$ above the contact point. With contacts at $x = 0$ and $x = w$, the circles meet above $x = w/2$ at height $r - \sqrt{r^2 - w^2/4}$, so
$$
h = r - \sqrt{r^2 - \frac{w^2}{4}} \approx \frac{w^2}{8r}, \qquad w = 2\sqrt{2rh - h^2}.
$$
The approximation holds for $w$ small next to $r$.

**Ball end mill on a cylinder.** On a convex cylinder of radius $R$, with contact points an angle $\theta$ apart (so $w = R\theta$), the tool centers lie on the circle of radius $R + r$ and the cusp lies on the bisecting line at distance $R + h$ from the axis. The law of cosines gives
$$
h = (R + r)\cos\frac{\theta}{2} - \sqrt{r^2 - (R + r)^2\sin^2\frac{\theta}{2}} - R.
$$
On a concave cylinder with $R > r$, the centers lie on the circle of radius $R - r$ and the cusp at distance $R - h$:
$$
h = R - (R - r)\cos\frac{\theta}{2} - \sqrt{r^2 - (R - r)^2\sin^2\frac{\theta}{2}}.
$$
For small steps both become
$$
h \approx \frac{w^2}{8}\Big(\frac{1}{r} \pm \frac{1}{R}\Big), \qquad w \approx \sqrt{\frac{8hrR}{R \pm r}},
$$
with $+$ for convex and $-$ for concave. On a general surface, $\pm 1/R$ is replaced by the normal curvature $\kappa$ of the surface across the passes, from the second [fundamental form](/fundamental-forms/), with $\kappa > 0$ on convex parts. The inverse for the cylinder is $\cos(\theta/2) = ((R \pm r)^2 + \rho^2 - r^2)/(2(R \pm r)\rho)$ with $\rho = R \pm h$.

**Bull-nose end mill on a plane.** A torus cutter with corner radius $r_c$ and flat radius $R_f$ leaves no scallop when $w \le 2R_f$, because the flat bottoms of the two passes meet. For $2R_f < w \le 2(R_f + r_c)$ the corner arcs meet, and
$$
h = r_c - \sqrt{r_c^2 - (w/2 - R_f)^2}.
$$

## Examples and non-examples

**Examples.**

- A ball end mill with $r = 5$ and step-over $w = 4$ on a plane leaves $h = 5 - \sqrt{21} = 0.4174$. The small-step formula gives $16/40 = 0.4$.
- To get $h = 0.01$ with $r = 5$ on a plane, the step-over is $w = 2\sqrt{0.1 - 0.0001} = 0.6321$, against $\sqrt{8 \cdot 5 \cdot 0.01} = 0.6325$ from the approximation.
- With $r = 5$ and $R = 20$, the same steps leave different scallops on different shapes:

| step along the surface | convex cylinder | plane | concave cylinder |
|---|---|---|---|
| $w = 2$ ($\theta = 0.1$) | 0.1274 (approx. 0.125) | 0.1010 | 0.0753 (approx. 0.075) |
| $w = 4$ ($\theta = 0.2$) | 0.5426 (approx. 0.5) | 0.4174 | 0.3045 (approx. 0.3) |

- A bull-nose end mill with $r_c = 2$ and $R_f = 3$ on a plane leaves no scallop at $w = 5$, a scallop of $2 - \sqrt3 = 0.2679$ at $w = 8$, and $h = r_c = 2$ at $w = 10 = 2(R_f + r_c)$, the largest step at which the two passes still meet.

**Non-examples.**

- **A flat end mill on a flat floor.** With $w$ less than the tool diameter, the floor is flat and the scallop height is 0. The marks on the floor come from the teeth and the feed, not from the step-over.
- **Feed marks.** The small waves along a pass, one per tooth, come from the feed per tooth. They are a different roughness, along the passes, not across them.
- **Chord error.** When a curved pass is sent to the machine as straight segments, each segment lies off the curve by its sagitta $\varepsilon$. On a circle of radius $\rho$, a chord with sagitta $\varepsilon$ has length $2\sqrt{2\rho\varepsilon - \varepsilon^2}$. This error is along the passes, and it adds to the scallop but is not the scallop.
- **The staircase effect.** In additive manufacturing, the cusp height of a layer is the distance between a sloped design surface and the edge of a flat layer, about $t\,|\cos\phi|$ for layer thickness $t$ and an angle $\phi$ between the normal and the build direction. See [staircase effect](/staircase-effect/).

## Related definitions

- The tool positions of the passes are [cutter location data](/cutter-location-data/), and the scallop is measured between the contact points that they come from.
- An [iso-scallop toolpath](/iso-scallop-toolpath/) places each pass so that the scallop to the last pass equals the allowed height. [Iso-parametric](/iso-parametric-toolpath/) and [iso-planar](/iso-planar-toolpath/) paths use one step for the whole surface, chosen for the worst place.
- The normal curvature across the passes is the second [fundamental form](/fundamental-forms/) in that direction, divided by the first. See [surface curvature](/surface-curvature/).
- A simulation of the cut on a [z-map model](/z-map-model/) measures the scallops of a path on the real geometry.
- For pocket floors cut with a flat end mill, the step-over is limited by coverage and not by scallops. See [direction-parallel toolpath](/direction-parallel-toolpath/).

## References
