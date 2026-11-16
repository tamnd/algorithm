---
tag: D7S5SH
kind: algorithm
slug: optimal-reciprocal-collision-avoidance
name: Optimal reciprocal collision avoidance
aliases:
- ORCA
area: robotics/multi-robot-systems
level: advanced
summary: Each robot turns every neighbor into one half-plane of allowed velocities, takes half of the needed change, and solves a small linear program for the velocity closest to its goal.
model: real-ram
complexity:
  vars: {r: the number of robots, k: the number of sensed neighbors per robot}
  time: {per_robot_step: O(k^2), expected_with_random_order: O(k), per_team_step: O(r k^2)}
  space: {extra: O(k)}
properties: {deterministic: true, randomized: false, online: true}
history:
  year: 2011
  people: [Jur van den Berg, Stephen J. Guy, Ming C. Lin, Dinesh Manocha]
  note: Van den Berg, Guy, Lin and Manocha replaced the cone of reciprocal velocity obstacles by one half-plane per pair and a 2D linear program, and proved that robots do not collide when every program is feasible.
prereqs: [velocity-obstacle, reciprocal-velocity-obstacles, seidel-linear-programming, convex-set]
see_also: [supporting-hyperplane-theorem, minkowski-sum, linear-programming-problem, dynamic-window-approach, swarm-robotics, multi-robot-system]
sources:
  - paper: doi:10.1007/978-3-642-19457-3_1
    title: Jur van den Berg, Stephen J. Guy, Ming C. Lin and Dinesh Manocha, Reciprocal n-body collision avoidance, Robotics Research (ISRR 2009), Springer Tracts in Advanced Robotics 70, 2011
    locator: pages 3 to 19 (the truncated velocity obstacle, the ORCA half-plane, the linear programs and the guarantee)
  - paper: doi:10.1109/ROBOT.2008.4543489
    title: Jur van den Berg, Ming C. Lin and Dinesh Manocha, Reciprocal velocity obstacles for real-time multi-agent navigation, IEEE International Conference on Robotics and Automation, 2008
    locator: pages 1928 to 1935 (the reciprocal idea that ORCA builds on)
---

Optimal reciprocal collision avoidance (ORCA) gives each robot a set of safe velocities that is an intersection of half-planes, one for each neighbor, and picks the safe velocity closest to the one it wants. Each half-plane asks the robot to make half of the smallest velocity change that avoids a collision within a time horizon $\tau$, trusting the neighbor to make the other half. Unlike [reciprocal velocity obstacles](/reciprocal-velocity-obstacles/), which score sampled velocities against cones and have no guarantee, ORCA solves a 2D [linear program](/seidel-linear-programming/) and proves that no two robots collide when every program is feasible. Unlike the plain [velocity obstacle](/velocity-obstacle/), it assumes the other robots react.

## In plain words

Two robots are about to bump into each other. Each robot works out the smallest change in speed and direction that would make the pair miss, and then makes just half of it, because it knows the other robot will make the other half. This gives each robot a straight line in the space of velocities: on one side the velocities are safe, on the other they are not.

A robot with many neighbors gets one such line per neighbor. It then looks for the velocity on the safe side of all lines that is closest to the velocity it wants. If the lines leave no room, it picks the velocity that breaks the lines the least. No messages are needed, because each robot sees the others and both robots of a pair compute the same line.

## The problem

**The model.** There are $r$ robots in the plane. Each robot is a disc with a radius in meters, a position, a velocity in meters per second, a top speed and a preferred velocity toward its goal. The robots are holonomic and reach a new velocity at once. Each robot senses the positions and velocities of the robots within a sensing range, and sends no messages; the sensing graph is the disc graph of that range. Time runs in synchronous steps of $\Delta t$ seconds: every robot computes its new velocity from the same snapshot, then all robots move. The horizon $\tau$, in seconds, says how far ahead collisions count.

**Input.** For one robot $A$: its state, its preferred velocity, the states of its sensed neighbors, $\tau$ and $\Delta t$.

**Output.** A new velocity for $A$, and a flag that tells whether the linear program was feasible.

**How it differs from close pages.** The [velocity obstacle](/velocity-obstacle/) treats the other robot as passive, so two robots that both use it oscillate. [Reciprocal velocity obstacles](/reciprocal-velocity-obstacles/) share the avoidance, but keep the non-convex cone, so they need sampling and can fail when two robots pick opposite sides. ORCA keeps only one half-plane per pair; the half-planes of the two robots fit together by construction, which removes the side problem and turns the choice into a linear program solved by [Seidel's method](/seidel-linear-programming/). The [dynamic window approach](/dynamic-window-approach/) handles one robot with acceleration limits among static obstacles.

## The algorithm

For robots $A$ and $B$, with $p = p_B - p_A$ and $R = r_A + r_B$, the truncated velocity obstacle $VO^\tau_{A|B}$ is the set of relative velocities $w$ for which the discs overlap at some time in $(0, \tau]$. It is a cone with its tip cut off by a circle of center $p / \tau$ and radius $R / \tau$, and it is open and convex. Let $u$ be the vector from the relative velocity $v_A - v_B$ to the nearest point of the boundary of $VO^\tau_{A|B}$, and let $n$ be the outward normal there.

```pseudo id=main
ORCA-STEP(robots, tau, dt)
L1  for each robot A, in parallel on the same snapshot, do
L2      N ← the robots that A senses
L3      for each B in N do build the half-plane ORCA_A|B:
L4          u ← the nearest boundary point of VO^tau_A|B minus (v_A − v_B);  n ← the outward normal there
L5          ORCA_A|B ← { v : (v − (v_A + u / 2)) · n ≥ 0 }
L6      v_new ← the v closest to v_pref with |v| ≤ v_max inside every ORCA_A|B, by an incremental 2D LP:
L7          for each half-plane, in order: if the current optimum is outside it then
L8              solve the 1D problem on its boundary line, cut by the speed disc and the earlier half-planes
L9      if some 1D problem is empty then
L10         v_new ← the v with |v| ≤ v_max that minimizes the largest distance to a violated half-plane (a 3D LP)
L11     return v_new and whether the LP was feasible
L12 every robot sets its new velocity and moves p ← p + v dt
```

Line L4 tests whether the nearest boundary point lies on the cut-off circle or on one of the two legs, and projects onto that part. Line L5 puts the boundary through $v_A + \frac12 u$: robot $A$ makes half of the change $u$, and robot $B$ computes the mirror half-plane with $-u$ and $-n$. If two robots already overlap, the code uses $\Delta t$ in place of $\tau$, so that they push apart within one step. Lines L6 to L8 are the incremental method of the linear programming page: when a new half-plane cuts off the current optimum, the new optimum lies on its boundary line, where the problem is one interval. Line L10 is the fallback for crowded scenes.

The code follows the structure of the RVO2 library of the authors. It takes the current velocity as the reference velocity $v^{opt}$ of the paper, which is the common choice.

## Example

Two robots of radius 0.5 m and top speed 1 m/s meet head on: $A$ at $(0, 0)$ m with velocity $(1, 0)$ m/s, and $B$ at $(4, 0)$ m with velocity $(-1, 0)$ m/s. They would touch at $t = 1.5$ s.

**Horizon $\tau = 2$ s.** The relative velocity $(2, 0)$ is inside $VO^2_{A|B}$. The tip of the truncated cone is at $p / \tau = (2, 0)$, so the relative velocity sits on it, and the nearest boundary point is on the right leg. The half-plane of $A$ passes through $(15/16, -\sqrt{15}/16) \approx (0.9375, -0.2421)$ m/s with direction $(-\sqrt{15}/4, 1/4)$. The closest permitted velocity to $(1, 0)$ is that point itself, so $A$ takes $v'_A \approx (0.9375, -0.2421)$ m/s and $B$ takes $-v'_A$. The change is $u / 2$ with $\lVert u \rVert = 0.5$ m/s. With the new velocities the centers come exactly 1.0 m apart, the contact distance, and do not overlap.

**Horizon $\tau = 1$ s.** The collision at 1.5 s is beyond the horizon. The half-plane passes through $(1.5, 0)$ and allows $v_x \le 1.5$ m/s, so $A$ keeps $(1, 0)$. The robots will react in a later step, when the collision is closer.

**A crowd.** Eight robots of radius 0.4 m on a circle of radius 6 m swap to the opposite points with $\tau = 2$ s and $\Delta t = 0.1$ s. With a small random change of at most 0.01 m/s on each preferred velocity, every linear program was feasible, no discs overlapped, and all robots arrived (measurement: 513 to 1369 steps over four seeds, closest distance 0.8 m, the contact distance). Without the random change, the exactly symmetric circle stopped in a deadlock with the robots about 1.31 m from the center.

## Correctness

The [proof](proofs/correctness/) shows that $VO^\tau_{A|B}$ is open and convex, and that the half-planes of $A$ and $B$ are mirror images with the same $u$. The main theorem: if $v'_A \in ORCA^\tau_{A|B}$ and $v'_B \in ORCA^\tau_{B|A}$, then $v'_A - v'_B$ lies in a closed half-plane that misses the obstacle, by the [supporting hyperplane theorem](/supporting-hyperplane-theorem/), so the robots do not overlap within $\tau$. So when every robot's program is feasible and every robot senses the robots it could meet within $\tau$, no two robots collide in the next $\tau$ seconds. It also proves that the incremental solver returns the closest permitted velocity, and that the fallback minimizes the largest violation. When the fallback runs, there is no guarantee, and there is no liveness theorem: symmetric scenes can deadlock.

## Complexity

- **One linear program (theorem).** With $k$ half-planes, the incremental method in the given order costs $O(k^2)$ in the worst case; with a random order of the half-planes it costs $O(k)$ expected, as in [Seidel's algorithm](/seidel-linear-programming/). The code keeps the given order, as RVO2 does.
- **Fallback.** The 3D program runs one 2D program per violated half-plane, $O(k^3)$ in the worst case in the given order. It is rare in sparse scenes.
- **Per team step.** $O(r k^2)$ in the [real RAM](/real-ram/) model, plus the neighbor search. A k-d tree or a grid keeps $k$ bounded by the density.
- **Messages.** None.
- **Memory.** $O(k)$ per robot for the half-planes.

## Properties

- **Collision-free when feasible (theorem).** For holonomic discs, synchronous steps, exact sensing and exact arithmetic.
- **Optimal in the local sense.** The velocity is the closest permitted one to the preferred velocity, which is what "optimal" in the name means; it says nothing about the travel time.
- **No liveness (theorem by example).** Robots can stop for ever in symmetric scenes.
- **Cheap.** One small 2D linear program per robot and step, with no sampling.
- **Deterministic.** The same input gives the same output; the random change of the preferred velocity is outside the method.

## Variants and improvements

- **Static obstacles.** Line segments become half-planes too, without the factor $\frac12$, because they do not react; RVO2 handles them first so that they are never violated.
- **Non-holonomic robots.** Extensions bound the tracking error of a car-like or differential-drive robot and enlarge the radius by it.
- **Acceleration limits.** Extensions add velocity constraints from the acceleration limits.
- **Three dimensions.** The same construction in 3D gives half-spaces and a 3D linear program, used for aerial robots.
- **Unequal shares.** The proof of the pair theorem works for any shares $\alpha u$ and $(1 - \alpha) u$ that add up to $u$, so a robot that carries a load can take less of the change.

## When to use it

Use ORCA for many holonomic robots or simulated agents that sense each other and must move without collisions in open space: crowd simulation, drone swarms, warehouse robots in open areas. It is fast and has a clear guarantee when feasible. Add a global planner for the route, because ORCA is local and can get stuck behind obstacles. Use a planner for [multi-agent pathfinding](/multi-agent-pathfinding/) in narrow corridors, where ORCA tends to deadlock.

## Pitfalls

- **Symmetry deadlocks.** Exactly symmetric scenes can stop. Add a small random change to the preferred velocities.
- **Horizon choice.** A short $\tau$ makes robots react late with large changes; a long $\tau$ makes them shy and slow in crowds.
- **Non-reacting agents.** People and static obstacles do not take their half. Treat them without the factor $\frac12$.
- **Sensing range.** The guarantee needs every robot that can be met within $\tau$ in the neighbor list. The range must be at least $2 v_{max} \tau$ plus the radii.
- **Dynamics.** A robot that cannot reach the new velocity at once breaks the assumption. Enlarge the radius or use a dynamics-aware variant.

## Implementations

## History

Fiorini and Shiller introduced velocity obstacles in 1998. Van den Berg, Lin and Manocha added reciprocity in 2008. Van den Berg, Guy, Lin and Manocha presented reciprocal n-body collision avoidance at the International Symposium of Robotics Research in 2009, published in 2011, with the half-plane construction, the linear programs and the guarantee. The authors released the RVO2 library, which follows that paper.

## References
