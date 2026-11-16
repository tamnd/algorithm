---
tag: 0PW0PJ
kind: algorithm
slug: dynamic-window-approach
name: Dynamic window approach
aliases:
- DWA
area: robotics/mobile-and-legged-robots
level: core
summary: "Searches the velocities reachable in the next step, keeps the safe ones, and picks the best by heading, clearance and speed."
model: real-ram
complexity:
  vars: {c: "the number of candidate velocity pairs", k: "the number of obstacles"}
  time: {worst: O(c k)}
  space: {extra: O(c)}
properties: {deterministic: true, randomized: false, online: true, exact: false}
history:
  year: 1997
  people: [Dieter Fox, Wolfram Burgard, Sebastian Thrun]
  note: "Fox, Burgard and Thrun searched the reachable and safe velocities of a synchro-drive robot directly, with a cycle of 0.25 s."
prereqs: [unicycle-model, configuration-space]
see_also: [vector-field-histogram, velocity-obstacle, potential-field-method, pure-pursuit, model-predictive-control, bug-algorithms, reciprocal-velocity-obstacles, nonholonomic-constraint]
sources:
  - paper: doi:10.1109/100.580977
    title: The dynamic window approach to collision avoidance
    locator: "Section 4 (the search space, eq. 14 for the admissible velocities, eq. 15 for the dynamic window, and the objective function)"
---

The dynamic window approach (DWA) is a local collision avoidance method for a mobile robot with limited accelerations. At each control cycle it looks at the pairs of forward speed $v$ and turn rate $\omega$ that the motors can reach before the next cycle (the dynamic window). It keeps the pairs on which the robot can still stop before it hits an obstacle (the admissible pairs). From those, it picks the pair with the best weighted sum of three scores: heading to the goal, clearance and speed. The robot holds that pair for one cycle, and the search starts again. Because each pair is held for a full cycle, the robot of the [unicycle model](/unicycle-model/) moves on a circular arc, and the safety test is a test of circles against obstacles. DWA is a reactive method: it plans only one cycle ahead, so it can stop in front of an obstacle and never reach the goal.

## In plain words

A driver on a dark road cannot turn the wheel instantly, and cannot stop instantly either. So at each moment the driver thinks only about the moves that the car can really make in the next second. Of those moves, the driver drops every one that would leave no room to stop before something in the way. Then the driver picks, among the safe moves, one that points at the destination, stays away from things and keeps a good speed.

DWA does the same, many times each second. It never commits to a long plan. This makes it fast and lets it react to new obstacles, but it can also get stuck in front of an obstacle that lies straight between the robot and the goal.

## The problem

**Input.** The pose $(x, y, \theta)$ and the current velocity $(v_0, \omega_0)$ of a round robot with radius $R$; the speed limits $v \in [0, v_{\max}]$ and $|\omega| \le \omega_{\max}$; the accelerations $a_v$ and $a_\omega$; the cycle $\Delta t$; the goal point; and a set of obstacles. Here the obstacles are discs, and the robot radius is added to each of them, so the robot is a point in the [configuration space](/configuration-space/) of positions. Arithmetic, square roots and trigonometric functions cost one step each, as in the [real RAM](/real-ram/).

**Output.** A velocity $(v, \omega)$ for the next cycle that the accelerations can reach, and that is admissible: if the robot holds it for one cycle and then brakes on the same arc, it stops before it touches an obstacle. Among such pairs, the output should score high on the objective. There is no guarantee that the robot reaches the goal.

**How it differs from close pages.** The [vector field histogram](/vector-field-histogram/) and [potential fields](/potential-field-method/) first choose a direction and then a steering command, so they do not respect the accelerations. [Velocity obstacles](/velocity-obstacle/) also search in velocity space, but for moving obstacles and a holonomic robot. [Pure pursuit](/pure-pursuit/) follows a given path and does not look at obstacles. [Model predictive control](/model-predictive-control/) optimizes a sequence of commands over a horizon; DWA is the special case of one held command, chosen by enumeration.

## The algorithm

```pseudo id=main
DWA(pose, (v0, ω0), goal, obstacles)
L1  window ← [v0 - a_v Δt, v0 + a_v Δt] × [ω0 - a_ω Δt, ω0 + a_ω Δt], clipped to the speed limits
L2  for each (v, ω) in a grid over the window, and the braking pair of (v0, ω0)
L3      dist ← the arc length to the first obstacle on the arc of (v, ω)
L4      if stop(v, ω) > dist then skip this pair
L5      h ← π - |angle to the goal at the stopping point|;  c ← min(dist, D);  s ← v
L6  divide h, c and s by their maxima over the kept pairs
L7  (v*, ω*) ← the kept pair with the largest α h + β c + γ s
L8  hold (v*, ω*) for Δt, then start again at L1 with the new pose and velocity
```

Line L1 is the dynamic window of Fox, Burgard and Thrun (eq. 15). Line L3 intersects the arc of $(v, \omega)$ with each inflated disc. The arc is a circle of radius $v/|\omega|$, or a straight line when $\omega = 0$; a pair with $v = 0$ turns the round robot in place and is always safe.

Line L4 is the safety test. The function stop$(v, \omega)$ is the arc length that the robot covers if it holds $(v, \omega)$ for one cycle and then brakes on the same arc: both speeds drop by the same fraction each cycle, so the ratio $\omega/v$ and the arc stay the same. With $n = \max(1, \lceil\max(v/(a_v\Delta t), |\omega|/(a_\omega\Delta t))\rceil)$ braking cycles, the speeds are $v, v(n-1)/n, \dots, v/n$, and
$$\operatorname{stop}(v, \omega) = \Delta t\,v\,\frac{n + 1}{2}.$$
The paper states the test as $v \le \sqrt{2\,\mathrm{dist}(v, \omega)\,\dot v_b}$ and $\omega \le \sqrt{2\,\mathrm{dist}(v, \omega)\,\dot\omega_b}$ (eq. 14), the stopping distance with braking from the start. The code uses the discrete form because the command is held for a full cycle before braking can start; the Example shows the difference.

Line L2 adds the braking pair $(v_0, \omega_0)(n-1)/n$ of the current velocity to the grid. It is always admissible (Lemma 2 of the proof), so line L7 always has a pair to pick. Line L5 measures the heading at the point where the robot would stop on the arc, as the paper does, so that a fast turn gets credit for the angle it will really turn. The clearance $c$ is capped at $D$ (3 m in the code), because a far obstacle should not matter. The weights of the paper are $\alpha = 2$ and $\beta = \gamma = 0.2$, with a cycle of 0.25 s.

## Example

The robot has $R = 0.3$ m, $v_{\max} = 0.95$ m/s, $\omega_{\max} = 1$ rad/s, $a_v = 0.5$ m/s², $a_\omega = 60$ deg/s² and $\Delta t = 0.25$ s. It is at the origin, faces the goal at $(6, 0)$, and drives straight at $v_0 = 0.75$ m/s. A disc of radius 0.3 m is at $(1.4, 0)$. With the robot radius added, it is a disc of radius 0.6, so the free distance straight ahead is 0.8 m.

The window is $v \in [0.625, 0.875]$ m/s and $|\omega| \le 0.262$ rad/s. On the straight line:

| $v$ (m/s) | braking cycles $n$ | stop$(v, 0)$ (m) | admissible (dist = 0.8 m) |
|---|---|---|---|
| 0.625 | 5 | 0.469 | yes |
| 0.75 | 6 | 0.656 | yes |
| 0.80 | 7 | 0.800 | yes (equal) |
| 0.875 | 7 | 0.875 | no |

The turning arcs in the window miss the disc by little, so their free distance is between 0.80 and 0.84 m, and $v = 0.875$ is not admissible on any of them. The chosen pair is $(0.8, 0)$: it points straight at the goal and is the fastest admissible pair. In the next cycles the robot slows down, turns past the disc and reaches the goal after 40 cycles (10 s, measured).

The continuous test of eq. 14 gives $v \le \sqrt{2 \cdot 0.8 \cdot 0.5} = 0.894$ m/s and accepts $v = 0.875$. But a robot that holds 0.875 m/s for 0.25 s covers 0.219 m, and braking from 0.875 m/s at 0.5 m/s² then needs 0.766 m, which is 0.985 m in total. The discrete test is the one that matches a controller that changes the command only once per cycle.

## Correctness

DWA is a heuristic for reaching the goal and has no guarantee of it: in the test `test_a_disc_on_the_line_is_a_local_minimum`, a disc straight between the robot and the goal stops the robot for good, because every pair that turns away loses more heading score than it gains in clearance. Safety, however, is a theorem. The [proof](proofs/correctness/) shows that if the obstacles are static and known, the motion model is exact, and the robot starts at rest, then every cycle has an admissible pair, and the robot never overlaps an obstacle. The key fact is that the braking pair on the current arc is always admissible: its stopping distance is exactly $v_0\Delta t$ shorter than that of the previous command, and the robot has just moved $v_0\Delta t$ along the same arc. The tests check the exact arc distance against dense sampling, the stopping distance against the braking sequence, and safety and the acceleration limits along every simulated run.

## Complexity

- **Time.** Each of the $c$ candidate pairs is tested against each of the $k$ obstacles in $O(1)$, so a cycle costs $O(ck)$. Measured: with an $11 \times 21$ grid plus the braking pair (232 pairs) and 14 discs, one cycle takes about 1.7 ms in this pure Python code. With an occupancy grid instead of discs, the cost of line L3 depends on the number of cells near the arc.
- **Space.** $O(c)$ for the scores of the kept pairs, needed for the normalization of line L6.

## Properties

- **Safe by construction.** Under the assumptions of the proof, the robot never enters an obstacle and always has an admissible command. The test `test_brakes_in_front_of_a_wall` puts a wall across the path; the robot stops in front of it.
- **Respects the accelerations.** Every command is inside the window, so the motors can follow it.
- **Not complete.** It can stop in a local minimum, or circle, and never reach a goal that a global planner would reach.
- **Sensitive to the weights.** Measured on 10 random fields of 14 discs with the goal 10 m away and 300 cycles: the weights $(2, 0.2, 0.2)$ reached the goal in 1 field, and the weights $(1, 1, 0.3)$ reached it in 9 fields. No run collided. These numbers describe this code, with its clearance cap and normalization, not the robot of the paper.
- **Online.** Each cycle uses only the current pose, velocity and obstacles.

## Variants and improvements

- **Global dynamic window.** Brock and Khatib replaced the heading term with a navigation function computed over a map, which removes most local minima.
- **Trajectory rollout.** Planners in the ROS navigation stack simulate each candidate pair over a horizon of a few seconds and score the rollout against a global path and a cost map.
- **Curvature-velocity method.** Simmons chose $(v, \omega)$ by a similar weighted objective with constraints from the obstacles, published a year earlier.
- **Holonomic and car-like robots.** The window gets a third dimension for sideways speed, or the curvature replaces $\omega$ for a [car-like robot](/nonholonomic-constraint/).
- **Moving obstacles.** Predicting each obstacle along its own velocity, as in [velocity obstacles](/velocity-obstacle/), replaces the static distance of line L3.

## When to use it

Use DWA as the local planner of a mobile robot with real acceleration limits, under a global planner that gives it a nearby goal or a path to follow. It is cheap, easy to tune and safe with respect to the obstacles it sees. Do not use it alone in a cluttered space with dead ends, for a fast car-like robot that needs plans of many seconds, or among many moving people, where a predictive method does better.

## Pitfalls

- **Local minima.** A wall or a U-shaped obstacle between the robot and the goal can stop the robot for good. Give DWA a global path, or replace the heading term with a navigation function.
- **The stopping test.** Eq. 14 assumes braking starts at once. If the command is held for a cycle first, the test must include that cycle, as in the Example.
- **Coarse grids.** A grid that is too coarse can miss a narrow gap, and the braking pair must stay in the candidate set, or the robot can find no admissible pair after a sudden obstacle.
- **The robot shape.** Inflating obstacles by a radius is exact only for a round robot. For other shapes, check the swept area of the arc.
- **Unnormalized scores.** Without line L6, the term with the largest units dominates, and the weights lose their meaning.

## Implementations

## History

Fox, Burgard and Thrun published the dynamic window approach in 1997. Their robot had a synchro drive and sonar sensors, used a cycle of 0.25 s, accelerations of 50 cm/s² and 60 deg/s², and reached speeds up to 95 cm/s. Simmons had proposed the curvature-velocity method, which also searches over $(v, \omega)$, in 1996. Brock and Khatib added a navigation function in 1999 to escape local minima. Later local planners in the ROS navigation stack used the same search over sampled velocities.

## References
