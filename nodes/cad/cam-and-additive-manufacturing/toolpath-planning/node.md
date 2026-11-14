---
tag: H9F8NN
kind: problem
slug: toolpath-planning
name: Toolpath planning
aliases:
- toolpath generation
area: cad/cam-and-additive-manufacturing
level: intro
summary: Given a part, a tool and a machine, find a path for the tool that removes or deposits the right material with no gouge or collision, in short time.
prereqs: [coverage-path-planning, minkowski-sum]
see_also: [pocket-machining, cutter-location-data, scallop-height, gouge-detection, nc-verification, slicing-for-additive-manufacturing, infill-pattern, traveling-salesman-problem]
sources:
  - book: isbn:978-0-412-78020-2
    title: Byoung K. Choi and Robert B. Jerard, Sculptured Surface Machining, Theory and Applications, Kluwer Academic Publishers, 1998
    locator: the chapters on the fundamentals of tool-path generation, on gouge and collision, and on the kinds of finishing paths
  - book: isbn:978-3-540-54103-5
    title: Martin Held, On the Computational Geometry of Pocket Machining, Lecture Notes in Computer Science 500, Springer, 1991
    locator: the introduction, which states the planar problem of clearing a pocket with a disk tool
  - paper: doi:10.1016/S0925-7721(00)00015-8
    title: Esther M. Arkin, Sándor P. Fekete and Joseph S. B. Mitchell, Approximation algorithms for lawn mowing and milling, Computational Geometry 17(1-2), 25-50, 2000
    locator: the definitions of the lawn mowing and milling problems, their NP-hardness and their approximation algorithms
---

Toolpath planning asks how a tool should move so that a machine makes a given part. In milling, the tool is a rotating cutter, and the path must remove all the material of the stock that is not part, without cutting into the part. In 3D printing, the tool is a nozzle or a laser spot, and the path must put material exactly where the part is. In both cases the path must not hit the part or the machine with the tool holder, and it should take little time. This is a problem of mechanical manufacturing: placement and routing here mean where a tool goes and how it moves, not the placement and routing of the cells and wires of a circuit. This page states the problem and its limits. The methods are on the pages that it links.

## In plain words

You have a block of material and a drawing of the part you want. A machine holds a tool and can move it. You must tell the machine where to move the tool, step by step, so that what remains at the end is the part.

The tool has a size and a shape. It cannot get into corners smaller than itself, and its round end leaves small ridges between passes. If the tool goes too deep, it spoils the part. The holder must not hit the part either. Among all the paths that make a good part, you want a short and smooth one, because the machine time costs money.

A 3D printer has the same task the other way round: it lays a thin bead along a path, layer by layer, and the beads must fill the part without gaps.

## Definition

**Input.** A part $P$ and a stock $S \supseteq P$, both solids in space. A tool $T$, a solid of revolution around its axis, such as a ball, flat or bull-nose end mill, with a holder above it. A machine, which fixes the allowed tool axes: one vertical axis on a three-axis machine, a cone of axes on a five-axis machine. A tolerance $\varepsilon > 0$.

**Path.** A path is a curve $\gamma(t) = (c(t), a(t))$ of tool positions $c$ and unit axis directions $a$, for $t \in [0, 1]$, in one or more pieces joined by rapid moves clear of the stock. The tool removes the [swept volume](/swept-volume/) $W(\gamma) = \bigcup_t T(c(t), a(t))$, the union of the placed tools, which for a fixed axis is the [Minkowski sum](/minkowski-sum/) of the path with the tool. The list of positions sent to the machine is the [cutter location data](/cutter-location-data/).

**Feasible path (milling).**

1. *No gouge.* The tool does not enter the part: the interior of $W(\gamma)$ does not meet $P$.
2. *No collision.* The holder and the machine do not meet the part or the stock away from the cut.
3. *Enough removed.* What is left, $S \setminus W(\gamma)$, lies within distance $\varepsilon$ of $P$. On finished surfaces this bounds the [scallop height](/scallop-height/).

**Goal.** Among feasible paths, minimize a cost: the machining time, the length, the number of retractions, or a mix that also counts sharp turns and the load on the tool. The machining time depends on the length and on how often the machine must slow down.

**Additive form.** The tool deposits a bead, a disk or a ball of material, along the path. The path must fill each layer of the part, the deposited set must lie within $\varepsilon$ of the layer, and the path should have few starts and stops.

Some parts cannot be made at all with a given tool: material in a corner smaller than the tool, or in a place that no allowed axis can reach, stays. Then the goal is to remove all material that the tool can reach, and to report the rest.

## Variants

- **2.5D milling.** The part is a stack of flat levels, and each level is a [pocket machining](/pocket-machining/) problem in the plane.
- **Three-axis surface finishing.** A ball or bull-nose tool with a vertical axis follows a free-form surface. The passes can follow the parameter lines of the surface ([iso-parametric](/iso-parametric-toolpath/)), parallel planes ([iso-planar](/iso-planar-toolpath/)), or a fixed scallop height ([iso-scallop](/iso-scallop-toolpath/)). The grid method of the [inverse tool offset](/inverse-tool-offset/) gives gouge-free tool positions for any part.
- **Five-axis machining.** The axis can tilt, which reaches more of the part and allows wider passes, but adds collision checks. The axes that reach a point form its [accessibility cone](/accessibility-cone/).
- **Roughing and finishing.** Roughing removes the bulk fast with a large tool and leaves a thin layer. Finishing removes the layer to the tolerance.
- **Additive manufacturing.** The part is cut into layers by [slicing](/slicing-for-additive-manufacturing/), and each layer is filled with a wall path and an [infill pattern](/infill-pattern/) or with one continuous [Fermat spiral](/fermat-spiral-toolpath/).
- **Coverage by robots.** A mower or a cleaning robot that must pass over every point of a floor solves the planar coverage problem, see [coverage path planning](/coverage-path-planning/).

## Examples

**A straight slot.** A slot of width $2r$ and length $\ell + 2r$ with rounded ends, cut by a flat end mill of radius $r$ to a fixed depth. One straight pass of length $\ell$ along the middle removes the slot exactly. This path meets the length bound below with equality.

**A rectangular pocket.** A $10 \times 10$ pocket and a tool of radius 1. The tool center must stay in the square $[1, 9]^2$, so the corners keep $(4 - \pi) \approx 0.86$ of material that no path removes. The machinable area is $96 + \pi$, and every path that removes it has length at least 48 by the bound below.

**A ball on a slope.** A ball end mill of radius $r$ that touches a plane at the point $p$ has its center at $p + r\,n$, where $n$ is the unit normal. Moving the center over the offset of the surface keeps the ball on the surface. Passes a distance $w$ apart on a flat surface leave scallops of height $r - \sqrt{r^2 - w^2/4}$.

**A printed square layer.** A $10 \times 10$ layer printed with a bead of width 0.5 needs about $100 / 0.5 = 200$ of path for the infill, by the same area argument as in the bound below.

## Known algorithms

- **Pockets.** [Contour-parallel](/contour-parallel-toolpath/), [direction-parallel](/direction-parallel-toolpath/) and [Voronoi](/voronoi-pocket-machining/) paths. See [pocket machining](/pocket-machining/).
- **Free-form surfaces.** [Iso-parametric](/iso-parametric-toolpath/), [iso-planar](/iso-planar-toolpath/) and [iso-scallop](/iso-scallop-toolpath/) paths, with tool positions from offsets or from the [inverse tool offset](/inverse-tool-offset/), and checks by [gouge detection](/gouge-detection/).
- **Verification.** [NC verification](/nc-verification/), for example on a [z-map model](/z-map-model/), simulates the cut and finds gouges and missed material.
- **Additive layers.** [Triangle mesh slicing](/triangle-mesh-slicing/) and [adaptive slicing](/adaptive-slicing/) make the layers. [Infill patterns](/infill-pattern/) and [Fermat spirals](/fermat-spiral-toolpath/) fill them, and [support structure generation](/support-structure-generation/) adds supports.
- **Order of pieces.** The order in which the pieces of a path are cut, and the moves between them, are a [traveling salesman problem](/traveling-salesman-problem/) on the pieces, solved by heuristics.

## Bounds

**Length from area.** Take a planar path of total length $L$ and a disk tool of radius $r$. The region that the tool sweeps is the Minkowski sum of the path with the disk, and its area is at most $2rL + \pi r^2$ for each connected piece. So a path that removes a region of area $A$ in one piece has
$$
L \ge \frac{A - \pi r^2}{2r}.
$$
The straight slot above meets this bound. Any overlap of neighbouring passes makes the path longer, and in practice paths are longer than the bound because they overlap and turn. The same argument with a bead of width $b$ gives $L \ge A / b$ approximately for a printed layer.

**What no path removes.** With a disk tool of radius $r$ in a planar region $P$, the tool center must stay in the inward offset $P_r$, so no path removes more than the opening $P_r \oplus D_r$. In a corner with angle $\alpha$, the material $r^2(\cot(\alpha/2) - (\pi - \alpha)/2)$ stays. In three-axis machining, a concave part of the surface with a radius of curvature smaller than the ball radius cannot be reached by the ball without a gouge, so the tool must stop short and leave material there.

**Hardness.** The planar milling problem, find the shortest path of a disk that stays in a region and sweeps all of it that it can reach, is NP-hard for regions with holes (Arkin, Fekete and Mitchell, 2000). So is the lawn mowing problem, where the tool may leave the region. Both have polynomial-time algorithms with a constant approximation factor. Minimizing the number of retractions of a zigzag path in a pocket with holes is NP-hard as well (Arkin, Held and Smith, 2000, see [pocket machining](/pocket-machining/)). For free-form surfaces with gouge, collision and machine time constraints, no exact optimal method is known, and the methods in use are judged by measured length, time and surface quality.

## Reductions

- **To offsets.** For a ball end mill, the tool centers that touch but do not enter the part form the [offset surface](/offset-surface/) at the ball radius, cut where it folds. For a solid part the set of free tool positions is the complement of an offset solid, see [solid offsetting](/solid-offsetting/). Toolpath planning becomes the planning of a path for a point on this set.
- **To coverage.** With the free set known, removing the material is covering a region with the swept tool, which is [coverage path planning](/coverage-path-planning/).
- **To the traveling salesman problem.** When the passes are fixed, the order and the direction of the passes, and the links between them, form a traveling salesman problem on the passes.
- **Additive to planar.** Slicing turns a 3D print into one planar fill problem per layer.

## Applications

- **CNC milling.** Molds, dies, turbine blades, car bodies and aircraft parts are milled from paths made by CAM systems.
- **3D printing.** Every printer runs a path made by a slicer from the layers of the part.
- **Laser and water-jet cutting, engraving.** A path along the contours, with an order that keeps the moves short and the heat spread.
- **Robot coverage.** Mowing, painting, cleaning and inspection use the same path planning in the plane.

## References
