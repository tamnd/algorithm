---
tag: 1RDEDT
kind: problem
slug: peg-in-hole
name: Peg-in-hole insertion
aliases:
- peg-in-hole problem
area: robotics/grasping-and-manipulation
level: core
summary: "Insert a peg into a tight hole despite position errors, the classic test of compliant assembly."
prereqs: [friction-cone, wrench]
see_also: [impedance-control, admittance-control, hybrid-position-force-control, manipulation-planning, configuration-space, motion-planning, quasi-static-pushing, task-and-motion-planning]
sources:
  - paper: doi:10.1115/1.3149634
    title: Daniel E. Whitney, Quasi-static assembly of compliantly supported rigid parts, Journal of Dynamic Systems, Measurement, and Control 104(1), 1982
    locator: pages 65 to 77 (two-point contact, jamming, wedging and the jamming diagram)
  - paper: doi:10.1177/027836498400300101
    title: Tomas Lozano-Perez, Matthew T. Mason and Russell H. Taylor, Automatic synthesis of fine-motion strategies for robots, International Journal of Robotics Research 3(1), 1984
    locator: pages 3 to 24 (preimages and compliant motion strategies under uncertainty)
  - paper: doi:10.1109/SFCS.1987.42
    title: John Canny and John Reif, New lower bound techniques for robot motion planning problems, 28th Annual Symposium on Foundations of Computer Science, 1987
    locator: pages 49 to 60 (compliant motion planning with uncertainty in control is NEXPTIME-hard)
  - paper: doi:10.1109/TSMC.1981.4308708
    title: Matthew T. Mason, Compliance and force control for computer controlled manipulators, IEEE Transactions on Systems, Man, and Cybernetics 11(6), 1981
    locator: pages 418 to 432
  - book: isbn:9781107156302
    title: Kevin M. Lynch and Frank C. Park, Modern Robotics, Mechanics, Planning, and Control, Cambridge University Press, 2017
    locator: Chapter 11, Sections 11.6 and 11.7 (hybrid motion-force control and impedance control)
---

Peg-in-hole insertion is the problem of pushing a rigid peg into a hole whose clearance is smaller than the position error of the robot. A cylindrical peg of diameter $d$ must enter a hole of diameter $D$, with the clearance ratio $c = (D - d)/D$ often below 0.01, while the robot knows the hole position only to within a millimeter or so. Pure position control then fails, because the peg hits the chamfer or the hole edge and the contact forces become large. A solution must use contact: a passive compliance, a force feedback law, or a planned sequence of motions that slide along surfaces and are guaranteed to end in the hole. The problem is the standard benchmark of compliant assembly, and Whitney's 1982 analysis of jamming and wedging is its classical theory.

## In plain words

You try to put a pin into a hole that is barely larger than the pin, and you cannot see exactly where the hole is. If you push hard in the wrong place, something breaks. So you let the pin touch the edge, feel the forces, and let them guide the pin into the hole.

Once the pin is partly inside, two new failures can happen. The pin can jam: it touches the hole at two points, and with the force you apply, friction stops it. Or it can wedge: it is tilted so much that friction at the two contacts holds it by itself, whatever you do. Good strategies keep the tilt small and push in the right direction.

## Definition

**Input.** The geometry of the peg and the hole (diameters $d < D$, chamfers, depth), a bound $\epsilon$ on the error of the initial pose of the peg relative to the hole, a coefficient of friction $\mu$ at the contacts, and a model of the robot: what it can command (positions, a [wrench](/wrench/), or an impedance) and what it can sense (pose, force).

**Question.** Find a strategy, that is a sequence of commanded motions or a feedback law, that brings the peg from any start within the error bound to the fully inserted pose, without contact forces above a given limit and without jamming or wedging.

**Quasi-static two-dimensional model.** In Whitney's model the peg is rigid, the motion is slow so that inertia is ignored, and contact obeys Coulomb friction. In two-point contact, the peg touches one wall of the hole with the side of its tip and the other wall at the hole entrance, at depth $l$, with tilt $\theta \approx cD/l$. Let the $x$ axis point toward the side to which the top of the peg leans, let $F_x$ and $F_z$ be the applied force, with $F_z > 0$ into the hole, and let $M$ be the applied moment about the peg tip, positive when it increases the tilt. With $r = d/2$ and the normal forces $N_1$ at the entrance and $N_2$ at the tip, force and moment balance give

$$N_1 = \frac{M - \mu r F_x}{l}, \qquad N_2 = N_1 - F_x,$$

and the peg can still slide in only if $F_z > \mu(N_1 + N_2)$. With $u = F_x/F_z$, $m = M/(rF_z)$ and $\lambda = l/(2\mu r)$, the peg slides in two-point contact when

$$m - \mu(1 + \lambda)u < \lambda,$$

and in one-point contact, where only the normal force $|F_x|$ acts, when $|u| < 1/\mu$. The same bounds with $m$ and $u$ negated hold for the other direction of tilt. Outside these bounds the peg jams. The conventions and the form of these bounds are written for this page; Whitney's paper draws them as a parallelogram in the $(u, m)$ plane, the jamming diagram.

**Wedging.** In two-point contact, the contact forces can balance each other along the line between the two contacts when this line lies inside both [friction cones](/friction-cone/). The line rises by $l$ over a horizontal distance of about $d$, so this can happen only if $l \le \mu d$, that is $\lambda \le 1$. Since $l \approx cD/\theta_0$ at the first two-point contact, wedging cannot happen if the initial tilt satisfies $\theta_0 < c/\mu$.

## Variants

- **Chamfered or unchamfered holes.** A chamfer turns a lateral position error into a sliding motion toward the hole, so it enlarges the set of starts that succeed.
- **Round peg in a round hole in 3D.** The peg has five degrees of freedom that matter, and contact can occur at points on a circle; the 2D analysis applies in the plane of the tilt.
- **Prismatic pegs.** Square or rectangular pegs need the orientation about the axis to match, which adds a rotation search.
- **Multiple pegs and connectors.** Electrical connectors and multi-pin parts have several holes at once, with tighter tolerances.
- **Planning formulation.** With bounded control and sensing errors, find a sequence of commanded velocities, each ending in a recognizable state, that is guaranteed to reach the goal: the preimage problem of Lozano-Perez, Mason and Taylor.
- **Learning formulation.** Learn an insertion policy from trials, often with a force sensor and a camera, and measure the success rate on new parts.

## Examples

- **Jamming threshold.** A peg of radius $r = 10$ mm with $\mu = 0.3$ is in two-point contact at depth $l = 3$ mm, so $\lambda = 3/(2 \cdot 0.3 \cdot 10) = 0.5$. With a pure push $F_z = 10$ N and $F_x = 0$, it jams once the moment that increases the tilt reaches $M = \lambda r F_z = 50$ N mm. A side force of $-2$ N, which pushes against the lean, lowers the threshold to $M = 41$ N mm, and $+2$ N raises it to $59$ N mm.
- **Wedging bound.** With $D = 20$ mm, a clearance of 0.2 mm ($c = 0.01$) and $\mu = 0.3$, wedging cannot happen if the tilt at the first two-point contact is below $c/\mu = 0.033$ rad, about 1.9 degrees. At $l = 3$ mm the tilt is about $0.2/3 = 0.067$ rad, and $\lambda = 0.5 \le 1$, so wedging is possible there.
- **Position control only.** If the hole is 0.5 mm off and the gripper is stiff, the peg lands on the edge of the hole and the force rises with the stiffness of the robot until a limit stops it; the insertion fails.

## Known algorithms

- **Remote center compliance (RCC).** A passive wrist, developed at the Charles Stark Draper Laboratory, whose center of compliance lies near the peg tip. A lateral force then shifts the peg without tilting it, and a moment tilts it without shifting it, which keeps $m$ and $u$ inside the jamming bounds. It needs no sensing and no computation.
- **Impedance and admittance control.** Make the robot behave like a spring and damper in the lateral and rotational directions with [impedance control](/impedance-control/) or [admittance control](/admittance-control/), so that contact forces push the peg into alignment, as the RCC does passively.
- **Hybrid force/position control.** Control the force along the hole axis and the lateral forces and moments to zero, with motion only along the axis, using [hybrid position/force control](/hybrid-position-force-control/).
- **Search strategies.** Press the peg on the surface and move it along a spiral or a raster until the force drops or the position falls, which shows that the tip is over the hole; then tilt and insert.
- **Preimage backchaining.** Plan backward from the goal through preimages, the sets of starts from which one commanded compliant motion is guaranteed to reach a recognizable subgoal (Lozano-Perez, Mason and Taylor 1984).
- **Learning.** Reinforcement learning and learning from demonstration produce insertion policies from force and vision data; they are judged by measured success rates, not by guarantees.

## Bounds

- **Planning with uncertainty is intractable in general.** Canny and Reif proved that deciding whether a sequence of commanded velocities is guaranteed to move a point among polyhedral obstacles in 3D to a goal, when the actual motion may differ from the command and slide on obstacles, is NEXPTIME-hard.
- **Mechanical bounds.** In the quasi-static model above, the success region in the $(u, m)$ plane depends on the depth only through $\lambda = l/(2\mu r)$, and it grows with $\lambda$. So jamming is most likely early in the insertion, and wedging is possible only while $l \le 2\mu r$.

## Reductions

- **To compliant motion planning.** Peg-in-hole with sliding contacts and bounded errors is a case of motion planning in the [configuration space](/configuration-space/) of the peg, where the hole walls are obstacles that the peg may touch and slide on. The Canny and Reif lower bound is for this general class, not for the peg-in-hole geometry alone.
- **To force control.** Once the peg is in two-point contact, the remaining task is a force regulation problem: keep $(u, m)$ inside the jamming bounds while pushing along the axis.

## Applications

Assembly of shafts into bearings, pins into holes, connectors into sockets, and parts into fixtures in manufacturing, and the same contact problems appear in docking, in surgery (inserting a needle or an instrument through a port) and in the benchmarks of robot learning, where peg insertion is a standard task.

## References
