---
tag: 2DNNAR
kind: concept
slug: velocity-obstacle
name: Velocity obstacle
aliases:
- collision cone
area: robotics/mobile-and-legged-robots
level: core
summary: "The set of robot velocities that lead to a collision with a moving obstacle within some time, if both keep their velocities."
prereqs: [configuration-space, minkowski-sum]
see_also: [reciprocal-velocity-obstacles, optimal-reciprocal-collision-avoidance, dynamic-window-approach, vector-field-histogram, kinodynamic-planning, collision-detection, potential-field-method, seidel-linear-programming]
sources:
  - paper: doi:10.1177/027836499801700706
    title: "Paolo Fiorini and Zvi Shiller, Motion planning in dynamic environments using velocity obstacles"
    locator: "The International Journal of Robotics Research 17(7), pp. 760-772, the whole paper (the collision cone, the velocity obstacle as the cone shifted by the obstacle velocity, the reachable avoidance velocities, and the avoidance maneuvers)"
---

A velocity obstacle is the set of velocities of a robot that would make it collide with a moving obstacle at some future time, if the robot and the obstacle both keep a constant velocity. For two discs, it is a cone in the plane of the robot's velocities, with its apex at the obstacle's velocity and its axis toward the obstacle. Any velocity outside the cone keeps the robot clear of that obstacle for all time; any velocity inside it leads to a contact. With many obstacles, the robot takes the union of the cones and picks a velocity outside all of them that it can reach in the next control cycle, often the one closest to the velocity it would like to have. Paolo Fiorini and Zvi Shiller introduced the idea for planning in dynamic environments in 1998. It is the basis of the [reciprocal velocity obstacle](/reciprocal-velocity-obstacles/) and [ORCA](/optimal-reciprocal-collision-avoidance/) methods for groups of robots and crowds.

## In plain words

You walk across a station hall and someone walks toward you. If you both keep your speed and direction, will you bump into each other? That depends on your speed and direction. Some choices lead to a bump; the others do not. The choices that lead to a bump form a wedge: aim inside it and you collide, aim outside it and you pass.

A robot draws one such wedge for each moving thing around it. Then it picks a speed and direction outside all the wedges, as close as it can to where it wants to go. It does this again many times each second, because people change their speed and direction.

## The idea

**Relative motion.** Let robot $A$ be a disc of radius $r_A$ at $p_A$ with velocity $v_A$, and let obstacle $B$ be a disc of radius $r_B$ at $p_B$ with velocity $v_B$. Seen from $B$, the robot moves with the relative velocity $v_A - v_B$. In the [configuration space](/configuration-space/) of $A$'s center, $B$ grows to the disc of radius $r = r_A + r_B$ about $p_B$; for other shapes, it grows to the [Minkowski sum](/minkowski-sum/) $B \oplus (-A)$.

**Collision cone.** The collision cone is the set of relative velocities whose ray from $p_A$ meets the grown obstacle:

$$CC = \{\, u : p_A + t u \in D(p_B, r) \text{ for some } t \ge 0 \,\}.$$

If $d = |p_B - p_A| > r$, this is a closed cone with its apex at the origin, its axis along $p_B - p_A$, and the half-angle $\alpha = \arcsin(r/d)$.

**Velocity obstacle.** The velocity obstacle is the collision cone shifted by the obstacle's velocity:

$$VO_{A|B} = \{\, v_A : v_A - v_B \in CC \,\} = CC \oplus \{v_B\}.$$

The name "collision cone" is sometimes used for this shifted set too; strictly, the collision cone lives in relative velocities and the velocity obstacle in the robot's own velocities.

**Facts that follow from the definition (theorem).**

- If $v_A \notin VO_{A|B}$ and both velocities stay constant, then $A$ and $B$ never touch.
- If $v_A \in VO_{A|B}$, they touch at some time $t \ge 0$.
- For several obstacles, the velocities that avoid all of them are the complement of the union $\bigcup_j VO_{A|B_j}$.

Both statements hold only under the constant-velocity assumption. When an obstacle turns or speeds up, the cone is out of date, and the robot must recompute it at every cycle.

**Time horizon.** A collision far in the future is not a threat yet. The truncated velocity obstacle keeps only the collisions within a time $\tau$:

$$VO^\tau_{A|B} = \{\, v_A : |p_A + t(v_A - v_B) - p_B| \le r \text{ for some } t \in [0, \tau] \,\}.$$

In relative velocities it is the union of the discs $D((p_B - p_A)/t,\ r/t)$ for $t \in (0, \tau]$: the cone with its tip near the apex cut off by the disc $D((p_B - p_A)/\tau,\ r/\tau)$.

**Choosing a velocity.** The robot can reach only some velocities in one cycle, because of its acceleration limits. Fiorini and Shiller call the reachable velocities outside the union of the velocity obstacles the reachable avoidance velocities. A common rule picks, among them, the velocity closest to a preferred velocity that points to the goal, as the [dynamic window approach](/dynamic-window-approach/) does with its own score. If the set is empty, no constant velocity is safe for the horizon, and the robot picks the velocity with the latest collision, or stops.

## Examples

**One disc that comes head on.** Robot $A$ is at the origin with $r_A = 0.5$, and obstacle $B$ is at $(5, 0)$ with $r_B = 0.5$ and $v_B = (-1, 0)$. So $r = 1$, $d = 5$, and the half-angle is $\alpha = \arcsin(0.2) \approx 11.54°$. The axis of the cone points along $+x$.

| $v_A$ | $v_A - v_B$ | Angle to the axis | In $VO$? | First contact |
|---|---|---|---|---|
| $(1, 0)$ | $(2, 0)$ | $0°$ | yes | $t = 2$ |
| $(1, 0.4)$ | $(2, 0.4)$ | $11.31°$ | yes | $t \approx 2.31$ |
| $(1, 0.5)$ | $(2, 0.5)$ | $14.04°$ | no | never |

For $v_A = (1, 0.4)$, the closest approach of the relative ray to $p_B$ is $|5 \cdot 0.4|/\sqrt{4.16} \approx 0.981 < 1$, and the first contact solves $4.16 t^2 - 20 t + 24 = 0$, which gives $t = 19.2/8.32 \approx 2.31$. For $v_A = (1, 0.5)$, the closest approach is $2.5/\sqrt{4.25} \approx 1.213 > 1$. With a horizon of $\tau = 2$, the velocity $(1, 0.4)$ is outside $VO^\tau$: the contact would come at 2.31 s, later than the horizon. The velocity $(1, 0)$ is on the boundary of $VO^\tau$, with contact at exactly $t = 2$.

**Two robots that both avoid.** If both $A$ and $B$ use velocity obstacles and treat each other as passive, each moves fully out of the other's cone. At the next cycle, each sees that the old velocity is now safe again and turns back, and they oscillate. The [reciprocal velocity obstacle](/reciprocal-velocity-obstacles/) fixes this by letting each robot take half of the avoidance.

## Where it is used

- **Mobile robots among moving obstacles.** Reactive collision avoidance with people, vehicles or other robots, as a local layer under a global planner.
- **Multi-robot systems and crowds.** [Reciprocal velocity obstacles](/reciprocal-velocity-obstacles/) and [ORCA](/optimal-reciprocal-collision-avoidance/), which replaces each cone by a half-plane and picks the velocity by a small linear program, as in [Seidel's algorithm](/seidel-linear-programming/). Crowd simulation in games and films uses them for thousands of agents.
- **Ships and aircraft.** Collision avoidance at sea and in the air, where the vehicles move at almost constant velocity for long times, so the assumption fits well.
- **Kinodynamic planning.** As a fast test inside [kinodynamic planners](/kinodynamic-planning/) that must check many velocities against moving obstacles.

## References
