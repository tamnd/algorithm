---
tag: P1VX9T
kind: problem
slug: support-structure-generation
name: Support structure generation
aliases:
- support generation
area: cad/cam-and-additive-manufacturing
level: core
summary: Add removable structures under overhangs whose slope exceeds a critical angle, so each layer has material below it, with little extra material.
prereqs: [build-orientation, slicing-for-additive-manufacturing]
see_also: [tree-support, euclidean-steiner-tree-problem, minkowski-sum, polygon-clipping, triangle-mesh-slicing, infill-pattern, topology-optimization]
sources:
  - paper: doi:10.1111/cgf.12437
    title: Juraj Vanek, Jorge A. Garcia Galicia and Bedrich Benes, Clever support, efficient support structure generation for digital fabrication, Computer Graphics Forum 33(5), 2014, 117 to 125 (SGP 2014)
    locator: the detection of the points that need support and the comparison of tree supports with the supports of common slicers
  - paper: doi:10.1137/0132072
    title: M. R. Garey, R. L. Graham and D. S. Johnson, The complexity of computing Steiner minimal trees, SIAM Journal on Applied Mathematics 32(4), 1977, 835 to 859
    locator: the NP-hardness of the Euclidean Steiner tree problem
  - book: isbn:978-3-030-56126-0
    title: Ian Gibson, David Rosen, Brent Stucker and Mahyar Khorasani, Additive Manufacturing Technologies, 3rd edition, Springer, 2021
    locator: the discussion of support structures for the different process families (chapter not confirmed)
---

Support structure generation is the problem of adding temporary material to a print so that every layer has something to rest on. A layer can stick out a little past the layer below it, but not much. A face that slopes down at a shallow angle, an overhang, and a point that is lower than everything around it, an island, would print onto air. The supports hold these regions up while the part is built and are removed afterwards. The goal is a structure that holds every region that needs it, does not pass through the part, can be removed, and uses little material, time and contact area with the part. The critical angle is a property of the process and the material. For material extrusion a value near $45°$ from the horizontal is a common rule of thumb, not a theorem. The minimum-length version is close to a Steiner tree problem, which is NP-hard, but this page claims no hardness for the support problem itself. The methods in use are heuristics.

## In plain words

A printer puts each new layer on top of the last one. If a layer reaches out too far, the new material has nothing under it and droops or falls. So the printer first builds props under such places, like the scaffolding under a bridge that is being built. After the print, the props are broken or washed off.

Props cost plastic and time, and they leave marks where they touch the part. A good support plan holds up every part that needs it and uses as few and as small props as it can.

## Definition

**Input.** A closed triangle mesh $M$ in its build orientation, with build direction $+z$ and the plate at $z = 0$, a layer thickness $t$, and a critical angle $\alpha$ measured from the horizontal. Often also a bead width $w$ and a minimum feature size.

**What needs support.** There are two equivalent views.

- *Facets.* A facet with outward normal $n$ needs support if it faces down and is less steep than $\alpha$: $n_z < 0$ and $n_z^2 > \cos^2\!\alpha \,\|n\|^2$ (no square root needed). A vertex that is strictly lower than all its neighbors starts an island and needs support. Facets on the plate need none.
- *Layers.* Let $L_j$ be the region of layer $j$, a [polygon with holes](/polygon-with-holes/). A point of $L_j$ is self-supported if it lies within the horizontal distance $r = t \cot\alpha$ of $L_{j-1}$. The region that needs support in layer $j$ is $L_j \setminus (L_{j-1} \oplus D_r)$, where $D_r$ is the disk of radius $r$ and $\oplus$ is the [Minkowski sum](/minkowski-sum/). This is a polygon difference, see [polygon clipping](/polygon-clipping/).

**Output.** A support structure $S$, a set of solids or of struts with a width, such that:

1. every region that needs support, in the part and in $S$ itself, rests on $S$, on the part below, or on the plate, under the same angle rule;
2. $S$ does not overlap the interior of the part, and touches it only at contact regions;
3. $S$ can be removed: each piece is reachable for a tool, or soluble.

**Objective.** Minimize the volume of $S$, or the print time of $S$, or the contact area with the part, or a weighted sum. Some processes add other costs: in metal powder bed fusion supports also conduct heat and hold the part against warping, and in resin printing they must resist the peel force of each layer.

**Why about $45°$.** In one layer of thickness $t$, a face that rises at the angle $\beta$ from the horizontal moves outward by $t \cot\beta$. A bead of width $w$ stays on the bead below if it moves out by at most about $w/2$. So the face is self-supporting if $t\cot\beta \le w/2$, that is $\tan\beta \ge 2t/w$. With the common setting $w = 2t$, this gives $\beta \ge 45°$. This is a geometric estimate. Cooling, speed, material and the bridging of short gaps all change the real limit, so slicers expose $\alpha$ as a setting.

## Variants

- **Ground only or on the part.** Supports may stand only on the plate, or also on lower parts of the part. The second uses less material and leaves more marks.
- **Shape of the support.** Vertical pillars or walls under each overhang region, sparse lines or a grid like an [infill pattern](/infill-pattern/), branching [tree supports](/tree-support/), or lattices.
- **Bridges.** A horizontal span between two supported ends can print without support if it is short. Some methods build bridges on purpose, as in the scaffoldings of Dumas, Hergel and Lefebvre (2014).
- **Support-free design.** Change the orientation (see [build orientation](/build-orientation/)) or the shape, for example add $45°$ chamfers under overhangs, so that nothing needs support. [Topology optimization](/topology-optimization/) can include an overhang constraint for the same goal.
- **Soluble supports.** A second material that dissolves removes the access condition.

## Examples

**A T shape.** Let the part be a stem $10 \times 10 \times 30$ mm with a crossbar $30 \times 10 \times 10$ mm on top, centered, so the crossbar sticks out 10 mm on each side at heights 30 to 40 mm. The underside of each arm is a horizontal facet with $n = (0, 0, -1)$, so $n_z^2 = 1 > \cos^2 45° = \tfrac12$: it needs support. The two arms have $2 \cdot 10 \cdot 10 = 200$ mm² of overhang at height 30.

| plan | support volume | contact area |
|---|---|---|
| solid pillars from the plate | $2 \cdot 10 \cdot 10 \cdot 30 = 6000$ mm³ | 200 mm² |
| the same pillars as 20% sparse infill | about 1200 mm³ | 200 mm² |
| chamfer each arm underside at $45°$ | 0 (but the part changes) | 0 |
| print the T upside down | 0 | 0 |

In the layer view with $t = 0.2$ mm and $\alpha = 45°$, $r = 0.2$ mm. Layer $L_j$ at $z = 30$ is the $30 \times 10$ rectangle and $L_{j-1}$ is the $10 \times 10$ square. The region that needs support is the rectangle minus the square grown by 0.2 mm, two pieces of $9.8 \times 10$ mm, a total of 196 mm². The other 4 mm² print on the edge of the stem.

**A tie at the threshold.** A facet with the normal $n = (0, -1, -1)$ slopes at exactly $45°$. Then $n_z^2 = 1$ and $\cos^2 45° \cdot \|n\|^2 = 1$, so the strict test says it needs no support. With floats, $\cos 45°$ is rounded and the same facet can fall on either side. An exact test with $\cos^2\alpha$ as a rational number decides the tie.

## Known algorithms

- **Pillars and zones.** Project each overhang region straight down to the plate or to the part and fill the column with a sparse pattern. This is the default of most slicers. It is simple and uses a lot of material under high overhangs.
- **[Tree supports](/tree-support/).** Vanek, Garcia Galicia and Benes (2014) find the points that need support and merge their support cones top down into trees of struts. They measured on average about 40% less support material and 29% less print time than the supports of the slicers they compared with. These are measured numbers on their test models, not bounds.
- **Scaffolding with bridges.** Dumas, Hergel and Lefebvre (2014) build supports from vertical pillars joined by horizontal bridges.
- **Layer-based support regions.** The layer view of the definition gives the support region of each layer with polygon offsets and differences. Slicers then fill those regions.

## Bounds

- **Area that needs support.** In the facet view the area that needs support is $\sum_f A_f$ over the overhang facets. For solid vertical pillars on the plate, the volume is fixed by the geometry: it is the integral of the height above the plate over the projection of that area. Sparse pillars scale it by the density, and trees and bridges can use less.
- **Hardness.** For points that need support and struts that may lean within a cone, the shortest support is a Steiner-type tree with a slope rule and free end points on the plate. The [Euclidean Steiner tree problem](/euclidean-steiner-tree-problem/) is NP-hard (Garey, Graham and Johnson 1977), and Vanek and coauthors relate their problem to it. This page does not give a reduction, so the NP-hardness of the support problem itself is not claimed here. The methods in use are heuristics with no bound on how far they are from the optimum.
- **Counting.** With $n$ facets and $k$ layers, the layer view needs $k$ polygon differences, each of a size that depends on the contours, so it is polynomial in the size of the slices.

## Reductions

- **From the layer view to polygon operations.** The support region of each layer is a Minkowski sum and a difference of polygons, so support region detection reduces to polygon offsetting and clipping.
- **Shortest tree support and Steiner trees.** If all points are at the same height far above the plate and struts may lean almost freely, the shortest support is close to a Steiner tree of the points with one trunk. This links the two problems, but it is not an exact reduction.
- **To orientation.** For each build direction the cost of the best support is one objective of [build orientation](/build-orientation/).

## Applications

- Material extrusion, where supports are printed in the same or a soluble material.
- Vat photopolymerization, where parts hang from the plate and every island needs a support point.
- Metal powder bed fusion, where supports also carry heat away and hold the part against thermal stress.
- Design for additive manufacturing, where designers change shapes to need fewer supports.

## References
