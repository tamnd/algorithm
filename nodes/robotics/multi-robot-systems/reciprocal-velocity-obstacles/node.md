---
tag: VJAYA8
kind: algorithm
slug: reciprocal-velocity-obstacles
name: Reciprocal velocity obstacles
aliases:
- RVO
area: robotics/multi-robot-systems
level: advanced
summary: Each robot takes half of the avoidance by choosing velocities outside a velocity obstacle whose apex sits at the average of both velocities, which removes the oscillation of plain velocity obstacles.
model: real-ram
complexity:
  vars: {r: the number of robots, s: the number of candidate velocities per robot, k: the number of sensed neighbors per robot}
  time: {per_robot_step: O(s k), per_team_step: O(r s k)}
  space: {extra: O(s + k)}
properties: {deterministic: true, randomized: false, online: true}
history:
  year: 2008
  people: [Jur van den Berg, Ming C. Lin, Dinesh Manocha]
  note: Van den Berg, Lin and Manocha moved the apex of the velocity obstacle to the average of the two velocities, so that two robots that both avoid share the effort and do not oscillate.
prereqs: [velocity-obstacle, multi-robot-system]
see_also: [optimal-reciprocal-collision-avoidance, dynamic-window-approach, potential-field-method, collision-detection, swarm-robotics, synchronous-model]
sources:
  - paper: doi:10.1109/ROBOT.2008.4543489
    title: Jur van den Berg, Ming C. Lin and Dinesh Manocha, Reciprocal velocity obstacles for real-time multi-agent navigation, IEEE International Conference on Robotics and Automation, 2008
    locator: pages 1928 to 1935 (the definition of the reciprocal velocity obstacle, the same side and no oscillation results, and the penalty with sampled velocities)
  - paper: doi:10.1007/978-3-642-19457-3_1
    title: Jur van den Berg, Stephen J. Guy, Ming C. Lin and Dinesh Manocha, Reciprocal n-body collision avoidance, Robotics Research, Springer Tracts in Advanced Robotics 70, 2011
    locator: pages 3 to 19 (the discussion of RVO as the method that ORCA replaces)
---

Reciprocal velocity obstacles (RVO) let many robots avoid each other with no messages and no central planner. A [velocity obstacle](/velocity-obstacle/) is the set of velocities that lead to a collision if the other robot keeps its velocity; when both robots use it, both dodge fully, then both see the way clear and return, and they oscillate. RVO moves the apex of the obstacle to the average of the two velocities, so each robot takes half of the avoidance and a mirrored choice is stable. Unlike [optimal reciprocal collision avoidance](/optimal-reciprocal-collision-avoidance/), which gives each pair a half-plane and a linear program, RVO picks a velocity by a sampled penalty and has no collision guarantee for three or more robots.

## In plain words

Two people walk toward each other in a corridor. If each one steps fully aside, expecting the other to walk straight, both step aside, then both see the path is clear and step back, and they dance. RVO tells each walker: assume the other person will do half of the work, and do only your half. If both do this and both pick the same side, they pass each other cleanly, and no one wants to step back.

Each robot looks at the robots near it and their speeds. It tries many possible new velocities, and for each one it asks how soon it would hit someone if the others also did their half. It picks the velocity that is close to where it wants to go and keeps a collision far away.

## The problem

**The model.** There are $r$ robots in the plane. Each robot is a disc with a radius in meters, a position, a velocity in meters per second, a maximum speed and a *preferred velocity*, which points to its goal. The robots are holonomic: they can take any velocity in their speed disc at once. Each robot senses the positions and velocities of the robots within a sensing range, and the robots send no messages; the sensing graph is the disc graph of this range. Time runs in synchronous steps of length $\Delta t$ seconds: every robot picks its new velocity from the same snapshot, then all robots move.

**Input.** For one robot $A$: its own state and its preferred velocity $v^{pref}_A$, and the states of the sensed robots.

**Output.** A new velocity $v'_A$ for the next step.

**How it differs from close pages.** The [velocity obstacle](/velocity-obstacle/) assumes the other robot does not react, and is right for passive obstacles. RVO assumes the other robot runs the same rule. [Optimal reciprocal collision avoidance](/optimal-reciprocal-collision-avoidance/) keeps the idea of shared effort but replaces the cone by a half-plane per pair and the sampling by a [linear program](/seidel-linear-programming/), and it proves collision avoidance when the program is feasible. The [dynamic window approach](/dynamic-window-approach/) samples velocities under acceleration limits for one robot among static obstacles. The [potential field method](/potential-field-method/) works on positions and has no notion of time to collision.

## The algorithm

For robots $A$ and $B$ with $p = p_B - p_A$ and $R = r_A + r_B$, the collision cone $C$ is the set of relative velocities $w$ for which the ray $t w$, $t > 0$, enters the open disc of radius $R$ around $p$. The velocity obstacle is $VO_{A|B}(v_B) = v_B + C$. The reciprocal velocity obstacle is

$$RVO_{A|B}(v_A, v_B) = \{ v' : 2 v' - v_A \in VO_{A|B}(v_B) \},$$

the velocity obstacle with its apex moved from $v_B$ to $\tfrac12 (v_A + v_B)$. Each robot scores a set of candidate velocities with the penalty of the paper, $\omega / t_c(v') + \lVert v' - v^{pref}_A \rVert$, where $t_c$ is the time to the first collision under the reciprocal assumption and $\omega$ is a weight in meters.

```pseudo id=main
RVO-STEP(robots, dt, omega)
L1  for each robot A, in parallel on the same snapshot, do
L2      for each candidate v' among v_pref, 0 and a polar grid in the speed disc do
L3          tc ← ∞
L4          for each sensed robot B do
L5              w ← 2 v' − v_A − v_B
L6              tc ← min(tc, the first time t > 0 with |p_B − p_A − t w| < r_A + r_B)
L7          penalty(v') ← omega / tc + |v' − v_pref|
L8      v'_A ← the candidate with the smallest penalty (the first one on ties)
L9  every robot sets v_A ← v'_A and moves p_A ← p_A + v_A dt
```

Line L5 is the reciprocal relative velocity: $v' \in RVO_{A|B}$ exactly when $w$ is in the cone. Line L6 solves a quadratic in $t$. A candidate with $t_c = \infty$ has only the distance term, so a free preferred velocity is always kept. A candidate with $t_c = 0$, an overlap now, gets an infinite penalty.

The paper draws random samples. The code uses a fixed polar grid of rings and spokes whose spokes start at the direction of the preferred velocity. Then two robots in mirror image positions get mirror image candidate lists, and they pick mirror image velocities, which is the case the theorems cover.

## Example

Two robots of radius 0.5 m and top speed 1 m/s meet head on: $A$ at $(0, 0)$ m moving at $(1, 0)$ m/s, $B$ at $(4, 0)$ m moving at $(-1, 0)$ m/s, with $\omega = 1$ m and $\Delta t = 0.1$ s. The apex of $RVO_{A|B}$ is $\tfrac12 (v_A + v_B) = 0$, and $v'$ is inside when $2 v'$ points within the half angle $\arcsin(1 / 4) \approx 14.5°$ of the direction to $B$.

The straight velocity $(1, 0)$ is inside, so $A$ turns. The grid with 6 rings and 32 spokes has spokes every $11.25°$; the spoke at $11.25°$ is still inside, and the first free candidate at full speed is at $22.5°$: $v'_A = (\cos 22.5°, \sin 22.5°) \approx (0.924, 0.383)$ m/s. Robot $B$ picks exactly $-v'_A$. The relative velocity $v'_A - v'_B = 2 v'_A$ misses the disc, so the time to collision is infinite. In the simulation of 80 steps, both robots turn to their left, turn back toward their goals as they pass, and end with velocities $(1, 0)$ and $(-1, 0)$ again. The smallest distance between the centers is about 1.007 m, above the 1 m contact distance, and $A$ never swings to the other side (measurement).

With plain velocity obstacles and the same penalty, both robots dodge in step 1, both see the straight path free in step 2 and go straight, and the pattern repeats with period 2 for all 10 steps of the test (measurement). This is the oscillation that RVO removes.

## Correctness

The [proof](proofs/correctness/) shows two theorems for two robots, under the assumptions of holonomic discs, synchronous steps and exact sensing. *Same side*: if each robot picks a velocity outside its own reciprocal velocity obstacle, and both pass on the same side, the robots never collide, because the relative velocity is the average of two vectors in the same closed half-plane outside the cone. *No oscillation*: if the choice is mirrored, $v'_A + v'_B = v_A + v_B$, then in the next step the old velocity is inside the new obstacle and the new velocity stays outside, so neither robot wants to go back. The proof also shows why the code makes mirrored choices in a mirrored scene.

The selection rule itself is a heuristic. It may pick a velocity inside an obstacle if the penalty favors it, and with three or more robots nothing makes every pair choose the same side. So RVO has no collision guarantee for the full method; the tests measure no overlap in a swap of 6 robots of radius 0.4 m on a circle of radius 6 m.

## Complexity

- **Per robot per step (theorem).** $s$ candidates times $k$ sensed robots, each a constant-time quadratic, so $O(s k)$ in the [real RAM](/real-ram/) model. With 6 rings and 32 spokes, $s = 194$.
- **Per team step.** $O(r s k)$, or $O(r^2 s)$ when every robot senses every other. Finding the neighbors with a spatial grid or a k-d tree keeps $k$ small.
- **Messages.** None: each robot uses only what it senses.
- **Memory.** $O(s + k)$ per robot.

## Properties

- **Reciprocal.** Each robot does half of the avoidance; the apex of its obstacle is the average velocity, not the other robot's velocity.
- **No oscillation for mirrored pairs (theorem).** A mirrored choice stays valid in the next step.
- **No collision guarantee in general.** The same side condition is needed (theorem), and the penalty does not enforce it; the tests find over 100 pairs, out of 3000 random ones, where each choice is outside its own obstacle but the opposite sides collide.
- **Reactive and local.** A robot plans only one velocity ahead, so it can be trapped in local minima such as a dead end.
- **Deterministic** with the fixed grid and the tie rule; the paper's random samples make it randomized.

## Variants and improvements

- **Optimal reciprocal collision avoidance.** [ORCA](/optimal-reciprocal-collision-avoidance/) uses one half-plane per neighbor and solves a small linear program, which gives a guarantee and is faster than sampling.
- **Side rules.** Later variants mix the plain and the reciprocal obstacle, or add a fixed bias to one side, so that two robots are less likely to pick opposite sides (heuristic).
- **Finite horizon.** Counting only collisions within $\tau$ seconds makes the obstacle a truncated cone, so far robots do not affect the choice.
- **Static obstacles.** A plain velocity obstacle is used for obstacles that do not react.
- **Non-holonomic robots.** Extensions restrict the candidates to velocities the robot can reach in one step.

## When to use it

Use RVO for crowds of agents in games and crowd simulation, or for many small holonomic robots that sense each other but do not talk. It is simple to write and robust in practice. Use [ORCA](/optimal-reciprocal-collision-avoidance/) when a collision guarantee or more speed is needed, and use a planner for [multi-agent pathfinding](/multi-agent-pathfinding/) when the robots must get through narrow passages.

## Pitfalls

- **Opposite sides.** Two robots that choose opposite sides can still collide. Break symmetry the same way for all robots, for example by measuring sample directions from the preferred velocity, or by a small fixed bias to one side.
- **Mixed populations.** The reciprocal assumption fails when the other agent does not run RVO, such as a person or a static obstacle. Use the plain velocity obstacle for them.
- **Sensing noise.** The obstacle depends on the other robot's velocity, which is estimated. Add a margin to the radii.
- **Time step.** The method assumes the new velocity is reached at once. A large $\Delta t$ or slow acceleration leaves a gap between the plan and the motion.
- **Weight.** A small $\omega$ lets robots come close for a small gain in speed; a large $\omega$ makes them shy. Tune it for the density.

## Implementations

## History

Fiorini and Shiller introduced velocity obstacles for a robot among moving obstacles in 1998. Van den Berg, Lin and Manocha presented reciprocal velocity obstacles at ICRA 2008 and showed it on crowd simulations with many agents. In the follow-up paper on reciprocal n-body collision avoidance, published in 2011, van den Berg, Guy, Lin and Manocha replaced the cones by half-planes and named the result ORCA.

## References
