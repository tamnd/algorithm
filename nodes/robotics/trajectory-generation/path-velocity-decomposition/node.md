---
tag: B2GWFF
kind: technique
slug: path-velocity-decomposition
name: Path-velocity decomposition
aliases:
- Kant-Zucker decomposition
area: robotics/trajectory-generation
level: advanced
summary: "Plans a path among static obstacles first and then a velocity profile along it that avoids moving obstacles, in a path-time plane."
history:
  year: 1986
  people: [Kamal Kant, Steven W. Zucker]
  note: "Kant and Zucker split trajectory planning among moving obstacles into a path planning problem among the static obstacles and a velocity planning problem along the chosen path, solved in the plane of path position and time."
prereqs: [motion-planning, time-scaling]
see_also: [coupled-and-decoupled-planning, prioritized-multi-robot-planning, time-optimal-path-parameterization, kinodynamic-planning, visibility-graph, dijkstra, multi-agent-pathfinding, trajectory-generation-problem]
sources:
  - paper: doi:10.1177/027836498600500304
    title: "Kamal Kant and Steven W. Zucker, Toward efficient trajectory planning, the path-velocity decomposition, The International Journal of Robotics Research 5(3), 1986, 72-89"
    locator: "the whole paper (the path planning problem, the velocity planning problem, and the path-time space with forbidden regions)"
  - book: isbn:9780521862059
    title: "Steven M. LaValle, Planning Algorithms, Cambridge University Press, 2006"
    locator: "Section 7.1.3 (the velocity-tuning method among moving obstacles, and why it is not complete)"
---

Path-velocity decomposition is a way to plan the motion of a robot among obstacles that move, such as people, vehicles or other robots. Planning in the full space of configuration and time at once is expensive, so the technique splits the problem in two. First it plans a geometric path that avoids the static obstacles and ignores the moving ones. Then it fixes that path and plans only how fast to move along it, so that the robot is never at the same place as a moving obstacle at the same time. The second step is a search in a plane: one axis is the position $s$ along the path, the other is time $t$, and each moving obstacle becomes a forbidden region where it blocks the path. A motion is a curve in that plane that goes forward in time, does not go backward along the path, and respects the speed limit. Kant and Zucker (1986) introduced the split. It makes the problem much smaller, but it can miss solutions that need a different path, so it is a heuristic in that sense: LaValle calls the method incomplete. The timing step is a [time scaling](/time-scaling/) with obstacles added.

## In plain words

You must cross a room to the door while people walk around. A simple way to do it: first pick a route around the furniture, as if the people were not there. Then walk that route and only choose your speed: slow down or wait to let someone pass, and speed up when the way is clear. You never change the route, only the timing. That is far easier than thinking about every possible route at every moment. The catch is that some situations need a new route. If someone stops and stands in the doorway of your route, waiting does not help, even if another door is open.

## When it applies

- The robot has a **fixed path** that can be found without the moving obstacles, and changing the speed along it is cheap and safe.
- The **moving obstacles have known motions**, at least over the planning horizon, or predictions that the planner treats as known.
- The **static part dominates** the geometry: the moving obstacles block the path only now and then, so waiting or hurrying usually works.
- The robot can **stop and wait** on the path, or at least slow down. A system that must keep moving, such as a fixed-wing aircraft, leaves fewer options.

It does not apply, or loses much, when the moving obstacles block the path for a long time, when the best motion requires leaving the path, or when the robot cannot slow down enough.

## The template

```pseudo id=main
PATH-VELOCITY(start, goal, static obstacles, moving obstacles, speed limit V)
L1  θ ← a free path from start to goal among the static obstacles, θ : [0, L] → C by arc length
L2  for each moving obstacle O: F_O ← {(s, t) : the robot at θ(s) meets O at time t}
L3  F ← the union of all F_O                       ▷ forbidden regions in the (s, t) plane
L4  find a curve s(t) from (0, 0) to (L, T) with 0 ≤ ds/dt ≤ V that avoids F, with T as small as possible
L5  if no such curve exists then report failure        ▷ the path of L1 does not work
L6  return the trajectory θ(s(t))
```

L1 can use any planner, such as a [visibility graph](/visibility-graph/) in the plane or a sampling-based planner in higher dimensions. L2 maps each moving obstacle into the path-time plane. L4 is the heart of the method. If the forbidden regions are polygons and only the speed is bounded, it is a shortest-time path problem in a plane among polygons with a slope constraint, which can be solved with a graph on the corners of the regions or on a grid with [Dijkstra's algorithm](/dijkstra/). With an acceleration limit, the state of L4 must include $\dot s$, and the search is in $(s, \dot s, t)$.

**Why L4 is cheaper than the full problem.** For a robot with $n$ degrees of freedom, the full problem lives in a space of dimension $n + 1$ (configuration and time). The decomposition solves one problem of dimension $n$ without time in L1 and one problem of dimension 2 in L4.

**Why it can fail.** L5 is reached when the path of L1 is blocked for good, even though another path would work. The method is not complete: a solution of the original problem may exist and the method may not find it (LaValle, Section 7.1.3).

## Classic examples

**A robot and one crossing obstacle.** The path of L1 is 10 m long and the speed is at most 2 m/s, so alone the robot needs 5 s. A moving obstacle crosses the path and occupies $s \in [4, 6]$ during $t \in [2, 4]$. Passing before it would need the robot past $s = 6$ by $t = 2$, a speed of 3 m/s, which is too fast. So the robot must not be inside $[4, 6]$ before $t = 4$. The fastest curve in L4 drives at 2 m/s to $s = 4$, arriving at $t = 2$, waits there until $t = 4$, and then drives the last 6 m in 3 s: $T = 7$ s. No curve is faster, because the robot is at most at $s = 4$ at $t = 4$ and then needs at least $6/2 = 3$ s more. Other curves reach the same time: any curve that stays at or below $s = 4$ until $t = 4$ and then drives at full speed, for example a constant 1 m/s for the first 4 s.

**The same scene where the decomposition fails.** Now the obstacle stops at $t = 2$ and stays on $s \in [4, 6]$ for good, while the free space has room to go around it. L4 finds no curve, and L5 reports failure, although a robot that leaves the path would reach the goal. This is the incompleteness of the method.

**Multi-robot coordination.** In [prioritized multi-robot planning](/prioritized-multi-robot-planning/), the robots plan one at a time, and each treats the robots planned before as moving obstacles with known motions. Keeping each robot on its own path and choosing only the timing is the path-velocity decomposition applied robot by robot; it is one of the decoupled methods of [coupled and decoupled planning](/coupled-and-decoupled-planning/), with the same loss of completeness.

**Timing along a path under dynamic limits.** With no moving obstacles, L4 only has to respect the limits of the robot, and the problem becomes [time-optimal path parameterization](/time-optimal-path-parameterization/), or [feedrate scheduling](/feedrate-scheduling/) for machine tools. These problems use the same split between the path and its timing.

## Variations

- **Several candidate paths.** Run L1 to L5 on several paths, for example from a roadmap, and keep the best result. This recovers some cases where one path fails.
- **Acceleration limits.** Add $\dot s$ to the state of L4 and search in $(s, \dot s, t)$; this is a small [kinodynamic](/kinodynamic-planning/) problem.
- **Path-time obstacles with uncertainty.** Grow each forbidden region by a margin that increases with the prediction time.
- **Replanning.** Repeat L2 to L4 every cycle with new predictions of the moving obstacles, keeping the path of L1.
- **Coordination diagrams.** For two robots on fixed paths, the plane of $(s_1, s_2)$ plays the role of the path-time plane, and a monotone curve in it avoids collisions between them.

## Pitfalls

- **Treating the method as complete.** It is not. If L5 reports failure, a solution may still exist; plan another path or use a full space-time planner.
- **Forgetting the robot's size.** The forbidden region must include every $(s, t)$ where the robot body, not a point, overlaps the obstacle. Grow the obstacles or use the robot shape in L2.
- **Ignoring acceleration.** A curve in L4 with sudden speed changes is not feasible for a robot with an acceleration limit; waiting and then starting at full speed, as in the first example, needs an acceleration phase.
- **Bad path choice.** A path through a busy corridor can be short and still slow, because of waiting. The cost of L1 does not see the moving obstacles.
- **Monotone time, monotone path.** Curves in L4 must go forward in time; most implementations also forbid moving backward along the path. Allowing it can help but enlarges the search.

## References
