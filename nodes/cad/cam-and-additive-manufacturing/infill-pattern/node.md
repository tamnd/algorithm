---
tag: SV3GQN
kind: concept
slug: infill-pattern
name: Infill pattern
aliases:
- sparse infill
area: cad/cam-and-additive-manufacturing
level: intro
summary: The partial filling of a printed part's interior, such as grid, honeycomb or gyroid, that trades weight and time against stiffness.
prereqs: [slicing-for-additive-manufacturing]
see_also: [direction-parallel-toolpath, contour-parallel-toolpath, fermat-spiral-toolpath, adaptive-slicing, scallop-height, implicit-surface, topology-optimization]
sources:
  - book: isbn:978-3-030-56126-0
    title: Ian Gibson, David Rosen, Brent Stucker and Mahyar Khorasani, Additive Manufacturing Technologies, 3rd edition, Springer, 2021
    locator: the discussion of fill patterns and build parameters for material extrusion (chapter not confirmed)
  - paper: "Alan H. Schoen, Infinite periodic minimal surfaces without self-intersections, NASA Technical Note TN D-5541, 1970"
    locator: the description of the gyroid
---

An infill pattern is the structure that a printer puts inside a part, between its outer walls. A solid interior takes the most material and time. Most extrusion slicers instead print a few solid shells (the outer walls and the top and bottom layers) and fill the inside with a sparse pattern, called sparse infill. Common patterns are parallel lines, a grid, triangles, a honeycomb and a gyroid. The two parameters are the pattern and the density, the fraction of the interior that is filled. A lower density saves material and time and makes the part lighter and less stiff. How much less stiff depends on the pattern, the material, the process and the load. This page gives the geometry of the patterns and makes no claim about their strength.

## In plain words

Most printed parts are not solid inside. The printer makes a closed skin and fills the inside with a light frame, like the cells of a beehive. A fuller frame makes a heavier and stiffer part that takes longer to print. Different shapes of frame use the same amount of plastic in different ways. Some shapes are the same in every layer, and some change from layer to layer so that they hold together in all three directions.

## The idea

A slicer first cuts the part into layer contours. It offsets each contour inward to get the walls, see [contour-parallel toolpath](/contour-parallel-toolpath/). The region that is left is filled with a pattern, clipped to the region.

- **Lines.** Parallel lines at spacing $s$, with the direction turned by $90°$ in each layer. This is a [direction-parallel toolpath](/direction-parallel-toolpath/) with a large spacing. Each layer has lines in one direction only.
- **Grid.** Lines in two directions in the same layer. The crossings print over the same spot twice.
- **Triangles.** Lines in three directions at $60°$, which divide the layer into triangles.
- **Honeycomb.** Hexagonal cells, the same in every layer, so the walls form vertical prisms.
- **Gyroid.** The gyroid is a periodic surface described by Schoen (1970). Slicers use the level set $\sin x \cos y + \sin y \cos z + \sin z \cos x = 0$, an [implicit surface](/implicit-surface/) that is close to it. Each layer prints the curve where the plane $z = $ const meets the surface, so the curve changes from layer to layer, and the walls connect in all three directions.

The density of a pattern with straight walls is its area fraction in one layer. With bead width $w$ and spacing $s$:

| pattern | filled fraction of a layer |
|---|---|
| lines at spacing $s$ | $w/s$ |
| grid at spacing $s$ | $1 - (1 - w/s)^2 = 2w/s - (w/s)^2$ |
| honeycomb of edge $a$ | about $\dfrac{2w}{\sqrt3\,a}$ for $w \ll a$ |

The grid has $(w/s)^2$ less than twice the line fraction because the squares where the two directions cross are counted once. For the honeycomb, each hexagon of area $\tfrac{3\sqrt3}2 a^2$ owns 3 of its 6 edges (each edge is shared by two cells), which is a wall length of $3a$, so the fraction is $3aw / (\tfrac{3\sqrt3}2 a^2) = 2w/(\sqrt3\,a)$ to first order in $w/a$.

The infill has no visible surface, so slicers often print it with thicker layers than the walls, which is a simple form of [adaptive slicing](/adaptive-slicing/). The ridges between neighbor beads of a solid fill are the printing analog of the [scallop height](/scallop-height/) between passes in machining.

## Examples

- Lines with $w = 0.4$ mm at $s = 2$ mm give a density of $0.4/2 = 20\%$.
- A grid with the same $w$ and $s$ gives $1 - 0.8^2 = 36\%$. A grid at $20\%$ needs $1 - (1 - w/s)^2 = 0.2$, so $w/s = 1 - \sqrt{0.8} \approx 0.106$ and $s \approx 3.8$ mm.
- A honeycomb with edge $a = 3$ mm and $w = 0.4$ mm gives about $2 \cdot 0.4 / (\sqrt3 \cdot 3) \approx 15\%$.
- In the gyroid level set, the plane $z = 0$ gives $\sin x \cos y + \sin y = 0$, that is $\sin y = -\sin x \cos y$, so $\tan y = -\sin x$, a wave curve. At $z = \pi/2$ the curve is $\sin x \cos y + \cos x = 0$, a different curve, shifted. Both are periodic with period $2\pi$.

## Where it is used

- Material extrusion printers use sparse infill in almost every part that is not a thin shell. Slicers expose the pattern and the density as settings.
- A Fermat spiral or contour fill is used for solid layers when the path should be continuous, see [Fermat spiral toolpath](/fermat-spiral-toolpath/).
- Graded infill changes the density inside one part, denser near loads and sparser elsewhere. [Topology optimization](/topology-optimization/) goes further and computes where material should be.
- Lattice and gyroid structures are also used in powder bed processes for light parts and heat exchangers, where the cells are part of the design, not only a filler.

## References
