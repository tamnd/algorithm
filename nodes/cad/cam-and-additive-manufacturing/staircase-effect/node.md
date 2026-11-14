---
tag: Q74DWM
kind: concept
slug: staircase-effect
name: Staircase effect
aliases:
- stair-stepping
- layer cusp
area: cad/cam-and-additive-manufacturing
level: intro
summary: The stepped error of a layered part on sloped surfaces, measured by cusp height, which grows with layer thickness and with the angle to the build direction.
prereqs: [slicing-for-additive-manufacturing]
see_also: [adaptive-slicing, scallop-height, build-orientation, triangle-mesh-slicing]
sources:
  - paper: doi:10.1016/0010-4485(94)90032-9
    title: Atanas Dolenc and Ismo Mäkelä, Slicing procedures for layered manufacturing techniques, Computer-Aided Design 26(2), 1994, 119 to 126
    locator: the definition of the cusp height of a layer on a sloped surface
  - book: isbn:978-3-030-56126-0
    title: Ian Gibson, David Rosen, Brent Stucker and Mahyar Khorasani, Additive Manufacturing Technologies, 3rd edition, Springer, 2021
    locator: the discussion of stair stepping and layer thickness (chapter not confirmed)
---

The staircase effect is the error that a layered process makes on every surface that is not vertical. Each layer has vertical walls, so a sloped or curved surface becomes a flight of small steps. This is also called stair-stepping. The usual measure is the cusp height, the largest distance from the steps to the design surface along its normal. For a layer of thickness $t$ and a surface whose normal makes the angle $\theta$ with the build direction, the cusp height is $c = t\,|\cos\theta|$. Dolenc and Mäkelä (1994) used this measure to choose layer thicknesses, which is the basis of [adaptive slicing](/adaptive-slicing/).

## In plain words

A printer builds a part from flat layers with straight sides. A wall that goes straight up comes out right. A slope comes out as stairs, and a dome looks like a stack of coins. Thinner layers give smaller stairs. The stairs are tallest where the surface is almost flat, and they disappear on walls that go straight up. Near the top of a dome the stairs are the largest, so thin layers matter most there.

## The idea

Cut the part with a vertical plane that contains the normal of the surface. In this plane, the surface is a line with unit normal $(\sin\theta, \cos\theta)$, where $\theta$ is the angle from the build direction $z$. Put the origin on the surface at the bottom of a layer. The surface is the line $x\sin\theta + z\cos\theta = 0$. The slicer takes the contour at the bottom of the layer, so the layer has a vertical wall from $(0, 0)$ to $(0, t)$. The top corner $(0, t)$ is at distance
$$c = |0 \cdot \sin\theta + t\cos\theta| = t\,|\cos\theta|$$
from the surface. This is the cusp height, also called the layer cusp. Two cases follow at once:

- a vertical wall has $\theta = 90°$, so $c = 0$;
- a horizontal face has $\theta = 0°$, so $c = t$, the whole layer thickness.

The cusp height is a geometric bound. It assumes square layer edges, so it does not model the rounded edges of real beads, shrinkage or the resolution of the machine. If the slicer takes the contour at the middle of each layer, the steps cross the surface, and the largest distance on either side is $\tfrac12 t\,|\cos\theta|$. The error can also be measured as the area or the volume between the steps and the surface, which changes the formulas but not the trend.

The cusp height depends on the slope, so it depends on the [build orientation](/build-orientation/). Turning a part can move its flat faces to vertical walls, where they have no steps.

## Examples

- Layers of $t = 0.2$ mm on a surface with $\theta = 60°$ (a surface $30°$ from vertical) give $c = 0.2 \cdot \tfrac12 = 0.1$ mm.
- The same layers on a surface with $\theta = 30°$ (a gentle slope, $30°$ from horizontal) give $c = 0.2 \cdot \tfrac{\sqrt3}2 \approx 0.173$ mm.
- A triangle facet with the normal $n = (0, -4, 8)$ has $|\cos\theta| = 8/\sqrt{80} = 2/\sqrt5 \approx 0.894$. A bound $c \le \tfrac14$ then allows $t \le \tfrac14 \cdot \tfrac{\sqrt5}2 \approx 0.28$. With the squared test $t^2 \cdot 64 \le \tfrac1{16} \cdot 80$, this is checked without a square root.
- A hemisphere printed with its flat face down has $c = t$ at the top, where the surface is horizontal, and $c = 0$ at the equator.

## Where it is used

- [Adaptive slicing](/adaptive-slicing/) chooses each layer thickness so that the cusp height stays under a bound.
- [Build orientation](/build-orientation/) uses the total cusp height or the area of sloped surface as one of its objectives.
- Finishing by sanding or machining must remove material to a depth of up to $c$ to reach the design surface, if the steps lie outside it, so the cusp height tells how much stock to leave.
- [Scallop height](/scallop-height/) is the same kind of measure in machining: the ridge left between two passes of a ball-end tool.

## References
