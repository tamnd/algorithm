---
tag: G7CHSB
kind: problem
slug: five-axis-tool-orientation
name: Five-axis tool orientation
aliases:
- tool axis orientation
- tool inclination
area: cad/cam-and-additive-manufacturing
level: core
summary: Choose the tool axis at each cutter contact point in five-axis milling so the cut is wide, free of gouges and collisions, and the axis changes smoothly.
prereqs: [toolpath-planning, cutter-location-data, surface-curvature]
see_also: [principal-axis-method, collision-free-tool-orientation, accessibility-cone, gouge-detection, flank-milling, scallop-height, configuration-space, feedrate-scheduling]
sources:
  - book: isbn:978-0-412-78020-2
    title: Byoung K. Choi and Robert B. Jerard, Sculptured Surface Machining, Theory and Applications, Kluwer Academic Publishers, 1998
    locator: the material on five-axis machining, tool positioning and interference checks
  - paper: doi:10.1016/S0890-6955(96)00046-6
    title: N. Rao, F. Ismail and S. Bedi, Tool path planning for five-axis machining using the principal axis method, International Journal of Machine Tools and Manufacture 37(7), 1025-1040, 1997
    locator: the tilt of a flat or toroidal end mill from the local curvature, and the effect of the feed direction
  - paper: "Cha-Soo Jun, Kyungduck Cha and Yuan-Shin Lee, Optimizing tool orientations for 5-axis machining by configuration-space search method, Computer-Aided Design 35(6), 549-566, 2003"
    locator: the feasible region of tool orientations at each contact point in the space of two angles, and the smoothing of the orientations along the path
  - paper: "K. Morishige, K. Kase and Y. Takeuchi, Collision-free tool path generation using 2-dimensional C-space for 5-axis control machining, The International Journal of Advanced Manufacturing Technology 13(6), 393-400, 1997"
    locator: the map of collisions into a two-dimensional space of tool directions
---

Five-axis tool orientation is the problem of choosing the direction of the tool axis at each point of a toolpath in five-axis milling. A five-axis machine moves the tool in three linear axes and turns it, or the part, about two rotary axes, so at each cutter contact point the axis can point in any direction of a cone around the surface normal. The choice decides how wide a strip the tool cuts, whether it gouges the part near or far from the contact point, whether the holder hits the part or the fixture, whether the machine can reach the angles, and how fast the rotary axes must turn. This is the manufacturing side of mechanical CAD: it is about holding a cutter against a part, not about the placement and routing of circuits. The problem has no single agreed formal statement and no known hardness result. Practice solves it by local formulas, such as the [principal axis method](/principal-axis-method/), combined with feasibility maps of directions, such as the [accessibility cone](/accessibility-cone/) and the [C-space of tool orientations](/collision-free-tool-orientation/), and by smoothing along the path.

## In plain words

On a three-axis machine the cutter always points straight down. On a five-axis machine it can lean in any direction, like a hand that holds a pen at an angle.

Leaning helps in two ways. The cutter can reach under overhangs and into deep, steep pockets. And a cutter with a flat end, leaned a little, touches a curved surface over a wide band, so each pass removes a wider strip and the job needs fewer passes.

Leaning also brings dangers. The cutter can dig into the part beside the point it is cutting, and the holder can hit a wall. The machine has limits on how far it can turn, and it is slow when it must turn a lot between two nearby points. So at every point the angle must be safe, reachable and close to the angle at the point before.

## Definition

**Input.** A part surface $S$ with unit normals $n$ pointing out of the material. A path of cutter contact points $p_1, \dots, p_m$ on $S$ with feed directions $f_i$ tangent to $S$. A tool: a ball, flat or toroidal end mill with its shank and holder, as a solid of revolution about its axis. A machine: a kinematic chain with two rotary axes, their ranges, and their speed and acceleration limits. A tolerance $h$ for the material left between passes.

**Frame and angles.** At $p_i$ put $b_i = n_i \times f_i$. The tool axis is a unit vector $a_i$, written by a lead angle $\lambda$, a turn toward $f_i$, and a tilt angle $\omega$, a turn toward $b_i$:
$$
a_i = \cos\lambda\cos\omega\; n_i + \sin\lambda\; f_i + \cos\lambda\sin\omega\; b_i .
$$
The tool tip is then placed so that the tool touches $S$ at $p_i$ with normal $n_i$, which gives the [cutter location](/cutter-location-data/).

**Constraints.** For each $i$:

1. *No local gouge.* Near $p_i$ the tool surface stays on the outer side of $S$. For a ball this is a curvature test. For a flat or toroidal end mill it depends on the tilt, see [gouge detection](/gouge-detection/).
2. *No global gouge and no collision.* No other part of the tool, shank or holder enters the part or the fixture. For the axis as a half-line from the tool center, the set of free directions is the [accessibility cone](/accessibility-cone/) at $p_i$.
3. *Machine limits.* The rotary angles that give $a_i$ lie in the ranges of the machine.
4. *Smoothness.* The axis changes between neighbors stay small, $\angle(a_i, a_{i+1}) \le \delta$, and the rotary moves that realize them stay within the speed and acceleration limits.

**Goal.** Choose $a_1, \dots, a_m$ that satisfy the constraints and make the cut efficient. Usual objectives are the widest strip for the tolerance $h$, which cuts the number of passes, the least total change of the axis, or the least machining time. Each paper weighs these in its own way, and there is no single standard objective.

## Variants

- **Ball end mill.** The cut shape at the contact does not depend on the axis, so the axis matters only for access, collisions and the cutting speed, which is zero at the tip of the ball.
- **Flat and toroidal end mills, point milling.** The axis decides the shape of the cut. A small lead makes the effective radius large, see Examples.
- **3+2 machining.** The axis is fixed for each region and changes only between regions, so the problem becomes choosing a few directions that cover the part, as in [accessibility](/accessibility-cone/) analysis.
- **[Flank milling](/flank-milling/).** The side of the tool cuts along a line, and the axis follows the rulings of a ruled surface.
- **Multi-point contact.** The axis is chosen so the tool touches the surface at two points, which widens the strip further.
- **Five-axis printing and other processes.** The same orientation questions arise in multi-axis deposition, with the nozzle in place of the tool.

## Examples

**Effective radius of a tilted flat end mill on a plane.** A flat end mill of radius $R = 5$ with lead $\lambda = 10°$ touches a plane with the lowest point of its rim. Seen along the feed, the rim is an ellipse with semi axes 5 and $5\sin 10° = 0.8682$, so the effective radius at the contact is $R/\sin\lambda = 28.79$. The strip in which the gap to the plane is at most $h = 0.01$ has the width
$$
2R\sqrt{1 - (1 - h/(R\sin\lambda))^2} = 1.513,
$$
while a ball end mill of radius 5 cuts a strip $2\sqrt{2 \cdot 5 \cdot 0.01 - 0.01^2} = 0.632$ wide. Smaller leads give wider strips: 2.13 at $5°$ and 2.74 at $3°$. At $20°$ the width is 1.08.

| lead $\lambda$ | 3° | 5° | 10° | 20° | ball, radius 5 |
|---|---|---|---|---|---|
| width for $h = 0.01$ | 2.74 | 2.13 | 1.51 | 1.08 | 0.63 |

On a concave surface the lead cannot be that small, as the ellipse would gouge the sides. The [principal axis method](/principal-axis-method/) gives the smallest safe lead.

**Pole singularity.** On a machine with a tilt axis $A$ and a rotary table $C$, the axis $a = (\sin A\cos C, \sin A\sin C, \cos A)$. A path whose axis moves from 1° on one side of the $C$ axis to 1° on the other, passing 0.1° beside it, changes direction by about 2°. But $C = \operatorname{atan2}(a_y, a_x)$ goes from $174.3°$ to $5.7°$, a turn of $168.6°$. Near the pole, small changes of the axis need large table moves, and planners keep the axis away from it or move the path.

**Steep wall.** In a pocket with a deep, narrow slot, a vertical axis may be the only free direction, and a tilted one hits the wall. The [accessibility cone](/accessibility-cone/) page works through a slot of this kind.

## Known algorithms

- **Fixed lead and tilt.** Keep $\lambda$ and $\omega$ constant along the path. Simple, but it can gouge on concave parts and waste the fit on flat ones.
- **[Principal axis method](/principal-axis-method/).** Tilt in the plane of minimum curvature by the angle that matches the effective radius to the maximum curvature. Exact on cylinders, local elsewhere.
- **Multi-point, rolling ball and arc-intersect methods.** Fit the tool to the surface at two points or along a circle, which also guards against gouges away from the contact.
- **C-space methods.** Map gouges and collisions into the plane of two angles at each contact point, then choose a smooth path of free points. See [collision-free tool orientation](/collision-free-tool-orientation/).
- **Visibility and accessibility.** Compute the [accessibility cone](/accessibility-cone/) by ray tests or on the sphere of directions, then pick axes from it, often for 3+2 setups.
- **Smoothing in joint space.** After a first choice, smooth the rotary angles under the speed and acceleration limits of the machine, and handle the pole by local changes of the path.

## Bounds

The constraints are geometric and depend on the whole part, so the feasible set at a point can be any closed set on the sphere of directions, and the problem has no closed form in general. No hardness result is known to us for the continuous problem. If each point gets a finite set of $k$ candidate directions, and the cost is a sum of a term for each point and a term for each pair of neighbors, the best choice is a shortest path in a layered graph with $m$ layers, which takes $O(m k^2)$ time. The local part has exact answers in special models, such as the tilt of the principal axis method on a cylinder.

## Reductions

- **Collision checks to ray tests.** With the tool as a half-line, a direction is free when the ray from the tool center misses the part, which is [ray casting](/ray-casting/). A thick tool is handled by growing the obstacles by its radius, which is conservative.
- **Feasible directions to C-space.** Each obstacle becomes a region in the plane of two angles, as in [configuration space](/configuration-space/) for robots.
- **Smoothing to shortest paths.** With discrete candidates the smooth choice is a shortest path in a layered graph.
- **Machine moves to time.** The chosen axes and positions feed [feedrate scheduling](/feedrate-scheduling/), where the rotary limits bound the speed.

## Applications

Five-axis tool orientation is part of every five-axis CAM system. It is needed for impellers, blisks and turbine blades, where the tool must reach between blades, for molds and dies with deep cavities, for aircraft structural parts with thin walls, and for finishing large, gently curved surfaces with flat or toroidal end mills, where a good tilt cuts the number of passes by a large factor.

## References
